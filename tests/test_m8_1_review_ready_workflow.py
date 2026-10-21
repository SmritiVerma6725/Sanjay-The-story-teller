#!/usr/bin/env python3
"""SignBridge Milestone M8.1 — Review-Ready Vocabulary Workflow Test Suite

Tests:
1. Schema validation of structured sign records (HELLO, THANK_YOU).
2. Authoritative source presence and verification documentation.
3. Skeleton joint compatibility against CANONICAL_BONES.
4. Promotion gate rule: Rejects promotion to IMPLEMENTED_VALIDATED without >=3 reviews.
5. Ingestion block: HELLO and THANK_YOU are strictly classified as BLOCKED_SOURCE_OR_REVIEW.
6. Non-fabrication guarantee: No guessed animation clips exist in keyframe_registry for HELLO or THANK_YOU.
7. Worksheet reference validation: Confirms review worksheets exist for both candidates.
"""

import json
import os
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools' / 'isl_motion_extraction'))

import validate_sign_metadata as vsm

class TestM81ReviewReadyWorkflow(unittest.TestCase):
    """Unit tests for M8.1 review-ready sign records, metadata schema, and promotion gates."""

    @classmethod
    def setUpClass(cls):
        cls.records_dir = ROOT / 'Docs' / 'records'
        cls.hello_record = cls.records_dir / 'sign_record_hello.json'
        cls.thank_you_record = cls.records_dir / 'sign_record_thank_you.json'

    def test_01_sign_records_exist(self):
        """Review-ready sign records exist for both HELLO and THANK_YOU."""
        self.assertTrue(self.hello_record.exists(), "sign_record_hello.json must exist")
        self.assertTrue(self.thank_you_record.exists(), "sign_record_thank_you.json must exist")

    def test_02_hello_record_schema_and_metadata(self):
        """HELLO record conforms to schema and has required source and blocking details."""
        valid, errors = vsm.validate_sign_record(self.hello_record)
        self.assertTrue(valid, f"HELLO record validation failed: {errors}")
        data = json.loads(self.hello_record.read_text(encoding='utf-8'))
        self.assertEqual(data["canonicalId"], "HELLO")
        self.assertEqual(data["implementationReadiness"], "BLOCKED_SOURCE_OR_REVIEW")
        self.assertEqual(data["authoritativeSource"]["license"], "Government Open Data License - India (GODL)")
        self.assertFalse(data["requiredAnimationAsset"]["assetPresence"])
        self.assertIsNone(data["requiredAnimationAsset"]["assetPath"])

    def test_03_thank_you_record_schema_and_metadata(self):
        """THANK_YOU record conforms to schema and has required source and blocking details."""
        valid, errors = vsm.validate_sign_record(self.thank_you_record)
        self.assertTrue(valid, f"THANK_YOU record validation failed: {errors}")
        data = json.loads(self.thank_you_record.read_text(encoding='utf-8'))
        self.assertEqual(data["canonicalId"], "THANK_YOU")
        self.assertEqual(data["implementationReadiness"], "BLOCKED_SOURCE_OR_REVIEW")
        self.assertEqual(data["authoritativeSource"]["license"], "Government Open Data License - India (GODL)")
        self.assertFalse(data["requiredAnimationAsset"]["assetPresence"])
        self.assertIsNone(data["requiredAnimationAsset"]["assetPath"])

    def test_04_active_joints_belong_to_canonical_bones(self):
        """All joints specified in the records belong to the canonical Y-Bot rig."""
        for path in [self.hello_record, self.thank_you_record]:
            data = json.loads(path.read_text(encoding='utf-8'))
            joints = data["expectedSkeletonMapping"]["primaryActiveJoints"]
            for j in joints:
                self.assertIn(j, vsm.CANONICAL_BONES, f"Joint '{j}' in {path.name} not in CANONICAL_BONES")

    def test_05_promotion_gate_rejects_unreviewed_promotion(self):
        """Validator strictly rejects promotion to IMPLEMENTED_VALIDATED with fewer than 3 reviews."""
        import tempfile
        mock_data = json.loads(self.hello_record.read_text(encoding='utf-8'))
        mock_data["implementationReadiness"] = "IMPLEMENTED_VALIDATED"
        mock_data["approvalHistory"] = [{"reviewer": "TEST", "score": 90}]  # Only 1 review
        
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as tf:
            json.dump(mock_data, tf)
            temp_path = Path(tf.name)
            
        try:
            valid, errors = vsm.validate_sign_record(temp_path)
            self.assertFalse(valid, "Must reject promotion with only 1/3 reviews")
            self.assertTrue(any("Promotion violation" in e for e in errors))
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_06_non_fabrication_rule_enforced_in_lexicon(self):
        """Confirms HELLO and THANK_YOU remain animationId: null in SEED_LEXICON (no guessed keyframes)."""
        lexicon_path = ROOT / 'extension' / 'translation' / 'isl_translator.js'
        content = lexicon_path.read_text(encoding='utf-8')
        
        # HELLO must NOT have animationId defined
        hello_match = re.search(r'HELLO:\s*Object\.freeze\(\{([\s\S]*?)\}\)', content)
        self.assertTrue(hello_match)
        self.assertNotIn("animationId:", hello_match.group(1), "HELLO must not have animationId defined")
        
        # THANK_YOU must NOT have animationId defined
        ty_match = re.search(r'THANK_YOU:\s*Object\.freeze\(\{([\s\S]*?)\}\)', content)
        self.assertTrue(ty_match)
        self.assertNotIn("animationId:", ty_match.group(1), "THANK_YOU must not have animationId defined")

    def test_07_review_worksheets_exist(self):
        """Review worksheets exist for qualified Deaf-native reviewers."""
        ws_hello = ROOT / 'Docs' / 'ISL_HELLO_REVIEW_WORKSHEET.md'
        ws_ty = ROOT / 'Docs' / 'ISL_THANK_YOU_REVIEW_WORKSHEET.md'
        self.assertTrue(ws_hello.exists(), "Docs/ISL_HELLO_REVIEW_WORKSHEET.md must exist")
        self.assertTrue(ws_ty.exists(), "Docs/ISL_THANK_YOU_REVIEW_WORKSHEET.md must exist")


if __name__ == '__main__':
    unittest.main()
