# SignBridge Controlled Pilot — Incident Report Template

**Document Reference:** `Docs/M4_STAGE_4_PILOT_PACKAGE/INCIDENT_REPORT_TEMPLATE.md`  
**Milestone:** SignBridge M4 Stage 4 (Controlled Pilot Preparation)  
**Governance State:** `DRY_RUN_ONLY — NOT_AUTHORIZED — TEMPLATE`  

---

## 1. Incident Overview
* **Incident ID:** `[ INC-YYYYMMDD-### ]`
* **Date & Timestamp:** `[ YYYY-MM-DD HH:MM:SS UTC ]`
* **Participant ID:** `[ e.g. P-001 (or N/A if technical pre-flight) ]`
* **Session Step:** `[ e.g. Scenario B / Tab Navigation / Shutdown ]`
* **Reporting Facilitator:** `[ Facilitator Name ]`

---

## 2. Severity Classification
Select one:
- [ ] **LOW:** Minor cosmetic UI glitch; no functional disruption; test continued normally.
- [ ] **MEDIUM:** Transient speech recognition delay or dropped audio chunk; recovered automatically.
- [ ] **HIGH:** Browser tab frozen; uncaught exception in console; session paused to restart backend.
- [ ] **CRITICAL:** Visual rendering artifact causing offensive/confusing gesture; participant distress; memory leak; session **aborted immediately**.

---

## 3. Incident Description
### Observed Behavior:
*(Describe exactly what occurred on screen or in the browser)*

### Expected Behavior:
*(What was supposed to occur according to the protocol)*

### System Logs & Error Messages:
```
[Browser Console / Python Backend Traceback]
```

---

## 4. Remediation & Rollback Action
- [ ] Session Aborted immediately: `[ YES / NO ]`
- [ ] Participant reassured and debriefed: `[ YES / NO ]`
- [ ] Browser and backend restarted: `[ YES / NO ]`
- [ ] Reverted to production baseline `isl_namaste_godl_v1`: `[ YES / NO ]`
- [ ] Bug logged in project repository: `[ Issue # or File ]`

---

## 5. Sign-Off
* **Facilitator Signature:** ____________________  
* **Date:** ____________________  
* **Project Owner Review:** `[ PENDING / REVIEWED / RESOLVED ]`
