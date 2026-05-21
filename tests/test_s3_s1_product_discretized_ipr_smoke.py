"""Tests for S3 x S1 Product-Discretized IPR Smoke (Gate 2)"""

import json
from pathlib import Path

import numpy as np
import pytest

from cc_toy_lab.spectral.s3_s1_product_discretized import build_s3_s1_product_operator


def test_ipr_smoke_script_exists():
    """Verify IPR smoke script exists."""
    script_path = Path("scripts/s3_s1_product_discretized_ipr_smoke.py")
    assert script_path.exists(), f"IPR smoke script not found: {script_path}"


def test_ipr_computation_basic():
    """Test basic IPR computation."""
    # Fully localized state
    psi_localized = np.zeros(100)
    psi_localized[0] = 1.0
    ipr_loc = np.sum(np.abs(psi_localized) ** 4)
    assert np.isclose(ipr_loc, 1.0), "Localized IPR should be 1.0"

    # Fully delocalized state
    psi_deloc = np.ones(100) / np.sqrt(100)
    ipr_deloc = np.sum(np.abs(psi_deloc) ** 4)
    expected_deloc = 1.0 / 100
    assert np.isclose(
        ipr_deloc, expected_deloc, rtol=1e-10
    ), f"Delocalized IPR should be 1/N = {expected_deloc}"


def test_ipr_clean_vs_disordered_mini():
    """Mini test: clean vs disordered IPR contrast for S3xS1."""
    j_max = 1
    s1_size = 8
    alpha = 0.0
    radius = 1.0
    seed = 123
    n_low = 3

    # Clean case
    H_clean, _, _ = build_s3_s1_product_operator(
        j_max=j_max,
        s1_family="spectral_circle",
        s1_size=s1_size,
        alpha=alpha,
        mode="geometric_weight",
        disorder_strength=0.0,
        seed=seed,
        radius=radius,
    )
    eigvals_clean, eigvecs_clean = np.linalg.eigh(H_clean)
    sort_idx = np.argsort(np.abs(eigvals_clean))
    eigvecs_clean = eigvecs_clean[:, sort_idx]

    ipr_clean = []
    for i in range(n_low):
        ipr = np.sum(np.abs(eigvecs_clean[:, i]) ** 4)
        ipr_clean.append(ipr)
    mean_ipr_clean = np.mean(ipr_clean)

    # Disordered case
    H_dis, _, _ = build_s3_s1_product_operator(
        j_max=j_max,
        s1_family="spectral_circle",
        s1_size=s1_size,
        alpha=alpha,
        mode="geometric_weight",
        disorder_strength=8.0,
        seed=seed,
        radius=radius,
    )
    eigvals_dis, eigvecs_dis = np.linalg.eigh(H_dis)
    sort_idx = np.argsort(np.abs(eigvals_dis))
    eigvecs_dis = eigvecs_dis[:, sort_idx]

    ipr_dis = []
    for i in range(n_low):
        ipr = np.sum(np.abs(eigvecs_dis[:, i]) ** 4)
        ipr_dis.append(ipr)
    mean_ipr_dis = np.mean(ipr_dis)

    # Contrast check
    assert (
        mean_ipr_dis > mean_ipr_clean
    ), f"Disordered IPR {mean_ipr_dis:.4f} should be > clean IPR {mean_ipr_clean:.4f}"
    contrast = mean_ipr_dis / mean_ipr_clean
    assert contrast > 1.1, f"Contrast {contrast:.2f} should be > 1.1 for mini test"


def test_ipr_ratio_to_baseline():
    """Test IPR ratio to 1/N baseline for S3xS1."""
    j_max = 2
    s1_size = 16
    H, _, _ = build_s3_s1_product_operator(
        j_max=j_max,
        s1_family="spectral_circle",
        s1_size=s1_size,
        alpha=0.0,
        mode="clean",
        disorder_strength=0.0,
        seed=42,
        radius=1.0,
    )
    N = H.shape[0]
    eigvals, eigvecs = np.linalg.eigh(H)
    sort_idx = np.argsort(np.abs(eigvals))
    eigvecs = eigvecs[:, sort_idx]

    ipr_first = np.sum(np.abs(eigvecs[:, 0]) ** 4)
    baseline = 1.0 / N
    ratio = ipr_first / baseline

    # For clean case, IPR should be O(1/N) but may be slightly higher
    assert ratio > 0.1, f"Ratio {ratio:.4f} suspiciously low"
    assert ratio < 100, f"Ratio {ratio:.4f} suspiciously high"


@pytest.mark.slow
def test_ipr_smoke_run_mini():
    """Mini run of S3xS1 IPR smoke (single family, small grid)."""
    from scripts.s3_s1_product_discretized_ipr_smoke import run_ipr_smoke

    config = {
        "families": ["spectral_circle"],
        "j_max_values": [1],
        "s1_sizes": [8],
        "alpha_values": [0.0],
        "disorder_values": [0.0, 8.0],
        "seeds": [123],
        "n_low": 3,
        "radius": 1.0,
        "mode": "geometric_weight",
    }

    output_dir = Path("reports/RUNS/test_s3_s1_ipr_smoke_mini")
    output_dir.mkdir(parents=True, exist_ok=True)

    aggregate, results = run_ipr_smoke(output_dir, config)

    # Check aggregate keys
    assert "ipr_smoke_verdict" in aggregate
    assert "ipr_contrast_ratio" in aggregate
    assert aggregate["total_cases"] == 2  # 1 clean + 1 disordered

    # Check files
    assert (output_dir / "metrics.json").exists()
    assert (output_dir / "config.json").exists()
    assert (output_dir / "summary.md").exists()

    # Load and verify metrics
    with open(output_dir / "metrics.json") as f:
        metrics = json.load(f)
    assert "aggregate" in metrics
    assert "per_case" in metrics
    assert len(metrics["per_case"]) == 2

    # Verify contrast
    assert aggregate["ipr_contrast_ratio"] > 1.0, "Disordered should have higher IPR than clean"
