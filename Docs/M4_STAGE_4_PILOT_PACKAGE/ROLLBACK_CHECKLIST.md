# SignBridge Controlled Pilot — Rollback Checklist

**Document Reference:** `Docs/M4_STAGE_4_PILOT_PACKAGE/ROLLBACK_CHECKLIST.md`  
**Milestone:** SignBridge M4 Stage 4 (Controlled Pilot Preparation)  
**Governance State:** `DRY_RUN_ONLY — NOT_AUTHORIZED — OPERATIONAL CHECKLIST`  

---

## 1. Rollback Trigger Criteria
Execute immediate rollback if any of the following occur during pilot execution:
1. **Linguistic Hazard:** Avatar articulates an inaccurate, confusing, or culturally offensive handshape.
2. **Technical Instability:** Uncaught JavaScript exception halts animation loop or crashes WebGL context.
3. **Severe Latency Regression:** Real-Time Factor exceeds 1.5, causing cascading audio queue buildup and lag $> 4\text{ seconds}$.
4. **Licensing or Ethical Challenge:** Unresolved copyright challenge received regarding source assets.

---

## 2. Immediate Rollback Action Steps (< 60 Seconds)

### Step 1: Halt Capture & Stop Playback
- [ ] Instruct participant/facilitator to click **Stop Capture** in the popup.
- [ ] If popup unresponsive, close the active YouTube video tab to force MediaStreamTrack termination.
- [ ] Close the 3D Avatar window.

### Step 2: Kill Local Processes & Clear RAM
- [ ] In terminal, terminate Python backend: `Ctrl+C` (or `taskkill /F /IM python.exe`).
- [ ] Close all Google Chrome instances to flush `chrome.storage.session`.

### Step 3: Revert Registry to Protected Baseline
- [ ] Verify `extension/keyframe_registry.js` resolves default lexicon strictly to `isl_namaste_godl_v1`.
- [ ] Verify candidate `isl_namaste_mocap_candidate_v1` is excluded from production lookup:
  ```javascript
  // Confirmed Baseline Protection:
  REGISTERED_CLIPS.set('isl_namaste_godl_v1', ISL_NAMASTE_CLIP);
  ```

### Step 4: Purge In-Flight Data
- [ ] Verify `signbridge-backend/` contains zero persisted WAV recordings.
- [ ] Log rollback action in `Docs/INCIDENT_LOG.md`.

---

## 3. Post-Rollback Verification
- [ ] Re-run regression suite: `python run_all_m4_stage4_tests.py` -> Must yield 100% PASS.
- [ ] Notify SignBridge Project Owner with incident documentation.
- [ ] Freeze all further pilot sessions until formal owner re-authorization.
