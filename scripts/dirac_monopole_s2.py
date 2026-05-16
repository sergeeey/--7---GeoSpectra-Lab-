from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.dirac_monopole_s2 import (
    MonopoleDiracConfig,
    all_controls_passed,
    evaluate_index_controls,
    format_cli_table,
    results_table,
    save_index_artifacts,
)


def append_issue_log(run_dir: Path) -> None:
    path = Path("reports") / "ISSUES_SCIENTIFIC.md"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## S2 Dirac monopole index control failure\n\n"
            "The finite-mode S2 monopole index control did not reproduce the expected index. "
            "Do not make chirality-related claims until this is understood. "
            f"Run directory: {run_dir}\n"
        )


def update_chirality_report(config: MonopoleDiracConfig, results: dict, run_dir: Path, mode: str) -> None:
    report = Path("reports") / "CHIRALITY_INDEX_REPORT.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    status = "passed" if all_controls_passed(results) else "failed"
    full_pending = "\nFull mode remains pending.\n" if mode == "quick" else "\nFull mode has been run for this report.\n"
    next_steps = (
        "1. Run full mode to test q = -3..3 across a larger cutoff set.\n"
        "2. Replace or complement this finite-mode control with a more geometric\n"
        "   discretization of the `S2` Dirac operator.\n"
        "3. Only after this index-control layer remains stable, investigate whether any\n"
        "   project-specific toy Dirac operators have protected zero modes."
        if mode == "quick"
        else "1. Replace or complement this finite-mode control with a more geometric\n"
        "   discretization of the `S2` Dirac operator.\n"
        "2. Only after this index-control layer remains stable, investigate whether any\n"
        "   project-specific toy Dirac operators have protected zero modes.\n"
        "3. Keep physical chirality claims blocked until a project-specific operator\n"
        "   passes an independent index test."
    )
    body = f"""# S² Dirac Monopole Index Test

## Purpose

This report records the first chirality-related control test in GeoSpectra Lab.
The goal is to verify that the code can reproduce a known index-theorem toy
result before any chirality-related claims are made elsewhere in the project.

## Mathematical Background

For a Dirac operator on `S2` coupled to a `U(1)` magnetic monopole of charge
`q`, the continuum index theorem predicts an index proportional to the monopole
charge. The convention implemented here is:

```text
q > 0 has positive-chirality zero modes
q < 0 has negative-chirality zero modes
Index(D) = n_plus - n_minus = q
```

## Numerical Implementation

This is a finite-mode spectral toy control, not a continuum lattice
discretization. It builds a chiral block operator `D = [[0, A^T], [A, 0]]`
with chirality operator `Gamma = diag(+1, -1)`. The nonzero finite-mode spectrum
is paired as `±lambda`, while `|q|` exact zero modes are assigned to the
chirality selected by the sign of `q`.

The nonzero toy levels use:

```text
lambda_n = sqrt(n * (n + |q|)) / R
degeneracy_n = 2n + |q|
n = 1, ..., cutoff
```

Zero-mode tolerance: `{config.zero_tolerance}`.

## q Values Tested

Mode: `{mode}`

```text
q_values = {config.q_values}
cutoffs = {config.cutoffs}
```

Run directory:

```text
{run_dir}
```

## Index Results

{results_table(results)}

Overall status: `{status}`.

## Convergence Behavior

The index is checked across the configured finite-mode cutoffs. Passing results
mean that increasing the cutoff did not destroy the index count under this toy
construction.

{full_pending}
## Limitations

- This is a finite-mode spectral toy model, not a geometric proof and not a
  full numerical discretization of spinor bundles on `S2`.
- Exact zero modes are built into the control using the known monopole spectral
  structure.
- This validates index-counting infrastructure and chirality bookkeeping only.
- It does not validate the Anderson model, spectral localization physics, or
  covariant compactification.

## What This Validates

- The code can count zero modes by chirality under an explicit convention.
- The numerical index `n_plus - n_minus` tracks monopole charge `q` in this
  known finite-mode toy control.
- The zero-mode tolerance and chirality threshold are documented and
  reproducible.

## What This Does NOT Validate

- It does not prove chiral fermions in covariant compactification.
- It does not bypass Witten/Lichnerowicz no-go theorems.
- It does not derive Standard Model fermions.
- It does not derive `SU(3) x SU(2) x U(1)`.
- It does not validate real cosmology or real extra-dimensional stabilization.

## Next Steps

{next_steps}
"""
    report.write_text(body, encoding="utf-8")


def run(args: argparse.Namespace) -> dict:
    if args.full:
        config = MonopoleDiracConfig(q_values=(-3, -2, -1, 0, 1, 2, 3), cutoffs=(1, 2, 3, 5))
        mode = "full"
    else:
        config = MonopoleDiracConfig(q_values=(0, 1, 2), cutoffs=(1, 2, 3))
        mode = "quick"
    run_dir = make_run_dir(f"dirac_monopole_s2_{mode}")
    results = evaluate_index_controls(config)
    save_index_artifacts(config=config, results=results, output_dir=run_dir)
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_chirality_report(config=config, results=results, run_dir=run_dir, mode=mode)
        if not all_controls_passed(results):
            append_issue_log(run_dir)
    print(format_cli_table(results))
    print(f"S2 Dirac monopole index {mode} run complete: {run_dir}")
    if not all_controls_passed(results):
        raise SystemExit(1)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="S2 Dirac monopole finite-mode index control.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="Small q/cutoff smoke index control.")
    mode.add_argument("--full", action="store_true", help="Full q=-3..3 convergence control.")
    args = parser.parse_args()
    if not args.quick and not args.full:
        args.quick = True
    return args


if __name__ == "__main__":
    run(parse_args())
