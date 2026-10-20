"""SignBridge M3.9 — 1-Euro Temporal Smoothing & Jitter Evaluation

Implements the adaptive 1-Euro Filter (Casiez et al., 2012) for 3D positional
trajectories and quaternions. Provides quantitative roughness and jitter metrics.
"""

import math
from typing import Dict, List, Optional, Tuple

from coordinate_utils import (
    quat_identity,
    quat_normalize,
    quat_slerp,
    vec3_dist,
    vec3_length,
    vec3_sub,
)


class LowPassFilterVec3:
    """Standard low-pass filter for 3D vector coordinates."""

    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha
        self.y: Optional[Tuple[float, float, float]] = None

    def filter(self, val: Tuple[float, float, float], alpha: Optional[float] = None) -> Tuple[float, float, float]:
        a = self.alpha if alpha is None else alpha
        if self.y is None:
            self.y = val
        else:
            self.y = (
                a * val[0] + (1.0 - a) * self.y[0],
                a * val[1] + (1.0 - a) * self.y[1],
                a * val[2] + (1.0 - a) * self.y[2],
            )
        return self.y


class OneEuroFilterVec3:
    """Adaptive 1-Euro filter for 3D vector coordinates.
    Eliminates high-frequency noise during holds (low velocity) while
    minimizing phase lag during rapid stroke movements (high velocity).
    """

    def __init__(self, min_cutoff: float = 1.0, beta: float = 0.007, d_cutoff: float = 1.0):
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)

        self.x_filt = LowPassFilterVec3()
        self.dx_filt = LowPassFilterVec3()
        self.last_time: Optional[float] = None

    def _alpha(self, rate: float, cutoff: float) -> float:
        tau = 1.0 / (2.0 * math.pi * cutoff)
        te = 1.0 / rate if rate > 0 else 0.04
        return 1.0 / (1.0 + tau / te)

    def filter(self, x: Tuple[float, float, float], timestamp: float) -> Tuple[float, float, float]:
        if self.last_time is None:
            self.last_time = timestamp
            return self.x_filt.filter(x, 1.0)

        dt = timestamp - self.last_time
        self.last_time = timestamp

        # Guard against duplicate or negative timestamps
        if dt <= 1e-5:
            dt = 1e-4
        rate = 1.0 / dt

        # Estimate derivative (velocity)
        prev_x = self.x_filt.y or x
        dx = (
            (x[0] - prev_x[0]) * rate,
            (x[1] - prev_x[1]) * rate,
            (x[2] - prev_x[2]) * rate,
        )
        edx = self.dx_filt.filter(dx, self._alpha(rate, self.d_cutoff))

        # Dynamic cutoff
        speed = vec3_length(edx)
        cutoff = self.min_cutoff + self.beta * speed
        return self.x_filt.filter(x, self._alpha(rate, cutoff))


class OneEuroFilterQuat:
    """Adaptive 1-Euro filter for 4D quaternions using SLERP."""

    def __init__(self, min_cutoff: float = 1.2, beta: float = 0.005):
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)

        self.prev_q: Optional[Tuple[float, float, float, float]] = None
        self.last_time: Optional[float] = None

    def filter(self, q: Tuple[float, float, float, float], timestamp: float) -> Tuple[float, float, float, float]:
        target = quat_normalize(q)
        if self.prev_q is None:
            self.prev_q = target
            self.last_time = timestamp
            return target

        dt = timestamp - self.last_time
        self.last_time = timestamp

        if dt <= 1e-5:
            dt = 1e-4
        rate = 1.0 / dt

        # Angular speed estimate from dot product
        dot = abs(
            self.prev_q[0]*target[0] +
            self.prev_q[1]*target[1] +
            self.prev_q[2]*target[2] +
            self.prev_q[3]*target[3]
        )
        dot = max(-1.0, min(1.0, dot))
        angle = 2.0 * math.acos(dot)
        angular_speed = angle * rate

        cutoff = self.min_cutoff + self.beta * angular_speed
        tau = 1.0 / (2.0 * math.pi * cutoff)
        te = dt
        alpha = 1.0 / (1.0 + tau / te)
        alpha = max(0.01, min(1.0, alpha))

        filtered = quat_slerp(self.prev_q, target, alpha)
        self.prev_q = filtered
        return filtered


def calculate_trajectory_jitter(points: List[Tuple[float, float, float]]) -> float:
    """Calculates the second-order acceleration roughness metric (mean acceleration magnitude).
    Lower value indicates smoother, less jittery movement.
    """
    if len(points) < 3:
        return 0.0

    acc_sum = 0.0
    for i in range(1, len(points) - 1):
        p_prev = points[i - 1]
        p_curr = points[i]
        p_next = points[i + 1]

        # Second derivative: (p_next - 2*p_curr + p_prev)
        a_x = p_next[0] - 2.0 * p_curr[0] + p_prev[0]
        a_y = p_next[1] - 2.0 * p_curr[1] + p_prev[1]
        a_z = p_next[2] - 2.0 * p_curr[2] + p_prev[2]

        acc_sum += math.sqrt(a_x * a_x + a_y * a_y + a_z * a_z)

    return acc_sum / (len(points) - 2)
