# SignBridge M8 — Prioritized Controlled ISL Vocabulary Expansion Backlog

**Document Reference:** `Docs/M8_ISL_VOCABULARY_EXPANSION_BACKLOG.md`  
**Machine-Readable Fixture:** `Docs/m8_isl_vocabulary_expansion_backlog.json`  
**Milestone:** SignBridge M8 (Sign Coverage & Translation Reliability)  
**Execution Date:** October 21, 2026  
**Governance Policy:** **`STRICT APPROVAL GATES — ZERO AUTO-PROMOTION — ZERO FABRICATED GLOSSES`**  

---

## 1. Backlog Objectives & Governance Principles

This backlog prioritizes high-value missing expressions identified during empirical benchmark evaluation and user testing.

> [!IMPORTANT]
> ### Mandatory Expansion Rules:
> 1. **No Invented Signs:** Never fabricate a handshape, movement, or gloss and claim it is authentic ISL without official ISLRTC attribution or Deaf-native confirmation.
> 2. **No Automatic Promotion:** Authoring a 3D animation does not make it approved. Every candidate remains experimental until reviewed by qualified Deaf-native signers under the M4 review protocol (>=80% approval score across 3 reviews).
> 3. **Decoupled Architecture:** Lexicon entries without validated 3D animation assets must remain marked `animationId: null` to guarantee honest neutral rest poses.

---

## 2. Prioritized Candidate ISL Expression Register

| Pri | English Meaning / Intent | Candidate ISL Expression (Requires Expert Confirmation) | Required Animation Asset | Provenance & Rights Status | Linguistic Review Status | Technical Playback Status | Benchmark Source |
| :---: | :--- | :--- | :---: | :--- | :---: | :--- | :--- |
| **P1** | **Polite greeting / saying hello** (`HELLO`) | Open flat hand raised to temple/chest, gentle outward forward arc (ISLRTC Vol 1, Word #0002) | `isl_hello_v1` | ISLRTC Dictionary Vol 1 (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Unanimated in repo / No 3D keyframe asset linked | test_speech_sample.wav ('Hello world') |
| **P2** | **Expression of gratitude / thanks** (`THANK_YOU`) | Flat dominant hand touching chin/lips, moving downward and forward toward addressee (ISLRTC Vol 1) | `isl_thank_you_v1` | ISLRTC Dictionary Vol 1 (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Unanimated in repo / Multi-word lemma ('thank you', 'thanks') | Benchmark conversational corpus ('Thank you very much') |
| **P3** | **Requesting or offering assistance / aid** (`HELP`) | Closed dominant fist resting on open flat non-dominant palm, moving forward/upward together (ISLRTC Vol 1) | `isl_help_v1` | ISLRTC Dictionary Vol 1 (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Unanimated in repo / No 3D keyframe asset linked | Benchmark conversational corpus ('Please help me') |
| **P4** | **Polite request marker** (`PLEASE`) | Flat open hand rubbing clockwise over center of chest (ISLRTC Vol 1) | `isl_please_v1` | ISLRTC Dictionary Vol 1 (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Unanimated in repo / No 3D keyframe asset linked | Benchmark conversational corpus ('Please help me') |
| **P5** | **Expression of quality, well-being, or greeting ('Good morning')** (`GOOD`) | Dominant thumb-up fist moving forward from chest (ISLRTC Vol 1) | `isl_good_v1` | ISLRTC Dictionary Vol 1 (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Unanimated in repo / No 3D keyframe asset linked | Benchmark conversational corpus ('Good morning') |
| **P6** | **Inquiring or stating a person's name** (`NAME`) | Dominant H-hand tapping non-dominant H-hand index/middle fingers (ISLRTC Vol 1) | `isl_name_v1` | ISLRTC Dictionary Vol 1 (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Unanimated in repo / No 3D keyframe asset linked | Benchmark conversational corpus ('What is your name?') |
| **P7** | **Referring to addressee (2nd person pronoun)** (`YOU`) | Dominant index finger pointing forward directly toward addressee in 3D signing space (Spatial deictic) | `isl_you_deictic_v1` | Standard ISL spatial deictic pointing syntax | `Candidate backlog (0/3 reviews completed)` | Unanimated in repo / Fallback 500ms neutral hold | Live Speech Routing Regression (Scenario 2, Scenario 5) |
| **P8** | **Referring to signer (1st person pronoun)** (`I`) | Dominant index finger pointing inward toward center of signer sternum (Spatial deictic) | `isl_i_deictic_v1` | Standard ISL spatial deictic pointing syntax | `Candidate backlog (0/3 reviews completed)` | Unanimated in repo / Fallback 500ms neutral hold | Live Speech Routing Regression (Scenario 8: 'me' -> I) |
| **P9** | **WH-question inquiring about identity, name, or object** (`WHAT`) | Both open hands held forward palms up, slight side-to-side flutter with furrowed eyebrows (ISLRTC Vol 1) | `isl_what_wh_v1` | ISLRTC Dictionary Vol 1 (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Missing from SEED_LEXICON / Grammar heuristic shifts to terminus | Benchmark conversational corpus ('What is your name?') |
| **P10** | **WH-question inquiring about location ('Where is...')** (`WHERE`) | Dominant index finger wagging side-to-side with questioning facial expression (ISLRTC Vol 1) | `isl_where_wh_v1` | ISLRTC Dictionary Vol 1 (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Missing from SEED_LEXICON / Grammar heuristic shifts to terminus | Benchmark conversational corpus ('Where is the hospital?') |
| **P11** | **Expression of deep satisfaction / pride** (`PROUD`) | Dominant thumb pointing upward, moving up center chest toward neck (ISLRTC Dictionary) | `isl_proud_v1` | ISLRTC Dictionary (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Missing from SEED_LEXICON / Holds neutral rest pose | Scenario 8 ('She makes me very, very proud.') |
| **P12** | **The earth / global sphere** (`WORLD`) | Both W-hands or cupped hands circling each other forming a spherical shape (ISLRTC Dictionary) | `isl_world_v1` | ISLRTC Dictionary (data.gov.in / GODL) | `Candidate backlog (0/3 reviews completed)` | Missing from SEED_LEXICON / Holds neutral rest pose | test_speech_sample.wav ('Hello world') |

---

## 3. Recommended Phased Implementation Roadmap

### Phase 1: High-Frequency Conversational Greetings & Gratitude
- Rig and keyframe `isl_hello_v1` and `isl_thank_you_v1` from verified ISLRTC Dictionary specifications.
- Submit to formal Deaf-native review panel.

### Phase 2: Core Polite Assistance & Spatial Pronouns
- Rig `isl_help_v1`, `isl_please_v1`, and spatial deictic pointing clips `isl_you_deictic_v1` and `isl_i_deictic_v1`.
- Enforce spatial orientation parameters for 1st vs 2nd person deictic targeting.

### Phase 3: WH-Questions & Context Adjectives
- Expand `SEED_LEXICON` to include interrogative tokens (`WHAT`, `WHERE`) with coordinated non-manual markers (eyebrow furrowing).
- Rig `isl_what_wh_v1` and `isl_where_wh_v1`.
