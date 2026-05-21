"""Extended wilson_ring/s64 tests — check alpha and disorder sensitivity."""

import numpy as np
import pytest

from cc_toy_lab.spectral.s3_s1_product_discretized import analyze_s3_s1_hermiticity


@pytest.mark.parametrize("j_max", [0, 1, 2])
@pytest.mark.parametrize("alpha", [0.0, 0.5, 1.0])
@pytest.mark.parametrize("disorder", [0.0, 4.0, 8.0])
@pytest.mark.parametrize("seed", [123, 456, 789])
def test_wilson_s64_grid(j_max, alpha, disorder, seed):
    """Extended parameter grid to reproduce Gate 1 failures."""
    result = analyze_s3_s1_hermiticity(
        j_max=j_max,
        s1_size=64,
        alpha=alpha,
        disorder_strength=disorder,
        seed=seed,
        radius=1.0,
        s1_family="wilson_ring",
        hermiticity_tol=1e-9,
    )

    if not result["passed"]:
        print(f"\n⚠️ FAILURE: j_max={j_max}, alpha={alpha}, disorder={disorder}, seed={seed}")
        print(f"  hermiticity_residual: {result['hermiticity_residual']:.2e}")

    # Track failures but don't assert (want to see all of them)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
