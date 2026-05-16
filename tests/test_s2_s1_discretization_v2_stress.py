import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.s1_discretization_v2_stress import (
    S1DiscretizationV2StressConfig,
    _classify_stress_result,
    build_stress_config,
    run_s1_discretization_v2_stress,
    save_s1_discretization_v2_stress_artifacts,
)


ROOT = Path(__file__).resolve().parents[1]


def test_build_stress_config_matches_requested_profile():
    config = build_stress_config(seed=12051)

    assert isinstance(config, S1DiscretizationV2StressConfig)
    assert config.s1_families == ("spectral_circle", "ring", "wilson_ring")
    assert config.reference_family == "spectral_circle"

    benchmark = config.benchmark_template
    assert benchmark.q_values == (0, 1, -1, 2, -2)
    assert benchmark.cutoff == 2
    assert benchmark.s1_sizes == (8, 16, 24, 32)
    assert benchmark.boundary_twists == (0.0, 0.25, 0.5)
    assert benchmark.s1_modes == ("clean", "gauge_phase", "geometric_weight")
    assert benchmark.disorder_values == (0.0, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0)
    assert benchmark.perturbation_values == (0.0, 1e-5)
    assert benchmark.realizations == 5
    assert benchmark.zero_tolerance_scan == (1e-8, 1e-7, 1e-6)


def test_tiny_stress_profile_runs_and_collects_artifacts(tmp_path: Path):
    config = build_stress_config(seed=123, test_profile="tiny")

    assessment = run_s1_discretization_v2_stress(config)
    artifacts = save_s1_discretization_v2_stress_artifacts(
        assessment, tmp_path / "20990101-000010_s1_discretization_v2_stress"
    )

    assert assessment.reference_family == "spectral_circle"
    assert assessment.stress_classification in {"v2_stress_passed", "v2_limitation"}
    assert len(assessment.family_results) == 3

    assert Path(artifacts["config"]).exists()
    assert Path(artifacts["metrics"]).exists()
    assert Path(artifacts["data"]).exists()
    assert Path(artifacts["summary"]).exists()
    assert Path(artifacts["figures_dir"]).exists()


def test_case_level_fixed_window_failures_force_v2_limitation():
    assert _classify_stress_result(fixed_window_failure_cases=[]) == "v2_stress_passed"
    assert _classify_stress_result(fixed_window_failure_cases=[{"family": "ring"}]) == "v2_limitation"


def test_stress_metrics_keep_v2_and_kernel_only_fields(tmp_path: Path):
    config = build_stress_config(seed=123, test_profile="tiny")
    assessment = run_s1_discretization_v2_stress(config)
    artifacts = save_s1_discretization_v2_stress_artifacts(
        assessment, tmp_path / "20990101-000011_s1_discretization_v2_stress"
    )

    metrics = json.loads(Path(artifacts["metrics"]).read_text(encoding="utf-8"))

    assert "family_metrics" in metrics
    assert "stress_diagnostics" in metrics
    assert "historical_kernel_only_run" in metrics
    assert "reference_v2_run" in metrics
    assert "case_level_fixed_window_all_passed" in metrics

    for family in ("spectral_circle", "ring", "wilson_ring"):
        family_metrics = metrics["family_metrics"][family]
        assert "classification" in family_metrics
        assert "all_basic_gates_passed" in family_metrics
        assert "kernel_only_localization_gate_passed" in family_metrics
        assert "fixed_window_localization_gate_passed" in family_metrics
        assert "localization_gate_v2_passed" in family_metrics
        assert "window_selection_sensitivity" in family_metrics
        assert "localization_gate_passed" in family_metrics
        assert "q_control_passed" in family_metrics
        assert "pbc_gate_passed" in family_metrics
        assert "apbc_gate_passed" in family_metrics
        assert "flux_response_observed" in family_metrics
        assert "s1_not_spectator" in family_metrics
        assert "threshold_stable" in family_metrics
        assert "total_observations" in family_metrics

    diagnostics = metrics["stress_diagnostics"]
    assert "failure_count_by_family" in diagnostics
    assert "failure_count_by_gate" in diagnostics
    assert "failure_count_by_s1_size" in diagnostics
    assert "failure_count_by_disorder" in diagnostics
    assert "failure_count_by_twist" in diagnostics
    assert "fixed_window_failure_cases" in diagnostics
    assert "kernel_only_vs_fixed_window_disagreements" in diagnostics
    assert "ring_doubler_sensitive_cases" in diagnostics


def test_stress_metrics_include_v3_fields_when_enabled(tmp_path: Path):
    config = build_stress_config(seed=123, test_profile="tiny", enable_v3=True)
    assessment = run_s1_discretization_v2_stress(config)
    artifacts = save_s1_discretization_v2_stress_artifacts(
        assessment, tmp_path / "20990101-000011_s1_discretization_v2_stress_v3"
    )

    metrics = json.loads(Path(artifacts["metrics"]).read_text(encoding="utf-8"))
    diagnostics = metrics["stress_diagnostics"]

    for family in ("spectral_circle", "ring", "wilson_ring"):
        family_metrics = metrics["family_metrics"][family]
        for key in (
            "localization_gate_v3_classification",
            "pass_rate_across_windows",
            "window_sensitivity_score",
            "window_robust_localization_passed",
            "unstable_window_cases",
            "v2_vs_v3_disagreement",
        ):
            assert key in family_metrics

    assert "v3_all_families_window_robust" in diagnostics
    assert diagnostics["v3_case_level_result_available"] is True
    assert "v3_case_level_all_passed" in diagnostics
    assert "v3_failure_cases" in diagnostics
    assert "v3_failure_count_by_family" in diagnostics
    assert "v3_failure_count_by_disorder" in diagnostics
    assert "v3_failure_count_by_s1_size" in diagnostics
    assert "v3_failure_count_by_alpha" in diagnostics
    assert "v3_failure_count_by_q" in diagnostics
    assert "v3_window_sensitive_cases" in diagnostics
    assert "v3_fragile_pass_cases" in diagnostics
    assert "v2_vs_v3_disagreement_count_by_family" in diagnostics


def test_stress_data_npz_includes_v3_case_level_arrays(tmp_path: Path):
    config = build_stress_config(seed=123, test_profile="tiny", enable_v3=True)
    assessment = run_s1_discretization_v2_stress(config)
    artifacts = save_s1_discretization_v2_stress_artifacts(
        assessment, tmp_path / "20990101-000011_s1_discretization_v2_stress_v3_npz"
    )
    data = np.load(Path(artifacts["data"]))

    expected = {
        "case_localization_gate_v3_classification",
        "case_pass_rate_across_windows",
        "case_window_sensitivity_score",
        "case_window_robust_localization_passed",
        "case_v2_vs_v3_disagreement",
        "case_localization_gate_v2_passed",
    }
    assert expected.issubset(data.files)


def test_stress_summary_keeps_non_claims_and_avoids_global_chiral_index_language(tmp_path: Path):
    config = build_stress_config(seed=123, test_profile="tiny")
    assessment = run_s1_discretization_v2_stress(config)
    artifacts = save_s1_discretization_v2_stress_artifacts(
        assessment, tmp_path / "20990101-000012_s1_discretization_v2_stress"
    )

    summary_text = Path(artifacts["summary"]).read_text(encoding="utf-8").lower()

    assert "not continuum compactification" in summary_text
    assert "not s6" in summary_text
    assert "not s3 x s6" in summary_text
    assert "not standard model" in summary_text
    assert "not physical chirality" in summary_text
    assert "not witten/lichnerowicz bypass" in summary_text
    assert "global chiral index" not in summary_text


def test_stress_cli_tiny_smoke_creates_run_and_artifacts(tmp_path: Path):
    runs_root = tmp_path / "RUNS"
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(runs_root),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000013",
        CC_TOY_LAB_S1_DISCRETIZATION_V2_STRESS_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [sys.executable, "scripts/s2_s1_discretization_v2_stress.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    run_dir = runs_root / "20990101-000013_s1_discretization_v2_stress"
    assert result.returncode == 0, result.stderr
    assert run_dir.exists()
    assert (run_dir / "config.json").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "data.npz").exists()
    assert (run_dir / "summary.md").exists()
    assert (run_dir / "figures").exists()
    assert "run_path=" in result.stdout
    assert "stress_classification=" in result.stdout
    assert "comparison_classification=" in result.stdout
    assert "s1_discretization_v2_stress complete" in result.stdout


def test_stress_cli_tiny_v3_smoke_creates_run_and_artifacts(tmp_path: Path):
    runs_root = tmp_path / "RUNS"
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(runs_root),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000014",
        CC_TOY_LAB_S1_DISCRETIZATION_V2_STRESS_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [sys.executable, "scripts/s2_s1_discretization_v2_stress.py", "--enable-v3"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    run_dir = runs_root / "20990101-000014_s1_discretization_v2_stress_v3"
    assert result.returncode == 0, result.stderr
    assert run_dir.exists()
    assert (run_dir / "metrics.json").exists()
    assert "localization_gate_v3_diagnostic=true" in result.stdout
    assert "v3_window_robust_all_families=" in result.stdout
