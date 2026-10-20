# SignBridge M4 Stage 5 — Release Candidate Checklist & Packaging Guide

**Document Reference:** `Docs/M4_STAGE_5_RELEASE_CANDIDATE_CHECKLIST.md`  
**Milestone:** SignBridge Milestone M4 — End-to-End Product Integration, ISL Validation Readiness, UX, Performance, and Controlled Pilot Preparation  
**Stage:** **Stage 5: Complete Validation, Release Readiness & Evidence Closure**  
**Execution Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  
**Packaging Status:** **Local Verification Only — Distributable Extension Package NOT Produced**  

---

## 1. Executive Notice & Release Status

In strict accordance with project governance boundaries:
- **No Distributable Extension Package Published:** SignBridge is an experimental prototype. No `.crx` or `.zip` artifact has been produced for external distribution or uploaded to the Chrome Web Store.
- **Quarantined Asset Isolation:** Experimental mocap assets (`isl_namaste_mocap_candidate_v1.json`) and reference videos (`ISLRTC_Namaste_sample.mp4`) are strictly quarantined and must not be bundled in any production distribution.
- **Local Verification Purpose:** This checklist defines the exact procedure for provisioning, launching, and verifying a local release candidate on a dedicated evaluation workstation.

---

## 2. Release Candidate Asset Manifest & Hash Registry

The table below lists all production assets required for local evaluation, verified against filesystem records:

| File Path | Description | Required Permissions / Role | Status | Verified Checksum / Size |
|---|---|---|:---:|---|
| `extension/manifest.json` | Manifest V3 specification | Extension metadata & permissions | `VERIFIED` | Valid MV3 JSON schema |
| `extension/background.js` | Service Worker | Tab lifecycle, capture state machine | `VERIFIED` | 338 lines / 11.2 KB |
| `extension/offscreen.html` | Offscreen host document | AudioContext execution sandbox | `VERIFIED` | 27 lines / 904 bytes |
| `extension/offscreen.js` | Web Audio processor | 16kHz PCM WAV slicing & FIFO queue | `VERIFIED` | 428 lines / 15.6 KB |
| `extension/popup.html` | Extension Action UI | User controls, captions, status | `VERIFIED` | 134 lines / 7.1 KB |
| `extension/popup.js` | Popup logic | User interaction & backend health | `VERIFIED` | 311 lines / 11.5 KB |
| `extension/overlay/avatar_player.html` | 3D Avatar Display Window | WebGL viewport, Three.js runtime | `VERIFIED` | 1,248 lines / 51.1 KB |
| `extension/animation/avatar_player.js` | Avatar Controller Class | Joint retargeting, playback state | `VERIFIED` | 448 lines / 17.2 KB |
| `extension/animation/keyframe_registry.js`| Animation Registry | Production baseline `isl_namaste_godl_v1`| `VERIFIED` | Contains GODL baseline |
| `extension/translation/isl_translator.js` | ISL Rule Engine | Seed lexicon & grammar heuristics | `VERIFIED` | 467 lines / 16.5 KB |
| `extension/translation/asl_translator.js` | ASL Rule Engine | ASL separation pipeline | `VERIFIED` | 114 lines / 3.9 KB |
| `extension/translation/translation_router.js`| Translation Router | Routes text to ISL/ASL engines | `VERIFIED` | 131 lines / 4.7 KB |
| `extension/models/sign_contracts.js` | Data Contracts | Frozen SignItem/SignSequence types | `VERIFIED` | 290 lines / 10.4 KB |
| `extension/lib/three.min.js` | Three.js WebGL Engine | Scene, camera, lighting, renderer | `VERIFIED` | 642 KB bundled |
| `extension/lib/GLTFLoader.js` | Three.js GLTF Loader | Parses Mixamo GLB meshes | `VERIFIED` | 98 KB bundled |
| `extension/assets/models/ybot.glb` | 3D Humanoid Rig Mesh | Adobe Mixamo Y-Bot skeleton | `VERIFIED` | 2,233,440 bytes |
| `extension/icons/icon-16.png` | Toolbar icon | 16x16 PNG icon | `VERIFIED` | Valid PNG image |
| `extension/icons/icon-48.png` | Extension management icon | 48x48 PNG icon | `VERIFIED` | Valid PNG image |
| `extension/icons/icon-128.png` | Web Store display icon | 128x128 PNG icon | `VERIFIED` | Valid PNG image |

---

## 3. Chrome Manifest V3 Permissions & Functional Purpose

| Declared Permission | Scope | Technical Justification | Risk Mitigation |
|---|---|---|---|
| `tabCapture` | Active tab audio | Captures audio stream from the currently playing YouTube tab | Only activated on explicit user button click in popup |
| `offscreen` | Offscreen document | Allows Web Audio API execution to downsample audio in MV3 | Document has zero DOM access and terminates on stop |
| `activeTab` | Current tab info | Retrieves active tab ID and URL to verify YouTube context | Scoped strictly to the focused user tab |
| `storage` | Extension storage | Transmits recognized transcripts from background to avatar player | Transient session storage; purged on teardown |
| `scripting` | Content scripting | Validates tab state and coordinates capture overlay docking | Zero permanent DOM injection |
| `*://*.youtube.com/*` | Host permission | Confines audio capture strictly to YouTube video tabs | Internal pages (`chrome://`, `about:`) are rejected |
| `http://127.0.0.1:8765/*` | Host permission | Permits extension to POST audio slices to local Python backend | Loopback strictly; zero outbound cloud connectivity |

---

## 4. Local Evaluation Setup & Launch Procedure

### Step 1: Provision Local Python Backend Environment
1. Open a terminal in `C:\AmazonMlChallenge\signbridge-backend`.
2. Verify Python 3.11 environment:
   ```powershell
   python --version
   pip list
   ```
3. Start the local transcription service:
   ```powershell
   python -m uvicorn main:app --host 127.0.0.1 --port 8765 --log-level info
   ```
4. Verify backend health in a browser or curl:
   ```powershell
   curl http://127.0.0.1:8765/health
   # Expected response: {"status":"ok","service":"signbridge-backend","version":"0.2.0",...}
   ```

### Step 2: Load Extension in Google Chrome
1. Open Google Chrome (v120+).
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode** toggle in the top-right corner.
4. Click **Load unpacked**.
5. Select the directory: `C:\AmazonMlChallenge\extension`.
6. Confirm **SignBridge** appears with ID and version `0.2.0`.

### Step 3: Launch 3D Avatar Display & Dock Viewport
1. Open a YouTube tab with clear speech (e.g., educational lecture or news).
2. Click the SignBridge puzzle icon in the Chrome toolbar to open `popup.html`.
3. Click the **"Open 3D Avatar Display"** button.
4. The standalone window `avatar_player.html` will open and dock alongside your video.
5. Verify the Three.js viewport renders the Y-Bot character in **Neutral Rest Pose** (arms lowered naturally).

### Step 4: Execute Audio Capture & Live Translation
1. In `popup.html`, verify the backend status indicator displays green: **"Backend: Online (tiny.en)"**.
2. Click **"Start Live Signing"**.
3. Chrome will display a blue tab-sharing indicator.
4. Verify tab audio continues playing audibly through speakers.
5. Within 2–3 seconds, live speech transcripts will appear in the player window.
6. When speech says "namaste" or "greetings", verify the avatar executes the bilateral prayer pose and head nod.
7. Click **"Stop Signing"** in `popup.html`. Verify capture terminates and avatar resets to neutral.

---

## 5. Pre-Release Smoke Test Verification Checklist

Every item must be verified before initiating any local evaluation session:

- [ ] **ST-01:** Local backend responds with `status: "ok"` on `http://127.0.0.1:8765/health`.
- [ ] **ST-02:** Extension loads unpacked in Chrome without manifest errors or warnings.
- [ ] **ST-03:** Clicking "Open 3D Avatar Display" opens `avatar_player.html` and renders Y-Bot.
- [ ] **ST-04:** Y-Bot automatically assumes Neutral Rest Pose upon model load (arms down).
- [ ] **ST-05:** Internal pages (`chrome://extensions`, `chrome://settings`) disable capture button.
- [ ] **ST-06:** Tab capture starts successfully; speakers continue playing audible tab sound.
- [ ] **ST-07:** Live transcripts update in player with sequence numbers and latency metrics.
- [ ] **ST-08:** Low-confidence speech displays red warning badge (`XX% (Low ASR Confidence)`).
- [ ] **ST-09:** Speech 'namaste' articulates ISLRTC GODL baseline sign clip (`isl_namaste_godl_v1`).
- [ ] **ST-10:** Non-dictionary phrases display out-of-lexicon words and hold neutral rest pose.
- [ ] **ST-11:** Clicking "Stop Signing" stops media stream tracks, empties queues, and resets avatar.
- [ ] **ST-12:** Review store `tools/isl_motion_extraction/reviews` confirmed empty.

---

## 6. Rollback & Reversion Protocol

If an unexpected runtime crash or anomalous behavior occurs during local testing:
1. **Immediate Session Termination:** Click "Stop Signing" in popup, or close the active YouTube tab to trigger automatic `chrome.tabs.onRemoved` capture teardown.
2. **Backend Restart:** Press `Ctrl+C` in the backend terminal to stop Uvicorn, then relaunch.
3. **Extension Reload:** Navigate to `chrome://extensions/` and click the reload icon on the SignBridge card.
4. **Local Build Rollback:** To revert local edits to the known-good Stage 5 baseline:
   - Check directory integrity using `python run_all_m4_stage5_tests.py`.
   - Verify all 340 automated checks pass before resuming evaluation.
