import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.anderson_3d import (
    Anderson3DConfig,
    build_anderson_3d_hamiltonian,
    run_anderson_3d_benchmark,
)


def test_anderson_3d_matrix_is_symmetric_and_right_size():
    hamiltonian = build_anderson_3d_hamiltonian(lattice_size=4, disorder=3.0, seed=7)
    dense = hamiltonian.toarray()
    assert dense.shape == (64, 64)
    assert np.allclose(dense, dense.T)


def test_anderson_3d_seed_is_reproducible():
    h1 = build_anderson_3d_hamiltonian(lattice_size=4, disorder=5.0, seed=11).toarray()
    h2 = build_anderson_3d_hamiltonian(lattice_size=4, disorder=5.0, seed=11).toarray()
    assert np.allclose(h1, h2)


def test_anderson_3d_ipr_increases_with_strong_disorder(tmp_path: Path):
    config = Anderson3DConfig(
        lattice_sizes=(4,),
        disorder_values=(4.0, 24.0),
        realizations=2,
        seed=5,
        eigen_count=24,
    )
    result = run_anderson_3d_benchmark(config=config, output_dir=tmp_path)
    points = result.by_size[4]
    assert points[-1].mean_ipr > points[0].mean_ipr
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "figures" / "anderson_3d_r_statistics.png").exists()
    assert (tmp_path / "figures" / "anderson_3d_ipr.png").exists()


def test_anderson_3d_reports_finite_values(tmp_path: Path):
    config = Anderson3DConfig(
        lattice_sizes=(4,),
        disorder_values=(4.0, 12.0),
        realizations=2,
        seed=9,
        eigen_count=24,
    )
    result = run_anderson_3d_benchmark(config=config, output_dir=tmp_path)
    for point in result.by_size[4]:
        assert np.isfinite(point.mean_r)
        assert np.isfinite(point.mean_ipr)
        assert point.realizations == 2


def test_anderson_3d_cli_quick_smoke():
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/anderson_3d_benchmark.py", "--quick"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    assert "anderson_3d_benchmark_quick" in result.stdout
