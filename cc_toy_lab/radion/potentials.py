from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.optimize import minimize_scalar


@dataclass(frozen=True)
class RadionParams:
    a: float = 1.0
    b: float = 0.5
    c: float = 0.3
    gamma: float = 0.5
    m_eff: float = 1.0
    kk_terms: int = 24
    kk_mass0: float = 0.15
    kk_strength: float = 0.015
    kk_cutoff: float = 7.0


@dataclass(frozen=True)
class Minimum:
    radius: float
    value: float
    curvature: float


DEFAULT_RADION_PARAMS = RadionParams()

Potential = Callable[[float | np.ndarray, RadionParams], float | np.ndarray]


def potential_a(radius: float | np.ndarray, params: RadionParams = DEFAULT_RADION_PARAMS) -> float | np.ndarray:
    return params.a / np.asarray(radius) ** 2


def potential_b(radius: float | np.ndarray, params: RadionParams = DEFAULT_RADION_PARAMS) -> float | np.ndarray:
    r = np.asarray(radius)
    return params.a / r**2 + params.b * r**2


def potential_c(radius: float | np.ndarray, params: RadionParams = DEFAULT_RADION_PARAMS) -> float | np.ndarray:
    r = np.asarray(radius)
    return params.a / r**2 + params.b * r**2 + params.c / r**4


def kk_regularized_energy(radius: float | np.ndarray, params: RadionParams = DEFAULT_RADION_PARAMS) -> float | np.ndarray:
    """Toy-regularized KK tower contribution.

    This is not a complete quantum effective energy. The exponential cutoff is
    a numerical toy regularizer used only for reproducible diagnostics.
    """
    r = np.asarray(radius, dtype=float)
    total = np.zeros_like(r, dtype=float)
    for k in range(1, params.kk_terms + 1):
        weight = np.exp(-k / params.kk_cutoff)
        total = total + weight * np.sqrt((k / r) ** 2 + params.kk_mass0**2)
    return params.kk_strength * total


def potential_d(radius: float | np.ndarray, params: RadionParams = DEFAULT_RADION_PARAMS) -> float | np.ndarray:
    return potential_b(radius, params) + kk_regularized_energy(radius, params)


def analytic_radius_b(params: RadionParams = DEFAULT_RADION_PARAMS) -> float:
    return float((params.a / params.b) ** 0.25)


def derivative(potential: Potential, radius: float, params: RadionParams = DEFAULT_RADION_PARAMS) -> float:
    r = float(radius)
    if potential is potential_a:
        return float(-2.0 * params.a / r**3)
    if potential is potential_b:
        return float(-2.0 * params.a / r**3 + 2.0 * params.b * r)
    if potential is potential_c:
        return float(-2.0 * params.a / r**3 + 2.0 * params.b * r - 4.0 * params.c / r**5)
    step = max(1e-5, abs(r) * 1e-5)
    return float((potential(r + step, params) - potential(r - step, params)) / (2.0 * step))


def curvature(potential: Potential, radius: float, params: RadionParams = DEFAULT_RADION_PARAMS) -> float:
    r = float(radius)
    if potential is potential_a:
        return float(6.0 * params.a / r**4)
    if potential is potential_b:
        return float(6.0 * params.a / r**4 + 2.0 * params.b)
    if potential is potential_c:
        return float(6.0 * params.a / r**4 + 2.0 * params.b + 20.0 * params.c / r**6)
    step = max(1e-4, abs(r) * 1e-4)
    return float((potential(r + step, params) - 2.0 * potential(r, params) + potential(r - step, params)) / step**2)


def find_minimum(
    potential: Potential,
    params: RadionParams = DEFAULT_RADION_PARAMS,
    bracket: tuple[float, float] = (0.25, 4.5),
) -> Minimum:
    result = minimize_scalar(lambda x: float(potential(x, params)), bounds=bracket, method="bounded", options={"xatol": 1e-12})
    radius = float(result.x)
    return Minimum(radius=radius, value=float(result.fun), curvature=curvature(potential, radius, params))
