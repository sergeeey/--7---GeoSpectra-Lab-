"""Gate 4 Dry-Run — S³×S¹ Finite-Size Scaling Feasibility Check

⚠️ GUARDRAILS (read before execution):
- Purpose: Dry-run feasibility check ONLY (runtime estimate, failure detection)
- This is NOT valid for scientific verdict or Gate 4 evidence
- Do not use outputs as confirmatory data
- Do not interpret metrics or claim validation
- Protocol locked: commit 1f4173c (pre-registration)
- Dry-run plan: commit ef49495

Dry-run scope: 36 cases (3 families × 2 W × 3 sizes × 2 j_max × 1 seed)
Full grid: 216 cases (3 families × 3 W × 4 sizes × 2 j_max × 3 seeds)

Feasibility verdicts:
- FULL_GRID_FEASIBLE: <2h runtime, <5% failures
- BATCHED_GRID_REQUIRED: 2-8h runtime, <10% failures
- PROTOCOL_REVISION_REQUIRED: >8h runtime OR >10% failures
- DRY_RUN_FAILED: Critical errors prevent execution

Date: 2026-05-21
Status: FEASIBILITY-ONLY (pre-execution check)
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


# Gate 4 dry-run grid (exact 36-case specification)
DRY_RUN_GRID = {
    "families": ["spectral_circle", "ring", "wilson_ring"],  # S³×S¹ families
    "disorder_values": [0, 20],  # W=0 (clean), W=20 (disorder)
    "sizes": [16, 64, 128],  # S¹ lattice sizes (subset of full 16/64/128/256)
    "j_max_values": [2, 3],  # S³ spin truncation
    "seeds": [123],  # Single seed for dry-run
    "alpha": 0.0,  # S¹ flux (PBC)
    "mode": "geometric_weight",  # Disorder mode
    "radius": 1.0,  # Manifold radius
}

# Protocol commits
PROTOCOL_COMMIT = "1f4173c"
DRY_RUN_PLAN_COMMIT = "ef49495"


def generate_dry_run_cases():
    """Generate exact 36-case dry-run grid."""
    cases = []
    case_id = 0

    for family in DRY_RUN_GRID["families"]:
        for w in DRY_RUN_GRID["disorder_values"]:
            for size in DRY_RUN_GRID["sizes"]:
                for j_max in DRY_RUN_GRID["j_max_values"]:
                    for seed in DRY_RUN_GRID["seeds"]:
                        case = {
                            "id": case_id,
                            "family": family,
                            "disorder_strength": w,
                            "s1_size": size,
                            "j_max": j_max,
                            "seed": seed,
                            "alpha": DRY_RUN_GRID["alpha"],
                            "mode": DRY_RUN_GRID["mode"],
                            "radius": DRY_RUN_GRID["radius"],
                        }
                        cases.append(case)
                        case_id += 1

    return cases


def print_grid_plan():
    """Print dry-run grid without execution (--print-plan mode)."""
    cases = generate_dry_run_cases()

    print("=" * 80)
    print("Gate 4 Dry-Run Grid Plan")
    print("=" * 80)
    print()
    print(f"Total cases: {len(cases)}")
    print()
    print("Grid parameters:")
    print(f"  Families: {DRY_RUN_GRID['families']}")
    print(f"  Disorder W: {DRY_RUN_GRID['disorder_values']}")
    print(f"  S¹ sizes: {DRY_RUN_GRID['sizes']}")
    print(f"  j_max: {DRY_RUN_GRID['j_max_values']}")
    print(f"  Seeds: {DRY_RUN_GRID['seeds']}")
    print()
    print("Breakdown:")
    print(
        f"  {len(DRY_RUN_GRID['families'])} families × {len(DRY_RUN_GRID['disorder_values'])} W × "
        f"{len(DRY_RUN_GRID['sizes'])} sizes × {len(DRY_RUN_GRID['j_max_values'])} j_max × "
        f"{len(DRY_RUN_GRID['seeds'])} seed = {len(cases)} cases"
    )
    print()
    print("-" * 80)
    print("Sample cases (first 5):")
    print("-" * 80)
    for i, case in enumerate(cases[:5]):
        print(
            f"Case {case['id']:3d}: {case['family']:20s} W={case['disorder_strength']:2.0f} "
            f"N={case['s1_size']:3d} j_max={case['j_max']} seed={case['seed']}"
        )
    print("...")
    print()

    return len(cases)


def run_single_case(case):
    """Run single dry-run case and measure runtime."""
    start = time.time()
    error = None

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

        # Compute eigenvalues (Gate 4 requirement)
        eigvals = np.linalg.eigvalsh(H)

        # Extract metrics (minimal, for runtime measurement only)
        N = H.shape[0]
        low_eigvals = eigvals[: int(0.1 * N)]  # Bottom 10%
        mean_low_ipr = float(np.mean(low_eigvals))  # Placeholder metric

    except Exception as e:
        error = str(e)
        mean_low_ipr = None

    elapsed = time.time() - start

    result = {
        "case_id": case["id"],
        "family": case["family"],
        "disorder_strength": case["disorder_strength"],
        "s1_size": case["s1_size"],
        "j_max": case["j_max"],
        "seed": case["seed"],
        "runtime_sec": elapsed,
        "mean_low_ipr": mean_low_ipr,
        "error": error,
    }

    return result


def compute_feasibility_verdict(results, total_runtime):
    """Compute dry-run feasibility verdict."""
    n_total = len(results)
    n_failed = sum(1 for r in results if r["error"] is not None)
    failure_rate = n_failed / n_total if n_total > 0 else 1.0

    # Estimate full 216-case runtime (scale by 6x)
    full_grid_factor = 216 / 36
    estimated_full_runtime = total_runtime * full_grid_factor
    estimated_full_hours = estimated_full_runtime / 3600

    # Feasibility thresholds
    if n_failed >= n_total * 0.5:
        verdict = "DRY_RUN_FAILED"
        reason = f"Critical failure rate: {failure_rate*100:.1f}% ({n_failed}/{n_total})"
    elif estimated_full_hours > 8.0 or failure_rate > 0.10:
        verdict = "PROTOCOL_REVISION_REQUIRED"
        reason = f"Runtime {estimated_full_hours:.1f}h > 8h OR failure rate {failure_rate*100:.1f}% > 10%"
    elif estimated_full_hours > 2.0 or failure_rate > 0.05:
        verdict = "BATCHED_GRID_REQUIRED"
        reason = f"Runtime {estimated_full_hours:.1f}h requires batching OR {failure_rate*100:.1f}% failures"
    else:
        verdict = "FULL_GRID_FEASIBLE"
        reason = f"Runtime {estimated_full_hours:.1f}h < 2h, failures {failure_rate*100:.1f}% < 5%"

    return {
        "verdict": verdict,
        "reason": reason,
        "estimated_full_runtime_hours": estimated_full_hours,
        "failure_rate": failure_rate,
        "n_failed": n_failed,
        "n_total": n_total,
    }


def save_results(output_dir, results, total_runtime, feasibility):
    """Save dry-run results to output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # config.json
    config = {
        "purpose": "Gate 4 dry-run feasibility check",
        "protocol_commit": PROTOCOL_COMMIT,
        "dry_run_plan_commit": DRY_RUN_PLAN_COMMIT,
        "no_verdict": True,
        "full_gate4_execution": False,
        "grid": DRY_RUN_GRID,
        "n_cases": len(results),
    }
    with open(output_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)

    # timing.json
    timing_by_family = defaultdict(list)
    timing_by_size = defaultdict(list)

    for r in results:
        if r["error"] is None:
            timing_by_family[r["family"]].append(r["runtime_sec"])
            timing_by_size[r["s1_size"]].append(r["runtime_sec"])

    timing = {
        "total_runtime_sec": total_runtime,
        "per_case_mean_sec": total_runtime / len(results) if results else 0,
        "per_case_max_sec": max((r["runtime_sec"] for r in results), default=0),
        "by_family": {k: np.mean(v) for k, v in timing_by_family.items()},
        "by_size": {k: np.mean(v) for k, v in timing_by_size.items()},
        "estimated_full_216_runtime_sec": feasibility["estimated_full_runtime_hours"] * 3600,
        "failures": feasibility["n_failed"],
    }
    with open(output_dir / "timing.json", "w") as f:
        json.dump(timing, f, indent=2)

    # results.json (per-case results)
    with open(output_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    # summary.md
    summary_lines = [
        "# Gate 4 Dry-Run Summary",
        "",
        "## Purpose",
        "Dry-run feasibility check ONLY. Not valid for scientific verdict.",
        "",
        "## Execution",
        f"- Total cases: {len(results)}",
        f"- Completed: {len(results) - feasibility['n_failed']}",
        f"- Failed: {feasibility['n_failed']}",
        f"- Failure rate: {feasibility['failure_rate']*100:.1f}%",
        "",
        "## Runtime",
        f"- Dry-run total: {total_runtime/60:.1f} min",
        f"- Per-case mean: {timing['per_case_mean_sec']:.2f} sec",
        f"- Estimated full 216-case: {feasibility['estimated_full_runtime_hours']:.1f} hours",
        "",
        "## Feasibility Verdict",
        f"**{feasibility['verdict']}**",
        "",
        f"Reason: {feasibility['reason']}",
        "",
        "## Protocol References",
        f"- Pre-registration: commit {PROTOCOL_COMMIT}",
        f"- Dry-run plan: commit {DRY_RUN_PLAN_COMMIT}",
        "",
        "## Next Steps",
    ]

    if feasibility["verdict"] == "FULL_GRID_FEASIBLE":
        summary_lines.append("✅ Full 216-case grid can proceed as single execution.")
    elif feasibility["verdict"] == "BATCHED_GRID_REQUIRED":
        summary_lines.append("⚠️ Full grid requires batching (8 jobs × 27 cases).")
    elif feasibility["verdict"] == "PROTOCOL_REVISION_REQUIRED":
        summary_lines.append("🔴 Protocol revision required (reduce grid or optimize code).")
    else:
        summary_lines.append("🔴 Dry-run failed. Debug before proceeding.")

    with open(output_dir / "summary.md", "w") as f:
        f.write("\n".join(summary_lines))


def main():
    """Run Gate 4 dry-run feasibility check."""
    parser = argparse.ArgumentParser(description="Gate 4 Dry-Run Feasibility Check")
    parser.add_argument(
        "--print-plan", action="store_true", help="Print grid plan without execution"
    )
    args = parser.parse_args()

    if args.print_plan:
        n_cases = print_grid_plan()
        print(f"✅ Grid plan verified: {n_cases} cases")
        return

    # Execute dry-run
    print("=" * 80)
    print("Gate 4 Dry-Run — S³×S¹ Finite-Size Scaling Feasibility Check")
    print("=" * 80)
    print()
    print("⚠️ GUARDRAILS:")
    print("  - Purpose: Feasibility check ONLY (runtime estimate, failure detection)")
    print("  - NOT valid for scientific verdict or Gate 4 evidence")
    print("  - Do not interpret metrics or claim validation")
    print()
    print(f"Protocol: commit {PROTOCOL_COMMIT}")
    print(f"Dry-run plan: commit {DRY_RUN_PLAN_COMMIT}")
    print()

    output_dir = Path("reports/RUNS/gate4_dry_run_v0.1.20")
    cases = generate_dry_run_cases()

    print(f"Grid: {len(cases)} cases")
    print(f"Output: {output_dir}")
    print()
    print("-" * 80)

    start_total = time.time()
    results = []

    for i, case in enumerate(cases):
        print(
            f"[{i+1}/{len(cases)}] {case['family']:20s} W={case['disorder_strength']:2.0f} "
            f"N={case['s1_size']:3d} j_max={case['j_max']} ... ",
            end="",
            flush=True,
        )

        result = run_single_case(case)
        results.append(result)

        if result["error"] is None:
            print(f"✅ {result['runtime_sec']:.2f}s")
        else:
            print(f"❌ FAILED: {result['error'][:50]}")

    total_runtime = time.time() - start_total

    print("-" * 80)
    print()
    print(f"✅ Dry-run complete: {len(cases)} cases in {total_runtime/60:.1f} min")
    print()

    # Compute feasibility verdict
    feasibility = compute_feasibility_verdict(results, total_runtime)

    print("=" * 80)
    print("Feasibility Verdict")
    print("=" * 80)
    print()
    print(f"**{feasibility['verdict']}**")
    print()
    print(f"Reason: {feasibility['reason']}")
    print()
    print(
        f"Estimated full 216-case runtime: {feasibility['estimated_full_runtime_hours']:.1f} hours"
    )
    print(
        f"Failure rate: {feasibility['failure_rate']*100:.1f}% ({feasibility['n_failed']}/{feasibility['n_total']})"
    )
    print()

    # Save results
    save_results(output_dir, results, total_runtime, feasibility)

    print(f"Results saved: {output_dir}/")
    print()
    print("Next: Review timing.json and summary.md before full Gate 4 execution")
    print()


if __name__ == "__main__":
    main()
