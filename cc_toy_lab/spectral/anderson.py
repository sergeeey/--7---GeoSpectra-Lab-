from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

from cc_toy_lab.spectral.metrics import inverse_participation_ratio, mean_adjacent_gap_ratio


@dataclass(frozen=True)
class AndersonPoint:
    disorder: float
    mean_r: float
    stderr_r: float
    mean_ipr: float
    stderr_ipr: float
    realizations: int


@dataclass(frozen=True)
class AndersonSweep:
    by_size: dict[int, list[AndersonPoint]]


def build_anderson_hamiltonian(
    size: int = 512,
    disorder: float = 1.0,
    hopping: float = 1.0,
    seed: int | None = None,
    periodic: bool = True,
) -> sparse.csr_matrix:
    """1D Anderson tight-binding Hamiltonian with onsite disorder."""
    if size < 4:
        raise ValueError("size must be >= 4")
    rng = np.random.default_rng(seed)
    diagonal = rng.uniform(-disorder / 2.0, disorder / 2.0, size=size)
    off = np.full(size - 1, hopping, dtype=float)
    matrix = sparse.diags([off, diagonal, off], offsets=[-1, 0, 1], format="lil")
    if periodic:
        matrix[0, size - 1] = hopping
        matrix[size - 1, 0] = hopping
    return matrix.tocsr()


def _central_eigensystem(matrix: sparse.spmatrix, window_fraction: float = 0.4) -> tuple[np.ndarray, np.ndarray]:
    size = matrix.shape[0]
    if size <= 192:
        values, vectors = np.linalg.eigh(matrix.toarray())
    else:
        k = min(max(48, size // 4), size - 2)
        values, vectors = eigsh(matrix, k=k, sigma=0.0, which="LM")
        order = np.argsort(values)
        values = values[order]
        vectors = vectors[:, order]

    half_width = (float(values[-1]) - float(values[0])) * window_fraction / 2.0
    mask = (values >= -half_width) & (values <= half_width)
    if np.count_nonzero(mask) < 8:
        return values, vectors
    return values[mask], vectors[:, mask]


def analyze_anderson_once(
    size: int,
    disorder: float,
    seed: int,
    window_fraction: float = 0.4,
) -> tuple[float, float]:
    hamiltonian = build_anderson_hamiltonian(size=size, disorder=disorder, seed=seed)
    values, vectors = _central_eigensystem(hamiltonian, window_fraction=window_fraction)
    r_value = mean_adjacent_gap_ratio(values)
    ipr_values = inverse_participation_ratio(vectors)
    return float(r_value), float(np.mean(ipr_values))


def run_anderson_sweep(
    sizes: list[int] | tuple[int, ...] = (512,),
    disorder_values: list[float] | np.ndarray | tuple[float, ...] = tuple(np.linspace(0.5, 30.0, 30)),
    realizations: int = 30,
    seed: int = 42,
    window_fraction: float = 0.4,
) -> AndersonSweep:
    by_size: dict[int, list[AndersonPoint]] = {}
    for size in sizes:
        points: list[AndersonPoint] = []
        for w_index, disorder in enumerate(disorder_values):
            r_values: list[float] = []
            ipr_values: list[float] = []
            for realization in range(realizations):
                run_seed = seed + 100_000 * int(size) + 1_000 * w_index + realization
                r_value, ipr_value = analyze_anderson_once(
                    size=size,
                    disorder=float(disorder),
                    seed=run_seed,
                    window_fraction=window_fraction,
                )
                if not np.isnan(r_value):
                    r_values.append(r_value)
                    ipr_values.append(ipr_value)
            r_arr = np.asarray(r_values, dtype=float)
            ipr_arr = np.asarray(ipr_values, dtype=float)
            points.append(
                AndersonPoint(
                    disorder=float(disorder),
                    mean_r=float(np.mean(r_arr)),
                    stderr_r=float(np.std(r_arr, ddof=1) / np.sqrt(max(len(r_arr), 1))) if len(r_arr) > 1 else 0.0,
                    mean_ipr=float(np.mean(ipr_arr)),
                    stderr_ipr=float(np.std(ipr_arr, ddof=1) / np.sqrt(max(len(ipr_arr), 1))) if len(ipr_arr) > 1 else 0.0,
                    realizations=len(r_arr),
                )
            )
        by_size[int(size)] = points
    return AndersonSweep(by_size=by_size)
