import numpy as np

from cc_toy_lab.geometry.analytic_spectra import (
    product_spectrum,
    sphere_laplacian_degeneracy,
    sphere_laplacian_eigenvalue,
    sphere_scalar_curvature,
)


def test_sphere_scalar_curvature():
    assert sphere_scalar_curvature(2, radius=1.0) == 2.0
    assert sphere_scalar_curvature(3, radius=1.0) == 6.0
    assert sphere_scalar_curvature(6, radius=1.0) == 30.0
    assert sphere_scalar_curvature(6, radius=2.0) == 7.5


def test_sphere_laplacian_eigenvalues():
    assert sphere_laplacian_eigenvalue(2, 0) == 0.0
    assert sphere_laplacian_eigenvalue(2, 2) == 6.0
    assert sphere_laplacian_eigenvalue(3, 2) == 8.0
    assert sphere_laplacian_eigenvalue(6, 1, radius=2.0) == 1.5


def test_sphere_degeneracies():
    assert [sphere_laplacian_degeneracy(2, ell) for ell in range(4)] == [1, 3, 5, 7]
    assert [sphere_laplacian_degeneracy(3, ell) for ell in range(4)] == [1, 4, 9, 16]
    assert [sphere_laplacian_degeneracy(6, ell) for ell in range(3)] == [1, 7, 27]


def test_product_spectrum_sum_rule():
    spectrum = product_spectrum(3, 6, ell_max_a=1, ell_max_b=1, radius_a=2.0, radius_b=1.0)
    values = {(row.ell_a, row.ell_b): row.eigenvalue for row in spectrum}
    assert np.isclose(values[(0, 0)], 0.0)
    assert np.isclose(values[(1, 0)], 3.0 / 4.0)
    assert np.isclose(values[(0, 1)], 6.0)
    assert np.isclose(values[(1, 1)], 6.75)


# --- Hardcoded reference values to avoid circular validation. ---
# Expected numbers below are computed from closed forms λ_ℓ = ℓ(ℓ+n−1)/R²
# and R_scal = n(n−1)/R², not by calling sphere_laplacian_eigenvalue or other helpers under test.


def test_hardcoded_s2_laplacian_eigenvalues_ell_0_4_r1():
    # S^2: n=2, λ_ℓ = ℓ(ℓ+1)/R² with R=1
    expected = [0.0, 2.0, 6.0, 12.0, 20.0]
    for ell, ref in enumerate(expected):
        assert sphere_laplacian_eigenvalue(2, ell, radius=1.0) == ref


def test_hardcoded_s3_laplacian_eigenvalues_ell_0_4_r1():
    # S^3: n=3, λ_ℓ = ℓ(ℓ+2)/R² with R=1
    expected = [0.0, 3.0, 8.0, 15.0, 24.0]
    for ell, ref in enumerate(expected):
        assert sphere_laplacian_eigenvalue(3, ell, radius=1.0) == ref


def test_hardcoded_s6_laplacian_eigenvalues_ell_0_4_r1():
    # S^6: n=6, λ_ℓ = ℓ(ℓ+5)/R² with R=1
    expected = [0.0, 6.0, 14.0, 24.0, 36.0]
    for ell, ref in enumerate(expected):
        assert sphere_laplacian_eigenvalue(6, ell, radius=1.0) == ref


def test_hardcoded_laplacian_radius_scaling_r2():
    # Hardcoded reference values to avoid circular validation (same formulas, R=2 → divide by 4).
    assert sphere_laplacian_eigenvalue(2, 1, radius=2.0) == 0.5  # 2/4
    assert sphere_laplacian_eigenvalue(2, 3, radius=2.0) == 3.0  # 12/4
    assert sphere_laplacian_eigenvalue(3, 2, radius=2.0) == 2.0  # 8/4
    assert sphere_laplacian_eigenvalue(6, 2, radius=2.0) == 3.5  # 14/4


def test_hardcoded_sphere_degeneracies_extended():
    # Hardcoded reference values to avoid circular validation (multiplicities for scalar harmonics).
    assert [sphere_laplacian_degeneracy(2, ell) for ell in range(5)] == [1, 3, 5, 7, 9]
    assert [sphere_laplacian_degeneracy(3, ell) for ell in range(5)] == [1, 4, 9, 16, 25]
    assert [sphere_laplacian_degeneracy(6, ell) for ell in range(5)] == [1, 7, 27, 77, 182]


def test_hardcoded_sphere_scalar_curvature():
    # Hardcoded reference values to avoid circular validation: R_scal = n(n−1)/R².
    assert sphere_scalar_curvature(2, radius=1.0) == 2.0
    assert sphere_scalar_curvature(3, radius=1.0) == 6.0
    assert sphere_scalar_curvature(6, radius=1.0) == 30.0
    assert sphere_scalar_curvature(2, radius=2.0) == 0.5
    assert sphere_scalar_curvature(3, radius=2.0) == 1.5
    assert sphere_scalar_curvature(6, radius=2.0) == 7.5


def test_hardcoded_product_spectrum_s3xs6_reference():
    # Hardcoded reference values to avoid circular validation (sum of independent sphere Laplacians).
    spectrum = product_spectrum(3, 6, ell_max_a=1, ell_max_b=1, radius_a=2.0, radius_b=1.0)
    by_key = {(row.ell_a, row.ell_b): (row.eigenvalue, row.degeneracy) for row in spectrum}

    assert by_key[(0, 0)] == (0.0, 1)
    assert np.isclose(by_key[(1, 0)][0], 0.75) and by_key[(1, 0)][1] == 4
    assert by_key[(0, 1)] == (6.0, 7)
    assert np.isclose(by_key[(1, 1)][0], 6.75) and by_key[(1, 1)][1] == 28
