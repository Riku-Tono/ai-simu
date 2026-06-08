# metrics.py
# Calculation logic for drift / friction / intervention.
# Currently a pass-through implementation that returns scalar values as-is.
#
# Future extension:
#   When u_fast / u_slow are changed to 2D vectors of [emotion, desire],
#   only the internals of compute_metrics() need to be replaced with vector
#   calculations — the overall structure stays the same.

from __future__ import annotations
import math
from typing import Union

# Type aliases: currently float, future list[float, float]
Scalar = float
Vector2 = list[float]
UhoVector = Union[Scalar, Vector2]


def _norm(v: UhoVector) -> float:
    """Return the norm of a scalar or 2D vector."""
    if isinstance(v, (int, float)):
        return float(v)
    return math.sqrt(sum(x ** 2 for x in v))


def _diff(a: UhoVector, b: UhoVector) -> UhoVector:
    """Return a - b as a vector or scalar."""
    if isinstance(a, (int, float)):
        return float(a) - float(b)
    return [x - y for x, y in zip(a, b)]


def compute_metrics(
    u_fast: UhoVector,
    u_slow: UhoVector,
    prev_u_slow: UhoVector | None = None,
) -> dict:
    """
    Compute and return drift / friction / intervention_flag.

    Parameters
    ----------
    u_fast      : Instantaneous momentum (scalar or [emotion, desire])
    u_slow      : Slowly-changing judgment axis (scalar or [emotion, desire])
    prev_u_slow : Previous u_slow value (used to compute drift delta)

    Returns
    -------
    dict with keys: drift, friction, intervention_flag
    """
    fast_norm = _norm(u_fast)
    slow_norm = _norm(u_slow)

    # drift: how far u_slow has deviated from its reference point
    # Future: compute via angular distance or Euclidean distance between vectors
    if prev_u_slow is not None:
        delta = _diff(u_slow, prev_u_slow)
        drift = _norm(delta)
    else:
        drift = 0.0

    # friction: magnitude of divergence between u_fast and u_slow
    # Future: account for direction via cosine distance or dot product
    friction = abs(fast_norm - slow_norm)

    # intervention_flag: simple threshold rule
    # Future: replaceable with a state machine or reinforcement learning policy
    intervention_flag = fast_norm > 0.35 or friction > 0.30

    return {
        "drift": round(drift, 4),
        "friction": round(friction, 4),
        "intervention_flag": intervention_flag,
    }
