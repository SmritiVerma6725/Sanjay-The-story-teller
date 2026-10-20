# SignBridge — Architecture Decision Records (ADRs)

**Document Version:** 1.1 (Post-Review Corrections)  
**Status:** M0 Conditionally Accepted — Awaiting Human Approval to Begin M1  
**Date:** October 2026

---

## ADR-001: Hybrid Decoupled Architecture vs Monolithic Fork

### Context
SignBridge requires capturing live browser video audio, transcribing it in near-real-time, translating the text into sign language representations, and rendering a 3D avatar overlay on YouTube. 
Three candidate repositories were evaluated:
- **Kozha**: Good extension shell, but relies on scraping existing YouTube closed captions and calls a remote web service; uses an older CWASA WebGL engine.
- **Yap Render**: Interactive Next.js web app with Mixamo avatar and ISL glossing, but is unlicensed (All Rights Reserved) and relies on Gemini API.
- **GenASL**: Extensive research design for ASL, but licensed under GPLv3, incomplete (`run()` raises `NotImplementedError`), and uses `yt-dlp` to download entire videos from YouTube rather than live tab capture.

### Decision
We decide **NOT** to fork any single repository wholesale. Instead, we implement a **clean, modular, decoupled architecture**:
1. A lightweight **Chrome Manifest V3 Extension** handling tab audio capture, overlay UI, YouTube DOM synchronization, and 3D rendering.
2. A local **Zero-Cost Python Worker** (`faster-whisper` + FastAPI) running on `127.0.0.1:8765` for speech recognition and audio segmentation.
3. Completely **independent translation and sign registry modules** for Indian Sign Language (ISL) and American Sign Language (ASL).

### Consequences
- **Pros:** Full license compliance, zero copyleft contamination from GenASL, zero copyright violation from Yap Render, true active tab-audio capture without microphone dependence, and independent testability of each stage.
- **Cons:** Requires implementing the extension shell and audio capture pipeline cleanly rather than inheriting an existing codebase.

---

## ADR-002: Live Tab-Audio Capture & Playback Preservation

### Context
PRD FR-02 requires capturing audio from the playing YouTube tab without microphone dependence, functioning when headphones are connected or disconnected, and maintaining uninterrupted, audible video playback.
- GenASL downloads the video using `yt-dlp` (cannot work on live streams or dynamically playing video, high disk I/O, heavy latency).
- Kozha reads subtitle tracks (fails if a video lacks captions).
- Yap Render uses `webkitSpeechRecognition` with the user's microphone (fails when headphones are plugged in, captures ambient room noise).

### Decision
We follow Chrome's documented Manifest V3 tab audio capture workflow:
1. User clicks the extension action or floating overlay "Start" button (providing explicit user gesture).
2. Service worker invokes `chrome.tabCapture.getMediaStreamId()`.
3. The stream ID is passed to an **Offscreen Document** (`offscreen.html`).
4. In the offscreen document, `navigator.mediaDevices.getUserMedia({ audio: { mandatory: { chromeMediaSource: "tab", chromeMediaSourceId: streamId } } })` obtains the live audio stream.
5. **Playback preservation (Documented API Design — To Be Tested in M1):** An `AudioContext` is created:
   ```javascript
   const audioCtx = new AudioContext();
   const source = audioCtx.createMediaStreamSource(stream);
   source.connect(audioCtx.destination); // Routes audio back to speakers/headphones
   ```
6. **Audio segmentation:** A parallel branch feeds a `MediaRecorder` collecting 2.0–3.0s audio slices, forwarded via HTTP POST to the local transcription service.

### Status & Verification Caveat
- **Status:** **DESIGN SPECIFICATION (UNTESTED).**
- While documented in Chrome Extensions API guidance, this behavior has **not yet been executed or validated** on the SignBridge test machine. Empirical verification of audible playback preservation and headphone transitions is an explicit prerequisite for completing Milestone M1.

---

## ADR-003: Exclusion of Unlicensed, Copyleft, and Ambiguous Assets

### Context
- `yap_render_repo` has no license file in its repository (`"private": true` in `package.json`). Under copyright law, unlicensed source code is strictly protected by default copyright ("All Rights Reserved").
- `kozha_repo/data/Indian_SL.sigml` originates from two community repositories (`Text-to-Sign-Language` and `text_to_isl`) whose upstream repositories declare **no license**. Kozha's own credits page marks their license as **"Unclear"**.
- `GenASL` is licensed under GNU GPLv3, which is a strong copyleft license. Incorporating GenASL source code directly into SignBridge would mandate GPLv3 across the entire project.
- **ASL-LEX 2.0:** While its lexical database is shared for non-commercial research, its reference videos of native signers are proprietary media without redistribution rights. Furthermore, ASL-LEX contains **zero 3D animation assets**.

### Decision
1. **Exclude all source code files from `yap_render_repo`**. Algorithmic concepts (e.g. standard ISL SOV grammatical rules) may only be implemented clean-room.
2. **Exclude `Indian_SL.sigml` and unverified community SiGML files** until formal open-source licenses are declared.
3. **Exclude GenASL source code** to prevent GPLv3 copyleft contamination.
4. **Exclude ASL-LEX reference videos from distribution**. Use ASL-LEX solely as an academic linguistic reference for phonological properties.
5. Acknowledge that the project currently possesses **zero verified 3D ISL animation assets**. Initial ISL signs must be authored cleanly and submitted for review.

### Consequences
- **Pros:** Complete legal safety, zero copyright exposure, clean open-source pedigree.
- **Cons:** Vocabulary cannot be imported wholesale from unverified repositories. Initial vocabulary must be curated deliberately in Milestone M3.

---

## ADR-004: Local Speech Recognition Engine Selection (`faster-whisper`)

### Context
PRD FR-04 requires a locally runnable speech-recognition model without paid APIs. 
Candidates:
1. Paid Cloud APIs (OpenAI Whisper API, Google Speech-to-Text): Violates zero-cost policy.
2. Browser Web Speech API: Sourced from microphone or cloud; cannot consume tab audio stream in background.
3. `openai-whisper` (PyTorch): Open-source MIT, but high VRAM/CPU memory footprint and slower inference on CPU.
4. `faster-whisper` (CTranslate2): Open-source MIT, 8-bit quantization on CPU, native word-level timestamps.

### Decision
We select **`faster-whisper`** (running `tiny.en` or `base.en` on CPU with `int8` quantization) hosted in a lightweight local Python FastAPI service (`127.0.0.1:8765`).

### Status & Verification (Milestone M2 Executed)
- **Status:** **M2 IMPLEMENTED — END-TO-END VERIFICATION PENDING.**
- **Test Machine Hardware:**
  - CPU: Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz (2 physical cores, 4 logical processors)
  - RAM: 16.0 GB (15.89 GB visible, ~4.9 GB free during benchmark)
  - OS: Windows 10/11 64-bit
- **Benchmark Sample:** `test_speech_sample.wav` (5.22s, 22050 Hz, 16-bit mono PCM, speech: *"Hello world, this is signbridge local speech recognition test."*)
- **Quantization:** `int8` on CPU (`compute_type="int8"`, `device="cpu"`, `cpu_threads=4`)

| Model | Weights Size | Load Time | Avg Inference Latency (5.22s Sample) | Measured RTF | Single-Sample Transcription Observation | Real-Time Capable on CPU? |
|---|---|---|---|---|---|---|
| **`tiny.en`** | ~75 MB | 1.54s | **1466.2 ms** (1.47s for 5.22s) | **0.281** | *"Hello world, this is sign bridge local speech recognition test."* (Single-sample observation; split compound word) | **YES (< 1.0, ~560ms per 2.0s slice, derived)** |
| **`base.en`** | ~145 MB | 2.13s | **3653.5 ms** (3.65s for 5.22s) | **0.700** | *"Hello World, this is SignBridge Local Speech Recognition Test."* (Single-sample observation; capitalized proper nouns) | Marginally (< 1.0, ~1.4s per 2.0s slice, derived) |

- **Default Selection:** `tiny.en` is selected as the default local model for real-time live streaming on dual-core CPU machines due to its RTF of 0.281, leaving substantial CPU headroom for video playback and UI rendering. `base.en` is retained as a configurable option (`SIGNBRIDGE_MODEL=base.en`).

### Critical Architectural Notes (M2 Review):
1. **Preliminary Benchmark & Single-Sample Observation:**
   - The reported 1.47s latency and 0.281 RTF are measured on a single 5.22s audio sample (`test_speech_sample.wav`). The estimated 560 ms per 2.0s chunk is derived from that measurement, not an exhaustive measurement across arbitrary streaming video audio.
   - Successful recognition of this single sample is a qualitative endpoint validation, **not a general accuracy or Word Error Rate (WER) finding**. General accuracy across accents, background audio, and noisy speech is not claimed.
2. **Spoken Language vs. Sign Language Scope:**
   - `tiny.en` and `base.en` are strictly **English-only** speech models. 
   - Toggling the UI language between **ISL** and **ASL** sets the **target sign language** for downstream avatar translation; it does **not** change the input spoken speech recognition capability.
   - Processing non-English video speech will require multilingual models (such as `tiny` or `base`) with explicit language routing, which incurs higher resource costs on CPU.
3. **Word Splitting at Chunk Boundaries:**
   - Slicing continuous audio into independent 2.0s chunks means words uttered across chunk boundaries may be split or misrecognized (e.g. chunk #1 transcribed as *"sign"*, chunk #2 as *"bridge"*).
   - Milestone M3 and M4 must evaluate audio overlap, timestamp alignment, and transcript concatenation to avoid repeated or omitted words.
4. **Pending Integration Verification:**
   - While backend tests (`test_backend.py`) and browser in-engine tests (`test_m2_suite.html`) pass, the live pipeline of captured YouTube tab audio arriving at the backend and returning text to the popup remains pending an integration smoke test alongside deferred physical audio tests.

---

## ADR-009: In-Memory PCM WAV Audio Encoding & Bounded Queue Transport

### Context
Milestone M1 collected `MediaRecorder` chunks formatted as `audio/webm;codecs=opus`. However:
1. `MediaRecorder(stream, 2000)` produces an EBML/Tracks container header only in the first chunk; subsequent chunks are raw Matroska Clusters lacking codec private headers, causing standard audio decoders (including ffmpeg / PyAV) to fail on chunks 2+.
2. Direct raw PCM Blobs without headers are rejected by standard HTTP audio endpoints.
3. If the backend is temporarily slow or offline, an unbounded queue causes memory ballooning and can degrade browser video playback.

### Decision
1. **In-Memory Downsampling & RIFF WAV Encoding:**
   - In `offscreen.js`, the live tab audio stream is tapped using Web Audio API `ScriptProcessorNode` (4096 buffer).
   - Audio is downsampled in memory from browser native rates (44.1kHz / 48kHz) to **16,000 Hz** (Whisper native rate).
   - Each 2.0s slice is encoded with a standard 44-byte RIFF/WAVE header into 16-bit linear PCM mono (`audio/wav`, ~64 KB per chunk).
   - Every chunk is 100% self-contained and immediately decodable by PyAV/Whisper with zero container fragmentation.
2. **Playback Preservation Route:**
   - `mediaSourceNode.connect(audioContext.destination)` is retained unmodified as the primary playback route.
   - The analysis branch connects to a muted gain node (`gain = 0`) to keep the processor running without creating acoustic echo.
3. **Bounded FIFO Queue & Concurrency Mutex:**
   - `MAX_QUEUE_SIZE = 3`. If the queue exceeds 3 items, the oldest pending chunk is dropped to strictly bound memory consumption.
   - Concurrency lock ensures strictly **1 in-flight HTTP request** at any given time.
   - Per-request timeout is bounded to **8.0 seconds** via `AbortController`.
   - If the backend is stopped or slow, errors are caught gracefully, reported to the popup, and video playback continues audibly without interruption.
4. **Strict Localhost Boundary:**
   - Audio chunks are transmitted strictly to `http://127.0.0.1:8765/api/transcribe`. Zero audio bytes are written to disk or transmitted to any external network destination.

---

## ADR-005: 3D Avatar Rig: Mixamo Y-Bot Rig vs CWASA Engine

### Context
Two rendering approaches were evaluated:
1. **CWASA (University of East Anglia):**
   - Renders SiGML XML via a legacy CoffeeScript bundle (`allcsa.js`, 4.8MB) and Java `.jar` avatar files.
   - Licensed under CC BY-ND (Attribution-NoDerivatives) — cannot modify the renderer or avatar shaders.
2. **Three.js with Adobe Mixamo Y-Bot Rig:**
   - Standard WebGL with Three.js (MIT).
   - `ybot.glb` (2.2MB) is a skinned humanoid rig available under Adobe Mixamo terms.
   - Clean, modern GLTF format allowing standard WebGL shaders and smooth bone interpolation.

### Decision
We adopt **Three.js with the Mixamo Y-Bot rig** as the primary avatar renderer for the SignBridge MVP. 

### Critical Rig vs. Sign Animation Distinction
- **Y-Bot is a skeletal rig, NOT a sign language asset:** Adobe Mixamo provides a neutral 3D humanoid mesh with armature bones (`mixamorigHips`, `mixamorigLeftArm`, etc.). It contains **zero sign-language animations or gestures**.
- **Redistribution Terms:** Under Adobe's terms of use, Mixamo characters may be used in 2D and 3D projects. However, distributing raw 3D assets in a public repository carries legal nuances. In SignBridge, the rig is bundled strictly as an embedded component of the extension application.
- All sign animations driving this rig must be explicitly authored or sourced from legally verified sign keyframe libraries.

---

## ADR-006: Language Prioritization and Grammar Hypotheses

### Context
PRD Section 1.4 Principle 2 states: *"ISL and ASL must be treated as distinct languages, not interchangeable sets of gestures."*
Human review approved:
1. Prioritizing **Indian Sign Language (ISL)** for Milestone M3.
2. Prioritizing **American Sign Language (ASL)** for Milestone M5.

### Decision
1. **Sequencing:** Build the complete end-to-end pipeline for ISL first (M3), validating audio capture, transcription, translation, and rendering before introducing ASL (M5).
2. **Linguistic Framing as Hypotheses:**
   - Proposed rule-based transformations (e.g., converting English SVO to ISL SOV, fronting time markers, placing question words at the end, eliminating auxiliary verbs) are treated as **working heuristic hypotheses**, not absolute or complete linguistic rules.
   - **Gloss is NOT equivalent to fluent ISL:** Writing text in uppercase gloss does not capture spatial syntax, classifier predicates, or non-manual facial markers.
   - We explicitly disclaim linguistic validation until generated signs are evaluated by qualified Deaf-native signers or fluent ISL educators.

---

## ADR-007: Extension Shell Tooling: Vanilla JavaScript

### Context
Human review evaluated whether to use vanilla JavaScript or introduce a Node.js/npm/TypeScript/Vite toolchain.
- The student test machine has Python 3.11, uv, and winget, but Node.js is not present in PATH.
- Adding Node.js, npm packages, build steps, and TypeScript introduces additional complexity and potential build failure points.

### Decision
We approve **vanilla JavaScript** (ES6+ with standard browser APIs) for the initial Chrome Manifest V3 extension shell:
1. No Node.js or npm dependencies required for extension development.
2. No transpilation or bundling step needed; the extension directory can be directly loaded as an unpacked extension in Chrome Developer Mode.
3. If future complexity (such as complex React components or bundling) strictly demands it, Node.js tooling may be proposed with explicit justification.

---

## ADR-008: Closure of the "SignZen" Investigation

### Context
PRD Milestone M0 instructed auditing Kozha, Yap Render, GenASL, and "SignZen".
Investigations revealed no public open-source sign language project exists under that name.

### Decision
We officially close investigation of **SignZen** and designate it as an **unverified / non-existent open-source repository**. No code or dependencies from this name will be tracked.

---

## ADR-010: SignItem & SignSequence Data Contracts and Decoupled Animation Identifier

### Context
Milestone M3 Phase 3.1 establishes the data contracts between the upstream linguistic translation layer (M3 Phase 3.2), the keyframe asset registry (M3 Phase 3.3), the avatar animation player (M3 Phase 3.4), and YouTube video synchronization (M4).
A key design decision is whether the concrete animation/sign asset identifier (`animationId`) should be required or optional on `SignItem`.

### Decision
1. **Schema Specifications:**
   - Implement `SignItem` and `SignSequence` contracts as pure, zero-dependency JavaScript objects in [`extension/models/sign_contracts.js`](file:///C:/AmazonMlChallenge/extension/models/sign_contracts.js) using a UMD module wrapper.
   - Enforce strict validation: gloss uppercase alphanumeric format, category enum (`lexical`, `fingerspelling`, `pause`), non-negative finite `durationMs`, source enum (`seed_dictionary`, `fingerspell_fallback`, `grammar_pause`), language enum (`ISL`, `ASL`), non-negative timestamps with `endMediaTimeMs >= startMediaTimeMs`, and required honest `unsupportedWords` string array.
   - For `category: 'fingerspelling'`, enforce a single-character gloss (e.g. `'A'`, `'B'`).
2. **Animation Identifier Decision (`animationId` as Optional / Nullable):**
   - **`animationId` is designed as an EXPLICIT OPTIONAL string (`string | null`).**
   - **Rationale:** 
     - **Separation of Concerns:** The linguistic translation engine (Phase 3.2) generates grammatical `SignItem` sequences based on spoken transcripts and linguistic glosses. It should not be coupled to the physical asset file naming scheme or procedural keyframe identifiers.
     - **Asset Resolution Timing:** Asset binding occurs downstream at the Keyframe Asset Registry (Phase 3.3). If a sign is not yet animated or is handled dynamically, `animationId` remains `null` until resolved by the player.
     - **Pauses and Fallbacks:** Transitional pauses (`category: 'pause'`) do not possess discrete animation clips; their `animationId` is naturally `null`.
     - When provided, `animationId` is strictly validated to ensure it contains only safe alphanumeric and delimiter characters (`^[a-zA-Z0-9_.-]+$`).
3. **Immutability:**
   - Factory functions `createSignItem` and `createSignSequence` freeze their return values (`Object.freeze`) to guarantee that queued sign sequences cannot be mutated mid-playback.

---

## ADR-011: Experimental Rule-Based ISL Text-to-Gloss Translator & Seed Lexicon Matching

### Context
Milestone M3 Phase 3.2 requires transforming raw spoken transcripts into structured `SignSequence` objects for Indian Sign Language (ISL) using the 15-word seed vocabulary and data contracts established in Phase 3.1.
Critical engineering constraints:
1. No ungrounded claims of linguistic validity or fluent English-to-ISL machine translation.
2. Honest reporting of unsupported words (never emit phantom signs or silently discard missing words).
3. Disconnecting gloss generation from animation playback (finding a matching gloss does not mean an animation was played).

### Decision
1. **Implementation Structure:**
   - Implemented in [`extension/translation/isl_translator.js`](file:///C:/AmazonMlChallenge/extension/translation/isl_translator.js) as a pure, decoupled UMD module.
   - Depends strictly on [`extension/models/sign_contracts.js`](file:///C:/AmazonMlChallenge/extension/models/sign_contracts.js).
2. **Seed Lexicon Matching:**
   - Matches against the 15 approved seed entries (`HELLO`, `THANK_YOU`, `PLEASE`, `WELCOME`, `SORRY`, `YES`, `NO`, `NAME`, `YOU`, `I`, `HELP`, `GOOD`, `BAD`, `STOP`, `WAIT`).
   - Greedily resolves multi-word phrases first (`"thank you"` -> `THANK_YOU`) before matching single-word lemmas (`"hi"` -> `HELLO`, `"me"` -> `I`, `"your"` -> `YOU`).
3. **Honest Unsupported-Word Tracking:**
   - Any token not present in the seed lexicon is strictly preserved in `unsupportedWords`.
   - By default, unsupported words produce **zero phantom signs**.
   - Optional fingerspelling fallback (`enableFingerspellingFallback: true`) decomposes unsupported words into single A-Z letters (`category: 'fingerspelling'`, `source: 'fingerspell_fallback'`), while **still preserving the source word in `unsupportedWords`** and asserting `fingerspellingApplied: true`.
4. **Isolated Experimental Grammar Heuristics:**
   - Isolated in `applyExperimentalGrammarHeuristics()` and disabled by default (`enableExperimentalReordering: false`).
   - When enabled for experimental evaluation, it tests basic rule-based approximations:
     - Eliminating English auxiliary verbs (*is, am, are, was, were*) and articles (*a, an, the*).
     - Fronting temporal adverbs (*today, yesterday, now*).
     - Shifting WH-question words (*what, where, why*) to the sentence terminus.
     - Basic Subject-Object-Verb (SOV) reordering on 3-token pronoun phrases.
   - **Linguistic Disclaimer:** These heuristics are explicit approximations for pipeline flow testing. They do **not** claim to reflect the expressive spatial syntax, classifier morphology, or facial non-manuals of natural ISL. Deaf-native evaluation in Milestone M6 remains required.

---

## ADR-012: Declarative Keyframe Schema, Rig Bone Normalization, and Safe Asset Fallback (Phase 3.3)

### Context
Milestone M3 Phase 3.3 requires a bounded feasibility prototype to verify skeletal articulation of the Mixamo Y-Bot avatar (`ybot.glb`), establish a validated keyframe schema, implement a neutral rest pose and a synthetic technical motion prototype, and connect animation identifiers to the existing `SignItem` contract without claiming unverified linguistic signs possess animations.

### Decision
1. **Canonical Bone Hierarchy & Normalization:**
   - The verified Adobe Mixamo Y-Bot rig contains exactly 67 joints (`Armature` skin).
   - All finger digits have 4 joints per finger (`Thumb1..4`, `Index1..4`, `Middle1..4`, `Ring1..4`, `Pinky1..4`), confirming complete physiological hand articulation for fingerspelling and signs.
   - `normalizeBoneName()` automatically handles both glTF prefixed joints (`mixamorig:RightArm`) and canonical compact joints (`RightArm`).
2. **Strict Declarative Keyframe Schema:**
   - Implemented in [`extension/animation/keyframe_registry.js`](file:///C:/AmazonMlChallenge/extension/animation/keyframe_registry.js).
   - Validates bone membership against the canonical 67-joint set, rejects non-finite or malformed Euler/quaternion angles, enforces non-negative monotonically ordered keyframe times, and requires positive clip durations.
   - Requires an explicit boolean `isLinguisticISL` flag on all clips, preventing unverified motions from being presented as valid sign language.
3. **Neutral Rest Pose & Synthetic Technical Motion:**
   - `NEUTRAL_REST_POSE` (`pose_neutral_rest_v1`): Relaxes the avatar from default glTF T-pose by rotating upper arms down by ~72° (-1.25 rad Z right, +1.25 rad Z left), forearms slightly forward, and fingers slightly curved.
   - `TECHNICAL_TEST_CLIP` (`tech_test_motion_v1`): A multi-frame procedural arm and hand motion created solely to evaluate keyframe playback, timing, and transitions. It is explicitly annotated with `isLinguisticISL: false` and provenance noting non-linguistic engineering test status.
4. **Decoupled Animation Resolver & Safe Neutral Fallback:**
   - `resolveSignAnimation(signItem)` resolves against registered clips.
   - If a clip is not registered (as is the case for all 15 lexical signs and 26 fingerspelling letters in Phase 3.3), the resolver returns `resolved: false`, `clip: null`, and `fallbackPose: NEUTRAL_REST_POSE`.
   - Finding a matching gloss in the translator seed dictionary does **not** grant or imply a valid animation.
5. **Rigid Separation from Unlicensed Repositories:**
   - No procedural animation code or files were copied from `yap_render_repo` or unverified SiGML sources.

### Consequences
- **Pros:** Mathematically sound interpolation (Euler linear, Quaternion Slerp), verifiable skeletal feasibility, clean decoupling between linguistic translation and 3D rendering, and safe degradation to neutral rest pose.
- **Cons:** Vocabulary currently has 0 production ISL signs registered; 3D sign animation assets must be created and verified during subsequent M3 phases with native community review.

---

## ADR-013: Local Three.js WebGL Avatar Player Architecture & Skeletal Binding (Milestone M3 Phase 3.4)

### Context
Milestone M3 Phase 3.4 requires a minimal local 3D avatar player prototype using the Adobe Mixamo Y-Bot rig (`ybot.glb`) to demonstrate skeletal articulation, neutral pose application, keyframe evaluation, and playback controls (play, pause, resume, restart, return-to-neutral).
Critical constraints:
1. Preserve zero-cost, local-only architecture with zero cloud dependencies or paid APIs.
2. Comply with Chrome Manifest V3 Content Security Policy (`script-src 'self'`).
3. Primary-source licensing review: Three.js and GLTFLoader are MIT-licensed; Mixamo terms permit royalty-free application use but restrict standalone redistribution of raw 3D assets.
4. Procedural movements must remain explicitly labeled: **Synthetic technical test — NOT a validated ISL sign**.
5. Do not alter M1 audio capture, M2 transcription, or existing translation behavior.

### Decision
1. **Bundled Standalone Dependencies (`extension/lib/`):**
   - Bundled Three.js r128 (`three.min.js`) and `GLTFLoader.js` locally in `extension/lib/`.
   - Both components are governed by the MIT License (Copyright © 2010–2021 Three.js authors: Ricardo Cabello / mrdoob).
   - Documented in [`extension/lib/LICENSE_THREEJS.txt`](file:///C:/AmazonMlChallenge/extension/lib/LICENSE_THREEJS.txt).
   - Zero remote network requests during avatar playback; 100% compliant with MV3 `'self'` CSP.
2. **Avatar Player Architecture (`extension/animation/avatar_player.js`):**
   - Implemented as `SignBridgeAvatarPlayer.AvatarPlayer`, a pure UMD component that manages WebGL scene graph, perspective camera, multi-point lighting, and renderer.
   - Automatically maps all 67 joints from the loaded `SkinnedMesh` to canonical names.
   - Applies `NEUTRAL_REST_POSE` immediately on load so the avatar relaxes from default T-pose (~72° / 1.25 rad Z arm lowering).
   - Integrates with `SignBridgeKeyframeRegistry`: evaluates keyframes and interpolates bone rotations (Slerp for quaternions, linear for Euler angles) during timeline playback.
   - Implements full state machine: `playClip()`, `pause()`, `resume()`, `restart()`, `stop()`, and `resetToNeutralPose()`.
3. **Safe Error Handling & Fallback:**
   - Missing/null clips, invalid keyframes, or unregistered dictionary glosses (`HELLO`) trigger graceful fallback to `NEUTRAL_REST_POSE` without crashing.
   - Unknown bones in animation transforms are tracked in `missingBonesEncountered` and safely bypassed.
4. **Interactive Local Player Page (`extension/overlay/avatar_player.html`):**
   - Features visible 3D viewport, real-time playback controls, error injection buttons, progress scrubber, and live joint telemetry (Euler angles for `RightArm`, `RightForeArm`, `RightHand`).
   - Features prominent banner: `⚠ SYNTHETIC TECHNICAL TEST — NOT A VALIDATED ISL SIGN`.
5. **Rigid Separation from Unlicensed Code:**
   - Zero code copied from `yap_render_repo` or unverified community SiGML repositories.

### Consequences
- **Pros:** Full skeletal binding verified on loaded 3D model; live controls work reliably; zero remote dependencies; strict governance labels enforced.
- **Cons:** Model has no facial blendshapes (morph targets); production ISL signs remain unauthored pending native signer consultation.

---

## ADR-014: Phase 3.5 Bounded Pilot Plan, ISL Native Signer Review Protocol & Skeletal Rig Boundaries

### Context
Following the approval of M3 Phase 3.4 (technical Three.js avatar-player prototype), the project is preparing for Milestone M3 Phase 3.5.
Key constraints:
1. Do not author all 15 seed signs or 26 fingerspelling letters without human validation.
2. Select 2–3 bounded pilot candidate signs with documented primary sources (ISLRTC).
3. Establish a formal review methodology by fluent Deaf ISL signers before claiming any linguistic accuracy.
4. Verify the actual articulation boundaries of the Adobe Mixamo Y-Bot rig.
5. Ensure unreviewed or unavailable signs strictly fall back to `NEUTRAL_REST_POSE`.
6. Maintain strict invariance of M1 audio capture, M2 speech transcription, and M3.2 translation heuristics.
7. Recheck model licensing conditions for extension packaging and public redistribution.

### Decision
1. **Pilot Candidate Selection & Traceable Linguistic Sources (3 Core Signs):**
   - **Candidate 1: `NAMASTE` / `GREETING`**
     - *Primary Source Entry:* ISLRTC 10,000-Word Dictionary, Category: Greetings & Salutations, Entry: "Namaste" / "Greetings" (Module 1.2).
     - *Traceable Digital Portals:* [DEPwD ISLRTC Online Dictionary Portal](https://divyangjan.depwd.gov.in/islrtc/) | [ISLRTC Official Portal](http://www.islrtc.nic.in/) | [ISLRTC Official Channel](https://www.youtube.com/@ISLRTCNEWDELHI).
     - *Phonological Parameters:* Two-handed symmetrical sign. Palms flat together in front of upper chest (Anjali Mudra), slight forward head/hand bow.
     - *Kinematic Test Focus:* Symmetrical bilateral arm coordination (`LeftArm`/`RightArm`, `LeftForeArm`/`RightForeArm`), palm-to-palm spatial alignment.
     - *Status:* **PROPOSED PILOT CANDIDATE — NOT LINGUISTICALLY VALIDATED** (`isLinguisticISL: false`).
   - **Candidate 2: `THANK_YOU`**
     - *Primary Source Entry:* ISLRTC 10,000-Word Dictionary, Category: Basic Communication / Polite Expressions, Entry: "Thank you"; NCERT ISL Glossary on [DIKSHA Portal](https://diksha.gov.in/).
     - *Traceable Digital Portals:* [DEPwD ISLRTC Online Dictionary Portal](https://divyangjan.depwd.gov.in/islrtc/) | [ISLRTC YouTube Channel](https://www.youtube.com/@ISLRTCNEWDELHI).
     - *Phonological Parameters:* Dominant flat hand (B-handshape) touches chin/lower lip, moving downward and forward toward the addressee.
     - *Kinematic Test Focus:* Unilateral dominant arm trajectory, chin-proximity targeting, smooth forward stroke deceleration.
     - *Status:* **PROPOSED PILOT CANDIDATE — NOT LINGUISTICALLY VALIDATED** (`isLinguisticISL: false`).
   - **Candidate 3: `HELP`**
     - *Primary Source Entry:* ISLRTC 10,000-Word Dictionary, Category: Everyday Actions & Emergency, Entry: "Help".
     - *Traceable Digital Portals:* [DEPwD ISLRTC Online Dictionary Portal](https://divyangjan.depwd.gov.in/islrtc/) | [Sign Learn Mobile App (DEPwD/ISLRTC)](http://www.islrtc.nic.in/).
     - *Phonological Parameters:* Two-handed asymmetric sign. Non-dominant flat hand palm up at chest height; dominant closed fist (A-handshape) rests on non-dominant palm; both hands lift upward together.
     - *Kinematic Test Focus:* Asymmetrical dual-arm positioning, hand-on-palm contact, synchronized vertical translation (+Y).
     - *Status:* **PROPOSED PILOT CANDIDATE — NOT LINGUISTICALLY VALIDATED** (`isLinguisticISL: false`).

2. **ISL Review Rubric Status: Internal Engineering Quality Gate (Not Official Certification):**
   - The proposed 3-reviewer panel and 4.0/5.0 threshold represents an **internal engineering quality gate and preliminary heuristic filter**, NOT an official certification standard or universal linguistic stamp.
   - Passing internal review does not establish universal ISL validity across regional dialects.
   - **Deaf Community Co-Design:** Deaf ISL users and native signers must be actively involved in defining, evaluating, and refining the review process. All reviewer feedback, dissenting opinions, and dialectal variations must be transparently documented in the project repository.
   - **Evaluation Dimensions (Heuristic Gate):** Standard Stokoe/ISL phonological parameters: Handshape (*Dez*), Location (*Tab*), Movement (*Sig*), Orientation, and Non-Manual Markers (*NMM*).
   - **Prohibition on Self-Certification:** AI agents, software engineers, and automated tests are strictly forbidden from unilaterally declaring any gesture linguistically valid.

3. **Y-Bot Skeletal Articulation Feasibility & Limitations:**
   - *Confirmed Capabilities:* 67 physical joints, including 20 joints per hand (4 joints across 5 digits each), full 3-phalanx finger bending, and wrist flexion/twist.
   - *Rig Limitations:*
     - **No Facial Skeleton or Blend Shapes:** `ybot.glb` has zero facial bones and zero morph targets. In ISL, non-manual markers (eyebrow raises, mouth morphemes, head tilts) are phonemic and grammatical. The Y-Bot cannot articulate facial grammar (though basic head tilt via `Neck`/`Head` is possible).
     - **No Metacarpal Palm Splay:** Metacarpal bases are fixed; finger abduction requires rotating proximal phalanges, causing minor skinning pinch at extreme spread.
     - **No Real-Time Collision Detection:** Hand-to-hand contacts (`NAMASTE`, `HELP`) require manual keyframe offset tuning to prevent polygonal mesh interpenetration.
     - **Skinning Pinches at High Wrist Angles:** Wrist flexion exceeding 60° causes visible deformation at the forearm cuff.

4. **Preservation of Safe Neutral Fallback:**
   - Any unreviewed, missing, or unsupported sign strictly evaluates to `NEUTRAL_REST_POSE`.
   - The registry flags `{ resolved: false, clip: null, fallbackPose: NEUTRAL_REST_POSE, isLinguisticISL: false }`.

5. **Licensing & Distribution Recheck:**
   - Adobe Mixamo terms permit royalty-free inclusion of 3D characters in packaged software applications (e.g. unpacked or packed Chrome extensions).
   - Redistribution of standalone raw `.glb` files in public open-source repositories remains a gray area under stock asset terms.
   - For long-term public open-source distribution, SignBridge will evaluate CC0/CC-BY humanoid rigs (e.g. MakeHuman / Blender Studio assets) to eliminate proprietary redistribution ambiguity.

### Consequences
- **Pros:** Prevents unverified sign hallucination; grounds technical work in documented ISLRTC standards; provides clear criteria for community sign-off; documents exact hardware/mesh boundaries.
- **Cons:** Animation authoring is intentionally throttled pending manual visual inspection and Deaf community review.




