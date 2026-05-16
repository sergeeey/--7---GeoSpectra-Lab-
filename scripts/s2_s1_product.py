from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s2_s1_product import (  # noqa: E402
    S2S1Assessment,
    S2S1ProductConfig,
    run_s2_s1_product_benchmark,
    save_s2_s1_run_artifacts,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Toy S2 x S1 product benchmark CLI.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--quick", action="store_true", help="Configured quick S2 x S1 product benchmark.")
    mode.add_argument("--full", action="store_true", help="Configured larger S2 x S1 product benchmark.")
    parser.add_argument("--seed", type=int, default=12051, help="Base RNG seed for reproducible runs.")
    return parser.parse_args()


def config_from_args(args: argparse.Namespace) -> tuple[str, S2S1ProductConfig]:
    if os.environ.get("CC_TOY_LAB_S2_S1_CLI_TEST_PROFILE") == "tiny":
        return (
            "quick",
            S2S1ProductConfig(
                q_values=(0, 1, -1),
                cutoff=2,
                s1_sizes=(1, 8),
                boundary_twists=(0.0, 0.5),
                s1_modes=("clean", "geometric_weight"),
                disorder_values=(0.0, 8.0),
                perturbation_values=(0.0,),
                realizations=1,
                seed=args.seed,
                note=_note_with_cli_context("tiny test profile"),
            ),
        )
    if args.full:
        return (
            "full",
            S2S1ProductConfig(
                q_values=(0, 1, -1, 2, -2),
                cutoff=2,
                s1_sizes=(8, 16, 24),
                boundary_twists=(0.0, 0.25, 0.5),
                s1_modes=("clean", "gauge_phase", "geometric_weight"),
                disorder_values=(0.0, 1.0, 2.0, 4.0, 8.0),
                perturbation_values=(0.0, 1e-5),
                realizations=5,
                seed=args.seed,
                note=_note_with_cli_context("full profile uses cutoff=2 for runtime safety"),
            ),
        )
    return (
        "quick",
        S2S1ProductConfig(
            q_values=(0, 1, -1),
            cutoff=2,
            s1_sizes=(8, 16),
            boundary_twists=(0.0, 0.5),
            s1_modes=("clean", "gauge_phase", "geometric_weight"),
            disorder_values=(0.0, 2.0, 8.0),
            perturbation_values=(0.0, 1e-5),
            realizations=3,
            seed=args.seed,
            note=_note_with_cli_context("quick CLI profile"),
        ),
    )


def run(args: argparse.Namespace) -> tuple[Path, S2S1Assessment, dict]:
    mode, config = config_from_args(args)
    assessment = run_s2_s1_product_benchmark(config)
    run_dir = make_run_dir(mode)
    artifacts = save_s2_s1_run_artifacts(assessment, run_dir)
    print_summary(mode=mode, run_dir=run_dir, assessment=assessment)
    return run_dir, assessment, artifacts


def make_run_dir(mode: str) -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base_dir = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base_dir / f"{stamp}_s2_s1_product_{mode}"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def print_summary(mode: str, run_dir: Path, assessment: S2S1Assessment) -> None:
    print(f"run_path={run_dir}")
    print(f"classification={assessment.classification}")
    print(f"all_basic_gates_passed={assessment.all_basic_gates_passed}")
    print(f"q_control_passed={assessment.q_control_passed}")
    print(f"pbc_gate_passed={assessment.pbc_gate_passed}")
    print(f"apbc_gate_passed={assessment.apbc_gate_passed}")
    print(f"flux_response_observed={assessment.flux_response_observed}")
    print(f"s1_not_spectator={assessment.s1_not_spectator}")
    print(f"localization_gate_passed={assessment.localization_gate_passed}")
    print(f"threshold_stable={assessment.threshold_stable}")
    print(f"total_observations={assessment.total_observations}")
    print(f"s2_s1_product_{mode} complete")


def _note_with_cli_context(extra_note: str) -> str:
    return (
        "Toy S2 x S1 spectral-circle product. This module constructs the operator "
        "core only and does not claim continuum compactification or a full-product "
        f"chiral theorem. CLI context: {extra_note}."
    )


def main() -> int:
    args = parse_args()
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
