# SignBridge M3.26 — Evidence Gap Register

**Document Reference:** `Docs/M3_26_EVIDENCE_GAP_REGISTER.md`  
**Milestone:** SignBridge M3.26 — Independent Evidence Audit & Owner Approval Readiness  
**Audit Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance Mode:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  

---

## 1. Purpose & Scope

The Evidence Gap Register documents all identified discrepancies, missing verification artifacts, test invocation limitations, and routing ambiguities discovered during the independent M3.26 audit of M3.25 deliverables. Each gap is assigned a unique identifier, an objective severity rating, supporting evidence from the repository, and the concrete action required for resolution.

---

## 2. Summary Table of Identified Gaps

| Gap ID | Category | Description | Severity | Status | Action Required |
|:---:|:---|:---|:---:|:---:|:---|
| **GAP-01** | Test Execution | Test commands recorded in report (`pytest`, `python test_backend.py`) fail if run as documented due to environment/path requirements. | **MEDIUM** | **RESOLVED IN DOCS** | Document exact runner commands (`python -m unittest`, venv path and Cwd requirements). |
| **GAP-02** | Test Accounting | M3.25 test pass breakdown had accounting ambiguity (241 vs 238; 0-record ingestion audit counted in total; Browser Usability mislabeled). | **LOW** | **RECONCILED** | Provide explicit arithmetic reconciliation in M3.26 audit report. |
| **GAP-03** | Contact Verification | TGT-005 (IGNOU SOH) `soh@ignou.ac.in` is absent from saved DOM capture (`TGT-005_IGNOU_home.dom.html`); routing is to Director's desk. | **HIGH** | **OPEN (ROUTING REVIEW)** | Retain `NEEDS_OWNER_ROUTING_REVIEW`. Recommend requesting internal referral to DISLI coordinator if approved. |
| **GAP-04** | Evidence Preservation | TGT-003 (AIFD) has complete rendered HTML (`137,113` bytes) confirming `aifdeaf@gmail.com`, but lacks a companion PNG screenshot. | **LOW** | **DOCUMENTED** | Document HTML-only evidence capture; capture PNG in next browser session if desired. |
| **GAP-05** | Legal / Licensing | Reference MP4 redistribution rights remain `UNRESOLVED`; third-party repository labels are not authoritative. | **HIGH** | **ISOLATED / QUARANTINED** | Maintain strict prohibition against video attachment or external hosting. Enforce local-only studio review. |
| **GAP-06** | Governance Controls | M3.25 Gate 1 grouped all 5 recipients into an all-or-nothing checkbox; did not support selective approval. | **MEDIUM** | **RESOLVED IN M3.26** | Provide granular per-target checkboxes in M3.26 Owner Decision Checklist. |
| **GAP-07** | Avatar Limitation | Current Y-Bot avatar has no facial bones or blendshapes, preventing evaluation of ISL facial markers. | **HIGH** | **DISCLOSED IN DRAFTS** | All drafts instruct evaluators to mark facial expressions as `NOT ASSESSABLE`. |

---

## 3. Detailed Gap Records

### GAP-01: Discrepancy in Automated Test Invocations
- **Severity:** `MEDIUM`
- **Category:** Test Environment & Execution
- **Finding:**
  1. The M3.25 report listed `pytest tools/isl_motion_extraction/tests/test_outreach_governance.py`. On the host environment, `pytest` is not installed on the system PATH, producing `CommandNotFoundException` (exit code 1). Tests must be run via `python -m unittest`.
  2. The M3.25 report listed `python signbridge-backend/test_backend.py`. Running this from workspace root fails with `ModuleNotFoundError: No module named 'fastapi'` because backend dependencies are isolated in `signbridge-backend\.venv`. Furthermore, `test_backend.py` loads `test_speech_sample.wav` via a relative path, requiring the command's working directory (`Cwd`) to be `signbridge-backend`.
- **Evidence:**
  - `pytest tools/isl_motion_extraction/tests/test_outreach_governance.py` -> Exit Code 1 (`The term 'pytest' is not recognized`).
  - `python signbridge-backend/test_backend.py` (from root) -> Exit Code 1 (`ModuleNotFoundError: No module named 'fastapi'`).
  - `.venv\Scripts\python.exe test_backend.py` (from `c:\AmazonMlChallenge\signbridge-backend`) -> Exit Code 0 (8/8 tests passed).
- **Resolution:**
  - Document the exact working directory and interpreter invocation in `Docs/M3_26_INDEPENDENT_AUDIT.md`.
  - Ensure automation scripts and execution reports specify the virtual environment interpreter explicitly.

---

### GAP-02: Test Count Accounting & Reporting Ambiguity
- **Severity:** `LOW`
- **Category:** Verification Reporting
- **Finding:**
  1. In the M3.25 summary prompt, the total was stated as 241/241, breaking down into: Outreach governance: 15, Motion extraction: 59, Readiness preflight: 27, Ingestion audit: 0 records, Speech backend: 8, Chrome runner: 132.
  2. However, running `python -m unittest discover -s tools/isl_motion_extraction/tests` runs **59 tests total**, which *already includes* `test_outreach_governance.py` (15 tests), along with `test_retargeting.py` (13), `test_review_readiness.py` (12), `test_review_roundtrip.py` (10), and `test_review_validator.py` (9).
  3. The separate browser usability suite (`test_browser_usability.py`) contains **15 checks**, which matches the number "15" that was mislabeled as "Outreach governance: 15" in the bullet list.
  4. The ingestion directory audit (`validate_review_record.py`) scanned **0 records** and exited with code 0. Counting "0 records" as an additive test pass in the headline math was confusing.
- **Evidence:**
  - True mathematical sum of automated checks:
    - 59 (Unittest Discovery Suite)
    - 15 (Browser Usability Suite)
    - 27 (Readiness Diagnostic Preflight)
    - 8 (Speech Backend Suite)
    - 132 (Chrome In-Engine Test Runner)
    - **Total: 59 + 15 + 27 + 8 + 132 = 241 automated checks passed.**
- **Resolution:**
  - Fully clarify the exact test composition in `Docs/M3_26_INDEPENDENT_AUDIT.md`.
  - Disentangle directory audit status (0 records = 0 reviews fabricated) from the unit/integration check count.

---

### GAP-03: TGT-005 (IGNOU SOH) Contact Evidence & Routing Ambiguity
- **Severity:** `HIGH`
- **Category:** Contact Channel & Routing Verification
- **Finding:**
  1. The legacy departmental URL (`https://www.ignou.ac.in/schools/school-of-humanities` / `/ignou/aboutignou/school/soh/introduction`) returned HTTP 404 following IGNOU's migration to the Samarth e-Gov portal.
  2. The retained DOM evidence file `Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.dom.html` contains the university homepage, which does *not* contain the email address `soh@ignou.ac.in` on the page itself.
  3. Even if verified, `soh@ignou.ac.in` routes to the general office of the Director of the School of Humanities, rather than directly to the DISLI (Diploma in Indian Sign Language Interpretation) coordinator or ISL faculty.
- **Evidence:**
  - `grep` on `TGT-005_IGNOU_home.dom.html` returned zero matches for `soh@ignou.ac.in`.
  - `verification_summary.json` notes: `"status": "NEEDS_OWNER_REVIEW"`, `"verified_url": "https://www.ignou.ac.in/"`.
- **Resolution:**
  - Retain `NEEDS_OWNER_ROUTING_REVIEW`.
  - Ensure the owner checklist presents the option to exclude TGT-005, or include Draft 3 with explicit request to forward to the DISLI coordinator.

---

### GAP-04: TGT-003 (AIFD) Missing PNG Screenshot Capture
- **Severity:** `LOW`
- **Category:** Evidence Preservation
- **Finding:**
  1. During M3.23 Chrome verification, the legacy domain `aifd.org.in` failed DNS lookup (`[Errno 11001] getaddrinfo failed`).
  2. The active official domain `https://aifdeaf.org/contact-us/` was resolved and captured as rendered HTML (`TGT-003_aifdeaf_contact.html`, 137,113 bytes), which confirms `aifdeaf@gmail.com` at line 644.
  3. However, no companion PNG screenshot was written to `Docs/evidence/m3_23_chrome_verification/` for TGT-003 (unlike TGT-001, TGT-002, TGT-004, and TGT-005).
- **Evidence:**
  - Directory listing of `Docs/evidence/m3_23_chrome_verification/` contains `TGT-003_aifdeaf_contact.html` (137,113 bytes) but no `TGT-003*.png`.
  - `verification_summary.json` records `"screenshot_path": "None (DNS Failure)"`.
- **Resolution:**
  - Classify AIFD publication as `VERIFIED_FROM_ARTIFACT` (HTML DOM), but note the missing visual screenshot in the gap register.
  - A visual screenshot can be re-captured in a future verification phase if desired by the owner.

---

### GAP-05: Unresolved Redistribution Rights for Reference Video
- **Severity:** `HIGH`
- **Category:** Legal & Licensing Compliance
- **Finding:**
  1. The reference video `ISLRTC_Namaste_sample.mp4` (SHA-256 `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8`) was sourced from ISLRTC dictionary documentation.
  2. Public distribution rights remain **UNRESOLVED**. Third-party repository tags (e.g. GitHub repo licenses) do not grant legal distribution rights for government-sourced lexical media.
- **Evidence:**
  - `Docs/M3_25_OWNER_DECISION_PACKAGE.md` Section 5 explicitly records licensing as `UNRESOLVED`.
- **Resolution:**
  - Enforce zero distribution: no email attachments, no cloud links, no inclusion in public extension bundles.
  - Evaluation remains strictly localized to `localhost` in the reviewer's private Chrome studio.
  - Owner must explicitly sign Decision Gate 4 acknowledging this status.

---

### GAP-06: All-or-Nothing Decision Gate 1 in M3.25
- **Severity:** `MEDIUM`
- **Category:** Owner Decision Workflow
- **Finding:**
  1. The M3.25 owner approval sheet had a single `[ ] PENDING — Approve proposed recipient contact channels` checkbox covering all 5 targets together.
  2. This prevented the owner from approving verified targets (e.g., TGT-001, TGT-004) while excluding unverified or ambiguous targets (e.g., TGT-005).
- **Evidence:**
  - `Docs/M3_25_OWNER_DECISION_PACKAGE.md` lines 201-212.
- **Resolution:**
  - Created `Docs/M3_26_OWNER_DECISION_CHECKLIST.md` providing independent per-target checkboxes for each of the 5 institutions.

---

### GAP-07: Avatar Rig Physical Limitations (Rigid Face)
- **Severity:** `HIGH`
- **Category:** Linguistic Evaluation Fidelity
- **Finding:**
  1. Adobe Mixamo Y-Bot has a rigid metallic mesh without facial bones or blendshapes.
  2. Indian Sign Language incorporates non-manual markers (NMM) including facial expressions and mouth morphemes. The avatar cannot articulately display these features.
- **Evidence:**
  - `preview_mocap.html` displays: `"Non-manual markers (facial expressions) cannot be assessed on this rig."`
  - In-engine test: `avatar player articulates real Namaste sign with bilateral prayer pose and head nod`.
- **Resolution:**
  - All invitation drafts explicitly state this limitation.
  - Evaluators are instructed in the worksheet to mark facial expressions as `NOT ASSESSABLE ON CURRENT RIG`, preventing false negative ratings on articulatory parameters the avatar cannot express.
