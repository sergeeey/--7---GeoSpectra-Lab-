from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import make_run_dir, write_json, write_summary
from cc_toy_lab.spectral.anderson_3d import GOE_R, POISSON_R, build_anderson_3d_hamiltonian
from cc_toy_lab.spectral.anderson_windows import choose_window_indices
from cc_toy_lab.spectral.metrics import inverse_participation_ratio, level_spacings


@dataclass(frozen=True)
class Quantile05DiagnosticConfig:
    lattice_sizes: tuple[int, ...] = (6, 7, 8)
    disorder_values: tuple[float, ...] = (20.0, 24.0, 28.0, 32.0, 36.0)
    windows: tuple[str, ...] = ("center", "quantile_0.5")
    realizations: int = 10
    seed: int = 4242
    hopping: float = 1.0
    periodic: bool = False
    window_fraction: float = 0.2
    quantile_fraction: float = 0.1
    min_levels: int = 8
    histogram_disorders: tuple[float, ...] = (24.0, 32.0)
    note: str = "Targeted diagnostic for quantile_0.5 full spectrum-window failure"


@dataclass(frozen=True)
class DiagnosticPoint:
    lattice_size: int
    sites: int
    disorder: float
    window_name: str
    mean_r: float
    stderr_r: float
    mean_ipr: float
    stderr_ipr: float
    n_levels_used: int
    realizations: int
    distance_to_goe: float
    distance_to_poisson: float
    closer_to_poisson: bool


def adjacent_gap_ratios(levels: np.ndarray) -> np.ndarray:
    spacings = level_spacings(levels)
    if spacings.size < 2:
        return np.asarray([], dtype=float)
    lower = np.minimum(spacings[:-1], spacings[1:])
    upper = np.maximum(spacings[:-1], spacings[1:])
    return lower / upper


def run_diagnostics(config: Quantile05DiagnosticConfig, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    observations: list[dict] = []
    histogram_rows: list[dict] = []
    for lattice_size in config.lattice_sizes:
        for w_index, disorder in enumerate(config.disorder_values):
            for realization in range(config.realizations):
                run_seed = config.seed + 1_000_000 * lattice_size + 10_000 * w_index + realization
                hamiltonian = build_anderson_3d_hamiltonian(
                    lattice_size=lattice_size,
                    disorder=disorder,
                    hopping=config.hopping,
                    seed=run_seed,
                    periodic=config.periodic,
                )
                eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian.toarray())
                for window_name in config.windows:
                    indices = choose_window_indices(
                        eigenvalues,
                        window_name,
                        fraction=config.window_fraction,
                        quantile_fraction=config.quantile_fraction,
                        min_levels=config.min_levels,
                    )
                    selected_values = eigenvalues[indices]
                    selected_vectors = eigenvectors[:, indices]
                    ratios = adjacent_gap_ratios(selected_values)
                    ipr_values = inverse_participation_ratio(selected_vectors)
                    observations.append(
                        {
                            "lattice_size": lattice_size,
                            "sites": lattice_size**3,
                            "disorder": disorder,
                            "window_name": window_name,
                            "realization": realization,
                            "seed": run_seed,
                            "mean_r": float(np.mean(ratios)),
                            "mean_ipr": float(np.mean(ipr_values)),
                            "n_levels_used": int(indices.size),
                        }
                    )
                    if any(np.isclose(disorder, target) for target in config.histogram_disorders):
                        for ratio in ratios:
                            histogram_rows.append(
                                {
                                    "lattice_size": lattice_size,
                                    "disorder": disorder,
                                    "window_name": window_name,
                                    "ratio": float(ratio),
                                }
                            )

    points = _aggregate_points(observations)
    classification = _classify(points, config)
    payload = {
        "config": asdict(config),
        "points": [asdict(point) for point in points],
        "observations": observations,
        "histogram_rows": histogram_rows,
        "classification": classification,
        "pass_fail_criterion": (
            "A window passes the earlier basic check when weak disorder is closer to GOE, "
            "strong disorder is closer to Poisson than weak and closer to Poisson than GOE, "
            "and IPR increases."
        ),
    }

    write_json(output_dir / "config.json", asdict(config))
    write_json(output_dir / "metrics.json", payload)
    _save_npz(output_dir / "data.npz", points, observations, histogram_rows)
    _plot_r_vs_w(points, config, figures_dir / "r_vs_w_quantile05.png")
    _plot_ipr_vs_w(points, config, figures_dir / "ipr_vs_w_quantile05.png")
    _plot_r_histograms(histogram_rows, config, figures_dir / "r_histograms_w24_w32.png")
    write_summary(output_dir / "summary.md", "Anderson quantile_0.5 failure diagnostics", _summary_lines(points, classification, output_dir))
    return payload


def _aggregate_points(observations: list[dict]) -> list[DiagnosticPoint]:
    keys = sorted({(row["lattice_size"], row["disorder"], row["window_name"]) for row in observations})
    points: list[DiagnosticPoint] = []
    for lattice_size, disorder, window_name in keys:
        rows = [
            row
            for row in observations
            if row["lattice_size"] == lattice_size
            and np.isclose(row["disorder"], disorder)
            and row["window_name"] == window_name
        ]
        r_values = np.asarray([row["mean_r"] for row in rows], dtype=float)
        ipr_values = np.asarray([row["mean_ipr"] for row in rows], dtype=float)
        levels = np.asarray([row["n_levels_used"] for row in rows], dtype=float)
        mean_r = float(np.mean(r_values))
        points.append(
            DiagnosticPoint(
                lattice_size=int(lattice_size),
                sites=int(lattice_size**3),
                disorder=float(disorder),
                window_name=str(window_name),
                mean_r=mean_r,
                stderr_r=float(np.std(r_values, ddof=1) / np.sqrt(r_values.size)) if r_values.size > 1 else 0.0,
                mean_ipr=float(np.mean(ipr_values)),
                stderr_ipr=float(np.std(ipr_values, ddof=1) / np.sqrt(ipr_values.size)) if ipr_values.size > 1 else 0.0,
                n_levels_used=int(round(float(np.mean(levels)))),
                realizations=len(rows),
                distance_to_goe=float(abs(mean_r - GOE_R)),
                distance_to_poisson=float(abs(mean_r - POISSON_R)),
                closer_to_poisson=bool(abs(mean_r - POISSON_R) < abs(mean_r - GOE_R)),
            )
        )
    return points


def _classify(points: list[DiagnosticPoint], config: Quantile05DiagnosticConfig) -> str:
    largest = max(point.lattice_size for point in points)
    q_points = [
        point
        for point in points
        if point.lattice_size == largest and point.window_name == "quantile_0.5"
    ]
    center_points = [
        point
        for point in points
        if point.lattice_size == largest and point.window_name == "center"
    ]
    q_by_w = {point.disorder: point for point in q_points}
    center_by_w = {point.disorder: point for point in center_points}
    strong = q_by_w.get(max(config.disorder_values))
    w24 = q_by_w.get(24.0)
    weak = q_by_w.get(min(config.disorder_values))
    if strong is None or weak is None:
        return "unresolved: missing weak or strong reference point"
    ipr_increases = strong.mean_ipr > weak.mean_ipr
    r_moves_down = strong.mean_r < weak.mean_r
    strong_poisson = strong.closer_to_poisson
    center_strong = center_by_w.get(max(config.disorder_values))
    center_poisson = center_strong.closer_to_poisson if center_strong else False
    if w24 is not None and w24.closer_to_poisson and ipr_increases:
        return (
            "likely statistical/finite-size/seed-count effect: quantile_0.5 at W=24 "
            "becomes Poisson-like in the targeted rerun"
        )
    if ipr_increases and r_moves_down and not strong_poisson and center_poisson:
        return "likely window-selection or finite-size effect: quantile_0.5 trends toward localization but lags center r-statistics"
    if ipr_increases and r_moves_down and not strong_poisson:
        return "unresolved finite-size/statistical effect: IPR and r trend improve, but strong r is not Poisson-like"
    if not ipr_increases:
        return "possible true mixed/delocalized behavior: IPR does not increase"
    return "likely resolved at stronger disorder: quantile_0.5 becomes Poisson-like"


def _save_npz(path: Path, points: list[DiagnosticPoint], observations: list[dict], histogram_rows: list[dict]) -> None:
    np.savez(
        path,
        point_lattice_size=np.asarray([point.lattice_size for point in points], dtype=int),
        point_disorder=np.asarray([point.disorder for point in points], dtype=float),
        point_window=np.asarray([point.window_name for point in points]),
        point_mean_r=np.asarray([point.mean_r for point in points], dtype=float),
        point_stderr_r=np.asarray([point.stderr_r for point in points], dtype=float),
        point_mean_ipr=np.asarray([point.mean_ipr for point in points], dtype=float),
        point_stderr_ipr=np.asarray([point.stderr_ipr for point in points], dtype=float),
        obs_lattice_size=np.asarray([row["lattice_size"] for row in observations], dtype=int),
        obs_disorder=np.asarray([row["disorder"] for row in observations], dtype=float),
        obs_window=np.asarray([row["window_name"] for row in observations]),
        obs_mean_r=np.asarray([row["mean_r"] for row in observations], dtype=float),
        obs_mean_ipr=np.asarray([row["mean_ipr"] for row in observations], dtype=float),
        hist_lattice_size=np.asarray([row["lattice_size"] for row in histogram_rows], dtype=int),
        hist_disorder=np.asarray([row["disorder"] for row in histogram_rows], dtype=float),
        hist_window=np.asarray([row["window_name"] for row in histogram_rows]),
        hist_ratio=np.asarray([row["ratio"] for row in histogram_rows], dtype=float),
    )


def _plot_r_vs_w(points: list[DiagnosticPoint], config: Quantile05DiagnosticConfig, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for lattice_size in config.lattice_sizes:
        for window_name, marker in (("center", "o"), ("quantile_0.5", "s")):
            rows = _rows(points, lattice_size, window_name)
            if not rows:
                continue
            ax.errorbar(
                [row.disorder for row in rows],
                [row.mean_r for row in rows],
                yerr=[row.stderr_r for row in rows],
                marker=marker,
                capsize=3,
                label=f"L={lattice_size} {window_name}",
            )
    ax.axhline(GOE_R, color="black", linestyle="--", linewidth=1.0, label="GOE")
    ax.axhline(POISSON_R, color="black", linestyle=":", linewidth=1.0, label="Poisson")
    ax.set_xlabel("disorder W")
    ax.set_ylabel("mean adjacent-gap ratio <r>")
    ax.set_title("Targeted quantile_0.5 diagnostics: r vs W")
    ax.legend(fontsize="x-small", ncols=2)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _plot_ipr_vs_w(points: list[DiagnosticPoint], config: Quantile05DiagnosticConfig, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for lattice_size in config.lattice_sizes:
        for window_name, marker in (("center", "o"), ("quantile_0.5", "s")):
            rows = _rows(points, lattice_size, window_name)
            if not rows:
                continue
            ax.errorbar(
                [row.disorder for row in rows],
                [row.mean_ipr for row in rows],
                yerr=[row.stderr_ipr for row in rows],
                marker=marker,
                capsize=3,
                label=f"L={lattice_size} {window_name}",
            )
    ax.set_xlabel("disorder W")
    ax.set_ylabel("mean IPR")
    ax.set_yscale("log")
    ax.set_title("Targeted quantile_0.5 diagnostics: IPR vs W")
    ax.legend(fontsize="x-small", ncols=2)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _plot_r_histograms(histogram_rows: list[dict], config: Quantile05DiagnosticConfig, path: Path) -> None:
    fig, axes = plt.subplots(1, len(config.histogram_disorders), figsize=(10, 4), constrained_layout=True)
    if len(config.histogram_disorders) == 1:
        axes = [axes]
    largest = max(config.lattice_sizes)
    for ax, disorder in zip(axes, config.histogram_disorders):
        for window_name, alpha in (("center", 0.55), ("quantile_0.5", 0.55)):
            ratios = [
                row["ratio"]
                for row in histogram_rows
                if row["lattice_size"] == largest
                and np.isclose(row["disorder"], disorder)
                and row["window_name"] == window_name
            ]
            ax.hist(ratios, bins=np.linspace(0, 1, 21), alpha=alpha, label=window_name)
        ax.set_title(f"L={largest}, W={disorder:g}")
        ax.set_xlabel("adjacent gap ratio r")
        ax.set_ylabel("count")
        ax.legend(fontsize="small")
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _rows(points: list[DiagnosticPoint], lattice_size: int, window_name: str) -> list[DiagnosticPoint]:
    return sorted(
        [
            point
            for point in points
            if point.lattice_size == lattice_size and point.window_name == window_name
        ],
        key=lambda point: point.disorder,
    )


def _points_table(points: list[DiagnosticPoint]) -> str:
    lines = [
        "| L | W | window | <r> | stderr_r | IPR | stderr_ipr | closer to Poisson |",
        "| ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for point in sorted(points, key=lambda row: (row.lattice_size, row.disorder, row.window_name)):
        lines.append(
            f"| {point.lattice_size} | {point.disorder:.4g} | {point.window_name} | "
            f"{point.mean_r:.4f} | {point.stderr_r:.4f} | {point.mean_ipr:.6g} | "
            f"{point.stderr_ipr:.2g} | {point.closer_to_poisson} |"
        )
    return "\n".join(lines)


def _summary_lines(points: list[DiagnosticPoint], classification: str, output_dir: Path) -> list[str]:
    largest = max(point.lattice_size for point in points)
    final_points = [point for point in points if point.lattice_size == largest]
    return [
        "Targeted diagnostic for the quantile_0.5 full spectrum-window failure.",
        "Pass/fail criterion inspected: weak GOE-like, strong Poisson-like, and IPR growth.",
        "",
        f"Classification: {classification}",
        "",
        "## Final Lattice Summary",
        "",
        _points_table(final_points),
        "",
        "Interpretation: this is benchmark diagnosis only, not proof of target physical localization.",
        "Non-claims: no chirality, no covariant compactification proof, no Standard Model derivation.",
        f"Run directory: {output_dir}",
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose quantile_0.5 Anderson spectrum-window failure.")
    parser.add_argument("--smoke", action="store_true", help="Tiny fast run for tests.")
    parser.add_argument("--periodic", action="store_true", help="Use periodic boundary conditions.")
    parser.add_argument("--seed", type=int, default=4242)
    parser.add_argument("--realizations", type=int, default=None)
    return parser.parse_args()


def config_from_args(args: argparse.Namespace) -> Quantile05DiagnosticConfig:
    if args.smoke:
        return Quantile05DiagnosticConfig(
            lattice_sizes=(4,),
            disorder_values=(24.0, 32.0),
            realizations=2,
            seed=args.seed,
            periodic=args.periodic,
            min_levels=8,
        )
    return Quantile05DiagnosticConfig(
        realizations=args.realizations if args.realizations is not None else 10,
        seed=args.seed,
        periodic=args.periodic,
    )


def main() -> None:
    args = parse_args()
    config = config_from_args(args)
    run_dir = make_run_dir("anderson_quantile05_diagnostics")
    payload = run_diagnostics(config, run_dir)
    print(f"classification={payload['classification']}")
    print(f"anderson_quantile05_diagnostics complete: {run_dir}")


if __name__ == "__main__":
    main()
