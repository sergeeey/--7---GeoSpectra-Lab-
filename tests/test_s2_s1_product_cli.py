import os
import subprocess
import sys
from pathlib import Path


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


def test_s2_s1_product_cli_quick_smoke_creates_run_and_artifacts(tmp_path: Path):
    runs_root = tmp_path / "RUNS"
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(runs_root),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000000",
        CC_TOY_LAB_S2_S1_CLI_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [sys.executable, "scripts/s2_s1_product.py", "--quick"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    run_dir = runs_root / "20990101-000000_s2_s1_product_quick"
    assert result.returncode == 0, result.stderr
    assert run_dir.exists()
    assert (run_dir / "config.json").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "data.npz").exists()
    assert (run_dir / "summary.md").exists()
    assert (run_dir / "figures").exists()
    assert "run_path=" in result.stdout
    assert "classification=" in result.stdout
    assert "all_basic_gates_passed=" in result.stdout
    assert "total_observations=" in result.stdout
    assert "s2_s1_product_quick complete" in result.stdout


def test_s2_s1_product_cli_does_not_update_project_docs(tmp_path: Path):
    before = _doc_snapshot()
    env = dict(
        os.environ,
        CC_TOY_LAB_RUNS_ROOT=str(tmp_path / "RUNS"),
        CC_TOY_LAB_FIXED_TIMESTAMP="20990101-000001",
        CC_TOY_LAB_S2_S1_CLI_TEST_PROFILE="tiny",
    )

    result = subprocess.run(
        [sys.executable, "scripts/s2_s1_product.py", "--quick"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert _doc_snapshot() == before
