"""Tests to ensure negative controls implementation does NOT mutate Gate 4B."""

import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cc_toy_lab.spectral.s3_s1_product_discretized import build_s3_s1_product_operator
from cc_toy_lab.controls.negative_controls import (
    build_random_hermitian_control,
    build_scrambled_geometry_control,
    build_broken_wilson_control,
)


def test_s3s1_operator_still_hermitian():
    """Verify S³×S¹ operator Hermiticity unchanged after importing negative controls."""
    # Build standard S³×S¹ operator
    op, _, meta = build_s3_s1_product_operator(
        j_max=2,
        s1_size=16,
        alpha=0.0,
        mode="clean",
        disorder_strength=0.0,
        seed=123,
        radius=1.0,
        s1_family="spectral_circle",
    )

    # Check Hermiticity
    hermiticity_residual = np.max(np.abs(op - op.conj().T))
    assert hermiticity_residual < 1e-10, (
        f"S³×S¹ operator not Hermitian after negative controls import: "
        f"residual={hermiticity_residual}"
    )


def test_s3s1_dimension_unchanged():
    """Verify S³×S¹ operator dimension formula unchanged."""
    from cc_toy_lab.spectral.dirac_s3 import s3_dimension

    # Test cases from Gate 4B grid
    test_cases = [
        (2, 16),  # j_max=2, s1_size=16
        (3, 128),  # j_max=3, s1_size=128 (max Gate 4B case)
    ]

    for j_max, s1_size in test_cases:
        op, _, meta = build_s3_s1_product_operator(
            j_max=j_max,
            s1_size=s1_size,
            alpha=0.0,
            mode="clean",
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
            s1_family="spectral_circle",
        )

        expected_dim = s3_dimension(j_max) * s1_size
        actual_dim = op.shape[0]

        assert actual_dim == expected_dim, (
            f"S³×S¹ dimension changed for (j_max={j_max}, s1_size={s1_size}): "
            f"expected {expected_dim}, got {actual_dim}"
        )


def test_controls_in_separate_module():
    """Verify negative controls are in separate module, not mixed with S³×S¹."""
    import cc_toy_lab.controls.negative_controls as controls_module
    import cc_toy_lab.spectral.s3_s1_product_discretized as s3s1_module

    # Controls module should have control builders
    assert hasattr(controls_module, "build_random_hermitian_control")
    assert hasattr(controls_module, "build_scrambled_geometry_control")
    assert hasattr(controls_module, "build_broken_wilson_control")

    # S³×S¹ module should NOT have control builders
    assert not hasattr(s3s1_module, "build_random_hermitian_control")
    assert not hasattr(s3s1_module, "build_scrambled_geometry_control")
    assert not hasattr(s3s1_module, "build_broken_wilson_control")


def test_control_hermiticity():
    """Verify all negative controls produce Hermitian matrices."""
    test_params = {
        "j_max": 2,
        "s1_size": 16,
        "disorder_strength": 10.0,
        "seed": 123,
        "radius": 1.0,
    }

    # Test random_hermitian
    op_rh, _ = build_random_hermitian_control(**test_params)
    residual_rh = np.max(np.abs(op_rh - op_rh.conj().T))
    assert residual_rh < 1e-10, f"random_hermitian not Hermitian: residual={residual_rh}"

    # Test scrambled_geometry
    op_sg, _ = build_scrambled_geometry_control(**test_params, alpha=0.0)
    residual_sg = np.max(np.abs(op_sg - op_sg.conj().T))
    assert residual_sg < 1e-10, f"scrambled_geometry not Hermitian: residual={residual_sg}"

    # Test broken_wilson
    op_bw, _ = build_broken_wilson_control(**test_params, alpha=0.0)
    residual_bw = np.max(np.abs(op_bw - op_bw.conj().T))
    assert residual_bw < 1e-10, f"broken_wilson not Hermitian: residual={residual_bw}"


def test_control_dimension_matches_s3s1():
    """Verify controls have same dimension as corresponding S³×S¹ case."""
    from cc_toy_lab.spectral.dirac_s3 import s3_dimension

    test_params = {
        "j_max": 3,
        "s1_size": 64,
        "disorder_strength": 20.0,
        "seed": 456,
        "radius": 1.0,
    }

    expected_dim = s3_dimension(test_params["j_max"]) * test_params["s1_size"]

    # Test all controls
    op_rh, meta_rh = build_random_hermitian_control(**test_params)
    assert (
        op_rh.shape[0] == expected_dim
    ), f"random_hermitian dimension mismatch: {op_rh.shape[0]} vs {expected_dim}"
    assert meta_rh["total_dimension"] == expected_dim

    op_sg, meta_sg = build_scrambled_geometry_control(**test_params, alpha=0.0)
    assert (
        op_sg.shape[0] == expected_dim
    ), f"scrambled_geometry dimension mismatch: {op_sg.shape[0]} vs {expected_dim}"
    assert meta_sg["total_dimension"] == expected_dim

    op_bw, meta_bw = build_broken_wilson_control(**test_params, alpha=0.0)
    assert (
        op_bw.shape[0] == expected_dim
    ), f"broken_wilson dimension mismatch: {op_bw.shape[0]} vs {expected_dim}"
    assert meta_bw["total_dimension"] == expected_dim


def test_control_deterministic_with_seed():
    """Verify controls are deterministic given same seed."""
    params = {
        "j_max": 2,
        "s1_size": 16,
        "disorder_strength": 10.0,
        "seed": 789,
        "radius": 1.0,
    }

    # Random hermitian
    op1, _ = build_random_hermitian_control(**params)
    op2, _ = build_random_hermitian_control(**params)
    assert np.allclose(op1, op2, atol=1e-14), "random_hermitian not deterministic"

    # Scrambled geometry
    op1, _ = build_scrambled_geometry_control(**params, alpha=0.0)
    op2, _ = build_scrambled_geometry_control(**params, alpha=0.0)
    assert np.allclose(op1, op2, atol=1e-14), "scrambled_geometry not deterministic"

    # Broken Wilson
    op1, _ = build_broken_wilson_control(**params, alpha=0.0)
    op2, _ = build_broken_wilson_control(**params, alpha=0.0)
    assert np.allclose(op1, op2, atol=1e-14), "broken_wilson not deterministic"


def test_default_execution_does_not_start_pilot():
    """Verify run_negative_controls_v0_1_22.py does NOT execute by default."""
    # This is a protocol test (not unit test)
    # Verifies --print-plan is default behavior

    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_negative_controls_v0_1_22.py",
            "--print-plan",
        ],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )

    assert result.returncode == 0, f"Script failed: {result.stderr}"

    # Should print plan, NOT execute
    assert "Total cases: 54" in result.stdout
    assert "⚠️ Execution DISABLED" in result.stdout or "without execution" in result.stdout

    # Should NOT create output files
    output_dir = Path(__file__).parent.parent / "reports" / "RUNS" / "negative_controls_v0.1.22"
    if output_dir.exists():
        # If directory exists from previous run, check it's not being written to
        initial_files = list(output_dir.glob("**/*"))

        # Run again
        subprocess.run(
            [sys.executable, "scripts/run_negative_controls_v0_1_22.py"],
            capture_output=True,
            cwd=Path(__file__).parent.parent,
        )

        final_files = list(output_dir.glob("**/*"))
        assert len(final_files) == len(
            initial_files
        ), "Default execution created new files (should only print plan)"
