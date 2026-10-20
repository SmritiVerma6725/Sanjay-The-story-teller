# SignBridge M3.19 — Independent ISL Review & Evidence-Based Decision Report

**Document Reference:** `Docs/M3_19_REVIEW_EXECUTION_REPORT.md`  
**Milestone:** M3.19 — Independent ISL Review & Evidence-Based Decision  
**Execution Date:** October 2026  
**Status:** **HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Active in extension)  
**Experimental Motion Candidate:** `isl_namaste_mocap_candidate_v1` (Retained as experimental)  
**Evaluated Gloss:** *NAMASTE* / *GREETINGS* (ISLRTC Dictionary Vol 1, Word #0001)  

---

## Executive Summary & Formal Decision Record

SignBridge Milestone M3.19 executes the formal evaluation and decision gate for the experimental motion-capture candidate `isl_namaste_mocap_candidate_v1`.

### Formal Governance Decision:
```
================================================================================
FORMAL MILESTONE DECISION: NO PRODUCTION PROMOTION
STATUS: HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND

1. The experimental candidate 'isl_namaste_mocap_candidate_v1' CANNOT be promoted
   to production and must remain strictly classified as:
   validationStatus: "experimental_awaiting_validation".
2. The active production baseline remains 'isl_namaste_godl_v1' (unchanged).
3. Production speech translation in the Chrome extension routes spoken "namaste"
   strictly to 'isl_namaste_godl_v1'.
4. In accordance with SignBridge anti-fabrication ethics, zero synthetic or
   simulated human reviews have been authored.
================================================================================
```

---

## 1. Legitimate Public Institutional Outreach Directory (Task 1)

In compliance with Task 1, prospective evaluator outreach targets are drawn exclusively from publicly available, recognized Indian Sign Language institutions, deaf organizations, and university research programs. **No private individuals have been contacted, and no outreach communications have been dispatched without explicit project owner authorization.**

| Organization / Institution | Institutional Focus | Public Website / Domain | Public Outreach Role |
| :--- | :--- | :--- | :--- |
| **Indian Sign Language Research and Training Centre (ISLRTC)** | Autonomous body under DEPwD, Ministry of Social Justice & Empowerment, Govt. of India; lexicographic authority for ISL. | [`islrtc.nic.in`](https://islrtc.nic.in) | Sponsoring authority of reference dictionary; source of certified interpreters and linguistic researchers. |
| **National Association of the Deaf (NAD) India** | National deaf-led advocacy organization representing the Indian Deaf community. | [`nadindia.org`](https://nadindia.org) | Deaf native signers and community governance feedback. |
| **All India Federation of the Deaf (AIFD)** | National apex federation of deaf associations in India, founded 1955. | [`aifd.org.in`](http://www.aifd.org.in) | Deaf community leaders and educators. |
| **Deaf Enabled Foundation (DEF)** | Non-governmental organization conducting ISL training and interpreter development across India. | [`def.org.in`](https://def.org.in) | Certified ISL interpreters and community trainers. |
| **IGNOU School of Humanities (DISLI Program)** | National open university delivering the Diploma in Indian Sign Language Interpretation (DISLI). | [`ignou.ac.in`](https://www.ignou.ac.in) | Certified academic interpreter educators. |

*Disclaimer:* The above entities are listed solely as prospective institutional consultation avenues. No endorsement, partnership, or prior contact is claimed or implied.

---

## 2. Personalized Outreach Invitation Drafts (Task 2)

Based on [`Docs/ISL_REVIEWER_INVITATION.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEWER_INVITATION.md), the following personalized, transparent invitation drafts have been prepared for the project owner's review. **None of these invitations have been sent.**

### Draft A: For Certified Interpreters (DISLI / ISLRTC)
```
Subject: Invitation to evaluate an experimental 3D ISL animation candidate (Namaste)

Dear [Evaluator Name],

We are developing SignBridge, an open-source, local-first accessibility tool designed to assist deaf signers by rendering speech as 3D Indian Sign Language animations.

We have generated an experimental 3D reconstruction of the sign NAMASTE from the official ISLRTC video using computer vision. However, automated tracking does not equal linguistic accuracy. We need qualified ISL interpreters to evaluate whether the avatar's movement is linguistically acceptable, requires tuning, or should be rejected.

Key details:
- Time required: ~15 to 25 minutes.
- Tools: A side-by-side inspection studio running 100% locally in Google Chrome (no cloud calls, no webcam required).
- Voluntary & Independent: You are fully empowered to identify flaws, indicate uncertainty, or declare movement unassessable.
- Avatar Limitation: The 3D avatar (Mixamo Y-Bot) has a rigid metallic face lacking facial blendshapes; facial expressions are unrenderable.

If you are open to reviewing this candidate, please let us know, and we will share the review package (Docs/ISL_REVIEWER_INVITATION.md). Thank you for your leadership.
```

### Draft B: For Deaf Native Signers & Deaf Community Leaders
```
Subject: Request for Deaf-native review of experimental SignBridge animation (Namaste)

Dear [Evaluator Name],

We are reaching out to ask if you would be willing to review an experimental 3D avatar sign for NAMASTE developed by the open-source SignBridge project.

We believe that only Deaf native signers have the authority to decide if a sign is natural, grammatically correct, and respectful. Our computer-vision tool produced this candidate motion, but it has NOT been validated by any human signer.

Participation is completely voluntary:
- You may review with your name, a pseudonym, or anonymously.
- You can tell us if the sign looks good, looks unnatural, or is broken.
- Negative feedback and rejection of the animation are just as valuable as approval.
- The review runs entirely on your local computer; no personal data or video is uploaded to the internet.

Please see Docs/ISL_REVIEWER_INVITATION.md for details. We would be honored to receive your guidance if you have time to participate.
```

### Draft C: For Academic Sign Language Linguists
```
Subject: ISL Phonological Review: Experimental motion-capture candidate (Gloss: NAMASTE)

Dear [Evaluator Name],

SignBridge is preparing its first motion-capture candidate (Word #0001, NAMASTE) for formal linguistic evaluation. As an ISL linguistic researcher, we would value your evaluation of the candidate across the five standard phonological parameters (DEZ, TAB, ORI, SIG, and NMM).

The evaluation studio (tools/isl_motion_extraction/preview_mocap.html) provides synchronized video comparison, timeline scrubbing at 0.25x/0.5x speed, and scrutiny jump points for monocular tracking anomaly intervals (Frames 22, 59, 62).

Participation is voluntary and independent. The full protocol and schema are documented in Docs/ISL_REVIEWER_INVITATION.md and Docs/ISL_REVIEWER_HANDOFF.md. Please let us know if you would be interested in conducting an evaluation session.
```

---

## 3. Reviewer Packet & Cryptographic Hashes (Task 3)

The complete reviewer packet is assembled, verified, and ready for deployment:

| Asset | File Path | Expected SHA-256 Checksum |
| :--- | :--- | :--- |
| **Animation Candidate** | `tools/isl_motion_extraction/output/isl_namaste_mocap_candidate_v1.json` | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` |
| **Extension Asset Copy** | `extension/assets/animations/isl_namaste_mocap_candidate_v1.json` | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` |
| **Reference Video** | `tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4` | `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8` |
| **Review Studio UI** | `tools/isl_motion_extraction/preview_mocap.html` | Client-side HTML/JS side-by-side inspection studio |
| **Handoff Document** | `Docs/ISL_REVIEWER_HANDOFF.md` | Complete reviewer packet instructions |
| **Session Guide** | `Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md` | Step-by-step evaluator protocol |
| **Feedback Form** | `Docs/ISL_REVIEW_FEEDBACK_TEMPLATE.md` | Fillable review template conforming to schema v1.0.0 |

---

## 4. Evidence Intake & Directory Validation (Task 4 & 5)

In accordance with Tasks 4 and 5, the review storage directory was scanned using the read-only validator:

```powershell
python tools/isl_motion_extraction/validate_review_record.py
```

### Observed Validator Output:
```
================================================================================
SignBridge M3.14 — ISL Review Record Validation Report
================================================================================

[STATUS] HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND
Scanned directory: C:\AmazonMlChallenge\tools\isl_motion_extraction\reviews

Notice:
  - Zero review records were detected in the review storage directory.
  - In accordance with SignBridge evidence integrity standards, no synthetic
    or simulated review records have been fabricated.
  - The experimental candidate remains unvalidated pending real human review.
================================================================================
```

### Evidence Ingestion Integrity Checks:
- **Zero Dummy Records:** The live review folder `tools/isl_motion_extraction/reviews/` contains only `README.md`.
- **Protected Metadata Immutability:** In `preview_mocap.html`, imported JSON records cannot override protected provenance or identity fields (`candidateId`, `candidateFileSha256`, `referenceVideoSha256`, `reviewSchemaVersion`, `validationStatus`).
- **Read-Only Ingestion:** The validator executes in memory without modifying on-disk records.

---

## 5. Physical Articulatory Observations vs. Interpretations (Task 6)

Because no external reviewer records have been submitted, direct human linguistic findings cannot be recorded. However, physical computer-vision tracking facts are rigorously separated from subjective interpretation:

| Phonological Dimension | Objective Tracking & Kinematic Reality (Facts) | Potential Linguistic Limitation (Interpretation Awaiting Human Review) |
| :--- | :--- | :--- |
| **1. Handshape (DEZ)** | Retargeter maps MediaPipe hand landmarks to 16 finger joints per hand using forward kinematics. Fingers are extended and adducted together. | Reviewers must evaluate whether thumb adduction beside the index finger feels natural or stiff on the Y-Bot mesh. |
| **2. Location (TAB)** | Bilateral contact constraint clamps wrists to $79.8\text{ mm}$ mean separation at mid-chest height ($y \approx 1.05\text{ m}$ relative to avatar root). | Reviewers must determine whether hands are held at standard sternum height or positioned too high/low for natural discourse. |
| **3. Orientation (ORI)** | Wrists are oriented with palms facing medially (towards each other) and fingertips directed superiorly toward chin. | Reviewers must evaluate whether wrist flexion angle ($35^\circ$ forward incline) matches native signing norms. |
| **4. Movement (SIG)** | Clip lasts 3080 ms: 880 ms lap lift, 1480 ms static prayer hold, 720 ms lap descent. 1-Euro temporal filter smooths jitter. | Reviewers must judge whether the 1.48-second hold duration is natural or feels unnaturally static/robotic. |
| **5. Non-Manuals (NMM)** | Avatar performs a forward head tilt (+0.18 rad) during the hold interval. Mixamo Y-Bot mesh has **zero facial blendshapes, eye bones, or jaw bones**. | **Definitive Technical Limitation:** Facial expressions and mouth patterns cannot be displayed. Evaluators must score NMMs as `Not Assessable (Rig Limitation)`. |

---

## 6. Disagreements, Evidence Requests & Limitations (Task 7 & 8)

### 6.1 Disagreements & Uncertainty Handling
- When reviews are received, dissenting evaluations will be recorded individually rather than averaged away.
- A candidate cannot be certified by a simple numerical average score; consensus requires unanimous agreement that the sign contains no misleading or offensive articulatory errors.

### 6.2 Missing Evidence & Declared Requests
- In single-camera frontal video (`ISLRTC_Namaste_sample.mp4`), bilateral hand contact creates visual overlap, causing MediaPipe simultaneous tracking to drop to ~49.4%.
- Evaluators are expected to utilize the **Uncertainty Declaration** toggle in `preview_mocap.html` to request side-profile camera angles or multi-camera recordings if monocular depth ambiguity prevents confident assessment.

### 6.3 Rig Limitations
- The Mixamo Y-Bot rig is physically incapable of expressive facial animation. Linguistic validation of grammatical non-manual markers will require a future rig featuring Apple ARKit or FACS-compatible blendshapes.

---

## 7. Source-Video Licensing Tracking (Task 9)

In accordance with Task 9, the reference video licensing status remains documented as **UNRESOLVED** regarding raw redistribution:
1. **data.gov.in GODL Terms:** Government Open Data License - India grants royalty-free rights to adapt and extract derivative data (such as 3D skeletal keypoint coordinates) with mandatory attribution.
2. **islrtc.nic.in Portal Notice:** The official portal copyright policy reserves all reproduction rights without written permission.
3. **Hugging Face Mirror (`silentone0725`):** The re-encoded sample originates from a third-party mirror whose "MIT" claim is legally invalid.
4. **Enforced Boundary:** Because raw MP4 redistribution rights are unresolved, the reference video is restricted to local offline evaluation (`tools/isl_motion_extraction/reference_videos/`) and is **strictly excluded** from the Chrome extension release package.

---

## 8. Comprehensive Suite-by-Suite Test Execution

All 9 test suites were executed independently in their respective runtime environments and verified:

| # | Test Suite | Scope & Runtime | Command | Exit Code | Result |
|---|:---|:---|:---|:---:|:---|
| **1** | **Review Validator Unit Suite** | Schema validation, hash tampering detection, missing metadata, template vs. completed classification, and read-only behavior. | `python tools/isl_motion_extraction/tests/test_review_validator.py` | `0` | **9 / 9 PASSED** (0.142s) |
| **2** | **Review Round-Trip Test Suite** | Serialization, rich Unicode (Hindi/English), multiline notes, uncertainty, unknown field preservation, and neutral markdown export. | `python tools/isl_motion_extraction/tests/test_review_roundtrip.py` | `0` | **10 / 10 PASSED** (0.223s) |
| **3** | **Browser Usability CDP Suite** | Headless Chrome interactive testing of `preview_mocap.html` over CDP (DOM init, scrubbing, jumps, rubric, uncertainty, local storage, markdown). | `python tools/isl_motion_extraction/tests/test_browser_usability.py` | `0` | **15 / 15 PASSED** |
| **4** | **Review Readiness Unit Suite** | Candidate clip metadata, bone count (67), canonical joints, duration (3080ms), coordinate spaces, and Y-Bot compatibility. | `python tools/isl_motion_extraction/tests/test_review_readiness.py` | `0` | **12 / 12 PASSED** (0.147s) |
| **5** | **Retargeting Pipeline Unit Suite** | Landmark extraction, quaternion math, kinematic contact solvers, temporal smoothing, and candidate export. | `python tools/isl_motion_extraction/tests/test_retargeting.py` | `0` | **13 / 13 PASSED** (0.129s) |
| **6** | **Pre-Flight Diagnostic Tool** | Standalone pre-flight checklist verifying file sizes, SHA-256 hashes, Y-Bot rig presence, and production isolation. | `python tools/isl_motion_extraction/check_review_readiness.py` | `0` | **27 / 27 CHECKS PASSED** |
| **7** | **Review Ingestion Tool** | Read-only scanner of `tools/isl_motion_extraction/reviews/`. | `python tools/isl_motion_extraction/validate_review_record.py` | `0` | **0 records detected**<br>`STATUS: HUMAN REVIEW PENDING` |
| **8** | **Backend Speech Recognition Suite** | FastAPI / faster-whisper server health, speech transcription, sequential audio slicing, and loopback privacy boundary. | `.venv\Scripts\python.exe test_backend.py` *(in `signbridge-backend/`)* | `0` | **8 / 8 PASSED** |
| **9** | **Chrome In-Engine Regression Suite** | Extension Manifest V3, WebGL rendering, translation pipeline, keyframes, and retargeting contracts in real Chrome DOM. | `python run_chrome_tests.py` | `0` | **132 / 132 PASSED**<br>(M1: 9, M2: 10, M3: 113) |

---

## 9. Next Steps for M3.20

1. **Project Owner Dispatch:** The project owner may select prospective reviewers from the legitimate institutional directory and dispatch the personalized invitations ([`Docs/ISL_REVIEWER_INVITATION.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEWER_INVITATION.md)).
2. **Intake & Verification:** When genuine completed reviews are received, place the exported JSON records into `tools/isl_motion_extraction/reviews/` and execute `validate_review_record.py`.
3. **Evidence-Based Motion Tuning:** If reviewers request kinematic adjustments, utilize [`Docs/ISL_CORRECTION_WORKFLOW.md`](file:///c:/AmazonMlChallenge/Docs/ISL_CORRECTION_WORKFLOW.md) to generate a versioned `v2` candidate for follow-up review.
