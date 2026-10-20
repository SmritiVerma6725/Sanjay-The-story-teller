# Indian Sign Language (ISL) Expert Review Session Guide: NAMASTE Candidate Motion

**Document Reference:** `Docs/ISL_NAMASTE_REVIEW_SESSION_GUIDE.md`  
**Milestone:** M3.10 — ISL Review Readiness & Safe Candidate Integration  
**Target Sign:** *NAMASTE* / *GREETINGS* (ISLRTC Dictionary Vol 1, Word #0001)  
**Evaluated Motion Asset:** `isl_namaste_mocap_candidate_v1.json` (77 frames, 3080 ms, 25 FPS)  
**Evaluation Studio:** `tools/isl_motion_extraction/preview_mocap.html`  
**Avatar Rig:** Adobe Mixamo Y-Bot (`ybot.glb`, Three.js WebGL)  
**Governance Classification:** **EXPERIMENTAL MOTION RECONSTRUCTION — PENDING QUALIFIED REVIEW**

---

## 1. Purpose & Guiding Principles

This guide outlines the standard operating procedure for conducting a formal, respectful, and rigorous linguistic evaluation session of the SignBridge *Namaste* motion-capture candidate with a **qualified Deaf-native ISL signer, certified ISL interpreter (DISLI/ISLRTC), or sign linguistics researcher**.

### Core Evaluation Principles:
1. **Deaf-Led Authority:** Machine learning outputs, mathematical kinematics, and Government Open Data licenses (GODL) do **not** constitute linguistic validation. Only fluent ISL signers possess the authority to certify whether a rendered sign is natural, grammatically accurate, and respectful.
2. **Transparent Limitations:** Reviewers must be fully briefed on avatar rig limitations (e.g. rigid metallic face lacking facial expressions) prior to evaluation so assessment focuses on valid articulatory features.
3. **No Fabricated Evidence:** Flagged low-confidence frames (Frames 22, 59, 62) must be explicitly presented to the reviewer for scrutiny rather than smoothed over or concealed.
4. **Zero Cloud / Data Privacy:** All evaluation tools execute 100% locally on localhost; no video, webcam, or reviewer responses are transmitted to any external server.

---

## 2. Reviewer Eligibility & Profile

An evaluative reviewer should meet at least one of the following criteria:
- **Deaf Native Signer:** Deaf individual who uses Indian Sign Language as their primary daily language.
- **Certified ISL Interpreter:** Interpreter holding formal certification (e.g., DISLI from ISLRTC or recognized state institute) with active interpreting practice.
- **Deaf Educator / Linguist:** Teacher of the Deaf or linguistic researcher specializing in Indian Sign Language grammar and phonology.

---

## 3. Pre-Session Setup & Environment

### Hardware & Display:
- **Display:** Minimum 1080p display (1920×1080) to view the reference video and 3D avatar side-by-side without horizontal scrolling.
- **Browser:** Google Chrome (recommended for WebGL performance and hardware acceleration).

### Launching the Review Studio Locally:
1. Open a terminal at the project root `C:\AmazonMlChallenge`.
2. Start a local HTTP server:
   ```powershell
   python -m http.server 8000
   ```
3. Open Google Chrome and navigate to:
   ```
   http://localhost:8000/tools/isl_motion_extraction/preview_mocap.html
   ```
4. Verify that:
   - The reference video appears in the left viewport.
   - The Y-Bot 3D avatar renders in the right viewport with arms relaxed at sides (Neutral Rest Pose).
   - The timeline scrubber (0 to 3080 ms) is functional.

---

## 4. Reviewer Briefing Protocol (Spoken / Signed Script)

Before starting playback, provide the following explanation to the reviewer in ISL or accessible written English:

> *"Welcome. We are developing SignBridge, a local accessibility tool for converting speech to Indian Sign Language avatars. Today, we are evaluating an experimental 3D reconstruction of the sign **Namaste**, extracted from the official ISLRTC dictionary video.*
>
> *Please note two critical technical boundaries before reviewing:*
> 1. *The avatar (Y-Bot) has articulated arms, wrists, and fingers, but has a smooth metallic face with **no facial expressions or mouth shapes**. A forward head nod is animated, but facial expressions cannot be rendered on this avatar. Please evaluate the head nod, but mark mouth/facial expressions as 'Not Assessable on Current Rig'.*
> 2. *Because the source was a single front-facing camera, the computer had difficulty tracking the hands at the exact moments when they touched or separated. We have specifically marked three uncertain frames (Frames 22, 59, and 62) so you can tell us whether the movement looks natural or broken.*
>
> *Your honest feedback will decide whether this candidate can be approved, needs tuning, or must be rejected. Thank you for your leadership."*

---

## 5. Concise Review Session Checklist

Follow this 7-step checklist during every evaluation session. **Do not lead the evaluator toward a positive verdict.** The evaluator must be completely free to reject the animation or disagree with previous assessments.

- [ ] **1. Explaining the experimental status and limitations:** Brief evaluator on candidate's unvalidated status, lack of facial blendshapes on Y-Bot, and monocular occlusion constraints.
- [ ] **2. Showing the reference video and avatar at normal speed (1.0x):** Play full synchronized sequence ($0\text{ ms} - 3080\text{ ms}$) without interruption.
- [ ] **3. Repeating the comparison at 0.5x and 0.25x speed:** Inspect slow-motion hand trajectory, finger alignment, and contact timing using the speed dropdown.
- [ ] **4. Recording spontaneous qualitative observations:** Gather evaluator's initial impressions in their own words before prompting with discrete categories.
- [ ] **5. Inspecting the five linguistic dimensions separately:** Evaluate Handshape, Location, Orientation, Movement, and Non-Manuals individually.
- [ ] **6. Reviewing key transition intervals and tracking anomalies:** Scrutinize Frame 22 (lift stroke), Frame 40 (palm contact), Frame 59 (hand separation), and Frame 62 (lap return).
- [ ] **7. Recording uncertainty or requests for additional evidence:** Record any missing angles, video artifacts, or rig limitations preventing assessment.
- [ ] **8. Exporting and preserving the review record:** Download the signed review JSON (`ISL_Namaste_Review_*.json`) and store in `tools/isl_motion_extraction/reviews/`.

---

## 6. Step-by-Step Evaluation Workflow

```
[Step 1: Watch Reference Video (Uninterrupted)]
       │
[Step 2: Watch 3D Avatar (Uninterrupted)]
       │
[Step 3: Synchronized Playback at 1.0x, 0.5x & 0.25x]
       │
[Step 4: Record Open-Ended Qualitative Notes (First Impression)]
       │
[Step 5: Score the 5 Phonological Parameters]
       │
[Step 6: Scrutinize Key Transition Intervals (Frames 22, 59, 62)]
       │
[Step 7: Record Uncertainty / Request Further Evidence]
       │
[Step 8: Select Overall Recommendation Verdict]
       │
[Step 9: Export Review Record (JSON & Markdown)]
```

### Step 1: Watch Reference Video
- In the left viewport, observe the native signer's motion in [`ISLRTC_Namaste_sample.mp4`](file:///C:/AmazonMlChallenge/tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4).
- Pay attention to the start of the arm lift from the lap, the height where palms meet, the duration of the prayer hold (*Anjali Mudra*), the forward head nod, and the return to lap.

### Step 2: Watch 3D Avatar
- Click **"► Play Synchronized"** or press **Spacebar**.
- Observe the avatar's execution at normal speed ($1.0\times$) from $t = 0\text{ ms}$ to $t = 3080\text{ ms}$.
- Note overall naturalness, rhythm, and whether the sign is immediately recognizable as *Namaste*.

### Step 3: Synchronized Comparison & Slow-Motion Inspection
- Select **"0.5x (Half-Speed)"** or **"0.25x (Slow-Motion)"** from the Speed dropdown.
- Scrub the timeline to inspect the simultaneous alignment of the signer and the avatar.
- Check whether the avatar's hands meet at the same moment as the reference signer ($t \approx 1000\text{ ms}$).

### Step 4: Record Open-Ended Qualitative Notes (Initial Impression)
- Before prompting the evaluator with discrete rating categories, ask for their unprompted, open-ended impression.
- In the **Step 1 — Open-Ended Observations** textarea, record their spontaneous comments regarding overall naturalness, posture, stiffness, cultural nuance, or areas of uncertainty in their own words.

### Step 5: Score the Five Linguistic Parameters
In the integrated **Step 2 — Structured Parameter Assessment** table:
- **1. Handshape (DEZ):** Select `Acceptable`, `Minor Issue`, `Unacceptable`, or `Not Assessable`. (Are fingers straight and pressed together? Is thumb beside index finger?)
- **2. Location (TAB):** Select finding. (Is contact point at sternum height, centered horizontally, and properly spaced from chest?)
- **3. Orientation (ORI):** Select finding. (Are palms facing medial toward each other? Are fingertips pointing upward toward chin?)
- **4. Movement (SIG):** Select finding. (Is upward trajectory smooth? Is the hold duration stationary without trembling? Is descent natural?)
- **5. Non-Manuals (NMM):** Select `Head Tilt Acceptable`, `Timing Off`, `Unacceptable`, or `Not Assessable (Rig Limitation)`. (Note: Mixamo Y-Bot has a rigid metallic face lacking blendshapes; facial morphemes must be marked `Not Assessable`).

### Step 6: Scrutinize Key Transition Intervals (Tracking Anomalies)
Use the dedicated scrutiny jump buttons in the review studio to inspect tracking anomaly intervals:

1. **Frame 22 ($880\text{ ms}$ — Lift Stroke):**
   - Click **"Frame 22 (880ms: Lift Stroke)"**.
   - *Context:* Right hand tracking dropped below detection threshold during initial separation from lap; motion is temporally interpolated.
   - *Review Question:* Does the avatar's upward lift appear acceptable and natural, or is there an unnatural jerk, lag, or twitch?
   - Check the checkbox if upward motion appears acceptable; leave unchecked if distorted or unassessed.

2. **Frame 40 ($1600\text{ ms}$ — Palm Contact Hold):**
   - Click **"Frame 40 (1600ms: Palm Contact)"**.
   - *Context:* Bilateral contact constraint enforces wrist separation with a maximum correction clamp.
   - *Review Question:* Are palms positioned comfortably at sternum height without flaring elbows or interpenetration?

3. **Frame 59 ($2360\text{ ms}$ — Hand Separation):**
   - Click **"Frame 59 (2360ms: Hand Separation)"**.
   - *Context:* Hand tracking is occluded as hands begin parting.
   - *Review Question:* Do hands separate smoothly without visual popping or discontinuity?
   - Check the checkbox if release motion appears smooth; leave unchecked if distorted or unassessed.

4. **Frame 62 ($2480\text{ ms}$ — Lap Return):**
   - Click **"Frame 62 (2480ms: Lap Return)"**.
   - *Context:* Hands re-enter the lap rest region where MediaPipe ceases hand detection.
   - *Review Question:* Does the descent to lap rest appear clean and symmetrical?
   - Check the checkbox if descent appears clean; leave unchecked if distorted or unassessed.

### Step 7: Declare Uncertainty / Request Further Evidence
- If monocular camera angle, video quality, or avatar rig limitations make any aspect inconclusive:
  - Check **"Step 4 — Declare Uncertainty / Request Further Evidence"**.
  - Detail specific evidence required (e.g., side-profile camera angle, multi-signer reference video, slower capture, or facial blendshape rig).

### Step 8: Select Overall Recommendation Verdict
Select one of the four equally accessible verdict options:
- **Provisional Approval for Further Review:** Eligible for broader panel review. **Important:** This does NOT constitute production approval.
- **Requires Revisions / Tuning:** Linguistic or kinematic corrections needed before further evaluation.
- **Rejected:** Unacceptable or misleading ISL representation (must be discarded or re-extracted).
- **Not Assessable / Inconclusive:** Rig limitations, monocular occlusion, or insufficient evidence prevent a definitive verdict (Default state).

### Step 9: Export Signed Review Record
- Click **"💾 Save Progress Locally"** to store results in browser `localStorage`.
- Click **"⬇ Export Review JSON"** to download the structured review record (`ISL_Namaste_Review_*.json`).
- Optionally click **"⬇ Export Review Markdown"** or **"📋 Copy Summary to Clipboard"** for human-readable meeting records.
- Place exported JSON files into `tools/isl_motion_extraction/reviews/` for offline schema validation.

---

## 7. Post-Review Action Protocol

Depending on the reviewer's verdict:
- **If Approved Provisionally for Further Review:** The candidate clip is queued for multi-signer panel evaluation. It remains strictly excluded from live production routing (`validationStatus: "experimental_awaiting_validation"`).
- **If Tuning Required:** Retargeting parameters in `tools/isl_motion_extraction/retargeter.py` and `contact_constraints.py` are adjusted to address specific notes, generating a versioned candidate (`v2`).
- **If Rejected:** The motion capture pipeline is flagged as insufficient for this sign, and alternative capture methods (e.g. multi-camera capture or expert manual authoring) are pursued.
- **If Inconclusive / Not Assessable:** The declared evidence requests are logged and reviewed before re-evaluating.

---

## 8. Keyboard Shortcuts Quick Reference

| Shortcut Key | Action |
|---|---|
| **Spacebar** | Toggle Synchronized Play / Pause |
| **Arrow Left (←)** | Step backward 1 frame ($-40\text{ ms}$) |
| **Arrow Right (→)** | Step forward 1 frame ($+40\text{ ms}$) |
| **Key R** | Restart playback from beginning ($0\text{ ms}$) |
