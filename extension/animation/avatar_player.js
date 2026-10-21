/**
 * SignBridge — Milestone M3 Phase 3.4: Three.js Avatar Player Prototype
 *
 * Implements:
 * 1. WebGL 3D scene setup (Three.js perspective camera, lighting, WebGLRenderer).
 * 2. Skinned humanoid rig loading from local Adobe Mixamo Y-Bot GLB.
 * 3. 67-joint bone mapping with automatic canonical name normalization.
 * 4. Application of NEUTRAL_REST_POSE to physical rig bones.
 * 5. Procedural playback of TECHNICAL_TEST_CLIP using keyframe interpolation.
 * 6. Playback state machine: play, pause, resume, restart, stop, and safe neutral fallback.
 * 7. Graceful error handling for missing models, missing bones, and un-animated glosses.
 * 8. Telemetry and inspectable bone transforms on actual loaded model nodes.
 *
 * CRITICAL GOVERNANCE & PROVENANCE DISCLAIMER:
 * - Procedural motions played in this module are SYNTHETIC TECHNICAL TESTS,
 *   NOT validated linguistic ISL signs.
 * - Current motions are explicitly labeled: "Synthetic technical test — NOT a validated ISL sign".
 */

(function (root, factory) {
  if (typeof module === 'object' && typeof module.exports === 'object') {
    const THREE = require('../lib/three.min.js');
    const KeyframeRegistry = require('./keyframe_registry.js');
    module.exports = factory(THREE, KeyframeRegistry);
  } else if (typeof define === 'function' && define.amd) {
    define(['../lib/three.min.js', './keyframe_registry.js'], factory);
  } else {
    root.SignBridgeAvatarPlayer = factory(
      root.THREE || (typeof globalThis !== 'undefined' ? globalThis.THREE : null),
      root.SignBridgeKeyframeRegistry || (typeof globalThis !== 'undefined' ? globalThis.SignBridgeKeyframeRegistry : null)
    );
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function (THREE, KeyframeRegistry) {
  'use strict';

  // Fallback defaults
  const DEFAULT_MODEL_PATH = '../assets/models/ybot.glb';
  const TECHNICAL_TEST_NOTICE = 'Synthetic technical test — NOT a validated ISL sign';
  const NEUTRAL_REST_NOTICE = 'Neutral rest pose — avatar relaxed at sides';

  class AvatarPlayerError extends Error {
    constructor(message, code = 'PLAYER_ERROR', details = null) {
      super(message);
      this.name = 'AvatarPlayerError';
      this.code = code;
      this.details = details;
    }
  }

  class AvatarPlayer {
    /**
     * Creates an AvatarPlayer instance.
     *
     * @param {HTMLElement} container - DOM element to mount the canvas.
     * @param {Object} [options] - Configuration options.
     */
    constructor(container, options = {}) {
      if (!container && !options.headless) {
        throw new AvatarPlayerError('Container element is required for AvatarPlayer', 'MISSING_CONTAINER');
      }

      this.container = container;
      this.options = Object.assign({
        modelUrl: DEFAULT_MODEL_PATH,
        width: container ? (container.clientWidth || 320) : 320,
        height: container ? (container.clientHeight || 400) : 400,
        backgroundColor: 0x0f172a,
        cameraPosition: [0, 1.30, 1.65],
        cameraTarget: [0, 1.20, 0],
        fov: 46,
        autoPlayNeutral: true,
        onLoad: null,
        onError: null,
        onStateChange: null,
        keyframeRegistry: KeyframeRegistry || (typeof window !== 'undefined' ? window.SignBridgeKeyframeRegistry : null)
      }, options);

      this.keyframeRegistry = this.options.keyframeRegistry;
      if (!this.keyframeRegistry) {
        throw new AvatarPlayerError('KeyframeRegistry dependency is required', 'MISSING_DEPENDENCY');
      }

      // Three.js instances
      this.scene = null;
      this.camera = null;
      this.renderer = null;
      this.clock = null;
      this.animFrameId = null;

      // Model & Rig data
      this.model = null;
      this.skinnedMesh = null;
      this.bones = new Map(); // canonicalName -> THREE.Bone
      this.initialRotations = new Map(); // canonicalName -> THREE.Euler or Quaternion
      this.missingBonesEncountered = new Set();

      // State machine
      this.isLoaded = false;
      this.isLoading = false;
      this.loadError = null;
      this.isPlaying = false;
      this.isPaused = false;
      this.currentTimeMs = 0;
      this.currentClip = null;
      this.currentPoseId = null;
      this.loop = false;
      this.isDisposed = false;

      // Contracts dependency
      this.contracts = (this.options && this.options.contracts) || (typeof window !== 'undefined' ? window.SignBridgeContracts : null);

      // Sequence playback state
      this.activeSequence = null;
      this.sequenceSigns = [];
      this.sequenceSignIndex = 0;
      this.sequencePlaybackState = 'IDLE'; // 'IDLE' | 'PLAYING' | 'HELD_NEUTRAL' | 'PAUSED' | 'COMPLETED' | 'INTERRUPTED'
      this.currentSignIsFallback = false;
      this.currentSignGloss = null;
      this.currentSignNotice = null;
      this.currentSignElapsedMs = 0;
      this.currentSignDurationMs = 0;
      this.lastInterruptedSequenceId = null;
      this.lastCompletedClip = null;
      this.lastCompletedGloss = null;
      this.lastCompletedDurationMs = 0;
      this.sequenceHadEligibleAnimation = false;

      // Initialize Three.js scene
      this._initScene();

      // Trigger model loading if URL provided
      if (this.options.modelUrl) {
        this.loadModel(this.options.modelUrl);
      }
    }

    /**
     * Initializes Three.js scene, camera, lights, and renderer.
     * @private
     */
    _initScene() {
      if (!THREE) {
        throw new AvatarPlayerError('THREE is not available on window or scope', 'MISSING_THREE');
      }

      this.scene = new THREE.Scene();
      this.clock = new THREE.Clock();

      // Camera positioned to view upper torso, head, and hands
      const aspect = this.options.width / this.options.height;
      this.camera = new THREE.PerspectiveCamera(this.options.fov, aspect, 0.1, 100);
      const [cx, cy, cz] = this.options.cameraPosition;
      this.camera.position.set(cx, cy, cz);
      const [tx, ty, tz] = this.options.cameraTarget;
      this.camera.lookAt(tx, ty, tz);

      // Lights: Bright ambient + frontal key + fill
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
      this.scene.add(ambientLight);

      const frontLight = new THREE.DirectionalLight(0xffffff, 1.0);
      frontLight.position.set(0, 1.5, 2.5);
      this.scene.add(frontLight);

      const fillLight = new THREE.DirectionalLight(0x93c5fd, 0.5);
      fillLight.position.set(-1.5, 1.0, 1.0);
      this.scene.add(fillLight);

      // WebGL Renderer
      try {
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(this.options.width, this.options.height);
        this.renderer.setPixelRatio(typeof window !== 'undefined' && window.devicePixelRatio ? window.devicePixelRatio : 1);
        this.renderer.setClearColor(this.options.backgroundColor, 1);

        if (this.container) {
          const prevCanvas = this.container.querySelector('canvas#signbridge-avatar-canvas');
          if (prevCanvas) {
            this.container.removeChild(prevCanvas);
          }
          this.container.appendChild(this.renderer.domElement);
          this.renderer.domElement.id = 'signbridge-avatar-canvas';
          this.renderer.domElement.style.display = 'block';
          this.renderer.domElement.style.width = '100%';
          this.renderer.domElement.style.height = '100%';
        }
      } catch (err) {
        this.loadError = new AvatarPlayerError(`WebGL initialization failed: ${err.message}`, 'WEBGL_INIT_FAILED', err);
        if (typeof this.options.onError === 'function') {
          this.options.onError(this.loadError);
        }
      }

      // Start render loop
      this._startRenderLoop();
    }

    /**
     * Loads the avatar GLB/GLTF model.
     *
     * @param {string} url - Model path or URL.
     * @returns {Promise<AvatarPlayer>}
     */
    loadModel(url) {
      this.isLoading = true;
      this.loadError = null;

      return new Promise((resolve, reject) => {
        if (!THREE.GLTFLoader) {
          const err = new AvatarPlayerError('THREE.GLTFLoader is not available. Please ensure GLTFLoader.js is loaded.', 'MISSING_GLTF_LOADER');
          this.loadError = err;
          this.isLoading = false;
          if (typeof this.options.onError === 'function') this.options.onError(err);
          return reject(err);
        }

        const loader = new THREE.GLTFLoader();
        loader.load(
          url,
          (gltf) => {
            if (this.isDisposed) return;
            try {
              this.model = gltf.scene || gltf.scenes[0];
              this._setupModelRig(this.model);

              this.scene.add(this.model);
              this.isLoaded = true;
              this.isLoading = false;

              // Apply neutral rest pose by default
              if (this.options.autoPlayNeutral) {
                this.resetToNeutralPose();
              }

              if (typeof this.options.onLoad === 'function') {
                this.options.onLoad(this);
              }
              this._notifyStateChange();
              resolve(this);
            } catch (setupErr) {
              this.loadError = new AvatarPlayerError(`Rig setup failed: ${setupErr.message}`, 'RIG_SETUP_FAILED', setupErr);
              this.isLoading = false;
              if (typeof this.options.onError === 'function') this.options.onError(this.loadError);
              reject(this.loadError);
            }
          },
          undefined,
          (err) => {
            this.isLoading = false;
            this.loadError = new AvatarPlayerError(`Failed to load 3D model from '${url}': ${err.message || 'Network/Parse error'}`, 'MODEL_LOAD_FAILED', err);
            if (typeof this.options.onError === 'function') {
              this.options.onError(this.loadError);
            }
            this._notifyStateChange();
            reject(this.loadError);
          }
        );
      });
    }

    /**
     * Traverses the loaded hierarchy to map canonical joints and store bind transforms.
     * @private
     */
    _setupModelRig(rootNode) {
      this.bones.clear();
      this.initialRotations.clear();
      this.missingBonesEncountered.clear();

      rootNode.traverse((node) => {
        // SkinnedMesh vertices are deformed by bone matrices in GPU shaders.
        // Three.js CPU frustum culling evaluates static bounding spheres transformed
        // by root node matrices (which for Mixamo rigs include root scaling and rotation),
        // causing the un-skinned static bounding sphere to fall outside the camera FOV
        // and mistakenly culling the mesh. Setting frustumCulled = false ensures reliable rendering.
        if (node.isSkinnedMesh || node.isMesh) {
          node.frustumCulled = false;
        }

        if (node.isSkinnedMesh) {
          this.skinnedMesh = node;
        }

        if (node.isBone) {
          const canonicalName = this.keyframeRegistry.normalizeBoneName(node.name);
          if (this.keyframeRegistry.isValidRigBone(canonicalName)) {
            this.bones.set(canonicalName, node);
            this.initialRotations.set(canonicalName, node.quaternion.clone());
          }
        }
      });

      if (this.bones.size === 0) {
        throw new Error('No valid skeletal bones found in model. Expected 67-joint humanoid rig.');
      }
    }

    /**
     * Applies a validated Pose or Keyframe transform set to the physical model bones.
     *
     * @param {Object} pose - Object containing a `transforms` array of BoneTransform items.
     * @returns {{ appliedCount: number, missingCount: number, errors: string[] }}
     */
    applyPose(pose) {
      if (!this.isLoaded || !this.model) {
        return { appliedCount: 0, missingCount: 0, errors: ['Model is not loaded'] };
      }

      if (!pose || !Array.isArray(pose.transforms)) {
        return { appliedCount: 0, missingCount: 0, errors: ['Invalid pose: missing transforms array'] };
      }

      let appliedCount = 0;
      let missingCount = 0;
      const errors = [];

      for (const t of pose.transforms) {
        if (!t || typeof t.bone !== 'string') continue;

        const canonical = this.keyframeRegistry.normalizeBoneName(t.bone);
        const boneNode = this.bones.get(canonical);

        if (!boneNode) {
          this.missingBonesEncountered.add(t.bone);
          missingCount++;
          continue;
        }

        // Apply rotation
        const rotType = t.rotationType || (Array.isArray(t.rotation) && t.rotation.length === 4 ? 'quaternion' : 'euler');
        if (rotType === 'quaternion' && Array.isArray(t.rotation) && t.rotation.length === 4) {
          boneNode.quaternion.set(t.rotation[0], t.rotation[1], t.rotation[2], t.rotation[3]);
          appliedCount++;
        } else if (rotType === 'euler' && Array.isArray(t.rotation) && t.rotation.length === 3) {
          boneNode.rotation.set(t.rotation[0], t.rotation[1], t.rotation[2], 'XYZ');
          appliedCount++;
        } else {
          errors.push(`Bone '${t.bone}': unsupported rotation format`);
        }

        // Apply optional translational position
        if (Array.isArray(t.position) && t.position.length === 3) {
          boneNode.position.set(t.position[0], t.position[1], t.position[2]);
        }
      }

      if (typeof pose.poseId === 'string') {
        this.currentPoseId = pose.poseId;
      }

      this.render();
      return { appliedCount, missingCount, errors };
    }

    /**
     * Resets the avatar to the canonical Neutral Rest Pose.
     *
     * @returns {boolean}
     */
    resetToNeutralPose() {
      const neutralPose = this.keyframeRegistry.NEUTRAL_REST_POSE;
      const res = this.applyPose(neutralPose);

      this.isPlaying = false;
      this.isPaused = false;
      this.currentTimeMs = 0;
      this.currentClip = null;
      this.currentPoseId = neutralPose.poseId;
      this.lastCompletedClip = null;
      this.lastCompletedGloss = null;
      this.lastCompletedDurationMs = 0;
      this.sequenceHadEligibleAnimation = false;
      this.sequencePlaybackState = 'IDLE';

      this._notifyStateChange();
      return res.appliedCount > 0;
    }

    /**
     * Starts playing a validated SignAnimationClip.
     *
     * @param {Object} clip - SignAnimationClip object.
     * @param {Object} [options] - Options (e.g. `loop`).
     * @returns {{ success: boolean, clipId?: string, isLinguisticISL?: boolean, errors?: string[] }}
     */
    playClip(clip, options = {}) {
      if (!clip) {
        console.warn('AvatarPlayer: Cannot play null clip. Safely falling back to Neutral Rest Pose.');
        this.resetToNeutralPose();
        return { success: false, errors: ['Clip is null or undefined; defaulted to neutral pose'] };
      }

      const val = this.keyframeRegistry.validateAnimationClip(clip);
      if (!val.valid) {
        console.warn('AvatarPlayer: Invalid animation clip. Safely falling back to Neutral Rest Pose.', val.errors);
        this.resetToNeutralPose();
        return { success: false, errors: val.errors };
      }

      this.currentClip = clip;
      this.currentTimeMs = 0;
      this.isPlaying = true;
      this.isPaused = false;
      this.loop = !!options.loop;

      // Evaluate t = 0 immediately
      const initialEval = this.keyframeRegistry.evaluateClipAtTime(this.currentClip, 0);
      this.applyPose(initialEval);

      this._notifyStateChange();
      return {
        success: true,
        clipId: clip.animationId,
        isLinguisticISL: clip.isLinguisticISL
      };
    }

    /**
     * Plays a clip resolved from a SignItem contract via KeyframeRegistry.
     * If the sign has no registered animation, falls back safely to Neutral Rest Pose.
     *
     * @param {Object} signItem - SignItem contract object.
     * @returns {{ resolved: boolean, animationId?: string, isLinguisticISL: boolean, notice: string }}
     */
    playSignItem(signItem) {
      const resolution = this.keyframeRegistry.resolveSignAnimation(signItem);
      if (resolution.resolved && resolution.clip) {
        this.playClip(resolution.clip);
        return {
          resolved: true,
          animationId: resolution.animationId,
          isLinguisticISL: resolution.isLinguisticISL,
          notice: resolution.isLinguisticISL ? 'Verified linguistic sign' : TECHNICAL_TEST_NOTICE
        };
      }

      // Safe Unresolved Fallback
      this.resetToNeutralPose();
      return {
        resolved: false,
        animationId: null,
        isLinguisticISL: false,
        notice: `No 3D clip exists for gloss '${signItem ? signItem.gloss : 'UNKNOWN'}'; avatar held in neutral rest pose`
      };
    }

    /**
     * Plays a validated SignSequence contract sequentially on the avatar.
     * Unregistered/unknown signs trigger safe neutral rest pose fallback for their duration.
     * If a new sequence arrives during playback, gracefully interrupts and plays the new one.
     *
     * @param {Object} sequence - Validated SignSequence object.
     * @param {Object} [options] - Sequence options.
     * @returns {{ success: boolean, sequenceId: string, signsCount: number, status: string }}
     */
    playSignSequence(sequence, options = {}) {
      if (!sequence || typeof sequence !== 'object') {
        throw new AvatarPlayerError('SignSequence must be a non-null object', 'INVALID_SEQUENCE');
      }

      // Validate sequence if contracts validator is available
      if (this.contracts && typeof this.contracts.validateSignSequence === 'function') {
        const val = this.contracts.validateSignSequence(sequence);
        if (!val.valid) {
          throw new AvatarPlayerError(`Invalid SignSequence contract: ${val.errors.join('; ')}`, 'INVALID_SEQUENCE');
        }
      }

      // Graceful interruption of in-flight sequence
      if (this.activeSequence && this.isPlaying) {
        this.lastInterruptedSequenceId = this.activeSequence.sequenceId;
        this.sequencePlaybackState = 'INTERRUPTED';
      }

      this.activeSequence = sequence;
      this.sequenceSigns = Array.isArray(sequence.signs) ? sequence.signs : [];
      this.sequenceSignIndex = 0;
      this.currentSignElapsedMs = 0;
      this.sequenceHadEligibleAnimation = false;
      this.lastCompletedClip = null;
      this.lastCompletedGloss = null;
      this.lastCompletedDurationMs = 0;

      // Handle empty sequence (e.g. silence or empty transcript) safely
      if (this.sequenceSigns.length === 0) {
        this.resetToNeutralPose();
        this.currentSignGloss = null;
        this.currentSignIsFallback = false;
        this.currentSignNotice = sequence.unsupportedWords && sequence.unsupportedWords.length > 0
          ? `All words unsupported (${sequence.unsupportedWords.length}); held in neutral rest pose`
          : 'Empty sequence; held in neutral rest pose';
        this.sequencePlaybackState = 'COMPLETED';
        this.isPlaying = false;
        this._notifyStateChange();
        return {
          success: true,
          sequenceId: sequence.sequenceId,
          signsCount: 0,
          status: 'EMPTY_SEQUENCE'
        };
      }

      this.isPlaying = true;
      this.isPaused = false;
      this._playCurrentSequenceSign();

      return {
        success: true,
        sequenceId: sequence.sequenceId,
        signsCount: this.sequenceSigns.length,
        status: 'PLAYING'
      };
    }

    /**
     * Resolves and initiates playback of the current sign item in active sequence.
     * @private
     */
    _playCurrentSequenceSign() {
      if (!this.activeSequence || this.sequenceSignIndex >= this.sequenceSigns.length) {
        // Sequence completed - smoothly return avatar to neutral rest pose
        const neutralPose = this.keyframeRegistry.NEUTRAL_REST_POSE;
        this.applyPose(neutralPose);
        this.currentPoseId = neutralPose.poseId;

        if (this.currentClip) {
          this.lastCompletedClip = this.currentClip;
          this.lastCompletedDurationMs = this.currentClip.durationMs;
          this.currentTimeMs = this.currentClip.durationMs;
        }

        if (this.sequenceHadEligibleAnimation && this.lastCompletedClip) {
          this.lastCompletedGloss = this.lastCompletedClip.gloss;
          this.lastCompletedDurationMs = this.lastCompletedClip.durationMs;
          this.currentTimeMs = this.lastCompletedClip.durationMs;
        } else {
          this.lastCompletedClip = null;
          this.lastCompletedGloss = null;
          this.lastCompletedDurationMs = 0;
          this.currentTimeMs = 0;
        }

        this.currentClip = null;
        this.currentSignGloss = null;
        this.sequencePlaybackState = 'COMPLETED';
        this.isPlaying = false;
        this.isPaused = false;
        this.currentSignIsFallback = false;
        this.currentSignNotice = 'Sequence playback complete — returned to neutral rest pose';
        this._notifyStateChange();
        return;
      }

      const signItem = this.sequenceSigns[this.sequenceSignIndex];
      this.currentSignGloss = signItem.gloss;
      this.currentSignDurationMs = typeof signItem.durationMs === 'number' ? signItem.durationMs : 750;
      this.currentSignElapsedMs = 0;

      const resolution = this.keyframeRegistry.resolveSignAnimation(signItem);

      if (resolution.resolved && resolution.clip) {
        // Registered 3D animation clip found
        this.sequenceHadEligibleAnimation = true;
        this.lastCompletedClip = resolution.clip;
        this.lastCompletedGloss = resolution.clip.gloss;
        this.lastCompletedDurationMs = resolution.clip.durationMs;
        this.currentSignIsFallback = false;
        this.sequencePlaybackState = 'PLAYING';
        this.currentSignNotice = resolution.isLinguisticISL
          ? 'Verified linguistic sign'
          : TECHNICAL_TEST_NOTICE;
        this.playClip(resolution.clip, { loop: false });
      } else {
        // Safe Neutral Rest Pose Fallback for un-animated or unknown glosses
        this.currentSignIsFallback = true;
        this.currentSignNotice = signItem.source === 'seed_dictionary'
          ? `Dictionary gloss '${signItem.gloss}' awaiting qualified 3D review — held in neutral rest pose`
          : `Unknown gloss '${signItem.gloss}' — held in neutral rest pose (no fabricated signing)`;
        const neutralPose = this.keyframeRegistry.NEUTRAL_REST_POSE;
        this.applyPose(neutralPose);
        this.currentPoseId = neutralPose.poseId;
        this.currentClip = null;
        this.sequencePlaybackState = 'HELD_NEUTRAL';
        this.isPlaying = true; // Active in sequence timeline
        this._notifyStateChange();
      }
    }

    /**
     * Advances to the next sign in the active sequence.
     * @private
     */
    _advanceSequenceSign() {
      this.sequenceSignIndex++;
      this._playCurrentSequenceSign();
    }

    /**
     * Pauses animation playback at current timestamp.
     */
    pause() {
      if (this.isPlaying && !this.isPaused) {
        this.isPlaying = false;
        this.isPaused = true;
        if (this.activeSequence) {
          this.sequencePlaybackState = 'PAUSED';
        }
        this._notifyStateChange();
      }
    }

    /**
     * Resumes playback from paused timestamp.
     */
    resume() {
      if (this.isPaused) {
        this.isPaused = false;
        this.isPlaying = true;
        if (this.activeSequence) {
          this.sequencePlaybackState = this.currentSignIsFallback ? 'HELD_NEUTRAL' : 'PLAYING';
        }
        this._notifyStateChange();
      }
    }

    /**
     * Restarts current clip or sequence playback from t = 0.
     */
    restart() {
      if (this.activeSequence && this.sequenceSigns.length > 0) {
        this.sequenceSignIndex = 0;
        this.currentSignElapsedMs = 0;
        this.isPlaying = true;
        this.isPaused = false;
        this._playCurrentSequenceSign();
        return;
      }

      if (this.currentClip) {
        this.currentTimeMs = 0;
        this.isPlaying = true;
        this.isPaused = false;
        const initialEval = this.keyframeRegistry.evaluateClipAtTime(this.currentClip, 0);
        this.applyPose(initialEval);
        this._notifyStateChange();
      } else {
        this.resetToNeutralPose();
      }
    }

    /**
     * Stops current animation and returns avatar to neutral rest pose.
     */
    stop() {
      this.activeSequence = null;
      this.sequenceSigns = [];
      this.sequenceSignIndex = 0;
      this.sequencePlaybackState = 'IDLE';
      this.currentSignGloss = null;
      this.currentSignIsFallback = false;
      this.sequenceHadEligibleAnimation = false;
      this.lastCompletedClip = null;
      this.lastCompletedGloss = null;
      this.lastCompletedDurationMs = 0;
      this.resetToNeutralPose();
    }

    /**
     * Updates timeline interpolation and skeletal transforms by elapsed milliseconds.
     *
     * @param {number} deltaMs - Elapsed time in milliseconds.
     */
    update(deltaMs) {
      if (!this.isPlaying || this.isPaused) {
        return;
      }

      // Sequence timeline update
      if (this.activeSequence && this.sequenceSigns.length > 0) {
        if (this.currentSignIsFallback) {
          this.currentSignElapsedMs += deltaMs;
          if (this.currentSignElapsedMs >= this.currentSignDurationMs) {
            this._advanceSequenceSign();
          }
          return;
        }

        if (this.currentClip) {
          this.currentTimeMs += deltaMs;
          const clipDuration = this.currentClip.durationMs || 1000;
          if (this.currentTimeMs >= clipDuration) {
            this._advanceSequenceSign();
            return;
          }
          const evalResult = this.keyframeRegistry.evaluateClipAtTime(this.currentClip, this.currentTimeMs);
          this.applyPose(evalResult);
        }
        return;
      }

      // Standalone clip playback
      if (this.currentClip) {
        this.currentTimeMs += deltaMs;

        if (this.currentTimeMs >= this.currentClip.durationMs) {
          if (this.loop) {
            this.currentTimeMs = this.currentTimeMs % this.currentClip.durationMs;
          } else {
            this.currentTimeMs = this.currentClip.durationMs;
            this.isPlaying = false;
          }
        }

        const evalResult = this.keyframeRegistry.evaluateClipAtTime(this.currentClip, this.currentTimeMs);
        this.applyPose(evalResult);

        if (!this.isPlaying) {
          this._notifyStateChange();
        }
      }
    }

    /**
     * Starts internal requestAnimationFrame render loop.
     * @private
     */
    _startRenderLoop() {
      if (typeof window === 'undefined' || typeof requestAnimationFrame === 'undefined') {
        return; // Headless / node environment without animation loop
      }

      this.renderCount = 0;
      this.lastRenderError = null;

      const render = () => {
        if (this.isDisposed) return;
        this.animFrameId = requestAnimationFrame(render);

        try {
          const deltaSeconds = this.clock ? this.clock.getDelta() : 0.016;
          const deltaMs = deltaSeconds * 1000;

          this.update(deltaMs);

          if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
            this.renderCount = (this.renderCount || 0) + 1;
          }
        } catch (renderErr) {
          this.lastRenderError = renderErr;
          console.error('[SignBridge] Render error:', renderErr);
        }
      };
      this.animFrameId = requestAnimationFrame(render);
    }

    /**
     * Dispatches state change notifications to registered listeners.
     * @private
     */
    _notifyStateChange() {
      if (typeof this.options.onStateChange === 'function') {
        try {
          this.options.onStateChange(this.getStatus());
        } catch (e) {
          console.error('AvatarPlayer: onStateChange handler error', e);
        }
      }
    }

    /**
     * Returns a snapshot of player status and governance telemetry.
     *
     * @returns {Object}
     */
    /**
     * Returns a snapshot of player status and governance telemetry.
     *
     * @returns {Object}
     */
    getStatus() {
      const isTechTest = this.currentClip && !this.currentClip.isLinguisticISL;
      let labelNotice = NEUTRAL_REST_NOTICE;
      if (this.activeSequence) {
        if (this.currentSignIsFallback) {
          labelNotice = this.currentSignNotice || 'Unknown gloss fallback (Neutral Rest Pose)';
        } else if (this.currentClip) {
          labelNotice = this.currentClip.isLinguisticISL
            ? 'Verified linguistic ISL sign'
            : TECHNICAL_TEST_NOTICE;
        } else if (this.sequencePlaybackState === 'COMPLETED' && this.lastCompletedClip) {
          labelNotice = this.lastCompletedClip.isLinguisticISL
            ? 'Verified linguistic ISL sign'
            : TECHNICAL_TEST_NOTICE;
        } else {
          labelNotice = this.currentSignNotice || NEUTRAL_REST_NOTICE;
        }
      } else if (this.currentClip) {
        labelNotice = this.currentClip.isLinguisticISL
          ? 'Verified linguistic ISL sign'
          : TECHNICAL_TEST_NOTICE;
      }

      const activeDuration = this.currentClip
        ? this.currentClip.durationMs
        : (this.currentSignIsFallback
            ? this.currentSignDurationMs
            : (this.sequencePlaybackState === 'COMPLETED' && this.lastCompletedClip ? (this.lastCompletedDurationMs || 0) : 0));

      const activeClipId = this.currentClip
        ? this.currentClip.animationId
        : (this.sequencePlaybackState === 'COMPLETED' && this.lastCompletedClip ? this.lastCompletedClip.animationId : null);

      const activeLinguistic = this.currentClip
        ? !!this.currentClip.isLinguisticISL
        : (this.sequencePlaybackState === 'COMPLETED' && this.lastCompletedClip ? !!this.lastCompletedClip.isLinguisticISL : false);

      const activeTime = this.currentClip
        ? Math.round(this.currentTimeMs)
        : (this.currentSignIsFallback
            ? Math.round(this.currentSignElapsedMs)
            : (this.sequencePlaybackState === 'COMPLETED' && this.lastCompletedClip ? Math.round(this.lastCompletedDurationMs || 0) : 0));

      return {
        isLoaded: this.isLoaded,
        isLoading: this.isLoading,
        loadError: this.loadError ? this.loadError.message : null,
        isPlaying: this.isPlaying,
        isPaused: this.isPaused,
        currentTimeMs: activeTime,
        durationMs: activeDuration,
        currentClipId: activeClipId,
        currentPoseId: this.currentPoseId,
        isLinguisticISL: activeLinguistic,
        labelNotice,
        boneCount: this.bones.size,
        missingBones: Array.from(this.missingBonesEncountered),
        renderCount: this.renderCount || 0,
        lastRenderError: this.lastRenderError ? this.lastRenderError.message : null,
        cameraPosition: this.camera ? [this.camera.position.x, this.camera.position.y, this.camera.position.z] : null,
        // Sequence playback telemetry (M3.5)
        activeSequenceId: this.activeSequence ? this.activeSequence.sequenceId : null,
        activeLanguage: this.activeSequence ? this.activeSequence.language : null,
        sequenceSignsCount: this.sequenceSigns ? this.sequenceSigns.length : 0,
        sequenceSignIndex: this.sequenceSignIndex,
        currentGloss: this.currentSignGloss || (this.sequencePlaybackState === 'COMPLETED' && this.lastCompletedClip ? this.lastCompletedGloss : null),
        currentSignIsFallback: this.currentSignIsFallback,
        sequencePlaybackState: this.sequencePlaybackState || 'IDLE',
        unsupportedWords: (this.activeSequence && Array.isArray(this.activeSequence.unsupportedWords))
          ? this.activeSequence.unsupportedWords
          : []
      };
    }

    /**
     * Inspects current live bone transforms on the loaded model.
     * Used by automated unit tests to verify physical rig articulation.
     *
     * @param {string} boneName - Canonical or prefixed bone name.
     * @returns {{ rotation: number[], position: number[], quaternion: number[] } | null}
     */
    getBoneTransform(boneName) {
      const canonical = this.keyframeRegistry.normalizeBoneName(boneName);
      const bone = this.bones.get(canonical);
      if (!bone) return null;

      return {
        rotation: [bone.rotation.x, bone.rotation.y, bone.rotation.z],
        quaternion: [bone.quaternion.x, bone.quaternion.y, bone.quaternion.z, bone.quaternion.w],
        position: [bone.position.x, bone.position.y, bone.position.z]
      };
    }

    /**
     * Explicitly renders a single frame to the canvas.
     */
    render() {
      if (this.renderer && this.scene && this.camera) {
        this.renderer.render(this.scene, this.camera);
      }
    }

    /**
     * Resizes the WebGL renderer and adjusts camera aspect ratio.
     *
     * @param {number} width - New width in pixels.
     * @param {number} height - New height in pixels.
     */
    resize(width, height) {
      if (this.camera && this.renderer) {
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
      }
    }

    /**
     * Cleans up all WebGL, DOM, and animation frame resources.
     */
    dispose() {
      this.isDisposed = true;
      if (this.animFrameId) {
        cancelAnimationFrame(this.animFrameId);
        this.animFrameId = null;
      }

      if (this.model && this.scene) {
        this.scene.remove(this.model);
      }

      if (this.renderer) {
        if (this.renderer.domElement && this.renderer.domElement.parentNode) {
          this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
        }
        this.renderer.dispose();
      }

      this.bones.clear();
      this.initialRotations.clear();
      this.missingBonesEncountered.clear();
    }
  }

  const VERSION = '1.0.2-speech-avatar-m35';
  AvatarPlayer.VERSION = VERSION;
  console.log(`[SignBridge] AvatarPlayer loaded (v${VERSION}) — frustumCulled=false, camera=[0, 1.30, 1.65], sequence playback ready`);

  return Object.freeze({
    VERSION,
    AvatarPlayer,
    AvatarPlayerError,
    TECHNICAL_TEST_NOTICE,
    NEUTRAL_REST_NOTICE
  });
});
