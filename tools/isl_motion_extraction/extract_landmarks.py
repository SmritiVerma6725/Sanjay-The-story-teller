"""SignBridge M3.8 — Offline MediaPipe Motion Capture & Landmark Extraction Pipeline

Processes local video files using MediaPipe Holistic Task to extract 3D pose,
hand, and facial landmarks without external APIs or cloud dependencies.

Outputs:
1. Complete diagnostic JSON with video metadata, frame timestamps,
   normalized coordinates, world coordinates, confidence/visibility values,
   and missing-landmark statistics.
2. Annotated visualization image showing tracked skeleton and hand joints.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    HolisticLandmarker,
    HolisticLandmarkerOptions,
    RunningMode,
)

# Standard MediaPipe Pose Landmarks indices
POSE_CONNECTIONS = [
    # Torso
    (11, 12), (11, 23), (12, 24), (23, 24),
    # Left arm
    (11, 13), (13, 15),
    # Right arm
    (12, 14), (14, 16),
    # Left hand key links
    (15, 17), (15, 19), (15, 21),
    # Right hand key links
    (16, 18), (16, 20), (16, 22),
    # Face orientation
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10),
]

# Standard MediaPipe Hand Landmarks connections (21 joints per hand)
HAND_CONNECTIONS = [
    # Wrist to MCP
    (0, 1), (0, 5), (0, 9), (0, 13), (0, 17),
    # Thumb
    (1, 2), (2, 3), (3, 4),
    # Index
    (5, 6), (6, 7), (7, 8),
    # Middle
    (9, 10), (10, 11), (11, 12),
    # Ring
    (13, 14), (14, 15), (15, 16),
    # Pinky
    (17, 18), (18, 19), (19, 20),
    # Palm arch
    (5, 9), (9, 13), (13, 17),
]

POSE_LANDMARK_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer",
    "right_eye_inner", "right_eye", "right_eye_outer", "left_ear", "right_ear",
    "mouth_left", "mouth_right",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_pinky", "right_pinky",
    "left_index", "right_index", "left_thumb", "right_thumb",
    "left_hip", "right_hip", "left_knee", "right_knee",
    "left_ankle", "right_ankle", "left_heel", "right_heel",
    "left_foot_index", "right_foot_index"
]


def extract_landmarks(
    video_path: str,
    output_json_path: str,
    vis_output_path: Optional[str] = None,
    model_path: Optional[str] = None,
    max_frames: Optional[int] = None,
    stride: int = 1,
) -> Dict[str, Any]:
    """Extracts holistic landmarks from a video file and produces diagnostic outputs."""
    v_path = Path(video_path).resolve()
    if not v_path.exists():
        raise FileNotFoundError(f"Video file not found: {v_path}")

    if model_path is None:
        model_path = str(Path(__file__).parent / "models" / "holistic_landmarker.task")
    m_path = Path(model_path).resolve()
    if not m_path.exists():
        raise FileNotFoundError(
            f"MediaPipe model asset not found: {m_path}. Run download_models.py first."
        )

    cap = cv2.VideoCapture(str(v_path))
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video file: {v_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS)) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
    fourcc_str = "".join([chr((fourcc_int >> (8 * i)) & 0xFF) for i in range(4)])

    video_metadata = {
        "sourceFile": str(v_path.name),
        "sourcePath": str(v_path),
        "fileSizeBytes": v_path.stat().st_size,
        "width": width,
        "height": height,
        "fps": fps,
        "totalFrames": total_frames,
        "durationSeconds": round(total_frames / fps, 3) if fps > 0 else 0,
        "fourcc": fourcc_str,
    }

    print(f"[SignBridge MoCap] Processing: {v_path.name}")
    print(f"  Resolution: {width}x{height} | FPS: {fps} | Frames: {total_frames}")
    print(f"  MediaPipe Model: {m_path.name}")

    options = HolisticLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(m_path)),
        running_mode=RunningMode.IMAGE,
        min_pose_detection_confidence=0.5,
        min_pose_landmarks_confidence=0.5,
        min_hand_landmarks_confidence=0.5,
        min_face_landmarks_confidence=0.5,
    )

    frame_records = []
    stats = {
        "processedFrames": 0,
        "poseDetectedCount": 0,
        "leftHandDetectedCount": 0,
        "rightHandDetectedCount": 0,
        "faceDetectedCount": 0,
        "bothHandsDetectedCount": 0,
        "handOcclusionDetectedCount": 0,  # One or both hands dropped during active pose
    }

    # Tracking visibility sums for key joints
    pose_visibility_sums = [0.0] * 33
    pose_visibility_counts = [0] * 33

    start_time = time.time()
    frame_idx = 0
    candidate_vis_frames = []

    with HolisticLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % stride != 0:
                frame_idx += 1
                continue

            if max_frames and len(frame_records) >= max_frames:
                break

            timestamp_ms = round((frame_idx / fps) * 1000, 2)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            result = landmarker.detect(mp_img)
            stats["processedFrames"] += 1

            has_pose = bool(result.pose_landmarks and len(result.pose_landmarks) > 0)
            has_lhand = bool(result.left_hand_landmarks and len(result.left_hand_landmarks) > 0)
            has_rhand = bool(result.right_hand_landmarks and len(result.right_hand_landmarks) > 0)
            has_face = bool(result.face_landmarks and len(result.face_landmarks) > 0)

            if has_pose:
                stats["poseDetectedCount"] += 1
            if has_lhand:
                stats["leftHandDetectedCount"] += 1
            if has_rhand:
                stats["rightHandDetectedCount"] += 1
            if has_face:
                stats["faceDetectedCount"] += 1
            if has_lhand and has_rhand:
                stats["bothHandsDetectedCount"] += 1
            elif (has_lhand and not has_rhand) or (has_rhand and not has_lhand):
                stats["handOcclusionDetectedCount"] += 1

            # Format pose landmarks
            pose_data = []
            pose_world_data = []
            if has_pose:
                for j_idx, lm in enumerate(result.pose_landmarks):
                    vis = float(getattr(lm, "visibility", 1.0) or 0.0)
                    pose_visibility_sums[j_idx] += vis
                    pose_visibility_counts[j_idx] += 1
                    pose_data.append({
                        "id": j_idx,
                        "name": POSE_LANDMARK_NAMES[j_idx] if j_idx < len(POSE_LANDMARK_NAMES) else f"joint_{j_idx}",
                        "x": round(float(lm.x), 5),
                        "y": round(float(lm.y), 5),
                        "z": round(float(lm.z), 5),
                        "visibility": round(vis, 4),
                    })

                if result.pose_world_landmarks:
                    for j_idx, wlm in enumerate(result.pose_world_landmarks):
                        pose_world_data.append({
                            "id": j_idx,
                            "x": round(float(wlm.x), 5),
                            "y": round(float(wlm.y), 5),
                            "z": round(float(wlm.z), 5),
                        })

            # Format hand landmarks
            left_hand_data = []
            if has_lhand:
                for j_idx, lm in enumerate(result.left_hand_landmarks):
                    left_hand_data.append({
                        "id": j_idx,
                        "x": round(float(lm.x), 5),
                        "y": round(float(lm.y), 5),
                        "z": round(float(lm.z), 5),
                    })

            right_hand_data = []
            if has_rhand:
                for j_idx, lm in enumerate(result.right_hand_landmarks):
                    right_hand_data.append({
                        "id": j_idx,
                        "x": round(float(lm.x), 5),
                        "y": round(float(lm.y), 5),
                        "z": round(float(lm.z), 5),
                    })

            # Face structural summary (478 landmarks total, capture key structural points)
            face_summary = None
            if has_face:
                face_summary = {
                    "totalLandmarks": len(result.face_landmarks),
                    "noseTip": {
                        "x": round(float(result.face_landmarks[1].x), 5),
                        "y": round(float(result.face_landmarks[1].y), 5),
                        "z": round(float(result.face_landmarks[1].z), 5),
                    },
                    "chin": {
                        "x": round(float(result.face_landmarks[152].x), 5),
                        "y": round(float(result.face_landmarks[152].y), 5),
                        "z": round(float(result.face_landmarks[152].z), 5),
                    },
                    "leftEye": {
                        "x": round(float(result.face_landmarks[33].x), 5),
                        "y": round(float(result.face_landmarks[33].y), 5),
                        "z": round(float(result.face_landmarks[33].z), 5),
                    },
                    "rightEye": {
                        "x": round(float(result.face_landmarks[263].x), 5),
                        "y": round(float(result.face_landmarks[263].y), 5),
                        "z": round(float(result.face_landmarks[263].z), 5),
                    },
                }

            record = {
                "frameIndex": frame_idx,
                "timestampMs": timestamp_ms,
                "poseDetected": has_pose,
                "leftHandDetected": has_lhand,
                "rightHandDetected": has_rhand,
                "faceDetected": has_face,
                "poseLandmarks": pose_data,
                "poseWorldLandmarks": pose_world_data,
                "leftHandLandmarks": left_hand_data,
                "rightHandLandmarks": right_hand_data,
                "faceSummary": face_summary,
            }
            frame_records.append(record)

            # Keep sample frames for visualization (e.g. 20%, 50%, 80% mark)
            if frame_idx in (10, 35, 60) or (frame_idx == 35):
                candidate_vis_frames.append((frame_idx, frame.copy(), record))

            frame_idx += 1

    cap.release()
    elapsed = time.time() - start_time
    proc_fps = stats["processedFrames"] / elapsed if elapsed > 0 else 0

    print(f"  Processed {stats['processedFrames']} frames in {elapsed:.2f}s ({proc_fps:.1f} FPS)")

    # Compute aggregate percentages
    n_proc = max(1, stats["processedFrames"])
    summary_stats = {
        "processedFrames": stats["processedFrames"],
        "poseDetectionRatePercent": round((stats["poseDetectedCount"] / n_proc) * 100, 1),
        "leftHandDetectionRatePercent": round((stats["leftHandDetectedCount"] / n_proc) * 100, 1),
        "rightHandDetectionRatePercent": round((stats["rightHandDetectedCount"] / n_proc) * 100, 1),
        "bothHandsDetectionRatePercent": round((stats["bothHandsDetectedCount"] / n_proc) * 100, 1),
        "faceDetectionRatePercent": round((stats["faceDetectedCount"] / n_proc) * 100, 1),
        "asymmetricOcclusionRatePercent": round((stats["handOcclusionDetectedCount"] / n_proc) * 100, 1),
    }

    # Per-joint visibility averages
    key_joint_visibilities = {}
    for j_idx in [11, 12, 13, 14, 15, 16, 19, 20]:
        count = pose_visibility_counts[j_idx]
        name = POSE_LANDMARK_NAMES[j_idx]
        avg_vis = (pose_visibility_sums[j_idx] / count) if count > 0 else 0.0
        key_joint_visibilities[name] = round(avg_vis, 4)
    summary_stats["keyJointVisibilities"] = key_joint_visibilities

    # Generate visualization if requested
    vis_file = None
    if vis_output_path and len(candidate_vis_frames) > 0:
        vis_out = Path(vis_output_path).resolve()
        vis_out.parent.mkdir(parents=True, exist_ok=True)
        # Select best frame (middle frame 35 if available, else first candidate)
        selected = candidate_vis_frames[1] if len(candidate_vis_frames) > 1 else candidate_vis_frames[0]
        s_idx, s_frame, s_record = selected
        annotated = draw_landmarks_on_frame(s_frame, s_record)
        cv2.imwrite(str(vis_out), annotated)
        vis_file = str(vis_out)
        print(f"  Visualization saved to: {vis_out}")

    diagnostic_payload = {
        "generator": "SignBridge ISL Motion Extraction Pipeline v1.0.0",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "videoMetadata": video_metadata,
        "summaryStatistics": summary_stats,
        "visualizationFile": vis_file,
        "retargetingFeasibility": evaluate_retargeting_feasibility(summary_stats),
        "frames": frame_records,
    }

    out_json = Path(output_json_path).resolve()
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(diagnostic_payload, f, indent=2)

    print(f"  Diagnostic JSON saved to: {out_json}")
    return diagnostic_payload


def draw_landmarks_on_frame(frame: np.ndarray, record: Dict[str, Any]) -> np.ndarray:
    """Draws skeleton and hand landmarks onto an image frame with high-contrast colors."""
    h, w, _ = frame.shape
    vis = frame.copy()

    # Draw title header banner
    cv2.rectangle(vis, (0, 0), (w, 60), (20, 20, 20), -1)
    status_text = (
        f"SignBridge MoCap Diagnostic — Frame {record['frameIndex']} ({record['timestampMs']}ms) | "
        f"Pose: {'OK' if record['poseDetected'] else 'LOST'} | "
        f"Hands: L={'OK' if record['leftHandDetected'] else 'LOST'}, R={'OK' if record['rightHandDetected'] else 'LOST'}"
    )
    cv2.putText(vis, status_text, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 200), 2)

    # Draw pose connections (cyan)
    pose_lms = record.get("poseLandmarks", [])
    if pose_lms:
        pt_map = {item["id"]: (int(item["x"] * w), int(item["y"] * h)) for item in pose_lms}
        for (i1, i2) in POSE_CONNECTIONS:
            if i1 in pt_map and i2 in pt_map:
                cv2.line(vis, pt_map[i1], pt_map[i2], (255, 200, 0), 2)
        for idx, pt in pt_map.items():
            # Highlight wrists and elbows
            if idx in (13, 14, 15, 16):
                cv2.circle(vis, pt, 6, (0, 0, 255), -1)
                cv2.circle(vis, pt, 8, (255, 255, 255), 1)
            else:
                cv2.circle(vis, pt, 4, (0, 255, 255), -1)

    # Draw left hand (green)
    l_hand = record.get("leftHandLandmarks", [])
    if l_hand:
        l_map = {item["id"]: (int(item["x"] * w), int(item["y"] * h)) for item in l_hand}
        for (i1, i2) in HAND_CONNECTIONS:
            if i1 in l_map and i2 in l_map:
                cv2.line(vis, l_map[i1], l_map[i2], (50, 255, 50), 2)
        for pt in l_map.values():
            cv2.circle(vis, pt, 3, (0, 255, 0), -1)

    # Draw right hand (magenta)
    r_hand = record.get("rightHandLandmarks", [])
    if r_hand:
        r_map = {item["id"]: (int(item["x"] * w), int(item["y"] * h)) for item in r_hand}
        for (i1, i2) in HAND_CONNECTIONS:
            if i1 in r_map and i2 in r_map:
                cv2.line(vis, r_map[i1], r_map[i2], (255, 50, 255), 2)
        for pt in r_map.values():
            cv2.circle(vis, pt, 3, (255, 0, 255), -1)

    return vis


def evaluate_retargeting_feasibility(stats: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates whether the extracted tracking quality is feasible for Y-Bot retargeting."""
    pose_ok = stats["poseDetectionRatePercent"] >= 80.0
    hands_ok = stats["bothHandsDetectionRatePercent"] >= 50.0
    occlusion_risk = stats["asymmetricOcclusionRatePercent"] > 20.0

    return {
        "poseTrackingFeasible": pose_ok,
        "handTrackingFeasible": hands_ok,
        "occlusionRiskHigh": occlusion_risk,
        "recommendation": (
            "Feasible for arm and torso inverse kinematics. "
            "Hand tracking requires temporal smoothing and bilateral contact heuristic "
            "when palms press together (Anjali Mudra) because MediaPipe experiences self-occlusion."
        ) if pose_ok else "Tracking insufficient for reliable retargeting.",
        "rigCompatibilityNotes": {
            "avatarRig": "Adobe Mixamo Y-Bot (ybot.glb)",
            "armArticulation": "Supported (RightArm, RightForeArm, LeftArm, LeftForeArm)",
            "fingerArticulation": "Supported on rig (4 phalanges per finger), but MediaPipe noisy under close contact",
            "facialNonManuals": "NOT SUPPORTED on standard Y-Bot (rig has zero facial blendshapes/bones)",
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="SignBridge Offline MediaPipe Motion Extraction Prototype"
    )
    parser.add_argument(
        "--video",
        type=str,
        default="tools/isl_motion_extraction/reference_videos/ISLRTC_Namaste_sample.mp4",
        help="Path to local video file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="tools/isl_motion_extraction/output/landmark_extraction_diagnostic.json",
        help="Output path for diagnostic JSON",
    )
    parser.add_argument(
        "--vis-output",
        type=str,
        default="tools/isl_motion_extraction/output/skeleton_visualization.png",
        help="Output path for annotated diagnostic visualization image",
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default="tools/isl_motion_extraction/models/holistic_landmarker.task",
        help="Path to MediaPipe Holistic Task model bundle",
    )
    parser.add_argument("--stride", type=int, default=1, help="Frame stride")
    parser.add_argument("--max-frames", type=int, default=None, help="Max frames to process")

    args = parser.parse_args()
    extract_landmarks(
        video_path=args.video,
        output_json_path=args.output,
        vis_output_path=args.vis_output,
        model_path=args.model_path,
        max_frames=args.max_frames,
        stride=args.stride,
    )


if __name__ == "__main__":
    main()
