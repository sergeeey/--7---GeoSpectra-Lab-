from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import make_run_dir, write_json, write_summary
from cc_toy_lab.spectral.anderson_3d import GOE_R, POISSON_R, build_anderson_3d_hamiltonian
from cc_toy_lab.spectral.anderson_windows import choose_window_indices
from cc_toy_lab.spectral.metrics import inverse_participation_ratio, mean_adjacent_gap_ratio


BASELINE = "v0.1.6-mvp-spectrum-window-quick"
HISTORICAL_NULL_RESULT = "W=0.5, <r>=0.2631"


@dataclass(frozen=True)
class BoundaryComparisonConfig:
    lattice_sizes: tuple[int, ...] = (5, 6, 7)
    disorder_values: tuple[float, ...] = (4.0, 8.0, 12.0, 16.0, 20.0, 24.0)
    windows: tuple[str, ...] = ("center", "quantile_0.5")
    boundary_modes: tuple[str, ...] = ("open", "periodic")
    realizations: int = 4
    seed: int = 5151
    hopping: float = 1.0
    window_fraction: float = 0.2
    quantile_fraction: float = 0.1
    min_levels: int = 8
    weak_reference_disorder: float = 4.0
    strong_reference_disorder: float = 24.0
    note: str = "3D Anderson open-vs-periodic boundary comparison; benchmark diagnostic only"


@dataclass(frozen=True)
class BoundaryPoint:
    boundary: str
    lattice_size: int
    sites: int
    disorder: float
    window_name: str
    mean_r: float
    stderr_r: float
    mean_ipr: float
    stderr_ipr: float
    n_levels_used: int
    realizations: int


@dataclass(frozen=True)
class BoundaryAssessment:
    boundary: str
    lattice_size: int
    window_name: str
    weak_reference_r: float
    strong_reference_r: float
    weak_reference_ipr: float
    strong_reference_ipr: float
    weak_closer_to_goe: bool
    strong_closer_to_poisson_than_weak: bool
    ipr_increases: bool
    basic_checks_passed: bool


@dataclass(frozen=True)
class BoundaryComparisonResult:
    config: BoundaryComparisonConfig
    points: list[BoundaryPoint]
    assessments: list[BoundaryAssessment]
    final_lattice_size: int
    all_boundary_basic_checks_passed: bool
    boundary_changes_basic_diagnostic: bool
    max_abs_delta_r: float
    max_abs_delta_ipr: float
    summary_statement: str


def analyze_boundary_once(
    lattice_size: int,
    disorder: float,
    seed: int,
    boundary: str,
    windows: tuple[str, ...],
    hopping: float = 1.0,
    window_fraction: float = 0.2,
    quantile_fraction: float = 0.1,
    min_levels: int = 8,
) -> dict[str, tuple[float, float, int]]:
    if boundary not in {"open", "periodic"}:
        raise ValueError("boundary must be 'open' or 'periodic'")
    hamiltonian = build_anderson_3d_hamiltonian(
        lattice_size=lattice_size,
        disorder=disorder,
        hopping=hopping,
        seed=seed,
        periodic=boundary == "periodic",
    )
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian.toarray())
    output: dict[str, tuple[float, float, int]] = {}
    for window_name in windows:
        indices = choose_window_indices(
            eigenvalues,
            window_name,
            fraction=window_fraction,
            quantile_fraction=quantile_fraction,
            min_levels=min_levels,
        )
        selected_values = eigenvalues[indices]
        selected_vectors = eigenvectors[:, indices]
        r_value = mean_adjacent_gap_ratio(selected_values)
        ipr_values = inverse_participation_ratio(selected_vectors)
        output[window_name] = (float(r_value), float(np.mean(ipr_values)), int(indices.size))
    return output


def run_boundary_comparison(
    config: BoundaryComparisonConfig,
    output_dir: Path | None = None,
) -> BoundaryComparisonResult:
    points: list[BoundaryPoint] = []
    for boundary_index, boundary in enumerate(config.boundary_modes):
        for lattice_size in config.lattice_sizes:
            for w_index, disorder in enumerate(config.disorder_values):
                by_window: dict[str, dict[str, list[float]]] = {
                    window: {"r": [], "ipr": [], "levels": []} for window in config.windows
                }
                for realization in range(config.realizations):
                    run_seed = (
                        config.seed
                        + 100_000_000 * boundary_index
                        + 1_000_000 * int(lattice_size)
                        + 10_000 * w_index
                        + realization
                    )
                    once = analyze_boundary_once(
                        lattice_size=int(lattice_size),
                        disorder=float(disorder),
                        seed=run_seed,
                        boundary=boundary,
                        windows=config.windows,
                        hopping=config.hopping,
                        window_fraction=config.window_fraction,
                        quantile_fraction=config.quantile_fraction,
                        min_levels=config.min_levels,
                    )
                    for window_name, (r_value, ipr_value, n_levels) in once.items():
                        if np.isfinite(r_value) and np.isfinite(ipr_value):
                            by_window[window_name]["r"].append(r_value)
                            by_window[window_name]["ipr"].append(ipr_value)
                            by_window[window_name]["levels"].append(float(n_levels))
                for window_name in config.windows:
                    points.append(
                        _make_point(
                            boundary=boundary,
                            lattice_size=int(lattice_size),
                            disorder=float(disorder),
                            window_name=window_name,
                            r_values=by_window[window_name]["r"],
                            ipr_values=by_window[window_name]["ipr"],
                            levels_used=by_window[window_name]["levels"],
                        )
                    )

    final_lattice_size = max(config.lattice_sizes)
    assessments = _assess_boundaries(points, final_lattice_size, config)
    all_basic = all(assessment.basic_checks_passed for assessment in assessments)
    boundary_changes = _boundary_changes_basic_diagnostic(assessments)
    max_delta_r, max_delta_ipr = _max_boundary_deltas(points, final_lattice_size, config)
    summary_statement = _summary_statement(all_basic, boundary_changes)
    result = BoundaryComparisonResult(
        config=config,
        points=points,
        assessments=assessments,
        final_lattice_size=int(final_lattice_size),
        all_boundary_basic_checks_passed=all_basic,
        boundary_changes_basic_diagnostic=boundary_changes,
        max_abs_delta_r=max_delta_r,
        max_abs_delta_ipr=max_delta_ipr,
        summary_statement=summary_statement,
    )
    if output_dir is not None:
        save_boundary_comparison_artifacts(result=result, output_dir=output_dir)
    return result


def save_boundary_comparison_artifacts(result: BoundaryComparisonResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "config.json", asdict(result.config))
    write_json(output_dir / "metrics.json", _metrics_payload(result))
    _save_data_npz(result, output_dir / "data.npz")
    _save_r_plot(result, figures_dir / "r_open_vs_periodic.png")
    _save_ipr_plot(result, figures_dir / "ipr_open_vs_periodic.png")
    _save_delta_heatmap(result, figures_dir / "boundary_delta_heatmap.png")
    write_summary(output_dir / "summary.md", "3D Anderson Boundary Comparison", _summary_lines(result, output_dir))


def final_boundary_table(result: BoundaryComparisonResult) -> str:
    rows = [point for point in result.points if point.lattice_size == result.final_lattice_size]
    return _points_table(rows)


def boundary_assessments_table(result: BoundaryComparisonResult) -> str:
    lines = [
        "| boundary | window | weak <r> | strong <r> | weak IPR | strong IPR | passed |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for assessment in sorted(result.assessments, key=lambda item: (item.boundary, item.window_name)):
        lines.append(
            f"| {assessment.boundary} | {assessment.window_name} | "
            f"{assessment.weak_reference_r:.4f} | {assessment.strong_reference_r:.4f} | "
            f"{assessment.weak_reference_ipr:.6g} | {assessment.strong_reference_ipr:.6g} | "
            f"{assessment.basic_checks_passed} |"
        )
    return "\n".join(lines)


def _make_point(
    boundary: str,
    lattice_size: int,
    disorder: float,
    window_name: str,
    r_values: list[float],
    ipr_values: list[float],
    levels_used: list[float],
) -> BoundaryPoint:
    if not r_values or not ipr_values:
        raise ValueError(f"no finite observations for {boundary}, L={lattice_size}, W={disorder}, {window_name}")
    r_arr = np.asarray(r_values, dtype=float)
    ipr_arr = np.asarray(ipr_values, dtype=float)
    levels_arr = np.asarray(levels_used, dtype=float)
    return BoundaryPoint(
        boundary=boundary,
        lattice_size=lattice_size,
        sites=lattice_size**3,
        disorder=disorder,
        window_name=window_name,
        mean_r=float(np.mean(r_arr)),
        stderr_r=float(np.std(r_arr, ddof=1) / np.sqrt(r_arr.size)) if r_arr.size > 1 else 0.0,
        mean_ipr=float(np.mean(ipr_arr)),
        stderr_ipr=float(np.std(ipr_arr, ddof=1) / np.sqrt(ipr_arr.size)) if ipr_arr.size > 1 else 0.0,
        n_levels_used=int(round(float(np.mean(levels_arr)))),
        realizations=int(r_arr.size),
    )


def _assess_boundaries(
    points: list[BoundaryPoint],
    lattice_size: int,
    config: BoundaryComparisonConfig,
) -> list[BoundaryAssessment]:
    assessments: list[BoundaryAssessment] = []
    for boundary in config.boundary_modes:
        for window_name in config.windows:
            subset = [
                point
                for point in points
                if point.lattice_size == lattice_size
                and point.boundary == boundary
                and point.window_name == window_name
            ]
            weak = _nearest_disorder_point(subset, config.weak_reference_disorder)
            strong = _nearest_disorder_point(subset, config.strong_reference_disorder)
            weak_goe_distance = abs(weak.mean_r - GOE_R)
            weak_poisson_distance = abs(weak.mean_r - POISSON_R)
            strong_goe_distance = abs(strong.mean_r - GOE_R)
            strong_poisson_distance = abs(strong.mean_r - POISSON_R)
            weak_closer_to_goe = weak_goe_distance < weak_poisson_distance
            strong_closer_to_poisson_than_weak = (
                strong_poisson_distance < weak_poisson_distance
                and strong_poisson_distance < strong_goe_distance
            )
            ipr_increases = strong.mean_ipr > weak.mean_ipr
            assessments.append(
                BoundaryAssessment(
                    boundary=boundary,
                    lattice_size=lattice_size,
                    window_name=window_name,
                    weak_reference_r=weak.mean_r,
                    strong_reference_r=strong.mean_r,
                    weak_reference_ipr=weak.mean_ipr,
                    strong_reference_ipr=strong.mean_ipr,
                    weak_closer_to_goe=weak_closer_to_goe,
                    strong_closer_to_poisson_than_weak=strong_closer_to_poisson_than_weak,
                    ipr_increases=ipr_increases,
                    basic_checks_passed=weak_closer_to_goe and strong_closer_to_poisson_than_weak and ipr_increases,
                )
            )
    return assessments


def _boundary_changes_basic_diagnostic(assessments: list[BoundaryAssessment]) -> bool:
    windows = sorted({assessment.window_name for assessment in assessments})
    for window_name in windows:
        values = {
            assessment.boundary: assessment.basic_checks_passed
            for assessment in assessments
            if assessment.window_name == window_name
        }
        if "open" in values and "periodic" in values and values["open"] != values["periodic"]:
            return True
    return False


def _max_boundary_deltas(
    points: list[BoundaryPoint],
    lattice_size: int,
    config: BoundaryComparisonConfig,
) -> tuple[float, float]:
    max_delta_r = 0.0
    max_delta_ipr = 0.0
    for disorder in config.disorder_values:
        for window_name in config.windows:
            open_point = _matching_point(points, lattice_size, "open", float(disorder), window_name)
            periodic_point = _matching_point(points, lattice_size, "periodic", float(disorder), window_name)
            if open_point is None or periodic_point is None:
                continue
            max_delta_r = max(max_delta_r, abs(periodic_point.mean_r - open_point.mean_r))
            max_delta_ipr = max(max_delta_ipr, abs(periodic_point.mean_ipr - open_point.mean_ipr))
    return float(max_delta_r), float(max_delta_ipr)


def _matching_point(
    points: list[BoundaryPoint],
    lattice_size: int,
    boundary: str,
    disorder: float,
    window_name: str,
) -> BoundaryPoint | None:
    for point in points:
        if (
            point.lattice_size == lattice_size
            and point.boundary == boundary
            and np.isclose(point.disorder, disorder)
            and point.window_name == window_name
        ):
            return point
    return None


def _nearest_disorder_point(points: list[BoundaryPoint], disorder: float) -> BoundaryPoint:
    if not points:
        raise ValueError("cannot select nearest disorder point from empty points")
    return min(points, key=lambda point: abs(point.disorder - disorder))


def _summary_statement(all_basic: bool, boundary_changes: bool) -> str:
    if all_basic and not boundary_changes:
        return "Open and periodic boundaries preserve the basic localization diagnostic in this run."
    if boundary_changes:
        return "Open and periodic boundaries disagree for at least one basic diagnostic; treat as a limitation."
    return "At least one boundary/window failed the basic localization diagnostic, but boundaries did not change the pass/fail pattern."


def _metrics_payload(result: BoundaryComparisonResult) -> dict:
    return {
        "points": [asdict(point) for point in result.points],
        "assessments": [asdict(assessment) for assessment in result.assessments],
        "final_lattice_size": result.final_lattice_size,
        "all_boundary_basic_checks_passed": result.all_boundary_basic_checks_passed,
        "boundary_changes_basic_diagnostic": result.boundary_changes_basic_diagnostic,
        "max_abs_delta_r": result.max_abs_delta_r,
        "max_abs_delta_ipr": result.max_abs_delta_ipr,
        "summary_statement": result.summary_statement,
        "pass_fail_criterion": (
            "A boundary/window passes when weak disorder is closer to GOE than Poisson, "
            "strong disorder is closer to Poisson than the weak reference and closer to "
            "Poisson than GOE, and IPR increases."
        ),
    }


def _save_data_npz(result: BoundaryComparisonResult, path: Path) -> None:
    rows = result.points
    np.savez(
        path,
        boundary=np.asarray([point.boundary for point in rows]),
        lattice_size=np.asarray([point.lattice_size for point in rows], dtype=int),
        sites=np.asarray([point.sites for point in rows], dtype=int),
        disorder=np.asarray([point.disorder for point in rows], dtype=float),
        window_name=np.asarray([point.window_name for point in rows]),
        mean_r=np.asarray([point.mean_r for point in rows], dtype=float),
        stderr_r=np.asarray([point.stderr_r for point in rows], dtype=float),
        mean_ipr=np.asarray([point.mean_ipr for point in rows], dtype=float),
        stderr_ipr=np.asarray([point.stderr_ipr for point in rows], dtype=float),
        n_levels_used=np.asarray([point.n_levels_used for point in rows], dtype=int),
        realizations=np.asarray([point.realizations for point in rows], dtype=int),
    )


def _save_r_plot(result: BoundaryComparisonResult, path: Path) -> None:
    fig, axes = plt.subplots(1, len(result.config.windows), figsize=(11, 4.6), constrained_layout=True, sharey=True)
    if len(result.config.windows) == 1:
        axes = [axes]
    for ax, window_name in zip(axes, result.config.windows):
        for boundary, marker in (("open", "o"), ("periodic", "s")):
            points = _final_points(result, boundary, window_name)
            ax.errorbar(
                [point.disorder for point in points],
                [point.mean_r for point in points],
                yerr=[point.stderr_r for point in points],
                marker=marker,
                capsize=3,
                label=boundary,
            )
        ax.axhline(GOE_R, color="black", linestyle="--", linewidth=1.0, label="GOE")
        ax.axhline(POISSON_R, color="black", linestyle=":", linewidth=1.0, label="Poisson")
        ax.set_title(window_name)
        ax.set_xlabel("disorder W")
        ax.set_ylabel("mean adjacent-gap ratio <r>")
        ax.legend(fontsize="small")
    fig.suptitle(f"Boundary comparison: r-statistics, L={result.final_lattice_size}")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_ipr_plot(result: BoundaryComparisonResult, path: Path) -> None:
    fig, axes = plt.subplots(1, len(result.config.windows), figsize=(11, 4.6), constrained_layout=True, sharey=True)
    if len(result.config.windows) == 1:
        axes = [axes]
    for ax, window_name in zip(axes, result.config.windows):
        for boundary, marker in (("open", "o"), ("periodic", "s")):
            points = _final_points(result, boundary, window_name)
            ax.errorbar(
                [point.disorder for point in points],
                [point.mean_ipr for point in points],
                yerr=[point.stderr_ipr for point in points],
                marker=marker,
                capsize=3,
                label=boundary,
            )
        ax.set_title(window_name)
        ax.set_xlabel("disorder W")
        ax.set_ylabel("mean IPR")
        ax.set_yscale("log")
        ax.legend(fontsize="small")
    fig.suptitle(f"Boundary comparison: IPR, L={result.final_lattice_size}")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_delta_heatmap(result: BoundaryComparisonResult, path: Path) -> None:
    windows = list(result.config.windows)
    disorders = list(result.config.disorder_values)
    matrix = np.full((len(windows), len(disorders)), np.nan, dtype=float)
    for i, window_name in enumerate(windows):
        for j, disorder in enumerate(disorders):
            open_point = _matching_point(result.points, result.final_lattice_size, "open", float(disorder), window_name)
            periodic_point = _matching_point(
                result.points,
                result.final_lattice_size,
                "periodic",
                float(disorder),
                window_name,
            )
            if open_point is not None and periodic_point is not None:
                matrix[i, j] = periodic_point.mean_r - open_point.mean_r
    limit = max(0.02, float(np.nanmax(np.abs(matrix))) if np.isfinite(matrix).any() else 0.02)
    fig, ax = plt.subplots(figsize=(8, max(3.5, 0.65 * len(windows))), constrained_layout=True)
    image = ax.imshow(matrix, aspect="auto", cmap="coolwarm", vmin=-limit, vmax=limit)
    ax.set_xticks(np.arange(len(disorders)), [f"{w:g}" for w in disorders])
    ax.set_yticks(np.arange(len(windows)), windows)
    ax.set_xlabel("disorder W")
    ax.set_title(f"Periodic minus open <r>, L={result.final_lattice_size}")
    fig.colorbar(image, ax=ax, label="delta <r>")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _final_points(result: BoundaryComparisonResult, boundary: str, window_name: str) -> list[BoundaryPoint]:
    return sorted(
        [
            point
            for point in result.points
            if point.lattice_size == result.final_lattice_size
            and point.boundary == boundary
            and point.window_name == window_name
        ],
        key=lambda point: point.disorder,
    )


def _points_table(points: list[BoundaryPoint]) -> str:
    lines = [
        "| boundary | L | W | window | <r> | stderr_r | mean IPR | stderr_ipr | levels | realizations |",
        "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for point in sorted(points, key=lambda p: (p.boundary, p.lattice_size, p.disorder, p.window_name)):
        lines.append(
            f"| {point.boundary} | {point.lattice_size} | {point.disorder:.4g} | {point.window_name} | "
            f"{point.mean_r:.4f} | {point.stderr_r:.4f} | {point.mean_ipr:.6g} | "
            f"{point.stderr_ipr:.2g} | {point.n_levels_used} | {point.realizations} |"
        )
    return "\n".join(lines)


def _summary_lines(result: BoundaryComparisonResult, output_dir: Path) -> list[str]:
    return [
        "3D Anderson open-vs-periodic boundary comparison.",
        "Model: cubic lattice, nearest-neighbor hopping, onsite box disorder.",
        "This run compares center and quantile_0.5 spectral windows at the final lattice size.",
        "",
        "## Final-Size Boundary Table",
        "",
        final_boundary_table(result),
        "",
        "## Boundary Assessments",
        "",
        boundary_assessments_table(result),
        "",
        f"Summary: {result.summary_statement}",
        f"All boundary basic checks passed: {result.all_boundary_basic_checks_passed}.",
        f"Boundary changes basic diagnostic: {result.boundary_changes_basic_diagnostic}.",
        f"Max |delta <r>| periodic-open: {result.max_abs_delta_r:.4f}.",
        f"Max |delta IPR| periodic-open: {result.max_abs_delta_ipr:.6g}.",
        f"Historical null-result preserved elsewhere: {HISTORICAL_NULL_RESULT}.",
        "Interpretation: benchmark stability only, not proof of target physical localization.",
        "Non-claims: no chirality, no covariant compactification proof, no Witten/Lichnerowicz bypass, no SM derivation.",
        f"Run directory: {output_dir}",
    ]


def append_null_or_issue_logs(result: BoundaryComparisonResult, run_dir: Path) -> None:
    if result.all_boundary_basic_checks_passed and not result.boundary_changes_basic_diagnostic:
        return
    null_path = Path("reports") / "NULL_RESULTS.md"
    with null_path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## 3D Anderson boundary-condition diagnostic limitation\n\n"
            f"Run directory: `{run_dir}`\n\n"
            f"Summary: {result.summary_statement}\n\n"
            f"All boundary basic checks passed: `{result.all_boundary_basic_checks_passed}`.\n"
            f"Boundary changes basic diagnostic: `{result.boundary_changes_basic_diagnostic}`.\n"
            f"Max |delta <r>| periodic-open: `{result.max_abs_delta_r:.4f}`.\n"
            f"Max |delta IPR| periodic-open: `{result.max_abs_delta_ipr:.6g}`.\n\n"
            "This is a limitation of the current Anderson boundary benchmark, not evidence "
            "against the already validated r-statistics implementation. The historical "
            f"1D quick null-result remains preserved: `{HISTORICAL_NULL_RESULT}`.\n"
        )

    issue_path = Path("reports") / "ISSUES_SCIENTIFIC.md"
    with issue_path.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n## 3D Anderson boundary comparison needs follow-up\n\n"
            f"Run directory: `{run_dir}`\n\n"
            "A boundary-sensitive result should be diagnosed through larger L, more seeds, "
            "spectrum-window refinement, eigenvalue-solver checks, and disorder-grid refinement "
            "before stronger localization statements are made.\n"
        )


def update_spectral_report(result: BoundaryComparisonResult, run_dir: Path) -> None:
    report = Path("reports") / "SPECTRAL_REPORT.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Spectral Report\n"
    section = f"""
## 3D Anderson Boundary Comparison

Command:

```powershell
python scripts/anderson_3d_boundary_comparison.py
```

Run directory:

```text
{run_dir}
```

Baseline context: `{BASELINE}`.

Final-size boundary results:

{final_boundary_table(result)}

Boundary assessments:

{boundary_assessments_table(result)}

Summary:

- {result.summary_statement}
- All boundary basic checks passed: `{result.all_boundary_basic_checks_passed}`.
- Boundary changes basic diagnostic: `{result.boundary_changes_basic_diagnostic}`.
- Max absolute periodic-open delta in `<r>`: `{result.max_abs_delta_r:.4f}`.
- Max absolute periodic-open delta in IPR: `{result.max_abs_delta_ipr:.6g}`.
- Historical null-result preserved: `{HISTORICAL_NULL_RESULT}`.

Saved artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/r_open_vs_periodic.png`
- `{run_dir}/figures/ipr_open_vs_periodic.png`
- `{run_dir}/figures/boundary_delta_heatmap.png`

Interpretation:

This compares whether the configured 3D Anderson localization diagnostic is
stable under open versus periodic boundary conditions. It is benchmark evidence
only. It does not prove localization in a target compactification model,
chirality, covariant compactification, Witten/Lichnerowicz bypass, or Standard
Model physics.
"""
    report.write_text(_replace_or_append_section(existing, "## 3D Anderson Boundary Comparison", section), encoding="utf-8")


def update_validation_status(result: BoundaryComparisonResult, run_dir: Path) -> None:
    report = Path("reports") / "VALIDATION_STATUS.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Validation Status - GeoSpectra Lab\n"
    section = f"""
### 3D Anderson Boundary Comparison

Latest run:

```text
{run_dir}
```

Command:

```powershell
python scripts/anderson_3d_boundary_comparison.py
```

Status:

- All boundary basic checks passed: `{result.all_boundary_basic_checks_passed}`.
- Boundary changes basic diagnostic: `{result.boundary_changes_basic_diagnostic}`.
- Summary: {result.summary_statement}
- Max absolute periodic-open delta in `<r>`: `{result.max_abs_delta_r:.4f}`.
- Max absolute periodic-open delta in IPR: `{result.max_abs_delta_ipr:.6g}`.

Boundary assessments:

{boundary_assessments_table(result)}

Artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/r_open_vs_periodic.png`
- `{run_dir}/figures/ipr_open_vs_periodic.png`
- `{run_dir}/figures/boundary_delta_heatmap.png`

Interpretation:

This is an open-vs-periodic benchmark stability check only. It does not prove
target-model localization, physical chirality, covariant compactification, or
Standard Model derivation. The historical 1D quick null-result remains
preserved: `{HISTORICAL_NULL_RESULT}`.
"""
    report.write_text(
        _insert_or_replace_before(existing, "## Null / Limiting Results", "### 3D Anderson Boundary Comparison", section),
        encoding="utf-8",
    )


def update_readme_command() -> None:
    readme = Path("README.md")
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    command = "python scripts/anderson_3d_boundary_comparison.py"
    if command in text:
        return
    anchor = "python scripts/anderson_3d_spectrum_windows.py --quick\n"
    if anchor in text:
        text = text.replace(anchor, anchor + f"{command}\n", 1)
    output_anchor = "- `reports/RUNS/<timestamp>_anderson_3d_spectrum_windows_quick/`\n"
    if output_anchor in text:
        text = text.replace(
            output_anchor,
            output_anchor + "- `reports/RUNS/<timestamp>_anderson_3d_boundary_comparison/`\n",
            1,
        )
    readme.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare open and periodic 3D Anderson boundary conditions.")
    parser.add_argument("--smoke", action="store_true", help="Tiny fast run for tests.")
    parser.add_argument("--seed", type=int, default=5151)
    parser.add_argument("--realizations", type=int, default=None)
    return parser.parse_args()


def config_from_args(args: argparse.Namespace) -> BoundaryComparisonConfig:
    if args.smoke:
        return BoundaryComparisonConfig(
            lattice_sizes=(4,),
            disorder_values=(4.0, 24.0),
            windows=("center", "quantile_0.5"),
            realizations=1,
            seed=args.seed,
            min_levels=8,
        )
    return BoundaryComparisonConfig(
        realizations=args.realizations if args.realizations is not None else 4,
        seed=args.seed,
    )


def run(args: argparse.Namespace) -> BoundaryComparisonResult:
    config = config_from_args(args)
    run_dir = make_run_dir("anderson_3d_boundary_comparison")
    result = run_boundary_comparison(config=config, output_dir=run_dir)
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_spectral_report(result=result, run_dir=run_dir)
        update_validation_status(result=result, run_dir=run_dir)
        update_readme_command()
        append_null_or_issue_logs(result=result, run_dir=run_dir)

    print(final_boundary_table(result))
    print()
    print(boundary_assessments_table(result))
    print(f"all_boundary_basic_checks_passed={result.all_boundary_basic_checks_passed}")
    print(f"boundary_changes_basic_diagnostic={result.boundary_changes_basic_diagnostic}")
    print(f"max_abs_delta_r={result.max_abs_delta_r:.4f}")
    print(f"max_abs_delta_ipr={result.max_abs_delta_ipr:.6g}")
    print(f"summary={result.summary_statement}")
    print(f"anderson_3d_boundary_comparison complete: {run_dir}")
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
