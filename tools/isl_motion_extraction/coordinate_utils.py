"""SignBridge M3.9 — Coordinate Utilities & Quaternion Kinematics

Provides 3D vector math, coordinate frame transformations between MediaPipe
and Three.js/Mixamo spaces, robust vector-to-quaternion solvers, and quaternion math.
"""

import math
from typing import List, Tuple, Union

# MediaPipe Pose joint index constants
NOSE = 0
LEFT_EYE_INNER = 1
LEFT_EYE = 2
LEFT_EYE_OUTER = 3
RIGHT_EYE_INNER = 4
RIGHT_EYE = 5
RIGHT_EYE_OUTER = 6
LEFT_EAR = 7
RIGHT_EAR = 8
MOUTH_LEFT = 9
MOUTH_RIGHT = 10
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_PINKY = 17
RIGHT_PINKY = 18
LEFT_INDEX = 19
RIGHT_INDEX = 20
LEFT_THUMB = 21
RIGHT_THUMB = 22
LEFT_HIP = 23
RIGHT_HIP = 24


def vec3(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """Creates a 3D float tuple."""
    return (float(x), float(y), float(z))


def vec3_add(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vec3_sub(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vec3_scale(v: Tuple[float, float, float], s: float) -> Tuple[float, float, float]:
    return (v[0] * s, v[1] * s, v[2] * s)


def vec3_dot(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vec3_cross(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def vec3_length_sq(v: Tuple[float, float, float]) -> float:
    return v[0] * v[0] + v[1] * v[1] + v[2] * v[2]


def vec3_length(v: Tuple[float, float, float]) -> float:
    return math.sqrt(vec3_length_sq(v))


def vec3_dist(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    return vec3_length(vec3_sub(a, b))


def vec3_normalize(v: Tuple[float, float, float], fallback: Tuple[float, float, float] = (0.0, 1.0, 0.0)) -> Tuple[float, float, float]:
    l = vec3_length(v)
    if l < 1e-8 or not math.isfinite(l):
        return fallback
    return (v[0] / l, v[1] / l, v[2] / l)


def vec3_lerp(a: Tuple[float, float, float], b: Tuple[float, float, float], t: float) -> Tuple[float, float, float]:
    return (
        a[0] + t * (b[0] - a[0]),
        a[1] + t * (b[1] - a[1]),
        a[2] + t * (b[2] - a[2]),
    )


# =========================================================================
# Quaternion Mathematics [x, y, z, w]
# =========================================================================

def quat_identity() -> Tuple[float, float, float, float]:
    return (0.0, 0.0, 0.0, 1.0)


def quat_length(q: Tuple[float, float, float, float]) -> float:
    return math.sqrt(q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3])


def quat_normalize(q: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    l = quat_length(q)
    if l < 1e-8 or not math.isfinite(l):
        return quat_identity()
    return (q[0] / l, q[1] / l, q[2] / l, q[3] / l)


def quat_multiply(p: Tuple[float, float, float, float], q: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    """Multiplies two quaternions p * q (representing rotation q followed by p)."""
    px, py, pz, pw = p
    qx, qy, qz, qw = q
    return (
        pw * qx + px * qw + py * qz - pz * qy,
        pw * qy - px * qz + py * qw + pz * qx,
        pw * qz + px * qy - py * qx + pz * qw,
        pw * qw - px * qx - py * qy - pz * qz,
    )


def quat_conjugate(q: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
    return (-q[0], -q[1], -q[2], q[3])


def quat_rotate_vec3(q: Tuple[float, float, float, float], v: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """Rotates a 3D vector v by unit quaternion q."""
    vq = (v[0], v[1], v[2], 0.0)
    res = quat_multiply(quat_multiply(q, vq), quat_conjugate(q))
    return (res[0], res[1], res[2])


def quat_from_axis_angle(axis: Tuple[float, float, float], angle_rad: float) -> Tuple[float, float, float, float]:
    """Constructs a unit quaternion from an axis and angle in radians."""
    norm_axis = vec3_normalize(axis)
    half = angle_rad * 0.5
    s = math.sin(half)
    return quat_normalize((norm_axis[0] * s, norm_axis[1] * s, norm_axis[2] * s, math.cos(half)))


def quat_from_two_vectors(v_from: Tuple[float, float, float], v_to: Tuple[float, float, float]) -> Tuple[float, float, float, float]:
    """Calculates the minimal rotation quaternion that aligns unit vector v_from to v_to.
    Handles parallel and anti-parallel singular edge cases robustly.
    """
    v1 = vec3_normalize(v_from)
    v2 = vec3_normalize(v_to)
    dot = vec3_dot(v1, v2)

    # Identical vectors (no rotation)
    if dot >= 0.999999:
        return quat_identity()

    # Opposite vectors (180 degree flip around any orthogonal axis)
    if dot <= -0.999999:
        # Find orthogonal axis
        ortho = vec3_cross((1.0, 0.0, 0.0), v1)
        if vec3_length_sq(ortho) < 0.01:
            ortho = vec3_cross((0.0, 1.0, 0.0), v1)
        ortho = vec3_normalize(ortho)
        return quat_from_axis_angle(ortho, math.pi)

    # General case: w = 1 + dot, xyz = cross product
    axis = vec3_cross(v1, v2)
    w = 1.0 + dot
    return quat_normalize((axis[0], axis[1], axis[2], w))


def quat_slerp(q1: Tuple[float, float, float, float], q2: Tuple[float, float, float, float], t: float) -> Tuple[float, float, float, float]:
    """Spherical linear interpolation between two unit quaternions."""
    ax, ay, az, aw = q1
    bx, by, bz, bw = q2

    dot = ax * bx + ay * by + az * bz + aw * bw
    if dot < 0.0:
        bx = -bx
        by = -by
        bz = -bz
        bw = -bw
        dot = -dot

    if dot > 0.9995:
        # Linear interpolation for nearly coincident rotations
        rx = ax + t * (bx - ax)
        ry = ay + t * (by - ay)
        rz = az + t * (bz - az)
        rw = aw + t * (bw - aw)
        return quat_normalize((rx, ry, rz, rw))

    dot = max(-1.0, min(1.0, dot))
    theta = math.acos(dot)
    sin_theta = math.sin(theta)
    if abs(sin_theta) < 1e-6:
        return quat_normalize(q1)

    s1 = math.sin((1.0 - t) * theta) / sin_theta
    s2 = math.sin(t * theta) / sin_theta

    return (
        s1 * ax + s2 * bx,
        s1 * ay + s2 * by,
        s1 * az + s2 * bz,
        s1 * aw + s2 * bw,
    )


def quat_to_euler_xyz(q: Tuple[float, float, float, float]) -> Tuple[float, float, float]:
    """Converts a unit quaternion [x, y, z, w] to intrinsic XYZ Euler angles in radians.
    Matches Three.js Euler('XYZ') conventions.
    """
    x, y, z, w = quat_normalize(q)

    # Matrix element m12 = 2 * (x * z + y * w)
    sin_y = 2.0 * (x * z + y * w)
    sin_y = max(-1.0, min(1.0, sin_y))

    if abs(sin_y) < 0.99999:
        rot_y = math.asin(sin_y)
        rot_x = math.atan2(-2.0 * (y * z - w * x), w * w - x * x - y * y + z * z)
        rot_z = math.atan2(-2.0 * (x * y - w * z), w * w + x * x - y * y - z * z)
    else:
        # Gimbal lock at north/south pole
        rot_y = math.copysign(math.pi * 0.5, sin_y)
        rot_x = math.atan2(2.0 * (x * y + w * z), w * w - x * x + y * y - z * z)
        rot_z = 0.0

    return (rot_x, rot_y, rot_z)


# =========================================================================
# Coordinate Frame Conversion (MediaPipe -> Three.js / Avatar Space)
# =========================================================================

def mediapipe_world_to_threejs(p: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """Converts a MediaPipe world landmark [x, y, z] (in meters, centered at hips)
    into standard Three.js right-handed coordinate frame:
    - MediaPipe: +X is Right, +Y is Down (or Up in world, check convention), +Z is Toward camera.
    In MediaPipe world landmarks:
      - X is positive towards user's right (our left if facing camera)
      - Y is negative upwards towards head, positive downwards towards feet
      - Z is depth (smaller/negative is closer to camera)
    Three.js space:
      - +X is Right
      - +Y is Up
      - +Z is Forward / Out of screen
    We map:
      x_3js = -p[0]  (flip X to avatar's anatomical perspective: avatar facing forward)
      y_3js = -p[1]  (flip Y so upward is positive)
      z_3js = -p[2]  (flip Z so forward reaching is positive)
    """
    return (-p[0], -p[1], -p[2])


def mediapipe_norm_to_threejs(p: Tuple[float, float, float], ref_center: Tuple[float, float, float] = (0.5, 0.5, 0.0)) -> Tuple[float, float, float]:
    """Converts normalized 2D/3D screen space landmark (0..1) into a centered Three.js space."""
    return (
        -(p[0] - ref_center[0]),
        -(p[1] - ref_center[1]),
        -(p[2] - ref_center[2]),
    )
