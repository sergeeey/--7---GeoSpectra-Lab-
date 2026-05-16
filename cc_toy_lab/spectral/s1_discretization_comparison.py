from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.s1_discretizations import S1_DISCRETIZATION_FAMILIES
from cc_toy_lab.spectral.s2_s1_product import S2S1Assessment, S2S1ProductConfig, run_s2_s1_product_benchmark


@dataclass(frozen=True)
class S1DiscretizationComparisonConfig:
    """Configuration shell for cross-family S1 discretization comparison."""

    benchmark_template: S2S1ProductConfig = field(default_factory=S2S1ProductConfig)
    s1_families: tuple[str, ...] = ("spectral_circle", "ring")
    reference_family: str = "spectral_circle"
    note: str = (
        "Toy S1 discretization robustness comparison for the S2 x S1 product benchmark. "
        "This compares benchmark-level gate conclusions across S1 families and does not "
        "claim continuum compactification or a full-product global chiral index theorem."
    )


@dataclass(frozen=True)
class S1DiscretizationFamilyResult:
    """Benchmark result for one S1 discretization family."""

    family: str
    assessment: S2S1Assessment


@dataclass(frozen=True)
class S1DiscretizationComparisonAssessment:
    """Cross-family comparison assessment for S1 discretization robustness."""

    config: S1DiscretizationComparisonConfig
    family_results: tuple[S1DiscretizationFamilyResult, ...]
    reference_family: str
    all_families_match_reference: bool
    all_families_pass_basic_gates: bool
    classification: str
    notes: tuple[str, ...]


def compare_s1_discretizations(config: S1DiscretizationComparisonConfig) -> S1DiscretizationComparisonAssessment:
    """Compare benchmark-level gate outcomes across S1 discretization families."""
    if not config.s1_families:
        raise ValueError("s1_families must not be empty")
    unknown = [family for family in config.s1_families if family not in S1_DISCRETIZATION_FAMILIES]
    if unknown:
        raise ValueError(f"unknown S1 discretization family: {','.join(sorted(unknown))}")
    if config.reference_family not in config.s1_families:
        raise ValueError("reference_family must be one of s1_families")

    family_results: list[S1DiscretizationFamilyResult] = []
    for family in config.s1_families:
        family_config = replace(
            config.benchmark_template,
            s1_family=family,
            note=(
                f"{config.note} Reference family={config.reference_family}; "
                f"current family={family}. {config.benchmark_template.note}"
            ),
        )
        family_results.append(
            S1DiscretizationFamilyResult(
                family=family,
                assessment=run_s2_s1_product_benchmark(family_config),
            )
        )

    results_by_family = {result.family: result for result in family_results}
    reference = results_by_family[config.reference_family].assessment
    reference_gate_vector = _gate_vector(reference)
    all_families_match_reference = all(
        _gate_vector(result.assessment) == reference_gate_vector and result.assessment.classification == reference.classification
        for result in family_results
    )
    all_families_pass_basic_gates = all(result.assessment.all_basic_gates_passed for result in family_results)

    if not reference.all_basic_gates_passed:
        classification = "reference_failed"
    elif all_families_match_reference and all_families_pass_basic_gates:
        classification = "robust_across_discretizations"
    else:
        classification = "mixed_or_limiting"

    notes = _comparison_notes(
        family_results=tuple(family_results),
        reference_family=config.reference_family,
        all_families_match_reference=all_families_match_reference,
        all_families_pass_basic_gates=all_families_pass_basic_gates,
    )
    return S1DiscretizationComparisonAssessment(
        config=config,
        family_results=tuple(family_results),
        reference_family=config.reference_family,
        all_families_match_reference=bool(all_families_match_reference),
        all_families_pass_basic_gates=bool(all_families_pass_basic_gates),
        classification=classification,
        notes=notes,
    )


def run_s1_discretization_comparison(
    config: S1DiscretizationComparisonConfig,
) -> S1DiscretizationComparisonAssessment:
    """Run the in-memory S1 discretization comparison."""
    return compare_s1_discretizations(config)


def save_s1_discretization_comparison_artifacts(
    assessment: S1DiscretizationComparisonAssessment, run_dir: Path | str
) -> dict:
    """Save comparison artifacts without changing project baseline or claims."""
    run_path = Path(run_dir)
    run_path.mkdir(parents=True, exist_ok=True)
    figures_dir = run_path / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    config_path = run_path / "config.json"
    metrics_path = run_path / "metrics.json"
    data_path = run_path / "data.npz"
    summary_path = run_path / "summary.md"

    config_path.write_text(json.dumps(_config_payload(assessment.config), indent=2, sort_keys=True), encoding="utf-8")
    metrics_path.write_text(json.dumps(_metrics_payload(assessment), indent=2, sort_keys=True), encoding="utf-8")
    np.savez_compressed(data_path, **_data_payload(assessment))
    summary_path.write_text(_build_summary_markdown(assessment), encoding="utf-8")

    return {
        "config": str(config_path),
        "metrics": str(metrics_path),
        "data": str(data_path),
        "summary": str(summary_path),
        "figures_dir": str(figures_dir),
    }


def _config_payload(config: S1DiscretizationComparisonConfig) -> dict:
    payload = asdict(config)
    payload["benchmark_template"] = asdict(config.benchmark_template)
    return payload


def _metrics_payload(assessment: S1DiscretizationComparisonAssessment) -> dict:
    family_metrics: dict[str, dict] = {}
    for result in assessment.family_results:
        family_metrics[result.family] = {
            "classification": result.assessment.classification,
            "all_basic_gates_passed": bool(result.assessment.all_basic_gates_passed),
            "total_observations": int(result.assessment.total_observations),
            "q_control_passed": bool(result.assessment.q_control_passed),
            "pbc_gate_passed": bool(result.assessment.pbc_gate_passed),
            "apbc_gate_passed": bool(result.assessment.apbc_gate_passed),
            "flux_response_observed": bool(result.assessment.flux_response_observed),
            "s1_not_spectator": bool(result.assessment.s1_not_spectator),
            "localization_gate_passed": bool(result.assessment.localization_gate_passed),
            "kernel_only_localization_gate_passed": bool(result.assessment.kernel_only_localization_gate_passed),
            "fixed_window_localization_gate_passed": bool(result.assessment.fixed_window_localization_gate_passed),
            "localization_gate_v2_passed": bool(result.assessment.localization_gate_v2_passed),
            "localization_window_mode": str(result.assessment.localization_window_mode),
            "window_selection_sensitivity": bool(
                result.assessment.kernel_only_localization_gate_passed
                != result.assessment.fixed_window_localization_gate_passed
            ),
            "threshold_stable": bool(result.assessment.threshold_stable),
            "notes": list(result.assessment.notes),
            "localization_gate_v3_classification": result.assessment.localization_gate_v3_classification,
            "pass_rate_across_windows": result.assessment.pass_rate_across_windows,
            "window_sensitivity_score": result.assessment.window_sensitivity_score,
            "window_robust_localization_passed": result.assessment.window_robust_localization_passed,
            "unstable_window_cases": (
                [dict(entry) for entry in result.assessment.unstable_window_cases]
                if result.assessment.unstable_window_cases is not None
                else None
            ),
            "v2_vs_v3_disagreement": result.assessment.v2_vs_v3_disagreement,
        }
    return {
        "reference_family": assessment.reference_family,
        "comparison_classification": assessment.classification,
        "all_families_match_reference": bool(assessment.all_families_match_reference),
        "all_families_pass_basic_gates": bool(assessment.all_families_pass_basic_gates),
        "notes": list(assessment.notes),
        "family_metrics": family_metrics,
    }


def _data_payload(assessment: S1DiscretizationComparisonAssessment) -> dict[str, np.ndarray]:
    rows = tuple(assessment.family_results)
    return {
        "family": np.asarray([row.family for row in rows], dtype=str),
        "total_observations": np.asarray([row.assessment.total_observations for row in rows], dtype=int),
        "all_basic_gates_passed": np.asarray([row.assessment.all_basic_gates_passed for row in rows], dtype=bool),
        "q_control_passed": np.asarray([row.assessment.q_control_passed for row in rows], dtype=bool),
        "pbc_gate_passed": np.asarray([row.assessment.pbc_gate_passed for row in rows], dtype=bool),
        "apbc_gate_passed": np.asarray([row.assessment.apbc_gate_passed for row in rows], dtype=bool),
        "flux_response_observed": np.asarray([row.assessment.flux_response_observed for row in rows], dtype=bool),
        "s1_not_spectator": np.asarray([row.assessment.s1_not_spectator for row in rows], dtype=bool),
        "localization_gate_passed": np.asarray([row.assessment.localization_gate_passed for row in rows], dtype=bool),
        "kernel_only_localization_gate_passed": np.asarray(
            [row.assessment.kernel_only_localization_gate_passed for row in rows], dtype=bool
        ),
        "fixed_window_localization_gate_passed": np.asarray(
            [row.assessment.fixed_window_localization_gate_passed for row in rows], dtype=bool
        ),
        "localization_gate_v2_passed": np.asarray(
            [row.assessment.localization_gate_v2_passed for row in rows], dtype=bool
        ),
        "window_selection_sensitivity": np.asarray(
            [
                row.assessment.kernel_only_localization_gate_passed
                != row.assessment.fixed_window_localization_gate_passed
                for row in rows
            ],
            dtype=bool,
        ),
        "threshold_stable": np.asarray([row.assessment.threshold_stable for row in rows], dtype=bool),
        "classification": np.asarray([row.assessment.classification for row in rows], dtype=str),
        "localization_window_mode": np.asarray([row.assessment.localization_window_mode for row in rows], dtype=str),
        "localization_gate_v3_classification": np.asarray(
            [row.assessment.localization_gate_v3_classification or "" for row in rows], dtype=str
        ),
        "pass_rate_across_windows": np.asarray(
            [
                np.nan if row.assessment.pass_rate_across_windows is None else float(row.assessment.pass_rate_across_windows)
                for row in rows
            ],
            dtype=float,
        ),
        "window_sensitivity_score": np.asarray(
            [
                np.nan if row.assessment.window_sensitivity_score is None else float(row.assessment.window_sensitivity_score)
                for row in rows
            ],
            dtype=float,
        ),
        "window_robust_localization_passed": np.asarray(
            [
                np.nan
                if row.assessment.window_robust_localization_passed is None
                else float(row.assessment.window_robust_localization_passed)
                for row in rows
            ],
            dtype=float,
        ),
        "v2_vs_v3_disagreement": np.asarray(
            [
                np.nan if row.assessment.v2_vs_v3_disagreement is None else float(row.assessment.v2_vs_v3_disagreement)
                for row in rows
            ],
            dtype=float,
        ),
    }


def _build_summary_markdown(assessment: S1DiscretizationComparisonAssessment) -> str:
    lines = [
        "# S1 Discretization Comparison Summary",
        "",
        "This is a toy S1 discretization robustness comparison, not continuum compactification.",
        "",
        "full-product global chiral index is not the headline metric.",
        "",
        f"Reference family: `{assessment.reference_family}`",
        "",
        f"Comparison classification: `{assessment.classification}`",
        "",
        f"All families match reference: `{assessment.all_families_match_reference}`",
        "",
        f"All families pass basic gates: `{assessment.all_families_pass_basic_gates}`",
        "",
        "## Family Results",
        "| Family | Classification | All Basic Gates | kernel_only_localization_gate_passed | fixed_window_localization_gate_passed | localization_gate_v2_passed | window_selection_sensitivity | Total Observations |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: |",
    ]
    for result in assessment.family_results:
        lines.append(
            f"| `{result.family}` | `{result.assessment.classification}` | "
            f"`{result.assessment.all_basic_gates_passed}` | "
            f"`{result.assessment.kernel_only_localization_gate_passed}` | "
            f"`{result.assessment.fixed_window_localization_gate_passed}` | "
            f"`{result.assessment.localization_gate_v2_passed}` | "
            f"`{result.assessment.kernel_only_localization_gate_passed != result.assessment.fixed_window_localization_gate_passed}` | "
            f"`{result.assessment.total_observations}` |"
        )
    if _comparison_includes_v3_localization(assessment):
        lines.extend(
            [
                "",
                "## Localization gate v3 (diagnostic only)",
                "",
                "Toy window sweep over `low_energy_count` values. This section does **not** assert continuum "
                "compactification, Standard Model physics, physical chirality, or a Witten/Lichnerowicz bypass.",
                "",
                "| Family | localization_gate_v3_classification | pass_rate_across_windows | "
                "window_sensitivity_score | window_robust_localization_passed | v2_vs_v3_disagreement | "
                "unstable_window_case_count |",
                "| --- | --- | ---: | ---: | --- | --- | ---: |",
            ]
        )
        for result in assessment.family_results:
            a = result.assessment
            unstable = a.unstable_window_cases
            n_unstable = len(unstable) if unstable else 0
            lines.append(
                f"| `{result.family}` | `{a.localization_gate_v3_classification}` | "
                f"`{a.pass_rate_across_windows}` | `{a.window_sensitivity_score}` | "
                f"`{a.window_robust_localization_passed}` | `{a.v2_vs_v3_disagreement}` | `{n_unstable}` |"
            )
        lines.extend(
            [
                "",
                "Full `unstable_window_cases` payloads are stored in `metrics.json` under each "
                "`family_metrics` entry.",
            ]
        )
    lines.extend(
        [
            "",
            "## Notes",
            *[f"- {note}" for note in assessment.notes],
            "",
            "## Scientific Non-Claims",
            "- not continuum compactification",
            "- not S6",
            "- not S3 x S6",
            "- not Standard Model",
            "- not physical chirality proof",
            "- not Witten/Lichnerowicz bypass",
        ]
    )
    return "\n".join(lines) + "\n"


def _comparison_includes_v3_localization(assessment: S1DiscretizationComparisonAssessment) -> bool:
    return any(result.assessment.localization_gate_v3_classification is not None for result in assessment.family_results)


def _comparison_notes(
    family_results: tuple[S1DiscretizationFamilyResult, ...],
    reference_family: str,
    all_families_match_reference: bool,
    all_families_pass_basic_gates: bool,
) -> tuple[str, ...]:
    notes = [
        f"reference_family={reference_family}",
        f"family_count={len(family_results)}",
        f"all_families_match_reference={all_families_match_reference}",
        f"all_families_pass_basic_gates={all_families_pass_basic_gates}",
    ]
    failing = [result.family for result in family_results if not result.assessment.all_basic_gates_passed]
    if failing:
        notes.append("families_with_failed_gates=" + ",".join(failing))
    sensitivity = [
        result.family
        for result in family_results
        if result.assessment.kernel_only_localization_gate_passed
        != result.assessment.fixed_window_localization_gate_passed
    ]
    if sensitivity:
        notes.append("families_with_window_selection_sensitivity=" + ",".join(sensitivity))
    return tuple(notes)


def _gate_vector(assessment: S2S1Assessment) -> tuple[bool, ...]:
    return (
        bool(assessment.q_control_passed),
        bool(assessment.pbc_gate_passed),
        bool(assessment.apbc_gate_passed),
        bool(assessment.flux_response_observed),
        bool(assessment.s1_not_spectator),
        bool(assessment.localization_gate_passed),
        bool(assessment.kernel_only_localization_gate_passed),
        bool(assessment.fixed_window_localization_gate_passed),
        bool(assessment.localization_gate_v2_passed),
        bool(assessment.threshold_stable),
        bool(assessment.all_basic_gates_passed),
    )
