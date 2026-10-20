# SignBridge M3.24 — Outreach Readiness & Channel Verification Matrix

**Document Reference:** `Docs/M3_24_OUTREACH_READINESS_MATRIX.md`  
**Milestone:** SignBridge M3.24 — Owner Approval Sheet and Outreach Readiness Updates  
**Date:** October 20, 2026  
**Auditor / Editor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Execution Environment:** Chrome Headless CDP / TLS 1.3 / Local File Provenance  
**Current Governance State:** **`DRY_RUN_ONLY — PENDING EXPLICIT PROJECT-OWNER AUTHORIZATION`**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Active in Chrome extension & unchanged)  
**Evaluated Motion Candidate:** `isl_namaste_mocap_candidate_v1` (Quarantined in isolated experimental assets)  

---

## 1. Executive Summary & Verification Reconciliation

Milestone **M3.24** updates the outreach readiness matrix based on the empirical Chrome browser verification conducted in M3.23. All five proposed institutions remain in scope for the intended rollout, subject to owner review and explicit authorization.

### Key Corrections Incorporated from M3.23 Findings:
1. **NAD India (TGT-002):** Replaced unlisted `nadindia@gmail.com` with official published inbox `secretary@nadindia.org` on `https://nadindia.org/Contact`.
2. **AIFD (TGT-003):** Replaced defunct domain `aifd.org.in` with active official domain `https://aifdeaf.org/` and proposed email `aifdeaf@gmail.com`. Marked as **`NEEDS_REVERIFICATION`** rather than conclusively verified.
3. **DEF (TGT-004):** Verified trailing slash requirement (`https://def.org.in/contact/`). Email `info@def.org.in` confirmed visible on official contact page.
4. **ISLRTC (TGT-001):** Email `islrtcnewdelhi@gmail.com` confirmed visible on `https://islrtc.nic.in/contact-us/`.
5. **IGNOU SOH (TGT-005):** Replaced legacy 404 URL with active Samarth portal URL `https://www.ignou.ac.in/schools/school-of-humanities`. Noted that `soh@ignou.ac.in` is a general School Director's desk requiring owner routing guidance.

---

## 2. Comprehensive Outreach Readiness Matrix

| Target ID | Institution Name & Category | Proposed Contact Email | Official Contact URL | Evidence Source & Verification Status | Relevance to Review Request | Outstanding Uncertainties | Owner Decision | Dispatch Status |
|:---:|:---|:---|:---|:---|:---|:---|:---:|:---:|
| **TGT-001** | **ISLRTC**<br>*(Indian Sign Language Research & Training Centre)*<br>Autonomous Govt Body under MSJE / DEPwD | `islrtcnewdelhi@gmail.com` | `https://islrtc.nic.in/contact-us/` | **`VERIFIED_ON_OFFICIAL_SITE`**<br>Visible on official contact page (DOM line 503: `islrtcnewdelhi[at]gmail[dot]com`).<br>DOM: `TGT-001_ISLRTC_contact.dom.html`<br>Screenshot: `TGT-001_ISLRTC_contact.png` | Statutory author of ISL Dictionary Vol 1 (#0001); source of reference video; national interpreter certification authority. | Inbox deliverability and active monitoring are not verified by website publication. | `[ ] PENDING` | **`NOT_AUTHORIZED`** |
| **TGT-002** | **National Association of the Deaf (NAD) India**<br>Deaf-Led National Advocacy Apex Body | `secretary@nadindia.org`<br>*(Proposed Replacement)* | `https://nadindia.org/Contact`<br>*(Case-sensitive capital 'C')* | **`PROPOSED_FOR_OWNER_APPROVAL`**<br>M3.23 found previously proposed `nadindia@gmail.com` unlisted. Published inbox is `secretary@nadindia.org` (DOM line 891).<br>DOM: `TGT-002_NAD_contact.dom.html`<br>Screenshot: `TGT-002_NAD_contact.png` | Premier Deaf-led national advocacy organization; ensures Deaf-native community ownership and leadership in sign evaluation. | Inbox deliverability not tested; website contains template placeholder for phone `(123) 456-7890`. | `[ ] PENDING` | **`NOT_AUTHORIZED`** |
| **TGT-003** | **All India Federation of the Deaf (AIFD)**<br>National Deaf Federation (Est. 1955) | `aifdeaf@gmail.com`<br>*(Proposed Replacement)* | `https://aifdeaf.org/contact-us/`<br>*(Alternative Official Domain)* | **`NEEDS_REVERIFICATION`**<br>M3.23 found legacy domain `aifd.org.in` failing DNS resolution (`[Errno 11001]`). Active portal identified as `aifdeaf.org` with address `aifdeaf@gmail.com`. | Historical federation of deaf associations and clubs across India representing grassroots signers. | Replacement domain and mailbox need formal reverification before dispatch. Delivery to old Yahoo address is unverified. | `[ ] PENDING` | **`NOT_AUTHORIZED`** |
| **TGT-004** | **Deaf Enabled Foundation (DEF)**<br>Community Sign Training & Accessibility Foundation | `info@def.org.in` | `https://def.org.in/contact/`<br>*(Trailing slash required)* | **`VERIFIED_ON_OFFICIAL_SITE`**<br>Visible on official contact page (DOM line 638) with Secunderabad head office details.<br>DOM: `TGT-004_DEF_contact.html`<br>Screenshot: `TGT-004_def.org.png` | Extensive community sign training, certified interpreter network, and ISL educational accessibility initiatives. | Inbox deliverability and active monitoring are not verified by website publication. | `[ ] PENDING` | **`NOT_AUTHORIZED`** |
| **TGT-005** | **IGNOU School of Humanities (SOH)**<br>Academic ISL Interpreter Training Authority (DISLI) | `soh@ignou.ac.in` | `https://www.ignou.ac.in/schools/school-of-humanities`<br>*(Current Samarth CMS portal)* | **`NEEDS_OWNER_ROUTING_REVIEW`**<br>Legacy URL returned 404 after university portal overhaul. Directory lists `soh@ignou.ac.in` and `directorsoh@ignou.ac.in`.<br>DOM: `TGT-005_IGNOU_home.dom.html`<br>Screenshot: `TGT-005_IGNOU_home.png` | Academic home of Diploma in Indian Sign Language Interpretation (DISLI) in collaboration with ISLRTC; linguistics faculty. | `soh@ignou.ac.in` is a general School Director's desk and may not directly reach the DISLI program coordinator or linguistics faculty. | `[ ] PENDING` | **`NOT_AUTHORIZED`** |

---

## 3. Detailed Audit Notes & Reconciliation Per Target

### Target TGT-001 (ISLRTC)
- **Historical M3.22 Entry:** `https://islrtc.nic.in/contact-us`, `islrtcnewdelhi@gmail.com`
- **M3.24 Corrected Entry:** `https://islrtc.nic.in/contact-us/`, `islrtcnewdelhi@gmail.com`
- **Reconciliation & Status:** Contact email is visibly confirmed in the live DOM (Line 503) as `islrtcnewdelhi[at]gmail[dot]com`. Trailing slash added to URL for canonical routing. Status remains **`VERIFIED_ON_OFFICIAL_SITE`**. No claim of inbox deliverability or active monitoring is made.

### Target TGT-002 (NAD India)
- **Historical M3.22 Entry:** `https://nadindia.org/contact`, `nadindia@gmail.com`
- **M3.24 Corrected Entry:** `https://nadindia.org/Contact`, `secretary@nadindia.org`
- **Reconciliation & Status:** M3.23 browser audit revealed `nadindia@gmail.com` is completely unlisted on `nadindia.org`. The official contact page visibly publishes `secretary@nadindia.org` (Line 891). URL route requires capital 'C'. Status is set to **`PROPOSED_FOR_OWNER_APPROVAL`** (not auto-approved).

### Target TGT-003 (AIFD)
- **Historical M3.22 Entry:** `http://aifd.org.in`, `aifd1955@yahoo.co.in`
- **M3.24 Corrected Entry:** `https://aifdeaf.org/contact-us/`, `aifdeaf@gmail.com`
- **Reconciliation & Status:** Domain `aifd.org.in` is completely defunct (DNS resolution failed). The active registered domain is `aifdeaf.org`. Because the available headless evidence did not capture a conclusive full DOM dump of the replacement page during M3.23, the status is honestly marked **`NEEDS_REVERIFICATION`** and proposed for owner evaluation rather than claimed as verified.

### Target TGT-004 (DEF)
- **Historical M3.22 Entry:** `https://def.org.in/contact`, `info@def.org.in`
- **M3.24 Corrected Entry:** `https://def.org.in/contact/`, `info@def.org.in`
- **Reconciliation & Status:** URL requires trailing slash on DEF's WordPress instance (`/contact` returned 404). Contact email `info@def.org.in` is visibly confirmed on the official page (Line 638). Status remains **`VERIFIED_ON_OFFICIAL_SITE`**. Deliverability is not tested.

### Target TGT-005 (IGNOU School of Humanities)
- **Historical M3.22 Entry:** `http://ignou.ac.in/ignou/aboutignou/school/soh/introduction`, `soh@ignou.ac.in`
- **M3.24 Corrected Entry:** `https://www.ignou.ac.in/schools/school-of-humanities`, `soh@ignou.ac.in`
- **Reconciliation & Status:** Port 80 connection resets; legacy URL 404s after university migration to the Samarth eGov portal. SOH email `soh@ignou.ac.in` is listed in official directories. However, because it addresses the general School Director's office, status is marked **`NEEDS_OWNER_ROUTING_REVIEW`** to allow the project owner to determine whether to contact the general desk or seek the specific DISLI program coordinator.

---

## 4. Technical Safeguards, Cryptographic Hashes & Provenance

All technical safeguards have been carried forward and verified against local repository files:

```
================================================================================
CRYPTOGRAPHIC ASSET PROVENANCE AUDIT
================================================================================
1. Candidate Output JSON:
   Path: tools/isl_motion_extraction/output/isl_namaste_mocap_candidate_v1.json
   Computed SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
   Expected SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
   Status: BIT-FOR-BIT MATCH (VERIFIED)

2. Extension Candidate Asset Copy:
   Path: extension/assets/animations/isl_namaste_mocap_candidate_v1.json
   Computed SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
   Expected SHA-256: 6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46
   Status: BIT-FOR-BIT MATCH (VERIFIED)

3. Reference Video:
   Path: tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4
   Computed SHA-256: 129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8
   Expected SHA-256: 129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8
   Status: BIT-FOR-BIT MATCH (VERIFIED)
================================================================================
```

### Production Routing Safeguards:
- `isl_namaste_godl_v1` remains the active production baseline in `extension/animation/keyframe_registry.js` and `extension/translation/isl_translator.js`.
- Candidate `isl_namaste_mocap_candidate_v1` remains strictly quarantined with `isLinguisticISL: false` and `status: "experimental_awaiting_validation"`.
- Technical retargeting metrics do not constitute linguistic or cultural correctness.

### Licensing & Redistribution Safeguards:
- Raw reference-video redistribution rights remain **UNRESOLVED**.
- The reference MP4 video is **strictly prohibited** from email attachments, external uploads, or bundle inclusion in `extension/assets/`.
- Third-party mirror license tags are not legal proof of copyright permission.
- The proposed review workflow operates locally on `localhost` via Chrome WebGL and does not require redistributing the reference video.

---

## 5. Governance & Operational Gate Status

```
================================================================================
M3.24 OUTREACH READINESS GATE STATUS
================================================================================
System Execution Mode:          DRY_RUN_ONLY
Total Tracked Institutions:     5 (All 5 in scope for intended rollout)
Verified on Official Sites:     2 (TGT-001 ISLRTC, TGT-004 DEF)
Proposed for Owner Approval:    1 (TGT-002 NAD India)
Needs Reverification:           1 (TGT-003 AIFD)
Needs Owner Routing Review:     1 (TGT-005 IGNOU SOH)
External Messages Dispatched:   0 (Zero)
External Forms Submitted:       0 (Zero)
External Contacts Approached:   0 (Zero)
Binary Files Shared:            0 (Zero)
Owner Authorization Executed:   NO (Awaiting explicit human signature)
Operational Gate Status:        LOCKED IN DRY_RUN_ONLY
Linguistic Validation Status:   HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD
================================================================================
```
