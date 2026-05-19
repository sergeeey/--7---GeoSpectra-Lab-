"""Toy S3 Dirac operator (SU(2) representation, Gate 1 prototype).

GATE 1 STATUS: PROTOTYPE IMPLEMENTATION
- Constructs Hermitian operator with correct dimension
- Eigenvalue structure simplified (not full SU(2) representation theory yet)
- Purpose: proof-of-concept that Track C feasible (days, not weeks)

TODO for Gate 3 (full diagnostic):
- Implement full SU(2) Wigner D-matrices
- Physical eigenvalues λ_{j,±} = ±(j + 1/2) / R
- Kernel structure for topological index
"""

from __future__ import annotations

import numpy as np


def build_s3_dirac_operator(
    j_max: int,
    radius: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Build a finite-mode S3 Dirac operator (Gate 1 prototype).

    Args:
        j_max: Maximum spin quantum number (truncation cutoff)
        radius: S³ radius (default 1.0)

    Returns:
        operator: Hermitian matrix (dimension: sum_{j=0}^{j_max} (2j+1)²)
        chirality: Placeholder chirality operator (Gate 1: identity)

    Mathematical background:
        - S³ = SU(2) manifold (parallelizable, no monopole charge)
        - Spinor bundle: trivial
        - Quantum numbers: j ∈ {0, 1/2, 1, 3/2, ..., j_max}
        - Dimension per j: (2j+1)² (full SU(2) representation)
        - Physical eigenvalues: λ_{j,±} = ±(j + 1/2) / R

    Gate 1 simplifications:
        - Eigenvalue structure placeholder (not full SU(2) yet)
        - Chirality operator = identity (no topological index)
        - Hermiticity verified, shape correct
    """
    if j_max < 0:
        raise ValueError("j_max must be >= 0")
    if radius <= 0:
        raise ValueError("radius must be positive")

    # Calculate total dimension: sum_{j=0}^{j_max/2} (2j+1)²
    # Convention: j_max=N → highest j = N/2
    # j_max=1 → j in [0, 0.5] → dim = 1 + 4 = 5
    # j = k * 0.5 for k in [0, 1, 2, ..., j_max]
    j_values = [k * 0.5 for k in range(0, int(j_max) + 1)]
    dimensions = [int((2 * j + 1) ** 2) for j in j_values]  # Force int for dimension
    total_dim = int(sum(dimensions))

    # Gate 1 prototype: construct Hermitian matrix with block structure
    # Each j-block has dimension (2j+1)²
    # Eigenvalues: simplified ±(j + 0.5) / radius pattern
    operator = np.zeros((total_dim, total_dim), dtype=complex)

    offset = 0
    for j, dim_j in zip(j_values, dimensions, strict=False):
        # Block for this j value
        # Simplified eigenvalue: ±(j + 0.5) / radius
        eigenvalue_pos = (j + 0.5) / radius
        eigenvalue_neg = -(j + 0.5) / radius

        # Half the block gets positive eigenvalue, half gets negative
        half_dim = dim_j // 2
        for i in range(half_dim):
            operator[offset + i, offset + i] = eigenvalue_pos
        for i in range(half_dim, dim_j):
            operator[offset + i, offset + i] = eigenvalue_neg

        offset += dim_j

    # Hermitize (force exact Hermiticity numerically)
    operator = 0.5 * (operator + operator.conj().T)

    # Placeholder chirality (Gate 1: identity, no topological index)
    chirality = np.ones(total_dim, dtype=float)

    return operator, chirality


def s3_dimension(j_max: int) -> int:
    """Calculate total Hilbert space dimension for S³ truncated at j_max.

    j_max=1 means j in [0, 0.5, 1], so dimension = 1 + 4 + 9 = 14.
    Wait, that's wrong. Let me recalculate:
    - j_max=1 should mean max j is 1, so j in {0, 1/2, 1}
    - But test expects s3_dimension(1) == 5...

    Test comment says: "j=0,1/2: 1 + (2*0.5+1)² = 1 + 4 = 5"
    So j_max=1 means "include j up to 1/2", NOT "up to 1".

    Fix: j_max=N means include j values [0, 1/2, 1, ..., N/2]
    So for j_max=1: j in [0, 1/2] → dim = 1 + 4 = 5
    For j_max=2: j in [0, 1/2, 1] → dim = 1 + 4 + 9 = 14
    """
    # j_max=N means max j value is N/2
    # j = k * 0.5 for k in [0, 1, 2, ..., j_max]
    j_values = [k * 0.5 for k in range(0, int(j_max) + 1)]
    return int(sum((2 * j + 1) ** 2 for j in j_values))
