from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from cc_toy_lab.radion.potentials import DEFAULT_RADION_PARAMS, Potential, RadionParams, derivative


@dataclass(frozen=True)
class RadionTrajectory:
    time: np.ndarray
    radius: np.ndarray
    momentum: np.ndarray


def integrate_radion_trajectory(
    potential: Potential,
    initial_radius: float,
    initial_momentum: float = 0.0,
    params: RadionParams = DEFAULT_RADION_PARAMS,
    t_final: float = 40.0,
    dt: float = 0.005,
    rtol: float = 1e-9,
    atol: float = 1e-11,
) -> RadionTrajectory:
    if initial_radius <= 0:
        raise ValueError("initial_radius must be positive")
    if dt <= 0 or t_final <= 0:
        raise ValueError("dt and t_final must be positive")

    def rhs(_: float, state: np.ndarray) -> np.ndarray:
        radius = max(float(state[0]), 1e-6)
        momentum = float(state[1])
        return np.array([momentum, -params.gamma * momentum - derivative(potential, radius, params) / params.m_eff])

    steps = int(round(t_final / dt))
    time = np.linspace(0.0, t_final, steps + 1)
    solution = solve_ivp(
        rhs,
        (0.0, t_final),
        [initial_radius, initial_momentum],
        t_eval=time,
        rtol=rtol,
        atol=atol,
        max_step=dt,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return RadionTrajectory(time=solution.t, radius=solution.y[0], momentum=solution.y[1])


def run_multitrajectory(
    potential: Potential,
    initial_radii: list[float],
    initial_momentum: float = 0.0,
    params: RadionParams = DEFAULT_RADION_PARAMS,
    t_final: float = 40.0,
    dt: float = 0.005,
) -> list[RadionTrajectory]:
    return [
        integrate_radion_trajectory(
            potential=potential,
            initial_radius=radius,
            initial_momentum=initial_momentum,
            params=params,
            t_final=t_final,
            dt=dt,
        )
        for radius in initial_radii
    ]
