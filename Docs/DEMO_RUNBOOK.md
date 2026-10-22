# SignBridge — Prototype Demonstration Runbook

**Milestone:** Final Prototype Freeze & Demonstration Handoff  
**Workspace:** `C:\Users\HP\OneDrive\Desktop\PROJECTS\Smriti_SignBridge`  
**Date:** October 2026  
**Status:** Frozen Prototype / Demonstration-Ready  

---

## 1. System Overview & Architecture

SignBridge is an experimental Chrome extension and local ASR backend providing speech-to-Indian Sign Language (ISL) visualization via a 3D avatar.

### Architectural Components
1. **Local Speech Recognition Backend (`signbridge-backend`)**:
   - Python 3.10+ FastAPI service running `faster-whisper` (`tiny.en`, CPU int8).
   - Standard endpoint: `http://127.0.0.1:8765`.
   - Health check: `GET http://127.0.0.1:8765/health`.
   - Transcription endpoint: `POST http://127.0.0.1:8765/transcribe`.
2. **Chrome Extension (Manifest V3)**:
   - Location: `extension/`.
   - Offscreen document (`offscreen.html` / `offscreen.js`) for tab audio capture via `chrome.tabCapture`.
   - Popup interface (`popup.html` / `popup.js`) for bridge control, live telemetry, and translation status.
   - Dedicated 3D Avatar Player overlay (`overlay/avatar_player.html` / `overlay/avatar_player_controller.js`) powered by Three.js and Y-Bot GLB.
   - Zero-dependency contract and translation layer (`models/sign_contracts.js`, `translation/isl_translator.js`, `translation/translation_router.js`).
   - Skeletal keyframe registry (`animation/keyframe_registry.js`) enforcing ISL governance.

---

## 2. Startup Instructions

### Step 2.1 — Start the Local Whisper ASR Backend

1. Open a new PowerShell terminal on Windows.
2. Navigate to the backend directory:
   ```powershell
   cd "C:\Users\HP\OneDrive\Desktop\PROJECTS\Smriti_SignBridge\signbridge-backend"
   ```
3. Activate the virtual environment (if using venv) or use Python directly:
   ```powershell
   python run.py
   ```
   *Expected console output:*
   ```text
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Loading Whisper model: tiny.en (device=cpu, compute_type=int8)
   INFO:     Whisper model loaded successfully.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://127.0.0.1:8765 (Press CTRL+C to quit)
   ```
4. Verify backend health in browser or PowerShell:
   ```powershell
   curl http://127.0.0.1:8765/health
   ```
   *Expected response:*
   ```json
   {"status":"ok","service":"signbridge-backend","version":"0.2.0","model":"tiny.en","device":"cpu","compute_type":"int8","uptime_seconds":...}
   ```

### Step 2.2 — Load the Chrome Extension

1. Launch Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode** (toggle in upper right corner).
4. Click **Load unpacked** (top left).
5. Select the folder:
   `C:\Users\HP\OneDrive\Desktop\PROJECTS\Smriti_SignBridge\extension`
6. Confirm the extension appears with title **SignBridge - Speech-to-ISL** (Version 0.2.0 or 1.0.0) and inspect views shows background service worker (`background.js`).
7. Pin the SignBridge extension to the Chrome toolbar for quick access.

### Step 2.3 — Launch the 3D Avatar Player

1. In Chrome, open a new tab and navigate to:
   ```text
   chrome-extension://<EXTENSION_ID>/overlay/avatar_player.html
   ```
   *(Or click "Open Avatar Player" directly from the extension popup).*
2. Verify the 3D viewport renders:
   - Adobe Mixamo Y-Bot 3D model loads (`ybot.glb`, 2.2 MB).
   - SkinnedMesh initializes with 65 canonical joints mapped.
   - Initial pose lowers arms naturally into `pose_neutral_rest_v1` (arms down at sides, fingers relaxed).
   - Status badge in top right displays: `● IDLE` or `NEUTRAL`.
   - Governance banner displays: `Experimental ISL — Awaiting Human Panel Validation`.

---

## 3. Demonstration 1 — Real ISL Namaste Benchmark

This benchmark demonstrates the verified vertical slice: speech recognition mapping to the officially sourced ISLRTC GODL v1.0 Namaste baseline animation.

### Step-by-Step Procedure
1. Ensure the Avatar Player window (`avatar_player.html`) is visible on screen.
2. Open a media tab with clear English speech saying "Namaste" or "Greetings" (e.g. YouTube or local audio file), OR open the extension popup.
3. Open the SignBridge popup:
   - Click the extension icon.
   - Verify backend status displays: `✔ Online (signbridge-backend v0.2.0, model: tiny.en, cpu/int8)`.
4. Click **Start Tab Capture & Bridge**:
   - The status changes to `CAPTURE: ACTIVE`.
5. Play audio of the word: `"Namaste"`.
6. Observe the Avatar Player:
   - **Incoming transcript rendered:** `"namaste"`.
   - **Routing status updates:** `✔ Articulating ISL Namaste (ISLRTC GODL v1.0 Baseline)`.
   - **Animation Clip:** `isl_namaste_godl_v1` (1800 ms duration).
   - **Visual Kinematics:**
     - Both hands rise synchronously from neutral rest pose toward the chest.
     - Palms join in bilateral anjali mudra (prayer pose).
     - Head performs a slight reverent nod.
     - Hands separate and smoothly return to neutral rest pose at sides.
   - **Playback Telemetry:**
     - During playback: State badge displays `► PLAYING`, title displays `NAMASTE — isl_namaste_godl_v1 (1800 ms)`, progress bar tracks from `0%` to `100%`.
     - Upon completion (at 1800 ms): Badge displays `✔ COMPLETED`, title displays `NAMASTE — isl_namaste_godl_v1 (1800 ms) — COMPLETED`.
7. In the popup UI:
   - Translation status displays: `TRANSLATED`.
   - Generated signs: `1 sign(s) (NAMASTE)`.
   - Unsupported words: `(none)`.

---

## 4. Demonstration 2 — Safe Fallback for Unsupported Input

This demonstration highlights SignBridge's core safety and ethical governance: out-of-lexicon words and un-animated dictionary entries strictly hold a neutral rest pose rather than inventing fake 3D gestures.

### Demonstration 2A: Out-of-Lexicon English Input
1. With the bridge active, play audio or speak an unsupported sentence:
   ```text
   "She makes me very, very proud."
   ```
   *(Or: `"quantum computing rocket"`)*
2. Observe the Avatar Player:
   - **Transcript displayed:** `"She makes me very, very proud."`
   - **Routing Status:**
     `⚠ Out-of-lexicon words: [she, makes, very, very, proud] — Neutral pose held (PRD: Zero synthetic gestures)`
   - **Avatar Behavior:** The avatar **remains motionless** at neutral rest pose.
   - **Playback Telemetry:**
     - Badge displays: `NEUTRAL`.
     - Title displays: `Neutral Rest Pose (0 ms)`.
     - Progress bar remains at `0%`.
     - No synthetic or arbitrary arm movements occur.
3. In the popup UI:
   - Translation status displays: `PARTIAL / UNSUPPORTED` or `UNSUPPORTED`.
   - Playable clips: `0 playable clips`.
   - Unsupported words explicitly listed: `she, makes, very, very, proud`.
   - Governance notice: `Partial mapping: [I] in dictionary awaiting 3D review (no clip); [she, makes, very, very, proud] unsupported — Neutral pose held`.

### Demonstration 2B: Dictionary Match Awaiting 3D Review
1. Provide audio for a word in the dictionary that does not yet have an approved 3D animation clip:
   ```text
   "Thank you"
   ```
   *(Or `"Hello"`)*
2. Observe the Avatar Player:
   - **Transcript displayed:** `"thank you"`
   - **Routing Status:**
     `⚠ Words in dictionary, 3D animation awaiting qualified review — neutral pose held [THANK_YOU]`
   - **Avatar Behavior:** Holds neutral rest pose for 500 ms safety buffer, then completes.
   - **Telemetry:** Title displays `Neutral Rest Pose (0 ms)`, badge displays `NEUTRAL`, progress bar displays `0%`.
   - **Integrity Guarantee:** Never fabricates hand gestures for unreviewed vocabulary.

---

## 5. Demonstration 3 — Daily Routine (01:35–01:55) Single-Video Prototype

This demonstration executes the controlled single-video pipeline on the selected A1 English learning segment.

### Video & Window Information
- **Source Video:** [YouTube `sMkzwmMs0jM`](https://www.youtube.com/watch?v=sMkzwmMs0jM) (*"Daily Routine | A1 English | Talk About Your Day"*)
- **Target Segment:** `01:35.00 – 01:55.00` (Media Time: `95,000 ms – 115,000 ms`, Duration: `20.0s`)
- **Verified Dialogue in Segment:**
  1. `01:38.00 – 01:46.00`: *"I walk to the bathroom to wash my face and brush my teeth."*
  2. `01:46.00 – 01:52.00`: *"After that, I go back to my bedroom to get dressed."*
- **Licensing Constraint (LEGAL-01):** Stream audio directly from YouTube in Chrome; do not download, record, or redistribute video files.

### Demonstration Procedure (Live Audio Capture)
1. Ensure the backend is running (`http://127.0.0.1:8765/health` returns `200 ok`).
2. In Google Chrome, open the YouTube video in a tab: `https://www.youtube.com/watch?v=sMkzwmMs0jM`.
3. Pause the video and seek to timestamp **`01:35`**.
4. Open the Avatar Player in an adjacent window or tab (`overlay/avatar_player.html`).
5. Open the SignBridge extension popup and click **"Start Tab Capture & Bridge"**. Status updates to `CAPTURE: ACTIVE`.
6. Resume playback on the YouTube tab and let it play from **`01:35` to `01:55`** (20 seconds), then pause.
7. **Observe Real-Time Pipeline Observations:**
   - **Audio Pipeline:** Tab audio streams to the local Whisper backend in 2-second slices without interrupting audible playback.
   - **Transcription Telemetry:**
     - Segment 1: `"I walk to the bathroom to wash my face and brush my teeth."`
     - Segment 2: `"After that, I go back to my bedroom to get dressed."`
   - **Lexicon Evaluation & Routing:**
     - **Approved playable animations:** Exactly **0 clips (0%)**. (Only `NAMASTE` has an approved playable clip in the system).
     - **Words present in lexicon without animations:** Exactly **1 lemma (`I`)**, matching 5 total token occurrences across the two utterances (`"I"`, `"my"`, `"my"` in Utterance 1; `"I"`, `"my"` in Utterance 2). Its status is `animationId: null` (un-animated, awaiting review).
     - **Words outside the lexicon (Out-of-lexicon words):**
       - Utterance 1: 10 raw token instances / 8 unique words (`walk`, `to`, `the`, `bathroom`, `wash`, `face`, `and`, `brush`, `teeth`).
       - Utterance 2: 9 raw token instances / 8 unique words (`after`, `that`, `go`, `back`, `to`, `bedroom`, `get`, `dressed`).
       - Combined: 19 raw token instances / 15 unique words.
   - **Routing Banner Display:**
     `⚠ Words in dictionary, 3D animation awaiting qualified review [I]; Out-of-lexicon words: [walk, to, the, bathroom, ...] — neutral pose held`
   - **Avatar Behavior:** The 3D avatar strictly **maintains neutral rest pose** (`NEUTRAL_REST_POSE`). No fake motions, arm flapping, or fingerspelling substitutions occur.

### In-Player Prototype Verification (Deterministic Fallback)
If live tab audio is unavailable, permissions are blocked, or you need immediate deterministic verification:
1. In `overlay/avatar_player.html`, click **`► Daily Routine (01:35–01:55 Unreviewed Prototype)`**.
2. **Observe Instantaneous State & Verification:**
   - Transcript updates to: `"I walk to the bathroom to wash my face and brush my teeth."`
   - Target Language: `ISL`.
   - Pipeline Status Badge: `UNREVIEWED CANDIDATE (0/3 Reviews)`.
   - Sequence ID: `daily_routine_seg_01 (01:38–01:46 / 98000–106000ms)`.
   - Generated Signs Telemetry: `0 playable clips (1 dictionary match: I [un-animated]; 6 out-of-lexicon content words: walk, bathroom, wash, face, brush, teeth)`.
   - Governance Notice: `PROVISIONAL UNAPPROVED CANDIDATE: NOT a validated ISL translation. Strictly requires review by 3 qualified Deaf-native ISL linguists. Zero synthetic gestures enforced.`
   - Avatar remains safely anchored in neutral rest pose.

### Clean Shutdown Procedure
1. On the YouTube tab, pause the video.
2. In the extension popup, click **"Stop Tab Capture & Bridge"**.
3. Status badge returns to `CAPTURE: IDLE`.
4. AudioContext and Web Audio stream tracks are closed cleanly; avatar resets to neutral.

---

## 6. Demonstration 4 — Direct Diagnostic & Benchmark Controls

If testing without live audio or microphone input, the Avatar Player includes standalone diagnostic buttons for direct verification:

1. On `avatar_player.html`, locate the **Diagnostic Controls** panel below the 3D canvas.
2. Click **Run Namaste Benchmark**:
   - Triggers the complete 1800 ms ISL Namaste baseline sequence.
   - Validates Three.js skeletal deformation, timeline interpolation, and completion callbacks.
3. Click **Test Neutral Fallback**:
   - Sends an unsupported mock payload to verify immediate safe fallback to neutral rest pose.
4. Click **Reset Avatar**:
   - Immediately stops any active motion and resets Y-Bot joints to `pose_neutral_rest_v1`.

---

## 7. Troubleshooting Guide

| Issue | Root Cause | Exact Resolution Steps |
| :--- | :--- | :--- |
| **Backend Offline / Red Status** | `signbridge-backend` is not running, or running on wrong port. | 1. Check `http://127.0.0.1:8765/health` in browser.<br>2. In PowerShell, restart: `cd signbridge-backend && python run.py`.<br>3. Verify port 8765 is not blocked by Windows Firewall or another process (`netstat -ano \| findstr 8765`). |
| **Tab Audio Capture Failure** | Chrome permissions denied or tab is silent. | 1. Audio capture requires an active media tab playing audible sound.<br>2. Ensure the active tab is not muted.<br>3. In Chrome settings (`chrome://settings/content/microphone`), ensure extension permissions are allowed.<br>4. Re-open extension popup and click "Start Tab Capture & Bridge". |
| **Avatar Canvas Blank / Black** | WebGL context loss or missing `ybot.glb`. | 1. Open Chrome DevTools on `avatar_player.html` (`F12`).<br>2. Check Console for WebGL errors.<br>3. Verify `extension/assets/models/ybot.glb` exists (file size ~2.24 MB).<br>4. Verify hardware acceleration is enabled in Chrome: `chrome://settings/system` -> *Use graphics acceleration when available*. |
| **CSP Error on Avatar Player** | Inline scripts blocked by Chrome Manifest V3 CSP. | 1. All controller logic has been decoupled into `overlay/avatar_player_controller.js`.<br>2. Ensure `overlay/avatar_player.html` references the script via `<script src="avatar_player_controller.js"></script>`.<br>3. Do NOT inject inline `<script>` tags. |
| **Transcript Received but No Animation** | Expected behavior for un-animated vocabulary. | 1. Check the routing status banner in the player.<br>2. Only `NAMASTE` currently has an approved baseline animation (`isl_namaste_godl_v1`).<br>3. All other English words safely fall back to neutral rest pose per PRD governance. |

---

## 8. Verification Checklist Before Starting Demonstration

- [ ] FastAPI backend running on port 8765 (`curl http://127.0.0.1:8765/health` returns `200 ok`).
- [ ] Extension loaded unpacked in Chrome (`chrome://extensions`).
- [ ] Avatar Player opened (`avatar_player.html`) with Y-Bot visible in neutral pose.
- [ ] Namaste benchmark tested via button or audio (plays bilateral prayer gesture, 1800 ms).
- [ ] Unsupported input tested (holds neutral rest pose, zero phantom motions).
