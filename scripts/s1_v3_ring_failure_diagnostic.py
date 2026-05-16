"""Targeted diagnostic for the six case-level v3 strong-disorder ring failures (toy S2 x S1).

Not continuum compactification. Does not promote baselines or alter stress metrics.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from datetime import datetime
from itertools import product
from pathlib import Path
from typing import Any, Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s2_s1_product import (  # noqa: E402
    S2S1ProductConfig,
    compare_localization_gate_v3,
)

# Six W>=8 v3 failure anchors from reports/S1_LOCALIZATION_WINDOW_V3_STRONG_DISORDER_FAILURE_ANALYSIS.md
ANCHOR_CASES: tuple[dict[str, Any], ...] = (
    {"family": "ring", "q": 1, "s1_size": 8, "alpha": 0.0, "disorder_strength": 8.0, "seed": 11836052},
    {"family": "ring", "q": -1, "s1_size": 8, "alpha": 0.0, "disorder_strength": 8.0, "seed": 9836055},
    {"family": "ring", "q": 2, "s1_size": 8, "alpha": 0.0, "disorder_strength": 12.0, "seed": 12837054},
    {"family": "ring", "q": 2, "s1_size": 8, "alpha": 0.0, "disorder_strength": 16.0, "seed": 12838052},
    {"family": "ring", "q": 2, "s1_size": 16, "alpha": 0.0, "disorder_strength": 8.0, "seed": 13636052},
    {"family": "ring", "q": 2, "s1_size": 24, "alpha": 0.0, "disorder_strength": 8.0, "seed": 14436152},
)


@dataclass(frozen=True)
class V3RingDiagnosticConfig:
    """Focused grid around v3 fragile_pass / non-robust cases on ring at strong disorder."""

    families: tuple[str, ...] = ("ring", "spectral_circle", "wilson_ring")
    q_values: tuple[int, ...] = (-2, -1, 1, 2)
    s1_sizes: tuple[int, ...] = (8, 16, 24, 32, 48)
    boundary_twists: tuple[float, ...] = (0.0, 0.25, 0.5)
    disorder_values: tuple[float, ...] = (8.0, 12.0, 16.0)
    seed_span: int = 1
    cutoff: int = 2
    perturbation: float = 0.0
    zero_tolerance: float = 1e-7
    radius: float = 1.0
    reference_low_energy_count: int = 8
    note: str = (
        "Toy S2 x S1 localization gate v3 diagnostic for six documented ring strong-disorder cases. "
        "Not continuum compactification."
    )


def _anchor_seed_set() -> tuple[int, ...]:
    return tuple(int(c["seed"]) for c in ANCHOR_CASES)


def _expand_seeds(anchors: Iterable[int], span: int) -> tuple[int, ...]:
    out: set[int] = set()
    for s in anchors:
        for d in range(-span, span + 1):
            out.add(int(s) + int(d))
    return tuple(sorted(out))


def _default_template() -> S2S1ProductConfig:
    return S2S1ProductConfig()


def _run_one_case(
    *,
    family: str,
    q: int,
    s1_size: int,
    alpha: float,
    disorder_strength: float,
    seed: int,
    cfg: V3RingDiagnosticConfig,
    template: S2S1ProductConfig,
    grid_kind: str,
) -> dict[str, Any]:
    v3 = compare_localization_gate_v3(
        q=int(q),
        cutoff=int(cfg.cutoff),
        s1_size=int(s1_size),
        alpha=float(alpha),
        seed=int(seed),
        radius=float(cfg.radius),
        perturbation=float(cfg.perturbation),
        zero_tolerance=float(cfg.zero_tolerance),
        disordered_strength=float(disorder_strength),
        ipr_margin=float(template.localization_ipr_margin),
        s1_family=str(family),
        low_energy_count_values=tuple(int(x) for x in template.localization_gate_v3_low_energy_count_values),
        reference_low_energy_count=int(cfg.reference_low_energy_count),
    )
    clean_ref = v3["clean_observation_ref"]
    dis_ref = v3["disordered_observation_ref"]
    v2_pass = bool(v3["fixed_window_localization_gate_passed"])
    v3_robust = bool(v3["window_robust_localization_passed"])
    row: dict[str, Any] = {
        "grid_kind": grid_kind,
        "family": str(family),
        "q": int(q),
        "s1_size": int(s1_size),
        "alpha": float(alpha),
        "disorder_strength": float(disorder_strength),
        "perturbation": float(cfg.perturbation),
        "seed": int(seed),
        "localization_gate_v3_classification": str(v3["classification"]),
        "pass_rate_across_windows": float(v3["pass_rate_across_windows"]),
        "window_sensitivity_score": float(v3["window_sensitivity_score"]),
        "window_robust_localization_passed": bool(v3["window_robust_localization_passed"]),
        "unstable_window_cases": list(v3["unstable_window_cases"]),
        "kernel_only_localization_gate_passed": bool(v3["kernel_only_localization_gate_passed"]),
        "fixed_window_localization_gate_passed": v2_pass,
        "localization_gate_v2_passed": v2_pass,
        "localization_gate_v2_result": "pass" if v2_pass else "fail",
        "kernel_only_result": "pass" if v3["kernel_only_localization_gate_passed"] else "fail",
        "v2_vs_v3_disagreement": bool(v2_pass != v3_robust),
        "ipr_delta_by_window": {str(k): float(v) for k, v in v3["ipr_delta_by_window"].items()},
        "pass_by_window": {str(k): bool(v) for k, v in v3["pass_by_window"].items()},
        "min_abs_eigenvalue_clean": float(clean_ref.min_abs_eigenvalue),
        "min_abs_eigenvalue_disordered": float(dis_ref.min_abs_eigenvalue),
        "kernel_count_clean": int(clean_ref.kernel_count),
        "kernel_count_disordered": int(dis_ref.kernel_count),
        "clean_s1_low_energy_ipr": float(clean_ref.s1_low_energy_ipr),
        "disordered_s1_low_energy_ipr": float(dis_ref.s1_low_energy_ipr),
        "clean_s1_fixed_window_ipr": float(clean_ref.s1_fixed_window_ipr),
        "disordered_s1_fixed_window_ipr": float(dis_ref.s1_fixed_window_ipr),
    }
    row["is_anchor_case"] = _is_anchor_row(row)
    return row


def _is_anchor_row(row: dict[str, Any]) -> bool:
    for a in ANCHOR_CASES:
        if (
            row["family"] == a["family"]
            and int(row["q"]) == int(a["q"])
            and int(row["s1_size"]) == int(a["s1_size"])
            and float(row["alpha"]) == float(a["alpha"])
            and float(row["disorder_strength"]) == float(a["disorder_strength"])
            and int(row["seed"]) == int(a["seed"])
        ):
            return True
    return False


def run_sweep(cfg: V3RingDiagnosticConfig, template: S2S1ProductConfig) -> list[dict[str, Any]]:
    seeds = _expand_seeds(_anchor_seed_set(), cfg.seed_span)
    jobs = list(
        product(
            cfg.families,
            cfg.q_values,
            cfg.s1_sizes,
            cfg.boundary_twists,
            cfg.disorder_values,
            seeds,
        )
    )
    if not jobs:
        return []

    def _one(job: tuple[str, int, int, float, float, int]) -> dict[str, Any]:
        family, q, s1_size, alpha, w, seed = job
        return _run_one_case(
            family=family,
            q=q,
            s1_size=s1_size,
            alpha=alpha,
            disorder_strength=w,
            seed=seed,
            cfg=cfg,
            template=template,
            grid_kind="sweep",
        )

    serial = os.environ.get("CC_TOY_LAB_V3_DIAG_SERIAL", "").lower() in ("1", "true", "yes")
    workers_raw = os.environ.get("CC_TOY_LAB_V3_DIAG_WORKERS", "").strip()
    if serial:
        return [_one(job) for job in jobs]
    nw = int(workers_raw) if workers_raw.isdigit() else max(1, min(8, (os.cpu_count() or 4)))
    with ThreadPoolExecutor(max_workers=nw) as pool:
        return list(pool.map(_one, jobs))


def run_anchor_exact_rows(cfg: V3RingDiagnosticConfig, template: S2S1ProductConfig) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for a in ANCHOR_CASES:
        rows.append(
            _run_one_case(
                family=str(a["family"]),
                q=int(a["q"]),
                s1_size=int(a["s1_size"]),
                alpha=float(a["alpha"]),
                disorder_strength=float(a["disorder_strength"]),
                seed=int(a["seed"]),
                cfg=cfg,
                template=template,
                grid_kind="anchor_exact",
            )
        )
    return rows


def _interpret(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Heuristic interpretation labels (toy diagnostic only; not a theorem)."""
    fails = [r for r in rows if not r["window_robust_localization_passed"]]
    if not fails:
        return {
            "diagnostic_label": "no_v3_window_robust_failures_on_this_grid",
            "reasons": ["every evaluated cell passed window_robust_localization_passed."],
            "tags": [],
        }

    fams_fail = {str(r["family"]) for r in fails}
    alphas_fail = {float(r["alpha"]) for r in fails}
    sizes_fail = {int(r["s1_size"]) for r in fails}
    tags: list[str] = []
    reasons: list[str] = []

    non_ring = bool(fams_fail - {"ring"})
    if non_ring:
        tags.append("cross_family_v3_failures")
        reasons.append("v3 non-robust cells appear outside ring.")
    else:
        tags.append("ring_only_failures")
        reasons.append("all v3 non-robust cells are on ring family.")

    if alphas_fail == {0.0}:
        tags.append("alpha_zero_only")
        reasons.append("failures restricted to alpha=0 slice.")
    elif 0.0 in alphas_fail:
        tags.append("alpha_zero_mixed")
        reasons.append("failures include alpha=0 but also other twists.")
    else:
        tags.append("no_alpha_zero_failures")
        reasons.append("no failures at alpha=0 on this sweep (unexpected vs stress anchors).")

    if fails and max(sizes_fail) <= 8:
        tags.append("small_s1_only")
        reasons.append("all failures have s1_size<=8.")
    elif fails and max(sizes_fail) >= 32:
        tags.append("persists_at_large_s1")
        reasons.append("failures still occur at s1_size>=32.")
    elif fails:
        tags.append("mixed_s1_failure_sizes")
        reasons.append("failure sizes span small and medium/large N.")

    # Seed sensitivity at anchor coordinates (ignore family for this block — anchors are ring)
    seed_blocks: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        if r["grid_kind"] not in ("sweep", "anchor_exact"):
            continue
        key = (r["family"], int(r["q"]), int(r["s1_size"]), float(r["alpha"]), float(r["disorder_strength"]))
        seed_blocks[key].append(r)

    unstable_anchor_neighborhoods = 0
    for a in ANCHOR_CASES:
        key = (a["family"], int(a["q"]), int(a["s1_size"]), float(a["alpha"]), float(a["disorder_strength"]))
        block = seed_blocks.get(key, [])
        if len(block) < 2:
            continue
        n_fail = sum(1 for r in block if not r["window_robust_localization_passed"])
        if n_fail >= 1 and n_fail < len(block):
            unstable_anchor_neighborhoods += 1
    if unstable_anchor_neighborhoods:
        tags.append("seed_neighborhood_mixed")
        reasons.append(
            f"for {unstable_anchor_neighborhoods} anchor (family,q,size,alpha,W) tuples, "
            "pass/fail varies across nearby seeds."
        )

    # Map to user-requested rubric
    if non_ring and max(sizes_fail) >= 16:
        label = "genuine_unresolved_v3_strong_disorder_limitation_candidate"
    elif not non_ring and alphas_fail == {0.0} and max(sizes_fail) <= 8:
        label = "candidate_ring_alpha0_small_s1_artifact"
    elif not non_ring and alphas_fail == {0.0}:
        label = "candidate_ring_alpha0_regime_artifact"
    elif not non_ring:
        label = "candidate_ring_discretization_artifact"
    elif non_ring:
        label = "cross_family_v3_failures_observed"
    else:
        label = "unresolved_mixed_pattern"

    return {
        "diagnostic_label": label,
        "reasons": reasons,
        "tags": tags,
        "failure_row_count": len(fails),
        "failure_families": sorted(fams_fail),
        "failure_alpha_values": sorted(alphas_fail),
        "failure_s1_sizes": sorted(sizes_fail),
        "unstable_anchor_neighborhoods": int(unstable_anchor_neighborhoods),
    }


def _config_payload(cfg: V3RingDiagnosticConfig, template: S2S1ProductConfig) -> dict[str, Any]:
    return {
        "diagnostic_config": asdict(cfg),
        "benchmark_template_defaults": asdict(template),
        "anchor_cases": list(ANCHOR_CASES),
        "baseline_tag": "v0.1.14-mvp-s2-s1-discretization-v2-full",
        "source_memo": "reports/S1_LOCALIZATION_WINDOW_V3_STRONG_DISORDER_FAILURE_ANALYSIS.md",
        "reference_stress_v3_run": "reports/RUNS/20260513-213053_s1_discretization_v2_stress_v3",
    }


def _save_npz(rows: list[dict[str, Any]], out: Path) -> None:
    def _json_map(m: dict[str, Any]) -> str:
        return json.dumps(m, sort_keys=True)

    np.savez_compressed(
        out,
        grid_kind=np.asarray([r["grid_kind"] for r in rows], dtype=str),
        family=np.asarray([r["family"] for r in rows], dtype=str),
        q=np.asarray([r["q"] for r in rows], dtype=int),
        s1_size=np.asarray([r["s1_size"] for r in rows], dtype=int),
        alpha=np.asarray([r["alpha"] for r in rows], dtype=float),
        disorder_strength=np.asarray([r["disorder_strength"] for r in rows], dtype=float),
        seed=np.asarray([r["seed"] for r in rows], dtype=int),
        is_anchor=np.asarray([bool(r["is_anchor_case"]) for r in rows], dtype=bool),
        v3_class=np.asarray([r["localization_gate_v3_classification"] for r in rows], dtype=str),
        pass_rate=np.asarray([r["pass_rate_across_windows"] for r in rows], dtype=float),
        w_score=np.asarray([r["window_sensitivity_score"] for r in rows], dtype=float),
        v3_robust=np.asarray([r["window_robust_localization_passed"] for r in rows], dtype=bool),
        v2_pass=np.asarray([r["fixed_window_localization_gate_passed"] for r in rows], dtype=bool),
        ko_pass=np.asarray([r["kernel_only_localization_gate_passed"] for r in rows], dtype=bool),
        min_ev_d=np.asarray([r["min_abs_eigenvalue_disordered"] for r in rows], dtype=float),
        kc_d=np.asarray([r["kernel_count_disordered"] for r in rows], dtype=int),
        n_unstable=np.asarray([len(r["unstable_window_cases"]) for r in rows], dtype=int),
        ipr_delta_json=np.asarray([_json_map(r["ipr_delta_by_window"]) for r in rows], dtype=str),
    )


def _summary_md(cfg: V3RingDiagnosticConfig, metrics: dict[str, Any]) -> str:
    lines = [
        "# S1 v3 ring strong-disorder failure diagnostic (toy S2 x S1)",
        "",
        "Not continuum compactification. Not S6 / S3×S6. Not Standard Model. "
        "Not physical chirality. Not Witten/Lichnerowicz bypass.",
        "",
        f"Baseline (informational): `{metrics.get('baseline_tag', '')}`",
        f"Source memo: `{metrics.get('source_memo', '')}`",
        "",
        f"Grid rows: `{metrics['counts']['total_rows']}` (sweep `{metrics['counts']['sweep_rows']}`, "
        f"anchor_exact `{metrics['counts']['anchor_rows']}`).",
        "",
        "## Interpretation (heuristic)",
        "```json",
        json.dumps(metrics["interpretation"], indent=2, sort_keys=True),
        "```",
        "",
        "## Anchor reproduction (six documented cases)",
        "```json",
        json.dumps(metrics.get("anchor_exact_rows", []), indent=2, sort_keys=True),
        "```",
        "",
        "## Failure counts by family / alpha / s1_size (evaluated cells)",
        "```json",
        json.dumps(metrics.get("failure_breakdown", {}), indent=2, sort_keys=True),
        "```",
        "",
        "## Notes",
        "- v3 uses `compare_localization_gate_v3` with the same `low_energy_count` sweep as stress.",
        "- `window_robust_localization_passed` is False for `fail` / `fragile_pass` / `window_sensitive`.",
        "- Baseline is not promoted; historical v2/kernel-only/stress records stay authoritative for their runs.",
        "",
    ]
    return "\n".join(lines) + "\n"


def _failure_breakdown(rows: list[dict[str, Any]]) -> dict[str, Any]:
    eval_rows = [r for r in rows if r["grid_kind"] in ("sweep", "anchor_exact")]
    fails = [r for r in eval_rows if not r["window_robust_localization_passed"]]
    by_fam = Counter(str(r["family"]) for r in fails)
    by_alpha = Counter(str(r["alpha"]) for r in fails)
    by_size = Counter(str(r["s1_size"]) for r in fails)
    by_w = Counter(str(r["disorder_strength"]) for r in fails)
    by_seed = Counter(str(r["seed"]) for r in fails)
    return {
        "sweep_failure_count": len(fails),
        "by_family": dict(sorted(by_fam.items())),
        "by_alpha": dict(sorted(by_alpha.items(), key=lambda kv: float(kv[0]))),
        "by_s1_size": dict(sorted(by_size.items(), key=lambda kv: int(kv[0]))),
        "by_disorder_strength": dict(sorted(by_w.items(), key=lambda kv: float(kv[0]))),
        "by_seed": dict(sorted(by_seed.items(), key=lambda kv: int(kv[0]))),
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v3 ring strong-disorder failure diagnostic (toy).")
    p.add_argument(
        "--tiny",
        action="store_true",
        help="Only the six documented anchor cases (CI smoke; no family/size sweep).",
    )
    p.add_argument(
        "--seed-span",
        type=int,
        default=None,
        help="Include each anchor seed plus [-span..+span] neighbors in sweep (default 1).",
    )
    return p.parse_args()


def make_run_dir() -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base_dir = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base_dir / f"{stamp}_s1_v3_ring_failure_diagnostic"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def main() -> int:
    args = parse_args()
    template = _default_template()
    if args.tiny:
        anchor_cfg = V3RingDiagnosticConfig(seed_span=0)
        sweep_rows: list[dict[str, Any]] = []
        anchor_rows = run_anchor_exact_rows(anchor_cfg, template)
        cfg = anchor_cfg
    else:
        span = 1 if args.seed_span is None else int(args.seed_span)
        if span < 0:
            raise SystemExit("--seed-span must be non-negative")
        cfg = V3RingDiagnosticConfig(seed_span=span)
        sweep_rows = run_sweep(cfg, template)
        anchor_rows = []

    all_rows = sweep_rows + anchor_rows

    interpretation = _interpret(all_rows)
    metrics: dict[str, Any] = {
        "baseline_tag": "v0.1.14-mvp-s2-s1-discretization-v2-full",
        "source_memo": "reports/S1_LOCALIZATION_WINDOW_V3_STRONG_DISORDER_FAILURE_ANALYSIS.md",
        "interpretation": interpretation,
        "anchor_exact_rows": anchor_rows,
        "failure_breakdown": _failure_breakdown(all_rows),
        "counts": {
            "sweep_rows": len(sweep_rows),
            "anchor_rows": len(anchor_rows),
            "total_rows": len(all_rows),
        },
        "grid_rows": all_rows,
    }

    run_dir = make_run_dir()
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.json").write_text(
        json.dumps(_config_payload(cfg, template), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    _save_npz(all_rows, run_dir / "data.npz")
    (run_dir / "summary.md").write_text(_summary_md(cfg, metrics), encoding="utf-8")
    (run_dir / "figures" / ".placeholder").write_text(
        "optional figures not generated in this diagnostic\n", encoding="utf-8"
    )

    print(f"run_path={run_dir}")
    print(f"diagnostic_label={interpretation['diagnostic_label']}")
    print("s1_v3_ring_failure_diagnostic complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
