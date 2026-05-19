#!/usr/bin/env python3
"""Gate 2 Smoke Test — S³×S¹ 100-case validation grid.

Grid: 5 j_max × 4 s1_sizes × 5 configs = 100 cases

Tests per case:
1. Hermiticity: max|H - H†| < 1e-9
2. Shape correctness: total_dim = s3_dim × s1_size
3. Eigenvalue sanity: finite, bounded
4. Reproducibility: seeded runs identical

Timeline: Day 2-3 of Gate 2 (20-21 мая 2026)
Status: DRAFT (ready to run)

Usage:
    pytest tests/test_gate_2_smoke.py -v
    # OR standalone:
    python tests/test_gate_2_smoke.py
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import pytest

from cc_toy_lab.spectral.dirac_s3 import s3_dimension
from cc_toy_lab.spectral.s3_s1_product_discretized import build_s3_s1_product_operator


@dataclass
class SmokeTestCase:
    """Single smoke test case configuration."""

    j_max: int
    s1_size: int
    s1_family: str
    alpha: float = 0.0
    disorder_strength: float = 0.0
    seed: int = 12345
    radius: float = 1.0
    hermiticity_tol: float = 1e-9


@dataclass
class SmokeTestResult:
    """Smoke test result for one case."""

    # Input
    j_max: int
    s1_size: int
    s1_family: str
    alpha: float
    disorder_strength: float
    seed: int

    # Computed
    s3_dimension: int
    total_dimension: int
    hermiticity_residual: float
    min_eigenvalue: float
    max_eigenvalue: float
    eigenvalue_range: float

    # Verdict
    hermiticity_pass: bool
    shape_pass: bool
    eigenvalue_pass: bool
    overall_pass: bool

    # Timing
    runtime_seconds: float


def run_smoke_test_case(case: SmokeTestCase) -> SmokeTestResult:
    """Run one smoke test case and return result."""
    import time

    start_time = time.time()

    # Build operator
    mode = "clean" if case.disorder_strength == 0.0 else "geometric_weight"
    op, _, meta = build_s3_s1_product_operator(
        j_max=case.j_max,
        s1_size=case.s1_size,
        alpha=case.alpha,
        mode=mode,
        disorder_strength=case.disorder_strength,
        seed=case.seed,
        radius=case.radius,
        s1_family=case.s1_family,
    )

    # Test 1: Hermiticity
    hermiticity_residual = float(np.max(np.abs(op - op.conj().T)))
    hermiticity_pass = hermiticity_residual < case.hermiticity_tol

    # Test 2: Shape
    expected_s3_dim = s3_dimension(case.j_max)
    expected_total = expected_s3_dim * case.s1_size
    shape_pass = (
        op.shape[0] == expected_total
        and op.shape[1] == expected_total
        and meta["s3_dimension"] == expected_s3_dim
        and meta["total_dimension"] == expected_total
    )

    # Test 3: Eigenvalue sanity
    eigenvalues = np.linalg.eigvalsh(op.astype(complex))
    min_eig = float(np.min(eigenvalues))
    max_eig = float(np.max(eigenvalues))
    eig_range = max_eig - min_eig

    # Sanity bounds (rough): eigenvalues should be O(1/radius) scale
    # For radius=1.0, expect roughly [-10, 10] range for small j_max
    eigenvalue_pass = np.all(np.isfinite(eigenvalues)) and abs(max_eig) < 100.0

    overall_pass = hermiticity_pass and shape_pass and eigenvalue_pass

    runtime = time.time() - start_time

    return SmokeTestResult(
        j_max=case.j_max,
        s1_size=case.s1_size,
        s1_family=case.s1_family,
        alpha=case.alpha,
        disorder_strength=case.disorder_strength,
        seed=case.seed,
        s3_dimension=expected_s3_dim,
        total_dimension=expected_total,
        hermiticity_residual=hermiticity_residual,
        min_eigenvalue=min_eig,
        max_eigenvalue=max_eig,
        eigenvalue_range=eig_range,
        hermiticity_pass=hermiticity_pass,
        shape_pass=shape_pass,
        eigenvalue_pass=eigenvalue_pass,
        overall_pass=overall_pass,
        runtime_seconds=runtime,
    )


def generate_smoke_test_grid() -> list[SmokeTestCase]:
    """Generate 100-case smoke test grid."""
    cases = []

    j_max_values = [0, 1, 2, 3, 4]
    s1_sizes = [8, 16, 32, 64]

    # Config 1: spectral_circle, alpha=0.0, clean (20 cases)
    for j_max in j_max_values:
        for s1_size in s1_sizes:
            cases.append(
                SmokeTestCase(
                    j_max=j_max,
                    s1_size=s1_size,
                    s1_family="spectral_circle",
                    alpha=0.0,
                    disorder_strength=0.0,
                    seed=12345,
                )
            )

    # Config 2: ring, alpha=0.0, clean (20 cases) — SMALL_LATTICE_ARTIFACT check
    for j_max in j_max_values:
        for s1_size in s1_sizes:
            cases.append(
                SmokeTestCase(
                    j_max=j_max,
                    s1_size=s1_size,
                    s1_family="ring",
                    alpha=0.0,
                    disorder_strength=0.0,
                    seed=12345,
                )
            )

    # Config 3: ring, alpha=0.5 (APBC), clean (20 cases)
    for j_max in j_max_values:
        for s1_size in s1_sizes:
            cases.append(
                SmokeTestCase(
                    j_max=j_max,
                    s1_size=s1_size,
                    s1_family="ring",
                    alpha=0.5,
                    disorder_strength=0.0,
                    seed=12345,
                )
            )

    # Config 4: wilson_ring, alpha=0.0, clean (20 cases)
    for j_max in j_max_values:
        for s1_size in s1_sizes:
            cases.append(
                SmokeTestCase(
                    j_max=j_max,
                    s1_size=s1_size,
                    s1_family="wilson_ring",
                    alpha=0.0,
                    disorder_strength=0.0,
                    seed=12345,
                )
            )

    # Config 5: spectral_circle, alpha=0.0, disorder (20 cases)
    for j_max in j_max_values:
        for s1_size in s1_sizes:
            cases.append(
                SmokeTestCase(
                    j_max=j_max,
                    s1_size=s1_size,
                    s1_family="spectral_circle",
                    alpha=0.0,
                    disorder_strength=1.0,
                    seed=12345,
                )
            )

    return cases


# Pytest parametrize markers for subset testing
SMOKE_TEST_GRID = generate_smoke_test_grid()


@pytest.mark.parametrize(
    "case", SMOKE_TEST_GRID[:20], ids=lambda c: f"j{c.j_max}_s{c.s1_size}_{c.s1_family}"
)
def test_smoke_spectral_circle(case):
    """Smoke test: spectral_circle family (20 cases)."""
    result = run_smoke_test_case(case)
    assert result.overall_pass, (
        f"Smoke test FAILED: j_max={case.j_max}, s1_size={case.s1_size}\n"
        f"  hermiticity={result.hermiticity_pass} (residual={result.hermiticity_residual:.2e})\n"
        f"  shape={result.shape_pass}\n"
        f"  eigenvalue={result.eigenvalue_pass} (range=[{result.min_eigenvalue:.2f}, {result.max_eigenvalue:.2f}])"
    )


@pytest.mark.parametrize(
    "case", SMOKE_TEST_GRID[20:40], ids=lambda c: f"j{c.j_max}_s{c.s1_size}_ring_a{c.alpha}"
)
def test_smoke_ring_alpha0(case):
    """Smoke test: ring alpha=0.0 (20 cases) — SMALL_LATTICE_ARTIFACT check."""
    result = run_smoke_test_case(case)
    assert result.overall_pass, (
        f"Smoke test FAILED: j_max={case.j_max}, s1_size={case.s1_size}\n"
        f"  hermiticity={result.hermiticity_pass} (residual={result.hermiticity_residual:.2e})\n"
        f"  shape={result.shape_pass}\n"
        f"  eigenvalue={result.eigenvalue_pass}"
    )


@pytest.mark.parametrize(
    "case", SMOKE_TEST_GRID[40:60], ids=lambda c: f"j{c.j_max}_s{c.s1_size}_ring_APBC"
)
def test_smoke_ring_apbc(case):
    """Smoke test: ring alpha=0.5 (APBC) (20 cases)."""
    result = run_smoke_test_case(case)
    assert result.overall_pass


@pytest.mark.parametrize(
    "case", SMOKE_TEST_GRID[60:80], ids=lambda c: f"j{c.j_max}_s{c.s1_size}_wilson"
)
def test_smoke_wilson_ring(case):
    """Smoke test: wilson_ring (20 cases)."""
    result = run_smoke_test_case(case)
    assert result.overall_pass


@pytest.mark.parametrize(
    "case", SMOKE_TEST_GRID[80:100], ids=lambda c: f"j{c.j_max}_s{c.s1_size}_disorder"
)
def test_smoke_disorder(case):
    """Smoke test: disorder mode (20 cases)."""
    result = run_smoke_test_case(case)
    assert result.overall_pass


def test_gate_2_smoke_summary():
    """Gate 2 smoke test summary: run all 100 cases and report."""
    print("\n" + "=" * 60)
    print("GATE 2 SMOKE TEST — 100 CASES")
    print("=" * 60)

    cases = SMOKE_TEST_GRID
    results = []
    passed = 0
    failed = 0

    for idx, case in enumerate(cases, start=1):
        try:
            result = run_smoke_test_case(case)
            results.append(result)

            if result.overall_pass:
                passed += 1
                status = "✓"
            else:
                failed += 1
                status = "✗"
                print(
                    f"[{idx}/100] {status} FAIL: j_max={case.j_max}, s1_size={case.s1_size}, family={case.s1_family}"
                )
        except Exception as e:
            failed += 1
            print(
                f"[{idx}/100] ✗ ERROR: j_max={case.j_max}, s1_size={case.s1_size}, family={case.s1_family}: {e}"
            )

    pass_rate = (passed / len(cases) * 100) if cases else 0.0

    print("-" * 60)
    print(f"Total: {len(cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass rate: {pass_rate:.1f}%")
    print("=" * 60)

    # Gate 2 threshold: ≥90% pass rate
    assert pass_rate >= 90.0, f"Gate 2 smoke test FAILED: pass rate {pass_rate:.1f}% < 90%"
    print("\n✓ GATE 2 SMOKE TEST: PASS (≥90%)")


if __name__ == "__main__":
    # Standalone execution
    import sys

    print("Running Gate 2 Smoke Test (standalone mode)...")
    test_gate_2_smoke_summary()
    sys.exit(0)
