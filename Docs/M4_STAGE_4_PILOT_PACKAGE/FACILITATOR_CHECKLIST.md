# SignBridge Controlled Pilot — Facilitator Checklist

**Document Reference:** `Docs/M4_STAGE_4_PILOT_PACKAGE/FACILITATOR_CHECKLIST.md`  
**Milestone:** SignBridge M4 Stage 4 (Controlled Pilot Preparation)  
**Governance State:** `DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`  

---

## Pre-Session Preparation (T-30 Minutes)
- [ ] **Host Workstation Check:**
  - [ ] Operating System: Windows 10/11, macOS 12+, or Ubuntu 22.04.
  - [ ] Chrome Version: $\ge 120$ with SignBridge extension loaded in Developer Mode.
  - [ ] Python Virtual Environment: `signbridge-backend\.venv` active.
  - [ ] Local Faster-Whisper Model: `tiny.en` loaded and tested locally.
  - [ ] Display Setup: 1080p display with WebGL 2.0 acceleration confirmed.
- [ ] **Interpreter Coordination:**
  - [ ] Certified ISL Interpreter present (in-person or dedicated video link).
  - [ ] Briefed on non-critical study protocol and emergency stopping signs.
- [ ] **Documentation Materials:**
  - [ ] Participant Information Sheet (English & recorded ISL video).
  - [ ] Participant Consent Form (Draft).
  - [ ] Test Case Worksheet with anonymous Participant ID (e.g., `P-001`).

---

## Session Execution (45 Minutes)
- [ ] **Phase 1: Briefing & Accessible Consent (10 mins):**
  - [ ] Explain study purpose: User interface and software reliability evaluation.
  - [ ] Reiterate: Experimental prototype; animations NOT certified by ISL linguists.
  - [ ] Confirm no high-stakes/emergency reliance.
  - [ ] Obtain voluntary signed consent.
- [ ] **Phase 2: Onboarding & Setup (5 mins):**
  - [ ] Position Chrome with YouTube test video in primary tab.
  - [ ] Open 3D Avatar window docked alongside video.
  - [ ] Demonstrate "Start Audio Capture" and "Stop Capture" controls.
- [ ] **Phase 3: Test Scenario Execution (20 mins):**
  - [ ] **Scenario A (Baseline Sign):** Play "Namaste" clip -> Verify prayer gesture articulation.
  - [ ] **Scenario B (Unanimated Word):** Play "Thank You" clip -> Verify neutral hold & review-pending notice.
  - [ ] **Scenario C (Out-of-Lexicon):** Play technical clip -> Verify unsupported words badge & neutral hold.
  - [ ] **Scenario D (Pauses & Silence):** Play conversational clip -> Verify silence handling & zero queue lag.
- [ ] **Phase 4: Debriefing & Questionnaire (10 mins):**
  - [ ] Administer post-session evaluation questionnaire.
  - [ ] Collect qualitative feedback on visual clarity and latency.
  - [ ] Provide participant compensation stipend.

---

## Post-Session Cleanup & Data Purge (Immediate)
- [ ] Click "Clear Transcript" in extension popup.
- [ ] Terminate local backend server (`Ctrl+C`).
- [ ] Close all Chrome browser windows to wipe `chrome.storage.session`.
- [ ] Verify zero audio recording files remain on disk.
- [ ] Store anonymized facilitator worksheet in secure local study folder.
