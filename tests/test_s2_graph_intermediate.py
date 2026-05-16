import os
import subprocess
import sys
from pathlib import Path

from cc_toy_lab.spectral.s2_graph_intermediate import (
    S2GraphProductConfig,
    analyze_s2_graph_product,
    run_s2_graph_product_benchmark,
)


def test_s2_graph_product_index_tracks_q_times_graph_size():
    result = analyze_s2_graph_product(q=1, cutoff=2, graph_size=6, disorder=0.0, perturbation=0.0, seed=5)

    assert result.expected_index == 6
    assert result.numerical_index == 6
    assert result.n_plus == 6
    assert result.n_minus == 0
    assert result.index_passed


def test_s2_graph_product_index_sign_flip():
    positive = analyze_s2_graph_product(q=1, cutoff=2, graph_size=5, disorder=1.0, perturbation=1e-5, seed=7)
    negative = analyze_s2_graph_product(q=-1, cutoff=2, graph_size=5, disorder=1.0, perturbation=1e-5, seed=7)

    assert positive.numerical_index == 5
    assert negative.numerical_index == -5
    assert positive.numerical_index == -negative.numerical_index


def test_s2_graph_product_perturbation_preserves_index_and_saves(tmp_path: Path):
    config = S2GraphProductConfig(
        q_values=(1,),
        graph_sizes=(6,),
        disorder_values=(0.0, 8.0),
        perturbation_values=(0.0, 1e-4),
        realizations=2,
        seed=17,
    )

    result = run_s2_graph_product_benchmark(config=config, output_dir=tmp_path)

    assert result.all_index_checks_passed
    assert result.all_anticommutators_preserved
    assert result.ipr_growth_observed
    assert (tmp_path / "config.json").exists()
    assert (tmp_path / "metrics.json").exists()
    assert (tmp_path / "data.npz").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "figures" / "index_vs_disorder.png").exists()
    assert (tmp_path / "figures" / "zero_mode_ipr_vs_disorder.png").exists()
    assert (tmp_path / "figures" / "perturbation_stability.png").exists()
    assert (tmp_path / "figures" / "chirality_counts.png").exists()


def test_s2_graph_intermediate_cli_quick_smoke():
    env = dict(os.environ, CC_TOY_LAB_SKIP_REPORT_UPDATE="1")
    result = subprocess.run(
        [sys.executable, "scripts/s2_graph_intermediate.py", "--quick"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0
    assert "s2_graph_intermediate_quick complete" in result.stdout
