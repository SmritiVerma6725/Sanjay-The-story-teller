/**
 * SignBridge — Milestone M3 Phase 3.3: Declarative Keyframe Schema & Feasibility Prototype
 *
 * Implements:
 * 1. Declarative Keyframe and Animation Clip schema definitions.
 * 2. Strict schema validators for bone identifiers, Euler/Quaternion rotations, and timing.
 * 3. Canonical Mixamo bone hierarchy mapping and normalization.
 * 4. Documented Neutral Rest Pose definition.
 * 5. Synthetic Technical Motion Prototype (clearly labeled; NOT a linguistic ISL sign).
 * 6. Animation resolver connecting SignItem contracts to registered animation assets.
 * 7. Keyframe interpolation engine (Linear for Euler, Slerp for Quaternions).
 *
 * CRITICAL GOVERNANCE & PROVENANCE DISCLAIMER:
 * - This module is a technical engineering prototype to evaluate skeletal rig feasibility.
 * - Procedural motions in this file are SYNTHETIC TESTS, NOT validated linguistic ISL signs.
 * - Finding a matching gloss does NOT mean an animation exists. Unless a clip is registered
 *   and resolved, the system defaults safely to the neutral rest pose and flags unresolved status.
 */

(function (root, factory) {
  if (typeof module === 'object' && typeof module.exports === 'object') {
    const contracts = require('../models/sign_contracts.js');
    module.exports = factory(contracts);
  } else if (typeof define === 'function' && define.amd) {
    define(['../models/sign_contracts.js'], factory);
  } else {
    root.SignBridgeKeyframeRegistry = factory(
      root.SignBridgeContracts || (typeof globalThis !== 'undefined' ? globalThis.SignBridgeContracts : null)
    );
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function (SignBridgeContracts) {
  'use strict';

  // =========================================================================
  // 1. Canonical Mixamo Bone Hierarchy & Dictionary
  // =========================================================================

  /**
   * The complete verified 67-joint skeleton of Adobe Mixamo Y-Bot (ybot.glb).
   * Keyed by canonical compact bone name (e.g. "RightHandIndex1").
   */
  const CANONICAL_BONES = Object.freeze(new Set([
    // Core & Head
    'Hips', 'Spine', 'Spine1', 'Spine2', 'Neck', 'Head', 'HeadTop_End',
    'LeftEye', 'RightEye',
    
    // Left Upper Body & Arm
    'LeftShoulder', 'LeftArm', 'LeftForeArm', 'LeftHand',
    // Left Hand Fingers (4 joints per digit)
    'LeftHandThumb1', 'LeftHandThumb2', 'LeftHandThumb3', 'LeftHandThumb4',
    'LeftHandIndex1', 'LeftHandIndex2', 'LeftHandIndex3', 'LeftHandIndex4',
    'LeftHandMiddle1', 'LeftHandMiddle2', 'LeftHandMiddle3', 'LeftHandMiddle4',
    'LeftHandRing1', 'LeftHandRing2', 'LeftHandRing3', 'LeftHandRing4',
    'LeftHandPinky1', 'LeftHandPinky2', 'LeftHandPinky3', 'LeftHandPinky4',

    // Right Upper Body & Arm
    'RightShoulder', 'RightArm', 'RightForeArm', 'RightHand',
    // Right Hand Fingers (4 joints per digit)
    'RightHandThumb1', 'RightHandThumb2', 'RightHandThumb3', 'RightHandThumb4',
    'RightHandIndex1', 'RightHandIndex2', 'RightHandIndex3', 'RightHandIndex4',
    'RightHandMiddle1', 'RightHandMiddle2', 'RightHandMiddle3', 'RightHandMiddle4',
    'RightHandRing1', 'RightHandRing2', 'RightHandRing3', 'RightHandRing4',
    'RightHandPinky1', 'RightHandPinky2', 'RightHandPinky3', 'RightHandPinky4',

    // Lower Body
    'LeftUpLeg', 'LeftLeg', 'LeftFoot', 'LeftToeBase', 'LeftToe_End',
    'RightUpLeg', 'RightLeg', 'RightFoot', 'RightToeBase', 'RightToe_End'
  ]));

  /**
   * Normalizes any Mixamo bone string variant to its canonical compact name.
   * e.g. "mixamorig:RightArm" -> "RightArm", "mixamorigRightArm" -> "RightArm".
   *
   * @param {string} rawName - Raw bone name.
   * @returns {string} Canonical name.
   */
  function normalizeBoneName(rawName) {
    if (typeof rawName !== 'string') return '';
    return rawName.trim().replace(/^mixamorig:?/, '');
  }

  /**
   * Checks whether a bone identifier belongs to the verified Y-Bot skeletal rig.
   *
   * @param {string} rawName - Candidate bone name.
   * @returns {boolean}
   */
  function isValidRigBone(rawName) {
    const compact = normalizeBoneName(rawName);
    return CANONICAL_BONES.has(compact);
  }

  // =========================================================================
  // 2. Custom Keyframe Validation Error
  // =========================================================================

  class KeyframeValidationError extends Error {
    constructor(message, errors = []) {
      super(message);
      this.name = 'KeyframeValidationError';
      this.errors = Array.isArray(errors) ? errors : [errors];
    }
  }

  // =========================================================================
  // 3. Declarative Keyframe Schema Validators
  // =========================================================================

  /**
   * Validates a single BoneTransform object.
   *
   * @param {Object} transform - Candidate transform.
   * @returns {{ valid: boolean, errors: string[] }}
   */
  function validateBoneTransform(transform) {
    const errors = [];
    if (!transform || typeof transform !== 'object') {
      return { valid: false, errors: ['BoneTransform must be a non-null object'] };
    }

    // 1. bone name check
    if (typeof transform.bone !== 'string' || transform.bone.trim().length === 0) {
      errors.push('BoneTransform.bone must be a non-empty string');
    } else if (!isValidRigBone(transform.bone)) {
      errors.push(`BoneTransform.bone '${transform.bone}' is not a valid joint in the Y-Bot rig`);
    }

    // 2. rotation check
    const rotType = transform.rotationType || (Array.isArray(transform.rotation) && transform.rotation.length === 4 ? 'quaternion' : 'euler');
    if (!['euler', 'quaternion'].includes(rotType)) {
      errors.push(`BoneTransform.rotationType must be 'euler' or 'quaternion', got '${rotType}'`);
    }

    if (!Array.isArray(transform.rotation)) {
      errors.push('BoneTransform.rotation must be an array of numbers');
    } else {
      if (rotType === 'euler') {
        if (transform.rotation.length !== 3) {
          errors.push(`Euler rotation must have exactly 3 components [x, y, z], got ${transform.rotation.length}`);
        } else if (transform.rotation.some(v => typeof v !== 'number' || !Number.isFinite(v))) {
          errors.push('Euler rotation components must all be finite numbers');
        }
      } else if (rotType === 'quaternion') {
        if (transform.rotation.length !== 4) {
          errors.push(`Quaternion rotation must have exactly 4 components [x, y, z, w], got ${transform.rotation.length}`);
        } else if (transform.rotation.some(v => typeof v !== 'number' || !Number.isFinite(v))) {
          errors.push('Quaternion components must all be finite numbers');
        } else {
          // Check non-zero length
          const lenSq = transform.rotation.reduce((sum, v) => sum + v * v, 0);
          if (lenSq < 1e-8) {
            errors.push('Quaternion rotation cannot be a zero-length vector');
          }
        }
      }
    }

    // 3. optional position offset check
    if (transform.position !== undefined && transform.position !== null) {
      if (!Array.isArray(transform.position) || transform.position.length !== 3) {
        errors.push('BoneTransform.position, if provided, must be a 3-element array [x, y, z]');
      } else if (transform.position.some(v => typeof v !== 'number' || !Number.isFinite(v))) {
        errors.push('BoneTransform.position components must all be finite numbers');
      }
    }

    return { valid: errors.length === 0, errors };
  }

  /**
   * Validates an entire Keyframe object.
   *
   * @param {Object} kf - Candidate keyframe.
   * @param {number} clipDurationMs - Total duration of parent clip.
   * @returns {{ valid: boolean, errors: string[] }}
   */
  function validateKeyframe(kf, clipDurationMs) {
    const errors = [];
    if (!kf || typeof kf !== 'object') {
      return { valid: false, errors: ['Keyframe must be a non-null object'] };
    }

    if (typeof kf.timeMs !== 'number' || !Number.isFinite(kf.timeMs)) {
      errors.push('Keyframe.timeMs must be a finite number');
    } else if (kf.timeMs < 0) {
      errors.push(`Keyframe.timeMs must be non-negative (>= 0), got ${kf.timeMs}`);
    } else if (typeof clipDurationMs === 'number' && kf.timeMs > clipDurationMs) {
      errors.push(`Keyframe.timeMs (${kf.timeMs}) exceeds clip duration (${clipDurationMs})`);
    }

    if (!Array.isArray(kf.transforms)) {
      errors.push('Keyframe.transforms must be an array of BoneTransform objects');
    } else {
      kf.transforms.forEach((t, idx) => {
        const res = validateBoneTransform(t);
        if (!res.valid) {
          res.errors.forEach(e => errors.push(`Keyframe.transforms[${idx}]: ${e}`));
        }
      });
    }

    return { valid: errors.length === 0, errors };
  }

  /**
   * Validates a complete SignAnimationClip structure.
   *
   * @param {Object} clip - Candidate clip.
   * @returns {{ valid: boolean, errors: string[] }}
   */
  function validateAnimationClip(clip) {
    const errors = [];
    if (!clip || typeof clip !== 'object') {
      return { valid: false, errors: ['SignAnimationClip must be a non-null object'] };
    }

    // 1. animationId
    if (typeof clip.animationId !== 'string' || !/^[a-zA-Z0-9_.-]+$/.test(clip.animationId.trim())) {
      errors.push(`SignAnimationClip.animationId must be a valid alphanumeric/dash/underscore identifier, got '${clip.animationId}'`);
    }

    // 2. gloss
    if (typeof clip.gloss !== 'string' || clip.gloss.trim().length === 0) {
      errors.push('SignAnimationClip.gloss must be a non-empty string');
    }

    // 3. durationMs
    if (typeof clip.durationMs !== 'number' || !Number.isFinite(clip.durationMs) || clip.durationMs <= 0) {
      errors.push(`SignAnimationClip.durationMs must be a positive finite number (> 0), got ${clip.durationMs}`);
    }

    // 4. isLinguisticISL (mandatory boolean guard)
    if (typeof clip.isLinguisticISL !== 'boolean') {
      errors.push('SignAnimationClip.isLinguisticISL must be a boolean flag');
    }

    // 5. provenance
    if (typeof clip.provenance !== 'string' || clip.provenance.trim().length === 0) {
      errors.push('SignAnimationClip.provenance must document asset origin and review status');
    }

    // 6. keyframes array
    if (!Array.isArray(clip.keyframes) || clip.keyframes.length === 0) {
      errors.push('SignAnimationClip.keyframes must be a non-empty array of Keyframe objects');
    } else {
      let lastTime = -1;
      clip.keyframes.forEach((kf, idx) => {
        const kfRes = validateKeyframe(kf, clip.durationMs);
        if (!kfRes.valid) {
          kfRes.errors.forEach(e => errors.push(`keyframes[${idx}]: ${e}`));
        }
        if (typeof kf.timeMs === 'number') {
          if (kf.timeMs < lastTime) {
            errors.push(`keyframes[${idx}].timeMs (${kf.timeMs}) is not monotonically ordered (previous was ${lastTime})`);
          }
          lastTime = kf.timeMs;
        }
      });
    }

    return { valid: errors.length === 0, errors };
  }

  // =========================================================================
  // 4. Documented Neutral Rest Pose & Synthetic Technical Test Motion
  // =========================================================================

  /**
   * Neutral Rest Pose for Adobe Mixamo Y-Bot.
   *
   * Arms are lowered naturally by ~72 degrees (-1.25 rad on Z for right arm,
   * +1.25 rad on Z for left arm) with slight forward flexion on forearms (0.2 rad on X)
   * and natural resting finger curvature (0.15 rad on fingers 1 and 2).
   */
  const NEUTRAL_REST_POSE = Object.freeze({
    poseId: 'pose_neutral_rest_v1',
    description: 'Natural resting pose: arms relaxed at sides, forearms slightly forward, relaxed fingers',
    transforms: Object.freeze([
      // Right arm down from T-pose (in Mixamo coordinates, +Z rotates -X arm downwards to side)
      Object.freeze({ bone: 'RightArm', rotation: [0, 0, 1.25], rotationType: 'euler' }),
      Object.freeze({ bone: 'RightForeArm', rotation: [0.25, 0, 0], rotationType: 'euler' }),
      Object.freeze({ bone: 'RightHand', rotation: [0, 0, 0], rotationType: 'euler' }),
      // Relaxed right fingers
      Object.freeze({ bone: 'RightHandIndex1', rotation: [0, 0, -0.15], rotationType: 'euler' }),
      Object.freeze({ bone: 'RightHandMiddle1', rotation: [0, 0, -0.15], rotationType: 'euler' }),
      Object.freeze({ bone: 'RightHandRing1', rotation: [0, 0, -0.15], rotationType: 'euler' }),
      Object.freeze({ bone: 'RightHandPinky1', rotation: [0, 0, -0.15], rotationType: 'euler' }),
      Object.freeze({ bone: 'RightHandThumb1', rotation: [0.1, 0, -0.1], rotationType: 'euler' }),

      // Left arm down from T-pose (in Mixamo coordinates, -Z rotates +X arm downwards to side)
      Object.freeze({ bone: 'LeftArm', rotation: [0, 0, -1.25], rotationType: 'euler' }),
      Object.freeze({ bone: 'LeftForeArm', rotation: [0.25, 0, 0], rotationType: 'euler' }),
      Object.freeze({ bone: 'LeftHand', rotation: [0, 0, 0], rotationType: 'euler' }),
      // Relaxed left fingers
      Object.freeze({ bone: 'LeftHandIndex1', rotation: [0, 0, 0.15], rotationType: 'euler' }),
      Object.freeze({ bone: 'LeftHandMiddle1', rotation: [0, 0, 0.15], rotationType: 'euler' }),
      Object.freeze({ bone: 'LeftHandRing1', rotation: [0, 0, 0.15], rotationType: 'euler' }),
      Object.freeze({ bone: 'LeftHandPinky1', rotation: [0, 0, 0.15], rotationType: 'euler' }),
      Object.freeze({ bone: 'LeftHandThumb1', rotation: [0.1, 0, 0.1], rotationType: 'euler' })
    ])
  });

  /**
   * Synthetic Technical Motion Prototype.
   *
   * Explicitly labeled: isLinguisticISL = false.
   * Purpose: Verify multi-keyframe time sequencing, interpolation, and safe return to rest pose.
   */
  const TECHNICAL_TEST_CLIP = Object.freeze({
    animationId: 'tech_test_motion_v1',
    gloss: 'TECHNICAL_TEST_MOTION',
    durationMs: 2000,
    isLinguisticISL: false,
    provenance: 'SignBridge Phase 3.3 synthetic technical feasibility motion; NOT a validated ISL sign',
    keyframes: Object.freeze([
      // Frame 0: Start at neutral rest pose (arms at sides)
      Object.freeze({
        timeMs: 0,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [0, 0, 1.25], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [0.25, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [0, 0, 0], rotationType: 'euler' })
        ])
      }),
      // Frame 1 (600ms): Raise right arm to chest height, forearm forward
      Object.freeze({
        timeMs: 600,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [-0.5, 0, 0.4], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [0.8, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [0, 0.2, 0.2], rotationType: 'euler' })
        ])
      }),
      // Frame 2 (1200ms): Hand wave outward
      Object.freeze({
        timeMs: 1200,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [-0.5, 0, 0.4], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [0.8, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [0, -0.3, -0.2], rotationType: 'euler' })
        ])
      }),
      // Frame 3 (2000ms): Smooth return to neutral rest pose
      Object.freeze({
        timeMs: 2000,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [0, 0, 1.25], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [0.25, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [0, 0, 0], rotationType: 'euler' })
        ])
      })
    ])
  });

  /**
   * Indian Sign Language (ISL) Canonical Sign: NAMASTE.
   *
   * PROVENANCE & LICENSING:
   * - Source: Indian Sign Language Research and Training Centre (ISLRTC)
   *   Dictionary (Vol 1, Word #0001, Entry "Namaste" / "Greetings"),
   *   Department of Empowerment of Persons with Disabilities, Ministry of
   *   Social Justice and Empowerment, Government of India.
   * - Published on data.gov.in under the Government Open Data License - India (GODL).
   * - License: Free, worldwide, royalty-free, non-exclusive permission to adapt,
   *   reproduce, and distribute with required attribution.
   * - Lexical Form: Two-handed symmetrical sign. Palms pressed flat against each
   *   other in Anjali Mudra at sternum height; fingers straight and together;
   *   slight respectful forward head tilt (~10 degrees).
   * - Linguistic Review Status: Geometric transcription of official ISLRTC lexical
   *   specification on Adobe Mixamo Y-Bot rig; pending formal Deaf-native sign
   *   validation panel review.
   */
  const ISL_NAMASTE_CLIP = Object.freeze({
    animationId: 'isl_namaste_godl_v1',
    gloss: 'NAMASTE',
    durationMs: 1800,
    isLinguisticISL: true,
    validationStatus: 'experimental_awaiting_validation',
    captureMethod: 'hand_authored_geometric_approximation',
    sourceReference: 'ISLRTC Dictionary Vol 1, Word #0001 (data.gov.in / GODL)',
    provenance: 'Hand-authored geometric transcription based on official ISLRTC Dictionary Entry (data.gov.in) under Government Open Data License - India (GODL); NOT captured from video motion-capture; experimental and awaiting formal Deaf-native sign validation panel review',
    keyframes: Object.freeze([
      // Frame 0 (0ms): Start at neutral rest pose (arms at sides)
      Object.freeze({
        timeMs: 0,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [0, 0, 1.25], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [0.25, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftArm', rotation: [0, 0, -1.25], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftForeArm', rotation: [0.25, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHand', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'Head', rotation: [0, 0, 0], rotationType: 'euler' })
        ])
      }),
      // Frame 1 (450ms): Forearms flex upward, arms adduct forward toward center chest
      Object.freeze({
        timeMs: 450,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [-0.4, 0.15, 0.5], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [1.1, 0.2, 0.1], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [-0.1, 0.05, 0.0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftArm', rotation: [-0.4, -0.15, -0.5], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftForeArm', rotation: [1.1, -0.2, -0.1], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHand', rotation: [-0.1, -0.05, 0.0], rotationType: 'euler' }),
          Object.freeze({ bone: 'Head', rotation: [0.08, 0, 0], rotationType: 'euler' })
        ])
      }),
      // Frame 2 (900ms): Palms pressed flat at sternum (Anjali Mudra), fingers straight, respectful head nod
      Object.freeze({
        timeMs: 900,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [-0.55, 0.25, 0.40], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [1.35, 0.25, 0.15], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [-0.2, 0.1, 0.0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandIndex1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandMiddle1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandRing1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandPinky1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandThumb1', rotation: [0.05, 0, 0], rotationType: 'euler' }),

          Object.freeze({ bone: 'LeftArm', rotation: [-0.55, -0.25, -0.40], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftForeArm', rotation: [1.35, -0.25, -0.15], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHand', rotation: [-0.2, -0.1, 0.0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandIndex1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandMiddle1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandRing1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandPinky1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandThumb1', rotation: [0.05, 0, 0], rotationType: 'euler' }),

          Object.freeze({ bone: 'Head', rotation: [0.18, 0, 0], rotationType: 'euler' })
        ])
      }),
      // Frame 3 (1350ms): Hold prayer pose at chest with respectful bow held
      Object.freeze({
        timeMs: 1350,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [-0.55, 0.25, 0.40], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [1.35, 0.25, 0.15], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [-0.2, 0.1, 0.0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandIndex1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandMiddle1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandRing1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandPinky1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHandThumb1', rotation: [0.05, 0, 0], rotationType: 'euler' }),

          Object.freeze({ bone: 'LeftArm', rotation: [-0.55, -0.25, -0.40], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftForeArm', rotation: [1.35, -0.25, -0.15], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHand', rotation: [-0.2, -0.1, 0.0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandIndex1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandMiddle1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandRing1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandPinky1', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHandThumb1', rotation: [0.05, 0, 0], rotationType: 'euler' }),

          Object.freeze({ bone: 'Head', rotation: [0.18, 0, 0], rotationType: 'euler' })
        ])
      }),
      // Frame 4 (1800ms): Smooth return to neutral rest pose
      Object.freeze({
        timeMs: 1800,
        transforms: Object.freeze([
          Object.freeze({ bone: 'RightArm', rotation: [0, 0, 1.25], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightForeArm', rotation: [0.25, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'RightHand', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftArm', rotation: [0, 0, -1.25], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftForeArm', rotation: [0.25, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'LeftHand', rotation: [0, 0, 0], rotationType: 'euler' }),
          Object.freeze({ bone: 'Head', rotation: [0, 0, 0], rotationType: 'euler' })
        ])
      })
    ])
  });

  // =========================================================================
  // 5. Keyframe Interpolation Engine (Euler Linear & Quaternion Slerp)
  // =========================================================================

  /**
   * Spherical Linear Interpolation (Slerp) between two unit quaternions.
   *
   * @param {number[]} qA - Quaternion [x, y, z, w].
   * @param {number[]} qB - Quaternion [x, y, z, w].
   * @param {number} t - Interpolation factor [0..1].
   * @returns {number[]} Interpolated unit quaternion [x, y, z, w].
   */
  function slerpQuaternions(qA, qB, t) {
    let [ax, ay, az, aw] = qA;
    let [bx, by, bz, bw] = qB;

    let dot = ax * bx + ay * by + az * bz + aw * bw;
    if (dot < 0) {
      bx = -bx;
      by = -by;
      bz = -bz;
      bw = -bw;
      dot = -dot;
    }

    if (dot > 0.9995) {
      // Linear interpolation for nearly parallel quaternions
      const rx = ax + t * (bx - ax);
      const ry = ay + t * (by - ay);
      const rz = az + t * (bz - az);
      const rw = aw + t * (bw - aw);
      const len = Math.hypot(rx, ry, rz, rw) || 1;
      return [rx / len, ry / len, rz / len, rw / len];
    }

    const theta = Math.acos(dot);
    const sinTheta = Math.sin(theta);
    const factorA = Math.sin((1 - t) * theta) / sinTheta;
    const factorB = Math.sin(t * theta) / sinTheta;

    return [
      factorA * ax + factorB * bx,
      factorA * ay + factorB * by,
      factorA * az + factorB * bz,
      factorA * aw + factorB * bw
    ];
  }

  /**
   * Evaluates a SignAnimationClip at an elapsed time in milliseconds,
   * returning interpolated bone rotations.
   *
   * @param {Object} clip - Validated SignAnimationClip.
   * @param {number} elapsedMs - Time offset in milliseconds.
   * @returns {Map<string, { rotation: number[], rotationType: string }>}
   */
  function evaluateClipAtTime(clip, elapsedMs) {
    const res = validateAnimationClip(clip);
    if (!res.valid) {
      throw new KeyframeValidationError(`Cannot evaluate invalid clip: ${res.errors.join('; ')}`, res.errors);
    }

    const clampedTime = Math.max(0, Math.min(clip.durationMs, elapsedMs));
    const kfs = clip.keyframes;

    // Find bounding keyframes
    let kfA = kfs[0];
    let kfB = kfs[kfs.length - 1];

    for (let i = 0; i < kfs.length - 1; i++) {
      if (clampedTime >= kfs[i].timeMs && clampedTime <= kfs[i + 1].timeMs) {
        kfA = kfs[i];
        kfB = kfs[i + 1];
        break;
      }
    }

    const span = kfB.timeMs - kfA.timeMs;
    const alpha = span > 0 ? (clampedTime - kfA.timeMs) / span : 0;

    const transformsA = new Map(kfA.transforms.map(t => [normalizeBoneName(t.bone), t]));
    const transformsB = new Map(kfB.transforms.map(t => [normalizeBoneName(t.bone), t]));

    const evaluatedBones = new Map();
    const allBoneNames = new Set([...transformsA.keys(), ...transformsB.keys()]);

    for (const bone of allBoneNames) {
      const tA = transformsA.get(bone);
      const tB = transformsB.get(bone);

      if (tA && tB && tA.rotationType === tB.rotationType) {
        if (tA.rotationType === 'quaternion') {
          const rot = slerpQuaternions(tA.rotation, tB.rotation, alpha);
          evaluatedBones.set(bone, { rotation: rot, rotationType: 'quaternion' });
        } else {
          // Linear interpolation for Euler angles
          const [ax, ay, az] = tA.rotation;
          const [bx, by, bz] = tB.rotation;
          const rot = [
            ax + alpha * (bx - ax),
            ay + alpha * (by - ay),
            az + alpha * (bz - az)
          ];
          evaluatedBones.set(bone, { rotation: rot, rotationType: 'euler' });
        }
      } else if (tA) {
        evaluatedBones.set(bone, { rotation: [...tA.rotation], rotationType: tA.rotationType });
      } else if (tB) {
        evaluatedBones.set(bone, { rotation: [...tB.rotation], rotationType: tB.rotationType });
      }
    }

    const transformList = [];
    for (const [bone, data] of evaluatedBones.entries()) {
      transformList.push({ bone, rotation: data.rotation, rotationType: data.rotationType });
    }

    return {
      timeMs: clampedTime,
      transforms: transformList,
      boneMap: evaluatedBones
    };
  }

  // =========================================================================
  // 6. Animation Registry & Asset Resolution
  // =========================================================================

  /**
   * In-memory registry holding verified/tested animation clips.
   */
  const REGISTERED_CLIPS = new Map();

  // Register the synthetic technical prototype
  REGISTERED_CLIPS.set(TECHNICAL_TEST_CLIP.animationId, TECHNICAL_TEST_CLIP);

  // Register the canonical ISLRTC GODL sign animation clip
  REGISTERED_CLIPS.set(ISL_NAMASTE_CLIP.animationId, ISL_NAMASTE_CLIP);

  /**
   * Registers a new animation clip into the registry.
   *
   * @param {Object} clip - SignAnimationClip candidate.
   * @returns {boolean} True if successfully validated and registered.
   */
  function registerAnimationClip(clip) {
    const validation = validateAnimationClip(clip);
    if (!validation.valid) {
      throw new KeyframeValidationError(`Clip registration failed: ${validation.errors.join('; ')}`, validation.errors);
    }
    REGISTERED_CLIPS.set(clip.animationId, Object.freeze(clip));
    return true;
  }

  /**
   * Resolves an animation clip for a SignItem without falsely claiming
   * that unverified glosses have valid animations.
   *
   * @param {Object} signItem - SignItem instance from sign_contracts.
   * @returns {{ resolved: boolean, clip: Object|null, animationId: string|null, isLinguisticISL: boolean, fallbackPose: Object }}
   */
  function resolveSignAnimation(signItem) {
    if (!signItem || typeof signItem !== 'object') {
      return {
        resolved: false,
        clip: null,
        animationId: null,
        isLinguisticISL: false,
        fallbackPose: NEUTRAL_REST_POSE,
        reason: 'Invalid or missing SignItem'
      };
    }

    // 1. Direct animationId lookup if explicitly provided on SignItem
    if (typeof signItem.animationId === 'string' && signItem.animationId.trim().length > 0) {
      const clip = REGISTERED_CLIPS.get(signItem.animationId.trim());
      if (clip) {
        return {
          resolved: true,
          clip,
          animationId: clip.animationId,
          isLinguisticISL: clip.isLinguisticISL,
          fallbackPose: NEUTRAL_REST_POSE
        };
      }
    }

    // 2. Gloss-based lookup in registered clips
    if (typeof signItem.gloss === 'string') {
      for (const clip of REGISTERED_CLIPS.values()) {
        if (clip.gloss === signItem.gloss) {
          return {
            resolved: true,
            clip,
            animationId: clip.animationId,
            isLinguisticISL: clip.isLinguisticISL,
            fallbackPose: NEUTRAL_REST_POSE
          };
        }
      }
    }

    // 3. Honest Unresolved State (Safe fallback to Neutral Rest Pose)
    return {
      resolved: false,
      clip: null,
      animationId: null,
      isLinguisticISL: false,
      fallbackPose: NEUTRAL_REST_POSE,
      reason: `No registered 3D animation clip exists for gloss '${signItem.gloss}'`
    };
  }

  // =========================================================================
  // 7. Public API Export
  // =========================================================================

  const VERSION = '1.0.1-pose-fix-20261018';
  console.log(`[SignBridge] KeyframeRegistry loaded (v${VERSION}) — Rest pose RightArm=+1.25 rad`);

  return Object.freeze({
    VERSION,

    // Rig Constants
    CANONICAL_BONES,
    normalizeBoneName,
    isValidRigBone,

    // Error Class
    KeyframeValidationError,

    // Validators
    validateBoneTransform,
    validateKeyframe,
    validateAnimationClip,

    // Built-in Poses & Prototype Clips
    NEUTRAL_REST_POSE,
    TECHNICAL_TEST_CLIP,
    ISL_NAMASTE_CLIP,

    // Math & Interpolation
    slerpQuaternions,
    evaluateClipAtTime,

    // Registry & Resolution
    registerAnimationClip,
    resolveSignAnimation,
    getRegisteredClips: () => new Map(REGISTERED_CLIPS)
  });
});
