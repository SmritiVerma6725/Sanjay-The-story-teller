# SignBridge M3 — Final Security & Privacy Audit

**Document Reference:** `Docs/M3_FINAL_SECURITY_PRIVACY_AUDIT.md`  
**Milestone:** SignBridge Milestone M3 — Complete End-to-End Closure  
**Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  

---

## 1. Executive Summary

Milestone **M3** establishes a local-first, zero-cloud-leakage architecture for Indian Sign Language (ISL) video captioning and 3D avatar animation. This audit independently inspects the Chrome Manifest V3 security boundaries, Web Audio processing paths, local speech backend isolation, outreach dispatch firewalls, and review record integrity.

---

## 2. Chrome Extension Permission & Manifest V3 Audit

### Inspected File: `extension/manifest.json`

```json
{
  "manifest_version": 3,
  "name": "SignBridge — Tab Audio Capture",
  "version": "0.1.0",
  "permissions": [
    "tabCapture",
    "offscreen",
    "activeTab",
    "storage",
    "scripting"
  ],
  "host_permissions": [
    "*://*.youtube.com/*",
    "http://127.0.0.1:8765/*"
  ]
}
```

### Security Findings:
1. **Manifest V3 Conformance:** The extension strictly adheres to Manifest V3 using a Service Worker (`background.js`) and an Offscreen Document (`offscreen.html`) for audio processing.
2. **Permission Minimization:**
   - `tabCapture`: Required exclusively to stream active-tab audio via ephemeral `streamId`.
   - `offscreen`: Required to host Web Audio API context for audio downsampling and playback routing.
   - `activeTab`: Scopes injection strictly to the user-initiated tab upon icon click.
   - `storage`: Required for `chrome.storage.session` state machine persistence.
   - `scripting`: Scoped strictly to YouTube player interaction.
3. **Host Permission Boundary:** Host permissions are strictly bounded to `*://*.youtube.com/*` (video tab) and `http://127.0.0.1:8765/*` (local Python backend). No external cloud domains or third-party analytical endpoints are permitted or listed.

---

## 3. Audio Data Flow & Zero Cloud Leakage Verification

### Inspected Files: `extension/offscreen.js`, `extension/background.js`

```
[ Tab Audio Stream ] ──(tabCapture)──► [ MediaStreamSource ]
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
        [ audioContext.destination ]                    [ ScriptProcessorNode ]
           (Audible Playback Preserved)                   (4096-sample buffer)
                                                                       │
                                                        [ Downsample to 16kHz PCM ]
                                                                       │
                                                        [ 2.0s WAV Slicing Buffer ]
                                                                       │
                                                        [ Bounded Queue (Max 3) ]
                                                                       │
                                                                 (HTTP POST)
                                                                       ▼
                                                          [ http://127.0.0.1:8765 ]
                                                            (Local Faster-Whisper)
```

### Privacy & Resource Findings:
1. **Audible Playback Preservation:** Sourced audio is routed directly to `audioContext.destination`, ensuring the user's speaker/headphone output is never muted.
2. **Bounded In-Memory Buffering:** Audio slices are bounded to 2.0-second intervals (32,000 samples @ 16kHz mono). Memory accumulation is strictly capped; the transcription queue discards oldest chunks if `MAX_QUEUE_SIZE > 3`, preventing memory exhaustion.
3. **Strict Local Transport:** The endpoint is hardcoded to `http://127.0.0.1:8765/api/transcribe`. Grep search across `extension/` confirms zero calls to external APIs, analytics, or cloud transcription services.
4. **Lifecycle & Resource Cleanup:**
   - Tab closure or navigation immediately triggers `chrome.tabs.onRemoved` / `chrome.tabs.onUpdated`.
   - `stopCapture()` stops all `MediaStreamTrack` instances, disconnects `ScriptProcessorNode` and `muteGainNode`, and invokes `audioContext.close()`.
   - No audio contexts, streams, or listeners leak across repeated capture sessions.

---

## 4. Local Speech Backend Security & Binding Audit

### Inspected Files: `signbridge-backend/main.py`, `config.py`

### Backend Audit Findings:
1. **Localhost Binding:**
   - Configuration defaults to `host = "127.0.0.1"` and `port = 8765`.
   - The server does not bind to `0.0.0.0`, preventing LAN or WAN access.
2. **CORS Isolation:**
   - CORS origin regex is strictly locked: `r"chrome-extension://.*|http://127\.0\.0\.1.*|http://localhost.*"`.
   - Web origins from arbitrary public domains are rejected.
3. **Payload Sanitization & Size Limits:**
   - `max_audio_bytes` is enforced at `10 MB` (`10 * 1024 * 1024` bytes).
   - Payloads exceeding 10 MB are rejected immediately with HTTP 413 Payload Too Large.
   - Corrupted or non-audio uploads trigger HTTP 400 Bad Request without unhandled exceptions or crash loops.
4. **Offline Model Execution:**
   - Model weights (`tiny.en`) run entirely on local CPU via `faster-whisper` and CTranslate2.
   - Zero telemetry, transcription logs, or audio snippets are transmitted upstream during runtime.

---

## 5. Outreach Dispatch Safety & Dry-Run Firewall

### Inspected Files: Entire repository, `test_outreach_governance.py`

### Firewall Verification:
1. **Absence of Dispatch Automation:**
   - Comprehensive ripgrep scan of the entire repository for `smtplib`, `sendmail`, `email.mime`, and external HTTP mail APIs returned **zero occurrences**.
   - No executable code exists in the codebase that can dispatch an email or submit a contact form.
2. **Governance Gate Lockout:**
   - All milestone documents enforce `DRY_RUN_ONLY`.
   - Active system default is hard-locked to `REMAIN_IN_DRY_RUN (ACTIVE DEFAULT)`.
   - Decision Gate 5 in `Docs/M3_26_OWNER_DECISION_CHECKLIST.md` establishes an explicit firewall: approving recipients, drafts, or rollout plans does not authorize dispatch. Live sending requires an independent affirmative signature.

---

## 6. Review Record Integrity & Anti-Fabrication Safeguards

### Inspected Files: `tools/isl_motion_extraction/validate_review_record.py`, `reviews/`

### Integrity Findings:
1. **Zero Synthetic Reviews in Storage:**
   - The directory `tools/isl_motion_extraction/reviews/` contains zero files.
   - No mock, synthetic, or simulated review records have been placed in the review ingestion path.
2. **Read-Only Validation:**
   - `validate_review_record.py` computes SHA-256 hashes before and after validation, ensuring records cannot be mutated during inspection.
   - Any modification to candidate ID, candidate SHA-256 hash, or schema triggers immediate rejection.
3. **Rig Limitation Guard:**
   - The review worksheet and documentation explicitly label facial expressions and non-manual markers as `NOT ASSESSABLE ON CURRENT RIG`, preventing false negative ratings on articulatory dimensions the Y-Bot mesh cannot physically express.

---

## 7. Security & Privacy Certification

The SignBridge M3 codebase complies with all local-first privacy requirements, Manifest V3 security boundaries, and anti-fabrication governance policies.
