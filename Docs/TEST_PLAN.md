# SignBridge — Test Plan & Quality Assurance Strategy

**Document Version:** 1.5 (Milestone M3 Phase 3.2 ISL Translator Verified)  
**Status:** M3 Phase 3.1 & 3.2 Implemented & Verified (M2 Live Verification Pending)  
**Date:** October 2026

---

## 1. Quality Principles & Ground Rules

1. **Empirical Verification Only:** A test is **never marked as passed** unless it was physically executed on the test machine with recorded console outputs or test reports. Everything else is marked `NOT YET RUN` or `NOT VERIFIED`.
2. **Untested vs Documented APIs:** Documented browser behaviors (such as `chrome.tabCapture` audio routing) are treated as **unverified hypotheses** until demonstrated on physical hardware.
3. **Headphone & Playback Preservation:** Tests must evaluate both headphone-connected and headphone-disconnected states without relying on an external ambient microphone.
4. **Linguistic Disclaimers:** Automated tests evaluate schema compliance, timing constraints, and rule syntax. They **do not prove linguistic validity**. SignBridge does not claim linguistic accuracy without evaluations conducted with fluent or Deaf-native signers.

---

## 2. Test Architecture & Levels

```
                     ┌───────────────────────────────┐
                     │    End-to-End User Flows      │
                     │  (YouTube Playback, Seek,     │
                     │   Headphones On/Off, Drift)   │
                     └───────────────┬───────────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     │       Integration Tests       │
                     │  (TabCapture -> Playback Aud, │
                     │   AudioStream -> Whisper ASR, │
                     │   Transcript -> Gloss -> 3D)  │
                     └───────────────┬───────────────┘
                                     │
                     ┌───────────────┴───────────────┐
                     │          Unit Tests           │
                     │  (Grammar Heuristics, Timing  │
                     │   Math, Slerp Interpolation,  │
                     │   Schema Contracts, Licenses) │
                     └───────────────────────────────┘
```

---

## 3. Detailed Milestone Test Criteria

### 3.1 Milestone M1 Acceptance Tests: Tab-Audio Capture & Playback Preservation

Milestone M1 cannot be closed without running and passing each of the following empirical tests:

| Test ID | Test Case | Test Procedure | Pass / Fail Acceptance Criteria | Current Status |
|---|---|---|---|---|
| **M1-TC01** | **Explicit User Activation** | 1. Open a YouTube video.<br>2. Verify capture does not begin automatically.<br>3. Click the extension "Start" button. | Capture stream is requested only in response to a direct user click. No background eavesdropping. | `NOT YET RUN (Code Implemented; Awaiting Live Chrome Session)` |
| **M1-TC02** | **Audible Playback Preservation (Speakers)** | 1. Play video through internal laptop speakers at 50% volume.<br>2. Start tab capture.<br>3. Listen for continuous audio output. | Sound continues playing through laptop speakers at identical volume with zero muting, crackling, or distortion. | `NOT YET RUN (Code Implemented; Awaiting Physical Speaker Test)` |
| **M1-TC03** | **Audible Playback Preservation (Headphones)** | 1. Plug in 3.5mm or USB headphones.<br>2. Start tab capture on playing YouTube video.<br>3. Listen through headphones. | Sound plays cleanly through headphones. No microphone feedback loop or room noise present. | `NOT YET RUN (Code Implemented; Awaiting Physical Headphone Test)` |
| **M1-TC04** | **Headphone Connect / Disconnect Transition** | 1. Start capture with headphones plugged in.<br>2. Unplug headphones during active playback.<br>3. Plug headphones back in. | Audio seamlessly switches between headphones and speakers; capture stream does not disconnect or crash. | `NOT YET RUN (Code Implemented; Awaiting Hardware Transition Test)` |
| **M1-TC05** | **Audio Chunk Slicing** | 1. Capture 10 seconds of speech.<br>2. Observe `MediaRecorder` slice generation in offscreen document. | Generates consecutive 2.0s WebM/PCM slices; each chunk has valid headers and non-zero byte size. | `NOT YET RUN (Code Implemented; Awaiting Live Stream Session)` |
| **M1-TC06** | **Video Pause & Resume** | 1. Pause the YouTube video.<br>2. Wait 5 seconds.<br>3. Resume video playback. | During pause, audio stream produces silence or pauses chunking; resumes without buffer overflow upon playback. | `NOT YET RUN (Code Implemented; Awaiting Live Stream Session)` |
| **M1-TC07** | **Video Seeking** | 1. Seek forward 30 seconds, then seek backward 15 seconds. | Audio stream immediately reflects new playback timestamp; no buffered stale audio plays. | `NOT YET RUN (Code Implemented; Awaiting Live Stream Session)` |
| **M1-TC08** | **Playback Rate Changes** | 1. Change YouTube speed to 0.5x, 1.5x, and 2.0x. | Audio capture continues without pitch corruption or buffer overrun. | `NOT YET RUN (Code Implemented; Awaiting Live Stream Session)` |
| **M1-TC09** | **Stop Capture & Resource Release** | 1. Click "Stop" in extension.<br>2. Inspect Chrome Task Manager. | Stream tracks stopped (`track.stop()`), `AudioContext` closed, offscreen document destroyed. Audio returns to default browser handling. | `NOT YET RUN (Code Implemented; Awaiting Live Stream Session)` |
| **M1-TC10** | **Error Handling & Navigation** | 1. Start capture.<br>2. Navigate to another URL or close the tab. | Extension handles stream termination gracefully without throwing unhandled exceptions in background console. | `NOT YET RUN (Code Implemented; Awaiting Live Stream Session)` |

---

### 3.2 Milestone M2 Acceptance Tests: Local Transcription & Benchmarking

Milestone M2 requires establishing an empirical latency and accuracy baseline:

#### Mandatory Benchmarking Protocol:
- **Test Machine Baseline Documentation:**
  - Operating System: Windows 11 (build recorded)
  - CPU: Processor model and physical core count
  - RAM: Total installed memory and available memory during run
  - GPU: Available graphics hardware (if any) or CPU-only declaration
- **Benchmark Execution Method:**
  1. Prepare a standard 60-second reference speech WAV file (16kHz mono).
  2. Slice into thirty 2.0-second sequential chunks.
  3. Submit chunks sequentially to `POST /api/transcribe` on local FastAPI service.
  4. Measure:
     - Worker inference time (ms) per chunk.
     - End-to-end HTTP round-trip latency (ms).
     - Calculated Real-Time Factor (RTF = inference_time / chunk_duration).
     - Peak memory utilization (MB) of the Python process.
- **Models Evaluated:** `tiny.en` vs `base.en` with `compute_type="int8"`.

| Test ID | Target Metric | Engineering Goal | Status |
|---|---|---|---|
| **M2-TC01** | Real-Time Factor (RTF) | RTF <= 0.25 on CPU (<= 500ms per 2.0s chunk) | `NOT VERIFIED (Unverified estimate — pending M2)` |
| **M2-TC02** | End-to-End Latency | Median latency <= 1.0s from chunk emission to JSON response | `NOT VERIFIED (Unverified estimate — pending M2)` |
| **M2-TC03** | Word Error Rate (WER) | WER <= 15% on clean reference speech | `NOT VERIFIED (Pending M2 evaluation)` |

---

### 3.3 Milestone M3 & M5 Acceptance Tests: Translation & Animation

| Test ID | Target System | Scope & Acceptance Criteria | Status |
|---|---|---|---|
| **M3-TC01** | ISL Grammar Transformations | English SVO converted to heuristic ISL SOV; auxiliary verbs removed; WH-words placed at sentence end. *(Note: Evaluates rule syntax only; not linguistic certification).* | `NOT YET RUN (Planned M3)` |
| **M3-TC02** | ISL Seed Vocabulary Resolution | Known seed words (greetings, numbers) map to valid bone keyframes. Unknown words trigger A-Z fingerspelling fallback. | `NOT YET RUN (Planned M3)` |
| **M3-TC03** | Three.js Skeletal Playback | Mixamo Y-Bot mesh renders in overlay iframe and executes bone animations without WebGL crashes or NaN rotations. | `NOT YET RUN (Planned M3)` |
| **M3-TC04** | End-to-End Latency | Total elapsed time from spoken word ending to avatar beginning corresponding sign gesture is <= 3.0 seconds. | `NOT VERIFIED (Pending M3 run)` |
| **M5-TC01** | ASL Grammar & Lexicon | Topic-Comment translation rules and ASL-LEX pilot verified signs execute independently of ISL module. | `NOT YET RUN (Planned M5)` |

---

## 4. Milestone M0 Audit & Verification Evidence

The following table records the empirical verification steps executed during Milestone M0:

| Action / Verification Step | Tool / Command Executed | Observed Result | Recorded Status |
|---|---|---|---|
| **Workspace Directory Scan** | `list_dir c:/AmazonMlChallenge` | Found 3 cloned directories: `kozha_repo`, `yap_render_repo`, `GenASL`, plus `Docs/`. | **VERIFIED** |
| **Cloned Git Remotes** | `git -C <repo> remote -v` | Confirmed upstream URLs: `sanaro99/GenASL`, `zhan-a/Kozha`, `mitarthpathak/yap-render`. | **VERIFIED** |
| **Python Environment Check** | `python --version` | Verified Python 3.11.9 is available. | **VERIFIED** |
| **Package Tooling Check** | `uv --version`, `winget --version` | Verified `uv 0.11.32` and `winget.exe` are available. | **VERIFIED** |
| **Node.js Environment Check** | `node --version; npm --version` | `node` and `npm` not recognized in system PATH. | **VERIFIED (Not in PATH)** |
| **License File Audit** | Inspected `LICENSE` and `package.json` in each repository | Kozha: MIT; GenASL: GPLv3; Yap Render: No license file (`private: true`). | **VERIFIED** |
| **"SignZen" Investigation** | Web and GitHub searches | No open-source sign language repository exists under this name. | **VERIFIED (Non-existent)** |
| **Audio Capture Method Audit** | Grep across all cloned codebases | Kozha scrapes captions; Yap Render uses microphone; GenASL uses yt-dlp. None use `chrome.tabCapture`. | **VERIFIED** |
| **`faster-whisper` Latency & RTF** | Benchmarking script | No benchmark was executed during M0. | **NOT VERIFIED (Unverified Estimate)** |
| **`chrome.tabCapture` Playback** | Physical audio test in browser | No extension code was executed during M0. | **NOT VERIFIED (Pending M1)** |
| **ISL Translation Naturalness** | Evaluation with Deaf signers | No evaluation conducted during M0. | **NOT VERIFIED (Pending M3/M6)** |

---

## 5. Milestone M1 Automated Test Evidence & Verification

The following empirical tests were executed using Chrome 155 (`chrome.exe`) and automated test runner (`run_chrome_tests.py` and `extension/tests/test_m1_suite.html`):

| Test Component | Verification Tool / Script | Execution Result | Recorded Status |
|---|---|---|---|
| **Manifest V3 Schema & Permissions** | `python run_chrome_tests.py` (Manifest parser) | `manifest_version: 3`; required permissions: `tabCapture`, `offscreen`, `activeTab`, `storage`, `scripting`; host permissions: `*://*.youtube.com/*`, `http://127.0.0.1:8765/*`. | **VERIFIED** |
| **Extension Static Asset Integrity** | `python run_chrome_tests.py` (File/PNG validator) | Verified presence of `manifest.json`, `popup.html`, `popup.js`, `popup.css`, `offscreen.html`, `offscreen.js`, `background.js`, `icons/icon-16.png` (16x16), `icons/icon-48.png` (48x48), `icons/icon-128.png` (128x128). | **VERIFIED** |
| **Popup UI DOM Elements** | Chrome 155 (`test_m1_suite.html`) | DOMParser confirmed 21 required M1 UI elements: capture button, status badge, tab indicators, telemetry items, language selector, backend health card. | **VERIFIED** |
| **Default Language Selection** | Chrome 155 (`test_m1_suite.html`) | Verified `langISL` is checked by default; `langASL` available as secondary choice. | **VERIFIED** |
| **Explicit Activation Notice** | Chrome 155 (`test_m1_suite.html`) | Verified UI explicitly requires user activation (PRD FR-01) with zero background auto-start. | **VERIFIED** |
| **Telemetry Formatters** | Chrome 155 (`test_m1_suite.html`) | Verified `formatBytes` (0B, 512B, 2.0KB, 2.5MB) and `formatDuration` (00:00, 00:09, 01:05, 60:05). | **VERIFIED** |
| **URL Navigation/Internal Filter** | Chrome 155 (`test_m1_suite.html`) | Verified rejection of `chrome://`, `about:blank`, `edge://` with descriptive user alerts; accepted YouTube & HTTP. | **VERIFIED** |
| **Service Worker State Machine** | Chrome 155 (`test_m1_suite.html`) | Verified `idle` -> `starting` -> `capturing` -> `stopping` -> `idle` lifecycle and duplicate start blocking. | **VERIFIED** |
| **Web Audio Destination Routing** | Chrome 155 (`test_m1_suite.html`) | Verified `createMediaStreamSource` connects to `audioContext.destination` (playback preservation pipeline). | **VERIFIED** |
| **Resource Cleanup Architecture** | Chrome 155 (`test_m1_suite.html`) | Verified `track.stop()` iterates all tracks and `audioContext.close()` transitions context to `closed`. | **VERIFIED** |
| **Physical Audio & Speaker Playback** | Physical hardware test | Requires active YouTube playback with physical speakers and human listener. | **NOT YET RUN (Awaiting physical hardware test)** |
| **Physical Headphone Transition** | Physical hardware test | Requires physical plug/unplug of 3.5mm/USB headphones during live playback. | **NOT YET RUN (Awaiting physical hardware test)** |

---

## 6. Milestone M2 Empirical Test Evidence & Benchmarking

### 6.1 Local Python Backend Unit & Integration Tests (`test_backend.py`)

Executed with `python test_backend.py` against `fastapi.testclient.TestClient(app)`:

| Test Case | Test Description | Input / Condition | Observed Result | Status |
|---|---|---|---|---|
| **M2-BE-01** | Health Check Endpoint | `GET /health` | Returned HTTP 200: `{ status: "ok", service: "signbridge-backend", version: "0.2.0", model: "tiny.en", device: "cpu", compute_type: "int8", uptime_seconds: ... }` | **VERIFIED** |
| **M2-BE-02** | Speech WAV Sample Transcription | `POST /api/transcribe` with `test_speech_sample.wav` (5.22s, 22050Hz, mono) | Returned HTTP 200: text *"Hello world, this is signbridge local speech recognition test."*, word timestamps for all words, inference time ~1576ms, RTF = 0.302. | **VERIFIED** |
| **M2-BE-03** | Sequential Audio Slices Transcription | `POST /api/transcribe` with three 2.0s sequential slices (seq=1, 2, 3; t=0.0, 2.0, 4.0) | All 3 returned HTTP 200 in strict order: Chunk #1 *"Hello world, this is sign"*; Chunk #2 *"bridge local speech recognition."*; Chunk #3 *"test."*. Preserved `sequence_id` and timestamps. | **VERIFIED** |
| **M2-BE-04** | Empty Audio Chunk Handling | `POST /api/transcribe` with 0-byte audio payload | Returned HTTP 200: `{ status: "empty", text: "", segments: [], metrics: { inference_time_ms: 0, rtf: 0, audio_bytes: 0 } }`. | **VERIFIED** |
| **M2-BE-05** | Malformed / Corrupted Audio Rejection | `POST /api/transcribe` with invalid non-audio byte string | Returned HTTP 400 Bad Request with descriptive `AudioDecodingError` message. | **VERIFIED** |
| **M2-BE-06** | Oversized Payload Enforcement | `POST /api/transcribe` with 11 MB payload (> 10MB limit) | Returned HTTP 413 Payload Too Large. | **VERIFIED** |
| **M2-BE-07** | Privacy Boundary (Zero Outbound Network) | Socket monkey-patch intercepting all non-loopback connections | 0 external connections attempted during transcription. Completely offline operation. | **VERIFIED** |

### 6.2 Chrome Extension In-Engine Automated Tests (`test_m2_suite.html`)

Executed via headless Chrome (`run_chrome_tests.py`):

| Test Case | Test Description | Observed In-Engine Result | Status |
|---|---|---|---|
| **M2-EXT-01** | Popup M2 UI Elements | `DOMParser` confirmed presence of `transcriptionBadge`, `clearTranscriptBtn`, `transcriptBox`, `emptyTranscriptNotice`, `transcriptText`, `asrMetrics`, `asrLatency`, `asrRtf`, `asrChunkSeq`. | **VERIFIED** |
| **M2-EXT-02** | Header Subtitle Update | Verified header subtitle states *"Tab Audio & Local ASR • M2"*. | **VERIFIED** |
| **M2-EXT-03** | Honest Labeling Disclaimer | Verified footnote explicitly states *"Recognized speech text only (M2). Sign language avatar translation begins in M3."* | **VERIFIED** |
| **M2-EXT-04** | Web Audio 16kHz Downsampling | 48,000 Hz float input downsampled to exactly 32,000 samples for 2.0s slice at 16,000 Hz. | **VERIFIED** |
| **M2-EXT-05** | Standard 44-Byte RIFF WAV Encoding | Formatted RIFF header, format chunk (1=PCM, 1=Mono, 16000Hz, 32000 Bps, 16-bit), data chunk (64000 bytes). | **VERIFIED** |
| **M2-EXT-06** | Bounded FIFO Queue (Max 3 Items) | Pushed 5 consecutive chunks; oldest 2 dropped; strictly bounded memory at 3 items. | **VERIFIED** |
| **M2-EXT-07** | Single-Request Concurrency Mutex | Parallel calls serialized; maximum concurrent in-flight requests strictly 1; dispatched in FIFO order. | **VERIFIED** |
| **M2-EXT-08** | AbortController 8s Timeout | Verified timeout signal cancels long-running fetch and raises `AbortError`. | **VERIFIED** |
| **M2-EXT-09** | Playback Preservation Unbroken by Errors | Simulated backend HTTP 503 / network failure; verified Web Audio `mediaSource.connect(audioContext.destination)` remains intact. | **VERIFIED** |
| **M2-EXT-10** | Strict Loopback Privacy Boundary | Verified backend endpoint URLs are strictly `http://127.0.0.1:8765/*`; zero cloud endpoints. | **VERIFIED** |

### 6.3 Empirical Hardware & Latency Benchmarks (`benchmark_models.py`)

- **Host Hardware:** Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz (2 physical cores, 4 threads), 16.0 GB RAM (15.89 GB visible), Windows 10/11 64-bit.
- **Audio Sample:** `test_speech_sample.wav` (5.22s, 22050 Hz, 16-bit PCM mono).
- **Quantization:** `int8` on CPU (`compute_type="int8"`, `device="cpu"`, `cpu_threads=4`).

| Benchmark Metric | `tiny.en` (int8, CPU) | `base.en` (int8, CPU) | Engineering Significance |
|---|---|---|---|
| **Model Weights Size** | ~75 MB | ~145 MB | Minimal disk footprint; downloads in <10s on broadband |
| **Cold Load Time** | 1.54s | 2.13s | Fast server startup on CPU |
| **Inference Time (5.22s sample)** | **1466.2 ms (1.47s)** | **3653.5 ms (3.65s)** | `tiny.en` is 2.5x faster than `base.en` on this benchmark run |
| **Calculated RTF** | **0.281** | **0.700** | Derived from the 5.22s run; `tiny.en` leaves ~72% CPU headroom for playback & UI |
| **Estimated Latency / 2.0s slice** | **~560 ms** (derived) | **~1400 ms** (derived) | Mathematical extrapolation from the 5.22s measurement; not a per-chunk streaming benchmark |
| **Single-Sample Transcription Observation** | *"Hello world, this is sign bridge local speech recognition test."* | *"Hello World, this is SignBridge Local Speech Recognition Test."* | **Single-sample qualitative observation only:** `tiny.en` recognized all spoken words on this sample ('sign bridge' split); does NOT establish general accuracy, WER, or robustness across diverse speakers/accents |
| **Selection for MVP Streaming** | **Selected Default** | Available Config Option | Defaulting to `tiny.en` minimizes queue backlog risk on dual-core hardware |

> [!NOTE]
> **Benchmark & Pipeline Caveats (M2 Review):**
> 1. **Preliminary Benchmark Baseline:** The reported 1.47s inference time and derived 560 ms/chunk estimate are based solely on a single 5.22s WAV sample. Streaming latency across continuous video audio will vary with background noise, speech tempo, and CPU contention.
> 2. **Single-Sample Accuracy vs. General WER:** Successful transcription of one clear speech sample is an empirical proof-of-endpoint, not a statistical accuracy finding. No general accuracy claim is made.
> 3. **Spoken Language vs. Target Sign Language Scope:** `tiny.en` is strictly an English-language speech recognition model. Selecting Indian Sign Language (ISL) or American Sign Language (ASL) in the UI selects the target sign language for translation, not the spoken input language. Transcribing non-English speech will require deploying multilingual models (e.g. `tiny` or `base`) and explicit language detection/handling.
> 4. **Boundary Word Splitting Across Chunks:** Independent transcription of 2.0s audio slices can split words across slice boundaries (e.g., chunk #1 ending with *"sign"* and chunk #2 beginning with *"bridge"*). Downstream processing in M3/M4 will evaluate boundary overlap, transcript merging, and word-level timestamps.

### 6.4 Unexecuted Integration & Physical Verification

| Verification Item | Required Action | Status |
|---|---|---|
| **Live Extension-to-Backend Integration Smoke Test** | Start local backend (`127.0.0.1:8765`), open a live YouTube video in Chrome, start capture from popup, confirm captured audio chunks reach backend, and verify transcription displays in popup UI. | **PENDING INTEGRATION SMOKE TEST (Narrow smoke test to be conducted alongside deferred live browser tests)** |
| **Live YouTube Tab Capture Flow** | Playing active YouTube video in Chrome, clicking Start, observing continuous streaming capture in offscreen document. | **NOT VERIFIED (Deferred to live browser testing)** |
| **Physical Speaker Audible Playback** | Listening to internal laptop speakers during live YouTube capture to confirm no audible muting. | **NOT VERIFIED (Deferred to physical hardware testing)** |
| **Physical Headphone Plug/Unplug** | Connecting and disconnecting 3.5mm/USB headphones during active capture. | **NOT VERIFIED (Deferred to physical hardware testing)** |

---

## 7. Milestone M3 Phase 3.1 Empirical Test Evidence: Data Contracts

Executed via headless Google Chrome 155 (`run_chrome_tests.py` running `extension/tests/test_m3_suite.html`):

| Test Suite / Category | Tests Run | In-Engine Verification Details | Status |
|---|---|---|---|
| **1. Valid Objects & Immutability** | 5 | Valid minimal/full SignItem, default values, frozen immutability, full SignSequence with child items and unsupported words. | **VERIFIED (5/5 PASS)** |
| **2. Missing Fields Enforcement** | 4 | Rejects missing/blank gloss, category, durationMs, source, sequenceId, language, timestamps, signs, unsupportedWords, fingerspellingApplied. | **VERIFIED (4/4 PASS)** |
| **3. Allowed Enum Values & Consistency** | 5 | Rejects invalid category, invalid source, invalid language, invalid headTilt/eyebrows; enforces category-source consistency (fingerspelling $\rightarrow$ fingerspell_fallback). | **VERIFIED (5/5 PASS)** |
| **4. Duration & Timestamp Boundaries** | 4 | Rejects negative/non-finite durationMs, negative startMediaTimeMs/endMediaTimeMs, inverted timestamps (`end < start`); accepts zero-length boundary intervals. | **VERIFIED (4/4 PASS)** |
| **5. Empty Sequences & Child Validation** | 2 | Accepts valid empty sequences (silence); recursively validates and pinpoints invalid child SignItems inside sequence. | **VERIFIED (2/2 PASS)** |
| **6. Unsupported Words & Honest Telemetry** | 2 | Accepts string arrays of unmapped vocabulary; rejects numbers, nulls, and whitespace-only strings. | **VERIFIED (2/2 PASS)** |
| **7. Fingerspelling Constraints** | 3 | Accepts single-character gloss (e.g. `'A'`, `'K'`); rejects multi-character gloss for fingerspelling category; enforces boolean `fingerspellingApplied`. | **VERIFIED (3/3 PASS)** |
| **8. Animation Identifier Contract** | 3 | Accepts valid alphanumeric/dash/underscore `animationId`; accepts `null` or omitted `animationId` (decoupling linguistic gloss from asset registry); rejects spaces and invalid symbols. | **VERIFIED (3/3 PASS)** |
| **Phase 3.1 Total** | **28** | **28 executed in Chrome 155; 28 PASSED; 0 FAILED** | **VERIFIED** |

---

## 8. Milestone M3 Phase 3.2 Empirical Test Evidence: ISL Text-to-Gloss Translator

Executed via headless Google Chrome 155 (`run_chrome_tests.py` running `extension/tests/test_m3_suite.html`):

| Test Suite / Category | Tests Run | In-Engine Verification Details | Status |
|---|---|---|---|
| **9. Text Normalization & Tokenization** | 4 | Strips punctuation, converts to lowercase, handles whitespace/tabs, empty transcripts, and punctuation-only strings; sets question flag. | **VERIFIED (4/4 PASS)** |
| **10. Seed Lexicon Matching & Lemmas** | 4 | Matches canonical single-word seed signs, lemma variations (`"hi"` $\rightarrow$ `HELLO`, `"thanks"` $\rightarrow$ `THANK_YOU`, `"me"` $\rightarrow$ `I`), prioritizes multi-word phrases (`"thank you"`), and handles repeated known words. | **VERIFIED (4/4 PASS)** |
| **11. Unsupported Words & Honest Reporting** | 3 | Zero phantom signs emitted for all-unknown transcripts; partitions mixed known/unknown transcripts; preserves repeated unknown words in `unsupportedWords`. | **VERIFIED (3/3 PASS)** |
| **12. Fingerspelling Fallback Mode** | 3 | Default mode leaves unknown words in `unsupportedWords` without phantom signs; fallback mode expands to single-letter `SignItem`s (`category: 'fingerspelling'`, `source: 'fingerspell_fallback'`) while still honestly preserving source word in `unsupportedWords`. | **VERIFIED (3/3 PASS)** |
| **13. Isolated Experimental Grammar Heuristics** | 5 | Eliminates auxiliary verbs (*is, am, are*) and articles (*a, the*); fronts temporal adverbs (*today*); shifts WH-question words to terminus; basic SVO $\rightarrow$ SOV reordering on pronoun phrases; verifies heuristics are bypassed when `enableExperimentalReordering` is false. | **VERIFIED (5/5 PASS)** |
| **14. Contract Compliance & Boundary Metadata** | 4 | Output `SignSequence` strictly passes `validateSignSequence`; returned objects are deeply frozen and immutable; handles empty transcripts and clamps negative/inverted timestamps. | **VERIFIED (4/4 PASS)** |
| **Phase 3.2 Total** | **23** | **23 executed in Chrome 155; 23 PASSED; 0 FAILED** | **VERIFIED** |

---

## 9. Milestone M3 Phase 3.3 Empirical Test Evidence: Declarative Keyframe Schema & Feasibility Prototype

Executed via headless Google Chrome 155 (`run_chrome_tests.py` running `extension/tests/test_m3_suite.html`):

| Test Suite / Category | Tests Run | In-Engine Verification Details | Status |
|---|---|---|---|
| **15. Keyframe Schema & Canonical Bone Dictionary** | 9 | Identifies canonical Mixamo bone names with and without `mixamorig:` prefix; confirms 67 canonical joints; rejects unknown bones (e.g. `Tentacle`, `Wings`); validates Euler, Quaternion, and position transforms; rejects malformed rotations (wrong dimensions, NaNs, zero-magnitude quaternions); enforces non-negative monotonically ordered keyframe times; strictly enforces boolean `isLinguisticISL` guard; rejects clips missing required provenance or duration. | **VERIFIED (9/9 PASS)** |
| **16. Neutral Rest Pose & Synthetic Motion Prototype** | 5 | Validates all `NEUTRAL_REST_POSE` bone transforms against schema; verifies bilateral arm lowering from T-pose (~72° / 1.25 rad Z) and resting finger curvature; verifies synthetic technical prototype clip (`tech_test_motion_v1`) passes validation, asserts `isLinguisticISL === false`, and declares synthetic feasibility provenance; evaluates timeline interpolation at t=0, midpoint, and endpoint; verifies Slerp produces unit quaternions with accurate intermediate rotations. | **VERIFIED (5/5 PASS)** |
| **17. Animation Resolver & Safe Neutral Fallback** | 5 | Resolves registered prototype clip by explicit `animationId`; resolves registered clip by matching `gloss`; returns `resolved: false` with safe fallback to `NEUTRAL_REST_POSE` for un-animated dictionary glosses (`HELLO`, `THANK_YOU`, `PLEASE`, `A`, `Z`); ensures no false claims of animations exist without assets; gracefully handles null, undefined, and empty inputs. | **VERIFIED (5/5 PASS)** |
| **Phase 3.3 Total** | **19** | **19 executed in Chrome 155; 19 PASSED; 0 FAILED** | **VERIFIED** |

---

## 10. Milestone M3 Phase 3.4 Empirical Test Evidence: Three.js Avatar Player Prototype

Executed via headless Google Chrome 155 (`run_chrome_tests.py` running `extension/tests/test_m3_suite.html`):

| Test Suite / Category | Tests Run | In-Engine Verification Details | Status |
|---|---|---|---|
| **18. Model Loading & Skeletal Articulation** | 9 | Verifies `AvatarPlayer` class export; rejects null container; initializes Three.js scene, camera, lights, and appends canvas; loads local `ybot.glb` binary over HTTP; discovers all 67 canonical joints on the physical `SkinnedMesh`; automatically applies `NEUTRAL_REST_POSE` upon load, lowering arms (~72° / 1.25 rad Z) from T-pose; verifies that `applyPose()` directly modifies physical `THREE.Bone` rotations in the scene graph; handles 404 missing model load gracefully with structured `AvatarPlayerError` (`MODEL_LOAD_FAILED`); **regression test verifies `frustumCulled = false` on all meshes and asserts rasterized avatar pixels via `gl.readPixels(...)` to ensure the viewport is not blank.** | **VERIFIED (9/9 PASS)** |
| **19. Playback Controls & Safe Recovery** | 10 | Plays `TECHNICAL_TEST_CLIP` and evaluates timeline interpolation on actual model bones across keyframes; pause freezes bones at current evaluated timestamp; resume advances from paused position; restart resets playback to t=0 and initial rest pose; stop returns avatar to neutral rest pose; safely recovers from null/invalid clips with neutral rest fallback; safely handles `playSignItem` for un-animated dictionary gloss (`HELLO`) by holding neutral pose; safely ignores unknown bones in transforms and records them in telemetry; strictly enforces non-linguistic label (`isLinguisticISL === false`); `dispose()` cleans up WebGL renderer, cancels animation frame, and clears scene hierarchy. | **VERIFIED (10/10 PASS)** |
| **Phase 3.4 Total** | **19** | **19 executed in Chrome 155; 19 PASSED; 0 FAILED** | **VERIFIED** |
| **Milestone M3 Overall Total** | **89** | **Phase 3.1 (28) + Phase 3.2 (23) + Phase 3.3 (19) + Phase 3.4 (19) = 89 PASSED; 0 FAILED** | **VERIFIED** |
| **SignBridge Overall In-Engine Total** | **108** | **M1 (9) + M2 (10) + M3 (89) = 108 PASSED; 0 FAILED** | **VERIFIED** |

### 10.1 Visual Render & Interactive Playback Verification
- Visual render evidence was captured at 1280x900 resolution in Chrome: [`extension/overlay/avatar_render_evidence.png`](file:///C:/AmazonMlChallenge/extension/overlay/avatar_render_evidence.png).
- Confirmed visible dark-slate viewport card, interactive playback buttons (Play, Pause, Resume, Restart, Return to Neutral), error injection buttons, real-time progress scrubber, status badges (`NEUTRAL`, `PLAYING`, `PAUSED`), and live joint telemetry reading physical Euler angles from the rig.
- Verified that the avatar is fully visible with natural resting arm posture and centered camera framing.
- Verified prominent governance banner: `⚠ SYNTHETIC TECHNICAL TEST — NOT A VALIDATED ISL SIGN`.

---

## 11. Milestone M3 Phase 3.5 Bounded Pilot Test Strategy & Verification Matrix

### 11.1 Automated Regression Verification vs. Manual In-Chrome Verification

| Verification Level | Scope | Method / Tool | Pass / Pending Status |
|---|---|---|---|
| **Automated Unit & In-Engine (108 Tests)** | M1 Extension Shell (9)<br>M2 Local Speech Recognition (10)<br>M3.1 Data Contracts (28)<br>M3.2 ISL Translation Engine (23)<br>M3.3 Keyframe Schema (19)<br>M3.4 Avatar Player & Visibility (19) | `python run_chrome_tests.py` running in headless Chrome 155 | **108 / 108 PASSED** (0 failures). Deterministically asserts object immutability, schema rules, Slerp math, joint discovery, WebGL visibility, and error handling. |
| **Manual Local Visual Inspection** | Visual aesthetic, lighting, framing, 60fps rendering fluidity, and interactive controls on `extension/overlay/avatar_player.html` | Human review in desktop Google Chrome | **PENDING USER MANUAL INSPECTION** (Automated headless screenshot captured in `avatar_render_evidence.png`). |
| **Physical Audio Verification** | Audible playback preservation through speakers/headphones during live tab audio capture | Physical human listening test on hardware | **PENDING PHYSICAL HARDWARE VERIFICATION** (Deferred by user; unchanged). |
| **Live Integration Smoke Test** | End-to-end YouTube tab capture $\rightarrow$ offscreen PCM conversion $\rightarrow$ local Whisper transcription $\rightarrow$ popup UI display | Live test with playing YouTube video | **PENDING INTEGRATION SMOKE TEST** (Deferred; unchanged). |
| **ISL Linguistic Accuracy** | Pilot candidate animations (`NAMASTE`, `THANK_YOU`, `HELP`) reviewed by native signers | 5-stage human-in-the-loop review protocol (ADR-014) | **AWAITING NATIVE SIGNER PANEL REVIEW** (No self-certification permitted). |







