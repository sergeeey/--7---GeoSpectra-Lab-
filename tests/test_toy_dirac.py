import numpy as np

from cc_toy_lab.spectral.toy_dirac import build_toy_dirac_operator


def test_toy_dirac_block_shape():
    d = build_toy_dirac_operator(size=32, mass_disorder=0.1, seed=3)
    assert d.shape == (64, 64)


def test_toy_dirac_spectrum_symmetry():
    d = build_toy_dirac_operator(size=24, mass_disorder=0.0, seed=3)
    eigenvalues = np.linalg.eigvalsh(d.toarray())
    assert np.allclose(eigenvalues, -eigenvalues[::-1], atol=1e-10)
