# SignBridge M4 Stage 4 — Blockers & Owner Decisions Register

**Document Reference:** `Docs/M4_STAGE_4_BLOCKERS_AND_OWNER_DECISIONS.md`  
**Milestone:** SignBridge Milestone M4 — End-to-End Product Integration, ISL Validation Readiness, UX, Performance, and Controlled Pilot Preparation  
**Stage:** **Stage 4: Blockers Register & Owner Decisions Package**  
**Execution Date:** October 20, 2026  
**Auditor / Decision Author:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  

---

## 1. Executive Purpose

Milestone M4 Stage 4 preparation is complete. All autonomous engineering, benchmarking, and simulation tasks have finished with 322 passing checks. To advance the project responsibly to Stage 5 closure and prepare for real-world pilot testing, explicit human-in-the-loop decisions are required from the SignBridge Project Owner.

This document compiles the **4 formal owner decisions** and their associated evidence, risks, and recommended actions.

---

## 2. Outstanding Owner Decision Items

### Decision Item 1: Revision of Peak Memory Budget (CTranslate2 Initialization)
* **Context:** The original PRD proposed a `< 250 MB` memory ceiling for the local Python backend.
* **Empirical Measurements (Stage 3):**
  - Steady-State Working Set: **`185.54 MB`** (Passing $< 250\text{ MB}$).
  - Transient Peak Working Set: **`256.44 MB`** (Exceeded by 6.44 MB / 2.5% during cold start weight deserialization).
* **Technical Rationale:** The transient spike occurs once when CTranslate2 memory-maps model weights and allocates MKL/OpenVINO threading structures. Memory returns to 185 MB within 500ms and remains flat during continuous streaming.
* **Options for Owner:**
  - **Option A (Recommended):** Formally approve a dual memory threshold: **`< 300 MB` Peak Working Set** during startup, and **`< 250 MB` Steady-State Working Set** during operation.
  - **Option B:** Reject revision and mandate engineering investigation into smaller quantization formats (e.g. `int8_float16`) or lazy weight loading.
* **Owner Decision:** `[ PENDING_OWNER_APPROVAL ]`

---

### Decision Item 2: Reference Video Licensing Strategy (`LEGAL-01`)
* **Context:** The video asset `ISLRTC_Namaste_sample.mp4` originates from a YouTube upload of ISLRTC dictionary footage. Its licensing status remains `UNRESOLVED` in `Docs/ASSET_LICENSES.md`.
* **Legal Finding:** While ISLRTC dictionary metadata is published under Government Open Data License - India (GODL) on `data.gov.in`, third-party YouTube uploads carry uncertain distribution rights.
* **Options for Owner:**
  - **Option A (Recommended):** Restrict pilot test clips strictly to official Government of India open data sources (`data.gov.in` GODL distributions) and prohibit bundling or external redistribution of the YouTube reference video.
  - **Option B:** Direct legal counsel to send a formal inquiry to ISLRTC / DEPwD requesting explicit confirmation of educational derivative rights for the YouTube video series.
* **Owner Decision:** `[ PENDING_OWNER_APPROVAL ]`

---

### Decision Item 3: Controlled Pilot Ethics & Institutional Clearance Path (`OPS-03`)
* **Context:** Controlled pilot evaluation involves human participants from the Deaf and Hard-of-Hearing community.
* **Ethical Safeguards Prepared:** A complete multimodal informed consent draft (`PARTICIPANT_CONSENT_DRAFT.md`) with plain English text, certified ISL interpreter requirement, and voluntary withdrawal protocol has been authored.
* **Options for Owner:**
  - **Option A (Formal Institutional Clearance):** Submit the Stage 4 protocol and consent draft to an Institutional Review Board (IRB) or University Ethics Committee for formal review.
  - **Option B (Exemption Determination):** Authorize pilot execution under an institutional usability testing exemption, provided no personal health information (PHI) is collected and consent is fully documented.
* **Owner Decision:** `[ PENDING_OWNER_APPROVAL ]`

---

### Decision Item 4: Authorization to Initiate Participant Outreach (`OPS-06`)
* **Context:** All reviewer and participant outreach mechanisms are currently locked under **`DRY_RUN_ONLY — NOT_AUTHORIZED`**. Zero emails, forms, or invitations have been transmitted.
* **Readiness Finding:** Technical readiness is 100% complete (322 passing checks; 17 dry-run scenarios passed).
* **Options for Owner:**
  - **Option A (Authorize Stage 4 Dry-Run Closure Only):** Approve Stage 4 closure as `PREPARATION_COMPLETE — PILOT_BLOCKED_BY_EXTERNAL_DEPENDENCIES` without authorizing active participant recruitment.
  - **Option B (Authorize Pilot Recruitment):** Formally lift the outreach lockout, authorizing facilitators to contact pre-identified pilot participants using the approved Stage 4 package.
* **Owner Decision:** `[ PENDING_OWNER_APPROVAL ]`

---

## 3. Summary of Decision Registry

| ID | Domain | Decision Topic | Status | Recommended Action |
|:---:|:---|:---|:---:|:---|
| **DEC-01** | Technical | Revise peak memory ceiling to 300 MB | `PENDING_OWNER_APPROVAL` | Approve Option A (Dual threshold: 300MB peak / 250MB steady) |
| **DEC-02** | Legal | Resolve source reference video licensing strategy | `PENDING_OWNER_APPROVAL` | Approve Option A (Confine pilot strictly to data.gov.in GODL) |
| **DEC-03** | Ethical | Determine IRB / Ethics clearance pathway | `PENDING_OWNER_APPROVAL` | Submit consent materials for formal institutional review |
| **DEC-04** | Operational | Authorize participant recruitment & pilot start | `PENDING_OWNER_APPROVAL` | Maintain lockout until Decisions 1–3 are finalized |
