import numpy as np

from cc_toy_lab.spectral.anderson import build_anderson_hamiltonian, run_anderson_sweep


def test_anderson_matrix_is_symmetric():
    h = build_anderson_hamiltonian(size=64, disorder=2.0, seed=7)
    dense = h.toarray()
    assert np.allclose(dense, dense.T)


def test_anderson_reproducible_seed():
    h1 = build_anderson_hamiltonian(size=32, disorder=4.0, seed=42).toarray()
    h2 = build_anderson_hamiltonian(size=32, disorder=4.0, seed=42).toarray()
    assert np.allclose(h1, h2)


def test_anderson_ipr_increases_with_strong_disorder_smoke():
    result = run_anderson_sweep(
        sizes=[96],
        disorder_values=[0.5, 30.0],
        realizations=4,
        seed=12,
        window_fraction=0.5,
    )
    low = result.by_size[96][0]
    high = result.by_size[96][1]
    assert high.mean_ipr > low.mean_ipr
