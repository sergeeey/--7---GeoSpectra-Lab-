from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

import numpy as np

from cc_toy_lab.spectral.s1_discretization_comparison import (
    S1DiscretizationComparisonConfig,
    S1DiscretizationFamilyResult,
    compare_s1_discretizations,
)
from cc_toy_lab.spectral.s2_s1_product import S2S1ProductConfig, compare_localization_gate_v3


DEFAULT_HISTORICAL_KERNEL_ONLY_RUN = "reports/RUNS/20260512-191838_s1_discretization_comparison_full"
DEFAULT_REFERENCE_V2_RUN = "reports/RUNS/20260512-203723_s1_discretization_comparison_full"
DEFAULT_INDEPENDENT_RERUN = "reports/RUNS/20260512-211633_s1_discretization_comparison_full"
DEFAULT_INDEPENDENT_AUDIT = "reports/INDEPENDENT_AUDIT_v0.1.14.md"


@dataclass(frozen=True)
class S1DiscretizationV2StressConfig:
    """Stress configuration for the toy S2 x S1 localization gate v2."""

    benchmark_template: S2S1ProductConfig = field(default_factory=S2S1ProductConfig)
    s1_families: tuple[str, ...] = ("spectral_circle", "ring", "wilson_ring")
    reference_family: str = "spectral_circle"
    historical_kernel_only_run: str = DEFAULT_HISTORICAL_KERNEL_ONLY_RUN
    reference_v2_run: str = DEFAULT_REFERENCE_V2_RUN
    independent_rerun: str = DEFAULT_INDEPENDENT_RERUN
    independent_audit: str = DEFAULT_INDEPENDENT_AUDIT
    note: str = (
        "Toy S2 x S1 localization gate v2 stress-test across S1 discretization families. "
        "This records fixed-window robustness and preserves the historical kernel-only mixed result. "
        "This is not continuum compactification."
    )


@dataclass(frozen=True)
class S1DiscretizationV2StressAssessment:
    """Stress assessment for localization gate v2 across S1 discretization families."""

    config: S1DiscretizationV2StressConfig
    family_results: tuple[S1DiscretizationFamilyResult, ...]
    reference_family: str
    comparison_classification: str
    all_families_match_reference: bool
    all_families_pass_basic_gates: bool
    stress_classification: str
    fixed_window_all_families_passed: bool
    kernel_only_all_families_passed: bool
    case_level_fixed_window_all_passed: bool
    stress_diagnostics: dict
    notes: tuple[str, ...]


def build_stress_config(
    *,
    seed: int = 12051,
    realizations: int = 5,
    test_profile: str | None = None,
    enable_v3: bool = False,
) -> S1DiscretizationV2StressConfig:
    """Build the requested stress profile or a tiny test profile."""
    if test_profile == "tiny":
        config = S1DiscretizationV2StressConfig(
            benchmark_template=S2S1ProductConfig(
                q_values=(0, 1),
                cutoff=2,
                s1_sizes=(4, 8),
                boundary_twists=(0.0, 0.5),
                s1_modes=("clean", "geometric_weight"),
                disorder_values=(0.0, 8.0),
                perturbation_values=(0.0,),
                realizations=1,
                seed=seed,
                zero_tolerance=1e-7,
                zero_tolerance_scan=(1e-8, 1e-7, 1e-6),
                note=(
                    "Tiny toy S2 x S1 localization gate v2 stress-test profile for tests only. "
                    "This is not continuum compactification."
                ),
            ),
            note=(
                "Tiny toy S2 x S1 localization gate v2 stress-test used for tests only. "
                "Historical kernel-only results remain preserved."
            ),
        )
        return _enable_v3_in_stress_config(config, enable_v3=enable_v3)
    config = S1DiscretizationV2StressConfig(
        benchmark_template=S2S1ProductConfig(
            q_values=(0, 1, -1, 2, -2),
            cutoff=2,
            s1_sizes=(8, 16, 24, 32),
            boundary_twists=(0.0, 0.25, 0.5),
            s1_modes=("clean", "gauge_phase", "geometric_weight"),
            disorder_values=(0.0, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0),
            perturbation_values=(0.0, 1e-5),
            realizations=realizations,
            seed=seed,
            zero_tolerance=1e-7,
            zero_tolerance_scan=(1e-8, 1e-7, 1e-6),
            note=(
                "Toy S2 x S1 benchmark template used inside localization gate v2 stress-test. "
                "This is not continuum compactification."
            ),
        ),
    )
    return _enable_v3_in_stress_config(config, enable_v3=enable_v3)


def run_s1_discretization_v2_stress(config: S1DiscretizationV2StressConfig) -> S1DiscretizationV2StressAssessment:
    """Run stress-test without changing any promoted project baseline."""
    comparison = compare_s1_discretizations(
        S1DiscretizationComparisonConfig(
            benchmark_template=config.benchmark_template,
            s1_families=config.s1_families,
            reference_family=config.reference_family,
            note=config.note,
        )
    )
    family_results = tuple(comparison.family_results)
    diagnostics = _build_stress_diagnostics(config, family_results)
    fixed_window_all_families_passed = all(
        result.assessment.localization_gate_v2_passed for result in family_results
    )
    kernel_only_all_families_passed = all(
        result.assessment.kernel_only_localization_gate_passed for result in family_results
    )
    case_level_fixed_window_all_passed = not diagnostics["fixed_window_failure_cases"]
    stress_classification = _classify_stress_result(
        fixed_window_failure_cases=diagnostics["fixed_window_failure_cases"]
    )
    notes = _stress_notes(
        config=config,
        comparison_classification=comparison.classification,
        fixed_window_all_families_passed=fixed_window_all_families_passed,
        kernel_only_all_families_passed=kernel_only_all_families_passed,
        case_level_fixed_window_all_passed=case_level_fixed_window_all_passed,
        diagnostics=diagnostics,
    )
    return S1DiscretizationV2StressAssessment(
        config=config,
        family_results=family_results,
        reference_family=comparison.reference_family,
        comparison_classification=comparison.classification,
        all_families_match_reference=bool(comparison.all_families_match_reference),
        all_families_pass_basic_gates=bool(comparison.all_families_pass_basic_gates),
        stress_classification=stress_classification,
        fixed_window_all_families_passed=bool(fixed_window_all_families_passed),
        kernel_only_all_families_passed=bool(kernel_only_all_families_passed),
        case_level_fixed_window_all_passed=bool(case_level_fixed_window_all_passed),
        stress_diagnostics=diagnostics,
        notes=notes,
    )


def save_s1_discretization_v2_stress_artifacts(
    assessment: S1DiscretizationV2StressAssessment, run_dir: Path | str
) -> dict:
    """Save stress artifacts while keeping historical kernel-only evidence visible."""
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


def _build_stress_diagnostics(
    config: S1DiscretizationV2StressConfig,
    family_results: tuple[S1DiscretizationFamilyResult, ...],
) -> dict:
    failure_by_family: Counter[str] = Counter()
    failure_by_gate: Counter[str] = Counter()
    failure_by_s1_size: Counter[str] = Counter()
    failure_by_disorder: Counter[str] = Counter()
    failure_by_twist: Counter[str] = Counter()
    fixed_window_failure_cases: list[dict] = []
    disagreements: list[dict] = []
    ring_doubler_sensitive_cases: list[dict] = []
    v3_failure_count_by_family: Counter[str] = Counter()
    v3_failure_count_by_disorder: Counter[str] = Counter()
    v3_failure_count_by_s1_size: Counter[str] = Counter()
    v3_failure_count_by_alpha: Counter[str] = Counter()
    v3_failure_count_by_q: Counter[str] = Counter()
    v2_vs_v3_disagreement_count_by_family: Counter[str] = Counter()
    v3_failure_cases: list[dict] = []
    v3_window_sensitive_cases: list[dict] = []
    v3_fragile_pass_cases: list[dict] = []
    all_cases: list[dict] = []
    v3_case_level_enabled = bool(config.benchmark_template.localization_gate_v3_enabled)

    for result in family_results:
        family = result.family
        clean_index: dict[tuple[int, int, float, float, int], object] = {}
        for observation in result.assessment.observations:
            if observation.mode != "clean" or not np.isclose(observation.disorder_strength, 0.0):
                continue
            realization = _infer_realization(config.benchmark_template, observation)
            clean_index[
                (
                    int(observation.q),
                    int(observation.s1_size),
                    float(observation.alpha),
                    float(observation.perturbation),
                    int(realization),
                )
            ] = observation

        for observation in result.assessment.observations:
            if observation.mode != "geometric_weight":
                continue
            realization = _infer_realization(config.benchmark_template, observation)
            clean_key = (
                int(observation.q),
                int(observation.s1_size),
                float(observation.alpha),
                float(observation.perturbation),
                int(realization),
            )
            clean = clean_index.get(clean_key)
            if clean is None:
                raise ValueError(
                    "missing clean observation for stress diagnostic "
                    f"family={family} q={observation.q} size={observation.s1_size} "
                    f"alpha={observation.alpha} perturbation={observation.perturbation} realization={realization}"
                )
            kernel_only_localization_gate_passed = bool(observation.s1_low_energy_ipr > clean.s1_low_energy_ipr + 1e-6)
            fixed_window_localization_gate_passed = bool(
                observation.s1_fixed_window_ipr > clean.s1_fixed_window_ipr + 1e-6
            )
            case = {
                "family": family,
                "q": int(observation.q),
                "s1_size": int(observation.s1_size),
                "alpha": float(observation.alpha),
                "disorder_strength": float(observation.disorder_strength),
                "perturbation": float(observation.perturbation),
                "seed": None if observation.seed is None else int(observation.seed),
                "kernel_only_localization_gate_passed": bool(kernel_only_localization_gate_passed),
                "fixed_window_localization_gate_passed": bool(fixed_window_localization_gate_passed),
                "localization_gate_v2_passed": bool(fixed_window_localization_gate_passed),
                "window_selection_sensitivity": bool(
                    kernel_only_localization_gate_passed != fixed_window_localization_gate_passed
                ),
                "clean_ipr": float(clean.s1_low_energy_ipr),
                "disordered_ipr": float(observation.s1_low_energy_ipr),
                "clean_fixed_window_ipr": float(clean.s1_fixed_window_ipr),
                "disordered_fixed_window_ipr": float(observation.s1_fixed_window_ipr),
                "clean_kernel_count": int(clean.kernel_count),
                "disordered_kernel_count": int(observation.kernel_count),
            }
            if v3_case_level_enabled:
                v3_case = compare_localization_gate_v3(
                    q=int(observation.q),
                    cutoff=config.benchmark_template.cutoff,
                    s1_size=int(observation.s1_size),
                    alpha=float(observation.alpha),
                    seed=int(observation.seed) if observation.seed is not None else None,
                    radius=config.benchmark_template.s1_radius,
                    perturbation=float(observation.perturbation),
                    zero_tolerance=config.benchmark_template.zero_tolerance,
                    disordered_strength=float(observation.disorder_strength),
                    ipr_margin=config.benchmark_template.localization_ipr_margin,
                    s1_family=family,
                    low_energy_count_values=tuple(
                        int(x) for x in config.benchmark_template.localization_gate_v3_low_energy_count_values
                    ),
                    reference_low_energy_count=int(config.benchmark_template.low_energy_count),
                )
                case["localization_gate_v3_classification"] = str(v3_case["classification"])
                case["pass_rate_across_windows"] = float(v3_case["pass_rate_across_windows"])
                case["window_sensitivity_score"] = float(v3_case["window_sensitivity_score"])
                case["window_robust_localization_passed"] = bool(v3_case["window_robust_localization_passed"])
                case["unstable_window_cases"] = list(v3_case["unstable_window_cases"])
                case["v2_vs_v3_disagreement"] = bool(
                    case["fixed_window_localization_gate_passed"] != case["window_robust_localization_passed"]
                )
                if not case["window_robust_localization_passed"]:
                    v3_failure_count_by_family[family] += 1
                    v3_failure_count_by_disorder[_fmt_float(observation.disorder_strength)] += 1
                    v3_failure_count_by_s1_size[str(observation.s1_size)] += 1
                    v3_failure_count_by_alpha[_fmt_float(observation.alpha)] += 1
                    v3_failure_count_by_q[str(int(observation.q))] += 1
                    v3_failure_cases.append(case.copy())
                if case["localization_gate_v3_classification"] == "window_sensitive":
                    v3_window_sensitive_cases.append(case.copy())
                if case["localization_gate_v3_classification"] == "fragile_pass":
                    v3_fragile_pass_cases.append(case.copy())
                if case["v2_vs_v3_disagreement"]:
                    v2_vs_v3_disagreement_count_by_family[family] += 1
            else:
                case["localization_gate_v3_classification"] = ""
                case["pass_rate_across_windows"] = np.nan
                case["window_sensitivity_score"] = np.nan
                case["window_robust_localization_passed"] = np.nan
                case["unstable_window_cases"] = []
                case["v2_vs_v3_disagreement"] = np.nan
            all_cases.append(case)
            if not case["kernel_only_localization_gate_passed"]:
                failure_by_gate["kernel_only_localization_gate_passed"] += 1
            if not case["fixed_window_localization_gate_passed"]:
                failure_by_family[family] += 1
                failure_by_gate["fixed_window_localization_gate_passed"] += 1
                failure_by_gate["localization_gate_v2_passed"] += 1
                failure_by_s1_size[str(observation.s1_size)] += 1
                failure_by_disorder[_fmt_float(observation.disorder_strength)] += 1
                failure_by_twist[_fmt_float(observation.alpha)] += 1
                fixed_window_failure_cases.append(case)
            if case["window_selection_sensitivity"]:
                failure_by_gate["window_selection_sensitivity"] += 1
                disagreements.append(case)
                if family == "ring" and case["clean_kernel_count"] > 1:
                    ring_doubler_sensitive_cases.append(case)

    v3_enabled = False
    v3_window_robust_flags: list[bool] = []
    for result in family_results:
        v3_robust = result.assessment.window_robust_localization_passed
        v3_disagree = result.assessment.v2_vs_v3_disagreement
        if v3_robust is not None:
            v3_enabled = True
            robust_flag = bool(v3_robust)
            v3_window_robust_flags.append(robust_flag)
            if not robust_flag:
                v3_failure_count_by_family[result.family] += 1
        if v3_disagree is not None and bool(v3_disagree):
            v3_enabled = True

    return {
        "total_localization_cases": len(all_cases),
        "failure_count_by_family": dict(sorted(failure_by_family.items())),
        "failure_count_by_gate": dict(sorted(failure_by_gate.items())),
        "failure_count_by_s1_size": dict(sorted(failure_by_s1_size.items())),
        "failure_count_by_disorder": dict(sorted(failure_by_disorder.items())),
        "failure_count_by_twist": dict(sorted(failure_by_twist.items())),
        "fixed_window_failure_cases": fixed_window_failure_cases,
        "kernel_only_vs_fixed_window_disagreements": disagreements,
        "ring_doubler_sensitive_cases": ring_doubler_sensitive_cases,
        "v3_enabled": bool(v3_enabled),
        "v3_case_level_result_available": bool(v3_case_level_enabled),
        "v3_case_level_all_passed": bool(not v3_failure_cases) if v3_case_level_enabled else None,
        "v3_failure_cases": v3_failure_cases,
        "v3_window_sensitive_cases": v3_window_sensitive_cases,
        "v3_fragile_pass_cases": v3_fragile_pass_cases,
        "v3_all_families_window_robust": bool(all(v3_window_robust_flags)) if v3_window_robust_flags else None,
        "v3_failure_count_by_family": dict(sorted(v3_failure_count_by_family.items())),
        "v3_failure_count_by_disorder": dict(sorted(v3_failure_count_by_disorder.items())),
        "v3_failure_count_by_s1_size": dict(sorted(v3_failure_count_by_s1_size.items())),
        "v3_failure_count_by_alpha": dict(sorted(v3_failure_count_by_alpha.items())),
        "v3_failure_count_by_q": dict(sorted(v3_failure_count_by_q.items())),
        "v2_vs_v3_disagreement_count_by_family": dict(sorted(v2_vs_v3_disagreement_count_by_family.items())),
        "figures_generated": False,
        "all_cases": all_cases,
    }


def _config_payload(config: S1DiscretizationV2StressConfig) -> dict:
    payload = asdict(config)
    payload["benchmark_template"] = asdict(config.benchmark_template)
    return payload


def _metrics_payload(assessment: S1DiscretizationV2StressAssessment) -> dict:
    family_metrics: dict[str, dict] = {}
    for result in assessment.family_results:
        family_metrics[result.family] = {
            "classification": result.assessment.classification,
            "all_basic_gates_passed": bool(result.assessment.all_basic_gates_passed),
            "kernel_only_localization_gate_passed": bool(result.assessment.kernel_only_localization_gate_passed),
            "fixed_window_localization_gate_passed": bool(result.assessment.fixed_window_localization_gate_passed),
            "localization_gate_v2_passed": bool(result.assessment.localization_gate_v2_passed),
            "window_selection_sensitivity": bool(
                result.assessment.kernel_only_localization_gate_passed
                != result.assessment.fixed_window_localization_gate_passed
            ),
            "q_control_passed": bool(result.assessment.q_control_passed),
            "pbc_gate_passed": bool(result.assessment.pbc_gate_passed),
            "apbc_gate_passed": bool(result.assessment.apbc_gate_passed),
            "flux_response_observed": bool(result.assessment.flux_response_observed),
            "s1_not_spectator": bool(result.assessment.s1_not_spectator),
            "localization_gate_passed": bool(result.assessment.localization_gate_passed),
            "threshold_stable": bool(result.assessment.threshold_stable),
            "total_observations": int(result.assessment.total_observations),
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
    diagnostics = dict(assessment.stress_diagnostics)
    diagnostics.pop("all_cases", None)
    return {
        "reference_family": assessment.reference_family,
        "comparison_classification": assessment.comparison_classification,
        "stress_classification": assessment.stress_classification,
        "all_families_match_reference": bool(assessment.all_families_match_reference),
        "all_families_pass_basic_gates": bool(assessment.all_families_pass_basic_gates),
        "fixed_window_all_families_passed": bool(assessment.fixed_window_all_families_passed),
        "kernel_only_all_families_passed": bool(assessment.kernel_only_all_families_passed),
        "case_level_fixed_window_all_passed": bool(assessment.case_level_fixed_window_all_passed),
        "historical_kernel_only_run": assessment.config.historical_kernel_only_run,
        "reference_v2_run": assessment.config.reference_v2_run,
        "independent_rerun": assessment.config.independent_rerun,
        "independent_audit": assessment.config.independent_audit,
        "notes": list(assessment.notes),
        "family_metrics": family_metrics,
        "stress_diagnostics": diagnostics,
    }


def _data_payload(assessment: S1DiscretizationV2StressAssessment) -> dict[str, np.ndarray]:
    family_rows = tuple(assessment.family_results)
    case_rows = tuple(assessment.stress_diagnostics["all_cases"])
    return {
        "family": np.asarray([row.family for row in family_rows], dtype=str),
        "classification": np.asarray([row.assessment.classification for row in family_rows], dtype=str),
        "total_observations": np.asarray([row.assessment.total_observations for row in family_rows], dtype=int),
        "all_basic_gates_passed": np.asarray([row.assessment.all_basic_gates_passed for row in family_rows], dtype=bool),
        "kernel_only_localization_gate_passed": np.asarray(
            [row.assessment.kernel_only_localization_gate_passed for row in family_rows], dtype=bool
        ),
        "fixed_window_localization_gate_passed": np.asarray(
            [row.assessment.fixed_window_localization_gate_passed for row in family_rows], dtype=bool
        ),
        "localization_gate_v2_passed": np.asarray(
            [row.assessment.localization_gate_v2_passed for row in family_rows], dtype=bool
        ),
        "window_selection_sensitivity": np.asarray(
            [
                row.assessment.kernel_only_localization_gate_passed
                != row.assessment.fixed_window_localization_gate_passed
                for row in family_rows
            ],
            dtype=bool,
        ),
        "localization_gate_v3_classification": np.asarray(
            [row.assessment.localization_gate_v3_classification or "" for row in family_rows], dtype=str
        ),
        "pass_rate_across_windows": np.asarray(
            [
                np.nan if row.assessment.pass_rate_across_windows is None else float(row.assessment.pass_rate_across_windows)
                for row in family_rows
            ],
            dtype=float,
        ),
        "window_sensitivity_score": np.asarray(
            [
                np.nan
                if row.assessment.window_sensitivity_score is None
                else float(row.assessment.window_sensitivity_score)
                for row in family_rows
            ],
            dtype=float,
        ),
        "window_robust_localization_passed": np.asarray(
            [
                np.nan
                if row.assessment.window_robust_localization_passed is None
                else float(row.assessment.window_robust_localization_passed)
                for row in family_rows
            ],
            dtype=float,
        ),
        "v2_vs_v3_disagreement": np.asarray(
            [
                np.nan if row.assessment.v2_vs_v3_disagreement is None else float(row.assessment.v2_vs_v3_disagreement)
                for row in family_rows
            ],
            dtype=float,
        ),
        "case_family": np.asarray([row["family"] for row in case_rows], dtype=str),
        "case_q": np.asarray([row["q"] for row in case_rows], dtype=int),
        "case_s1_size": np.asarray([row["s1_size"] for row in case_rows], dtype=int),
        "case_alpha": np.asarray([row["alpha"] for row in case_rows], dtype=float),
        "case_disorder_strength": np.asarray([row["disorder_strength"] for row in case_rows], dtype=float),
        "case_perturbation": np.asarray([row["perturbation"] for row in case_rows], dtype=float),
        "case_seed": np.asarray([row["seed"] for row in case_rows], dtype=int),
        "case_kernel_only_localization_gate_passed": np.asarray(
            [row["kernel_only_localization_gate_passed"] for row in case_rows], dtype=bool
        ),
        "case_fixed_window_localization_gate_passed": np.asarray(
            [row["fixed_window_localization_gate_passed"] for row in case_rows], dtype=bool
        ),
        "case_localization_gate_v2_passed": np.asarray(
            [row["localization_gate_v2_passed"] for row in case_rows], dtype=bool
        ),
        "case_window_selection_sensitivity": np.asarray(
            [row["window_selection_sensitivity"] for row in case_rows], dtype=bool
        ),
        "case_localization_gate_v3_classification": np.asarray(
            [row["localization_gate_v3_classification"] for row in case_rows], dtype=str
        ),
        "case_pass_rate_across_windows": np.asarray([row["pass_rate_across_windows"] for row in case_rows], dtype=float),
        "case_window_sensitivity_score": np.asarray(
            [row["window_sensitivity_score"] for row in case_rows], dtype=float
        ),
        "case_window_robust_localization_passed": np.asarray(
            [row["window_robust_localization_passed"] for row in case_rows], dtype=float
        ),
        "case_v2_vs_v3_disagreement": np.asarray([row["v2_vs_v3_disagreement"] for row in case_rows], dtype=float),
        "case_clean_kernel_count": np.asarray([row["clean_kernel_count"] for row in case_rows], dtype=int),
        "case_disordered_kernel_count": np.asarray([row["disordered_kernel_count"] for row in case_rows], dtype=int),
    }


def _build_summary_markdown(assessment: S1DiscretizationV2StressAssessment) -> str:
    diagnostics = assessment.stress_diagnostics
    lines = [
        "# S1 Discretization Localization Gate v2 Stress Summary",
        "",
        "This is a toy S2 x S1 stress-test, not continuum compactification.",
        "",
        f"Stress classification: `{assessment.stress_classification}`",
        "",
        f"Comparison classification: `{assessment.comparison_classification}`",
        "",
        f"Family-aggregate fixed-window all-pass: `{assessment.fixed_window_all_families_passed}`",
        "",
        f"Case-level fixed-window all-pass: `{assessment.case_level_fixed_window_all_passed}`",
        "",
        f"Reference family: `{assessment.reference_family}`",
        "",
        f"Historical kernel-only run preserved: `{assessment.config.historical_kernel_only_run}`",
        "",
        f"Reference v2 run: `{assessment.config.reference_v2_run}`",
        "",
        f"Independent rerun: `{assessment.config.independent_rerun}`",
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
    lines.extend(
        [
            "",
            "## Stress Diagnostics",
            f"- Total localization cases: `{diagnostics['total_localization_cases']}`",
            f"- failure_count_by_family: `{json.dumps(diagnostics['failure_count_by_family'], sort_keys=True)}`",
            f"- failure_count_by_gate: `{json.dumps(diagnostics['failure_count_by_gate'], sort_keys=True)}`",
            f"- failure_count_by_s1_size: `{json.dumps(diagnostics['failure_count_by_s1_size'], sort_keys=True)}`",
            f"- failure_count_by_disorder: `{json.dumps(diagnostics['failure_count_by_disorder'], sort_keys=True)}`",
            f"- failure_count_by_twist: `{json.dumps(diagnostics['failure_count_by_twist'], sort_keys=True)}`",
            f"- fixed_window_failure_cases: `{len(diagnostics['fixed_window_failure_cases'])}`",
            f"- kernel_only_vs_fixed_window_disagreements: `{len(diagnostics['kernel_only_vs_fixed_window_disagreements'])}`",
            f"- ring_doubler_sensitive_cases: `{len(diagnostics['ring_doubler_sensitive_cases'])}`",
            f"- v3_enabled: `{diagnostics['v3_enabled']}`",
            f"- v3_case_level_result_available: `{diagnostics['v3_case_level_result_available']}`",
            f"- v3_case_level_all_passed: `{diagnostics['v3_case_level_all_passed']}`",
            f"- v3_all_families_window_robust: `{diagnostics['v3_all_families_window_robust']}`",
            f"- v3_failure_count_by_family: `{json.dumps(diagnostics['v3_failure_count_by_family'], sort_keys=True)}`",
            f"- v3_failure_count_by_disorder: `{json.dumps(diagnostics['v3_failure_count_by_disorder'], sort_keys=True)}`",
            f"- v3_failure_count_by_s1_size: `{json.dumps(diagnostics['v3_failure_count_by_s1_size'], sort_keys=True)}`",
            f"- v3_failure_count_by_alpha: `{json.dumps(diagnostics['v3_failure_count_by_alpha'], sort_keys=True)}`",
            f"- v3_failure_count_by_q: `{json.dumps(diagnostics['v3_failure_count_by_q'], sort_keys=True)}`",
            f"- v3_failure_cases: `{len(diagnostics['v3_failure_cases'])}`",
            f"- v3_window_sensitive_cases: `{len(diagnostics['v3_window_sensitive_cases'])}`",
            f"- v3_fragile_pass_cases: `{len(diagnostics['v3_fragile_pass_cases'])}`",
            (
                "- v2_vs_v3_disagreement_count_by_family: "
                f"`{json.dumps(diagnostics['v2_vs_v3_disagreement_count_by_family'], sort_keys=True)}`"
            ),
            "- No figures were generated for this stress run; `figures/` was created as a placeholder.",
            "",
            "## Interpretation Rules Applied",
            "- Historical kernel-only mixed result remains preserved and separate.",
            "- A clean fixed-window v2 stress result does not auto-promote the baseline.",
            "- Any fixed-window v2 failure must remain visible and not be hidden.",
            "",
            "## Scientific Non-Claims",
            "- not continuum compactification",
            "- not S6",
            "- not S3 x S6",
            "- not Standard Model",
            "- not physical chirality",
            "- not Witten/Lichnerowicz bypass",
            "",
            "## Notes",
            *[f"- {note}" for note in assessment.notes],
        ]
    )
    return "\n".join(lines) + "\n"


def _stress_notes(
    *,
    config: S1DiscretizationV2StressConfig,
    comparison_classification: str,
    fixed_window_all_families_passed: bool,
    kernel_only_all_families_passed: bool,
    case_level_fixed_window_all_passed: bool,
    diagnostics: dict,
) -> tuple[str, ...]:
    notes = [
        f"historical_kernel_only_run={config.historical_kernel_only_run}",
        f"reference_v2_run={config.reference_v2_run}",
        f"independent_rerun={config.independent_rerun}",
        f"comparison_classification={comparison_classification}",
        f"fixed_window_all_families_passed={fixed_window_all_families_passed}",
        f"kernel_only_all_families_passed={kernel_only_all_families_passed}",
        f"case_level_fixed_window_all_passed={case_level_fixed_window_all_passed}",
        f"fixed_window_failure_case_count={len(diagnostics['fixed_window_failure_cases'])}",
        (
            "kernel_only_vs_fixed_window_disagreement_count="
            f"{len(diagnostics['kernel_only_vs_fixed_window_disagreements'])}"
        ),
        f"ring_doubler_sensitive_case_count={len(diagnostics['ring_doubler_sensitive_cases'])}",
        "historical_kernel_only_result_not_erased=True",
        "baseline_not_auto_promoted=True",
        "no_physics_overclaim=True",
    ]
    return tuple(notes)


def _classify_stress_result(*, fixed_window_failure_cases: list[dict]) -> str:
    return "v2_stress_passed" if not fixed_window_failure_cases else "v2_limitation"


def _infer_realization(template: S2S1ProductConfig, observation) -> int:
    mode_index = template.s1_modes.index(observation.mode)
    disorder_index = template.disorder_values.index(float(observation.disorder_strength))
    perturbation_index = template.perturbation_values.index(float(observation.perturbation))
    offset = (
        int(template.seed)
        + 1_000_000 * int(observation.q + 10)
        + 100_000 * int(observation.s1_size)
        + 10_000 * int(mode_index)
        + 1_000 * int(disorder_index)
        + 100 * int(perturbation_index)
    )
    if observation.seed is None:
        raise ValueError("stress diagnostic requires observation seeds to infer realizations")
    realization = int(observation.seed) - offset
    if realization < 0 or realization >= template.realizations:
        raise ValueError(
            f"invalid inferred realization={realization} for family={observation.s1_family} seed={observation.seed}"
        )
    return realization


def _fmt_float(value: float) -> str:
    return f"{value:.6g}"


def _enable_v3_in_stress_config(
    config: S1DiscretizationV2StressConfig, *, enable_v3: bool
) -> S1DiscretizationV2StressConfig:
    if not enable_v3:
        return config
    extra = " v3 window-sweep localization diagnostic enabled (toy, non-claim)."
    return replace(
        config,
        benchmark_template=replace(
            config.benchmark_template,
            localization_gate_v3_enabled=True,
            note=config.benchmark_template.note + extra,
        ),
        note=config.note + extra,
    )
