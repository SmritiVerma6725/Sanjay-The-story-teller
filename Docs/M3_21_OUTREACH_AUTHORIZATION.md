# SignBridge M3.21 — Outreach Authorization Gate & Policy Control

**Document Reference:** `Docs/M3_21_OUTREACH_AUTHORIZATION.md`  
**Milestone:** SignBridge M3.21 — Authorization-Gated Outreach & Reviewer Response Management  
**Creation Date:** October 2026  
**Current Gate Status:** **DRY_RUN_ONLY — PENDING EXPLICIT PROJECT-OWNER SIGNATURE**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Active in extension & unchanged)  
**Evaluated Candidate:** `isl_namaste_mocap_candidate_v1` (Quarantined)  

---

## 1. Purpose of the Authorization Gate

The SignBridge project enforces a strict authorization boundary between **review preparation** and **live external communication**:
- Automated tooling, scripts, or agents **must never** automatically transmit electronic mail, submit contact forms, share animation assets, or contact external institutions.
- All outreach targets, message texts, and recipient channels must be explicitly reviewed and signed off by the human project owner.
- Until an explicit, documented signature is recorded in this document, the system remains strictly locked in **`DRY_RUN_ONLY`** mode.

---

## 2. Authorized vs. Restricted Actions

| Action Category | Operational Action | Authorization Status | Enforced Constraint |
| :--- | :--- | :---: | :--- |
| **Preparation** | Researching public institutional directories | **AUTHORIZED** | Restrict to public institutional websites; no harvesting of private contacts. |
| **Preparation** | Drafting personalized invitation templates | **AUTHORIZED** | Must remain completely neutral; no presumption of avatar correctness. |
| **Preparation** | Generating local test suites & trackers | **AUTHORIZED** | Internal verification only. |
| **External Outreach** | Sending electronic mail to institutions | **RESTRICTED / NOT AUTHORIZED** | **Requires Project-Owner Signature (Section 6).** |
| **Asset Distribution** | Uploading or emailing candidate animation JSON | **RESTRICTED / NOT AUTHORIZED** | Prohibited until reviewer explicitly agrees and consents. |
| **Media Distribution** | Redistributing raw reference video (`ISLRTC_Namaste_sample.mp4`) | **STRICTLY PROHIBITED** | Reference video redistribution rights remain unresolved. Excluded from release. |
| **Production Promotion** | Promoting candidate to `KeyframeRegistry` | **STRICTLY PROHIBITED** | Prohibited until genuine consensus review records are validated. |

---

## 3. Approved Outreach Targets & Recipient Channels

The following public recipient channels have been identified from public institutional headers for project-owner review. **No communication may be directed to any channel not explicitly approved in this table.**

| Target ID | Institution Name | Category | Publicly Published Address | Approved for Dispatch? | Verification Audit Note |
|---|---|---|---|:---:|---|
| **TGT-001** | **ISLRTC (Indian Sign Language Research and Training Centre)** | Autonomous Govt Authority (DEPwD, MSJE) | `islrtcnewdelhi@gmail.com` | **PENDING APPROVAL** | Transcribed from official portal `islrtc.nic.in/contact-us` (October 2026). Active mailbox status unverified. |
| **TGT-002** | **National Association of the Deaf (NAD) India** | Deaf-Led National Advocacy Apex Body | `nadindia@gmail.com` | **PENDING APPROVAL** | Transcribed from official portal `nadindia.org/contact` (October 2026). Active mailbox status unverified. |
| **TGT-003** | **All India Federation of the Deaf (AIFD)** | National Deaf Federation (Est. 1955) | `aifd1955@yahoo.co.in` | **PENDING APPROVAL** | Transcribed from official portal `aifd.org.in` (October 2026). Active mailbox status unverified. |
| **TGT-004** | **Deaf Enabled Foundation (DEF)** | Community Sign Organization & Training | `info@def.org.in` | **PENDING APPROVAL** | Transcribed from official portal `def.org.in` (October 2026). Active mailbox status unverified. |
| **TGT-005** | **IGNOU School of Humanities (DISLI Program)** | Academic Interpreter Training Authority | `soh@ignou.ac.in` | **PENDING APPROVAL** | Transcribed from university portal `ignou.ac.in` SOH faculty directory (October 2026). Active mailbox status unverified. |

---

## 4. Approved Message Texts

Only the following three pre-vetted message drafts are authorized for dispatch upon gate sign-off:

### Approved Message 1: For Certified ISL Interpreters (TGT-001, TGT-004)
- **Subject:** `SignBridge Project: Invitation to evaluate experimental 3D ISL animation candidate (Namaste)`
- **Approved Body:** See [`Docs/M3_20_OUTREACH_STATUS_REPORT.md#draft-1-certified-isl-interpreters-islrtc--disli-programs`](file:///c:/AmazonMlChallenge/Docs/M3_20_OUTREACH_STATUS_REPORT.md).
- **Mandatory Disclosures:** Candidate is unvalidated computer-vision reconstruction; Mixamo Y-Bot has rigid metallic face without facial blendshapes; 15–25 min commitment; local-only browser execution; voluntary participation; right to disagree or mark Not Assessable.

### Approved Message 2: For Deaf Native Signers & Deaf Community Leaders (TGT-002, TGT-003)
- **Subject:** `Request for Deaf-native linguistic guidance: Experimental SignBridge 3D sign (Namaste)`
- **Approved Body:** See [`Docs/M3_20_OUTREACH_STATUS_REPORT.md#draft-2-deaf-native-signers--deaf-community-advocacy-leaders`](file:///c:/AmazonMlChallenge/Docs/M3_20_OUTREACH_STATUS_REPORT.md).
- **Mandatory Disclosures:** Deaf-led linguistic authority recognized; candidate not linguistically approved; zero cloud tracking; anonymous/pseudonymous participation supported; critical and rejecting verdicts fully welcomed.

### Approved Message 3: For Academic Sign Language Linguists (TGT-005)
- **Subject:** `Invitation for ISL Phonological Evaluation: 3D Motion-Capture Candidate (Gloss: NAMASTE)`
- **Approved Body:** See [`Docs/M3_20_OUTREACH_STATUS_REPORT.md#draft-3-academic-sign-language-linguists--phonologists`](file:///c:/AmazonMlChallenge/Docs/M3_20_OUTREACH_STATUS_REPORT.md).
- **Mandatory Disclosures:** Five-parameter phonological analysis (DEZ, TAB, ORI, SIG, NMM); tracking anomaly frame intervals (Frames 22, 59, 62); non-leading evaluation; documented dissent policy.

---

## 5. Restrictions on Attachments, Follow-Ups & Data Governance

1. **Attachment Prohibition:** Initial outreach emails must **not** include binary attachments, raw video files, or bulk animation JSON. All materials must be shared via controlled review studio links or local package distribution after recipient confirms interest.
2. **Follow-Up Restriction:** Unsolicited follow-up messages are strictly limited to **maximum one (1)** polite reminder sent no earlier than **seven (7) calendar days** after initial authorized dispatch. If no reply is received after one follow-up, the status must transition to `NO_RESPONSE` and contact must cease.
3. **Sensitive Personal Data Minimization:** Reviewers must never be asked for national identification numbers, financial details, medical information, or private addresses. The only requested metadata is voluntary signing fluency/role and review date.
4. **Local Execution Guarantee:** All evaluation workflows execute 100% client-side on `localhost` via WebGL and local file APIs. Zero audio, video, or evaluator keystrokes are transmitted to any external server.

---

## 6. Project-Owner Authorization Sign-Off Record

> [!CAUTION]
> **GATE LOCKOUT STATUS:**  
> This record must be manually reviewed, signed, and dated by the human project owner. Until signed, no electronic communication may occur.

```
================================================================================
PROJECT OWNER AUTHORIZATION RECORD (GATE STATUS)
================================================================================

Project Owner Name:         [ PENDING PROJECT OWNER SIGN-OFF ]
Institutional Title / Role: [ PENDING ]
Authorization Date:         [ UNCONFIRMED / UNSIGNED ]

Authorized Scope of Action:
  [ ] DRY_RUN_ONLY (No messages sent, internal preparation only) — [ACTIVE DEFAULT]
  [ ] STAGE_1_DISPATCH (Authorize sending Message 1 to TGT-001 and TGT-004)
  [ ] STAGE_2_DISPATCH (Authorize sending Message 2 to TGT-002 and TGT-003)
  [ ] STAGE_3_DISPATCH (Authorize sending Message 3 to TGT-005)

Owner Signature:            ____________________________________________________
Execution Mode:             DRY_RUN_ONLY (Awaiting signature)
Current System Status:      OUTREACH PENDING EXPLICIT AUTHORIZATION
================================================================================
```
