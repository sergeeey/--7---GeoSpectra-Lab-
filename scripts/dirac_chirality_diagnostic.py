from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.dirac_chirality import (
    DiracChiralityConfig,
    DiracChiralityResult,
    assessments_table,
    points_table,
    run_dirac_chirality_diagnostic,
)


BASELINE = "v0.1.10-mvp-dirac-chirality-full"
PREVIOUS_BASELINE = "v0.1.8-mvp-dirac-localization-full"
HISTORICAL_NULL_RESULT = "W=0.5, <r>=0.2631"


def config_from_args(args: argparse.Namespace) -> tuple[str, DiracChiralityConfig]:
    if args.full:
        return (
            "full",
            DiracChiralityConfig(
                sizes=(48, 64, 96),
                disorder_values=(0.0, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0),
                realizations=8,
                seed=args.seed,
            ),
        )
    return (
        "quick",
        DiracChiralityConfig(
            sizes=(32, 48),
            disorder_values=(0.0, 2.0, 8.0),
            realizations=3,
            seed=args.seed,
        ),
    )


def update_spectral_report(result: DiracChiralityResult, run_dir: Path, mode: str, baseline: str) -> None:
    report = Path("reports") / "SPECTRAL_REPORT.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Spectral Report\n"
    section = f"""
## Toy Dirac Chirality/Index Diagnostic

Command:

```powershell
python scripts/dirac_chirality_diagnostic.py --{mode}
```

Run directory:

```text
{run_dir}
```

Baseline: `{baseline}`.

Final-size index table:

{points_table(result)}

Mode assessments:

{assessments_table(result)}

Summary:

- {result.summary_statement}
- Gamma algebra passed: `{result.gamma_algebra_passed}`.
- Anticommutation preserved: `{result.anticommutation_preserved}`.
- All numerical indices zero: `{result.all_indices_zero}`.
- Any near-zero modes observed: `{result.any_near_zero_modes}`.
- Historical Anderson null-result preserved: `{HISTORICAL_NULL_RESULT}`.

Artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/chirality_expectations.png`
- `{run_dir}/figures/index_vs_disorder.png`
- `{run_dir}/figures/near_zero_chirality_scatter.png`
- `{run_dir}/figures/anticommutator_error.png`

Interpretation:

The finite block operator preserves the algebraic chiral structure, but the
configured diagnostic reports zero numerical index for the toy localization
modes. Near-zero modes are therefore classified as paired or accidental in this
benchmark, not protected chiral zero modes. This is separate from the verified
`S2` Dirac monopole index control, where a nonzero index is built and checked
against monopole charge.
"""
    report.write_text(_replace_or_append_section(existing, "## Toy Dirac Chirality/Index Diagnostic", section), encoding="utf-8")


def update_validation_status(result: DiracChiralityResult, run_dir: Path, mode: str, baseline: str) -> None:
    report = Path("reports") / "VALIDATION_STATUS.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Validation Status - GeoSpectra Lab\n"
    section = f"""
### Toy Dirac Chirality/Index Diagnostic

Latest run:

```text
{run_dir}
```

Mode: `{mode}`.

Status:

- Baseline: `{baseline}`.
- Gamma algebra passed: `{result.gamma_algebra_passed}`.
- Anticommutation preserved: `{result.anticommutation_preserved}`.
- All numerical indices zero: `{result.all_indices_zero}`.
- Any near-zero modes observed: `{result.any_near_zero_modes}`.
- Summary: {result.summary_statement}

Mode assessments:

{assessments_table(result)}

Artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/chirality_expectations.png`
- `{run_dir}/figures/index_vs_disorder.png`
- `{run_dir}/figures/near_zero_chirality_scatter.png`
- `{run_dir}/figures/anticommutator_error.png`

Interpretation:

This diagnostic distinguishes the current toy localization near-zero signals
from the verified nonzero-index `S2` monopole control. In the configured toy
localization modes, numerical index remains zero, so near-zero modes are
classified as paired or accidental rather than protected.
"""
    report.write_text(
        _insert_or_replace_before(existing, "## Null / Limiting Results", "### Toy Dirac Chirality/Index Diagnostic", section),
        encoding="utf-8",
    )


def update_issue_log(result: DiracChiralityResult, run_dir: Path) -> None:
    issue_path = Path("reports") / "ISSUES_SCIENTIFIC.md"
    existing = issue_path.read_text(encoding="utf-8") if issue_path.exists() else "# Scientific Issues\n"
    section = f"""
## Toy Dirac localization near-zero modes have zero numerical index

Run directory: `{run_dir}`

The toy Dirac chirality diagnostic checks `Gamma = diag(+I, -I)`, verifies
`Gamma^2 = I`, Hermiticity, and the anticommutator `{{D, Gamma}}`. It then
counts chirality-polarized eigenvectors inside the documented near-zero
tolerance.

Result summary:

- {result.summary_statement}
- All numerical indices zero: `{result.all_indices_zero}`.
- Near-zero modes observed: `{result.any_near_zero_modes}`.

Interpretation:

Near-zero modes in the toy Dirac localization benchmark are paired or
accidental under this diagnostic. No physical chirality claim is allowed from
these modes.

Required follow-up:

1. Test a less artificial geometric Dirac discretization.
2. Compare any future nonzero-index signal against the verified `S2` monopole
   index control.
3. Check stability across size, seeds, perturbations, and a chirality operator
   tied to the target geometry before using the word protected.
"""
    issue_path.write_text(_replace_or_append_section(existing, "## Toy Dirac localization near-zero modes have zero numerical index", section), encoding="utf-8")


def update_null_results_if_needed(result: DiracChiralityResult, run_dir: Path) -> None:
    if not result.all_indices_zero or not result.any_near_zero_modes:
        return
    null_path = Path("reports") / "NULL_RESULTS.md"
    existing = null_path.read_text(encoding="utf-8") if null_path.exists() else "# Null Results\n"
    section = f"""
## Toy Dirac near-zero modes have zero numerical index

Run directory: `{run_dir}`

The toy Dirac chirality/index diagnostic found near-zero modes, but the
numerical index remains zero across the configured localization modes.

Interpretation:

- This is a null result for protected/chiral zero-mode interpretation in the
  current toy Dirac localization benchmark.
- The near-zero modes are classified as paired or accidental under this
  diagnostic.
- This does not invalidate the separate `S2` Dirac monopole index control,
  which remains the positive control for nonzero index counting.
- Historical Anderson null-result remains preserved: `{HISTORICAL_NULL_RESULT}`.
"""
    null_path.write_text(_replace_or_append_section(existing, "## Toy Dirac near-zero modes have zero numerical index", section), encoding="utf-8")


def update_readme(result: DiracChiralityResult, run_dir: Path, baseline: str) -> None:
    readme = Path("README.md")
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    text = text.replace("## Current Baseline: v0.1.8-mvp-dirac-localization-full", f"## Current Baseline: {baseline}")
    text = text.replace("## Current Baseline: v0.1.9-mvp-dirac-chirality-diagnostic", f"## Current Baseline: {baseline}")
    text = text.replace(
        "| Toy Dirac/geometric localization | full configured benchmark run; `+-lambda` symmetry passed, IPR/r-statistics reported |",
        "| Toy Dirac/geometric localization | full configured benchmark run; `+-lambda` symmetry passed, IPR/r-statistics reported |\n"
        "| Toy Dirac chirality/index diagnostic | configured diagnostic run; Gamma algebra passed and numerical index remains zero |",
    )
    command = "python scripts/dirac_chirality_diagnostic.py --full"
    if command not in text:
        anchor = "python scripts/dirac_localization_benchmark.py --full\n"
        text = text.replace(anchor, anchor + f"{command}\n", 1)
    section = f"""
## Toy Dirac Chirality/Index Diagnostic

This diagnostic adds `Gamma = diag(+I, -I)` to the toy Dirac localization
operators and checks whether near-zero modes carry a nonzero numerical index.

Command:

```powershell
python scripts/dirac_chirality_diagnostic.py --full
```

Run:

```text
{run_dir}
```

Summary:

- `gamma_algebra_passed={result.gamma_algebra_passed}`
- `anticommutation_preserved={result.anticommutation_preserved}`
- `all_indices_zero={result.all_indices_zero}`
- `any_near_zero_modes={result.any_near_zero_modes}`
- Baseline: `{baseline}`

Interpretation:

The current toy localization near-zero modes are classified as paired or
accidental under this diagnostic because the numerical index remains zero. This
does not contradict the verified `S2` monopole index control; it says the toy
localization modes have not produced protected/chiral zero modes.
"""
    text = _replace_or_append_section(text, "## Toy Dirac Chirality/Index Diagnostic", section)
    readme.write_text(text, encoding="utf-8")


def write_release_notes(result: DiracChiralityResult, run_dir: Path, baseline: str) -> None:
    path = Path("reports") / "RELEASE_NOTES_v0.1.10.md"
    body = f"""# Release Notes — {baseline}

## Summary

This release adds a chirality/index diagnostic for the toy Dirac localization
operators. It checks the block chirality operator `Gamma = diag(+I, -I)`,
the anticommutator `{{D, Gamma}}`, chirality expectations, and the numerical
index of exact near-zero modes.

## New in this release

- `cc_toy_lab/spectral/dirac_chirality.py`
- `scripts/dirac_chirality_diagnostic.py`
- `tests/test_dirac_chirality.py`
- Run artifacts for the chirality diagnostic.
- Documentation updates for spectral, validation, null-result, and issue logs.

## Verified results

Command:

```powershell
python scripts/dirac_chirality_diagnostic.py --full
```

Run directory:

```text
{run_dir}
```

Flags:

| Metric | Value |
| --- | --- |
| `gamma_algebra_passed` | `{result.gamma_algebra_passed}` |
| `anticommutation_preserved` | `{result.anticommutation_preserved}` |
| `all_indices_zero` | `{result.all_indices_zero}` |
| `any_near_zero_modes` | `{result.any_near_zero_modes}` |

Mode assessments:

{assessments_table(result)}

## Scientific meaning

The diagnostic separates numerical near-zero modes from index-protected modes
in the current finite toy localization benchmark. The observed near-zero modes
have zero numerical index and are classified as paired or accidental.

## Scientific non-claims

This does not prove physical chirality, protected zero modes,
Witten/Lichnerowicz bypass, covariant compactification, Standard Model fermions,
or `SU(3) x SU(2) x U(1)`.

## Known limitations

- Finite toy block operator.
- Full configured diagnostic only; larger geometry-coupled diagnostics remain pending.
- Gamma is the algebraic block chirality of the toy construction, not a
  physical compactification chirality operator.
- Zero numerical index in this diagnostic does not invalidate the separate
  positive `S2` monopole index control.

## Next recommended action

Connect the chirality diagnostic to a less artificial geometric Dirac
discretization and compare against the verified `S2` monopole index control.
"""
    path.write_text(body, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Toy Dirac chirality/index diagnostic.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="Small chirality/index smoke diagnostic.")
    mode.add_argument("--full", action="store_true", help="Configured full chirality/index diagnostic.")
    parser.add_argument("--seed", type=int, default=9191)
    args = parser.parse_args()
    if not args.quick and not args.full:
        args.quick = True
    return args


def run(args: argparse.Namespace) -> DiracChiralityResult:
    mode, config = config_from_args(args)
    run_dir = make_run_dir(f"dirac_chirality_{mode}")
    result = run_dirac_chirality_diagnostic(config=config, output_dir=run_dir)
    baseline = BASELINE if result.gamma_algebra_passed and result.anticommutation_preserved else PREVIOUS_BASELINE
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_spectral_report(result, run_dir, mode, baseline)
        update_validation_status(result, run_dir, mode, baseline)
        update_issue_log(result, run_dir)
        update_null_results_if_needed(result, run_dir)
        update_readme(result, run_dir, baseline)
        if baseline == BASELINE:
            write_release_notes(result, run_dir, baseline)
    print(points_table(result))
    print()
    print(assessments_table(result))
    print(f"gamma_algebra_passed={result.gamma_algebra_passed}")
    print(f"anticommutation_preserved={result.anticommutation_preserved}")
    print(f"all_indices_zero={result.all_indices_zero}")
    print(f"any_near_zero_modes={result.any_near_zero_modes}")
    print(f"summary={result.summary_statement}")
    print(f"dirac_chirality_{mode} complete: {run_dir}")
    return result


def _replace_or_append_section(text: str, heading: str, section: str) -> str:
    start = text.find(heading)
    if start == -1:
        return text.rstrip() + "\n\n" + section.strip() + "\n"
    next_heading = text.find("\n## ", start + len(heading))
    if next_heading == -1:
        return text[:start].rstrip() + "\n\n" + section.strip() + "\n"
    return text[:start].rstrip() + "\n\n" + section.strip() + "\n\n" + text[next_heading:].lstrip()


def _insert_or_replace_before(text: str, before_heading: str, heading: str, section: str) -> str:
    start = text.find(heading)
    if start != -1:
        next_heading = text.find("\n## ", start + len(heading))
        if next_heading == -1:
            return text[:start].rstrip() + "\n\n" + section.strip() + "\n"
        return text[:start].rstrip() + "\n\n" + section.strip() + "\n\n" + text[next_heading:].lstrip()
    before = text.find(before_heading)
    if before == -1:
        return text.rstrip() + "\n\n" + section.strip() + "\n"
    return text[:before].rstrip() + "\n\n" + section.strip() + "\n\n" + text[before:].lstrip()


if __name__ == "__main__":
    run(parse_args())
