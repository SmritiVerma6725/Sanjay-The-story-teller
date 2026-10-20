# SignBridge M4 Stage 4 — Controlled Pilot Protocol

**Document Reference:** `Docs/M4_STAGE_4_CONTROLLED_PILOT_PROTOCOL.md`  
**Milestone:** SignBridge Milestone M4 — End-to-End Product Integration, ISL Validation Readiness, UX, Performance, and Controlled Pilot Preparation  
**Stage:** **Stage 4: Controlled Pilot Protocol & Operational Governance**  
**Execution Date:** October 20, 2026  
**Auditor / Operational Author:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  
**Baseline Status:** `isl_namaste_godl_v1` is `IMPLEMENTED_UNVALIDATED` (Awaiting Qualified Deaf-Native Review)  
**Evaluated Motion Candidate:** `isl_namaste_mocap_candidate_v1` (Quarantined in isolated experimental assets)  

---

## 1. Scope, Purpose, and Intended Use

### 1.1 Purpose
This protocol defines the formal operational, ethical, and technical framework for conducting a future **Controlled Pilot Evaluation** of the SignBridge browser extension and local speech-to-sign pipeline. The objective of the pilot is to evaluate:
1. **User Experience & Interaction Flow:** Participant ability to configure, start, monitor, and stop tab audio interpretation during video playback.
2. **Software Reliability & Resilience:** Pipeline behavior during tab navigation, audio pauses, background noise, and session termination.
3. **Clarity of Transparency Indicators:** User comprehension of confidence indicators, out-of-lexicon notices, and linguistic disclaimers.

### 1.2 Intended Use
- **Target Audience:** Deaf, Hard-of-Hearing (DHH), and hearing participants who provide informed, voluntary consent in an observational laboratory or controlled remote setting.
- **Controlled Setting Only:** The software is to be evaluated strictly in 1-on-1 facilitated sessions with dedicated observation and immediate debriefing.

### 1.3 Critical Exclusions & Operational Prohibitions
> [!CAUTION]
> **HIGH-STAKES COMMUNICATION PROHIBITION:**
> Under no circumstances may SignBridge be used, relied upon, or tested in:
> 1. Emergency services (police, fire, ambulance, disaster response).
> 2. Medical, clinical, diagnostic, or psychiatric consultations.
> 3. Legal proceedings, courtroom testimony, police interviews, or contractual negotiations.
> 4. Financial transactions or critical banking operations.
> 5. Classroom examinations or educational assessments without certified human interpreters.
> 
> SignBridge is an **experimental research prototype**. It does not substitute for qualified human sign language interpreters (certified by ISLRTC or relevant statutory bodies).

---

## 2. Participant Eligibility & Accessible Informed Consent

### 2.1 Eligibility Criteria
To ensure ethical and valid evaluation, participant inclusion criteria are established:
- **Age:** 18 years or older.
- **Language Familiarity:** Daily or conversational user of Indian Sign Language (ISL) or English speech / captions.
- **Technical Literacy:** Basic familiarity with operating the Google Chrome web browser.
- **Voluntary Participation:** Willingness to provide written or signed video consent without coercion or financial duress.

### 2.2 Accessible Informed Consent Protocol
Consent materials must be provided in accessible, multimodal formats:
1. **Written English Information Sheet:** Written in clear, non-technical plain English (Flesch-Kincaid Grade Level $\le 8$).
2. **Recorded ISL Video Explanation:** Pre-recorded ISL video summarizing the study purpose, data handling, voluntary nature, and risks.
3. **Certified Human Interpreter Present:** In-person or remote certified ISL interpreter present during all consent discussions.
4. **Explicit Experimental Warning:** Participants must be informed explicitly:
   > *"SignBridge is an experimental prototype. Its current avatar movements were created by technical engineers and have NOT YET been certified as linguistically correct by qualified Deaf-native ISL teachers. The avatar may sign inaccurately or fail to sign certain words."*
5. **Right to Immediate Withdrawal:** Participants may pause, stop, or withdraw from the pilot at any point without explanation and without forfeiting any participation stipend. Upon withdrawal, all session telemetry is immediately purged.

---

## 3. Data Privacy, Storage, and Data Lifecycle

### 3.1 100% Local Data Processing
All data processing occurs locally on the testing machine:
- **Audio Processing:** Tab audio is captured in Chrome RAM via `tabCapture` and sliced into 2.0s PCM WAV buffers.
- **Speech Recognition:** Faster-Whisper runs locally on the CPU (`127.0.0.1:8765`). Zero audio bytes or transcripts are transmitted across the internet.
- **Zero Cloud Endpoints:** The extension does not communicate with Google Cloud, AWS, OpenAI, or external analytics endpoints.

### 3.2 Ephemeral In-Memory Lifecycle
| Data Element | Format | In-Memory Location | Retention Duration | Deletion Trigger |
|:---|:---|:---|:---|:---|
| **Raw Tab Audio** | Float32 Samples | Chrome Offscreen RAM | Max 2.0 seconds | Overwritten by next audio chunk |
| **WAV Slices** | 16kHz PCM Blob | Chrome Offscreen RAM | Max 8.0 seconds (HTTP request) | Discarded upon HTTP 200 response |
| **Live Transcripts** | Text string | `chrome.storage.session` | Max 30 entries | Cleared on session stop or browser exit |
| **Playback Telemetry** | Sequence ID, timestamp | DOM elements | Ephemeral | Reset upon session stop |
| **Participant Observations** | Facilitator notes | Local markdown file | Study duration (max 30 days) | Deleted upon study publication |

### 3.3 Post-Session Data Deletion Procedure
Immediately upon conclusion of each pilot session:
1. Click **Clear Transcript** in the popup UI.
2. Stop the local Python backend process (`Ctrl+C`).
3. Clear `chrome.storage.session` by closing all Chrome windows.
4. Verify no WAV files or audio dumps exist in `signbridge-backend/` or temporary OS folders.

---

## 4. Hardware & Software Prerequisites

Before initializing a pilot session, the test facilitator must verify the host workstation against the documented technical baseline:

| Component | Minimum Requirement | Verified Test Platform (Stage 3) | Compliance Check |
|:---|:---|:---|:---:|
| **Operating System** | Windows 10/11, macOS 12+, or Ubuntu 22.04 | Windows 10 Pro (Build 10.0.22631) | Verified |
| **Processor (CPU)** | 4 Cores (x86_64 or Apple Silicon) | AMD64 4 Logical Cores | Verified |
| **System Memory (RAM)**| $\ge 8\text{ GB}$ total system RAM | 16 GB Physical RAM | Verified |
| **Available Disk Space** | $\ge 2\text{ GB}$ for local model weights | Local HuggingFace cache | Verified |
| **Web Browser** | Google Chrome $\ge 120$ (Manifest V3) | Google Chrome 140.0.7339.128 | Verified |
| **Python Runtime** | Python 3.10 or 3.11 with VirtualEnv | Python 3.11.9 (`signbridge-backend\.venv`) | Verified |
| **Speech Model** | Faster-Whisper `tiny.en` (`int8`, CPU) | Local `tiny.en` cache | Verified |
| **Display & GPU** | WebGL 2.0 hardware acceleration | Intel/NVIDIA/AMD GPU driver active | Verified |

---

## 5. Structured Pilot Session Script

Each pilot session follows a structured, step-by-step 45-minute facilitator script:

### Step 1: Pre-Flight Briefing & Accessible Consent (10 minutes)
1. Welcome participant; facilitate introductions with certified ISL interpreter.
2. Review the Participant Information Sheet and play the ISL video explanation.
3. Reiterate the non-emergency, experimental nature of the tool.
4. Obtain signed written/video consent.
5. Confirm participant comfort and assign a randomized, anonymous participant ID (e.g., `P-001`).

### Step 2: System Setup & Onboarding Walkthrough (5 minutes)
1. Launch local backend (`python main.py` at `127.0.0.1:8765`).
2. Open Chrome with the SignBridge extension loaded.
3. Walk participant through popup UI: Explain "Start Capturing Tab Audio", "Open 3D Avatar Display", and "Clear Transcript".
4. Position the 3D Avatar window docked alongside the video playback tab.

### Step 3: Evaluated Interaction Scenarios (20 minutes)
The facilitator guides the participant through four standardized video clips:

1. **Scenario A — Baseline Sign ("Namaste" / Greetings):**
   - *Video Material:* Educational video containing clear phrase: *"Namaste, welcome to the session."*
   - *Expected System Behavior:* Speech recognized (`"Namaste"`), routed to `isl_namaste_godl_v1`, avatar executes bilateral prayer gesture, status badge turns green.
   - *Participant Evaluation:* Did the avatar sign smoothly? Was the motion recognizable?
2. **Scenario B — Non-Animated Dictionary Word ("Thank You"):**
   - *Video Material:* Video containing phrase: *"Thank you for your attention."*
   - *Expected System Behavior:* Speech recognized (`"Thank you"`), word present in lexicon but lacks validated 3D animation, status displays: `⚠ Words in dictionary, 3D animation awaiting qualified review — neutral pose held`. Avatar holds neutral rest pose (zero fake gestures).
   - *Participant Evaluation:* Did the participant understand why the avatar held a neutral pose? Did the visual badge clearly explain the status?
3. **Scenario C — Out-of-Lexicon Phrase ("Quantum computing"):**
   - *Video Material:* Technology lecture containing technical jargon.
   - *Expected System Behavior:* Speech recognized, words identified as out-of-lexicon (`unsupportedWords`), avatar holds neutral pose, telemetry displays unsupported words list.
   - *Participant Evaluation:* Does the participant prefer a neutral pose over confusing, fabricated gestures?
4. **Scenario D — Background Noise & Speech Pauses:**
   - *Video Material:* Clip with conversational pauses and light ambient background music.
   - *Expected System Behavior:* Silence rejected in $<40\text{ ms}$; avatar maintains steady rest pose; speech resumes without lag or queue overflow.

### Step 4: Post-Session Debriefing & Semi-Structured Interview (10 minutes)
1. Facilitate debriefing using standardized post-session Likert questionnaire (1–5 scale):
   - Perceived lag between speech and avatar motion.
   - Visual clarity of the avatar gestures.
   - Clarity of status messages and warning badges.
   - Overall comfort with the interface layout.
2. Open qualitative feedback: Participant suggestions for improvements.
3. Thank participant and provide compensation stipend.

---

## 6. Incident Reporting, Stopping Conditions, and Rollback

### 6.1 Session Stopping Conditions
The facilitator must **immediately abort the session** if:
1. Participant signals distress, fatigue, or requests to withdraw.
2. Avatar exhibits visual glitches, joint inversion, or erratic unconstrained bone rotations.
3. Chrome process hangs, crashes, or produces out-of-memory errors.
4. Backend process crashes repeatedly or fails to restart.

### 6.2 Incident Logging Protocol
Any unexpected behavior must be recorded in an **Incident Report** (`Docs/M4_STAGE_4_PILOT_PACKAGE/INCIDENT_REPORT_TEMPLATE.md`) documenting:
- Incident Timestamp and Participant ID.
- Scenario being executed.
- Observed system state, console error messages, and backend traceback.
- Severity classification: `LOW` (cosmetic UI glitch), `MEDIUM` (transient ASR delay), `HIGH` (crash, hang, unhandled exception), or `CRITICAL` (misleading/offensive avatar gesture).

### 6.3 Immediate Rollback Procedure
If a regression or critical bug is discovered:
1. Abort the session and ensure participant safety and comfort.
2. Revert active animation library to production baseline `isl_namaste_godl_v1`.
3. Clear `chrome.storage.session` and restart browser.
4. File an immediate blocker in `Docs/M4_BLOCKERS_AND_DEPENDENCIES.md`.

---

## 7. Protocol Governance & Authorization Boundary

> [!IMPORTANT]
> **GOVERNANCE NOTICE:**  
> This protocol specifies operational procedures for a **future** controlled pilot.  
> Completion of Milestone M4 Stage 4 constitutes **PREPARATION ONLY**.  
> **No actual human participants may be contacted, recruited, or scheduled until:**
> 1. Formal written approval is granted by the SignBridge Project Owner.
> 2. Institutional Ethics / Review Board (IRB) exemption or clearance is documented.
> 3. YouTube source-video licensing is authoritatively resolved from `UNRESOLVED`.
> 4. All outreach mechanisms remain strictly locked in `DRY_RUN_ONLY — NOT_AUTHORIZED`.
