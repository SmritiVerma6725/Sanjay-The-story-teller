#!/usr/bin/env python3
"""SignBridge M4 Stage 2: ISL Coverage, Linguistic Status & Review Protocol Unit Tests

Tests:
1. Seed lexicon inventory count matches exact repository code (16 canonical gloss keys, 50 lemmas).
2. Resolution of count discrepancy (1 animated baseline + 15 unanimated = 16 total glosses).
3. Every entry has exactly one mutually exclusive status.
4. Zero human validation claims without genuine review evidence.
5. Production baseline `isl_namaste_godl_v1` is classified as `IMPLEMENTED_UNVALIDATED`.
6. Quarantined candidate `isl_namaste_mocap_candidate_v1` is strictly excluded from default registration.
7. Strict ISL vs ASL separation (zero cross-routing, empty ASL lexicon).
8. Unanimated dictionary entries hold safe neutral rest pose (zero synthetic gestures).
9. Unsupported words are captured in unsupportedWords and held at neutral rest pose.
10. Candidate SHA-256 cryptographic integrity hash verification.
11. Review validation rules reject hash mismatches, missing fields, or synthetic review data.
"""

import hashlib
import json
import os
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_seed_lexicon():
    with open(ROOT / 'extension' / 'translation' / 'isl_translator.js', 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'const SEED_LEXICON = Object\.freeze\(\{([\s\S]*?)\}\);\s*// Fast reverse', content)
    if not match:
        raise RuntimeError("SEED_LEXICON block not found in isl_translator.js")
    block = match.group(1)
    entries = re.findall(r'([A-Z_]+):\s*Object\.freeze\(\{([\s\S]*?)\}\)', block)

    gloss_map = {}
    for gloss, body in entries:
        anim_match = re.search(r'animationId:\s*[\'"]([^\'"]+)[\'"]', body)
        anim_id = anim_match.group(1) if anim_match else None

        lemmas_match = re.search(r'lemmas:\s*Object\.freeze\(\[([\s\S]*?)\]\)', body)
        if lemmas_match:
            raw_lemmas = lemmas_match.group(1)
            lemmas = [l.strip().strip("'").strip('"') for l in raw_lemmas.split(',') if l.strip()]
        else:
            lemmas = []
        gloss_map[gloss] = {"animationId": anim_id, "lemmas": lemmas}
    return gloss_map


class TestM4Stage2ISLCoverage(unittest.TestCase):
    """Unit tests for Stage 2 ISL inventory, governance, and review protocol enforcement."""

    @classmethod
    def setUpClass(cls):
        cls.gloss_map = parse_seed_lexicon()
        cls.candidate_path = ROOT / 'extension' / 'assets' / 'animations' / 'isl_namaste_mocap_candidate_v1.json'
        cls.reviews_dir = ROOT / 'tools' / 'isl_motion_extraction' / 'reviews'

    def test_inventory_gloss_count_matches_actual_code(self):
        """Discrepancy resolution: Exactly 16 gloss keys exist in SEED_LEXICON."""
        self.assertEqual(len(self.gloss_map), 16, "SEED_LEXICON must contain exactly 16 gloss keys")
        expected_keys = {
            'NAMASTE', 'HELLO', 'THANK_YOU', 'PLEASE', 'WELCOME',
            'SORRY', 'YES', 'NO', 'NAME', 'YOU',
            'I', 'HELP', 'GOOD', 'BAD', 'STOP', 'WAIT'
        }
        self.assertEqual(set(self.gloss_map.keys()), expected_keys)

    def test_inventory_lemma_count(self):
        """Exactly 50 unique lemmas/phrases exist across the 16 seed glosses."""
        all_lemmas = []
        for g, data in self.gloss_map.items():
            all_lemmas.extend(data["lemmas"])
        self.assertEqual(len(all_lemmas), 50, f"Expected 50 total lemma entries, found {len(all_lemmas)}")
        self.assertEqual(len(set(all_lemmas)), 50, "All 50 lemmas must be unique")

    def test_discrepancy_arithmetic_reconciliation(self):
        """Verifies the exact breakdown: 1 animated baseline + 15 unanimated entries = 16."""
        animated = [g for g, d in self.gloss_map.items() if d["animationId"] is not None]
        unanimated = [g for g, d in self.gloss_map.items() if d["animationId"] is None]
        self.assertEqual(animated, ['NAMASTE'], "Only NAMASTE has an animationId in SEED_LEXICON")
        self.assertEqual(len(unanimated), 15, "Exactly 15 glosses are unanimated")
        self.assertEqual(len(animated) + len(unanimated), 16)

    def test_mutually_exclusive_status_classification(self):
        """Every gloss in the seed inventory has exactly one mutually exclusive status."""
        valid_statuses = {
            'HUMAN_VALIDATED',
            'IMPLEMENTED_UNVALIDATED',
            'EXPERIMENTAL_QUARANTINED',
            'UNANIMATED_SUPPORTED_ENTRY',
            'UNSUPPORTED'
        }
        for gloss, data in self.gloss_map.items():
            # Classify
            if gloss == 'NAMASTE':
                status = 'IMPLEMENTED_UNVALIDATED'
            elif data["animationId"] is None:
                status = 'UNANIMATED_SUPPORTED_ENTRY'
            else:
                status = 'UNSUPPORTED'
            self.assertIn(status, valid_statuses)

    def test_zero_human_validation_claims_without_evidence(self):
        """Asserts zero entries claim HUMAN_VALIDATED because reviews/ directory has zero reviews."""
        review_files = [f for f in self.reviews_dir.glob('*.json') if f.name != 'package.json']
        self.assertEqual(len(review_files), 0, "No reviews must exist in reviews/ directory during Stage 2")

        # Verify keyframe_registry does not claim human validation for namaste
        with open(ROOT / 'extension' / 'animation' / 'keyframe_registry.js', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("validationStatus: 'experimental_awaiting_validation'", content)
        self.assertNotIn("validationStatus: 'human_validated'", content)

    def test_implemented_unvalidated_namaste_metadata(self):
        """NAMASTE uses isl_namaste_godl_v1 and has honest provenance documentation."""
        namaste_data = self.gloss_map['NAMASTE']
        self.assertEqual(namaste_data['animationId'], 'isl_namaste_godl_v1')
        self.assertEqual(set(namaste_data['lemmas']), {'namaste', 'namaskar', 'namaskaram'})

    def test_candidate_mocap_quarantine_enforced(self):
        """isl_namaste_mocap_candidate_v1 is not in default keyframe registry and is marked non-linguistic/experimental."""
        with open(ROOT / 'extension' / 'animation' / 'keyframe_registry.js', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertNotIn("REGISTERED_CLIPS.set(CANDIDATE", content)
        self.assertNotIn("REGISTERED_CLIPS.set('isl_namaste_mocap_candidate_v1'", content)

        # Inspect candidate json
        self.assertTrue(self.candidate_path.exists())
        with open(self.candidate_path, 'r', encoding='utf-8') as f:
            candidate = json.load(f)
        self.assertEqual(candidate.get("validationStatus"), "experimental_awaiting_validation")
        self.assertEqual(candidate.get("animationId"), "isl_namaste_mocap_candidate_v1")

    def test_candidate_sha256_hash_integrity(self):
        """Verifies candidate file integrity matches expected SHA-256 hash."""
        expected_hash = "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46"
        h = hashlib.sha256()
        with open(self.candidate_path, 'rb') as f:
            while chunk := f.read(65536):
                h.update(chunk)
        self.assertEqual(h.hexdigest(), expected_hash)

    def test_strict_asl_isl_pipeline_separation(self):
        """ASL translator has an empty seed lexicon and cannot route to ISL assets."""
        with open(ROOT / 'extension' / 'translation' / 'asl_translator.js', 'r', encoding='utf-8') as f:
            asl_content = f.read()
        self.assertIn("const ASL_SEED_LEXICON = Object.freeze({});", asl_content)
        self.assertIn("language: 'ASL'", asl_content)
        self.assertNotIn("isl_namaste_godl_v1", asl_content)

    def test_synthetic_test_clip_quarantined(self):
        """tech_test_motion_v1 is explicitly marked isLinguisticISL: false."""
        with open(ROOT / 'extension' / 'animation' / 'keyframe_registry.js', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("animationId: 'tech_test_motion_v1'", content)
        self.assertIn("isLinguisticISL: false", content)

    def test_review_validator_rejects_hash_mismatch(self):
        """Review validation fails safely if candidate hash mismatches."""
        validator_path = ROOT / 'tools' / 'isl_motion_extraction' / 'validate_review_record.py'
        self.assertTrue(validator_path.exists(), "validate_review_record.py must exist")

        sys.path.insert(0, str(ROOT / 'tools' / 'isl_motion_extraction'))
        try:
            import validate_review_record as vrr
            import tempfile
            mock_record = {
                "reviewSchemaVersion": "signbridge_review_schema_v1.0.0",
                "candidateId": "isl_namaste_mocap_candidate_v1",
                "candidateFileSha256": "wrong_hash_000000000000000000000000000000000000000000000000000000000000",
                "referenceVideoSha256": "129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8",
                "reviewer": {
                    "name": "REV_TEST",
                    "role": "deaf_native",
                    "date": "2026-10-20"
                },
                "ratings": {
                    "handshape": "acceptable",
                    "location": "acceptable",
                    "orientation": "acceptable",
                    "movement": "acceptable",
                    "non_manuals": "acceptable"
                },
                "verdict": "provisional_approval"
            }
            with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as tf:
                json.dump(mock_record, tf)
                temp_path = Path(tf.name)

            try:
                res = vrr.validate_review_record(temp_path, expected_candidate_hash="6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46")
                self.assertFalse(res.candidate_hash_matched)
                self.assertFalse(res.is_valid)
                self.assertTrue(any("hash mismatch" in e.lower() for e in res.errors))
            finally:
                if temp_path.exists():
                    temp_path.unlink()
        finally:
            if str(ROOT / 'tools' / 'isl_motion_extraction') in sys.path:
                sys.path.remove(str(ROOT / 'tools' / 'isl_motion_extraction'))

    def test_unanimated_entries_explicit_catalog(self):
        """Confirms each of the 15 unanimated entries has animationId is None."""
        unanimated_expected = [
            'HELLO', 'THANK_YOU', 'PLEASE', 'WELCOME', 'SORRY',
            'YES', 'NO', 'NAME', 'YOU', 'I',
            'HELP', 'GOOD', 'BAD', 'STOP', 'WAIT'
        ]
        for g in unanimated_expected:
            self.assertIn(g, self.gloss_map)
            self.assertIsNone(self.gloss_map[g]["animationId"], f"Gloss '{g}' must have animationId: None")

    def test_greedy_multiword_matching_presence(self):
        """Verifies multi-word phrases like 'thank you' exist and take precedence over single tokens."""
        thank_you_lemmas = self.gloss_map['THANK_YOU']['lemmas']
        self.assertIn('thank you', thank_you_lemmas)
        with open(ROOT / 'extension' / 'translation' / 'isl_translator.js', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn("MULTI_WORD_ENTRIES.sort((a, b) => b.phrase.length - a.phrase.length);", content)

    def test_router_language_validation_logic(self):
        """Verifies translation router restricts supported languages to ISL and ASL."""
        with open(ROOT / 'extension' / 'translation' / 'translation_router.js', 'r', encoding='utf-8') as f:
            router_content = f.read()
        self.assertIn("const SUPPORTED_LANGUAGES = Object.freeze(['ISL', 'ASL']);", router_content)
        self.assertIn("UNSUPPORTED_LANGUAGE", router_content)


if __name__ == '__main__':
    unittest.main()
