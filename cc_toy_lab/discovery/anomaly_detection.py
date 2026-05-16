from __future__ import annotations

import numpy as np


def zscore_flags(values: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if values.size == 0 or np.std(values) == 0:
        return np.zeros(values.shape, dtype=bool)
    z = np.abs((values - np.mean(values)) / np.std(values))
    return z > threshold
