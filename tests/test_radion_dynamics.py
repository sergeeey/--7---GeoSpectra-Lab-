import numpy as np

from cc_toy_lab.radion.dynamics import integrate_radion_trajectory, run_multitrajectory
from cc_toy_lab.radion.potentials import DEFAULT_RADION_PARAMS, potential_b


def test_radion_ode_converges_to_R0():
    result = integrate_radion_trajectory(
        potential_b,
        initial_radius=2.5,
        initial_momentum=-0.5,
        params=DEFAULT_RADION_PARAMS,
        t_final=40.0,
        dt=0.02,
    )
    assert np.isclose(result.radius[-1], 1.1892, rtol=5e-4)


def test_multitrajectory_converges_to_one_attractor():
    results = run_multitrajectory(
        potential_b,
        initial_radii=[0.5, 0.8, 1.5, 2.5, 3.5],
        initial_momentum=0.0,
        params=DEFAULT_RADION_PARAMS,
        t_final=40.0,
        dt=0.02,
    )
    finals = np.array([item.radius[-1] for item in results])
    assert np.max(np.abs(finals - 1.1892) / 1.1892) < 5e-4
