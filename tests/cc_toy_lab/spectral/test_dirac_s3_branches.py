"""RED unit tests for S³ Dirac branch indexing (Gate 4B postmortem).

PURPOSE:
    Verify low spectrum eigenvalue structure for S³ Dirac operator.
    Tests are written BEFORE fix to establish RED phase (TDD).

CONTEXT:
    Gate 4B v0.1.23 source verification suggested expected spectrum ±3/2, ±5/2, ±7/2.
    Current code produces: -9/2, -7/2, -5/2, +3/2, +5/2, +7/2 (asymmetric).
    Root cause: k ≥ 1 in arXiv:1103.4097 eq (6.4) → negative starts at -5/2.

HYPOTHESIS:
    If k=0 is physically valid for negative branch → -3/2 should exist.
    If paper says k ≥ 1 only → current code is correct, no fix needed.

TESTS:
    1. test_current_spectrum_baseline: Document current state (should PASS)
    2. test_negative_3_2_presence: Critical test for -3/2 (should FAIL if k ≥ 1)
    3. test_positive_3_2_presence: Baseline for +3/2 (should PASS)
    4. test_radius_scaling: Verify λ ∝ 1/R (should PASS)

REFERENCES:
    - arXiv:1103.4097 page 15, equation (6.4)
    - cc_toy_lab/spectral/dirac_s3.py lines 67-82
    - reports/CODE_FIX_PLAN_v0.1.24_S3_BRANCH_INDEXING.md
"""

from __future__ import annotations

import numpy as np
import pytest


# Import from active implementation
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[3] / "cc_toy_lab"))
from spectral.dirac_s3 import build_s3_dirac_operator


class TestDiracS3LowSpectrum:
    """Test suite for S³ Dirac low eigenvalue spectrum."""

    @pytest.fixture
    def operator_r1_jmax2(self) -> np.ndarray:
        """Build S³ Dirac operator with R=1.0, j_max=2 (3 levels)."""
        operator, _ = build_s3_dirac_operator(j_max=2, radius=1.0)
        return operator

    @pytest.fixture
    def eigenvalues_r1_jmax2(self, operator_r1_jmax2: np.ndarray) -> np.ndarray:
        """Compute eigenvalues for R=1.0, j_max=2."""
        eigenvalues = np.linalg.eigvalsh(operator_r1_jmax2)
        return eigenvalues

    @pytest.fixture
    def unique_eigenvalues_r1(self, eigenvalues_r1_jmax2: np.ndarray) -> np.ndarray:
        """Get unique eigenvalues rounded to 6 decimals."""
        return np.unique(np.round(eigenvalues_r1_jmax2, 6))

    # -------------------------------------------------------------------------
    # TEST 1: BASELINE — Document corrected spectrum (should PASS after v0.1.24 fix)
    # -------------------------------------------------------------------------
    def test_corrected_spectrum_baseline(self, unique_eigenvalues_r1: np.ndarray) -> None:
        """Document corrected low spectrum after v0.1.24 branch indexing fix.

        This test documents the CORRECTED STATE after fix (v0.1.24).
        Expected to PASS — verifies fix restored -3/2 eigenvalue.

        Corrected code: negative k ≥ 0 (includes k=0 → -3/2), positive k ≥ 1
        Source: arXiv:1103.4097 Section 6, verified in S3_DIRAC_SOURCE_VERIFICATION_v0.1.23.md
        """
        # Corrected implementation after v0.1.24 fix (includes -3/2)
        expected_corrected = np.array(
            [-4.5, -3.5, -2.5, -1.5, 1.5, 2.5]
        )  # -9/2, -7/2, -5/2, -3/2, +3/2, +5/2

        actual_low_6 = unique_eigenvalues_r1[:6]

        # Should PASS after fix (verifies -3/2 present)
        np.testing.assert_array_almost_equal(
            actual_low_6,
            expected_corrected,
            decimal=4,
            err_msg="Corrected spectrum does not match source-verified expectation",
        )

    # -------------------------------------------------------------------------
    # TEST 2: CRITICAL — Presence of -3/2 (should FAIL if k ≥ 1 enforced)
    # -------------------------------------------------------------------------
    def test_negative_3_2_presence(self, unique_eigenvalues_r1: np.ndarray) -> None:
        """Verify that -3/2 exists in low spectrum (CRITICAL TEST).

        This is the RED phase test. Expected to FAIL on current code if k ≥ 1 enforced.

        CONTEXT:
            - Gate 4B expected: -3/2 present (symmetric spectrum)
            - Current code: k ≥ 1 → lowest negative is -5/2
            - If k=0 allowed: λ₋ = -(0 + 3/2) = -3/2 would appear

        EXPECTED BEHAVIOR:
            - Current code (k ≥ 1): FAIL (no -3/2)
            - After fix (k ≥ 0): PASS (has -3/2)

        SOURCE VERIFICATION:
            Must check arXiv:1103.4097 eq (6.4) to determine if k=0 is valid.
        """
        target_eigenvalue = -1.5  # -3/2
        tolerance = 1e-4

        # Check if -3/2 exists in unique eigenvalues
        is_present = np.any(np.abs(unique_eigenvalues_r1 - target_eigenvalue) < tolerance)

        # RED phase: this should FAIL on current code (k ≥ 1)
        assert is_present, (
            f"FAIL: -3/2 eigenvalue not found in spectrum.\n"
            f"Current low spectrum: {unique_eigenvalues_r1[:6]}\n"
            f"Expected: -3/2 present (for symmetric ±3/2, ±5/2, ±7/2 structure)\n"
            f"Likely cause: k starts from 1 instead of 0 for negative branch"
        )

    # -------------------------------------------------------------------------
    # TEST 3: BASELINE — Presence of +3/2 (should PASS)
    # -------------------------------------------------------------------------
    def test_positive_3_2_presence(self, unique_eigenvalues_r1: np.ndarray) -> None:
        """Verify that +3/2 exists in low spectrum (baseline).

        This test should PASS on current code (positive branch already correct).

        Current code: k=1 → λ₊ = +(1 + 1/2) = +3/2 ✓
        """
        target_eigenvalue = 1.5  # +3/2
        tolerance = 1e-4

        # Check if +3/2 exists in unique eigenvalues
        is_present = np.any(np.abs(unique_eigenvalues_r1 - target_eigenvalue) < tolerance)

        # Should PASS (positive branch already has k=1 → +3/2)
        assert is_present, (
            f"FAIL: +3/2 eigenvalue not found in spectrum.\n"
            f"Current low spectrum: {unique_eigenvalues_r1[:6]}\n"
            f"This indicates unexpected regression in positive branch indexing."
        )

    # -------------------------------------------------------------------------
    # TEST 4: SCALING — Eigenvalues scale as 1/R (should PASS)
    # -------------------------------------------------------------------------
    def test_radius_scaling(self) -> None:
        """Verify eigenvalues scale inversely with radius: λ(R) = λ(1) / R.

        This test verifies basic spectral scaling law.
        Should PASS on current code (independent of branch indexing issue).

        Mathematical basis: Dirac operator ~∇/R → eigenvalues ~ 1/R
        """
        # Build operators with R=1.0 and R=2.0
        operator_r1, _ = build_s3_dirac_operator(j_max=1, radius=1.0)
        operator_r2, _ = build_s3_dirac_operator(j_max=1, radius=2.0)

        eigenvalues_r1 = np.linalg.eigvalsh(operator_r1)
        eigenvalues_r2 = np.linalg.eigvalsh(operator_r2)

        # Sort for comparison
        eigenvalues_r1 = np.sort(eigenvalues_r1)
        eigenvalues_r2 = np.sort(eigenvalues_r2)

        # R=2.0 eigenvalues should be half of R=1.0 eigenvalues
        expected_r2 = eigenvalues_r1 / 2.0

        np.testing.assert_array_almost_equal(
            eigenvalues_r2,
            expected_r2,
            decimal=6,
            err_msg="Eigenvalues do not scale as 1/R",
        )


# -------------------------------------------------------------------------
# ADDITIONAL TEST: Low spectrum structure (optional, for completeness)
# -------------------------------------------------------------------------
class TestDiracS3SpectrumStructure:
    """Additional structural tests for S³ Dirac spectrum."""

    def test_low_spectrum_count(self) -> None:
        """Verify that j_max=2 produces at least 6 unique eigenvalues.

        This ensures we have enough levels to test low spectrum structure.
        """
        operator, _ = build_s3_dirac_operator(j_max=2, radius=1.0)
        eigenvalues = np.linalg.eigvalsh(operator)
        unique_eigs = np.unique(np.round(eigenvalues, 6))

        # Should have at least 6 unique eigenvalues for low spectrum analysis
        assert len(unique_eigs) >= 6, (
            f"FAIL: Expected ≥6 unique eigenvalues, got {len(unique_eigs)}\n"
            f"j_max=2 should produce k=1,2,3 levels → 6 unique eigenvalues"
        )

    def test_hermiticity(self) -> None:
        """Verify operator is Hermitian (eigenvalues are real).

        Basic sanity check: Dirac operator must be Hermitian.
        """
        operator, _ = build_s3_dirac_operator(j_max=1, radius=1.0)

        # Check Hermiticity: A† = A
        is_hermitian = np.allclose(operator, operator.conj().T)

        assert is_hermitian, "FAIL: Operator is not Hermitian"

        # Check eigenvalues are real (imaginary part negligible)
        eigenvalues = np.linalg.eigvalsh(operator)
        assert np.all(
            np.abs(np.imag(eigenvalues)) < 1e-10
        ), "FAIL: Eigenvalues have imaginary component"
