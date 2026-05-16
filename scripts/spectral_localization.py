from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import ensure_report_tree, make_run_dir, write_json, write_summary
from cc_toy_lab.spectral.anderson import build_anderson_hamiltonian, run_anderson_sweep
from cc_toy_lab.spectral.metrics import inverse_participation_ratio, mean_adjacent_gap_ratio


def _sample_eigenvectors(size: int, disorder: float, seed: int) -> tuple[np.ndarray, np.ndarray]:
    hamiltonian = build_anderson_hamiltonian(size=size, disorder=disorder, seed=seed)
    values, vectors = np.linalg.eigh(hamiltonian.toarray())
    center = size // 2
    slc = slice(max(0, center - 32), min(size, center + 32))
    return values[slc], vectors[:, slc]


def run(args: argparse.Namespace) -> dict[str, str | float]:
    ensure_report_tree()
    if args.quick:
        sizes = [96, 160]
        disorder_values = np.linspace(0.5, 30.0, 8)
        realizations = 4
    else:
        sizes = [args.size]
        disorder_values = np.linspace(0.5, 30.0, args.disorder_count)
        realizations = args.realizations

    sweep = run_anderson_sweep(
        sizes=sizes,
        disorder_values=disorder_values,
        realizations=realizations,
        seed=args.seed,
        window_fraction=0.5,
    )
    primary_size = sizes[0]
    points = sweep.by_size[primary_size]
    w = np.array([point.disorder for point in points])
    r = np.array([point.mean_r for point in points])
    ipr = np.array([point.mean_ipr for point in points])

    low_values, low_vectors = _sample_eigenvectors(primary_size, float(w[0]), args.seed)
    high_values, high_vectors = _sample_eigenvectors(primary_size, float(w[-1]), args.seed + 1)
    low_r_values = []
    high_r_values = []
    for levels in [low_values, high_values]:
        spacings = np.diff(np.sort(levels))
        rv = np.minimum(spacings[:-1], spacings[1:]) / np.maximum(spacings[:-1], spacings[1:])
        if levels is low_values:
            low_r_values = rv
        else:
            high_r_values = rv

    fig, axes = plt.subplots(3, 2, figsize=(14, 13), constrained_layout=True)
    fig.suptitle("Spectral localization toy benchmark")
    axes[0, 0].plot(w, r, marker="o")
    axes[0, 0].axhline(0.5307, color="gray", linestyle="--", label="GOE")
    axes[0, 0].axhline(0.3863, color="gray", linestyle=":", label="Poisson")
    axes[0, 0].set_xscale("log")
    axes[0, 0].set_title("<r>(W)")
    axes[0, 0].set_xlabel("W")
    axes[0, 0].set_ylabel("<r>")
    axes[0, 0].legend()

    axes[0, 1].plot(w, ipr, marker="s", color="tab:red")
    axes[0, 1].set_xscale("log")
    axes[0, 1].set_yscale("log")
    axes[0, 1].set_title("Mean IPR(W)")
    axes[0, 1].set_xlabel("W")
    axes[0, 1].set_ylabel("IPR")

    axes[1, 0].hist(low_r_values, bins=18, color="tab:blue", alpha=0.8)
    axes[1, 0].set_title("r histogram, weak disorder")
    axes[1, 1].hist(high_r_values, bins=18, color="tab:orange", alpha=0.8)
    axes[1, 1].set_title("r histogram, strong disorder")

    axes[2, 0].plot(np.abs(low_vectors[:, low_vectors.shape[1] // 2]) ** 2, label="weak W")
    axes[2, 0].plot(np.abs(high_vectors[:, high_vectors.shape[1] // 2]) ** 2, label="strong W")
    axes[2, 0].set_title("Example eigenvector amplitudes")
    axes[2, 0].set_xlabel("site")
    axes[2, 0].set_ylabel("|psi|^2")
    axes[2, 0].legend()

    size_values = []
    high_ipr = []
    for size, size_points in sweep.by_size.items():
        size_values.append(size)
        high_ipr.append(size_points[-1].mean_ipr)
    axes[2, 1].plot(size_values, high_ipr, marker="d")
    axes[2, 1].set_title("Finite-size smoke: strong-W IPR")
    axes[2, 1].set_xlabel("N")
    axes[2, 1].set_ylabel("IPR")

    run_dir = make_run_dir("spectral_localization")
    figure_path = Path("reports") / "FIGURES" / "spectral_localization_dashboard.png"
    fig.savefig(figure_path, dpi=160)
    fig.savefig(run_dir / "figures" / "spectral_localization_dashboard.png", dpi=160)
    plt.close(fig)

    metrics = {
        "primary_size": primary_size,
        "realizations": realizations,
        "weak_disorder_r": float(r[0]),
        "strong_disorder_r": float(r[-1]),
        "weak_disorder_ipr": float(ipr[0]),
        "strong_disorder_ipr": float(ipr[-1]),
        "figure": str(figure_path),
        "note": "This is a localization benchmark only; it does not prove chirality or a Dirac index.",
    }
    goe_distance = abs(float(r[0]) - 0.5307)
    poisson_distance = abs(float(r[0]) - 0.3863)
    if goe_distance >= poisson_distance:
        null_path = Path("reports") / "NULL_RESULTS.md"
        with null_path.open("a", encoding="utf-8") as handle:
            handle.write(
                "\n## Spectral weak-disorder GOE check\n\n"
                f"At W={w[0]:.4g}, <r>={r[0]:.4f}, which is not closer to GOE than to Poisson. "
                "This is logged as a toy-model limitation, not hidden as success. "
                f"Run directory: {run_dir}\n"
            )
    write_json(run_dir / "config.json", {"sizes": sizes, "disorder_values": disorder_values, "seed": args.seed})
    write_json(run_dir / "metrics.json", metrics)
    np.savez(run_dir / "data.npz", disorder=w, mean_r=r, mean_ipr=ipr)
    lines = [
        "What was checked: 1D Anderson toy localization with adjacent-gap ratios and IPR.",
        f"Weak disorder: r={r[0]:.4f}, IPR={ipr[0]:.4g}.",
        f"Strong disorder: r={r[-1]:.4f}, IPR={ipr[-1]:.4g}.",
        "Interpretation limit: GOE/Poisson and IPR are localization diagnostics, not chirality diagnostics.",
        f"Run directory: {run_dir}",
    ]
    write_summary(Path("reports") / "SPECTRAL_REPORT.md", "Spectral Report", lines)
    write_summary(run_dir / "summary.md", "Spectral Localization Run", lines)
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=512)
    parser.add_argument("--disorder-count", type=int, default=30)
    parser.add_argument("--realizations", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--quick", action="store_true", help="Run a small smoke benchmark.")
    return parser.parse_args()


if __name__ == "__main__":
    metrics = run(parse_args())
    print("Spectral localization complete")
    print(f"figure={metrics['figure']}")
    print(f"weak_r={metrics['weak_disorder_r']:.4f} strong_r={metrics['strong_disorder_r']:.4f}")
