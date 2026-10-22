# SignBridge M5 — Dataset and Authorized Resources Audit

## 1. Executive Summary & Objective

Milestone M5 investigates lawful, authentic Indian Sign Language (ISL) resources to support continuous English-to-ISL translation and 3D avatar articulation. 

### Core Ethical & Linguistic Mandates
1. **Spoken English $\ne$ Indian Sign Language:** English and ISL operate on fundamentally different grammars (SVO vs. SOV/Topic-Comment). Word-for-word token substitution is linguistically invalid.
2. **Strict Prohibition on Language Conflation:** Neither ASL (American Sign Language) nor DGS (German Sign Language) may be substituted for ISL.
3. **Strict Licensing Governance:** Licensing terms must be verified against primary legal documents. Public web availability does not constitute a license to scrape, train, or redistribute.
4. **Zero Synthetic / Fabricated Signs:** Unanimated or unsupported words must hold a neutral rest pose pending verified reference data.

---

## 2. Resource Evaluation Register

### 2.1 Official ISLRTC ISL Dictionary (Volumes 1–3)
- **Publishing Authority:** Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities, Ministry of Social Justice and Empowerment, Government of India.
- **Access Portal:** Published via official portal and `data.gov.in`.
- **Modality & Content:** ~10,000 isolated video demonstrations (MP4) across Volume 1 (3,000 entries), Volume 2 (3,000 entries), and Volume 3 (4,000 entries).
- **Alignment:** Word/Concept level (English Lemma $\leftrightarrow$ Hindi translation $\leftrightarrow$ Single isolated ISL sign video).
- **Licensing:** **Government Open Data License - India (GODL)**.
  - *Permitted:* Royalty-free, worldwide, non-exclusive license to use, adapt, and build upon data for commercial or non-commercial purposes.
  - *Conditions:* Mandatory attribution: `"Source: Indian Sign Language Research and Training Centre (ISLRTC), via data.gov.in under GODL"`. Must not claim endorsement or misrepresent government agency affiliation.
- **Translation Suitability:** **LEXICAL ONLY**. Does NOT contain aligned continuous parallel English-to-ISL sentences, spatial syntax transitions, or discourse markers.
- **Animation Suitability:** **EXCELLENT FOR MOTION RETARGETING**. Ground-truth videos can be processed via MediaPipe Holistic or markerless pose extraction to derive humanoid keyframes (e.g., benchmark `isl_namaste_godl_v1`).
- **Hardware & Storage Requirements:** ~85 GB raw video storage; CPU/GPU for 30 FPS landmarker extraction.

### 2.2 INCLUDE Dataset (IIT Madras)
- **Source:** Sridhar et al., ACM Multimedia 2020 (*"INCLUDE: A Large Scale Dataset for Indian Sign Language Recognition"*).
- **Modality & Content:** 4,287 video clips covering 263 isolated word classes performed by 7 native/fluent signers.
- **Licensing:** **CC-BY-NC 4.0 (Research Only)**. Commercial redistribution or incorporation into commercial products is prohibited.
- **Translation Suitability:** **UNSUITABLE**. Designed purely for isolated Sign Language Recognition (SLR), not English-to-ISL sequence translation.
- **Animation Suitability:** **POOR TO MARGINAL**. Videos contain varying lighting, camera angles, and lack depth calibration.

### 2.3 CISLR / Continuous ISL Research Corpora (Academic)
- **Curators:** Academic research groups (e.g. IIIT Hyderabad, IIT Ropar).
- **Modality & Content:** Small-scale laboratory-recorded continuous sentence videos (typically 100 to 500 domain-restricted sentences, e.g. agricultural queries, railway announcements).
- **Licensing:** **Restricted Academic Access**. Available only upon signed institutional data-sharing agreements; redistribution strictly barred.
- **Translation Suitability:** **HIGHLY DOMAIN-CONSTRAINED**. Insufficient sample diversity to train generalized NLP sequence-to-sequence translation models.

### 2.4 International Benchmarks (PHOENIX-Weather 2014T, How2Sign)
- **PHOENIX 2014T:** German Sign Language (DGS).
- **How2Sign:** American Sign Language (ASL).
- **Audit Finding:** **STRICTLY EXCLUDED**. Using ASL or DGS models or glosses for Indian Sign Language is linguistically invalid and explicitly prohibited by PRD Section 3.

---

## 3. Data Readiness Assessment & Model Strategy

| Dimension | Current Finding | Engineering Recommendation |
| :--- | :--- | :--- |
| **English-to-ISL Parallel Sentences** | No open-source, large-scale, licensed parallel sentence corpus currently exists for ISL. | **Do NOT initiate expensive transformer training.** Retain a modular, replaceable rule-based translation interface (`SignBridgeTranslationRouter`) with honest fallback. |
| **Isolated Lexical Ground Truth** | ISLRTC Dictionary (~10,000 words under GODL) is legally authorized and high-quality. | Use ISLRTC GODL videos for incremental sign motion extraction, requiring 3/3 qualified Deaf-native panel reviews prior to production promotion. |
| **Model Pretraining Feasibility** | No pre-existing Hugging Face / PyTorch English-to-ISL gloss checkpoint exists under commercial/open licensing. | Avoid placeholder ML models that hallucinate incorrect glosses. |

---

## 4. Conclusion & Next Steps
1. The translation layer must remain a **strictly governed rule-based and phrase-level router** that reports unsupported vocabulary honestly.
2. Motion extraction must expand exclusively using authorized **ISLRTC GODL** source videos.
3. Every new sign must follow the documented 5-parameter Deaf-native evaluation protocol ([`Docs/M4_STAGE_2_HUMAN_REVIEW_PROTOCOL.md`](M4_STAGE_2_HUMAN_REVIEW_PROTOCOL.md)) before promotion from `UNANIMATED_SUPPORTED_ENTRY` to `IMPLEMENTED_UNVALIDATED`.
