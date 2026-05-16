import numpy as np

from cc_toy_lab.radion.potentials import (
    DEFAULT_RADION_PARAMS,
    curvature,
    find_minimum,
    potential_a,
    potential_b,
)


def test_potential_B_minimum_matches_R0():
    params = DEFAULT_RADION_PARAMS
    minimum = find_minimum(potential_b, params, bracket=(0.2, 4.5))
    assert np.isclose(minimum.radius, 1.1892, atol=5e-4)


def test_potential_B_curvature_positive():
    params = DEFAULT_RADION_PARAMS
    minimum = find_minimum(potential_b, params, bracket=(0.2, 4.5))
    assert curvature(potential_b, minimum.radius, params) > 0.0


def test_unstable_potential_A_no_false_minimum():
    params = DEFAULT_RADION_PARAMS
    left = potential_a(0.5, params)
    right = potential_a(4.0, params)
    assert right < left
