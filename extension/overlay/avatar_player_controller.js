    let player = null;

    window.addEventListener("DOMContentLoaded", () => {
      const container = document.getElementById("avatar-container");
      const statusOverlay = document.getElementById("viewport-status");
      const clipTitle = document.getElementById("clip-title");
      const timeDisplay = document.getElementById("time-display");
      const progressFill = document.getElementById("progress-fill");
      const telLoaded = document.getElementById("tel-loaded");
      const telState = document.getElementById("tel-state");
      const telClip = document.getElementById("tel-clip");
      const telIslGuard = document.getElementById("tel-isl-guard");
      const telBones = document.getElementById("tel-bones");
      const jointTelemetry = document.getElementById("joint-telemetry");
      const governanceBanner = document.getElementById("governance-banner") || document.querySelector(".governance-banner");

      const btnPlay = document.getElementById("btn-play");
      const btnPause = document.getElementById("btn-pause");
      const btnResume = document.getElementById("btn-resume");
      const btnRestart = document.getElementById("btn-restart");
      const btnNeutral = document.getElementById("btn-neutral");
      const btnMissing = document.getElementById("btn-test-missing");
      const btnUnreg = document.getElementById("btn-test-unregistered");

      // Pipeline UI elements
      const selectTargetLang = document.getElementById("select-target-lang");
      const pipeLangBadge = document.getElementById("pipe-lang-badge");
      const inputTranscript = document.getElementById("input-transcript");
      const btnTranslatePlay = document.getElementById("btn-translate-play");
      const btnInterrupt = document.getElementById("btn-interrupt");
      const btnCheckBackend = document.getElementById("btn-check-backend");

      const btnSampleNamaste = document.getElementById("btn-sample-namaste");
      const btnSampleHello = document.getElementById("btn-sample-hello");
      const btnSampleThankYou = document.getElementById("btn-sample-thankyou");
      const btnSampleMixed = document.getElementById("btn-sample-mixed");
      const btnSampleMulti = document.getElementById("btn-sample-multi");
      const btnSampleUnknown = document.getElementById("btn-sample-unknown");
      const btnSampleEmpty = document.getElementById("btn-sample-empty");
      const btnSampleDemoCombo = document.getElementById("btn-sample-demo-combo");
      const btnSampleDailyRoutine = document.getElementById("btn-sample-daily-routine");

      const telPipeTranscript = document.getElementById("tel-pipe-transcript");
      const telPipeLang = document.getElementById("tel-pipe-lang");
      const telPipeStatus = document.getElementById("tel-pipe-status");
      const telPipeSeqId = document.getElementById("tel-pipe-seq-id");
      const telPipeSigns = document.getElementById("tel-pipe-signs");
      const telPipeUnsupported = document.getElementById("tel-pipe-unsupported");
      const telPipeCurrentGloss = document.getElementById("tel-pipe-current-gloss");
      const telPipeFallback = document.getElementById("tel-pipe-fallback");
      const telPipePlayerState = document.getElementById("tel-pipe-player-state");
      const telWhisperBackend = document.getElementById("tel-whisper-backend");
      const telPipeNotice = document.getElementById("tel-pipe-notice");

      // Diagnostic DOM elements
      const diagThree = document.getElementById("diag-three");
      const diagGltf = document.getElementById("diag-gltf");
      const diagRegVer = document.getElementById("diag-reg-ver");
      const diagPlayerVer = document.getElementById("diag-player-ver");
      const diagWebglStatus = document.getElementById("diag-webgl-status");
      const diagWebglRenderer = document.getElementById("diag-webgl-renderer");
      const diagCanvasSize = document.getElementById("diag-canvas-size");
      const diagCanvasObscured = document.getElementById("diag-canvas-obscured");
      const diagGlError = document.getElementById("diag-gl-error");
      const diagModelStatus = document.getElementById("diag-model-status");
      const diagMeshesCount = document.getElementById("diag-meshes-count");
      const diagFrustumCulling = document.getElementById("diag-frustum-culling");
      const diagWorldBounds = document.getElementById("diag-world-bounds");
      const diagCameraFraming = document.getElementById("diag-camera-framing");
      const diagRenderCount = document.getElementById("diag-render-count");
      const diagRenderLoop = document.getElementById("diag-render-loop");
      const diagLoadError = document.getElementById("diag-load-error");
      const diagRenderError = document.getElementById("diag-render-error");

      const PlayerClass = window.SignBridgeAvatarPlayer.AvatarPlayer;
      const K = window.SignBridgeKeyframeRegistry;
      const Router = window.SignBridgeTranslationRouter;

      // Diagnostic static checks
      diagThree.innerHTML = typeof THREE !== 'undefined' ? `<span class="diag-ok">&#10004; Loaded (r128)</span>` : `<span class="diag-err">&#10008; Missing</span>`;
      diagGltf.innerHTML = (typeof THREE !== 'undefined' && typeof THREE.GLTFLoader !== 'undefined') ? `<span class="diag-ok">&#10004; Loaded</span>` : `<span class="diag-err">&#10008; Missing</span>`;
      diagRegVer.innerHTML = K && K.VERSION ? `<span class="diag-ok">${K.VERSION}</span>` : `<span class="diag-warn">Legacy / Unversioned</span>`;
      diagPlayerVer.innerHTML = window.SignBridgeAvatarPlayer && window.SignBridgeAvatarPlayer.VERSION ? `<span class="diag-ok">${window.SignBridgeAvatarPlayer.VERSION}</span>` : `<span class="diag-warn">Legacy / Unversioned</span>`;

      try {
        player = new PlayerClass(container, {
          modelUrl: "../assets/models/ybot.glb",
          width: container.clientWidth || 360,
          height: 440,
          onLoad: (p) => {
            statusOverlay.textContent = "Y-Bot Rig Loaded (67 joints)";
            telLoaded.textContent = "Loaded (ybot.glb, 2.2MB)";
            telBones.textContent = `${p.bones.size} / 67 joints`;
            updateUI();
            updateDiagnostics();
          },
          onError: (err) => {
            statusOverlay.textContent = "Model Load Failed";
            telLoaded.textContent = "Error: " + err.message;
            telLoaded.style.color = "#f87171";
            diagLoadError.innerHTML = `<span class="diag-err">${err.message}</span>`;
            updateDiagnostics();
          },
          onStateChange: () => {
            updateUI();
            updateDiagnostics();
          }
        });

        // Expose player globally for Chrome DevTools / test console inspection
        window.player = player;
      } catch (err) {
        statusOverlay.textContent = "Player Init Error: " + err.message;
        console.error(err);
        diagLoadError.innerHTML = `<span class="diag-err">${err.message}</span>`;
      }

      function updateUI() {
        if (!player) return;
        const st = player.getStatus();

        // Badge
        let badgeHtml = '<span class="status-badge badge-neutral">NEUTRAL</span>';
        if (st.isPlaying) {
          if (st.currentSignIsFallback) {
            badgeHtml = '<span class="status-badge badge-paused" style="background:#7c2d12; color:#fed7aa;">&#9632; FALLBACK NEUTRAL</span>';
          } else {
            badgeHtml = '<span class="status-badge badge-playing">&#9658; PLAYING</span>';
          }
        } else if (st.isPaused) {
          badgeHtml = '<span class="status-badge badge-paused">&#10074;&#10074; PAUSED</span>';
        } else if (st.sequencePlaybackState === 'COMPLETED') {
          if (st.currentClipId) {
            badgeHtml = '<span class="status-badge badge-playing" style="background:#065f46; color:#6ee7b7;">&#10004; COMPLETED</span>';
          } else {
            badgeHtml = '<span class="status-badge badge-neutral">NEUTRAL</span>';
          }
        }
        telState.innerHTML = badgeHtml;

        // Active clip name and playback progress label
        telClip.textContent = st.currentClipId || (st.currentSignIsFallback && st.currentGloss ? `${st.currentGloss} (Neutral Fallback)` : (st.currentPoseId || "Neutral rest pose"));
        if (clipTitle) {
          if (st.isPlaying) {
            if (st.currentSignIsFallback) {
              clipTitle.textContent = `${st.currentGloss || 'Unknown'} (Neutral Fallback — ${st.durationMs} ms)`;
            } else if (st.currentGloss && st.currentClipId) {
              clipTitle.textContent = `${st.currentGloss} — ${st.currentClipId} (${st.durationMs} ms)`;
            } else if (st.currentClipId) {
              clipTitle.textContent = `${st.currentClipId} (${st.durationMs} ms)`;
            } else {
              clipTitle.textContent = `Playing (${st.durationMs} ms)`;
            }
          } else if (st.sequencePlaybackState === 'COMPLETED') {
            if (st.currentClipId) {
              const doneLabel = st.currentGloss ? `${st.currentGloss} — ${st.currentClipId}` : st.currentClipId;
              clipTitle.textContent = `${doneLabel} (${st.durationMs} ms) — COMPLETED`;
            } else {
              clipTitle.textContent = "Neutral Rest Pose (0 ms)";
            }
          } else if (st.isPaused) {
            const pausedLabel = st.currentGloss || st.currentClipId || 'Motion';
            clipTitle.textContent = `${pausedLabel} (${st.durationMs} ms) — PAUSED`;
          } else {
            clipTitle.textContent = "Neutral Rest Pose (0 ms)";
          }
        }

        // Duration, elapsed time, and progress bar
        timeDisplay.textContent = `${st.currentTimeMs} / ${st.durationMs} ms`;
        const pct = st.durationMs > 0 ? Math.min(100, Math.round((st.currentTimeMs / st.durationMs) * 100)) : 0;
        progressFill.style.width = `${pct}%`;

        // Linguistic validity indicator
        if (telIslGuard) {
          if (st.isLinguisticISL) {
            telIslGuard.innerHTML = '<span style="color: #facc15;">true (Experimental ISL — Awaiting Human Panel Validation)</span>';
          } else if (st.currentClipId === 'tech_test_motion_v1' || (!st.isLinguisticISL && st.isPlaying)) {
            telIslGuard.innerHTML = '<span style="color: #f87171;">false (Synthetic test — NOT a validated sign)</span>';
          } else if (st.currentSignIsFallback) {
            telIslGuard.innerHTML = '<span style="color: #cbd5e1;">false (Neutral rest pose — zero gestures)</span>';
          } else {
            telIslGuard.innerHTML = '<span style="color: #94a3b8;">false (Neutral Rest Pose)</span>';
          }
        }

        // Top governance banner update
        if (governanceBanner) {
          if (st.currentClipId === 'tech_test_motion_v1' || (!st.isLinguisticISL && st.isPlaying)) {
            governanceBanner.textContent = "⚠ Synthetic technical test — NOT a validated ISL sign";
            governanceBanner.style.background = "#7f1d1d";
          } else if (st.isLinguisticISL) {
            governanceBanner.textContent = "ℹ ISLRTC Lexical Baseline (GODL) — Experimental: Awaiting Certified Deaf-Native Human Panel Review (0/3 reviews completed)";
            governanceBanner.style.background = "#1e3a8a";
          } else {
            governanceBanner.textContent = "SignBridge 3D Avatar — Active Lexicon Baseline: ISL Namaste (Experimental) | Synthetic Test Motion";
            governanceBanner.style.background = "#1e293b";
          }
        }

        // Live bone inspection
        if (player.isLoaded) {
          const rArm = player.getBoneTransform("RightArm");
          const rFore = player.getBoneTransform("RightForeArm");
          const rHand = player.getBoneTransform("RightHand");

          if (rArm && rFore && rHand) {
            jointTelemetry.innerHTML = `
              <strong>RightArm:</strong> [X: ${rArm.rotation[0].toFixed(2)}, Y: ${rArm.rotation[1].toFixed(2)}, Z: ${rArm.rotation[2].toFixed(2)}] rad<br>
              <strong>RightForeArm:</strong> [X: ${rFore.rotation[0].toFixed(2)}, Y: ${rFore.rotation[1].toFixed(2)}, Z: ${rFore.rotation[2].toFixed(2)}] rad<br>
              <strong>RightHand:</strong> [X: ${rHand.rotation[0].toFixed(2)}, Y: ${rHand.rotation[1].toFixed(2)}, Z: ${rHand.rotation[2].toFixed(2)}] rad
            `;
          }
        }

        // Pipeline telemetry update
        telPipeCurrentGloss.textContent = st.currentGloss || 'None';
        if (st.currentSignIsFallback) {
          telPipeFallback.textContent = 'Active (Held in Neutral Rest Pose — Unknown/Un-animated Gloss)';
          telPipeFallback.style.color = '#facc15';
        } else if (st.isPlaying) {
          telPipeFallback.textContent = 'Inactive (Playing Registered 3D Motion)';
          telPipeFallback.style.color = '#34d399';
        } else {
          telPipeFallback.textContent = 'Idle (Safe Neutral)';
          telPipeFallback.style.color = '#94a3b8';
        }

        telPipePlayerState.innerHTML = badgeHtml;
        telPipeNotice.textContent = activePipelineMetadata.noticeText || st.labelNotice || 'Synthetic technical test — NOT a validated sign';

        // Pipeline status update based on playback progress
        if (telPipeStatus) {
          if (activePipelineMetadata.statusState === 'COMBO') {
            telPipeStatus.innerHTML = '<span class="diag-ok">COMBO TEST SEQUENCE</span>';
          } else if (st.sequencePlaybackState === 'COMPLETED') {
            if (st.currentClipId) {
              if (activePipelineMetadata.unsupportedCount === 0 && activePipelineMetadata.pendingReviewCount === 0) {
                telPipeStatus.innerHTML = '<span class="status-badge" style="background:#065f46; color:#6ee7b7;">&#10004; PLAYBACK_COMPLETE</span>';
              } else {
                telPipeStatus.innerHTML = '<span class="status-badge" style="background:#9a3412; color:#fed7aa;">PARTIAL / UNSUPPORTED</span>';
              }
            } else {
              if (activePipelineMetadata.pendingReviewCount > 0 && activePipelineMetadata.unsupportedCount > 0) {
                telPipeStatus.innerHTML = '<span class="status-badge" style="background:#9a3412; color:#fed7aa;">PARTIAL / UNSUPPORTED</span>';
              } else if (activePipelineMetadata.pendingReviewCount > 0) {
                telPipeStatus.innerHTML = '<span class="status-badge" style="background:#854d0e; color:#fef08a;">PENDING_REVIEW</span>';
              } else if (activePipelineMetadata.unsupportedCount > 0) {
                telPipeStatus.innerHTML = '<span class="status-badge" style="background:#7f1d1d; color:#fca5a5;">UNSUPPORTED</span>';
              }
            }
          }
        }
      }

      function updateDiagnostics() {
        if (!player) return;
        const st = player.getStatus();

        // WebGL diagnostics
        if (player.renderer) {
          const gl = player.renderer.getContext();
          if (gl) {
            const v = gl.getParameter(gl.VERSION) || "WebGL";
            const r = gl.getParameter(gl.RENDERER) || "Generic";
            diagWebglStatus.innerHTML = `<span class="diag-ok">&#10004; Success (${v.split(' ')[0]})</span>`;
            diagWebglRenderer.textContent = r.length > 32 ? r.substring(0, 32) + '...' : r;
            const err = gl.getError();
            diagGlError.innerHTML = err === 0 ? `<span class="diag-ok">0 (NO_ERROR)</span>` : `<span class="diag-err">Error code ${err}</span>`;
          }
          const cvs = player.renderer.domElement;
          if (cvs) {
            const rect = cvs.getBoundingClientRect();
            diagCanvasSize.textContent = `${Math.round(rect.width)}x${Math.round(rect.height)} px (buffer ${cvs.width}x${cvs.height})`;

            // Check if canvas is covered or obscured by another DOM element
            if (rect.width > 0 && rect.height > 0) {
              const elAtCenter = document.elementFromPoint(rect.left + rect.width / 2, rect.top + rect.height / 2);
              if (elAtCenter === cvs || elAtCenter === container) {
                diagCanvasObscured.innerHTML = `<span class="diag-ok">&#10004; No (Canvas is top-most)</span>`;
              } else if (elAtCenter) {
                diagCanvasObscured.innerHTML = `<span class="diag-warn">⚠ Covered by &lt;${elAtCenter.tagName.toLowerCase()} id="${elAtCenter.id}"&gt;</span>`;
              }
            }
          }
        }

        // Model diagnostics
        if (player.isLoaded && player.model) {
          diagModelStatus.innerHTML = `<span class="diag-ok">&#10004; Loaded (${player.bones.size} joints)</span>`;
          let meshCount = 0;
          let allCulledDisabled = true;
          player.model.traverse(n => {
            if (n.isMesh || n.isSkinnedMesh) {
              meshCount++;
              if (n.frustumCulled) allCulledDisabled = false;
            }
          });
          diagMeshesCount.innerHTML = `<span class="diag-ok">${meshCount} meshes visible</span>`;
          diagFrustumCulling.innerHTML = allCulledDisabled
            ? `<span class="diag-ok">&#10004; Disabled (frustumCulled=false)</span>`
            : `<span class="diag-err">⚠ Enabled (Risk of culling)</span>`;

          const box = new THREE.Box3().setFromObject(player.model);
          diagWorldBounds.textContent = `min: [${box.min.x.toFixed(3)}, ${box.min.y.toFixed(3)}, ${box.min.z.toFixed(3)}] max: [${box.max.x.toFixed(3)}, ${box.max.y.toFixed(3)}, ${box.max.z.toFixed(3)}]`;
        }

        // Camera framing
        if (player.camera) {
          diagCameraFraming.textContent = `Pos: [${player.camera.position.x.toFixed(2)}, ${player.camera.position.y.toFixed(2)}, ${player.camera.position.z.toFixed(2)}], FOV: ${player.camera.fov}°`;
        }

        // Render loop ticks
        diagRenderCount.textContent = st.renderCount || 0;
        if (st.lastRenderError) {
          diagRenderError.innerHTML = `<span class="diag-err">${st.lastRenderError}</span>`;
        }
      }

      // Live inspector timer loop (unconditional UI & diagnostics update)
      setInterval(() => {
        if (player) {
          updateUI();
          updateDiagnostics();
        }
      }, 100);

      // Active pipeline translation and health state
      let activePipelineMetadata = {
        eligibleCount: 0,
        pendingReviewCount: 0,
        unsupportedCount: 0,
        statusState: 'IDLE',
        noticeText: ''
      };

      // Speech-to-Sign Pipeline Execution
      function executeSpeechPipeline(transcript, targetLang) {
        if (!player) return;

        telPipeTranscript.textContent = `"${transcript}"`;
        telPipeLang.textContent = targetLang;

        try {
          const sequence = Router.routeTranscriptTranslation(transcript, targetLang);
          telPipeSeqId.textContent = sequence.sequenceId;

          const signs = sequence.signs || [];
          const unsupported = sequence.unsupportedWords || [];

          // Separate signs with an eligible registered 3D animation clip from un-animated dictionary matches
          const eligibleSigns = [];
          const pendingReviewSigns = [];

          for (const s of signs) {
            const res = player.keyframeRegistry ? player.keyframeRegistry.resolveSignAnimation(s) : { resolved: false, clip: null };
            if (res.resolved && res.clip) {
              eligibleSigns.push(s);
            } else {
              pendingReviewSigns.push(s);
            }
          }

          activePipelineMetadata.eligibleCount = eligibleSigns.length;
          activePipelineMetadata.pendingReviewCount = pendingReviewSigns.length;
          activePipelineMetadata.unsupportedCount = unsupported.length;

          // Distinct Status Mapping
          if (targetLang === 'ASL') {
            activePipelineMetadata.statusState = 'UNSUPPORTED';
            telPipeStatus.innerHTML = '<span class="status-badge" style="background:#7f1d1d; color:#fca5a5;">UNSUPPORTED</span>';
            activePipelineMetadata.noticeText = 'ASL pipeline active — ASL lexical assets scheduled for M5 (no English word substitution)';
          } else if (eligibleSigns.length === 0 && pendingReviewSigns.length === 0 && unsupported.length > 0) {
            activePipelineMetadata.statusState = 'UNSUPPORTED';
            telPipeStatus.innerHTML = '<span class="status-badge" style="background:#7f1d1d; color:#fca5a5;">UNSUPPORTED</span>';
            activePipelineMetadata.noticeText = `All words unsupported [${unsupported.join(', ')}] — Zero synthetic gestures (PRD governance rule)`;
          } else if (eligibleSigns.length === 0 && pendingReviewSigns.length > 0) {
            if (unsupported.length > 0) {
              activePipelineMetadata.statusState = 'PARTIAL / UNSUPPORTED';
              telPipeStatus.innerHTML = '<span class="status-badge" style="background:#9a3412; color:#fed7aa;">PARTIAL / UNSUPPORTED</span>';
              activePipelineMetadata.noticeText = `Partial mapping: [${pendingReviewSigns.map(s => s.gloss).join(', ')}] in dictionary awaiting 3D review (no clip); [${unsupported.join(', ')}] unsupported — Neutral pose held`;
            } else {
              activePipelineMetadata.statusState = 'PENDING_REVIEW';
              telPipeStatus.innerHTML = '<span class="status-badge" style="background:#854d0e; color:#fef08a;">PENDING_REVIEW</span>';
              activePipelineMetadata.noticeText = `Dictionary matches [${pendingReviewSigns.map(s => s.gloss).join(', ')}] lack approved 3D animations (awaiting qualified review) — Neutral pose held`;
            }
          } else if (eligibleSigns.length > 0) {
            if (pendingReviewSigns.length > 0 || unsupported.length > 0) {
              activePipelineMetadata.statusState = 'PARTIAL / UNSUPPORTED';
              telPipeStatus.innerHTML = '<span class="status-badge" style="background:#9a3412; color:#fed7aa;">PARTIAL / UNSUPPORTED</span>';
              activePipelineMetadata.noticeText = `Partial playback: Articulating eligible sign [${eligibleSigns.map(s => s.gloss).join(', ')}]; unreviewed/unsupported tokens held neutral`;
            } else {
              activePipelineMetadata.statusState = 'PLAYING';
              telPipeStatus.innerHTML = '<span class="status-badge badge-playing">&#9658; PLAYING</span>';
              activePipelineMetadata.noticeText = 'Verified ISLRTC GODL v1.0 lexical sign — Experimental (awaiting Deaf-native review)';
            }
          } else {
            activePipelineMetadata.statusState = 'UNSUPPORTED';
            telPipeStatus.innerHTML = '<span class="status-badge" style="background:#7f1d1d; color:#fca5a5;">UNSUPPORTED</span>';
            activePipelineMetadata.noticeText = 'Empty sequence — Neutral rest pose held';
          }

          // Format Generated Signs distinguishing eligible playable clips from dictionary matches
          if (eligibleSigns.length > 0) {
            const eligibleStr = `${eligibleSigns.length} playable clip(s) (${eligibleSigns.map(s => s.gloss).join(', ')})`;
            if (pendingReviewSigns.length > 0) {
              telPipeSigns.textContent = `${eligibleStr} | ${pendingReviewSigns.length} dictionary match(es) (${pendingReviewSigns.map(s => s.gloss).join(', ')} — awaiting review)`;
            } else {
              telPipeSigns.textContent = eligibleStr;
            }
          } else if (pendingReviewSigns.length > 0) {
            telPipeSigns.textContent = `0 playable clips (${pendingReviewSigns.length} dictionary match(es) awaiting review: ${pendingReviewSigns.map(s => s.gloss).join(', ')})`;
          } else {
            telPipeSigns.textContent = '0 sign(s) (None)';
          }

          telPipeUnsupported.textContent = unsupported.length > 0 ? unsupported.join(', ') : 'None';
          telPipeNotice.textContent = activePipelineMetadata.noticeText;

          // Pass validated SignSequence directly to the Avatar Player
          player.playSignSequence(sequence);
          updateUI();
        } catch (err) {
          console.error('[SignBridge] Pipeline error:', err);
          activePipelineMetadata.statusState = 'ERROR';
          telPipeStatus.innerHTML = `<span class="diag-err">ERROR: ${err.message}</span>`;
          telPipeNotice.textContent = err.message;
        }
      }

      // Language selector change
      selectTargetLang.addEventListener("change", () => {
        const lang = selectTargetLang.value;
        if (lang === 'ISL') {
          pipeLangBadge.className = 'badge-isl';
          pipeLangBadge.textContent = 'TARGET: ISL';
        } else {
          pipeLangBadge.className = 'badge-asl';
          pipeLangBadge.textContent = 'TARGET: ASL (M5 STUB)';
        }
      });

      // Pipeline Button Handlers
      btnTranslatePlay.addEventListener("click", () => {
        const text = inputTranscript.value;
        const lang = selectTargetLang.value;
        executeSpeechPipeline(text, lang);
      });

      btnInterrupt.addEventListener("click", () => {
        // Simulates rapid incoming speech interrupting an in-flight sequence
        executeSpeechPipeline("Hello", selectTargetLang.value);
        statusOverlay.textContent = "Interrupted with 'Hello'";
      });

      if (btnSampleNamaste) {
        btnSampleNamaste.addEventListener("click", () => {
          inputTranscript.value = "Namaste";
          executeSpeechPipeline("Namaste", selectTargetLang.value);
        });
      }

      btnSampleHello.addEventListener("click", () => {
        inputTranscript.value = "Hello";
        executeSpeechPipeline("Hello", selectTargetLang.value);
      });

      btnSampleThankYou.addEventListener("click", () => {
        inputTranscript.value = "Thank you";
        executeSpeechPipeline("Thank you", selectTargetLang.value);
      });

      btnSampleMixed.addEventListener("click", () => {
        inputTranscript.value = "Hello world";
        executeSpeechPipeline("Hello world", selectTargetLang.value);
      });

      btnSampleMulti.addEventListener("click", () => {
        inputTranscript.value = "Welcome please";
        executeSpeechPipeline("Welcome please", selectTargetLang.value);
      });

      btnSampleUnknown.addEventListener("click", () => {
        inputTranscript.value = "Computer internet";
        executeSpeechPipeline("Computer internet", selectTargetLang.value);
      });

      btnSampleEmpty.addEventListener("click", () => {
        inputTranscript.value = "";
        executeSpeechPipeline("", selectTargetLang.value);
      });

      btnSampleDemoCombo.addEventListener("click", () => {
        // Combination sequence: Tech motion clip followed by un-animated gloss
        const C = window.SignBridgeContracts;
        const comboSequence = C.createSignSequence({
          sequenceId: 'seq-combo-demo-' + Date.now(),
          language: 'ISL',
          rawTranscript: 'Tech Motion + Hello',
          sourceChunkSeq: 0,
          startMediaTimeMs: 0,
          endMediaTimeMs: 3000,
          signs: [
            C.createSignItem({
              gloss: 'TECHNICAL_TEST_MOTION',
              category: 'lexical',
              durationMs: 2000,
              source: 'seed_dictionary',
              animationId: 'tech_test_motion_v1'
            }),
            C.createSignItem({
              gloss: 'HELLO',
              category: 'lexical',
              durationMs: 1000,
              source: 'seed_dictionary'
            })
          ],
          fingerspellingApplied: false,
          grammarApplied: false,
          unsupportedWords: ['demo_word']
        });
        inputTranscript.value = "Tech Motion + Hello";
        telPipeTranscript.textContent = '"Tech Motion + Hello (Deterministic Combo)"';
        telPipeLang.textContent = 'ISL';
        activePipelineMetadata.statusState = 'COMBO';
        activePipelineMetadata.noticeText = 'Synthetic technical motion + neutral fallback test';
        telPipeStatus.innerHTML = '<span class="diag-ok">COMBO TEST SEQUENCE</span>';
        telPipeSeqId.textContent = comboSequence.sequenceId;
        telPipeSigns.textContent = '2 signs (TECHNICAL_TEST_MOTION [Clip], HELLO [Neutral Fallback])';
        telPipeUnsupported.textContent = 'demo_word';
        player.playSignSequence(comboSequence);
        updateUI();
      });

      if (btnSampleDailyRoutine) {
        btnSampleDailyRoutine.addEventListener("click", () => {
          const sampleText = "I walk to the bathroom to wash my face and brush my teeth.";
          inputTranscript.value = sampleText;
          telPipeTranscript.textContent = `"${sampleText}" (Daily Routine 01:35–01:55 Segment)`;
          telPipeLang.textContent = 'ISL';
          activePipelineMetadata.statusState = 'UNREVIEWED CANDIDATE';
          activePipelineMetadata.noticeText = 'PROVISIONAL UNAPPROVED CANDIDATE: NOT a validated ISL translation. Strictly requires review by 3 qualified Deaf-native ISL linguists. Zero synthetic gestures enforced.';
          telPipeStatus.innerHTML = '<span class="status-badge" style="background:#9a3412; color:#fed7aa;">UNREVIEWED CANDIDATE (0/3 Reviews)</span>';
          telPipeSeqId.textContent = 'daily_routine_seg_01 (01:38–01:46 / 98000–106000ms)';
          telPipeSigns.textContent = '0 playable clips (1 dictionary match: I [un-animated]; 6 out-of-lexicon words: walk, bathroom, wash, face, brush, teeth)';
          telPipeUnsupported.textContent = 'walk, bathroom, wash, face, brush, teeth';
          telPipeNotice.textContent = activePipelineMetadata.noticeText;
          if (bridgeLiveTranscript) bridgeLiveTranscript.textContent = `"${sampleText}"`;
          if (bridgeStatusBadge) {
            bridgeStatusBadge.className = "badge-isl";
            bridgeStatusBadge.style.background = "#1e3a8a";
            bridgeStatusBadge.style.color = "#93c5fd";
            bridgeStatusBadge.textContent = "PROTOTYPE: ACTIVE";
          }
          if (bridgeRoutingStatus) {
            bridgeRoutingStatus.textContent = "⚠ Daily Routine Segment (01:35–01:55): Unapproved candidate glosses — NOT a validated ISL translation (0/3 reviews); 0% animated, neutral rest pose held";
            bridgeRoutingStatus.style.color = "#facc15";
          }
          player.resetToNeutralPose();
          updateUI();
        });
      }

      // Check Whisper local backend with explicit timeout and error reporting
      let activeHealthCheckId = 0;
      let isHealthCheckInFlight = false;

      async function checkWhisperBackendHealth() {
        if (!telWhisperBackend) return;
        if (isHealthCheckInFlight) {
          console.info('[SignBridge Diagnostics] Health check already in flight. Skipping overlapping trigger.');
          return;
        }

        const checkId = ++activeHealthCheckId;
        isHealthCheckInFlight = true;
        if (btnCheckBackend) btnCheckBackend.disabled = true;

        telWhisperBackend.textContent = 'Polling http://127.0.0.1:8765/health...';
        telWhisperBackend.style.color = '#38bdf8';

        const HEALTH_TIMEOUT_MS = 5000;
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);

        try {
          const resp = await fetch('http://127.0.0.1:8765/health', {
            method: 'GET',
            mode: 'cors',
            signal: controller.signal
          });
          clearTimeout(timeoutId);

          if (checkId !== activeHealthCheckId) return; // Stale check guard

          if (resp.ok) {
            const data = await resp.json();
            if (data && data.status === 'ok') {
              const service = data.service || 'fastapi';
              const ver = data.version ? `v${data.version}` : '';
              const model = data.model ? `model: ${data.model}` : 'tiny.en';
              const device = data.device ? `${data.device}/${data.compute_type || 'int8'}` : 'cpu';
              telWhisperBackend.innerHTML = `<span class="diag-ok">&#10004; Online (${service} ${ver}, ${model}, ${device})</span>`;
            } else {
              telWhisperBackend.innerHTML = `<span class="diag-warn">Offline (Malformed health response from backend)</span>`;
            }
          } else {
            telWhisperBackend.innerHTML = `<span class="diag-warn">Offline (HTTP ${resp.status} ${resp.statusText || 'Error'} from 127.0.0.1:8765)</span>`;
          }
        } catch (e) {
          clearTimeout(timeoutId);
          if (checkId !== activeHealthCheckId) return; // Stale check guard

          const isTimeout = e.name === 'AbortError';
          const isConnRefused = e.message && (e.message.includes('Failed to fetch') || e.message.includes('NetworkError'));
          let detail = e.message || 'Unknown error';
          if (isTimeout) {
            detail = `Request timed out after ${HEALTH_TIMEOUT_MS}ms (Backend busy or slow)`;
          } else if (isConnRefused) {
            detail = 'Connection refused (Backend offline on 127.0.0.1:8765 — Run backend server)';
          }
          telWhisperBackend.innerHTML = `<span class="diag-warn">Offline / Inactive (${detail})</span>`;
        } finally {
          isHealthCheckInFlight = false;
          if (btnCheckBackend) btnCheckBackend.disabled = false;
        }
      }

      window.checkWhisperBackendHealth = checkWhisperBackendHealth;

      btnCheckBackend.addEventListener("click", () => {
        checkWhisperBackendHealth();
      });

      // Query initial health on load
      checkWhisperBackendHealth();

      // Standard Viewport Button Handlers
      btnPlay.addEventListener("click", () => {
        player.playClip(K.TECHNICAL_TEST_CLIP);
        updateUI();
      });

      btnPause.addEventListener("click", () => {
        player.pause();
        updateUI();
      });

      btnResume.addEventListener("click", () => {
        player.resume();
        updateUI();
      });

      btnRestart.addEventListener("click", () => {
        player.restart();
        updateUI();
      });

      btnNeutral.addEventListener("click", () => {
        player.resetToNeutralPose();
        updateUI();
      });

      btnMissing.addEventListener("click", () => {
        // Intentionally passes null to test safe fallback
        const res = player.playClip(null);
        statusOverlay.textContent = "Tested null clip -> Fallback to Neutral";
        updateUI();
      });

      btnUnreg.addEventListener("click", () => {
        // Tests dictionary gloss 'HELLO' which has no registered 3D clip
        const res = player.playSignItem({ gloss: "HELLO", category: "lexical", durationMs: 750, source: "seed_dictionary" });
        statusOverlay.textContent = "Unregistered sign -> Safe Neutral Fallback";
        updateUI();
      });

      // -----------------------------------------------------------------------
      // Milestone M4: Live Tab Audio & Extension Bridge Implementation
      // -----------------------------------------------------------------------
      let activeSessionId = null;
      let lastProcessedSeqId = 0;

      const bridgeStatusBadge = document.getElementById("bridge-status-badge");
      const bridgeSessionId = document.getElementById("bridge-session-id");
      const bridgeLiveTranscript = document.getElementById("bridge-live-transcript");
      const bridgeConfidence = document.getElementById("bridge-confidence");
      const bridgeChunkSeq = document.getElementById("bridge-chunk-seq");
      const bridgeRoutingStatus = document.getElementById("bridge-routing-status");

      function handleLiveTranscriptDispatch(payload) {
        if (!payload || payload.version !== "1.0.0") return;

        // Session recovery / verification
        if (!activeSessionId) {
          activeSessionId = payload.sessionId;
          lastProcessedSeqId = 0;
        } else if (payload.sessionId && payload.sessionId !== activeSessionId) {
          console.warn(`[SignBridge Avatar Bridge] Received transcript from mismatched session '${payload.sessionId}' (active: '${activeSessionId}'). Dropping.`);
          return;
        }

        // Monotonic sequence check (Strict De-duplication and Order Enforcement)
        if (typeof payload.sequenceId === "number") {
          if (payload.sequenceId <= lastProcessedSeqId) {
            console.warn(`[SignBridge Avatar Bridge] Dropping duplicate or out-of-order chunk #${payload.sequenceId} (last processed: #${lastProcessedSeqId})`);
            return;
          }
          lastProcessedSeqId = payload.sequenceId;
        }

        // Update Bridge Telemetry UI
        if (bridgeStatusBadge) {
          bridgeStatusBadge.className = "badge-isl";
          bridgeStatusBadge.style.background = "#065f46";
          bridgeStatusBadge.style.color = "#6ee7b7";
          bridgeStatusBadge.textContent = "CAPTURE: ACTIVE";
        }
        if (bridgeSessionId) {
          bridgeSessionId.textContent = payload.sessionId || "Active Session";
        }
        if (bridgeChunkSeq) {
          const timeSec = payload.timestamp ? payload.timestamp.toFixed(1) : "0.0";
          const durSec = payload.duration ? payload.duration.toFixed(1) : "2.0";
          bridgeChunkSeq.textContent = `#${payload.sequenceId} (${timeSec}s, ${durSec}s slice)`;
        }

        const rawText = (payload.text || "").trim();
        if (bridgeLiveTranscript) {
          bridgeLiveTranscript.textContent = rawText ? `"${rawText}"` : "[Silence / No Speech Detected]";
        }

        // Confidence reporting: ONLY if backend provides a valid confidence value
        if (bridgeConfidence) {
          if (typeof payload.confidence === "number" && !isNaN(payload.confidence)) {
            const pct = Math.round(payload.confidence * 100);
            if (payload.confidence < 0.60) {
              bridgeConfidence.style.color = "#f87171";
              bridgeConfidence.textContent = `${pct}% (Low ASR Confidence)`;
            } else {
              bridgeConfidence.style.color = "#34d399";
              bridgeConfidence.textContent = `${pct}%`;
            }
          } else {
            bridgeConfidence.textContent = "--";
            bridgeConfidence.style.color = "#94a3b8";
          }
        }

        // Silence / Empty Audio Handling: Do NOT animate; maintain neutral pose
        if (!rawText) {
          if (bridgeRoutingStatus) {
            bridgeRoutingStatus.textContent = "Silence detected — Holding neutral rest pose (zero gestures)";
            bridgeRoutingStatus.style.color = "#94a3b8";
          }
          if (player) {
            if (!player.isPlaying || !player.currentClip) {
              player.resetToNeutralPose();
              updateUI();
            }
          }
          return;
        }

        // Update manual input box to reflect live transcript
        inputTranscript.value = rawText;

        // Execute Speech-to-Sign Pipeline
        const targetLang = selectTargetLang ? selectTargetLang.value : "ISL";
        executeSpeechPipeline(rawText, targetLang);

        // Update Bridge Routing Status based on sequence outcome
        if (bridgeRoutingStatus && player && player.activeSequence) {
          const signs = player.activeSequence.signs || [];
          const unsupported = player.activeSequence.unsupportedWords || [];

          if (signs.length > 0) {
            const hasNamaste = signs.some(s => s.gloss === "NAMASTE");
            const unreviewedGlosses = signs.filter(s => s.gloss !== "NAMASTE").map(s => s.gloss);

            if (hasNamaste) {
              if (unreviewedGlosses.length > 0) {
                bridgeRoutingStatus.textContent = `✔ Articulating ISL Namaste (ISLRTC GODL v1.0 Baseline) | [${unreviewedGlosses.join(", ")}] awaiting qualified review`;
              } else {
                bridgeRoutingStatus.textContent = "✔ Articulating ISL Namaste (ISLRTC GODL v1.0 Baseline)";
              }
              bridgeRoutingStatus.style.color = "#34d399";
            } else {
              if (unsupported.length > 0) {
                bridgeRoutingStatus.textContent = `⚠ Words in dictionary, 3D animation awaiting qualified review [${signs.map(s => s.gloss).join(', ')}]; Out-of-lexicon words: [${unsupported.join(", ")}] — neutral pose held`;
              } else {
                bridgeRoutingStatus.textContent = `⚠ Words in dictionary, 3D animation awaiting qualified review — neutral pose held [${signs.map(s => s.gloss).join(', ')}]`;
              }
              bridgeRoutingStatus.style.color = "#facc15";
            }
          } else if (unsupported.length > 0) {
            bridgeRoutingStatus.textContent = `⚠ Out-of-lexicon words: [${unsupported.join(", ")}] — Neutral pose held (PRD: Zero synthetic gestures)`;
            bridgeRoutingStatus.style.color = "#fca5a5";
          }
        }
      }

      function handleCaptureStopped(payload) {
        activeSessionId = null;
        lastProcessedSeqId = 0;
        webPollEnabled = false;
        if (bridgeStatusBadge) {
          bridgeStatusBadge.className = "badge-isl";
          bridgeStatusBadge.style.background = "#1e293b";
          bridgeStatusBadge.style.color = "#94a3b8";
          bridgeStatusBadge.textContent = "CAPTURE: IDLE";
        }
        if (bridgeRoutingStatus) {
          bridgeRoutingStatus.textContent = "Capture session stopped — Avatar at neutral rest pose";
          bridgeRoutingStatus.style.color = "#94a3b8";
        }
        if (player) {
          player.resetToNeutralPose();
          updateUI();
        }
      }

      function handleCaptureStarted(payload) {
        activeSessionId = payload.sessionId || null;
        lastProcessedSeqId = 0;
        webPollEnabled = true;
        if (bridgeStatusBadge) {
          bridgeStatusBadge.className = "badge-isl";
          bridgeStatusBadge.style.background = "#065f46";
          bridgeStatusBadge.style.color = "#6ee7b7";
          bridgeStatusBadge.textContent = "CAPTURE: ACTIVE";
        }
        if (bridgeSessionId) {
          bridgeSessionId.textContent = activeSessionId || "Active";
        }
        if (bridgeRoutingStatus) {
          bridgeRoutingStatus.textContent = "Audio capture active in tab — Listening for speech...";
          bridgeRoutingStatus.style.color = "#38bdf8";
        }
        if (player) {
          player.resetToNeutralPose();
          updateUI();
        }
      }

      // Expose handlers on window for browser test harnesses / deterministic E2E verification
      window.handleLiveTranscriptDispatch = handleLiveTranscriptDispatch;
      window.handleCaptureStopped = handleCaptureStopped;
      window.handleCaptureStarted = handleCaptureStarted;

      function initExtensionBridge() {
        if (typeof chrome === "undefined" || !chrome.runtime || !chrome.runtime.onMessage) {
          console.info("[SignBridge Avatar Bridge] Chrome runtime unavailable (running in standalone browser mode).");
          return;
        }

        // Listen for runtime broadcasts from service worker
        chrome.runtime.onMessage.addListener((message) => {
          if (!message || !message.type) return;

          if (message.type === "SIGNBRIDGE_TRANSCRIPTION_DISPATCH") {
            handleLiveTranscriptDispatch(message);
          } else if (message.type === "SIGNBRIDGE_CAPTURE_STOPPED") {
            handleCaptureStopped(message);
          } else if (message.type === "SIGNBRIDGE_CAPTURE_STARTED") {
            handleCaptureStarted(message);
          }
        });

        // Listen for session storage changes
        if (chrome.storage && chrome.storage.session) {
          chrome.storage.session.onChanged.addListener((changes) => {
            if (changes.captureState && changes.captureState.newValue) {
              const state = changes.captureState.newValue;
              if (state.status === "idle" && activeSessionId) {
                handleCaptureStopped({ reason: "Session state transitioned to idle" });
              }
            }
          });

          // Recover initial state in case player was opened while capture is ALREADY running
          chrome.storage.session.get("captureState").then((data) => {
            const state = data ? data.captureState : null;
            if (state && state.status === "capturing") {
              console.info("[SignBridge Avatar Bridge] Connecting to running capture session:", state.sessionId);
              activeSessionId = state.sessionId;
              lastProcessedSeqId = state.lastProcessedSequenceId || 0;
              if (bridgeStatusBadge) {
                bridgeStatusBadge.className = "badge-isl";
                bridgeStatusBadge.style.background = "#065f46";
                bridgeStatusBadge.style.color = "#6ee7b7";
                bridgeStatusBadge.textContent = "CAPTURE: ACTIVE";
              }
              if (bridgeSessionId) {
                bridgeSessionId.textContent = activeSessionId;
              }
              if (bridgeLiveTranscript && state.latestTranscript) {
                bridgeLiveTranscript.textContent = `"${state.latestTranscript}"`;
              }
              if (bridgeRoutingStatus) {
                bridgeRoutingStatus.textContent = "Connected to running tab capture — Awaiting next speech chunk";
                bridgeRoutingStatus.style.color = "#38bdf8";
              }
            }
          }).catch(() => {});
        }
      }

      // Initialize Extension Bridge
      initExtensionBridge();

      // Fallback bridge for Web-Origin Test Viewers (e.g. http://localhost:8080)
      let lastPolledSeqId = -1;
      let webPollEnabled = true;

      async function pollLocalBackendTranscript() {
        if (typeof chrome !== 'undefined' && chrome.storage) return; // Use native extension bridge if available
        if (!webPollEnabled) return;
        try {
          const res = await fetch("http://127.0.0.1:8765/api/transcript/latest");
          if (res.status === 200) {
            const data = await res.json();
            if (data && data.text && typeof data.sequence_id === "number") {
              if (data.sequence_id === lastPolledSeqId) return;
              lastPolledSeqId = data.sequence_id;
              handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "web_poll_session",
                sequenceId: data.sequence_id,
                timestamp: data.timestamp || 0,
                duration: data.duration || 2.0,
                text: data.text,
                confidence: data.confidence || null,
                metrics: data.metrics || {}
              });
            }
          }
        } catch (_) {
          // Backend offline or waiting for audio
        }
      }
      setInterval(pollLocalBackendTranscript, 500);
    });
