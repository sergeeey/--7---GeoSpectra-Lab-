from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s2_s1_product import build_s2_s1_product_operator  # noqa: E402


ALLOWED_LIKELY_CAUSES = (
    "weak_disorder",
    "margin_artifact",
    "finite_size",
    "window_selection",
    "basis_artifact",
    "unresolved",
)


@dataclass(frozen=True)
class S1RingLocalizationDiagnosticConfig:
    q_values: tuple[int, ...] = (1, -1)
    cutoff: int = 2
    s1_sizes: tuple[int, ...] = (8, 16, 24, 32)
    boundary_twists: tuple[float, ...] = (0.0, 0.5)
    s1_families: tuple[str, ...] = ("spectral_circle", "ring", "wilson_ring")
    disorder_values: tuple[float, ...] = (0.0, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0)
    seeds: tuple[int, ...] = (12051, 12052, 12053, 12054, 12055)
    low_energy_count: int = 8
    zero_tolerance: float = 1e-7
    ipr_margins: tuple[float, ...] = (0.0, 1e-6, 0.01, 0.02, 0.05)
    s1_radius: float = 1.0
    note: str = (
        "Toy S1 localization sensitivity diagnostic for the S2 x S1 product benchmark. "
        "This is a discretization-sensitivity analysis only and does not claim continuum "
        "compactification, physical chirality, or any Standard Model derivation."
    )


@dataclass(frozen=True)
class LocalizationSpectrumMetrics:
    gate_ipr: float
    fixed_window_ipr: float
    min_abs_eigenvalue: float
    kernel_count: int
    low_energy_signature: tuple[float, ...]


@dataclass(frozen=True)
class LocalizationDiagnosticPoint:
    family: str
    q: int
    s1_size: int
    alpha: float
    seed: int
    disorder_strength: float
    clean_ipr: float
    disordered_ipr: float
    ipr_delta: float
    localization_gate_passed: bool
    clean_fixed_window_ipr: float
    disordered_fixed_window_ipr: float
    fixed_window_ipr_delta: float
    fixed_window_localization_passed: bool
    clean_min_abs_eigenvalue: float
    disordered_min_abs_eigenvalue: float
    clean_kernel_count: int
    disordered_kernel_count: int
    clean_low_energy_signature: tuple[float, ...]
    disordered_low_energy_signature: tuple[float, ...]
    ipr_margin_passes: tuple[tuple[str, bool], ...]


@dataclass(frozen=True)
class S1RingLocalizationDiagnosticAssessment:
    config: S1RingLocalizationDiagnosticConfig
    points: tuple[LocalizationDiagnosticPoint, ...]
    family_metrics: dict[str, dict]
    likely_cause: str
    supporting_notes: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Toy ring-localization diagnostic CLI.")
    parser.add_argument("--seed", type=int, default=12051, help="Base RNG seed for reproducible runs.")
    parser.add_argument(
        "--seed-count",
        type=int,
        default=5,
        help="Number of consecutive seeds to analyze starting from --seed.",
    )
    return parser.parse_args()


def config_from_args(args: argparse.Namespace) -> S1RingLocalizationDiagnosticConfig:
    seed_count = max(int(args.seed_count), 1)
    seeds = tuple(int(args.seed) + offset for offset in range(seed_count))
    if os.environ.get("CC_TOY_LAB_RING_DIAGNOSTIC_CLI_TEST_PROFILE") == "tiny":
        return S1RingLocalizationDiagnosticConfig(
            q_values=(1, -1),
            cutoff=2,
            s1_sizes=(8, 16),
            boundary_twists=(0.0, 0.5),
            s1_families=("spectral_circle", "ring", "wilson_ring"),
            disorder_values=(0.0, 8.0, 12.0),
            seeds=seeds[:2] if len(seeds) >= 2 else seeds,
            low_energy_count=4,
            ipr_margins=(0.0, 1e-6, 0.01),
            note=(
                "Toy S1 localization sensitivity diagnostic tiny test profile. "
                "This is not continuum compactification and does not establish full "
                "discretization robustness."
            ),
        )
    return S1RingLocalizationDiagnosticConfig(seeds=seeds)


def run_diagnostic(config: S1RingLocalizationDiagnosticConfig) -> S1RingLocalizationDiagnosticAssessment:
    clean_cache: dict[tuple[str, int, int, float], LocalizationSpectrumMetrics] = {}
    points: list[LocalizationDiagnosticPoint] = []

    for family in config.s1_families:
        for q in config.q_values:
            for s1_size in config.s1_sizes:
                for alpha in config.boundary_twists:
                    clean_key = (family, q, s1_size, float(alpha))
                    if clean_key not in clean_cache:
                        clean_cache[clean_key] = compute_spectrum_metrics(
                            q=q,
                            cutoff=config.cutoff,
                            s1_size=s1_size,
                            alpha=alpha,
                            family=family,
                            mode="clean",
                            disorder_strength=0.0,
                            seed=config.seeds[0],
                            radius=config.s1_radius,
                            zero_tolerance=config.zero_tolerance,
                            low_energy_count=config.low_energy_count,
                        )
                    clean_metrics = clean_cache[clean_key]
                    for seed in config.seeds:
                        for disorder_strength in config.disorder_values:
                            disordered_metrics = compute_spectrum_metrics(
                                q=q,
                                cutoff=config.cutoff,
                                s1_size=s1_size,
                                alpha=alpha,
                                family=family,
                                mode="geometric_weight",
                                disorder_strength=disorder_strength,
                                seed=seed,
                                radius=config.s1_radius,
                                zero_tolerance=config.zero_tolerance,
                                low_energy_count=config.low_energy_count,
                            )
                            ipr_delta = disordered_metrics.gate_ipr - clean_metrics.gate_ipr
                            fixed_window_delta = (
                                disordered_metrics.fixed_window_ipr - clean_metrics.fixed_window_ipr
                            )
                            points.append(
                                LocalizationDiagnosticPoint(
                                    family=family,
                                    q=int(q),
                                    s1_size=int(s1_size),
                                    alpha=float(alpha),
                                    seed=int(seed),
                                    disorder_strength=float(disorder_strength),
                                    clean_ipr=float(clean_metrics.gate_ipr),
                                    disordered_ipr=float(disordered_metrics.gate_ipr),
                                    ipr_delta=float(ipr_delta),
                                    localization_gate_passed=bool(
                                        disordered_metrics.gate_ipr > clean_metrics.gate_ipr + 1e-6
                                    ),
                                    clean_fixed_window_ipr=float(clean_metrics.fixed_window_ipr),
                                    disordered_fixed_window_ipr=float(disordered_metrics.fixed_window_ipr),
                                    fixed_window_ipr_delta=float(fixed_window_delta),
                                    fixed_window_localization_passed=bool(
                                        disordered_metrics.fixed_window_ipr > clean_metrics.fixed_window_ipr + 1e-6
                                    ),
                                    clean_min_abs_eigenvalue=float(clean_metrics.min_abs_eigenvalue),
                                    disordered_min_abs_eigenvalue=float(disordered_metrics.min_abs_eigenvalue),
                                    clean_kernel_count=int(clean_metrics.kernel_count),
                                    disordered_kernel_count=int(disordered_metrics.kernel_count),
                                    clean_low_energy_signature=clean_metrics.low_energy_signature,
                                    disordered_low_energy_signature=disordered_metrics.low_energy_signature,
                                    ipr_margin_passes=tuple(
                                        (
                                            _margin_key(margin),
                                            bool(disordered_metrics.gate_ipr > clean_metrics.gate_ipr + margin),
                                        )
                                        for margin in config.ipr_margins
                                    ),
                                )
                            )

    family_metrics = build_family_metrics(points=tuple(points), config=config)
    likely_cause, notes = infer_likely_cause(family_metrics)
    return S1RingLocalizationDiagnosticAssessment(
        config=config,
        points=tuple(points),
        family_metrics=family_metrics,
        likely_cause=likely_cause,
        supporting_notes=notes,
    )


def compute_spectrum_metrics(
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    family: str,
    mode: str,
    disorder_strength: float,
    seed: int,
    radius: float,
    zero_tolerance: float,
    low_energy_count: int,
) -> LocalizationSpectrumMetrics:
    operator, _lifted, metadata = build_s2_s1_product_operator(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=0.0,
        s1_family=family,
    )
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    abs_eigenvalues = np.abs(eigenvalues)
    order = np.argsort(abs_eigenvalues)
    fixed_window_indices = order[: min(int(low_energy_count), abs_eigenvalues.size)]
    kernel_indices = np.flatnonzero(abs_eigenvalues <= zero_tolerance)
    gate_indices = kernel_indices if kernel_indices.size else fixed_window_indices
    signature = tuple(float(value) for value in _normalized_signature(abs_eigenvalues[fixed_window_indices]))
    s2_dimension = int(metadata["s2_dimension"])
    return LocalizationSpectrumMetrics(
        gate_ipr=_mean_s1_marginal_ipr(
            eigenvectors=eigenvectors,
            selected_indices=np.asarray(gate_indices, dtype=int),
            s2_dimension=s2_dimension,
            s1_size=s1_size,
        ),
        fixed_window_ipr=_mean_s1_marginal_ipr(
            eigenvectors=eigenvectors,
            selected_indices=np.asarray(fixed_window_indices, dtype=int),
            s2_dimension=s2_dimension,
            s1_size=s1_size,
        ),
        min_abs_eigenvalue=float(np.min(abs_eigenvalues)),
        kernel_count=int(kernel_indices.size),
        low_energy_signature=signature,
    )


def build_family_metrics(
    points: tuple[LocalizationDiagnosticPoint, ...],
    config: S1RingLocalizationDiagnosticConfig,
) -> dict[str, dict]:
    family_metrics: dict[str, dict] = {}
    target_size = min(24, max(config.s1_sizes))
    for family in config.s1_families:
        rows = [row for row in points if row.family == family]
        target_rows = [row for row in rows if np.isclose(row.alpha, 0.0) and np.isclose(row.disorder_strength, 8.0)]
        representative_rows = [
            row
            for row in rows
            if np.isclose(row.alpha, 0.0)
            and np.isclose(row.disorder_strength, 8.0)
            and row.q == 1
            and row.s1_size == target_size
        ]
        if not representative_rows:
            representative_rows = target_rows or rows
        largest_size = max(row.s1_size for row in target_rows) if target_rows else max(row.s1_size for row in rows)
        failed_target_rows = [row for row in target_rows if not row.localization_gate_passed]
        failure_largest_size_share = _safe_fraction(
            numerator=sum(1 for row in failed_target_rows if row.s1_size == largest_size),
            denominator=len(failed_target_rows),
        )
        family_metrics[family] = {
            "representative_clean_kernel_count": float(np.mean([row.clean_kernel_count for row in representative_rows])),
            "representative_clean_ipr": float(np.mean([row.clean_ipr for row in representative_rows])),
            "representative_clean_signature": list(representative_rows[0].clean_low_energy_signature),
            "representative_disordered_signature_w8": list(representative_rows[0].disordered_low_energy_signature),
            "target_failure_rate_at_w8": _safe_fraction(
                numerator=sum(1 for row in target_rows if not row.localization_gate_passed),
                denominator=len(target_rows),
            ),
            "target_margin_flip_rate": _safe_fraction(
                numerator=sum(
                    1
                    for row in target_rows
                    if (not row.localization_gate_passed) and dict(row.ipr_margin_passes).get(_margin_key(0.0), False)
                ),
                denominator=len(target_rows),
            ),
            "target_fixed_window_recovery_rate": _safe_fraction(
                numerator=sum(
                    1
                    for row in target_rows
                    if (not row.localization_gate_passed) and row.fixed_window_localization_passed
                ),
                denominator=max(1, sum(1 for row in target_rows if not row.localization_gate_passed)),
            ),
            "target_pass_rate_at_w12": _safe_fraction(
                numerator=sum(
                    1
                    for row in rows
                    if np.isclose(row.alpha, 0.0)
                    and np.isclose(row.disorder_strength, 12.0)
                    and row.localization_gate_passed
                ),
                denominator=sum(
                    1
                    for row in rows
                    if np.isclose(row.alpha, 0.0) and np.isclose(row.disorder_strength, 12.0)
                ),
            ),
            "target_failure_largest_size_share": float(failure_largest_size_share),
            "w8_mean_ipr_delta": float(np.mean([row.ipr_delta for row in target_rows])) if target_rows else 0.0,
            "w12_mean_ipr_delta": float(
                np.mean(
                    [
                        row.ipr_delta
                        for row in rows
                        if np.isclose(row.alpha, 0.0) and np.isclose(row.disorder_strength, 12.0)
                    ]
                )
            )
            if any(np.isclose(row.alpha, 0.0) and np.isclose(row.disorder_strength, 12.0) for row in rows)
            else 0.0,
            "mean_ipr_delta_by_w": {
                _margin_key(disorder): float(
                    np.mean([row.ipr_delta for row in rows if np.isclose(row.disorder_strength, disorder)])
                )
                for disorder in config.disorder_values
            },
            "pass_rate_by_w": {
                _margin_key(disorder): _safe_fraction(
                    numerator=sum(
                        1
                        for row in rows
                        if np.isclose(row.disorder_strength, disorder) and row.localization_gate_passed
                    ),
                    denominator=sum(1 for row in rows if np.isclose(row.disorder_strength, disorder)),
                )
                for disorder in config.disorder_values
            },
        }
    return family_metrics


def infer_likely_cause(family_metrics: dict[str, dict]) -> tuple[str, tuple[str, ...]]:
    ring = family_metrics.get("ring", {})
    reference_families = [name for name in family_metrics if name != "ring"]
    reference_clean_kernel = max(
        (family_metrics[name].get("representative_clean_kernel_count", 0.0) for name in reference_families),
        default=0.0,
    )
    reference_clean_ipr = max(
        (family_metrics[name].get("representative_clean_ipr", 0.0) for name in reference_families),
        default=0.0,
    )

    notes: list[str] = []
    extra_clean_kernel = ring.get("representative_clean_kernel_count", 0.0) > reference_clean_kernel + 0.5
    elevated_clean_ipr = ring.get("representative_clean_ipr", 0.0) > max(1.5 * reference_clean_ipr, reference_clean_ipr + 0.01)
    if extra_clean_kernel:
        notes.append("ring shows extra clean kernel relative to reference families")
    if elevated_clean_ipr:
        notes.append("ring clean low-energy states already have elevated IPR")

    margin_flip_rate = ring.get("target_margin_flip_rate", 0.0)
    if margin_flip_rate >= 0.5:
        notes.append("most target failures would disappear at zero ipr_margin")
        return "margin_artifact", tuple(notes)

    fixed_window_recovery_rate = ring.get("target_fixed_window_recovery_rate", 0.0)
    if fixed_window_recovery_rate >= 0.5:
        notes.append("target failures recover when using a fixed low-energy window instead of kernel-only selection")
        if extra_clean_kernel:
            notes.append("the window-selection issue is likely triggered by a ring-specific doubled clean kernel")
        return "window_selection", tuple(notes)

    if extra_clean_kernel and elevated_clean_ipr:
        notes.append("ring clean kernel structure differs qualitatively from spectral_circle and wilson_ring")
        return "basis_artifact", tuple(notes)

    w8_failure_rate = ring.get("target_failure_rate_at_w8", 0.0)
    w12_pass_rate = ring.get("target_pass_rate_at_w12", 0.0)
    if w8_failure_rate > 0.0 and w12_pass_rate >= 0.75 and ring.get("w12_mean_ipr_delta", 0.0) > ring.get("w8_mean_ipr_delta", 0.0):
        notes.append("ring failures at W=8 weaken substantially by W=12")
        return "weak_disorder", tuple(notes)

    largest_size_share = ring.get("target_failure_largest_size_share", 0.0)
    if largest_size_share >= 0.75 and w8_failure_rate > 0.0:
        notes.append("ring failures concentrate on the largest target size")
        return "finite_size", tuple(notes)

    notes.append("no single diagnostic signature dominated the ring failure pattern")
    return "unresolved", tuple(notes)


def save_artifacts(assessment: S1RingLocalizationDiagnosticAssessment, run_dir: Path | str) -> dict[str, str]:
    run_path = Path(run_dir)
    run_path.mkdir(parents=True, exist_ok=True)
    figures_dir = run_path / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    config_path = run_path / "config.json"
    metrics_path = run_path / "metrics.json"
    data_path = run_path / "data.npz"
    summary_path = run_path / "summary.md"

    config_path.write_text(json.dumps(asdict(assessment.config), indent=2, sort_keys=True), encoding="utf-8")
    metrics_path.write_text(json.dumps(_metrics_payload(assessment), indent=2, sort_keys=True), encoding="utf-8")
    np.savez_compressed(data_path, **_data_payload(assessment))
    summary_path.write_text(_build_summary_markdown(assessment), encoding="utf-8")

    _plot_ring_ipr_vs_disorder(assessment, figures_dir / "ring_ipr_vs_disorder.png")
    _plot_family_ipr_comparison(assessment, figures_dir / "family_ipr_comparison.png")
    _plot_ipr_delta_heatmap(assessment, figures_dir / "ipr_delta_heatmap.png")

    return {
        "config": str(config_path),
        "metrics": str(metrics_path),
        "data": str(data_path),
        "summary": str(summary_path),
        "figures_dir": str(figures_dir),
    }


def make_run_dir() -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base_dir = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base_dir / f"{stamp}_s1_ring_localization_diagnostic"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def run(args: argparse.Namespace) -> tuple[Path, S1RingLocalizationDiagnosticAssessment, dict[str, str]]:
    config = config_from_args(args)
    assessment = run_diagnostic(config)
    run_dir = make_run_dir()
    artifacts = save_artifacts(assessment, run_dir)
    print_summary(run_dir=run_dir, assessment=assessment)
    return run_dir, assessment, artifacts


def print_summary(run_dir: Path, assessment: S1RingLocalizationDiagnosticAssessment) -> None:
    print(f"run_path={run_dir}")
    print(f"likely_cause={assessment.likely_cause}")
    print(f"ring_w8_failure_rate={assessment.family_metrics['ring']['target_failure_rate_at_w8']:.6f}")
    print(
        "ring_fixed_window_recovery_rate="
        f"{assessment.family_metrics['ring']['target_fixed_window_recovery_rate']:.6f}"
    )
    print("s1_ring_localization_diagnostic complete")


def _metrics_payload(assessment: S1RingLocalizationDiagnosticAssessment) -> dict:
    return {
        "likely_cause": assessment.likely_cause,
        "supporting_notes": list(assessment.supporting_notes),
        "family_metrics": assessment.family_metrics,
        "point_count": len(assessment.points),
        "scientific_non_claims": [
            "not continuum compactification",
            "not full discretization robustness",
            "not physical chirality proof",
            "not Standard Model",
            "not S6",
            "not S3 x S6",
        ],
    }


def _data_payload(assessment: S1RingLocalizationDiagnosticAssessment) -> dict[str, np.ndarray]:
    rows = assessment.points
    margin_keys = tuple(_margin_key(margin) for margin in assessment.config.ipr_margins)
    margin_arrays = {
        f"margin_pass_{key}": np.asarray([dict(row.ipr_margin_passes).get(key, False) for row in rows], dtype=bool)
        for key in margin_keys
    }
    return {
        "family": np.asarray([row.family for row in rows], dtype=str),
        "q": np.asarray([row.q for row in rows], dtype=int),
        "s1_size": np.asarray([row.s1_size for row in rows], dtype=int),
        "alpha": np.asarray([row.alpha for row in rows], dtype=float),
        "seed": np.asarray([row.seed for row in rows], dtype=int),
        "disorder_strength": np.asarray([row.disorder_strength for row in rows], dtype=float),
        "clean_ipr": np.asarray([row.clean_ipr for row in rows], dtype=float),
        "disordered_ipr": np.asarray([row.disordered_ipr for row in rows], dtype=float),
        "ipr_delta": np.asarray([row.ipr_delta for row in rows], dtype=float),
        "localization_gate_passed": np.asarray([row.localization_gate_passed for row in rows], dtype=bool),
        "clean_fixed_window_ipr": np.asarray([row.clean_fixed_window_ipr for row in rows], dtype=float),
        "disordered_fixed_window_ipr": np.asarray([row.disordered_fixed_window_ipr for row in rows], dtype=float),
        "fixed_window_ipr_delta": np.asarray([row.fixed_window_ipr_delta for row in rows], dtype=float),
        "fixed_window_localization_passed": np.asarray(
            [row.fixed_window_localization_passed for row in rows], dtype=bool
        ),
        "clean_min_abs_eigenvalue": np.asarray([row.clean_min_abs_eigenvalue for row in rows], dtype=float),
        "disordered_min_abs_eigenvalue": np.asarray(
            [row.disordered_min_abs_eigenvalue for row in rows], dtype=float
        ),
        "clean_kernel_count": np.asarray([row.clean_kernel_count for row in rows], dtype=int),
        "disordered_kernel_count": np.asarray([row.disordered_kernel_count for row in rows], dtype=int),
        **margin_arrays,
    }


def _build_summary_markdown(assessment: S1RingLocalizationDiagnosticAssessment) -> str:
    ring_metrics = assessment.family_metrics["ring"]
    lines = [
        "# S1 Ring Localization Diagnostic Summary",
        "",
        "This is a discretization-sensitivity analysis only, not continuum compactification.",
        "",
        f"Likely cause: `{assessment.likely_cause}`",
        "",
        "## Ring Target Snapshot",
        f"- target_failure_rate_at_w8: `{ring_metrics['target_failure_rate_at_w8']:.6f}`",
        f"- target_fixed_window_recovery_rate: `{ring_metrics['target_fixed_window_recovery_rate']:.6f}`",
        f"- target_pass_rate_at_w12: `{ring_metrics['target_pass_rate_at_w12']:.6f}`",
        f"- representative_clean_kernel_count: `{ring_metrics['representative_clean_kernel_count']:.6f}`",
        f"- representative_clean_ipr: `{ring_metrics['representative_clean_ipr']:.6f}`",
        "",
        "## Supporting Notes",
        *[f"- {note}" for note in assessment.supporting_notes],
        "",
        "## Family Metrics",
    ]
    for family, metrics in assessment.family_metrics.items():
        lines.extend(
            [
                f"### `{family}`",
                f"- target_failure_rate_at_w8: `{metrics['target_failure_rate_at_w8']:.6f}`",
                f"- target_fixed_window_recovery_rate: `{metrics['target_fixed_window_recovery_rate']:.6f}`",
                f"- representative_clean_kernel_count: `{metrics['representative_clean_kernel_count']:.6f}`",
                f"- representative_clean_ipr: `{metrics['representative_clean_ipr']:.6f}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Scientific Non-Claims",
            "- not continuum compactification",
            "- not full discretization robustness",
            "- not S6",
            "- not S3 x S6",
            "- not Standard Model",
            "- not physical chirality proof",
        ]
    )
    return "\n".join(lines) + "\n"


def _plot_ring_ipr_vs_disorder(assessment: S1RingLocalizationDiagnosticAssessment, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    disorder_values = assessment.config.disorder_values
    ring_rows = [row for row in assessment.points if row.family == "ring" and np.isclose(row.alpha, 0.0)]
    for s1_size in assessment.config.s1_sizes:
        size_rows = [row for row in ring_rows if row.s1_size == s1_size]
        if not size_rows:
            continue
        y_values = [
            float(np.mean([row.disordered_ipr for row in size_rows if np.isclose(row.disorder_strength, disorder)]))
            for disorder in disorder_values
        ]
        clean_level = float(np.mean([row.clean_ipr for row in size_rows]))
        ax.plot(disorder_values, y_values, marker="o", label=f"ring size={s1_size}")
        ax.axhline(clean_level, linestyle="--", alpha=0.25, color=ax.lines[-1].get_color())
    ax.set_title("Ring family IPR vs disorder")
    ax.set_xlabel("disorder strength W")
    ax.set_ylabel("mean gate IPR (alpha=0.0)")
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def _plot_family_ipr_comparison(assessment: S1RingLocalizationDiagnosticAssessment, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    disorder_values = assessment.config.disorder_values
    for family in assessment.config.s1_families:
        family_rows = [row for row in assessment.points if row.family == family and np.isclose(row.alpha, 0.0)]
        y_values = [
            float(np.mean([row.ipr_delta for row in family_rows if np.isclose(row.disorder_strength, disorder)]))
            for disorder in disorder_values
        ]
        ax.plot(disorder_values, y_values, marker="o", label=family)
    ax.axhline(0.0, linestyle="--", color="black", alpha=0.5)
    ax.set_title("Family comparison of IPR delta")
    ax.set_xlabel("disorder strength W")
    ax.set_ylabel("mean disordered-clean gate IPR delta")
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def _plot_ipr_delta_heatmap(assessment: S1RingLocalizationDiagnosticAssessment, output_path: Path) -> None:
    ring_rows = [row for row in assessment.points if row.family == "ring" and np.isclose(row.alpha, 0.0)]
    sizes = assessment.config.s1_sizes
    disorder_values = assessment.config.disorder_values
    heatmap = np.zeros((len(sizes), len(disorder_values)), dtype=float)
    for size_index, s1_size in enumerate(sizes):
        for disorder_index, disorder in enumerate(disorder_values):
            subset = [
                row.ipr_delta
                for row in ring_rows
                if row.s1_size == s1_size and np.isclose(row.disorder_strength, disorder)
            ]
            heatmap[size_index, disorder_index] = float(np.mean(subset)) if subset else 0.0
    fig, ax = plt.subplots(figsize=(8, 4.8))
    image = ax.imshow(heatmap, aspect="auto", cmap="coolwarm")
    ax.set_title("Ring IPR delta heatmap (alpha=0.0)")
    ax.set_xlabel("disorder strength W")
    ax.set_ylabel("S1 size")
    ax.set_xticks(np.arange(len(disorder_values)), labels=[str(value) for value in disorder_values])
    ax.set_yticks(np.arange(len(sizes)), labels=[str(value) for value in sizes])
    fig.colorbar(image, ax=ax, label="mean gate IPR delta")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def _mean_s1_marginal_ipr(
    eigenvectors: np.ndarray,
    selected_indices: np.ndarray,
    s2_dimension: int,
    s1_size: int,
) -> float:
    if selected_indices.size == 0:
        return float("nan")
    ipr_values: list[float] = []
    for idx in np.asarray(selected_indices, dtype=int):
        reshaped = eigenvectors[:, idx].reshape(s2_dimension, s1_size)
        marginal = np.sum(np.abs(reshaped) ** 2, axis=0)
        ipr_values.append(float(np.sum(marginal**2)))
    return float(np.mean(ipr_values))


def _normalized_signature(values: np.ndarray) -> np.ndarray:
    signature = np.asarray(values, dtype=float)
    if signature.size == 0:
        return np.zeros(0, dtype=float)
    scale = max(float(np.max(signature)), 1.0)
    return signature / scale


def _margin_key(value: float) -> str:
    return f"{float(value):g}"


def _safe_fraction(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return float(numerator) / float(denominator)


def main() -> int:
    args = parse_args()
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
