# SignBridge Milestone M3.15 — Reviewer Session Execution & Evidence Capture Report

**Milestone:** M3.15 — Reviewer Session Execution & Evidence Capture  
**Date:** October 2026  
**Status:** **HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND**  
**Execution Environment:** Purely offline local CPU execution (zero cloud inference, zero paid APIs)  
**Target Candidate:** `isl_namaste_mocap_candidate_v1` (Version: `1.0.0-experimental`)  
**Production Baseline (Unmodified):** `isl_namaste_godl_v1` in `extension/animation/keyframe_registry.js`  

---

## 1. Executive Summary

Milestone M3.15 audited and improved the reviewer session execution and evidence capture workflows for SignBridge Indian Sign Language (ISL) avatar animations.

In strict adherence to the project's evidence integrity standard—**Zero Fabrication of Human Evidence**—this report confirms that **no qualified human review has occurred yet**. No evaluator identity, rating, consensus approval, or feedback was fabricated. The milestone status remains officially:

> **`HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND`**

The milestone prioritized reviewer usability, non-leading assessment protocols, and evidence capture fidelity by:
1. Auditing the review studio for concrete usability barriers.
2. Adding explicit support for **declaring uncertainty and requesting further multi-angle evidence** directly within the review record.
3. Converting all scrutiny frame labels to neutral, non-leading wording.
4. Extending the review-record validator and regression test suite to enforce evidence request schema preservation.
5. Verifying that the production baseline (`isl_namaste_godl_v1`) remains isolated from experimental assets.

---

## 2. Usability Audit & Changes Implemented (Tasks 1 & 2)

An audit of the review studio (`tools/isl_motion_extraction/preview_mocap.html`) identified two critical usability gaps:
- **Gap 1: Inability to Declare Uncertainty or Request Additional Evidence:** Monocular 2D reference video introduces visual ambiguity during bilateral palm contact (*Anjali Mudra*). Evaluators previously had to choose between forced ratings or burying uncertainty in free-text notes.
- **Gap 2: Leading Phrasing in Scrutiny Checkboxes:** Scrutiny frame checkboxes previously included evaluative statements (e.g. *"Motion looks natural despite tracking loss"*), subtly steering the evaluator toward positive confirmation.

### Concrete Changes Implemented:
| Component | File | Change Description |
| :--- | :--- | :--- |
| **Evidence Request UI** | `preview_mocap.html` | Added an amber-highlighted checkbox (`#chk-need-evidence`) allowing reviewers to formally declare uncertainty and an input box (`#evidence-request-details`) to specify required angles/captures (e.g., side profile angle, slower capture). |
| **Neutral Scrutiny Labels** | `preview_mocap.html` | Replaced leading text with neutral labels: *"Frame 22 (880ms lift): Lift stroke inspected — naturalness confirmed (uncheck if jerky/unnatural)"*. |
| **Data Preservation** | `preview_mocap.html` | Updated `collectWorksheetData()` and `loadWorksheetState()` to preserve `furtherEvidenceRequested` and `evidenceRequestDetails` across JSON exports, local saves, and JSON reload cycles. |
| **Markdown Export** | `preview_mocap.html` | Added section `## 3. Rig Limitations & Evidence Requests` in generated Markdown summaries. |
| **Review Validator** | `validate_review_record.py` | Added extraction, validation, and reporting for `further_evidence_requested` and `evidence_request_details`. |
| **Validator Unit Tests** | `test_review_validator.py` | Added `test_further_evidence_request_supported` unit test (**9 / 9 tests passing**). |
| **Handoff Documentation** | `Docs/ISL_REVIEWER_HANDOFF.md` | Updated exact reference video filename (`ISLRTC_Namaste_sample.mp4`), added instructions for requesting further evidence, and reinforced reviewer independence. |

---

## 3. Review Integrity & Anti-Tamper Verification (Task 3)

The following integrity safeguards were verified:
1. **Hash Transparency:** Candidate SHA-256 (`6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46`) and reference video SHA-256 (`129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8`) are prominently displayed in the review studio header.
2. **Export Binding:** Exported JSON and Markdown records permanently record candidate ID, version, file hash, video file, and video hash.
3. **Template vs. Genuine Review Discrimination:** The review validator detects when a record contains mostly `unrated` dimensions or placeholder reviewer names, classifying it as `TEMPLATE_OR_UNRATED` rather than a completed evaluation.
4. **Hash Mismatch Protection:** The review studio displays an alert modal and an amber warning banner if an imported review references a different candidate hash, preventing cross-candidate attribution.
5. **Read-Only Ingestion:** `validate_review_record.py` opens review files in read-only mode (`"r"`). File byte contents and modification timestamps are mathematically unchanged before and after validation.
6. **Zero Cloud Calls:** The review studio and validator execute 100% locally on localhost without network calls or telemetry transmission.

---

## 4. The Six Validation Outcome States (Task 4)

SignBridge strictly delineates six validation outcome states:

| Outcome State | Definition | Current Status |
| :--- | :--- | :--- |
| **`TECHNICAL_CHECKS_PASSED`** | Pipeline builds, WebGL renders at 60 FPS, all 27 automated pre-session diagnostic checks pass. | **ACHIEVED** |
| **`HUMAN_REVIEW_PENDING`** | Studio, handoff guide, and validator ready; awaiting qualified Deaf-native / certified interpreter session. | **CURRENT STATE** |
| **`HUMAN_REVIEW_RECORDED`** | Traceable review records from qualified signers ingested and validated. | **PENDING** |
| **`LINGUISTIC_CONCERNS_UNRESOLVED`**| Evaluators submitted conflicting feedback or requested multi-camera evidence. | **PENDING** |
| **`REQUIRES_REVISION`** | Evaluators rejected candidate or requested specific retargeting adjustments. | **PENDING** |
| **`APPROVED_FOR_DEFINED_USE`** | Community consensus reached; minimum scores met; formal production promotion PR approved. | **NOT APPROVED** |

---

## 5. Reviewer-Facing Handoff Summary (Task 5)

[`Docs/ISL_REVIEWER_HANDOFF.md`](file:///C:/AmazonMlChallenge/Docs/ISL_REVIEWER_HANDOFF.md) and [`Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md`](file:///C:/AmazonMlChallenge/Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md) provide the complete, non-leading briefing for evaluators:
- **Independent Assessment:** Evaluators are explicitly instructed to assess the sign independently and never assume the avatar is correct.
- **Unvalidated Status:** Evaluators are informed that the animation is experimental and has not been linguistically validated.
- **Playback Controls:** Instructions explain how to use Spacebar, frame stepping ($\pm 40\text{ ms}$), variable speed controls ($1.0\times, 0.5\times, 0.25\times$), and scrutiny jump shortcuts (Frames 22, 40, 59, 62).
- **Documenting Uncertainty:** Evaluators are instructed on how to check *Declare Uncertainty / Request Further Evidence* and how to mark unrenderable non-manual markers as *Not Assessable*.
- **No Inferred Consensus:** No reviewer has been recruited, contacted, or agreed to participate. All handoff materials remain generic instructions ready for genuine deployment.

---

## 6. Production Baseline & Licensing Status

### Production Baseline Status:
- The production keyframe registry in [`extension/animation/keyframe_registry.js`](file:///C:/AmazonMlChallenge/extension/animation/keyframe_registry.js) continues mapping live speech tokens (`"namaste"`, `"greetings"`) strictly to the baseline clip `isl_namaste_godl_v1`.
- `isl_namaste_mocap_candidate_v1` is unexposed to live user speech.
- Zero production code was modified during this milestone.

### Licensing Status (Qualified Legal Provenance):
- **Source Video:** Originates from the Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India.
- **Verified Terms:** Published under the National Data Sharing and Accessibility Policy (NDSAP) via `data.gov.in` under the **Government Open Data License - India (GODL)**. This license grants worldwide, royalty-free, non-exclusive rights to adapt and create derivative works with mandatory attribution:
  > *"Source: Indian Sign Language Research and Training Centre (ISLRTC), via data.gov.in under GODL."*
- **Legal vs Linguistic Independence:** Copyright permission to extract keypoints from an open government dataset is strictly independent from linguistic validation. Legal rights do not confer linguistic correctness, and linguistic defects do not impair copyright compliance.

---

## 7. Automated Test Suite Execution (Task 6)

All test suites were executed offline on local CPU. All 199 checks passed with exit code 0:

| Test Suite | Command Line | Exit Code | Checks Passed | Status |
| :--- | :--- | :--- | :--- | :--- |
| **M3.14 Pre-Session Readiness** | `tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/check_review_readiness.py` | `0` | 27 / 27 | **PASSED** |
| **Review Record Validator Unit Tests** | `tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/tests/test_review_validator.py` | `0` | 9 / 9 | **PASSED** |
| **Review Readiness & Schema Tests** | `tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/tests/test_review_readiness.py` | `0` | 12 / 12 | **PASSED** |
| **Retargeting & Kinematics** | `tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/tests/test_retargeting.py` | `0` | 13 / 13 | **PASSED** |
| **In-Engine Chrome Tests (Suites 1–23)** | `tools\isl_motion_extraction\.venv\Scripts\python.exe run_chrome_tests.py` | `0` | 132 / 132 | **PASSED** |
| **Whisper Backend ASR Tests** | `signbridge-backend\.venv\Scripts\python.exe test_backend.py` *(from `signbridge-backend`)* | `0` | 8 / 8 | **PASSED** |
| **Review Directory Scan Diagnostic** | `tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/validate_review_record.py` | `0` | Clean Scan (`HUMAN REVIEW PENDING`) | **PASSED** |

**Total Automated Checks Across Project:** **199 / 199 checks passed** (Exit Code 0).

---

## 8. Remaining Usability & Technical Limitations

1. **Human Evaluation Pending:** Genuine evaluation requires direct participation of qualified Deaf-native ISL signers or certified DISLI interpreters.
2. **Rig Blendshape Limitation:** The Mixamo Y-Bot rig lacks facial blendshapes; grammatical facial morphemes cannot be rendered. Reviewers must continue marking facial non-manuals as *Not Assessable*.
3. **Monocular Occlusion Limitation:** MediaPipe Holistic achieves ~49.4% simultaneous bilateral hand visibility during *Anjali Mudra*. Frames 28–46 rely on heuristic wrist proximity clamping ($79.8\text{ mm}$ target). Evaluators may check *Declare Uncertainty* if multi-angle footage is necessary to evaluate palm separation.
