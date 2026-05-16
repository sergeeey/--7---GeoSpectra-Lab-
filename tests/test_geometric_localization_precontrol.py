"""Tests for graph-Laplacian geometric localization pre-control and dumbbell tiny diagnostic."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

import pytest

from cc_toy_lab.geometry.geometric_localization_precontrol import (
    build_dumbbell_cylinder_points,
    build_straight_cylinder_points,
    build_variable_radius_cylinder_points,
    run_dumbbell_tiny_diagnostic,
    run_straight_cylinder_precontrol,
    run_variable_radius_cylinder_precontrol,
    save_dumbbell_tiny_diagnostic_artifacts,
    save_straight_cylinder_precontrol_artifacts,
    save_variable_radius_cylinder_precontrol_artifacts,
    tiny_dumbbell_config,
    tiny_straight_cylinder_config,
    tiny_variable_radius_cylinder_config,
)


def test_cylinder_point_cloud_shape() -> None:
    pts = build_straight_cylinder_points(1.0, 4.0, 12, 16, jitter=0.0, seed=0)
    assert pts.shape == (12 * 16, 3)
    r = np.sqrt(pts[:, 0] ** 2 + pts[:, 1] ** 2)
    assert np.allclose(r, 1.0, atol=1e-10)
    assert pts[:, 2].min() >= -2.0 - 1e-10 and pts[:, 2].max() <= 2.0 + 1e-10


def test_tiny_graph_connected_and_degree_stats() -> None:
    cfg = tiny_straight_cylinder_config()
    r = run_straight_cylinder_precontrol(cfg)
    assert r.connected_components == 1
    assert r.degree_min >= 1.0
    assert r.degree_max < r.n_points
    assert r.degree_mean > 0.0


def test_spectrum_metrics_present() -> None:
    cfg = tiny_straight_cylinder_config()
    r = run_straight_cylinder_precontrol(cfg)
    assert len(r.modes) >= 1
    m0 = r.modes[0]
    assert hasattr(m0, "eigenvalue")
    assert m0.ipr > 0.0
    assert -3.0 <= m0.z_center_of_mass <= 3.0
    assert abs(m0.z_mass_left + m0.z_mass_center + m0.z_mass_right - 1.0) < 1e-6


def test_artifacts_saved_and_summary_non_claims(tmp_path: Path) -> None:
    cfg = tiny_straight_cylinder_config()
    r = run_straight_cylinder_precontrol(cfg)
    paths = save_straight_cylinder_precontrol_artifacts(r, tmp_path / "run1")
    assert paths["config"].exists()
    assert paths["metrics"].exists()
    assert paths["data"].exists()
    assert paths["summary"].exists()
    assert (tmp_path / "run1" / "figures" / ".placeholder").exists()
    m = json.loads(paths["metrics"].read_text(encoding="utf-8"))
    for k in (
        "connected_components",
        "degree_min",
        "degree_max",
        "degree_mean",
        "degree_std",
        "low_modes",
        "null_verdict",
    ):
        assert k in m
    assert len(m["low_modes"]) >= 1
    row = m["low_modes"][0]
    for k in ("eigenvalue", "ipr", "z_center_of_mass", "z_mass_left", "z_mass_center", "z_mass_right"):
        assert k in row
    blob = np.load(paths["data"])
    assert "points" in blob and "z" in blob and "low_eigenvalues" in blob
    text = paths["summary"].read_text(encoding="utf-8")
    assert "Scientific non-claims" in text
    assert "Witten" in text or "Lichnerowicz" in text


def test_cli_smoke(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    runs = tmp_path / "RUNS"
    env = {
        **os.environ,
        "CC_TOY_LAB_RUNS_ROOT": str(runs),
        "CC_TOY_LAB_FIXED_TIMESTAMP": "20990103-000043",
    }
    r = subprocess.run(
        [
            sys.executable,
            "scripts/geometric_localization_precontrol.py",
            "--straight-cylinder",
            "--tiny",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    rd = runs / "20990103-000043_geometric_localization_precontrol_straight_cylinder_tiny"
    assert rd.exists()
    assert "null_verdict=" in r.stdout


def test_note_file_has_non_claims() -> None:
    root = Path(__file__).resolve().parents[1]
    note = root / "reports" / "GEOMETRIC_LOCALIZATION_STRAIGHT_CYLINDER_TINY_NOTE.md"
    assert note.exists()
    t = note.read_text(encoding="utf-8")
    assert "non-claims" in t.lower() or "Non-claims" in t
    assert "Standard Model" in t


def test_variable_radius_invalid_modulation_raises() -> None:
    with pytest.raises(ValueError, match="relative_radius_modulation"):
        build_variable_radius_cylinder_points(1.0, 4.0, 8, 8, 1.0, seed=0)


def test_variable_radius_radial_profile_nontrivial() -> None:
    pts = build_variable_radius_cylinder_points(1.0, 4.0, 24, 32, 0.22, jitter=0.0, seed=1)
    r = np.sqrt(pts[:, 0] ** 2 + pts[:, 1] ** 2)
    assert r.max() - r.min() > 0.05


def test_variable_radius_tiny_graph_and_verdict() -> None:
    cfg = tiny_variable_radius_cylinder_config()
    r = run_variable_radius_cylinder_precontrol(cfg)
    assert r.connected_components == 1
    assert r.gate_radius_profile_nontrivial
    assert r.control_verdict in (
        "variable_radius_cylinder_precontrol_pass",
        "graph_artifact_risk",
        "variable_radius_cylinder_precontrol_fail",
        "variable_radius_geometry_invalid",
    )


def test_variable_radius_artifacts_and_npz(tmp_path: Path) -> None:
    cfg = tiny_variable_radius_cylinder_config()
    r = run_variable_radius_cylinder_precontrol(cfg)
    paths = save_variable_radius_cylinder_precontrol_artifacts(r, tmp_path / "vr")
    m = json.loads(paths["metrics"].read_text(encoding="utf-8"))
    assert m["control_verdict"] == r.control_verdict
    assert "radial_extent_ratio" in m
    assert "gate_radius_profile_nontrivial" in m
    blob = np.load(paths["data"])
    assert "r_xy" in blob and "low_eigenvalues" in blob
    text = paths["summary"].read_text(encoding="utf-8")
    assert "Scientific non-claims" in text
    assert "Witten" in text or "Lichnerowicz" in text


def test_cli_variable_radius_smoke(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    runs = tmp_path / "RUNS"
    env = {
        **os.environ,
        "CC_TOY_LAB_RUNS_ROOT": str(runs),
        "CC_TOY_LAB_FIXED_TIMESTAMP": "20990103-000044",
    }
    r = subprocess.run(
        [
            sys.executable,
            "scripts/geometric_localization_precontrol.py",
            "--variable-radius-cylinder",
            "--tiny",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    rd = runs / "20990103-000044_geometric_localization_precontrol_variable_radius_cylinder_tiny"
    assert rd.exists()
    assert "control_verdict=" in r.stdout


def test_variable_radius_note_non_claims() -> None:
    root = Path(__file__).resolve().parents[1]
    note = root / "reports" / "GEOMETRIC_LOCALIZATION_VARIABLE_RADIUS_CYLINDER_TINY_NOTE.md"
    assert note.exists()
    t = note.read_text(encoding="utf-8")
    assert "non-claims" in t.lower() or "Non-claims" in t
    assert "Standard Model" in t


def test_dumbbell_point_cloud_shape() -> None:
    pts = build_dumbbell_cylinder_points(6.0, 0.4, 1.0, 16, 12, 0.8, jitter=0.0, seed=2)
    assert pts.shape == (16 * 12, 3)
    assert abs(pts[:, 2].max() - 3.0) < 1e-9 and abs(pts[:, 2].min() + 3.0) < 1e-9


def test_dumbbell_radius_profile_positive() -> None:
    pts = build_dumbbell_cylinder_points(6.0, 0.35, 1.0, 32, 32, 0.8, jitter=0.0, seed=0)
    r = np.hypot(pts[:, 0], pts[:, 1])
    assert np.all(r >= 0.349)
    assert np.all(r <= 1.001)


def test_dumbbell_tiny_runs_k8_and_k12() -> None:
    cfg = tiny_dumbbell_config()
    assert cfg.k_values == (8, 12)
    res = run_dumbbell_tiny_diagnostic(cfg)
    assert len(res.cases) == len(cfg.throat_radii) * len(cfg.k_values)
    ks = {c.k_neighbors for c in res.cases}
    assert ks == {8, 12}


def test_dumbbell_tiny_all_graph_connected() -> None:
    res = run_dumbbell_tiny_diagnostic(tiny_dumbbell_config())
    for c in res.cases:
        assert c.connected_components == 1
        assert c.gate_graph_connected


def test_dumbbell_mass_region_fields_in_metrics(tmp_path: Path) -> None:
    res = run_dumbbell_tiny_diagnostic(tiny_dumbbell_config())
    paths = save_dumbbell_tiny_diagnostic_artifacts(res, tmp_path / "db")
    m = json.loads(paths["metrics"].read_text(encoding="utf-8"))
    assert m["aggregate_verdict"] == res.aggregate_verdict
    assert "k_sensitivity_ok_by_throat" in m
    row0 = m["cases"][0]["low_modes"][0]
    for k in (
        "mass_left_bulb",
        "mass_throat",
        "mass_right_bulb",
        "throat_mass_fraction",
        "bulb_mass_fraction",
        "localization_region_label",
        "mode_symmetry_left_right",
    ):
        assert k in row0


def test_dumbbell_verdict_is_defined() -> None:
    res = run_dumbbell_tiny_diagnostic(tiny_dumbbell_config())
    assert res.aggregate_verdict in (
        "dumbbell_signal_candidate",
        "dumbbell_null_or_weak_signal",
        "graph_artifact_risk",
        "threshold_geometry_sensitivity",
        "sampling_artifact_risk",
    )


def test_dumbbell_artifacts_and_summary_non_claims(tmp_path: Path) -> None:
    res = run_dumbbell_tiny_diagnostic(tiny_dumbbell_config())
    paths = save_dumbbell_tiny_diagnostic_artifacts(res, tmp_path / "d2")
    assert paths["config"].exists()
    assert paths["metrics"].exists()
    assert paths["data"].exists()
    assert paths["summary"].exists()
    assert (tmp_path / "d2" / "figures" / ".placeholder").exists()
    blob = np.load(paths["data"])
    assert "points" in blob and "r_xy" in blob
    text = paths["summary"].read_text(encoding="utf-8")
    assert "Scientific non-claims" in text
    assert "20260514-120000" in text and "20260514-121500" in text


def test_cli_dumbbell_smoke(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    runs = tmp_path / "RUNS"
    env = {
        **os.environ,
        "CC_TOY_LAB_RUNS_ROOT": str(runs),
        "CC_TOY_LAB_FIXED_TIMESTAMP": "20990103-000045",
    }
    r = subprocess.run(
        [
            sys.executable,
            "scripts/geometric_localization_precontrol.py",
            "--dumbbell",
            "--tiny",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    rd = runs / "20990103-000045_geometric_localization_dumbbell_tiny"
    assert rd.exists()
    assert "aggregate_verdict=" in r.stdout


def test_dumbbell_tiny_note_sections() -> None:
    root = Path(__file__).resolve().parents[1]
    note = root / "reports" / "GEOMETRIC_LOCALIZATION_DUMBBELL_TINY_NOTE.md"
    assert note.exists()
    t = note.read_text(encoding="utf-8")
    assert "dumbbell tiny" in t.lower()
    assert "non-claims" in t.lower() or "scientific non" in t.lower()
    assert "Standard Model" in t
