"""CLI: targeted ring/alpha=0 follow-up diagnostic (product-discretized S2 x S1)."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s2_s1_product_discretized_ring_alpha0_followup import (  # noqa: E402
    build_ring_alpha0_followup_config,
    estimate_ring_alpha0_case_count,
    run_ring_alpha0_followup,
    save_ring_alpha0_followup_artifacts,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Ring/alpha=0 follow-up diagnostic: lattice-size scaling investigation."
    )
    p.add_argument(
        "--full",
        action="store_true",
        help="Run full targeted grid (s1_size up to 96; ~340-350 cases). Default is smoke grid.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Report grid size only, do not run operators.",
    )
    return p.parse_args()


def make_run_dir() -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base / f"{stamp}_s2_s1_product_discretized_ring_alpha0_followup"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def main() -> int:
    args = parse_args()
    smoke = not args.full
    cfg = build_ring_alpha0_followup_config(smoke=smoke)
    case_count = estimate_ring_alpha0_case_count(cfg)

    if args.dry_run:
        print(f"dry_run=True")
        print(f"smoke={cfg.smoke}")
        print(f"estimated_case_count={case_count}")
        print(f"ring_s1_sizes={cfg.ring_s1_sizes}")
        print(f"ring_q_values={cfg.ring_q_values}")
        print(f"ring_w_values={cfg.ring_w_values}")
        print(f"ring_seeds={cfg.ring_seeds}")
        print(f"reference_families={cfg.reference_families}")
        return 0

    run = run_ring_alpha0_followup(cfg)
    run_dir = make_run_dir()
    save_ring_alpha0_followup_artifacts(run, run_dir)

    print(f"run_path={run_dir}")
    print(f"ring_alpha0_followup_classification={run.classification}")
    print(f"decision_verdict={run.decision_rules.get('verdict', 'UNKNOWN')}")
    print(f"smoke={cfg.smoke} case_count={len(run.cases)}")
    print(f"complete_failure_count={run.evidence.get('complete_failure_count', 0)}")
    print(f"window_sensitive_count={run.evidence.get('window_sensitive_count', 0)}")
    print(f"failures_at_s1_size_ge_64={run.evidence.get('failures_at_s1_size_ge_64', 0)}")
    print(
        f"failure_rate_at_large_lattice={run.evidence.get('failure_rate_at_large_lattice', 0.0):.4f}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
