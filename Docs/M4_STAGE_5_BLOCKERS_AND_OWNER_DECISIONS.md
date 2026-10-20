# SignBridge M4 Stage 5 — Blockers Register & Owner Decisions Package

**Document Reference:** `Docs/M4_STAGE_5_BLOCKERS_AND_OWNER_DECISIONS.md`  
**Milestone:** SignBridge Milestone M4 — End-to-End Product Integration, ISL Validation Readiness, UX, Performance, and Controlled Pilot Preparation  
**Stage:** **Stage 5: Complete Validation, Release Readiness & Evidence Closure**  
**Execution Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  

---

## 1. Executive Purpose

Milestone M4 Stage 5 has completed all local engineering, test automation, performance benchmarking, privacy auditing, and release preparation. The unified test suite passes **340 / 340 checks**. 

However, SignBridge is an accessibility application intended for the Deaf and Hard-of-Hearing community. Engineering verification alone cannot establish linguistic sign accuracy, legal redistribution rights, or ethical participant consent.

This document identifies the **4 remaining blockers** that prevent live pilot testing or public release, specifies the exact evidence required to remove each blocker, and presents the formal decisions awaiting the SignBridge Project Owner.

---

## 2. Master Blockers Register

| Blocker ID | Domain | Blocker Title | Severity | Impact on Project | Evidence Required to Remove Blocker | Current State |
|:---:|:---|:---|:---:|:---|:---|:---:|
| **`LEGAL-01`** | Legal & Provenance | Unresolved Reference Video Derivative Rights | **HIGH** | Blocks bundling or redistribution of `ISLRTC_Namaste_sample.mp4` | Formal legal opinion or written permission from ISLRTC / DEPwD confirming educational redistribution rights for YouTube footage | `UNRESOLVED` |
| **`DEAF-01`** | Linguistic Accuracy | Baseline Clip Unvalidated; Zero Linguistic Certifications | **CRITICAL** | Blocks claims of ISL accuracy; blocks promotion of mocap candidate | Minimum of 3 independent evaluations from qualified Deaf-native ISL signers with $\ge 80\%$ score per `Docs/M4_STAGE_2_PROMOTION_GATES.md` | `0 / 3 REVIEWS` |
| **`PERF-01`** | Resource Budget | Peak Memory Working Set Exceeds 250 MB Target | **MEDIUM** | Technically blocks strict adherence to legacy PRD memory target | Written authorization from Project Owner approving dual-threshold memory policy (300 MB peak / 250 MB steady-state) | `PENDING_APPROVAL` |
| **`OPS-06`** | Ethics & Outreach | Participant Outreach Lockout Maintained | **HIGH** | Blocks recruitment of real Deaf participants for pilot testing | Formal Project Owner written directive authorizing participant outreach and approving consent protocol | `NOT_AUTHORIZED` |

---

## 3. Detailed Blocker Analysis & Remediation Pathways

### Blocker 1: Reference Video Derivative Rights (`LEGAL-01`)
- **Root Cause:** The sample video `ISLRTC_Namaste_sample.mp4` is derived from a third-party YouTube upload (`silentone0725`). While official ISLRTC dictionary metadata is published under Government Open Data License - India (GODL) on `data.gov.in`, third-party YouTube distribution creates legal ambiguity regarding derivative re-distribution.
- **Evidence Required to Clear:**
  - Written confirmation from ISLRTC / Department of Empowerment of Persons with Disabilities (DEPwD), Government of India, confirming educational research and fair-use rights; OR
  - Direct pipeline adaptation using official raw video datasets hosted directly on `data.gov.in`.
- **Interim Safeguard:** Video is quarantined strictly within `tools/isl_motion_extraction/reference_videos/` and is completely excluded from the browser extension package.

### Blocker 2: Linguistic Sign Accuracy & Review Gap (`DEAF-01`)
- **Root Cause:** The active baseline `isl_namaste_godl_v1` is an authored geometric approximation; the experimental candidate `isl_namaste_mocap_candidate_v1` has zero human reviews. No qualified Deaf-native signer or certified interpreter has yet reviewed the 3D animations.
- **Evidence Required to Clear:**
  - Conducting an in-person or remote review session using `tools/isl_motion_extraction/preview_mocap.html`.
  - Ingestion of 3 genuine, cryptographically signed review records into `tools/isl_motion_extraction/reviews/` scoring $\ge 80\%$ across handshape, location, orientation, movement, and non-manual markers.
- **Interim Safeguard:** Baseline is strictly labeled `IMPLEMENTED_UNVALIDATED`. Out-of-lexicon words hold neutral pose with 0 fake gestures. Candidate remains quarantined.

### Blocker 3: Peak Memory Budget Revision (`PERF-01`)
- **Root Cause:** CTranslate2 model initialization causes a brief memory spike to `256.44 MB`, exceeding the legacy PRD target of `< 250 MB` by 6.44 MB (2.5%). Steady-state operational memory is well within budget at `185.54 MB`.
- **Evidence Required to Clear:**
  - Project Owner formal sign-off approving a 300 MB peak ceiling; OR
  - Engineering effort to implement smaller quantization formats or lazy model loading.
- **Interim Safeguard:** Peak memory is tracked and reported honestly as exceeding the 250 MB budget, without silently altering criteria.

### Blocker 4: Outreach Lockout & Consent Clearance (`OPS-06`)
- **Root Cause:** All outreach is currently locked under `DRY_RUN_ONLY — NOT_AUTHORIZED`. Zero emails or recruitment forms have been transmitted.
- **Evidence Required to Clear:**
  - Formal institutional review (IRB) or documented usability testing exemption.
  - Project Owner signature on the pilot authorization directive.
- **Interim Safeguard:** Pilot package materials in `Docs/M4_STAGE_4_PILOT_PACKAGE/` are maintained strictly as drafts.

---

## 4. Formal Project Owner Decisions Required

The Project Owner must record formal determinations on the following 4 decision gates:

| Decision Gate | Decision Topic | Recommended Option | Alternative Option | Status |
|:---:|:---|:---|:---|:---:|
| **DEC-01** | Peak Memory Budget | **Option A:** Approve dual threshold: 300 MB peak / 250 MB steady-state | **Option B:** Require engineering to compress weights under 250 MB peak | `[ PENDING_OWNER_APPROVAL ]` |
| **DEC-02** | Reference Video Strategy | **Option A:** Confine pilot strictly to data.gov.in GODL raw media | **Option B:** Submit formal legal inquiry to ISLRTC/DEPwD | `[ PENDING_OWNER_APPROVAL ]` |
| **DEC-03** | Pilot Ethics Pathway | **Option A:** Submit consent draft to formal institutional ethics board (IRB) | **Option B:** Authorize under documented usability testing exemption | `[ PENDING_OWNER_APPROVAL ]` |
| **DEC-04** | Pilot Recruitment | **Option A:** Maintain lockout; close M4 as technically ready | **Option B:** Lift lockout; authorize recruitment of 3–5 pilot participants | `[ PENDING_OWNER_APPROVAL ]` |
