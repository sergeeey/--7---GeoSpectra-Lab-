from __future__ import annotations

import numpy as np
from scipy.interpolate import UnivariateSpline


def unfold_spectrum(levels: np.ndarray, smooth: float = 0.01) -> np.ndarray:
    """Return a smoothed rank-space unfolding for diagnostic plots."""
    values = np.sort(np.asarray(levels, dtype=float))
    if values.size < 4:
        return values.copy()
    ranks = np.arange(values.size, dtype=float)
    spline = UnivariateSpline(values, ranks, s=smooth * values.size)
    return spline(values)
