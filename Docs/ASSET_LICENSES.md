# SignBridge — Asset & License Audit (M0–M3.7)

**Document Version:** 1.5 (Milestone M3.8 Implemented — Motion Capture Extraction Pipeline & License Verification)  
**Audit Date:** October 2026  
**Status:** M3.8 Implemented — ISL NAMASTE Slice Audited (Hand-Authored Approximation Awaiting Linguistic Validation); ISLRTC License (GODL vs DEPwD Portal) Verified; Offline MediaPipe MoCap Pipeline Built & Benchmark Tested (5.0 FPS CPU); Zero Cloud Dependencies  
**Audit Scope:** Independent evaluation of source code, model weights, datasets, reference videos, 3D rigs, animation clips, fonts, and dependencies across `signbridge-backend`, `extension`, candidate repositories, and upstream providers.

---

## 1. Compliance Principles & Evaluation Rules

Under the SignBridge Free-Only Technology Policy and PRD principles:
1. **Zero External Runtime Cost:** The core prototype must operate completely without paid APIs, subscriptions, or proprietary cloud infrastructure.
2. **Granular Asset-Level Auditing:** A repository's top-level license does **not** grant rights to bundled third-party datasets, model weights, 3D meshes, reference videos, or animation keyframes. Each category must be audited and recorded separately.
3. **Strict Treatment of Unlicensed Assets:** Repositories or files lacking an explicit open-source license are treated as **All Rights Reserved** under copyright law and cannot be copied, modified, or redistributed.
4. **Copyleft Isolation:** Reciprocal licenses (such as GPLv3 in GenASL) must not infect the core extension or modular components.
5. **No Presumption of Legal Certainty:** This document records documented licensing facts and identifies legal uncertainties for project and institutional review. It does not constitute formal legal counsel.

---

## 2. Granular Component & Asset Inventory

### 2.1 Candidate Repositories (Source Code Only)

| Component | Category | Source / Origin | Version / Commit | Exact License | Non-Commercial Only? | Modification Permitted? | Redistribution Permitted? | Required Attribution | Approval Status | Unresolved Questions & Legal Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| **Kozha Extension Shell** | Source Code | [github.com/zhan-a/Kozha](https://github.com/zhan-a/Kozha) (`extension/`) | `v2.0.0` (commit `69e9d69`) | MIT License | No | Yes | Yes | Copyright (c) 2026 Zhan Amankeldy & Bogdan Mironov | **Approved for Shell Concept** | Extension structure and UI concepts are MIT. However, the YouTube scraper (`content-youtube.js`) scrapes subtitles and must not be used for tab capture. |
| **Kozha Server** | Source Code | [github.com/zhan-a/Kozha](https://github.com/zhan-a/Kozha) (`server/`) | commit `69e9d69` | MIT License | No | Yes | Yes | Same as above | **Conditional Reference** | Python FastAPI server using spaCy and HamNoSys. Serves as architectural reference only. |
| **Yap Render Source Code** | Source Code | [github.com/mitarthpathak/yap-render](https://github.com/mitarthpathak/yap-render) | commit `52fe61f` | **NO LICENSE** (`private: true` in `package.json`) | N/A | **No** | **No** | N/A | **REJECTED / EXCLUDED** | Unlicensed code. All rights reserved by original authors (Mitarth Pathak et al.). Zero code may be copied. |
| **GenASL Source Code** | Source Code | [github.com/sanaro99/GenASL](https://github.com/sanaro99/GenASL) | commit `039da5e` | GNU GPLv3 | No | Yes (under GPLv3) | Yes (under GPLv3) | Full GPLv3 notices & source disclosure | **REJECTED for Inclusion** | Strong copyleft. Direct inclusion would force all SignBridge code under GPLv3. Incomplete prototype (`run()` raises `NotImplementedError`). |
| **SignZen** | Source Code | Search on GitHub / Web | N/A | N/A | N/A | N/A | N/A | N/A | **REJECTED / NON-EXISTENT** | No open-source repository found. Name refers to unrelated commercial Salesforce e-signature or ERP products. |

---

### 2.2 3D Avatars, Rigs & Mesh Files

| Asset | Category | Source / Maintainer | Version / File | Exact License / Terms | Non-Commercial Only? | Modification Permitted? | Redistribution Permitted? | Required Attribution | Approval Status | Detailed Licensing Notes & Caveats |
|---|---|---|---|---|---|---|---|---|---|---|
| **Y-Bot Character Rig** | 3D Mesh & Skeletal Rig | Adobe Mixamo ([mixamo.com](https://www.mixamo.com/)) | `ybot.glb` (2.2 MB) | Adobe General Terms of Use & [Mixamo FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) | No | Yes (animation & character retargeting) | **Conditional (project use permitted; raw asset extraction restricted)** | None formally required by FAQ, but good practice to cite Adobe Mixamo | **Conditional (Approved for Rig Geometry)** | **CRITICAL:** Y-Bot is a general humanoid rig containing bones and skinning. It contains **ZERO sign language animations**. Bundling in a browser extension is acceptable for rendering, but raw GLB redistribution terms should be monitored. |
| **CWASA Avatar Engine** | Avatar Rendering Engine | Virtual Humans Group, University of East Anglia ([CWA System](http://vh.cmp.uea.ac.uk/index.php/CWA)) | `allcsa.js` (4.8 MB) + `.jar` avatars | Creative Commons Attribution-NoDerivatives 4.0 ([CC BY-ND 4.0](https://vh.cmp.uea.ac.uk/index.php/CWASA_Conditions_of_Use)) | No | **NO (Strict No-Derivatives)** | Yes (unmodified only) | Virtual Humans Group, University of East Anglia | **Conditional (Unmodified Only)** | Legacy CoffeeScript/WebGL runtime. Engine code cannot be modified. Bundling is permitted under CC BY-ND 4.0 provided exact attribution is retained. |
| **Ready Player Me ("brunette.glb")** | 3D Mesh | Ready Player Me (found in `yap_render_repo`) | `brunette.glb` (4.7 MB) | CC BY-NC 4.0 | **Yes (Non-commercial only)** | Yes | Yes (Non-commercial) | Ready Player Me | **REJECTED / EXCLUDED** | Unnecessary non-commercial restriction. Replaced by Mixamo Y-Bot in upstream repo. Excluded from SignBridge. |

---

### 2.3 Sign Language Datasets, Videos & Animation Files

> [!IMPORTANT]
> **Key Finding:** There are currently **ZERO approved, verified 3D Indian Sign Language (ISL) animation assets** available from the candidate repositories. Lexical databases and reference videos must not be confused with avatar-ready animation files.

| Dataset / Asset | Category | Language | Source / Provenance | Declared License | Non-Commercial Only? | Redistribution Permitted? | Approval Status | Critical Review & Limitations |
|---|---|---|---|---|---|---|---|---|
| **ASL-LEX 2.0 Lexical Database** | Lexical / Linguistic Dataset | ASL | ASL-LEX Project ([asl-lex.org](https://asl-lex.org/)) | CC BY-NC 4.0 (website) / CC BY 4.0 (OSF) | **Yes** (strict website terms) | Yes (derived linguistic data) | **Conditional (Linguistic Reference Only)** | **NOT ANIMATION DATA.** ASL-LEX is a tabular database of phonological and lexical properties (handshape, location, movement type). It contains **no 3D animation clips, MoCap data, or SiGML code**. |
| **ASL-LEX 2.0 Reference Videos** | Reference Video Recordings | ASL | ASL-LEX Project ([asl-lex.org](https://asl-lex.org/)) | All Rights Reserved (Proprietary website media) | **Yes** | **NO** | **REJECTED / EXCLUDED from Redistribution** | Videos of human signers on asl-lex.org are for viewing/reference only. They **cannot be packaged, bundled, or redistributed** in the SignBridge extension without explicit institutional permission. |
| **ASL Pilot Signs (Kozha derived)** | 3D SiGML Sign Encodings | ASL | Hand-authored in Kozha (`data/American_SL_ASL.sigml`) | Derived work in Kozha (MIT repo) | Unknown | Conditional | **Unverified Pilot Only (Not Certified)** | 14 hand-authored signs. Kozha's own documentation notes these are pilot heuristics and have **zero formal Deaf-native review**. They are not certified sign language animations. |
| **ISLRTC Indian Sign Language Dictionary (data.gov.in)** | Lexical & Video Corpus | ISL | Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India ([data.gov.in](https://data.gov.in)) | Government Open Data License - India (GODL) | No (Commercial & Non-Commercial permitted) | Yes (with attribution) | **Approved for Derivative Extraction & Retargeting** | Official national dictionary of Indian Sign Language (10,000+ words across Volumes 1–3). Published under NDSAP on data.gov.in under GODL. Grants a worldwide, royalty-free, non-exclusive license to use, adapt, and create derivative works (including 3D keypoint extraction) with mandatory attribution: *"Source: Indian Sign Language Research and Training Centre (ISLRTC), via data.gov.in under GODL."* |
| **ISLRTC Official Website (`islrtc.nic.in`)** | Portal & Media Downloads | ISL | DEPwD / ISLRTC portal | Copyright DEPwD / All Rights Reserved | N/A | **NO (Reproduction prohibited without prior permission)** | **RESTRICTED for Direct Scraping** | Official website copyright policy states: *"Contents of the website cannot be reproduced partially or fully without due permission from DEPwD/ISLRTC."* Video assets must originate from the open NDSAP/GODL data.gov.in distribution, not direct portal scraping. |
| **ISLRTC Hugging Face Mirror (`silentone0725`)** | Re-encoded Video Mirror | ISL | Third-party HEVC re-encoding of data.gov.in dataset | Uploader declared "MIT" (Legally Defective) | No | Yes (under underlying GODL terms) | **Conditional Technical Reference** | A third-party uploader cannot legally relicense Government of India copyrighted works as MIT. The underlying legal basis remains GODL. Permissible to process as a technical HEVC mirror, but attribution and rights derive from GODL, NOT MIT. |
| **ISL Namaste Animation Clip (`isl_namaste_godl_v1`)** | 3D Bone Keyframe Clip | ISL | Derived from ISLRTC Dictionary Vol 1, Word #0001 ("Namaste" / "Greetings") via clean-room manual keyframing | Derived work under Government Open Data License - India (GODL) | No | Yes (with attribution) | **Experimental — Awaiting Linguistic Validation** | 1800ms bilateral prayer pose (Anjali Mudra) at sternum with forward head nod. **PROVENANCE & VALIDATION AUDIT (M3.8):** This clip is a **hand-authored geometric approximation**, NOT captured from video motion-capture. While legally compliant under GODL, it is **unverified by a qualified Deaf-native ISL signer** and must remain classified as experimental. |
| **ISL Community Dataset (Divanshu & Shoebham)** | SiGML Dataset | ISL | `Text-to-Sign-Language` & `text_to_isl` (bundled in Kozha) | **NO LICENSE DECLARED (Unclear)** | Unknown | **NO** | **REJECTED / EXCLUDED** | Kozha's credits page explicitly states: *"No license declared in either upstream repository. License: Unclear."* Excluded under SignBridge policy. |
| **Yap Render Procedural Animations** | Bone Rotation Keyframes | ISL | `components/avatar/animations/Words` | **NO LICENSE (All Rights Reserved)** | Unknown | **NO** | **REJECTED / EXCLUDED** | Euler rotation keyframes authored by unlicensed project. Cannot be copied. |
| **DictaSign Parallel Corpus** | Sign Corpus (SiGML) | BSL, LSF, GSL | IDGS, Universität Hamburg ([DictaSign](https://www.sign-lang.uni-hamburg.de/dicta-sign/portal/)) | CC BY-NC-SA 3.0 | **Yes** | Yes (Non-commercial, Share-Alike) | **Conditional (Test Fixture for BSL/LSF)** | 881 BSL signs, 381 LSF signs. Recorded with native signers. Validated for research and non-commercial testing. |
| **WLASL (Word-Level ASL)** | Video Dataset | ASL | Dongxu Li et al. (GenASL Phase 4) | Academic Research Use Only | **Yes** | **NO** (Third-party YouTube links) | **REJECTED for Extension Bundling** | Academic dataset consisting largely of scraped YouTube video URLs. Many URLs are dead. Not suitable for offline extension distribution. |
| **NGT, Algerian, Bangla, Kurdish, VSL Corpora** | SiGML Datasets | Various | Community repositories bundled in Kozha | **NO LICENSE DECLARED (Unclear)** | Unknown | **NO** | **REJECTED / EXCLUDED** | Unlicensed community uploads. Excluded per policy. |

---

### 2.4 Machine Learning Models & Speech Recognition (Verified M2)

| Asset / Library | Category | Maintainer / Source | Exact License | Non-Commercial Only? | Runtime Cost | Approval Status | Findings & Benchmarking Status |
|---|---|---|---|---|---|---|---|
| **faster-whisper** | ASR Library | SYSTRAN / OpenAI Whisper via CTranslate2 ([GitHub](https://github.com/SYSTRAN/faster-whisper)) | MIT License | No | Zero (Local CPU) | **VERIFIED & BENCHMARKED (M2)** | Open-source inference engine using CTranslate2. Verified zero external network calls during transcription. Measured RTF = 0.281 on Intel i5-7200U (`tiny.en`). |
| **OpenAI Whisper Model Weights** | Pretrained Neural Network Weights | OpenAI / Systran CTranslate2 conversion | MIT License | No | Zero (Local) | **VERIFIED & BENCHMARKED (M2)** | `tiny.en` (~75MB) and `base.en` (~145MB) weights verified under MIT license. Self-hosted locally on loopback (`127.0.0.1:8765`). |
| **FastAPI** | Web Framework | Sebastián Ramírez | MIT License | No | Zero (Local) | **VERIFIED & APPROVED (M2)** | Permissive MIT web framework used for local HTTP service. |
| **Uvicorn** | ASGI Server | Encode | BSD-3-Clause | No | Zero (Local) | **VERIFIED & APPROVED (M2)** | Permissive ASGI server bound strictly to loopback (`127.0.0.1`). |
| **python-multipart** | Streaming Multipart Parser | Andrew Chen Wang | Apache-2.0 | No | Zero (Local) | **VERIFIED & APPROVED (M2)** | Permissive streaming multipart parser for audio upload chunks. |
| **NumPy** | Array Computing | NumPy Developers | BSD-3-Clause | No | Zero (Local) | **VERIFIED & APPROVED (M2)** | Permissive numerical computing library used by CTranslate2. |
| **HTTPX** | HTTP Client | Encode | BSD-3-Clause | No | Zero (Local) | **VERIFIED & APPROVED (M2)** | Permissive HTTP client for testing and health verification. |
| **Google Gemini API** | Cloud ML Service | Google | Google API Terms of Service | No (Commercial allowed) | Paid / Rate-limited Free Tier | **REJECTED for Core Prototype** | Cloud dependency requiring API credentials; violates zero-cost and local-first requirements. |
| **OpenAI API (GPT-4 / Whisper API)** | Cloud ML Service | OpenAI | OpenAI API Terms of Service | No | Paid | **REJECTED** | Paid cloud API; strictly excluded. |
| **spaCy Models (`en_core_web_sm`)** | NLP Pipeline Weights | Explosion AI | MIT License | No | Zero (Local) | **Approved for NLP (Planned M3)** | Permissive MIT model for English tokenization and part-of-speech tagging. |
| **MediaPipe Holistic Task Models** | Vision MoCap Model Bundle | Google / MediaPipe Tasks | Apache-2.0 | No | Zero (Local CPU) | **VERIFIED & BENCHMARKED (M3.8)** | Offline pose, hand, and face landmark extraction model (`holistic_landmarker.task`, 13.6MB). Self-contained local execution; zero network calls. Verified at 5.0 FPS CPU inference. |
| **Argos Translate** | Offline Translation Engine | Argos Open Technologies | MIT License | No | Zero (Local) | **Approved for Translation** | Local neural machine translation engine. |

---

### 2.5 Fonts & Notation Systems

| Asset | Category | Source / Maintainer | Exact License | Approval Status | Usage & Redistribution Notes |
|---|---|---|---|---|---|
| **HamNoSys 4.0** | Notation System | IDGS, Universität Hamburg | Creative Commons Attribution 4.0 ([CC BY 4.0](https://www.sign-lang.uni-hamburg.de/dgs-korpus/tools/hamnosys)) | **Approved** | Phonetic sign notation specification. Free to use and adapt with attribution to IDGS. |
| **bgHamNoSysUnicode Font** | TrueType Font File | IDGS, Universität Hamburg | Academic / IDGS Distribution Terms | **Approved for Dev/Debug UI** | Academic use permitted. Upstream license file must accompany font redistribution. |

---

## 3. Summary of Licensing Status

1. **Permitted for Use (M1, M2 & M3.7 Implemented):**
   - Chrome Manifest V3 extension structure and floating panel CSS concepts (MIT, from Kozha).
   - Adobe Mixamo `ybot.glb` rig geometry and skeleton (royalty-free under Adobe terms for 3D applications).
   - `faster-whisper`, CTranslate2, and OpenAI Whisper model weights (`tiny.en`, `base.en`) (MIT).
   - FastAPI, Uvicorn, NumPy, python-multipart, HTTPX (MIT / BSD-3-Clause / Apache-2.0).
   - Three.js WebGL library (MIT).
   - HamNoSys 4.0 notation specification (CC BY 4.0).
   - DictaSign BSL/LSF sign corpus for non-commercial integration tests (CC BY-NC-SA 3.0).
   - **ISLRTC Indian Sign Language Dictionary & `ISL_NAMASTE_CLIP` (`isl_namaste_godl_v1`)** (Government Open Data License - India, GODL via data.gov.in). Permitted for adaptation, display, and distribution with attribution.

2. **Strictly Excluded:**
   - All source code from `yap_render_repo` (Unlicensed / All Rights Reserved).
   - All source code from `GenASL` (GPLv3 copyleft contamination).
   - Unlicensed ISL SiGML corpus from Kozha (`Indian_SL.sigml`).
   - ASL-LEX 2.0 reference videos (proprietary media, no redistribution rights).
   - All paid or cloud-hosted AI APIs (OpenAI, Gemini).
   - Unlicensed community corpora (NGT, Kurdish, Algerian, Bangla, Vietnamese).

3. **Current Asset Status & Next Step:**
   - **Milestone M3.7 Vertical Slice Achieved:** The first canonical, permissively licensed Indian Sign Language sign (`NAMASTE`, `isl_namaste_godl_v1`) is implemented and verified on the Mixamo rig under GODL.
   - **Broader ISL Vocabulary Strategy:** Broad-scale ISL animation cannot be manually authored bone-by-bone. The recommended architectural next step is an automated offline pipeline applying MediaPipe Holistic / SignPose to lift 3D joint rotations from the 10,000 official ISLRTC dictionary video clips (under GODL) into canonical Mixamo skeletal keyframe clips, followed by Deaf-native community panel review.
