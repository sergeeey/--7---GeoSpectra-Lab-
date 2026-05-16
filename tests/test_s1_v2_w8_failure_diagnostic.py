import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_w8_diagnostic_cli_tiny_smoke(tmp_path: Path):
    runs_root = tmp_path / "RUNS"
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(runs_root),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000020",
    )
    result = subprocess.run(
        [sys.executable, "scripts/s1_v2_w8_failure_diagnostic.py", "--tiny"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    run_dir = runs_root / "20990101-000020_s1_v2_w8_failure_diagnostic"
    assert result.returncode == 0, result.stderr
    assert run_dir.exists()
    assert (run_dir / "config.json").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "data.npz").exists()
    assert (run_dir / "summary.md").exists()
    assert (run_dir / "figures").exists()
    assert "run_path=" in result.stdout
    assert "diagnostic_classification=" in result.stdout
    assert "s1_v2_w8_failure_diagnostic complete" in result.stdout

    metrics = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))
    assert "classification" in metrics
    assert "anchor" in metrics
    assert "grid_rows" in metrics
    assert metrics["counts"]["primary_rows"] >= 1
