# SignBridge M4 — Stage 2: Formal ISL Human Review Protocol

**Document Reference:** `Docs/M4_STAGE_2_HUMAN_REVIEW_PROTOCOL.md`  
**Milestone:** SignBridge M4 Stage 2 (ISL Coverage Audit & Review Protocol)  
**Execution Date:** October 20, 2026  
**Status:** **`HUMAN REVIEW PENDING — PROTOCOL ESTABLISHED — ZERO REVIEWS RECORDED`**  
**Auditor / Implementation Agent:** Antigravity Autonomous Pair Programming Auditor  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  
**Production Baseline:** `isl_namaste_godl_v1` (Active, Implemented, Unvalidated)  
**Quarantined Candidate:** `isl_namaste_mocap_candidate_v1` (`isLinguisticISL=false`, quarantined)  

---

## 1. Overview & Ethical Foundation

Sign languages are natural, autonomous linguistic systems possessing rich spatial grammars, phonological parameters, and cultural heritage. Indian Sign Language (ISL) is NOT a manual encoding of English or Hindi speech, and cannot be validated by automated heuristics, MediaPipe landmark confidence scores, or engineering self-assessments.

This protocol establishes the rigorous, ethical, and reproducible framework for conducting qualified human evaluations of candidate 3D sign animations before any candidate can be considered for production baseline promotion.

> [!IMPORTANT]
> **Anti-Fabrication Mandate:**
> Zero qualified human reviews have occurred to date. No reviewers, qualifications, consent signatures, or scoring records may be invented or fabricated. The official review status across all assets remains **`HUMAN REVIEW PENDING`**.

---

## 2. Reviewer Qualifications & Verification

To ensure linguistic integrity, evaluations must be conducted exclusively with qualified reviewers.

### A. Recognized Reviewer Categories:
1. **Category A — Deaf-Native / Primary Signer:**
   - Deaf individual who uses Indian Sign Language (ISL) as their primary everyday language.
   - Self-attested primary language status with community affiliation or regional Deaf association recognition.
2. **Category B — Certified ISL Interpreter:**
   - Professional possessing formal certification (e.g., Diploma in Indian Sign Language Interpretation [DISLI] or equivalent credentials recognized by the Rehabilitation Council of India / ISLRTC).
   - Minimum 2 years of active interpreting experience.
3. **Category C — Sign Language Linguist / Educator:**
   - Academic researcher, linguist, or educator with published research or formal teaching credentials in Indian Sign Language linguistics, phonology, or syntax.

### B. Qualification Recording & Privacy:
- Qualifications are recorded in the structured review record metadata (`reviewerRole`, `credentialAuthority`, `yearsExperienceCategory`).
- To safeguard participant privacy, reviewer personal identities are anonymized with consistent pseudonymous identifiers (e.g., `REV_ISL_A01`, `REV_ISL_B02`).
- Real-world contact information is stored strictly offline in an encrypted registry accessible only to authorized institutional compliance officers, never checked into version control.

---

## 3. Voluntary Participation & Informed Consent

Participation in SignBridge evaluations must be completely voluntary:
1. **Accessible Consent Presentation:**
   - Informed consent must be offered in accessible formats: a recorded ISL video briefing alongside plain-language written English and Hindi.
2. **Key Disclosures:**
   - The purpose of the study: technical evaluation of 3D avatar animations synthesized from motion-capture data.
   - Clarification that evaluation does not imply endorsement of the overall software.
   - Right to pause, skip items, or withdraw at any moment without penalty.
3. **Consent Archiving:**
   - Consent must be signed (digitally or physically) and verified before the review session commences.
   - The review record contains a boolean field `informedConsentObtained: true` alongside the consent document hash.

---

## 4. Multi-Parameter Linguistic Review Rubric

Reviewers evaluate candidate sign animations across six core linguistic parameters using a 1–5 Likert scale, accompanied by qualitative observations:

### Parameter 1: Handshape (Morphology)
- *Criteria:* Are the finger extensions, joint flexions, and thumb oppositions accurate to standard ISL lexical forms?
- *Common failure modes:* Splayed fingers, unnatural finger penetration, missing thumb contact, loose fist.

### Parameter 2: Palm & Finger Orientation
- *Criteria:* Are the palm faces and pointing vectors aligned correctly relative to the signer's body and addressee?
- *Common failure modes:* Inverted palms, wrong radial/ulnar orientation.

### Parameter 3: Movement (Kinematics & Dynamics)
- *Criteria:* Is the trajectory, path, speed, repetition, and acceleration natural and linguistically appropriate?
- *Common failure modes:* Robotic constant-velocity motion, abrupt snapping, exaggerated arm sweeps.

### Parameter 4: Location (Signing Space & Place of Articulation)
- *Criteria:* Is the sign articulated in the proper spatial location (e.g., sternum, chin, forehead, neutral space)?
- *Common failure modes:* Sign positioned too low (waist level) or too high, hands colliding or drifting.

### Parameter 5: Non-Manual Markers (NMM)
- *Criteria:* Where applicable, are head nods, head tilts, shoulder shifts, and eye gaze coordinated with manual movement?
- *Common failure modes:* Rigid head during respectful greetings, desynchronized head nod.

### Parameter 6: Overall Comprehensibility & Naturalness
- *Criteria:* Would a native ISL signer immediately recognize and understand this sign in context? Is it respectful and acceptable?

---

## 5. Allowed Review Verdicts

Each reviewer renders an overall categorical verdict:

1. **`ACCEPTABLE`**:
   - The animation accurately represents the ISL sign. Minor technical imperfections do not impede immediate comprehension or linguistic acceptability.
2. **`MINOR_ISSUE`**:
   - The sign is recognizable, but contains identifiable kinematic, timing, or handshape flaws that should be corrected before wide deployment.
3. **`UNACCEPTABLE`**:
   - The animation is linguistically incorrect, offensive, confusing, or fails to convey the intended ISL sign. Cannot be used in production.
4. **`NOT_ASSESSABLE`**:
   - The video or animation failed to play, rendering glitches obscured the motion, or the reviewer lacks sufficient regional context to render a fair judgment. Must be clearly distinguished from negative evaluations.

---

## 6. Disagreements, Uncertainty & Insufficient Evidence

- **Regional Lexical Variation:** ISL exhibits natural regional lexical variations (e.g., North vs. South dialects). If a reviewer notes a variant difference, this must be explicitly documented under `dialectOrRegionalNote`.
- **Handling Disagreements:** A candidate with mixed verdicts (e.g., 2 `ACCEPTABLE` and 1 `UNACCEPTABLE`) CANNOT be promoted automatically. The conflict must be reviewed by an expert panel or adjudication lead.
- **Request for Further Evidence:** Reviewers may flag `requestFurtherEvidence: true` if additional camera angles, slower playback, or context sentences are needed.

---

## 7. Cryptographic Binding to Candidate Hash

Every review record must be permanently, cryptographically bound to the exact candidate asset evaluated:
- **`candidateId`:** Matches the animation asset identifier (e.g., `isl_namaste_mocap_candidate_v1`).
- **`candidateSha256`:** The exact SHA-256 digest of the candidate JSON file (e.g., `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46`).
- **Validation Rule:** If the candidate JSON file changes by even a single byte, its hash will change, instantly invalidating prior reviews unless re-evaluated.

---

## 8. Anti-Fabrication & Review Integrity Safeguards

The automated test suite enforces strict validation rules on all imported review records:

1. **Anti-Self-Reporting:** Reviews authored by software engineers, developers, or automated scripts are rejected by the validator.
2. **Prohibition of Synthetic Records:** Any record generated by scripts or unit tests must reside strictly in temporary test directories; zero mock records may enter `tools/isl_motion_extraction/reviews/`.
3. **Read-Only Ingestion:** Validated review files in `reviews/` are treated as immutable legal evidence.
4. **Hash Mismatch Rejection:** `validate_review_record.py` automatically asserts that `candidateSha256` in the review matches the actual file on disk.

---

## 9. Review Ingestion & Storage Architecture

```
tools/isl_motion_extraction/
├── preview_mocap.html                 # Review Studio UI (interactive playback, scrubbing, rubric)
├── check_review_readiness.py          # Pre-session automated readiness diagnostic
├── validate_review_record.py          # Schema & hash validator
├── reviews/                           # Dedicated review record store
│   └── README.md                      # Audit directory guidelines (Current records: 0)
└── output/
    └── isl_namaste_mocap_candidate_v1.json (SHA-256: 6f24e6...)
```

### Review Record JSON Schema (`signbridge_review_schema_v1.0.0`):
```json
{
  "schemaVersion": "1.0.0",
  "reviewId": "REV_NAMASTE_20261020_001",
  "candidateId": "isl_namaste_mocap_candidate_v1",
  "candidateSha256": "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46",
  "reviewTimestamp": "2026-10-20T12:00:00Z",
  "reviewer": {
    "pseudonymId": "REV_ISL_A01",
    "qualificationCategory": "DEAF_NATIVE_SIGNER",
    "informedConsentObtained": true
  },
  "scores": {
    "handshape": 4,
    "orientation": 4,
    "movement": 4,
    "location": 5,
    "nonManualMarkers": 4,
    "comprehensibility": 4
  },
  "verdict": "ACCEPTABLE",
  "qualitativeFeedback": "Clear Anjali mudra and appropriate respectful nod.",
  "dialectOrRegionalNote": "Standard national ISLRTC variant.",
  "isSyntheticOrTestRecord": false
}
```

---

## 10. Status & Summary

- **Current Qualified Reviews on File:** **0**
- **Status of Mocap Candidate:** **`EXPERIMENTAL_QUARANTINED`**
- **Status of Production Baseline:** **`IMPLEMENTED_UNVALIDATED`**
- **Governance:** **`DRY_RUN_ONLY — ZERO OUTREACH DISPATCHED`**
