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

    Raises:
        ValueError: If vector is zero (norm^2 < 1e-15) or not 1D/2D.
    """
    arr = np.asarray(vector)
    if arr.ndim == 1:
        norm_sq = np.sum(np.abs(arr) ** 2)
        if norm_sq < 1e-15:
            raise ValueError("Cannot compute IPR for zero vector (norm^2 < 1e-15)")
        denom = norm_sq**2
        return float(np.sum(np.abs(arr) ** 4) / denom)
    if arr.ndim == 2:
        norm_sq = np.sum(np.abs(arr) ** 2, axis=0)
        if np.any(norm_sq < 1e-15):
            zero_cols = np.where(norm_sq < 1e-15)[0]
            raise ValueError(
                f"Cannot compute IPR for zero vector(s) in column(s): {zero_cols.tolist()}"
            )
        denom = norm_sq**2
        return np.sum(np.abs(arr) ** 4, axis=0) / denom
    raise ValueError("vector must be 1D or 2D")
