import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.anderson_3d import build_anderson_3d_hamiltonian


def test_periodic_boundary_adds_wraparound_edges():
    open_h = build_anderson_3d_hamiltonian(lattice_size=4, disorder=2.0, seed=13, periodic=False)
    periodic_h = build_anderson_3d_hamiltonian(lattice_size=4, disorder=2.0, seed=13, periodic=True)

    open_dense = open_h.toarray()
    periodic_dense = periodic_h.toarray()

    assert np.allclose(periodic_dense, periodic_dense.T)
    assert np.count_nonzero(periodic_dense) > np.count_nonzero(open_dense)
    assert not np.allclose(periodic_dense, open_dense)


def test_anderson_boundary_comparison_cli_smoke(tmp_path: Path):
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/anderson_3d_boundary_comparison.py", "--smoke"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert "anderson_3d_boundary_comparison complete" in result.stdout
