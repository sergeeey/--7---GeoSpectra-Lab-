from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import write_json, write_summary
from cc_toy_lab.spectral.anderson_3d import GOE_R, POISSON_R, build_anderson_3d_hamiltonian
from cc_toy_lab.spectral.metrics import inverse_participation_ratio, mean_adjacent_gap_ratio


@dataclass(frozen=True)
class AndersonWindowConfig:
    lattice_sizes: tuple[int, ...] = (5, 6)
    disorder_values: tuple[float, ...] = (4.0, 8.0, 12.0, 16.0, 24.0)
    realizations: int = 2
    seed: int = 42
    hopping: float = 1.0
    periodic: bool = False
    windows: tuple[str, ...] = ("center", "lower", "upper")
    window_fraction: float = 0.2
    quantile_fraction: float = 0.1
    min_levels: int = 8
    weak_reference_disorder: float = 4.0
    strong_reference_disorder: float = 24.0
    note: str = "3D Anderson spectrum-window diagnostic; localization diagnostic only"


@dataclass(frozen=True)
class AndersonWindowPoint:
    lattice_size: int
    sites: int
    disorder: float
    window_name: str
    window_definition: str
    mean_r: float
    stderr_r: float
    mean_ipr: float
    stderr_ipr: float
    n_levels_used: int
    min_levels_used: int
    realizations: int


@dataclass(frozen=True)
class AndersonWindowAssessment:
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
class AndersonWindowDiagnosticsResult:
    config: AndersonWindowConfig
    points: list[AndersonWindowPoint]
    assessments: list[AndersonWindowAssessment]
    final_lattice_size: int
    all_windows_basic_checks_passed: bool
    window_choice_changes_conclusion: bool
    summary_statement: str


def choose_window_indices(
    eigenvalues: np.ndarray,
    window_name: str,
    fraction: float = 0.2,
    quantile_fraction: float = 0.1,
    min_levels: int = 8,
) -> np.ndarray:
    """Return eigenvalue indices for a named spectral window.

    Indices are returned in ascending eigenvalue order. Window names are:
    center, lower, upper, or quantile_<q> with q in [0, 1].
    """
    values = np.asarray(eigenvalues, dtype=float)
    if values.ndim != 1 or values.size < 4:
        raise ValueError("eigenvalues must be a 1D array with at least 4 values")
    order = np.argsort(values)
    sorted_values = values[order]
    count_fraction = quantile_fraction if window_name.startswith("quantile_") else fraction
    count = _window_count(sorted_values.size, count_fraction, min_levels)

    if window_name == "center":
        positions = np.sort(np.argsort(np.abs(sorted_values))[:count])
    elif window_name == "lower":
        positions = np.arange(count)
    elif window_name == "upper":
        positions = np.arange(sorted_values.size - count, sorted_values.size)
    elif window_name.startswith("quantile_"):
        q = _parse_quantile(window_name)
        center = int(round(q * (sorted_values.size - 1)))
        start = center - count // 2
        start = max(0, min(start, sorted_values.size - count))
        positions = np.arange(start, start + count)
    else:
        raise ValueError(f"unknown spectral window: {window_name}")
    return order[positions]


def window_definition(window_name: str, config: AndersonWindowConfig) -> str:
    if window_name == "center":
        return f"{config.window_fraction:.3g} fraction with smallest abs(E)"
    if window_name == "lower":
        return f"lowest {config.window_fraction:.3g} eigenvalue fraction"
    if window_name == "upper":
        return f"highest {config.window_fraction:.3g} eigenvalue fraction"
    if window_name.startswith("quantile_"):
        q = _parse_quantile(window_name)
        return f"quantile window centered at q={q:.3g}, width fraction {config.quantile_fraction:.3g}"
    raise ValueError(f"unknown spectral window: {window_name}")


def analyze_anderson_windows_once(
    lattice_size: int,
    disorder: float,
    seed: int,
    windows: tuple[str, ...],
    hopping: float = 1.0,
    periodic: bool = False,
    window_fraction: float = 0.2,
    quantile_fraction: float = 0.1,
    min_levels: int = 8,
) -> dict[str, tuple[float, float, int]]:
    hamiltonian = build_anderson_3d_hamiltonian(
        lattice_size=lattice_size,
        disorder=disorder,
        hopping=hopping,
        seed=seed,
        periodic=periodic,
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
        ipr = inverse_participation_ratio(selected_vectors)
        output[window_name] = (float(r_value), float(np.mean(ipr)), int(indices.size))
    return output


def run_anderson_window_diagnostics(
    config: AndersonWindowConfig,
    output_dir: Path | None = None,
) -> AndersonWindowDiagnosticsResult:
    points: list[AndersonWindowPoint] = []
    for lattice_size in config.lattice_sizes:
        for w_index, disorder in enumerate(config.disorder_values):
            by_window: dict[str, dict[str, list[float]]] = {
                window: {"r": [], "ipr": [], "levels": []} for window in config.windows
            }
            for realization in range(config.realizations):
                run_seed = config.seed + 1_000_000 * lattice_size + 10_000 * w_index + realization
                once = analyze_anderson_windows_once(
                    lattice_size=int(lattice_size),
                    disorder=float(disorder),
                    seed=run_seed,
                    windows=config.windows,
                    hopping=config.hopping,
                    periodic=config.periodic,
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
                values = by_window[window_name]
                points.append(
                    _make_point(
                        lattice_size=int(lattice_size),
                        disorder=float(disorder),
                        window_name=window_name,
                        window_definition_text=window_definition(window_name, config),
                        r_values=values["r"],
                        ipr_values=values["ipr"],
                        levels_used=values["levels"],
                    )
                )

    final_lattice_size = max(config.lattice_sizes)
    assessments = _assess_windows(points, final_lattice_size, config)
    all_basic = all(assessment.basic_checks_passed for assessment in assessments)
    window_changes = _window_choice_changes_conclusion(assessments)
    summary_statement = _summary_statement(all_basic, window_changes)
    result = AndersonWindowDiagnosticsResult(
        config=config,
        points=points,
        assessments=assessments,
        final_lattice_size=int(final_lattice_size),
        all_windows_basic_checks_passed=all_basic,
        window_choice_changes_conclusion=window_changes,
        summary_statement=summary_statement,
    )
    if output_dir is not None:
        save_anderson_window_artifacts(result=result, output_dir=output_dir)
    return result


def save_anderson_window_artifacts(result: AndersonWindowDiagnosticsResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "config.json", asdict(result.config))
    write_json(output_dir / "metrics.json", _metrics_payload(result))
    _save_data_npz(result, output_dir / "data.npz")
    _save_r_by_window(result, figures_dir / "r_by_window.png")
    _save_ipr_by_window(result, figures_dir / "ipr_by_window.png")
    _save_window_heatmap(result, figures_dir / "window_comparison_heatmap.png")
    write_summary(output_dir / "summary.md", "3D Anderson Spectrum-Window Diagnostics", _summary_lines(result, output_dir))


def final_size_window_table(result: AndersonWindowDiagnosticsResult) -> str:
    rows = [
        point
        for point in result.points
        if point.lattice_size == result.final_lattice_size
    ]
    return _points_table(rows)


def assessments_table(result: AndersonWindowDiagnosticsResult) -> str:
    lines = [
        "| window | weak <r> | strong <r> | weak IPR | strong IPR | basic checks passed |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for assessment in result.assessments:
        lines.append(
            f"| {assessment.window_name} | {assessment.weak_reference_r:.4f} | "
            f"{assessment.strong_reference_r:.4f} | {assessment.weak_reference_ipr:.6g} | "
            f"{assessment.strong_reference_ipr:.6g} | {assessment.basic_checks_passed} |"
        )
    return "\n".join(lines)


def all_points_table(result: AndersonWindowDiagnosticsResult) -> str:
    return _points_table(result.points)


def _make_point(
    lattice_size: int,
    disorder: float,
    window_name: str,
    window_definition_text: str,
    r_values: list[float],
    ipr_values: list[float],
    levels_used: list[float],
) -> AndersonWindowPoint:
    if not r_values or not ipr_values:
        raise ValueError(f"no finite observations for L={lattice_size}, W={disorder}, window={window_name}")
    r_arr = np.asarray(r_values, dtype=float)
    ipr_arr = np.asarray(ipr_values, dtype=float)
    levels_arr = np.asarray(levels_used, dtype=float)
    return AndersonWindowPoint(
        lattice_size=lattice_size,
        sites=lattice_size**3,
        disorder=disorder,
        window_name=window_name,
        window_definition=window_definition_text,
        mean_r=float(np.mean(r_arr)),
        stderr_r=float(np.std(r_arr, ddof=1) / np.sqrt(r_arr.size)) if r_arr.size > 1 else 0.0,
        mean_ipr=float(np.mean(ipr_arr)),
        stderr_ipr=float(np.std(ipr_arr, ddof=1) / np.sqrt(ipr_arr.size)) if ipr_arr.size > 1 else 0.0,
        n_levels_used=int(round(float(np.mean(levels_arr)))),
        min_levels_used=int(np.min(levels_arr)),
        realizations=int(r_arr.size),
    )


def _assess_windows(
    points: list[AndersonWindowPoint],
    lattice_size: int,
    config: AndersonWindowConfig,
) -> list[AndersonWindowAssessment]:
    assessments: list[AndersonWindowAssessment] = []
    for window_name in config.windows:
        window_points = [
            point
            for point in points
            if point.lattice_size == lattice_size and point.window_name == window_name
        ]
        weak = _nearest_disorder_point(window_points, config.weak_reference_disorder)
        strong = _nearest_disorder_point(window_points, config.strong_reference_disorder)
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
            AndersonWindowAssessment(
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


def _window_choice_changes_conclusion(assessments: list[AndersonWindowAssessment]) -> bool:
    center = next((assessment for assessment in assessments if assessment.window_name == "center"), None)
    if center is None:
        return len({assessment.basic_checks_passed for assessment in assessments}) > 1
    return any(assessment.basic_checks_passed != center.basic_checks_passed for assessment in assessments)


def _summary_statement(all_basic: bool, window_changes: bool) -> str:
    if all_basic and not window_changes:
        return "Window choice did not change the basic localization diagnostic in this run."
    if window_changes:
        return "Window choice changed at least one basic localization diagnostic; treat this as a limitation."
    return "At least one spectrum window failed the basic localization diagnostic."


def _nearest_disorder_point(points: list[AndersonWindowPoint], disorder: float) -> AndersonWindowPoint:
    if not points:
        raise ValueError("cannot select nearest disorder point from an empty point list")
    return min(points, key=lambda point: abs(point.disorder - disorder))


def _window_count(size: int, fraction: float, min_levels: int) -> int:
    if not 0 < fraction <= 1:
        raise ValueError("window fraction must be in (0, 1]")
    return max(4, min(size, max(min_levels, int(round(size * fraction)))))


def _parse_quantile(window_name: str) -> float:
    try:
        q = float(window_name.removeprefix("quantile_"))
    except ValueError as exc:
        raise ValueError(f"invalid quantile window name: {window_name}") from exc
    if not 0.0 <= q <= 1.0:
        raise ValueError("quantile window must be in [0, 1]")
    return q


def _metrics_payload(result: AndersonWindowDiagnosticsResult) -> dict:
    return {
        "points": [asdict(point) for point in result.points],
        "assessments": [asdict(assessment) for assessment in result.assessments],
        "final_lattice_size": result.final_lattice_size,
        "all_windows_basic_checks_passed": result.all_windows_basic_checks_passed,
        "window_choice_changes_conclusion": result.window_choice_changes_conclusion,
        "summary_statement": result.summary_statement,
    }


def _save_data_npz(result: AndersonWindowDiagnosticsResult, path: Path) -> None:
    rows = result.points
    np.savez(
        path,
        lattice_size=np.asarray([point.lattice_size for point in rows], dtype=int),
        sites=np.asarray([point.sites for point in rows], dtype=int),
        disorder=np.asarray([point.disorder for point in rows], dtype=float),
        window_name=np.asarray([point.window_name for point in rows]),
        mean_r=np.asarray([point.mean_r for point in rows], dtype=float),
        stderr_r=np.asarray([point.stderr_r for point in rows], dtype=float),
        mean_ipr=np.asarray([point.mean_ipr for point in rows], dtype=float),
        stderr_ipr=np.asarray([point.stderr_ipr for point in rows], dtype=float),
        n_levels_used=np.asarray([point.n_levels_used for point in rows], dtype=int),
        min_levels_used=np.asarray([point.min_levels_used for point in rows], dtype=int),
        realizations=np.asarray([point.realizations for point in rows], dtype=int),
    )


def _save_r_by_window(result: AndersonWindowDiagnosticsResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for window_name in result.config.windows:
        points = _final_points_for_window(result, window_name)
        w = np.asarray([point.disorder for point in points], dtype=float)
        mean = np.asarray([point.mean_r for point in points], dtype=float)
        err = np.asarray([point.stderr_r for point in points], dtype=float)
        ax.errorbar(w, mean, yerr=err, marker="o", capsize=3, label=window_name)
    ax.axhline(GOE_R, color="black", linestyle="--", linewidth=1.0, label="GOE")
    ax.axhline(POISSON_R, color="black", linestyle=":", linewidth=1.0, label="Poisson")
    ax.set_xlabel("disorder W")
    ax.set_ylabel("mean adjacent-gap ratio <r>")
    ax.set_title(f"3D Anderson spectrum windows: r-statistics, L={result.final_lattice_size}")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_ipr_by_window(result: AndersonWindowDiagnosticsResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for window_name in result.config.windows:
        points = _final_points_for_window(result, window_name)
        w = np.asarray([point.disorder for point in points], dtype=float)
        mean = np.asarray([point.mean_ipr for point in points], dtype=float)
        err = np.asarray([point.stderr_ipr for point in points], dtype=float)
        ax.errorbar(w, mean, yerr=err, marker="s", capsize=3, label=window_name)
    ax.set_xlabel("disorder W")
    ax.set_ylabel("mean IPR")
    ax.set_yscale("log")
    ax.set_title(f"3D Anderson spectrum windows: IPR, L={result.final_lattice_size}")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_window_heatmap(result: AndersonWindowDiagnosticsResult, path: Path) -> None:
    windows = list(result.config.windows)
    disorders = list(result.config.disorder_values)
    matrix = np.full((len(windows), len(disorders)), np.nan, dtype=float)
    final_points = [point for point in result.points if point.lattice_size == result.final_lattice_size]
    for i, window_name in enumerate(windows):
        for j, disorder in enumerate(disorders):
            matches = [
                point
                for point in final_points
                if point.window_name == window_name and np.isclose(point.disorder, disorder)
            ]
            if matches:
                matrix[i, j] = matches[0].mean_r
    fig, ax = plt.subplots(figsize=(8, max(3.5, 0.45 * len(windows))), constrained_layout=True)
    image = ax.imshow(matrix, aspect="auto", cmap="viridis", vmin=POISSON_R, vmax=GOE_R)
    ax.set_xticks(np.arange(len(disorders)), [f"{w:g}" for w in disorders])
    ax.set_yticks(np.arange(len(windows)), windows)
    ax.set_xlabel("disorder W")
    ax.set_title(f"<r> by spectral window, L={result.final_lattice_size}")
    fig.colorbar(image, ax=ax, label="<r>")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _final_points_for_window(result: AndersonWindowDiagnosticsResult, window_name: str) -> list[AndersonWindowPoint]:
    points = [
        point
        for point in result.points
        if point.lattice_size == result.final_lattice_size and point.window_name == window_name
    ]
    return sorted(points, key=lambda point: point.disorder)


def _summary_lines(result: AndersonWindowDiagnosticsResult, output_dir: Path) -> list[str]:
    return [
        "3D Anderson spectrum-window diagnostics with dense eigensystems for small configured lattices.",
        "Open boundary conditions are used unless config.json says periodic=true.",
        "",
        "## Final-size Window Table",
        "",
        final_size_window_table(result),
        "",
        "## Window Assessments",
        "",
        assessments_table(result),
        "",
        f"Summary: {result.summary_statement}",
        f"All windows basic checks passed: {result.all_windows_basic_checks_passed}.",
        f"Window choice changes conclusion: {result.window_choice_changes_conclusion}.",
        "Interpretation: this is a benchmark diagnostic, not proof of localization in a target physical model.",
        "Non-claims: no chirality, no covariant compactification proof, no Standard Model derivation.",
        f"Run directory: {output_dir}",
    ]


def _points_table(points: list[AndersonWindowPoint]) -> str:
    lines = [
        "| L | W | window | <r> | stderr_r | mean IPR | stderr_ipr | levels | realizations |",
        "| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for point in sorted(points, key=lambda p: (p.lattice_size, p.disorder, p.window_name)):
        lines.append(
            f"| {point.lattice_size} | {point.disorder:.4g} | {point.window_name} | "
            f"{point.mean_r:.4f} | {point.stderr_r:.4f} | {point.mean_ipr:.6g} | "
            f"{point.stderr_ipr:.2g} | {point.n_levels_used} | {point.realizations} |"
        )
    return "\n".join(lines)
