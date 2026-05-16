"""Targeted ring/alpha=0 follow-up diagnostic for product-discretized S2 x S1 (toy).

Investigates whether ring/alpha=0 failures from full run are small-lattice artifacts
(vanish at s1_size>=64) or persistent ring/alpha=0 structural limitations.

Not continuum compactification; not baseline promotion; no global chiral index headline.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from cc_toy_lab.spectral.s2_s1_product_discretized import (
    ProductDiscretizedCaseResult,
    analyze_product_discretized_case,
    assess_product_discretized_results,
    build_product_discretized_config,
)


@dataclass(frozen=True)
class RingAlpha0FollowupConfig:
    """Grid for ring/alpha=0 lattice-size scaling + reference families."""

    smoke: bool
    ring_q_values: tuple[int, ...]
    ring_s1_sizes: tuple[int, ...]
    ring_w_values: tuple[float, ...]
    ring_seeds: tuple[int, ...]
    reference_families: tuple[str, ...]
    reference_q_values: tuple[int, ...]
    reference_s1_sizes: tuple[int, ...]
    reference_w_values: tuple[float, ...]
    reference_seeds: tuple[int, ...]
    alpha: float = 0.0
    baseline_tag: str = "v0.1.14-mvp-s2-s1-discretization-v2-full"
    operator_family: str = "product_discretized_kronecker_sum_D2_plus_P1"


@dataclass
class RingAlpha0FollowupRun:
    config: RingAlpha0FollowupConfig
    cases: tuple[ProductDiscretizedCaseResult, ...]
    analysis_cfg_fingerprint: str
    classification: str
    evidence: dict[str, Any]
    decision_rules: dict[str, Any]
    notes: tuple[str, ...] = field(
        default_factory=lambda: (
            "Toy ring/alpha=0 follow-up diagnostic for product-discretized Hamiltonian proxy.",
            "No global chiral index headline; not physical chirality proof.",
            "Investigates lattice-size scaling to distinguish artifact from limitation.",
        )
    )


def build_ring_alpha0_followup_config(*, smoke: bool = True) -> RingAlpha0FollowupConfig:
    """Follow-up grid per RING_ALPHA0_TARGETED_FOLLOWUP_PLAN.md.

    Smoke: small subset for CI/sanity.
    Full: targeted grid with s1_size scaling to 64/96.
    """
    if smoke:
        return RingAlpha0FollowupConfig(
            smoke=True,
            ring_q_values=(0, 1, -1),
            ring_s1_sizes=(8, 16, 32),
            ring_w_values=(0.0, 4.0, 8.0),
            ring_seeds=(123,),
            reference_families=("spectral_circle",),
            reference_q_values=(0, 1),
            reference_s1_sizes=(8, 16),
            reference_w_values=(0.0, 4.0),
            reference_seeds=(123,),
        )
    # Full targeted grid from planning doc
    return RingAlpha0FollowupConfig(
        smoke=False,
        ring_q_values=(-3, -2, -1, 0, 1, 2, 3),
        ring_s1_sizes=(8, 16, 24, 32, 48, 64, 96),
        ring_w_values=(0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0),
        ring_seeds=(123, 456, 789),  # include known failure seeds if available
        reference_families=("spectral_circle", "wilson_ring"),
        reference_q_values=(-2, -1, 0, 1, 2),
        reference_s1_sizes=(8, 16, 32, 64),
        reference_w_values=(0.0, 4.0, 8.0, 12.0),
        reference_seeds=(123, 456),
    )


def estimate_ring_alpha0_case_count(cfg: RingAlpha0FollowupConfig) -> int:
    ring_count = (
        len(cfg.ring_seeds)
        * len(cfg.ring_q_values)
        * len(cfg.ring_s1_sizes)
        * len(cfg.ring_w_values)
    )
    ref_count = (
        len(cfg.reference_seeds)
        * len(cfg.reference_families)
        * len(cfg.reference_q_values)
        * len(cfg.reference_s1_sizes)
        * len(cfg.reference_w_values)
    )
    return ring_count + ref_count


def _classify_failure_type(c: ProductDiscretizedCaseResult) -> str:
    """Classify case into failure type categories."""
    # Control failure: q=0 disordered case that fails q0_control_passed
    if c.q == 0 and c.disorder_strength > 0.0 and not c.q0_control_passed:
        return "control_failure"

    # Clean cases (W=0) always robust_pass if gates pass
    if c.disorder_strength == 0.0:
        if c.kernel_only_localization_gate_passed and c.fixed_window_localization_gate_passed:
            return "robust_pass"
        return "clean_failure"  # should not happen

    # Disordered cases
    kernel_pass = c.kernel_only_localization_gate_passed
    fixed_pass = c.fixed_window_localization_gate_passed
    v2_pass = c.localization_gate_v2_passed
    v3_robust = c.window_robust_localization_passed

    # Complete failure: both kernel_only and fixed_window fail
    if not kernel_pass and not fixed_pass:
        return "complete_failure"

    # Window-sensitive: kernel_only fails but fixed_window passes
    if not kernel_pass and fixed_pass:
        return "window_sensitive"

    # v2/v3 disagreement: v2 and v3 give different verdicts
    if v2_pass != v3_robust:
        return "v2_v3_disagreement"

    # Robust pass: all gates pass
    if kernel_pass and fixed_pass and v2_pass and v3_robust:
        return "robust_pass"

    # Mixed (partial pass, not fitting above categories)
    return "mixed_partial_pass"


def _interpret_ring_alpha0_followup(
    cases: tuple[ProductDiscretizedCaseResult, ...],
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    """Classify follow-up results and apply decision rules."""

    # Control check
    q0_fp = sum(
        1 for c in cases if c.q == 0 and c.disorder_strength > 0.0 and not c.q0_control_passed
    )
    if q0_fp > 0:
        return (
            "ring_alpha0_followup_control_failure",
            {"q0_false_positive_count": int(q0_fp)},
            {"verdict": "INVALID", "reason": "q0_control_failure"},
        )

    # Classify all disordered cases by failure type
    disordered = [c for c in cases if c.disorder_strength > 0.0]

    complete_failures = [c for c in disordered if _classify_failure_type(c) == "complete_failure"]
    window_sensitive = [c for c in disordered if _classify_failure_type(c) == "window_sensitive"]
    v2_v3_disagree = [c for c in disordered if _classify_failure_type(c) == "v2_v3_disagreement"]

    # Reference family check
    ref_families = {"spectral_circle", "wilson_ring"} & set(c.s1_family for c in cases)
    ref_fails = [c for c in complete_failures + window_sensitive if c.s1_family in ref_families]
    if ref_fails:
        return (
            "ring_alpha0_followup_cross_family_regression",
            {
                "reference_family_failure_count": len(ref_fails),
                "reference_failures": [c.s1_family for c in ref_fails],
            },
            {"verdict": "REGRESSION", "reason": "reference_family_failures"},
        )

    # Ring-only failures
    ring_complete = [c for c in complete_failures if c.s1_family == "ring"]
    ring_window_sens = [c for c in window_sensitive if c.s1_family == "ring"]

    # Aggregate by s1_size
    failures_by_size: dict[int, int] = {}
    for c in ring_complete + ring_window_sens:
        failures_by_size[c.s1_size] = failures_by_size.get(c.s1_size, 0) + 1

    # Decision Rule 1: failures at s1_size >= 64
    large_lattice_sizes = {64, 96}
    failures_at_large = sum(
        1 for c in ring_complete + ring_window_sens if c.s1_size in large_lattice_sizes
    )
    total_large_lattice = sum(
        1 for c in disordered if c.s1_family == "ring" and c.s1_size in large_lattice_sizes
    )

    failure_rate_large = failures_at_large / total_large_lattice if total_large_lattice > 0 else 0.0

    # Evidence dict
    evidence: dict[str, Any] = {
        "total_cases": len(cases),
        "ring_alpha0_cases": sum(1 for c in cases if c.s1_family == "ring"),
        "complete_failure_count": len(ring_complete),
        "window_sensitive_count": len(ring_window_sens),
        "v2_v3_disagreement_count": len(v2_v3_disagree),
        "failures_by_s1_size": {str(k): v for k, v in sorted(failures_by_size.items())},
        "failures_at_s1_size_ge_64": int(failures_at_large),
        "total_at_s1_size_ge_64": int(total_large_lattice),
        "failure_rate_at_large_lattice": float(failure_rate_large),
        "reference_family_failure_count": 0,
    }

    # Decision rules application
    decision_rules: dict[str, Any] = {}

    # Rule 1: small-lattice artifact (failures vanish at large lattices)
    if failure_rate_large < 0.02:  # <2%
        decision_rules["rule_1_small_lattice_artifact"] = True
        decision_rules["verdict"] = "SMALL_LATTICE_ARTIFACT"
        decision_rules["reason"] = f"failure_rate_at_s1_size>=64 = {failure_rate_large:.3f} < 0.02"
        classification = "ring_alpha0_small_lattice_artifact"

    # Rule 2: persistent limitation (failures persist at large lattices)
    elif failure_rate_large >= 0.06:  # >=6%
        decision_rules["rule_2_persistent_limitation"] = True
        decision_rules["verdict"] = "PERSISTENT_LIMITATION"
        decision_rules["reason"] = f"failure_rate_at_s1_size>=64 = {failure_rate_large:.3f} >= 0.06"
        classification = "ring_alpha0_persistent_limitation"

    # Rule 3: window-gate issue (only window_sensitive cases, no complete failures at large)
    elif len(ring_complete) == 0 and len(ring_window_sens) > 0:
        decision_rules["rule_3_window_gate_issue"] = True
        decision_rules["verdict"] = "WINDOW_GATE_ISSUE"
        decision_rules["reason"] = "zero_complete_failures_all_window_sensitive"
        classification = "ring_alpha0_window_gate_issue"

    # Rule 4: intermediate zone (2-6% failure rate, needs interpretation)
    else:
        decision_rules["intermediate_zone"] = True
        decision_rules["verdict"] = "INTERMEDIATE"
        decision_rules["reason"] = (
            f"failure_rate_at_s1_size>=64 = {failure_rate_large:.3f} in [0.02, 0.06) zone"
        )
        classification = "ring_alpha0_intermediate_requires_review"

    return classification, evidence, decision_rules


def run_ring_alpha0_followup(cfg: RingAlpha0FollowupConfig) -> RingAlpha0FollowupRun:
    base = build_product_discretized_config(tiny=True, seed=123)
    cases: list[ProductDiscretizedCaseResult] = []

    # Ring cases at alpha=0
    for seed in cfg.ring_seeds:
        for q in cfg.ring_q_values:
            for n1 in cfg.ring_s1_sizes:
                for w in cfg.ring_w_values:
                    cases.append(
                        analyze_product_discretized_case(
                            cfg=base,
                            q=int(q),
                            s1_family="ring",
                            s1_size=int(n1),
                            alpha=float(cfg.alpha),
                            disorder_strength=float(w),
                            seed=int(seed),
                        )
                    )

    # Reference family cases (matched subset)
    for seed in cfg.reference_seeds:
        for fam in cfg.reference_families:
            for q in cfg.reference_q_values:
                for n1 in cfg.reference_s1_sizes:
                    for w in cfg.reference_w_values:
                        cases.append(
                            analyze_product_discretized_case(
                                cfg=base,
                                q=int(q),
                                s1_family=str(fam),
                                s1_size=int(n1),
                                alpha=float(cfg.alpha),
                                disorder_strength=float(w),
                                seed=int(seed),
                            )
                        )

    expected = estimate_ring_alpha0_case_count(cfg)
    if len(cases) != expected:
        raise RuntimeError(f"Ring/alpha=0 grid mismatch: {len(cases)} != {expected}")

    cls, ev, rules = _interpret_ring_alpha0_followup(tuple(cases))

    return RingAlpha0FollowupRun(
        config=cfg,
        cases=tuple(cases),
        analysis_cfg_fingerprint="tiny_product_discretized_base_cfg",
        classification=cls,
        evidence=ev,
        decision_rules=rules,
    )


def assess_ring_alpha0_followup(run: RingAlpha0FollowupRun) -> dict[str, Any]:
    """Flatten case rows + interpretation; reuses extended aggregates shape."""
    from cc_toy_lab.spectral.s2_s1_product_discretized import (
        ProductDiscretizedAssessment,
    )

    pseudo = ProductDiscretizedAssessment(
        config=build_product_discretized_config(tiny=True, seed=123),
        cases=run.cases,
        baseline_tag=run.config.baseline_tag,
        operator_family=run.config.operator_family,
        hermiticity_all_passed=all(c.hermiticity_max_residual <= 1e-9 for c in run.cases),
        shape_all_passed=all(c.total_dimension == c.s2_dimension * c.s1_size for c in run.cases),
        reproducibility_passed=True,
        q0_controls_all_passed=all(c.q0_control_passed for c in run.cases if c.q == 0),
        classification=run.classification,
        notes=run.notes,
    )
    base_metrics = assess_product_discretized_results(pseudo)
    base_metrics["ring_alpha0_followup_classification"] = run.classification
    base_metrics["ring_alpha0_followup_evidence"] = run.evidence
    base_metrics["ring_alpha0_followup_decision_rules"] = run.decision_rules
    base_metrics["ring_alpha0_smoke"] = bool(run.config.smoke)
    base_metrics["ring_alpha0_grid"] = asdict(run.config)
    return base_metrics


def _case_public(c: ProductDiscretizedCaseResult) -> dict[str, Any]:
    d = asdict(c)
    d["unstable_window_cases"] = list(c.unstable_window_cases)
    d["v2_vs_v3_disagreement"] = bool(
        c.localization_gate_v2_passed != c.window_robust_localization_passed
    )
    d["failure_type"] = _classify_failure_type(c)
    return d


def save_ring_alpha0_followup_artifacts(
    run: RingAlpha0FollowupRun, run_dir: Path
) -> dict[str, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)

    cfg_out = {**asdict(run.config), "analysis_cfg_fingerprint": run.analysis_cfg_fingerprint}
    (run_dir / "config.json").write_text(
        json.dumps(cfg_out, indent=2, sort_keys=True), encoding="utf-8"
    )

    metrics = assess_ring_alpha0_followup(run)
    metrics["cases"] = [_case_public(c) for c in run.cases]
    (run_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8"
    )

    cases = run.cases
    np.savez_compressed(
        run_dir / "data.npz",
        q=np.asarray([c.q for c in cases], dtype=int),
        s1_family=np.asarray([c.s1_family for c in cases], dtype=str),
        s1_size=np.asarray([c.s1_size for c in cases], dtype=int),
        alpha=np.asarray([c.alpha for c in cases], dtype=float),
        disorder=np.asarray([c.disorder_strength for c in cases], dtype=float),
        seed=np.asarray([c.seed for c in cases], dtype=int),
        kernel_pass=np.asarray([c.kernel_only_localization_gate_passed for c in cases], dtype=bool),
        fixed_pass=np.asarray([c.fixed_window_localization_gate_passed for c in cases], dtype=bool),
        v2_pass=np.asarray([c.localization_gate_v2_passed for c in cases], dtype=bool),
        v3_robust=np.asarray([c.window_robust_localization_passed for c in cases], dtype=bool),
        v3_class=np.asarray([c.localization_gate_v3_classification for c in cases], dtype=str),
        failure_type=np.asarray([_classify_failure_type(c) for c in cases], dtype=str),
    )

    summary = _build_ring_alpha0_summary_md(run, metrics)
    (run_dir / "summary.md").write_text(summary, encoding="utf-8")

    (run_dir / "figures" / ".placeholder").write_text(
        "figures not generated for ring/alpha=0 followup\n", encoding="utf-8"
    )

    return {
        "run_dir": run_dir,
        "config": run_dir / "config.json",
        "metrics": run_dir / "metrics.json",
        "data": run_dir / "data.npz",
        "summary": run_dir / "summary.md",
    }


def _build_ring_alpha0_summary_md(run: RingAlpha0FollowupRun, metrics: dict[str, Any]) -> str:
    lines = [
        "# Product-discretized ring/alpha=0 follow-up diagnostic",
        "",
        "**Scientific non-claims:** this does not prove continuum compactification; "
        "does not validate `S6` or `S3 x S6`; does not derive the Standard Model; "
        "does not prove physical chirality; does not bypass Witten/Lichnerowicz.",
        "",
        f"**Baseline (informational):** `{run.config.baseline_tag}`",
        f"**Operator family:** `{run.config.operator_family}`",
        f"**Smoke mode:** `{run.config.smoke}`",
        f"**Alpha:** `{run.config.alpha}` (fixed to 0.0 for ring/alpha=0 investigation)",
        "",
        "## Purpose",
        "",
        "Investigate whether ring/alpha=0 failures from full run (51 total, 37 complete + 14 window-sensitive) "
        "are small-lattice artifacts (vanish at s1_size>=64) or persistent structural limitations.",
        "",
        "## Decision Rules Applied",
        "",
        f"- Verdict: `{run.decision_rules.get('verdict', 'UNKNOWN')}`",
        f"- Reason: `{run.decision_rules.get('reason', 'N/A')}`",
        "",
        "### Rule Definitions",
        "",
        "1. **SMALL_LATTICE_ARTIFACT**: failure_rate at s1_size>=64 < 2%",
        "2. **PERSISTENT_LIMITATION**: failure_rate at s1_size>=64 >= 6%",
        "3. **WINDOW_GATE_ISSUE**: zero complete failures, all window-sensitive",
        "4. **INTERMEDIATE**: failure_rate in [2%, 6%) zone, requires review",
        "",
        "## Interpretation",
        "",
        f"- ring_alpha0_followup_classification: `{metrics['ring_alpha0_followup_classification']}`",
        f"- evidence: `{json.dumps(metrics['ring_alpha0_followup_evidence'], sort_keys=True)}`",
        "",
        "## Core Gates",
        "",
        f"- hermiticity_all_passed: `{metrics['hermiticity_all_passed']}`",
        f"- shape_all_passed: `{metrics['shape_all_passed']}`",
        f"- q0_controls_all_passed: `{metrics['q0_controls_all_passed']}`",
        "",
        "## Failure Breakdown",
        "",
        f"- Complete failures (both gates): {metrics['ring_alpha0_followup_evidence']['complete_failure_count']}",
        f"- Window-sensitive (kernel fail, fixed pass): {metrics['ring_alpha0_followup_evidence']['window_sensitive_count']}",
        f"- v2/v3 disagreements: {metrics['ring_alpha0_followup_evidence']['v2_v3_disagreement_count']}",
        f"- Reference family failures: {metrics['ring_alpha0_followup_evidence']['reference_family_failure_count']}",
        "",
        "## Lattice-Size Scaling",
        "",
        f"- Failures by s1_size: {metrics['ring_alpha0_followup_evidence']['failures_by_s1_size']}",
        f"- Failures at s1_size>=64: {metrics['ring_alpha0_followup_evidence']['failures_at_s1_size_ge_64']}",
        f"- Total cases at s1_size>=64: {metrics['ring_alpha0_followup_evidence']['total_at_s1_size_ge_64']}",
        f"- Failure rate at large lattice: {metrics['ring_alpha0_followup_evidence']['failure_rate_at_large_lattice']:.4f}",
        "",
        "## Metrics JSON",
        "",
        "Per-case: failure_type (robust_pass, complete_failure, window_sensitive, v2_v3_disagreement, control_failure), "
        "v3 classification, pass_rate_across_windows, window_sensitivity_score, "
        "unstable_window_cases, all gate verdicts, kernel counts, min_abs eigenvalues, IPR fields.",
        "",
    ]
    return "\n".join(lines) + "\n"
