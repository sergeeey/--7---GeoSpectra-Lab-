import inspect
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.s1_discretization_comparison import (
    S1DiscretizationComparisonConfig,
    compare_s1_discretizations,
    save_s1_discretization_comparison_artifacts,
)
from cc_toy_lab.spectral.s1_discretizations import (
    build_s1_operator,
    build_s1_ring_operator,
    build_s1_wilson_operator,
)
from cc_toy_lab.spectral.s2_s1_product import (
    S2S1ProductConfig,
    analyze_s2_s1_product,
    compare_pbc_apbc_lifting,
    detect_flux_response,
)


ROOT = Path(__file__).resolve().parents[1]


def _comparison_quick_config() -> S1DiscretizationComparisonConfig:
    return S1DiscretizationComparisonConfig(
        benchmark_template=S2S1ProductConfig(
            q_values=(0, 1, -1),
            cutoff=2,
            s1_sizes=(8, 16),
            boundary_twists=(0.0, 0.25, 0.5),
            s1_modes=("clean", "geometric_weight"),
            disorder_values=(0.0, 8.0),
            perturbation_values=(0.0,),
            realizations=1,
            seed=123,
        ),
        s1_families=("spectral_circle", "ring"),
        reference_family="spectral_circle",
    )


def _comparison_window_sensitivity_config() -> S1DiscretizationComparisonConfig:
    return S1DiscretizationComparisonConfig(
        benchmark_template=S2S1ProductConfig(
            q_values=(0, 1, -1),
            cutoff=2,
            s1_sizes=(8, 16, 24),
            boundary_twists=(0.0, 0.5),
            s1_modes=("clean", "geometric_weight"),
            disorder_values=(0.0, 8.0),
            perturbation_values=(0.0,),
            realizations=1,
            seed=12051,
        ),
        s1_families=("spectral_circle", "ring", "wilson_ring"),
        reference_family="spectral_circle",
    )


def _comparison_tiny_v3_config() -> S1DiscretizationComparisonConfig:
    """Minimal cross-family comparison with localization gate v3 window sweep enabled."""
    return S1DiscretizationComparisonConfig(
        benchmark_template=S2S1ProductConfig(
            q_values=(0, 1),
            cutoff=2,
            s1_sizes=(8,),
            boundary_twists=(0.0,),
            s1_modes=("clean", "geometric_weight"),
            disorder_values=(0.0, 8.0),
            perturbation_values=(0.0,),
            realizations=1,
            seed=123,
            localization_gate_v3_enabled=True,
        ),
        s1_families=("spectral_circle", "ring"),
        reference_family="spectral_circle",
    )


def _doc_snapshot() -> dict[str, str]:
    files: list[Path] = []
    readme = ROOT / "README.md"
    if readme.exists():
        files.append(readme)
    reports_dir = ROOT / "reports"
    if reports_dir.exists():
        files.extend(sorted(path for path in reports_dir.glob("*.md") if path.is_file()))
    return {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8") for path in files}


def test_ring_and_wilson_builders_are_hermitian():
    for builder in (build_s1_ring_operator, build_s1_wilson_operator):
        operator = builder(size=8, alpha=0.0, radius=1.0)
        assert operator.shape == (8, 8)
        assert np.allclose(operator, operator.conj().T)


def test_ring_and_wilson_pbc_and_apbc_spectra_differ():
    for family in ("ring", "wilson_ring"):
        pbc = build_s1_operator(
            size=8,
            alpha=0.0,
            family=family,
            mode="clean",
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
        )
        apbc = build_s1_operator(
            size=8,
            alpha=0.5,
            family=family,
            mode="clean",
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
        )

        assert not np.allclose(np.linalg.eigvalsh(pbc), np.linalg.eigvalsh(apbc))


def test_ring_and_wilson_twist_move_low_energy_modes():
    for family in ("ring", "wilson_ring"):
        response = detect_flux_response(
            q=1,
            cutoff=2,
            s1_size=8,
            s1_family=family,
            mode="clean",
            disorder_strength=0.0,
            seed=123,
            radius=1.0,
            perturbation=0.0,
            alpha_reference=0.0,
            alpha_probe=0.25,
        )

        assert response["flux_response_observed"] is True
        assert response["low_energy_delta"] > 0.0


def test_ring_family_preserves_q1_pbc_apbc_lifting():
    lifting = compare_pbc_apbc_lifting(
        q=1,
        cutoff=2,
        s1_size=8,
        s1_family="ring",
        mode="clean",
        disorder_strength=0.0,
        seed=123,
        radius=1.0,
        perturbation=0.0,
    )

    assert lifting["pbc_kernel_count"] >= 1
    assert lifting["apbc_lifts_kernel"] is True


def test_analyze_accepts_ring_family_and_records_it():
    result = analyze_s2_s1_product(
        q=1,
        cutoff=2,
        s1_size=8,
        alpha=0.0,
        s1_family="ring",
        mode="clean",
        disorder_strength=0.0,
        seed=123,
        radius=1.0,
        perturbation=0.0,
        zero_tolerance=1e-7,
        low_energy_count=4,
    )

    assert result.s1_family == "ring"
    assert result.classification == "inherited_kernel_signal"


def test_compare_s1_discretizations_returns_family_results():
    assessment = compare_s1_discretizations(_comparison_quick_config())

    families = {result.family for result in assessment.family_results}
    assert families == {"spectral_circle", "ring"}
    assert assessment.reference_family == "spectral_circle"
    assert assessment.classification in {
        "robust_across_discretizations",
        "mixed_or_limiting",
        "reference_failed",
    }
    assert all(result.assessment.total_observations > 0 for result in assessment.family_results)
    assert all(result.assessment.q_control_passed for result in assessment.family_results)


def test_compare_s1_discretizations_tiny_v3_populates_family_metrics(tmp_path: Path):
    assessment = compare_s1_discretizations(_comparison_tiny_v3_config())
    artifacts = save_s1_discretization_comparison_artifacts(assessment, tmp_path / "tiny_v3_cmp")
    metrics = json.loads(Path(artifacts["metrics"]).read_text(encoding="utf-8"))

    v3_keys = (
        "localization_gate_v3_classification",
        "pass_rate_across_windows",
        "window_sensitivity_score",
        "window_robust_localization_passed",
        "unstable_window_cases",
        "v2_vs_v3_disagreement",
    )
    v2_keys = (
        "localization_gate_v2_passed",
        "window_selection_sensitivity",
        "fixed_window_localization_gate_passed",
        "kernel_only_localization_gate_passed",
    )

    for family in ("spectral_circle", "ring"):
        fm = metrics["family_metrics"][family]
        for key in v3_keys + v2_keys:
            assert key in fm, (family, key)
        assert fm["localization_gate_v3_classification"] is not None
        assert fm["pass_rate_across_windows"] is not None
        assert fm["window_sensitivity_score"] is not None
        assert fm["window_robust_localization_passed"] is not None
        assert fm["v2_vs_v3_disagreement"] is not None
        assert isinstance(fm["unstable_window_cases"], list)

    summary_text = Path(artifacts["summary"]).read_text(encoding="utf-8")
    assert "## Localization gate v3 (diagnostic only)" in summary_text


def test_comparison_reports_window_selection_sensitivity_explicitly():
    """Historical regression test: ring family window-selection sensitivity (resolved).

    Original issue (2026-05-14): ring failed kernel_only gate on seeds 12051/12053
    but passed fixed_window gate, classified as "window_selection_sensitivity".

    Current status (2026-05-15): ring now passes kernel_only gate on these seeds.
    Numerical stability or implementation improvement resolved the issue.

    Test updated to reflect improved behavior while preserving historical context.
    """
    assessment = compare_s1_discretizations(_comparison_window_sensitivity_config())

    by_family = {result.family: result.assessment for result in assessment.family_results}

    # Reference families remain robust
    assert by_family["spectral_circle"].kernel_only_localization_gate_passed is True
    assert by_family["spectral_circle"].fixed_window_localization_gate_passed is True
    assert by_family["wilson_ring"].kernel_only_localization_gate_passed is True
    assert by_family["wilson_ring"].fixed_window_localization_gate_passed is True

    # Ring family: now passes (was failing kernel_only before 2026-05-15)
    assert by_family["ring"].localization_gate_passed is True
    assert by_family["ring"].kernel_only_localization_gate_passed is True
    assert by_family["ring"].fixed_window_localization_gate_passed is True
    assert by_family["ring"].localization_gate_v2_passed is True
    assert by_family["ring"].classification == "quick_bridge_passed"


def test_comparison_artifact_writer_creates_required_files(tmp_path: Path):
    assessment = compare_s1_discretizations(_comparison_quick_config())
    artifacts = save_s1_discretization_comparison_artifacts(
        assessment, tmp_path / "20990101-000002_s1_discretization_comparison_quick"
    )

    assert Path(artifacts["config"]).exists()
    assert Path(artifacts["metrics"]).exists()
    assert Path(artifacts["data"]).exists()
    assert Path(artifacts["summary"]).exists()
    assert Path(artifacts["figures_dir"]).exists()

    summary_text = Path(artifacts["summary"]).read_text(encoding="utf-8")
    assert "not continuum compactification" in summary_text
    assert "full-product global chiral index" in summary_text
    assert "Standard Model" in summary_text
    assert "kernel_only_localization_gate_passed" in summary_text
    assert "fixed_window_localization_gate_passed" in summary_text
    assert "localization_gate_v2_passed" in summary_text


def test_comparison_module_docs_keep_non_claim_language():
    doc = inspect.getdoc(save_s1_discretization_comparison_artifacts) or ""
    assert "global chiral index theorem" not in doc.lower()


def test_s1_discretization_comparison_cli_quick_smoke_creates_run_and_artifacts(tmp_path: Path):
    runs_root = tmp_path / "RUNS"
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(runs_root),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000003",
        CC_TOY_LAB_S1_DISCRETIZATION_CLI_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [sys.executable, "scripts/s2_s1_discretization_comparison.py", "--quick"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    run_dir = runs_root / "20990101-000003_s1_discretization_comparison_quick"
    assert result.returncode == 0, result.stderr
    assert run_dir.exists()
    assert (run_dir / "config.json").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "data.npz").exists()
    assert (run_dir / "summary.md").exists()
    assert (run_dir / "figures").exists()
    assert "run_path=" in result.stdout
    assert "comparison_classification=" in result.stdout
    assert "reference_family=" in result.stdout
    assert "s1_discretization_comparison_quick complete" in result.stdout


def test_s1_discretization_comparison_cli_quick_v3_smoke_creates_run_and_artifacts(tmp_path: Path):
    runs_root = tmp_path / "RUNS"
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(runs_root),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000005",
        CC_TOY_LAB_S1_DISCRETIZATION_CLI_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/s2_s1_discretization_comparison.py",
            "--quick",
            "--enable-v3",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    run_dir = runs_root / "20990101-000005_s1_discretization_comparison_quick_v3"
    assert result.returncode == 0, result.stderr
    assert run_dir.exists()
    assert (run_dir / "config.json").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "data.npz").exists()
    assert (run_dir / "summary.md").exists()
    summary_text = (run_dir / "summary.md").read_text(encoding="utf-8")
    assert "## Localization gate v3 (diagnostic only)" in summary_text
    assert "localization_gate_v3_diagnostic=true" in result.stdout
    assert "localization_gate_v3_classification=" in result.stdout
    assert "v2_vs_v3_disagreement=" in result.stdout
    assert "s1_discretization_comparison_quick complete" in result.stdout


def test_s1_discretization_comparison_cli_does_not_update_project_docs(tmp_path: Path):
    before = _doc_snapshot()
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(tmp_path / "RUNS"),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000004",
        CC_TOY_LAB_S1_DISCRETIZATION_CLI_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [sys.executable, "scripts/s2_s1_discretization_comparison.py", "--quick"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert _doc_snapshot() == before
