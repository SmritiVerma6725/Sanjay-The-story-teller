# SignBridge Controlled Pilot — Setup & Teardown Guide

**Document Reference:** `Docs/M4_STAGE_4_PILOT_PACKAGE/PILOT_SETUP_TEARDOWN_GUIDE.md`  
**Milestone:** SignBridge M4 Stage 4 (Controlled Pilot Preparation)  
**Governance State:** `DRY_RUN_ONLY — NOT_AUTHORIZED — OPERATIONAL GUIDE`  

---

## 1. Setup Phase (Step-by-Step)

### Step 1: Workstation Environment Preparation
1. Open PowerShell or Command Prompt in the repository root:
   ```powershell
   cd C:\AmazonMlChallenge
   ```
2. Verify Python virtual environment dependencies:
   ```powershell
   & ".\signbridge-backend\.venv\Scripts\python.exe" -c "import fastapi, faster_whisper; print('Backend environment OK')"
   ```
3. Run the automated pre-flight sanity check:
   ```powershell
   python run_all_m4_stage4_tests.py
   ```
   *Requirement:* Must output `TOTAL VERIFIED CHECKS: 322 / 322 PASSED across 6 suites (0 failures)`.

### Step 2: Start Local Transcription Backend
1. In a dedicated terminal, launch the backend service:
   ```powershell
   & ".\signbridge-backend\.venv\Scripts\python.exe" ".\signbridge-backend\main.py"
   ```
2. Confirm the startup output displays:
   ```
   INFO: Uvicorn running on http://127.0.0.1:8765
   INFO: Faster-Whisper model tiny.en loaded on CPU (int8)
   ```
3. Test health endpoint via browser: `http://127.0.0.1:8765/health` -> `{"status":"ok"}`.

### Step 3: Load Chrome Extension
1. Launch Google Chrome.
2. Navigate to `chrome://extensions`.
3. Enable **Developer mode** (toggle in upper right).
4. Click **Load unpacked** and select `C:\AmazonMlChallenge\extension`.
5. Pin the SignBridge icon to the Chrome toolbar.

### Step 4: Window Arrangement & Docking
1. Open the primary YouTube test video tab in Chrome (e.g. approved educational clip).
2. Click the SignBridge extension icon in the toolbar.
3. Verify the popup indicates `Online (tiny.en, CPU)` with a green dot.
4. Click **Open 3D Avatar Display**.
5. Arrange windows side-by-side:
   - Left half: Chrome with YouTube video tab.
   - Right half: SignBridge 3D Avatar Player window.

---

## 2. Teardown Phase (Step-by-Step)

### Step 1: Session Shutdown
1. In the extension popup, click **Stop Capture** (if active).
2. Click **Clear Transcript** to erase live text from session storage.
3. Close the 3D Avatar Player window.

### Step 2: Backend Termination
1. In the backend terminal, press `Ctrl+C` to terminate Uvicorn.
2. Confirm the terminal process has completely stopped.

### Step 3: Browser Session Cleanup
1. Close all Chrome browser windows. This immediately clears `chrome.storage.session` in memory.
2. Re-open Chrome to confirm state is clean and no tab capture remains active.

### Step 4: Data Verification
1. Inspect `signbridge-backend/` to verify zero `.wav` files were persisted.
2. Store completed, anonymized worksheets in the secure local study archive.
