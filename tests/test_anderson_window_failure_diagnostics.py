import subprocess
import sys


def test_quantile05_failure_diagnostic_cli_smoke():
    result = subprocess.run(
        [
            sys.executable,
            "scripts/anderson_3d_window_failure_diagnostics.py",
            "--smoke",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "anderson_quantile05_diagnostics" in result.stdout
    assert "classification=" in result.stdout
