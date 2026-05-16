"""Tests for product-discretized S2 x S1 toy scaffold."""

from __future__ import annotations

import dataclasses
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from cc_toy_lab.spectral.s2_s1_product_discretized import (
    ProductDiscretizedConfig,
    analyze_product_discretized_case,
    assess_product_discretized_results,
    build_product_discretized_config,
    build_product_discretized_operator,
    estimate_product_discretized_case_count,
    full_profile_dry_run_report,
    medium_profile_dry_run_report,
    run_product_discretized_full,
    run_product_discretized_tiny,
    save_product_discretized_artifacts,
    serialize_product_discretized_case,
)


def test_config_builds() -> None:
    cfg = build_product_discretized_config(tiny=True, seed=123)
    assert isinstance(cfg, ProductDiscretizedConfig)
    assert cfg.profile_name == "tiny"
    assert cfg.seeds == (123,)


def test_medium_config_builds_and_case_count() -> None:
    cfg = build_product_discretized_config(medium=True)
    assert cfg.profile_name == "medium"
    assert cfg.q_values == (0, 1, -1, 2, -2)
    assert cfg.s1_sizes == (8, 16, 24)
    assert cfg.alpha_values == (0.0, 0.25, 0.5)
    assert cfg.w_values == (0.0, 4.0, 8.0, 12.0)
    assert cfg.seeds == (123, 456)
    assert estimate_product_discretized_case_count(cfg) == 1080
    rep = medium_profile_dry_run_report(cfg)
    assert rep["expected_case_count"] == 1080
    assert rep["estimated_run_dir_suffix"] == "_s2_s1_product_discretized_medium"


def test_full_config_builds_and_case_count() -> None:
    cfg = build_product_discretized_config(full=True)
    assert cfg.profile_name == "full"
    assert cfg.q_values == (0, 1, -1, 2, -2, 3, -3)
    assert cfg.s1_families == ("spectral_circle", "ring", "wilson_ring")
    assert cfg.s1_sizes == (8, 16, 24, 32, 48)
    assert cfg.alpha_values == (0.0, 0.25, 0.5)
    assert cfg.w_values == (0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0)
    assert cfg.seeds == (123, 456, 789)
    assert cfg.low_energy_count_values == (4, 6, 8, 10, 12)
    assert cfg.spectator_large_s1 == 48
    assert estimate_product_discretized_case_count(cfg) == 6615
    rep = full_profile_dry_run_report(cfg)
    assert rep["profile_name"] == "full"
    assert rep["expected_case_count"] == 6615
    assert rep["estimated_run_dir_suffix"] == "_s2_s1_product_discretized_full"
    assert rep["grid_dimensions"]["low_energy_count_values"] == 5


def test_full_profile_dry_run_report_rejects_non_full_config() -> None:
    with pytest.raises(ValueError, match="full ProductDiscretizedConfig"):
        full_profile_dry_run_report(build_product_discretized_config(medium=True))


def test_build_config_rejects_ambiguous_profile() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        build_product_discretized_config(tiny=True, medium=True)
    with pytest.raises(ValueError, match="exactly one"):
        build_product_discretized_config(tiny=True, full=True)
    with pytest.raises(ValueError, match="exactly one"):
        build_product_discretized_config(medium=True, full=True)
    with pytest.raises(ValueError, match="exactly one"):
        build_product_discretized_config(tiny=False, medium=False, full=False)


def test_operator_shape() -> None:
    op, _, meta = build_product_discretized_operator(
        q=1,
        cutoff=2,
        s1_size=8,
        alpha=0.0,
        mode="clean",
        disorder_strength=0.0,
        seed=123,
        radius=1.0,
        s1_family="spectral_circle",
    )
    n = int(meta["s2_dimension"]) * 8
    assert op.shape == (n, n)


def test_operator_hermitian() -> None:
    op, _, _ = build_product_discretized_operator(
        q=-1,
        cutoff=2,
        s1_size=16,
        alpha=0.25,
        mode="geometric_weight",
        disorder_strength=4.0,
        seed=999,
        radius=1.0,
        s1_family="wilson_ring",
    )
    res = float(np.max(np.abs(op - op.conj().T)))
    assert res < 1e-9


def test_seed_reproducibility() -> None:
    a, _, _ = build_product_discretized_operator(
        q=1, cutoff=2, s1_size=8, alpha=0.0, mode="clean", disorder_strength=0.0, seed=42, radius=1.0, s1_family="ring"
    )
    b, _, _ = build_product_discretized_operator(
        q=1, cutoff=2, s1_size=8, alpha=0.0, mode="clean", disorder_strength=0.0, seed=42, radius=1.0, s1_family="ring"
    )
    assert np.allclose(a, b)


def test_q0_no_false_kernel_inflation() -> None:
    cfg = build_product_discretized_config(tiny=True, seed=123)
    c = analyze_product_discretized_case(
        cfg=cfg, q=0, s1_family="spectral_circle", s1_size=8, alpha=0.0, disorder_strength=8.0, seed=123
    )
    assert c.q0_control_passed
    assert c.disordered_kernel_count == 0


def test_tiny_runner_completes() -> None:
    cfg = build_product_discretized_config(tiny=True, seed=123)
    assessment = run_product_discretized_tiny(cfg)
    assert len(assessment.cases) == 72
    assert assessment.hermiticity_all_passed
    assert assessment.shape_all_passed
    assert assessment.reproducibility_passed


def test_tiny_includes_w0_and_w8_and_metrics_controls() -> None:
    cfg = build_product_discretized_config(tiny=True, seed=123)
    assessment = run_product_discretized_tiny(cfg)
    ws = {float(c.disorder_strength) for c in assessment.cases}
    assert 0.0 in ws and 8.0 in ws
    m = assess_product_discretized_results(assessment)
    assert m["clean_control_cases_count"] == 36
    assert m["disordered_cases_count"] == 36
    assert m["has_clean_control"] is True
    assert m["has_disordered_control"] is True
    assert m["disorder_contrast_available"] is True
    assert all(c.q0_control_passed for c in assessment.cases if c.q == 0)


def test_artifacts_saved(tmp_path: Path) -> None:
    cfg = build_product_discretized_config(tiny=True, seed=123)
    assessment = run_product_discretized_tiny(cfg)
    paths = save_product_discretized_artifacts(assessment, tmp_path / "run1")
    assert paths["config"].exists()
    assert paths["metrics"].exists()
    assert paths["data"].exists()
    assert paths["summary"].exists()
    assert (tmp_path / "run1" / "figures" / ".placeholder").exists()


def test_metrics_json_localization_fields(tmp_path: Path) -> None:
    cfg = build_product_discretized_config(tiny=True, seed=123)
    assessment = run_product_discretized_tiny(cfg)
    save_product_discretized_artifacts(assessment, tmp_path / "m")
    m = json.loads((tmp_path / "m" / "metrics.json").read_text(encoding="utf-8"))
    assert m["cases"]
    for key in (
        "clean_control_cases_count",
        "disordered_cases_count",
        "has_clean_control",
        "has_disordered_control",
        "disorder_contrast_available",
        "profile_name",
        "v3_failure_counts_by_bucket",
        "v2_vs_v3_disagreement_count",
        "ring_alpha0_cases_count",
        "ring_alpha0_failure_count",
        "q0_false_positive_count",
    ):
        assert key in m
    assert m["clean_control_cases_count"] == 36
    assert m["disordered_cases_count"] == 36
    row = m["cases"][0]
    for k in (
        "kernel_only_localization_gate_passed",
        "fixed_window_localization_gate_passed",
        "localization_gate_v2_passed",
        "pass_rate_across_windows",
        "window_sensitivity_score",
        "localization_gate_v3_classification",
        "window_robust_localization_passed",
        "flux_response_observed",
        "s1_not_spectator",
        "pbc_apbc_difference",
        "q0_control_passed",
        "ring_alpha0_caveat_detected",
    ):
        assert k in row


def test_summary_non_claims(tmp_path: Path) -> None:
    cfg = build_product_discretized_config(tiny=True, seed=123)
    assessment = run_product_discretized_tiny(cfg)
    save_product_discretized_artifacts(assessment, tmp_path / "s")
    text = (tmp_path / "s" / "summary.md").read_text(encoding="utf-8")
    assert "Scientific non-claims" in text
    assert "Witten" in text or "Witten/Lichnerowicz" in text


def test_no_forbidden_claim_language(tmp_path: Path) -> None:
    cfg = build_product_discretized_config(tiny=True, seed=123)
    assessment = run_product_discretized_tiny(cfg)
    save_product_discretized_artifacts(assessment, tmp_path / "f")
    text = (tmp_path / "f" / "summary.md").read_text(encoding="utf-8")
    blob = text + (tmp_path / "f" / "metrics.json").read_text(encoding="utf-8")
    assert "global_chiral_index" not in blob.lower()
    assert "physical_chirality_proven" not in blob.lower()


def test_cli_tiny_smoke(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    runs = tmp_path / "RUNS"
    env = {
        **os.environ,
        "CC_TOY_LAB_RUNS_ROOT": str(runs),
        "CC_TOY_LAB_FIXED_TIMESTAMP": "20990102-000042",
    }
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized.py", "--tiny", "--seed", "123"],
        cwd=root,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    rd = runs / "20990102-000042_s2_s1_product_discretized_tiny"
    assert rd.exists()
    assert "run_path=" in r.stdout
    assert "classification=" in r.stdout


def test_assess_payload_keys() -> None:
    cfg = build_product_discretized_config(tiny=True, seed=1)
    a = run_product_discretized_tiny(cfg)
    d = assess_product_discretized_results(a)
    assert "cases" in d and "classification" in d
    assert d["disorder_contrast_available"] is True
    assert d["profile_name"] == "tiny"
    assert isinstance(d["v3_failure_counts_by_bucket"], dict)
    assert "v2_vs_v3_disagreement_count" in d


def test_run_product_discretized_full_rejects_non_full_profile() -> None:
    with pytest.raises(ValueError, match="profile_name='full'"):
        run_product_discretized_full(build_product_discretized_config(medium=True))


def test_run_product_discretized_full_aborts_wrong_case_count(monkeypatch: pytest.MonkeyPatch) -> None:
    import cc_toy_lab.spectral.s2_s1_product_discretized as pd

    cfg = build_product_discretized_config(full=True)

    def bad_count(_c: ProductDiscretizedConfig) -> int:
        return 6614

    monkeypatch.setattr(pd, "estimate_product_discretized_case_count", bad_count)
    with pytest.raises(ValueError, match="6615"):
        pd.run_product_discretized_full(cfg)


def test_run_product_discretized_grid_progress_hook_tiny_profile() -> None:
    import cc_toy_lab.spectral.s2_s1_product_discretized as pd

    cfg = build_product_discretized_config(tiny=True, seed=7)
    calls: list[tuple[str, int]] = []

    def hook(phase: str, idx: int, _case: object) -> None:
        calls.append((phase, idx))

    pd._run_product_discretized_grid(cfg, after_each_case=hook)
    prim = [c for c in calls if c[0] == "primary"]
    repro = [c for c in calls if c[0] == "repro"]
    assert len(prim) == 72
    assert len(repro) == 72
    assert prim[0][1] == 0 and prim[-1][1] == 71
    assert repro[0][1] == 0 and repro[-1][1] == 71


def test_serialize_product_discretized_case_roundtrip_keys() -> None:
    cfg = build_product_discretized_config(tiny=True, seed=1)
    c = analyze_product_discretized_case(
        cfg=cfg, q=1, s1_family="ring", s1_size=8, alpha=0.0, disorder_strength=4.0, seed=123
    )
    d = serialize_product_discretized_case(c)
    assert d["q"] == 1
    assert d["s1_family"] == "ring"
    assert "localization_gate_v3_classification" in d


def test_cli_confirm_full_monkeypatched_runner(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib.util

    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("pd_cli", root / "scripts" / "s2_s1_product_discretized.py")
    cli = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(cli)
    import cc_toy_lab.spectral.s2_s1_product_discretized as pd

    sentinel: list[ProductDiscretizedConfig] = []

    def fake_full(cfg: ProductDiscretizedConfig, *, after_each_case: object = None) -> object:
        rd = tmp_path / "RUNS" / "20990103-121212_s2_s1_product_discretized_full"
        assert rd.is_dir(), "run_dir must exist before heavy work starts"
        assert (rd / "config.json").exists()
        rs_pre = json.loads((rd / "run_status.json").read_text(encoding="utf-8"))
        assert rs_pre["status"] == "running"
        assert rs_pre["expected_case_count"] == 6615
        assert "incomplete_artifacts_warning" in rs_pre
        sentinel.append(cfg)
        assert cfg.profile_name == "full"
        assert pd.estimate_product_discretized_case_count(cfg) == 6615
        tiny_a = pd.run_product_discretized_tiny(pd.build_product_discretized_config(tiny=True, seed=11))
        if after_each_case is not None:
            after_each_case("primary", 0, tiny_a.cases[0])
            after_each_case("repro", 0, tiny_a.cases[0])
        return dataclasses.replace(
            tiny_a,
            config=cfg,
            classification="product_discretized_full_diagnostic_complete",
        )

    monkeypatch.setattr(cli, "run_product_discretized_full", fake_full)
    monkeypatch.setenv("CC_TOY_LAB_RUNS_ROOT", str(tmp_path / "RUNS"))
    monkeypatch.setenv("CC_TOY_LAB_FIXED_TIMESTAMP", "20990103-121212")
    monkeypatch.setattr(sys, "argv", ["x", "--full", "--confirm-full-run"])
    rc = cli.main()
    assert rc == 0
    assert len(sentinel) == 1
    assert sentinel[0].profile_name == "full"
    rd = tmp_path / "RUNS" / "20990103-121212_s2_s1_product_discretized_full"
    assert rd.is_dir()
    assert (rd / "config.json").exists()
    assert (rd / "metrics.json").exists()
    assert (rd / "data.npz").exists()
    assert (rd / "summary.md").exists()
    assert (rd / "figures" / ".placeholder").exists()
    rs = json.loads((rd / "run_status.json").read_text(encoding="utf-8"))
    assert rs["status"] == "completed"
    assert rs["completed_cases"] == 6615
    assert rs["classification"] == "product_discretized_full_diagnostic_complete"
    prog = json.loads((rd / "progress.json").read_text(encoding="utf-8"))
    assert prog["expected_case_count"] == 6615
    assert prog["completed_primary_cases"] == 1
    assert prog["completed_repro_cases"] == 1
    assert "percent_complete" in prog and "current" in prog
    lines = (rd / "partial_results.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1


def test_cli_confirm_full_monkeypatched_runner_failed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib.util

    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("pd_cli_fail", root / "scripts" / "s2_s1_product_discretized.py")
    cli = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(cli)

    def boom(cfg: ProductDiscretizedConfig, *, after_each_case: object = None) -> object:
        rd = tmp_path / "RUNS" / "20990104-000001_s2_s1_product_discretized_full"
        assert rd.is_dir()
        assert json.loads((rd / "run_status.json").read_text(encoding="utf-8"))["status"] == "running"
        raise RuntimeError("simulated full failure")

    monkeypatch.setattr(cli, "run_product_discretized_full", boom)
    monkeypatch.setenv("CC_TOY_LAB_RUNS_ROOT", str(tmp_path / "RUNS"))
    monkeypatch.setenv("CC_TOY_LAB_FIXED_TIMESTAMP", "20990104-000001")
    monkeypatch.setattr(sys, "argv", ["x", "--full", "--confirm-full-run"])
    rc = cli.main()
    assert rc == 1
    rd = tmp_path / "RUNS" / "20990104-000001_s2_s1_product_discretized_full"
    rs = json.loads((rd / "run_status.json").read_text(encoding="utf-8"))
    assert rs["status"] == "failed"
    assert "simulated" in rs["error"]
    assert rs["completed_primary_cases"] == 0
    assert rs["completed_repro_cases"] == 0


def test_cli_confirm_requires_full() -> None:
    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized.py", "--tiny", "--confirm-full-run"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 2
    assert "requires --full" in r.stderr.lower()


def test_cli_full_dry_run_conflicts_confirm() -> None:
    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [
            sys.executable,
            "scripts/s2_s1_product_discretized.py",
            "--full",
            "--dry-run",
            "--confirm-full-run",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 2
    assert "cannot combine" in r.stderr.lower()


def test_cli_tiny_medium_mutually_exclusive() -> None:
    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized.py", "--tiny", "--medium"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode != 0
    r2 = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized.py", "--tiny", "--full", "--dry-run"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r2.returncode != 0


def test_cli_medium_dry_run() -> None:
    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized.py", "--medium", "--dry-run"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert "expected_case_count=1080" in r.stdout
    assert "grid_dimensions" in r.stdout
    assert "estimated_run_dir_suffix=_s2_s1_product_discretized_medium" in r.stdout
    assert "unchanged" in r.stdout.lower()


def test_cli_dry_run_requires_medium_or_full() -> None:
    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized.py", "--tiny", "--dry-run"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 2
    assert "medium or --full" in r.stderr or "medium or --full" in r.stdout


def test_cli_full_dry_run() -> None:
    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized.py", "--full", "--dry-run"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert "profile_name=full" in r.stdout
    assert "expected_case_count=6615" in r.stdout
    assert "estimated_run_dir_suffix=_s2_s1_product_discretized_full" in r.stdout
    assert "grid_dimensions" in r.stdout
    assert "warning: no operators were computed" in r.stdout.lower()
    assert "heavier than medium" in r.stdout.lower() or "much heavier" in r.stdout.lower()
    assert "unchanged" in r.stdout.lower()


def test_cli_full_without_dry_run_rejected() -> None:
    root = Path(__file__).resolve().parents[1]
    r = subprocess.run(
        [sys.executable, "scripts/s2_s1_product_discretized.py", "--full"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 2
    assert "confirm-full-run" in r.stderr.lower() or "--dry-run" in r.stderr.lower()
