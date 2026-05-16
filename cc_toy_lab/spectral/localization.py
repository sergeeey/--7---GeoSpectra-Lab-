from __future__ import annotations

import numpy as np


def finite_size_ipr_slope(sizes: np.ndarray, ipr_values: np.ndarray) -> float:
    """Log-log slope for IPR(N); delocalized states trend toward -1."""
    sizes = np.asarray(sizes, dtype=float)
    ipr_values = np.asarray(ipr_values, dtype=float)
    mask = (sizes > 0) & (ipr_values > 0)
    if np.count_nonzero(mask) < 2:
        return float("nan")
    slope, _ = np.polyfit(np.log(sizes[mask]), np.log(ipr_values[mask]), deg=1)
    return float(slope)
