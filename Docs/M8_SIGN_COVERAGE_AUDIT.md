# SignBridge M8 — Complete Sign Coverage & Translation Reliability Audit

**Document Reference:** `Docs/M8_SIGN_COVERAGE_AUDIT.md`  
**Machine-Readable Fixture:** `Docs/m8_sign_coverage_audit.json`  
**Milestone:** SignBridge M8 (Sign Coverage & Translation Reliability)  
**Execution Date:** October 21, 2026  
**Auditor:** Antigravity Autonomous Pair Programming Agent  
**Status:** **`AUDIT_COMPLETE — ZERO_HUMAN_VALIDATION_RECORDED`**  

---

## 1. Executive Summary & Inventory Reconciliation

| Metric | Count | Operational Definition & System Behavior |
| :--- | :---: | :--- |
| **Canonical Seed Gloss Keys** | **16** | Explicitly defined in `extension/translation/isl_translator.js` (`SEED_LEXICON`). |
| **Recognized Lemmas & Phrases** | **50** | Normalized lexical variations mapped to canonical glosses. |
| **Entries with Linked `animationId`** | **1** | Only `NAMASTE` (`isl_namaste_godl_v1`). |
| **Un-animated Dictionary Entries** | **15** | Recognized in lexicon but `animationId: null`. Safely holds neutral rest pose. |
| **Loadable Animation Assets** | **2** | 1 production baseline (`isl_namaste_godl_v1`) + 1 quarantined candidate (`isl_namaste_mocap_candidate_v1.json`). |
| **Technically Playable Clips** | **3** | Can render on Y-Bot rig: 1 baseline, 1 candidate (quarantined), 1 synthetic test. |
| **Linguistically Approved ISL Signs** | **0** | **ZERO APPROVED**. No animation has completed certified Deaf-native review. |
| **Completed Human Reviews** | **0 / 3** | Reviews directory `tools/isl_motion_extraction/reviews/` contains zero records. |

> [!IMPORTANT]
> **Core Architectural Law:**
> 1. A **dictionary match** does NOT count as a playable sign. Un-animated entries (`animationId: null`) must never increment generated sign counts.
> 2. A **technically playable animation** does NOT count as linguistically validated merely because Three.js rasterizes the bone rotations.
> 3. Namaste remains **`IMPLEMENTED_UNVALIDATED`** awaiting formal Deaf-native sign review.

---

## 2. Complete Lexicon Inventory & Animation Eligibility

| Gloss | Lemmas (50 total) | Linked Animation ID | 3D Asset Available? | Technical Playback | Linguistic Status | Fallback State |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **`NAMASTE`** | `namaste`, `namaskar`, `namaskaram` | `isl_namaste_godl_v1` | YES | Playable (1800ms) | Awaiting Review (0/3) | Neutral Rest Pose (End) |
| **`HELLO`** | `hello`, `hi`, `hey`, `greetings` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`THANK_YOU`** | `thank you`, `thanks`, `thank` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`PLEASE`** | `please` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`WELCOME`** | `welcome` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`SORRY`** | `sorry`, `apologize`, `apology` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`YES`** | `yes`, `yeah`, `yep`, `correct`, `agree` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`NO`** | `no`, `not`, `never`, `nope` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`NAME`** | `name`, `named`, `called` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`YOU`** | `you`, `your`, `yours` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`I`** | `i`, `me`, `my`, `mine`, `myself` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`HELP`** | `help`, `assist`, `assistance` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`GOOD`** | `good`, `fine`, `well`, `great` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`BAD`** | `bad`, `poor`, `wrong` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`STOP`** | `stop`, `halt`, `cease` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |
| **`WAIT`** | `wait`, `hold` | `*None (null)*` | NO | Neutral Rest Pose | Unanimated Entry | Neutral Rest Pose (500ms Hold) |

---

## 3. Technically Playable Animations vs. Linguistic Approval

| Animation ID | Target Gloss | Rig Compatibility | Renders on Y-Bot? | Linguistic ISL Guard | Review Record Status | Active in Production? |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **`isl_namaste_godl_v1`** | `NAMASTE` | 65/67 Canonical Mixamo joints | **YES** (1800ms) | `isLinguisticISL: true` | `0 / 3 reviews` (Awaiting validation) | **YES** (Production Baseline) |
| **`isl_namaste_mocap_candidate_v1`** | `NAMASTE` | 65/67 Canonical Mixamo joints | **YES** (1840ms) | `isLinguisticISL: false` (Quarantined) | `0 / 3 reviews` (Quarantined) | **NO** (Strictly isolated) |
| **`tech_test_motion_v1`** | `TECH_TEST_MOTION` | Mixamo RightArm wave | **YES** (2000ms) | `isLinguisticISL: false` (Synthetic) | N/A (Non-linguistic rig test) | **NO** (Test-only clip) |

---

## 4. Inconsistent or Missing Animation References

The audit identified **15 dictionary entries** with missing 3D animations:
- `HELLO`, `THANK_YOU`, `PLEASE`, `WELCOME`, `SORRY`, `YES`, `NO`, `NAME`, `YOU`, `I`, `HELP`, `GOOD`, `BAD`, `STOP`, `WAIT`

### Operational Risks & Mitigation:
1. **Risk of Misleading 'TRANSLATED' Claim:** If an application checks `sequence.signs.length > 0`, it might report a successful translation even when all signs lack 3D animations and the avatar remains neutral.
2. **Implemented Fix in M8:** In `avatar_player_controller.js`, status states are strictly resolved into: `PLAYBACK_COMPLETE`, `PARTIAL / UNSUPPORTED`, `UNSUPPORTED`, and `PENDING_REVIEW`. Tokens with `animationId: null` format as `0 playable clips (N dictionary match(es) awaiting review)`.
3. **Telemetry Synchronization:** Un-animated signs trigger a 500ms neutral fallback; upon completion, telemetry badge returns to `NEUTRAL` and title displays `Neutral Rest Pose (0 ms)`.

---

## 5. Benchmark Corpus Analysis & Unsupported Word Catalog

We evaluated the complete test corpus across audio fixtures and regression suites:

| ID | Source Context | Transcript | Matched Glosses | Playable Clips | Unsupported Words | Resulting Pipeline Status |
|:---|:---|:---|:---:|:---:|:---|:---:|
| **BM-01** | signbridge-backend/test_speech_sample.wav (Deterministic Fixture) | *"Hello world, this is signbridge local speech recognition test."* | `HELLO` | *0 clips* | `world`, `this`, `is`, `signbridge`, `local`, `speech`, `recognition`, `test` | `PARTIAL / UNSUPPORTED` |
| **BM-02** | Live Speech Routing Regression (Scenario 8 / Issue A) | *"She makes me very, very proud."* | `I` | *0 clips* | `she`, `makes`, `very`, `very`, `proud` | `PARTIAL / UNSUPPORTED` |
| **BM-03** | Browser Bridge E2E & Dry-Run Simulator (Scenario 8) | *"quantum computing rocket"* | *None* | *0 clips* | `quantum`, `computing`, `rocket` | `UNSUPPORTED` |
| **BM-04** | Live Speech Routing Regression (Scenario 3) | *"superconducting tokamak reactor"* | *None* | *0 clips* | `superconducting`, `tokamak`, `reactor` | `UNSUPPORTED` |
| **BM-05** | Standard Everyday Conversation Test Query 1 | *"What is your name?"* | `YOU`, `NAME` | *0 clips* | `what`, `is` | `PARTIAL / UNSUPPORTED` |
| **BM-06** | Standard Everyday Conversation Test Query 2 | *"Good morning, please help me."* | `GOOD`, `PLEASE`, `HELP`, `I` | *0 clips* | `morning` | `PARTIAL / UNSUPPORTED` |
| **BM-07** | Standard Everyday Conversation Test Query 3 | *"Thank you very much, you are welcome."* | `THANK_YOU`, `YOU`, `WELCOME` | *0 clips* | `very`, `much`, `are` | `PARTIAL / UNSUPPORTED` |
| **BM-08** | Standard Everyday Conversation Test Query 4 | *"Where is the hospital?"* | *None* | *0 clips* | `where`, `is`, `the`, `hospital` | `UNSUPPORTED` |

### Exhaustive List of Unsupported Tokens Across Benchmarks:

`are`, `computing`, `hospital`, `is`, `local`, `makes`, `morning`, `much`, `proud`, `quantum`, `reactor`, `recognition`, `rocket`, `she`, `signbridge`, `speech`, `superconducting`, `test`, `the`, `this`, `tokamak`, `very`, `what`, `where`, `world`

---

## 6. Audit Conclusion & Next Steps

1. **Baseline Integrity:** `isl_namaste_godl_v1` is the only active 3D animation. It functions reliably but remains unvalidated by humans.
2. **Zero Hallucination Guarantee:** All 15 un-animated entries and all out-of-lexicon words hold neutral rest pose without fabricating synthetic signing.
3. **Controlled Expansion Needed:** A structured backlog of priority vocabulary is established in `Docs/M8_ISL_VOCABULARY_EXPANSION_BACKLOG.md`.
