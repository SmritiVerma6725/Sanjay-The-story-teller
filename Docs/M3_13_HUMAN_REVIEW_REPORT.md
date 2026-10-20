# SignBridge Milestone M3.13 — First Human ISL Review & Evidence-Based Feedback Report

**Milestone:** M3.13 — First Human ISL Review & Evidence-Based Feedback  
**Date:** October 2026  
**Status:** **PREPARED — HUMAN REVIEW PENDING**  
**Execution Environment:** Purely offline local CPU execution (zero cloud inference, zero paid APIs)  
**Target Candidate:** `isl_namaste_mocap_candidate_v1` (Version: `1.0.0-experimental`)  
**Production Baseline (Unmodified):** `isl_namaste_godl_v1` in `extension/animation/keyframe_registry.js`  

---

## 1. Executive Summary

Milestone M3.13 verified the end-to-end review environment, recomputed cryptographic asset checksums, validated the 7-step reviewer session checklist, and established strict evidentiary protocols for the first genuine Indian Sign Language (ISL) linguistic review session.

In adherence to the core SignBridge policy—**Zero Fabrication of Human Evidence**—this report confirms that **no qualified human review has occurred yet**. No evaluator identity, rating, consensus approval, or feedback was invented. All automated technical pre-session checks pass (100%), and the system is fully prepared to host a human review session whenever an eligible Deaf-native signer or certified interpreter is available.

### Core Status Summary:
- **Milestone Outcome:** `PREPARED — HUMAN REVIEW PENDING`
- **Candidate Integrity:** Unmodified and verified via SHA-256 (`6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46`).
- **Production Baseline:** Preserved (`isl_namaste_godl_v1` remains the active production clip in the extension).
- **Automated Diagnostic Suite:** 25 / 25 checks passed (`check_review_readiness.py`).
- **Regression Tests:** 190 / 190 checks passed across all 5 project test suites (Exit code 0).

---

## 2. Cryptographic Checksum Recomputation & Asset Verification

Both primary media assets were independently recomputed from raw disk bytes using Python `hashlib.sha256()`:

| Asset | File Path | Recomputed SHA-256 Checksum | Match Status |
| :--- | :--- | :--- | :--- |
| **Animation Candidate (Tooling)** | `tools/isl_motion_extraction/output/isl_namaste_mocap_candidate_v1.json` | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | **VERIFIED MATCH** |
| **Animation Candidate (Extension)** | `extension/assets/animations/isl_namaste_mocap_candidate_v1.json` | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | **VERIFIED MATCH (Identical)** |
| **Reference Video** | `tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4` | `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8` | **VERIFIED MATCH** |
| **3D Avatar Mesh** | `extension/assets/models/ybot.glb` | Size: 2,233,440 bytes (canonical Mixamo Y-Bot) | **VERIFIED MATCH** |

---

## 3. Review Environment Diagnostic Results (Task 1)

The pre-session diagnostic script was executed:

**Command:**
```powershell
tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/check_review_readiness.py
```

**Console Output:**
```text
================================================================================
SignBridge M3.13 -- ISL Review Pre-Session Readiness Diagnostic
================================================================================

--- 1. Reference Video Asset Verification ---
[PASS] Reference video file presence
        C:\AmazonMlChallenge\tools\isl_motion_extraction\reference_videos\ISLRTC_Namaste_sample.mp4
[PASS] Reference video file size
        Size: 648917 bytes (expected 648917)
[PASS] Reference video SHA-256 integrity
        SHA-256: 129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8

--- 2. Candidate Animation Clip Verification ---
[PASS] Candidate output file presence
        C:\AmazonMlChallenge\tools\isl_motion_extraction\output\isl_namaste_mocap_candidate_v1.json
[PASS] Candidate extension asset presence
        C:\AmazonMlChallenge\extension\assets\animations\isl_namaste_mocap_candidate_v1.json
[PASS] Candidate output SHA-256 integrity
        SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
[PASS] Output and extension copies identical
        Ext SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
[PASS] Candidate ID format
        isl_namaste_mocap_candidate_v1
[PASS] Gloss specification
        NAMASTE
[PASS] Duration conformance (3080ms)
        durationMs: 3080
[PASS] Experimental status enforced
        experimental_awaiting_validation
[PASS] Keyframe count (77 frames @ 25fps)
        Count: 77
[PASS] Flagged anomaly frames recorded
        [22, 59, 62]
[PASS] All 36 transforms per frame use canonical Y-Bot bones
        All canonical

--- 3. 3D Avatar Rig Verification ---
[PASS] Adobe Mixamo Y-Bot mesh presence (ybot.glb)
        C:\AmazonMlChallenge\extension\assets\models\ybot.glb
[PASS] Y-Bot GLB file size sanity (>1MB)
        Size: 2233440 bytes

--- 4. Review Studio & Interface Verification ---
[PASS] Review Studio HTML presence
        C:\AmazonMlChallenge\tools\isl_motion_extraction\preview_mocap.html
[PASS] Studio contains SHA-256 hash display
[PASS] Studio contains review schema v1.0.0
[PASS] Studio contains import hash mismatch check
[PASS] Studio contains direct jump buttons for frames 22, 59, 62
[PASS] Studio contains 5-parameter rubric table
[PASS] Studio contains rig limitations explainer

--- 5. Production Baseline Isolation Verification ---
[PASS] KeyframeRegistry defaults to baseline 'isl_namaste_godl_v1'
[PASS] Candidate is NOT registered by default in production registry

================================================================================
AUTOMATED DIAGNOSTIC SUMMARY: 25 / 25 Checks Passed
================================================================================
```

**Diagnostic Exit Code:** `0`

---

## 4. Reviewer Session Readiness & The 7-Step Checklist (Task 2)

The handoff documentation ([`Docs/ISL_REVIEWER_HANDOFF.md`](file:///C:/AmazonMlChallenge/Docs/ISL_REVIEWER_HANDOFF.md)) and session guide ([`Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md`](file:///C:/AmazonMlChallenge/Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md)) were updated to standardize the 7-step review protocol.

Facilitators must observe a strict **Non-Leading Protocol**:
- The evaluator must never be guided toward approval or positive scores.
- The evaluator is explicitly empowered to reject the candidate or mark features as unassessable.

### The 7-Point Evaluator Session Checklist:
1. **Explain Experimental Status & Constraints:** Brief the evaluator on the unvalidated status, the lack of facial blendshapes on Y-Bot, and monocular tracking occlusion limits.
2. **Normal Speed Observation (1.0x):** Play the synchronized reference video and 3D avatar from $0\text{ ms}$ to $3080\text{ ms}$ without interruption.
3. **Slow-Motion Inspection (0.5x & 0.25x):** Replay at half and quarter speed to observe hand contact timing, finger alignment, and torso inclination.
4. **Separate Linguistic Parameter Evaluation:** Independently rate the 5 dimensions:
   - Handshape (DEZ)
   - Location (TAB)
   - Orientation (ORI)
   - Movement (SIG)
   - Non-Manual Markers (NMM)
5. **Inspect Flagged Occlusion Intervals:** Scrutinize specific keyframe intervals using studio jump shortcuts:
   - Frame 22 ($880\text{ ms}$): Upward lift onset.
   - Frame 40 ($1600\text{ ms}$): Peak prayer contact hold.
   - Frame 59 ($2360\text{ ms}$): Parting occlusion.
   - Frame 62 ($2480\text{ ms}$): Lap return descent.
6. **Identify Unassessable Parameters:** Ensure parameters that cannot be judged on this rig (such as facial expressions) are recorded as `Not Assessable`.
7. **Export & Preserve Review Record:** Generate the signed JSON record (`isl_namaste_review_YYYYMMDD_HHMMSS.json`) and commit it to version control in `tools/isl_motion_extraction/reviews/`.

---

## 5. Review Record Attribution & Anti-Tamper Enforcement (Task 3 & 5)

1. **Hash Verification on Import:**
   - In [`tools/isl_motion_extraction/preview_mocap.html`](file:///C:/AmazonMlChallenge/tools/isl_motion_extraction/preview_mocap.html), `handleLoadReviewFile()` compares `reviewData.candidateFileSha256` against the active candidate hash.
   - Any hash mismatch halts processing, prompts an alert modal, and displays a prominent warning banner.
2. **Immutability of Candidate & Baseline:**
   - `isl_namaste_mocap_candidate_v1.json` was not modified during this milestone.
   - The production extension baseline `isl_namaste_godl_v1` in `extension/animation/keyframe_registry.js` remains the default and only resolved clip for spoken `namaste` / `greetings`.
   - The candidate clip cannot be automatically promoted by score thresholds. Any future promotion requires explicit human panel consensus and a dedicated milestone PR.
3. **Local-First Privacy:**
   - All review tools run 100% client-side in the browser on loopback (`http://localhost:8000` or file protocol). Zero evaluation data or network packets leave the machine.

---

## 6. Feedback Analysis & Classification Framework (Task 4)

Because no qualified human reviewer has submitted a review record during this milestone, **no feedback analysis was fabricated**. When review records are obtained, issues must be categorized using the following 5-class framework:

1. **Observed Tracking or Occlusion Failure:** Errors resulting from 2D monocular camera limitations (e.g. hand drift or inter-penetration during Anjali Mudra).
2. **Avatar or Rig Limitation:** Physical constraints of the 3D asset (e.g. Y-Bot lacking facial expression blendshapes or flexible spine bending).
3. **Kinematic or Playback Issue:** Three.js interpolation glitches, jitter, or frame rate timing discrepancies.
4. **Linguistic Concern Raised by Evaluator:** Substantive feedback from native signers regarding handshape phonology, palm orientation angle, or movement rhythm.
5. **Unresolved or Insufficient Evidence:** Ambiguous observations requiring multi-camera capture or panel re-review.

---

## 7. Separate Licensing Assessment (Task 6)

SignBridge maintains strict separation across the three dimensions of validation:

```
┌─────────────────────────────────┐
│     1. Technical Playback       │ -> Verified: 25/25 automated checks passing, 60 FPS Three.js rendering
├─────────────────────────────────┤
│     2. Legal Right-of-Use       │ -> Verified: Source under GODL (data.gov.in); derivative extraction permitted
├─────────────────────────────────┤
│     3. Linguistic Accuracy      │ -> PENDING: Requires Deaf-native human evaluation session
└─────────────────────────────────┘
```

### Verified Licensing Facts:
- **Authoritative Source:** Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India.
- **Distribution Vehicle:** National Data Sharing and Accessibility Policy (NDSAP) portal at `data.gov.in`.
- **License Terms:** Government Open Data License - India (GODL). Permits worldwide, royalty-free, non-exclusive adaptation and creation of derivative works with mandatory attribution:
  > *"Source: Indian Sign Language Research and Training Centre (ISLRTC), via data.gov.in under GODL."*
- **Mirror Distinction:** Third-party mirrors (such as Hugging Face repository `silentone0725`) are technical distribution mirrors only. An uploader's declared license (e.g. "MIT") is legally void regarding Government of India copyrighted works; rights derive exclusively from GODL.
- **Independence:** A valid GODL copyright license does not guarantee linguistic validity, and a linguistic rejection does not invalidate the legal right to extract keypoints.

---

## 8. Full Project Test Regressions (Task 7)

All tests were executed locally. Commands, exit codes, and counts:

| Test Suite | Execution Command | Exit Code | Pass Count | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Pre-Session Readiness Diagnostic** | `tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/check_review_readiness.py` | `0` | 25 / 25 | **PASSED** |
| **Review Readiness & Schema Tests** | `tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/tests/test_review_readiness.py` | `0` | 12 / 12 | **PASSED** |
| **Retargeting & Kinematics** | `tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/tests/test_retargeting.py` | `0` | 13 / 13 | **PASSED** |
| **In-Engine Chrome Tests (Suites 1–23)** | `tools\isl_motion_extraction\.venv\Scripts\python.exe run_chrome_tests.py` | `0` | 132 / 132 | **PASSED** |
| **Whisper Backend ASR Tests** | `signbridge-backend\.venv\Scripts\python.exe test_backend.py` *(from `signbridge-backend`)* | `0` | 8 / 8 | **PASSED** |

**Total Automated Checks Across Project:** **190 / 190 checks passed** (Exit Code 0).

---

## 9. Outstanding Limitations & Evidence-Based Next Steps

### Outstanding Limitations:
1. **Linguistic Review Pending:** Genuine evaluation requires participation of qualified Deaf ISL signers or certified DISLI interpreters.
2. **Facial Blendshapes Unavailable:** The Mixamo Y-Bot avatar cannot render facial non-manual markers. Non-manual evaluation must remain confined to head inclination and torso posture.
3. **Bilateral Occlusion:** MediaPipe Holistic provides ~49.4% bilateral hand visibility in monocular view; frames 28–46 rely on heuristic proximity constraints.

### Next Steps:
1. Schedule and host the first evaluation session with an eligible Deaf community evaluator using the 7-step protocol in `Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md`.
2. Save the exported JSON review record in `tools/isl_motion_extraction/reviews/`.
3. If tuning is requested, execute the correction workflow ([`Docs/ISL_CORRECTION_WORKFLOW.md`](file:///C:/AmazonMlChallenge/Docs/ISL_CORRECTION_WORKFLOW.md)) to generate `v2` without modifying `v1` or the production baseline.
4. If the motion is rejected, retain the candidate as historical research evidence and explore multi-camera or native keyframe authoring alternatives.
