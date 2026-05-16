import json
import os
import subprocess
import sys
from pathlib import Path

from scripts.s1_ring_localization_diagnostic import infer_likely_cause


ROOT = Path(__file__).resolve().parents[1]


def _doc_snapshot() -> dict[str, str]:
    files: list[Path] = []
    readme = ROOT / "README.md"
    if readme.exists():
        files.append(readme)
    reports_dir = ROOT / "reports"
    if reports_dir.exists():
        files.extend(sorted(path for path in reports_dir.glob("*.md") if path.is_file()))
    return {str(path.relative_to(ROOT)): path.read_text(encoding="utf-8") for path in files}


def test_infer_likely_cause_prefers_window_selection_for_doubled_clean_kernel():
    family_metrics = {
        "spectral_circle": {
            "representative_clean_kernel_count": 1.0,
            "representative_clean_ipr": 0.041667,
            "target_failure_rate_at_w8": 0.0,
            "target_margin_flip_rate": 0.0,
            "target_fixed_window_recovery_rate": 0.0,
            "target_pass_rate_at_w12": 1.0,
        },
        "wilson_ring": {
            "representative_clean_kernel_count": 1.0,
            "representative_clean_ipr": 0.041667,
            "target_failure_rate_at_w8": 0.0,
            "target_margin_flip_rate": 0.0,
            "target_fixed_window_recovery_rate": 0.0,
            "target_pass_rate_at_w12": 1.0,
        },
        "ring": {
            "representative_clean_kernel_count": 2.0,
            "representative_clean_ipr": 0.081551,
            "target_failure_rate_at_w8": 0.25,
            "target_margin_flip_rate": 0.0,
            "target_fixed_window_recovery_rate": 1.0,
            "target_pass_rate_at_w12": 1.0,
        },
    }

    likely_cause, notes = infer_likely_cause(family_metrics)

    assert likely_cause == "window_selection"
    assert any("extra clean kernel" in note for note in notes)


def test_s1_ring_localization_diagnostic_cli_smoke_creates_artifacts(tmp_path: Path):
    runs_root = tmp_path / "RUNS"
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(runs_root),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000005",
        CC_TOY_LAB_RING_DIAGNOSTIC_CLI_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [sys.executable, "scripts/s1_ring_localization_diagnostic.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    run_dir = runs_root / "20990101-000005_s1_ring_localization_diagnostic"
    assert result.returncode == 0, result.stderr
    assert run_dir.exists()
    assert (run_dir / "config.json").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "data.npz").exists()
    assert (run_dir / "summary.md").exists()
    assert (run_dir / "figures").exists()
    assert (run_dir / "figures" / "ring_ipr_vs_disorder.png").exists()
    assert (run_dir / "figures" / "family_ipr_comparison.png").exists()
    assert (run_dir / "figures" / "ipr_delta_heatmap.png").exists()
    assert "run_path=" in result.stdout
    assert "likely_cause=" in result.stdout
    assert "s1_ring_localization_diagnostic complete" in result.stdout

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["likely_cause"] in {
        "weak_disorder",
        "margin_artifact",
        "finite_size",
        "window_selection",
        "basis_artifact",
        "unresolved",
    }
    assert {"spectral_circle", "ring", "wilson_ring"} == set(metrics["family_metrics"])


def test_s1_ring_localization_diagnostic_cli_does_not_update_project_docs(tmp_path: Path):
    before = _doc_snapshot()
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(tmp_path / "RUNS"),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000006",
        CC_TOY_LAB_RING_DIAGNOSTIC_CLI_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [sys.executable, "scripts/s1_ring_localization_diagnostic.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert _doc_snapshot() == before
