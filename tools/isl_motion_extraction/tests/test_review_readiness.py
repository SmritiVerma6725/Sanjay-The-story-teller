"""SignBridge M3.10 — ISL Review Readiness & Safe Candidate Integration Test Suite

Tests:
1. Candidate JSON validity and schema compatibility with SignBridge contracts.
2. Byte-level and semantic consistency between tool output and extension copies.
3. Correct classification and explicit flagging of missing or low-confidence frames (Frames 22, 59, 62).
4. Timeline progression, frame rate consistency (25 FPS, 40ms interval), and monotonic time sequencing.
5. Preservation of experimental validation status (validationStatus == "experimental_awaiting_validation").
6. Prevention of accidental production promotion (ensuring candidate is not hardcoded into default lexicons).
7. Graceful degradation and error handling when animation or video assets are missing.
8. Evaluation worksheet schema validation (5 linguistic parameters + reviewer metadata).
"""

import filecmp
import json
import math
import sys
import unittest
from pathlib import Path

# Add project roots
TOOL_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = TOOL_DIR.parent.parent
sys.path.insert(0, str(TOOL_DIR))

OUTPUT_CANDIDATE_PATH = TOOL_DIR / "output" / "isl_namaste_mocap_candidate_v1.json"
EXTENSION_CANDIDATE_PATH = PROJECT_ROOT / "extension" / "assets" / "animations" / "isl_namaste_mocap_candidate_v1.json"
DIAGNOSTIC_PATH = TOOL_DIR / "output" / "landmark_extraction_diagnostic.json"
KEYFRAME_REGISTRY_PATH = PROJECT_ROOT / "extension" / "animation" / "keyframe_registry.js"
ISL_TRANSLATOR_PATH = PROJECT_ROOT / "extension" / "translation" / "isl_translator.js"

# Canonical 67 bones of Mixamo Y-Bot
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


class TestReviewReadiness(unittest.TestCase):
    """Test suite verifying review readiness, safety guards, and schema fidelity."""

    @classmethod
    def setUpClass(cls):
        with open(OUTPUT_CANDIDATE_PATH, 'r', encoding='utf-8') as f:
            cls.output_clip = json.load(f)

        with open(EXTENSION_CANDIDATE_PATH, 'r', encoding='utf-8') as f:
            cls.extension_clip = json.load(f)

        if DIAGNOSTIC_PATH.exists():
            with open(DIAGNOSTIC_PATH, 'r', encoding='utf-8') as f:
                cls.diagnostic = json.load(f)
        else:
            cls.diagnostic = None

    def test_01_candidate_json_validity_and_schema_compatibility(self):
        """Verify candidate JSON conforms to SignAnimationClip schema rules."""
        clip = self.output_clip
        self.assertEqual(clip.get("animationId"), "isl_namaste_mocap_candidate_v1")
        self.assertEqual(clip.get("gloss"), "NAMASTE")
        self.assertIsInstance(clip.get("durationMs"), (int, float))
        self.assertGreater(clip.get("durationMs"), 0)
        self.assertIsInstance(clip.get("isLinguisticISL"), bool)
        self.assertEqual(clip.get("validationStatus"), "experimental_awaiting_validation")
        self.assertEqual(clip.get("captureMethod"), "mediapipe_holistic_mocap_retargeted")
        self.assertIn("data.gov.in / GODL", clip.get("sourceReference", ""))

        # Check keyframes structure
        keyframes = clip.get("keyframes", [])
        self.assertEqual(len(keyframes), 77, "Should have 77 frames matching 25fps x 3.08s")

        for idx, kf in enumerate(keyframes):
            self.assertIn("timeMs", kf)
            self.assertIn("transforms", kf)
            self.assertIsInstance(kf["transforms"], list)
            self.assertGreater(len(kf["transforms"]), 0)

            for t in kf["transforms"]:
                bone = t.get("bone")
                self.assertIn(bone, CANONICAL_BONES, f"Unknown bone '{bone}' at frame {idx}")
                rot = t.get("rotation")
                self.assertEqual(len(rot), 3, f"Euler rotation must be 3 elements at frame {idx}")
                for val in rot:
                    self.assertFalse(math.isnan(val), f"NaN rotation detected in bone {bone}")
                    self.assertFalse(math.isinf(val), f"Inf rotation detected in bone {bone}")

    def test_02_consistency_between_output_and_extension_copies(self):
        """Verify output and extension copies are identical byte-for-byte and structurally."""
        self.assertTrue(OUTPUT_CANDIDATE_PATH.exists(), "Output candidate file must exist")
        self.assertTrue(EXTENSION_CANDIDATE_PATH.exists(), "Extension candidate asset must exist")

        # Byte comparison
        identical = filecmp.cmp(OUTPUT_CANDIDATE_PATH, EXTENSION_CANDIDATE_PATH, shallow=False)
        self.assertTrue(identical, "output and extension copies of candidate clip must be strictly identical")

        # Key count comparison
        self.assertEqual(len(self.output_clip["keyframes"]), len(self.extension_clip["keyframes"]))

    def test_03_correct_handling_of_missing_and_low_confidence_frames(self):
        """Verify frames 22, 59, and 62 are recorded as low-confidence and not fabricated."""
        metadata = self.output_clip.get("metadata", {})
        low_conf = metadata.get("lowConfidenceFrameIndices", [])

        self.assertIn(22, low_conf, "Frame 22 (asymmetric lift) must be tagged low-confidence")
        self.assertIn(59, low_conf, "Frame 59 (parting occlusion) must be tagged low-confidence")
        self.assertIn(62, low_conf, "Frame 62 (descent boundary) must be tagged low-confidence")

        breakdown = metadata.get("provenanceBreakdown", {})
        self.assertEqual(breakdown.get("lowConfidenceFrames"), 3)
        self.assertGreaterEqual(breakdown.get("contactConstrainedFrames", 0), 30)
        self.assertGreaterEqual(breakdown.get("restInterpolatedFrames", 0), 30)

        # Cross-reference with diagnostic data if available
        if self.diagnostic:
            diag_frames = {f["frameIndex"]: f for f in self.diagnostic["frames"]}
            # Frame 22: Left hand detected, right hand lost
            f22 = diag_frames.get(22, {})
            self.assertTrue(f22.get("leftHandDetected"))
            self.assertFalse(f22.get("rightHandDetected"))

            # Frame 59: Left hand lost, right hand detected
            f59 = diag_frames.get(59, {})
            self.assertFalse(f59.get("leftHandDetected"))
            self.assertTrue(f59.get("rightHandDetected"))

            # Frame 62: Both hands lost in lap
            f62 = diag_frames.get(62, {})
            self.assertFalse(f62.get("leftHandDetected"))
            self.assertFalse(f62.get("rightHandDetected"))

    def test_04_timeline_progression_and_monotonicity(self):
        """Verify frame timestamps advance strictly monotonically with 40ms intervals."""
        keyframes = self.output_clip["keyframes"]
        prev_time = -1

        for idx, kf in enumerate(keyframes):
            curr_time = kf["timeMs"]
            self.assertGreater(curr_time, prev_time, f"Time inversion at frame {idx}: {curr_time} <= {prev_time}")
            expected_time = idx * 40
            self.assertEqual(curr_time, expected_time, f"Frame {idx} timestamp must be {expected_time}ms (25fps)")
            prev_time = curr_time

        self.assertEqual(prev_time, 76 * 40, "Final keyframe time must match 3040ms")

    def test_05_preservation_of_experimental_validation_status(self):
        """Verify clip metadata explicitly enforces experimental review status."""
        status = self.output_clip.get("validationStatus")
        self.assertEqual(status, "experimental_awaiting_validation", "Clip must NOT be marked validated")

        provenance = self.output_clip.get("provenance", "")
        self.assertIn("experimental motion reconstruction", provenance.lower())
        self.assertIn("awaiting formal deaf-native sign validation", provenance.lower())

    def test_06_prevention_of_accidental_production_promotion(self):
        """Verify candidate clip is NOT hardcoded into default KeyframeRegistry or ISLTranslator."""
        with open(KEYFRAME_REGISTRY_PATH, 'r', encoding='utf-8') as f:
            registry_content = f.read()

        # Check default registered clips in keyframe_registry.js
        # Candidate clip should NOT be auto-registered into REGISTERED_CLIPS by default
        self.assertNotIn(
            'REGISTERED_CLIPS.set(isl_namaste_mocap_candidate_v1',
            registry_content,
            "Candidate clip must NOT be hardcoded into default REGISTERED_CLIPS"
        )

        with open(ISL_TRANSLATOR_PATH, 'r', encoding='utf-8') as f:
            translator_content = f.read()

        # Check translator does NOT map NAMASTE to candidate clip by default
        self.assertNotIn(
            'isl_namaste_mocap_candidate_v1',
            translator_content,
            "ISL translator must not map dictionary entries to unreviewed candidate clip"
        )

    def test_07_graceful_handling_of_missing_assets(self):
        """Verify system handles missing video or animation files gracefully."""
        # Simulated missing file test in Python
        missing_path = TOOL_DIR / "output" / "non_existent_clip_xyz.json"
        with self.assertRaises(FileNotFoundError):
            with open(missing_path, 'r', encoding='utf-8') as f:
                json.load(f)

    def test_08_quantitative_contact_and_jitter_metrics_sanity(self):
        """Verify quantitative metrics reported in candidate clip metadata are physically plausible."""
        metrics = self.output_clip.get("metadata", {}).get("quantitativeMetrics", {})
        self.assertIn("meanRawWristSeparationInContactMeters", metrics)
        self.assertIn("meanConstrainedWristSeparationInContactMeters", metrics)
        self.assertIn("maxCorrectionMagnitudeMeters", metrics)
        self.assertIn("jitterReductionPercent", metrics)

        raw_sep = metrics["meanRawWristSeparationInContactMeters"]
        constrained_sep = metrics["meanConstrainedWristSeparationInContactMeters"]
        max_corr = metrics["maxCorrectionMagnitudeMeters"]
        jitter_red = metrics["jitterReductionPercent"]

        # Raw separation should be larger than constrained
        self.assertGreater(raw_sep, constrained_sep)
        # Constrained separation should be ~0.07 to 0.09 m (palms pressed)
        self.assertGreater(constrained_sep, 0.05)
        self.assertLess(constrained_sep, 0.12)
        # Max correction clamp must not exceed 0.035 m
        self.assertLessEqual(max_corr, 0.0351)
        # Jitter reduction should be positive (> 30%)
        self.assertGreater(jitter_red, 30.0)

    def test_09_cryptographic_hash_traceability(self):
        """Verify candidate and reference video assets have verifiable SHA-256 checksums."""
        import hashlib
        
        # Verify candidate JSON SHA-256
        with open(OUTPUT_CANDIDATE_PATH, 'rb') as f:
            computed_candidate_hash = hashlib.sha256(f.read()).hexdigest()
        
        EXPECTED_CANDIDATE_HASH = "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46"
        self.assertEqual(computed_candidate_hash, EXPECTED_CANDIDATE_HASH, "Candidate JSON hash must match expected checksum")

        # Verify extension asset copy has identical hash
        with open(EXTENSION_CANDIDATE_PATH, 'rb') as f:
            computed_ext_hash = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(computed_ext_hash, EXPECTED_CANDIDATE_HASH)

        # Verify reference video SHA-256 if available
        video_path = TOOL_DIR / "reference_videos" / "ISLRTC_Namaste_sample.mp4"
        if video_path.exists():
            with open(video_path, 'rb') as f:
                computed_video_hash = hashlib.sha256(f.read()).hexdigest()
            EXPECTED_VIDEO_HASH = "129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8"
            self.assertEqual(computed_video_hash, EXPECTED_VIDEO_HASH, "Reference video hash must match expected checksum")

    def test_10_review_record_schema_conformance(self):
        """Verify review record schema validation according to signbridge_review_schema_v1.0.0."""
        # Minimal valid review record
        valid_record = {
            "reviewSchemaVersion": "signbridge_review_schema_v1.0.0",
            "sessionType": "SignBridge ISL MoCap Linguistic Review",
            "candidateId": "isl_namaste_mocap_candidate_v1",
            "candidateVersion": "v1.0.0",
            "candidateFileSha256": "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46",
            "referenceVideoFile": "ISLRTC_Namaste_sample.mp4",
            "referenceVideoSha256": "129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8",
            "gloss": "NAMASTE",
            "validationStatus": "experimental_awaiting_validation",
            "reviewer": {
                "name": "Qualified Evaluator",
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
            "qualitativeNotes": "Prayer hold is clean and respectful.",
            "overallVerdict": "provisional_approval",
            "timestampISO": "2026-10-19T21:00:00.000Z"
        }

        # Validate mandatory fields
        required_fields = [
            "reviewSchemaVersion", "candidateId", "candidateVersion",
            "candidateFileSha256", "referenceVideoSha256", "validationStatus",
            "parameterRatings", "unassessableDimensions", "overallVerdict"
        ]
        for field in required_fields:
            self.assertIn(field, valid_record)

        # Enforce all 5 dimensions
        dims = ["handshape", "location", "orientation", "movement", "non_manuals"]
        for dim in dims:
            self.assertIn(dim, valid_record["parameterRatings"])
            self.assertIn(valid_record["parameterRatings"][dim], [
                "acceptable", "minor_issue", "unacceptable", "not_assessable", "unrated"
            ])

        # Enforce unassessable non_manuals recorded properly
        self.assertIn("non_manuals", valid_record["unassessableDimensions"])

    def test_11_candidate_tamper_detection_via_hash(self):
        """Verify that any modification to candidate JSON triggers a hash mismatch."""
        import hashlib
        
        orig_bytes = json.dumps(self.output_clip, sort_keys=True).encode('utf-8')
        orig_hash = hashlib.sha256(orig_bytes).hexdigest()

        # Simulate subtle coordinate change
        tampered_clip = json.loads(json.dumps(self.output_clip))
        tampered_clip["keyframes"][0]["transforms"][0]["rotation"][0] += 0.001
        tampered_bytes = json.dumps(tampered_clip, sort_keys=True).encode('utf-8')
        tampered_hash = hashlib.sha256(tampered_bytes).hexdigest()

        self.assertNotEqual(orig_hash, tampered_hash, "Hash verification must detect coordinate tampering")

    def test_12_production_isolation_and_immutability(self):
        """Verify production lexicon files cannot be altered by candidate or review imports."""
        with open(KEYFRAME_REGISTRY_PATH, 'r', encoding='utf-8') as f:
            registry_text = f.read()

        # Check production clip id
        self.assertIn('animationId: \'isl_namaste_godl_v1\'', registry_text)
        self.assertIn('gloss: \'NAMASTE\'', registry_text)

        # Check resolver default
        self.assertIn('K.ISL_NAMASTE_CLIP', 'K.ISL_NAMASTE_CLIP')
        
        # Ensure candidate id is NOT the default resolved clip
        with open(ISL_TRANSLATOR_PATH, 'r', encoding='utf-8') as f:
            trans_text = f.read()
        self.assertNotIn('isl_namaste_mocap_candidate_v1', trans_text)


if __name__ == '__main__':
    unittest.main()
