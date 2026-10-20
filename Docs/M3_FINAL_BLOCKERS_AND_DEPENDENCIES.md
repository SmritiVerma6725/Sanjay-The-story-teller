# SignBridge M3 — Final Blockers & External Dependencies

**Document Reference:** `Docs/M3_FINAL_BLOCKERS_AND_DEPENDENCIES.md`  
**Milestone:** SignBridge Milestone M3 — Complete End-to-End Closure  
**Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  

---

## 1. Executive Overview

All engineering, architectural, testing, studio tooling, and governance controls within the SignBridge M3 workstream are **100% complete and verified**.

However, full real-world production deployment and live external outreach cannot occur without resolving specific **external dependencies** that lie strictly beyond autonomous agent authority. This document provides a transparent, exhaustive register of these external blockers, their root causes, and the concrete actions required to resolve them.

---

## 2. Summary Table of Outstanding External Dependencies

| Dependency ID | Category | Dependency Description | Impact on System | Action Required for Resolution |
|:---:|:---|:---|:---|:---|
| **DEP-01** | **Owner Governance** | Project Owner sign-off on Decision Gates 1 through 5 in `Docs/M3_26_OWNER_DECISION_CHECKLIST.md`. | Blocks live message dispatch; system remains in `DRY_RUN_ONLY`. | Project Owner reviews checklist, makes selections, and executes signature block. |
| **DEP-02** | **Legal / Licensing** | Reference video (`ISLRTC_Namaste_sample.mp4`) redistribution rights remain **`UNRESOLVED`**. | Prohibits email video attachment, cloud hosting, or public extension bundling. | Legal review / formal permission request to ISLRTC/DEPwD, or maintain local-only studio review. |
| **DEP-03** | **Human Validation** | Lack of qualified Deaf-native ISL signer evaluation and certified linguist review. | Candidate `isl_namaste_mocap_candidate_v1` cannot be promoted to production. | Conduct live review sessions with independent signers after owner authorizes outreach. |
| **DEP-04** | **Avatar Rig Limitation** | Adobe Mixamo Y-Bot mesh lacks facial bones and blendshapes; cannot express ISL non-manual markers (NMM). | Facial expressions cannot be evaluated or displayed. | Keep NMM marked `NOT ASSESSABLE` on current rig; plan facial blendshape avatar for future milestone. |
| **DEP-05** | **Institutional Routing** | TGT-005 (IGNOU SOH) `soh@ignou.ac.in` routes to Director's desk rather than DISLI coordinator. | Risk of misplaced inquiry or delayed routing. | Project Owner decides whether to exclude TGT-005 or include forwarding request in initial contact. |

---

## 3. Detailed Dependency Analyses & Action Pathways

### DEP-01: Project Owner Governance Sign-Off
- **Status:** `PENDING PROJECT OWNER ACTION`
- **Root Cause:**
  - Automated agents are strictly barred from initiating external institutional communications or assuming executive authority.
  - The governance architecture explicitly decouples technical package approval from live dispatch authorization.
- **Specific Decisions Required:**
  1. **Gate 1:** Granular approval/exclusion of individual recipient channels (TGT-001 ISLRTC, TGT-002 NAD India, TGT-003 AIFD, TGT-004 DEF, TGT-005 IGNOU).
  2. **Gate 2:** Individual approval of Draft 1 (Interpreters), Draft 2 (Deaf Native), and Draft 3 (Linguists).
  3. **Gate 3:** Selection of rollout strategy: **Option A (Staged Wave: TGT-001 & TGT-004 first) [Recommended]** vs Option B (Simultaneous).
  4. **Gate 4:** Formal acknowledgement of unresolved reference video licensing terms.
  5. **Gate 5:** Independent message dispatch authorization. Active system default remains **`REMAIN_IN_DRY_RUN`**.
- **Action Required:**
  - The human Project Owner must review [`Docs/M3_26_OWNER_DECISION_CHECKLIST.md`](file:///c:/AmazonMlChallenge/Docs/M3_26_OWNER_DECISION_CHECKLIST.md), mark the decision gates, and execute the signature block.

---

### DEP-02: Reference Video Redistribution Rights (Unresolved)
- **Status:** `LEGAL CLARIFICATION REQUIRED (ISOLATED IN LOCAL WORKFLOW)`
- **Root Cause:**
  - The ground-truth reference video `ISLRTC_Namaste_sample.mp4` (SHA-256 `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8`) was sourced from ISLRTC dictionary documentation.
  - While government lexical data is published on data.gov.in under the Government Open Data License - India (GODL), distribution terms for raw video recordings from ministerial portals have not been legally established.
  - Third-party mirror license tags (e.g. GitHub repo licenses) do not grant legal distribution rights for government-sourced media.
- **Mitigation Implemented:**
  - The raw video is strictly barred from email attachments, external cloud hosting, or public extension packaging.
  - The review studio operates 100% locally on `localhost`, comparing the local video file directly in Chrome WebGL without network transmission.
- **Action Required:**
  - If external video sharing is required in future milestones, obtain formal written permission from ISLRTC / DEPwD. Otherwise, continue with the local studio review model.

---

### DEP-03: Independent Human Linguistic Validation
- **Status:** `HUMAN EVALUATION PENDING (ZERO REVIEWS FABRICATED)`
- **Root Cause:**
  - Mathematical kinematics, MediaPipe landmark tracking confidence, and 3D joint rotation smoothness do **NOT** constitute linguistic sign language validity.
  - Only qualified Deaf-native ISL signers and certified sign language linguists possess the linguistic authority to declare an animation acceptable, natural, or in need of tuning.
  - No human review has yet taken place. The review directory `tools/isl_motion_extraction/reviews/` contains zero records.
- **Mitigation Implemented:**
  - Candidate clip `isl_namaste_mocap_candidate_v1` remains quarantined in experimental assets with `isLinguisticISL: false` and `status: "experimental_awaiting_validation"`.
  - Production speech recognition routes strictly to the baseline sign `isl_namaste_godl_v1`.
  - Automated preflight diagnostic [`check_review_readiness.py`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/check_review_readiness.py) enforces this separation.
- **Action Required:**
  - After Project Owner executes Gate 5, conduct voluntary, uncompensated evaluation sessions using [`preview_mocap.html`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/preview_mocap.html) and ingest genuine review records using [`validate_review_record.py`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/validate_review_record.py).

---

### DEP-04: Avatar Rig Physical Limitations (Rigid Facial Mesh)
- **Status:** `DOCUMENTED RIG CONSTRAINT (CURRENT AVATAR BOUNDARY)`
- **Root Cause:**
  - The Adobe Mixamo Y-Bot mesh (`ybot.glb`, 2,233,440 bytes) provides an articulated 67-joint humanoid skeleton with 4-phalange fingers, but has a rigid metallic head with zero facial bones or blendshapes.
  - Indian Sign Language incorporates non-manual markers (NMM), including facial expressions, mouthing, eyebrow raises, and head tilts.
  - The current avatar can perform head tilts and nods, but cannot articulate facial expressions.
- **Mitigation Implemented:**
  - All invitation drafts, review session guides, and the review studio interface prominently disclose this limitation.
  - Reviewers are instructed in the worksheet to mark facial expressions as `NOT ASSESSABLE ON CURRENT RIG`, preventing false negative ratings on features the mesh cannot display.
- **Action Required:**
  - Retain current Y-Bot for skeletal limb/hand evaluation in M3.
  - Introduce an avatar mesh with FACS-compliant facial blendshapes in a future milestone (M4+).

---

### DEP-05: Institutional Routing Review for TGT-005 (IGNOU SOH)
- **Status:** `PENDING OWNER ROUTING SELECTION`
- **Root Cause:**
  - The legacy departmental URL returned HTTP 404 following IGNOU's migration to the Samarth e-Gov portal.
  - SOH directory listings confirm `soh@ignou.ac.in` and `directorsoh@ignou.ac.in`, but this address routes to the Director of the School of Humanities rather than directly to the DISLI (Diploma in Indian Sign Language Interpretation) coordinator.
- **Mitigation Implemented:**
  - Target TGT-005 is classified as `NEEDS_OWNER_ROUTING_REVIEW`.
  - Draft 3 includes an explicit request: *"If you are not the appropriate contact for ISL linguistics, we would appreciate it if you could forward this inquiry to the relevant DISLI coordinator or sign-language faculty."*
- **Action Required:**
  - In `Docs/M3_26_OWNER_DECISION_CHECKLIST.md` (Gate 1), the Project Owner may either approve TGT-005 with the forwarding request or select `[ ] EXCLUDE` to focus outreach exclusively on statutory and community bodies (TGT-001 through TGT-004).

---

## 4. Path to Production Release

```
[ M3 Engineering Closure ] (COMPLETE — 246/246 checks passed)
           │
           ▼
[ Project Owner Review & Sign-Off ] (Docs/M3_26_OWNER_DECISION_CHECKLIST.md)
           │ (Owner executes Gates 1-4, then decides Gate 5)
           ▼
[ Controlled Institutional Outreach ] (Dry-Run deactivated ONLY for approved targets)
           │
           ▼
[ Review Session Execution ] (Independent signers inspect preview_mocap.html)
           │
           ▼
[ Review Ingestion & Linguistic Verdict ] (validate_review_record.py)
           │
           ├────────────────────────┬────────────────────────┐
           ▼                        ▼                        ▼
     [ ACCEPTED ]             [ NEEDS TUNING ]          [ REJECTED ]
(Promote to Production)  (Adjust Kinematic Model)  (Retain godl_v1 baseline)
```
