from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import write_json, write_summary
from cc_toy_lab.spectral.metrics import mean_adjacent_gap_ratio


EXPECTED_R = {
    "poisson": 0.3863,
    "goe": 0.5307,
    "gue": 0.5996,
}

DEFAULT_TOLERANCES = {
    "poisson": 0.035,
    "goe": 0.04,
    "gue": 0.045,
}


@dataclass(frozen=True)
class ControlConfig:
    matrix_size: int = 240
    realizations: int = 24
    seed: int = 42
    include_gue: bool = True
    bulk_fraction: float = 0.5
    tolerance_scale: float = 1.0


@dataclass(frozen=True)
class EnsembleControlResult:
    ensemble: str
    expected_r: float
    mean_r: float
    std_r: float
    stderr_r: float
    tolerance: float
    passed: bool
    samples: int


def generate_poisson_levels(size: int, rng_seed: int | None = None, rng: np.random.Generator | None = None) -> np.ndarray:
    """Generate uncorrelated levels from cumulative exponential spacings."""
    if size < 4:
        raise ValueError("size must be >= 4")
    local_rng = np.random.default_rng(rng_seed) if rng is None else rng
    spacings = local_rng.exponential(scale=1.0, size=size)
    return np.cumsum(spacings)


def generate_goe_levels(size: int, rng_seed: int | None = None, rng: np.random.Generator | None = None) -> np.ndarray:
    """Generate eigenlevels of a real symmetric Gaussian matrix."""
    if size < 4:
        raise ValueError("size must be >= 4")
    local_rng = np.random.default_rng(rng_seed) if rng is None else rng
    matrix = local_rng.normal(size=(size, size))
    matrix = (matrix + matrix.T) / np.sqrt(2.0 * size)
    return np.linalg.eigvalsh(matrix)


def generate_gue_levels(size: int, rng_seed: int | None = None, rng: np.random.Generator | None = None) -> np.ndarray:
    """Generate eigenlevels of a complex Hermitian Gaussian matrix."""
    if size < 4:
        raise ValueError("size must be >= 4")
    local_rng = np.random.default_rng(rng_seed) if rng is None else rng
    real = local_rng.normal(size=(size, size))
    imag = local_rng.normal(size=(size, size))
    matrix = real + 1j * imag
    matrix = (matrix + matrix.conj().T) / np.sqrt(4.0 * size)
    return np.linalg.eigvalsh(matrix)


def _bulk(levels: np.ndarray, fraction: float) -> np.ndarray:
    if not (0 < fraction <= 1.0):
        raise ValueError("bulk_fraction must be in (0, 1]")
    levels = np.sort(np.asarray(levels, dtype=float))
    if fraction == 1.0:
        return levels
    trim = int((1.0 - fraction) * len(levels) / 2.0)
    return levels[trim : len(levels) - trim]


def _evaluate_one(
    ensemble: str,
    generator: Callable[[int, None, np.random.Generator], np.ndarray],
    config: ControlConfig,
    rng: np.random.Generator,
) -> tuple[EnsembleControlResult, np.ndarray]:
    values: list[float] = []
    for _ in range(config.realizations):
        levels = generator(config.matrix_size, None, rng)
        values.append(mean_adjacent_gap_ratio(_bulk(levels, config.bulk_fraction)))
    samples = np.asarray(values, dtype=float)
    expected = EXPECTED_R[ensemble]
    tolerance = DEFAULT_TOLERANCES[ensemble] * config.tolerance_scale
    mean_r = float(np.mean(samples))
    std_r = float(np.std(samples, ddof=1)) if len(samples) > 1 else 0.0
    stderr = float(std_r / np.sqrt(max(len(samples), 1)))
    result = EnsembleControlResult(
        ensemble=ensemble,
        expected_r=expected,
        mean_r=mean_r,
        std_r=std_r,
        stderr_r=stderr,
        tolerance=tolerance,
        passed=abs(mean_r - expected) <= tolerance,
        samples=len(samples),
    )
    return result, samples


def evaluate_controls(
    config: ControlConfig,
    output_dir: Path | None = None,
) -> dict[str, EnsembleControlResult]:
    """Evaluate synthetic r-statistics controls and optionally save artifacts."""
    rng = np.random.default_rng(config.seed)
    generators: dict[str, Callable[[int, None, np.random.Generator], np.ndarray]] = {
        "poisson": generate_poisson_levels,
        "goe": generate_goe_levels,
    }
    if config.include_gue:
        generators["gue"] = generate_gue_levels

    results: dict[str, EnsembleControlResult] = {}
    raw_samples: dict[str, np.ndarray] = {}
    for ensemble, generator in generators.items():
        result, samples = _evaluate_one(ensemble, generator, config, rng)
        results[ensemble] = result
        raw_samples[ensemble] = samples

    if output_dir is not None:
        save_control_artifacts(config=config, results=results, raw_samples=raw_samples, output_dir=output_dir)

    return results


def save_control_artifacts(
    config: ControlConfig,
    results: dict[str, EnsembleControlResult],
    raw_samples: dict[str, np.ndarray],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "config.json", asdict(config))
    write_json(output_dir / "metrics.json", {name: asdict(result) for name, result in results.items()})
    np.savez(output_dir / "data.npz", **raw_samples)

    fig, axes = plt.subplots(1, len(results), figsize=(5 * len(results), 4), constrained_layout=True)
    if len(results) == 1:
        axes = [axes]
    for ax, (ensemble, samples) in zip(axes, raw_samples.items()):
        result = results[ensemble]
        ax.hist(samples, bins=min(12, max(4, len(samples) // 2)), alpha=0.8, color="tab:blue")
        ax.axvline(result.expected_r, color="black", linestyle="--", label="expected")
        ax.axvline(result.mean_r, color="tab:red", linestyle="-", label="measured")
        ax.set_title(f"{ensemble.upper()} r-stat controls")
        ax.set_xlabel("<r> per realization")
        ax.set_ylabel("count")
        ax.legend(fontsize=8)
    fig.savefig(figures_dir / "r_stat_control_histograms.png", dpi=160)
    plt.close(fig)

    lines = ["Synthetic r-statistics controls validate the statistic pipeline only; this is not a physics result.", ""]
    lines.extend(format_results_table(results).splitlines())
    lines.append("")
    failed = [name for name, result in results.items() if not result.passed]
    if failed:
        lines.append(f"Failed controls: {', '.join(failed)}.")
    else:
        lines.append("All executed controls passed finite-size tolerances.")
    lines.append("Limitations: finite matrix size and finite realizations produce sampling error; GUE is optional.")
    write_summary(output_dir / "summary.md", "R-Statistics Control Run", lines)


def format_results_table(results: dict[str, EnsembleControlResult]) -> str:
    lines = [
        "| Ensemble | Expected <r> | Measured <r> | StdErr | Tolerance | Passed |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for result in results.values():
        lines.append(
            f"| {result.ensemble.upper()} | {result.expected_r:.4f} | {result.mean_r:.4f} | "
            f"{result.stderr_r:.4f} | {result.tolerance:.4f} | {result.passed} |"
        )
    return "\n".join(lines)
