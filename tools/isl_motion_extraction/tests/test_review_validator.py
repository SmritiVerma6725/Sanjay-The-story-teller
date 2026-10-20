#!/usr/bin/env python3
"""Unit tests for SignBridge M3.14 Review Record Validator (validate_review_record.py)"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Add tool directory to path
TOOL_DIR = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(TOOL_DIR))

from validate_review_record import (
    validate_review_record,
    scan_review_records,
    EXPECTED_CANDIDATE_ID,
    EXPECTED_CANDIDATE_SHA256,
    EXPECTED_VIDEO_SHA256,
    SUPPORTED_SCHEMA_VERSION
)


class TestReviewValidator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="signbridge_review_test_"))

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_sample_review(self, overrides=None):
        base = {
            "reviewSchemaVersion": SUPPORTED_SCHEMA_VERSION,
            "sessionType": "SignBridge ISL MoCap Linguistic Review",
            "candidateId": EXPECTED_CANDIDATE_ID,
            "candidateVersion": "v1.0.0",
            "candidateFileSha256": EXPECTED_CANDIDATE_SHA256,
            "referenceVideoFile": "ISLRTC_Namaste_sample.mp4",
            "referenceVideoSha256": EXPECTED_VIDEO_SHA256,
            "gloss": "NAMASTE",
            "sourceReference": "ISLRTC Dictionary Vol 1, Word #0001 (data.gov.in / GODL)",
            "validationStatus": "experimental_awaiting_validation",
            "reviewer": {
                "name": "Sunita Sharma",
                "role": "deaf_native",
                "date": "2026-10-19"
            },
            "rigLimitationsAcknowledged": True,
            "unassessableDimensions": ["non_manuals"],
            "parameterRatings": {
                "handshape": "acceptable",
                "location": "acceptable",
                "orientation": "acceptable",
                "movement": "acceptable",
                "non_manuals": "not_assessable"
            },
            "flaggedFramesInspected": {
                "frame22_lift_natural": True,
                "frame59_parting_smooth": True,
                "frame62_lap_rest_clean": True
            },
            "qualitativeNotes": "The prayer hand posture is natural. Forearms angle appropriately.",
            "overallVerdict": "provisional_approval",
            "timestampISO": "2026-10-19T22:00:00.000Z",
            "validationSummary": {
                "allDimensionsRated": True,
                "unratedDimensions": []
            }
        }
        if overrides:
            for k, v in overrides.items():
                if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                    base[k].update(v)
                else:
                    base[k] = v
        return base

    def test_completed_genuine_review_validates(self):
        review_data = self._create_sample_review()
        file_path = self.test_dir / "valid_review.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(review_data, f, indent=2)

        res = validate_review_record(file_path)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.record_type, "COMPLETED_GENUINE_REVIEW")
        self.assertTrue(res.candidate_hash_matched)
        self.assertTrue(res.video_hash_matched)
        self.assertEqual(res.unrated_count, 0)
        self.assertEqual(res.not_assessable_count, 1)
        self.assertEqual(len(res.errors), 0)

    def test_hash_mismatch_detection(self):
        review_data = self._create_sample_review({
            "candidateFileSha256": "0000000000000000000000000000000000000000000000000000000000000000"
        })
        file_path = self.test_dir / "mismatched_review.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(review_data, f, indent=2)

        res = validate_review_record(file_path)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.record_type, "HASH_MISMATCH")
        self.assertFalse(res.candidate_hash_matched)
        self.assertTrue(any("mismatch" in e.lower() for e in res.errors))

    def test_not_assessable_preserved_distinct_from_negative(self):
        review_data = self._create_sample_review({
            "parameterRatings": {
                "handshape": "acceptable",
                "location": "acceptable",
                "orientation": "acceptable",
                "movement": "unacceptable",
                "non_manuals": "not_assessable"
            }
        })
        file_path = self.test_dir / "mixed_ratings.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(review_data, f, indent=2)

        res = validate_review_record(file_path)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.ratings["movement"], "unacceptable")
        self.assertEqual(res.ratings["non_manuals"], "not_assessable")
        self.assertEqual(res.not_assessable_count, 1)

    def test_template_or_unrated_distinction(self):
        review_data = self._create_sample_review({
            "reviewer": {"name": "Anonymous Reviewer", "role": "deaf_native", "date": "2026-10-19"},
            "parameterRatings": {
                "handshape": "unrated",
                "location": "unrated",
                "orientation": "unrated",
                "movement": "unrated",
                "non_manuals": "not_assessable"
            },
            "qualitativeNotes": "",
            "overallVerdict": "not_assessable"
        })
        file_path = self.test_dir / "template_review.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(review_data, f, indent=2)

        res = validate_review_record(file_path)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.record_type, "TEMPLATE_OR_UNRATED")
        self.assertGreaterEqual(res.unrated_count, 4)

    def test_schema_violation_missing_fields(self):
        # Missing parameterRatings
        bad_data = {
            "reviewSchemaVersion": SUPPORTED_SCHEMA_VERSION,
            "candidateId": EXPECTED_CANDIDATE_ID
        }
        file_path = self.test_dir / "bad_schema.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(bad_data, f)

        res = validate_review_record(file_path)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.record_type, "SCHEMA_VIOLATION")
        self.assertTrue(len(res.errors) > 0)

    def test_corrupted_json_handled_safely(self):
        file_path = self.test_dir / "corrupted.json"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("{ invalid json text syntax here ...")

        res = validate_review_record(file_path)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.record_type, "CORRUPTED")
        self.assertTrue(any("syntax error" in e.lower() for e in res.errors))

    def test_read_only_immutability(self):
        review_data = self._create_sample_review()
        file_path = self.test_dir / "immutable_review.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(review_data, f, indent=2)

        with open(file_path, "rb") as f:
            initial_bytes = f.read()
        initial_mtime = os.path.getmtime(file_path)

        validate_review_record(file_path)

        with open(file_path, "rb") as f:
            after_bytes = f.read()
        after_mtime = os.path.getmtime(file_path)

        self.assertEqual(initial_bytes, after_bytes, "File content was modified during validation!")
        self.assertEqual(initial_mtime, after_mtime, "File mtime was altered during validation!")

    def test_further_evidence_request_supported(self):
        review_data = self._create_sample_review({
            "furtherEvidenceRequested": True,
            "evidenceRequestDetails": "Need side angle recording to verify palm distance from sternum."
        })
        file_path = self.test_dir / "evidence_requested_review.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(review_data, f, indent=2)

        res = validate_review_record(file_path)
        self.assertTrue(res.is_valid)
        self.assertTrue(res.further_evidence_requested)
        self.assertIn("side angle", res.evidence_request_details)

    def test_scan_empty_directory_returns_empty_list(self):
        empty_dir = self.test_dir / "empty_reviews"
        empty_dir.mkdir()
        results = scan_review_records(empty_dir)
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
