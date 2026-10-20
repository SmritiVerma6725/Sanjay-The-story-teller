# SignBridge Controlled Pilot — Privacy & Data Deletion Checklist

**Document Reference:** `Docs/M4_STAGE_4_PILOT_PACKAGE/PRIVACY_DATA_DELETION_CHECKLIST.md`  
**Milestone:** SignBridge M4 Stage 4 (Controlled Pilot Preparation)  
**Governance State:** `DRY_RUN_ONLY — NOT_AUTHORIZED — PRIVACY PROTOCOL`  

---

## 1. Localhost Isolation Verification (Pre-Session)
- [ ] Backend host verified bound to `127.0.0.1:8765` (`signbridge-backend/config.py`).
- [ ] Manifest permissions verified: Only `tabCapture`, `offscreen`, `activeTab`, `storage`, `scripting`.
- [ ] Ambient microphone access verified absent: `audioCapture` NOT present in manifest.
- [ ] Network traffic monitor confirmed: Zero outbound WAN traffic during active transcription.

---

## 2. In-Session Privacy Protections
- [ ] Only internal tab audio processed; no room microphones enabled.
- [ ] Transcripts held in volatile session memory (`chrome.storage.session`), never in persistent storage.
- [ ] Participant identifier is anonymized (e.g. `P-001`); zero PII (names, emails) collected in telemetry.

---

## 3. Post-Session Data Deletion Verification (Post-Session)
Execute immediately after each participant completes their session:

| Item | Storage Location | Deletion Action | Completed |
|:---|:---|:---|:---:|
| **Tab Audio Slices** | Chrome Offscreen RAM | Discarded automatically upon HTTP response. | [ ] |
| **Session Transcripts** | `chrome.storage.session` | Click "Clear Transcript" in popup; close browser. | [ ] |
| **Backend Memory** | Python RAM (`io.BytesIO`) | Terminate backend process (`Ctrl+C`). | [ ] |
| **Temporary Audio Dumps** | Local filesystem (`signbridge-backend/`) | Verify zero `.wav` or `.tmp` files created. | [ ] |
| **Facilitator Notes** | Anonymized worksheet | Stored in encrypted/locked local project folder. | [ ] |

---

## 4. Participant Withdrawal Procedure
If a participant exercises their right to withdraw:
1. Immediately stop audio capture and close avatar player.
2. In the presence of the participant and interpreter, execute the Post-Session Data Deletion steps above.
3. Mark participant record as `WITHDRAWN — ALL DATA PURGED`.
4. Destroy any handwritten notes or observational worksheets associated with the session.
