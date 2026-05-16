"""CLI: targeted W≈4 transition-regime diagnostic (product-discretized S2 x S1)."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s2_s1_product_discretized_w4_diagnostic import (  # noqa: E402
    build_w4_diagnostic_config,
    run_w4_diagnostic,
    save_w4_diagnostic_artifacts,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="W-sweep diagnostic near W=4 (product-discretized caveat).")
    p.add_argument(
        "--full",
        action="store_true",
        help="Run full milestone grid (large; not for CI). Default is smoke grid.",
    )
    return p.parse_args()


def make_run_dir() -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base / f"{stamp}_s2_s1_product_discretized_w4_diagnostic"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def main() -> int:
    args = parse_args()
    smoke = not args.full
    cfg = build_w4_diagnostic_config(smoke=smoke)
    run = run_w4_diagnostic(cfg)
    run_dir = make_run_dir()
    save_w4_diagnostic_artifacts(run, run_dir)
    print(f"run_path={run_dir}")
    print(f"w4_diagnostic_classification={run.classification}")
    print(f"smoke={cfg.smoke} case_count={len(run.cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
