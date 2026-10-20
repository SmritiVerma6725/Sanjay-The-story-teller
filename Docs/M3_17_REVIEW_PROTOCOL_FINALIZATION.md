# SignBridge M3.17 — Review Protocol Finalization & External Reviewer Handoff

**Document Reference:** `Docs/M3_17_REVIEW_PROTOCOL_FINALIZATION.md`  
**Milestone:** M3.17 — Review Protocol Finalization & External Reviewer Handoff  
**Execution Date:** October 2026  
**Status:** **HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Hand-authored canonical slice)  
**Experimental Motion Candidate:** `isl_namaste_mocap_candidate_v1` (MediaPipe Holistic retargeted reconstruction)  

---

## Executive Summary

SignBridge Milestone M3.17 finalizes a neutral, reproducible, and verifiable Indian Sign Language (ISL) review protocol and external reviewer handoff package. In accordance with strict evidence integrity standards:
- **Zero Fabricated Evidence:** No synthetic evaluator records or artificial ratings have been generated.
- **Traceable Provenance:** Every candidate file, reference video, and export format is bound to cryptographic SHA-256 checksums.
- **Evaluator Neutrality:** Evaluator-facing tools and session guides prompt for open-ended, spontaneous observations before presenting discrete evaluation parameters. Positive, negative, uncertain, and not-assessable options are equally accessible, and the default verdict is inconclusive.
- **Clear Governance Boundaries:** Technical execution readiness is strictly distinguished from linguistic validation. The experimental motion candidate remains excluded from production speech routing.
- **Test Reconciliation:** All test suites have been audited, with exact command lines, exit codes, and counting methodologies reported without misleading overlap or double-counting.

---

## 1. Neutrality Audit Findings & Protocol Updates (Task 1)

All reviewer-facing prompts, button labels, session guides, and feedback worksheets were audited to eliminate leading language and prevent false assumptions.

### 1.1 Structural Changes to Evaluation Flow
In `tools/isl_motion_extraction/preview_mocap.html`, the evaluation worksheet was re-architected into sequential steps:
1. **Step 1 — Open-Ended Observations & Spontaneous Impressions:**  
   Reviewers are prompted to describe their initial impressions, kinematic stiffness, posture, bilateral symmetry, cultural nuances, or areas of uncertainty in their own words *before* viewing discrete scoring categories.
2. **Step 2 — Structured Parameter Assessment:**  
   The five phonological parameters (Handshape, Location, Orientation, Movement, Non-Manual Markers) provide four equally prominent categorical options: `Acceptable`, `Minor Issue`, `Unacceptable`, `Not Assessable`. Non-manual markers clearly acknowledge that the Mixamo Y-Bot rig lacks facial blendshapes, defaulting to `Not Assessable (Rig Limitation)`.
3. **Step 3 — Key Transition Interval Scrutiny:**  
   Neutralized checkboxes for flagged tracking anomaly frames (Frames 22, 59, 62) clarify that motion is evaluated without presumption:
   - Frame 22 ($880\text{ ms}$ lift stroke): Check if upward motion appears acceptable; leave unchecked if distorted or unassessed.
   - Frame 59 ($2360\text{ ms}$ hand separation): Check if hand separation appears smooth; leave unchecked if distorted or unassessed.
   - Frame 62 ($2480\text{ ms}$ lap rest): Check if descent to lap appears clean; leave unchecked if distorted or unassessed.
4. **Step 4 — Uncertainty Declaration & Further Evidence Request:**  
   Reviewers can declare uncertainty and specify additional evidence required (e.g., side profile video, multi-angle capture, slower frame rate, or facial blendshapes).
5. **Step 5 — Overall Recommendation Verdict:**  
   Provides four balanced determinations with `Not Assessable / Inconclusive` selected by default:
   - `Provisional Approval for Further Review` (Explicitly noted: *Eligible for broader panel review; NOT approved for production*).
   - `Requires Revisions / Tuning` (Kinematic or linguistic adjustments needed).
   - `Rejected` (Unacceptable or misleading ISL representation).
   - `Not Assessable / Inconclusive` (Insufficient evidence or rig limitations prevent assessment).

### 1.2 Neutrality Principles Enforced
- **No Presumption of Correctness:** The review studio and documentation state explicitly that the avatar candidate is unvalidated and may contain significant tracking artifacts.
- **Tracking Confidence $\neq$ Sign Accuracy:** Computer vision tracking states (`REST_INTERPOLATED`, `CONTACT_CONSTRAINED`, `LOW_CONFIDENCE`) are displayed as technical telemetry rather than linguistic accuracy.
- **Provisional Approval $\neq$ Production Approval:** Provisional approval only qualifies a candidate for multi-signer panel scrutiny; production promotion remains blocked.
- **No Single Metric Dominance:** Bilateral solver convergence, landmark confidence, and frame-rate benchmarks do not dictate or influence the human verdict.

---

## 2. Review Record Schema & Compatibility Results (Task 2)

The review record validator (`tools/isl_motion_extraction/validate_review_record.py`) was evaluated for schema validation, tamper detection, and forward compatibility.

### 2.1 Compatibility Matrix

| Condition | Tested Behavior | Validator Result | Status |
| :--- | :--- | :--- | :--- |
| **Valid Complete Record** | Evaluates valid schema `signbridge_review_schema_v1.0.0` with matching hashes. | Clean pass; zero errors. | ✔ PASS |
| **Unsupported Schema Version** | Schema version outside `signbridge_review_schema_v1.*` family. | Rejection with hard validation error. | ✔ PASS |
| **Conflicting Candidate ID** | Record specifies mismatched candidate ID (e.g. `isl_namaste_mocap_v2`). | Hard rejection (`Candidate ID mismatch`). | ✔ PASS |
| **Candidate Hash Mismatch** | Record specifies valid candidate ID but incorrect SHA-256 hash. | Hard rejection (`Candidate SHA-256 mismatch`). | ✔ PASS |
| **Reference Video Hash Mismatch** | Record references altered or substituted reference video. | Hard rejection (`Reference video SHA-256 mismatch`). | ✔ PASS |
| **Missing Identity Metadata** | Reviewer profile lacks required fields (`role` or `date`). | Hard rejection (`Missing required reviewer field`). | ✔ PASS |
| **Unknown / Extended Fields** | Future metadata added (e.g. `evaluatorPanelAffiliation`). | Preserved in `res.data` with non-fatal warning. | ✔ PASS |
| **Malformed / Corrupt JSON** | Non-JSON text or truncated byte streams. | Clean parse failure; zero silent corruption. | ✔ PASS |
| **Read-Only Ingestion** | Validator scans files without modifying on-disk bytes or timestamps. | Verified strictly read-only; zero mutation. | ✔ PASS |

---

## 3. Reconciled Test Reporting & Evidence (Task 3)

### 3.1 Test Count Discrepancy Resolution
In milestone M3.16, the Chrome in-engine runner reported 19 checks, while earlier milestones reported 124 or 132 checks. Investigation identified the root cause:
- **Root Cause:** In `run_chrome_tests.py`, headless Chrome ran with `--virtual-time-budget=5000` (5 seconds). The M1 suite (9 checks) and M2 suite (10 checks) finished within 1.5 seconds, totaling 19 checks. However, the comprehensive M3 suite (`test_m3_suite.html`) executes 113 async Three.js WebGL and retargeting tests across 23 sub-suites, requiring approximately 8–10 seconds. At 5000ms, Chrome dumped the DOM while M3's summary element still read `"Running tests..."`.
- **Resolution:** Updated `run_chrome_tests.py` to allocate a 25000ms virtual time budget for M3 (`'25000' if 'm3' in test_url else '6000'`).
- **Observed Result:** Headless Chrome now captures all 113 M3 tests, correctly reporting **132 / 132 tests passing** (9 in M1 + 10 in M2 + 113 in M3).

### 3.2 Comprehensive Suite-by-Suite Test Execution

All test suites were executed independently in their respective runtime environments:

| Suite Name | Scope & Methodology | Execution Command | Exit Code | Observed Result |
| :--- | :--- | :--- | :---: | :--- |
| **Chrome In-Engine Regression Suite** | Real browser DOM execution of extension M1, M2, and M3 data contract/rendering tests. | `python run_chrome_tests.py` | `0` | **132 / 132 PASSED**<br>(M1: 9, M2: 10, M3: 113) |
| **Browser Usability CDP Suite** | Headless Chrome interactive testing of `preview_mocap.html` over Chrome DevTools Protocol (CDP). | `python tools/isl_motion_extraction/tests/test_browser_usability.py` | `0` | **15 / 15 PASSED** |
| **Review Round-Trip Test Suite** | Python unit tests for review record serialization, rich Unicode, uncertainty, and unknown-field round trips. | `python tools/isl_motion_extraction/tests/test_review_roundtrip.py` | `0` | **10 / 10 PASSED** |
| **Review Validator Unit Suite** | Python unit tests for schema validation, tamper detection, missing metadata, and read-only behavior. | `python tools/isl_motion_extraction/tests/test_review_validator.py` | `0` | **9 / 9 PASSED** |
| **Review Readiness Unit Suite** | Python unit tests for candidate clip metadata, geometry, coordinate spaces, and Y-Bot compatibility. | `python tools/isl_motion_extraction/tests/test_review_readiness.py` | `0` | **12 / 12 PASSED** |
| **Retargeting Pipeline Unit Suite** | Python unit tests for landmark extraction, quaternion math, kinematic solvers, and candidate export. | `python tools/isl_motion_extraction/tests/test_retargeting.py` | `0` | **13 / 13 PASSED** |
| **Review Pre-Flight Diagnostic** | Standalone pre-flight checklist verifying file sizes, SHA-256 hashes, Y-Bot rig, and isolation. | `python tools/isl_motion_extraction/check_review_readiness.py` | `0` | **27 / 27 CHECKS PASSED** |
| **Backend Speech Recognition Suite** | FastAPI / faster-whisper server health, transcription, streaming slices, and loopback privacy tests. | `.venv\Scripts\python.exe test_backend.py` *(in `signbridge-backend/`)* | `0` | **8 / 8 PASSED** |
| **Review Record Ingestion Tool** | Read-only scanner of `tools/isl_motion_extraction/reviews/`. | `python tools/isl_motion_extraction/validate_review_record.py` | `0` | **0 records detected**<br>`STATUS: HUMAN REVIEW PENDING` |

*Note on Test Counting:* The above suites test distinct software layers. The 132 Chrome in-engine tests validate client-side browser runtime modules; the 15 browser usability checks validate live interactive UI behavior; the 44 Python unit tests validate data schemas and retargeting algorithms; the 27 diagnostic checks validate static asset integrity; and the 8 backend tests validate speech recognition. They are reported separately and not aggregated into an arbitrary single count.

---

## 4. Human-Review Handoff Package (Task 4)

The reviewer handoff package is assembled and ready for deployment to external reviewers:
- **Handoff Guide:** `Docs/ISL_REVIEWER_HANDOFF.md`
- **Session Guide:** `Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md`
- **Feedback Template:** `Docs/ISL_REVIEW_FEEDBACK_TEMPLATE.md`
- **Correction Workflow:** `Docs/ISL_CORRECTION_WORKFLOW.md`
- **Review Studio UI:** `tools/isl_motion_extraction/preview_mocap.html`

### 4.1 Verified Checksums & Traceability

```
Candidate Animation Asset (tools & extension identical):
SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46

Reference Video Asset (ISLRTC Dictionary Vol 1, Word #0001):
SHA-256: 129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8
```

### 4.2 Reviewer Rights & Neutral Participation
- Participation is voluntary and confidential; anonymous identifiers or pseudonyms are accepted.
- Evaluators are explicitly informed that they have full authority to reject the animation, request additional video evidence, or declare the sign not assessable.
- No evaluator has been contacted or claimed to participate prior to formal recruitment.

---

## 5. Production & Licensing Boundaries (Task 5)

### 5.1 Production Speech Translation Routing
- The active Chrome extension runtime strictly routes the speech transcript for `"namaste"` to the canonical hand-authored clip `isl_namaste_godl_v1`.
- The experimental motion candidate `isl_namaste_mocap_candidate_v1` is excluded from default lexicon resolution in `KeyframeRegistry`.
- Automated tests (Suite 21 & Suite 23) verify that speech transcription triggers only the approved production baseline, preventing automatic promotion.

### 5.2 Authoritative Licensing Analysis

| Asset / Source | Declared License | Video Access Rights | Derivative Extraction Rights | Redistribution Rights | Governance Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ISLRTC National Dictionary (data.gov.in)** | Government Open Data License - India (GODL) | Publicly accessible under NDSAP policy. | **Permitted:** Adapt, modify, extract, and build derivative models/keyframes. | **Permitted:** Must include mandatory attribution: *"Source: ISLRTC via data.gov.in under GODL."* | **Does NOT certify accuracy:** GODL grants copyright permission, not linguistic or cultural approval. |
| **ISLRTC Web Portal (`islrtc.nic.in`)** | All Rights Reserved (DEPwD) | Browsing permitted on official portal. | **Restricted:** Reproduction or extraction prohibited without written permission. | **Prohibited:** Cannot scrape or redistribute portal downloads. | Assets must originate exclusively from the official data.gov.in GODL open release. |
| **Adobe Mixamo Y-Bot Rig (`ybot.glb`)** | Adobe Mixamo Terms of Use | Free download via Mixamo account. | **Permitted:** Rigging, retargeting, and animation rendering in applications. | **Conditional:** Permitted within application bundle; raw standalone asset redistribution restricted. | Rig contains zero sign language data; facial expressions are unrenderable. |
| **MediaPipe Holistic Models** | Apache-2.0 | Free download via Google AI Edge. | **Permitted:** Landmark detection on local CPU. | **Permitted:** Standard Apache-2.0 attribution. | Monocular tracking drops during hand contact/overlap. |

---

## 6. Current Governance Status

```
================================================================================
FINAL GOVERNANCE STATUS:
HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND

Active Production Baseline:  isl_namaste_godl_v1 (Unchanged)
Experimental Candidate:     isl_namaste_mocap_candidate_v1 (Pending qualified review)
Review Storage Directory:    tools/isl_motion_extraction/reviews/ (0 genuine records)
================================================================================
```

### Next Steps:
1. Deliver the finalized handoff package (`Docs/ISL_REVIEWER_HANDOFF.md`) to qualified Deaf-native signers or certified interpreters.
2. Receive genuine, cryptographically bound review records and store them in `tools/isl_motion_extraction/reviews/`.
3. Ingest and validate records using `validate_review_record.py` to inform milestone M3.18 validation or kinematic tuning.
