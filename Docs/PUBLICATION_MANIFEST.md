# SignBridge — Publication Manifest

**Document Reference:** `Docs/PUBLICATION_MANIFEST.md`  
**Milestone:** SignBridge Milestone M4 — Final Release Packaging & Publication  
**Execution Date:** October 20, 2026  
**Auditor:** Antigravity Autonomous Agent (Pair Programming Auditor)  
**Governance State:** **`DRY_RUN_ONLY — NOT_AUTHORIZED — ZERO EXTERNAL OUTREACH`**  

---

## 1. Publication Manifest Ledger

The following table itemizes all files and directories across the workspace, indicating their publication decision (`INCLUDE`, `EXCLUDE`, or `HOLD`) and technical rationale:

| Source Path | Destination Path | File Type | Purpose / Domain | Decision | Technical Rationale & Notes |
|---|---|---|---|:---:|---|
| `README.md` | `README.md` | Markdown | Master project documentation | **`INCLUDE`** | Completely updated with comprehensive M1–M4 Stage 5 documentation |
| `LICENSE` | `LICENSE` | Text | License & third-party terms | **`INCLUDE`** | Multi-licensed asset breakdown (MIT code, Adobe Y-Bot, GODL ISLRTC) |
| `.gitignore` | `.gitignore` | Configuration | Git ignore rules | **`INCLUDE`** | Comprehensive exclusions for models, videos, scratch files, profiles |
| `CONTRIBUTING.md` | `CONTRIBUTING.md` | Markdown | Contributor & governance guide | **`INCLUDE`** | Details local setup, test execution, and strict linguistic promotion gates |
| `SECURITY.md` | `SECURITY.md` | Markdown | Security policy & disclosure | **`INCLUDE`** | Defines local-first threat model and sanitized reporting procedures |
| `run_all_m3_tests.py` | `run_all_m3_tests.py` | Python Script | M3 master test runner | **`INCLUDE`** | Unifies 246 checks across 7 M3 sub-suites |
| `run_all_m4_stage1_tests.py` | `run_all_m4_stage1_tests.py` | Python Script | M4 Stage 1 test runner | **`INCLUDE`** | Executes message bridge contract and CDP browser smoke tests |
| `run_all_m4_stage2_tests.py` | `run_all_m4_stage2_tests.py` | Python Script | M4 Stage 2 test runner | **`INCLUDE`** | Executes ISL vocabulary inventory and promotion gate tests |
| `run_all_m4_stage3_tests.py` | `run_all_m4_stage3_tests.py` | Python Script | M4 Stage 3 test runner | **`INCLUDE`** | Executes performance benchmarks, memory bounds, and privacy tests |
| `run_all_m4_stage4_tests.py` | `run_all_m4_stage4_tests.py` | Python Script | M4 Stage 4 test runner | **`INCLUDE`** | Executes controlled pilot dry-run and readiness verification |
| `run_all_m4_stage5_tests.py` | `run_all_m4_stage5_tests.py` | Python Script | M4 Stage 5 master runner | **`INCLUDE`** | Master unified runner verifying all 340 checks across 7 suites |
| `run_chrome_tests.py` | `run_chrome_tests.py` | Python Script | In-engine Chrome test runner | **`INCLUDE`** | Automated WebGL test runner for Chrome extensions |
| `parse_seed_lexicon.py` | `parse_seed_lexicon.py` | Python Script | ISL seed lexicon parser | **`INCLUDE`** | Utility to parse and validate the 16 seed dictionary entries |
| `extension/` | `extension/` | Directory (MV3) | Chrome Extension frontend | **`INCLUDE`** | Manifest V3, background service worker, offscreen audio processor, popup UI |
| `extension/assets/models/ybot.glb` | `extension/assets/models/ybot.glb` | Binary 3D Mesh | Mixamo Y-Bot skeleton rig | **`INCLUDE`** | 2.2 MB character mesh used for WebGL avatar rendering |
| `extension/assets/animations/isl_namaste_mocap_candidate_v1.json` | `extension/assets/animations/isl_namaste_mocap_candidate_v1.json` | JSON Keyframes | Quarantined candidate animation | **`INCLUDE`** | Isolated experimental asset for review studio; excluded from production registry |
| `signbridge-backend/` | `signbridge-backend/` | Directory (Python) | Local ASR FastAPI backend | **`INCLUDE`** | FastAPI app, CTranslate2 faster-whisper service, models, and test fixtures |
| `signbridge-backend/test_speech_sample.wav` | `signbridge-backend/test_speech_sample.wav` | Audio (WAV) | Test audio fixture | **`INCLUDE`** | 230 KB test audio sample for backend integration tests |
| `signbridge-backend/.venv/` | N/A | Virtual Environment | Local Python environment | **`EXCLUDE`** | Excluded via `.gitignore` (machine-specific binaries) |
| `tests/` | `tests/` | Directory (Python) | Test suites for M4 Stages 1–5 | **`INCLUDE`** | Automated unit, contract, CDP browser, and validation tests |
| `benchmarks/` | `benchmarks/` | Directory | Benchmarking scripts & results | **`INCLUDE`** | Pipeline latency harness and machine-readable JSON result artifacts |
| `tools/m4_stage4_dry_run_simulator.py` | `tools/m4_stage4_dry_run_simulator.py` | Python Script | Pilot dry-run simulator | **`INCLUDE`** | 17-scenario dry-run execution harness |
| `tools/isl_motion_extraction/` | `tools/isl_motion_extraction/` | Directory | MoCap extraction & review | **`INCLUDE`** | MediaPipe retargeting scripts, Review Studio HTML, review validator |
| `tools/isl_motion_extraction/models/*.task` | N/A | ML Binary Models | Pretrained MediaPipe weights | **`EXCLUDE`** | Large binary models (13.6MB, 7.8MB, 5.7MB); downloadable via script |
| `tools/isl_motion_extraction/reference_videos/*.mp4` | N/A | Video (MP4) | Sample reference sign video | **`HOLD`** | Rights-uncleared YouTube video (`ISLRTC_Namaste_sample.mp4`); excluded per rule |
| `tools/isl_motion_extraction/reviews/` | `tools/isl_motion_extraction/reviews/` | Directory | Genuine review store | **`INCLUDE`** | Preserved completely empty (zero fake/synthetic reviews) |
| `Docs/` | `Docs/` | Directory | Authoritative documentation | **`INCLUDE`** | Complete collection of 25+ reports, audits, matrices, and pilot packages |
| `Docs/M4_STAGE_4_PILOT_PACKAGE/` | `Docs/M4_STAGE_4_PILOT_PACKAGE/` | Directory | 9-part pilot preparation package | **`INCLUDE`** | Facilitator guides, consent draft, worksheets, incident templates, schemas |
| `GenASL/` | N/A | Git Repo | Cloned reference candidate | **`EXCLUDE`** | Excluded via `.gitignore` (GPLv3 copyleft contamination risk) |
| `kozha_repo/` | N/A | Git Repo | Cloned reference candidate | **`EXCLUDE`** | Excluded via `.gitignore` (external reference repository) |
| `yap_render_repo/` | N/A | Git Repo | Cloned reference candidate | **`EXCLUDE`** | Excluded via `.gitignore` (unlicensed upstream repository) |
| `*.bmp` (Root bitmaps) | N/A | Bitmap Images | Raw desktop screenshots | **`EXCLUDE`** | Excluded via `.gitignore` (uncompressed 5.3MB desktop screen captures) |
| `scratch_*.py`, `crop_*.ps1`, `test_*.py` (Root) | N/A | Scripts | Temporary automation scripts | **`EXCLUDE`** | Excluded via `.gitignore` (superseded by standardized test suites) |
| Chrome Profiles (`.chrome_test_profile/`, etc.) | N/A | Directory | Browser user data | **`EXCLUDE`** | Excluded via `.gitignore` (ephemeral cookies and browser caches) |

---

## 2. Summary of Publication Metrics

- **Total Directories Included:** 6 (`extension/`, `signbridge-backend/`, `tests/`, `benchmarks/`, `tools/`, `Docs/`)
- **Total Master Scripts Included:** 8 (`run_all_m3_tests.py`, `run_all_m4_stage1_tests.py` through `run_all_m4_stage5_tests.py`, `run_chrome_tests.py`, `parse_seed_lexicon.py`)
- **Total Documentation Files Included:** 28+ Markdown and JSON specifications
- **Rights-Uncleared Video Assets Excluded:** 1 (`ISLRTC_Namaste_sample.mp4` on `HOLD`)
- **Large Pretrained Binary Models Excluded:** 3 (`holistic_landmarker.task`, `hand_landmarker.task`, `pose_landmarker.task`)
- **External Repositories Excluded:** 3 (`GenASL/`, `kozha_repo/`, `yap_render_repo/`)
- **Review Repository Status:** 100% Clean & Empty
