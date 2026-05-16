from __future__ import annotations

from dataclasses import dataclass
from math import factorial


@dataclass(frozen=True)
class ProductSpectrumRow:
    ell_a: int
    ell_b: int
    eigenvalue: float
    degeneracy: int


def _validate_sphere(dimension: int, radius: float = 1.0) -> None:
    if dimension < 1:
        raise ValueError("dimension must be >= 1")
    if radius <= 0:
        raise ValueError("radius must be positive")


def sphere_scalar_curvature(dimension: int, radius: float = 1.0) -> float:
    """Scalar curvature of the round sphere S^n_R."""
    _validate_sphere(dimension, radius)
    return float(dimension * (dimension - 1) / radius**2)


def sphere_laplacian_eigenvalue(dimension: int, ell: int, radius: float = 1.0) -> float:
    """Eigenvalue ell(ell+n-1)/R^2 of the non-negative scalar Laplacian."""
    _validate_sphere(dimension, radius)
    if ell < 0:
        raise ValueError("ell must be non-negative")
    return float(ell * (ell + dimension - 1) / radius**2)


def sphere_laplacian_degeneracy(dimension: int, ell: int) -> int:
    """Multiplicity of scalar spherical harmonics of degree ell on S^n."""
    _validate_sphere(dimension)
    if ell < 0:
        raise ValueError("ell must be non-negative")
    if dimension == 1:
        return 1 if ell == 0 else 2
    numerator = (2 * ell + dimension - 1) * factorial(ell + dimension - 2)
    denominator = factorial(ell) * factorial(dimension - 1)
    return int(numerator // denominator)


def product_spectrum(
    dimension_a: int,
    dimension_b: int,
    ell_max_a: int,
    ell_max_b: int,
    radius_a: float = 1.0,
    radius_b: float = 1.0,
) -> list[ProductSpectrumRow]:
    """Scalar product spectrum for S^a x S^b as a Minkowski sum."""
    rows: list[ProductSpectrumRow] = []
    for ell_a in range(ell_max_a + 1):
        value_a = sphere_laplacian_eigenvalue(dimension_a, ell_a, radius_a)
        deg_a = sphere_laplacian_degeneracy(dimension_a, ell_a)
        for ell_b in range(ell_max_b + 1):
            value_b = sphere_laplacian_eigenvalue(dimension_b, ell_b, radius_b)
            deg_b = sphere_laplacian_degeneracy(dimension_b, ell_b)
            rows.append(
                ProductSpectrumRow(
                    ell_a=ell_a,
                    ell_b=ell_b,
                    eigenvalue=float(value_a + value_b),
                    degeneracy=deg_a * deg_b,
                )
            )
    return sorted(rows, key=lambda row: (row.eigenvalue, row.ell_a, row.ell_b))
