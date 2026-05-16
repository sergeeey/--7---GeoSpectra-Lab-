import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.dirac_localization import (
    DiracLocalizationConfig,
    build_toy_dirac_localization_operator,
    run_dirac_localization_benchmark,
)


def test_dirac_localization_operator_is_hermitian_and_chiral_symmetric():
    operator = build_toy_dirac_localization_operator(size=24, mode="gauge_phase", disorder=1.5, seed=7)
    dense = operator.toarray()
    gamma = np.diag(np.r_[np.ones(24), -np.ones(24)])

    assert dense.shape == (48, 48)
    assert np.allclose(dense, dense.conj().T)
    assert np.allclose(gamma @ dense @ gamma, -dense)


def test_dirac_localization_rejects_unknown_mode():
    try:
        build_toy_dirac_localization_operator(size=16, mode="unknown", disorder=1.0, seed=1)
    except ValueError as exc:
        assert "unknown mode" in str(exc)
    else:
        raise AssertionError("unknown mode should raise ValueError")


def test_dirac_localization_benchmark_saves_artifacts(tmp_path: Path):
    config = DiracLocalizationConfig(
        sizes=(24,),
        disorder_values=(0.0, 2.0),
        modes=("clean", "random_mass"),
        realizations=2,
        seed=19,
        near_zero_tol=1e-6,
    )

    result = run_dirac_localization_benchmark(config=config, output_dir=tmp_path)

    assert result.points
    assert all(np.isfinite(point.mean_symmetry_error) for point in result.points)
    assert all(point.mean_symmetry_error < 1e-8 for point in result.points)
    assert (tmp_path / "config.json").exists()
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "data.npz").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "figures" / "dirac_spectrum.png").exists()
    assert (tmp_path / "figures" / "dirac_ipr_vs_disorder.png").exists()
    assert (tmp_path / "figures" / "dirac_r_statistics.png").exists()
    assert (tmp_path / "figures" / "dirac_near_zero_count.png").exists()


def test_dirac_localization_cli_quick_smoke():
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/dirac_localization_benchmark.py", "--quick"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert "dirac_localization_quick complete" in result.stdout
