# SignBridge M3.24 — Owner Approval Sheet and Outreach Readiness Updates

**Document Reference:** `Docs/M3_24_UPDATE_REPORT.md`  
**Milestone:** SignBridge M3.24 — Owner Approval Sheet and Outreach Readiness Updates  
**Execution Date:** October 20, 2026  
**Auditor / Editor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Execution Mode:** **`DRY_RUN_ONLY — PENDING EXPLICIT PROJECT-OWNER AUTHORIZATION`**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Active in Chrome extension & unchanged)  
**Evaluated Motion Candidate:** `isl_namaste_mocap_candidate_v1` (Quarantined in isolated experimental assets)  

---

## 1. Executive Summary & Deliverables Audit

Milestone **M3.24** updates the SignBridge outreach approval documentation, recipient matrix, and invitation drafts based on the empirical Chrome browser verification completed in M3.23. The updated package is prepared for formal review and explicit sign-off by the project owner.

### Strictly Maintained Governance Invariants:
1. **Zero External Outreach Executed:** In strict compliance with project governance, **zero emails were transmitted, zero contact forms were submitted, no individuals or institutions were approached, and zero candidate or video files were uploaded or distributed externally.**
2. **Distinct Decision Gates:** Document and recipient approval is decoupled from message dispatch. Approval of the outreach plan **DOES NOT** authorize sending emails.
3. **Historical Record Integrity:** M3.21, M3.22, and M3.23 deliverables are preserved intact as historical audit records. M3.24 explicitly identifies corrections and grounds them in empirical evidence without silent rewrites.
4. **Licensing & Technical Quarantine:** The reference MP4 video redistribution rights remain **UNRESOLVED**, and the file remains quarantined. Production speech-to-sign routing continues to resolve strictly to `isl_namaste_godl_v1`.

### Files Created & Modified in M3.24:

| File Path | Operation | Description |
|:---|:---:|:---|
| [`Docs/M3_24_OWNER_APPROVAL_SHEET.md`](file:///c:/AmazonMlChallenge/Docs/M3_24_OWNER_APPROVAL_SHEET.md) | **Created** | Comprehensive approval sheet with corrected recipient matrix, complete revised drafts, clarified Draft 2 wording, licensing declarations, and a 5-part explicit owner sign-off gate. |
| [`Docs/M3_24_OUTREACH_READINESS_MATRIX.md`](file:///c:/AmazonMlChallenge/Docs/M3_24_OUTREACH_READINESS_MATRIX.md) | **Created** | Granular channel verification ledger detailing evidence sources, DOM findings, remit plausibility, outstanding uncertainties, and owner approval status. |
| [`Docs/M3_24_UPDATE_REPORT.md`](file:///c:/AmazonMlChallenge/Docs/M3_24_UPDATE_REPORT.md) | **Created** | (This Document) Execution audit, reconciliation summary, test suite reporting, and milestone status. |
| [`tools/isl_motion_extraction/tests/test_outreach_governance.py`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/tests/test_outreach_governance.py) | **Modified** | Expanded from 9 to 12 unit tests to assert presence of M3.24 files, corrected recipients, Draft 2 wording, and the 5-part decision gate. |

---

## 2. Institutional Recipient Matrix Corrections

All five institutions remain in scope for the intended rollout, subject to owner evaluation and explicit authorization.

```
====================================================================================================
M3.24 RECIPIENT MATRIX RECONCILIATION SUMMARY
====================================================================================================
TGT-001 (ISLRTC):       VERIFIED_ON_OFFICIAL_SITE   (islrtcnewdelhi@gmail.com on islrtc.nic.in/contact-us/)
TGT-002 (NAD India):    PROPOSED_FOR_OWNER_APPROVAL (secretary@nadindia.org on nadindia.org/Contact)
TGT-003 (AIFD):         NEEDS_REVERIFICATION        (aifdeaf@gmail.com on active domain aifdeaf.org)
TGT-004 (DEF):          VERIFIED_ON_OFFICIAL_SITE   (info@def.org.in on def.org.in/contact/)
TGT-005 (IGNOU SOH):    NEEDS_OWNER_ROUTING_REVIEW  (soh@ignou.ac.in on ignou.ac.in/schools/school-of-humanities)
====================================================================================================
```

### Granular Institution Details:

1. **Target TGT-001 — ISLRTC (Indian Sign Language Research and Training Centre)**
   - **Proposed Email:** `islrtcnewdelhi@gmail.com`
   - **Official URL:** `https://islrtc.nic.in/contact-us/` (Canonical trailing slash)
   - **M3.23 Evidence:** Confirmed visibly published in official DOM (Line 503) as `islrtcnewdelhi[at]gmail[dot]com` (NIC anti-spam format). Full page screenshot captured at `Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.png`.
   - **Verification Status:** `VERIFIED_ON_OFFICIAL_SITE`. Website publication confirms the public directory entry but does not establish inbox deliverability or active monitoring.
   - **Relevance:** Statutory body that published ISL Dictionary Vol 1 (Namaste #0001); conducts national interpreter certification.

2. **Target TGT-002 — NAD India (National Association of the Deaf)**
   - **Proposed Email:** `secretary@nadindia.org` *(Replaced `nadindia@gmail.com`)*
   - **Official URL:** `https://nadindia.org/Contact` *(Case-sensitive route; capital 'C')*
   - **M3.23 Evidence:** The previously proposed `nadindia@gmail.com` does not appear anywhere on `nadindia.org`. The official contact page visibly publishes `<a href="mailto:secretary@nadindia.org">secretary@nadindia.org</a>` (Line 891). Screenshot at `TGT-002_NAD_contact.png`.
   - **Verification Status:** `PROPOSED_FOR_OWNER_APPROVAL`. Marked as proposed for owner evaluation, not automatically approved for dispatch.
   - **Relevance:** Premier Deaf-led national advocacy organization; ensures community representation and linguistic self-determination.

3. **Target TGT-003 — AIFD (All India Federation of the Deaf)**
   - **Proposed Email:** `aifdeaf@gmail.com` *(Replaced `aifd1955@yahoo.co.in`)*
   - **Proposed Official URL:** `https://aifdeaf.org/contact-us/` *(Alternative active domain)*
   - **M3.23 Evidence:** The legacy domain `aifd.org.in` completely failed DNS resolution (`[Errno 11001]`). Web research identified `https://aifdeaf.org/` as the active official portal with listed email `aifdeaf@gmail.com`.
   - **Verification Status:** **`NEEDS_REVERIFICATION`**. Because headless Chrome automated capture did not dump a complete rendered DOM of the replacement portal, the replacement address is honestly classified as `NEEDS_REVERIFICATION` rather than claimed as conclusively verified.
   - **Relevance:** National federation founded in 1955 representing deaf associations across India.

4. **Target TGT-004 — DEF (Deaf Enabled Foundation)**
   - **Proposed Email:** `info@def.org.in`
   - **Official URL:** `https://def.org.in/contact/` *(Trailing slash required; bare path 404s)*
   - **M3.23 Evidence:** Confirmed visibly published in official DOM (Line 638) as `info@def.org.in` with Secunderabad head office address. Screenshot at `TGT-004_def.org.png`.
   - **Verification Status:** `VERIFIED_ON_OFFICIAL_SITE`. Deliverability is not tested.
   - **Relevance:** Extensive community sign education, certified interpreter network, and accessibility media production.

5. **Target TGT-005 — IGNOU School of Humanities (SOH)**
   - **Proposed Email:** `soh@ignou.ac.in`
   - **Current School URL:** `https://www.ignou.ac.in/schools/school-of-humanities` *(Current Samarth portal)*
   - **M3.23 Evidence:** The legacy URL (`/ignou/aboutignou/school/soh/introduction`) returned a 404 due to the university-wide migration to the Samarth eGov portal. Official directories list `soh@ignou.ac.in` and `directorsoh@ignou.ac.in`. Portal screenshot at `TGT-005_IGNOU_home.png`.
   - **Verification Status:** `NEEDS_OWNER_ROUTING_REVIEW`. `soh@ignou.ac.in` is a general School Director's desk and may not directly reach the DISLI program coordinator or linguistics faculty.
   - **Relevance:** Academic institution that co-established the DISLI interpreter curriculum with ISLRTC; home of academic sign linguistics faculty.

---

## 3. Invitation Draft Neutrality & Draft 2 Clarification

All three invitation drafts were audited to guarantee absolute neutrality, non-coercive framing, and protection of evaluator independence.

### Key Draft Wording Update (Draft 2):
In Draft 2 (assigned to Deaf Native Signers & Community Leaders at TGT-002 and TGT-003), the sentence:
> *“A side-by-side comparison between the original ISLRTC dictionary video and a 3D humanoid avatar”*

has been updated to:
> **“What you will review (if you choose to participate): A side-by-side comparison between the dictionary reference video and a 3D avatar within a local Chrome studio (no video is attached to this email).”**

### Neutrality & Safety Checklist Across All Drafts:
- [x] **Neutral, Non-Coercive Language:** No claims that the avatar is "accurate," "natural," or "ready."
- [x] **No Institutional Endorsement:** Does not claim or request endorsement from any institution.
- [x] **Explicit Experimental Status:** States that mathematical kinematics and tracking confidence do not equal linguistic correctness.
- [x] **Rig Limitations Fully Disclosed:** Discloses that the Mixamo Y-Bot rig has a rigid metallic face without facial blendshapes.
- [x] **Mandatory `NOT ASSESSABLE` Option:** Instructs evaluators to mark facial expressions as `NOT ASSESSABLE`.
- [x] **Uncertainty & Dissent Protected:** Empowers evaluators to declare monocular perspective ambiguity and guarantees dissenting records will be preserved.
- [x] **Voluntary & Uncompensated:** Clearly states participation is voluntary with zero commercial pressure or compensation promises.

---

## 4. Technical Safeguards & Provenance Audit

Local repository assets were independently checked against cryptographic baselines:

```
================================================================================
CRYPTOGRAPHIC FILE INTEGRITY AUDIT
================================================================================
1. Experimental Candidate Output JSON:
   Path: tools/isl_motion_extraction/output/isl_namaste_mocap_candidate_v1.json
   Computed SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
   Expected SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
   Integrity Status: MATCH (Bit-for-bit verified)

2. Extension Candidate Copy:
   Path: extension/assets/animations/isl_namaste_mocap_candidate_v1.json
   Computed SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
   Expected SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
   Integrity Status: MATCH (Identical to extraction output)

3. Reference Video:
   Path: tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4
   Computed SHA-256: 129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8
   Expected SHA-256: 129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8
   Integrity Status: MATCH (Original source reference)
================================================================================
```

### Production Routing Safeguards:
- `isl_namaste_godl_v1` remains the active production baseline in `extension/animation/keyframe_registry.js` and `extension/translation/isl_translator.js`.
- Candidate `isl_namaste_mocap_candidate_v1` is strictly excluded from default registration.
- Retargeting metrics (e.g. wrist distance 0.080m) are treated purely as kinematic telemetry and not as linguistic proof.
- `tools/isl_motion_extraction/reviews/` contains zero records; zero reviews have been fabricated.

### Licensing Safeguards:
- **Redistribution Rights Unresolved:** Redistribution rights for `ISLRTC_Namaste_sample.mp4` remain explicitly marked **UNRESOLVED**.
- **Attachment Prohibition:** The raw video is prohibited from email attachments, external hosting, or bundle inclusion in `extension/assets/`.
- **Third-Party Labels Disclaimed:** Third-party license tags are not treated as legal permission from the rights holder.
- **Workflow Independence:** The evaluation studio operates entirely on `localhost` via Chrome WebGL and does not redistribute the reference video.

---

## 5. Independent Test Execution Results

All 10 test suites were executed independently during M3.24:

| Suite ID | Suite Name | Command Executed | Mode | Exit Code | Checks Run | Passed | Failed | Status |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **S1** | Review Record Validator | `python tools/isl_motion_extraction/tests/test_review_validator.py` | CLI Sync | 0 | 9 | 9 | 0 | **PASSED** |
| **S2** | Review Round-Trip Suite | `python tools/isl_motion_extraction/tests/test_review_roundtrip.py` | CLI Sync | 0 | 10 | 10 | 0 | **PASSED** |
| **S3** | Browser Usability CDP Suite | `python tools/isl_motion_extraction/tests/test_browser_usability.py` | Headless Chrome | 0 | 15 | 15 | 0 | **PASSED** |
| **S4** | Review Readiness Suite | `python tools/isl_motion_extraction/tests/test_review_readiness.py` | CLI Sync | 0 | 12 | 12 | 0 | **PASSED** |
| **S5** | Retargeting Pipeline Suite | `python tools/isl_motion_extraction/tests/test_retargeting.py` | CLI Sync | 0 | 13 | 13 | 0 | **PASSED** |
| **S6** | Outreach Governance (Expanded) | `python tools/isl_motion_extraction/tests/test_outreach_governance.py` | CLI Sync | 0 | 12 | 12 | 0 | **PASSED** |
| **S7** | Pre-Flight Readiness Diagnostic | `python tools/isl_motion_extraction/check_review_readiness.py` | CLI Sync | 0 | 27 | 27 | 0 | **PASSED** |
| **S8** | Ingestion Directory Audit | `python tools/isl_motion_extraction/validate_review_record.py` | CLI Sync | 0 | 0 records | 0 records | 0 | **AWAITING SUBMISSIONS** |
| **S9** | Local Speech Backend Suite | `signbridge-backend\.venv\Scripts\python.exe test_backend.py` | Async Task | 0 | 8 | 8 | 0 | **PASSED** |
| **S10** | Chrome In-Engine Regression | `python run_chrome_tests.py` | Headless Chrome | 0 | 132 | 132 | 0 | **PASSED** |

**Total Automated Checks Executed:** **238 checks / 238 PASSED / 0 FAILED**

---

## 6. Explicit Owner Sign-Off Gate & Pending Decisions

Section 6 of [`Docs/M3_24_OWNER_APPROVAL_SHEET.md`](file:///c:/AmazonMlChallenge/Docs/M3_24_OWNER_APPROVAL_SHEET.md) presents five distinct decision gates for project-owner action:

1. **Decision on Corrected Recipients:** Approval of updated addresses for TGT-001 through TGT-005.
2. **Decision on Complete Invitation Drafts:** Approval of verbatim texts for Drafts 1, 2 (clarified), and 3.
3. **Decision on Rollout Scope:** Approval to keep all five institutions in scope or execute a staged rollout (e.g. TGT-001 and TGT-004 first).
4. **Acknowledgement of Licensing Uncertainty:** Formal acknowledgement that reference-video redistribution rights remain unresolved.
5. **Separate Dispatch Authorization Gate:** Explicit decision regarding future dispatch (currently locked in `REMAIN_IN_DRY_RUN`).

Every decision is currently set to `PENDING`. No email dispatch can occur until the owner explicitly signs and executes Gate 5.

---

## 7. Milestone Completion Statement

In accordance with the M3.24 objective:
- The owner approval sheet, readiness matrix, and governance tests have been updated with verified contact channels and clarified draft language.
- Historical verification records (M3.21, M3.22, M3.23) are preserved intact.
- The system remains strictly locked in `DRY_RUN_ONLY`. Zero external messages have been sent.
- The experimental candidate remains quarantined, and production routing remains locked to `isl_namaste_godl_v1`.

```
================================================================================
M3.24 STATUS: READY FOR OWNER REVIEW — OUTREACH NOT AUTHORIZED — HUMAN REVIEW PENDING
================================================================================
```
