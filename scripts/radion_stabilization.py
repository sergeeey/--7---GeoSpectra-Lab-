from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from cc_toy_lab.radion.dashboard import create_radion_dashboard
from cc_toy_lab.radion.dynamics import integrate_radion_trajectory, run_multitrajectory
from cc_toy_lab.radion.mfg import simulate_mfg
from cc_toy_lab.radion.phase_transition import ALPHA_C, alpha_grid_invariance, scan_alpha_transition
from cc_toy_lab.radion.potentials import (
    DEFAULT_RADION_PARAMS,
    analytic_radius_b,
    curvature,
    find_minimum,
    potential_a,
    potential_b,
    potential_c,
    potential_d,
)
from cc_toy_lab.runs import ensure_report_tree, make_run_dir, write_json, write_summary


def run(args: argparse.Namespace) -> dict[str, float | str]:
    ensure_report_tree()
    params = DEFAULT_RADION_PARAMS
    r0 = analytic_radius_b(params)
    minimum_b = find_minimum(potential_b, params)
    minimum_c = find_minimum(potential_c, params)
    minimum_d = find_minimum(potential_d, params)

    stable_trajectories = run_multitrajectory(
        potential_b,
        initial_radii=[0.5, 0.8, 1.5, 2.5, 3.5],
        initial_momentum=0.0,
        params=params,
        t_final=args.t_final,
        dt=args.dt,
    )
    unstable_trajectories = [
        integrate_radion_trajectory(
            potential_a,
            initial_radius=radius,
            initial_momentum=0.0,
            params=params,
            t_final=min(args.t_final, 8.0),
            dt=max(args.dt, 0.01),
        )
        for radius in [0.5, 0.8, 1.5, 2.5, 3.5]
    ]
    mfg_result = simulate_mfg(
        target_radius=r0,
        n_agents=args.n_agents,
        alpha=2.0,
        diffusion=0.0005,
        t_final=args.t_final,
        dt=args.dt,
        seed=args.seed,
    )
    phase_scan = scan_alpha_transition(np.linspace(1.0, 1.8, 321), params=params)
    invariance = alpha_grid_invariance(params=params)

    final_radii = np.array([trajectory.radius[-1] for trajectory in stable_trajectories])
    max_relative_error = float(np.max(np.abs(final_radii - r0) / r0))
    mfg_target = 1.0 / r0
    mfg_relative_error = float(abs(mfg_result.x_bar[-1] - mfg_target) / mfg_target)
    alpha_errors = {resolution: abs(estimate - ALPHA_C) for resolution, estimate in invariance.items()}

    assert abs(minimum_b.radius - 1.1892) < 5e-4, "Potential B minimum does not match R0"
    assert curvature(potential_b, minimum_b.radius, params) > 0.0, "Potential B is not stable"
    assert max_relative_error < 5e-4, "Stable trajectories did not converge tightly enough"
    assert mfg_relative_error < 0.0135, "MFG self-consistency failed"
    assert max(alpha_errors.values()) < 0.01, "alpha grid invariance failed"

    run_dir = make_run_dir("radion_stabilization")
    dashboard_path = Path("reports") / "FIGURES" / "radion_stabilization_dashboard.png"
    create_radion_dashboard(
        stable_trajectories=stable_trajectories,
        unstable_trajectories=unstable_trajectories,
        mfg_result=mfg_result,
        phase_scan=phase_scan,
        output_path=dashboard_path,
        params=params,
    )
    run_figure = run_dir / "figures" / "radion_stabilization_dashboard.png"
    create_radion_dashboard(
        stable_trajectories=stable_trajectories,
        unstable_trajectories=unstable_trajectories,
        mfg_result=mfg_result,
        phase_scan=phase_scan,
        output_path=run_figure,
        params=params,
    )

    config = {
        "a": params.a,
        "b": params.b,
        "c": params.c,
        "gamma": params.gamma,
        "n_agents": args.n_agents,
        "t_final": args.t_final,
        "dt": args.dt,
        "seed": args.seed,
        "alpha_c": ALPHA_C,
    }
    metrics = {
        "R0_B_analytic": r0,
        "R0_B_numeric": minimum_b.radius,
        "R0_C_numeric": minimum_c.radius,
        "R0_D_numeric": minimum_d.radius,
        "curvature_B": minimum_b.curvature,
        "curvature_C": minimum_c.curvature,
        "curvature_D": minimum_d.curvature,
        "max_multitrajectory_relative_error": max_relative_error,
        "mfg_relative_error": mfg_relative_error,
        "estimated_alpha_c": phase_scan.estimated_alpha_c,
        "alpha_grid_invariance": invariance,
        "dashboard": str(dashboard_path),
    }
    write_json(run_dir / "config.json", config)
    write_json(run_dir / "metrics.json", metrics)
    np.savez(
        run_dir / "data.npz",
        stable_time=stable_trajectories[0].time,
        stable_radii=np.vstack([trajectory.radius for trajectory in stable_trajectories]),
        mfg_time=mfg_result.time,
        mfg_x_bar=mfg_result.x_bar,
        phase_alpha=phase_scan.alpha_values,
        phase_radius=phase_scan.radius,
        phase_order=phase_scan.order_parameter,
    )
    report_lines = [
        "What was checked: four toy radion potentials, damped ODE convergence, MFG self-consistency, and a threshold phase scan.",
        f"Potential B analytic R0: {r0:.6f}; numeric R0: {minimum_b.radius:.6f}.",
        f"Trajectory max relative error: {max_relative_error:.6g}.",
        f"MFG relative error against 1/R0: {mfg_relative_error:.6g}.",
        f"Estimated alpha_c: {phase_scan.estimated_alpha_c:.6f}.",
        "What this proves: the specified toy equations have a stable attractor under the chosen parameters.",
        "What this does not prove: physical compactification, a full quantum effective energy, or the covariant compactification theory.",
        f"Run directory: {run_dir}",
    ]
    write_summary(Path("reports") / "RADION_REPORT.md", "Radion Report", report_lines)
    write_summary(run_dir / "summary.md", "Radion Stabilization Run", report_lines)
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-agents", type=int, default=300)
    parser.add_argument("--t-final", type=float, default=40.0)
    parser.add_argument("--dt", type=float, default=0.005)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


if __name__ == "__main__":
    metrics = run(parse_args())
    print("Radion stabilization complete")
    print(f"dashboard={metrics['dashboard']}")
    print(f"R0_B={metrics['R0_B_numeric']:.6f}")
    print(f"mfg_relative_error={metrics['mfg_relative_error']:.6g}")
