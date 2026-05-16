from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.anderson_3d import (
    GOE_R,
    POISSON_R,
    Anderson3DConfig,
    Anderson3DBenchmarkResult,
    final_size_summary,
    results_table,
    run_anderson_3d_benchmark,
)


def append_null_or_issue_logs(result: Anderson3DBenchmarkResult, run_dir: Path) -> None:
    if result.weak_closer_to_goe and result.quick_basic_checks_passed:
        return
    null_path = Path("reports") / "NULL_RESULTS.md"
    with null_path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## 3D Anderson quick benchmark limitation\n\n"
            f"Run directory: {run_dir}\n\n"
            f"Weak reference `<r>` = {result.weak_reference_r:.4f}. "
            f"GOE distance = {abs(result.weak_reference_r - GOE_R):.4f}; "
            f"Poisson distance = {abs(result.weak_reference_r - POISSON_R):.4f}. "
            f"Weak reference closer to GOE: {result.weak_closer_to_goe}.\n\n"
            f"Strong reference `<r>` = {result.strong_reference_r:.4f}. "
            f"Strong reference closer to Poisson than weak reference: "
            f"{result.strong_closer_to_poisson_than_weak}. "
            f"IPR increases: {result.ipr_increases}.\n\n"
            "Interpretation: this is a limitation of the current 3D quick benchmark design, "
            "not evidence against the already validated r-statistics implementation.\n"
        )
    issue_path = Path("reports") / "ISSUES_SCIENTIFIC.md"
    with issue_path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## 3D Anderson quick benchmark needs diagnosis\n\n"
            f"Run directory: {run_dir}\n\n"
            "If weak disorder is not GOE-like or strong disorder does not move toward Poisson, "
            "diagnose spectrum window, boundary conditions, lattice size, disorder range, "
            "eigenvalue solver, degeneracies, and finite-size treatment before making "
            "localization claims.\n"
        )


def update_spectral_report(result: Anderson3DBenchmarkResult, run_dir: Path, mode: str) -> None:
    report = Path("reports") / "SPECTRAL_REPORT.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    status = f"{mode} benchmark basic checks passed" if result.quick_basic_checks_passed else f"{mode} benchmark needs diagnosis"
    validation_scope = (
        "This full configured benchmark is stronger than quick mode, but still not a proof of localization "
        "in the target physical model."
        if mode == "full"
        else "This is still a quick benchmark."
    )
    body = f"""# Spectral Report

Baseline: `v0.1.5-mvp-anderson3d-full-scaling`

## Full Synthetic Control Validation

The r-statistics implementation has already been validated on synthetic
Poisson, GOE, and optional GUE ensembles in full mode.

| Ensemble | Expected <r> | Measured <r> | StdErr | Tolerance | Passed |
| --- | ---: | ---: | ---: | ---: | --- |
| POISSON | 0.3863 | 0.3817 | 0.0029 | 0.0350 | True |
| GOE | 0.5307 | 0.5309 | 0.0026 | 0.0400 | True |
| GUE | 0.5996 | 0.5960 | 0.0027 | 0.0450 | True |

Synthetic-control run: `reports/RUNS/20260511-224352_r_stat_controls_full`

## 3D Anderson Benchmark

Mode: `{mode}`

Model:

```text
H_ij = epsilon_i delta_ij + t * nearest_neighbor_terms
epsilon_i ~ Uniform[-W/2, W/2]
```

Boundary conditions: `{"periodic" if result.config.periodic else "open"}`.

Run directory:

```text
{run_dir}
```

Final-size {mode} results:

{final_size_summary(result)}

All size/results table:

{results_table(result)}

Basic benchmark status: `{status}`.

Checks:

- Weak reference closer to GOE than Poisson: `{result.weak_closer_to_goe}`.
- Strong reference closer to Poisson than the weak reference: `{result.strong_closer_to_poisson_than_weak}`.
- IPR increases from weak to strong disorder: `{result.ipr_increases}`.

Saved artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/anderson_3d_r_statistics.png`
- `{run_dir}/figures/anderson_3d_ipr.png`

Interpretation:

This benchmark is a stronger Anderson diagnostic than the previous 1D quick
smoke. {validation_scope} It does not prove chirality and does not validate
covariant compactification.

## Previous Anderson Quick Smoke Baseline

The earlier 1D quick Anderson smoke remains recorded:

```text
W=0.5, <r>=0.2631
```

That result is a limitation of the old quick setup, not evidence against the
r-statistics implementation.

## Next Spectral Validation Steps

1. Add spectrum-window diagnostics.
2. Compare open and periodic boundary conditions.
3. Increase lattice size, seed count, and W-grid resolution.
4. Keep localization claims separate from chirality claims.
"""
    report.write_text(body, encoding="utf-8")


def run(args: argparse.Namespace) -> Anderson3DBenchmarkResult:
    if args.full:
        config = Anderson3DConfig(
            lattice_sizes=(4, 5, 6, 7),
            disorder_values=(1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0),
            realizations=8,
            seed=args.seed,
            periodic=args.periodic,
            eigen_count=64,
        )
        mode = "full"
    else:
        config = Anderson3DConfig(
            lattice_sizes=(4, 5, 6),
            disorder_values=(1.0, 4.0, 8.0, 12.0, 16.0, 24.0),
            realizations=4,
            seed=args.seed,
            periodic=args.periodic,
            eigen_count=48,
        )
        mode = "quick"
    run_dir = make_run_dir(f"anderson_3d_benchmark_{mode}")
    result = run_anderson_3d_benchmark(config=config, output_dir=run_dir)
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_spectral_report(result=result, run_dir=run_dir, mode=mode)
        append_null_or_issue_logs(result=result, run_dir=run_dir)
    print(final_size_summary(result))
    print(f"basic_checks_passed={result.quick_basic_checks_passed}")
    print(f"anderson_3d_benchmark_{mode} complete: {run_dir}")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="3D cubic Anderson localization benchmark.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="Small 3D Anderson benchmark.")
    mode.add_argument("--full", action="store_true", help="Larger finite-size 3D Anderson benchmark.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--periodic", action="store_true", help="Use periodic boundary conditions.")
    args = parser.parse_args()
    if not args.quick and not args.full:
        args.quick = True
    return args


if __name__ == "__main__":
    run(parse_args())
