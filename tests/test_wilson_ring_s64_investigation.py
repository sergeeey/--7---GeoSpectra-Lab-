"""Wilson_ring/s64 Failures Investigation

Gate 1 showed 5 failures ONLY in wilson_ring + s1_size=64.
Other sizes (8, 16, 32) passed, other families passed s64.

Hypothesis: Numerical instability or threshold sensitivity at large dimensions.

Purpose: Reproduce failures, compare thresholds, document as bug/artifact/caveat.
"""

import numpy as np
import pytest

from cc_toy_lab.spectral.s3_s1_product_discretized import (
    analyze_s3_s1_hermiticity,
    build_s3_s1_product_operator,
)


class TestWilsonRingS64Reproduce:
    """Reproduce wilson_ring/s64 failures from Gate 1."""

    @pytest.mark.parametrize("j_max", [0, 1, 2])
    def test_wilson_ring_s64_hermiticity_strict(self, j_max):
        """Strict threshold (1e-9) — expect failures for some j_max."""
        result = analyze_s3_s1_hermiticity(
            j_max=j_max,
            s1_size=64,
            alpha=0.0,
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
            s1_family="wilson_ring",
            hermiticity_tol=1e-9,
        )

        print(f"\nWilson_ring s64 STRICT (tol=1e-9): j_max={j_max}")
        print(f"  hermiticity_residual: {result['hermiticity_residual']:.2e}")
        print(f"  total_dimension: {result['total_dimension']}")
        print(f"  passed: {result['passed']}")

        # Don't assert — just record
        # (we expect some failures here)

    @pytest.mark.parametrize("j_max", [0, 1, 2])
    def test_wilson_ring_s64_hermiticity_relaxed(self, j_max):
        """Relaxed threshold (1e-8) — check if failures disappear."""
        result = analyze_s3_s1_hermiticity(
            j_max=j_max,
            s1_size=64,
            alpha=0.0,
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
            s1_family="wilson_ring",
            hermiticity_tol=1e-8,
        )

        print(f"\nWilson_ring s64 RELAXED (tol=1e-8): j_max={j_max}")
        print(f"  hermiticity_residual: {result['hermiticity_residual']:.2e}")
        print(f"  passed: {result['passed']}")

        # Check if relaxed threshold helps
        if not result["passed"]:
            print(f"  ⚠️ STILL FAILS even with tol=1e-8")


class TestS64Comparison:
    """Compare wilson_ring/s64 vs other families/sizes."""

    def test_spectral_circle_s64_baseline(self):
        """Spectral_circle/s64 should pass (baseline)."""
        result = analyze_s3_s1_hermiticity(
            j_max=2,
            s1_size=64,
            alpha=0.0,
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
            s1_family="spectral_circle",
            hermiticity_tol=1e-9,
        )

        print(f"\nSpectral_circle s64 (baseline): j_max=2")
        print(f"  hermiticity_residual: {result['hermiticity_residual']:.2e}")
        print(f"  passed: {result['passed']}")

        assert result["passed"], (
            f"Baseline (spectral_circle/s64) should pass: "
            f"residual={result['hermiticity_residual']:.2e}"
        )

    def test_wilson_ring_s32_should_pass(self):
        """Wilson_ring/s32 should pass (smaller size)."""
        result = analyze_s3_s1_hermiticity(
            j_max=2,
            s1_size=32,
            alpha=0.0,
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
            s1_family="wilson_ring",
            hermiticity_tol=1e-9,
        )

        print(f"\nWilson_ring s32 (smaller): j_max=2")
        print(f"  hermiticity_residual: {result['hermiticity_residual']:.2e}")
        print(f"  passed: {result['passed']}")

        assert result["passed"], (
            f"Wilson_ring/s32 should pass (only s64 fails): "
            f"residual={result['hermiticity_residual']:.2e}"
        )

    def test_ring_s64_comparison(self):
        """Ring/s64 for comparison (different family)."""
        result = analyze_s3_s1_hermiticity(
            j_max=2,
            s1_size=64,
            alpha=0.0,
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
            s1_family="ring",
            hermiticity_tol=1e-9,
        )

        print(f"\nRing s64 (different family): j_max=2")
        print(f"  hermiticity_residual: {result['hermiticity_residual']:.2e}")
        print(f"  passed: {result['passed']}")

        # Don't assert — ring had its own issues at small sizes


class TestScalingAnalysis:
    """Analyze how Hermiticity residual scales with s1_size."""

    def test_wilson_ring_scaling(self):
        """Check Hermiticity residual vs s1_size for wilson_ring."""
        j_max = 2
        sizes = [8, 16, 32, 64]
        residuals = []

        for s1_size in sizes:
            result = analyze_s3_s1_hermiticity(
                j_max=j_max,
                s1_size=s1_size,
                alpha=0.0,
                disorder_strength=0.0,
                seed=123,
                radius=1.0,
                s1_family="wilson_ring",
                hermiticity_tol=1e-9,
            )
            residuals.append(result["hermiticity_residual"])

            print(f"\nWilson_ring scaling: s1_size={s1_size}")
            print(f"  hermiticity_residual: {result['hermiticity_residual']:.2e}")
            print(f"  total_dimension: {result['total_dimension']}")

        # Check if residual grows with size
        print(f"\nScaling summary:")
        for size, res in zip(sizes, residuals):
            print(f"  s1_size={size:3d}: residual={res:.2e}")

        # Hypothesis: residual should grow roughly as O(sqrt(N)) or O(N) for numerical errors
        # If residual jumps discontinuously at s64 → threshold issue
        # If residual grows smoothly → numerical accumulation


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
