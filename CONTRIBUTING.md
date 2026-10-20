# Contributing to SignBridge

Thank you for your interest in contributing to **SignBridge**!

SignBridge is an open-source, local-first research prototype developed to provide real-time Indian Sign Language (ISL) avatar visualization for web video. Because this software directly impacts accessibility for the Deaf and Hard-of-Hearing community, all contributions must adhere to strict ethical, linguistic, and privacy safeguards.

---

## 1. Core Principles

1. **Zero Cloud Leakage & Privacy First:** All audio capture, speech transcription, and avatar rendering must execute 100% locally on the user's machine. Zero external API calls, tracking scripts, or telemetry are permitted.
2. **Strict Linguistic Integrity:** Automated joint tracking confidence or ML inference metrics **never equal linguistic correctness**. No sign language animation may be labeled as "validated" or promoted into production without qualified Deaf-native review.
3. **Honest Fallbacks:** If a word is not supported by the dictionary or lacks an animated keyframe clip, the avatar **must hold a neutral rest pose**. Never generate synthetic, fabricated, or random gestures.
4. **Data Minimization:** No personal health information (PHI), personal identifiable information (PII), or raw user audio recordings may be retained on disk.

---

## 2. Development Setup

### Prerequisites
- **Operating System:** Windows 10/11, macOS, or Linux
- **Python:** Python 3.11+
- **Browser:** Google Chrome 120+ (with hardware WebGL acceleration enabled)

### Local Backend Setup
```bash
cd signbridge-backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python run.py
```
Verify the backend responds on `http://127.0.0.1:8765/health`.

### Chrome Extension Setup
1. Open Chrome and navigate to `chrome://extensions/`.
2. Toggle **Developer mode** on in the upper-right corner.
3. Click **Load unpacked** and select the `extension/` directory.
4. Open a YouTube video tab, click the SignBridge puzzle icon, and click **"Open 3D Avatar Display"**.

---

## 3. Running the Verification Suites

Before opening a pull request, run the unified master test suite:

```bash
python run_all_m4_stage5_tests.py
```

This runner executes all 340 automated checks across 7 sub-suites:
- M3 Baseline Kinematic & Usability Suite (246 checks)
- M4 Stage 1 Bridge Contract & Sequence Ordering (14 checks)
- M4 Stage 1 Browser E2E Smoke Test in Chrome WebGL (16 checks via CDP)
- M4 Stage 2 ISL Vocabulary & Governance Suite (14 checks)
- M4 Stage 3 Performance, Privacy & Failure Recovery Suite (15 checks)
- M4 Stage 4 Controlled Pilot Dry-Run Suite (17 checks)
- M4 Stage 5 Complete Validation & Release Readiness Suite (18 checks)

All 340 checks must pass with exit code `0`.

---

## 4. Linguistic Governance & Promotion Gates

### Quarantine Policy
- Any candidate animation extracted from video motion capture or procedural keyframing must be placed in `tools/isl_motion_extraction/output/` and marked with:
  ```json
  "validationStatus": "experimental_awaiting_validation"
  ```
- Experimental clips must **never** be hardcoded into `extension/animation/keyframe_registry.js` or `isl_translator.js`.

### Promotion Requirements
Per [`Docs/M4_STAGE_2_PROMOTION_GATES.md`](Docs/M4_STAGE_2_PROMOTION_GATES.md), promoting an experimental clip to production baseline requires:
1. Three independent evaluations from certified Deaf-native ISL signers.
2. An overall parameter rating $\ge 80\%$.
3. Zero ratings of `unacceptable` on primary parameters (handshape, location, movement).
4. Verifiable cryptographic SHA-256 hash match on candidate and reference assets.
5. Explicit, written authorization from the Project Owner.

---

## 5. Submitting Changes

1. Fork the repository and create a feature branch (`git checkout -b feature/my-feature`).
2. Implement your changes adhering to existing code conventions.
3. Ensure no secrets, `.env` files, `.bmp` files, or rights-uncleared videos are committed.
4. Verify all tests pass locally.
5. Commit with a clear, conventional commit message (`git commit -m "feat: add bounded queue telemetry"`).
6. Push to your branch and submit a Pull Request with a clear description of the change and test evidence.
