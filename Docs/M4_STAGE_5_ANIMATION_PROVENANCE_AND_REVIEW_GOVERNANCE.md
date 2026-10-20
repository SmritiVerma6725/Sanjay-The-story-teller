# SignBridge M4 Stage 5 — Animation Provenance & Review Governance

**Document Reference:** `Docs/M4_STAGE_5_ANIMATION_PROVENANCE_AND_REVIEW_GOVERNANCE.md`  
**Milestone:** SignBridge Milestone M4 — End-to-End Product Integration, ISL Validation Readiness, UX, Performance, and Controlled Pilot Preparation  
**Stage:** **Stage 5: Complete Validation, Release Readiness & Evidence Closure**  
**Execution Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  
**Production Baseline:** `isl_namaste_godl_v1` (`IMPLEMENTED_UNVALIDATED`)  
**Quarantined Candidate:** `isl_namaste_mocap_candidate_v1` (Quarantined in Isolated Experimental Assets)  

---

## 1. Executive Purpose

This document provides a comprehensive audit of all 3D animation assets, skeletal rigs, dictionary mappings, linguistic statuses, and governance safeguards across the SignBridge repository. It enforces cryptographic traceability, strict isolation of experimental assets, and fail-closed protections against the premature promotion of unvalidated sign language animations.

---

## 2. Animation Asset Inventory & Provenance Ledger

| Asset Identifier | Asset Type | Source / Provenance | Declared License | SHA-256 Checksum | Linguistic Status | Production Registry Status |
|---|---|---|---|---|:---:|:---:|
| **`isl_namaste_godl_v1`** | Hand-authored 3D bone keyframe clip (1800ms) | Clean-room authored approximation of ISLRTC Vol 1, Word #0001 ("Namaste") | Government Open Data License - India (GODL) | Embedded in `keyframe_registry.js` | **`IMPLEMENTED_UNVALIDATED`** | **Active Production Baseline** |
| **`isl_namaste_mocap_candidate_v1`** | MediaPipe Holistic MoCap extraction (3080ms, 77 frames) | Extracted from `ISLRTC_Namaste_sample.mp4` via offline 1-Euro smoothed pipeline | Source video under GODL; third-party YouTube distribution unresolved | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | **`EXPERIMENTAL_AWAITING_VALIDATION`** | **Quarantined** (Excluded from production registry) |
| **`ISLRTC_Namaste_sample.mp4`** | Reference video clip (648.9 KB, 25fps) | ISLRTC Indian Sign Language Dictionary footage via third-party YouTube upload | Base work GODL; YouTube derivative/redistribution rights `UNRESOLVED` | `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8` | Reference Media Only | **Isolated in `reference_videos/`** |
| **`ybot.glb`** | 3D Skeletal Rig Mesh (2.2 MB, 67 joints) | Adobe Mixamo humanoid character rig (`ybot.glb`) | Adobe Mixamo Royalty-Free Terms of Use | Verified on disk (`2,233,440 bytes`) | Non-Linguistic Hardware Rig | **Active Avatar Geometry** |
| **`TECHNICAL_TEST_CLIP`** | Synthetic arm waving clip (1000ms) | Procedural test keyframes authored for pipeline validation | Internal clean-room test code | Embedded in `keyframe_registry.js` | **`NON_LINGUISTIC_TEST_ONLY`** | **Test Runner Only** (`isLinguisticISL=false`) |

---

## 3. Fail-Closed Governance Safeguards

### 3.1 Strict Separation of Production Baseline and Quarantined Candidate
- In `extension/animation/keyframe_registry.js`, the default `KeyframeRegistry` registers **only** `isl_namaste_godl_v1`.
- `isl_namaste_mocap_candidate_v1` is **not hardcoded** in `keyframe_registry.js`. It exists strictly as an isolated JSON file in `extension/assets/animations/` and `tools/isl_motion_extraction/output/` for use in the specialized Review Studio (`preview_mocap.html`).
- Automated tests (`test_m4_stage5_validation.py:test_11` and `test_review_readiness.py:test_06`) verify that importing or translating tokens in the production extension never resolves to the unvalidated mocap candidate.

### 3.2 Zero Hallucinated Gestures for Unsupported Vocabulary
- When speech input contains phrases outside the seed lexicon (or dictionary words that do not have 3D keyframe clips), `isl_translator.js` partitions them into `unsupportedWords`.
- `avatar_player.html` detects unsupported words and immediately executes `player.resetToNeutralPose()`.
- The UI renders an explicit, honest banner:  
  `⚠ Out-of-lexicon words: [...] — Neutral pose held (PRD: Zero synthetic gestures)`.
- **Automated Verification:** Verified in headless Chrome CDP (`tests/test_m4_browser_bridge_e2e.py`, Checks 6–8) and unit tests (`tests/test_m4_stage5_validation.py:test_08`).

### 3.3 Genuine Review Store Integrity & Anti-Fabrication Safeguards
- In accordance with SignBridge governance standards, **zero synthetic or simulated reviews** may exist in `tools/isl_motion_extraction/reviews/`.
- Automated test `test_m4_stage5_validation.py:test_13` verifies that `reviews/` contains exactly 0 files.
- The validator `validate_review_record.py` enforces cryptographic verification:
  1. Rejects any review where `candidateFileSha256` does not match `6f24e6...`.
  2. Rejects any review where `referenceVideoSha256` does not match `129811...`.
  3. Rejects records missing essential rubric fields (`handshape`, `location`, `orientation`, `movement`, `non_manuals`).
  4. Preserves `not_assessable` distinctly from negative ratings.
  5. Distinguishes template forms from completed reviews.

### 3.4 Reviewer PII Minimization
- The review record schema (`signbridge_review_schema_v1.0.0`) is designed for strict privacy:
  - Requires `role` (e.g. `deaf_native`, `certified_interpreter`, `deaf_educator`, `sign_linguist`, `community_member`, `anonymous`).
  - Supports pseudonyms or anonymous submissions.
  - Prohibits personal identifiable information (no phone numbers, physical addresses, national IDs, or financial data).

---

## 4. Legal & Provenance Analysis of Unresolved Assets

### Reference Video Asset (`ISLRTC_Namaste_sample.mp4`)
- **Claimed Source:** Indian Sign Language Research and Training Centre (ISLRTC), Ministry of Social Justice and Empowerment, Government of India.
- **Underlying License:** Government Open Data License - India (GODL), published on `data.gov.in`. Under GODL, users are granted a worldwide, royalty-free, non-exclusive license to use, adapt, and create derivative works, provided proper attribution is made:  
  *"Source: Indian Sign Language Research and Training Centre (ISLRTC), via data.gov.in under GODL."*
- **Unresolved Legal Issue (`LEGAL-01`):** The specific sample video `ISLRTC_Namaste_sample.mp4` was downloaded from a third-party YouTube mirror channel (`silentone0725`). While the uploader labeled their repository "MIT", a third-party uploader cannot legally relicense Government of India copyrighted works. Direct redistribution or packaging of third-party YouTube clips carries legal uncertainty.
- **Enforced Safeguard:** The video is isolated in `tools/isl_motion_extraction/reference_videos/` and is **excluded from extension release packaging**.
- **Required Action:** The Project Owner must direct whether to:
  - *Option A:* Confine pilot testing strictly to the official `data.gov.in` GODL distribution, excluding all YouTube media.
  - *Option B:* Seek written confirmation of educational redistribution rights from ISLRTC / DEPwD.

---

## 5. Promotion Gate Status

Per `Docs/M4_STAGE_2_PROMOTION_GATES.md`, candidate promotion to production requires:
1. Three independent evaluations from qualified Deaf-native ISL signers.
2. Minimum overall acceptance score $\ge 80\%$.
3. Zero ratings of `unacceptable` on critical structural parameters (handshape, location, movement).
4. Full cryptographic hash match on candidate and reference video.
5. Explicit, written sign-off by the Project Owner.

**Current Gate Status:** **0 / 3 Reviews Completed**. Candidate remains **QUARANTINED**.
