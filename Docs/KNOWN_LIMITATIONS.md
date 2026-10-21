# SignBridge — Known Limitations & Governance Status

**Milestone:** Final Prototype Freeze & Demonstration Handoff  
**Workspace:** `C:\Users\HP\OneDrive\Desktop\PROJECTS\Smriti_SignBridge`  
**Date:** October 2026  
**Status:** Frozen Prototype / Demonstration-Ready  

---

## 1. Executive Summary

SignBridge is an engineering prototype designed to validate the architectural feasibility of real-time tab audio capture, local offline Whisper ASR transcription, rule-based Indian Sign Language (ISL) gloss mapping, and 3D avatar skeletal deformation in a Chrome extension.

In accordance with core project directives, **linguistic authenticity and ethical safety strictly supersede visual animation completeness**. The prototype intentionally restricts 3D motion playback to verified and sourced sign clips. Where vocabulary is un-animated or out-of-lexicon, the avatar strictly holds a neutral rest pose rather than displaying fabricated or synthetic gestures.

---

## 2. Incomplete English-to-ISL Vocabulary Coverage

### 2.1 Lexicon Structure & Distribution
The current translation subsystem (`extension/translation/isl_translator.js` and `extension/models/sign_contracts.js`) operates against a tightly controlled seed lexicon:

| Category | Count | Gloss Entries | Runtime Behavior |
| :--- | :---: | :--- | :--- |
| **Fully Animated Baseline** | **1** | `NAMASTE` | Plays official 1800 ms skeletal animation (`isl_namaste_godl_v1`). |
| **Un-animated Dictionary Entries** | **15** | `HELLO`, `THANK_YOU`, `PLEASE`, `SORRY`, `YES`, `NO`, `GOOD`, `BAD`, `HELP`, `WATER`, `FOOD`, `NAME`, `WHERE`, `YOU`, `I` | Recognized as valid dictionary matches; resolves to `animationId: null`; holds safe 500 ms neutral rest pose. |
| **Out-of-Lexicon English Words** | *All others* | Any English word outside the 16 seed glosses | Surfaced in `unsupportedWords`; avatar remains at neutral rest pose (`pose_neutral_rest_v1`). |

### 2.2 Why Un-animated Vocabulary Remains at Neutral Pose
- **Rejection of Synthetic Guessing:** In Milestone M8, synthetic keyframe interpolation for `HELLO` and `THANK_YOU` was strictly forbidden. Creating guessed joint angles without verified ISL motion data violates Indian Sign Language linguistic integrity.
- **Decoupled Architecture:** As defined in ADR-010, `animationId: null` (`UNANIMATED_SUPPORTED_ENTRY`) cleanly decouples the linguistic translator from physical 3D asset availability. When official keyframes become available, they can be registered without rewriting translator contracts.

### 2.3 Experimental Grammar Engine
- Natural ISL uses Subject-Object-Verb (SOV) order, topic-comment structure, and non-manual facial markers, differing significantly from English Subject-Verb-Object (SVO) syntax.
- An experimental rule-based reordering engine exists in `extension/translation/isl_translator.js` (temporal marker fronting, WH-word shift to terminus, auxiliary verb omission).
- **Current Status:** Disabled by default (`enableExperimentalReordering: false`). Heuristic grammar transformations require validation by certified Deaf linguists before being enabled in live translation.

---

## 3. Experimental Linguistic Status & Validation Gaps

### 3.1 Status of the Namaste Baseline Clip (`isl_namaste_godl_v1`)
- Sourced from the Indian Sign Language Research and Training Centre (ISLRTC) baseline under Government Open Data License - India (GODL).
- Retargeted to Adobe Mixamo Y-Bot canonical skeleton (65 articulated joints).
- **Linguistic Validation Status:** `experimental_awaiting_validation`.
- **Review Progress:** **0 of 3** formal Deaf-native panel reviews completed.
- Governance banners in the avatar player explicitly warn users: *"Experimental ISL — Awaiting Human Panel Validation"*.

### 3.2 Quarantined MoCap Candidate Clip (`isl_namaste_mocap_candidate_v1.json`)
- Derived from computer vision landmark extraction (MediaPipe 33-landmark pose + 21-landmark bilateral hands) from video footage.
- Contains 77 keyframes at 25 fps (3080 ms).
- **Known Kinematic Anomalies:** Frame 22 (elbow flare/hyperflexion), Frame 59 (palm interpenetration during contact), Frame 62 (asymmetrical thumb release).
- **Quarantine Enforced:** The candidate clip is isolated in `tools/isl_motion_extraction/output/` and excluded from the production `KeyframeRegistry`. It cannot be promoted to production until reviewed and signed off in `tools/isl_motion_extraction/preview_mocap.html`.

---

## 4. Source Verification & Licensing Governance

### 4.1 Legal Hold on Reference Video (`LEGAL-01`)
- File: `tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4`.
- **Status:** **Missing by design under active legal hold**.
- **Rationale:** Video footage crawled from public sources has unresolved copyright and redistribution terms under third-party platform policies. While the extracted mathematical joint angles (GODL v1.0) are open data, raw binary video redistribution remains restricted.
- **Testing Impact:** Automated diagnostic scripts (`check_review_readiness.py`, `test_m4_stage5_validation.py`) intentionally report this single asset check as a controlled failure.

### 4.2 Outstanding Source Verification for Vocabulary Expansion (HELLO & THANK_YOU)
- During Milestone M8.1 and M8.2 investigations, official ISLRTC dictionary entries were verified conceptually, but direct open-access high-resolution video datasets with unambiguous commercial/redistribution licenses were not available locally.
- Review records created in `Docs/records/sign_record_hello.json` and `Docs/records/sign_record_thank_you.json` are formally assigned status:
  `"implementation_status": "BLOCKED_SOURCE_OR_REVIEW"`
- No 3D keyframe extraction may occur for these words until primary raw video datasets are officially archived with verified licensing.

---

## 5. Pending Human Reviews & Community Outreach

### 5.1 Review Protocol Architecture
SignBridge has established an end-to-end human review protocol documented in:
- `Docs/M4_STAGE_2_HUMAN_REVIEW_PROTOCOL.md` (Formal 5-parameter rubric: Handshape, Orientation, Location, Movement, Non-Manual Expression).
- `Docs/ISL_NAMASTE_REVIEW_CHECKLIST.md` (Session execution guide).
- `Docs/ISL_HELLO_REVIEW_WORKSHEET.md` & `Docs/ISL_THANK_YOU_REVIEW_WORKSHEET.md` (Standardized worksheets for panel evaluators).
- `tools/isl_motion_extraction/validate_review_record.py` (Cryptographic SHA-256 validation for review records).

### 5.2 Outreach Status Across Target Organizations
Formal outreach packages have been audited across 5 Indian organizations:
1. **ISLRTC** (Indian Sign Language Research and Training Centre, New Delhi).
2. **NAD India** (National Association of the Deaf, New Delhi).
3. **AIFD** (All India Federation of the Deaf, New Delhi).
4. **DEF** (Deaf EnAbled Foundation, Hyderabad).
5. **IGNOU** (Indira Gandhi National Open University - School of Foreign Languages / Sign Language Unit).

**Blockers to Execution:**
- Live panel sessions require funding allocation for qualified Deaf-native reviewer honoraria.
- Institutional memoranda of understanding (MoUs) for ethical data co-ownership remain unexecuted.
- Until certified Deaf-native reviewers evaluate clips in person or via the review studio (`preview_mocap.html`), SignBridge cannot claim linguistic authority.

---

## 6. Summary of Architectural Guarantees

Despite the limitations above, the frozen prototype enforces strict architectural boundaries:
1. **Zero Hallucinated Gestures:** The avatar will never play an unverified gesture or synthetic interpolation when speech is unrecognized or un-animated.
2. **Decoupled Contracts:** Contract schemas (`SignItem`, `SignSequence`) are deeply frozen and immutable, preventing mid-playback state corruption.
3. **Full Local Execution:** Speech transcription runs completely offline on `http://127.0.0.1:8765`, ensuring zero user audio is transmitted to external cloud APIs.
4. **Transparent Telemetry:** Every UI surface honestly reports whether an animation is playing, held in neutral pose, or awaiting human panel review.
