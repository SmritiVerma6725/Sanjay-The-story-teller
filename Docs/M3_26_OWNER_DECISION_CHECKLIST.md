# SignBridge M3.26 — Owner Decision Checklist

**Document Reference:** `Docs/M3_26_OWNER_DECISION_CHECKLIST.md`  
**Milestone:** SignBridge M3.26 — Independent Evidence Audit & Owner Approval Readiness  
**Presentation Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Current Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  

---

## 1. Owner Decision Framework & Governance Rules

This checklist provides the **SignBridge Project Owner** with an actionable, granular framework to review, selectively approve, or reject components of the reviewer outreach package.

### Mandatory Governance Principles:
1. **Decoupled Gates:** Approving recipients or drafts **DOES NOT** authorize message dispatch. Any outreach dispatch requires an independent, affirmative signature in Decision Gate 5.
2. **Granular Approval:** The project owner is free to approve verified institutions while excluding unverified or ambiguous ones.
3. **Conservative Default:** Any gate or checkbox left blank, undecided, or unsigned remains strictly **`WITHHELD / NOT APPROVED`**.
4. **Active System State:** **`REMAIN_IN_DRY_RUN (ACTIVE DEFAULT)`**. No emails can be sent, no contact forms submitted, and no external requests dispatched without explicit authorization.

---

## 2. Granular Decision Gates for Project Owner

```
====================================================================================================
PROJECT OWNER DECISION ACTION RECORD (M3.26)
====================================================================================================

Project Owner Name:         [ PENDING PROJECT OWNER REVIEW ]
Institutional Role:         [ PENDING ]
Decision Date:              [ UNCONFIRMED / UNSIGNED ]

----------------------------------------------------------------------------------------------------
GATE 1: RECIPIENT INSTITUTIONS & CONTACT CHANNELS (SELECT INDIVIDUALLY)
----------------------------------------------------------------------------------------------------
Audit summary for each proposed institutional recipient:

[ ] APPROVE  |  [ ] EXCLUDE  : TGT-001 — ISLRTC (Indian Sign Language Research & Training Centre)
    Contact: islrtcnewdelhi@gmail.com
    Status:  VERIFIED_ON_OFFICIAL_SITE (DOM line 503 on https://islrtc.nic.in/contact-us/)
    Routing: Central administrative desk; requests referral to senior certified interpreters.

[ ] APPROVE  |  [ ] EXCLUDE  : TGT-002 — NAD India (National Association of the Deaf)
    Contact: secretary@nadindia.org (Proposed replacement for unlisted Gmail)
    Status:  PROPOSED_FOR_OWNER_APPROVAL (DOM line 891 on https://nadindia.org/Contact)
    Routing: Direct executive leadership desk of the General Secretary.

[ ] APPROVE  |  [ ] EXCLUDE  : TGT-003 — AIFD (All India Federation of the Deaf)
    Contact: aifdeaf@gmail.com (Proposed replacement on active official domain)
    Status:  VERIFIED_ON_ACTIVE_DOMAIN (HTML line 644 on https://aifdeaf.org/contact-us/)
    Routing: Central Delhi secretariat desk; requests referral to ISL training wing.

[ ] APPROVE  |  [ ] EXCLUDE  : TGT-004 — DEF (Deaf Enabled Foundation)
    Contact: info@def.org.in
    Status:  VERIFIED_ON_OFFICIAL_SITE (DOM line 638 on https://def.org.in/contact/)
    Routing: Central Secunderabad office; requests referral to certified trainers.

[ ] APPROVE  |  [ ] EXCLUDE  : TGT-005 — IGNOU School of Humanities (SOH)
    Contact: soh@ignou.ac.in
    Status:  NEEDS_OWNER_ROUTING_REVIEW (Legacy page 404s; address absent from saved homepage DOM)
    Routing: Director's desk; requires forwarding request to DISLI coordinator / linguists.
    Note:    Recommendation is to EXCLUDE from initial wave or require internal forwarding request.

----------------------------------------------------------------------------------------------------
GATE 2: REVIEW INVITATION DRAFTS (SELECT INDIVIDUALLY)
----------------------------------------------------------------------------------------------------
Full verbatim texts are available in Docs/M3_25_OWNER_DECISION_PACKAGE.md (Section 3).
All drafts include standardized inspection phrasing:
"A side-by-side comparison between the dictionary reference video and a 3D avatar within a local Chrome studio (no video is attached to this email)."

[ ] APPROVE  |  [ ] REVISE  : Draft 1 — Certified ISL Interpreters & Trainers (TGT-001, TGT-004)
    Covers: Experimental status, local Chrome studio, Y-Bot rig facial limits, voluntary terms.

[ ] APPROVE  |  [ ] REVISE  : Draft 2 — Deaf Native Signers & Deaf Community Leaders (TGT-002, TGT-003)
    Covers: Deaf community authority, voluntary feedback, pseudonymous review, rig disclosures.

[ ] APPROVE  |  [ ] REVISE  : Draft 3 — Academic ISL Linguists & Phonologists (TGT-005)
    Covers: 5-parameter phonological breakdown (DEZ, TAB, ORI, SIG, NMM), anomaly frame intervals.

----------------------------------------------------------------------------------------------------
GATE 3: OUTREACH ROLLOUT STRATEGY (SELECT ONE)
----------------------------------------------------------------------------------------------------
[ ] OPTION A (RECOMMENDED): Staged Outreach Wave
    Initial wave restricted to TGT-001 (ISLRTC) and TGT-004 (DEF) only.
    TGT-002, TGT-003, and TGT-005 deferred until initial institutional response and workflow validation.

[ ] OPTION B: Simultaneous Outreach
    Contact all approved recipients in Gate 1 concurrently.

[ ] OPTION C: Custom Rollout Scope (Specify Below):
    ____________________________________________________________________________________________

----------------------------------------------------------------------------------------------------
GATE 4: ACKNOWLEDGEMENT OF UNRESOLVED REFERENCE VIDEO LICENSING
----------------------------------------------------------------------------------------------------
Confirm understanding that redistribution rights for ISLRTC_Namaste_sample.mp4 remain UNRESOLVED.
No video files may be attached to emails, hosted in the cloud, or bundled in public web extensions.
Reviewers must inspect the video locally in their private Chrome studio instance.

[ ] ACKNOWLEDGED & ACCEPTED  |  [ ] NOT ACCEPTED / REQUIRES LEGAL REVIEW

----------------------------------------------------------------------------------------------------
GATE 5: INDEPENDENT MESSAGE DISPATCH AUTHORIZATION (CRITICAL SAFETY GATE)
----------------------------------------------------------------------------------------------------
Authorizing Gates 1 through 4 prepares the outreach package but DOES NOT authorize sending messages.
Any live electronic dispatch requires affirmative selection of AUTHORIZE_LIVE_DISPATCH below.

[X] REMAIN_IN_DRY_RUN (ACTIVE DEFAULT)
    Zero messages will be sent. The repository remains in dry-run mode.

[ ] AUTHORIZE_LIVE_DISPATCH
    Authorizes sending approved messages to approved recipients under selected rollout scope.
    (Requires explicit written signature and date below).

----------------------------------------------------------------------------------------------------
PROJECT OWNER SIGNATURE BLOCK
----------------------------------------------------------------------------------------------------
Owner Decision Notes / Instructions:
____________________________________________________________________________________________________
____________________________________________________________________________________________________

Owner Signature:            ____________________________________________________
Signature Date:             ____________________________________________________
Active Milestone Status:    DRY_RUN_ONLY (Awaiting owner signature)
====================================================================================================
```

---

## 3. Recommended Action Plan for Project Owner

1. **Gate 1:** Approve **TGT-001** and **TGT-004** (official-site publication verified). Approve **TGT-002** with replacement address `secretary@nadindia.org`. Approve **TGT-003** on active domain `https://aifdeaf.org/`. Mark **TGT-005** as `EXCLUDE` or request internal forwarding.
2. **Gate 2:** Approve **Drafts 1, 2, and 3** as drafted (all neutrality, disclosure, and standardized wording requirements are met).
3. **Gate 3:** Select **Option A (Staged Outreach)** to test responsiveness with statutory/training bodies before broader community outreach.
4. **Gate 4:** Formally **Acknowledge** unresolved licensing terms.
5. **Gate 5:** Select **`REMAIN_IN_DRY_RUN`** until ready to conduct actual live outreach.
