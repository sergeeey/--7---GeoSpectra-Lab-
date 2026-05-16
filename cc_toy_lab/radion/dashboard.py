from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.radion.dynamics import RadionTrajectory
from cc_toy_lab.radion.mfg import MFGResult
from cc_toy_lab.radion.phase_transition import PhaseScan
from cc_toy_lab.radion.potentials import (
    DEFAULT_RADION_PARAMS,
    RadionParams,
    curvature,
    find_minimum,
    potential_a,
    potential_b,
    potential_c,
    potential_d,
)


def create_radion_dashboard(
    stable_trajectories: list[RadionTrajectory],
    unstable_trajectories: list[RadionTrajectory],
    mfg_result: MFGResult,
    phase_scan: PhaseScan,
    output_path: Path,
    params: RadionParams = DEFAULT_RADION_PARAMS,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    radii = np.linspace(0.35, 4.0, 500)
    potentials = [
        ("A: a/R^2", potential_a, "tab:red"),
        ("B: a/R^2+bR^2", potential_b, "tab:cyan"),
        ("C: B+c/R^4", potential_c, "gold"),
        ("D: B+KK toy", potential_d, "mediumaquamarine"),
    ]
    fig, axes = plt.subplots(3, 2, figsize=(16, 14), constrained_layout=True)
    fig.suptitle("Radion stabilization toy dashboard", fontsize=16)

    ax = axes[0, 0]
    for label, fn, color in potentials:
        values = np.asarray(fn(radii, params), dtype=float)
        ax.plot(radii, np.clip(values, 0, 10), label=label, color=color)
        if fn is not potential_a:
            minimum = find_minimum(fn, params)
            ax.axvline(minimum.radius, color=color, linestyle=":", alpha=0.7)
    ax.set_xlabel("R")
    ax.set_ylabel("V_eff(R), clipped")
    ax.set_title("Effective potentials")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    labels: list[str] = []
    curvatures: list[float] = []
    for label, fn, _ in potentials[1:]:
        minimum = find_minimum(fn, params)
        labels.append(label.split(":")[0])
        curvatures.append(curvature(fn, minimum.radius, params))
    ax.bar(labels, curvatures, color=["tab:cyan", "gold", "mediumaquamarine"])
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_ylabel("d2V/dR2 at minimum")
    ax.set_title("Curvature / stability")

    ax = axes[1, 0]
    for trajectory in stable_trajectories:
        ax.plot(trajectory.time, trajectory.radius, linewidth=1.4)
    ax.axhline(find_minimum(potential_b, params).radius, color="white", linestyle="--", linewidth=1.2, label="R0 B")
    ax.set_xlabel("t")
    ax.set_ylabel("R(t)")
    ax.set_title("Stable trajectories for potential B")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    for trajectory in unstable_trajectories:
        ax.plot(trajectory.time, trajectory.radius, linewidth=1.4)
    ax.set_xlabel("t")
    ax.set_ylabel("R(t)")
    ax.set_title("Potential A: no stabilizing minimum")

    ax = axes[2, 0]
    if stable_trajectories:
        stable = stable_trajectories[0]
        ax.plot(stable.time, stable.radius, label="R(t)", color="tab:cyan")
    ax2 = ax.twinx()
    ax2.plot(mfg_result.time, mfg_result.x_bar, label="x_bar(t)", color="tab:orange", alpha=0.85)
    ax2.plot(mfg_result.time, mfg_result.target, label="1/R0", color="white", linestyle=":")
    ax.set_xlabel("t")
    ax.set_ylabel("R(t)")
    ax2.set_ylabel("mean mode state")
    ax.set_title("MFG self-consistency")
    ax.legend(loc="upper left", fontsize=8)
    ax2.legend(loc="upper right", fontsize=8)

    ax = axes[2, 1]
    ax.plot(phase_scan.alpha_values, phase_scan.radius, color="cornflowerblue", label="R0(alpha)")
    ax2 = ax.twinx()
    ax2.plot(phase_scan.alpha_values, phase_scan.order_parameter, color="orchid", linestyle="--", label="Phi=1/R0")
    ax.axvline(phase_scan.estimated_alpha_c, color="white", linestyle=":", label="alpha_c")
    ax.fill_between(
        phase_scan.alpha_values,
        0,
        np.nan_to_num(phase_scan.radius, nan=0.0),
        where=phase_scan.exists_minimum,
        color="cornflowerblue",
        alpha=0.12,
    )
    ax.set_xlabel("alpha")
    ax.set_ylabel("R0(alpha)")
    ax2.set_ylabel("order parameter")
    ax.set_title("Toy stabilization phase transition")
    ax.legend(loc="upper left", fontsize=8)
    ax2.legend(loc="upper right", fontsize=8)

    fig.savefig(output_path, dpi=160)
    plt.close(fig)
    return output_path
