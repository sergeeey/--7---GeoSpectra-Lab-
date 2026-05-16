from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import write_json, write_summary
from cc_toy_lab.spectral.dirac_localization import (
    DIRAC_LOCALIZATION_MODES,
    build_toy_dirac_localization_operator,
)


@dataclass(frozen=True)
class DiracChiralityConfig:
    sizes: tuple[int, ...] = (32, 48)
    disorder_values: tuple[float, ...] = (0.0, 2.0, 8.0)
    modes: tuple[str, ...] = DIRAC_LOCALIZATION_MODES
    realizations: int = 3
    seed: int = 9191
    near_zero_tol: float = 1e-6
    chirality_threshold: float = 0.5
    near_zero_window: int = 8
    algebra_tolerance: float = 1e-8
    note: str = (
        "Toy block-Dirac chirality diagnostic. Numerical index is counted only "
        "from eigenvalues inside near_zero_tol; near-zero signals are not "
        "physical chirality claims."
    )


@dataclass(frozen=True)
class DiracChiralityObservation:
    size: int
    dimension: int
    mode: str
    disorder: float
    seed: int
    gamma_square_error: float
    gamma_hermitian_error: float
    anticommutator_error: float
    near_zero_count: int
    n_plus: int
    n_minus: int
    ambiguous_count: int
    numerical_index: int
    min_abs_eigenvalue: float
    mean_abs_chirality_near_window: float
    max_abs_chirality_near_window: float
    exact_zero_chiralities: list[float]
    near_window_chiralities: list[float]
    classification: str


@dataclass(frozen=True)
class DiracChiralityPoint:
    size: int
    dimension: int
    mode: str
    disorder: float
    mean_anticommutator_error: float
    max_anticommutator_error: float
    mean_near_zero_count: float
    mean_n_plus: float
    mean_n_minus: float
    mean_numerical_index: float
    min_numerical_index: int
    max_numerical_index: int
    mean_abs_chirality_near_window: float
    max_abs_chirality_near_window: float
    mean_min_abs_eigenvalue: float
    realizations: int
    classifications: tuple[str, ...]


@dataclass(frozen=True)
class DiracChiralityModeAssessment:
    size: int
    mode: str
    weak_disorder: float
    strong_disorder: float
    weak_index: float
    strong_index: float
    weak_near_zero_count: float
    strong_near_zero_count: float
    index_stays_zero: bool
    anticommutator_preserved: bool
    classification: str


@dataclass(frozen=True)
class DiracChiralityResult:
    config: DiracChiralityConfig
    observations: list[DiracChiralityObservation]
    points: list[DiracChiralityPoint]
    assessments: list[DiracChiralityModeAssessment]
    final_size: int
    gamma_algebra_passed: bool
    anticommutation_preserved: bool
    all_indices_zero: bool
    any_near_zero_modes: bool
    summary_statement: str


def chirality_operator(size: int) -> np.ndarray:
    """Return Gamma = diag(+I, -I) for a 2*size chiral block space."""
    if size < 1:
        raise ValueError("size must be positive")
    return np.diag(np.r_[np.ones(size), -np.ones(size)]).astype(complex)


def gamma_algebra_errors(operator: np.ndarray, gamma: np.ndarray) -> tuple[float, float, float]:
    """Return Gamma^2, Hermiticity, and normalized anticommutator errors."""
    identity = np.eye(gamma.shape[0], dtype=complex)
    gamma_scale = max(1.0, float(np.linalg.norm(gamma, ord="fro")))
    op_scale = max(1.0, float(np.linalg.norm(operator, ord="fro")))
    gamma_square_error = float(np.linalg.norm(gamma @ gamma - identity, ord="fro") / gamma_scale)
    gamma_hermitian_error = float(np.linalg.norm(gamma - gamma.conj().T, ord="fro") / gamma_scale)
    anticommutator = operator @ gamma + gamma @ operator
    anticommutator_error = float(np.linalg.norm(anticommutator, ord="fro") / op_scale)
    return gamma_square_error, gamma_hermitian_error, anticommutator_error


def analyze_dirac_chirality(
    size: int,
    mode: str,
    disorder: float,
    seed: int,
    near_zero_tol: float = 1e-6,
    chirality_threshold: float = 0.5,
    near_zero_window: int = 8,
    algebra_tolerance: float = 1e-8,
) -> DiracChiralityObservation:
    operator_sparse = build_toy_dirac_localization_operator(
        size=size,
        mode=mode,
        disorder=disorder,
        seed=seed,
    )
    operator = operator_sparse.toarray()
    gamma = chirality_operator(size)
    gamma_square_error, gamma_hermitian_error, anticommutator_error = gamma_algebra_errors(operator, gamma)
    values, vectors = np.linalg.eigh(operator)
    abs_values = np.abs(values)
    exact_zero_indices = np.flatnonzero(abs_values <= near_zero_tol)
    near_window_size = max(1, min(int(near_zero_window), values.size))
    near_window_indices = np.argsort(abs_values)[:near_window_size]

    gamma_vectors = gamma @ vectors
    chiralities = np.real(np.einsum("ij,ij->j", np.conj(vectors), gamma_vectors))
    exact_chiralities = chiralities[exact_zero_indices]
    near_window_chiralities = chiralities[near_window_indices]

    n_plus = int(np.count_nonzero(exact_chiralities >= chirality_threshold))
    n_minus = int(np.count_nonzero(exact_chiralities <= -chirality_threshold))
    ambiguous = int(exact_chiralities.size - n_plus - n_minus)
    numerical_index = n_plus - n_minus
    classification = classify_zero_modes(
        anticommutator_error=anticommutator_error,
        algebra_tolerance=algebra_tolerance,
        near_zero_count=int(exact_zero_indices.size),
        n_plus=n_plus,
        n_minus=n_minus,
        ambiguous_count=ambiguous,
        numerical_index=numerical_index,
    )
    return DiracChiralityObservation(
        size=int(size),
        dimension=int(2 * size),
        mode=str(mode),
        disorder=float(disorder),
        seed=int(seed),
        gamma_square_error=gamma_square_error,
        gamma_hermitian_error=gamma_hermitian_error,
        anticommutator_error=anticommutator_error,
        near_zero_count=int(exact_zero_indices.size),
        n_plus=n_plus,
        n_minus=n_minus,
        ambiguous_count=ambiguous,
        numerical_index=numerical_index,
        min_abs_eigenvalue=float(np.min(abs_values)),
        mean_abs_chirality_near_window=float(np.mean(np.abs(near_window_chiralities))),
        max_abs_chirality_near_window=float(np.max(np.abs(near_window_chiralities))),
        exact_zero_chiralities=[float(value) for value in exact_chiralities],
        near_window_chiralities=[float(value) for value in near_window_chiralities],
        classification=classification,
    )


def classify_zero_modes(
    anticommutator_error: float,
    algebra_tolerance: float,
    near_zero_count: int,
    n_plus: int,
    n_minus: int,
    ambiguous_count: int,
    numerical_index: int,
) -> str:
    if anticommutator_error > algebra_tolerance:
        return "unresolved_chiral_structure_broken"
    if near_zero_count == 0:
        return "no_exact_near_zero_modes"
    if ambiguous_count:
        return "unresolved_ambiguous_chirality"
    if numerical_index == 0:
        if n_plus == n_minus and n_plus > 0:
            return "paired_accidental_or_symmetry_zero_modes"
        return "paired_or_accidental_zero_index"
    return "potentially_protected_unverified_nonzero_index"


def run_dirac_chirality_diagnostic(
    config: DiracChiralityConfig,
    output_dir: Path | None = None,
) -> DiracChiralityResult:
    observations: list[DiracChiralityObservation] = []
    for size in config.sizes:
        for mode_index, mode in enumerate(config.modes):
            for w_index, disorder in enumerate(config.disorder_values):
                for realization in range(config.realizations):
                    run_seed = config.seed + 1_000_000 * int(size) + 100_000 * mode_index + 10_000 * w_index + realization
                    observations.append(
                        analyze_dirac_chirality(
                            size=int(size),
                            mode=mode,
                            disorder=float(disorder),
                            seed=run_seed,
                            near_zero_tol=config.near_zero_tol,
                            chirality_threshold=config.chirality_threshold,
                            near_zero_window=config.near_zero_window,
                            algebra_tolerance=config.algebra_tolerance,
                        )
                    )
    points = _aggregate_points(observations)
    final_size = max(config.sizes)
    assessments = _assess_modes(points, final_size, config)
    gamma_algebra_passed = all(
        obs.gamma_square_error < config.algebra_tolerance and obs.gamma_hermitian_error < config.algebra_tolerance
        for obs in observations
    )
    anticommutation_preserved = all(obs.anticommutator_error < config.algebra_tolerance for obs in observations)
    all_indices_zero = all(obs.numerical_index == 0 for obs in observations)
    any_near_zero_modes = any(obs.near_zero_count > 0 for obs in observations)
    summary = _summary_statement(gamma_algebra_passed, anticommutation_preserved, all_indices_zero, any_near_zero_modes, assessments)
    result = DiracChiralityResult(
        config=config,
        observations=observations,
        points=points,
        assessments=assessments,
        final_size=final_size,
        gamma_algebra_passed=gamma_algebra_passed,
        anticommutation_preserved=anticommutation_preserved,
        all_indices_zero=all_indices_zero,
        any_near_zero_modes=any_near_zero_modes,
        summary_statement=summary,
    )
    if output_dir is not None:
        save_dirac_chirality_artifacts(result, output_dir)
    return result


def save_dirac_chirality_artifacts(result: DiracChiralityResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "config.json", asdict(result.config))
    write_json(output_dir / "metrics.json", _metrics_payload(result))
    _save_data_npz(result, output_dir / "data.npz")
    _save_chirality_expectations_plot(result, figures_dir / "chirality_expectations.png")
    _save_index_plot(result, figures_dir / "index_vs_disorder.png")
    _save_near_zero_scatter(result, figures_dir / "near_zero_chirality_scatter.png")
    _save_anticommutator_plot(result, figures_dir / "anticommutator_error.png")
    write_summary(output_dir / "summary.md", "Toy Dirac Chirality Diagnostic", _summary_lines(result, output_dir))


def points_table(result: DiracChiralityResult) -> str:
    rows = [point for point in result.points if point.size == result.final_size]
    lines = [
        "| size | mode | disorder | mean index | index range | near-zero count | n_plus | n_minus | max {D,Gamma} | classification |",
        "| ---: | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for point in sorted(rows, key=lambda item: (item.mode, item.disorder)):
        lines.append(
            f"| {point.size} | {point.mode} | {point.disorder:.4g} | "
            f"{point.mean_numerical_index:.4g} | [{point.min_numerical_index}, {point.max_numerical_index}] | "
            f"{point.mean_near_zero_count:.4g} | {point.mean_n_plus:.4g} | {point.mean_n_minus:.4g} | "
            f"{point.max_anticommutator_error:.2e} | {', '.join(point.classifications)} |"
        )
    return "\n".join(lines)


def assessments_table(result: DiracChiralityResult) -> str:
    lines = [
        "| mode | weak W | strong W | weak index | strong index | weak zeros | strong zeros | index stays zero | {D,Gamma} preserved | classification |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for assessment in sorted(result.assessments, key=lambda item: item.mode):
        lines.append(
            f"| {assessment.mode} | {assessment.weak_disorder:.4g} | {assessment.strong_disorder:.4g} | "
            f"{assessment.weak_index:.4g} | {assessment.strong_index:.4g} | "
            f"{assessment.weak_near_zero_count:.4g} | {assessment.strong_near_zero_count:.4g} | "
            f"{assessment.index_stays_zero} | {assessment.anticommutator_preserved} | "
            f"{assessment.classification} |"
        )
    return "\n".join(lines)


def _aggregate_points(observations: list[DiracChiralityObservation]) -> list[DiracChiralityPoint]:
    keys = sorted({(obs.size, obs.mode, obs.disorder) for obs in observations})
    points: list[DiracChiralityPoint] = []
    for size, mode, disorder in keys:
        rows = [obs for obs in observations if obs.size == size and obs.mode == mode and np.isclose(obs.disorder, disorder)]
        indexes = np.asarray([row.numerical_index for row in rows], dtype=float)
        near_zero = np.asarray([row.near_zero_count for row in rows], dtype=float)
        n_plus = np.asarray([row.n_plus for row in rows], dtype=float)
        n_minus = np.asarray([row.n_minus for row in rows], dtype=float)
        anticommutator = np.asarray([row.anticommutator_error for row in rows], dtype=float)
        min_abs = np.asarray([row.min_abs_eigenvalue for row in rows], dtype=float)
        mean_abs_chi = np.asarray([row.mean_abs_chirality_near_window for row in rows], dtype=float)
        max_abs_chi = np.asarray([row.max_abs_chirality_near_window for row in rows], dtype=float)
        points.append(
            DiracChiralityPoint(
                size=int(size),
                dimension=int(2 * size),
                mode=str(mode),
                disorder=float(disorder),
                mean_anticommutator_error=float(np.mean(anticommutator)),
                max_anticommutator_error=float(np.max(anticommutator)),
                mean_near_zero_count=float(np.mean(near_zero)),
                mean_n_plus=float(np.mean(n_plus)),
                mean_n_minus=float(np.mean(n_minus)),
                mean_numerical_index=float(np.mean(indexes)),
                min_numerical_index=int(np.min(indexes)),
                max_numerical_index=int(np.max(indexes)),
                mean_abs_chirality_near_window=float(np.mean(mean_abs_chi)),
                max_abs_chirality_near_window=float(np.max(max_abs_chi)),
                mean_min_abs_eigenvalue=float(np.mean(min_abs)),
                realizations=len(rows),
                classifications=tuple(sorted({row.classification for row in rows})),
            )
        )
    return points


def _assess_modes(
    points: list[DiracChiralityPoint],
    final_size: int,
    config: DiracChiralityConfig,
) -> list[DiracChiralityModeAssessment]:
    assessments: list[DiracChiralityModeAssessment] = []
    weak_disorder = min(config.disorder_values)
    strong_disorder = max(config.disorder_values)
    for mode in config.modes:
        rows = [point for point in points if point.size == final_size and point.mode == mode]
        weak = min(rows, key=lambda point: abs(point.disorder - weak_disorder))
        strong = min(rows, key=lambda point: abs(point.disorder - strong_disorder))
        max_abs_index = max(abs(point.min_numerical_index) for point in rows + [weak, strong])
        max_abs_index = max(max_abs_index, max(abs(point.max_numerical_index) for point in rows + [weak, strong]))
        anticommutator_preserved = max(point.max_anticommutator_error for point in rows) < config.algebra_tolerance
        if max_abs_index == 0 and any(point.mean_near_zero_count > 0 for point in rows):
            classification = "paired_or_accidental_zero_index"
        elif max_abs_index == 0:
            classification = "no_index_signal"
        else:
            classification = "nonzero_index_unresolved_requires_stability_tests"
        assessments.append(
            DiracChiralityModeAssessment(
                size=final_size,
                mode=mode,
                weak_disorder=weak.disorder,
                strong_disorder=strong.disorder,
                weak_index=weak.mean_numerical_index,
                strong_index=strong.mean_numerical_index,
                weak_near_zero_count=weak.mean_near_zero_count,
                strong_near_zero_count=strong.mean_near_zero_count,
                index_stays_zero=max_abs_index == 0,
                anticommutator_preserved=anticommutator_preserved,
                classification=classification,
            )
        )
    return assessments


def _summary_statement(
    gamma_algebra_passed: bool,
    anticommutation_preserved: bool,
    all_indices_zero: bool,
    any_near_zero_modes: bool,
    assessments: list[DiracChiralityModeAssessment],
) -> str:
    nonzero_modes = [assessment.mode for assessment in assessments if not assessment.index_stays_zero]
    return (
        f"Gamma algebra passed={gamma_algebra_passed}; anticommutation preserved={anticommutation_preserved}; "
        f"all numerical indices zero={all_indices_zero}; near-zero modes observed={any_near_zero_modes}; "
        f"nonzero-index modes={nonzero_modes}. Near-zero modes remain numerical signals unless an index "
        "diagnostic is stable across size, seeds, and perturbations."
    )


def _metrics_payload(result: DiracChiralityResult) -> dict:
    return {
        "points": [asdict(point) for point in result.points],
        "observations": [asdict(observation) for observation in result.observations],
        "assessments": [asdict(assessment) for assessment in result.assessments],
        "final_size": result.final_size,
        "gamma_algebra_passed": result.gamma_algebra_passed,
        "anticommutation_preserved": result.anticommutation_preserved,
        "all_indices_zero": result.all_indices_zero,
        "any_near_zero_modes": result.any_near_zero_modes,
        "summary_statement": result.summary_statement,
        "comparison_control": "Compare against reports/CHIRALITY_INDEX_REPORT.md S2 Dirac monopole index control.",
        "scientific_warning": (
            "This toy diagnostic does not prove physical chirality, protected zero modes, "
            "Witten/Lichnerowicz bypass, covariant compactification, or Standard Model fermions."
        ),
    }


def _save_data_npz(result: DiracChiralityResult, path: Path) -> None:
    points = result.points
    obs = result.observations
    np.savez(
        path,
        point_size=np.asarray([point.size for point in points], dtype=int),
        point_mode=np.asarray([point.mode for point in points]),
        point_disorder=np.asarray([point.disorder for point in points], dtype=float),
        point_index=np.asarray([point.mean_numerical_index for point in points], dtype=float),
        point_near_zero=np.asarray([point.mean_near_zero_count for point in points], dtype=float),
        point_anticommutator=np.asarray([point.mean_anticommutator_error for point in points], dtype=float),
        obs_size=np.asarray([row.size for row in obs], dtype=int),
        obs_mode=np.asarray([row.mode for row in obs]),
        obs_disorder=np.asarray([row.disorder for row in obs], dtype=float),
        obs_seed=np.asarray([row.seed for row in obs], dtype=int),
        obs_index=np.asarray([row.numerical_index for row in obs], dtype=int),
        obs_near_zero=np.asarray([row.near_zero_count for row in obs], dtype=int),
        obs_min_abs=np.asarray([row.min_abs_eigenvalue for row in obs], dtype=float),
    )


def _save_chirality_expectations_plot(result: DiracChiralityResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
    final_obs = [obs for obs in result.observations if obs.size == result.final_size]
    x_ticks: list[str] = []
    x_pos = 0
    for mode in result.config.modes:
        mode_obs = [obs for obs in final_obs if obs.mode == mode]
        for disorder in sorted({obs.disorder for obs in mode_obs}):
            rows = [obs for obs in mode_obs if np.isclose(obs.disorder, disorder)]
            values = [value for obs in rows for value in obs.near_window_chiralities]
            if values:
                jitter = np.linspace(-0.22, 0.22, len(values))
                ax.scatter(np.full(len(values), x_pos) + jitter, values, s=12, alpha=0.7)
            x_ticks.append(f"{mode}\nW={disorder:g}")
            x_pos += 1
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.axhline(result.config.chirality_threshold, color="tab:red", linestyle="--", linewidth=0.8)
    ax.axhline(-result.config.chirality_threshold, color="tab:red", linestyle="--", linewidth=0.8)
    ax.set_ylabel("<psi|Gamma|psi> near-zero window")
    ax.set_xticks(np.arange(len(x_ticks)), x_ticks, rotation=80, fontsize=7)
    ax.set_title("Toy Dirac chirality expectations are diagnostic, not physical chirality")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_index_plot(result: DiracChiralityResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for mode in result.config.modes:
        rows = _final_rows(result, mode)
        ax.plot([row.disorder for row in rows], [row.mean_numerical_index for row in rows], marker="o", label=mode)
    ax.axhline(0.0, color="black", linestyle=":", linewidth=1.0)
    ax.set_xlabel("disorder strength")
    ax.set_ylabel("mean numerical index")
    ax.set_title("Toy Dirac numerical index by mode")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_near_zero_scatter(result: DiracChiralityResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    final_obs = [obs for obs in result.observations if obs.size == result.final_size]
    for mode in result.config.modes:
        rows = [obs for obs in final_obs if obs.mode == mode]
        ax.scatter(
            [row.min_abs_eigenvalue for row in rows],
            [row.max_abs_chirality_near_window for row in rows],
            s=20,
            alpha=0.75,
            label=mode,
        )
    ax.axvline(result.config.near_zero_tol, color="tab:red", linestyle="--", linewidth=0.8)
    ax.set_xscale("log")
    ax.set_xlabel("min |eigenvalue|")
    ax.set_ylabel("max |<psi|Gamma|psi>| in near-zero window")
    ax.set_title("Near-zero chirality scatter")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_anticommutator_plot(result: DiracChiralityResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for mode in result.config.modes:
        rows = _final_rows(result, mode)
        ax.plot([row.disorder for row in rows], [row.max_anticommutator_error for row in rows], marker="s", label=mode)
    ax.axhline(result.config.algebra_tolerance, color="tab:red", linestyle="--", linewidth=0.8, label="tolerance")
    ax.set_yscale("log")
    ax.set_xlabel("disorder strength")
    ax.set_ylabel("max normalized ||{D,Gamma}||")
    ax.set_title("Chiral-block anticommutator diagnostic")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _final_rows(result: DiracChiralityResult, mode: str) -> list[DiracChiralityPoint]:
    return sorted(
        [point for point in result.points if point.size == result.final_size and point.mode == mode],
        key=lambda point: point.disorder,
    )


def _summary_lines(result: DiracChiralityResult, output_dir: Path) -> list[str]:
    return [
        "Toy Dirac/geometric chirality/index diagnostic using Gamma = diag(+I, -I).",
        "",
        f"Summary: {result.summary_statement}",
        f"Gamma algebra passed: {result.gamma_algebra_passed}.",
        f"Anticommutation preserved: {result.anticommutation_preserved}.",
        f"All numerical indices zero: {result.all_indices_zero}.",
        f"Any near-zero modes observed: {result.any_near_zero_modes}.",
        "",
        "## Final-Size Index Table",
        "",
        points_table(result),
        "",
        "## Mode Assessments",
        "",
        assessments_table(result),
        "",
        "Interpretation: a zero numerical index means near-zero modes are paired or accidental in this toy diagnostic.",
        "Non-claims: no physical chirality, no protected zero modes, no Witten/Lichnerowicz bypass, no covariant compactification proof, no SM fermion derivation.",
        f"Run directory: {output_dir}",
    ]
