from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.anderson_windows import (
    AndersonWindowConfig,
    AndersonWindowDiagnosticsResult,
    all_points_table,
    assessments_table,
    final_size_window_table,
    run_anderson_window_diagnostics,
)


BASELINE = "v0.1.5-mvp-anderson3d-full-scaling"
HISTORICAL_NULL_RESULT = "W=0.5, <r>=0.2631"


def append_null_or_issue_logs(result: AndersonWindowDiagnosticsResult, run_dir: Path, mode: str) -> None:
    if result.all_windows_basic_checks_passed and not result.window_choice_changes_conclusion:
        return

    null_path = Path("reports") / "NULL_RESULTS.md"
    with null_path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## 3D Anderson spectrum-window diagnostic limitation\n\n"
            f"Run directory: {run_dir}\n\n"
            f"Mode: `{mode}`.\n\n"
            f"Summary: {result.summary_statement}\n\n"
            f"All windows basic checks passed: {result.all_windows_basic_checks_passed}.\n"
            f"Window choice changes conclusion: {result.window_choice_changes_conclusion}.\n\n"
            "This is a limitation of the current window-resolved Anderson benchmark, "
            "not evidence against the already validated r-statistics implementation. "
            f"The historical 1D quick null-result remains preserved: `{HISTORICAL_NULL_RESULT}`.\n"
        )

    issue_path = Path("reports") / "ISSUES_SCIENTIFIC.md"
    with issue_path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## 3D Anderson spectrum-window diagnostics need follow-up\n\n"
            f"Run directory: {run_dir}\n\n"
            "A window-dependent result should be diagnosed through eigenvalue solver checks, "
            "window-selection thresholds, degeneracy inspection, finite-size behavior, and "
            "open-vs-periodic boundary comparison before making stronger localization claims.\n"
        )


def update_spectral_report(result: AndersonWindowDiagnosticsResult, run_dir: Path, mode: str) -> None:
    report = Path("reports") / "SPECTRAL_REPORT.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Spectral Report\n"
    section = f"""
## Spectrum-Window Diagnostics

Mode: `{mode}`

Command:

```powershell
python scripts/anderson_3d_spectrum_windows.py --{mode}
```

Run directory:

```text
{run_dir}
```

Baseline context: `{BASELINE}`.

Final-size window results:

{final_size_window_table(result)}

Window assessments:

{assessments_table(result)}

Summary:

- {result.summary_statement}
- All windows basic checks passed: `{result.all_windows_basic_checks_passed}`.
- Window choice changes conclusion: `{result.window_choice_changes_conclusion}`.
- Historical null-result preserved: `{HISTORICAL_NULL_RESULT}`.

Saved artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/r_by_window.png`
- `{run_dir}/figures/ipr_by_window.png`
- `{run_dir}/figures/window_comparison_heatmap.png`

Interpretation:

Spectrum-window diagnostics test whether the 3D Anderson localization
diagnostic depends on the chosen spectral region. This strengthens benchmark
evidence only. It does not prove localization in a target compactification
model, chirality, covariant compactification, or Standard Model physics.
"""
    report.write_text(_replace_or_append_section(existing, "## Spectrum-Window Diagnostics", section), encoding="utf-8")


def update_validation_status(result: AndersonWindowDiagnosticsResult, run_dir: Path, mode: str) -> None:
    report = Path("reports") / "VALIDATION_STATUS.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Validation Status — GeoSpectra Lab\n"
    section = f"""
### Spectrum-Window Diagnostics

Latest verified run:

```text
{run_dir}
```

Mode: `{mode}`.

Status:

- All windows basic checks passed: `{result.all_windows_basic_checks_passed}`.
- Window choice changes conclusion: `{result.window_choice_changes_conclusion}`.
- Summary: {result.summary_statement}

Window assessments:

{assessments_table(result)}

Artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/r_by_window.png`
- `{run_dir}/figures/ipr_by_window.png`
- `{run_dir}/figures/window_comparison_heatmap.png`

Interpretation:

This validates a window-resolved benchmark diagnostic only. It does not prove
target-model localization, chirality, covariant compactification, or Standard
Model derivation. The historical 1D quick null-result remains preserved:
`{HISTORICAL_NULL_RESULT}`.
"""
    report.write_text(_insert_or_replace_before(existing, "## Null / Limiting Results", "### Spectrum-Window Diagnostics", section), encoding="utf-8")


def update_readme_command() -> None:
    readme = Path("README.md")
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    command = "python scripts/anderson_3d_spectrum_windows.py --quick"
    if command in text:
        return
    anchor = "python scripts/anderson_3d_benchmark.py --quick\n"
    if anchor in text:
        text = text.replace(anchor, anchor + f"{command}\n", 1)
    output_anchor = "- `reports/RUNS/<timestamp>_anderson_3d_benchmark_quick/`\n"
    if output_anchor in text:
        text = text.replace(
            output_anchor,
            output_anchor + "- `reports/RUNS/<timestamp>_anderson_3d_spectrum_windows_quick/`\n",
            1,
        )
    readme.write_text(text, encoding="utf-8")


def run(args: argparse.Namespace) -> AndersonWindowDiagnosticsResult:
    if args.full:
        config = AndersonWindowConfig(
            lattice_sizes=(5, 6, 7),
            disorder_values=(1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0, 24.0),
            realizations=5,
            seed=args.seed,
            periodic=args.periodic,
            windows=(
                "center",
                "lower",
                "upper",
                "quantile_0.1",
                "quantile_0.3",
                "quantile_0.5",
                "quantile_0.7",
                "quantile_0.9",
            ),
        )
        mode = "full"
    else:
        config = AndersonWindowConfig(
            lattice_sizes=(5, 6),
            disorder_values=(4.0, 8.0, 12.0, 16.0, 24.0),
            realizations=2,
            seed=args.seed,
            periodic=args.periodic,
            windows=("center", "lower", "upper"),
        )
        mode = "quick"

    run_dir = make_run_dir(f"anderson_3d_spectrum_windows_{mode}")
    result = run_anderson_window_diagnostics(config=config, output_dir=run_dir)
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_spectral_report(result=result, run_dir=run_dir, mode=mode)
        update_validation_status(result=result, run_dir=run_dir, mode=mode)
        update_readme_command()
        append_null_or_issue_logs(result=result, run_dir=run_dir, mode=mode)

    print(final_size_window_table(result))
    print()
    print(assessments_table(result))
    print(f"all_windows_basic_checks_passed={result.all_windows_basic_checks_passed}")
    print(f"window_choice_changes_conclusion={result.window_choice_changes_conclusion}")
    print(f"summary={result.summary_statement}")
    print(f"anderson_3d_spectrum_windows_{mode} complete: {run_dir}")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="3D Anderson spectrum-window diagnostics.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="Small spectrum-window diagnostic.")
    mode.add_argument("--full", action="store_true", help="Larger spectrum-window diagnostic.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--periodic", action="store_true", help="Use periodic boundary conditions.")
    args = parser.parse_args()
    if not args.quick and not args.full:
        args.quick = True
    return args


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
