"""Targeted diagnostic for the single W>=8 fixed-window v2 failure (toy S2 x S1).

This is not continuum compactification. Does not promote baselines or alter stress memos.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s2_s1_product import (  # noqa: E402
    S2S1ProductConfig,
    analyze_s2_s1_product,
    build_s2_s1_product_operator,
    _benchmark_seed,  # noqa: SLF001
    _low_energy_signature,  # noqa: SLF001
)

# Must match stress `s1_modes` order so `_benchmark_seed(..., mode_index=2, ...)` hits geometric_weight.
STRESS_S1_MODES = ("clean", "gauge_phase", "geometric_weight")
GEOMETRIC_MODE_INDEX = STRESS_S1_MODES.index("geometric_weight")

# First seven entries match stress `disorder_values` indices 0..6; 6.0 and 10.0 are appended for unique seeds.
DISORDER_VALUES_FOR_SEEDING: tuple[float, ...] = (0.0, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 6.0, 10.0)

DEFAULT_BASE_SEED = 12051
DEFAULT_REALIZATION = 4
DEFAULT_IPR_MARGIN = 1e-6
ANCHOR_SEED = 9836055


@dataclass(frozen=True)
class W8DiagnosticConfig:
    """Configuration for the W=8 failure diagnostic sweep."""

    base_seed: int = DEFAULT_BASE_SEED
    realization: int = DEFAULT_REALIZATION
    cutoff: int = 2
    low_energy_count: int = 8
    zero_tolerance: float = 1e-7
    chirality_threshold: float = 0.5
    ipr_margin: float = DEFAULT_IPR_MARGIN
    radius: float = 1.0
    perturbation: float = 0.0
    families: tuple[str, ...] = ("ring", "spectral_circle", "wilson_ring")
    q_values: tuple[int, ...] = (-1, 1)
    s1_sizes: tuple[int, ...] = (8, 16, 24, 32)
    boundary_twists: tuple[float, ...] = (0.0, 0.25, 0.5)
    disorder_sweep: tuple[float, ...] = (6.0, 8.0, 10.0, 12.0, 16.0)
    seed_sensitivity_span: int = 10
    ipr_margin_sweep: tuple[float, ...] = (0.0, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4)
    low_energy_count_sweep: tuple[int, ...] = (4, 6, 8, 10, 12)
    note: str = (
        "Toy S2 x S1 localization gate v2 diagnostic around the r=5 stress W=8 ring outlier. "
        "Not continuum compactification."
    )


def _disorder_index_for_seeding(disorder_strength: float) -> int:
    for i, w in enumerate(DISORDER_VALUES_FOR_SEEDING):
        if float(w) == float(disorder_strength):
            return int(i)
    raise ValueError(f"disorder_strength={disorder_strength!r} not in seeding tuple")


def _run_seed(*, base_seed: int, q: int, s1_size: int, disorder_strength: float, realization: int, perturbation_index: int) -> int:
    d_idx = _disorder_index_for_seeding(disorder_strength)
    return int(
        _benchmark_seed(
            base_seed,
            q,
            s1_size,
            GEOMETRIC_MODE_INDEX,
            d_idx,
            perturbation_index,
            realization,
        )
    )


def _gates(
    *,
    clean_ipr_k: float,
    dis_ipr_k: float,
    clean_ipr_fw: float,
    dis_ipr_fw: float,
    margin: float,
) -> tuple[bool, bool, bool]:
    ko = bool(dis_ipr_k > clean_ipr_k + margin)
    fw = bool(dis_ipr_fw > clean_ipr_fw + margin)
    return ko, fw, bool(ko != fw)


def _analyze_pair(
    *,
    family: str,
    q: int,
    s1_size: int,
    alpha: float,
    disorder_strength: float,
    seed: int,
    cfg: W8DiagnosticConfig,
) -> tuple[object, object]:
    common = dict(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=alpha,
        radius=cfg.radius,
        perturbation=cfg.perturbation,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.low_energy_count,
        chirality_tolerance=cfg.chirality_threshold,
        s1_family=family,
    )
    clean = analyze_s2_s1_product(mode="clean", disorder_strength=0.0, seed=seed, **common)
    disordered = analyze_s2_s1_product(
        mode="geometric_weight",
        disorder_strength=float(disorder_strength),
        seed=seed,
        **common,
    )
    return clean, disordered


def _row_from_pair(
    *,
    family: str,
    q: int,
    s1_size: int,
    alpha: float,
    disorder_strength: float,
    seed: int,
    clean,
    disordered,
    margin: float,
    low_energy_count: int,
) -> dict:
    fw_delta = float(disordered.s1_fixed_window_ipr - clean.s1_fixed_window_ipr)
    ko_delta = float(disordered.s1_low_energy_ipr - clean.s1_low_energy_ipr)
    ko_pass, fw_pass, sens = _gates(
        clean_ipr_k=clean.s1_low_energy_ipr,
        dis_ipr_k=disordered.s1_low_energy_ipr,
        clean_ipr_fw=clean.s1_fixed_window_ipr,
        dis_ipr_fw=disordered.s1_fixed_window_ipr,
        margin=margin,
    )
    return {
        "family": family,
        "q": int(q),
        "s1_size": int(s1_size),
        "alpha": float(alpha),
        "disorder_strength": float(disorder_strength),
        "perturbation": float(clean.perturbation),
        "seed": int(seed),
        "clean_fixed_window_ipr": float(clean.s1_fixed_window_ipr),
        "disordered_fixed_window_ipr": float(disordered.s1_fixed_window_ipr),
        "fixed_window_ipr_delta": fw_delta,
        "clean_kernel_only_ipr": float(clean.s1_low_energy_ipr),
        "disordered_kernel_only_ipr": float(disordered.s1_low_energy_ipr),
        "kernel_only_ipr_delta": ko_delta,
        "clean_kernel_count": int(clean.kernel_count),
        "disordered_kernel_count": int(disordered.kernel_count),
        "clean_min_abs_eigenvalue": float(clean.min_abs_eigenvalue),
        "disordered_min_abs_eigenvalue": float(disordered.min_abs_eigenvalue),
        "kernel_only_localization_gate_passed": ko_pass,
        "fixed_window_localization_gate_passed": fw_pass,
        "window_selection_sensitivity": sens,
        "ipr_margin_used": float(margin),
        "low_energy_count_used": int(low_energy_count),
    }


def _spectrum_block(
    *,
    family: str,
    q: int,
    s1_size: int,
    alpha: float,
    disorder_strength: float,
    seed: int,
    cfg: W8DiagnosticConfig,
) -> dict:
    common_sig = dict(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=alpha,
        radius=cfg.radius,
        perturbation=cfg.perturbation,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.low_energy_count,
        s1_family=family,
    )
    clean_sig = _low_energy_signature(
        mode="clean",
        disorder_strength=0.0,
        seed=seed,
        **common_sig,
    )
    dis_sig = _low_energy_signature(
        mode="geometric_weight",
        disorder_strength=float(disorder_strength),
        seed=seed,
        **common_sig,
    )
    op_c, _, meta_c = build_s2_s1_product_operator(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode="clean",
        disorder_strength=0.0,
        seed=seed,
        radius=cfg.radius,
        perturbation=cfg.perturbation,
        s1_family=family,
    )
    op_d, _, _meta_d = build_s2_s1_product_operator(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode="geometric_weight",
        disorder_strength=float(disorder_strength),
        seed=seed,
        radius=cfg.radius,
        perturbation=cfg.perturbation,
        s1_family=family,
    )
    ev_c = np.linalg.eigvalsh(op_c)
    ev_d = np.linalg.eigvalsh(op_d)
    abs_c = np.sort(np.abs(ev_c))[: cfg.low_energy_count]
    abs_d = np.sort(np.abs(ev_d))[: cfg.low_energy_count]
    return {
        "clean_low_energy_abs_spectrum": abs_c.tolist(),
        "disordered_low_energy_abs_spectrum": abs_d.tolist(),
        "clean_scaled_signature": clean_sig.tolist(),
        "disordered_scaled_signature": dis_sig.tolist(),
        "signature_l1_delta": float(np.sum(np.abs(np.asarray(clean_sig, dtype=float) - np.asarray(dis_sig, dtype=float)))),
        "s2_dimension": int(meta_c["s2_dimension"]),
        "total_dimension": int(meta_c["total_dimension"]),
    }


def run_primary_grid(cfg: W8DiagnosticConfig) -> list[dict]:
    rows: list[dict] = []
    for family, q, s1_size, alpha, w in product(
        cfg.families,
        cfg.q_values,
        cfg.s1_sizes,
        cfg.boundary_twists,
        cfg.disorder_sweep,
    ):
        seed = _run_seed(
            base_seed=cfg.base_seed,
            q=q,
            s1_size=s1_size,
            disorder_strength=w,
            realization=cfg.realization,
            perturbation_index=0,
        )
        clean, disordered = _analyze_pair(
            family=family,
            q=q,
            s1_size=s1_size,
            alpha=alpha,
            disorder_strength=w,
            seed=seed,
            cfg=cfg,
        )
        row = _row_from_pair(
            family=family,
            q=q,
            s1_size=s1_size,
            alpha=alpha,
            disorder_strength=w,
            seed=seed,
            clean=clean,
            disordered=disordered,
            margin=cfg.ipr_margin,
            low_energy_count=cfg.low_energy_count,
        )
        row["grid_kind"] = "primary"
        rows.append(row)
    return rows


def run_seed_sensitivity(cfg: W8DiagnosticConfig) -> list[dict]:
    rows: list[dict] = []
    family, q, s1_size, alpha, w = "ring", -1, 8, 0.0, 8.0
    for delta in range(-cfg.seed_sensitivity_span, cfg.seed_sensitivity_span + 1):
        seed = ANCHOR_SEED + int(delta)
        clean, disordered = _analyze_pair(
            family=family,
            q=q,
            s1_size=s1_size,
            alpha=alpha,
            disorder_strength=w,
            seed=seed,
            cfg=cfg,
        )
        row = _row_from_pair(
            family=family,
            q=q,
            s1_size=s1_size,
            alpha=alpha,
            disorder_strength=w,
            seed=seed,
            clean=clean,
            disordered=disordered,
            margin=cfg.ipr_margin,
            low_energy_count=cfg.low_energy_count,
        )
        row["grid_kind"] = "seed_sensitivity"
        row["seed_delta_from_anchor"] = int(delta)
        rows.append(row)
    return rows


def run_anchor_exact_extended(cfg: W8DiagnosticConfig) -> dict:
    """Exact stress-matching anchor + margin / low_energy sweeps (no extra eigh for margin-only)."""
    family, q, s1_size, alpha, w = "ring", -1, 8, 0.0, 8.0
    seed = ANCHOR_SEED
    clean, disordered = _analyze_pair(
        family=family,
        q=q,
        s1_size=s1_size,
        alpha=alpha,
        disorder_strength=w,
        seed=seed,
        cfg=cfg,
    )
    base_row = _row_from_pair(
        family=family,
        q=q,
        s1_size=s1_size,
        alpha=alpha,
        disorder_strength=w,
        seed=seed,
        clean=clean,
        disordered=disordered,
        margin=cfg.ipr_margin,
        low_energy_count=cfg.low_energy_count,
    )
    base_row["grid_kind"] = "anchor_exact"

    margin_rows: list[dict] = []
    for m in cfg.ipr_margin_sweep:
        ko, fw, sens = _gates(
            clean_ipr_k=clean.s1_low_energy_ipr,
            dis_ipr_k=disordered.s1_low_energy_ipr,
            clean_ipr_fw=clean.s1_fixed_window_ipr,
            dis_ipr_fw=disordered.s1_fixed_window_ipr,
            margin=float(m),
        )
        margin_rows.append(
            {
                "ipr_margin": float(m),
                "kernel_only_pass": ko,
                "fixed_window_pass": fw,
                "window_selection_sensitivity": sens,
            }
        )

    le_rows: list[dict] = []
    for lec in cfg.low_energy_count_sweep:
        sub = dataclasses.replace(cfg, low_energy_count=int(lec))
        c2, d2 = _analyze_pair(
            family=family,
            q=q,
            s1_size=s1_size,
            alpha=alpha,
            disorder_strength=w,
            seed=seed,
            cfg=sub,
        )
        ko, fw, sens = _gates(
            clean_ipr_k=c2.s1_low_energy_ipr,
            dis_ipr_k=d2.s1_low_energy_ipr,
            clean_ipr_fw=c2.s1_fixed_window_ipr,
            dis_ipr_fw=d2.s1_fixed_window_ipr,
            margin=cfg.ipr_margin,
        )
        le_rows.append(
            {
                "low_energy_count": int(lec),
                "kernel_only_pass": ko,
                "fixed_window_pass": fw,
                "window_selection_sensitivity": sens,
                "fixed_window_ipr_delta": float(d2.s1_fixed_window_ipr - c2.s1_fixed_window_ipr),
                "kernel_only_ipr_delta": float(d2.s1_low_energy_ipr - c2.s1_low_energy_ipr),
            }
        )

    spectrum = _spectrum_block(
        family=family,
        q=q,
        s1_size=s1_size,
        alpha=alpha,
        disorder_strength=w,
        seed=seed,
        cfg=cfg,
    )
    return {
        "anchor_base_row": base_row,
        "ipr_margin_sensitivity": margin_rows,
        "low_energy_count_sensitivity": le_rows,
        "spectrum": spectrum,
    }


def _classify(rows: list[dict], anchor_block: dict) -> dict:
    """Heuristic classification from primary grid + seed sweep (interpretation aid only)."""
    w8 = [r for r in rows if r.get("grid_kind") == "primary" and float(r["disorder_strength"]) >= 8.0]
    fw_fail_w8 = [r for r in w8 if not r["fixed_window_localization_gate_passed"]]
    by_fam: dict[str, int] = {}
    for r in fw_fail_w8:
        by_fam[r["family"]] = by_fam.get(r["family"], 0) + 1

    seed_rows = [r for r in rows if r.get("grid_kind") == "seed_sensitivity"]
    anchor_fw_fails = sum(1 for r in seed_rows if not r["fixed_window_localization_gate_passed"])

    ring_s8 = [r for r in w8 if r["family"] == "ring" and r["s1_size"] == 8 and not r["fixed_window_localization_gate_passed"]]
    other_sizes = [r for r in w8 if r["s1_size"] != 8 and not r["fixed_window_localization_gate_passed"]]
    other_fam = [r for r in w8 if r["family"] != "ring" and not r["fixed_window_localization_gate_passed"]]

    margin_flip = anchor_block["ipr_margin_sensitivity"]
    margin_passes = [bool(r["fixed_window_pass"]) for r in margin_flip]
    margin_sensitive = bool(margin_passes) and any(margin_passes) and not all(margin_passes)

    le_flip = anchor_block["low_energy_count_sensitivity"]
    le_passes = [bool(r["fixed_window_pass"]) for r in le_flip]
    le_sensitive = bool(le_passes) and any(le_passes) and not all(le_passes)

    reasons: list[str] = []
    label = "unresolved"

    non_ring_fail = bool(other_fam)
    larger_size_fail = bool([r for r in fw_fail_w8 if int(r["s1_size"]) > 8])

    if not fw_fail_w8:
        label = "not_reproduced_on_primary_w_ge_8_grid"
        reasons.append("no fixed-window failures for W>=8 on the primary diagnostic grid with stress-aligned seeds.")
    elif non_ring_fail and larger_size_fail:
        label = "genuine_strong_disorder_v2_limitation"
        reasons.append("fixed-window failures at W>=8 appear for a non-ring family and for s1_size>8.")
    elif non_ring_fail or larger_size_fail:
        label = "unresolved"
        reasons.append("partial spread across family/size at W>=8; not enough to claim global strong-disorder limitation.")
    elif le_sensitive:
        label = "threshold_or_window_definition_artifact"
        reasons.append(
            "fixed-window outcome flips with low_energy_count while kernel-only stays passed on the anchor "
            "(fixed low-energy window vs kernel-selected window mismatch)."
        )
    elif margin_sensitive:
        label = "threshold_or_ipr_margin_artifact"
        reasons.append("fixed_window gate depends on ipr_margin on the anchor (threshold/margin coupling).")
    elif all(r["family"] == "ring" and int(r["s1_size"]) == 8 for r in fw_fail_w8):
        if len(seed_rows) >= 5 and anchor_fw_fails <= max(2, len(seed_rows) // 5):
            label = "seed_specific_or_small_size_window_selection_artifact"
            reasons.append("failures at W>=8 stay on ring/s1_size=8; nearby seeds rarely fail.")
        else:
            label = "ring_small_size_window_selection_artifact"
            reasons.append("failures at W>=8 stay on ring/s1_size=8; seed neighborhood shows repeated sensitivity.")
    else:
        label = "unresolved"

    return {
        "diagnostic_classification": label,
        "reasons": reasons,
        "margin_sensitivity_on_anchor": margin_sensitive,
        "low_energy_count_sensitivity_on_anchor": le_sensitive,
        "primary_w8_ge_fixed_window_failures": len(fw_fail_w8),
        "primary_w8_failures_by_family": by_fam,
        "seed_sensitivity_anchor_fixed_window_failures": int(anchor_fw_fails),
        "seed_sensitivity_total": len(seed_rows),
        "ring_s1_size_8_w8_failures": len(ring_s8),
        "non_ring_w8_failures": len(other_fam),
        "w8_failures_non_s1_8": len(other_sizes),
    }


def _build_config_payload(cfg: W8DiagnosticConfig) -> dict:
    d = asdict(cfg)
    d["benchmark_template_defaults"] = asdict(S2S1ProductConfig())
    d["stress_s1_modes_reference"] = list(STRESS_S1_MODES)
    d["disorder_values_for_seeding"] = list(DISORDER_VALUES_FOR_SEEDING)
    d["anchor_reference_seed"] = ANCHOR_SEED
    d["baseline_tag"] = "v0.1.14-mvp-s2-s1-discretization-v2-full"
    d["reference_stress_run"] = "reports/RUNS/20260513-001436_s1_discretization_v2_stress"
    return d


def _save_npz(*, rows: list[dict], anchor: dict, out: Path) -> None:
    fam = np.asarray([r["family"] for r in rows], dtype=str)
    np.savez_compressed(
        out,
        grid_kind=np.asarray([r.get("grid_kind", "") for r in rows], dtype=str),
        family=fam,
        q=np.asarray([r["q"] for r in rows], dtype=int),
        s1_size=np.asarray([r["s1_size"] for r in rows], dtype=int),
        alpha=np.asarray([r["alpha"] for r in rows], dtype=float),
        disorder_strength=np.asarray([r["disorder_strength"] for r in rows], dtype=float),
        seed=np.asarray([r["seed"] for r in rows], dtype=int),
        fixed_window_ipr_delta=np.asarray([r["fixed_window_ipr_delta"] for r in rows], dtype=float),
        kernel_only_ipr_delta=np.asarray([r["kernel_only_ipr_delta"] for r in rows], dtype=float),
        kernel_only_pass=np.asarray([r["kernel_only_localization_gate_passed"] for r in rows], dtype=bool),
        fixed_window_pass=np.asarray([r["fixed_window_localization_gate_passed"] for r in rows], dtype=bool),
        window_sensitivity=np.asarray([r["window_selection_sensitivity"] for r in rows], dtype=bool),
        anchor_margin_ipr=np.asarray([r["ipr_margin"] for r in anchor["ipr_margin_sensitivity"]], dtype=float),
        anchor_margin_fw_pass=np.asarray([r["fixed_window_pass"] for r in anchor["ipr_margin_sensitivity"]], dtype=bool),
        anchor_lec=np.asarray([r["low_energy_count"] for r in anchor["low_energy_count_sensitivity"]], dtype=int),
        anchor_lec_fw_pass=np.asarray([r["fixed_window_pass"] for r in anchor["low_energy_count_sensitivity"]], dtype=bool),
    )


def _summary_md(cfg: W8DiagnosticConfig, metrics: dict) -> str:
    lines = [
        "# S1 v2 W=8 failure diagnostic (toy S2 x S1)",
        "",
        "Not continuum compactification. Not S6 / S3×S6 / Standard Model. "
        "Not physical chirality. Not Witten/Lichnerowicz bypass.",
        "",
        f"Baseline tag (informational only): `{metrics.get('baseline_tag', '')}`",
        f"Reference stress run: `{metrics.get('reference_stress_run', '')}`",
        "",
        f"Diagnostic classification: `{metrics['classification']['diagnostic_classification']}`",
        "",
        "## Counts",
        f"- primary grid rows: `{metrics['counts']['primary_rows']}`",
        f"- seed sensitivity rows: `{metrics['counts']['seed_rows']}`",
        "",
        "## Classification detail",
        "```json",
        json.dumps(metrics["classification"], indent=2, sort_keys=True),
        "```",
        "",
        "## Anchor (ring, q=-1, s1_size=8, W=8, alpha=0, seed=9836055)",
        "```json",
        json.dumps(metrics["anchor"]["anchor_base_row"], indent=2, sort_keys=True),
        "```",
        "",
        "## IPR margin sensitivity (anchor)",
        "```json",
        json.dumps(metrics["anchor"]["ipr_margin_sensitivity"], indent=2, sort_keys=True),
        "```",
        "",
        "## low_energy_count sensitivity (anchor)",
        "```json",
        json.dumps(metrics["anchor"]["low_energy_count_sensitivity"], indent=2, sort_keys=True),
        "```",
        "",
        "## Low-energy spectrum block",
        "```json",
        json.dumps(metrics["anchor"]["spectrum"], indent=2, sort_keys=True),
        "```",
        "",
        "## Notes",
        "- Gates use the same rule as stress diagnostics: IPR deltas vs `ipr_margin` (default 1e-6).",
        "- Primary grid uses `_benchmark_seed` with `mode_index=geometric_weight` and stress-aligned disorder indices for 8/12/16.",
        "- Seeds 6.0 and 10.0 use appended disorder indices so they do not collide with stress indices.",
        "- Baseline is not promoted; prior stress memos are authoritative for their runs.",
        "",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="W=8 fixed-window v2 failure diagnostic (toy).")
    p.add_argument("--tiny", action="store_true", help="Minimal grid for CI / smoke tests.")
    return p.parse_args()


def build_tiny_config() -> W8DiagnosticConfig:
    return W8DiagnosticConfig(
        families=("ring",),
        q_values=(-1,),
        s1_sizes=(8, 16),
        boundary_twists=(0.0,),
        disorder_sweep=(8.0,),
        seed_sensitivity_span=1,
        ipr_margin_sweep=(1e-6, 1e-5),
        low_energy_count_sweep=(8, 10),
        note="Tiny diagnostic profile for automated tests.",
    )


def make_run_dir() -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base_dir = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base_dir / f"{stamp}_s1_v2_w8_failure_diagnostic"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def main() -> int:
    args = parse_args()
    cfg = build_tiny_config() if args.tiny else W8DiagnosticConfig()

    primary = run_primary_grid(cfg)
    seed_sens = run_seed_sensitivity(cfg)
    anchor = run_anchor_exact_extended(cfg)
    all_rows = primary + seed_sens

    classification = _classify(all_rows, anchor)
    metrics = {
        "baseline_tag": "v0.1.14-mvp-s2-s1-discretization-v2-full",
        "reference_stress_run": "reports/RUNS/20260513-001436_s1_discretization_v2_stress",
        "classification": classification,
        "anchor": anchor,
        "counts": {"primary_rows": len(primary), "seed_rows": len(seed_sens), "total_rows": len(all_rows)},
        "grid_rows": all_rows,
    }

    run_dir = make_run_dir()
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.json").write_text(json.dumps(_build_config_payload(cfg), indent=2, sort_keys=True), encoding="utf-8")
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    _save_npz(rows=all_rows, anchor=anchor, out=run_dir / "data.npz")
    (run_dir / "summary.md").write_text(_summary_md(cfg, metrics), encoding="utf-8")
    (run_dir / "figures" / ".placeholder").write_text("figures optional; not generated in this diagnostic\n", encoding="utf-8")

    print(f"run_path={run_dir}")
    print(f"diagnostic_classification={classification['diagnostic_classification']}")
    print("s1_v2_w8_failure_diagnostic complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
