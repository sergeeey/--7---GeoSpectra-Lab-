import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from scripts.anderson_3d_periodic_followup import PeriodicFollowupConfig, run_periodic_followup


def test_periodic_followup_saves_core_artifacts(tmp_path: Path):
    config = PeriodicFollowupConfig(
        lattice_sizes=(4,),
        disorder_values=(16.0, 24.0, 32.0),
        windows=("center", "quantile_0.5"),
        realizations=2,
        seed=23,
        include_open_reference=True,
        open_reference_lattice_size=4,
    )

    result = run_periodic_followup(config=config, output_dir=tmp_path)

    assert result.points
    assert result.classification
    assert all(np.isfinite(point.mean_r) for point in result.points)
    assert all(np.isfinite(point.mean_ipr) for point in result.points)
    assert (tmp_path / "config.json").exists()
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "data.npz").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "figures" / "periodic_r_vs_w.png").exists()
    assert (tmp_path / "figures" / "periodic_ipr_vs_w.png").exists()
    assert (tmp_path / "figures" / "periodic_distance_to_poisson_goe.png").exists()
    assert (tmp_path / "figures" / "periodic_open_comparison_optional.png").exists()


def test_periodic_followup_cli_smoke():
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/anderson_3d_periodic_followup.py", "--smoke"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert "anderson_periodic_followup complete" in result.stdout
