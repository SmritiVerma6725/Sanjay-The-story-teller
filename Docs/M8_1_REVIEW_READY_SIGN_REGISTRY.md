# SignBridge M8.1 — Review-Ready Vocabulary Register & Authoritative Source Audit

**Document Reference:** `Docs/M8_1_REVIEW_READY_SIGN_REGISTRY.md`  
**Milestone:** SignBridge M8.1 (Review-Ready Vocabulary Expansion)  
**Execution Date:** October 21, 2026  
**Auditor:** Antigravity Autonomous Pair Programming Agent  
**Status:** **`REVIEW_READY_RECORDS_ESTABLISHED — IMPLEMENTATION_BLOCKED_PENDING_AUTHORITATIVE_SOURCE`**  

---

## 1. Authoritative Source Material Verification (Step 1)

This audit evaluates the evidentiary basis for expanding the sign library to include **`HELLO`** and **`THANK_YOU`**.

### Detailed Source Audit Matrix

| Evaluation Dimension | Sign: `HELLO` | Sign: `THANK_YOU` |
| :--- | :--- | :--- |
| **Exact Source Title** | *Indian Sign Language Dictionary (1st Edition 2018 / 2nd Edition 2019)* | *Indian Sign Language Dictionary (1st Edition 2018 / 2nd Edition 2019)* |
| **Publisher & Authority** | Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India, New Delhi. | Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India, New Delhi. |
| **Identified Entry / Citation** | Salutations / Everyday Greetings: "Hello" / "Greetings" | Social Expressions: "Thank You" / "Thanks" |
| **Stable Reference / URL** | `https://islrtc.nic.in` & `data.gov.in` metadata index | `https://islrtc.nic.in` & `data.gov.in` metadata index |
| **Physical Source Accessibility in Workspace** | **UNAVAILABLE LOCALLY**. While textual descriptions exist in the project seed lexicon (`isl_translator.js`), official raw ISLRTC video files, landmark coordinate streams, or motion-capture files for "Hello" have not been downloaded or imported into the workspace. | **UNAVAILABLE LOCALLY**. Textual gloss description exists in `isl_translator.js`, but official raw ISLRTC video files, landmark coordinate streams, or motion-capture files for "Thank You" have not been downloaded or imported into the workspace. |
| **Copyright & Licensing Status** | Official Indian government public datasets published on `data.gov.in` fall under the **Government Open Data License - India (GODL)**. However, per `LEGAL-01`, third-party YouTube footage is rights-uncleared for redistribution. | Same as HELLO: GODL terms apply to official raw portal data, but un-cleared third-party streams remain prohibited. |
| **Language Specificity (ISL vs. ASL/BSL)** | **ISL-SPECIFIC**. In urban ISL communities, casual "Hello" is signed with an open flat hand at the temple/chest curving outward. It is distinct from ASL informal wave and BSL two-handed greeting. Formal greetings in traditional contexts frequently default to NAMASTE. | **ISL-SPECIFIC**. Standard ISL sign starts at chin/mouth with flat hand and moves outward toward the addressee with slight forward head nod. |
| **Implementation Verdict** | **`BLOCKED_SOURCE_OR_REVIEW`** | **`BLOCKED_SOURCE_OR_REVIEW`** |

> [!IMPORTANT]
> **Core Governance Principle:**  
> In strict compliance with instructions: **"Do not claim that a sign follows an ISLRTC specification unless the corresponding source has actually been located and verified... If authoritative motion data is unavailable, leave the motion and animation asset unimplemented and mark the item BLOCKED_SOURCE_OR_REVIEW. Do not generate guessed keyframes."**
> 
> Because raw motion-capture or video assets for `HELLO` and `THANK_YOU` have not been ingested into the repository, **no guessed 3D animations have been fabricated**. The items are documented in review-ready structured records and held in safe neutral rest pose (`animationId: null`).

---

## 2. Review-Ready Sign Records (Step 2)

Structured machine-readable records are maintained in:
1. `Docs/records/sign_record_hello.json`
2. `Docs/records/sign_record_thank_you.json`

### Summary of Register Content

- **`HELLO`**:
  - Canonical Gloss: `HELLO`
  - Lemmas: `hello`, `hi`, `hey`, `greetings`
  - Planned Asset ID: `isl_hello_v1` (Target duration: 700 ms)
  - Target Rig: Adobe Mixamo Y-Bot (`ybot.glb`, 65–67 canonical bones)
  - Active Joints: `RightShoulder`, `RightArm`, `RightForeArm`, `RightHand`, `RightHandIndex1-4`, `Head`
  - Technical Status: **`BLOCKED_SOURCE_OR_REVIEW`**
  - Linguistic Status: **`AWAITING_DEAF_NATIVE_PANEL_EVALUATION (0/3 reviews)`**
  - Review Worksheet: [`Docs/ISL_HELLO_REVIEW_WORKSHEET.md`](file:///C:/Users/HP/OneDrive/Desktop/PROJECTS/Smriti_SignBridge/Docs/ISL_HELLO_REVIEW_WORKSHEET.md)

- **`THANK_YOU`**:
  - Canonical Gloss: `THANK_YOU`
  - Lemmas: `thank you`, `thanks`, `thank`
  - Planned Asset ID: `isl_thank_you_v1` (Target duration: 800 ms)
  - Target Rig: Adobe Mixamo Y-Bot (`ybot.glb`, 65–67 canonical bones)
  - Active Joints: `RightShoulder`, `RightArm`, `RightForeArm`, `RightHand`, `RightHandIndex1-4`, `Neck`, `Head`
  - Technical Status: **`BLOCKED_SOURCE_OR_REVIEW`**
  - Linguistic Status: **`AWAITING_DEAF_NATIVE_PANEL_EVALUATION (0/3 reviews)`**
  - Review Worksheet: [`Docs/ISL_THANK_YOU_REVIEW_WORKSHEET.md`](file:///C:/Users/HP/OneDrive/Desktop/PROJECTS/Smriti_SignBridge/Docs/ISL_THANK_YOU_REVIEW_WORKSHEET.md)

---

## 3. Technical Workflow & Safe Promotion Gates (Step 3)

The following safe infrastructure has been established:
1. **Metadata & Skeleton Validator:** [`tools/isl_motion_extraction/validate_sign_metadata.py`](file:///C:/Users/HP/OneDrive/Desktop/PROJECTS/Smriti_SignBridge/tools/isl_motion_extraction/validate_sign_metadata.py) validates record schemas and ensures declared active joints exist within `CANONICAL_BONES`.
2. **Promotion Gatekeeper:** Strictly prevents any sign from being labeled `IMPLEMENTED_VALIDATED` without a minimum of 3 independent, completed review records signed by qualified Deaf-native reviewers or certified interpreters.
3. **Quarantine Path:** Experimental animation files must reside in `extension/assets/animations/` and remain excluded from `keyframe_registry.js` default registration.
4. **Fallback Integrity:** In `extension/translation/isl_translator.js`, `HELLO` and `THANK_YOU` maintain `animationId: null`. Spoken occurrences trigger honest neutral fallback poses (500 ms) and report `0 playable clips (dictionary match awaiting review)`.

---

## 4. Preservation of Active Prototype (Step 4)

- **Namaste Motion (`isl_namaste_godl_v1`):** Unaltered and preserved.
- **Y-Bot Mesh (`ybot.glb`):** SHA-256 hash `B173DB980714113C91D14B2E0E6E1DD65978490392A7CCBFF5BBA17A38F9CED5` verified.
- **Candidate MoCap (`isl_namaste_mocap_candidate_v1.json`):** SHA-256 hash `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` quarantined.
- **Content Security Policy:** Strict CSP maintained without `'unsafe-inline'`.
- **Legal Hold Check:** Excluded reference video `ISLRTC_Namaste_sample.mp4` preserved under `LEGAL-01`.
