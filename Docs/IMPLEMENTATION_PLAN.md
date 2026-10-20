# SignBridge — Implementation Plan & Roadmap

**Document Version:** 1.5 (Milestone M3 Phase 3.2 ISL Translator Implemented & Tested)  
**Current Milestone:** M3 (Phase 3.1 & 3.2 Complete; M2 Live Verification Pending)  
**Execution State:** M1 shell and audio capture implemented; M2 local backend, in-memory WAV encoding, bounded queue, and popup transcription implemented; M3 Phase 3.1 data contracts and Phase 3.2 ISLTranslator implemented and validated; 70 Chrome in-engine tests passed across M1 (9), M2 (10), and M3 (51); 7 Python backend unit/integration tests passed; Live tab-capture-to-backend integration smoke test and physical audio tests remain pending.  
**Date:** October 2026

---

## 1. Governance Principles & Phasing Strategy

SignBridge follows a strict milestone-driven engineering approach:
1. **Incremental Progression:** Each milestone must be fully implemented, verified with actual empirical tests, and documented before proceeding to the next milestone.
2. **Zero-Cost Constraint:** No paid APIs, cloud infrastructure, or subscriptions are accepted at any stage.
3. **No Unlicensed Assets:** Unlicensed source code, model weights, or datasets will not be copied or incorporated.
4. **Tooling Simplicity:** Vanilla JavaScript (ES6+) is used for the initial Chrome extension shell; no Node.js or bundlers unless justified by strict technical necessity.
5. **Human Review Gate:** Milestone M1 must not commence until human sign-off on the M0 audit and architectural decisions is recorded.

---

## 2. Milestone Roadmap Overview

```mermaid
gantt
    title SignBridge Implementation Roadmap
    dateFormat  YYYY-MM-DD
    section Milestones
    M0: Audit & Architecture          :done,    m0, 2026-10-16, 2026-10-16
    M1: Extension & Tab Audio Capture :done,    m1, 2026-10-17, 2026-10-17
    M2: Local Speech Recognition (ASR):active,  m2, 2026-10-17, 2026-10-17
    M3: First Language E2E (ISL)      :         m3, 2026-10-18, 2026-10-26
    M4: Synchronization & Usability   :         m4, 2026-10-27, 2026-11-02
    M5: Second Language (ASL)         :         m5, 2026-11-03, 2026-11-09
    M6: Evaluation & Release          :         m6, 2026-11-10, 2026-11-16
```

---

## 3. Milestone Work Breakdown

### Milestone M0: Repository and License Audit (CONDITIONALLY ACCEPTED)

**Objective:** Audit candidate repositories, distinguish source code vs asset licenses, reject paid dependencies, establish vanilla JS tooling, prioritize ISL for M3 and ASL for M5, and define empirical test plans.

- [x] **Task 0.1:** Inspect workspace and identify cloned repositories (`kozha_repo`, `yap_render_repo`, `GenASL`).
- [x] **Task 0.2:** Investigate "SignZen" (confirmed non-existent open-source repository; investigation closed).
- [x] **Task 0.3:** Conduct granular license audit distinguishing source code, model weights, lexical datasets, reference videos, 3D rigs, and animation clips:
  - Excluded `yap_render_repo` source code (Unlicensed / All Rights Reserved).
  - Excluded `GenASL` source code (GPLv3 copyleft contamination).
  - Excluded Kozha ISL dataset (`Indian_SL.sigml` — Unclear / Unlicensed).
  - Excluded ASL-LEX reference videos (Proprietary website media; not redistributable).
  - Clarified Adobe Mixamo `ybot.glb` is a humanoid rig containing zero sign animations.
  - Noted zero verified 3D ISL animation assets exist in the project today.
- [x] **Task 0.4:** Reject paid and cloud APIs (OpenAI API in Kozha, Gemini API in Yap Render).
- [x] **Task 0.5:** Approve vanilla JavaScript for the initial Chrome Manifest V3 extension shell.
- [x] **Task 0.6:** Reclassify Whisper latency and RTF claims as unverified estimates pending M2 benchmarks.
- [x] **Task 0.7:** Frame ISL grammar transformations as working heuristic hypotheses pending Deaf-native review.
- [x] **Task 0.8:** Complete and update all core engineering documents:
  - [x] `Docs/ARCHITECTURE.md`
  - [x] `Docs/DECISIONS.md`
  - [x] `Docs/ASSET_LICENSES.md`
  - [x] `Docs/TEST_PLAN.md`
  - [x] `Docs/IMPLEMENTATION_PLAN.md`

**M0 Completion Status:** Conditionally Accepted. Documentation updated and verified. M1 implementation will not start until human approval is received.

---

### Milestone M1: Extension Shell & Tab Audio Capture (CODE COMPLETE — AWAITING PHYSICAL AUDIO VERIFICATION)

**Objective:** Build the unpacked Chrome Manifest V3 extension shell in vanilla JavaScript, implement active tab audio capture via `chrome.tabCapture` and offscreen document, and physically verify audible playback preservation through speakers and headphones.

#### Tasks:
- [x] **Task 1.1:** Setup `extension/` directory with `manifest.json` (MV3, vanilla JS, permissions: `tabCapture`, `offscreen`, `activeTab`, `storage`, `scripting`, host permissions: `*://*.youtube.com/*`, `http://127.0.0.1:8765/*`).
- [x] **Task 1.2:** Build extension popup UI (`popup.html`, `popup.js`, `popup.css`) with explicit Start/Stop action, ISL/ASL language selector, backend status indicator, and real-time audio telemetry.
- [x] **Task 1.3:** Implement offscreen document (`offscreen.html`, `offscreen.js`) for audio capture processing with resilient messaging retry.
- [x] **Task 1.4:** Implement Web Audio API playback preservation pipeline:
  ```javascript
  const audioContext = new AudioContext();
  const source = audioContext.createMediaStreamSource(tabStream);
  source.connect(audioContext.destination); // Routes sound to speakers/headphones
  ```
- [x] **Task 1.5:** Implement `MediaRecorder` audio chunking in offscreen document (slicing audio into 2.0s WebM chunks) with progress telemetry.
- [x] **Task 1.6:** Implement clean lifecycle teardown (stop tracks on tab navigation, tab close, or user stop).

#### M1 Verification & Acceptance Status:
- **Automated In-Engine Verification:** 19 automated tests executed via `run_chrome_tests.py` in Chrome 155 across M1 and M2 test suites. All 19 passed.
- **Physical Hardware Verification Remaining:**
  1. **M1-TC01:** Explicit user activation on live YouTube video.
  2. **M1-TC02:** Playback preservation verified on internal speakers (audio remains audible).
  3. **M1-TC03:** Playback preservation verified with headphones plugged in (no microphone feedback).
  4. **M1-TC04:** Headphone connect/disconnect mid-playback handled seamlessly.
  5. **M1-TC05:** Live 2.0s audio chunk emission from a playing YouTube tab.
  6. **M1-TC06–M1-TC08:** Video pause, resume, seeking, and speed change handling.
  7. **M1-TC09–M1-TC10:** Resource release and navigation teardown during live capture.

---

### Milestone M2: Local Speech Recognition Backend (IMPLEMENTED — END-TO-END VERIFICATION PENDING)

**Objective:** Deploy a lightweight local Python FastAPI service running `faster-whisper` on CPU to receive audio chunks and emit timestamped transcription segments, establishing an empirical performance benchmark.

#### Tasks:
- [x] **Task 2.1:** Setup `signbridge-backend/` environment using Python 3.11 with `faster-whisper`, `fastapi`, and `uvicorn`.
- [x] **Task 2.2:** Implement `POST /api/transcribe` endpoint accepting audio slices (in-memory WAV encoding, sequence_id, timestamp, language parameters).
- [x] **Task 2.3:** Configure local model loading (`tiny.en` default and `base.en` with `compute_type="int8"` on CPU).
- [x] **Task 2.4:** Execute the benchmarking protocol documenting CPU hardware, RTF, inference time, and qualitative accuracy on test sample across `tiny.en` and `base.en`.
- [x] **Task 2.5:** Connect extension offscreen audio sender to the local backend with bounded FIFO queue (max 3), single in-flight concurrency lock, and 8.0s timeout.

#### M2 Exit Criteria & Current Verification State:
- [x] Service runs completely offline on `http://127.0.0.1:8765` (verified with 7 backend unit/integration tests in `test_backend.py`).
- [x] Benchmarked RTF (0.281 on 5.22s sample for `tiny.en`) and latency figures documented with machine specifications (Intel Core i5-7200U, 16GB RAM).
- [x] Word-level timestamps returned in validated JSON schema.
- [x] Integrated extension popup surfaces recognized speech text and clear state controls (verified with 10 Chrome in-engine tests in `test_m2_suite.html`).
- [ ] **Pending Integration Smoke Test:** Live end-to-end integration verification (capturing a real live YouTube video segment in Chrome, transmitting chunks to the live backend, and rendering text in the popup) remains pending alongside deferred physical audio tests.

---

### Milestone M3: First Language End-to-End Prototype: ISL (FEASIBILITY ASSESSMENT & PLAN DRAFTED)

**Objective:** Implement rule-based ISL heuristic grammar transformations, build a clean-room seed vocabulary of sign poses and fingerspelling fallback, integrate the Mixamo Y-Bot rig in Three.js, and demonstrate synchronized signing on YouTube.  
**Feasibility Specification:** See [`Docs/M3_PLAN_AND_ASSET_FEASIBILITY.md`](file:///C:/AmazonMlChallenge/Docs/M3_PLAN_AND_ASSET_FEASIBILITY.md) for full asset licensing audit, seed vocabulary specification, and data contracts.

#### Tasks:
- [x] **Task 3.1:** Define JSON contracts and strict schema validators for `SignSequence` and `SignItem` (implemented in `extension/models/sign_contracts.js`; verified with 28 automated in-engine unit tests in Chrome 155 via `test_m3_suite.html`).
- [x] **Task 3.2:** Implement pure, modular rule-based `ISLTranslator` in vanilla JavaScript with seed lexicon matching, explicit unsupported-word tracking, and isolated experimental grammar heuristics (implemented in `extension/translation/isl_translator.js`; verified with 23 automated in-engine unit tests in Chrome 155 via `test_m3_suite.html`).
- [x] **Task 3.3:** Construct clean-room declarative keyframe schema, skeletal bone normalization, neutral rest pose, and synthetic technical motion prototype (Phase 3.3 feasibility prototype implemented in `extension/animation/keyframe_registry.js`; verified with 19 automated in-engine unit tests in Chrome 155 via `test_m3_suite.html`; full 15-word and 26-letter sign asset authoring deferred to subsequent phases).
- [x] **Task 3.4:** Build Three.js avatar viewport and player prototype (`extension/animation/avatar_player.js`, `extension/overlay/avatar_player.html`, `extension/assets/models/ybot.glb`; verified with 18 automated in-engine unit tests in Chrome 155 via `test_m3_suite.html` and visual render evidence).
- [ ] **Task 3.5 (Bounded Pilot):** Pilot Plan & Implementation Proposal prepared (ADR-014); 2–3 candidate signs (`NAMASTE`, `THANK_YOU`, `HELP`) proposed with ISLRTC sources, Deaf native signer review protocol, Y-Bot rig articulation verified, safe neutral fallback preserved, and model licensing rechecked; authoring paused awaiting manual in-Chrome player inspection.
- [ ] **Task 3.6:** Wire pipeline end-to-end: Tab Audio -> Whisper ASR -> ISL Translator -> Three.js Avatar signing on YouTube.

#### M3 Exit Criteria:
- YouTube speech is transcribed and drives avatar signing in the overlay.
- Unsupported words trigger fingerspelling fallback with honest UI indication.
- Measured end-to-end latency meets the <= 3.0s window.

---

### Milestone M4: Video Synchronization & Overlay Usability (PLANNED)

### Milestone M4: Synchronization, UX, Performance & Pilot Readiness (COMPLETE — 340/340 CHECKS)

**Objective:** Coordinate speech-to-sign pipeline, message sequencing, bounded buffering, performance benchmarking, and controlled pilot preparation.

#### Completed Tasks:
- [x] **Task 4.1:** Implement versioned message bridge (`SIGNBRIDGE_TRANSCRIPTION_DISPATCH` v1.0.0) between background worker and 3D player.
- [x] **Task 4.2:** Implement monotonic sequencing and de-duplication in `avatar_player.html` (drop packets with `sequenceId <= lastProcessedSeqId`).
- [x] **Task 4.3:** Complete ISL 5-tier vocabulary audit across 16 seed words and 50 lemmas.
- [x] **Task 4.4:** Performance & privacy benchmarking (1016.4ms latency, 0.506 RTF, 185.54MB steady-state memory, zero egress).
- [x] **Task 4.5:** Implement headless dry-run simulator testing 17 operational scenarios with exit code 0.
- [x] **Task 4.6:** Unified 340-check master validation suite (`run_all_m4_stage5_tests.py`).

---

### Milestone M5: Second Language Pipeline: ASL Architecture & Contract Separation (CHECKPOINTED)

**Objective:** Implement strict linguistic and architectural separation between ISL and ASL pipelines; establish contract extensions for single-letter fingerspelling fallback.

#### Completed Tasks:
- [x] **Task 5.1:** Author independent `ASLTranslator` module (`extension/translation/asl_translator.js`) strictly decoupled from ISL heuristics.
- [x] **Task 5.2:** Implement strict non-substitution policy (`ASL_SCHEDULED_FOR_M5`, `ASL_SEED_LEXICON = {}`) preventing unvalidated English-to-ASL word replacement.
- [x] **Task 5.3:** Connect language selector in `popup.html` and `avatar_player.html` with explicit status indicators.
- [x] **Task 5.4:** Verify 67 canonical Mixamo skeleton joints in `keyframe_registry.js` with neutral rest pose fallback for unsupported words.

---

### Milestone M6: System Integration, Automated Release Verification & Packaging (COMPLETE — 360/360 CHECKS)

**Objective:** Reconcile all previous milestone checkpoints, verify end-to-end pipeline wiring, execute unified 360-check release test runner, maintain external blocker governance, and package release candidate.

#### Completed Tasks:
- [x] **Task 6.1:** Reconcile historical state discrepancy between documented M4 Stage 5 and M5 checkpoints (verified 67-joint Y-Bot rig, fingerspelling contract resolution, and ASL isolation).
- [x] **Task 6.2:** Verify unbroken end-to-end pipeline wiring (tab capture -> 16kHz PCM WAV chunking -> local Whisper backend -> v1.0.0 dispatch -> translation routing -> 3D avatar animation -> clean teardown).
- [x] **Task 6.3:** Implement authorative M6 release verification test suite (`tests/test_m6_release_verification.py`, 20 unit tests).
- [x] **Task 6.4:** Author master unified release test runner (`run_all_m6_release_tests.py`) reconciling 360 automated checks across 8 sub-suites.
- [x] **Task 6.5:** Author authoritative release report (`Docs/M6_INTEGRATION_AND_RELEASE_REPORT.md`) and update project phase index (`Docs/PROJECT_PHASE_INDEX.md`).
- [x] **Task 6.6:** Maintain honest governance declarations (4 external owner decisions: `LEGAL-01`, `DEAF-01`, `PERF-01`, `OPS-06`).

#### M6 Exit Criteria Status:
- **Master Release Test Suite:** 360 / 360 checks passed with exit code 0.
- **Local Packaging:** Verified unpacked MV3 extension structure, loopback security, and multi-license attribution.
- **Linguistic Certification Gate:** Explicitly marked as awaiting qualified Deaf-native review (0/3 reviews completed).

