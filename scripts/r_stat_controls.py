from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.random_matrix_controls import (
    ControlConfig,
    evaluate_controls,
    format_results_table,
)


def append_failure_log(results: dict, run_dir: Path) -> None:
    failed = [name for name, result in results.items() if not result.passed]
    if not failed:
        return
    path = Path("reports") / "NULL_RESULTS.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## Synthetic r-statistics control failure\n\n"
            f"Failed controls: {', '.join(failed)}. "
            "This means the statistic pipeline or finite-size settings need review before relying on Anderson localization results. "
            f"Run directory: {run_dir}\n"
        )


def update_spectral_report(results: dict, run_dir: Path) -> None:
    report = Path("reports") / "SPECTRAL_REPORT.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    passed = all(result.passed for result in results.values())
    body = f"""# Spectral Report

## Synthetic R-Statistics Controls

What was checked: synthetic spectra with known adjacent-gap ratio behavior.
This validates the `mean_adjacent_gap_ratio` statistic pipeline only; it is not
a physics result and does not say anything about chirality.

{format_results_table(results)}

Pipeline status: {'validated within finite-size tolerances' if passed else 'not validated; see NULL_RESULTS.md'}.

Run directory: `{run_dir}`

Limitations: estimates are finite-size and finite-realization approximations.
GUE is optional and should be treated as an additional control, not a required
physics benchmark.

## Anderson Quick Smoke Baseline

Previous quick Anderson smoke: weak disorder `W=0.5` produced `<r>=0.2631`,
which was not closer to GOE than to Poisson. This remains a null/limiting result
for that quick configuration and should not be hidden.

Interpretation limit: GOE/Poisson/GUE controls validate statistics, while
Anderson runs test a model. Neither proves chirality, protected zero modes, or
covariant compactification.
"""
    report.write_text(body, encoding="utf-8")


def run(args: argparse.Namespace) -> dict:
    if args.full:
        config = ControlConfig(matrix_size=360, realizations=60, seed=args.seed, include_gue=not args.no_gue)
        mode = "full"
    else:
        config = ControlConfig(matrix_size=180, realizations=18, seed=args.seed, include_gue=not args.no_gue)
        mode = "quick"
    run_dir = make_run_dir(f"r_stat_controls_{mode}")
    results = evaluate_controls(config, output_dir=run_dir)
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_spectral_report(results, run_dir)
        append_failure_log(results, run_dir)
    print(format_results_table(results))
    if not all(result.passed for result in results.values()):
        raise SystemExit(1)
    print(f"r-stat controls complete: {run_dir}")
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synthetic r-statistics controls.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="Small finite-size control run.")
    mode.add_argument("--full", action="store_true", help="Larger finite-size control run.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-gue", action="store_true", help="Skip optional GUE control.")
    args = parser.parse_args()
    if not args.quick and not args.full:
        args.quick = True
    return args


if __name__ == "__main__":
    run(parse_args())
