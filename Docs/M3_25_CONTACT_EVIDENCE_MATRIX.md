# SignBridge M3.25 — Contact Evidence & Verification Matrix

**Document Reference:** `Docs/M3_25_CONTACT_EVIDENCE_MATRIX.md`  
**Milestone:** SignBridge M3.25 — Final Outreach Readiness Audit & Owner Decision Package  
**Audit Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Execution Environment:** Chrome Headless CDP / TLS 1.3 / Local File Provenance  
**Current Governance State:** **`DRY_RUN_ONLY — PENDING EXPLICIT PROJECT-OWNER AUTHORIZATION`**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Active in Chrome extension & unchanged)  
**Evaluated Motion Candidate:** `isl_namaste_mocap_candidate_v1` (Quarantined in isolated experimental assets)  

---

## 1. Executive Summary & Verification Methodology

In strict compliance with M3.25 standards, every prospective outreach target is evaluated across **four separate, non-fungible verification dimensions**:

1. **Official-Site Publication Verified:** Is the specific email address visibly published on the current, active official website of the institution?
2. **Organizational Relevance Established:** Does the institution's official remit and operational scope make it a plausible, authoritative recipient for an Indian Sign Language (ISL) review request?
3. **Recipient Routing Established:** Does the email address route directly to a qualified ISL specialist / Deaf leader, or to a general administrative office requiring internal forwarding?
4. **Inbox Deliverability Tested:** Has the email address been verified as active, monitored, and free of blocking filters? (*In accordance with the dry-run safety gate, this is strictly `NOT_TESTED` for all targets.*)

Evidence is derived solely from rendered browser DOM dumps and network captures. Search engine snippets, directory aggregators, and unverified project notes are rejected as proof.

---

## 2. Four-Dimensional Institutional Verification Matrix

| Target ID | Institution Name | Proposed Contact Address | Official Page URL | 1. Official Publication | 2. Org Relevance | 3. Recipient Routing | 4. Deliverability | Current Readiness Status | Owner Decision | Dispatch Status |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **TGT-001** | **ISLRTC** | `islrtcnewdelhi@gmail.com` | `https://islrtc.nic.in/contact-us/` | **VERIFIED** | **ESTABLISHED** | **ADMIN DESK** | **NOT_TESTED** | **`VERIFIED_ON_OFFICIAL_SITE`** | `[ ] PENDING` | **`NOT_AUTHORIZED`** |
| **TGT-002** | **NAD India** | `secretary@nadindia.org` | `https://nadindia.org/Contact` | **VERIFIED** | **ESTABLISHED** | **EXECUTIVE ROUTING** | **NOT_TESTED** | **`PROPOSED_FOR_OWNER_APPROVAL`** | `[ ] PENDING` | **`NOT_AUTHORIZED`** |
| **TGT-003** | **AIFD** | `aifdeaf@gmail.com` | `https://aifdeaf.org/contact-us/` | **VERIFIED** | **ESTABLISHED** | **ADMIN DESK** | **NOT_TESTED** | **`VERIFIED_ON_ACTIVE_DOMAIN`** | `[ ] PENDING` | **`NOT_AUTHORIZED`** |
| **TGT-004** | **DEF** | `info@def.org.in` | `https://def.org.in/contact/` | **VERIFIED** | **ESTABLISHED** | **ADMIN DESK** | **NOT_TESTED** | **`VERIFIED_ON_OFFICIAL_SITE`** | `[ ] PENDING` | **`NOT_AUTHORIZED`** |
| **TGT-005** | **IGNOU SOH** | `soh@ignou.ac.in` | `https://www.ignou.ac.in/schools/school-of-humanities` | **UNVERIFIED (Page 404)** | **ESTABLISHED** | **DIRECTOR DESK** | **NOT_TESTED** | **`NEEDS_OWNER_ROUTING_REVIEW`** | `[ ] PENDING` | **`NOT_AUTHORIZED`** |

*Notice: Website publication confirms presence on a public webpage, but NEVER establishes that an inbox is active, monitored, or deliverable. Testing deliverability via electronic messages is strictly prohibited under DRY_RUN_ONLY.*

---

## 3. Detailed Institution Evidence & Verification Profiles

### Target TGT-001: Indian Sign Language Research and Training Centre (ISLRTC)
- **Institution Name:** Indian Sign Language Research and Training Centre (ISLRTC)
- **Category:** Statutory Authority / Certified Interpreters (Autonomous body under DEPwD, MSJE, Govt of India)
- **Proposed Contact Address:** `islrtcnewdelhi@gmail.com`
- **Official Portal URL:** `https://islrtc.nic.in/contact-us/`
- **Page Title:** `Contact Us | Indian Sign Language Research and Training Center ,Government of India | India`
- **Observation Date:** October 20, 2026
- **Evidence Files:**
  - DOM Dump: [`Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.dom.html) (Line 503)
  - Page Screenshot: [`Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.png)
- **Granular Four-Dimensional Assessment:**
  1. *Official Publication:* **VERIFIED.** Line 503 of the rendered DOM explicitly publishes `Email :&nbsp;islrtcnewdelhi[at]gmail[dot]com` (standard NIC anti-scraping obfuscation for `islrtcnewdelhi@gmail.com`).
  2. *Organizational Relevance:* **ESTABLISHED (Authoritative).** ISLRTC is the national statutory body standardizing ISL, creator of ISL Dictionary Vol 1 (source of Word #0001 NAMASTE), and national certifier of ISL interpreters (DISLI/DTISL).
  3. *Recipient Routing:* **ADMINISTRATIVE DESK.** The address routes to the central Delhi administrative secretariat. Initial outreach should request routing to certified interpreter evaluators.
  4. *Inbox Deliverability:* **NOT_TESTED.** No messages sent.
- **Assigned Draft:** Draft 1 (Certified ISL Interpreters & Statutory Bodies)
- **Readiness Classification:** **`VERIFIED_ON_OFFICIAL_SITE`**

---

### Target TGT-002: National Association of the Deaf (NAD) India
- **Institution Name:** National Association of the Deaf (NAD) India
- **Category:** Deaf Native Signers & Deaf Community Advocacy Leaders
- **Proposed Contact Address:** `secretary@nadindia.org` *(Replaced unlisted `nadindia@gmail.com`)*
- **Official Portal URL:** `https://nadindia.org/Contact` *(Case-sensitive route; capital 'C')*
- **Page Title:** `Contact Us - National Association of the Deaf - National Association of the Deaf, India`
- **Observation Date:** October 20, 2026
- **Evidence Files:**
  - DOM Dump: [`Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.dom.html) (Lines 888–893)
  - Page Screenshot: [`Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.png)
- **Granular Four-Dimensional Assessment:**
  1. *Official Publication:* **VERIFIED.** Line 891 of the rendered DOM visibly publishes `<a href="mailto:secretary@nadindia.org">secretary@nadindia.org</a>`. The previously proposed `nadindia@gmail.com` is completely unlisted on the official domain.
  2. *Organizational Relevance:* **ESTABLISHED (Premier Advocacy).** NAD India is the apex organization led by Deaf individuals in India, fighting for ISL recognition under the RPwD Act 2016. Engaging NAD leadership ensures Deaf-native community ownership.
  3. *Recipient Routing:* **EXECUTIVE LEADERSHIP ROUTING.** Routes directly to the General Secretary / executive desk of the association.
  4. *Inbox Deliverability:* **NOT_TESTED.** No messages sent.
- **Outstanding Uncertainties:** Phone field on website contains an unconfigured template placeholder `(123) 456-7890`, though the SMS number `9810234165` is valid.
- **Assigned Draft:** Draft 2 (Deaf Native Signers & Deaf Community Leaders)
- **Readiness Classification:** **`PROPOSED_FOR_OWNER_APPROVAL`**

---

### Target TGT-003: All India Federation of the Deaf (AIFD)
- **Institution Name:** All India Federation of the Deaf (AIFD)
- **Category:** Deaf Federation / Community Advocates (Est. 1955)
- **Proposed Contact Address:** `aifdeaf@gmail.com` *(Replaced unverified `aifd1955@yahoo.co.in`)*
- **Official Portal URL:** `https://aifdeaf.org/contact-us/` *(Active official domain; `aifd.org.in` is defunct)*
- **Page Title:** `Contact Us – All India Federation of the Deaf`
- **Observation Date:** October 20, 2026
- **Evidence Files:**
  - Rendered HTML: [`Docs/evidence/m3_23_chrome_verification/TGT-003_aifdeaf_contact.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-003_aifdeaf_contact.html) (Lines 635–648)
  - DNS Failure Record for `aifd.org.in`: `[Errno 11001] getaddrinfo failed`
- **Granular Four-Dimensional Assessment:**
  1. *Official Publication:* **VERIFIED ON ACTIVE DOMAIN.** Line 644 of the official page HTML explicitly displays `aifdeaf@gmail.com / aifddeaf@yahoo.com` at `12-13, Shaheed Jeet Singh Marg, Qutab Institutional Area, New Delhi – 110067` alongside WhatsApp `+91 76776 99977`.
  2. *Organizational Relevance:* **ESTABLISHED (Historic Federation).** Founded in 1955, AIFD coordinates state deaf associations across 13+ states (AAD, BrAD, GAD, TNFD, etc.) and runs active ISL training workshops and national ISL conferences.
  3. *Recipient Routing:* **CENTRAL SECRETARIAT DESK.** The address routes to the central Delhi office; outreach should request forwarding to the Sign Language Training & Workshop wing.
  4. *Inbox Deliverability:* **NOT_TESTED.** No messages sent.
- **Assigned Draft:** Draft 2 (Deaf Native Signers & Deaf Community Leaders)
- **Readiness Classification:** **`VERIFIED_ON_ACTIVE_DOMAIN`** *(Subject to owner sign-off on domain update)*

---

### Target TGT-004: Deaf Enabled Foundation (DEF)
- **Institution Name:** Deaf Enabled Foundation (DEF)
- **Category:** Community Sign Interpreters & Accessibility Trainers
- **Proposed Contact Address:** `info@def.org.in`
- **Official Portal URL:** `https://def.org.in/contact/` *(Trailing slash required)*
- **Page Title:** `Contact Us – Deaf Enabled Foundation`
- **Observation Date:** October 20, 2026
- **Evidence Files:**
  - Rendered DOM: [`Docs/evidence/m3_23_chrome_verification/TGT-004_DEF_contact.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-004_DEF_contact.html) (Line 638)
  - Page Screenshot: [`Docs/evidence/m3_23_chrome_verification/TGT-004_def.org.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-004_def.org.png)
- **Granular Four-Dimensional Assessment:**
  1. *Official Publication:* **VERIFIED.** Line 638 of the rendered DOM visibly publishes `<div class="boc_list_item_text normal">info@def.org.in</div>` with head office address: `7th floor and 704, Navketan Complex, S.D. Road, Secunderabad, Telangana – 500 003` and mobile `+91 97033 81112`.
  2. *Organizational Relevance:* **ESTABLISHED (Community Sign Education).** Major community sign organization delivering formal interpreter education, accessible mobile media, and ISL skill programs.
  3. *Recipient Routing:* **CENTRAL INBOX.** Routes to the Secunderabad administrative team; initial message requests referral to senior certified interpreters.
  4. *Inbox Deliverability:* **NOT_TESTED.** No messages sent.
- **Assigned Draft:** Draft 1 (Certified ISL Interpreters & Statutory Bodies)
- **Readiness Classification:** **`VERIFIED_ON_OFFICIAL_SITE`**

---

### Target TGT-005: IGNOU School of Humanities (SOH)
- **Institution Name:** Indira Gandhi National Open University (IGNOU) — School of Humanities (SOH)
- **Category:** Academic Sign Language Linguists (DISLI Curriculum)
- **Proposed Contact Address:** `soh@ignou.ac.in`
- **Official Portal URL:** `https://www.ignou.ac.in/schools/school-of-humanities` *(Samarth eGov CMS)*
- **Page Title:** `Indira Gandhi National Open University (IGNOU)`
- **Observation Date:** October 20, 2026
- **Evidence Files:**
  - Portal Landing Snapshot: [`Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.png)
  - Portal DOM Dump: [`Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.dom.html)
- **Granular Four-Dimensional Assessment:**
  1. *Official Publication:* **UNVERIFIED ON SPECIFIC PAGE.** Legacy URL (`/ignou/aboutignou/school/soh/introduction`) returned HTTP 404 following portal migration. While `soh@ignou.ac.in` is confirmed in internal university directories, it is not verified on a currently functional contact subpage.
  2. *Organizational Relevance:* **ESTABLISHED (Academic DISLI Program).** SOH established the Diploma in Indian Sign Language Interpretation (DISLI) in formal academic collaboration with ISLRTC, housing academic faculty in sign phonology.
  3. *Recipient Routing:* **DIRECTOR'S OFFICE (NOT DIRECT TO DISLI).** `soh@ignou.ac.in` reaches the Director of the School of Humanities. It does not route directly to the DISLI Program Coordinator or individual sign linguistics faculty.
  4. *Inbox Deliverability:* **NOT_TESTED.** No messages sent.
- **Routing Recommendation:** If outreach is approved by the project owner, the invitation must explicitly ask the Director's office to forward the evaluation request to the DISLI Program Coordinator or designated ISL faculty.
- **Assigned Draft:** Draft 3 (Academic Sign Language Linguists & Phonologists)
- **Readiness Classification:** **`NEEDS_OWNER_ROUTING_REVIEW`**

---

## 4. Summary of Contact Readiness Classifications

```
================================================================================
M3.25 CONTACT READINESS CLASSIFICATION SUMMARY
================================================================================
Total Targets Evaluated:                 5 (All 5 retained in intended scope)
Verified on Official Live Site:          2 (TGT-001 ISLRTC, TGT-004 DEF)
Verified on Active Alternative Domain:   1 (TGT-003 AIFD)
Proposed Replacement Awaiting Sign-off:  1 (TGT-002 NAD India)
Needs Owner Routing Review:              1 (TGT-005 IGNOU SOH)
Inbox Deliverability Tested:             0 (0% — STRICTLY PROHIBITED IN DRY RUN)
Overall Milestone Gate:                  OUTREACH PENDING EXPLICIT AUTHORIZATION
================================================================================
```
