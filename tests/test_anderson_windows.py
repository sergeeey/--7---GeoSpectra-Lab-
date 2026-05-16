import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.anderson_windows import (
    AndersonWindowConfig,
    choose_window_indices,
    run_anderson_window_diagnostics,
)


def test_choose_window_indices_are_sorted_and_distinct_for_basic_windows():
    eigenvalues = np.linspace(-3.0, 3.0, 31)

    center = choose_window_indices(eigenvalues, "center", fraction=0.2, min_levels=4)
    lower = choose_window_indices(eigenvalues, "lower", fraction=0.2, min_levels=4)
    upper = choose_window_indices(eigenvalues, "upper", fraction=0.2, min_levels=4)

    assert np.all(np.diff(eigenvalues[center]) >= 0)
    assert np.array_equal(lower, np.arange(lower.size))
    assert np.array_equal(upper, np.arange(eigenvalues.size - upper.size, eigenvalues.size))
    assert np.max(np.abs(eigenvalues[center])) <= 0.6


def test_quantile_window_targets_requested_spectral_region():
    eigenvalues = np.linspace(-10.0, 10.0, 101)

    q10 = choose_window_indices(eigenvalues, "quantile_0.1", fraction=0.1)
    q90 = choose_window_indices(eigenvalues, "quantile_0.9", fraction=0.1)

    assert np.mean(eigenvalues[q10]) < -6.0
    assert np.mean(eigenvalues[q90]) > 6.0
    assert q10.size == q90.size


def test_anderson_window_diagnostics_save_artifacts(tmp_path: Path):
    config = AndersonWindowConfig(
        lattice_sizes=(4,),
        disorder_values=(4.0, 24.0),
        realizations=2,
        seed=17,
        windows=("center", "lower", "upper"),
        window_fraction=0.2,
    )

    result = run_anderson_window_diagnostics(config=config, output_dir=tmp_path)

    assert result.points
    assert {point.window_name for point in result.points} == {"center", "lower", "upper"}
    assert all(np.isfinite(point.mean_r) for point in result.points)
    assert all(np.isfinite(point.mean_ipr) for point in result.points)
    assert all(point.realizations == 2 for point in result.points)
    assert all(point.n_levels_used >= 8 for point in result.points)
    assert (tmp_path / "config.json").exists()
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "data.npz").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "figures" / "r_by_window.png").exists()
    assert (tmp_path / "figures" / "ipr_by_window.png").exists()
    assert (tmp_path / "figures" / "window_comparison_heatmap.png").exists()


def test_anderson_window_cli_quick_smoke():
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/anderson_3d_spectrum_windows.py", "--quick"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    assert "anderson_3d_spectrum_windows_quick" in result.stdout
