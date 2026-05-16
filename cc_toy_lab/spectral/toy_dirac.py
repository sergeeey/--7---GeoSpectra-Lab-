from __future__ import annotations

import numpy as np
from scipy import sparse


def build_toy_dirac_operator(
    size: int = 128,
    mass_disorder: float = 0.0,
    gauge_strength: float = 0.0,
    seed: int | None = None,
) -> sparse.csr_matrix:
    """Build a chiral block toy Dirac operator D = [[0, A], [A^T, 0]].

    This tests spectral symmetry and near-zero diagnostics only. It does not
    establish protected chirality or a Dirac index.
    """
    if size < 4:
        raise ValueError("size must be >= 4")
    rng = np.random.default_rng(seed)
    forward = sparse.diags([-np.ones(size), np.ones(size)], offsets=[0, 1], shape=(size, size), format="lil")
    forward[size - 1, 0] = 1.0
    mass = rng.normal(scale=mass_disorder, size=size)
    gauge = gauge_strength * np.sin(2.0 * np.pi * np.arange(size) / size)
    a_block = forward.tocsr() + sparse.diags(mass + gauge, format="csr")
    zero = sparse.csr_matrix((size, size))
    return sparse.bmat([[zero, a_block], [a_block.T, zero]], format="csr")
