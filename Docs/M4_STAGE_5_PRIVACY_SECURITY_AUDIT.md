# SignBridge M4 Stage 5 — Privacy & Security Audit

**Document Reference:** `Docs/M4_STAGE_5_PRIVACY_SECURITY_AUDIT.md`  
**Milestone:** SignBridge Milestone M4 — End-to-End Product Integration, ISL Validation Readiness, UX, Performance, and Controlled Pilot Preparation  
**Stage:** **Stage 5: Complete Validation, Release Readiness & Evidence Closure**  
**Execution Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  
**Audit Scope:** Extension Manifest V3, Web Audio graph, Python backend, storage channels, network boundaries, and data deletion lifecycles.

---

## 1. Executive Summary

This code-level security and privacy audit evaluates the real implementation against the PRD zero-cloud-leakage guarantee, data minimization requirements, and local processing bounds. 

Key Findings:
1. **Zero External Egress:** All tab audio processing and speech recognition occur 100% locally on loopback (`127.0.0.1:8765`). Zero external network calls are made to cloud APIs, analytics engines, or telemetry trackers.
2. **Tab Capture Boundaries:** Extension uses `chrome.tabCapture` exclusively; no physical microphone permissions (`audioCapture` / `getUserMedia({audio: true})`) are requested or used.
3. **Loopback Server Bounding:** FastAPI backend is bound strictly to `127.0.0.1:8765` (never `0.0.0.0`). CORS is restricted via regex to Chrome extension origins and localhost.
4. **Transient Audio Persistence:** Audio slices exist exclusively in memory as transient Float32 / PCM WAV byte buffers (2.0s duration) and are immediately garbage-collected upon transcription. Zero audio is written to disk.
5. **No Synthetic Human Reviews:** Review store (`tools/isl_motion_extraction/reviews`) is 100% segregated and verified empty.

---

## 2. Granular Data-Flow Table

The table below traces every data type across its complete lifecycle, from origination to deletion:

| Data Type | Source | Processing Location | Persistence | Destination | Deletion Behavior | Evidence | Residual Risk Classification |
|---|---|---|---|---|---|---|:---:|
| **Tab Audio Stream** | Active YouTube tab via `chrome.tabCapture` | In-memory Web Audio graph (`offscreen.js`) | Ephemeral (RAM only, 2.0s chunks) | Loopback `http://127.0.0.1:8765/api/transcribe` | Cleared immediately after fetch response or capture stop | `offscreen.js:370-379` (`sampleBuffer = []`, tracks stopped) | **`VERIFIED_BEHAVIOR`** |
| **PCM WAV Slices** | 48kHz -> 16kHz downsampler in `offscreen.js` | In-memory ArrayBuffer / Blob | Bounded RAM FIFO queue (max 3 chunks, ~64KB each) | Local Python FastAPI backend | Overwritten by FIFO when queue reaches 3; flushed on stop | `test_m4_stage3_performance_privacy.py:test_01` | **`VERIFIED_BEHAVIOR`** |
| **Whisper Model Weights** | Local disk storage in `signbridge-backend/` | Python CTranslate2 runtime process RAM | Process lifetime | CTranslate2 MKL threadpool | Purged from RAM on backend process exit | `transcriber.py:35-45` | **`VERIFIED_BEHAVIOR`** |
| **Live Speech Transcripts** | Faster-Whisper local ASR output | Python backend -> Extension storage / runtime message | Transient session storage (max 30 items) | `popup.html`, `avatar_player.html` | Ring buffer drops oldest; purged on `REQUEST_STOP_CAPTURE` | `test_m4_stage3_performance_privacy.py:test_04` | **`VERIFIED_BEHAVIOR`** |
| **ISL Sign Sequences** | `isl_translator.js` rule engine | In-memory browser JS heap | Ephemeral (active sequence duration) | `avatar_player.html` Three.js bone mixer | Overwritten by subsequent sequence; reset on session stop | `avatar_player.html:1082` (`resetToNeutralPose`) | **`VERIFIED_BEHAVIOR`** |
| **Error & Health Logs** | Backend Uvicorn logger & extension console | Local terminal stdout & Chrome DevTools console | Ephemeral terminal scrollback | Local terminal only | Not persisted to disk; raw audio bytes/transcripts omitted | `main.py:15-19`, `test_m4_stage3_performance_privacy.py` | **`VERIFIED_BEHAVIOR`** |
| **Human Review Records** | Manual reviewer evaluation form | Local disk (`tools/isl_motion_extraction/reviews/`) | Persistent local JSON | Local filesystem only | Manual deletion by facilitator; immutable during run | `validate_review_record.py`, `test_review_validator.py` | **`CODE_REVIEWED_UNTESTED`** (Store currently empty) |
| **Local LocalStorage** | Review Studio UI (`preview_mocap.html`) | Browser localStorage | Persistent per browser profile | Origin `http://127.0.0.1:8000` | Manual clearing or browser data reset | `test_m3_browser_usability.py:Check 14` | **`CODE_REVIEWED_UNTESTED`** (Dev studio only) |

---

## 3. Threat Modeling & Security Controls

### 3.1 Permission Scope & Least Privilege
- **Chrome Extension Manifest V3 (`extension/manifest.json`):**
  - `permissions`: `["tabCapture", "offscreen", "activeTab", "storage", "scripting"]`
  - `host_permissions`: `["*://*.youtube.com/*", "http://127.0.0.1:8765/*"]`
  - **Audit Finding:** Minimal and strictly bounded. No `<all_urls>` permission. No microphone device permission. No network interception (`webRequest` / `declarativeNetRequest`). No background tracking permissions.

### 3.2 Loopback Exposure & Local Port Security
- **FastAPI Backend Binding (`config.py` & `main.py`):**
  - Bound to `127.0.0.1:8765` by default.
  - CORS middleware restricts origins using regex: `r"chrome-extension://.*|http://127\.0\.0\.1.*|http://localhost.*"`.
  - **Residual Risk:** Any malicious local software running under the same user account on the local machine can connect to `127.0.0.1:8765`. However, the backend exposes zero administrative capabilities, zero file write endpoints, and zero system command execution. Requests are validated via Pydantic schemas, and payloads exceeding 10 MB trigger HTTP 413.

### 3.3 Zero Outbound Cloud Leakage
- **Network Egress Audit (`test_m4_stage5_validation.py:test_17`):**
  - Static grep and runtime inspection confirm zero HTTP/WebSocket connections to Google Analytics, OpenAI, Gemini, Sentry, Mixpanel, Datadog, or external servers.
  - All Three.js and Y-Bot GLB assets are bundled locally in `extension/lib/` and `extension/assets/models/`.

### 3.4 Data Retention & Disposal Verification
- **Post-Session Disposal:**
  - Upon clicking "Stop Capture", `REQUEST_STOP_CAPTURE` triggers complete teardown:
    1. MediaStream audio tracks are stopped immediately (`track.stop()`).
    2. AudioContext is closed (`audioContext.close()`).
    3. Memory sample buffers are zeroed (`sampleBuffer = []`).
    4. Bounded FIFO queues are emptied (`transcriptionQueue.length = 0`).
    5. Avatar player resets bone rotations to `NEUTRAL_REST_POSE`.
    6. No WAV files, temporary recordings, or audio dumps exist on disk.

---

## 4. Residual Risks & Audit Classification

1. **`VERIFIED_BEHAVIOR`:**
   - Zero cloud audio transmission.
   - Bounded in-memory queues (max 3 slices).
   - Clean session teardown releasing Web Audio tracks.
   - Monotonic sequence ordering dropping duplicate chunks.
2. **`CODE_REVIEWED_UNTESTED`:**
   - Multi-reviewer concurrent review ingestion (not tested because review store is intentionally empty).
3. **`UNRESOLVED_RISK`:**
   - Multi-tenant local workstation: Unauthenticated local loopback allows other processes on the same machine to submit audio slices to the ASR backend. For a controlled pilot, the workstation must be a dedicated single-user test environment.
