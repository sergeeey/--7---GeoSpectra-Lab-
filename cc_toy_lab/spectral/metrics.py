from __future__ import annotations

import numpy as np


def level_spacings(levels: np.ndarray) -> np.ndarray:
    sorted_levels = np.sort(np.asarray(levels, dtype=float))
    spacings = np.diff(sorted_levels)
    return spacings[spacings > 1e-12]


def mean_adjacent_gap_ratio(levels: np.ndarray) -> float:
    """Mean adjacent gap ratio, insensitive to smooth unfolding."""
    spacings = level_spacings(levels)
    if spacings.size < 2:
        return float("nan")
    lower = np.minimum(spacings[:-1], spacings[1:])
    upper = np.maximum(spacings[:-1], spacings[1:])
    return float(np.mean(lower / upper))


def inverse_participation_ratio(vector: np.ndarray) -> float | np.ndarray:
    """IPR = sum |psi|^4 / (sum |psi|^2)^2.

    If a 2D matrix is passed, columns are treated as eigenvectors.
    """
    arr = np.asarray(vector)
    if arr.ndim == 1:
        denom = np.sum(np.abs(arr) ** 2) ** 2
        return float(np.sum(np.abs(arr) ** 4) / denom)
    if arr.ndim == 2:
        denom = np.sum(np.abs(arr) ** 2, axis=0) ** 2
        return np.sum(np.abs(arr) ** 4, axis=0) / denom
    raise ValueError("vector must be 1D or 2D")
