"""Gate 1 Hermiticity test for S³×S¹ operators.

GATE 1 CHECKPOINT:
- Test: Hermiticity residual max|H - H†| < 1e-9
- Cases: 3 (j_max=0, 1, 2) × 2 (s1_size=8, 16) = 6 tests
- Pass threshold: 100% (all tests pass)

SUCCESS CRITERIA:
- All 6 tests pass → Gate 1 PASS → proceed to Tom message + Gate 2
- Any failure → Gate 1 FAIL → fallback Option A (contact reviewers)
"""

import numpy as np
import pytest

from cc_toy_lab.spectral.dirac_s3 import build_s3_dirac_operator, s3_dimension
from cc_toy_lab.spectral.s3_s1_product_discretized import (
    analyze_s3_s1_hermiticity,
    build_s3_s1_product_operator,
)


def test_s3_dimension_calculation():
    """Verify S³ Hilbert space dimension formula (arXiv:1103.4097 degeneracy)."""
    # j_max=0: k=1 → 2(1+1)² = 8
    assert s3_dimension(0) == 8

    # j_max=1: k=1,2 → 8 + 2(2+1)² = 8 + 18 = 26
    assert s3_dimension(1) == 26

    # j_max=2: k=1,2,3 → 8 + 18 + 2(3+1)² = 8 + 18 + 32 = 58
    assert s3_dimension(2) == 58


def test_s3_dirac_operator_hermiticity():
    """Verify S³ Dirac operator is Hermitian."""
    for j_max in [0, 1, 2]:
        d_s3, chi_s3 = build_s3_dirac_operator(j_max=j_max, radius=1.0)

        # Check Hermiticity
        residual = np.max(np.abs(d_s3 - d_s3.conj().T))
        assert (
            residual < 1e-12
        ), f"S³ Dirac operator not Hermitian at j_max={j_max}: residual={residual}"

        # Check dimension
        expected_dim = s3_dimension(j_max)
        assert d_s3.shape == (expected_dim, expected_dim), f"Dimension mismatch at j_max={j_max}"


@pytest.mark.parametrize("j_max", [0, 1, 2])
@pytest.mark.parametrize("s1_size", [8, 16])
def test_s3_s1_product_hermiticity(j_max, s1_size):
    """Gate 1 checkpoint: S³×S¹ Hermiticity test.

    PASS THRESHOLD: hermiticity_residual < 1e-9 for ALL cases.
    """
    result = analyze_s3_s1_hermiticity(
        j_max=j_max,
        s1_size=s1_size,
        alpha=0.0,
        disorder_strength=0.0,
        seed=123,
        radius=1.0,
        s1_family="spectral_circle",
        hermiticity_tol=1e-9,
    )

    print(f"\nGate 1 test: j_max={j_max}, s1_size={s1_size}")
    print(f"  hermiticity_residual: {result['hermiticity_residual']:.2e}")
    print(f"  s3_dimension: {result['s3_dimension']}")
    print(f"  total_dimension: {result['total_dimension']}")
    print(f"  passed: {result['passed']}")

    assert result["passed"], (
        f"Gate 1 FAILED: Hermiticity test for j_max={j_max}, s1_size={s1_size}\n"
        f"  hermiticity_residual={result['hermiticity_residual']:.2e} >= 1e-9"
    )


def test_s3_s1_product_shape():
    """Verify S³×S¹ product structure: total_dim = s3_dim × s1_size."""
    j_max = 1
    s1_size = 8
    op, lifted, meta = build_s3_s1_product_operator(
        j_max=j_max,
        s1_size=s1_size,
        alpha=0.0,
        mode="clean",
        disorder_strength=0.0,
        seed=123,
        radius=1.0,
        s1_family="spectral_circle",
    )

    s3_dim = s3_dimension(j_max)
    expected_total = s3_dim * s1_size

    assert (
        op.shape[0] == expected_total
    ), f"Operator shape mismatch: {op.shape[0]} != {expected_total}"
    assert op.shape[1] == expected_total, "Operator not square"
    assert meta["s3_dimension"] == s3_dim
    assert meta["total_dimension"] == expected_total
    assert (
        lifted.shape[0] == expected_total
    ), f"Lifted chirality shape mismatch: {lifted.shape[0]} != {expected_total}"


def test_gate_1_summary():
    """Gate 1 summary: run all Hermiticity tests and report pass/fail."""
    test_cases = [
        (0, 8),
        (0, 16),
        (1, 8),
        (1, 16),
        (2, 8),
        (2, 16),
    ]

    results = []
    for j_max, s1_size in test_cases:
        result = analyze_s3_s1_hermiticity(
            j_max=j_max,
            s1_size=s1_size,
            hermiticity_tol=1e-9,
        )
        results.append((j_max, s1_size, result["passed"], result["hermiticity_residual"]))

    print("\n" + "=" * 60)
    print("GATE 1 SUMMARY: S³×S¹ Hermiticity Test")
    print("=" * 60)
    print(f"{'j_max':<10}{'s1_size':<10}{'Passed':<10}{'Residual':<15}")
    print("-" * 60)
    for j_max, s1_size, passed, residual in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{j_max:<10}{s1_size:<10}{status:<10}{residual:<15.2e}")
    print("-" * 60)

    passed_count = sum(1 for _, _, passed, _ in results if passed)
    total_count = len(results)
    print(f"TOTAL: {passed_count}/{total_count} passed ({100*passed_count/total_count:.1f}%)")

    if passed_count == total_count:
        print("\n✓ GATE 1: PASS — All Hermiticity tests passed")
        print("→ Next: Send Tom message + prepare Gate 2 (smoke test)")
    else:
        print(f"\n✗ GATE 1: FAIL — {total_count - passed_count} tests failed")
        print("→ Fallback: Contact reviewers (Option A)")
    print("=" * 60)

    # Assert all passed for CI/CD
    assert (
        passed_count == total_count
    ), f"Gate 1 FAILED: {total_count - passed_count}/{total_count} tests failed"
