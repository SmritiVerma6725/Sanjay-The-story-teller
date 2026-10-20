# ISL Review Records Directory

This directory is the dedicated local storage location for genuine Indian Sign Language (ISL) evaluator review records exported from the SignBridge Review Studio (`tools/isl_motion_extraction/preview_mocap.html`).

## Review Record File Format
- Files should be exported JSON records conforming to `signbridge_review_schema_v1.0.0`.
- Filename convention: `ISL_Namaste_Review_<ReviewerName>_<YYYY-MM-DD>.json`.

## Audit & Evidence Integrity Rules
1. **Never fabricate records:** Only genuine reviews conducted with qualified Deaf-native signers, certified interpreters (DISLI/ISLRTC), or sign linguists may be stored here.
2. **Never modify imported records:** Review records are immutable audit evidence bound to the candidate's cryptographic SHA-256 hash.
3. **Validation:** Run `python tools/isl_motion_extraction/validate_review_record.py` to verify record schema, hash alignment, and completeness.
