# SignBridge Controlled Pilot — Test Case Worksheet

**Document Reference:** `Docs/M4_STAGE_4_PILOT_PACKAGE/TEST_CASE_WORKSHEET.md`  
**Milestone:** SignBridge M4 Stage 4 (Controlled Pilot Preparation)  
**Governance State:** `DRY_RUN_ONLY — NOT_AUTHORIZED — DRAFT TEMPLATE`  

---

**Participant ID:** `[ e.g. P-001 ]`  
**Facilitator:** `[ Facilitator Name ]`  
**Certified Interpreter:** `[ Interpreter Name ]`  
**Session Date & Time:** `[ YYYY-MM-DD HH:MM ]`  
**Workstation / OS:** `[ Windows 10/11 / macOS / Ubuntu ]`  

---

## Evaluation Grid

| Test ID | Test Scenario | Input Speech / Action | Expected System Response | Participant Observed Outcome | Pass / Fail / Note |
|:---:|:---|:---|:---|:---|:---:|
| **TC-01** | **UI Launch & Docking** | User opens popup, clicks "Open 3D Avatar Display". | Avatar window opens; model loaded; status shows `BRIDGE: STANDBY`. | [ ] Window opened<br>[ ] Y-Bot rendered | `[ PASS / FAIL ]` |
| **TC-02** | **Capture Activation** | User clicks "Start Audio Capture" on active video tab. | Button turns red ("Stop Capture"); badge shows `CAPTURE: ACTIVE`. | [ ] Audio heard in speaker<br>[ ] Badge active | `[ PASS / FAIL ]` |
| **TC-03** | **Baseline Sign Articulation** | Video plays phrase containing `"Namaste"`. | Transcript displays `"Namaste"`; avatar performs bilateral prayer pose; green badge. | [ ] Gesture executed<br>[ ] Returned to rest | `[ PASS / FAIL ]` |
| **TC-04** | **Unanimated Word Handling** | Video plays phrase containing `"Thank you"`. | Transcript displays `"Thank you"`; badge shows awaiting review notice; neutral rest held. | [ ] No fake gestures<br>[ ] Status badge clear | `[ PASS / FAIL ]` |
| **TC-05** | **Out-of-Lexicon Handling** | Video plays phrase with technical jargon. | Unsupported words listed in telemetry; avatar holds neutral rest pose. | [ ] Words surfaced<br>[ ] No hallucinated sign | `[ PASS / FAIL ]` |
| **TC-06** | **Speech Pauses & Silence** | Video pauses audio for 5 seconds. | Latency remains $<50\text{ ms}$; status reports silence; avatar holds motionless rest. | [ ] No jitter/stutter<br>[ ] Rest maintained | `[ PASS / FAIL ]` |
| **TC-07** | **Session Termination** | User clicks "Stop Capture". | Audio track stops; avatar resets to neutral pose; status shows `CAPTURE: IDLE`. | [ ] Clean shutdown<br>[ ] Resources freed | `[ PASS / FAIL ]` |

---

## Facilitator Observational Notes
1. **User Confusion / Hesitation:**  
   *(Record any moments where participant paused or expressed confusion about buttons or status badges)*  
   `...`

2. **Perceived Latency & Synchronization:**  
   *(Record participant feedback regarding the timing between speech audio and avatar movement)*  
   `...`

3. **Unexpected Behaviors / Glitches:**  
   *(Record any rendering glitches, lag spikes, or unexpected status messages)*  
   `...`
