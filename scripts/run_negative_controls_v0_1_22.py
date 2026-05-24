"""Negative Controls Pilot Execution — v0.1.22 (54 cases)

⚠️ CRITICAL GUARDRAILS:
- This script executes FALSIFICATION controls, NOT validation
- DO NOT run without reviewing pre-registration + implementation plan
- Protocol immutability: grid locked (54 cases), no threshold changes
- Forbidden claims: "negative controls validate S³×S¹"
- Default mode: --print-plan (does NOT execute pilot)

Purpose:
    Test whether harness can reject non-geometric baselines.
    If ANY control reproduces Gate 4B-like PASS pattern → harness lacks specificity.

Grid: 54 cases (25% of Gate 4B 216-case grid)
    - 3 controls × 2 W × 3 sizes × 1 j_max × 3 seeds

Batching strategy:
    - 6 batches × 9 cases (split by control × disorder_W)
    - Batch runtime: ~14 min per batch (estimated)

Pre-requisites:
1. Pre-registration: reports/S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md
2. Implementation plan: reports/NEGATIVE_CONTROLS_IMPLEMENTATION_PLAN_v0.1.22.md
3. Unit tests pass: pytest tests/test_negative_controls_*.py -v
4. Git status clean

Date: 2026-05-22
Status: IMPLEMENTATION (pilot execution pending explicit command)

Related:
- reports/S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md
- reports/NEGATIVE_CONTROLS_IMPLEMENTATION_PLAN_v0.1.22.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import time
import json
import numpy as np
from collections import defaultdict

from cc_toy_lab.controls.negative_controls import (
    build_random_hermitian_control,
    build_scrambled_geometry_control,
    build_broken_wilson_control,
)
from cc_toy_lab.spectral.metrics import mean_adjacent_gap_ratio, inverse_participation_ratio
from scipy.linalg import eigh


# Locked v0.1.22 negative controls grid
PILOT_GRID = {
    "controls": ["random_hermitian", "scrambled_geometry", "broken_wilson_term"],  # 3
    "disorder_values": [0, 20],  # 2 (skip W=12 diagnostic)
    "sizes": [16, 64, 128],  # 3 (skip 32)
    "j_max_values": [3],  # 1 (max dimension only)
    "seeds": [123, 456, 789],  # 3
    "alpha": 0.0,  # S¹ flux (PBC)
    "radius": 1.0,  # Manifold radius
}

PROTOCOL_VERSION = "v0.1.22"  # Negative controls pilot
OUTPUT_BASE = Path("reports/RUNS/negative_controls_v0.1.22")


def generate_full_grid():
    """Generate exact 54-case negative controls pilot grid."""
    cases = []
    case_id = 0

    for control in PILOT_GRID["controls"]:
        for w in PILOT_GRID["disorder_values"]:
            for size in PILOT_GRID["sizes"]:
                for j_max in PILOT_GRID["j_max_values"]:
                    for seed in PILOT_GRID["seeds"]:
                        case = {
                            "id": case_id,
                            "control": control,
                            "disorder_strength": w,
                            "s1_size": size,
                            "j_max": j_max,
                            "seed": seed,
                            "alpha": PILOT_GRID["alpha"],
                            "radius": PILOT_GRID["radius"],
                        }
                        cases.append(case)
                        case_id += 1

    return cases


def split_into_batches(cases):
    """Split 54 cases into 6 batches by (control, disorder_W).

    Batch 1: random_hermitian, W=0   → 9 cases
    Batch 2: random_hermitian, W=20  → 9 cases
    Batch 3: scrambled_geometry, W=0 → 9 cases
    Batch 4: scrambled_geometry, W=20 → 9 cases
    Batch 5: broken_wilson, W=0      → 9 cases
    Batch 6: broken_wilson, W=20     → 9 cases

    Each batch = 3 sizes × 1 j_max × 3 seeds = 9 cases
    """
    batches = []
    batch_id = 1

    for control in PILOT_GRID["controls"]:
        for w in PILOT_GRID["disorder_values"]:
            batch_cases = [
                c for c in cases if c["control"] == control and c["disorder_strength"] == w
            ]
            batches.append(
                {
                    "batch_id": batch_id,
                    "control": control,
                    "disorder_W": w,
                    "cases": batch_cases,
                }
            )
            batch_id += 1

    return batches


def print_grid_plan(batches, total_cases):
    """Print full grid plan without execution (--print-plan mode)."""
    print("=" * 80)
    print("Negative Controls Pilot Grid Plan — v0.1.22")
    print("=" * 80)
    print()
    print(f"Total cases: {total_cases}")
    print(f"Total batches: {len(batches)}")
    print(f"Cases per batch: {len(batches[0]['cases'])} (expected)")
    print()
    print("Grid parameters (locked v0.1.22):")
    print(f"  Controls: {PILOT_GRID['controls']}")
    print(f"  Disorder W: {PILOT_GRID['disorder_values']}")
    print(f"  S¹ sizes: {PILOT_GRID['sizes']}")
    print(f"  j_max: {PILOT_GRID['j_max_values']}")
    print(f"  seeds: {PILOT_GRID['seeds']}")
    print(f"  alpha: {PILOT_GRID['alpha']}")
    print()
    print("Purpose:")
    print("  Falsification-first specificity test")
    print("  Expected: controls should FAIL to reproduce Gate 4B PASS pattern")
    print("  False-pass danger: if ANY control shows Gate 4B-like robustness")
    print()
    print("Batches:")
    for batch in batches:
        print(
            f"  Batch {batch['batch_id']}: {batch['control']}, W={batch['disorder_W']} "
            f"({len(batch['cases'])} cases)"
        )
    print()
    print("⚠️ Execution DISABLED by default")
    print("  To run pilot: add --run-pilot flag (NOT recommended without review)")
    print()
    print("=" * 80)


def run_single_case(case: dict) -> dict:
    """Execute one negative control case.

    Metrics (same as Gate 4B):
    - true_ipr_mean: Canonical IPR (bottom 10% eigenstates, eigenvector-based)
    - r_stat: Level-spacing adjacent gap ratio
    """
    control = case["control"]
    j_max = case["j_max"]
    s1_size = case["s1_size"]
    disorder_strength = case["disorder_strength"]
    seed = case["seed"]
    alpha = case["alpha"]
    radius = case["radius"]

    # Build control operator
    start_time = time.perf_counter()

    if control == "random_hermitian":
        operator, meta = build_random_hermitian_control(
            j_max=j_max,
            s1_size=s1_size,
            disorder_strength=disorder_strength,
            seed=seed,
            radius=radius,
        )
    elif control == "scrambled_geometry":
        operator, meta = build_scrambled_geometry_control(
            j_max=j_max,
            s1_size=s1_size,
            alpha=alpha,
            disorder_strength=disorder_strength,
            seed=seed,
            radius=radius,
            scramble_mode="permutation",  # Default scramble mode
        )
    elif control == "broken_wilson_term":
        operator, meta = build_broken_wilson_control(
            j_max=j_max,
            s1_size=s1_size,
            alpha=alpha,
            disorder_strength=disorder_strength,
            seed=seed,
            radius=radius,
            wilson_mode="disabled",  # Default Wilson mode
        )
    else:
        raise ValueError(f"unknown control: {control}")

    # Compute eigenvalues + eigenvectors (full diagonalization)
    eigenvalues, eigenvectors = eigh(operator)

    # True IPR metric (v0.1.21 canonical metric)
    # Use bottom 10% eigenstates
    n_total = len(eigenvalues)
    n_low = max(1, int(0.1 * n_total))
    low_eigvecs = eigenvectors[:, :n_low]

    ipr_values = inverse_participation_ratio(low_eigvecs)
    true_ipr_mean = float(np.mean(ipr_values))

    # r-statistic (level-spacing diagnostic)
    r_stat = mean_adjacent_gap_ratio(eigenvalues)

    runtime_seconds = time.perf_counter() - start_time

    # Output
    result = {
        "control": control,
        "disorder_strength": disorder_strength,
        "s1_size": s1_size,
        "j_max": j_max,
        "seed": seed,
        "alpha": alpha,
        "radius": radius,
        "N": meta["total_dimension"],
        "true_ipr_mean": true_ipr_mean,
        "r_stat": r_stat,
        "uses_eigenvectors": True,
        "ipr_metric_version": "v0.1.22_negative_controls_true_ipr",
        "runtime_seconds": runtime_seconds,
        "meta": meta,
    }

    return result


def run_batch(
    batch: dict, output_dir: Path, case_limit: int = None, cooling_pause: float = 0.0
) -> list[dict]:
    """Execute all cases in one batch (or limited number for smoke test).

    Args:
        batch: Batch configuration dict
        output_dir: Output directory path
        case_limit: Optional limit on number of cases
        cooling_pause: Seconds to pause between cases (thermal constraint mitigation)
    """
    batch_dir = output_dir / f"batch_{batch['batch_id']:02d}"
    batch_dir.mkdir(parents=True, exist_ok=True)

    results = []
    cases_to_run = batch["cases"][:case_limit] if case_limit else batch["cases"]

    for i, case in enumerate(cases_to_run, start=1):
        print(
            f"  Case {i}/{len(cases_to_run)}: "
            f"{case['control']}, W={case['disorder_strength']}, "
            f"s1_size={case['s1_size']}, seed={case['seed']}..."
        )
        result = run_single_case(case)
        results.append(result)

        # Save individual case result
        case_file = batch_dir / f"case_{case['id']:03d}.json"
        with open(case_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        # Cooling pause (thermal constraint mitigation)
        if cooling_pause > 0 and i < len(cases_to_run):
            print(f"    💤 Cooling pause: {cooling_pause}s...")
            time.sleep(cooling_pause)

    return results


def main():
    parser = argparse.ArgumentParser(description="Negative Controls Pilot Execution v0.1.22")
    parser.add_argument(
        "--print-plan",
        action="store_true",
        default=True,
        help="Print grid plan without execution (default)",
    )
    parser.add_argument(
        "--run-pilot",
        action="store_true",
        default=False,
        help="⚠️ Execute 54-case pilot grid (requires explicit flag)",
    )
    parser.add_argument(
        "--batch-id",
        type=int,
        default=None,
        help="Run specific batch only (1-6)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(OUTPUT_BASE),
        help=f"Output directory (default: {OUTPUT_BASE})",
    )
    parser.add_argument(
        "--case-limit",
        type=int,
        default=None,
        help="Limit number of cases per batch (for smoke tests)",
    )
    parser.add_argument(
        "--cooling-pause",
        type=float,
        default=0.0,
        help="Pause (seconds) between cases for CPU cooling (thermal constraint mitigation)",
    )

    args = parser.parse_args()

    cases = generate_full_grid()
    batches = split_into_batches(cases)

    # Default: print plan only
    if not args.run_pilot:
        print_grid_plan(batches, len(cases))
        return

    # Execution blocked unless --run-pilot explicitly provided
    print("⚠️ WARNING: Executing negative controls pilot (54 cases)")
    print("   This is a falsification test, NOT a validation claim")
    print()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save grid config
    config = {
        "protocol_version": PROTOCOL_VERSION,
        "total_cases": len(cases),
        "total_batches": len(batches),
        "grid": PILOT_GRID,
    }
    config_file = output_dir / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # Execute batches
    if args.batch_id is not None:
        # Run single batch
        batch = batches[args.batch_id - 1]
        print(f"Running Batch {batch['batch_id']}/{len(batches)}...")
        if args.case_limit:
            print(f"  ⚠️ Smoke test mode: limiting to {args.case_limit} case(s)")
        if args.cooling_pause > 0:
            print(f"  ❄️ Thermal mitigation: {args.cooling_pause}s pause between cases")
        run_batch(batch, output_dir, case_limit=args.case_limit, cooling_pause=args.cooling_pause)
    else:
        # Run all batches
        for batch in batches:
            print(f"Running Batch {batch['batch_id']}/{len(batches)}...")
            if args.case_limit:
                print(f"  ⚠️ Smoke test mode: limiting to {args.case_limit} case(s)")
            if args.cooling_pause > 0:
                print(f"  ❄️ Thermal mitigation: {args.cooling_pause}s pause between cases")
            run_batch(
                batch, output_dir, case_limit=args.case_limit, cooling_pause=args.cooling_pause
            )

    print()
    print("✓ Negative controls pilot execution complete")
    print(f"  Output: {output_dir}")
    print()
    print("⚠️ NEXT STEPS:")
    print("  1. Aggregate results: python scripts/aggregate_negative_controls_results.py")
    print("  2. Apply decision rules: python scripts/apply_negative_controls_decision_rules.py")
    print("  3. Write results report: reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md")
    print()


if __name__ == "__main__":
    main()
