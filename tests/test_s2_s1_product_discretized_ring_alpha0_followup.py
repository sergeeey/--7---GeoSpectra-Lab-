"""Tests for ring/alpha=0 targeted follow-up diagnostic."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from cc_toy_lab.spectral.s2_s1_product_discretized_ring_alpha0_followup import (
    build_ring_alpha0_followup_config,
    estimate_ring_alpha0_case_count,
    run_ring_alpha0_followup,
    save_ring_alpha0_followup_artifacts,
)


def test_smoke_config_has_lattice_scaling() -> None:
    cfg = build_ring_alpha0_followup_config(smoke=True)
    assert cfg.ring_s1_sizes == (8, 16, 32)
    assert cfg.alpha == 0.0


def test_smoke_case_count() -> None:
    cfg = build_ring_alpha0_followup_config(smoke=True)
    ring = 1 * 3 * 3 * 3  # seeds * q * sizes * W = 27
    ref = 1 * 1 * 2 * 2 * 2  # seeds * families * q * sizes * W = 8
    assert estimate_ring_alpha0_case_count(cfg) == ring + ref


def test_full_config_case_count() -> None:
    cfg = build_ring_alpha0_followup_config(smoke=False)
    ring = 3 * 7 * 7 * 7  # seeds * q * sizes * W = 1029
    ref = 2 * 2 * 5 * 4 * 4  # seeds * families * q * sizes * W = 320
    assert estimate_ring_alpha0_case_count(cfg) == ring + ref  # 1349


def test_smoke_run_completes() -> None:
    cfg = build_ring_alpha0_followup_config(smoke=True)
    run = run_ring_alpha0_followup(cfg)
    assert len(run.cases) == 35
    assert run.classification
    assert "verdict" in run.decision_rules


def test_artifacts_and_summary_non_claims(tmp_path: Path) -> None:
    cfg = build_ring_alpha0_followup_config(smoke=True)
    run = run_ring_alpha0_followup(cfg)
    paths = save_ring_alpha0_followup_artifacts(run, tmp_path / "ring_alpha0")
    assert paths["config"].exists()
    assert paths["metrics"].exists()
    assert paths["data"].exists()
    assert paths["summary"].exists()
    assert (tmp_path / "ring_alpha0" / "figures" / ".placeholder").exists()

    cfg_j = json.loads(paths["config"].read_text(encoding="utf-8"))
    assert cfg_j["ring_s1_sizes"] == [8, 16, 32]
    assert cfg_j["alpha"] == 0.0

    text = paths["summary"].read_text(encoding="utf-8")
    assert "Scientific non-claims" in text
    assert "Witten" in text or "Lichnerowicz" in text

    blob = text + paths["metrics"].read_text(encoding="utf-8")
    assert "global_chiral_index" not in blob.lower()
    assert "physical_chirality_proven" not in blob.lower()


def test_metrics_row_has_failure_type(tmp_path: Path) -> None:
    cfg = build_ring_alpha0_followup_config(smoke=True)
    run = run_ring_alpha0_followup(cfg)
    save_ring_alpha0_followup_artifacts(run, tmp_path / "m")
    m = json.loads((tmp_path / "m" / "metrics.json").read_text(encoding="utf-8"))
    row = m["cases"][0]
    for k in (
        "failure_type",
        "localization_gate_v3_classification",
        "pass_rate_across_windows",
        "window_sensitivity_score",
        "unstable_window_cases",
        "window_robust_localization_passed",
        "localization_gate_v2_passed",
        "kernel_only_localization_gate_passed",
        "v2_vs_v3_disagreement",
        "clean_kernel_count",
        "disordered_kernel_count",
        "clean_min_abs_eigenvalue",
        "disordered_min_abs_eigenvalue",
    ):
        assert k in row


def test_cli_smoke(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    runs = tmp_path / "RUNS"
    env = {
        **os.environ,
        "CC_TOY_LAB_RUNS_ROOT": str(runs),
        "CC_TOY_LAB_FIXED_TIMESTAMP": "20990103-000042",
    }
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized_ring_alpha0_followup.py"],
        cwd=root,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    rd = runs / "20990103-000042_s2_s1_product_discretized_ring_alpha0_followup"
    assert rd.exists()
    assert "ring_alpha0_followup_classification=" in r.stdout
    assert "decision_verdict=" in r.stdout


def test_cli_dry_run() -> None:
    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized_ring_alpha0_followup.py", "--dry-run"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert "dry_run=True" in r.stdout
    assert "estimated_case_count=" in r.stdout
    assert "ring_s1_sizes=" in r.stdout
