from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from cc_toy_lab.radion.potentials import DEFAULT_RADION_PARAMS, RadionParams


ALPHA_C = 1.345


@dataclass(frozen=True)
class PhaseScan:
    alpha_values: np.ndarray
    exists_minimum: np.ndarray
    radius: np.ndarray
    order_parameter: np.ndarray
    curvature: np.ndarray
    estimated_alpha_c: float


def phase_radius(alpha: float, params: RadionParams = DEFAULT_RADION_PARAMS, alpha_c: float = ALPHA_C) -> float:
    """First-order toy threshold: no finite minimum below alpha_c."""
    if alpha < alpha_c:
        return float("nan")
    effective_b = params.b * (1.0 + 0.35 * (alpha - alpha_c))
    return float((params.a / effective_b) ** 0.25)


def phase_curvature(alpha: float, params: RadionParams = DEFAULT_RADION_PARAMS, alpha_c: float = ALPHA_C) -> float:
    radius = phase_radius(alpha, params=params, alpha_c=alpha_c)
    if np.isnan(radius):
        return float("nan")
    effective_b = params.b * (1.0 + 0.35 * (alpha - alpha_c))
    return float(6.0 * params.a / radius**4 + 2.0 * effective_b)


def scan_alpha_transition(
    alpha_values: np.ndarray,
    params: RadionParams = DEFAULT_RADION_PARAMS,
    alpha_c: float = ALPHA_C,
) -> PhaseScan:
    alpha_values = np.asarray(alpha_values, dtype=float)
    radius = np.array([phase_radius(float(alpha), params, alpha_c) for alpha in alpha_values])
    exists = np.isfinite(radius)
    order_parameter = np.where(exists, 1.0 / radius, 0.0)
    curv = np.array([phase_curvature(float(alpha), params, alpha_c) for alpha in alpha_values])
    estimated = float(alpha_values[np.argmax(exists)]) if np.any(exists) else float("nan")
    return PhaseScan(
        alpha_values=alpha_values,
        exists_minimum=exists,
        radius=radius,
        order_parameter=order_parameter,
        curvature=curv,
        estimated_alpha_c=estimated,
    )


def alpha_grid_invariance(
    resolutions: list[int] = [41, 81, 161],
    span: tuple[float, float] = (1.25, 1.45),
    params: RadionParams = DEFAULT_RADION_PARAMS,
) -> dict[int, float]:
    estimates: dict[int, float] = {}
    for resolution in resolutions:
        scan = scan_alpha_transition(np.linspace(span[0], span[1], resolution), params=params)
        estimates[resolution] = scan.estimated_alpha_c
    return estimates
