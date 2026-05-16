import numpy as np

from cc_toy_lab.radion.mfg import simulate_mfg
from cc_toy_lab.radion.phase_transition import scan_alpha_transition
from cc_toy_lab.radion.potentials import DEFAULT_RADION_PARAMS


def test_mfg_self_consistency():
    result = simulate_mfg(
        target_radius=1.1892,
        n_agents=80,
        alpha=2.0,
        diffusion=0.001,
        t_final=3.0,
        dt=0.01,
        seed=5,
    )
    target = 1.0 / 1.1892
    assert abs(result.x_bar[-1] - target) / target < 0.0135


def test_phase_transition_alpha_c_smoke():
    scan = scan_alpha_transition(
        alpha_values=np.linspace(1.25, 1.45, 41),
        params=DEFAULT_RADION_PARAMS,
    )
    assert abs(scan.estimated_alpha_c - 1.345) < 0.03
    assert np.any(scan.exists_minimum[scan.alpha_values > scan.estimated_alpha_c])
