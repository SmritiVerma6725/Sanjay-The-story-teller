# SignBridge M3.20 — External Reviewer Outreach Tracker

**Document Reference:** `Docs/M3_20_REVIEW_OUTREACH_TRACKER.md`  
**Milestone:** SignBridge M3.20 — Reviewer Outreach Execution & Response Tracking  
**Target Candidate:** `isl_namaste_mocap_candidate_v1`  
**Candidate SHA-256:** `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46`  
**Reference Video SHA-256:** `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8`  
**Governance Status:** **HUMAN REVIEW PENDING — OUTREACH PENDING AUTHORIZATION**  
**Active Production Baseline:** `isl_namaste_godl_v1` (Active in extension)  

---

## 1. Outreach Governance & Non-Spamming Policy

> [!IMPORTANT]
> **ANTI-FABRICATION & EXPLICIT AUTHORIZATION POLICY:**  
> 1. **Zero Unauthorized Outreach:** No electronic messages, form submissions, or external inquiries may be transmitted without the explicit authorization of the SignBridge project owner.
> 2. **Public Institutional Contacts Only:** Prospective contacts are restricted exclusively to publicly published organizational desks and official institutional channels. No personal emails, unverified phone numbers, or private social media accounts may be compiled or contacted.
> 3. **Accurate Tracking Without Pre-Commitment:** No institution or individual shall be recorded as a "Reviewer" or "Participant" until they have explicitly agreed to review the candidate.
> 4. **No Synthesized Responses:** If no responses or review records have been received, the status must remain strictly reported as **`Awaiting Outreach Authorization`** or **`Awaiting Responses`**.

---

## 2. Institutional Outreach Directory & Tracking Table

The following tracking table identifies verified public institutional bodies for prospective consultation. **All entries currently await explicit project-owner authorization prior to dispatch.**

| Entry ID | Target Institution / Body | Institutional Category | Publicly Verified Contact Channel | Date Contacted | Authorization Status | Response Status | Disclosed Qualifications | Next Action |
|---|---|---|---|---|---|---|---|---|
| **OUT-001** | **ISLRTC (Indian Sign Language Research and Training Centre)** | Autonomous Govt Authority (DEPwD, MSJE) | `islrtcnewdelhi@gmail.com`<br>Website: `islrtc.nic.in` | *Not Contacted* | **Pending Project Owner Authorization** | **No Outreach Dispatched** | *None (Pending)* | Await project owner approval before dispatching Draft A. |
| **OUT-002** | **National Association of the Deaf (NAD) India** | Deaf-Led National Advocacy Apex Body | `nadindia@gmail.com`<br>Website: `nadindia.org` | *Not Contacted* | **Pending Project Owner Authorization** | **No Outreach Dispatched** | *None (Pending)* | Await project owner approval before dispatching Draft B. |
| **OUT-003** | **All India Federation of the Deaf (AIFD)** | National Deaf Federation (Est. 1955) | `aifd1955@yahoo.co.in`<br>Website: `aifd.org.in` | *Not Contacted* | **Pending Project Owner Authorization** | **No Outreach Dispatched** | *None (Pending)* | Await project owner approval before dispatching Draft B. |
| **OUT-004** | **Deaf Enabled Foundation (DEF)** | Community Sign Organization & Training | `info@def.org.in`<br>Website: `def.org.in` | *Not Contacted* | **Pending Project Owner Authorization** | **No Outreach Dispatched** | *None (Pending)* | Await project owner approval before dispatching Draft A. |
| **OUT-005** | **IGNOU School of Humanities (DISLI Program)** | Academic Interpreter Training Authority | `soh@ignou.ac.in`<br>Website: `ignou.ac.in` | *Not Contacted* | **Pending Project Owner Authorization** | **No Outreach Dispatched** | *None (Pending)* | Await project owner approval before dispatching Draft C. |

---

## 3. Reviewer Response Intake Log

*This log records confirmed reviewer responses and formal submissions. It remains empty until genuine review records are validated.*

| Log ID | Date Received | Reviewer Identifier / Pseudonym | Disclosed Fluency / Role | Submission Format | Candidate SHA-256 Bound? | Ingestion Validator Status | Assigned Decision Gate |
|---|---|---|---|---|---|---|---|
| *None* | *N/A* | *No responses received yet* | *N/A* | *N/A* | *N/A* | `Zero review records in storage` | `HUMAN REVIEW PENDING` |

---

## 4. Secure Feedback Intake & Verification Protocol

When an evaluator agrees to participate and completes an evaluation session, feedback must be processed according to the following read-only intake pipeline:

```
[Evaluator Completes Review in preview_mocap.html]
                        │
                        ▼
  [Clicks "⬇ Export Review JSON" in Review Studio]
                        │
                        ▼
[JSON File: ISL_Namaste_Review_<Reviewer>_<Date>.json]
                        │
                        ▼
[File Placed in tools/isl_motion_extraction/reviews/]
                        │
                        ▼
[Execute: python tools/isl_motion_extraction/validate_review_record.py]
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
[Valid Hash & Schema]        [Tampered / Mismatched]
          │                           │
          ▼                           ▼
 [Audit Log Updated]         [Rejected with Hard Error]
          │                           │
          ▼                           ▼
 [Evidence Ingested]         [Investigation Flagged]
```

### Verification Criteria:
1. **Schema Check:** Must match `signbridge_review_schema_v1.*`.
2. **Candidate Identity & Hash Check:** Must explicitly match candidate ID `isl_namaste_mocap_candidate_v1` and SHA-256 `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46`.
3. **Reference Video Hash Check:** Must bind to `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8`.
4. **Identity & Role Requirement:** Reviewer profile must contain a role declaration (or explicit voluntary pseudonym / anonymous designation) and session date.
5. **Rating Validity:** Ratings for Handshape, Location, Orientation, Movement, and Non-Manuals must adhere to categorical findings (`acceptable`, `minor_issue`, `unacceptable`, `not_assessable`).
6. **Read-Only Preservation:** The validator operates without rewriting, modifying, or deleting on-disk records.

---

## 5. Current Tracker Status Summary

```
================================================================================
OUTREACH TRACKER STATUS SUMMARY:
Total Prospective Institutional Targets:  5 (Public organizations identified)
Total Inquiries Authorized:               0
Total Inquiries Dispatched:               0
Total Responses Received:                 0
Total Validated Review Records:           0
Active Production Baseline:               isl_namaste_godl_v1 (Unchanged)
Candidate Governance Status:              experimental_awaiting_validation
================================================================================
```
