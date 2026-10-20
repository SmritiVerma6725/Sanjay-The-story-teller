# SignBridge M3.18 — External ISL Reviewer Recruitment & Feedback Intake Readiness

**Document Reference:** `Docs/M3_18_EXTERNAL_REVIEW_READINESS.md`  
**Milestone:** M3.18 — External ISL Reviewer Recruitment & Feedback Intake  
**Execution Date:** October 2026  
**Status:** **HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Hand-authored canonical slice)  
**Experimental Motion Candidate:** `isl_namaste_mocap_candidate_v1` (MediaPipe Holistic retargeted reconstruction)  

---

## Executive Summary

SignBridge Milestone M3.18 prepares the system for genuine, independent external human review of the motion-capture reconstruction candidate `isl_namaste_mocap_candidate_v1`. 

In accordance with strict evidence integrity principles:
1. **Recruitment Materials Assembled:** An external reviewer invitation document ([`Docs/ISL_REVIEWER_INVITATION.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEWER_INVITATION.md)) has been authored with transparent statements of experimental status, neutral evaluation expectations, clear consent/privacy rules, and open requests for evaluator linguistic background without presumption.
2. **Review Packet Finalized:** The handoff packet and interactive studio ([`tools/isl_motion_extraction/preview_mocap.html`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/preview_mocap.html)) enforce open-ended qualitative observations before discrete scoring, four balanced categorical findings, explicit uncertainty declarations, and cryptographic SHA-256 asset binding.
3. **Review Integrity Guaranteed:** The live review storage directory (`tools/isl_motion_extraction/reviews/`) contains zero fabricated records. Unknown fields cannot override protected provenance or identity metadata. Ingestion remains strictly read-only.
4. **Authoritative Provenance & Licensing Verified:** Video source access terms under Government Open Data License - India (GODL) on `data.gov.in` have been reconciled against the `islrtc.nic.in` portal terms; redistribution limitations are explicitly marked as **unresolved** rather than asserting unconfirmed rights.
5. **Reconciled Test Reporting:** All 9 test suites across the Chrome runtime, CDP browser usability, Python unit tests, pre-flight diagnostics, and FastAPI backend were executed independently and passed with exit code `0`.

---

## 1. Reviewer Outreach Materials (Task 1)

The formal reviewer invitation document has been authored at:
[`Docs/ISL_REVIEWER_INVITATION.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEWER_INVITATION.md)

### Key Outreach Provisions:
- **Concise Project & Candidate Description:** Describes SignBridge's local-first, zero-cloud architecture and the specific 3D reconstruction of *Namaste* (ISLRTC Dictionary Vol 1, Word #0001).
- **Transparent Statement of Experimental Status:** Explicitly warns that the candidate was generated via an automated computer-vision pipeline, has **not** been linguistically certified, and must not be treated as authoritative sign language.
- **Review Commitment & Time Expectations:** Clear guidance that the review takes 15–25 minutes, detailing the step-by-step procedure.
- **Open Request for Evaluator Background:** Invites evaluators to specify their signing fluency (Deaf-native signer, certified interpreter, deaf educator, linguist, or community user) without presuming any specific identity. Anonymous or pseudonymous participation is fully supported.
- **Voluntary Participation & Compensation:** States transparently that SignBridge is an open-source, zero-budget research prototype. Reviewer participation is voluntary unless an institutional sponsor or formal honorarium agreement is arranged in advance.
- **Reviewer Independence & Right to Dissent:** Reviewers are expressly told that the avatar may be flawed, that negative verdicts (`Unacceptable`, `Requires Tuning`) and `Not Assessable` declarations are equally valid and valued, and that reviewers may decline or stop at any time.
- **Zero Fabricated Personnel:** No reviewer names, credentials, institutional affiliations, or agreements have been fabricated. No external communication will be transmitted without explicit authorization.

---

## 2. Neutral Review Packet Finalization (Task 2)

The review packet comprises:
1. **Reviewer Invitation:** [`Docs/ISL_REVIEWER_INVITATION.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEWER_INVITATION.md)
2. **Reviewer Handoff Guide:** [`Docs/ISL_REVIEWER_HANDOFF.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEWER_HANDOFF.md)
3. **Session Guide & Protocol:** [`Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md`](file:///c:/AmazonMlChallenge/Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md)
4. **Fillable Feedback Template:** [`Docs/ISL_REVIEW_FEEDBACK_TEMPLATE.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEW_FEEDBACK_TEMPLATE.md)
5. **Correction Workflow:** [`Docs/ISL_CORRECTION_WORKFLOW.md`](file:///c:/AmazonMlChallenge/Docs/ISL_CORRECTION_WORKFLOW.md)
6. **Side-by-Side Review Studio:** [`tools/isl_motion_extraction/preview_mocap.html`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/preview_mocap.html)

### Cryptographic Asset Binding:
- **Candidate Animation Asset (`isl_namaste_mocap_candidate_v1.json`):**  
  `SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46`  
  *(Verified identical across tooling output and Chrome extension directories).*
- **Reference Video Asset (`ISLRTC_Namaste_sample.mp4`):**  
  `SHA-256: 129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8`  
  *(648,917 bytes, 1080p HEVC @ 25 FPS).*

### Packet Verification Checklist:
- [x] **Open-ended qualitative notes precede discrete rating tables** (Step 1 in review studio and feedback template).
- [x] **Balanced 4-tier rubric** (`Acceptable`, `Minor Issue`, `Unacceptable`, `Not Assessable`) across Handshape, Location, Orientation, Movement, and Non-Manuals.
- [x] **Clear avatar rig limitations** (Mixamo Y-Bot rigid face documented; facial expressions marked `Not Assessable`).
- [x] **Dedicated uncertainty declaration** and evidence request field (`furtherEvidenceRequested` / `evidenceRequestDetails`).
- [x] **Clear three-tier validation distinction:**
  - *Tier 1 (Technical Feasibility):* Automated checks pass, 67 bones articulated, WebGL 60 FPS $\rightarrow$ **ACHIEVED**.
  - *Tier 2 (Linguistic Review):* Traceable feedback recorded from qualified human signers $\rightarrow$ **PENDING REVIEW**.
  - *Tier 3 (Approved for Defined Use):* Panel consensus achieved, limitations documented, production promotion authorized $\rightarrow$ **NOT APPROVED**.

---

## 3. Review Integrity Protection (Task 3)

### 3.1 Live Storage Isolation
- The dedicated review storage directory `tools/isl_motion_extraction/reviews/` contains **zero review records** (contains only `README.md` defining audit rules).
- No simulated, synthetic, or preliminary review records have been placed in the directory.
- Running `python tools/isl_motion_extraction/validate_review_record.py` reports:
  `STATUS: HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND`.

### 3.2 Schema Validation & Tamper Protection
The review validator ([`validate_review_record.py`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/validate_review_record.py)) enforces:
1. **Schema Family Enforcement:** Records outside `signbridge_review_schema_v1.*` are rejected with hard errors.
2. **Asset ID & Hash Binding:** Mismatches between the record's candidate ID or SHA-256 hash and the active asset are rejected as `HASH_MISMATCH` or `SCHEMA_VIOLATION`.
3. **Reference Video Integrity:** Substitutions of reference video hashes are detected and flagged.
4. **Protected Metadata Immutability:** In `preview_mocap.html` (`collectWorksheetData`), imported unknown/extended fields are filtered through a strict exclusion list. Protected identity and provenance fields (`candidateId`, `candidateFileSha256`, `referenceVideoSha256`, `reviewSchemaVersion`, `validationStatus`) can **never** be overridden by arbitrary imported JSON properties.
5. **Read-Only Ingestion:** The validation tool operates purely in memory, never modifying, rewriting, or updating on-disk review files.

---

## 4. Provenance & Licensing Boundaries (Task 4)

A rigorous audit of the reference video provenance and legal terms was performed:

| Attribution Dimension | Verified Fact / Documented Record | Legal Interpretation & Governance Boundary |
| :--- | :--- | :--- |
| **Source Entity** | Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India. | Primary national authority for Indian Sign Language lexicography. |
| **Source Corpus** | ISLRTC 10,000-Word Dictionary, Volume 1, Word #0001 (*Namaste* / *Greetings*). | Official dictionary reference performance. |
| **Open Data Platform** | Open Government Data Platform India (`data.gov.in`), National Data Sharing and Accessibility Policy (NDSAP). | Public dataset published under Government Open Data License - India (GODL). |
| **GODL License Terms** | Grants a worldwide, royalty-free, non-exclusive license to use, adapt, modify, extract, and create derivative works, with mandatory attribution: *"Source: ISLRTC via data.gov.in under GODL."* | **Permits derivative feature extraction** (e.g. computer vision landmark coordinates and 3D retargeted keyframes). GODL does **not** certify linguistic correctness of derivative products. |
| **ISLRTC Portal Notice (`islrtc.nic.in`)** | The DEPwD portal copyright policy states: *"Contents of this website may not be reproduced partially or fully, without due permission from ISLRTC."* | **Unresolved Conflict:** Direct web scraping of the portal is restricted. Assets must originate from the data.gov.in open release. |
| **Hugging Face Mirror (`silentone0725`)** | The video sample was accessed via a third-party HEVC re-encoded mirror (`silentone0725/isl-dictionary-videos`), accessed October 2026. The uploader asserted "MIT", which is legally defective as third parties cannot re-license government works. | **Unresolved Distribution Right:** Rights derive from GODL, not MIT. |
| **Final Licensing Determination** | Extraction of skeletal motion coordinates is permitted under GODL derivative rights. However, bundling and redistributing the raw reference MP4 video file in a public application carries an unresolved legal condition. | **ACTION TAKEN:** The raw reference video is restricted to offline local review tooling (`tools/isl_motion_extraction/reference_videos/`) and is **strictly excluded** from the distributed Chrome extension package (`extension/`). |

---

## 5. Comprehensive Suite-by-Suite Test Evidence (Task 5)

All 9 test suites were executed independently in their respective runtime environments. Each suite tests a distinct architectural layer:

| # | Test Suite | Scope & Boundary | Execution Command | Exit Code | Observed Result |
|---|:---|:---|:---|:---:|:---|
| **1** | **Review Validator Unit Suite** | Schema validation, hash tampering detection, missing metadata, template vs. completed classification, and read-only behavior. | `python tools/isl_motion_extraction/tests/test_review_validator.py` | `0` | **9 / 9 PASSED** (0.142s) |
| **2** | **Review Round-Trip Test Suite** | Serialization, rich Unicode (Hindi/English), multiline notes, uncertainty, unknown field preservation, and neutral markdown export. | `python tools/isl_motion_extraction/tests/test_review_roundtrip.py` | `0` | **10 / 10 PASSED** (0.223s) |
| **3** | **Headless Chrome Browser Usability CDP Suite** | Headless Chrome interactive testing of `preview_mocap.html` over CDP (DOM init, scrubbing, jumps, rubric, uncertainty, local storage, markdown). | `python tools/isl_motion_extraction/tests/test_browser_usability.py` | `0` | **15 / 15 PASSED** |
| **4** | **Review Readiness Unit Suite** | Candidate clip metadata, bone count (67), canonical joints, duration (3080ms), coordinate spaces, and Y-Bot compatibility. | `python tools/isl_motion_extraction/tests/test_review_readiness.py` | `0` | **12 / 12 PASSED** (0.147s) |
| **5** | **Retargeting Pipeline Unit Suite** | Landmark extraction, quaternion math, kinematic contact solvers, temporal smoothing, and candidate export. | `python tools/isl_motion_extraction/tests/test_retargeting.py` | `0` | **13 / 13 PASSED** (0.129s) |
| **6** | **Pre-Flight Diagnostic Tool** | Standalone pre-flight checklist verifying file sizes, SHA-256 hashes, Y-Bot rig presence, and production isolation. | `python tools/isl_motion_extraction/check_review_readiness.py` | `0` | **27 / 27 CHECKS PASSED** |
| **7** | **Review Ingestion Tool** | Read-only scanner of `tools/isl_motion_extraction/reviews/`. | `python tools/isl_motion_extraction/validate_review_record.py` | `0` | **0 records detected**<br>`STATUS: HUMAN REVIEW PENDING` |
| **8** | **Backend Speech Recognition Suite** | FastAPI / faster-whisper server health, speech transcription, sequential audio slicing, and loopback privacy boundary. | `.venv\Scripts\python.exe test_backend.py` *(in `signbridge-backend/`)* | `0` | **8 / 8 PASSED** |
| **9** | **Chrome In-Engine Regression Suite** | Extension Manifest V3, WebGL rendering, translation pipeline, keyframes, and retargeting contracts in real Chrome DOM. | `python run_chrome_tests.py` | `0` | **132 / 132 PASSED**<br>(M1: 9, M2: 10, M3: 113) |

*Accounting Methodology:* The test counts represent independent evaluations across distinct runtime boundaries:
- In-engine browser runtime tests (132 tests)
- Live CDP browser usability checks (15 checks)
- Algorithmic and schema unit tests (44 tests across 4 suites)
- Diagnostic pre-flight checks (27 checks)
- Backend speech recognition tests (8 tests)

They are not summed into a single deceptive number.

---

## 6. Current Governance & Production Status

```
================================================================================
FINAL GOVERNANCE STATUS:
HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND

Active Production Baseline:   isl_namaste_godl_v1 (Active in extension)
Experimental Candidate:      isl_namaste_mocap_candidate_v1 (Awaiting review)
Review Storage Directory:     tools/isl_motion_extraction/reviews/ (0 genuine records)
Production Speech Routing:    Spoken "namaste" -> isl_namaste_godl_v1
================================================================================
```

### Readiness for Human Evaluators:
SignBridge is fully prepared for genuine, independent human review:
- Evaluator invitation materials are neutral, transparent, and ready to share ([`Docs/ISL_REVIEWER_INVITATION.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEWER_INVITATION.md)).
- The side-by-side inspection studio runs 100% offline with zero cloud telemetry.
- Ingestion tooling is ready to validate genuine review JSON records upon submission without risk of data tampering or false attribution.
