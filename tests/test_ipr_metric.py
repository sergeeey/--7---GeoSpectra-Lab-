"""Unit tests for Inverse Participation Ratio (IPR) metric.

Ground truth tests for true eigenvector-based IPR = Σ|ψᵢ|⁴
Required before Gate 4B v0.1.21 metric-corrected execution.

Related:
- reports/S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md
- reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md Section 7.2
"""

from __future__ import annotations

import numpy as np
import pytest

from cc_toy_lab.spectral.metrics import inverse_participation_ratio


class TestIPRGroundTruth:
    """Ground truth tests for IPR metric validation."""

    def test_ipr_fully_localized_real(self):
        """IPR of δ-function (fully localized) should be 1.0.

        Physical interpretation: wavefunction concentrated at single site.
        """
        N = 100
        psi = np.zeros(N, dtype=float)
        psi[0] = 1.0  # Localized at site 0

        ipr = inverse_participation_ratio(psi)

        assert np.isclose(ipr, 1.0, atol=1e-10), f"Expected IPR=1.0 for δ-function, got {ipr}"

    def test_ipr_fully_localized_other_site(self):
        """IPR=1.0 holds for localization at any site."""
        N = 100
        psi = np.zeros(N, dtype=float)
        psi[50] = 1.0  # Localized at site 50

        ipr = inverse_participation_ratio(psi)

        assert np.isclose(ipr, 1.0, atol=1e-10)

    def test_ipr_fully_delocalized_real(self):
        """IPR of uniform state (fully delocalized) should be 1/N.

        Physical interpretation: wavefunction uniformly spread over N sites.
        """
        N = 100
        psi = np.ones(N, dtype=float) / np.sqrt(N)  # Normalized uniform state

        ipr = inverse_participation_ratio(psi)

        expected_ipr = 1.0 / N
        assert np.isclose(
            ipr, expected_ipr, rtol=1e-6
        ), f"Expected IPR=1/N={expected_ipr:.6f} for uniform state, got {ipr:.6f}"

    def test_ipr_fully_localized_complex(self):
        """IPR of complex δ-function should be 1.0.

        Tests complex vector support (required for quantum eigenstates).
        """
        N = 50
        psi = np.zeros(N, dtype=complex)
        psi[0] = 1.0 + 0.0j  # Complex localized state

        ipr = inverse_participation_ratio(psi)

        assert np.isclose(ipr, 1.0, atol=1e-10)

    def test_ipr_complex_superposition(self):
        """IPR of |ψ⟩ = (1+i)/√3 |0⟩ + 1/√3 |1⟩ should be 0.5.

        Example: two-site superposition with complex amplitudes.
        """
        N = 4
        psi = np.zeros(N, dtype=complex)
        psi[0] = (1.0 + 1.0j) / np.sqrt(3.0)
        psi[1] = 1.0 / np.sqrt(3.0)
        # psi[2] = psi[3] = 0

        # Verify normalization
        norm_squared = np.sum(np.abs(psi) ** 2)
        assert np.isclose(norm_squared, 1.0, atol=1e-10), "Test vector not normalized"

        ipr = inverse_participation_ratio(psi)

        # |ψ₀|⁴ = ((1+i)/√3)⁴ = (2/3)² = 4/9
        # |ψ₁|⁴ = (1/√3)⁴ = 1/9
        # IPR = 4/9 + 1/9 = 5/9 ≈ 0.5556
        expected_ipr = 5.0 / 9.0
        assert np.isclose(
            ipr, expected_ipr, rtol=1e-6
        ), f"Expected IPR={expected_ipr:.6f} for complex superposition, got {ipr:.6f}"

    def test_ipr_random_normalized_real(self):
        """IPR of random normalized vector should be in valid range (1/N, 1].

        Physical constraint: partially localized states.
        """
        N = 100
        np.random.seed(42)
        psi = np.random.randn(N)
        psi /= np.linalg.norm(psi)  # Normalize

        ipr = inverse_participation_ratio(psi)

        # Valid range check
        min_ipr = 1.0 / N
        max_ipr = 1.0
        assert (
            min_ipr < ipr <= max_ipr
        ), f"IPR={ipr:.6f} outside valid range ({min_ipr:.6f}, {max_ipr:.6f}]"

        # Finite check
        assert np.isfinite(ipr), f"IPR is not finite: {ipr}"

    def test_ipr_random_normalized_complex(self):
        """IPR of random complex normalized vector in valid range."""
        N = 100
        np.random.seed(123)
        psi = np.random.randn(N) + 1j * np.random.randn(N)
        psi /= np.linalg.norm(psi)

        ipr = inverse_participation_ratio(psi)

        min_ipr = 1.0 / N
        max_ipr = 1.0
        assert min_ipr < ipr <= max_ipr
        assert np.isfinite(ipr)

    def test_ipr_reproducible_with_seed(self):
        """IPR computation is deterministic for fixed random seed."""
        N = 50

        # First computation
        np.random.seed(789)
        psi1 = np.random.randn(N)
        psi1 /= np.linalg.norm(psi1)
        ipr1 = inverse_participation_ratio(psi1)

        # Second computation (same seed)
        np.random.seed(789)
        psi2 = np.random.randn(N)
        psi2 /= np.linalg.norm(psi2)
        ipr2 = inverse_participation_ratio(psi2)

        assert np.isclose(
            ipr1, ipr2, atol=1e-15
        ), f"IPR not reproducible: {ipr1:.10f} vs {ipr2:.10f}"

    def test_ipr_matrix_input_multiple_eigenvectors(self):
        """IPR handles 2D matrix input (multiple eigenvectors as columns)."""
        N = 50
        n_vecs = 5

        # Create 5 normalized eigenvectors
        np.random.seed(456)
        eigvecs = np.random.randn(N, n_vecs)
        # Normalize each column
        for i in range(n_vecs):
            eigvecs[:, i] /= np.linalg.norm(eigvecs[:, i])

        iprs = inverse_participation_ratio(eigvecs)

        # Should return array of 5 IPR values
        assert iprs.shape == (n_vecs,)

        # Each IPR in valid range
        for i, ipr in enumerate(iprs):
            assert 1.0 / N < ipr <= 1.0, f"IPR[{i}]={ipr:.6f} outside valid range"
            assert np.isfinite(ipr)

    def test_ipr_zero_vector_raises_error(self):
        """IPR of zero vector should raise ValueError (not silent NaN)."""
        N = 10
        psi = np.zeros(N, dtype=float)

        # IPR of zero vector is undefined (0/0)
        # Function must raise ValueError explicitly (v0.1.21: no silent NaN)
        with pytest.raises(ValueError, match="Cannot compute IPR for zero vector"):
            inverse_participation_ratio(psi)

    def test_ipr_unnormalized_vector(self):
        """IPR formula holds for unnormalized vectors via normalization term."""
        N = 20
        psi = np.array([2.0, 0.0, 0.0, 0.0] + [0.0] * (N - 4))  # Unnormalized

        ipr = inverse_participation_ratio(psi)

        # For δ-function (even unnormalized), IPR should still be 1.0
        # because IPR = sum|ψ|⁴ / (sum|ψ|²)²
        assert np.isclose(ipr, 1.0, atol=1e-10)

    def test_ipr_half_half_state(self):
        """IPR of |ψ⟩ = (|0⟩ + |1⟩)/√2 should be 0.5.

        Analytical: |ψ₀|⁴ = |ψ₁|⁴ = (1/√2)⁴ = 1/4
        IPR = 1/4 + 1/4 = 0.5
        """
        N = 10
        psi = np.zeros(N, dtype=float)
        psi[0] = 1.0 / np.sqrt(2.0)
        psi[1] = 1.0 / np.sqrt(2.0)

        ipr = inverse_participation_ratio(psi)

        assert np.isclose(ipr, 0.5, atol=1e-10), f"Expected IPR=0.5, got {ipr}"


class TestIPREdgeCases:
    """Edge cases and numerical stability tests."""

    def test_ipr_large_hilbert_space(self):
        """IPR computation stable for large N (Gate 4 max N=3712)."""
        N = 4000  # Larger than Gate 4 max
        psi = np.ones(N, dtype=float) / np.sqrt(N)

        ipr = inverse_participation_ratio(psi)

        expected_ipr = 1.0 / N
        assert np.isclose(ipr, expected_ipr, rtol=1e-6)

    def test_ipr_very_small_values(self):
        """IPR stable when |ψ|² values are very small but normalized."""
        N = 100
        psi = np.ones(N, dtype=float) * 1e-3
        psi /= np.linalg.norm(psi)

        ipr = inverse_participation_ratio(psi)

        expected_ipr = 1.0 / N
        assert np.isclose(ipr, expected_ipr, rtol=1e-5)

    def test_ipr_single_element_vector(self):
        """IPR of 1D vector (N=1) should be 1.0."""
        psi = np.array([1.0])

        ipr = inverse_participation_ratio(psi)

        assert np.isclose(ipr, 1.0, atol=1e-10)


class TestIPRGate4Consistency:
    """Tests specific to Gate 4 v0.1.21 requirements."""

    def test_ipr_bottom_10_percent_eigenvectors(self):
        """Simulate Gate 4 workflow: compute IPR for bottom 10% eigenstates."""
        N = 64  # Example: s1_size=64 case
        n_eigvals = N

        # Mock eigenvalues and eigenvectors
        np.random.seed(100)
        eigvals = np.sort(np.random.randn(n_eigvals))
        eigvecs = np.random.randn(N, n_eigvals)
        # Normalize each eigenvector
        for i in range(n_eigvals):
            eigvecs[:, i] /= np.linalg.norm(eigvecs[:, i])

        # Bottom 10%
        n_low = int(0.1 * N)
        low_indices = np.argsort(eigvals)[:n_low]
        low_eigvecs = eigvecs[:, low_indices]

        # Compute IPR for each low eigenstate
        iprs = inverse_participation_ratio(low_eigvecs)

        # Mean IPR (Gate 4 metric)
        mean_ipr = np.mean(iprs)

        # Sanity checks
        assert iprs.shape == (n_low,)
        assert np.all(iprs > 1.0 / N)
        assert np.all(iprs <= 1.0)
        assert np.isfinite(mean_ipr)
        assert 1.0 / N < mean_ipr <= 1.0

    def test_ipr_vs_eigenvalue_mean_not_equal(self):
        """Verify that mean(IPR) ≠ mean(eigenvalues).

        This is the v0.1.20 bug: eigenvalue mean was used instead of IPR.
        """
        N = 50
        np.random.seed(200)

        # Mock Hamiltonian eigenvalues and eigenvectors
        eigvals = np.sort(np.random.randn(N))
        eigvecs = np.random.randn(N, N)
        for i in range(N):
            eigvecs[:, i] /= np.linalg.norm(eigvecs[:, i])

        # Bottom 10%
        n_low = int(0.1 * N)
        low_eigvals = eigvals[:n_low]
        low_eigvecs = eigvecs[:, :n_low]

        # Gate 4 v0.1.20 (WRONG): mean eigenvalue
        mean_eigenvalue = np.mean(low_eigvals)

        # Gate 4 v0.1.21 (CORRECT): mean IPR
        iprs = inverse_participation_ratio(low_eigvecs)
        mean_ipr = np.mean(iprs)

        # These should NOT be equal (different physical quantities)
        assert not np.isclose(mean_eigenvalue, mean_ipr, rtol=0.1), (
            f"mean(eigenvalue)={mean_eigenvalue:.6f} ≈ mean(IPR)={mean_ipr:.6f} "
            "— this should not happen unless by coincidence"
        )

        # IPR is always positive and ≤1
        assert 0 < mean_ipr <= 1.0

        # Eigenvalues can be negative (binding energy)
        # No constraint on sign


# pytest configuration
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
