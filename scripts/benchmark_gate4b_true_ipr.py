"""Gate 4B True IPR Runtime Benchmark — v0.1.21

Measures eigenvector-based IPR runtime overhead before full 216-case rerun.

Purpose:
- Measure true IPR runtime (eigh) vs v0.1.20 (eigvalsh)
- Extrapolate 216-case runtime estimate
- Decide execution mode: full grid / batched / pilot / reduce grid

NOT a scientific test — this is a feasibility check.

Benchmark plan: reports/GATE4B_TRUE_IPR_RUNTIME_BENCHMARK_PLAN_v0.1.21.md

Date: 2026-05-22
Status: RUNTIME FEASIBILITY CHECK (not protocol/validation)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import time
import numpy as np
from datetime import datetime

from cc_toy_lab.spectral.s3_s1_product_discretized import build_s3_s1_product_operator
from cc_toy_lab.spectral.metrics import inverse_participation_ratio, mean_adjacent_gap_ratio


# Benchmark cases (from benchmark plan v0.1.21)
BENCHMARK_CASES = [
    {
        "id": "case_001_small",
        "label": "Small (baseline)",
        "family": "spectral_circle",
        "disorder_W": 0,
        "s1_size": 16,
        "j_max": 2,
        "seed": 123,
        "expected_N": 464,  # 16 × 29 j_max=2
        "purpose": "Minimum overhead measurement",
    },
    {
        "id": "case_002_medium",
        "label": "Medium (Gate 3C size)",
        "family": "ring",
        "disorder_W": 12,
        "s1_size": 64,
        "j_max": 3,
        "seed": 123,
        "expected_N": 2432,  # 64 × 38 j_max=3
        "purpose": "Typical case, comparable to Gate 3C",
    },
    {
        "id": "case_003_worst_case",
        "label": "Worst-case-like (largest)",
        "family": "wilson_ring",
        "disorder_W": 20,
        "s1_size": 128,
        "j_max": 3,
        "seed": 123,
        "expected_N": 3712,  # 128 × 29 j_max=3
        "purpose": "Upper bound overhead, largest N in grid",
    },
]

# Output directory
OUTPUT_DIR = Path("reports/RUNS/gate4b_true_ipr_benchmark_v0.1.21")

# v0.1.20 reference runtime (from actual run)
V0120_TOTAL_RUNTIME = 96.1  # minutes (216 cases)
V0120_MEAN_RUNTIME_PER_CASE = V0120_TOTAL_RUNTIME / 216  # ~0.445 minutes = 27 seconds


def run_benchmark_case(case):
    """Run single benchmark case and measure runtime + output fields."""
    print(f"\n{'='*80}")
    print(f"Running: {case['label']} ({case['id']})")
    print(
        f"Config: family={case['family']}, W={case['disorder_W']}, "
        f"s1_size={case['s1_size']}, j_max={case['j_max']}"
    )
    print(f"Expected N: ~{case['expected_N']}")
    print(f"{'='*80}")

    start = time.time()
    error = None
    actual_N = None
    true_ipr_mean = None
    mean_low_eigenvalue = None
    r_stat = None
    uses_eigenvectors = None
    ipr_metric_version = None

    try:
        # Build Hamiltonian
        H, chi, meta = build_s3_s1_product_operator(
            j_max=case["j_max"],
            s1_family=case["family"],
            s1_size=case["s1_size"],
            alpha=0.0,  # PBC
            mode="geometric_weight",
            disorder_strength=case["disorder_W"],
            seed=case["seed"],
            radius=1.0,
        )

        actual_N = H.shape[0]
        print(f"Actual N: {actual_N} (expected ~{case['expected_N']})")

        # Compute eigenvalues + eigenvectors (v0.1.21: eigh)
        print("Computing eigenvalues + eigenvectors (np.linalg.eigh)...")
        eig_start = time.time()
        eigvals, eigvecs = np.linalg.eigh(H)
        eig_elapsed = time.time() - eig_start
        print(f"  eigh completed in {eig_elapsed:.2f} sec")

        # True IPR computation
        n_low = int(0.1 * actual_N)
        low_indices = np.argsort(eigvals)[:n_low]
        low_eigvals = eigvals[low_indices]
        low_eigvecs = eigvecs[:, low_indices]

        print(f"Computing true IPR for {n_low} low eigenstates...")
        ipr_start = time.time()
        iprs = inverse_participation_ratio(low_eigvecs)
        true_ipr_mean = float(np.mean(iprs))
        ipr_elapsed = time.time() - ipr_start
        print(f"  IPR computation completed in {ipr_elapsed:.2f} sec")
        print(f"  true_ipr_mean = {true_ipr_mean:.6f}")

        # Diagnostic fields
        mean_low_eigenvalue = float(np.mean(low_eigvals))
        uses_eigenvectors = True
        ipr_metric_version = "v0.1.21_true_eigenvector_ipr"

        # r-statistic (secondary metric)
        try:
            r_stat = mean_adjacent_gap_ratio(low_eigvals)
            if np.isnan(r_stat):
                r_stat = None
            else:
                r_stat = float(r_stat)
        except Exception as e:
            r_stat = None
            print(f"  r-stat computation failed: {str(e)[:50]}")

        print(f"  r_stat = {r_stat if r_stat is not None else 'N/A'}")

    except Exception as e:
        error = str(e)
        print(f"\n❌ ERROR: {error}")

    elapsed = time.time() - start

    result = {
        "case_id": case["id"],
        "label": case["label"],
        "family": case["family"],
        "disorder_W": case["disorder_W"],
        "s1_size": case["s1_size"],
        "j_max": case["j_max"],
        "seed": case["seed"],
        "expected_N": case["expected_N"],
        "actual_N": actual_N,
        "runtime_sec": elapsed,
        "runtime_min": elapsed / 60,
        # v0.1.21 canonical fields
        "true_ipr_mean": true_ipr_mean,
        "uses_eigenvectors": uses_eigenvectors,
        "ipr_metric_version": ipr_metric_version,
        # Diagnostic fields
        "mean_low_eigenvalue": mean_low_eigenvalue,
        "r_stat": r_stat,
        "error": error,
    }

    print(f"\n✅ Case completed in {elapsed:.2f} sec ({elapsed/60:.2f} min)")

    return result


def compute_extrapolation(results):
    """Compute extrapolated 216-case runtime estimate."""
    successful_cases = [r for r in results if r["error"] is None]

    if not successful_cases:
        return {
            "status": "FAILED",
            "reason": "No successful benchmark cases",
        }

    # Mean runtime per case
    runtimes_sec = [r["runtime_sec"] for r in successful_cases]
    mean_runtime_sec = np.mean(runtimes_sec)
    mean_runtime_min = mean_runtime_sec / 60

    # Extrapolate to 216 cases
    extrapolated_total_sec = mean_runtime_sec * 216
    extrapolated_total_min = extrapolated_total_sec / 60
    extrapolated_total_hours = extrapolated_total_min / 60

    # Overhead vs v0.1.20
    overhead_factor = (
        mean_runtime_min / V0120_MEAN_RUNTIME_PER_CASE if V0120_MEAN_RUNTIME_PER_CASE > 0 else None
    )

    return {
        "status": "SUCCESS",
        "n_cases_benchmarked": len(successful_cases),
        "mean_runtime_per_case_sec": mean_runtime_sec,
        "mean_runtime_per_case_min": mean_runtime_min,
        "extrapolated_216_cases_min": extrapolated_total_min,
        "extrapolated_216_cases_hours": extrapolated_total_hours,
        "overhead_factor_vs_v0120": overhead_factor,
        "v0120_reference_per_case_min": V0120_MEAN_RUNTIME_PER_CASE,
    }


def apply_decision_rules(extrapolation):
    """Apply decision rules from benchmark plan."""
    if extrapolation["status"] == "FAILED":
        return {
            "decision": "BENCHMARK_FAILED",
            "reason": extrapolation.get("reason", "Unknown failure"),
            "action": "Debug and rerun benchmark",
        }

    hours = extrapolation["extrapolated_216_cases_hours"]

    if hours < 18:
        return {
            "decision": "FULL_GRID_FEASIBLE",
            "reason": f"Extrapolated runtime {hours:.1f} hours < 18 hours",
            "action": "Execute full 216-case grid via --run-all (can run overnight unattended)",
        }
    elif hours < 36:
        return {
            "decision": "BATCHED_GRID_REQUIRED",
            "reason": f"Extrapolated runtime {hours:.1f} hours (18-36 hours range)",
            "action": "Execute 216 cases in 2-3 batches over multiple days",
        }
    elif hours < 72:
        return {
            "decision": "PILOT_REQUIRED_BEFORE_FULL_RERUN",
            "reason": f"Extrapolated runtime {hours:.1f} hours (36-72 hours range)",
            "action": "Run 72-case pilot first (1 family × full grid) to validate metric + overhead",
        }
    else:
        return {
            "decision": "GRID_REDUCTION_REQUIRED",
            "reason": f"Extrapolated runtime {hours:.1f} hours > 72 hours",
            "action": "Drop s1_size=128 from grid (reduces to 162 cases), document as deviation",
        }


def write_results(results, extrapolation, decision):
    """Write benchmark results to output directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Benchmark config
    config = {
        "benchmark_version": "v0.1.21",
        "timestamp": timestamp,
        "n_cases": len(BENCHMARK_CASES),
        "cases": [
            {k: v for k, v in case.items() if k not in ["purpose"]} for case in BENCHMARK_CASES
        ],
    }

    with open(OUTPUT_DIR / "benchmark_config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Per-case results
    for result in results:
        case_file = OUTPUT_DIR / f"{result['case_id']}.json"
        with open(case_file, "w") as f:
            json.dump(result, f, indent=2)

    # Aggregated results
    summary = {
        "benchmark_version": "v0.1.21",
        "timestamp": timestamp,
        "n_cases_total": len(results),
        "n_cases_successful": len([r for r in results if r["error"] is None]),
        "n_cases_failed": len([r for r in results if r["error"] is not None]),
        "per_case_results": results,
        "extrapolation": extrapolation,
        "decision": decision,
    }

    with open(OUTPUT_DIR / "benchmark_results.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✅ Results written to: {OUTPUT_DIR}")


def print_summary(results, extrapolation, decision):
    """Print human-readable summary."""
    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY — Gate 4B True IPR Runtime v0.1.21")
    print("=" * 80)

    print("\nCases executed:")
    for r in results:
        status = "✅ SUCCESS" if r["error"] is None else "❌ FAILED"
        runtime = f"{r['runtime_sec']:.2f} sec" if r["error"] is None else "N/A"
        print(f"  {r['label']:30s} {status:12s} {runtime:15s}")

    if extrapolation["status"] == "SUCCESS":
        print("\nExtrapolation to 216 cases:")
        print(f"  Mean runtime per case: {extrapolation['mean_runtime_per_case_min']:.2f} min")
        print(f"  Extrapolated total: {extrapolation['extrapolated_216_cases_hours']:.1f} hours")
        print(f"  Overhead vs v0.1.20: {extrapolation['overhead_factor_vs_v0120']:.1f}×")

    print("\n" + "-" * 80)
    print("DECISION:")
    print("-" * 80)
    print(f"  {decision['decision']}")
    print(f"  Reason: {decision['reason']}")
    print(f"  Action: {decision['action']}")
    print()

    print("=" * 80)
    print(f"Benchmark complete. Results: {OUTPUT_DIR}")
    print("=" * 80)


def main():
    """Run 3 benchmark cases and generate decision recommendation."""
    print("=" * 80)
    print("Gate 4B True IPR Runtime Benchmark — v0.1.21")
    print("=" * 80)
    print(f"Benchmark plan: reports/GATE4B_TRUE_IPR_RUNTIME_BENCHMARK_PLAN_v0.1.21.md")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"\nExecuting {len(BENCHMARK_CASES)} benchmark cases...\n")

    # Run all benchmark cases
    results = []
    for case in BENCHMARK_CASES:
        result = run_benchmark_case(case)
        results.append(result)

    # Compute extrapolation
    print("\n" + "=" * 80)
    print("Computing extrapolation to 216 cases...")
    print("=" * 80)
    extrapolation = compute_extrapolation(results)

    # Apply decision rules
    decision = apply_decision_rules(extrapolation)

    # Write results
    write_results(results, extrapolation, decision)

    # Print summary
    print_summary(results, extrapolation, decision)


if __name__ == "__main__":
    main()
