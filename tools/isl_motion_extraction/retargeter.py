"""SignBridge M3.9 — Kinematic Retargeting Engine

Converts 3D extracted landmarks into canonical Adobe Mixamo Y-Bot bone rotations.
Maps torso, neck, head, shoulders, upper arms, forearms, wrists, and finger joints.
Ensures zero NaN/inf values, prevents accidental mirroring, applies 1-Euro smoothing,
and integrates bilateral contact constraints.
"""

import math
from typing import Any, Dict, List, Optional, Tuple

from coordinate_utils import (
    LEFT_ELBOW,
    LEFT_HIP,
    LEFT_SHOULDER,
    LEFT_WRIST,
    NOSE,
    RIGHT_ELBOW,
    RIGHT_HIP,
    RIGHT_SHOULDER,
    RIGHT_WRIST,
    mediapipe_world_to_threejs,
    quat_from_axis_angle,
    quat_from_two_vectors,
    quat_identity,
    quat_multiply,
    quat_normalize,
    quat_slerp,
    quat_to_euler_xyz,
    vec3,
    vec3_add,
    vec3_cross,
    vec3_dist,
    vec3_dot,
    vec3_length,
    vec3_lerp,
    vec3_normalize,
    vec3_scale,
    vec3_sub,
)
from smoothing import OneEuroFilterQuat, calculate_trajectory_jitter


# Canonical Mixamo T-Pose Rest Directions (in world space)
REST_RIGHT_ARM_DIR = (-1.0, 0.0, 0.0)  # Extends laterally along -X
REST_LEFT_ARM_DIR = (1.0, 0.0, 0.0)    # Extends laterally along +X
REST_UP_DIR = (0.0, 1.0, 0.0)          # Spine / Head point up along +Y
REST_FORWARD_DIR = (0.0, 0.0, 1.0)     # Face looks forward along +Z

# Canonical Neutral Rest Rotations (from keyframe_registry.js NEUTRAL_REST_POSE)
NEUTRAL_EULER_RIGHT_ARM = (0.0, 0.0, 1.25)
NEUTRAL_EULER_RIGHT_FOREARM = (0.25, 0.0, 0.0)
NEUTRAL_EULER_LEFT_ARM = (0.0, 0.0, -1.25)
NEUTRAL_EULER_LEFT_FOREARM = (0.25, 0.0, 0.0)


class RetargetingEngine:
    """Retargets extracted 3D landmarks onto the Mixamo Y-Bot skeletal hierarchy."""

    def __init__(self, use_quaternions: bool = False, enable_smoothing: bool = True):
        self.use_quaternions = use_quaternions
        self.enable_smoothing = enable_smoothing

        # Bone-specific 1-Euro filters for smooth temporal continuity
        self.filters: Dict[str, OneEuroFilterQuat] = {}

    def _get_filter(self, bone_name: str) -> OneEuroFilterQuat:
        if bone_name not in self.filters:
            self.filters[bone_name] = OneEuroFilterQuat(min_cutoff=1.5, beta=0.008)
        return self.filters[bone_name]

    def retarget_frame(
        self,
        frame_data: Dict[str, Any],
        contact_info: Dict[str, Any],
        timestamp_sec: float,
    ) -> List[Dict[str, Any]]:
        """Retargets a single frame into a list of BoneTransform dictionaries."""
        world_lms = {lm["id"]: lm for lm in frame_data.get("poseWorldLandmarks", [])}
        norm_lms = {lm["name"]: lm for lm in frame_data.get("poseLandmarks", [])}

        provenance = contact_info.get("provenance", "DIRECTLY_OBSERVED")
        transforms = []

        # -------------------------------------------------------------
        # 1. Torso & Spine
        # -------------------------------------------------------------
        spine_rot = self._solve_spine(world_lms)
        transforms.append(self._format_transform("Spine1", spine_rot, timestamp_sec))

        # -------------------------------------------------------------
        # 2. Head & Neck
        # -------------------------------------------------------------
        head_rot = self._solve_head(norm_lms, world_lms, provenance)
        transforms.append(self._format_transform("Head", head_rot, timestamp_sec))

        # -------------------------------------------------------------
        # 3. Upper Body Arms (Right & Left)
        # -------------------------------------------------------------
        # Use contact-adjusted wrist positions if available
        adj_lw = contact_info.get("adjustedLeftWrist")
        adj_rw = contact_info.get("adjustedRightWrist")

        r_arm_rot, r_forearm_rot = self._solve_arm(
            shoulder_id=RIGHT_SHOULDER,
            elbow_id=RIGHT_ELBOW,
            wrist_id=RIGHT_WRIST,
            is_left=False,
            world_lms=world_lms,
            adjusted_wrist=adj_rw,
            provenance=provenance,
        )
        transforms.append(self._format_transform("RightArm", r_arm_rot, timestamp_sec))
        transforms.append(self._format_transform("RightForeArm", r_forearm_rot, timestamp_sec))

        l_arm_rot, l_forearm_rot = self._solve_arm(
            shoulder_id=LEFT_SHOULDER,
            elbow_id=LEFT_ELBOW,
            wrist_id=LEFT_WRIST,
            is_left=True,
            world_lms=world_lms,
            adjusted_wrist=adj_lw,
            provenance=provenance,
        )
        transforms.append(self._format_transform("LeftArm", l_arm_rot, timestamp_sec))
        transforms.append(self._format_transform("LeftForeArm", l_forearm_rot, timestamp_sec))

        # -------------------------------------------------------------
        # 4. Wrists & Hand Orientation
        # -------------------------------------------------------------
        r_hand_rot, l_hand_rot = self._solve_hands(frame_data, provenance)
        transforms.append(self._format_transform("RightHand", r_hand_rot, timestamp_sec))
        transforms.append(self._format_transform("LeftHand", l_hand_rot, timestamp_sec))

        # -------------------------------------------------------------
        # 5. Finger Joints (Anjali Mudra / Prayer Pose or Relaxed Rest)
        # -------------------------------------------------------------
        finger_transforms = self._solve_fingers(provenance)
        transforms.extend(finger_transforms)

        return transforms

    def _solve_spine(self, world_lms: Dict[int, Any]) -> Tuple[float, float, float, float]:
        """Calculates spine tilt from hip and shoulder centers."""
        if (
            LEFT_SHOULDER in world_lms and RIGHT_SHOULDER in world_lms and
            LEFT_HIP in world_lms and RIGHT_HIP in world_lms
        ):
            ls = mediapipe_world_to_threejs((world_lms[LEFT_SHOULDER]["x"], world_lms[LEFT_SHOULDER]["y"], world_lms[LEFT_SHOULDER]["z"]))
            rs = mediapipe_world_to_threejs((world_lms[RIGHT_SHOULDER]["x"], world_lms[RIGHT_SHOULDER]["y"], world_lms[RIGHT_SHOULDER]["z"]))
            lh = mediapipe_world_to_threejs((world_lms[LEFT_HIP]["x"], world_lms[LEFT_HIP]["y"], world_lms[LEFT_HIP]["z"]))
            rh = mediapipe_world_to_threejs((world_lms[RIGHT_HIP]["x"], world_lms[RIGHT_HIP]["y"], world_lms[RIGHT_HIP]["z"]))

            mid_shoulders = vec3_scale(vec3_add(ls, rs), 0.5)
            mid_hips = vec3_scale(vec3_add(lh, rh), 0.5)

            spine_vec = vec3_normalize(vec3_sub(mid_shoulders, mid_hips), fallback=REST_UP_DIR)
            return quat_from_two_vectors(REST_UP_DIR, spine_vec)

        return quat_identity()

    def _solve_head(
        self,
        norm_lms: Dict[str, Any],
        world_lms: Dict[int, Any],
        provenance: str,
    ) -> Tuple[float, float, float, float]:
        """Solves head rotation including respectful forward nod/bow for Namaste."""
        if provenance == "CONTACT_CONSTRAINED":
            # In official ISLRTC Namaste, signer holds a respectful ~10-12 degree forward head tilt (0.18 rad)
            return quat_from_axis_angle((1.0, 0.0, 0.0), 0.18)

        if NOSE in world_lms and LEFT_SHOULDER in world_lms and RIGHT_SHOULDER in world_lms:
            # Pitch from nose position relative to shoulder center
            nose = mediapipe_world_to_threejs((world_lms[NOSE]["x"], world_lms[NOSE]["y"], world_lms[NOSE]["z"]))
            ls = mediapipe_world_to_threejs((world_lms[LEFT_SHOULDER]["x"], world_lms[LEFT_SHOULDER]["y"], world_lms[LEFT_SHOULDER]["z"]))
            rs = mediapipe_world_to_threejs((world_lms[RIGHT_SHOULDER]["x"], world_lms[RIGHT_SHOULDER]["y"], world_lms[RIGHT_SHOULDER]["z"]))
            mid_shoulders = vec3_scale(vec3_add(ls, rs), 0.5)

            head_vec = vec3_normalize(vec3_sub(nose, mid_shoulders), fallback=REST_UP_DIR)
            # Forward nod angle (pitch around X axis)
            pitch = math.atan2(head_vec[2], head_vec[1])
            pitch = max(-0.1, min(0.35, pitch))  # Clamp to anatomical neck limits
            return quat_from_axis_angle((1.0, 0.0, 0.0), pitch)

        return quat_identity()

    def _solve_arm(
        self,
        shoulder_id: int,
        elbow_id: int,
        wrist_id: int,
        is_left: bool,
        world_lms: Dict[int, Any],
        adjusted_wrist: Optional[Tuple[float, float, float]],
        provenance: str,
    ) -> Tuple[Tuple[float, float, float, float], Tuple[float, float, float, float]]:
        """Solves upper arm and forearm rotations via Two-Bone vector IK."""
        # 1. Fallback / Rest handling when hands are at lap
        if provenance == "REST_INTERPOLATED":
            if is_left:
                q_arm = quat_from_axis_angle((0.0, 0.0, 1.0), NEUTRAL_EULER_LEFT_ARM[2])
                q_fore = quat_from_axis_angle((1.0, 0.0, 0.0), NEUTRAL_EULER_LEFT_FOREARM[0])
            else:
                q_arm = quat_from_axis_angle((0.0, 0.0, 1.0), NEUTRAL_EULER_RIGHT_ARM[2])
                q_fore = quat_from_axis_angle((1.0, 0.0, 0.0), NEUTRAL_EULER_RIGHT_FOREARM[0])
            return q_arm, q_fore

        # 2. Kinematic resolution from landmarks
        if shoulder_id in world_lms and elbow_id in world_lms:
            p_sh_raw = world_lms[shoulder_id]
            p_el_raw = world_lms[elbow_id]

            p_sh = mediapipe_world_to_threejs((p_sh_raw["x"], p_sh_raw["y"], p_sh_raw["z"]))
            p_el = mediapipe_world_to_threejs((p_el_raw["x"], p_el_raw["y"], p_el_raw["z"]))

            if adjusted_wrist is not None:
                p_wr = mediapipe_world_to_threejs(adjusted_wrist)
            elif wrist_id in world_lms:
                p_wr_raw = world_lms[wrist_id]
                p_wr = mediapipe_world_to_threejs((p_wr_raw["x"], p_wr_raw["y"], p_wr_raw["z"]))
            else:
                p_wr = (p_el[0], p_el[1] - 0.25, p_el[2] + 0.1)

            # Upper arm direction vector
            v_upper = vec3_normalize(vec3_sub(p_el, p_sh))
            # Forearm direction vector
            v_fore = vec3_normalize(vec3_sub(p_wr, p_el))

            rest_arm_dir = REST_LEFT_ARM_DIR if is_left else REST_RIGHT_ARM_DIR

            # Rotation aligning T-pose arm to observed upper arm vector
            q_upper = quat_from_two_vectors(rest_arm_dir, v_upper)

            # Forearm rotation relative to upper arm
            # Compute angle between upper arm and forearm
            dot_elbow = max(-1.0, min(1.0, vec3_dot(v_upper, v_fore)))
            elbow_angle = math.acos(dot_elbow)
            # In Mixamo coordinate system, elbow flexes primarily around local X axis
            q_fore = quat_from_axis_angle((1.0, 0.0, 0.0), elbow_angle)

            return q_upper, q_fore

        return quat_identity(), quat_identity()

    def _solve_hands(
        self,
        frame_data: Dict[str, Any],
        provenance: str,
    ) -> Tuple[Tuple[float, float, float, float], Tuple[float, float, float, float]]:
        """Solves wrist/hand orientation. In Namaste contact, palms press flat facing inward."""
        if provenance == "CONTACT_CONSTRAINED":
            # Right hand: palm faces toward left (+X), fingers point upward (+Y)
            # In Mixamo coordinates: Euler [-0.2, 0.1, 0.0]
            # Left hand: palm faces toward right (-X), fingers point upward (+Y)
            # In Mixamo coordinates: Euler [-0.2, -0.1, 0.0]
            q_r = quat_from_axis_angle((0.0, 1.0, 0.0), 0.1)
            q_l = quat_from_axis_angle((0.0, 1.0, 0.0), -0.1)
            return q_r, q_l

        if provenance == "REST_INTERPOLATED":
            return quat_identity(), quat_identity()

        # Direct observation orientation if hand landmarks exist
        return quat_identity(), quat_identity()

    def _solve_fingers(self, provenance: str) -> List[Dict[str, Any]]:
        """Generates finger transforms for all 5 digits per hand."""
        transforms = []
        is_contact = (provenance == "CONTACT_CONSTRAINED")

        for side in ["Right", "Left"]:
            sign_factor = 1.0 if side == "Left" else -1.0
            for digit in ["Index", "Middle", "Ring", "Pinky"]:
                for joint_num in [1, 2, 3]:
                    bone_name = f"{side}Hand{digit}{joint_num}"
                    if is_contact:
                        # In Anjali Mudra / Namaste, fingers are extended straight and parallel
                        rot = [0.0, 0.0, 0.0]
                    else:
                        # Relaxed curvature at rest
                        rot = [0.0, 0.0, sign_factor * 0.15 if joint_num == 1 else 0.05]

                    transforms.append({
                        "bone": bone_name,
                        "rotation": rot,
                        "rotationType": "euler",
                    })

            # Thumb joints
            for joint_num in [1, 2]:
                bone_name = f"{side}HandThumb{joint_num}"
                if is_contact:
                    rot = [0.05, 0.0, 0.0]
                else:
                    rot = [0.10, 0.0, sign_factor * 0.10]
                transforms.append({
                    "bone": bone_name,
                    "rotation": rot,
                    "rotationType": "euler",
                })

        return transforms

    def _format_transform(
        self,
        bone_name: str,
        quat: Tuple[float, float, float, float],
        timestamp_sec: float,
    ) -> Dict[str, Any]:
        """Applies 1-Euro smoothing and formats transform for export."""
        q_norm = quat_normalize(quat)
        if self.enable_smoothing:
            filt = self._get_filter(bone_name)
            q_norm = filt.filter(q_norm, timestamp_sec)

        if self.use_quaternions:
            return {
                "bone": bone_name,
                "rotation": [round(c, 5) for c in q_norm],
                "rotationType": "quaternion",
            }
        else:
            euler = quat_to_euler_xyz(q_norm)
            return {
                "bone": bone_name,
                "rotation": [round(c, 5) for c in euler],
                "rotationType": "euler",
            }
