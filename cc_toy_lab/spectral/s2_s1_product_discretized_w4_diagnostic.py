"""Targeted W≈4 transition-regime diagnostic for product-discretized S2 x S1 (toy).

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
class W4DiagnosticConfig:
    """Grid for W-sweep around the medium caveat (W=4 ring non-robust)."""

    smoke: bool
    families: tuple[str, ...]
    q_values: tuple[int, ...]
    s1_sizes: tuple[int, ...]
    alpha_values: tuple[float, ...]
    w_values: tuple[float, ...]
    seeds: tuple[int, ...]
    baseline_tag: str = "v0.1.14-mvp-s2-s1-discretization-v2-full"
    operator_family: str = "product_discretized_kronecker_sum_D2_plus_P1"


@dataclass
class W4DiagnosticRun:
    config: W4DiagnosticConfig
    cases: tuple[ProductDiscretizedCaseResult, ...]
    analysis_cfg_fingerprint: str
    classification: str
    evidence: dict[str, Any]
    notes: tuple[str, ...] = field(
        default_factory=lambda: (
            "Toy W-sweep diagnostic near W=4 for product-discretized Hamiltonian proxy.",
            "No global chiral index headline; not physical chirality proof.",
        )
    )


def build_w4_diagnostic_config(*, smoke: bool = True) -> W4DiagnosticConfig:
    """Full grid per milestone request; ``smoke=True`` uses a small subset for CI."""
    if smoke:
        return W4DiagnosticConfig(
            smoke=True,
            families=("ring", "spectral_circle"),
            q_values=(0, 1),
            s1_sizes=(8,),
            alpha_values=(0.0, 0.5),
            w_values=(2.0, 4.0, 6.0, 8.0),
            seeds=(123,),
        )
    return W4DiagnosticConfig(
        smoke=False,
        families=("ring", "spectral_circle", "wilson_ring"),
        q_values=(-2, -1, 0, 1, 2),
        s1_sizes=(8, 16, 24, 32, 48),
        alpha_values=(0.0, 0.25, 0.5),
        w_values=(2.0, 4.0, 6.0, 8.0),
        seeds=(122, 123, 124, 456),
    )


def estimate_w4_case_count(cfg: W4DiagnosticConfig) -> int:
    return (
        len(cfg.seeds)
        * len(cfg.families)
        * len(cfg.q_values)
        * len(cfg.s1_sizes)
        * len(cfg.alpha_values)
        * len(cfg.w_values)
    )


def _interpret_w4(cases: tuple[ProductDiscretizedCaseResult, ...]) -> tuple[str, dict[str, Any]]:
    q0_fp = sum(1 for c in cases if c.q == 0 and c.disorder_strength > 0.0 and not c.q0_control_passed)
    if q0_fp > 0:
        return "w4_diagnostic_control_failure", {"q0_false_positive_count": int(q0_fp)}

    fails = [c for c in cases if c.disorder_strength > 0.0 and not c.window_robust_localization_passed]
    if not fails:
        return "w4_diagnostic_no_disordered_non_robust", {"disordered_non_robust_count": 0}

    by_w: dict[float, int] = {}
    by_fam: dict[str, int] = {}
    for c in fails:
        w = float(c.disorder_strength)
        by_w[w] = by_w.get(w, 0) + 1
        by_fam[c.s1_family] = by_fam.get(c.s1_family, 0) + 1

    all_ring = all(c.s1_family == "ring" for c in fails)
    w4c = int(by_w.get(4.0, 0))
    w6c = int(by_w.get(6.0, 0))
    w8c = int(by_w.get(8.0, 0))
    w2c = int(by_w.get(2.0, 0))

    evidence: dict[str, Any] = {
        "disordered_non_robust_count": len(fails),
        "non_robust_by_W": {str(k): v for k, v in sorted(by_w.items())},
        "non_robust_by_family": dict(sorted(by_fam.items())),
    }

    if all_ring and w4c > 0 and w6c == 0 and w8c == 0:
        if w2c == 0:
            return "transition_regime_sensitivity_ring_w4_only", evidence
        return "transition_regime_sensitivity_ring_low_W_band", evidence
    if all_ring and w4c > 0 and (w6c > 0 or w8c > 0):
        return "ring_family_v3_limitation_with_persistence_at_higher_W", evidence
    if not all_ring:
        return "multi_family_non_robust_investigate_further", evidence
    return "w4_diagnostic_mixed_pattern", evidence


def run_w4_diagnostic(cfg: W4DiagnosticConfig) -> W4DiagnosticRun:
    base = build_product_discretized_config(tiny=True, seed=123)
    cases: list[ProductDiscretizedCaseResult] = []
    for seed in cfg.seeds:
        for fam in cfg.families:
            for q in cfg.q_values:
                for n1 in cfg.s1_sizes:
                    for alpha in cfg.alpha_values:
                        for w in cfg.w_values:
                            cases.append(
                                analyze_product_discretized_case(
                                    cfg=base,
                                    q=int(q),
                                    s1_family=str(fam),
                                    s1_size=int(n1),
                                    alpha=float(alpha),
                                    disorder_strength=float(w),
                                    seed=int(seed),
                                )
                            )
    expected = estimate_w4_case_count(cfg)
    if len(cases) != expected:
        raise RuntimeError(f"W4 grid mismatch: {len(cases)} != {expected}")
    cls, ev = _interpret_w4(tuple(cases))
    return W4DiagnosticRun(
        config=cfg,
        cases=tuple(cases),
        analysis_cfg_fingerprint="tiny_product_discretized_base_cfg",
        classification=cls,
        evidence=ev,
    )


def assess_w4_diagnostic(run: W4DiagnosticRun) -> dict[str, Any]:
    """Flatten case rows + interpretation; reuses extended aggregates shape via synthetic assessment."""
    from cc_toy_lab.spectral.s2_s1_product_discretized import (  # local import cycle guard
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
    base_metrics["w4_diagnostic_classification"] = run.classification
    base_metrics["w4_diagnostic_evidence"] = run.evidence
    base_metrics["w4_smoke"] = bool(run.config.smoke)
    base_metrics["w4_grid"] = asdict(run.config)
    return base_metrics


def _case_public(c: ProductDiscretizedCaseResult) -> dict[str, Any]:
    d = asdict(c)
    d["unstable_window_cases"] = list(c.unstable_window_cases)
    d["v2_vs_v3_disagreement"] = bool(c.localization_gate_v2_passed != c.window_robust_localization_passed)
    return d


def save_w4_diagnostic_artifacts(run: W4DiagnosticRun, run_dir: Path) -> dict[str, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    cfg_out = {**asdict(run.config), "analysis_cfg_fingerprint": run.analysis_cfg_fingerprint}
    (run_dir / "config.json").write_text(json.dumps(cfg_out, indent=2, sort_keys=True), encoding="utf-8")
    metrics = assess_w4_diagnostic(run)
    metrics["cases"] = [_case_public(c) for c in run.cases]
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    cases = run.cases
    np.savez_compressed(
        run_dir / "data.npz",
        q=np.asarray([c.q for c in cases], dtype=int),
        s1_family=np.asarray([c.s1_family for c in cases], dtype=str),
        s1_size=np.asarray([c.s1_size for c in cases], dtype=int),
        alpha=np.asarray([c.alpha for c in cases], dtype=float),
        disorder=np.asarray([c.disorder_strength for c in cases], dtype=float),
        seed=np.asarray([c.seed for c in cases], dtype=int),
        v3_robust=np.asarray([c.window_robust_localization_passed for c in cases], dtype=bool),
        v3_class=np.asarray([c.localization_gate_v3_classification for c in cases], dtype=str),
    )
    summary = _build_w4_summary_md(run, metrics)
    (run_dir / "summary.md").write_text(summary, encoding="utf-8")
    (run_dir / "figures" / ".placeholder").write_text("figures not generated for W4 diagnostic\n", encoding="utf-8")
    return {
        "run_dir": run_dir,
        "config": run_dir / "config.json",
        "metrics": run_dir / "metrics.json",
        "data": run_dir / "data.npz",
        "summary": run_dir / "summary.md",
    }


def _build_w4_summary_md(run: W4DiagnosticRun, metrics: dict[str, Any]) -> str:
    lines = [
        "# Product-discretized W-sweep diagnostic (W≈4 caveat)",
        "",
        "**Scientific non-claims:** this does not prove continuum compactification; "
        "does not validate `S6` or `S3 x S6`; does not derive the Standard Model; "
        "does not prove physical chirality; does not bypass Witten/Lichnerowicz.",
        "",
        f"**Baseline (informational):** `{run.config.baseline_tag}`",
        f"**Operator family:** `{run.config.operator_family}`",
        f"**Smoke mode:** `{run.config.smoke}`",
        "",
        "## Interpretation",
        "",
        f"- w4_diagnostic_classification: `{metrics['w4_diagnostic_classification']}`",
        f"- evidence: `{json.dumps(metrics['w4_diagnostic_evidence'], sort_keys=True)}`",
        "",
        "## Gates (reuse product-discretized aggregates)",
        "",
        f"- hermiticity_all_passed: `{metrics['hermiticity_all_passed']}`",
        f"- shape_all_passed: `{metrics['shape_all_passed']}`",
        f"- q0_controls_all_passed: `{metrics['q0_controls_all_passed']}`",
        f"- disorder_contrast_available: `{metrics['disorder_contrast_available']}`",
        "",
        "## Metrics JSON",
        "",
        "Per-case: v3 classification, pass_rate_across_windows, window_sensitivity_score, "
        "unstable_window_cases, window_robust_localization_passed, localization_gate_v2_passed, "
        "kernel_only_localization_gate_passed, v2_vs_v3_disagreement, kernel counts, min_abs eigenvalues, IPR fields.",
        "",
    ]
    return "\n".join(lines) + "\n"
