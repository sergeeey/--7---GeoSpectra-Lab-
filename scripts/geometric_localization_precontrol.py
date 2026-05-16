"""CLI: graph-Laplacian geometric localization pre-control and dumbbell tiny diagnostic."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.geometry.geometric_localization_precontrol import (  # noqa: E402
    run_dumbbell_tiny_diagnostic,
    run_straight_cylinder_precontrol,
    run_variable_radius_cylinder_precontrol,
    save_dumbbell_tiny_diagnostic_artifacts,
    save_straight_cylinder_precontrol_artifacts,
    save_variable_radius_cylinder_precontrol_artifacts,
    tiny_dumbbell_config,
    tiny_straight_cylinder_config,
    tiny_variable_radius_cylinder_config,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Graph-Laplacian pre-control (cylinders) and dumbbell tiny diagnostic."
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--straight-cylinder",
        action="store_true",
        help="Straight-cylinder null geometry.",
    )
    g.add_argument(
        "--variable-radius-cylinder",
        action="store_true",
        help="Variable-radius cylinder semi-analytic control.",
    )
    g.add_argument(
        "--dumbbell",
        action="store_true",
        help="Dumbbell / throat-like tiny diagnostic (two-bulb smooth r(z)).",
    )
    p.add_argument(
        "--tiny",
        action="store_true",
        help="Tiny profile for the selected geometry flag.",
    )
    return p.parse_args()


def make_run_dir(*, suffix: str) -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base / f"{stamp}_geometric_localization_precontrol_{suffix}"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def main() -> int:
    args = parse_args()
    if not args.tiny:
        print("error: add --tiny (only tiny profiles are wired in this CLI)", file=sys.stderr)
        return 2
    if args.straight_cylinder:
        cfg = tiny_straight_cylinder_config()
        result = run_straight_cylinder_precontrol(cfg)
        run_dir = make_run_dir(suffix="straight_cylinder_tiny")
        save_straight_cylinder_precontrol_artifacts(result, run_dir)
        print(f"run_path={run_dir}")
        print(f"null_verdict={result.null_verdict}")
        print(f"n_points={result.n_points} connected_components={result.connected_components}")
        return 0
    if args.variable_radius_cylinder:
        cfg = tiny_variable_radius_cylinder_config()
        result = run_variable_radius_cylinder_precontrol(cfg)
        run_dir = make_run_dir(suffix="variable_radius_cylinder_tiny")
        save_variable_radius_cylinder_precontrol_artifacts(result, run_dir)
        print(f"run_path={run_dir}")
        print(f"control_verdict={result.control_verdict}")
        print(
            f"n_points={result.n_points} connected_components={result.connected_components} "
            f"radial_extent_ratio={result.radial_extent_ratio:.6g}"
        )
        return 0
    cfg = tiny_dumbbell_config()
    result = run_dumbbell_tiny_diagnostic(cfg)
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base / f"{stamp}_geometric_localization_dumbbell_tiny"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    save_dumbbell_tiny_diagnostic_artifacts(result, run_dir)
    print(f"run_path={run_dir}")
    print(f"aggregate_verdict={result.aggregate_verdict}")
    print(f"k_sensitivity_ok_by_throat={result.k_sensitivity_ok_by_throat}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
