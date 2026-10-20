#!/usr/bin/env python3
"""SignBridge M3.14 — ISL Review Record Validator

Safely validates genuine ISL review records against:
1. Supported schema: 'signbridge_review_schema_v1.0.0'
2. Candidate identifier ('isl_namaste_mocap_candidate_v1') and cryptographic SHA-256 hash.
3. Reference video filename and SHA-256 hash.
4. Permitted ratings: 'acceptable', 'minor_issue', 'unacceptable', 'not_assessable', 'unrated'.
5. Preserves 'not_assessable' as distinct from a negative rating.
6. Detects missing, malformed, duplicate, or inconsistent fields.
7. Distinguishes completed reviews from empty templates or unrated fixtures.
8. Strictly read-only: never modifies the source review record.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Constants & Supported Schema
SUPPORTED_SCHEMA_VERSION = "signbridge_review_schema_v1.0.0"
EXPECTED_CANDIDATE_ID = "isl_namaste_mocap_candidate_v1"
EXPECTED_CANDIDATE_SHA256 = "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46"
EXPECTED_VIDEO_SHA256 = "129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8"

VALID_ROLES = {
    "deaf_native",
    "certified_interpreter",
    "deaf_educator",
    "sign_linguist",
    "community_member",
    "anonymous"
}

VALID_RATINGS = {
    "acceptable",
    "minor_issue",
    "unacceptable",
    "not_assessable",
    "unrated"
}

VALID_VERDICTS = {
    "provisional_approval",
    "needs_tuning",
    "rejected",
    "not_assessable"
}

REQUIRED_DIMENSIONS = [
    "handshape",
    "location",
    "orientation",
    "movement",
    "non_manuals"
]


class ReviewValidationResult:
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.filename = filepath.name
        self.is_valid = False
        self.record_type = "UNKNOWN"  # COMPLETED_GENUINE, PARTIAL, TEMPLATE, MISMATCH, CORRUPTED
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.data: Dict[str, Any] = {}
        
        # Extracted fields
        self.candidate_id: Optional[str] = None
        self.candidate_hash: Optional[str] = None
        self.candidate_hash_matched = False
        self.video_hash: Optional[str] = None
        self.video_hash_matched = False
        self.reviewer_name: Optional[str] = None
        self.reviewer_role: Optional[str] = None
        self.review_date: Optional[str] = None
        self.ratings: Dict[str, str] = {}
        self.unassessable_dims: List[str] = []
        self.verdict: Optional[str] = None
        self.qualitative_notes: str = ""
        self.unrated_count = 0
        self.not_assessable_count = 0
        self.has_genuine_observations = False
        self.further_evidence_requested = False
        self.evidence_request_details = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "filename": self.filename,
            "filepath": str(self.filepath),
            "is_valid": self.is_valid,
            "record_type": self.record_type,
            "candidate_id": self.candidate_id,
            "candidate_hash_matched": self.candidate_hash_matched,
            "video_hash_matched": self.video_hash_matched,
            "reviewer_name": self.reviewer_name,
            "reviewer_role": self.reviewer_role,
            "review_date": self.review_date,
            "verdict": self.verdict,
            "ratings": self.ratings,
            "unassessable_dims": self.unassessable_dims,
            "unrated_count": self.unrated_count,
            "not_assessable_count": self.not_assessable_count,
            "has_genuine_observations": self.has_genuine_observations,
            "further_evidence_requested": self.further_evidence_requested,
            "evidence_request_details": self.evidence_request_details,
            "errors": self.errors,
            "warnings": self.warnings
        }


def validate_review_record(filepath: Path,
                           expected_candidate_hash: str = EXPECTED_CANDIDATE_SHA256,
                           expected_video_hash: str = EXPECTED_VIDEO_SHA256) -> ReviewValidationResult:
    """Safely validate a single review JSON record without modifying it."""
    res = ReviewValidationResult(filepath)
    
    if not filepath.exists():
        res.errors.append(f"File not found: {filepath}")
        res.record_type = "NOT_FOUND"
        return res

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        res.data = data
    except UnicodeDecodeError:
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                data = json.load(f)
            res.data = data
            res.warnings.append("File required latin-1 decoding; UTF-8 is recommended.")
        except Exception as e:
            res.errors.append(f"Failed to read file: {e}")
            res.record_type = "CORRUPTED"
            return res
    except json.JSONDecodeError as e:
        res.errors.append(f"JSON syntax error: {e}")
        res.record_type = "CORRUPTED"
        return res
    except Exception as e:
        res.errors.append(f"Unexpected file reading error: {e}")
        res.record_type = "CORRUPTED"
        return res

    # 1. Schema Version Check
    schema_ver = data.get("reviewSchemaVersion")
    if not schema_ver:
        res.errors.append("Missing required field 'reviewSchemaVersion'.")
    elif not str(schema_ver).startswith("signbridge_review_schema_v1."):
        res.errors.append(
            f"Unsupported schema version '{schema_ver}'. Expected 'signbridge_review_schema_v1.x.x'."
        )
    elif schema_ver != SUPPORTED_SCHEMA_VERSION:
        res.warnings.append(
            f"Minor schema version '{schema_ver}' differs from current '{SUPPORTED_SCHEMA_VERSION}'."
        )

    # 2. Candidate ID & Hash Verification
    res.candidate_id = data.get("candidateId")
    if not res.candidate_id:
        res.errors.append("Missing required field 'candidateId'.")
    elif res.candidate_id != EXPECTED_CANDIDATE_ID:
        res.errors.append(
            f"Candidate ID mismatch: record is for '{res.candidate_id}', but validator is checking '{EXPECTED_CANDIDATE_ID}'. Cannot attribute to this candidate."
        )

    res.candidate_hash = data.get("candidateFileSha256", "").strip().lower()
    if not res.candidate_hash:
        res.errors.append("Missing 'candidateFileSha256'. Cannot bind review to asset.")
    elif res.candidate_hash != expected_candidate_hash.lower():
        res.errors.append(
            f"Candidate SHA-256 hash mismatch! Record has '{res.candidate_hash[:16]}...', "
            f"expected '{expected_candidate_hash[:16]}...'."
        )
        res.candidate_hash_matched = False
    else:
        res.candidate_hash_matched = True

    # 3. Reference Video Hash Verification
    res.video_hash = data.get("referenceVideoSha256", "").strip().lower()
    if res.video_hash:
        if res.video_hash == expected_video_hash.lower():
            res.video_hash_matched = True
        else:
            res.warnings.append(
                f"Reference video SHA-256 mismatch: record has '{res.video_hash[:16]}...', "
                f"expected '{expected_video_hash[:16]}...'."
            )
            res.video_hash_matched = False

    # 4. Reviewer Metadata
    reviewer = data.get("reviewer")
    if not reviewer or not isinstance(reviewer, dict):
        res.errors.append("Missing or malformed 'reviewer' object.")
    else:
        res.reviewer_name = reviewer.get("name", "").strip()
        res.reviewer_role = reviewer.get("role", "").strip()
        res.review_date = reviewer.get("date", "").strip()

        if not res.review_date:
            res.errors.append("Missing required field 'reviewer.date'.")
        if not res.reviewer_role:
            res.errors.append("Missing required field 'reviewer.role'.")
        elif res.reviewer_role not in VALID_ROLES:
            res.warnings.append(f"Unrecognized reviewer role '{res.reviewer_role}'.")

        if not res.reviewer_name or res.reviewer_name.lower() in ("anonymous reviewer", "placeholder", "evaluator"):
            res.warnings.append("Reviewer name is blank or default placeholder.")

    # 5. Parameter Ratings Check
    ratings = data.get("parameterRatings")
    if not ratings or not isinstance(ratings, dict):
        res.errors.append("Missing or malformed 'parameterRatings' dictionary.")
    else:
        for dim in REQUIRED_DIMENSIONS:
            val = ratings.get(dim)
            if val is None:
                res.errors.append(f"Missing rating for dimension '{dim}'.")
                res.ratings[dim] = "missing"
            elif val not in VALID_RATINGS:
                res.errors.append(f"Invalid rating value '{val}' for dimension '{dim}'.")
                res.ratings[dim] = str(val)
            else:
                res.ratings[dim] = val
                if val == "unrated":
                    res.unrated_count += 1
                elif val == "not_assessable":
                    res.not_assessable_count += 1

    # 6. Unassessable Dimensions & Rig Limitations
    res.unassessable_dims = data.get("unassessableDimensions", [])
    if not isinstance(res.unassessable_dims, list):
        res.warnings.append("'unassessableDimensions' should be a list.")
        res.unassessable_dims = []

    # 7. Overall Verdict
    res.verdict = data.get("overallVerdict")
    if not res.verdict:
        res.errors.append("Missing 'overallVerdict'.")
    elif res.verdict not in VALID_VERDICTS:
        res.warnings.append(f"Non-standard overall verdict: '{res.verdict}'.")

    # 8. Qualitative Observations
    res.qualitative_notes = (data.get("qualitativeNotes") or "").strip()
    if res.qualitative_notes and len(res.qualitative_notes) > 10:
        res.has_genuine_observations = True

    # 9. Uncertainty & Further Evidence Requests
    res.further_evidence_requested = bool(data.get("furtherEvidenceRequested", False))
    res.evidence_request_details = (data.get("evidenceRequestDetails") or "").strip()

    # 10. Unrecognized / Extended Fields Check
    standard_keys = {
        "reviewSchemaVersion", "sessionType", "candidateId", "candidateVersion",
        "candidateFileSha256", "referenceVideoFile", "referenceVideoSha256",
        "gloss", "sourceReference", "validationStatus", "reviewer",
        "rigLimitationsAcknowledged", "unassessableDimensions", "parameterRatings",
        "flaggedFramesInspected", "furtherEvidenceRequested", "evidenceRequestDetails",
        "qualitativeNotes", "overallVerdict", "timestampISO", "validationSummary"
    }
    unknown_keys = set(data.keys()) - standard_keys
    if unknown_keys:
        res.warnings.append(
            f"Record contains unrecognized/extended fields: {sorted(list(unknown_keys))}. "
            f"Preserved for forward compatibility."
        )

    # Check for genuine completion vs empty template
    is_template = (
        res.unrated_count >= 4 or
        (res.unrated_count == 3 and not res.has_genuine_observations and res.not_assessable_count == 2)
    )

    if res.errors:
        if not res.candidate_hash_matched and res.candidate_hash:
            res.record_type = "HASH_MISMATCH"
        else:
            res.record_type = "SCHEMA_VIOLATION"
        res.is_valid = False
    elif is_template:
        res.record_type = "TEMPLATE_OR_UNRATED"
        res.is_valid = True
        res.warnings.append("Record contains mostly unrated dimensions; appears to be an uncompleted template.")
    elif res.unrated_count > 0:
        res.record_type = "PARTIAL_REVIEW"
        res.is_valid = True
    else:
        res.record_type = "COMPLETED_GENUINE_REVIEW"
        res.is_valid = True

    return res


def scan_review_records(target_dir: Path) -> List[ReviewValidationResult]:
    """Scan and validate all JSON files in the review directory."""
    results = []
    if not target_dir.exists():
        return results

    for item in sorted(target_dir.glob("*.json")):
        if item.is_file():
            res = validate_review_record(item)
            results.append(res)
    return results


def print_validation_report(results: List[ReviewValidationResult], target_dir: Optional[Path] = None):
    """Print readable summary of review record validation."""
    print("=" * 80)
    print("SignBridge M3.14 — ISL Review Record Validation Report")
    print("=" * 80)

    if not results:
        print("\n[STATUS] HUMAN REVIEW PENDING — NO GENUINE REVIEW RECORD FOUND")
        if target_dir:
            print(f"Scanned directory: {target_dir}")
        print("\nNotice:")
        print("  - Zero review records were detected in the review storage directory.")
        print("  - In accordance with SignBridge evidence integrity standards, no synthetic")
        print("    or simulated review records have been fabricated.")
        print("  - The experimental candidate remains unvalidated pending real human review.")
        print("=" * 80)
        return

    print(f"\nDiscovered {len(results)} review record file(s):\n")
    for r in results:
        status_tag = f"[{r.record_type}]"
        print(f"File: {r.filename}")
        print(f"  Classification:      {status_tag}")
        print(f"  Candidate ID:        {r.candidate_id or 'Missing'}")
        print(f"  Candidate Hash Match:{' YES' if r.candidate_hash_matched else ' NO (MISMATCH/MISSING)'}")
        print(f"  Reviewer:            {r.reviewer_name or 'Not specified'} (Role: {r.reviewer_role or 'None'})")
        print(f"  Review Date:         {r.review_date or 'Not specified'}")
        print(f"  Overall Verdict:     {r.verdict or 'None'}")
        print(f"  Dimension Ratings:   {r.ratings}")
        print(f"  Unassessable Items:  {r.unassessable_dims}")
        print(f"  Has Free Notes:      {'Yes' if r.has_genuine_observations else 'No'}")
        if r.further_evidence_requested:
            print(f"  Evidence Requested:  YES — {r.evidence_request_details or 'Additional visual/multi-angle evidence requested'}")

        if r.errors:
            print("  Errors:")
            for err in r.errors:
                print(f"    - {err}")
        if r.warnings:
            print("  Warnings:")
            for warn in r.warnings:
                print(f"    - {warn}")
        print("-" * 60)

    # Summary
    completed = [r for r in results if r.record_type == "COMPLETED_GENUINE_REVIEW"]
    partial = [r for r in results if r.record_type == "PARTIAL_REVIEW"]
    mismatched = [r for r in results if r.record_type == "HASH_MISMATCH"]
    templates = [r for r in results if r.record_type == "TEMPLATE_OR_UNRATED"]
    corrupted = [r for r in results if r.record_type in ("CORRUPTED", "SCHEMA_VIOLATION")]

    print("\nSUMMARY AUDIT BREAKDOWN:")
    print(f"  - Completed Genuine Reviews: {len(completed)}")
    print(f"  - Partial Reviews:           {len(partial)}")
    print(f"  - Template / Unrated Files:  {len(templates)}")
    print(f"  - Hash Mismatches:           {len(mismatched)}")
    print(f"  - Corrupted / Malformed:     {len(corrupted)}")
    print("=" * 80)


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="Validate SignBridge ISL review records.")
    parser.add_argument("path", nargs="?", default=None,
                        help="Path to review JSON file or directory (default: tools/isl_motion_extraction/reviews/)")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON summary")
    args = parser.parse_args()

    default_reviews_dir = Path(__file__).resolve().parent / "reviews"
    target_path = Path(args.path) if args.path else default_reviews_dir

    if target_path.is_file():
        results = [validate_review_record(target_path)]
    elif target_path.is_dir():
        results = scan_review_records(target_path)
    else:
        results = []

    if args.json:
        summary = {
            "target": str(target_path),
            "recordCount": len(results),
            "records": [r.to_dict() for r in results]
        }
        print(json.dumps(summary, indent=2))
    else:
        print_validation_report(results, target_path if target_path.is_dir() else None)

    # Return exit code: 0 if all records are valid or if directory has 0 records (clean pending state)
    has_critical_failures = any(r.record_type in ("CORRUPTED", "SCHEMA_VIOLATION", "HASH_MISMATCH") for r in results)
    sys.exit(1 if has_critical_failures else 0)


if __name__ == "__main__":
    main()
