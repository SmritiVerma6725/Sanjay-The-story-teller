# SignBridge M3 — Final Evidence Artifact Index

**Document Reference:** `Docs/M3_FINAL_EVIDENCE_INDEX.md`  
**Milestone:** SignBridge Milestone M3 — Complete End-to-End Closure  
**Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  

---

## 1. Overview & Verification Summary

This index catalogues all empirical evidence files, captured Chrome artifacts, cryptographic checksums, test harnesses, and governance reports within the repository. Every path represents a real file verified from disk.

---

## 2. Institutional Contact Verification Artifacts

All files reside in [`Docs/evidence/m3_23_chrome_verification/`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/):

| Target ID | Institution | Verified Contact Channel | Evidence Artifact Paths | File Size | Verification Status |
|:---:|:---|:---|:---|:---:|:---:|
| **TGT-001** | **ISLRTC** | `islrtcnewdelhi@gmail.com` | [`TGT-001_ISLRTC_contact.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.dom.html)<br>[`TGT-001_ISLRTC_contact.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-001_ISLRTC_contact.png) | 102,902 B<br>136,172 B | **`VERIFIED_ON_OFFICIAL_SITE`**<br>(DOM line 503) |
| **TGT-002** | **NAD India** | `secretary@nadindia.org` | [`TGT-002_NAD_contact.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.dom.html)<br>[`TGT-002_NAD_contact.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-002_NAD_contact.png) | 102,552 B<br>642,841 B | **`PROPOSED_FOR_OWNER_APPROVAL`**<br>(DOM line 891; replaced unlisted Gmail) |
| **TGT-003** | **AIFD** | `aifdeaf@gmail.com` | [`TGT-003_aifdeaf_contact.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-003_aifdeaf_contact.dom.html)<br>[`TGT-003_aifdeaf_contact.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-003_aifdeaf_contact.html)<br>[`TGT-003_aifdeaf_contact.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-003_aifdeaf_contact.png) | 138,031 B<br>137,113 B<br>83,607 B | **`VERIFIED_ON_ACTIVE_DOMAIN`**<br>(HTML line 644; PNG captured) |
| **TGT-004** | **DEF** | `info@def.org.in` | [`TGT-004_DEF_contact.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-004_DEF_contact.html)<br>[`TGT-004_def.org.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-004_def.org.png) | 85,584 B<br>72,674 B | **`VERIFIED_ON_OFFICIAL_SITE`**<br>(HTML line 638) |
| **TGT-005** | **IGNOU SOH** | `soh@ignou.ac.in` | [`TGT-005_IGNOU_home.dom.html`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.dom.html)<br>[`TGT-005_IGNOU_home.png`](file:///c:/AmazonMlChallenge/Docs/evidence/m3_23_chrome_verification/TGT-005_IGNOU_home.png) | 125,767 B<br>562,450 B | **`NEEDS_OWNER_ROUTING_REVIEW`**<br>(Legacy page 404s; address absent from root DOM) |

---

## 3. Cryptographic Provenance & Core Motion Assets

| Asset Description | Repository File Path | File Size | Verified SHA-256 Checksum | Operational Role |
|:---|:---|:---:|:---:|:---|
| **Reference Video (ISLRTC Namaste)** | [`tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4) | 648,917 B | `129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8` | Ground truth reference video for local studio comparison; redistribution rights **UNRESOLVED**. |
| **Candidate MoCap Clip (Output)** | [`tools/isl_motion_extraction/output/isl_namaste_mocap_candidate_v1.json`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/output/isl_namaste_mocap_candidate_v1.json) | 528,122 B | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | Evaluated motion-capture reconstruction; quarantined from default registration. |
| **Candidate Extension Copy Asset** | [`extension/assets/animations/isl_namaste_mocap_candidate_v1.json`](file:///c:/AmazonMlChallenge/extension/assets/animations/isl_namaste_mocap_candidate_v1.json) | 528,122 B | `6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46` | Bit-for-bit identical copy of candidate clip bundled in extension assets. |
| **Production Baseline Clip** | [`extension/animation/keyframe_registry.js`](file:///c:/AmazonMlChallenge/extension/animation/keyframe_registry.js#L373) | Inline JS | Defined in code as `isl_namaste_godl_v1` | Active production baseline sign (GODL licensed, Anjali Mudra prayer pose). |
| **3D Avatar Mesh Asset** | [`extension/assets/models/ybot.glb`](file:///c:/AmazonMlChallenge/extension/assets/models/ybot.glb) | 2,233,440 B | Standard Adobe Mixamo Y-Bot mesh | Articulated 67-joint humanoid skeleton; rigid metallic face without facial bones. |

---

## 4. Test Suites & Verification Tooling

| Tool / Test Harness | Path | Description | Checks Run |
|:---|:---|:---|:---:|
| **Master Test Runner** | [`run_all_m3_tests.py`](file:///c:/AmazonMlChallenge/run_all_m3_tests.py) | Master orchestrator running all 7 suites without double-counting | **246** |
| **Unit Test Suite** | [`tools/isl_motion_extraction/tests/`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/tests/) | 5 unit test modules covering governance, retargeting, readiness, and validator | **60** |
| **Browser Usability Suite** | [`tools/isl_motion_extraction/tests/test_browser_usability.py`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/tests/test_browser_usability.py) | Headless Chrome CDP automation exercising `preview_mocap.html` end-to-end | **15** |
| **Pre-Flight Diagnostic** | [`tools/isl_motion_extraction/check_review_readiness.py`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/check_review_readiness.py) | Comprehensive pre-session asset, schema, and rig diagnostic | **27** |
| **Review Ingestion Validator**| [`tools/isl_motion_extraction/validate_review_record.py`](file:///c:/AmazonMlChallenge/tools/isl_motion_extraction/validate_review_record.py) | Standalone validator ensuring review records match candidate hash and schema | **1** |
| **Local Backend Test Suite** | [`signbridge-backend/test_backend.py`](file:///c:/AmazonMlChallenge/signbridge-backend/test_backend.py) | Integration test suite for local Faster-Whisper FastAPI speech recognition service | **8** |
| **Chrome In-Engine Runner** | [`run_chrome_tests.py`](file:///c:/AmazonMlChallenge/run_chrome_tests.py) | Headless Chrome Mocha/Chai WebGL in-engine test runner (`19 + 113` tests) | **132** |

---

## 5. Milestone Governance Reports (M3.19 – M3.26)

| Milestone | Report Path | Core Topic |
|:---|:---|:---|
| **M3.19** | [`Docs/ISL_REVIEWER_INVITATION.md`](file:///c:/AmazonMlChallenge/Docs/ISL_REVIEWER_INVITATION.md) | Initial reviewer recruitment & consent protocols |
| **M3.20** | [`Docs/M3_20_OUTREACH_STATUS_REPORT.md`](file:///c:/AmazonMlChallenge/Docs/M3_20_OUTREACH_STATUS_REPORT.md) | Outreach tracking table and contact candidate preparation |
| **M3.21** | [`Docs/M3_21_OUTREACH_AUTHORIZATION.md`](file:///c:/AmazonMlChallenge/Docs/M3_21_OUTREACH_AUTHORIZATION.md) | Initial authorization gates and response tracker |
| **M3.22** | [`Docs/M3_22_OUTREACH_REPORT.md`](file:///c:/AmazonMlChallenge/Docs/M3_22_OUTREACH_REPORT.md) | Recipient matrix preparation across five institutions |
| **M3.23** | [`Docs/M3_23_CHROME_VERIFICATION_REPORT.md`](file:///c:/AmazonMlChallenge/Docs/M3_23_CHROME_VERIFICATION_REPORT.md) | First-pass Chrome browser verification of institutional sites |
| **M3.24** | [`Docs/M3_24_UPDATE_REPORT.md`](file:///c:/AmazonMlChallenge/Docs/M3_24_UPDATE_REPORT.md) | Contact updates, DNS failure handling, and draft revisions |
| **M3.25** | [`Docs/M3_25_FINAL_READINESS_AUDIT.md`](file:///c:/AmazonMlChallenge/Docs/M3_25_FINAL_READINESS_AUDIT.md) | Final readiness audit, 4D contact matrix, standardized draft text |
| **M3.26** | [`Docs/M3_26_INDEPENDENT_AUDIT.md`](file:///c:/AmazonMlChallenge/Docs/M3_26_INDEPENDENT_AUDIT.md) | Independent evidence audit, test reconciliation, gap register |
