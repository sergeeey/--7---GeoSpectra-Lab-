from __future__ import annotations

import numpy as np


def sample_sphere(
    dimension: int,
    count: int,
    radius: float = 1.0,
    seed: int | None = None,
) -> np.ndarray:
    """Uniformly sample S^dimension_R by normalizing Gaussian vectors."""
    if dimension < 1:
        raise ValueError("dimension must be >= 1")
    if count <= 0:
        raise ValueError("count must be positive")
    rng = np.random.default_rng(seed)
    points = rng.normal(size=(count, dimension + 1))
    norms = np.linalg.norm(points, axis=1)
    return radius * points / norms[:, None]
