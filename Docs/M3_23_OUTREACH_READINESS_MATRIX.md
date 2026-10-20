# SignBridge M3.23 — Outreach Readiness & Channel Verification Matrix

**Document Reference:** `Docs/M3_23_OUTREACH_READINESS_MATRIX.md`  
**Milestone:** SignBridge M3.23 — Independent Chrome Verification of Outreach Plan  
**Verification Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Execution Environment:** Chrome Browser / Headless CDP / TLS 1.3 / Local File Provenance  
**Current Governance State:** **DRY_RUN_ONLY — PENDING EXPLICIT PROJECT-OWNER SIGNATURE**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Active in extension & unchanged)  
**Evaluated Motion Candidate:** `isl_namaste_mocap_candidate_v1` (Quarantined in isolated experimental assets)  

---

## 1. Executive Channel Verification Summary

In accordance with the M3.23 mandate, all five proposed outreach targets from [`Docs/M3_22_OWNER_APPROVAL_SHEET.md`](file:///c:/AmazonMlChallenge/Docs/M3_22_OWNER_APPROVAL_SHEET.md) were independently audited via Chrome browser access, live HTTP/TLS inspection, and DOM text analysis.

No emails were sent, no contact forms were submitted, and no external parties were contacted. Website publication confirms the presence of contact details on an official domain, but does **not** establish that an inbox is actively monitored or deliverable.

### Institutional Verification Status At-A-Glance

| Target ID | Institution | Proposed Email (M3.22) | Verified Official Email | Chrome Verification Status | Remit Plausibility | Action Required by Owner |
|:---:|:---|:---|:---|:---:|:---:|:---|
| **TGT-001** | **ISLRTC** | `islrtcnewdelhi@gmail.com` | `islrtcnewdelhi@gmail.com` | **`VERIFIED_ON_OFFICIAL_SITE`** | **Plausible (High)**<br>Statutory author of ISL Dictionary Vol 1 (#0001) | Ready for explicit owner approval decision |
| **TGT-002** | **NAD India** | `nadindia@gmail.com` | `secretary@nadindia.org` | **`UNVERIFIED`**<br>(Proposed address unlisted) | **Plausible (High)**<br>Apex Deaf-led advocacy organization | Owner review needed: Update recipient to `secretary@nadindia.org` |
| **TGT-003** | **AIFD** | `aifd1955@yahoo.co.in` | `aifdeaf@gmail.com`<br>`aifddeaf@yahoo.com` | **`INACCESSIBLE`**<br>(Domain `aifd.org.in` defunct) | **Plausible (High)**<br>National Deaf Federation (Est. 1955) | Owner review needed: Update domain to `aifdeaf.org` and email to `aifdeaf@gmail.com` |
| **TGT-004** | **DEF** | `info@def.org.in` | `info@def.org.in` | **`VERIFIED_ON_OFFICIAL_SITE`** | **Plausible (High)**<br>Community sign training & interpreter services | Ready for explicit owner approval decision |
| **TGT-005** | **IGNOU SOH** | `soh@ignou.ac.in` | `soh@ignou.ac.in`<br>`directorsoh@ignou.ac.in` | **`NEEDS_OWNER_REVIEW`**<br>(Legacy URL 404; email verified in directory) | **Plausible (High)**<br>Academic DISLI training & linguistics | Owner review needed: Confirm portal directory reference and routing |

---

## 2. Granular Recipient Verification Audit

### Target TGT-001: Indian Sign Language Research and Training Centre (ISLRTC)
- **Institution Name:** Indian Sign Language Research and Training Centre (ISLRTC)
- **Category:** Statutory Authority / Certified Interpreters (Autonomous body under DEPwD, Ministry of Social Justice & Empowerment, Govt of India)
- **Proposed URL in M3.22:** `https://islrtc.nic.in/contact-us`
- **Audited Official URL:** `https://islrtc.nic.in/contact-us/` (Redirects to canonical trailing slash)
- **Audited Page Title:** `Contact Us | Indian Sign Language Research and Training Center ,Government of India | India`
- **Verification Date:** October 20, 2026
- **Proposed Email:** `islrtcnewdelhi@gmail.com`
- **Visible Email on Page:** `islrtcnewdelhi[at]gmail[dot]com` (Anti-scraping format for `islrtcnewdelhi@gmail.com`)
- **Additional Contacts Listed:**
  - Admission Enquiries: `isltcadmission[at]gmail[dot]com`, Mobile: `+91 90130 15606`
  - Office Phone: `011-26327558`, `011-26327550`
  - Address: Module no. 403-406, Fourth Floor, NSIC Business Park, Okhla Industrial Estate, New Delhi - 110020
- **Evidence Files:**
  - DOM Dump: [`Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.dom.html) (Line 503)
  - Full Page Screenshot: [`Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.png)
- **Institutional Remit & Plausibility:**
  - **Verdict:** Highly Plausible.
  - **Rationale:** ISLRTC is the national statutory body that standardizes ISL and created the official ISLRTC Dictionary Vol 1. Word #0001 (*NAMASTE*) is the exact source of the reference video used in the SignBridge reconstruction. ISLRTC also administers national interpreter certification (DISLI/DTISL).
- **Assigned Draft:** Draft 1 (Certified ISL Interpreters & Statutory Bodies)
- **Verification Status:** **`VERIFIED_ON_OFFICIAL_SITE`**
- **Issues Found:** None. Obfuscated format `[at]` / `[dot]` is standard Indian Government NIC anti-spam practice.

---

### Target TGT-002: National Association of the Deaf (NAD) India
- **Institution Name:** National Association of the Deaf (NAD) India
- **Category:** Deaf Native Signers & Deaf Community Advocacy Leaders
- **Proposed URL in M3.22:** `https://nadindia.org/contact`
- **Audited Official URL:** `https://nadindia.org/Contact` (Case-sensitive route; lowercase `/contact` returns 404)
- **Audited Page Title:** `Contact Us - National Association of the Deaf - National Association of the Deaf, India`
- **Verification Date:** October 20, 2026
- **Proposed Email:** `nadindia@gmail.com`
- **Visible Email on Page:** `<a href="mailto:secretary@nadindia.org">secretary@nadindia.org</a>` (Line 891)
- **Additional Contacts Listed:**
  - Mobile: `9810234165 (SMS Only)`
  - Phone: `(123) 456-7890` (Note: Static template placeholder present on site)
  - Address: `#102, 19A Vishal Complex, Opp. Una Enclave, Mayur Vihar, Phase-1, Delhi - 110091. India`
- **Evidence Files:**
  - DOM Dump: [`Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.dom.html) (Lines 888–893)
  - Full Page Screenshot: [`Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.png)
- **Institutional Remit & Plausibility:**
  - **Verdict:** Highly Plausible.
  - **Rationale:** NAD India is the premier national advocacy organization led by Deaf individuals in India, actively advocating for the legal recognition of ISL and deaf rights under RPwD Act 2016. Engaging NAD leadership ensures Deaf-native community ownership and prevents paternalistic assumptions.
- **Assigned Draft:** Draft 2 (Deaf Native Signers & Deaf Community Leaders)
- **Verification Status:** **`UNVERIFIED` (for `nadindia@gmail.com`) / `NEEDS_OWNER_REVIEW`**
- **Issues Found:**
  1. The proposed address `nadindia@gmail.com` does **not** appear anywhere on the official contact page. The published official inbox is `secretary@nadindia.org`.
  2. The contact page URL is case-sensitive on the server (`/Contact` succeeds; `/contact` returns 404).
  3. The phone number field contains an unconfigured placeholder `(123) 456-7890`, though the SMS number `9810234165` is valid.
- **Recommended Tracked Change:** Update proposed recipient address to `secretary@nadindia.org` and URL to `https://nadindia.org/Contact`, pending project-owner approval.

---

### Target TGT-003: All India Federation of the Deaf (AIFD)
- **Institution Name:** All India Federation of the Deaf (AIFD)
- **Category:** Deaf Federation / Community Advocates (Est. 1955)
- **Proposed URL in M3.22:** `http://aifd.org.in`
- **Audited Official URL:** DNS Resolution Failed for `aifd.org.in` (`[Errno 11001] getaddrinfo failed`). Domain is defunct.
- **Active Official Domain Identified:** `https://aifdeaf.org/` (Registered and active official domain)
- **Audited Page Title on Active Site:** `Contact Us – All India Federation of the Deaf`
- **Verification Date:** October 20, 2026
- **Proposed Email:** `aifd1955@yahoo.co.in`
- **Visible Email on Active Page:** `aifdeaf@gmail.com` and `aifddeaf@yahoo.com`
- **Additional Contacts Listed:**
  - Office Address: 18, Institutional Area, Shaheed Jeet Singh Marg, New Delhi - 110067
  - Telephone: `011-26966337`, `011-26966338`
- **Evidence Files:**
  - DNS Failure Record: Direct socket lookup confirms `aifd.org.in` has no active DNS A/AAAA records.
  - Active Portal Record: `https://aifdeaf.org/contact-us/`
- **Institutional Remit & Plausibility:**
  - **Verdict:** Highly Plausible.
  - **Rationale:** Founded in 1955, AIFD is one of the oldest national federations representing deaf associations, deaf clubs, and grassroots signers across India.
- **Assigned Draft:** Draft 2 (Deaf Native Signers & Deaf Community Leaders)
- **Verification Status:** **`INACCESSIBLE` (Proposed Domain) / `NEEDS_OWNER_REVIEW`**
- **Issues Found:**
  1. The proposed domain `aifd.org.in` is completely defunct.
  2. The proposed email `aifd1955@yahoo.co.in` cannot be verified on the defunct domain.
  3. The legitimate active domain is `aifdeaf.org` with active emails `aifdeaf@gmail.com` and `aifddeaf@yahoo.com`.
- **Recommended Tracked Change:** Update target domain to `https://aifdeaf.org/contact-us/` and recipient address to `aifdeaf@gmail.com`, pending project-owner approval.

---

### Target TGT-004: Deaf Enabled Foundation (DEF)
- **Institution Name:** Deaf Enabled Foundation (DEF)
- **Category:** Community Sign Interpreters & Accessibility Trainers
- **Proposed URL in M3.22:** `https://def.org.in/contact`
- **Audited Official URL:** `https://def.org.in/contact/` (Trailing slash required; `/contact` returns 404)
- **Audited Page Title:** `Contact Us – Deaf Enabled Foundation`
- **Verification Date:** October 20, 2026
- **Proposed Email:** `info@def.org.in`
- **Visible Email on Page:** `info@def.org.in` (Line 638)
- **Additional Contacts Listed:**
  - Head Office Address: 7th floor and 704, Navketan Complex, S.D. Road, Secunderabad, Telangana – 500 003
  - Branch Office (Chennai): 2nd & 3rd Floor, Old No. 131, New No: 259, Triplicane High Road, Triplicane, Chennai – 600005
  - Mobile: `+91 97033 81112`
- **Evidence Files:**
  - DOM Dump: [`Docs/evidence/m3_23_chrome_verification/TGT-004_DEF_contact.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-004_DEF_contact.html) (Line 638)
  - Full Page Screenshot: [`Docs/evidence/m3_23_chrome_verification/TGT-004_def.org.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-004_def.org.png)
- **Institutional Remit & Plausibility:**
  - **Verdict:** Highly Plausible.
  - **Rationale:** DEF provides extensive ISL educational materials, interpreter training programs, sign language mobile applications, and community empowerment initiatives. Their certified interpreters regularly evaluate sign accuracy in real-world contexts.
- **Assigned Draft:** Draft 1 (Certified ISL Interpreters & Statutory Bodies)
- **Verification Status:** **`VERIFIED_ON_OFFICIAL_SITE`**
- **Issues Found:**
  - The URL requires a trailing slash (`/contact/`). The bare path `/contact` serves a 404 handler on their WordPress instance. The proposed URL in M3.22 should include the trailing slash.

---

### Target TGT-005: IGNOU School of Humanities (SOH)
- **Institution Name:** Indira Gandhi National Open University (IGNOU) — School of Humanities (SOH)
- **Category:** Academic Sign Language Linguists (DISLI Program)
- **Proposed URL in M3.22:** `http://ignou.ac.in/ignou/aboutignou/school/soh/introduction`
- **Audited Official URL:** `https://www.ignou.ac.in/` (University Portal); legacy `/ignou/aboutignou/school/soh/...` subpath returns 404 due to the university's migration to the Samarth eGov portal.
- **Audited Page Title:** `Indira Gandhi National Open University (IGNOU)`
- **Verification Date:** October 20, 2026
- **Proposed Email:** `soh@ignou.ac.in`
- **Visible Email in Academic Directory:** `soh@ignou.ac.in` and `directorsoh@ignou.ac.in`
- **Additional Contacts Listed:**
  - Physical Location: Block-F, New Academic Complex, IGNOU, Maidan Garhi, New Delhi - 110068
  - SOH Telephone: `011-29532962`, `011-29535491`
- **Evidence Files:**
  - Portal Screenshot: [`Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.png)
  - Portal DOM: [`Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.dom.html)
- **Institutional Remit & Plausibility:**
  - **Verdict:** Highly Plausible.
  - **Rationale:** IGNOU's School of Humanities (in collaboration with ISLRTC) established the formal academic curriculum for the Diploma in Indian Sign Language Interpretation (DISLI) and houses academic faculty focused on sign linguistics and English-ISL translation. They are suited for the phonological rubric in Draft 3.
- **Assigned Draft:** Draft 3 (Academic Sign Language Linguists & Phonologists)
- **Verification Status:** **`NEEDS_OWNER_REVIEW`**
- **Issues Found:**
  1. Plain HTTP (`http://ignou.ac.in`) resets connections; port 443 (HTTPS) is required.
  2. The legacy subpath `/ignou/aboutignou/school/soh/introduction` returns 404 following the university's portal redesign.
  3. The general SOH mailbox (`soh@ignou.ac.in`) reaches the Director's office rather than the DISLI Program Coordinator directly.
- **Recommended Tracked Change:** Update URL reference to the current Samarth portal directory and obtain owner confirmation on whether to address the general Dean/Director desk (`soh@ignou.ac.in`) or identify the specific DISLI program coordinator.

---

## 3. Recommended Tracked Modifications to Recipient Matrix

To maintain project document integrity without silently overwriting approved source documents, the following changes are formally submitted for project-owner approval:

| Target ID | Field | M3.22 Approved Value | Proposed M3.23 Tracked Correction | Rationale |
|:---:|:---|:---|:---|:---|
| **TGT-001** | URL | `https://islrtc.nic.in/contact-us` | `https://islrtc.nic.in/contact-us/` | Adds trailing slash to match canonical server route. |
| **TGT-002** | Contact URL | `https://nadindia.org/contact` | `https://nadindia.org/Contact` | Server requires capital 'C'; lowercase yields 404. |
| **TGT-002** | Recipient Email | `nadindia@gmail.com` | `secretary@nadindia.org` | Visible, published email on official contact page. |
| **TGT-003** | Domain / URL | `http://aifd.org.in` | `https://aifdeaf.org/contact-us/` | Legacy domain `aifd.org.in` has no DNS records. Active domain is `aifdeaf.org`. |
| **TGT-003** | Recipient Email | `aifd1955@yahoo.co.in` | `aifdeaf@gmail.com` | Verified contact address on active official domain. |
| **TGT-004** | Contact URL | `https://def.org.in/contact` | `https://def.org.in/contact/` | Server requires trailing slash; bare path returns 404. |
| **TGT-005** | Contact URL | `http://ignou.ac.in/ignou/...` | `https://www.ignou.ac.in/schools/school-of-humanities` | Legacy path 404s after Samarth CMS migration; enforces HTTPS. |

---

## 4. Technical Safeguards & Invariants Check

| Safeguard Verification Item | Expected / Mandated Value | Actual On-Disk Value | Verification Result |
|:---|:---|:---|:---:|
| **Candidate Output Hash** | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | **MATCH (VERIFIED)** |
| **Extension Candidate Hash** | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | **MATCH (VERIFIED)** |
| **Reference Video Hash** | `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8` | `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8` | **MATCH (VERIFIED)** |
| **Production Lexicon Route** | `isl_namaste_godl_v1` | `isl_namaste_godl_v1` in `keyframe_registry.js` & `isl_translator.js` | **ISOLATED (VERIFIED)** |
| **Candidate Auto-Promotion** | Excluded from default clips | `isLinguisticISL: false`, `status: "experimental_awaiting_validation"` | **QUARANTINED (VERIFIED)** |
| **Reference MP4 in Extension** | Strictly prohibited | Not present in `extension/assets/` | **EXCLUDED (VERIFIED)** |
| **Redistribution Rights** | Explicitly marked unresolved | Marked unresolved in `ASSET_LICENSES.md` & `M3_22_OWNER_APPROVAL_SHEET.md` | **PRESERVED (VERIFIED)** |

---

## 5. Execution Gate Confirmation

```
================================================================================
M3.23 OUTREACH READINESS GATE STATUS
================================================================================
System Execution Mode:          DRY_RUN_ONLY
External Messages Sent:         0 (Zero)
External Forms Submitted:       0 (Zero)
Contacts Contacted:             0 (Zero)
Binary Files Shared:            0 (Zero)
Owner Authorization Executed:   NO (Awaiting explicit human signature)
Operational Gate Status:        LOCKED IN DRY_RUN_ONLY
Linguistic Validation Status:   HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD
================================================================================
```
