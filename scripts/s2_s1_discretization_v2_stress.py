from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s1_discretization_v2_stress import (  # noqa: E402
    build_stress_config,
    run_s1_discretization_v2_stress,
    save_s1_discretization_v2_stress_artifacts,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Toy S1 discretization localization gate v2 stress-test CLI.")
    parser.add_argument("--seed", type=int, default=12051, help="Base RNG seed for reproducible runs.")
    parser.add_argument(
        "--realizations",
        type=int,
        default=5,
        help="Override realizations for the full stress profile. Use 3 if runtime is too high.",
    )
    parser.add_argument(
        "--enable-v3",
        action="store_true",
        help="Enable localization gate v3 window sweep diagnostic (off by default).",
    )
    return parser.parse_args()


def config_from_args(args: argparse.Namespace):
    test_profile = os.environ.get("CC_TOY_LAB_S1_DISCRETIZATION_V2_STRESS_TEST_PROFILE")
    return build_stress_config(
        seed=args.seed,
        realizations=args.realizations,
        test_profile=test_profile,
        enable_v3=bool(args.enable_v3),
    )


def run(args: argparse.Namespace):
    config = config_from_args(args)
    assessment = run_s1_discretization_v2_stress(config)
    run_dir = make_run_dir(enable_v3=bool(args.enable_v3))
    artifacts = save_s1_discretization_v2_stress_artifacts(assessment, run_dir)
    print_summary(run_dir=run_dir, assessment=assessment, enable_v3=bool(args.enable_v3))
    return run_dir, assessment, artifacts


def make_run_dir(*, enable_v3: bool) -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base_dir = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = "_v3" if enable_v3 else ""
    run_dir = base_dir / f"{stamp}_s1_discretization_v2_stress{suffix}"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def print_summary(*, run_dir: Path, assessment, enable_v3: bool) -> None:
    print(f"run_path={run_dir}")
    print(f"stress_classification={assessment.stress_classification}")
    print(f"comparison_classification={assessment.comparison_classification}")
    print(f"fixed_window_all_families_passed={assessment.fixed_window_all_families_passed}")
    print(f"kernel_only_all_families_passed={assessment.kernel_only_all_families_passed}")
    if enable_v3:
        diag = assessment.stress_diagnostics
        print("localization_gate_v3_diagnostic=true")
        print(f"v3_window_robust_all_families={diag.get('v3_all_families_window_robust')}")
        print(f"v3_failure_count_by_family={diag.get('v3_failure_count_by_family')}")
        print(f"v2_vs_v3_disagreement_count_by_family={diag.get('v2_vs_v3_disagreement_count_by_family')}")
    print("s1_discretization_v2_stress complete")


def main() -> int:
    args = parse_args()
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
