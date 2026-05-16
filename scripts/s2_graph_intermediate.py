from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.s2_graph_intermediate import (
    S2GraphProductConfig,
    S2GraphProductResult,
    assessments_table,
    points_table,
    run_s2_graph_product_benchmark,
)


BASELINE = "v0.1.11-mvp-s2-graph-intermediate-quick"
HISTORICAL_NEGATIVE_CONTROL = "Toy Dirac localization/chirality: near-zero modes have zero numerical index."
POSITIVE_CONTROL = "S2 Dirac monopole finite-mode index control: index(D)=q."


def config_from_args(args: argparse.Namespace) -> tuple[str, S2GraphProductConfig]:
    if args.full:
        return (
            "full",
            S2GraphProductConfig(
                q_values=(-2, -1, 1, 2),
                graph_sizes=(8, 12, 16),
                disorder_values=(0.0, 1.0, 2.0, 4.0, 8.0),
                perturbation_values=(0.0, 1e-5, 1e-4),
                realizations=4,
                seed=args.seed,
            ),
        )
    return (
        "quick",
        S2GraphProductConfig(
            q_values=(1, 2),
            graph_sizes=(8, 12),
            disorder_values=(0.0, 2.0, 8.0),
            perturbation_values=(0.0, 1e-5),
            realizations=3,
            seed=args.seed,
        ),
    )


def update_reports(result: S2GraphProductResult, run_dir: Path, mode: str, baseline: str) -> None:
    update_spectral_report(result, run_dir, mode, baseline)
    update_validation_status(result, run_dir, mode, baseline)
    update_issue_log(result, run_dir)
    update_readme(result, run_dir, baseline)
    write_release_notes(result, run_dir, baseline)


def update_spectral_report(result: S2GraphProductResult, run_dir: Path, mode: str, baseline: str) -> None:
    path = Path("reports") / "SPECTRAL_REPORT.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Spectral Report\n"
    section = f"""
## S2 x Graph Intermediate Index-Localization Benchmark

Command:

```powershell
python scripts/s2_graph_intermediate.py --{mode}
```

Run directory:

```text
{run_dir}
```

Baseline: `{baseline}`.

Controls fixed for this benchmark:

- Negative control: {HISTORICAL_NEGATIVE_CONTROL}
- Positive control: {POSITIVE_CONTROL}

Points:

{points_table(result)}

Assessments:

{assessments_table(result)}

Summary:

- {result.summary_statement}
- All index checks passed: `{result.all_index_checks_passed}`.
- All anticommutators preserved: `{result.all_anticommutators_preserved}`.
- IPR growth observed: `{result.ipr_growth_observed}`.

Artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/index_vs_disorder.png`
- `{run_dir}/figures/zero_mode_ipr_vs_disorder.png`
- `{run_dir}/figures/perturbation_stability.png`
- `{run_dir}/figures/chirality_counts.png`

Interpretation:

This is a finite-mode `S2 monopole x graph` toy bridge. It combines a nonzero
index inherited from the verified S2 monopole control with a graph localization
selector. It is not a continuum `S2 x S1` proof and not a compactification
claim. It is a required intermediate control before any move toward `S6` or
`S3 x S6`.
"""
    path.write_text(_replace_or_append_section(existing, "## S2 x Graph Intermediate Index-Localization Benchmark", section), encoding="utf-8")


def update_validation_status(result: S2GraphProductResult, run_dir: Path, mode: str, baseline: str) -> None:
    path = Path("reports") / "VALIDATION_STATUS.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Validation Status - GeoSpectra Lab\n"
    existing = existing.replace("Current baseline: `v0.1.10-mvp-dirac-chirality-full`", f"Current baseline: `{baseline}`")
    section = f"""
### S2 x Graph Intermediate Index-Localization Benchmark

Latest run:

```text
{run_dir}
```

Mode: `{mode}`.

Status:

- Baseline: `{baseline}`.
- Negative control fixed: {HISTORICAL_NEGATIVE_CONTROL}
- Positive control preserved: {POSITIVE_CONTROL}
- All index checks passed: `{result.all_index_checks_passed}`.
- All anticommutators preserved: `{result.all_anticommutators_preserved}`.
- IPR growth observed: `{result.ipr_growth_observed}`.
- Summary: {result.summary_statement}

Assessments:

{assessments_table(result)}

Interpretation:

This is the first intermediate bridge that combines nonzero index and a graph
localization diagnostic in one toy setup. It remains a finite-mode control and
does not validate `S6`, `S3 x S6`, physical chirality, or covariant
compactification.
"""
    existing = _insert_or_replace_before(existing, "## Null / Limiting Results", "### S2 x Graph Intermediate Index-Localization Benchmark", section)
    path.write_text(existing, encoding="utf-8")


def update_issue_log(result: S2GraphProductResult, run_dir: Path) -> None:
    path = Path("reports") / "ISSUES_SCIENTIFIC.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Scientific Issues\n"
    section = f"""
## S2 x graph bridge is not yet a geometric compactification model

Run directory: `{run_dir}`

The benchmark combines the verified finite-mode `S2` monopole index control
with a graph-sector localization selector. This is useful as an intermediate
toy bridge, but it is not a continuum `S2 x S1` Dirac operator and not an
`S6` or `S3 x S6` compactification model.

Result summary:

- {result.summary_statement}

Interpretation constraints:

- The graph sector selects localized bases inside an index-carrying zero-mode
  sector.
- Index stability here comes from the rectangular chiral block inherited from
  the finite-mode monopole control.
- No physical chirality or Standard Model fermion claim is allowed.
- Move to `S6` or `S3 x S6` only after a less artificial geometric product
  discretization is tested.
"""
    path.write_text(_replace_or_append_section(existing, "## S2 x graph bridge is not yet a geometric compactification model", section), encoding="utf-8")


def update_readme(result: S2GraphProductResult, run_dir: Path, baseline: str) -> None:
    path = Path("README.md")
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace("## Current Baseline: v0.1.10-mvp-dirac-chirality-full", f"## Current Baseline: {baseline}")
    text = text.replace(
        "| Toy Dirac chirality/index diagnostic | configured diagnostic run; Gamma algebra passed and numerical index remains zero |",
        "| Toy Dirac chirality/index diagnostic | configured diagnostic run; Gamma algebra passed and numerical index remains zero |\n"
        "| S2 x graph intermediate bridge | quick run combines nonzero S2 monopole index with graph localization selector |",
    )
    command = "python scripts/s2_graph_intermediate.py --quick"
    if command not in text:
        anchor = "python scripts/dirac_chirality_diagnostic.py --full\n"
        text = text.replace(anchor, anchor + f"{command}\n", 1)
    section = f"""
## S2 x Graph Intermediate Bridge

This benchmark fixes the current controls:

- Negative control: toy Dirac localization/chirality has near-zero modes with
  zero numerical index.
- Positive control: finite-mode `S2` monopole index tracks `q`.

It then builds an intermediate finite-mode `S2 monopole x graph` toy model.
The index is inherited from the `S2` monopole sector, while the graph sector is
used as a localization selector inside the zero-mode sector.

Command:

```powershell
python scripts/s2_graph_intermediate.py --quick
```

Run:

```text
{run_dir}
```

Summary:

- `all_index_checks_passed={result.all_index_checks_passed}`
- `all_anticommutators_preserved={result.all_anticommutators_preserved}`
- `ipr_growth_observed={result.ipr_growth_observed}`
- Baseline: `{baseline}`

This is an intermediate toy control only. It is not `S6`, not `S3 x S6`, not a
physical compactification result, and not a Standard Model fermion derivation.
"""
    text = _replace_or_append_section(text, "## S2 x Graph Intermediate Bridge", section)
    path.write_text(text, encoding="utf-8")


def write_release_notes(result: S2GraphProductResult, run_dir: Path, baseline: str) -> None:
    path = Path("reports") / "RELEASE_NOTES_v0.1.11.md"
    body = f"""# Release Notes — {baseline}

## Summary

This release adds the first intermediate model between the existing controls
and future higher-dimensional compactification tests: a finite-mode
`S2 monopole x graph` toy benchmark.

## Control status

- Negative control: toy Dirac localization/chirality near-zero modes have zero
  numerical index.
- Positive control: finite-mode `S2` monopole index control remains the source
  of nonzero index.

## Verified command

```powershell
python scripts/s2_graph_intermediate.py --quick
```

Run directory:

```text
{run_dir}
```

## Verified flags

| Metric | Value |
| --- | --- |
| `all_index_checks_passed` | `{result.all_index_checks_passed}` |
| `all_anticommutators_preserved` | `{result.all_anticommutators_preserved}` |
| `ipr_growth_observed` | `{result.ipr_growth_observed}` |

## Scientific meaning

The benchmark combines nonzero index and graph-sector localization diagnostics
in a single finite toy setup. It supports the next-step strategy:

1. keep toy Dirac localization as negative control;
2. keep `S2` monopole as positive control;
3. use `S2 x graph` as the intermediate bridge;
4. only later move toward `S6` or `S3 x S6`.

## Scientific non-claims

This does not prove physical chirality, protected Standard Model fermions,
covariant compactification, `S6`, `S3 x S6`, or Witten/Lichnerowicz bypass.

## Next recommended action

Replace the graph selector with a less artificial geometric `S2 x S1` or
product-discretized Dirac operator and retest index stability plus localization.
"""
    path.write_text(body, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Intermediate S2 monopole x graph index-localization benchmark.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--full", action="store_true")
    parser.add_argument("--seed", type=int, default=11117)
    args = parser.parse_args()
    if not args.quick and not args.full:
        args.quick = True
    return args


def run(args: argparse.Namespace) -> S2GraphProductResult:
    mode, config = config_from_args(args)
    run_dir = make_run_dir(f"s2_graph_intermediate_{mode}")
    result = run_s2_graph_product_benchmark(config=config, output_dir=run_dir)
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_reports(result, run_dir, mode, BASELINE)
    print(points_table(result))
    print()
    print(assessments_table(result))
    print(f"all_index_checks_passed={result.all_index_checks_passed}")
    print(f"all_anticommutators_preserved={result.all_anticommutators_preserved}")
    print(f"ipr_growth_observed={result.ipr_growth_observed}")
    print(f"summary={result.summary_statement}")
    print(f"s2_graph_intermediate_{mode} complete: {run_dir}")
    if not result.all_index_checks_passed:
        raise SystemExit(1)
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
