from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.dirac_localization import (
    DiracLocalizationConfig,
    DiracLocalizationResult,
    assessments_table,
    final_size_table,
    run_dirac_localization_benchmark,
)


BASELINE = "v0.1.8-mvp-dirac-localization-full"
HISTORICAL_NULL_RESULT = "W=0.5, <r>=0.2631"


def config_from_args(args: argparse.Namespace) -> tuple[str, DiracLocalizationConfig]:
    if args.full:
        return (
            "full",
            DiracLocalizationConfig(
                sizes=(48, 64, 96),
                disorder_values=(0.0, 0.5, 1.0, 2.0, 4.0, 6.0, 8.0),
                modes=("clean", "random_mass", "gauge_phase", "geometric_weight"),
                realizations=8,
                seed=args.seed,
            ),
        )
    return (
        "quick",
        DiracLocalizationConfig(
            sizes=(32, 48),
            disorder_values=(0.0, 1.0, 2.0, 4.0, 8.0),
            modes=("clean", "random_mass", "gauge_phase", "geometric_weight"),
            realizations=3,
            seed=args.seed,
        ),
    )


def update_spectral_report(result: DiracLocalizationResult, run_dir: Path, mode: str) -> None:
    report = Path("reports") / "SPECTRAL_REPORT.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Spectral Report\n"
    section = f"""
## Toy Dirac/Geometric Localization Benchmark

Command:

```powershell
python scripts/dirac_localization_benchmark.py --{mode}
```

Run directory:

```text
{run_dir}
```

Baseline: `{BASELINE}`.

Final-size results:

{final_size_table(result)}

Mode assessments:

{assessments_table(result)}

Summary:

- {result.summary_statement}
- All `+-lambda` symmetry checks passed: `{result.all_symmetry_checks_passed}`.
- Any near-zero modes observed: `{result.any_near_zero_modes}`.
- Historical Anderson null-result preserved: `{HISTORICAL_NULL_RESULT}`.

Saved artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/dirac_spectrum.png`
- `{run_dir}/figures/dirac_ipr_vs_disorder.png`
- `{run_dir}/figures/dirac_r_statistics.png`
- `{run_dir}/figures/dirac_near_zero_count.png`

Interpretation:

This applies validated localization diagnostics to toy Dirac-like/geometric
operators. It does not prove physical chirality. Near-zero modes are numerical
signals only unless an index/chirality check is also implemented.
"""
    report.write_text(_replace_or_append_section(existing, "## Toy Dirac/Geometric Localization Benchmark", section), encoding="utf-8")


def update_validation_status(result: DiracLocalizationResult, run_dir: Path, mode: str) -> None:
    report = Path("reports") / "VALIDATION_STATUS.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Validation Status - GeoSpectra Lab\n"
    section = f"""
### Toy Dirac/Geometric Localization Benchmark

Latest run:

```text
{run_dir}
```

Mode: `{mode}`.

Status:

- Baseline: `{BASELINE}`.
- All `+-lambda` symmetry checks passed: `{result.all_symmetry_checks_passed}`.
- Any near-zero modes observed: `{result.any_near_zero_modes}`.
- Summary: {result.summary_statement}

Mode assessments:

{assessments_table(result)}

Artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/dirac_spectrum.png`
- `{run_dir}/figures/dirac_ipr_vs_disorder.png`
- `{run_dir}/figures/dirac_r_statistics.png`
- `{run_dir}/figures/dirac_near_zero_count.png`

Interpretation:

This is the first connection from calibrated localization diagnostics to toy
Dirac/geometric operators. It does not validate physical chirality, target-model
localization, covariant compactification, Witten/Lichnerowicz bypass, or
Standard Model fermions.
"""
    report.write_text(
        _insert_or_replace_before(existing, "## Null / Limiting Results", "### Toy Dirac/Geometric Localization Benchmark", section),
        encoding="utf-8",
    )


def update_issue_log(result: DiracLocalizationResult, run_dir: Path) -> None:
    issue_path = Path("reports") / "ISSUES_SCIENTIFIC.md"
    existing = issue_path.read_text(encoding="utf-8") if issue_path.exists() else "# Scientific Issues\n"
    section = f"""
## Toy Dirac Localization Interpretation Boundary

Run directory: `{run_dir}`

The toy Dirac/geometric localization benchmark reports r-statistics, IPR, and
near-zero counts for finite chiral block operators. Near-zero modes in this
benchmark are numerical signals only.

Interpretation constraints:

- Localization is not an index.
- Near-zero modes are not protected chiral zero modes.
- This benchmark does not prove Witten/Lichnerowicz bypass.
- This benchmark does not derive Standard Model fermions.

Summary: {result.summary_statement}
"""
    issue_path.write_text(_replace_or_append_section(existing, "## Toy Dirac Localization Interpretation Boundary", section), encoding="utf-8")


def update_null_log_if_needed(result: DiracLocalizationResult, run_dir: Path) -> None:
    if result.all_symmetry_checks_passed:
        return
    null_path = Path("reports") / "NULL_RESULTS.md"
    existing = null_path.read_text(encoding="utf-8") if null_path.exists() else "# Null Results\n"
    section = f"""
## Toy Dirac Localization Symmetry Failure

Run directory: `{run_dir}`

The benchmark failed the required `+-lambda` spectral symmetry check. Treat the
run as invalid until the finite chiral block construction is diagnosed.
"""
    null_path.write_text(_replace_or_append_section(existing, "## Toy Dirac Localization Symmetry Failure", section), encoding="utf-8")


def update_readme_command() -> None:
    readme = Path("README.md")
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    command = "python scripts/dirac_localization_benchmark.py --full"
    if command in text:
        return
    anchor = "python scripts/anderson_3d_periodic_followup.py\n"
    if anchor in text:
        text = text.replace(anchor, anchor + f"{command}\n", 1)
    readme.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Toy Dirac/geometric localization benchmark.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="Small benchmark for smoke validation.")
    mode.add_argument("--full", action="store_true", help="Larger configured benchmark.")
    parser.add_argument("--seed", type=int, default=7373)
    args = parser.parse_args()
    if not args.quick and not args.full:
        args.quick = True
    return args


def run(args: argparse.Namespace) -> DiracLocalizationResult:
    mode, config = config_from_args(args)
    run_dir = make_run_dir(f"dirac_localization_{mode}")
    result = run_dirac_localization_benchmark(config=config, output_dir=run_dir)
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_spectral_report(result, run_dir, mode)
        update_validation_status(result, run_dir, mode)
        update_issue_log(result, run_dir)
        update_null_log_if_needed(result, run_dir)
        update_readme_command()

    print(final_size_table(result))
    print()
    print(assessments_table(result))
    print(f"all_symmetry_checks_passed={result.all_symmetry_checks_passed}")
    print(f"any_near_zero_modes={result.any_near_zero_modes}")
    print(f"summary={result.summary_statement}")
    print(f"dirac_localization_{mode} complete: {run_dir}")
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
