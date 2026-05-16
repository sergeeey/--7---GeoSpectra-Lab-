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
BOUNDARY_COMPARISON_RUN = "reports/RUNS/20260512-093014_anderson_3d_boundary_comparison"
HISTORICAL_NULL_RESULT = "W=0.5, <r>=0.2631"


@dataclass(frozen=True)
class PeriodicFollowupConfig:
    lattice_sizes: tuple[int, ...] = (6, 7, 8)
    disorder_values: tuple[float, ...] = (16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0)
    windows: tuple[str, ...] = ("center", "quantile_0.5")
    realizations: int = 10
    seed: int = 6262
    hopping: float = 1.0
    window_fraction: float = 0.2
    quantile_fraction: float = 0.1
    min_levels: int = 8
    strong_poisson_disorder: float = 32.0
    reference_disorder: float = 24.0
    include_open_reference: bool = True
    open_reference_lattice_size: int | None = 8
    open_reference_realizations: int = 6
    note: str = "Targeted periodic-boundary follow-up for 3D Anderson benchmark; diagnostic only"


@dataclass(frozen=True)
class PeriodicPoint:
    boundary: str
    lattice_size: int
    sites: int
    disorder: float
    window_name: str
    mean_r: float
    stderr_r: float
    mean_ipr: float
    stderr_ipr: float
    distance_to_goe: float
    distance_to_poisson: float
    closer_to_poisson: bool
    strong_disorder_check_passed: bool | None
    n_levels_used: int
    realizations: int


@dataclass(frozen=True)
class PeriodicAssessment:
    lattice_size: int
    window_name: str
    reference_r_w24: float
    reference_ipr_w24: float
    w32_r: float
    w32_ipr: float
    max_w: float
    max_w_r: float
    max_w_ipr: float
    w24_closer_to_poisson: bool
    w32_closer_to_poisson: bool
    max_w_closer_to_poisson: bool
    all_w_ge_32_closer_to_poisson: bool
    any_w_ge_32_closer_to_poisson: bool
    ipr_mostly_monotonic: bool
    distance_to_poisson_improves: bool
    failure_resolved_by_stronger_disorder: bool


@dataclass(frozen=True)
class DegeneracyDiagnostic:
    lattice_size: int
    clean_periodic_degeneracy_fraction: float
    clean_open_degeneracy_fraction: float
    tolerance: float


@dataclass(frozen=True)
class PeriodicFollowupResult:
    config: PeriodicFollowupConfig
    points: list[PeriodicPoint]
    assessments: list[PeriodicAssessment]
    final_lattice_size: int
    degeneracy_diagnostic: DegeneracyDiagnostic
    stronger_disorder_makes_periodic_poisson_like: bool
    ipr_mostly_monotonic_all: bool
    spectrum_window_artifact_suspected: bool
    classification: str
    summary_statement: str


def analyze_once(
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
    if boundary not in {"periodic", "open"}:
        raise ValueError("boundary must be 'periodic' or 'open'")
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


def run_periodic_followup(
    config: PeriodicFollowupConfig,
    output_dir: Path | None = None,
) -> PeriodicFollowupResult:
    points = _run_periodic_points(config)
    if config.include_open_reference:
        points.extend(_run_open_reference_points(config))

    final_lattice_size = max(config.lattice_sizes)
    assessments = _assess_periodic(points, final_lattice_size, config)
    degeneracy = _clean_degeneracy_diagnostic(final_lattice_size)
    stronger_poisson = all(assessment.all_w_ge_32_closer_to_poisson for assessment in assessments)
    ipr_mostly_monotonic_all = all(assessment.ipr_mostly_monotonic for assessment in assessments)
    spectrum_window_artifact = _spectrum_window_artifact_suspected(assessments)
    classification = _classify_periodic_failure(assessments, degeneracy, spectrum_window_artifact)
    summary = _summary_statement(stronger_poisson, ipr_mostly_monotonic_all, spectrum_window_artifact, classification)
    result = PeriodicFollowupResult(
        config=config,
        points=points,
        assessments=assessments,
        final_lattice_size=final_lattice_size,
        degeneracy_diagnostic=degeneracy,
        stronger_disorder_makes_periodic_poisson_like=stronger_poisson,
        ipr_mostly_monotonic_all=ipr_mostly_monotonic_all,
        spectrum_window_artifact_suspected=spectrum_window_artifact,
        classification=classification,
        summary_statement=summary,
    )
    if output_dir is not None:
        save_periodic_followup_artifacts(result, output_dir)
    return result


def save_periodic_followup_artifacts(result: PeriodicFollowupResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "config.json", asdict(result.config))
    write_json(output_dir / "metrics.json", _metrics_payload(result))
    _save_data_npz(result, output_dir / "data.npz")
    _save_periodic_r_plot(result, figures_dir / "periodic_r_vs_w.png")
    _save_periodic_ipr_plot(result, figures_dir / "periodic_ipr_vs_w.png")
    _save_distance_plot(result, figures_dir / "periodic_distance_to_poisson_goe.png")
    _save_open_comparison_plot(result, figures_dir / "periodic_open_comparison_optional.png")
    write_summary(output_dir / "summary.md", "3D Anderson Periodic-Boundary Follow-Up", _summary_lines(result, output_dir))


def final_periodic_table(result: PeriodicFollowupResult) -> str:
    rows = [
        point
        for point in result.points
        if point.boundary == "periodic" and point.lattice_size == result.final_lattice_size
    ]
    return _points_table(rows)


def assessments_table(result: PeriodicFollowupResult) -> str:
    lines = [
        "| L | window | W24 <r> | W32 <r> | max W | max W <r> | W>=32 all Poisson-like | IPR mostly monotonic | resolved |",
        "| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for assessment in sorted(result.assessments, key=lambda item: (item.lattice_size, item.window_name)):
        lines.append(
            f"| {assessment.lattice_size} | {assessment.window_name} | "
            f"{assessment.reference_r_w24:.4f} | {assessment.w32_r:.4f} | "
            f"{assessment.max_w:.4g} | {assessment.max_w_r:.4f} | "
            f"{assessment.all_w_ge_32_closer_to_poisson} | {assessment.ipr_mostly_monotonic} | "
            f"{assessment.failure_resolved_by_stronger_disorder} |"
        )
    return "\n".join(lines)


def _run_periodic_points(config: PeriodicFollowupConfig) -> list[PeriodicPoint]:
    points: list[PeriodicPoint] = []
    for lattice_size in config.lattice_sizes:
        points.extend(
            _run_boundary_points(
                boundary="periodic",
                lattice_size=int(lattice_size),
                disorder_values=config.disorder_values,
                windows=config.windows,
                realizations=config.realizations,
                seed_base=config.seed,
                config=config,
                boundary_offset=0,
            )
        )
    return points


def _run_open_reference_points(config: PeriodicFollowupConfig) -> list[PeriodicPoint]:
    lattice_size = config.open_reference_lattice_size or max(config.lattice_sizes)
    realizations = min(config.open_reference_realizations, config.realizations)
    return _run_boundary_points(
        boundary="open",
        lattice_size=int(lattice_size),
        disorder_values=config.disorder_values,
        windows=config.windows,
        realizations=realizations,
        seed_base=config.seed,
        config=config,
        boundary_offset=100_000_000,
    )


def _run_boundary_points(
    boundary: str,
    lattice_size: int,
    disorder_values: tuple[float, ...],
    windows: tuple[str, ...],
    realizations: int,
    seed_base: int,
    config: PeriodicFollowupConfig,
    boundary_offset: int,
) -> list[PeriodicPoint]:
    points: list[PeriodicPoint] = []
    for w_index, disorder in enumerate(disorder_values):
        by_window: dict[str, dict[str, list[float]]] = {
            window: {"r": [], "ipr": [], "levels": []} for window in windows
        }
        for realization in range(realizations):
            run_seed = seed_base + boundary_offset + 1_000_000 * lattice_size + 10_000 * w_index + realization
            once = analyze_once(
                lattice_size=lattice_size,
                disorder=float(disorder),
                seed=run_seed,
                boundary=boundary,
                windows=windows,
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
        for window_name in windows:
            points.append(
                _make_point(
                    boundary=boundary,
                    lattice_size=lattice_size,
                    disorder=float(disorder),
                    window_name=window_name,
                    r_values=by_window[window_name]["r"],
                    ipr_values=by_window[window_name]["ipr"],
                    levels_used=by_window[window_name]["levels"],
                    strong_poisson_disorder=config.strong_poisson_disorder,
                )
            )
    return points


def _make_point(
    boundary: str,
    lattice_size: int,
    disorder: float,
    window_name: str,
    r_values: list[float],
    ipr_values: list[float],
    levels_used: list[float],
    strong_poisson_disorder: float,
) -> PeriodicPoint:
    if not r_values or not ipr_values:
        raise ValueError(f"no finite observations for {boundary}, L={lattice_size}, W={disorder}, {window_name}")
    r_arr = np.asarray(r_values, dtype=float)
    ipr_arr = np.asarray(ipr_values, dtype=float)
    levels_arr = np.asarray(levels_used, dtype=float)
    mean_r = float(np.mean(r_arr))
    closer_to_poisson = abs(mean_r - POISSON_R) < abs(mean_r - GOE_R)
    strong_check = bool(closer_to_poisson) if disorder >= strong_poisson_disorder else None
    return PeriodicPoint(
        boundary=boundary,
        lattice_size=lattice_size,
        sites=lattice_size**3,
        disorder=disorder,
        window_name=window_name,
        mean_r=mean_r,
        stderr_r=float(np.std(r_arr, ddof=1) / np.sqrt(r_arr.size)) if r_arr.size > 1 else 0.0,
        mean_ipr=float(np.mean(ipr_arr)),
        stderr_ipr=float(np.std(ipr_arr, ddof=1) / np.sqrt(ipr_arr.size)) if ipr_arr.size > 1 else 0.0,
        distance_to_goe=float(abs(mean_r - GOE_R)),
        distance_to_poisson=float(abs(mean_r - POISSON_R)),
        closer_to_poisson=bool(closer_to_poisson),
        strong_disorder_check_passed=strong_check,
        n_levels_used=int(round(float(np.mean(levels_arr)))),
        realizations=int(r_arr.size),
    )


def _assess_periodic(
    points: list[PeriodicPoint],
    final_lattice_size: int,
    config: PeriodicFollowupConfig,
) -> list[PeriodicAssessment]:
    assessments: list[PeriodicAssessment] = []
    for lattice_size in config.lattice_sizes:
        for window_name in config.windows:
            rows = _periodic_rows(points, int(lattice_size), window_name)
            ref = _nearest_disorder_point(rows, config.reference_disorder)
            w32 = _nearest_disorder_point(rows, config.strong_poisson_disorder)
            max_point = _nearest_disorder_point(rows, max(config.disorder_values))
            strong_rows = [point for point in rows if point.disorder >= config.strong_poisson_disorder]
            ipr_mostly = _mostly_monotonic([point.mean_ipr for point in rows])
            distance_improves = max_point.distance_to_poisson < rows[0].distance_to_poisson
            all_strong_poisson = all(point.closer_to_poisson for point in strong_rows)
            any_strong_poisson = any(point.closer_to_poisson for point in strong_rows)
            resolved = all_strong_poisson and ipr_mostly and distance_improves
            assessments.append(
                PeriodicAssessment(
                    lattice_size=int(lattice_size),
                    window_name=window_name,
                    reference_r_w24=ref.mean_r,
                    reference_ipr_w24=ref.mean_ipr,
                    w32_r=w32.mean_r,
                    w32_ipr=w32.mean_ipr,
                    max_w=max_point.disorder,
                    max_w_r=max_point.mean_r,
                    max_w_ipr=max_point.mean_ipr,
                    w24_closer_to_poisson=ref.closer_to_poisson,
                    w32_closer_to_poisson=w32.closer_to_poisson,
                    max_w_closer_to_poisson=max_point.closer_to_poisson,
                    all_w_ge_32_closer_to_poisson=all_strong_poisson,
                    any_w_ge_32_closer_to_poisson=any_strong_poisson,
                    ipr_mostly_monotonic=ipr_mostly,
                    distance_to_poisson_improves=distance_improves,
                    failure_resolved_by_stronger_disorder=resolved,
                )
            )
    return assessments


def _clean_degeneracy_diagnostic(lattice_size: int, tolerance: float = 1e-10) -> DegeneracyDiagnostic:
    periodic = build_anderson_3d_hamiltonian(lattice_size=lattice_size, disorder=0.0, seed=1, periodic=True)
    open_h = build_anderson_3d_hamiltonian(lattice_size=lattice_size, disorder=0.0, seed=1, periodic=False)
    periodic_values = np.linalg.eigvalsh(periodic.toarray())
    open_values = np.linalg.eigvalsh(open_h.toarray())
    return DegeneracyDiagnostic(
        lattice_size=lattice_size,
        clean_periodic_degeneracy_fraction=_small_gap_fraction(periodic_values, tolerance),
        clean_open_degeneracy_fraction=_small_gap_fraction(open_values, tolerance),
        tolerance=tolerance,
    )


def _small_gap_fraction(values: np.ndarray, tolerance: float) -> float:
    spacings = np.diff(np.sort(values))
    if spacings.size == 0:
        return 0.0
    return float(np.mean(np.abs(spacings) <= tolerance))


def _classify_periodic_failure(
    assessments: list[PeriodicAssessment],
    degeneracy: DegeneracyDiagnostic,
    spectrum_window_artifact: bool,
) -> str:
    final_lattice_size = max(assessment.lattice_size for assessment in assessments)
    final = [assessment for assessment in assessments if assessment.lattice_size == final_lattice_size]
    all_final_resolved = all(assessment.failure_resolved_by_stronger_disorder for assessment in final)
    any_w24_failed = any(not assessment.w24_closer_to_poisson for assessment in final)
    all_final_ipr = all(assessment.ipr_mostly_monotonic for assessment in final)
    lower_l_not_resolved = any(
        not assessment.failure_resolved_by_stronger_disorder
        for assessment in assessments
        if assessment.lattice_size != final_lattice_size
    )
    degeneracy_gap = (
        degeneracy.clean_periodic_degeneracy_fraction
        - degeneracy.clean_open_degeneracy_fraction
    )

    if all_final_resolved and any_w24_failed:
        return (
            "likely insufficient disorder range at W=24 with finite-size/seed-count sensitivity: "
            "periodic boundaries become Poisson-like for W>=32 at the final lattice size"
        )
    if all_final_resolved and lower_l_not_resolved:
        return (
            "likely finite-size effect: the final lattice resolves the periodic failure, "
            "but smaller lattices remain less stable"
        )
    if spectrum_window_artifact:
        return "likely spectrum-window artifact: center and quantile_0.5 do not agree at the final lattice size"
    if not all_final_ipr:
        return "unresolved model issue: IPR is not mostly monotonic under stronger periodic-boundary disorder"
    if degeneracy_gap > 0.05 and not all_final_resolved:
        return (
            "possible boundary-induced degeneracy plus finite-size effect: clean periodic spectrum is more degenerate "
            "and strong-disorder r-statistics remain unstable"
        )
    if any(assessment.any_w_ge_32_closer_to_poisson for assessment in final):
        return (
            "partially resolved but statistically unstable: at least one final-window strong-disorder point is "
            "Poisson-like, but the full W>=32 criterion does not hold"
        )
    return "unresolved: stronger periodic-boundary disorder did not robustly resolve the diagnostic failure"


def _summary_statement(
    stronger_poisson: bool,
    ipr_mostly_monotonic_all: bool,
    spectrum_window_artifact: bool,
    classification: str,
) -> str:
    if stronger_poisson and ipr_mostly_monotonic_all and not spectrum_window_artifact:
        return "Periodic failure is resolved in this targeted diagnostic at stronger disorder, but baseline is unchanged."
    return f"Periodic failure remains a limitation or partial limitation: {classification}"


def _spectrum_window_artifact_suspected(assessments: list[PeriodicAssessment]) -> bool:
    final_lattice_size = max(assessment.lattice_size for assessment in assessments)
    final = [assessment for assessment in assessments if assessment.lattice_size == final_lattice_size]
    states = {assessment.window_name: assessment.failure_resolved_by_stronger_disorder for assessment in final}
    if "center" in states and "quantile_0.5" in states:
        return states["center"] != states["quantile_0.5"]
    return len(set(states.values())) > 1


def _periodic_rows(points: list[PeriodicPoint], lattice_size: int, window_name: str) -> list[PeriodicPoint]:
    return sorted(
        [
            point
            for point in points
            if point.boundary == "periodic"
            and point.lattice_size == lattice_size
            and point.window_name == window_name
        ],
        key=lambda point: point.disorder,
    )


def _boundary_rows(points: list[PeriodicPoint], boundary: str, lattice_size: int, window_name: str) -> list[PeriodicPoint]:
    return sorted(
        [
            point
            for point in points
            if point.boundary == boundary
            and point.lattice_size == lattice_size
            and point.window_name == window_name
        ],
        key=lambda point: point.disorder,
    )


def _nearest_disorder_point(points: list[PeriodicPoint], disorder: float) -> PeriodicPoint:
    if not points:
        raise ValueError("cannot select nearest disorder point from empty points")
    return min(points, key=lambda point: abs(point.disorder - disorder))


def _mostly_monotonic(values: list[float], tolerance: float = 1e-12) -> bool:
    arr = np.asarray(values, dtype=float)
    if arr.size < 3:
        return True
    diffs = np.diff(arr)
    decreases = int(np.sum(diffs < -tolerance))
    return decreases <= 1


def _metrics_payload(result: PeriodicFollowupResult) -> dict:
    return {
        "points": [asdict(point) for point in result.points],
        "assessments": [asdict(assessment) for assessment in result.assessments],
        "final_lattice_size": result.final_lattice_size,
        "degeneracy_diagnostic": asdict(result.degeneracy_diagnostic),
        "stronger_disorder_makes_periodic_poisson_like": result.stronger_disorder_makes_periodic_poisson_like,
        "ipr_mostly_monotonic_all": result.ipr_mostly_monotonic_all,
        "spectrum_window_artifact_suspected": result.spectrum_window_artifact_suspected,
        "classification": result.classification,
        "summary_statement": result.summary_statement,
        "source_boundary_comparison_run": BOUNDARY_COMPARISON_RUN,
        "historical_null_result": HISTORICAL_NULL_RESULT,
        "baseline_remains": BASELINE,
    }


def _save_data_npz(result: PeriodicFollowupResult, path: Path) -> None:
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
        distance_to_goe=np.asarray([point.distance_to_goe for point in rows], dtype=float),
        distance_to_poisson=np.asarray([point.distance_to_poisson for point in rows], dtype=float),
        closer_to_poisson=np.asarray([point.closer_to_poisson for point in rows], dtype=bool),
        strong_check=np.asarray(
            [
                -1 if point.strong_disorder_check_passed is None else int(point.strong_disorder_check_passed)
                for point in rows
            ],
            dtype=int,
        ),
        n_levels_used=np.asarray([point.n_levels_used for point in rows], dtype=int),
        realizations=np.asarray([point.realizations for point in rows], dtype=int),
    )


def _save_periodic_r_plot(result: PeriodicFollowupResult, path: Path) -> None:
    fig, axes = plt.subplots(1, len(result.config.windows), figsize=(11, 4.7), constrained_layout=True, sharey=True)
    if len(result.config.windows) == 1:
        axes = [axes]
    for ax, window_name in zip(axes, result.config.windows):
        for lattice_size in result.config.lattice_sizes:
            rows = _periodic_rows(result.points, int(lattice_size), window_name)
            ax.errorbar(
                [row.disorder for row in rows],
                [row.mean_r for row in rows],
                yerr=[row.stderr_r for row in rows],
                marker="o",
                capsize=3,
                label=f"L={lattice_size}",
            )
        ax.axhline(GOE_R, color="black", linestyle="--", linewidth=1.0, label="GOE")
        ax.axhline(POISSON_R, color="black", linestyle=":", linewidth=1.0, label="Poisson")
        ax.set_title(window_name)
        ax.set_xlabel("disorder W")
        ax.set_ylabel("mean adjacent-gap ratio <r>")
        ax.legend(fontsize="small")
    fig.suptitle("Periodic-boundary follow-up: r-statistics")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_periodic_ipr_plot(result: PeriodicFollowupResult, path: Path) -> None:
    fig, axes = plt.subplots(1, len(result.config.windows), figsize=(11, 4.7), constrained_layout=True, sharey=True)
    if len(result.config.windows) == 1:
        axes = [axes]
    for ax, window_name in zip(axes, result.config.windows):
        for lattice_size in result.config.lattice_sizes:
            rows = _periodic_rows(result.points, int(lattice_size), window_name)
            ax.errorbar(
                [row.disorder for row in rows],
                [row.mean_ipr for row in rows],
                yerr=[row.stderr_ipr for row in rows],
                marker="s",
                capsize=3,
                label=f"L={lattice_size}",
            )
        ax.set_title(window_name)
        ax.set_xlabel("disorder W")
        ax.set_ylabel("mean IPR")
        ax.set_yscale("log")
        ax.legend(fontsize="small")
    fig.suptitle("Periodic-boundary follow-up: IPR")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_distance_plot(result: PeriodicFollowupResult, path: Path) -> None:
    fig, axes = plt.subplots(1, len(result.config.windows), figsize=(11, 4.7), constrained_layout=True, sharey=True)
    if len(result.config.windows) == 1:
        axes = [axes]
    final_lattice = result.final_lattice_size
    for ax, window_name in zip(axes, result.config.windows):
        rows = _periodic_rows(result.points, final_lattice, window_name)
        ax.plot([row.disorder for row in rows], [row.distance_to_poisson for row in rows], marker="o", label="to Poisson")
        ax.plot([row.disorder for row in rows], [row.distance_to_goe for row in rows], marker="s", label="to GOE")
        ax.set_title(f"L={final_lattice}, {window_name}")
        ax.set_xlabel("disorder W")
        ax.set_ylabel("absolute distance in <r>")
        ax.legend(fontsize="small")
    fig.suptitle("Periodic-boundary follow-up: distance to reference statistics")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_open_comparison_plot(result: PeriodicFollowupResult, path: Path) -> None:
    fig, axes = plt.subplots(1, len(result.config.windows), figsize=(11, 4.7), constrained_layout=True, sharey=True)
    if len(result.config.windows) == 1:
        axes = [axes]
    final_lattice = result.final_lattice_size
    for ax, window_name in zip(axes, result.config.windows):
        for boundary, marker in (("periodic", "o"), ("open", "s")):
            rows = _boundary_rows(result.points, boundary, final_lattice, window_name)
            if not rows:
                continue
            ax.errorbar(
                [row.disorder for row in rows],
                [row.mean_r for row in rows],
                yerr=[row.stderr_r for row in rows],
                marker=marker,
                capsize=3,
                label=boundary,
            )
        ax.axhline(GOE_R, color="black", linestyle="--", linewidth=1.0, label="GOE")
        ax.axhline(POISSON_R, color="black", linestyle=":", linewidth=1.0, label="Poisson")
        ax.set_title(f"L={final_lattice}, {window_name}")
        ax.set_xlabel("disorder W")
        ax.set_ylabel("<r>")
        ax.legend(fontsize="small")
    fig.suptitle("Periodic follow-up with open reference")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _points_table(points: list[PeriodicPoint]) -> str:
    lines = [
        "| boundary | L | W | window | <r> | stderr_r | IPR | stderr_ipr | dGOE | dPoisson | closer Poisson | strong check |",
        "| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for point in sorted(points, key=lambda row: (row.boundary, row.lattice_size, row.disorder, row.window_name)):
        strong_check = "" if point.strong_disorder_check_passed is None else str(point.strong_disorder_check_passed)
        lines.append(
            f"| {point.boundary} | {point.lattice_size} | {point.disorder:.4g} | {point.window_name} | "
            f"{point.mean_r:.4f} | {point.stderr_r:.4f} | {point.mean_ipr:.6g} | "
            f"{point.stderr_ipr:.2g} | {point.distance_to_goe:.4f} | {point.distance_to_poisson:.4f} | "
            f"{point.closer_to_poisson} | {strong_check} |"
        )
    return "\n".join(lines)


def _summary_lines(result: PeriodicFollowupResult, output_dir: Path) -> list[str]:
    return [
        "Targeted periodic-boundary follow-up after open-vs-periodic disagreement.",
        f"Source boundary comparison: {BOUNDARY_COMPARISON_RUN}",
        f"Baseline remains: {BASELINE}",
        "",
        f"Classification: {result.classification}",
        f"Summary: {result.summary_statement}",
        f"Stronger disorder W>=32 makes periodic boundary Poisson-like: {result.stronger_disorder_makes_periodic_poisson_like}.",
        f"IPR mostly monotonic across all periodic assessments: {result.ipr_mostly_monotonic_all}.",
        f"Spectrum-window artifact suspected: {result.spectrum_window_artifact_suspected}.",
        "",
        "Clean-spectrum degeneracy diagnostic:",
        f"- periodic small-gap fraction: {result.degeneracy_diagnostic.clean_periodic_degeneracy_fraction:.6g}",
        f"- open small-gap fraction: {result.degeneracy_diagnostic.clean_open_degeneracy_fraction:.6g}",
        "",
        "## Final Periodic Table",
        "",
        final_periodic_table(result),
        "",
        "## Assessments",
        "",
        assessments_table(result),
        "",
        f"Historical null-result preserved elsewhere: {HISTORICAL_NULL_RESULT}.",
        "Interpretation: benchmark diagnosis only, not proof of target physical localization.",
        "Non-claims: no chirality, no covariant compactification proof, no Witten/Lichnerowicz bypass, no SM derivation.",
        f"Run directory: {output_dir}",
    ]


def update_spectral_report(result: PeriodicFollowupResult, run_dir: Path) -> None:
    report = Path("reports") / "SPECTRAL_REPORT.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Spectral Report\n"
    section = f"""
## Periodic Boundary Follow-Up

Command:

```powershell
python scripts/anderson_3d_periodic_followup.py
```

Run directory:

```text
{run_dir}
```

Baseline remains `{BASELINE}`.

Classification:

```text
{result.classification}
```

Final periodic results:

{final_periodic_table(result)}

Assessments:

{assessments_table(result)}

Summary:

- {result.summary_statement}
- Stronger disorder `W>=32` makes periodic boundary Poisson-like: `{result.stronger_disorder_makes_periodic_poisson_like}`.
- IPR mostly monotonic across all periodic assessments: `{result.ipr_mostly_monotonic_all}`.
- Spectrum-window artifact suspected: `{result.spectrum_window_artifact_suspected}`.
- Clean periodic small-gap fraction: `{result.degeneracy_diagnostic.clean_periodic_degeneracy_fraction:.6g}`.
- Clean open small-gap fraction: `{result.degeneracy_diagnostic.clean_open_degeneracy_fraction:.6g}`.
- Historical null-result preserved: `{HISTORICAL_NULL_RESULT}`.

Saved artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/periodic_r_vs_w.png`
- `{run_dir}/figures/periodic_ipr_vs_w.png`
- `{run_dir}/figures/periodic_distance_to_poisson_goe.png`
- `{run_dir}/figures/periodic_open_comparison_optional.png`

Interpretation:

This diagnoses the periodic-boundary failure only. It does not promote the
baseline and does not prove target-model localization, chirality, covariant
compactification, Witten/Lichnerowicz bypass, or Standard Model physics.
"""
    report.write_text(_replace_or_append_section(existing, "## Periodic Boundary Follow-Up", section), encoding="utf-8")


def update_validation_status(result: PeriodicFollowupResult, run_dir: Path) -> None:
    report = Path("reports") / "VALIDATION_STATUS.md"
    existing = report.read_text(encoding="utf-8") if report.exists() else "# Validation Status - GeoSpectra Lab\n"
    section = f"""
### Periodic Boundary Follow-Up

Latest run:

```text
{run_dir}
```

Command:

```powershell
python scripts/anderson_3d_periodic_followup.py
```

Status:

- Baseline remains `{BASELINE}`.
- Classification: {result.classification}
- Stronger disorder `W>=32` makes periodic boundary Poisson-like: `{result.stronger_disorder_makes_periodic_poisson_like}`.
- IPR mostly monotonic across all periodic assessments: `{result.ipr_mostly_monotonic_all}`.
- Spectrum-window artifact suspected: `{result.spectrum_window_artifact_suspected}`.

Assessments:

{assessments_table(result)}

Artifacts:

- `{run_dir}/config.json`
- `{run_dir}/metrics.json`
- `{run_dir}/data.npz`
- `{run_dir}/summary.md`
- `{run_dir}/figures/periodic_r_vs_w.png`
- `{run_dir}/figures/periodic_ipr_vs_w.png`
- `{run_dir}/figures/periodic_distance_to_poisson_goe.png`
- `{run_dir}/figures/periodic_open_comparison_optional.png`
"""
    report.write_text(
        _insert_or_replace_before(existing, "## Null / Limiting Results", "### Periodic Boundary Follow-Up", section),
        encoding="utf-8",
    )


def update_null_and_issue_logs(result: PeriodicFollowupResult, run_dir: Path) -> None:
    null_path = Path("reports") / "NULL_RESULTS.md"
    existing_null = null_path.read_text(encoding="utf-8") if null_path.exists() else "# Null Results\n"
    null_section = f"""
## Periodic Boundary Follow-Up Status

Run directory: `{run_dir}`

Classification:

```text
{result.classification}
```

Summary:

- {result.summary_statement}
- Stronger disorder `W>=32` makes periodic boundary Poisson-like: `{result.stronger_disorder_makes_periodic_poisson_like}`.
- IPR mostly monotonic across all periodic assessments: `{result.ipr_mostly_monotonic_all}`.
- Spectrum-window artifact suspected: `{result.spectrum_window_artifact_suspected}`.
- Baseline remains `{BASELINE}`.
- Historical null-result preserved: `{HISTORICAL_NULL_RESULT}`.

This entry updates the boundary-condition limitation rather than erasing it.
The earlier open-vs-periodic disagreement remains part of the validation record.
"""
    null_path.write_text(_replace_or_append_section(existing_null, "## Periodic Boundary Follow-Up Status", null_section), encoding="utf-8")

    issue_path = Path("reports") / "ISSUES_SCIENTIFIC.md"
    existing_issue = issue_path.read_text(encoding="utf-8") if issue_path.exists() else "# Scientific Issues\n"
    issue_section = f"""
## Periodic Boundary Follow-Up Interpretation

Run directory: `{run_dir}`

Classification: {result.classification}

Remaining uncertainty:

- The benchmark remains finite-size limited.
- The pass/fail rule is a diagnostic threshold, not a theorem.
- Boundary-sensitive behavior should be retested with larger `L`, more seeds,
  solver checks, and window-width variation before stronger localization
  statements are made.
- No target compactification model has been validated.
"""
    issue_path.write_text(_replace_or_append_section(existing_issue, "## Periodic Boundary Follow-Up Interpretation", issue_section), encoding="utf-8")


def update_readme_command() -> None:
    readme = Path("README.md")
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    command = "python scripts/anderson_3d_periodic_followup.py"
    if command in text:
        return
    anchor = "python scripts/anderson_3d_boundary_comparison.py\n"
    if anchor in text:
        text = text.replace(anchor, anchor + f"{command}\n", 1)
    readme.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose periodic-boundary failure in 3D Anderson benchmark.")
    parser.add_argument("--smoke", action="store_true", help="Tiny fast run for tests.")
    parser.add_argument("--include-l9", action="store_true", help="Include L=9 in the diagnostic if runtime is acceptable.")
    parser.add_argument("--seed", type=int, default=6262)
    parser.add_argument("--realizations", type=int, default=None)
    return parser.parse_args()


def config_from_args(args: argparse.Namespace) -> PeriodicFollowupConfig:
    if args.smoke:
        return PeriodicFollowupConfig(
            lattice_sizes=(4,),
            disorder_values=(16.0, 24.0, 32.0),
            windows=("center", "quantile_0.5"),
            realizations=2,
            seed=args.seed,
            include_open_reference=True,
            open_reference_lattice_size=4,
            open_reference_realizations=2,
        )
    lattice_sizes = (6, 7, 8, 9) if args.include_l9 else (6, 7, 8)
    return PeriodicFollowupConfig(
        lattice_sizes=lattice_sizes,
        realizations=args.realizations if args.realizations is not None else 10,
        seed=args.seed,
        open_reference_lattice_size=max(lattice_sizes),
    )


def run(args: argparse.Namespace) -> PeriodicFollowupResult:
    config = config_from_args(args)
    run_dir = make_run_dir("anderson_periodic_followup")
    result = run_periodic_followup(config=config, output_dir=run_dir)
    if os.environ.get("CC_TOY_LAB_SKIP_REPORT_UPDATE") != "1":
        update_spectral_report(result, run_dir)
        update_validation_status(result, run_dir)
        update_null_and_issue_logs(result, run_dir)
        update_readme_command()

    print(final_periodic_table(result))
    print()
    print(assessments_table(result))
    print(f"classification={result.classification}")
    print(f"stronger_disorder_makes_periodic_poisson_like={result.stronger_disorder_makes_periodic_poisson_like}")
    print(f"ipr_mostly_monotonic_all={result.ipr_mostly_monotonic_all}")
    print(f"spectrum_window_artifact_suspected={result.spectrum_window_artifact_suspected}")
    print(f"summary={result.summary_statement}")
    print(f"anderson_periodic_followup complete: {run_dir}")
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
