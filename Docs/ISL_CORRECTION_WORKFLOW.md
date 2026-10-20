# SignBridge ISL Motion Correction & Versioning Workflow

**Document Reference:** `Docs/ISL_CORRECTION_WORKFLOW.md`  
**Milestone:** M3.11 — Review Workflow Verification & Feedback Loop  
**Target Domain:** Indian Sign Language (ISL) Avatar Motion Reconstruction  
**Status:** **ACTIVE GOVERNANCE SPECIFICATION**

---

## 1. Overview & Core Principles

This document specifies the formal, auditable procedure for receiving linguistic feedback from qualified Deaf-native evaluators, translating that feedback into kinematic parameter adjustments, and producing a new, traceable candidate motion version without compromising the established production baseline.

### Non-Negotiable Governance Principles:
1. **Preserve the Baseline:** The canonical production animation baseline (`isl_namaste_godl_v1`) and original reference video (`ISLRTC_Namaste_sample.mp4`) are permanent and immutable. No candidate version or review record may overwrite or replace them without formal approval.
2. **Preserve Review Records Intact:** Every evaluator's feedback is archived as an independent, hash-verified record. If evaluators disagree on a sign parameter (e.g. regional variation or stylistic height), both evaluations are preserved; disagreement is never averaged away or discarded.
3. **Separate Tracking Failure from Linguistic Correction:** Technical tracking anomalies (such as monocular hand self-occlusion) must be distinguished from linguistic corrections (such as native preference for elbow angle or hold duration).
4. **Zero Guessing Policy:** Engineers and algorithms must never guess or fabricate handshapes, finger flexions, or facial expressions to satisfy an evaluation. If human feedback is unavailable or ambiguous, the parameter remains explicitly flagged as *Unresolved*.
5. **Strict Candidate Versioning & Lineage:** Every kinematic correction generates a distinct, versioned candidate asset (e.g. `v1` $\rightarrow$ `v2`) with documented parentage, rationale, parameter diffs, and cryptographic hash verification.
6. **Continuous Automated Verification:** Every new candidate version must pass declarative schema validation, Two-Bone Vector IK constraints, 1-Euro smoothing sanity tests, and in-engine WebGL regression tests before presentation to reviewers.

---

## 2. End-to-End Correction Lifecycle

```
[Evaluator Review Session in Review Studio (preview_mocap.html)]
                          │
                          ▼
[Structured Feedback Record Exported (Docs/reviews/review_<hash>.json)]
                          │
                          ▼
[Triage: Distinguish Tracking Loss vs. Articulatory Critique]
                          │
                          ▼
[Kinematic Parameter Tuning in retargeter.py / contact_constraints.py]
                          │
                          ▼
[Export Versioned Candidate (e.g. isl_namaste_mocap_candidate_v2.json)]
                          │
                          ▼
[Run Full Test Regressions (Retargeting, In-Engine Chrome, Backend)]
                          │
                          ▼
[Update Candidate Provenance, Change Log, & SHA-256 Manifest]
                          │
                          ▼
[Re-Submit for Evaluator Review in preview_mocap.html]
```

---

## 3. Step-by-Step Correction Procedure

### Phase A: Ingest & Triage Review Feedback
1. **Archive the Signed Review Record:**  
   Store the exported review JSON from `preview_mocap.html` into `Docs/reviews/` with the filename format:
   ```
   Docs/reviews/review_<candidateId>_<reviewerPseudonym>_<YYYYMMDD>.json
   ```
2. **Audit the Cryptographic Checksum:**  
   Verify that the `candidateFileSha256` recorded in the review matches the actual evaluated candidate asset.
3. **Categorize Feedback Items:**
   - **Type A: Kinematic / Articulatory Adjustment:** (e.g. *"Forearms are held too high; lower wrist height by 3 cm"* or *"Palms should tilt forward by 5 degrees"*).
   - **Type B: Timing / Rhythm Adjustment:** (e.g. *"Prayer hold is too brief; extend peak contact duration by 200 ms"*).
   - **Type C: Monocular Tracking Anomaly:** (e.g. *"Frame 22 shows arm jitter during lift"* $\rightarrow$ adjust 1-Euro filter cutoff frequency $\beta$).
   - **Type D: Rig-Constrained Feature:** (e.g. *"Add mouth morpheme"* $\rightarrow$ documented as unrenderable on current Y-Bot metallic mesh; logged for future avatar upgrade).

---

### Phase B: Implement Kinematic Adjustments
1. **Locate the Parameter in Offline Solvers:**
   - Wrist separation / contact proximity: `tools/isl_motion_extraction/contact_constraints.py` (`ContactConstraintSolver`)
   - Maximum correction clamp: `ContactConstraintSolver.max_correction_m` (default: $0.035\text{ m}$)
   - Forearm flexion and upper arm rotation: `tools/isl_motion_extraction/retargeter.py` (`RetargetingEngine._solve_upper_body`)
   - Head bow angle and duration: `RetargetingEngine._solve_head`
   - Temporal smoothing responsiveness: `tools/isl_motion_extraction/smoothing.py` (`OneEuroFilterVec3`, `OneEuroFilterQuat`)
2. **Apply Minimal Targeted Modifications:**  
   Adjust only the parameters flagged by evaluator consensus. Do not modify unaffected joints.

---

### Phase C: Generate & Verify New Versioned Candidate
1. **Update Output Identifier & Version:**  
   When generating the next iteration, increment the candidate identifier:
   - Parent: `isl_namaste_mocap_candidate_v1` (Version `v1.0.0`)
   - Child: `isl_namaste_mocap_candidate_v2` (Version `v2.0.0`)
2. **Execute the Offline Export Pipeline:**
   ```powershell
   tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/export_animation.py --version v2 --parent isl_namaste_mocap_candidate_v1
   ```
3. **Compute and Record New Asset SHA-256:**
   ```powershell
   python -c "import hashlib; print(hashlib.sha256(open('tools/isl_motion_extraction/output/isl_namaste_mocap_candidate_v2.json', 'rb').read()).hexdigest())"
   ```
4. **Mirror Asset to Extension:**  
   Copy the validated candidate to `extension/assets/animations/isl_namaste_mocap_candidate_v2.json`.

---

### Phase D: Execute Regression & Verification Suites
Before presenting the new candidate to reviewers, run all four local regression suites:

```powershell
# 1. Review readiness and safety guard tests
tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/tests/test_review_readiness.py

# 2. Retargeting and kinematics unit tests
tools\isl_motion_extraction\.venv\Scripts\python.exe tools/isl_motion_extraction/tests/test_retargeting.py

# 3. Chrome in-engine avatar and contract tests (all suites)
python run_chrome_tests.py

# 4. Backend speech service privacy and transcription tests
cd signbridge-backend; .venv\Scripts\python.exe test_backend.py; cd ..
```

---

### Phase E: Record Candidate Lineage & Provenance
Maintain a structured candidate lineage entry in `Docs/M3_11_REVIEW_WORKFLOW_REPORT.md`:

| Candidate ID | Version | Parent ID | Evaluator Review Basis | Changes Implemented | New SHA-256 |
|---|---|---|---|---|---|
| `isl_namaste_mocap_candidate_v1` | `v1.0.0` | None (Direct MoCap) | Initial M3.9 Baseline | Two-Bone Vector IK, 1-Euro Filter, 35mm contact clamp | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` |
| `isl_namaste_mocap_candidate_v2` | `v2.0.0` | `v1.0.0` | *(Pending Reviewer Feedback)* | *(Document exact parameter adjustments)* | *(Computed upon export)* |

---

## 4. Production Lexicon Promotion Criteria

A candidate motion cannot be considered for promotion to the production lexicon (`KeyframeRegistry` and `ISLTranslator`) until all of the following criteria are met:

1. **Panel Consensus:** Formal evaluation by a panel of at least three independent, qualified Deaf-native signers / certified interpreters.
2. **Unanimous Approval or Clear Majority:** No unaddressed `Unacceptable` ratings on Handshape, Location, Orientation, or Movement.
3. **Zero Rig Breakage:** Zero reported clipping, hyper-extension, or unnatural bone pop artifacts.
4. **Governance Review:** Formal documentation sign-off archiving all panel review records in `Docs/reviews/`.
5. **Reversible Migration:** The previous production baseline (`isl_namaste_godl_v1`) is preserved in the asset registry as a permanent fallback.
