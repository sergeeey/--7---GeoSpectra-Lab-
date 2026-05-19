#!/usr/bin/env python3
"""Gate 2 Controls — Positive, Negative, Baseline Tests.

Day 3 of Gate 2 (21-22 мая 2026): validation beyond Hermiticity

Tests:
1. Positive control: S³ eigenvalues match analytical spectrum (arXiv:1103.4097)
2. Negative control: Random Hermitian matrix fails localization tests
3. Baseline metrics: spectral gap, IPR, kernel count

Timeline: Day 3-4 of Gate 2
Status: DRAFT (ready to run)

Usage:
    pytest tests/test_gate_2_controls.py -v
"""

from __future__ import annotations

import numpy as np
import pytest

from cc_toy_lab.spectral.dirac_s3 import build_s3_dirac_operator, s3_dimension


class TestPositiveControl:
    """Positive control: S³ Dirac eigenvalues match analytical theory."""

    def test_eigenvalues_vs_theory_j0(self):
        """j_max=0: expect λ = ±1.5/R (n=0 only)."""
        j_max = 0
        radius = 1.0

        # Build operator
        d_s3, _ = build_s3_dirac_operator(j_max=j_max, radius=radius)

        # Extract eigenvalues
        eigenvalues = np.linalg.eigvalsh(d_s3)

        # Expected: n=0 → λ = ±(0 + 3/2) / 1.0 = ±1.5
        expected = np.array([-1.5, 1.5])

        # Get unique eigenvalues (ignoring degeneracy)
        actual_unique = np.unique(np.round(eigenvalues, 6))

        # Compare
        np.testing.assert_allclose(actual_unique, expected, atol=1e-6)

    def test_eigenvalues_vs_theory_j1(self):
        """j_max=1: expect λ = ±1.5, ±2.5 (n=0,1)."""
        j_max = 1
        radius = 1.0

        d_s3, _ = build_s3_dirac_operator(j_max=j_max, radius=radius)
        eigenvalues = np.linalg.eigvalsh(d_s3)

        # Expected: n=0,1 → λ = ±1.5, ±2.5
        expected = np.array([-2.5, -1.5, 1.5, 2.5])

        actual_unique = np.unique(np.round(eigenvalues, 6))

        np.testing.assert_allclose(actual_unique, expected, atol=1e-6)

    def test_eigenvalues_vs_theory_j2(self):
        """j_max=2: expect λ = ±1.5, ±2.5, ±3.5 (n=0,1,2)."""
        j_max = 2
        radius = 1.0

        d_s3, _ = build_s3_dirac_operator(j_max=j_max, radius=radius)
        eigenvalues = np.linalg.eigvalsh(d_s3)

        # Expected: n=0,1,2 → λ = ±1.5, ±2.5, ±3.5
        expected = np.array([-3.5, -2.5, -1.5, 1.5, 2.5, 3.5])

        actual_unique = np.unique(np.round(eigenvalues, 6))

        np.testing.assert_allclose(actual_unique, expected, atol=1e-6)

    def test_eigenvalues_vs_theory_radius_scaling(self):
        """Eigenvalues scale with 1/radius."""
        j_max = 2
        radius = 2.0  # Double radius → half eigenvalues

        d_s3, _ = build_s3_dirac_operator(j_max=j_max, radius=radius)
        eigenvalues = np.linalg.eigvalsh(d_s3)

        # Expected: λ = ±(n + 3/2) / 2.0
        expected = np.array([-3.5, -2.5, -1.5, 1.5, 2.5, 3.5]) / 2.0

        actual_unique = np.unique(np.round(eigenvalues, 6))

        np.testing.assert_allclose(actual_unique, expected, atol=1e-6)


class TestNegativeControl:
    """Negative control: Random Hermitian matrix should NOT pass localization tests."""

    def test_random_hermitian_no_structure(self):
        """Random Hermitian matrix has no spectral structure → cannot pass FL gates."""
        # Generate random Hermitian matrix matching S³ dimension
        j_max = 2
        dim = s3_dimension(j_max)

        # Create random Hermitian
        np.random.seed(42)
        H_random = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
        H_random = 0.5 * (H_random + H_random.conj().T)

        # Test 1: Hermiticity (should pass — it's Hermitian by construction)
        hermiticity_residual = np.max(np.abs(H_random - H_random.conj().T))
        assert hermiticity_residual < 1e-9

        # Test 2: Eigenvalues (should be real but unstructured)
        eigenvalues = np.linalg.eigvalsh(H_random)

        # Check: eigenvalue spacing should NOT match S³ Dirac pattern
        # S³ Dirac: uniform spacing 1.0 (λ_n - λ_{n-1} = 1.0 for n=1,2,...)
        # Random: spacing variable

        unique_eigs = np.unique(np.round(eigenvalues, 6))
        if len(unique_eigs) > 1:
            spacings = np.diff(unique_eigs)
            # S³ Dirac: all spacings ≈ 1.0 (for radius=1.0)
            # Random: NOT uniform
            # Check: standard deviation of spacings should be large (not uniform)
            spacing_std = np.std(spacings)

            # S³ Dirac spacing_std ≈ 0 (uniform)
            # Random: spacing_std >> 0
            # Threshold: spacing_std > 0.1 → not Dirac-like
            assert (
                spacing_std > 0.1
            ), f"Random matrix suspiciously uniform spacing: {spacing_std:.3f}"


class TestBaselineMetrics:
    """Baseline metrics: spectral gap, IPR, kernel count."""

    def test_spectral_gap_nonzero(self):
        """Spectral gap: gap between lowest unique eigenvalue levels."""
        j_max = 2
        radius = 1.0

        d_s3, _ = build_s3_dirac_operator(j_max=j_max, radius=radius)
        eigenvalues = np.linalg.eigvalsh(d_s3)

        # Get unique eigenvalues (ignoring degeneracy)
        unique_eigs = np.unique(np.round(eigenvalues, 6))

        # Ground state = lowest unique eigenvalue
        ground_state = unique_eigs[0]

        # First excited = second lowest unique eigenvalue
        first_excited = unique_eigs[1]

        # Gap between unique levels
        gap = first_excited - ground_state

        # For S³ Dirac: uniform spacing = 1.0 between levels
        # For j_max=2: unique eigenvalues {-3.5, -2.5, -1.5, 1.5, 2.5, 3.5}
        # Ground state = -3.5, first excited = -2.5 → gap = 1.0
        assert gap > 0, f"Spectral gap must be positive, got {gap:.6f}"
        np.testing.assert_allclose(gap, 1.0, atol=1e-6)

    def test_kernel_count_zero(self):
        """Kernel count: S³ topologically trivial → expect 0 zero modes."""
        j_max = 2
        radius = 1.0

        d_s3, _ = build_s3_dirac_operator(j_max=j_max, radius=radius)
        eigenvalues = np.linalg.eigvalsh(d_s3)

        # Count zero modes (|λ| < 1e-9)
        kernel_count = np.sum(np.abs(eigenvalues) < 1e-9)

        # S³ trivial spinor bundle → no zero modes
        assert kernel_count == 0, f"Expected 0 zero modes (S³ trivial), got {kernel_count}"

    def test_eigenvalue_symmetry(self):
        """Eigenvalues symmetric around zero (Dirac property)."""
        j_max = 2
        radius = 1.0

        d_s3, _ = build_s3_dirac_operator(j_max=j_max, radius=radius)
        eigenvalues = np.linalg.eigvalsh(d_s3)

        # Get unique eigenvalues
        unique_eigs = np.unique(np.round(eigenvalues, 6))

        # Check: for every λ > 0, there exists -λ
        positive_eigs = unique_eigs[unique_eigs > 1e-9]
        negative_eigs = unique_eigs[unique_eigs < -1e-9]

        # Symmetry: |positive| == |negative|
        assert (
            len(positive_eigs) == len(negative_eigs)
        ), f"Eigenvalues not symmetric: {len(positive_eigs)} positive vs {len(negative_eigs)} negative"

        # Check: -positive_eigs == negative_eigs (reversed)
        np.testing.assert_allclose(-positive_eigs[::-1], negative_eigs, atol=1e-6)
