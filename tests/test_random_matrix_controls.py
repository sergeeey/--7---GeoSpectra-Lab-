import os
from pathlib import Path
import subprocess
import sys

from cc_toy_lab.spectral.random_matrix_controls import (
    EXPECTED_R,
    ControlConfig,
    evaluate_controls,
    generate_gue_levels,
    generate_poisson_levels,
)


def test_poisson_levels_are_sorted_and_pipeline_near_expected():
    config = ControlConfig(matrix_size=160, realizations=12, seed=11, include_gue=False)
    results = evaluate_controls(config)
    poisson = results["poisson"]
    assert poisson.passed
    assert abs(poisson.mean_r - EXPECTED_R["poisson"]) < poisson.tolerance


def test_goe_control_pipeline_near_expected():
    config = ControlConfig(matrix_size=160, realizations=12, seed=12, include_gue=False)
    results = evaluate_controls(config)
    goe = results["goe"]
    assert goe.passed
    assert abs(goe.mean_r - EXPECTED_R["goe"]) < goe.tolerance


def test_gue_generator_is_optional_and_hermitian_pipeline_works():
    levels = generate_gue_levels(size=80, rng_seed=3)
    assert len(levels) == 80
    assert all(levels[i] <= levels[i + 1] for i in range(len(levels) - 1))


def test_evaluate_controls_can_save_artifacts(tmp_path: Path):
    config = ControlConfig(matrix_size=96, realizations=6, seed=13, include_gue=True)
    results = evaluate_controls(config, output_dir=tmp_path)
    assert {"poisson", "goe", "gue"} == set(results)
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "summary.md").exists()


def test_poisson_generation_uses_exponential_spacings():
    levels = generate_poisson_levels(size=50, rng_seed=4)
    assert len(levels) == 50
    assert all(levels[i] < levels[i + 1] for i in range(len(levels) - 1))


def test_r_stat_controls_cli_quick_smoke():
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/r_stat_controls.py", "--quick", "--no-gue"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    assert "POISSON" in result.stdout
    assert "GOE" in result.stdout
