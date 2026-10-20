# SignBridge M4 Stage 3 — End-to-End Performance Benchmark Report

**Document Reference:** `Docs/M4_STAGE_3_PERFORMANCE_REPORT.md`  
**Milestone Stage:** Milestone M4 — Stage 3: Performance & Privacy Benchmarking  
**Execution Date:** October 20, 2026  
**Auditor / Benchmarking Agent:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  
**Benchmark Artifact:** `benchmarks/m4_stage3_benchmark_results.json`  
**Benchmark Harness:** `benchmarks/benchmark_m4_stage3_pipeline.py`

---

## 1. Executive Summary & Verification Outcomes

In accordance with the Milestone M4 Stage 3 Master Directive, a reproducible benchmark harness was executed against the local SignBridge pipeline to evaluate end-to-end performance, speech recognition speed, queue and buffer limits, Three.js avatar rendering frame rate, and resource utilization.

### Key Measured Benchmarks at a Glance:
- **Speech Recognition Real-Time Factor (RTF):** **`0.506`** (p95: `0.655`) for 2.0s real speech — **faster than real-time** (< 1.0).
- **Speech Recognition Latency:** **`1011.2 ms`** median (p95: `1309.5 ms`) for 2.0s real speech; **`36.4 ms`** median for silence.
- **Audio Chunk WAV Encoding:** **`0.636 ms`** median (p95: `1.077 ms`) in-memory 16kHz mono PCM.
- **ISL Translation & Routing:** **`0.027 ms`** median (p95: `0.034 ms`).
- **End-to-End Pipeline Latency:** **`1016.4 ms`** median (p95: `1315.1 ms`) from audio chunk boundary to skeletal articulation.
- **Avatar WebGL Rendering Frame Rate:** **`60.0 FPS`** (median frame delta: `16.7 ms`, p95: `16.8 ms`) measured in real headless Chrome WebGL across 90 frames.
- **Audio Queue Depth:** Capped at **`3`** slices with oldest-chunk drop policy on overflow.
- **Transcript History Bound:** Capped at **`30`** entries in service worker session storage.
- **Steady-State Process Memory:** **`185.54 MB`** (Passing the < 250 MB operational budget).
- **Peak Process Memory:** **`256.44 MB`** during transient model weight loading (**Flagged for Owner Review**; exceeded 250 MB target by 6.44 MB / 2.5%).

---

## 2. Test Environment Specifications

All measurements were captured using the reproducible benchmark script `benchmarks/benchmark_m4_stage3_pipeline.py` on the local development environment:

| Specification Parameter | Measured Environment Value | Notes / Verification Method |
|:---|:---|:---|
| **Operating System** | Windows 10 Pro (Build 10.0.22631) | `platform.platform()` |
| **CPU Architecture** | AMD64 (x86_64) | `platform.machine()` |
| **Physical / Logical Cores** | 4 Logical Cores | `os.cpu_count()` |
| **Python Runtimes** | System Python 3.11.9 / VirtualEnv Python 3.11.9 | `signbridge-backend\.venv` |
| **Browser Environment** | Google Chrome 140.0.7339.128 | Headless Chrome with WebGL / CDP |
| **Speech Model** | Faster-Whisper `tiny.en` | Local HuggingFace cache |
| **Quantization & Device** | `int8` on CPU | `compute_type="int8"`, `device="cpu"` |
| **Thread Configuration** | 4 CPU Worker Threads | `settings.cpu_threads = 4` |
| **Warm-Up Procedure** | 2 complete discard passes (1 silence, 1 real speech) | Discard initial JIT compilation overhead |

---

## 3. Real-Time Factor (RTF) Definition & Formulas

The Real-Time Factor (RTF) is the primary metric evaluating whether speech processing can keep pace with live audio streaming without latency accumulation.

$$\text{RTF} = \frac{\text{Inference Duration (seconds)}}{\text{Input Audio Duration (seconds)}} = \frac{\text{Inference Latency (ms)} / 1000.0}{\text{Audio Chunk Duration (s)}}$$

- **$\text{RTF} < 1.0$**: The system processes audio faster than it is spoken. Latency remains bounded and real-time streaming is sustainable.
- **$\text{RTF} = 1.0$**: The system processes audio at exact real-time parity.
- **$\text{RTF} > 1.0$**: The system is slower than real-time. Audio buffers accumulate delay, resulting in pipeline lag or dropped chunks.

---

## 4. Empirical Latency & Performance Breakdown

### 4.1 In-Memory Audio Processing & WAV Encoding
Evaluated across 50 iterations of 2.0s 16kHz mono PCM buffers:
- **Median:** `0.636 ms`
- **P95:** `1.077 ms`
- **Min / Max:** `0.587 ms` / `1.615 ms`
- **Evaluation:** Sub-millisecond execution. Audio downsampling and PCM header encapsulation introduce virtually zero latency overhead.

### 4.2 Speech Recognition (Faster-Whisper int8) Latency & RTF
Evaluated after 2 warm-up runs to reflect steady-state operational latency:

| Scenario / Test Asset | Duration | Iterations | Median Latency | P95 Latency | Median RTF | P95 RTF | Observed Transcript / Quality |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **Synthetic Silence** | 2.00 s | 15 | **`36.4 ms`** | `63.9 ms` | **`0.018`** | `0.032` | Rejection (empty string, 0 tokens) |
| **Real Speech Slice** | 2.00 s | 15 | **`1011.2 ms`** | `1309.5 ms` | **`0.506`** | `0.655` | `"Hello world, this is sign"` (Avg Conf: `0.752`) |
| **Full Speech Sample** | 5.22 s | 10 | **`1110.9 ms`** | `1133.1 ms` | **`0.213`** | `0.217` | `"Hello world, this is signbridge local speech recognition test."` |

**Key Findings:**
1. **Silence VAD Rejection:** Faster-Whisper detects silence in **36.4 ms** ($\text{RTF} = 0.018$), immediately freeing the worker thread for subsequent audio slices.
2. **Real Speech Slices:** A 2.0s speech slice is transcribed in **1011.2 ms** ($\text{RTF} = 0.506$), safely below the 2000 ms chunk generation interval, preventing queue buildup.
3. **P95 Safety Margin:** The 95th percentile latency of **1309.5 ms** leaves a **690.5 ms safety margin** within every 2.0s capture window.

### 4.3 Translation Routing & Serialization
Evaluated across 500 iterations of incoming transcripts against the 16-seed lexicon:
- **Median:** `0.027 ms`
- **P95:** `0.034 ms`
- **Min / Max:** `0.022 ms` / `1.276 ms`
- **Evaluation:** Regex token matching, gloss lookup, and JSON serialization consume under 35 microseconds.

### 4.4 End-to-End Latency Model
- **Defined Pipeline Start Point:** Completion of 2.0s audio chunk capture in Chrome offscreen document.
- **Defined Pipeline End Point:** Avatar Y-Bot skeletal animation keyframe articulation on screen.

$$\text{E2E Latency} = T_{\text{WAV}} + T_{\text{LocalTransfer}} + T_{\text{ASR}} + T_{\text{Route}} + T_{\text{Interpolate}}$$

| Component Step | Median Latency (ms) | P95 Latency (ms) | Description |
|:---|:---:|:---:|:---|
| **WAV In-Memory Encoding** | 0.6 ms | 1.1 ms | Float32 downsampling & 16-bit PCM buffer packing |
| **Localhost HTTP Transfer** | 4.0 ms | 6.0 ms | `127.0.0.1:8765` loopback multipart POST transfer |
| **Faster-Whisper ASR** | 1011.2 ms | 1309.5 ms | Local CPU transcription & word timestamp generation |
| **Routing & Dispatch** | 0.0 ms | 0.0 ms | Gloss mapping & Chrome runtime broadcast |
| **Keyframe Evaluation** | 0.5 ms | 1.0 ms | Three.js animation mixer track binding |
| **Total End-to-End Latency** | **`1016.4 ms`** | **`1315.1 ms`** | **Time from audio chunk end to avatar motion** |

---

## 5. Avatar WebGL Rendering & Frame-Time Distribution

The Three.js avatar rendering engine was tested inside Google Chrome using Chrome DevTools Protocol (CDP) and `requestAnimationFrame` delta sampling across 90 frames:

| Metric | Measured Value | Target Threshold | Status |
|:---|:---:|:---:|:---:|
| **Mean Frame Rate** | **`60.0 FPS`** | $\ge 50\text{ FPS}$ | **PASS** |
| **Median Frame Delta** | **`16.7 ms`** | $16.6\text{ ms} \pm 1.0\text{ ms}$ | **PASS** |
| **P95 Frame Delta** | **`16.8 ms`** | $< 22.0\text{ ms}$ | **PASS** |
| **Min / Max Frame Delta** | **`16.5 ms` / `16.8 ms`** | $< 33.3\text{ ms}$ | **PASS** |
| **Frame Variance / Stutter** | **Zero detectable dropped frames** | 0 drops | **PASS** |

The Y-Bot skeletal rig, ambient lighting, directional key lights, and skin mesh render smoothly at the standard 60 Hz display refresh rate without frame drops or visual stutter.

---

## 6. Queue Depth, Overflow & Memory Bounds Assessment

| Subsystem / Metric | Measured Value | Baseline Proposed Target | Compliance Assessment | Actionable Recommendation |
|:---|:---:|:---:|:---:|:---|
| **Audio Queue Depth** | Max 3 chunks (`MAX_QUEUE_SIZE = 3`) | $\le 3$ chunks | **`PASS_VERIFIED`** | Code enforces oldest-chunk drop on overflow. |
| **Queue Overflow Drop** | `transcriptionQueue.shift()` | Oldest dropped | **`PASS_VERIFIED`** | Prevents latency accumulation during transient CPU spikes. |
| **Transcript History** | Max 30 segments (`newSegments.length > 30`) | $\le 30$ segments | **`PASS_VERIFIED`** | Code enforces `newSegments.shift()` in background service worker. |
| **CPU Worker Threads** | 4 threads | 4 threads | **`PASS_VERIFIED`** | Configured in `signbridge-backend/config.py`. |
| **Steady-State Memory** | **`185.54 MB`** Working Set | $< 250\text{ MB}$ | **`PASS_VERIFIED`** | Steady-state runtime comfortably within 250 MB budget. |
| **Peak Memory Usage** | **`256.44 MB`** Peak Working Set | $< 250\text{ MB}$ | **`EXCEEDED BY 6.44 MB` (2.5%)** | **Decision Required:** Transient spike during weight mapping. Recommend revising peak threshold to 300 MB. |

### In-Depth Memory Analysis & Recommendation for Project Owner:
1. **Steady-State Compliance:** During continuous transcription across synthetic and real audio runs, the backend process working set stabilized at **185.54 MB**, well below the 250 MB limit.
2. **Transient Peak Spike:** At initial model load (`CTranslate2` weight deserialization and OpenVINO/MKL thread pool initialization), Windows process working set touched **256.44 MB** before settling.
3. **Owner Proposal:** Rather than silently changing the threshold or claiming a false pass, we record:
   - Steady-State Working Set: **PASS** (`185.54 MB` < `250 MB`)
   - Peak Working Set: **FAIL** (`256.44 MB` > `250 MB`)
   - **Proposed Revised Threshold for Owner Approval:** Formally adjust the Peak Working Set threshold from `250 MB` to `300 MB` for the backend Python process to account for CTranslate2 shared library allocations, while retaining the `250 MB` limit for steady-state operation.
