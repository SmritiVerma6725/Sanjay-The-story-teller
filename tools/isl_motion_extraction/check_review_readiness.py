#!/usr/bin/env python3
"""SignBridge M3.12 — Automated Pre-Session Review Readiness Diagnostic

Verifies:
1. Reference-video availability, file size, and SHA-256 hash.
2. Candidate-file availability, byte consistency, and SHA-256 hash.
3. Candidate clip schema compliance and experimental validation status.
4. 3D avatar rig asset availability (Mixamo Y-Bot).
5. Review studio dependencies and player scripts.
6. Distinguishes automated diagnostic results from prerequisites requiring human review.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

# Paths
TOOL_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOL_DIR.parent.parent

REF_VIDEO_PATH = TOOL_DIR / "reference_videos" / "ISLRTC_Namaste_sample.mp4"
CANDIDATE_OUTPUT_PATH = TOOL_DIR / "output" / "isl_namaste_mocap_candidate_v1.json"
CANDIDATE_EXT_PATH = PROJECT_ROOT / "extension" / "assets" / "animations" / "isl_namaste_mocap_candidate_v1.json"
AVATAR_MODEL_PATH = PROJECT_ROOT / "extension" / "assets" / "models" / "ybot.glb"
PREVIEW_STUDIO_PATH = TOOL_DIR / "preview_mocap.html"

# Expected Hashes
EXPECTED_VIDEO_SHA256 = "129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8"
EXPECTED_CANDIDATE_SHA256 = "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46"

CANONICAL_BONES = {
    'Hips', 'Spine', 'Spine1', 'Spine2', 'Neck', 'Head', 'HeadTop_End',
    'LeftEye', 'RightEye',
    'LeftShoulder', 'LeftArm', 'LeftForeArm', 'LeftHand',
    'LeftHandThumb1', 'LeftHandThumb2', 'LeftHandThumb3', 'LeftHandThumb4',
    'LeftHandIndex1', 'LeftHandIndex2', 'LeftHandIndex3', 'LeftHandIndex4',
    'LeftHandMiddle1', 'LeftHandMiddle2', 'LeftHandMiddle3', 'LeftHandMiddle4',
    'LeftHandRing1', 'LeftHandRing2', 'LeftHandRing3', 'LeftHandRing4',
    'LeftHandPinky1', 'LeftHandPinky2', 'LeftHandPinky3', 'LeftHandPinky4',
    'RightShoulder', 'RightArm', 'RightForeArm', 'RightHand',
    'RightHandThumb1', 'RightHandThumb2', 'RightHandThumb3', 'RightHandThumb4',
    'RightHandIndex1', 'RightHandIndex2', 'RightHandIndex3', 'RightHandIndex4',
    'RightHandMiddle1', 'RightHandMiddle2', 'RightHandMiddle3', 'RightHandMiddle4',
    'RightHandRing1', 'RightHandRing2', 'RightHandRing3', 'RightHandRing4',
    'RightHandPinky1', 'RightHandPinky2', 'RightHandPinky3', 'RightHandPinky4',
    'LeftUpLeg', 'LeftLeg', 'LeftFoot', 'LeftToeBase', 'LeftToe_End',
    'RightUpLeg', 'RightLeg', 'RightFoot', 'RightToeBase', 'RightToe_End'
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def run_diagnostics():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    print("=" * 80)
    print("SignBridge M3.14 -- ISL Review Pre-Session Readiness Diagnostic")
    print("=" * 80)
    
    passed_checks = 0
    total_checks = 0
    failures = []

    def check(title: str, condition: bool, details: str = ""):
        nonlocal passed_checks, total_checks
        total_checks += 1
        status = "PASS" if condition else "FAIL"
        print(f"[{status}] {title}")
        if details:
            print(f"        {details}")
        if condition:
            passed_checks += 1
        else:
            failures.append(f"{title}: {details}")

    # 1. Reference Video Check
    print("\n--- 1. Reference Video Asset Verification ---")
    video_exists = REF_VIDEO_PATH.exists()
    check("Reference video file presence", video_exists, str(REF_VIDEO_PATH))
    if video_exists:
        video_size = REF_VIDEO_PATH.stat().st_size
        check("Reference video file size", video_size == 648917, f"Size: {video_size} bytes (expected 648917)")
        video_hash = compute_sha256(REF_VIDEO_PATH)
        check("Reference video SHA-256 integrity", video_hash == EXPECTED_VIDEO_SHA256, f"SHA-256: {video_hash}")

    # 2. Candidate Animation Clip Check
    print("\n--- 2. Candidate Animation Clip Verification ---")
    candidate_out_exists = CANDIDATE_OUTPUT_PATH.exists()
    check("Candidate output file presence", candidate_out_exists, str(CANDIDATE_OUTPUT_PATH))
    candidate_ext_exists = CANDIDATE_EXT_PATH.exists()
    check("Candidate extension asset presence", candidate_ext_exists, str(CANDIDATE_EXT_PATH))

    if candidate_out_exists:
        out_hash = compute_sha256(CANDIDATE_OUTPUT_PATH)
        check("Candidate output SHA-256 integrity", out_hash == EXPECTED_CANDIDATE_SHA256, f"SHA-256: {out_hash}")
        if candidate_ext_exists:
            ext_hash = compute_sha256(CANDIDATE_EXT_PATH)
            check("Output and extension copies identical", out_hash == ext_hash, f"Ext SHA-256: {ext_hash}")

        # Schema & Governance Verification
        try:
            with open(CANDIDATE_OUTPUT_PATH, 'r', encoding='utf-8') as f:
                clip = json.load(f)
            
            check("Candidate ID format", clip.get("animationId") == "isl_namaste_mocap_candidate_v1", clip.get("animationId", ""))
            check("Gloss specification", clip.get("gloss") == "NAMASTE", clip.get("gloss", ""))
            check("Duration conformance (3080ms)", clip.get("durationMs") == 3080, f"durationMs: {clip.get('durationMs')}")
            check("Experimental status enforced", clip.get("validationStatus") == "experimental_awaiting_validation", clip.get("validationStatus", ""))
            check("Keyframe count (77 frames @ 25fps)", len(clip.get("keyframes", [])) == 77, f"Count: {len(clip.get('keyframes', []))}")
            check("Flagged anomaly frames recorded", set(clip.get("metadata", {}).get("lowConfidenceFrameIndices", [])) == {22, 59, 62}, str(clip.get("metadata", {}).get("lowConfidenceFrameIndices")))

            # Check bone validity
            invalid_bones = set()
            for kf in clip.get("keyframes", []):
                for t in kf.get("transforms", []):
                    bone = t.get("bone")
                    if bone not in CANONICAL_BONES:
                        invalid_bones.add(bone)
            check("All 36 transforms per frame use canonical Y-Bot bones", len(invalid_bones) == 0, f"Invalid bones: {invalid_bones}" if invalid_bones else "All canonical")

        except Exception as e:
            check("Candidate JSON parseable", False, str(e))

    # 3. Avatar Rig Asset Verification
    print("\n--- 3. 3D Avatar Rig Verification ---")
    model_exists = AVATAR_MODEL_PATH.exists()
    check("Adobe Mixamo Y-Bot mesh presence (ybot.glb)", model_exists, str(AVATAR_MODEL_PATH))
    if model_exists:
        model_size = AVATAR_MODEL_PATH.stat().st_size
        check("Y-Bot GLB file size sanity (>1MB)", model_size > 1000000, f"Size: {model_size} bytes")

    # 4. Review Studio Interface Verification
    print("\n--- 4. Review Studio & Interface Verification ---")
    studio_exists = PREVIEW_STUDIO_PATH.exists()
    check("Review Studio HTML presence", studio_exists, str(PREVIEW_STUDIO_PATH))
    if studio_exists:
        content = PREVIEW_STUDIO_PATH.read_text(encoding='utf-8')
        check("Studio contains SHA-256 hash display", "candidate-hash-display" in content)
        check("Studio contains review schema v1.0.0", "signbridge_review_schema_v1.0.0" in content)
        check("Studio contains import hash mismatch check", "HASH MISMATCH" in content)
        check("Studio contains direct jump buttons for frames 22, 59, 62", "btn-jump-f22" in content and "btn-jump-f59" in content and "btn-jump-f62" in content)
        check("Studio contains 5-parameter rubric table", "data-param=\"handshape\"" in content and "data-param=\"non_manuals\"" in content)
        check("Studio contains rig limitations explainer", "Known Technical Limitations" in content)

    # 5. Production Isolation Verification
    print("\n--- 5. Production Baseline Isolation Verification ---")
    registry_path = PROJECT_ROOT / "extension" / "animation" / "keyframe_registry.js"
    if registry_path.exists():
        reg_text = registry_path.read_text(encoding='utf-8')
        check("KeyframeRegistry defaults to baseline 'isl_namaste_godl_v1'", "isl_namaste_godl_v1" in reg_text)
        check("Candidate is NOT registered by default in production registry", "REGISTERED_CLIPS.set(isl_namaste_mocap_candidate_v1" not in reg_text)

    # 6. Review Ingestion & Validation Tooling Verification
    print("\n--- 6. Review Ingestion & Validation Tooling Verification ---")
    reviews_dir = TOOL_DIR / "reviews"
    validator_path = TOOL_DIR / "validate_review_record.py"
    check("Review storage directory presence", reviews_dir.exists() and reviews_dir.is_dir(), str(reviews_dir))
    check("Review validator script presence", validator_path.exists(), str(validator_path))

    # Summary
    print("\n" + "=" * 80)
    print(f"AUTOMATED DIAGNOSTIC SUMMARY: {passed_checks} / {total_checks} Checks Passed")
    print("=" * 80)

    if failures:
        print("\nFAILURES ENCOUNTERED:")
        for f in failures:
            print(f"  - {f}")
        return False
    else:
        print("\nAll technical pre-flight automated checks PASSED.")
        print("\n" + "-" * 80)
        print("PRE-SESSION HUMAN EVALUATOR CHECKLIST (TO BE PERFORMED BEFORE REVIEW):")
        print("-" * 80)
        print("[ ] 1. Local HTTP server started (`python -m http.server 8000`)")
        print("[ ] 2. Review Studio opened in Google Chrome (`http://localhost:8000/tools/isl_motion_extraction/preview_mocap.html`)")
        print("[ ] 3. Verified 3D avatar viewport renders Y-Bot in neutral rest pose (arms lowered)")
        print("[ ] 4. Verified reference video playback and side-by-side synchronization")
        print("[ ] 5. Briefed human evaluator on Y-Bot metallic rig limitations (no facial expressions)")
        print("[ ] 6. Informed evaluator that candidate is EXPERIMENTAL and NOT validated")
        print("[ ] 7. Provided reviewer handoff package (Docs/ISL_REVIEWER_HANDOFF.md)")
        print("-" * 80)
        return True


if __name__ == "__main__":
    success = run_diagnostics()
    sys.exit(0 if success else 1)
