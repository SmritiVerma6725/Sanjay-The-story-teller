# SignBridge M5 — Data Readiness and Model Training Feasibility Report

## 1. Readiness Summary

| Evaluation Criteria | Current Status | Assessment |
| :--- | :---: | :--- |
| **Open Parallel Sentence Corpus** | **NOT AVAILABLE** | No public, permissively licensed, sentence-aligned English $\leftrightarrow$ ISL corpus exists. |
| **Lexical Word Alignment** | **READY (GODL)** | ISLRTC Volumes 1–3 provide ~10,000 isolated lexical video demonstrations under GODL-India. |
| **Pretrained Translation Weights** | **NONE AVAILABLE** | No commercial or open HuggingFace/PyTorch weights exist for English-to-ISL glossing. |
| **Local Compute Requirements** | **VERIFIED** | Local ASR (`faster-whisper`, int8 on CPU) operates at RTF $\approx 0.08$ on localhost `127.0.0.1:8765`. |
| **3D Skeletal Rigging** | **VERIFIED** | Canonical 67-joint Y-Bot rig with quaternion Slerp interpolation verified in WebGL. |
| **Deaf-Native Review Baseline** | **PENDING (0/3)** | 0 of 3 qualified Deaf-native reviews completed; `NAMASTE` remains experimental. |

---

## 2. Model Training Feasibility Analysis

### 2.1 The "Translation is Not Transcription" Barrier
- Spoken English uses Subject-Verb-Object (SVO) order with morphological inflections and function words (articles, prepositions, copula verbs).
- Indian Sign Language uses Subject-Object-Verb (SOV) and Topic-Comment order, classifier handshapes, spatial reference indexing, and non-manual facial markers.
- Attempting to train a Sequence-to-Sequence (Seq2Seq) model (e.g., MarianMT, T5, BART) without a minimum of 20,000–50,000 authentic, natural parallel sentence pairs will result in catastrophic hallucination, producing nonsensical sign sequences that demean Deaf communication.

### 2.2 Hardware and Storage Assessment
- Large-scale translation model training would require dedicated multi-GPU nodes (NVIDIA A100/H100 or RTX 4090 clusters) with 200+ GB of dataset storage.
- Given that the necessary dataset does not exist under authorized licensing, commencing expensive training or downloading large language checkpoints is neither technically justified nor economically responsible.

---

## 3. Truthful Architectural Roadmap

```mermaid
flowchart TD
    subgraph Input ["Runtime Speech Stream"]
        Audio["Tab Audio Capture"] --> Whisper["faster-whisper (tiny.en, int8 CPU)"]
        Whisper --> Text["Transcribed English Text"]
    end

    subgraph TranslationLayer ["Modular Translation Interface"]
        Text --> Interface["ISignLanguageTranslator Interface"]
        Interface --> Router["Translation Router (translation_router.js)"]
        Router --> SeedLexicon["16-Word Bounded Seed Lexicon"]
        Router --> HeuristicGrammar["Experimental Grammar Heuristics (Optional)"]
    end

    subgraph GovernanceLayer ["Linguistic Safeguards & Classification"]
        SeedLexicon --> Classifier{"Classification"}
        Classifier -->|Eligible Animation (Namaste)| PlayableClip["isl_namaste_godl_v1 (1800 ms)"]
        Classifier -->|Unanimated Entry (15 words)| NeutralAwaiting["NEUTRAL_REST_POSE (Awaiting 3D Data)"]
        Classifier -->|Out-of-Lexicon Words| NeutralOut["NEUTRAL_REST_POSE (Zero Synthetic Gestures)"]
    end
```

### 3.1 Replaceable Translation Interface Strategy
1. **Preserve `SignBridgeTranslationRouter`:** Maintain the clean UMD interface `routeTranscriptTranslation(transcript, targetLanguage, options)`.
2. **Current Baseline (M5):** Rule-based phrase and lemma matcher with strict honest categorization (`unsupportedWords`).
3. **Future Extensibility:** When an authorized, reviewed parallel corpus becomes available, an external or local ML model can drop in behind `ISignLanguageTranslator` without breaking downstream `SignSequence` data contracts.

---

## 4. Operational Directives
- **Zero Fabrication:** Never guess or interpolate hand positions for words lacking motion data.
- **Explicit Telemetry:** Always surface partial translations and list unsupported tokens in the viewport.
- **Maintain Local Loopback:** All ASR inference remains bound to `127.0.0.1:8765`.
