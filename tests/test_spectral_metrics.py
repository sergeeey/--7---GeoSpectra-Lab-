import numpy as np

from cc_toy_lab.spectral.metrics import inverse_participation_ratio, mean_adjacent_gap_ratio


def test_r_statistic_poisson_synthetic():
    rng = np.random.default_rng(123)
    spacings = rng.exponential(scale=1.0, size=5000)
    levels = np.cumsum(spacings)
    r = mean_adjacent_gap_ratio(levels)
    assert 0.35 < r < 0.42


def test_r_statistic_goe_synthetic():
    rng = np.random.default_rng(123)
    values = []
    for _ in range(5):
        matrix = rng.normal(size=(180, 180))
        matrix = (matrix + matrix.T) / 2.0
        levels = np.linalg.eigvalsh(matrix)
        values.append(mean_adjacent_gap_ratio(levels[45:135]))
    r = float(np.mean(values))
    assert 0.48 < r < 0.58


def test_ipr_delocalized_vector():
    psi = np.ones(100) / np.sqrt(100)
    assert np.isclose(inverse_participation_ratio(psi), 0.01)


def test_ipr_localized_vector():
    psi = np.zeros(100)
    psi[12] = 1.0
    assert np.isclose(inverse_participation_ratio(psi), 1.0)
