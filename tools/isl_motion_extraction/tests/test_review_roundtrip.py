#!/usr/bin/env python3
"""SignBridge M3.16 — ISL Review Record Round-Trip & Usability Test Suite

Verifies the complete review workflow:
1. Data entry with rich types (Unicode, multiline text, explicit Not Assessable, evidence requests).
2. Local storage serialization / deserialization.
3. JSON export and reload.
4. Markdown summary generation and neutrality check.
5. Ingestion and verification via validate_review_record.py.
6. Robustness against missing fields, invalid ratings, malformed JSON, empty templates,
   conflicting metadata, unknown/extended fields, and candidate hash mismatches.
7. Verification that validator is strictly read-only and never mutates records.
"""

import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Tool directory setup
TOOL_DIR = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(TOOL_DIR))

from validate_review_record import (
    validate_review_record,
    EXPECTED_CANDIDATE_ID,
    EXPECTED_CANDIDATE_SHA256,
    EXPECTED_VIDEO_SHA256,
    SUPPORTED_SCHEMA_VERSION,
    REQUIRED_DIMENSIONS
)


def generate_markdown_summary(d):
    """Python reference mirror of generateMarkdownSummary in preview_mocap.html."""
    notes = d.get("qualitativeNotes") or "_No specific qualitative notes provided._"
    evidence_req = d.get("furtherEvidenceRequested", False)
    evidence_text = d.get("evidenceRequestDetails", "")
    evidence_str = (
        f"Yes — {evidence_text or 'Additional multi-angle video or slower reference capture requested'}"
        if evidence_req else "No — No further evidence requested at this time"
    )

    f_inspected = d.get("flaggedFramesInspected", {})
    f22_str = "Yes (Observed natural motion)" if f_inspected.get("frame22_lift_natural") else "No (Distortion / unnatural motion noted)"
    f59_str = "Yes (Observed smooth release)" if f_inspected.get("frame59_parting_smooth") else "No (Discontinuity / popping noted)"
    f62_str = "Yes (Observed clean rest)" if f_inspected.get("frame62_lap_rest_clean") else "No (Asymmetry / distortion noted)"

    ratings = d.get("parameterRatings", {})
    unassessable = d.get("unassessableDimensions", [])
    unassessable_str = ", ".join(unassessable) if unassessable else "None"

    reviewer = d.get("reviewer", {})

    return f"""# ISL Expert Review Finding: NAMASTE Candidate Motion

**Review Schema:** `{d.get('reviewSchemaVersion')}`  
**Review Session Date:** {reviewer.get('date')} ({d.get('timestampISO')})  
**Reviewer:** {reviewer.get('name')} (Role: {reviewer.get('role')})  
**Evaluated Candidate:** `{d.get('candidateId')}` (Version: `{d.get('candidateVersion')}`)  
**Candidate File SHA-256:** `{d.get('candidateFileSha256')}`  
**Reference Video File:** `{d.get('referenceVideoFile')}`  
**Reference Video SHA-256:** `{d.get('referenceVideoSha256')}`  
**Status:** `{d.get('validationStatus')}`  
**Source Provenance:** {d.get('sourceReference')}  

---

## 1. Five Phonological Parameters Evaluation
- **Handshape (DEZ):** `{ratings.get('handshape')}`
- **Location (TAB):** `{ratings.get('location')}`
- **Orientation (ORI):** `{ratings.get('orientation')}`
- **Movement (SIG):** `{ratings.get('movement')}`
- **Non-Manual Markers (NMM):** `{ratings.get('non_manuals')}`

## 2. Low-Confidence & Scrutiny Frames
- **Frame 22 ($880\\text{{ ms}}$ lift):** {f22_str}
- **Frame 59 ($2360\\text{{ ms}}$ release):** {f59_str}
- **Frame 62 ($2480\\text{{ ms}}$ lap rest):** {f62_str}

## 3. Rig Limitations & Evidence Requests
- **Avatar Rig:** Adobe Mixamo Y-Bot (`ybot.glb`)
- **Limitation Acknowledgment:** Rig possesses full 4-phalange articulated fingers, but has a rigid metallic face with zero facial blendshapes or eye bones.
- **Unassessable Dimensions:** {unassessable_str}
- **Further Evidence Requested:** {evidence_str}

## 4. Qualitative Notes & Recommendations
{notes}

## 5. Overall Reviewer Recommendation
**Verdict:** `{d.get('overallVerdict')}`
"""


class TestReviewRoundTrip(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="signbridge_m316_roundtrip_"))

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _build_rich_record(self):
        """Construct a full review record with Unicode, multiline notes, uncertainty, and unknown fields."""
        return {
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
                "name": "डॉ. सुनीता शर्मा (Dr. Sunita Sharma)",
                "role": "certified_interpreter",
                "date": "2026-10-20"
            },
            "rigLimitationsAcknowledged": True,
            "unassessableDimensions": ["non_manuals"],
            "parameterRatings": {
                "handshape": "acceptable",
                "location": "acceptable",
                "orientation": "acceptable",
                "movement": "minor_issue",
                "non_manuals": "not_assessable"
            },
            "flaggedFramesInspected": {
                "frame22_lift_natural": True,
                "frame59_parting_smooth": False,
                "frame62_lap_rest_clean": True
            },
            "furtherEvidenceRequested": True,
            "evidenceRequestDetails": "Side-profile multi-camera reference video requested to confirm wrist flexion angle.",
            "qualitativeNotes": (
                "नमस्ते (Namaste) observation notes:\n"
                "- Both palms make contact correctly at sternum level.\n"
                "- Frame 59 exhibits slight abruptness during hand release.\n"
                "- Head tilt at peak hold is observable; non-manual facial markers unassessable due to Y-Bot rig limitation."
            ),
            "overallVerdict": "needs_tuning",
            "timestampISO": "2026-10-20T18:30:00.000Z",
            "validationSummary": {
                "allDimensionsRated": True,
                "unratedDimensions": []
            },
            # Unknown / extended fields to verify forward compatibility
            "evaluatorPanelAffiliation": "Northern Deaf Association",
            "customEvaluationBadge": "AUDIT_Q4_2026"
        }

    def test_full_roundtrip_persistence_and_validation(self):
        """Simulate entry -> localStorage serialization -> export -> reload -> validation."""
        original_record = self._build_rich_record()

        # Step 1: Simulate localStorage JSON serialization / deserialization
        storage_serialized = json.dumps(original_record, ensure_ascii=False)
        storage_deserialized = json.loads(storage_serialized)
        self.assertEqual(original_record, storage_deserialized)

        # Step 2: Export to JSON file
        export_file = self.test_dir / "ISL_Namaste_Review_Sunita_Sharma_2026-10-20.json"
        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(storage_deserialized, f, indent=2, ensure_ascii=False)

        # Step 3: Reload exported JSON file
        with open(export_file, "r", encoding="utf-8") as f:
            reloaded_record = json.load(f)

        # Step 4: Validate exported JSON record using validate_review_record
        val_result = validate_review_record(export_file)

        # Confirm validation success
        self.assertTrue(val_result.is_valid)
        self.assertEqual(val_result.record_type, "COMPLETED_GENUINE_REVIEW")
        self.assertTrue(val_result.candidate_hash_matched)
        self.assertTrue(val_result.video_hash_matched)
        self.assertEqual(val_result.unrated_count, 0)
        self.assertEqual(val_result.not_assessable_count, 1)
        self.assertTrue(val_result.further_evidence_requested)
        self.assertIn("wrist flexion angle", val_result.evidence_request_details)

        # Step 5: Confirm all fields survived round trip without corruption
        self.assertEqual(reloaded_record["reviewer"]["name"], "डॉ. सुनीता शर्मा (Dr. Sunita Sharma)")
        self.assertIn("नमस्ते (Namaste) observation notes:", reloaded_record["qualitativeNotes"])
        self.assertIn("\n- Frame 59 exhibits slight abruptness", reloaded_record["qualitativeNotes"])
        self.assertEqual(reloaded_record["parameterRatings"]["non_manuals"], "not_assessable")
        self.assertEqual(reloaded_record["parameterRatings"]["movement"], "minor_issue")
        self.assertEqual(reloaded_record["overallVerdict"], "needs_tuning")
        self.assertTrue(reloaded_record["flaggedFramesInspected"]["frame22_lift_natural"])
        self.assertFalse(reloaded_record["flaggedFramesInspected"]["frame59_parting_smooth"])
        self.assertTrue(reloaded_record["flaggedFramesInspected"]["frame62_lap_rest_clean"])

        # Unknown / extended fields preserved
        self.assertEqual(reloaded_record["evaluatorPanelAffiliation"], "Northern Deaf Association")
        self.assertEqual(reloaded_record["customEvaluationBadge"], "AUDIT_Q4_2026")
        self.assertTrue(any("unrecognized/extended fields" in w for w in val_result.warnings))

        # Step 6: Generate and check Markdown export
        md_text = generate_markdown_summary(reloaded_record)
        self.assertIn("डॉ. सुनीता शर्मा (Dr. Sunita Sharma)", md_text)
        self.assertIn("नमस्ते (Namaste) observation notes:", md_text)
        self.assertIn("Frame 59 ($2360\\text{ ms}$ release):** No (Discontinuity / popping noted)", md_text)
        self.assertIn("Frame 22 ($880\\text{ ms}$ lift):** Yes (Observed natural motion)", md_text)
        self.assertIn("Further Evidence Requested:** Yes — Side-profile multi-camera reference video", md_text)
        self.assertIn("`needs_tuning`", md_text)

        # Verify no leading biased wording in Markdown
        self.assertNotIn("PASSED (Natural motion)", md_text)
        self.assertNotIn("PASSED (Smooth release)", md_text)

    def test_empty_values_and_whitespace_handling(self):
        """Confirm empty and whitespace fields do not crash round trip and produce appropriate warnings."""
        record = self._build_rich_record()
        record["reviewer"]["name"] = "   "  # whitespace reviewer name
        record["qualitativeNotes"] = ""     # empty qualitative notes
        record["furtherEvidenceRequested"] = False
        record["evidenceRequestDetails"] = ""

        test_file = self.test_dir / "empty_notes_review.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        res = validate_review_record(test_file)
        self.assertTrue(res.is_valid)
        self.assertTrue(any("Reviewer name is blank" in w for w in res.warnings))
        self.assertFalse(res.has_genuine_observations)
        self.assertFalse(res.further_evidence_requested)

        md = generate_markdown_summary(record)
        self.assertIn("_No specific qualitative notes provided._", md)
        self.assertIn("No — No further evidence requested at this time", md)

    def test_explicit_not_assessable_distinct_from_negative(self):
        """Verify 'not_assessable' is distinctly preserved and not conflated with negative ratings."""
        record = self._build_rich_record()
        record["parameterRatings"] = {
            "handshape": "acceptable",
            "location": "not_assessable",
            "orientation": "acceptable",
            "movement": "unacceptable",
            "non_manuals": "not_assessable"
        }
        record["unassessableDimensions"] = ["location", "non_manuals"]

        test_file = self.test_dir / "not_assessable_review.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        res = validate_review_record(test_file)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.ratings["location"], "not_assessable")
        self.assertEqual(res.ratings["non_manuals"], "not_assessable")
        self.assertEqual(res.ratings["movement"], "unacceptable")
        self.assertEqual(res.not_assessable_count, 2)
        self.assertEqual(res.unrated_count, 0)

    def test_missing_fields_validation_error(self):
        """Confirm missing schema, candidateId, or parameterRatings trigger schema violation."""
        # Missing parameterRatings
        bad_record = self._build_rich_record()
        del bad_record["parameterRatings"]

        test_file = self.test_dir / "missing_ratings.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(bad_record, f, indent=2)

        res = validate_review_record(test_file)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.record_type, "SCHEMA_VIOLATION")
        self.assertTrue(any("Missing or malformed 'parameterRatings'" in e for e in res.errors))

        # Missing dimension inside parameterRatings
        bad_record_2 = self._build_rich_record()
        del bad_record_2["parameterRatings"]["movement"]
        test_file_2 = self.test_dir / "missing_dimension.json"
        with open(test_file_2, "w", encoding="utf-8") as f:
            json.dump(bad_record_2, f, indent=2)

        res_2 = validate_review_record(test_file_2)
        self.assertFalse(res_2.is_valid)
        self.assertEqual(res_2.record_type, "SCHEMA_VIOLATION")
        self.assertTrue(any("Missing rating for dimension 'movement'" in e for e in res_2.errors))

    def test_invalid_ratings_rejected(self):
        """Confirm invalid ratings like 'good', 'poor', 'pass' are rejected."""
        bad_record = self._build_rich_record()
        bad_record["parameterRatings"]["handshape"] = "superb"

        test_file = self.test_dir / "invalid_rating.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(bad_record, f, indent=2)

        res = validate_review_record(test_file)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.record_type, "SCHEMA_VIOLATION")
        self.assertTrue(any("Invalid rating value 'superb'" in e for e in res.errors))

    def test_malformed_json_syntax(self):
        """Confirm malformed JSON string triggers CORRUPTED record type without crashing."""
        test_file = self.test_dir / "corrupted_syntax.json"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("{\n  \"reviewSchemaVersion\": \"signbridge_review_schema_v1.0.0\",\n  BROKEN_SYNTAX\n")

        res = validate_review_record(test_file)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.record_type, "CORRUPTED")
        self.assertTrue(any("JSON syntax error" in e for e in res.errors))

    def test_empty_template_classification(self):
        """Confirm template records with unrated fields are marked TEMPLATE_OR_UNRATED, not completed reviews."""
        template_record = self._build_rich_record()
        template_record["reviewer"] = {"name": "Anonymous Reviewer", "role": "deaf_native", "date": "2026-10-20"}
        template_record["parameterRatings"] = {dim: "unrated" for dim in REQUIRED_DIMENSIONS}
        template_record["qualitativeNotes"] = ""
        template_record["overallVerdict"] = "not_assessable"

        test_file = self.test_dir / "blank_template.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(template_record, f, indent=2)

        res = validate_review_record(test_file)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.record_type, "TEMPLATE_OR_UNRATED")
        self.assertEqual(res.unrated_count, 5)

    def test_candidate_hash_mismatch_prevents_misattribution(self):
        """Confirm a review for another candidate cannot be attributed to this candidate."""
        mismatched_record = self._build_rich_record()
        mismatched_record["candidateFileSha256"] = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

        test_file = self.test_dir / "mismatched_candidate.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(mismatched_record, f, indent=2)

        res = validate_review_record(test_file)
        self.assertFalse(res.is_valid)
        self.assertEqual(res.record_type, "HASH_MISMATCH")
        self.assertFalse(res.candidate_hash_matched)
        self.assertTrue(any("Candidate SHA-256 hash mismatch" in e for e in res.errors))

    def test_reference_video_hash_mismatch_warning(self):
        """Confirm mismatched reference video triggers warning without crash."""
        record = self._build_rich_record()
        record["referenceVideoSha256"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

        test_file = self.test_dir / "mismatched_video.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        res = validate_review_record(test_file)
        self.assertTrue(res.is_valid)  # Candidate is valid, but video hash is flagged
        self.assertFalse(res.video_hash_matched)
        self.assertTrue(any("Reference video SHA-256 mismatch" in w for w in res.warnings))

    def test_validator_does_not_modify_review_record(self):
        """Confirm the validator is strictly read-only and computes exact file hash before and after."""
        record = self._build_rich_record()
        test_file = self.test_dir / "read_only_test.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        # Compute SHA-256 before validation
        with open(test_file, "rb") as f:
            sha_before = hashlib.sha256(f.read()).hexdigest()

        # Run validation multiple times
        res1 = validate_review_record(test_file)
        res2 = validate_review_record(test_file)

        # Compute SHA-256 after validation
        with open(test_file, "rb") as f:
            sha_after = hashlib.sha256(f.read()).hexdigest()

        self.assertEqual(sha_before, sha_after)
        self.assertEqual(res1.record_type, res2.record_type)


if __name__ == "__main__":
    unittest.main()
