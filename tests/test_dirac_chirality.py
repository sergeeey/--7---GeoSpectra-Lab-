import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.dirac_chirality import (
    DiracChiralityConfig,
    analyze_dirac_chirality,
    chirality_operator,
    gamma_algebra_errors,
    run_dirac_chirality_diagnostic,
)
from cc_toy_lab.spectral.dirac_localization import build_toy_dirac_localization_operator


def test_gamma_algebra_for_block_operator():
    size = 24
    operator = build_toy_dirac_localization_operator(size=size, mode="random_mass", disorder=2.0, seed=11).toarray()
    gamma = chirality_operator(size)
    gamma_square_error, gamma_hermitian_error, anticommutator_error = gamma_algebra_errors(operator, gamma)

    assert np.allclose(gamma @ gamma, np.eye(2 * size))
    assert gamma_square_error < 1e-12
    assert gamma_hermitian_error < 1e-12
    assert anticommutator_error < 1e-12


def test_clean_zero_modes_are_paired_zero_index():
    observation = analyze_dirac_chirality(size=24, mode="clean", disorder=0.0, seed=3)

    assert observation.near_zero_count == 2
    assert observation.n_plus == 1
    assert observation.n_minus == 1
    assert observation.numerical_index == 0
    assert observation.classification == "paired_accidental_or_symmetry_zero_modes"


def test_chirality_diagnostic_saves_artifacts(tmp_path: Path):
    config = DiracChiralityConfig(
        sizes=(24,),
        disorder_values=(0.0, 2.0),
        modes=("clean", "random_mass"),
        realizations=2,
        seed=23,
    )

    result = run_dirac_chirality_diagnostic(config=config, output_dir=tmp_path)

    assert result.gamma_algebra_passed
    assert result.anticommutation_preserved
    assert result.all_indices_zero
    assert (tmp_path / "config.json").exists()
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "data.npz").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "figures" / "chirality_expectations.png").exists()
    assert (tmp_path / "figures" / "index_vs_disorder.png").exists()
    assert (tmp_path / "figures" / "near_zero_chirality_scatter.png").exists()
    assert (tmp_path / "figures" / "anticommutator_error.png").exists()


def test_dirac_chirality_cli_quick_smoke():
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/dirac_chirality_diagnostic.py", "--quick"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert "gamma_algebra_passed=True" in result.stdout
    assert "dirac_chirality_quick complete" in result.stdout
