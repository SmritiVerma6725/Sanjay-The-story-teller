"""SignBridge M3.9 — Bilateral Hand Contact Constraints & Occlusion Recovery

Detects and resolves bilateral hand contact during two-handed symmetrical signs
(specifically Anjali Mudra / Namaste prayer pose). Enforces strict correction limits,
records per-frame tracking provenance, and computes comparative before/after metrics.
"""

import math
from typing import Any, Dict, List, Optional, Tuple

from coordinate_utils import (
    LEFT_ELBOW,
    LEFT_SHOULDER,
    LEFT_WRIST,
    RIGHT_ELBOW,
    RIGHT_SHOULDER,
    RIGHT_WRIST,
    vec3,
    vec3_dist,
    vec3_length,
    vec3_lerp,
    vec3_sub,
)


class ContactConstraintSolver:
    """Solves bilateral contact alignment for Namaste prayer pose with strict safety clamps."""

    def __init__(
        self,
        contact_dist_threshold: float = 0.16,  # Meters between wrists to consider contact plausible
        target_wrist_separation: float = 0.07,  # Anatomical separation between wrist carpal centers in prayer pose
        max_correction_clamp: float = 0.035,   # Maximum allowed positional adjustment in meters
    ):
        self.contact_dist_threshold = contact_dist_threshold
        self.target_wrist_separation = target_wrist_separation
        self.max_correction_clamp = max_correction_clamp

    def process_sequence(self, frames: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Processes an entire sequence of frames, applying bilateral contact constraints
        where appropriate, tagging provenance, and generating quantitative metrics.
        """
        raw_wrist_distances = []
        constrained_wrist_distances = []
        provenance_tags = []
        low_confidence_frames = []

        processed_frames = []

        # First pass: analyze frames and identify candidate contact window
        # In our inspection, peak contact occurs when wrists are at sternum height
        for idx, fr in enumerate(frames):
            timestamp_ms = fr.get("timestampMs", idx * 40.0)
            pose_lms = {lm["name"]: lm for lm in fr.get("poseLandmarks", [])}
            world_lms = {lm["id"]: lm for lm in fr.get("poseWorldLandmarks", [])}

            has_lh = fr.get("leftHandDetected", False)
            has_rh = fr.get("rightHandDetected", False)

            # Check wrist positions in world space (in meters)
            lw_world = None
            rw_world = None
            if LEFT_WRIST in world_lms and RIGHT_WRIST in world_lms:
                lw_raw = world_lms[LEFT_WRIST]
                rw_raw = world_lms[RIGHT_WRIST]
                lw_world = vec3(lw_raw["x"], lw_raw["y"], lw_raw["z"])
                rw_world = vec3(rw_raw["x"], rw_raw["y"], rw_raw["z"])

            # Check normalized positions
            lw_norm = pose_lms.get("left_wrist")
            rw_norm = pose_lms.get("right_wrist")

            is_rest_phase = False
            if lw_norm and rw_norm:
                # When wrists are down at the lap (normalized Y > 0.95), signer is in neutral rest
                if lw_norm["y"] > 0.95 and rw_norm["y"] > 0.95:
                    is_rest_phase = True

            raw_dist = 0.0
            if lw_world and rw_world:
                raw_dist = vec3_dist(lw_world, rw_world)
                raw_wrist_distances.append(raw_dist)
            else:
                raw_wrist_distances.append(0.0)

            # Determine provenance tag and contact application
            tag = "DIRECTLY_OBSERVED"
            adjusted_lw = lw_world
            adjusted_rw = rw_world
            correction_applied = 0.0

            if is_rest_phase:
                tag = "REST_INTERPOLATED"
            elif lw_world and rw_world:
                # Plausible contact condition:
                # 1. Both wrists are elevated to chest height (Y between -0.15 and -0.40m relative to hips)
                # 2. Both wrists are forward in front of torso (Z < -0.20m)
                # 3. Raw distance is within contact candidate threshold (<= contact_dist_threshold)
                is_elevated = (-0.45 <= lw_world[1] <= -0.15) and (-0.45 <= rw_world[1] <= -0.15)
                is_forward = (lw_world[2] < -0.20) and (rw_world[2] < -0.20)
                is_contact_proximity = raw_dist <= self.contact_dist_threshold

                if is_elevated and is_forward and is_contact_proximity:
                    tag = "CONTACT_CONSTRAINED"

                    # Contact target:
                    # Midpoint in sagittal Y and Z
                    mid_y = 0.5 * (lw_world[1] + rw_world[1])
                    mid_z = 0.5 * (lw_world[2] + rw_world[2])
                    # Torso centerline midpoint in X
                    mid_x = 0.5 * (lw_world[0] + rw_world[0])

                    # Target positions: Left wrist at mid_x + half_sep, Right wrist at mid_x - half_sep
                    half_sep = self.target_wrist_separation * 0.5
                    target_lw = vec3(mid_x + half_sep, mid_y, mid_z)
                    target_rw = vec3(mid_x - half_sep, mid_y, mid_z)

                    # Compute adjustment vectors with clamp
                    disp_l = vec3_sub(target_lw, lw_world)
                    disp_r = vec3_sub(target_rw, rw_world)

                    len_l = vec3_length(disp_l)
                    len_r = vec3_length(disp_r)

                    clamp_l = min(1.0, self.max_correction_clamp / len_l) if len_l > 1e-6 else 1.0
                    clamp_r = min(1.0, self.max_correction_clamp / len_r) if len_r > 1e-6 else 1.0

                    adjusted_lw = (
                        lw_world[0] + disp_l[0] * clamp_l,
                        lw_world[1] + disp_l[1] * clamp_l,
                        lw_world[2] + disp_l[2] * clamp_l,
                    )
                    adjusted_rw = (
                        rw_world[0] + disp_r[0] * clamp_r,
                        rw_world[1] + disp_r[1] * clamp_r,
                        rw_world[2] + disp_r[2] * clamp_r,
                    )

                    correction_applied = max(len_l * clamp_l, len_r * clamp_r)
                else:
                    if not (has_lh and has_rh):
                        # Missing one hand during active motion
                        tag = "LOW_CONFIDENCE"
                        low_confidence_frames.append(idx)
                    else:
                        tag = "DIRECTLY_OBSERVED"

            provenance_tags.append(tag)

            c_dist = vec3_dist(adjusted_lw, adjusted_rw) if (adjusted_lw and adjusted_rw) else raw_dist
            constrained_wrist_distances.append(c_dist)

            processed_frames.append({
                "frameIndex": idx,
                "timestampMs": timestamp_ms,
                "provenance": tag,
                "rawWristDistance": round(raw_dist, 5),
                "constrainedWristDistance": round(c_dist, 5),
                "correctionMagnitude": round(correction_applied, 5),
                "rawLeftWrist": lw_world,
                "rawRightWrist": rw_world,
                "adjustedLeftWrist": adjusted_lw,
                "adjustedRightWrist": adjusted_rw,
                "leftHandDetected": has_lh,
                "rightHandDetected": has_rh,
            })

        # Calculate summary metrics
        contact_frames = [f for f in processed_frames if f["provenance"] == "CONTACT_CONSTRAINED"]
        raw_contact_dists = [f["rawWristDistance"] for f in contact_frames]
        post_contact_dists = [f["constrainedWristDistance"] for f in contact_frames]

        metrics = {
            "totalFrames": len(frames),
            "contactConstrainedFramesCount": len(contact_frames),
            "restInterpolatedFramesCount": sum(1 for p in provenance_tags if p == "REST_INTERPOLATED"),
            "directlyObservedFramesCount": sum(1 for p in provenance_tags if p == "DIRECTLY_OBSERVED"),
            "lowConfidenceFramesCount": len(low_confidence_frames),
            "lowConfidenceFrameIndices": low_confidence_frames,
            "meanRawWristSeparationInContact": round(sum(raw_contact_dists) / len(raw_contact_dists), 4) if raw_contact_dists else 0.0,
            "meanConstrainedWristSeparationInContact": round(sum(post_contact_dists) / len(post_contact_dists), 4) if post_contact_dists else 0.0,
            "maxCorrectionAppliedMeters": round(max((f["correctionMagnitude"] for f in contact_frames), default=0.0), 4),
        }

        return {
            "frames": processed_frames,
            "metrics": metrics,
        }
