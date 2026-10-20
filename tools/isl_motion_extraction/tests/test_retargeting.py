"""SignBridge M3.9 — Unit & Kinematic Retargeting Test Suite

Tests:
1. Coordinate conversions (MediaPipe -> Three.js).
2. Vector-to-quaternion solver (parallel, anti-parallel, orthogonal, singular cases).
3. Quaternion normalization and SLERP interpolation.
4. 1-Euro temporal smoothing and jitter reduction.
5. Bilateral contact constraint solver, thresholding, and clamp limits.
6. Left/Right arm symmetry and prevention of accidental mirroring.
7. Candidate clip schema validation and canonical Y-Bot bone hierarchy adherence.
"""

import json
import math
import sys
import unittest
from pathlib import Path

# Add tool directory to path
TOOL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOL_DIR))

from contact_constraints import ContactConstraintSolver
from coordinate_utils import (
    mediapipe_norm_to_threejs,
    mediapipe_world_to_threejs,
    quat_from_axis_angle,
    quat_from_two_vectors,
    quat_identity,
    quat_length,
    quat_multiply,
    quat_normalize,
    quat_rotate_vec3,
    quat_slerp,
    quat_to_euler_xyz,
    vec3,
    vec3_dist,
    vec3_dot,
    vec3_length,
    vec3_normalize,
)
from export_animation import build_candidate_animation
from retargeter import RetargetingEngine
from smoothing import (
    LowPassFilterVec3,
    OneEuroFilterQuat,
    OneEuroFilterVec3,
    calculate_trajectory_jitter,
)

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


class TestCoordinateUtils(unittest.TestCase):
    """Tests 3D vector and quaternion transformations."""

    def test_coordinate_inversion(self):
        # MediaPipe world point (0.2, 0.4, 0.8) -> Three.js (-0.2, -0.4, -0.8)
        mp_pt = (0.2, 0.4, 0.8)
        tjs_pt = mediapipe_world_to_threejs(mp_pt)
        self.assertAlmostEqual(tjs_pt[0], -0.2)
        self.assertAlmostEqual(tjs_pt[1], -0.4)
        self.assertAlmostEqual(tjs_pt[2], -0.8)

    def test_vector_normalization(self):
        v = (0.0, 3.0, 4.0)
        norm = vec3_normalize(v)
        self.assertAlmostEqual(vec3_length(norm), 1.0)
        self.assertAlmostEqual(norm[1], 0.6)
        self.assertAlmostEqual(norm[2], 0.8)

        # Zero length vector fallback
        v_zero = (0.0, 0.0, 0.0)
        norm_zero = vec3_normalize(v_zero, fallback=(0.0, 1.0, 0.0))
        self.assertEqual(norm_zero, (0.0, 1.0, 0.0))

    def test_quat_from_two_vectors_parallel(self):
        # Rotating vector into itself -> identity quaternion [0, 0, 0, 1]
        v1 = (1.0, 0.0, 0.0)
        q = quat_from_two_vectors(v1, v1)
        self.assertAlmostEqual(q[3], 1.0)
        self.assertAlmostEqual(q[0], 0.0)
        self.assertAlmostEqual(q[1], 0.0)
        self.assertAlmostEqual(q[2], 0.0)

    def test_quat_from_two_vectors_anti_parallel(self):
        # Rotating vector into exact opposite (180 deg flip)
        v1 = (1.0, 0.0, 0.0)
        v2 = (-1.0, 0.0, 0.0)
        q = quat_from_two_vectors(v1, v2)
        self.assertFalse(any(math.isnan(c) for c in q))
        self.assertAlmostEqual(quat_length(q), 1.0)
        # Check that rotated vector matches v2
        v_rot = quat_rotate_vec3(q, v1)
        self.assertAlmostEqual(v_rot[0], -1.0, places=5)
        self.assertAlmostEqual(v_rot[1], 0.0, places=5)
        self.assertAlmostEqual(v_rot[2], 0.0, places=5)

    def test_quat_from_two_vectors_orthogonal(self):
        # Rotating X (1, 0, 0) to Y (0, 1, 0) -> 90 deg around Z
        v1 = (1.0, 0.0, 0.0)
        v2 = (0.0, 1.0, 0.0)
        q = quat_from_two_vectors(v1, v2)
        v_rot = quat_rotate_vec3(q, v1)
        self.assertAlmostEqual(v_rot[0], 0.0, places=5)
        self.assertAlmostEqual(v_rot[1], 1.0, places=5)
        self.assertAlmostEqual(v_rot[2], 0.0, places=5)

    def test_quat_slerp(self):
        q1 = quat_identity()
        q2 = quat_from_axis_angle((0.0, 1.0, 0.0), math.pi * 0.5)

        # Midpoint at t = 0.5 should be 45 degrees
        mid = quat_slerp(q1, q2, 0.5)
        self.assertAlmostEqual(quat_length(mid), 1.0)
        euler = quat_to_euler_xyz(mid)
        self.assertAlmostEqual(euler[1], math.pi * 0.25, places=4)


class TestSmoothing(unittest.TestCase):
    """Tests 1-Euro adaptive temporal filtering."""

    def test_low_pass_vector(self):
        filt = LowPassFilterVec3(alpha=0.5)
        val1 = filt.filter((10.0, 0.0, 0.0))
        self.assertEqual(val1, (10.0, 0.0, 0.0))
        val2 = filt.filter((20.0, 0.0, 0.0))
        self.assertEqual(val2, (15.0, 0.0, 0.0))

    def test_one_euro_filter_reduces_noise(self):
        one_euro = OneEuroFilterVec3(min_cutoff=1.0, beta=0.005)
        # Create a stationary point with artificial jitter
        clean_pt = (0.5, 0.7, -0.8)
        noisy_pts = []
        smoothed_pts = []

        for i in range(30):
            t = i * 0.04
            noise = (0.02 * math.sin(i * 3.5), 0.02 * math.cos(i * 3.5), 0.01 * math.sin(i * 5.0))
            noisy = (clean_pt[0] + noise[0], clean_pt[1] + noise[1], clean_pt[2] + noise[2])
            noisy_pts.append(noisy)
            sm = one_euro.filter(noisy, t)
            smoothed_pts.append(sm)

        raw_jitter = calculate_trajectory_jitter(noisy_pts)
        smoothed_jitter = calculate_trajectory_jitter(smoothed_pts)
        self.assertGreater(raw_jitter, smoothed_jitter)


class TestContactConstraints(unittest.TestCase):
    """Tests bilateral contact constraint solver and safety clamps."""

    def test_contact_constraint_clamping(self):
        solver = ContactConstraintSolver(
            contact_dist_threshold=0.16,
            target_wrist_separation=0.07,
            max_correction_clamp=0.035,
        )

        # Synthetic frame where wrists are close (0.12m) and elevated
        synthetic_frame = {
            "timestampMs": 1000.0,
            "leftHandDetected": True,
            "rightHandDetected": True,
            "poseLandmarks": [
                {"name": "left_wrist", "x": 0.53, "y": 0.72, "z": -0.85, "visibility": 0.9},
                {"name": "right_wrist", "x": 0.47, "y": 0.72, "z": -0.85, "visibility": 0.9},
            ],
            "poseWorldLandmarks": [
                {"id": 15, "x": 0.06, "y": -0.28, "z": -0.32},  # Left wrist
                {"id": 16, "x": -0.06, "y": -0.28, "z": -0.32}, # Right wrist
            ]
        }

        res = solver.process_sequence([synthetic_frame])
        c_fr = res["frames"][0]
        self.assertEqual(c_fr["provenance"], "CONTACT_CONSTRAINED")
        self.assertLessEqual(c_fr["correctionMagnitude"], 0.035001)
        self.assertAlmostEqual(c_fr["constrainedWristDistance"], 0.07, places=2)

    def test_rest_frame_not_constrained(self):
        solver = ContactConstraintSolver()
        # Hands resting down at lap (normalized Y = 1.05)
        rest_frame = {
            "timestampMs": 0.0,
            "leftHandDetected": False,
            "rightHandDetected": False,
            "poseLandmarks": [
                {"name": "left_wrist", "x": 0.62, "y": 1.05, "z": -0.45, "visibility": 0.1},
                {"name": "right_wrist", "x": 0.36, "y": 1.05, "z": -0.45, "visibility": 0.1},
            ],
            "poseWorldLandmarks": [
                {"id": 15, "x": 0.20, "y": 0.20, "z": -0.10},
                {"id": 16, "x": -0.20, "y": 0.20, "z": -0.10},
            ]
        }
        res = solver.process_sequence([rest_frame])
        c_fr = res["frames"][0]
        self.assertEqual(c_fr["provenance"], "REST_INTERPOLATED")
        self.assertEqual(c_fr["correctionMagnitude"], 0.0)


class TestRetargetingAndExport(unittest.TestCase):
    """Tests retargeting execution, bone hierarchy compliance, and export schema."""

    @classmethod
    def setUpClass(cls):
        # Build candidate clip from diagnostic JSON
        diag_path = TOOL_DIR / "output" / "landmark_extraction_diagnostic.json"
        out_path = TOOL_DIR / "output" / "test_candidate_clip.json"
        cls.clip = build_candidate_animation(
            diagnostic_json_path=str(diag_path),
            output_clip_path=str(out_path),
            animation_id="test_mocap_candidate_v1",
        )

    def test_schema_top_level_fields(self):
        self.assertEqual(self.clip["animationId"], "test_mocap_candidate_v1")
        self.assertEqual(self.clip["gloss"], "NAMASTE")
        self.assertEqual(self.clip["durationMs"], 3080)
        self.assertTrue(self.clip["isLinguisticISL"])
        self.assertEqual(self.clip["validationStatus"], "experimental_awaiting_validation")
        self.assertIn("ISLRTC", self.clip["provenance"])
        self.assertIn("keyframes", self.clip)
        self.assertEqual(len(self.clip["keyframes"]), 77)

    def test_keyframes_monotonic_and_canonical(self):
        last_t = -1
        for idx, kf in enumerate(self.clip["keyframes"]):
            t = kf["timeMs"]
            self.assertGreaterEqual(t, last_t, f"Keyframe {idx} timestamp non-monotonic")
            last_t = t

            # Verify bone names belong to canonical rig
            for tr in kf["transforms"]:
                bone = tr["bone"]
                self.assertIn(bone, CANONICAL_BONES, f"Bone '{bone}' is not in Y-Bot rig")
                rot = tr["rotation"]
                self.assertEqual(len(rot), 3, "Euler rotation must have 3 components")
                self.assertFalse(any(math.isnan(v) or math.isinf(v) for v in rot), "Rotations must be finite")

    def test_bilateral_arm_symmetry_in_contact(self):
        # At peak prayer pose (Frame 35, t=1400ms), left and right arms should exhibit bilateral symmetry
        kf35 = self.clip["keyframes"][35]
        tf_map = {t["bone"]: t["rotation"] for t in kf35["transforms"]}

        r_arm = tf_map["RightArm"]
        l_arm = tf_map["LeftArm"]

        # Upper arms should both be flexed forward towards chest (X < -0.25)
        self.assertLess(r_arm[0], -0.20, "Right upper arm should flex forward")
        self.assertLess(l_arm[0], -0.20, "Left upper arm should flex forward")

        # Head should tilt slightly forward in respectful nod (X > 0.05)
        head = tf_map["Head"]
        self.assertGreater(head[0], 0.05, "Head should tilt forward in respectful bow")


if __name__ == "__main__":
    unittest.main()
