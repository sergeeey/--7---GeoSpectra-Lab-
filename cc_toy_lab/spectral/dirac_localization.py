from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse

from cc_toy_lab.runs import write_json, write_summary
from cc_toy_lab.spectral.anderson_3d import GOE_R, POISSON_R
from cc_toy_lab.spectral.metrics import inverse_participation_ratio, mean_adjacent_gap_ratio


DIRAC_LOCALIZATION_MODES = ("clean", "random_mass", "gauge_phase", "geometric_weight")


@dataclass(frozen=True)
class DiracLocalizationConfig:
    sizes: tuple[int, ...] = (48, 64)
    disorder_values: tuple[float, ...] = (0.0, 1.0, 2.0, 4.0, 8.0)
    modes: tuple[str, ...] = DIRAC_LOCALIZATION_MODES
    realizations: int = 4
    seed: int = 7373
    near_zero_tol: float = 1e-6
    positive_floor: float = 1e-8
    near_zero_window: int = 8
    note: str = (
        "Toy chiral block Dirac localization benchmark; near-zero modes are numerical signals, "
        "not protected chiral zero modes"
    )


@dataclass(frozen=True)
class DiracLocalizationObservation:
    size: int
    dimension: int
    mode: str
    disorder: float
    seed: int
    mean_r_positive: float
    mean_ipr_near_zero: float
    near_zero_count: int
    min_abs_eigenvalue: float
    symmetry_error: float
    positive_levels_used: int


@dataclass(frozen=True)
class DiracLocalizationPoint:
    size: int
    dimension: int
    mode: str
    disorder: float
    mean_r_positive: float
    stderr_r_positive: float
    mean_ipr_near_zero: float
    stderr_ipr_near_zero: float
    mean_near_zero_count: float
    stderr_near_zero_count: float
    mean_min_abs_eigenvalue: float
    mean_symmetry_error: float
    positive_levels_used: int
    realizations: int


@dataclass(frozen=True)
class DiracLocalizationModeAssessment:
    size: int
    mode: str
    weak_disorder: float
    strong_disorder: float
    weak_ipr: float
    strong_ipr: float
    weak_r: float
    strong_r: float
    ipr_increases: bool
    r_moves_toward_poisson: bool
    symmetry_passed: bool
    near_zero_signal_observed: bool


@dataclass(frozen=True)
class DiracLocalizationResult:
    config: DiracLocalizationConfig
    points: list[DiracLocalizationPoint]
    observations: list[DiracLocalizationObservation]
    assessments: list[DiracLocalizationModeAssessment]
    final_size: int
    all_symmetry_checks_passed: bool
    any_near_zero_modes: bool
    summary_statement: str


def build_toy_dirac_localization_operator(
    size: int = 64,
    mode: str = "clean",
    disorder: float = 0.0,
    seed: int | None = None,
) -> sparse.csr_matrix:
    """Build D = [[0, A], [A^dagger, 0]] for toy localization diagnostics.

    The construction enforces chiral block symmetry and Hermiticity. It is a
    finite-dimensional toy operator, not a continuum Dirac operator and not an
    index theorem calculation.
    """
    if size < 8:
        raise ValueError("size must be >= 8")
    if disorder < 0:
        raise ValueError("disorder must be non-negative")
    if mode not in DIRAC_LOCALIZATION_MODES:
        raise ValueError(f"unknown mode: {mode}")

    rng = np.random.default_rng(seed)
    a_block = _base_forward_derivative(size)
    if mode == "random_mass":
        mass = rng.normal(loc=0.0, scale=disorder / 2.0, size=size)
        a_block = a_block + sparse.diags(mass, format="csr")
    elif mode == "gauge_phase":
        phases = rng.uniform(-disorder, disorder, size=size)
        a_block = _forward_derivative_with_phases(size, phases)
    elif mode == "geometric_weight":
        log_weights = rng.normal(loc=0.0, scale=0.12 * disorder, size=size)
        weights = np.exp(np.clip(log_weights, -2.0, 2.0))
        onsite = rng.normal(loc=0.0, scale=0.08 * disorder, size=size)
        a_block = _weighted_forward_derivative(size, weights) + sparse.diags(onsite, format="csr")

    zero = sparse.csr_matrix((size, size), dtype=complex)
    return sparse.bmat([[zero, a_block], [a_block.getH(), zero]], format="csr")


def analyze_dirac_operator(
    size: int,
    mode: str,
    disorder: float,
    seed: int,
    near_zero_tol: float = 1e-6,
    positive_floor: float = 1e-8,
    near_zero_window: int = 8,
) -> tuple[DiracLocalizationObservation, np.ndarray, np.ndarray]:
    operator = build_toy_dirac_localization_operator(size=size, mode=mode, disorder=disorder, seed=seed)
    values, vectors = np.linalg.eigh(operator.toarray())
    positive = values[values > positive_floor]
    r_value = mean_adjacent_gap_ratio(positive)

    near_indices = np.where(np.abs(values) <= near_zero_tol)[0]
    if near_indices.size == 0:
        near_indices = np.argsort(np.abs(values))[: max(1, min(near_zero_window, values.size))]
    near_vectors = vectors[:, near_indices]
    near_ipr = inverse_participation_ratio(near_vectors)
    symmetry_error = spectral_symmetry_error(values)
    observation = DiracLocalizationObservation(
        size=size,
        dimension=2 * size,
        mode=mode,
        disorder=float(disorder),
        seed=int(seed),
        mean_r_positive=float(r_value),
        mean_ipr_near_zero=float(np.mean(near_ipr)),
        near_zero_count=int(np.sum(np.abs(values) <= near_zero_tol)),
        min_abs_eigenvalue=float(np.min(np.abs(values))),
        symmetry_error=float(symmetry_error),
        positive_levels_used=int(positive.size),
    )
    return observation, values, near_ipr


def spectral_symmetry_error(eigenvalues: np.ndarray) -> float:
    values = np.sort(np.asarray(eigenvalues, dtype=float))
    if values.size == 0:
        return float("nan")
    scale = max(1.0, float(np.max(np.abs(values))))
    return float(np.max(np.abs(values + values[::-1])) / scale)


def run_dirac_localization_benchmark(
    config: DiracLocalizationConfig,
    output_dir: Path | None = None,
) -> DiracLocalizationResult:
    observations: list[DiracLocalizationObservation] = []
    spectrum_examples: dict[str, np.ndarray] = {}
    for size in config.sizes:
        for mode_index, mode in enumerate(config.modes):
            for w_index, disorder in enumerate(config.disorder_values):
                for realization in range(config.realizations):
                    run_seed = config.seed + 1_000_000 * int(size) + 100_000 * mode_index + 10_000 * w_index + realization
                    observation, eigenvalues, _near_ipr = analyze_dirac_operator(
                        size=int(size),
                        mode=mode,
                        disorder=float(disorder),
                        seed=run_seed,
                        near_zero_tol=config.near_zero_tol,
                        positive_floor=config.positive_floor,
                        near_zero_window=config.near_zero_window,
                    )
                    observations.append(observation)
                    if int(size) == max(config.sizes) and realization == 0:
                        spectrum_examples[f"{mode}_W{float(disorder):g}"] = eigenvalues

    points = _aggregate_points(observations)
    final_size = max(config.sizes)
    assessments = _assess_modes(points, final_size, config)
    all_symmetry = all(point.mean_symmetry_error < 1e-8 for point in points)
    any_near_zero = any(point.mean_near_zero_count > 0 for point in points)
    summary = _summary_statement(assessments, all_symmetry, any_near_zero)
    result = DiracLocalizationResult(
        config=config,
        points=points,
        observations=observations,
        assessments=assessments,
        final_size=final_size,
        all_symmetry_checks_passed=all_symmetry,
        any_near_zero_modes=any_near_zero,
        summary_statement=summary,
    )
    if output_dir is not None:
        save_dirac_localization_artifacts(result, output_dir, spectrum_examples)
    return result


def save_dirac_localization_artifacts(
    result: DiracLocalizationResult,
    output_dir: Path,
    spectrum_examples: dict[str, np.ndarray],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "config.json", asdict(result.config))
    write_json(output_dir / "metrics.json", _metrics_payload(result))
    _save_data_npz(result, output_dir / "data.npz")
    _save_spectrum_plot(result, spectrum_examples, figures_dir / "dirac_spectrum.png")
    _save_ipr_plot(result, figures_dir / "dirac_ipr_vs_disorder.png")
    _save_r_plot(result, figures_dir / "dirac_r_statistics.png")
    _save_near_zero_plot(result, figures_dir / "dirac_near_zero_count.png")
    write_summary(output_dir / "summary.md", "Toy Dirac Localization Benchmark", _summary_lines(result, output_dir))


def final_size_table(result: DiracLocalizationResult) -> str:
    rows = [point for point in result.points if point.size == result.final_size]
    return _points_table(rows)


def assessments_table(result: DiracLocalizationResult) -> str:
    lines = [
        "| mode | weak W | strong W | weak IPR | strong IPR | weak <r> | strong <r> | IPR increases | r toward Poisson | near-zero signal |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for assessment in sorted(result.assessments, key=lambda item: item.mode):
        lines.append(
            f"| {assessment.mode} | {assessment.weak_disorder:.4g} | {assessment.strong_disorder:.4g} | "
            f"{assessment.weak_ipr:.6g} | {assessment.strong_ipr:.6g} | "
            f"{assessment.weak_r:.4f} | {assessment.strong_r:.4f} | "
            f"{assessment.ipr_increases} | {assessment.r_moves_toward_poisson} | "
            f"{assessment.near_zero_signal_observed} |"
        )
    return "\n".join(lines)


def _base_forward_derivative(size: int) -> sparse.csr_matrix:
    matrix = sparse.lil_matrix((size, size), dtype=complex)
    for i in range(size):
        matrix[i, i] = -1.0
        matrix[i, (i + 1) % size] = 1.0
    return matrix.tocsr()


def _forward_derivative_with_phases(size: int, phases: np.ndarray) -> sparse.csr_matrix:
    matrix = sparse.lil_matrix((size, size), dtype=complex)
    links = np.exp(1j * phases)
    for i in range(size):
        matrix[i, i] = -1.0
        matrix[i, (i + 1) % size] = links[i]
    return matrix.tocsr()


def _weighted_forward_derivative(size: int, weights: np.ndarray) -> sparse.csr_matrix:
    matrix = sparse.lil_matrix((size, size), dtype=complex)
    for i in range(size):
        matrix[i, i] = -weights[i]
        matrix[i, (i + 1) % size] = weights[(i + 1) % size]
    return matrix.tocsr()


def _aggregate_points(observations: list[DiracLocalizationObservation]) -> list[DiracLocalizationPoint]:
    keys = sorted({(obs.size, obs.mode, obs.disorder) for obs in observations})
    points: list[DiracLocalizationPoint] = []
    for size, mode, disorder in keys:
        rows = [obs for obs in observations if obs.size == size and obs.mode == mode and np.isclose(obs.disorder, disorder)]
        r_values = np.asarray([row.mean_r_positive for row in rows], dtype=float)
        finite_r = r_values[np.isfinite(r_values)]
        ipr_values = np.asarray([row.mean_ipr_near_zero for row in rows], dtype=float)
        near_zero = np.asarray([row.near_zero_count for row in rows], dtype=float)
        min_abs = np.asarray([row.min_abs_eigenvalue for row in rows], dtype=float)
        symmetry = np.asarray([row.symmetry_error for row in rows], dtype=float)
        levels = np.asarray([row.positive_levels_used for row in rows], dtype=float)
        points.append(
            DiracLocalizationPoint(
                size=int(size),
                dimension=int(2 * size),
                mode=str(mode),
                disorder=float(disorder),
                mean_r_positive=float(np.mean(finite_r)) if finite_r.size else float("nan"),
                stderr_r_positive=_stderr(finite_r),
                mean_ipr_near_zero=float(np.mean(ipr_values)),
                stderr_ipr_near_zero=_stderr(ipr_values),
                mean_near_zero_count=float(np.mean(near_zero)),
                stderr_near_zero_count=_stderr(near_zero),
                mean_min_abs_eigenvalue=float(np.mean(min_abs)),
                mean_symmetry_error=float(np.mean(symmetry)),
                positive_levels_used=int(round(float(np.mean(levels)))),
                realizations=len(rows),
            )
        )
    return points


def _assess_modes(
    points: list[DiracLocalizationPoint],
    final_size: int,
    config: DiracLocalizationConfig,
) -> list[DiracLocalizationModeAssessment]:
    assessments: list[DiracLocalizationModeAssessment] = []
    weak_disorder = min(config.disorder_values)
    strong_disorder = max(config.disorder_values)
    for mode in config.modes:
        rows = [point for point in points if point.size == final_size and point.mode == mode]
        weak = _nearest_disorder_point(rows, weak_disorder)
        strong = _nearest_disorder_point(rows, strong_disorder)
        weak_poisson_distance = abs(weak.mean_r_positive - POISSON_R)
        strong_poisson_distance = abs(strong.mean_r_positive - POISSON_R)
        assessments.append(
            DiracLocalizationModeAssessment(
                size=final_size,
                mode=mode,
                weak_disorder=weak.disorder,
                strong_disorder=strong.disorder,
                weak_ipr=weak.mean_ipr_near_zero,
                strong_ipr=strong.mean_ipr_near_zero,
                weak_r=weak.mean_r_positive,
                strong_r=strong.mean_r_positive,
                ipr_increases=strong.mean_ipr_near_zero > weak.mean_ipr_near_zero,
                r_moves_toward_poisson=strong_poisson_distance < weak_poisson_distance,
                symmetry_passed=max(point.mean_symmetry_error for point in rows) < 1e-8,
                near_zero_signal_observed=any(point.mean_near_zero_count > 0 for point in rows),
            )
        )
    return assessments


def _nearest_disorder_point(points: list[DiracLocalizationPoint], disorder: float) -> DiracLocalizationPoint:
    if not points:
        raise ValueError("cannot select nearest disorder point from empty points")
    return min(points, key=lambda point: abs(point.disorder - disorder))


def _stderr(values: np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size <= 1:
        return 0.0
    return float(np.std(arr, ddof=1) / np.sqrt(arr.size))


def _summary_statement(
    assessments: list[DiracLocalizationModeAssessment],
    all_symmetry: bool,
    any_near_zero: bool,
) -> str:
    ipr_modes = [assessment.mode for assessment in assessments if assessment.ipr_increases]
    r_modes = [assessment.mode for assessment in assessments if assessment.r_moves_toward_poisson]
    return (
        f"Symmetry passed={all_symmetry}; IPR increases in {ipr_modes}; "
        f"r-statistics moves toward Poisson in {r_modes}; near-zero modes observed={any_near_zero}. "
        "Near-zero modes are numerical signals only, not protected chiral zero modes."
    )


def _metrics_payload(result: DiracLocalizationResult) -> dict:
    return {
        "points": [asdict(point) for point in result.points],
        "observations": [asdict(observation) for observation in result.observations],
        "assessments": [asdict(assessment) for assessment in result.assessments],
        "final_size": result.final_size,
        "all_symmetry_checks_passed": result.all_symmetry_checks_passed,
        "any_near_zero_modes": result.any_near_zero_modes,
        "summary_statement": result.summary_statement,
        "scientific_warning": (
            "Localization and near-zero modes in this toy Dirac operator are not evidence for protected "
            "chirality, Witten/Lichnerowicz bypass, covariant compactification, or Standard Model fermions."
        ),
    }


def _save_data_npz(result: DiracLocalizationResult, path: Path) -> None:
    rows = result.points
    obs = result.observations
    np.savez(
        path,
        point_size=np.asarray([point.size for point in rows], dtype=int),
        point_mode=np.asarray([point.mode for point in rows]),
        point_disorder=np.asarray([point.disorder for point in rows], dtype=float),
        point_mean_r=np.asarray([point.mean_r_positive for point in rows], dtype=float),
        point_mean_ipr=np.asarray([point.mean_ipr_near_zero for point in rows], dtype=float),
        point_near_zero=np.asarray([point.mean_near_zero_count for point in rows], dtype=float),
        point_symmetry=np.asarray([point.mean_symmetry_error for point in rows], dtype=float),
        obs_size=np.asarray([row.size for row in obs], dtype=int),
        obs_mode=np.asarray([row.mode for row in obs]),
        obs_disorder=np.asarray([row.disorder for row in obs], dtype=float),
        obs_seed=np.asarray([row.seed for row in obs], dtype=int),
        obs_r=np.asarray([row.mean_r_positive for row in obs], dtype=float),
        obs_ipr=np.asarray([row.mean_ipr_near_zero for row in obs], dtype=float),
        obs_near_zero=np.asarray([row.near_zero_count for row in obs], dtype=int),
    )


def _save_spectrum_plot(
    result: DiracLocalizationResult,
    spectrum_examples: dict[str, np.ndarray],
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
    labels = list(spectrum_examples)[: min(8, len(spectrum_examples))]
    for offset, label in enumerate(labels):
        values = np.sort(spectrum_examples[label])
        near = values[np.argsort(np.abs(values))[: min(18, values.size)]]
        ax.scatter(near, np.full_like(near, offset, dtype=float), s=16, label=label)
    ax.axvline(0.0, color="black", linestyle=":", linewidth=1.0)
    ax.set_xlabel("eigenvalue near zero")
    ax.set_yticks(np.arange(len(labels)), labels)
    ax.set_title(f"Toy Dirac near-zero spectrum examples, size={result.final_size}")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_ipr_plot(result: DiracLocalizationResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for mode in result.config.modes:
        rows = _final_rows(result, mode)
        ax.errorbar(
            [row.disorder for row in rows],
            [row.mean_ipr_near_zero for row in rows],
            yerr=[row.stderr_ipr_near_zero for row in rows],
            marker="o",
            capsize=3,
            label=mode,
        )
    ax.set_xlabel("disorder strength")
    ax.set_ylabel("mean IPR of near-zero window")
    ax.set_yscale("log")
    ax.set_title(f"Toy Dirac localization: near-zero IPR, size={result.final_size}")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_r_plot(result: DiracLocalizationResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for mode in result.config.modes:
        rows = _final_rows(result, mode)
        ax.errorbar(
            [row.disorder for row in rows],
            [row.mean_r_positive for row in rows],
            yerr=[row.stderr_r_positive for row in rows],
            marker="s",
            capsize=3,
            label=mode,
        )
    ax.axhline(GOE_R, color="black", linestyle="--", linewidth=1.0, label="GOE")
    ax.axhline(POISSON_R, color="black", linestyle=":", linewidth=1.0, label="Poisson")
    ax.set_xlabel("disorder strength")
    ax.set_ylabel("positive-spectrum <r>")
    ax.set_title(f"Toy Dirac localization: r-statistics, size={result.final_size}")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_near_zero_plot(result: DiracLocalizationResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for mode in result.config.modes:
        rows = _final_rows(result, mode)
        ax.errorbar(
            [row.disorder for row in rows],
            [row.mean_near_zero_count for row in rows],
            yerr=[row.stderr_near_zero_count for row in rows],
            marker="^",
            capsize=3,
            label=mode,
        )
    ax.set_xlabel("disorder strength")
    ax.set_ylabel(f"near-zero count, tol={result.config.near_zero_tol:g}")
    ax.set_title("Toy Dirac near-zero count is not an index")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _final_rows(result: DiracLocalizationResult, mode: str) -> list[DiracLocalizationPoint]:
    return sorted(
        [point for point in result.points if point.size == result.final_size and point.mode == mode],
        key=lambda point: point.disorder,
    )


def _points_table(points: list[DiracLocalizationPoint]) -> str:
    lines = [
        "| size | mode | disorder | <r> positive | IPR near-zero | near-zero count | min |lambda| | symmetry error |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for point in sorted(points, key=lambda item: (item.size, item.mode, item.disorder)):
        lines.append(
            f"| {point.size} | {point.mode} | {point.disorder:.4g} | "
            f"{point.mean_r_positive:.4f} | {point.mean_ipr_near_zero:.6g} | "
            f"{point.mean_near_zero_count:.3g} | {point.mean_min_abs_eigenvalue:.3g} | "
            f"{point.mean_symmetry_error:.2e} |"
        )
    return "\n".join(lines)


def _summary_lines(result: DiracLocalizationResult, output_dir: Path) -> list[str]:
    return [
        "Toy Dirac/geometric localization benchmark using D = [[0, A], [A^dagger, 0]].",
        "This tests localization metrics on a chiral block toy operator.",
        "",
        f"Summary: {result.summary_statement}",
        f"All symmetry checks passed: {result.all_symmetry_checks_passed}.",
        f"Any near-zero modes observed: {result.any_near_zero_modes}.",
        "",
        "## Final-Size Results",
        "",
        final_size_table(result),
        "",
        "## Mode Assessments",
        "",
        assessments_table(result),
        "",
        "Warning: near-zero modes are numerical signals only and are not protected chiral zero modes.",
        "Non-claims: no chirality proof, no Witten/Lichnerowicz bypass, no covariant compactification proof, no SM fermion derivation.",
        f"Run directory: {output_dir}",
    ]
