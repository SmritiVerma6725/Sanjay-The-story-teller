# Indian Sign Language (ISL) Review Feedback Template

**Document Reference:** `Docs/ISL_REVIEW_FEEDBACK_TEMPLATE.md`  
**Review Record Schema:** `signbridge_review_schema_v1.0.0`  
**Target Gloss:** `NAMASTE` / `GREETINGS`  
**Candidate Identifier:** `isl_namaste_mocap_candidate_v1` (Version: `v1.0.0`)  
**Candidate Asset SHA-256:** `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46`  
**Reference Video Asset:** `ISLRTC_Namaste_sample.mp4` (SHA-256: `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8`)  
**Reference Source:** ISLRTC Dictionary Vol 1, Word #0001 (data.gov.in / Government Open Data License - India)  
**Target Rig:** Adobe Mixamo Y-Bot (`ybot.glb`, Three.js WebGL)  
**Governance Classification:** **EXPERIMENTAL MOTION RECONSTRUCTION — PENDING QUALIFIED REVIEW**

---

> [!IMPORTANT]
> **GOVERNANCE & EVALUATION NOTICE:**  
> This template establishes a structured, auditable feedback loop for qualified Deaf-native signers, certified ISL interpreters, and sign linguistics experts to record detailed articulatory critiques. **Filling out or submitting this feedback template does not certify the animation as valid ISL.** An animation remains strictly classified as `experimental_awaiting_validation` until a formal consensus panel approves it.

---

## 1. Review Context & Evaluator Information

*Evaluator identification is voluntary. Evaluators may provide their full professional credentials or an anonymous identifier/pseudonym.*

| Field | Reviewer Input |
|---|---|
| **Evaluator Name or Pseudonym:** | _____________________________________________ |
| **Voluntary Evaluator Role:** | [ ] Deaf Native ISL Signer<br>[ ] Certified Interpreter (DISLI/ISLRTC)<br>[ ] Deaf Educator / Teacher of the Deaf<br>[ ] Sign Language Linguist / Researcher<br>[ ] Deaf Community Member<br>[ ] Other Qualified Expert |
| **Review Session Date & Time:** | ________________________ (ISO Timestamp: _____________________) |
| **Review Tool / Environment:** | SignBridge Review Studio (`preview_mocap.html`) on Google Chrome |
| **Evaluated Candidate SHA-256:** | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` |
| **Reference Video SHA-256:** | `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8` |

---

## 2. Open-Ended Impressions & Spontaneous Qualitative Observations

*Please record your unprompted, spontaneous observations, kinematic impressions, stiffness, posture, cultural nuances, or initial thoughts in your own words before scoring discrete categories below:*

```
[Write initial observations, naturalness of entry/hold/exit, posture, bilateral symmetry, or areas where motion feels robotic or unclear]
```

---

## 3. Five Phonological Dimensions Evaluation

Please rate each of the five core linguistic parameters of ISL using one of the four standardized ratings:
- **Acceptable:** Movement accurately conforms to standard ISL articulation.
- **Minor Issue:** Noticeable inaccuracy or stiffness that does not destroy intelligibility.
- **Unacceptable:** Incorrect or ungrammatical movement that distorts meaning or looks unnatural.
- **Not Assessable:** Cannot be evaluated due to documented rig or capture constraints (e.g. avatar facial expression).

### Dimension 1: Handshape (DEZ - Designator)
*Target: Symmetrical flat open palms (B-handshape / 5-handshape variation); four fingers extended and adducted together; thumbs resting parallel to palm.*

- **Rating:** [ ] Acceptable &nbsp;&nbsp; [ ] Minor Issue &nbsp;&nbsp; [ ] Unacceptable &nbsp;&nbsp; [ ] Not Assessable
- **Specific Observations & Corrections:**  
  ____________________________________________________________________________________  
  ____________________________________________________________________________________

---

### Dimension 2: Location / Place of Articulation (TAB - Tabula)
*Target: Centered at sternum / mid-chest height; comfortable clearance from torso (10–15 cm); balanced midsagittal placement.*

- **Rating:** [ ] Acceptable &nbsp;&nbsp; [ ] Minor Issue &nbsp;&nbsp; [ ] Unacceptable &nbsp;&nbsp; [ ] Not Assessable
- **Specific Observations & Corrections:**  
  ____________________________________________________________________________________  
  ____________________________________________________________________________________

---

### Dimension 3: Orientation (ORI)
*Target: Palms facing medially towards each other; fingertips pointing superiorly (upward toward chin); symmetrical wrist flexion.*

- **Rating:** [ ] Acceptable &nbsp;&nbsp; [ ] Minor Issue &nbsp;&nbsp; [ ] Unacceptable &nbsp;&nbsp; [ ] Not Assessable
- **Specific Observations & Corrections:**  
  ____________________________________________________________________________________  
  ____________________________________________________________________________________

---

### Dimension 4: Movement (SIG - Signation)
*Target: Symmetrical upward preparatory rise; stable 1.3-second prayer hold at sternum; smooth deceleration and retraction back to lap rest.*

- **Rating:** [ ] Acceptable &nbsp;&nbsp; [ ] Minor Issue &nbsp;&nbsp; [ ] Unacceptable &nbsp;&nbsp; [ ] Not Assessable
- **Specific Observations & Corrections:**  
  ____________________________________________________________________________________  
  ____________________________________________________________________________________

---

### Dimension 5: Non-Manual Markers (NMM)
*Target: Respectful forward head tilt (+0.18 rad) during contact hold.*  
*Rig Limitation Note: Adobe Mixamo Y-Bot has a rigid metallic face lacking facial blendshapes or eye bones. Mouth morphemes, eyebrow movements, and eye gaze cannot be rendered.*

- **Head Tilt Rating:** [ ] Acceptable &nbsp;&nbsp; [ ] Minor Issue &nbsp;&nbsp; [ ] Unacceptable &nbsp;&nbsp; [ ] Not Assessable
- **Facial Morphemes / Mouth Shape:** [X] **Not Assessable on Y-Bot Rig** *(Rig Limitation Acknowledged)*
- **Specific Observations & Corrections:**  
  ____________________________________________________________________________________  
  ____________________________________________________________________________________

---

## 4. Scrutiny of Flagged Tracking Anomaly Frames

The automated extraction pipeline identified three specific intervals where monocular tracking confidence dipped or camera occlusion occurred. Please inspect these intervals in `preview_mocap.html`:

| Scrutiny Interval | Tracking Condition Grounding | Finding | Reviewer Remarks |
|---|---|---|---|
| **Frame 22 ($880\text{ ms}$)**<br>Lift Stroke | Right hand landmark confidence dipped below threshold during initial separation from lap. Solver temporally interpolated motion. | [ ] Acceptable Lift<br>[ ] Distorted / Jitter<br>[ ] Not Assessed | |
| **Frame 40 ($1600\text{ ms}$)**<br>Palm Contact Hold | Monocular hand self-occlusion. Bilateral solver clamped wrist separation to $79.8\text{ mm}$ ($35\text{ mm}$ max correction). | [ ] Natural Contact<br>[ ] Gap Unnatural<br>[ ] Mesh Clipping | |
| **Frame 59 ($2360\text{ ms}$)**<br>Hand Separation | Left hand was momentarily occluded by right hand as hands began separating after hold. | [ ] Smooth Release<br>[ ] Snapping / Discontinuous<br>[ ] Not Assessed | |
| **Frame 62 ($2480\text{ ms}$)**<br>Lap Return | Hands returned to lap rest region where MediaPipe ceases hand observation. | [ ] Clean Descent<br>[ ] Asymmetric Descent<br>[ ] Stiff / Robotic | |

---

## 5. Uncertainty Declaration & Evidence Requests

If monocular perspective, video resolution, or rig limitations make any aspect inconclusive, record requirements below:

- [ ] **Uncertainty Declared / Further Evidence Requested**
- **Specific Evidence Required:**  
  *(e.g., Multi-angle video, side profile view, higher frame-rate capture, or avatar rig with facial blendshapes)*  
  ____________________________________________________________________________________  
  ____________________________________________________________________________________

---

## 6. Actionable Kinematic Feedback & Free-Text Recommendations

*Please provide actionable guidance for kinematic tuning (e.g. adjust elbow flaring angle, increase/decrease wrist contact distance, soften retraction stroke):*

```
[Write qualitative observations, cultural considerations, or kinematic adjustment requests here]
```

---

## 7. Overall Evaluator Recommendation

Please select one official determination:

- [ ] **PROVISIONAL APPROVAL FOR FURTHER REVIEW:**  
  The motion is immediately intelligible, natural, and respectful. Candidate is ready for broader multi-signer panel review. **(Note: This is NOT approval for production deployment).**
  
- [ ] **REQUIRES REVISIONS / TUNING:**  
  The motion is fundamentally recognizable and promising, but requires specific parameter adjustments (e.g., retargeting solver tweaks) before panel review. Produces a versioned `v2` candidate.

- [ ] **REJECTED (Unacceptable ISL Representation):**  
  The candidate motion misrepresents the sign, contains severe visual artifacts, or violates ISL phonological rules. Must not be used in SignBridge.

- [ ] **NOT ASSESSABLE / INCONCLUSIVE (Default):**  
  Review session was inconclusive, rig limitations prevented complete assessment, or reviewer requested additional evidence before reaching a verdict.

---

## 6. Documented Disagreements & Unresolved Questions

*If multiple evaluators or panel members disagree on specific articulatory details, record the divergent perspectives below rather than averaging them away:*

| Disputed Feature | Perspective A | Perspective B | Unresolved Status |
|---|---|---|---|
| *(e.g. Forearm tilt angle)* | *(e.g. Slightly higher elevation preferred)* | *(e.g. Lower chest height standard in regional dialect)* | Requires broader regional survey |

---

## 7. Audit & Verification Sign-Off

- **Evaluation Record Hash:** `[Computed from JSON Record]`
- **Evaluator Signature / Identifier:** _____________________________________________
- **Review Schema Version:** `signbridge_review_schema_v1.0.0`
- **Submission Date:** ________________________
