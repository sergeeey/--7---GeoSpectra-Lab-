from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

from cc_toy_lab.runs import write_json, write_summary
from cc_toy_lab.spectral.metrics import inverse_participation_ratio, mean_adjacent_gap_ratio


GOE_R = 0.5307
POISSON_R = 0.3863


@dataclass(frozen=True)
class Anderson3DConfig:
    lattice_sizes: tuple[int, ...] = (4, 5, 6)
    disorder_values: tuple[float, ...] = (1.0, 4.0, 8.0, 12.0, 16.0, 24.0)
    realizations: int = 4
    seed: int = 42
    hopping: float = 1.0
    periodic: bool = False
    eigen_count: int = 48
    weak_reference_disorder: float = 4.0
    strong_reference_disorder: float = 24.0
    note: str = "3D cubic Anderson benchmark; localization diagnostic only"


@dataclass(frozen=True)
class Anderson3DPoint:
    lattice_size: int
    sites: int
    disorder: float
    mean_r: float
    stderr_r: float
    mean_ipr: float
    stderr_ipr: float
    realizations: int


@dataclass(frozen=True)
class Anderson3DBenchmarkResult:
    config: Anderson3DConfig
    by_size: dict[int, list[Anderson3DPoint]]
    weak_reference_r: float
    strong_reference_r: float
    weak_reference_ipr: float
    strong_reference_ipr: float
    weak_closer_to_goe: bool
    strong_closer_to_poisson_than_weak: bool
    ipr_increases: bool
    quick_basic_checks_passed: bool


def site_index(x: int, y: int, z: int, lattice_size: int) -> int:
    return x + lattice_size * (y + lattice_size * z)


def build_anderson_3d_hamiltonian(
    lattice_size: int = 4,
    disorder: float = 1.0,
    hopping: float = 1.0,
    seed: int | None = None,
    periodic: bool = False,
) -> sparse.csr_matrix:
    """Build a 3D cubic Anderson Hamiltonian with onsite box disorder.

    H_ij = epsilon_i delta_ij + t for nearest-neighbor lattice sites.
    Open boundaries are used by default to avoid extra periodic degeneracies in
    small quick-mode lattices.
    """
    if lattice_size < 2:
        raise ValueError("lattice_size must be >= 2")
    if disorder < 0:
        raise ValueError("disorder must be non-negative")
    sites = lattice_size**3
    rng = np.random.default_rng(seed)
    diagonal = rng.uniform(-disorder / 2.0, disorder / 2.0, size=sites)
    matrix = sparse.lil_matrix((sites, sites), dtype=float)
    matrix.setdiag(diagonal)

    for x in range(lattice_size):
        for y in range(lattice_size):
            for z in range(lattice_size):
                i = site_index(x, y, z, lattice_size)
                for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if nx < lattice_size and ny < lattice_size and nz < lattice_size:
                        j = site_index(nx, ny, nz, lattice_size)
                        matrix[i, j] = hopping
                        matrix[j, i] = hopping
                    elif periodic:
                        j = site_index(nx % lattice_size, ny % lattice_size, nz % lattice_size, lattice_size)
                        matrix[i, j] = hopping
                        matrix[j, i] = hopping
    return matrix.tocsr()


def central_eigensystem(
    hamiltonian: sparse.spmatrix,
    eigen_count: int = 48,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute eigenpairs nearest the band center.

    Dense diagonalization is used for the small quick-mode lattices. Sparse
    shift-invert is available for larger full-mode lattices.
    """
    size = hamiltonian.shape[0]
    if eigen_count < 8:
        raise ValueError("eigen_count must be >= 8")
    if size <= 260 or eigen_count >= size - 1:
        values, vectors = np.linalg.eigh(hamiltonian.toarray())
        center = len(values) // 2
        half = min(eigen_count // 2, center, len(values) - center)
        start = max(0, center - half)
        stop = min(len(values), center + half)
        return values[start:stop], vectors[:, start:stop]

    k = min(eigen_count, size - 2)
    values, vectors = eigsh(hamiltonian, k=k, sigma=0.0, which="LM")
    order = np.argsort(values)
    return values[order], vectors[:, order]


def analyze_anderson_3d_once(
    lattice_size: int,
    disorder: float,
    seed: int,
    hopping: float = 1.0,
    periodic: bool = False,
    eigen_count: int = 48,
) -> tuple[float, float]:
    hamiltonian = build_anderson_3d_hamiltonian(
        lattice_size=lattice_size,
        disorder=disorder,
        hopping=hopping,
        seed=seed,
        periodic=periodic,
    )
    eigenvalues, eigenvectors = central_eigensystem(hamiltonian, eigen_count=eigen_count)
    r_value = mean_adjacent_gap_ratio(eigenvalues)
    ipr = inverse_participation_ratio(eigenvectors)
    return float(r_value), float(np.mean(ipr))


def run_anderson_3d_benchmark(
    config: Anderson3DConfig,
    output_dir: Path | None = None,
) -> Anderson3DBenchmarkResult:
    by_size: dict[int, list[Anderson3DPoint]] = {}
    for lattice_size in config.lattice_sizes:
        points: list[Anderson3DPoint] = []
        for w_index, disorder in enumerate(config.disorder_values):
            r_values: list[float] = []
            ipr_values: list[float] = []
            for realization in range(config.realizations):
                run_seed = config.seed + 1_000_000 * lattice_size + 10_000 * w_index + realization
                r_value, ipr_value = analyze_anderson_3d_once(
                    lattice_size=lattice_size,
                    disorder=float(disorder),
                    seed=run_seed,
                    hopping=config.hopping,
                    periodic=config.periodic,
                    eigen_count=min(config.eigen_count, lattice_size**3 - 2),
                )
                if np.isfinite(r_value) and np.isfinite(ipr_value):
                    r_values.append(r_value)
                    ipr_values.append(ipr_value)
            points.append(_make_point(lattice_size, float(disorder), r_values, ipr_values))
        by_size[int(lattice_size)] = points

    largest_size = max(by_size)
    largest_points = by_size[largest_size]
    weak_point = _nearest_disorder_point(largest_points, config.weak_reference_disorder)
    strong_point = _nearest_disorder_point(largest_points, config.strong_reference_disorder)
    weak_goe_distance = abs(weak_point.mean_r - GOE_R)
    weak_poisson_distance = abs(weak_point.mean_r - POISSON_R)
    strong_goe_distance = abs(strong_point.mean_r - GOE_R)
    strong_poisson_distance = abs(strong_point.mean_r - POISSON_R)
    weak_closer_to_goe = weak_goe_distance < weak_poisson_distance
    strong_closer_to_poisson_than_weak = (
        strong_poisson_distance < weak_poisson_distance and strong_poisson_distance < strong_goe_distance
    )
    ipr_increases = strong_point.mean_ipr > weak_point.mean_ipr
    result = Anderson3DBenchmarkResult(
        config=config,
        by_size=by_size,
        weak_reference_r=weak_point.mean_r,
        strong_reference_r=strong_point.mean_r,
        weak_reference_ipr=weak_point.mean_ipr,
        strong_reference_ipr=strong_point.mean_ipr,
        weak_closer_to_goe=weak_closer_to_goe,
        strong_closer_to_poisson_than_weak=strong_closer_to_poisson_than_weak,
        ipr_increases=ipr_increases,
        quick_basic_checks_passed=weak_closer_to_goe and strong_closer_to_poisson_than_weak and ipr_increases,
    )
    if output_dir is not None:
        save_anderson_3d_artifacts(result=result, output_dir=output_dir)
    return result


def _make_point(lattice_size: int, disorder: float, r_values: list[float], ipr_values: list[float]) -> Anderson3DPoint:
    r_arr = np.asarray(r_values, dtype=float)
    ipr_arr = np.asarray(ipr_values, dtype=float)
    return Anderson3DPoint(
        lattice_size=int(lattice_size),
        sites=int(lattice_size**3),
        disorder=float(disorder),
        mean_r=float(np.mean(r_arr)),
        stderr_r=float(np.std(r_arr, ddof=1) / np.sqrt(len(r_arr))) if len(r_arr) > 1 else 0.0,
        mean_ipr=float(np.mean(ipr_arr)),
        stderr_ipr=float(np.std(ipr_arr, ddof=1) / np.sqrt(len(ipr_arr))) if len(ipr_arr) > 1 else 0.0,
        realizations=len(r_arr),
    )


def _nearest_disorder_point(points: list[Anderson3DPoint], disorder: float) -> Anderson3DPoint:
    return min(points, key=lambda point: abs(point.disorder - disorder))


def _basic_checks_passed(result: Anderson3DBenchmarkResult) -> bool:
    return result.weak_closer_to_goe and result.strong_closer_to_poisson_than_weak and result.ipr_increases


def save_anderson_3d_artifacts(result: Anderson3DBenchmarkResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "config.json", asdict(result.config))
    write_json(output_dir / "metrics.json", _metrics_payload(result))
    _save_data_npz(result, output_dir / "data.npz")
    _save_r_plot(result, figures_dir / "anderson_3d_r_statistics.png")
    _save_ipr_plot(result, figures_dir / "anderson_3d_ipr.png")
    write_summary(output_dir / "summary.md", "3D Anderson Benchmark Run", _summary_lines(result, output_dir))


def _metrics_payload(result: Anderson3DBenchmarkResult) -> dict:
    return {
        "points": [asdict(point) for size in sorted(result.by_size) for point in result.by_size[size]],
        "weak_reference_r": result.weak_reference_r,
        "strong_reference_r": result.strong_reference_r,
        "weak_reference_ipr": result.weak_reference_ipr,
        "strong_reference_ipr": result.strong_reference_ipr,
        "weak_closer_to_goe": result.weak_closer_to_goe,
        "strong_closer_to_poisson_than_weak": result.strong_closer_to_poisson_than_weak,
        "ipr_increases": result.ipr_increases,
        "quick_basic_checks_passed": result.quick_basic_checks_passed,
    }


def _save_data_npz(result: Anderson3DBenchmarkResult, path: Path) -> None:
    rows = [point for size in sorted(result.by_size) for point in result.by_size[size]]
    np.savez(
        path,
        lattice_size=np.asarray([point.lattice_size for point in rows], dtype=int),
        sites=np.asarray([point.sites for point in rows], dtype=int),
        disorder=np.asarray([point.disorder for point in rows], dtype=float),
        mean_r=np.asarray([point.mean_r for point in rows], dtype=float),
        stderr_r=np.asarray([point.stderr_r for point in rows], dtype=float),
        mean_ipr=np.asarray([point.mean_ipr for point in rows], dtype=float),
        stderr_ipr=np.asarray([point.stderr_ipr for point in rows], dtype=float),
        realizations=np.asarray([point.realizations for point in rows], dtype=int),
    )


def _save_r_plot(result: Anderson3DBenchmarkResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
    for size in sorted(result.by_size):
        points = result.by_size[size]
        w = np.asarray([point.disorder for point in points], dtype=float)
        mean = np.asarray([point.mean_r for point in points], dtype=float)
        err = np.asarray([point.stderr_r for point in points], dtype=float)
        ax.errorbar(w, mean, yerr=err, marker="o", capsize=3, label=f"L={size}")
    ax.axhline(GOE_R, color="black", linestyle="--", linewidth=1.0, label="GOE")
    ax.axhline(POISSON_R, color="black", linestyle=":", linewidth=1.0, label="Poisson")
    ax.set_xlabel("disorder W")
    ax.set_ylabel("mean adjacent-gap ratio <r>")
    ax.set_title("3D Anderson benchmark: r-statistics near band center")
    ax.legend()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _save_ipr_plot(result: Anderson3DBenchmarkResult, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
    for size in sorted(result.by_size):
        points = result.by_size[size]
        w = np.asarray([point.disorder for point in points], dtype=float)
        mean = np.asarray([point.mean_ipr for point in points], dtype=float)
        err = np.asarray([point.stderr_ipr for point in points], dtype=float)
        ax.errorbar(w, mean, yerr=err, marker="s", capsize=3, label=f"L={size}")
    ax.set_xlabel("disorder W")
    ax.set_ylabel("mean IPR near band center")
    ax.set_yscale("log")
    ax.set_title("3D Anderson benchmark: IPR near band center")
    ax.legend()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _summary_lines(result: Anderson3DBenchmarkResult, output_dir: Path) -> list[str]:
    lines = [
        "3D cubic Anderson benchmark with nearest-neighbor hopping and onsite box disorder.",
        "Open boundary conditions are used unless config.json says periodic=true.",
        "",
        results_table(result),
        "",
        f"Weak reference r={result.weak_reference_r:.4f}; strong reference r={result.strong_reference_r:.4f}.",
        f"Weak reference IPR={result.weak_reference_ipr:.6g}; strong reference IPR={result.strong_reference_ipr:.6g}.",
        f"Basic quick checks passed: {result.quick_basic_checks_passed}.",
        "Interpretation: this is a benchmark diagnostic, not proof of localization in the project model.",
        f"Run directory: {output_dir}",
    ]
    return lines


def results_table(result: Anderson3DBenchmarkResult) -> str:
    lines = [
        "| L | W | <r> | stderr_r | mean IPR | stderr_ipr | realizations |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for size in sorted(result.by_size):
        for point in result.by_size[size]:
            lines.append(
                f"| {point.lattice_size} | {point.disorder:.4g} | {point.mean_r:.4f} | "
                f"{point.stderr_r:.4f} | {point.mean_ipr:.6g} | {point.stderr_ipr:.2g} | "
                f"{point.realizations} |"
            )
    return "\n".join(lines)


def final_size_summary(result: Anderson3DBenchmarkResult) -> str:
    largest_size = max(result.by_size)
    points = result.by_size[largest_size]
    lines = [
        "| W | <r> | stderr_r | mean IPR | stderr_ipr |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for point in points:
        lines.append(
            f"| {point.disorder:.4g} | {point.mean_r:.4f} | {point.stderr_r:.4f} | "
            f"{point.mean_ipr:.6g} | {point.stderr_ipr:.2g} |"
        )
    return "\n".join(lines)
