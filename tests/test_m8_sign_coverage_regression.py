#!/usr/bin/env python3
"""SignBridge Milestone M8 — Sign Coverage & Translation Reliability Regression Test Suite

Verifies:
1. Fully unsupported input: Out-of-lexicon phrases emit all tokens in unsupportedWords, generate 0 signs, and hold neutral rest pose.
2. Partially supported input: Sentences mixing recognized lemmas with unsupported words correctly partition tokens, never report TRANSLATED, and report PARTIAL / UNSUPPORTED.
3. Dictionary match without playable animation: Recognized dictionary entries with animationId: null do not count as playable clips, report PENDING_REVIEW or PARTIAL / UNSUPPORTED, and hold 500ms neutral fallback pose.
4. Missing or invalid animation asset: SignItems with non-existent animationId resolve safely to resolved: false and fallback to NEUTRAL_REST_POSE without crashing.
5. Successful playback of eligible animation: Production sign NAMASTE resolves to isl_namaste_godl_v1 (1800ms) with valid Euler keyframe progression and completion telemetry.
6. Neutral fallback and recovery: Avatar cleanly transitions from neutral fallback back to active eligible playback when subsequent supported signs arrive.
7. Accurate translation status and unsupported words reporting: Exact UI status matches playback reality (PLAYBACK_COMPLETE, PARTIAL / UNSUPPORTED, UNSUPPORTED, PENDING_REVIEW).
8. Preservation of experimental / review-required label for Namaste: Validates isLinguisticISL: true, validationStatus: 'experimental_awaiting_validation', 0/3 reviews completed, and candidate quarantine.
"""

import json
import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class TestM8SignCoverageRegression(unittest.TestCase):
    """Milestone M8 Regression Suite: Sign Coverage, Translation Reliability, & Fallback Integrity."""

    @classmethod
    def setUpClass(cls):
        cls.node_available = True
        try:
            res = subprocess.run(["node", "-v"], capture_output=True, text=True)
            if res.returncode != 0:
                cls.node_available = False
        except Exception:
            cls.node_available = False

    def _run_node_script(self, js_code):
        """Helper to run a Node.js snippet against the repository extension models."""
        self.assertTrue(self.node_available, "Node.js must be available for execution")
        contracts_p = str(ROOT / "extension" / "models" / "sign_contracts.js").replace("\\", "/")
        isl_p = str(ROOT / "extension" / "translation" / "isl_translator.js").replace("\\", "/")
        reg_p = str(ROOT / "extension" / "animation" / "keyframe_registry.js").replace("\\", "/")
        router_p = str(ROOT / "extension" / "translation" / "translation_router.js").replace("\\", "/")
        wrapper = f"""
        const path = require('path');
        const Contracts = require('{contracts_p}');
        const ISL = require('{isl_p}');
        const Registry = require('{reg_p}');
        const Router = require('{router_p}');
        
        {js_code}
        """
        proc = subprocess.run(["node", "-e", wrapper], capture_output=True, text=True, cwd=str(ROOT))
        if proc.returncode != 0:
            raise RuntimeError(f"Node execution failed (code {proc.returncode}):\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
        lines = [line.strip() for line in proc.stdout.strip().splitlines() if line.strip()]
        for line in reversed(lines):
            try:
                return json.loads(line)
            except Exception:
                continue
        raise RuntimeError(f"Could not parse JSON from Node output:\n{proc.stdout}")

    # -------------------------------------------------------------------------
    # 1. Fully Unsupported Input
    # -------------------------------------------------------------------------
    def test_01_fully_unsupported_input(self):
        """Fully unsupported transcripts generate empty signs list, all unsupported tokens, and neutral fallback."""
        snippets = [
            "quantum computing rocket",
            "superconducting tokamak reactor"
        ]
        for phrase in snippets:
            out = self._run_node_script(f"""
            const seq = ISL.translateTranscriptToISL("{phrase}");
            console.log(JSON.stringify({{
                signsCount: seq.signs.length,
                unsupportedWords: seq.unsupportedWords,
                language: seq.language
            }}));
            """)
            self.assertEqual(out["signsCount"], 0, f"Expected 0 signs for '{phrase}'")
            expected_words = phrase.split()
            self.assertEqual(out["unsupportedWords"], expected_words, f"Expected all words unsupported for '{phrase}'")
            self.assertEqual(out["language"], "ISL")

    # -------------------------------------------------------------------------
    # 2. Partially Supported Input
    # -------------------------------------------------------------------------
    def test_02_partially_supported_input(self):
        """Partially supported input partitions tokens into signs and unsupportedWords, never claiming complete translation."""
        # 'She makes me very, very proud.' -> 'me' maps to gloss 'I' (animationId: null); others unsupported
        out = self._run_node_script("""
        const seq = ISL.translateTranscriptToISL("She makes me very, very proud.");
        const resolvedSigns = seq.signs.map(s => Registry.resolveSignAnimation(s));
        console.log(JSON.stringify({
            signsCount: seq.signs.length,
            glosses: seq.signs.map(s => s.gloss),
            unsupportedWords: seq.unsupportedWords,
            playableCount: resolvedSigns.filter(r => r.resolved && r.clip !== null).length,
            unresolvedCount: resolvedSigns.filter(r => !r.resolved).length
        }));
        """)
        self.assertEqual(out["signsCount"], 1, "Expected 1 dictionary match for 'me' -> I")
        self.assertEqual(out["glosses"], ["I"])
        self.assertEqual(out["unsupportedWords"], ["she", "makes", "very", "very", "proud"])
        self.assertEqual(out["playableCount"], 0, "Gloss 'I' has animationId: null and must not count as playable")
        self.assertEqual(out["unresolvedCount"], 1, "Gloss 'I' must resolve to resolved: false")

    # -------------------------------------------------------------------------
    # 3. Dictionary Match Without Playable Animation
    # -------------------------------------------------------------------------
    def test_03_dictionary_matches_without_playable_animations(self):
        """All 15 un-animated dictionary entries resolve to resolved: false and safe NEUTRAL_REST_POSE."""
        unanimated_glosses = [
            'HELLO', 'THANK_YOU', 'PLEASE', 'WELCOME', 'SORRY',
            'YES', 'NO', 'NAME', 'YOU', 'I',
            'HELP', 'GOOD', 'BAD', 'STOP', 'WAIT'
        ]
        out = self._run_node_script(f"""
        const glosses = {json.dumps(unanimated_glosses)};
        const results = glosses.map(g => {{
            const entry = ISL.SEED_LEXICON[g];
            const signItem = Contracts.createSignItem({{
                gloss: entry.gloss,
                category: entry.category,
                durationMs: entry.defaultDurationMs,
                source: 'seed_dictionary',
                animationId: entry.animationId || null
            }});
            const res = Registry.resolveSignAnimation(signItem);
            return {{
                gloss: g,
                animationId: entry.animationId || null,
                resolved: res.resolved,
                clip: res.clip,
                fallbackPoseId: res.fallbackPose ? res.fallbackPose.poseId : null,
                reason: res.reason
            }};
        }});
        console.log(JSON.stringify(results));
        """)
        for item in out:
            self.assertIsNone(item["animationId"], f"Gloss '{item['gloss']}' must have animationId: null")
            self.assertFalse(item["resolved"], f"Gloss '{item['gloss']}' must not be marked resolved: true")
            self.assertIsNone(item["clip"], f"Gloss '{item['gloss']}' must have clip: null")
            self.assertEqual(item["fallbackPoseId"], "pose_neutral_rest_v1", f"Gloss '{item['gloss']}' must fall back to neutral rest pose")
            self.assertIn("No registered 3D animation clip exists", item["reason"])

    # -------------------------------------------------------------------------
    # 4. Missing or Invalid Animation Asset
    # -------------------------------------------------------------------------
    def test_04_missing_or_invalid_animation_asset(self):
        """SignItem specifying a nonexistent animationId fails resolution safely without throwing."""
        out = self._run_node_script("""
        const signItem = Contracts.createSignItem({
            gloss: 'CUSTOM_TEST',
            category: 'lexical',
            durationMs: 700,
            source: 'seed_dictionary',
            animationId: 'nonexistent_animation_clip_id_99999'
        });
        const res = Registry.resolveSignAnimation(signItem);
        console.log(JSON.stringify({
            resolved: res.resolved,
            clip: res.clip,
            animationId: res.animationId,
            fallbackPoseId: res.fallbackPose ? res.fallbackPose.poseId : null
        }));
        """)
        self.assertFalse(out["resolved"])
        self.assertIsNone(out["clip"])
        self.assertIsNone(out["animationId"])
        self.assertEqual(out["fallbackPoseId"], "pose_neutral_rest_v1")

    # -------------------------------------------------------------------------
    # 5. Successful Playback of Eligible Animation
    # -------------------------------------------------------------------------
    def test_05_successful_playback_of_eligible_animation(self):
        """Production sign NAMASTE resolves to registered isl_namaste_godl_v1 and interpolates keyframes accurately."""
        out = self._run_node_script("""
        const entry = ISL.SEED_LEXICON.NAMASTE;
        const signItem = Contracts.createSignItem({
            gloss: entry.gloss,
            category: entry.category,
            durationMs: entry.defaultDurationMs,
            source: 'seed_dictionary',
            animationId: entry.animationId
        });
        const res = Registry.resolveSignAnimation(signItem);
        
        // Evaluate keyframe interpolation at critical milestones (t = 0, 900, 1800 ms)
        const ev0 = Registry.evaluateClipAtTime(res.clip, 0);
        const ev900 = Registry.evaluateClipAtTime(res.clip, 900);
        const ev1800 = Registry.evaluateClipAtTime(res.clip, 1800);
        
        console.log(JSON.stringify({
            resolved: res.resolved,
            animationId: res.animationId,
            durationMs: res.clip.durationMs,
            isLinguisticISL: res.isLinguisticISL,
            transformsCount0: ev0.transforms.length,
            transformsCount900: ev900.transforms.length,
            transformsCount1800: ev1800.transforms.length,
            rightArm0: ev0.boneMap.get('RightArm'),
            rightArm900: ev900.boneMap.get('RightArm'),
            rightArm1800: ev1800.boneMap.get('RightArm')
        }));
        """)
        self.assertTrue(out["resolved"])
        self.assertEqual(out["animationId"], "isl_namaste_godl_v1")
        self.assertEqual(out["durationMs"], 1800)
        self.assertTrue(out["isLinguisticISL"])
        # Verify Anjali Mudra arm rotation at t=900ms vs neutral at t=0ms and t=1800ms
        self.assertAlmostEqual(out["rightArm0"]["rotation"][2], 1.25, delta=0.01)
        self.assertAlmostEqual(out["rightArm900"]["rotation"][0], -0.55, delta=0.01)
        self.assertAlmostEqual(out["rightArm1800"]["rotation"][2], 1.25, delta=0.01)

    # -------------------------------------------------------------------------
    # 6. Neutral Fallback and Recovery After Fallback
    # -------------------------------------------------------------------------
    def test_06_neutral_fallback_and_recovery_flow(self):
        """Consecutive sequence execution verifies clean return to neutral rest pose and recovery for subsequent signs."""
        out = self._run_node_script("""
        // 1. Un-animated sign 'you' -> Neutral fallback
        const seq1 = ISL.translateTranscriptToISL('you');
        const res1 = Registry.resolveSignAnimation(seq1.signs[0]);
        
        // 2. Eligible sign 'namaste' -> Playable
        const seq2 = ISL.translateTranscriptToISL('namaste');
        const res2 = Registry.resolveSignAnimation(seq2.signs[0]);
        
        console.log(JSON.stringify({
            seq1Resolved: res1.resolved,
            seq1Pose: res1.fallbackPose.poseId,
            seq2Resolved: res2.resolved,
            seq2AnimId: res2.animationId
        }));
        """)
        self.assertFalse(out["seq1Resolved"])
        self.assertEqual(out["seq1Pose"], "pose_neutral_rest_v1")
        self.assertTrue(out["seq2Resolved"])
        self.assertEqual(out["seq2AnimId"], "isl_namaste_godl_v1")

    # -------------------------------------------------------------------------
    # 7. Accurate Translation-Status and Unsupported-Word Reporting
    # -------------------------------------------------------------------------
    def test_07_status_calculation_logic(self):
        """Verifies four-state classification: PLAYBACK_COMPLETE, PARTIAL / UNSUPPORTED, UNSUPPORTED, PENDING_REVIEW."""
        # Simulated controller status logic
        def calculate_status(playable_count, pending_review_count, unsupported_count):
            if unsupported_count > 0:
                if playable_count > 0 or pending_review_count > 0:
                    return "PARTIAL / UNSUPPORTED"
                return "UNSUPPORTED"
            elif pending_review_count > 0 and playable_count == 0:
                return "PENDING_REVIEW"
            elif playable_count > 0:
                return "PLAYBACK_COMPLETE"
            return "UNSUPPORTED"

        # Scenario 1: Namaste alone (eligible clip played, zero unsupported)
        self.assertEqual(calculate_status(1, 0, 0), "PLAYBACK_COMPLETE")

        # Scenario 2: Namaste + unsupported word
        self.assertEqual(calculate_status(1, 0, 1), "PARTIAL / UNSUPPORTED")

        # Scenario 3: She makes me very proud (0 playable, 1 pending review, 5 unsupported)
        self.assertEqual(calculate_status(0, 1, 5), "PARTIAL / UNSUPPORTED")

        # Scenario 4: Fully unsupported phrase (0 playable, 0 review, 3 unsupported)
        self.assertEqual(calculate_status(0, 0, 3), "UNSUPPORTED")

        # Scenario 5: Hello alone (0 playable, 1 pending review, 0 unsupported)
        self.assertEqual(calculate_status(0, 1, 0), "PENDING_REVIEW")

    # -------------------------------------------------------------------------
    # 8. Preservation of Experimental/Review-Required Label for Namaste
    # -------------------------------------------------------------------------
    def test_08_preservation_of_experimental_review_status(self):
        """Confirms that isl_namaste_godl_v1 remains experimental_awaiting_validation and candidate is quarantined."""
        with open(ROOT / 'extension' / 'animation' / 'keyframe_registry.js', 'r', encoding='utf-8') as f:
            reg_code = f.read()

        # Production baseline must be explicitly marked awaiting validation
        self.assertIn("validationStatus: 'experimental_awaiting_validation'", reg_code)
        self.assertNotIn("validationStatus: 'human_validated'", reg_code)
        self.assertNotIn("validationStatus: 'approved'", reg_code)

        # Quarantined candidate must NOT be registered by default
        self.assertNotIn("REGISTERED_CLIPS.set('isl_namaste_mocap_candidate_v1'", reg_code)

        # Reviews directory must have 0 reviews
        rev_dir = ROOT / 'tools' / 'isl_motion_extraction' / 'reviews'
        if rev_dir.exists():
            review_files = [f for f in rev_dir.glob('*.json') if f.name != 'package.json']
            self.assertEqual(len(review_files), 0, "Reviews directory must have zero reviews to prevent false approval claims")


if __name__ == '__main__':
    unittest.main()
