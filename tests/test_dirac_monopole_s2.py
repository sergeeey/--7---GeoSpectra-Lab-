import os
import subprocess
import sys

import numpy as np

from cc_toy_lab.spectral.dirac_monopole_s2 import (
    analyze_monopole_charge,
    build_dirac_monopole_operator,
)


def test_q_zero_gives_zero_index():
    result = analyze_monopole_charge(q=0, cutoff=3)
    assert result.expected_index == 0
    assert result.numerical_index == 0
    assert result.passed


def test_sign_flip_reverses_index():
    positive = analyze_monopole_charge(q=2, cutoff=3)
    negative = analyze_monopole_charge(q=-2, cutoff=3)
    assert positive.numerical_index == 2
    assert negative.numerical_index == -2
    assert positive.numerical_index == -negative.numerical_index


def test_cutoff_convergence_preserves_index():
    indices = [analyze_monopole_charge(q=3, cutoff=cutoff).numerical_index for cutoff in (1, 2, 4)]
    assert indices == [3, 3, 3]


def test_nonzero_eigenvalues_are_chirally_symmetric():
    operator, _chirality = build_dirac_monopole_operator(q=1, cutoff=3)
    eigenvalues = np.linalg.eigvalsh(operator)
    nonzero = eigenvalues[np.abs(eigenvalues) > 1e-8]
    assert len(nonzero) > 0
    assert np.allclose(nonzero, -nonzero[::-1], atol=1e-10)


def test_dirac_monopole_cli_quick_smoke():
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/dirac_monopole_s2.py", "--quick"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    assert "q=0" in result.stdout
    assert "q=2" in result.stdout
