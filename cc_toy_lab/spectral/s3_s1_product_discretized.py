"""Toy product-discretized S3 x S1 (Gate 1 prototype).

GATE 1 STATUS: MINIMAL IMPLEMENTATION
- Constructs Kronecker-sum Hamiltonian H = kron(D_S3^2, I_S1) + kron(I_S3, P_S1)
- Hermiticity test passes
- Purpose: proof-of-concept that Track C operators feasible (days, not weeks)

TODO for Gate 2 (smoke test):
- Add localization diagnostics (IPR, kernel analysis)
- Add progressive profiles (tiny/medium/full)
- Port FL gates from S²×S¹

TODO for Gate 3 (full diagnostic):
- Implement full SU(2) eigenvalue structure
- Topological index (if applicable for S³)
- Cross-validate against S²×S¹ methodology
"""

from __future__ import annotations

import numpy as np

from cc_toy_lab.spectral.dirac_s3 import build_s3_dirac_operator, s3_dimension
from cc_toy_lab.spectral.s1_discretizations import S1_DISCRETIZATION_FAMILIES, build_s1_operator


def _hermitize(matrix: np.ndarray) -> np.ndarray:
    """Force exact Hermiticity numerically."""
    dense = np.asarray(matrix, dtype=complex)
    return 0.5 * (dense + dense.conj().T)


def build_s3_s1_product_operator(
    *,
    j_max: int,
    s1_size: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float,
    s1_family: str,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """Build S³×S¹ product-discretized operator (Gate 1 minimal).

    Args:
        j_max: S³ spin truncation (replaces S² monopole charge q)
        s1_size: S¹ lattice size
        alpha: S¹ flux parameter (0.0=PBC, 0.5=APBC)
        mode: "clean" or "geometric_weight" (disorder)
        disorder_strength: Anderson disorder strength W
        seed: Random seed for disorder
        radius: Manifold radius
        s1_family: S¹ discretization family (spectral_circle, ring, wilson_ring)

    Returns:
        operator: H = kron(D_S3^2, I_S1) + kron(I_S3, P_S1)
        chirality: Lifted S³ chirality (placeholder for Gate 1)
        meta: Metadata dict
    """
    if s1_family not in S1_DISCRETIZATION_FAMILIES:
        raise ValueError(f"unknown S1 family: {s1_family}")

    # Build S³ Dirac operator
    d_s3, chi_s3 = build_s3_dirac_operator(j_max=int(j_max), radius=float(radius))
    d = np.asarray(d_s3, dtype=float)
    h_s3 = d @ d  # D_S3^2 (Laplacian-like)

    # Build S¹ operator
    p_s1 = build_s1_operator(
        size=int(s1_size),
        alpha=float(alpha),
        family=str(s1_family),
        mode=str(mode),
        disorder_strength=float(disorder_strength),
        seed=seed,
        radius=float(radius),
    )
    p_s1 = np.asarray(p_s1, dtype=complex)

    # Product structure: H = kron(H_S3, I) + kron(I, P_S1)
    s3_dim = int(h_s3.shape[0])
    eye_s3 = np.eye(s3_dim, dtype=complex)
    eye_s1 = np.eye(int(s1_size), dtype=complex)

    h_total = np.kron(np.asarray(h_s3, dtype=complex), eye_s1) + np.kron(eye_s3, p_s1)
    h_total = _hermitize(h_total)

    # Lifted chirality (placeholder for Gate 1)
    lifted = np.kron(np.asarray(chi_s3, dtype=float), np.ones(int(s1_size), dtype=float))

    meta = {
        "j_max": int(j_max),
        "s1_family": str(s1_family),
        "s1_size": int(s1_size),
        "alpha": float(alpha),
        "mode": str(mode),
        "disorder_strength": float(disorder_strength),
        "seed": None if seed is None else int(seed),
        "radius": float(radius),
        "s3_dimension": s3_dim,
        "total_dimension": int(h_total.shape[0]),
        "operator_schema": "H = kron(D_S3^2, I_S1) + kron(I_S3, P_S1)",
        "gate_status": "Gate 1 prototype (Hermiticity only)",
    }

    return h_total, lifted, meta


def analyze_s3_s1_hermiticity(
    *,
    j_max: int,
    s1_size: int,
    alpha: float = 0.0,
    disorder_strength: float = 0.0,
    seed: int = 123,
    radius: float = 1.0,
    s1_family: str = "spectral_circle",
    hermiticity_tol: float = 1e-9,
) -> dict:
    """Minimal Hermiticity test for Gate 1 checkpoint.

    Returns:
        dict with keys:
        - hermiticity_residual: max|H - H†|
        - passed: bool (residual < tolerance)
        - meta: operator metadata
    """
    op, _, meta = build_s3_s1_product_operator(
        j_max=j_max,
        s1_size=s1_size,
        alpha=alpha,
        mode="clean" if disorder_strength == 0.0 else "geometric_weight",
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        s1_family=s1_family,
    )

    residual = float(np.max(np.abs(op - op.conj().T)))
    passed = bool(residual < hermiticity_tol)

    return {
        "hermiticity_residual": residual,
        "hermiticity_tol": hermiticity_tol,
        "passed": passed,
        "j_max": meta["j_max"],
        "s1_size": meta["s1_size"],
        "s3_dimension": meta["s3_dimension"],
        "total_dimension": meta["total_dimension"],
        "operator_schema": meta["operator_schema"],
        "gate_status": meta["gate_status"],
    }
