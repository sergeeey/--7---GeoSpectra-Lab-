"""Gate 4B Batched Execution — S³×S¹ Finite-Size Scaling (216 cases) v0.1.21

VERSION: v0.1.21 (Metric-Corrected)
CRITICAL CHANGE FROM v0.1.20:
- Metric corrected: eigvalsh → eigh (eigenvalues + eigenvectors)
- True IPR = Σ|ψᵢ|⁴ (eigenvector-based), NOT mean(eigenvalues)
- Grid UNCHANGED: same 216 cases as v0.1.20
- Thresholds UNCHANGED: same decision rules

⚠️ CRITICAL GUARDRAILS:
- This script executes the LOCKED Gate 4 pre-registration (commit 1f4173c + v0.1.21 protocol)
- Do NOT run without completing pre-run thermal checklist + unit tests
- Protocol immutability: no grid/threshold changes allowed
- Forbidden claims: "S³×S¹ validated", "FL generalized", "W=20 optimal"
- No partial PASS: verdict requires all 216 cases complete

Batching strategy:
- 9 batches × 24 cases (split by family × disorder_W)
- Batch runtime: ~16 min per batch (v0.1.20 estimate)
- v0.1.21 runtime: TBD (benchmark required, ~10× overhead expected)

Pre-requisites:
1. Pre-registration locked: commit 1f4173c (v0.1.20) + v0.1.21 protocol
2. Unit tests pass: pytest tests/test_ipr_metric.py -v (ALL GREEN)
3. Runtime benchmark completed
4. Git status clean

Date: 2026-05-22 (v0.1.21 metric correction)
Status: METRIC IMPLEMENTATION (not protocol/grid change)

Related:
- reports/S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md
- reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md
- reports/GATE4_TRUE_IPR_RECOVERY_CHECK_v0.1.20.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import time
import json
import numpy as np
from collections import defaultdict

from cc_toy_lab.spectral.s3_s1_product_discretized import build_s3_s1_product_operator
from cc_toy_lab.spectral.metrics import mean_adjacent_gap_ratio, inverse_participation_ratio


# Locked Gate 4 pre-registration grid (commit 1f4173c)
FULL_GRID = {
    "families": ["spectral_circle", "ring", "wilson_ring"],  # 3
    "disorder_values": [0, 12, 20],  # 3
    "sizes": [16, 32, 64, 128],  # 4
    "j_max_values": [2, 3],  # 2
    "seeds": [123, 456, 789],  # 3
    "alpha": 0.0,  # S¹ flux (PBC)
    "mode": "geometric_weight",  # Disorder mode
    "radius": 1.0,  # Manifold radius
}

# Protocol commits
PROTOCOL_COMMIT = "1f4173c"  # Original v0.1.20 protocol
DRY_RUN_RESULTS_COMMIT = "52d221f"
BATCH_PROTOCOL_VERSION = "v0.1.21"  # Metric-corrected: true IPR

# Output directory (v0.1.21: metric-corrected rerun)
OUTPUT_BASE = Path("reports/RUNS/gate4_fss_v0.1.21")


def generate_full_grid():
    """Generate exact 216-case full Gate 4 grid from locked protocol."""
    cases = []
    case_id = 0

    for family in FULL_GRID["families"]:
        for w in FULL_GRID["disorder_values"]:
            for size in FULL_GRID["sizes"]:
                for j_max in FULL_GRID["j_max_values"]:
                    for seed in FULL_GRID["seeds"]:
                        case = {
                            "id": case_id,
                            "family": family,
                            "disorder_strength": w,
                            "s1_size": size,
                            "j_max": j_max,
                            "seed": seed,
                            "alpha": FULL_GRID["alpha"],
                            "mode": FULL_GRID["mode"],
                            "radius": FULL_GRID["radius"],
                        }
                        cases.append(case)
                        case_id += 1

    return cases


def split_into_batches(cases):
    """Split 216 cases into 9 batches by (family, disorder_W).

    Batch 1: spectral_circle, W=0   → 24 cases
    Batch 2: spectral_circle, W=12  → 24 cases
    Batch 3: spectral_circle, W=20  → 24 cases
    Batch 4: ring, W=0              → 24 cases
    Batch 5: ring, W=12             → 24 cases
    Batch 6: ring, W=20             → 24 cases
    Batch 7: wilson_ring, W=0       → 24 cases
    Batch 8: wilson_ring, W=12      → 24 cases
    Batch 9: wilson_ring, W=20      → 24 cases

    Each batch = 4 sizes × 2 j_max × 3 seeds = 24 cases
    """
    batches = []
    batch_id = 1

    for family in FULL_GRID["families"]:
        for w in FULL_GRID["disorder_values"]:
            batch_cases = [
                c for c in cases if c["family"] == family and c["disorder_strength"] == w
            ]
            batches.append(
                {
                    "batch_id": batch_id,
                    "family": family,
                    "disorder_W": w,
                    "cases": batch_cases,
                }
            )
            batch_id += 1

    return batches


def print_grid_plan(batches, total_cases):
    """Print full grid plan without execution (--print-plan mode)."""
    print("=" * 80)
    print("Gate 4 Full Grid Plan — S³×S¹ Finite-Size Scaling")
    print("=" * 80)
    print()
    print(f"Total cases: {total_cases}")
    print(f"Total batches: {len(batches)}")
    print(f"Cases per batch: {len(batches[0]['cases'])} (expected)")
    print()
    print("Grid parameters (locked, commit 1f4173c):")
    print(f"  Families: {FULL_GRID['families']}")
    print(f"  Disorder W: {FULL_GRID['disorder_values']}")
    print(f"  S¹ sizes: {FULL_GRID['sizes']}")
    print(f"  j_max: {FULL_GRID['j_max_values']}")
    print(f"  Seeds: {FULL_GRID['seeds']}")
    print()
    print("Breakdown:")
    print(
        f"  {len(FULL_GRID['families'])} families × {len(FULL_GRID['disorder_values'])} W × "
        f"{len(FULL_GRID['sizes'])} sizes × {len(FULL_GRID['j_max_values'])} j_max × "
        f"{len(FULL_GRID['seeds'])} seeds = {total_cases} cases"
    )
    print()
    print("-" * 80)
    print("Batch assignments:")
    print("-" * 80)

    for batch in batches:
        print(
            f"Batch {batch['batch_id']:2d}: {batch['family']:20s} W={batch['disorder_W']:2.0f} "
            f"→ {len(batch['cases']):2d} cases"
        )

    print()
    print("-" * 80)
    print("Coverage verification:")
    print("-" * 80)

    # Check for duplicates
    all_case_ids = []
    for batch in batches:
        all_case_ids.extend([c["id"] for c in batch["cases"]])

    n_unique = len(set(all_case_ids))
    n_duplicates = len(all_case_ids) - n_unique

    print(f"Total assigned cases: {len(all_case_ids)}")
    print(f"Unique cases: {n_unique}")
    print(f"Duplicates: {n_duplicates}")
    print(f"Missing cases: {total_cases - n_unique}")

    if n_unique == total_cases and n_duplicates == 0:
        print()
        print("✅ Coverage check PASSED: all 216 cases covered exactly once")
    else:
        print()
        print("❌ Coverage check FAILED: duplicates or missing cases detected")
        raise ValueError("Batch split has coverage errors")

    print()


def run_single_case(case):
    """Run single Gate 4 case and collect all required metrics.

    Metrics collected:
    - IPR (inverse participation ratio)
    - r-statistic (adjacent gap ratio)
    - Runtime
    - Error status
    """
    start = time.time()
    error = None
    mean_low_ipr = None
    r_stat = None
    r_stat_available = False
    r_stat_reason = None

    try:
        H, chi, meta = build_s3_s1_product_operator(
            j_max=case["j_max"],
            s1_family=case["family"],
            s1_size=case["s1_size"],
            alpha=case["alpha"],
            mode=case["mode"],
            disorder_strength=case["disorder_strength"],
            seed=case["seed"],
            radius=case["radius"],
        )

        # Compute eigenvalues AND eigenvectors (v0.1.21: corrected from eigvalsh)
        eigvals, eigvecs = np.linalg.eigh(H)

        # True IPR metric (v0.1.21: eigenvector-based, corrected from eigenvalue mean)
        N = H.shape[0]
        n_low = int(0.1 * N)  # Bottom 10%
        low_indices = np.argsort(eigvals)[:n_low]
        low_eigvals = eigvals[low_indices]
        low_eigvecs = eigvecs[:, low_indices]

        # Compute true IPR = Σ|ψᵢ|⁴ for each low eigenstate
        iprs = inverse_participation_ratio(low_eigvecs)  # Returns array
        mean_low_ipr = float(np.mean(iprs))

        # Diagnostic: eigenvalue mean (for v0.1.20 comparison)
        mean_low_eigenvalue = float(np.mean(low_eigvals))

        # r-statistic (adjacent gap ratio)
        # Use spectral window for localization analysis (bottom 10% same as IPR)
        try:
            r_stat = mean_adjacent_gap_ratio(low_eigvals)

            # Check if r-statistic is valid (not NaN)
            if np.isnan(r_stat):
                r_stat_available = False
                r_stat_reason = "insufficient_eigenvalues_in_window"
            else:
                r_stat_available = True
                r_stat_reason = None

        except Exception as e:
            r_stat = None
            r_stat_available = False
            r_stat_reason = f"r_stat_computation_error: {str(e)[:50]}"

    except Exception as e:
        error = str(e)
        mean_low_ipr = None
        mean_low_eigenvalue = None
        r_stat = None
        r_stat_available = False
        r_stat_reason = "case_execution_failed"

    elapsed = time.time() - start

    result = {
        "case_id": case["id"],
        "family": case["family"],
        "disorder_strength": case["disorder_strength"],
        "s1_size": case["s1_size"],
        "j_max": case["j_max"],
        "seed": case["seed"],
        "runtime_sec": elapsed,
        # v0.1.21 canonical metric fields
        "true_ipr_mean": mean_low_ipr,  # Canonical: mean of true IPR = Σ|ψᵢ|⁴
        "uses_eigenvectors": True,  # Confirms eigenvector-based computation
        # Diagnostic fields
        "mean_low_eigenvalue": mean_low_eigenvalue,  # For v0.1.20 comparison
        # Deprecated compatibility alias (v0.1.20 field name)
        "mean_low_ipr": mean_low_ipr,  # DEPRECATED: use true_ipr_mean (v0.1.21+)
        # Metadata
        "ipr_metric_version": "v0.1.21_true_eigenvector_ipr",
        # r-statistic (unchanged)
        "r_stat": r_stat,
        "r_stat_available": r_stat_available,
        "r_stat_reason": r_stat_reason,
        "error": error,
    }

    return result


def save_batch_results(batch_dir, batch, results, batch_runtime):
    """Save batch results to batch directory."""
    batch_dir.mkdir(parents=True, exist_ok=True)

    # batch_config.json
    config = {
        "batch_id": batch["batch_id"],
        "family": batch["family"],
        "disorder_W": batch["disorder_W"],
        "n_cases": len(batch["cases"]),
        "protocol_commit": PROTOCOL_COMMIT,
        "dry_run_results_commit": DRY_RUN_RESULTS_COMMIT,
        "batch_protocol_version": BATCH_PROTOCOL_VERSION,
    }
    with open(batch_dir / "batch_config.json", "w") as f:
        json.dump(config, f, indent=2)

    # results.json (per-case results)
    with open(batch_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    # timing.json
    timing_by_size = defaultdict(list)
    timing_by_jmax = defaultdict(list)

    for r in results:
        if r["error"] is None:
            timing_by_size[r["s1_size"]].append(r["runtime_sec"])
            timing_by_jmax[r["j_max"]].append(r["runtime_sec"])

    timing = {
        "batch_runtime_sec": batch_runtime,
        "per_case_mean_sec": batch_runtime / len(results) if results else 0,
        "per_case_max_sec": max((r["runtime_sec"] for r in results), default=0),
        "by_size": {k: float(np.mean(v)) for k, v in timing_by_size.items()},
        "by_jmax": {k: float(np.mean(v)) for k, v in timing_by_jmax.items()},
    }
    with open(batch_dir / "timing.json", "w") as f:
        json.dump(timing, f, indent=2)

    # status.json
    n_failed = sum(1 for r in results if r["error"] is not None)
    n_r_stat_unavailable = sum(1 for r in results if not r["r_stat_available"])

    if n_failed > 0:
        status = "completed_with_failures"
    elif n_r_stat_unavailable > 0:
        status = "completed_with_missing_r_stat"
    else:
        status = "completed"

    status_data = {
        "status": status,
        "n_cases": len(results),
        "n_failed": n_failed,
        "n_r_stat_unavailable": n_r_stat_unavailable,
        "batch_runtime_sec": batch_runtime,
    }
    with open(batch_dir / "status.json", "w") as f:
        json.dump(status_data, f, indent=2)

    # summary.md
    summary_lines = [
        f"# Batch {batch['batch_id']} Summary",
        "",
        f"**Family:** {batch['family']}",
        f"**Disorder W:** {batch['disorder_W']}",
        "",
        "## Execution",
        f"- Total cases: {len(results)}",
        f"- Completed: {len(results) - n_failed}",
        f"- Failed: {n_failed}",
        f"- r-statistic unavailable: {n_r_stat_unavailable}",
        "",
        "## Runtime",
        f"- Batch total: {batch_runtime/60:.1f} min",
        f"- Per-case mean: {timing['per_case_mean_sec']:.2f} sec",
        f"- Per-case max: {timing['per_case_max_sec']:.2f} sec",
        "",
        "## Status",
        f"**{status.upper()}**",
        "",
        "## Protocol References",
        f"- Pre-registration: commit {PROTOCOL_COMMIT}",
        f"- Dry-run results: commit {DRY_RUN_RESULTS_COMMIT}",
        "",
    ]

    with open(batch_dir / "summary.md", "w") as f:
        f.write("\n".join(summary_lines))


def run_batch(batch, output_base, force=False):
    """Execute a single batch."""
    batch_id = batch["batch_id"]
    batch_dir = output_base / "batches" / f"batch_{batch_id:02d}"

    # Check if batch already completed (resume logic)
    status_file = batch_dir / "status.json"
    if status_file.exists() and not force:
        with open(status_file, "r") as f:
            status_data = json.load(f)

        if status_data["status"] in ["completed", "completed_with_missing_r_stat"]:
            print(
                f"Batch {batch_id:2d} already completed (status: {status_data['status']}). Skipping."
            )
            print(f"Use --force to re-run.")
            return status_data

    print("=" * 80)
    print(f"Batch {batch_id:2d}: {batch['family']} W={batch['disorder_W']}")
    print("=" * 80)
    print(f"Cases: {len(batch['cases'])}")
    print(f"Output: {batch_dir}")
    print()
    print("-" * 80)

    start_batch = time.time()
    results = []

    for i, case in enumerate(batch["cases"]):
        print(
            f"[{i+1}/{len(batch['cases'])}] "
            f"N={case['s1_size']:3d} j_max={case['j_max']} seed={case['seed']} ... ",
            end="",
            flush=True,
        )

        result = run_single_case(case)
        results.append(result)

        if result["error"] is None:
            r_marker = "✅" if result["r_stat_available"] else "⚠️"
            print(f"{r_marker} {result['runtime_sec']:.2f}s")
        else:
            print(f"❌ FAILED: {result['error'][:50]}")

    batch_runtime = time.time() - start_batch

    print("-" * 80)
    print()
    print(
        f"✅ Batch {batch_id:2d} complete: {len(batch['cases'])} cases in {batch_runtime/60:.1f} min"
    )
    print()

    # Save results
    save_batch_results(batch_dir, batch, results, batch_runtime)

    # Read status
    with open(batch_dir / "status.json", "r") as f:
        status_data = json.load(f)

    return status_data


def check_all_batches_complete(output_base, n_batches):
    """Check if all batches have completed successfully."""
    batches_dir = output_base / "batches"

    if not batches_dir.exists():
        return False, "No batches directory found"

    statuses = []
    for batch_id in range(1, n_batches + 1):
        status_file = batches_dir / f"batch_{batch_id:02d}" / "status.json"

        if not status_file.exists():
            return False, f"Batch {batch_id} not started"

        with open(status_file, "r") as f:
            status = json.load(f)

        statuses.append(status)

        if status["status"] not in ["completed", "completed_with_missing_r_stat"]:
            return False, f"Batch {batch_id} status: {status['status']}"

    # Check for failures
    total_failed = sum(s["n_failed"] for s in statuses)
    if total_failed > 0:
        return False, f"Total failures across batches: {total_failed}"

    return True, "All batches completed successfully"


def main():
    """Run Gate 4 batched execution."""
    parser = argparse.ArgumentParser(
        description="Gate 4 Batched Execution — S³×S¹ Finite-Size Scaling"
    )
    parser.add_argument(
        "--print-plan",
        action="store_true",
        help="Print grid plan and batch assignments without execution",
    )
    parser.add_argument("--batch-id", type=int, help="Run specific batch (1-9)")
    parser.add_argument(
        "--run-all", action="store_true", help="Run all 9 batches sequentially (⚠️ USE WITH CAUTION)"
    )
    parser.add_argument(
        "--resume", action="store_true", help="Resume execution (skip completed batches)"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force re-run (overwrite existing batch results)"
    )
    args = parser.parse_args()

    # Generate full grid and batches
    cases = generate_full_grid()
    batches = split_into_batches(cases)

    # Verify coverage
    assert len(cases) == 216, f"Grid should have 216 cases, got {len(cases)}"
    assert len(batches) == 9, f"Should have 9 batches, got {len(batches)}"
    for batch in batches:
        assert (
            len(batch["cases"]) == 24
        ), f"Batch {batch['batch_id']} should have 24 cases, got {len(batch['cases'])}"

    # Print plan mode
    if args.print_plan:
        print_grid_plan(batches, len(cases))

        if args.batch_id:
            print()
            print("=" * 80)
            print(f"Batch {args.batch_id} Detail")
            print("=" * 80)
            batch = batches[args.batch_id - 1]
            print(f"Family: {batch['family']}")
            print(f"Disorder W: {batch['disorder_W']}")
            print(f"Cases: {len(batch['cases'])}")
            print()
            print("Sample cases (first 5):")
            for i, case in enumerate(batch["cases"][:5]):
                print(
                    f"  Case {case['id']:3d}: N={case['s1_size']:3d} "
                    f"j_max={case['j_max']} seed={case['seed']}"
                )
            print("  ...")

        return

    # Execution mode
    if not (args.batch_id or args.run_all or args.resume):
        print("ERROR: Must specify --batch-id, --run-all, or --resume")
        print("Use --print-plan to verify grid without execution")
        raise SystemExit(1)

    # Guardrails
    print()
    print("=" * 80)
    print("⚠️ CRITICAL GUARDRAILS")
    print("=" * 80)
    print("- Protocol locked: commit 1f4173c")
    print("- No grid/threshold changes allowed")
    print("- Forbidden claims: 'S³×S¹ validated', 'FL generalized', 'W=20 optimal'")
    print("- No partial PASS: verdict requires all 216 cases")
    print()

    if args.run_all:
        print("⚠️ WARNING: --run-all will execute ALL 9 batches sequentially (~2.4h)")
        print()

    # Save full grid config
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    config = {
        "purpose": "Gate 4 full execution (216 cases)",
        "protocol_commit": PROTOCOL_COMMIT,
        "dry_run_results_commit": DRY_RUN_RESULTS_COMMIT,
        "batch_protocol_version": BATCH_PROTOCOL_VERSION,
        "grid": FULL_GRID,
        "n_cases": len(cases),
        "n_batches": len(batches),
    }
    with open(OUTPUT_BASE / "config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Run batches
    if args.batch_id:
        batch = batches[args.batch_id - 1]
        run_batch(batch, OUTPUT_BASE, force=args.force)

    elif args.run_all or args.resume:
        for batch in batches:
            run_batch(batch, OUTPUT_BASE, force=args.force)

    # Check completion
    print()
    print("=" * 80)
    print("Overall Status")
    print("=" * 80)

    all_complete, message = check_all_batches_complete(OUTPUT_BASE, len(batches))

    print(f"Status: {message}")
    print()

    if all_complete:
        print("✅ All batches completed successfully")
        print()
        print("Next steps:")
        print("1. Merge results: Create merged/ directory")
        print("2. Verify coverage: All 216 cases present")
        print("3. Apply Decision Rule 1: 2.0× IPR contrast + r toward Poisson")
        print("4. Generate gate4_verdict.md: PASS/FAIL/PASS_WITH_CAVEATS")
    else:
        print("⚠️ Gate 4 incomplete")
        print()
        print("Action required:")
        print("- Re-run failed batches with --batch-id and --force")
        print("- Or use --resume to continue from last incomplete batch")
        print()
        print("DO NOT issue verdict until all batches complete")


if __name__ == "__main__":
    main()
