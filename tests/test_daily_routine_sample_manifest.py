#!/usr/bin/env python3
"""Tests for SignBridge Controlled Single-Video Prototype: Daily Routine 01:35-01:55 Segment.

Verifies:
1. Manifest structure, versioning, and required metadata.
2. Verified exact YouTube speech transcript timestamps and text strictly contained in 01:35–01:55.
3. Strict linguistic review status ('PENDING_DEAF_NATIVE_REVIEW' with 0/3 completed reviews, isApproved: False).
4. Explicit unapproved candidate status and visible disclaimers preventing misrepresentation.
5. Zero synthetic gestures policy: all un-animated/un-reviewed signs enforce NEUTRAL_REST_POSE.
6. Compliance with SignItem and SignSequence contracts (schema validation).
7. Non-violation of licensing and video distribution restrictions (LEGAL-01).
"""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestDailyRoutineSampleManifest(unittest.TestCase):
    """Validation test for the controlled Daily Routine sample manifest."""

    def setUp(self):
        self.manifest_path = ROOT / "extension" / "assets" / "samples" / "daily_routine_0135_0155_manifest.json"
        self.assertTrue(self.manifest_path.exists(), f"Sample manifest must exist at {self.manifest_path}")
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)

    def test_01_manifest_metadata_and_version(self):
        """Verifies manifest metadata, versioning, and video attribution."""
        self.assertEqual(self.manifest.get("manifestVersion"), "1.0.0")
        meta = self.manifest.get("metadata", {})
        self.assertIn("sMkzwmMs0jM", meta.get("youtubeUrl", ""))
        self.assertIn("Daily Routine", meta.get("videoTitle", ""))
        self.assertIn("LEGAL-01", meta.get("license", ""))
        self.assertIn("01:35", meta.get("windowTimingNote", ""))

    def test_02_segment_timeline_and_duration(self):
        """Verifies segment start/end media times (01:35 - 01:55)."""
        segment = self.manifest.get("segment", {})
        self.assertEqual(segment.get("startMediaTimeMs"), 95000)
        self.assertEqual(segment.get("endMediaTimeMs"), 115000)
        self.assertEqual(segment.get("durationMs"), 20000)
        self.assertGreaterEqual(segment.get("endMediaTimeMs"), segment.get("startMediaTimeMs"))

    def test_03_verified_speech_transcript(self):
        """Verifies exact spoken sentences strictly contained within the 01:35-01:55 window."""
        transcript = self.manifest.get("transcript", {})
        self.assertTrue(transcript.get("verified"), "Speech transcript must be verified")
        items = transcript.get("items", [])
        self.assertEqual(len(items), 2, "Expected exactly 2 complete transcript segments contained within 01:35-01:55")
        
        texts = [item["text"] for item in items]
        self.assertIn("I walk to the bathroom to wash my face and brush my teeth.", texts[0])
        self.assertIn("After that, I go back to my bedroom to get dressed.", texts[1])

        # Verify all items end on or before the 115000 ms (01:55) window boundary
        for item in items:
            self.assertGreaterEqual(item["startMs"], 95000, "Item must start within 01:35 window")
            self.assertLessEqual(item["endMs"], 115000, "Item must finish within 01:55 window")

    def test_04_linguistic_review_governance_and_disclaimer(self):
        """Verifies that ISL translation is strictly marked PENDING review and unapproved."""
        isl = self.manifest.get("islTranslation", {})
        self.assertEqual(isl.get("reviewStatus"), "PENDING_DEAF_NATIVE_REVIEW")
        self.assertFalse(isl.get("isApproved", True), "isApproved must be explicitly False")
        self.assertEqual(isl.get("reviewsCompleted"), 0, "Candidate translations cannot be approved without 3 reviews")
        self.assertEqual(isl.get("reviewsRequired"), 3)
        self.assertIn("UNAPPROVED PROVISIONAL CANDIDATE ONLY", isl.get("disclaimer", ""))
        
        for seg in isl.get("segments", []):
            self.assertFalse(seg.get("approvedForProduction"), "Must NOT be approved for production")
            self.assertTrue(seg.get("provisionalCandidateOnly"), "Must be flagged as provisional candidate only")
            self.assertEqual(seg.get("activeAnimationAction"), "NEUTRAL_REST_POSE")
            self.assertEqual(seg.get("animationCoverage"), "0%")

    def test_05_contract_compliance_for_candidate_glosses(self):
        """Verifies candidate gloss items adhere to SignItem constraints and have null animation."""
        isl = self.manifest.get("islTranslation", {})
        for seg in isl.get("segments", []):
            for gloss_item in seg.get("prePreparedCandidateGlosses", []):
                self.assertTrue(gloss_item["gloss"].isupper(), f"Gloss {gloss_item['gloss']} must be uppercase")
                self.assertIn(gloss_item["category"], ["lexical", "fingerspelling", "pause"])
                self.assertIsNone(gloss_item["animationId"], "Un-reviewed signs must have animationId: null")

    def test_06_zero_synthetic_gestures_enforced(self):
        """Verifies zero synthetic gestures policy and fallback state."""
        anim = self.manifest.get("animationStatus", {})
        self.assertTrue(anim.get("zeroSyntheticGesturesEnforced"))
        self.assertEqual(anim.get("fallbackState"), "NEUTRAL_REST_POSE")
        self.assertEqual(anim.get("segmentAnimationCoverage"), 0.0)
        self.assertIn("isl_namaste_godl_v1", anim.get("registeredProductionClips"))

    def test_07_review_worksheet_exists_and_matches_governance(self):
        """Verifies that the dedicated ISL review worksheet exists and defines required governance."""
        worksheet_path = ROOT / "Docs" / "ISL_DAILY_ROUTINE_0135_0155_REVIEW_WORKSHEET.md"
        self.assertTrue(worksheet_path.exists(), "Docs/ISL_DAILY_ROUTINE_0135_0155_REVIEW_WORKSHEET.md must exist")
        content = worksheet_path.read_text(encoding="utf-8")
        self.assertIn("01:35.00 – 01:55.00", content)
        self.assertIn("PENDING_DEAF_NATIVE_REVIEW", content)
        self.assertIn("0 OF 3 COMPLETED REVIEWS", content)
        self.assertIn("I walk to the bathroom to wash my face and brush my teeth.", content)
        self.assertIn("After that, I go back to my bedroom to get dressed.", content)
        self.assertIn("Pending Reviewer Input", content)
        self.assertIn("NEUTRAL_REST_POSE", content)


if __name__ == "__main__":
    unittest.main()
