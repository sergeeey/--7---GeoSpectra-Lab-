from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MFGResult:
    time: np.ndarray
    x_bar: np.ndarray
    target: np.ndarray
    final_agents: np.ndarray


def simulate_mfg(
    target_radius: float,
    n_agents: int = 300,
    alpha: float = 2.0,
    diffusion: float = 0.0005,
    t_final: float = 40.0,
    dt: float = 0.005,
    seed: int = 42,
    initial_mean: float = 0.4,
) -> MFGResult:
    """Euler-Maruyama MFG toy dynamics dx=-alpha(x-1/R)dt+sqrt(2D)dW."""
    if target_radius <= 0:
        raise ValueError("target_radius must be positive")
    if n_agents <= 0:
        raise ValueError("n_agents must be positive")
    rng = np.random.default_rng(seed)
    steps = int(round(t_final / dt))
    time = np.linspace(0.0, t_final, steps + 1)
    target_value = 1.0 / target_radius
    agents = initial_mean + 0.02 * rng.normal(size=n_agents)
    x_bar = np.empty(steps + 1)
    x_bar[0] = float(np.mean(agents))
    noise_scale = np.sqrt(2.0 * diffusion * dt)
    for step in range(1, steps + 1):
        agents += -alpha * (agents - target_value) * dt + noise_scale * rng.normal(size=n_agents)
        x_bar[step] = float(np.mean(agents))
    return MFGResult(time=time, x_bar=x_bar, target=np.full_like(time, target_value), final_agents=agents.copy())
