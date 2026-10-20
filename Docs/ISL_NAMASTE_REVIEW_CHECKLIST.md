# Indian Sign Language (ISL) Linguistic Review Checklist: NAMASTE Candidate Motion

**Document Reference:** `Docs/ISL_NAMASTE_REVIEW_CHECKLIST.md`  
**Evaluation Target:** Candidate Animation Clip `isl_namaste_mocap_candidate_v1`  
**Source Provenance:** ISLRTC Dictionary Vol 1, Word #0001 (`ISLRTC_Namaste_sample.mp4`)  
**Avatar Rig:** Adobe Mixamo Y-Bot (`ybot.glb`, Three.js)  
**Evaluation Tool:** SignBridge MoCap Preview Studio (`tools/isl_motion_extraction/preview_mocap.html`)  
**Status:** **EXPERIMENTAL RECONSTRUCTION — PENDING FORMAL ISL EXPERT REVIEW**

---

> [!IMPORTANT]
> **DISCLAIMER FOR REVIEWERS AND ENGINEERS:**  
> This checklist is designed for evaluation by a **qualified Deaf-native ISL signer, certified ISL interpreter, or sign linguistics expert**. Computational motion capture, mathematical joint solvers, and legal Open Data licenses (GODL) do **not** constitute linguistic validation. Under no circumstances should this animation be certified as standard ISL without sign-off on this protocol.

---

## 1. Reviewer Information & Session Context

| Field | Detail |
|---|---|
| **Reviewer Name:** | _____________________________________________ |
| **ISL Background:** | [ ] Deaf Native Signer &nbsp;&nbsp; [ ] Certified Interpreter (DISLI/ISLRTC) &nbsp;&nbsp; [ ] Deaf Educator / Linguist |
| **Years of Signing Experience:** | _____ years |
| **Date of Review:** | ________________________ |
| **Review Environment:** | Browser: Chrome &nbsp;&nbsp; Monitor / Display: ________________ |
| **Playback Tool:** | `tools/isl_motion_extraction/preview_mocap.html` |

---

## 2. Review Protocol & Setup

1. **Open the Evaluation Tool:**
   - Launch a local HTTP server: `python -m http.server 8000` from the repository root.
   - Open `http://localhost:8000/tools/isl_motion_extraction/preview_mocap.html` in Google Chrome.
2. **Review Reference Video First:**
   - Play the left-hand video (`ISLRTC_Namaste_sample.mp4`) at full speed ($1.0\times$) and half speed ($0.5\times$).
   - Note the native signer's preparatory lift, peak prayer hold (*Anjali Mudra*), subtle head bow, and descent.
3. **Review Candidate Avatar Motion:**
   - Play the right-hand 3D Y-Bot viewport synchronized with the reference video.
   - Use the interactive timeline scrubber (Frames 0 to 76, $0\text{ ms} - 3080\text{ ms}$) to inspect critical intervals.
4. **Complete the Parameter Rubrics Below:**
   - Score each of the five phonological parameters of ISL (Handshape, Location, Orientation, Movement, Non-Manuals).

---

## 3. Five-Parameter Linguistic Evaluation Rubric

### Parameter 1: Handshape (DEZ - Designator)
*In standard ISL Namaste, both hands form an open flat palm (5-handshape / B-handshape variation with fingers together and thumb alongside the palm).*

| Checkpoint | Expected Linguistic Feature | Avatar Motion Observed | Pass / Fail / Revise | Comments & Deficiencies |
|---|---|---|---|---|
| **1.1 Extension** | All fingers (index, middle, ring, pinky) fully extended during hold. | Fingers kinematically flattened at peak hold. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **1.2 Adduction** | Fingers held close together (adducted) rather than splayed. | Finger joints parallel to palm normal. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **1.3 Thumb Position** | Thumbs resting adjacent to index fingers, not tucked into palm. | Thumb extended parallel to palm plane. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **1.4 Bilateral Symmetry** | Dominant and non-dominant handshapes are identical. | Mirrored kinematic finger rotations. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |

---

### Parameter 2: Location / Place of Articulation (TAB - Tabula)
*The prayer sign must be articulated in neutral space directly in front of the mid-to-upper chest (sternum height).*

| Checkpoint | Expected Linguistic Feature | Avatar Motion Observed | Pass / Fail / Revise | Comments & Deficiencies |
|---|---|---|---|---|
| **2.1 Height** | Palms meet at mid-chest / sternum level (below chin, above diaphragm). | Hand midpoint centered at $Y \approx 1.25\text{ m}$ relative to Y-Bot origin. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **2.2 Distance from Body** | Hands held approximately 10–15 cm anterior to the chest (not pressed flush against sternum). | Hand positions maintain clearance from avatar chest mesh. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **2.3 Lateral Centering** | Contact occurs on the midsagittal plane (centered horizontally with nose and spine). | Constrained contact centered at $X \approx 0.0\text{ m}$. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |

---

### Parameter 3: Orientation (ORI)
*Palms must face each other medially, with fingertips directed upward.*

| Checkpoint | Expected Linguistic Feature | Avatar Motion Observed | Pass / Fail / Revise | Comments & Deficiencies |
|---|---|---|---|---|
| **3.1 Palm Orientation** | Palms face directly towards each other (palmar surface medial). | Right palm normals facing left ($+X$), Left palm normals facing right ($-X$). | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **3.2 Finger Direction** | Fingertips point superiorly (upward toward chin, tilted slightly forward $\approx 10^\circ$). | Forearms flexed $\approx 110^\circ$ bringing wrists up; fingers point $+Y$. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **3.3 Contact Surface** | Palmar surfaces of fingers and carpal pads touch without interpenetration. | Contact solver enforces 70 mm wrist distance, avoiding mesh clipping. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |

---

### Parameter 4: Movement (SIG - Signation)
*The dynamic trajectory comprises three phases: preparatory stroke, peak hold, and retraction stroke.*

| Phase & Interval | Expected Dynamic Motion | Avatar Motion Observed | Pass / Fail / Revise | Comments & Deficiencies |
|---|---|---|---|---|
| **4.1 Preparatory Stroke**<br>(Frames 0–24, $0–960\text{ ms}$) | Symmetrical upward and inward arc from resting position on lap to chest. Smooth acceleration without snapping. | Hands lift smoothly from rest ($Y \approx 0.85\text{ m}$) towards center; 1-Euro filter eliminates initial jitter. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **4.2 Peak Contact Hold**<br>(Frames 25–58, $1000–2320\text{ ms}$) | Hands meet gently and remain stationary in prayer hold for $\approx 1.3\text{ seconds}$ without drift or trembling. | Bilateral contact solver stabilizes separation at $79.8\text{ mm}$; trajectory jitter reduced by $58\%$. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |
| **4.3 Retraction Stroke**<br>(Frames 59–76, $2360–3040\text{ ms}$) | Hands part smoothly and return symmetrically downward to rest. | Symmetrical descent back to neutral sitting posture. | [ ] Pass &nbsp; [ ] Fail &nbsp; [ ] Revise | |

---

### Parameter 5: Non-Manual Markers (NMM) & Facial Expression
*In Indian culture and ISL, Namaste is accompanied by a respectful downward head tilt / slight bow and pleasant facial posture.*

| Checkpoint | Expected Feature | Avatar Motion Observed | Status / Limitation | Notes |
|---|---|---|---|---|
| **5.1 Head Tilt / Bow** | Forward nod $\approx 10^\circ - 15^\circ$ during peak contact hold. | Head pitch bone rotates $+0.18\text{ rad}$ forward during Frames 28–55. | [ ] Acceptable &nbsp; [ ] Unnatural &nbsp; [ ] Missing | |
| **5.2 Eye Gaze** | Eyes lower slightly in sync with the head nod. | Y-Bot has static head mesh without eye bones. | **Known Rig Limitation** | Eyeball orientation cannot be articulated on Y-Bot. |
| **5.3 Mouth / Facial Morpheme** | Relaxed, polite facial posture (slight gentle smile or neutral closure). | Y-Bot metallic face lacks blendshapes / FACS shapes. | **Known Rig Limitation** | Avatar upgrade to ARKit 52 mesh required for facial expressions. |

---

## 4. Detailed Frame-by-Frame Inspection Table (Key Intervals)

Please scrub the timeline to each of the designated frame indices and evaluate visual quality:

| Frame Index | Timestamp | Phase Description | Solver Classification | Specific Inspection Objective | Reviewer Finding |
|---|---|---|---|---|---|
| **Frame 0** | $0\text{ ms}$ | Neutral start | `REST_INTERPOLATED` | Are arms resting naturally at sides/lap without clipping into torso? | [ ] Good &nbsp; [ ] Needs adjustment |
| **Frame 22** | $880\text{ ms}$ | Lift transition | `LOW_CONFIDENCE` | **Flagged Frame:** Right hand landmark had low visibility. Does the lift motion look continuous or does it jitter/pop? | [ ] Natural &nbsp; [ ] Noticeable jerk &nbsp; [ ] Unacceptable |
| **Frame 25** | $1000\text{ ms}$ | Contact onset | `CONTACT_CONSTRAINED` | Do the hands meet cleanly? Is there visual interpenetration (palms merging into each other) or an artificial gap? | [ ] Clean contact &nbsp; [ ] Gap too large &nbsp; [ ] Clipping |
| **Frame 40** | $1600\text{ ms}$ | Peak hold | `CONTACT_CONSTRAINED` | Is the hold stable and motionless? Are the elbows resting comfortably without flaring unnaturally? | [ ] Stable &nbsp; [ ] Unnatural elbow angle &nbsp; [ ] Shaking |
| **Frame 58** | $2320\text{ ms}$ | Release onset | `CONTACT_CONSTRAINED` | Do hands hold shape right up until parting? | [ ] Holds shape &nbsp; [ ] Collapses early |
| **Frame 59** | $2360\text{ ms}$ | Parting separation | `LOW_CONFIDENCE` | **Flagged Frame:** Left hand was momentarily occluded during parting. Is the release smooth or abrupt? | [ ] Smooth &nbsp; [ ] Snapping &nbsp; [ ] Desynchronized |
| **Frame 62** | $2480\text{ ms}$ | Descent transition | `LOW_CONFIDENCE` | **Flagged Frame:** Boundary frame returning to lap. Are both arms descending at equal speeds? | [ ] Symmetrical &nbsp; [ ] Asymmetrical |
| **Frame 76** | $3040\text{ ms}$ | Terminal rest | `REST_INTERPOLATED` | Does the avatar return to a neutral rest state suitable for chaining into next sign? | [ ] Clean rest &nbsp; [ ] Awkward pose |

---

## 5. Overall Linguistic Assessment & Scoring

Rate the animation candidate on the following 5-point scales ($1 = \text{Unacceptable / Unrecognizable}$, $5 = \text{Flawless / Fully Native}$):

| Linguistic Dimension | Score (1 to 5) | Criteria |
|---|---|---|
| **Intelligibility** | [ ] 1 &nbsp; [ ] 2 &nbsp; [ ] 3 &nbsp; [ ] 4 &nbsp; [ ] 5 | Would a Deaf ISL signer immediately recognize this sign as *Namaste* without any caption or context? |
| **Morphological Accuracy** | [ ] 1 &nbsp; [ ] 2 &nbsp; [ ] 3 &nbsp; [ ] 4 &nbsp; [ ] 5 | Are the handshape, orientation, and contact point technically accurate according to ISL grammar? |
| **Kinematic Naturalness** | [ ] 1 &nbsp; [ ] 2 &nbsp; [ ] 3 &nbsp; [ ] 4 &nbsp; [ ] 5 | Does the movement feel like human signing rather than robotic or jerky machine interpolation? |
| **Timing & Rhythm** | [ ] 1 &nbsp; [ ] 2 &nbsp; [ ] 3 &nbsp; [ ] 4 &nbsp; [ ] 5 | Are the acceleration, peak hold duration ($1.3\text{s}$), and relaxation timing natural and respectful? |

---

## 6. Reviewer Recommendation & Verdict

Choose one of the following official determinations:

- [ ] **APPROVED AS IS (Production Ready):**  
  The motion capture reconstruction is accurate, natural, and immediately intelligible. Meets all criteria for inclusion in the SignBridge production lexicon.
  
- [ ] **PROVISIONAL APPROVAL (Acceptable with Minor Parameter Revisions):**  
  The sign is intelligible and fundamentally sound, but requires minor parameter tuning (e.g., adjust elbow flaring, slightly increase palm contact offset, or soften return stroke).

- [ ] **REVISE AND RE-SUBMIT (Major Correction Required):**  
  The sign has significant unnaturalness, inaccurate contact, or broken timing that would confuse or alienate native Deaf signers. Must be re-processed through the kinematics pipeline.

- [ ] **REJECTED (Unacceptable for ISL Representation):**  
  The candidate motion misrepresents the sign, suffers from severe visual artifacts, or lacks necessary grammatical components. Hand-authored or studio-grade multi-camera mocap should be pursued instead.

---

## 7. Reviewer Notes & Actionable Feedback

*Please record specific timestamps, bone adjustments, or qualitative observations below:*

```
[Write qualitative notes, cultural considerations, or specific kinematic feedback here]
```

---

## 8. Formal Sign-Off

**Reviewer Signature / Digital Identifier:** _____________________________________________  
**Organization / Affiliation:** _____________________________________________  
**Date:** ________________________  
**Verification Hash of Evaluated Clip:** `isl_namaste_mocap_candidate_v1` (77 frames, duration 3080 ms)
