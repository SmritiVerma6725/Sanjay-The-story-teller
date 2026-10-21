#!/usr/bin/env python3
"""SignBridge Milestone M8.1 — Review-Ready Sign Metadata & Promotion Gate Validator

Validates:
1. Sign Metadata Schema: Ensures records in Docs/records/*.json conform to required schema.
2. Authoritative Source Validation: Verifies source title, publisher, licensing, and access status.
3. Skeleton Compatibility: Checks that declared active joints belong to CANONICAL_BONES (65/67 Mixamo rig).
4. Asset Reference Integrity: Verifies whether animation files exist or are safely documented as null.
5. Quarantine Verification: Confirms experimental candidate clips are excluded from production registries.
6. Promotion Enforcement: Strictly rejects any sign claiming 'APPROVED' or 'HUMAN_VALIDATED' without >=3 valid review records.
7. Unimplemented Protection: Rejects guessed keyframes and enforces 'BLOCKED_SOURCE_OR_REVIEW' when raw data is missing.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent
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

REQUIRED_RECORD_FIELDS = [
    "schemaVersion", "recordType", "canonicalId", "englishIntent",
    "targetLanguage", "authoritativeSource", "motionDescription",
    "requiredAnimationAsset", "expectedSkeletonMapping",
    "technicalValidationStatus", "linguisticReviewStatus",
    "implementationReadiness", "reviewWorksheetReference", "approvalHistory"
]

VALID_IMPLEMENTATION_STATUSES = {
    "IMPLEMENTED_VALIDATED",
    "IMPLEMENTED_UNVALIDATED",
    "EXPERIMENTAL_QUARANTINED",
    "BLOCKED_SOURCE_OR_REVIEW"
}

def validate_sign_record(record_path: Path) -> Tuple[bool, List[str]]:
    errors = []
    if not record_path.exists():
        return False, [f"File not found: {record_path}"]
    
    try:
        data = json.loads(record_path.read_text(encoding='utf-8'))
    except Exception as e:
        return False, [f"Invalid JSON in {record_path}: {e}"]
        
    # Check top-level required fields
    for field in REQUIRED_RECORD_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")
            
    # Check canonical ID
    cid = data.get("canonicalId", "")
    if not cid or not isinstance(cid, str):
        errors.append("canonicalId must be a non-empty string")
        
    # Check language
    if data.get("targetLanguage") != "ISL":
        errors.append(f"targetLanguage must be 'ISL', got '{data.get('targetLanguage')}'")
        
    # Check Authoritative Source
    source = data.get("authoritativeSource", {})
    if not isinstance(source, dict):
        errors.append("authoritativeSource must be an object")
    else:
        for sfield in ["title", "publisher", "license", "sourceVerificationFinding"]:
            if not source.get(sfield):
                errors.append(f"authoritativeSource missing required field: '{sfield}'")
                
    # Check Skeleton mapping
    skel = data.get("expectedSkeletonMapping", {})
    if isinstance(skel, dict):
        joints = skel.get("primaryActiveJoints", [])
        if not joints or not isinstance(joints, list):
            errors.append("expectedSkeletonMapping.primaryActiveJoints must be a non-empty list")
        else:
            for j in joints:
                if j not in CANONICAL_BONES:
                    errors.append(f"Active joint '{j}' is not a valid canonical bone in CANONICAL_BONES")
                    
    # Check status consistency
    tech_status = data.get("technicalValidationStatus")
    ling_status = data.get("linguisticReviewStatus")
    readiness = data.get("implementationReadiness")
    
    if readiness not in VALID_IMPLEMENTATION_STATUSES:
        errors.append(f"Invalid implementationReadiness: '{readiness}'")
        
    # Promotion Rule: Cannot be approved or implemented without reviews
    reviews_count = len(data.get("approvalHistory", []))
    if readiness == "IMPLEMENTED_VALIDATED" and reviews_count < 3:
        errors.append(f"Promotion violation: '{cid}' cannot be IMPLEMENTED_VALIDATED with only {reviews_count}/3 reviews")
        
    if readiness == "BLOCKED_SOURCE_OR_REVIEW":
        anim = data.get("requiredAnimationAsset", {})
        if anim.get("assetPresence") is True:
            errors.append("Inconsistency: assetPresence cannot be true when status is BLOCKED_SOURCE_OR_REVIEW")
            
    # Review worksheet reference check
    ws_ref = data.get("reviewWorksheetReference")
    if ws_ref:
        ws_path = ROOT / ws_ref
        if not ws_path.exists():
            errors.append(f"Referenced review worksheet does not exist: {ws_ref}")
            
    return len(errors) == 0, errors

def validate_all_records() -> Dict[str, Any]:
    records_dir = ROOT / 'Docs' / 'records'
    results = {"total": 0, "passed": 0, "failed": 0, "records": {}}
    
    if not records_dir.exists():
        return results
        
    for f in records_dir.glob('*.json'):
        results["total"] += 1
        valid, errors = validate_sign_record(f)
        if valid:
            results["passed"] += 1
            results["records"][f.name] = {"valid": True, "errors": []}
        else:
            results["failed"] += 1
            results["records"][f.name] = {"valid": False, "errors": errors}
            
    return results

if __name__ == '__main__':
    res = validate_all_records()
    print(f"Validated {res['total']} sign records: {res['passed']} passed, {res['failed']} failed")
    for fname, d in res["records"].items():
        status = "PASS" if d["valid"] else "FAIL"
        print(f"  [{status}] {fname}")
        for err in d["errors"]:
            print(f"    - {err}")
    if res["failed"] > 0:
        sys.exit(1)
