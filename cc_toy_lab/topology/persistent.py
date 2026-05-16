from __future__ import annotations

import numpy as np


def pairwise_distance_summary(points: np.ndarray) -> dict[str, float]:
    """Lightweight topology-adjacent diagnostic when GUDHI is unavailable."""
    if points.ndim != 2:
        raise ValueError("points must be a 2D array")
    if len(points) < 2:
        return {"mean_distance": 0.0, "max_distance": 0.0}
    diffs = points[:, None, :] - points[None, :, :]
    distances = np.sqrt(np.sum(diffs**2, axis=-1))
    upper = distances[np.triu_indices(len(points), k=1)]
    return {"mean_distance": float(np.mean(upper)), "max_distance": float(np.max(upper))}
