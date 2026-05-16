from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import write_json, write_summary


@dataclass(frozen=True)
class MonopoleDiracConfig:
    """Configuration for the finite-mode S2 Dirac monopole index control."""

    q_values: tuple[int, ...] = (0, 1, 2)
    cutoffs: tuple[int, ...] = (1, 2)
    radius: float = 1.0
    zero_tolerance: float = 1e-8
    chirality_threshold: float = 0.5
    convention: str = "q>0 has positive-chirality zero modes; index=n_plus-n_minus=q"


@dataclass(frozen=True)
class MonopoleIndexResult:
    q: int
    cutoff: int
    expected_index: int
    numerical_index: int
    n_plus: int
    n_minus: int
    zero_modes: int
    ambiguous_zero_modes: int
    zero_tolerance: float
    smallest_abs_nonzero: float | None
    max_zero_abs_eigenvalue: float
    passed: bool


def monopole_singular_values(q: int, cutoff: int, radius: float = 1.0) -> np.ndarray:
    """Return positive S2 monopole Dirac singular values up to a finite cutoff.

    This finite-mode control uses the standard spectral pattern for the Dirac
    monopole toy model on S2: |q| zero modes and nonzero paired levels
    lambda_n = sqrt(n * (n + |q|)) / radius with degeneracy 2n + |q|,
    n = 1, ..., cutoff.
    """
    if cutoff < 1:
        raise ValueError("cutoff must be >= 1")
    if radius <= 0:
        raise ValueError("radius must be positive")
    abs_q = abs(int(q))
    values: list[float] = []
    for n in range(1, cutoff + 1):
        degeneracy = 2 * n + abs_q
        value = np.sqrt(n * (n + abs_q)) / radius
        values.extend([float(value)] * degeneracy)
    return np.asarray(values, dtype=float)


def build_dirac_monopole_operator(
    q: int,
    cutoff: int,
    radius: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Build a finite-mode chiral S2 Dirac monopole toy operator.

    The operator is represented in a chiral basis with Gamma = diag(+1, -1)
    and D = [[0, A^T], [A, 0]]. Positive and negative nonzero modes are paired.
    The rectangular off-diagonal block carries |q| exact zero modes in the
    chirality selected by q. Under this explicit convention:

    - q > 0 gives q positive-chirality zero modes.
    - q < 0 gives |q| negative-chirality zero modes.
    - index(D) = n_plus - n_minus = q.

    This is a finite-mode index-pipeline control, not a continuum discretization
    and not a physical compactification calculation.
    """
    q = int(q)
    singular_values = monopole_singular_values(q=q, cutoff=cutoff, radius=radius)
    paired_count = len(singular_values)
    plus_zero = max(q, 0)
    minus_zero = max(-q, 0)
    plus_dim = plus_zero + paired_count
    minus_dim = minus_zero + paired_count
    total_dim = plus_dim + minus_dim

    operator = np.zeros((total_dim, total_dim), dtype=float)
    plus_pair_start = plus_zero
    minus_pair_start = plus_dim + minus_zero
    for idx, value in enumerate(singular_values):
        plus_idx = plus_pair_start + idx
        minus_idx = minus_pair_start + idx
        operator[plus_idx, minus_idx] = value
        operator[minus_idx, plus_idx] = value

    chirality = np.concatenate([np.ones(plus_dim), -np.ones(minus_dim)])
    return operator, chirality


def analyze_monopole_charge(
    q: int,
    cutoff: int,
    radius: float = 1.0,
    zero_tolerance: float = 1e-8,
    chirality_threshold: float = 0.5,
) -> MonopoleIndexResult:
    """Compute the numerical index for one monopole charge and cutoff."""
    operator, chirality = build_dirac_monopole_operator(q=q, cutoff=cutoff, radius=radius)
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    abs_eigenvalues = np.abs(eigenvalues)
    zero_mask = abs_eigenvalues <= zero_tolerance
    zero_indices = np.flatnonzero(zero_mask)

    gamma_v = chirality[:, None] * eigenvectors
    chirality_expectations = np.real(np.sum(eigenvectors * gamma_v, axis=0))
    zero_chiralities = chirality_expectations[zero_indices]
    n_plus = int(np.count_nonzero(zero_chiralities >= chirality_threshold))
    n_minus = int(np.count_nonzero(zero_chiralities <= -chirality_threshold))
    ambiguous = int(len(zero_chiralities) - n_plus - n_minus)
    numerical_index = n_plus - n_minus
    expected_index = int(q)
    nonzero_abs = abs_eigenvalues[~zero_mask]
    smallest_nonzero = float(np.min(nonzero_abs)) if len(nonzero_abs) else None
    max_zero_abs = float(np.max(abs_eigenvalues[zero_mask])) if len(zero_indices) else 0.0
    passed = numerical_index == expected_index and ambiguous == 0
    return MonopoleIndexResult(
        q=int(q),
        cutoff=int(cutoff),
        expected_index=expected_index,
        numerical_index=numerical_index,
        n_plus=n_plus,
        n_minus=n_minus,
        zero_modes=int(len(zero_indices)),
        ambiguous_zero_modes=ambiguous,
        zero_tolerance=float(zero_tolerance),
        smallest_abs_nonzero=smallest_nonzero,
        max_zero_abs_eigenvalue=max_zero_abs,
        passed=bool(passed),
    )


def evaluate_index_controls(config: MonopoleDiracConfig) -> dict[int, list[MonopoleIndexResult]]:
    """Evaluate monopole index controls over charges and cutoffs."""
    results: dict[int, list[MonopoleIndexResult]] = {}
    for q in config.q_values:
        results[int(q)] = [
            analyze_monopole_charge(
                q=int(q),
                cutoff=int(cutoff),
                radius=config.radius,
                zero_tolerance=config.zero_tolerance,
                chirality_threshold=config.chirality_threshold,
            )
            for cutoff in config.cutoffs
        ]
    return results


def results_table(results: dict[int, list[MonopoleIndexResult]]) -> str:
    lines = [
        "| q | cutoff | expected index | numerical index | n_plus | n_minus | zero modes | passed |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for q in sorted(results):
        for result in results[q]:
            lines.append(
                f"| {result.q} | {result.cutoff} | {result.expected_index} | "
                f"{result.numerical_index} | {result.n_plus} | {result.n_minus} | "
                f"{result.zero_modes} | {result.passed} |"
            )
    return "\n".join(lines)


def final_cutoff_results(results: dict[int, list[MonopoleIndexResult]]) -> dict[int, MonopoleIndexResult]:
    return {q: values[-1] for q, values in results.items()}


def all_controls_passed(results: dict[int, list[MonopoleIndexResult]]) -> bool:
    return all(result.passed for values in results.values() for result in values)


def save_index_artifacts(
    config: MonopoleDiracConfig,
    results: dict[int, list[MonopoleIndexResult]],
    output_dir: Path,
) -> None:
    """Save config, metrics, data, figures, and markdown summary."""
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    flat_results = [result for q in sorted(results) for result in results[q]]
    write_json(output_dir / "config.json", asdict(config))
    write_json(output_dir / "metrics.json", {"results": [asdict(result) for result in flat_results]})

    qs: list[int] = []
    cutoffs: list[int] = []
    expected: list[int] = []
    numerical: list[int] = []
    n_plus: list[int] = []
    n_minus: list[int] = []
    for result in flat_results:
        qs.append(result.q)
        cutoffs.append(result.cutoff)
        expected.append(result.expected_index)
        numerical.append(result.numerical_index)
        n_plus.append(result.n_plus)
        n_minus.append(result.n_minus)
    np.savez(
        output_dir / "data.npz",
        q=np.asarray(qs, dtype=int),
        cutoff=np.asarray(cutoffs, dtype=int),
        expected_index=np.asarray(expected, dtype=int),
        numerical_index=np.asarray(numerical, dtype=int),
        n_plus=np.asarray(n_plus, dtype=int),
        n_minus=np.asarray(n_minus, dtype=int),
    )

    _save_eigenvalue_plot(config=config, results=results, figures_dir=figures_dir)
    _save_index_plot(results=results, figures_dir=figures_dir)

    lines = [
        "Finite-mode S2 Dirac monopole index control.",
        "",
        f"Convention: {config.convention}.",
        "",
        results_table(results),
        "",
        "This validates the index-counting pipeline on a known toy spectral model only.",
        "It does not prove chiral fermions in covariant compactification.",
    ]
    write_summary(output_dir / "summary.md", "S2 Dirac Monopole Index Run", lines)


def _save_eigenvalue_plot(
    config: MonopoleDiracConfig,
    results: dict[int, list[MonopoleIndexResult]],
    figures_dir: Path,
) -> None:
    final_results = final_cutoff_results(results)
    fig, axes = plt.subplots(len(final_results), 1, figsize=(8, 2.2 * len(final_results)), constrained_layout=True)
    if len(final_results) == 1:
        axes = [axes]
    for ax, q in zip(axes, sorted(final_results)):
        result = final_results[q]
        operator, _chirality = build_dirac_monopole_operator(q=q, cutoff=result.cutoff, radius=config.radius)
        eigenvalues = np.linalg.eigvalsh(operator)
        window = eigenvalues[np.abs(eigenvalues) <= 4.0]
        ax.scatter(np.arange(len(window)), window, s=14)
        ax.axhline(config.zero_tolerance, color="tab:red", linestyle="--", linewidth=0.8)
        ax.axhline(-config.zero_tolerance, color="tab:red", linestyle="--", linewidth=0.8)
        ax.set_title(f"q={q}, cutoff={result.cutoff}, index={result.numerical_index}")
        ax.set_ylabel("eigenvalue")
        ax.set_xlabel("near-zero eigenvalue index")
    fig.savefig(figures_dir / "dirac_monopole_s2_eigenvalues.png", dpi=160)
    plt.close(fig)


def _save_index_plot(results: dict[int, list[MonopoleIndexResult]], figures_dir: Path) -> None:
    final_results = final_cutoff_results(results)
    qs = np.asarray(sorted(final_results), dtype=int)
    expected = np.asarray([final_results[int(q)].expected_index for q in qs], dtype=int)
    numerical = np.asarray([final_results[int(q)].numerical_index for q in qs], dtype=int)
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    ax.plot(qs, expected, "o-", label="expected index")
    ax.plot(qs, numerical, "s--", label="numerical index")
    ax.set_xlabel("monopole charge q")
    ax.set_ylabel("index n_plus - n_minus")
    ax.set_title("S2 Dirac monopole index control")
    ax.legend()
    fig.savefig(figures_dir / "dirac_monopole_s2_index.png", dpi=160)
    plt.close(fig)


def format_cli_table(results: dict[int, list[MonopoleIndexResult]]) -> str:
    final_results = final_cutoff_results(results)
    lines = ["q | cutoff | expected | numerical | n_plus | n_minus | passed"]
    for q in sorted(final_results):
        result = final_results[q]
        lines.append(
            f"q={result.q} | cutoff={result.cutoff} | expected={result.expected_index} | "
            f"numerical={result.numerical_index} | n_plus={result.n_plus} | "
            f"n_minus={result.n_minus} | passed={result.passed}"
        )
    return "\n".join(lines)

