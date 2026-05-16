from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import write_json, write_summary
from cc_toy_lab.spectral.dirac_monopole_s2 import build_dirac_monopole_operator


@dataclass(frozen=True)
class S2GraphProductConfig:
    q_values: tuple[int, ...] = (1, 2)
    cutoff: int = 2
    graph_sizes: tuple[int, ...] = (8, 12)
    disorder_values: tuple[float, ...] = (0.0, 2.0, 8.0)
    perturbation_values: tuple[float, ...] = (0.0, 1e-5)
    realizations: int = 3
    seed: int = 11117
    zero_tolerance: float = 1e-7
    chirality_threshold: float = 0.5
    algebra_tolerance: float = 1e-8
    hopping: float = 1.0
    note: str = (
        "Intermediate finite-mode S2 monopole x graph toy model. The graph sector "
        "is a localization selector inside an index-carrying zero-mode sector, "
        "not a physical compactification result."
    )


@dataclass(frozen=True)
class S2GraphObservation:
    q: int
    cutoff: int
    graph_size: int
    disorder: float
    perturbation: float
    seed: int
    expected_index: int
    numerical_index: int
    n_plus: int
    n_minus: int
    zero_modes: int
    ambiguous_zero_modes: int
    index_passed: bool
    gamma_square_error: float
    gamma_hermitian_error: float
    anticommutator_error: float
    graph_selector_mean_ipr: float
    graph_selector_max_ipr: float
    min_abs_eigenvalue: float
    max_zero_abs_eigenvalue: float
    classification: str


@dataclass(frozen=True)
class S2GraphPoint:
    q: int
    cutoff: int
    graph_size: int
    disorder: float
    perturbation: float
    expected_index: int
    mean_index: float
    min_index: int
    max_index: int
    mean_zero_modes: float
    mean_n_plus: float
    mean_n_minus: float
    max_anticommutator_error: float
    mean_selector_ipr: float
    max_selector_ipr: float
    index_pass_rate: float
    realizations: int
    classifications: tuple[str, ...]


@dataclass(frozen=True)
class S2GraphAssessment:
    q: int
    graph_size: int
    weak_disorder: float
    strong_disorder: float
    perturbation: float
    weak_ipr: float
    strong_ipr: float
    expected_index: int
    weak_index: float
    strong_index: float
    index_stable: bool
    ipr_increases: bool
    anticommutator_preserved: bool
    classification: str


@dataclass(frozen=True)
class S2GraphProductResult:
    config: S2GraphProductConfig
    observations: list[S2GraphObservation]
    points: list[S2GraphPoint]
    assessments: list[S2GraphAssessment]
    all_index_checks_passed: bool
    all_anticommutators_preserved: bool
    ipr_growth_observed: bool
    summary_statement: str


def build_graph_selector(
    graph_size: int,
    disorder: float,
    seed: int,
    hopping: float = 1.0,
) -> np.ndarray:
    """Build an open-chain Anderson selector for the graph factor."""
    if graph_size < 2:
        raise ValueError("graph_size must be >= 2")
    if disorder < 0:
        raise ValueError("disorder must be non-negative")
    rng = np.random.default_rng(seed)
    matrix = np.zeros((graph_size, graph_size), dtype=float)
    if disorder:
        matrix[np.diag_indices(graph_size)] = rng.uniform(-disorder / 2.0, disorder / 2.0, graph_size)
    for i in range(graph_size - 1):
        matrix[i, i + 1] = hopping
        matrix[i + 1, i] = hopping
    return matrix


def graph_selector_ipr(graph_size: int, disorder: float, seed: int, hopping: float = 1.0) -> tuple[float, float]:
    selector = build_graph_selector(graph_size=graph_size, disorder=disorder, seed=seed, hopping=hopping)
    _values, vectors = np.linalg.eigh(selector)
    ipr = np.sum(np.abs(vectors) ** 4, axis=0)
    return float(np.mean(ipr)), float(np.max(ipr))


def build_s2_graph_product_operator(
    q: int,
    cutoff: int,
    graph_size: int,
    perturbation: float = 0.0,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Build a finite S2 monopole x graph product toy operator.

    The base operator is `D_S2(q) ⊗ I_graph`. Optional perturbations are
    off-diagonal in the chiral block and therefore preserve `{D, Gamma}=0`.
    Because the off-diagonal block is rectangular when `q != 0`, the index is
    stable under generic chiral perturbations. This is a finite-mode toy bridge,
    not a continuum product-geometry calculation.
    """
    if graph_size < 2:
        raise ValueError("graph_size must be >= 2")
    if perturbation < 0:
        raise ValueError("perturbation must be non-negative")
    s2_operator, s2_chirality = build_dirac_monopole_operator(q=q, cutoff=cutoff)
    product_operator = np.kron(s2_operator, np.eye(graph_size))
    product_chirality = np.kron(s2_chirality, np.ones(graph_size))
    if perturbation > 0:
        rng = np.random.default_rng(seed)
        plus = np.flatnonzero(product_chirality > 0)
        minus = np.flatnonzero(product_chirality < 0)
        random_block = rng.normal(0.0, perturbation / np.sqrt(max(1, len(minus))), size=(len(plus), len(minus)))
        perturbation_operator = np.zeros_like(product_operator)
        perturbation_operator[np.ix_(plus, minus)] = random_block
        perturbation_operator[np.ix_(minus, plus)] = random_block.T
        product_operator = product_operator + perturbation_operator
    return product_operator, product_chirality


def analyze_s2_graph_product(
    q: int,
    cutoff: int,
    graph_size: int,
    disorder: float,
    perturbation: float,
    seed: int,
    zero_tolerance: float = 1e-7,
    chirality_threshold: float = 0.5,
    algebra_tolerance: float = 1e-8,
    hopping: float = 1.0,
) -> S2GraphObservation:
    operator, chirality = build_s2_graph_product_operator(
        q=q,
        cutoff=cutoff,
        graph_size=graph_size,
        perturbation=perturbation,
        seed=seed,
    )
    gamma = np.diag(chirality)
    identity = np.eye(gamma.shape[0])
    op_scale = max(1.0, float(np.linalg.norm(operator, ord="fro")))
    gamma_scale = max(1.0, float(np.linalg.norm(gamma, ord="fro")))
    gamma_square_error = float(np.linalg.norm(gamma @ gamma - identity, ord="fro") / gamma_scale)
    gamma_hermitian_error = float(np.linalg.norm(gamma - gamma.T, ord="fro") / gamma_scale)
    anticommutator_error = float(np.linalg.norm(operator @ gamma + gamma @ operator, ord="fro") / op_scale)

    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    abs_values = np.abs(eigenvalues)
    zero_indices = np.flatnonzero(abs_values <= zero_tolerance)
    gamma_vectors = gamma @ eigenvectors
    chiralities = np.real(np.einsum("ij,ij->j", np.conj(eigenvectors), gamma_vectors))
    zero_chiralities = chiralities[zero_indices]
    n_plus = int(np.count_nonzero(zero_chiralities >= chirality_threshold))
    n_minus = int(np.count_nonzero(zero_chiralities <= -chirality_threshold))
    ambiguous = int(len(zero_chiralities) - n_plus - n_minus)
    numerical_index = n_plus - n_minus
    expected_index = int(q) * int(graph_size)
    selector_mean_ipr, selector_max_ipr = graph_selector_ipr(
        graph_size=graph_size,
        disorder=disorder,
        seed=seed,
        hopping=hopping,
    )
    index_passed = numerical_index == expected_index and ambiguous == 0
    classification = _classify(index_passed, anticommutator_error, algebra_tolerance, numerical_index)
    max_zero_abs = float(np.max(abs_values[zero_indices])) if len(zero_indices) else 0.0
    return S2GraphObservation(
        q=int(q),
        cutoff=int(cutoff),
        graph_size=int(graph_size),
        disorder=float(disorder),
        perturbation=float(perturbation),
        seed=int(seed),
        expected_index=expected_index,
        numerical_index=int(numerical_index),
        n_plus=n_plus,
        n_minus=n_minus,
        zero_modes=int(len(zero_indices)),
        ambiguous_zero_modes=ambiguous,
        index_passed=bool(index_passed),
        gamma_square_error=gamma_square_error,
        gamma_hermitian_error=gamma_hermitian_error,
        anticommutator_error=anticommutator_error,
        graph_selector_mean_ipr=selector_mean_ipr,
        graph_selector_max_ipr=selector_max_ipr,
        min_abs_eigenvalue=float(np.min(abs_values)),
        max_zero_abs_eigenvalue=max_zero_abs,
        classification=classification,
    )


def run_s2_graph_product_benchmark(
    config: S2GraphProductConfig,
    output_dir: Path | None = None,
) -> S2GraphProductResult:
    observations: list[S2GraphObservation] = []
    for q in config.q_values:
        for graph_size in config.graph_sizes:
            for disorder_index, disorder in enumerate(config.disorder_values):
                for perturbation_index, perturbation in enumerate(config.perturbation_values):
                    for realization in range(config.realizations):
                        run_seed = (
                            config.seed
                            + 1_000_000 * int(q + 10)
                            + 10_000 * int(graph_size)
                            + 1_000 * disorder_index
                            + 100 * perturbation_index
                            + realization
                        )
                        observations.append(
                            analyze_s2_graph_product(
                                q=int(q),
                                cutoff=config.cutoff,
                                graph_size=int(graph_size),
                                disorder=float(disorder),
                                perturbation=float(perturbation),
                                seed=run_seed,
                                zero_tolerance=config.zero_tolerance,
                                chirality_threshold=config.chirality_threshold,
                                algebra_tolerance=config.algebra_tolerance,
                                hopping=config.hopping,
                            )
                        )
    points = _aggregate_points(observations)
    assessments = _assess(points, config)
    all_index = all(obs.index_passed for obs in observations)
    all_anticomm = all(obs.anticommutator_error < config.algebra_tolerance for obs in observations)
    ipr_growth = any(assessment.ipr_increases for assessment in assessments)
    summary = (
        f"Index checks passed={all_index}; anticommutators preserved={all_anticomm}; "
        f"IPR growth observed={ipr_growth}. This is an intermediate S2 x graph toy bridge, "
        "not a physical compactification result."
    )
    result = S2GraphProductResult(
        config=config,
        observations=observations,
        points=points,
        assessments=assessments,
        all_index_checks_passed=all_index,
        all_anticommutators_preserved=all_anticomm,
        ipr_growth_observed=ipr_growth,
        summary_statement=summary,
    )
    if output_dir is not None:
        save_s2_graph_artifacts(result, output_dir)
    return result


def save_s2_graph_artifacts(result: S2GraphProductResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "config.json", asdict(result.config))
    write_json(output_dir / "metrics.json", _metrics_payload(result))
    _save_npz(result, output_dir / "data.npz")
    _save_index_plot(result, figures_dir / "index_vs_disorder.png")
    _save_ipr_plot(result, figures_dir / "zero_mode_ipr_vs_disorder.png")
    _save_perturbation_plot(result, figures_dir / "perturbation_stability.png")
    _save_chirality_counts_plot(result, figures_dir / "chirality_counts.png")
    write_summary(output_dir / "summary.md", "S2 x Graph Intermediate Index-Localization Benchmark", _summary_lines(result, output_dir))


def points_table(result: S2GraphProductResult) -> str:
    lines = [
        "| q | graph N | W | perturbation | expected index | mean index | zero modes | selector IPR | pass rate | classification |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for point in sorted(result.points, key=lambda item: (item.q, item.graph_size, item.perturbation, item.disorder)):
        lines.append(
            f"| {point.q} | {point.graph_size} | {point.disorder:.4g} | {point.perturbation:.2g} | "
            f"{point.expected_index} | {point.mean_index:.4g} | {point.mean_zero_modes:.4g} | "
            f"{point.mean_selector_ipr:.6g} | {point.index_pass_rate:.3g} | {', '.join(point.classifications)} |"
        )
    return "\n".join(lines)


def assessments_table(result: S2GraphProductResult) -> str:
    lines = [
        "| q | graph N | perturbation | weak W | strong W | expected index | weak index | strong index | weak IPR | strong IPR | index stable | IPR increases | classification |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for assessment in sorted(result.assessments, key=lambda item: (item.q, item.graph_size, item.perturbation)):
        lines.append(
            f"| {assessment.q} | {assessment.graph_size} | {assessment.perturbation:.2g} | "
            f"{assessment.weak_disorder:.4g} | {assessment.strong_disorder:.4g} | {assessment.expected_index} | "
            f"{assessment.weak_index:.4g} | {assessment.strong_index:.4g} | "
            f"{assessment.weak_ipr:.6g} | {assessment.strong_ipr:.6g} | "
            f"{assessment.index_stable} | {assessment.ipr_increases} | {assessment.classification} |"
        )
    return "\n".join(lines)


def _classify(index_passed: bool, anticommutator_error: float, tolerance: float, numerical_index: int) -> str:
    if anticommutator_error >= tolerance:
        return "unresolved_chiral_structure_broken"
    if index_passed and numerical_index != 0:
        return "index_positive_toy_signal"
    if index_passed:
        return "zero_index_control"
    return "index_failure"


def _aggregate_points(observations: list[S2GraphObservation]) -> list[S2GraphPoint]:
    keys = sorted({(obs.q, obs.graph_size, obs.disorder, obs.perturbation) for obs in observations})
    points: list[S2GraphPoint] = []
    for q, graph_size, disorder, perturbation in keys:
        rows = [
            obs
            for obs in observations
            if obs.q == q
            and obs.graph_size == graph_size
            and np.isclose(obs.disorder, disorder)
            and np.isclose(obs.perturbation, perturbation)
        ]
        indexes = np.asarray([row.numerical_index for row in rows], dtype=float)
        points.append(
            S2GraphPoint(
                q=int(q),
                cutoff=rows[0].cutoff,
                graph_size=int(graph_size),
                disorder=float(disorder),
                perturbation=float(perturbation),
                expected_index=rows[0].expected_index,
                mean_index=float(np.mean(indexes)),
                min_index=int(np.min(indexes)),
                max_index=int(np.max(indexes)),
                mean_zero_modes=float(np.mean([row.zero_modes for row in rows])),
                mean_n_plus=float(np.mean([row.n_plus for row in rows])),
                mean_n_minus=float(np.mean([row.n_minus for row in rows])),
                max_anticommutator_error=float(np.max([row.anticommutator_error for row in rows])),
                mean_selector_ipr=float(np.mean([row.graph_selector_mean_ipr for row in rows])),
                max_selector_ipr=float(np.max([row.graph_selector_max_ipr for row in rows])),
                index_pass_rate=float(np.mean([row.index_passed for row in rows])),
                realizations=len(rows),
                classifications=tuple(sorted({row.classification for row in rows})),
            )
        )
    return points


def _assess(points: list[S2GraphPoint], config: S2GraphProductConfig) -> list[S2GraphAssessment]:
    assessments: list[S2GraphAssessment] = []
    weak_disorder = min(config.disorder_values)
    strong_disorder = max(config.disorder_values)
    for q in config.q_values:
        for graph_size in config.graph_sizes:
            for perturbation in config.perturbation_values:
                rows = [
                    point
                    for point in points
                    if point.q == q and point.graph_size == graph_size and np.isclose(point.perturbation, perturbation)
                ]
                weak = min(rows, key=lambda point: abs(point.disorder - weak_disorder))
                strong = min(rows, key=lambda point: abs(point.disorder - strong_disorder))
                index_stable = all(point.index_pass_rate == 1.0 and point.mean_index == point.expected_index for point in rows)
                anticommutator_preserved = all(point.max_anticommutator_error < config.algebra_tolerance for point in rows)
                ipr_increases = strong.mean_selector_ipr > weak.mean_selector_ipr
                classification = "index_and_localization_toy_signal" if index_stable and ipr_increases else "unresolved_or_no_localization_growth"
                assessments.append(
                    S2GraphAssessment(
                        q=int(q),
                        graph_size=int(graph_size),
                        weak_disorder=weak.disorder,
                        strong_disorder=strong.disorder,
                        perturbation=float(perturbation),
                        weak_ipr=weak.mean_selector_ipr,
                        strong_ipr=strong.mean_selector_ipr,
                        expected_index=weak.expected_index,
                        weak_index=weak.mean_index,
                        strong_index=strong.mean_index,
                        index_stable=index_stable,
                        ipr_increases=ipr_increases,
                        anticommutator_preserved=anticommutator_preserved,
                        classification=classification,
                    )
                )
    return assessments


def _metrics_payload(result: S2GraphProductResult) -> dict:
    return {
        "observations": [asdict(obs) for obs in result.observations],
        "points": [asdict(point) for point in result.points],
        "assessments": [asdict(assessment) for assessment in result.assessments],
        "all_index_checks_passed": result.all_index_checks_passed,
        "all_anticommutators_preserved": result.all_anticommutators_preserved,
        "ipr_growth_observed": result.ipr_growth_observed,
        "summary_statement": result.summary_statement,
        "negative_control": "Toy Dirac localization v0.1.10: near-zero modes have zero numerical index.",
        "positive_control": "S2 Dirac monopole finite-mode index control: index(D)=q.",
        "scientific_warning": (
            "S2 x graph is an intermediate toy bridge. Graph localization is a selector in an "
            "index-carrying zero-mode sector and is not a physical compactification result."
        ),
    }


def _save_npz(result: S2GraphProductResult, path: Path) -> None:
    obs = result.observations
    np.savez(
        path,
        q=np.asarray([row.q for row in obs], dtype=int),
        graph_size=np.asarray([row.graph_size for row in obs], dtype=int),
        disorder=np.asarray([row.disorder for row in obs], dtype=float),
        perturbation=np.asarray([row.perturbation for row in obs], dtype=float),
        expected_index=np.asarray([row.expected_index for row in obs], dtype=int),
        numerical_index=np.asarray([row.numerical_index for row in obs], dtype=int),
        zero_modes=np.asarray([row.zero_modes for row in obs], dtype=int),
        selector_ipr=np.asarray([row.graph_selector_mean_ipr for row in obs], dtype=float),
    )


def _save_index_plot(result: S2GraphProductResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for q in result.config.q_values:
        rows = [p for p in result.points if p.q == q and p.perturbation == result.config.perturbation_values[0]]
        rows = sorted(rows, key=lambda p: (p.graph_size, p.disorder))
        for graph_size in sorted({p.graph_size for p in rows}):
            subset = [p for p in rows if p.graph_size == graph_size]
            ax.plot([p.disorder for p in subset], [p.mean_index for p in subset], marker="o", label=f"q={q}, N={graph_size}")
    ax.set_xlabel("graph disorder W")
    ax.set_ylabel("numerical index")
    ax.set_title("S2 x graph product index")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_ipr_plot(result: S2GraphProductResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for q in result.config.q_values:
        rows = [p for p in result.points if p.q == q and p.perturbation == result.config.perturbation_values[0]]
        for graph_size in sorted({p.graph_size for p in rows}):
            subset = sorted([p for p in rows if p.graph_size == graph_size], key=lambda p: p.disorder)
            ax.plot([p.disorder for p in subset], [p.mean_selector_ipr for p in subset], marker="s", label=f"q={q}, N={graph_size}")
    ax.set_xlabel("graph disorder W")
    ax.set_ylabel("mean graph selector IPR")
    ax.set_title("Localization selector inside index-carrying zero sector")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_perturbation_plot(result: S2GraphProductResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    strong_w = max(result.config.disorder_values)
    rows = [p for p in result.points if np.isclose(p.disorder, strong_w)]
    for q in result.config.q_values:
        for graph_size in result.config.graph_sizes:
            subset = sorted([p for p in rows if p.q == q and p.graph_size == graph_size], key=lambda p: p.perturbation)
            ax.plot([p.perturbation for p in subset], [p.mean_index for p in subset], marker="o", label=f"q={q}, N={graph_size}")
    ax.set_xscale("symlog", linthresh=1e-8)
    ax.set_xlabel("chiral off-diagonal perturbation")
    ax.set_ylabel("mean numerical index at strong W")
    ax.set_title("Index stability under chiral perturbations")
    ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_chirality_counts_plot(result: S2GraphProductResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    rows = [p for p in result.points if p.perturbation == result.config.perturbation_values[0]]
    labels = []
    plus_values = []
    minus_values = []
    for point in sorted(rows, key=lambda p: (p.q, p.graph_size, p.disorder)):
        if point.disorder != min(result.config.disorder_values):
            continue
        labels.append(f"q={point.q}\nN={point.graph_size}")
        plus_values.append(point.mean_n_plus)
        minus_values.append(point.mean_n_minus)
    x = np.arange(len(labels))
    ax.bar(x - 0.2, plus_values, width=0.4, label="n_plus")
    ax.bar(x + 0.2, minus_values, width=0.4, label="n_minus")
    ax.set_xticks(x, labels)
    ax.set_ylabel("zero-mode chirality count")
    ax.set_title("S2 x graph chirality counts")
    ax.legend()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _summary_lines(result: S2GraphProductResult, output_dir: Path) -> list[str]:
    return [
        "Intermediate S2 monopole x graph toy benchmark.",
        "",
        f"Summary: {result.summary_statement}",
        f"All index checks passed: {result.all_index_checks_passed}.",
        f"All anticommutators preserved: {result.all_anticommutators_preserved}.",
        f"IPR growth observed: {result.ipr_growth_observed}.",
        "",
        "## Points",
        "",
        points_table(result),
        "",
        "## Assessments",
        "",
        assessments_table(result),
        "",
        "Interpretation: this is a finite-mode bridge from positive S2 monopole index control to a graph localization selector.",
        "Non-claims: no S6/S3xS6 result, no physical compactification, no Standard Model fermion derivation.",
        f"Run directory: {output_dir}",
    ]
