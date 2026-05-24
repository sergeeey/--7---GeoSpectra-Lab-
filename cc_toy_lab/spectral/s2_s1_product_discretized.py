"""Toy product-discretized S2 x S1 refinement (Kronecker-sum Hamiltonian proxy).

This module is a diagnostic scaffold only. It does not replace ``s2_s1_product``
metrics definitions, does not promote baselines, and does not claim continuum
compactification or physical chirality.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import median
from collections.abc import Callable
from typing import Any, Literal

import numpy as np

from cc_toy_lab.spectral.dirac_monopole_s2 import build_dirac_monopole_operator
from cc_toy_lab.spectral.metrics import mean_adjacent_gap_ratio
from cc_toy_lab.spectral.s1_discretizations import S1_DISCRETIZATION_FAMILIES, build_s1_operator


def _hermitize(matrix: np.ndarray) -> np.ndarray:
    dense = np.asarray(matrix, dtype=complex)
    return 0.5 * (dense + dense.conj().T)


def _select_low_energy_indices(
    abs_eigenvalues: np.ndarray,
    kernel_indices: np.ndarray,
    low_energy_count: int,
) -> np.ndarray:
    if kernel_indices.size:
        return kernel_indices
    count = min(int(low_energy_count), abs_eigenvalues.size)
    return np.argsort(abs_eigenvalues)[:count]


def _select_fixed_window_low_energy_indices(
    abs_eigenvalues: np.ndarray, low_energy_count: int
) -> np.ndarray:
    count = min(int(low_energy_count), abs_eigenvalues.size)
    return np.argsort(abs_eigenvalues)[:count]


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


def _kernel_chirality_content(
    eigenvectors: np.ndarray,
    kernel_indices: np.ndarray,
    lifted_s2_chirality: np.ndarray,
    chirality_tolerance: float,
) -> tuple[int, int, int]:
    if kernel_indices.size == 0:
        return 0, 0, 0
    kernel_vectors = eigenvectors[:, kernel_indices]
    gamma_vectors = lifted_s2_chirality[:, None] * kernel_vectors
    expectations = np.real(np.sum(np.conj(kernel_vectors) * gamma_vectors, axis=0))
    n_plus = int(np.count_nonzero(expectations > chirality_tolerance))
    n_minus = int(np.count_nonzero(expectations < -chirality_tolerance))
    ambiguous = int(kernel_indices.size - n_plus - n_minus)
    return n_plus, n_minus, ambiguous


def _classify_kernel_pattern(q: int, alpha: float, kernel_count: int) -> str:
    if q != 0 and np.isclose(alpha, 0.0) and kernel_count > 0:
        return "inherited_kernel_signal"
    if q == 0 and kernel_count == 0:
        return "q_zero_no_inherited_kernel"
    if not np.isclose(alpha, 0.0) and kernel_count == 0:
        return "lifted_or_no_kernel"
    return "ambiguous"


@dataclass(frozen=True)
class ProductDiscretizedConfig:
    """Grid for the product-discretized refinement (tiny, medium, or full profile)."""

    profile_name: str = "tiny"
    q_values: tuple[int, ...] = (0, 1, -1)
    cutoff: int = 2
    s1_families: tuple[str, ...] = ("spectral_circle", "ring", "wilson_ring")
    s1_sizes: tuple[int, ...] = (8, 16)
    alpha_values: tuple[float, ...] = (0.0, 0.5)
    w_values: tuple[float, ...] = (0.0, 8.0)
    seeds: tuple[int, ...] = (123,)
    radius: float = 1.0
    zero_tolerance: float = 1e-7
    chirality_tolerance: float = 0.5
    reference_low_energy_count: int = 8
    low_energy_count_values: tuple[int, ...] = (4, 6, 8, 10, 12)
    localization_ipr_margin: float = 1e-6
    s1_mode_clean: str = "clean"
    s1_mode_disordered: str = "geometric_weight"
    flux_alpha_probe: float = 0.25
    flux_response_tolerance: float = 1e-10
    spectator_small_s1: int = 8
    spectator_large_s1: int = 16
    spectator_tolerance: float = 1e-10
    hermiticity_tol: float = 1e-9
    note: str = (
        "Toy product-discretized S2 x S1 Kronecker-sum Hamiltonian. Not continuum "
        "compactification. Not a global chiral index headline for the product."
    )


@dataclass
class ProductDiscretizedCaseResult:
    q: int
    cutoff: int
    s1_family: str
    s1_size: int
    alpha: float
    disorder_strength: float
    seed: int
    s2_dimension: int
    total_dimension: int
    hermiticity_max_residual: float
    clean_kernel_count: int
    disordered_kernel_count: int
    clean_min_abs_eigenvalue: float
    disordered_min_abs_eigenvalue: float
    clean_s1_low_energy_ipr: float
    disordered_s1_low_energy_ipr: float
    clean_s1_fixed_window_ipr: float
    disordered_s1_fixed_window_ipr: float
    kernel_only_localization_gate_passed: bool
    fixed_window_localization_gate_passed: bool
    localization_gate_v2_passed: bool
    localization_window_mode: str
    window_selection_sensitivity: bool
    pass_rate_across_windows: float
    window_sensitivity_score: float
    localization_gate_v3_classification: str
    window_robust_localization_passed: bool
    unstable_window_cases: tuple[dict[str, Any], ...]
    ipr_delta_by_window: dict[int, float]
    pass_by_window: dict[int, bool]
    flux_response_observed: bool
    s1_not_spectator: bool
    pbc_apbc_difference: bool
    q0_control_passed: bool
    ring_alpha0_caveat_detected: bool
    clean_kernel_pattern: str
    disordered_kernel_pattern: str
    mean_r_positive_disordered: float


@dataclass
class ProductDiscretizedAssessment:
    config: ProductDiscretizedConfig
    cases: tuple[ProductDiscretizedCaseResult, ...]
    baseline_tag: str
    operator_family: str
    hermiticity_all_passed: bool
    shape_all_passed: bool
    reproducibility_passed: bool
    q0_controls_all_passed: bool
    classification: str
    notes: tuple[str, ...] = field(default_factory=tuple)


def build_product_discretized_config(
    *,
    tiny: bool = False,
    medium: bool = False,
    full: bool = False,
    seed: int = 123,
) -> ProductDiscretizedConfig:
    n = int(tiny) + int(medium) + int(full)
    if n != 1:
        raise ValueError("specify exactly one of tiny=True, medium=True, or full=True")
    if tiny:
        return ProductDiscretizedConfig(profile_name="tiny", seeds=(int(seed),))
    if medium:
        return ProductDiscretizedConfig(
            profile_name="medium",
            q_values=(0, 1, -1, 2, -2),
            s1_sizes=(8, 16, 24),
            alpha_values=(0.0, 0.25, 0.5),
            w_values=(0.0, 4.0, 8.0, 12.0),
            seeds=(123, 456),
            spectator_large_s1=24,
        )
    return ProductDiscretizedConfig(
        profile_name="full",
        q_values=(0, 1, -1, 2, -2, 3, -3),
        s1_sizes=(8, 16, 24, 32, 48),
        alpha_values=(0.0, 0.25, 0.5),
        w_values=(0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0),
        seeds=(123, 456, 789),
        low_energy_count_values=(4, 6, 8, 10, 12),
        spectator_large_s1=48,
    )


def estimate_product_discretized_case_count(cfg: ProductDiscretizedConfig) -> int:
    """Cartesian grid size: seeds x q x family x s1_size x alpha x W."""
    return (
        len(cfg.seeds)
        * len(cfg.q_values)
        * len(cfg.s1_families)
        * len(cfg.s1_sizes)
        * len(cfg.alpha_values)
        * len(cfg.w_values)
    )


def medium_profile_dry_run_report(cfg: ProductDiscretizedConfig) -> dict[str, Any]:
    """No operator work; for CLI ``--medium --dry-run`` and tests."""
    if cfg.profile_name != "medium":
        raise ValueError("medium_profile_dry_run_report requires a medium ProductDiscretizedConfig")
    return {
        "expected_case_count": int(estimate_product_discretized_case_count(cfg)),
        "grid_dimensions": {
            "seeds": len(cfg.seeds),
            "q_values": len(cfg.q_values),
            "s1_families": len(cfg.s1_families),
            "s1_sizes": len(cfg.s1_sizes),
            "alpha_values": len(cfg.alpha_values),
            "w_values": len(cfg.w_values),
        },
        "estimated_run_dir_suffix": "_s2_s1_product_discretized_medium",
        "baseline_informational": "v0.1.14-mvp-s2-s1-discretization-v2-full (unchanged; not a promotion)",
    }


def full_profile_dry_run_report(cfg: ProductDiscretizedConfig) -> dict[str, Any]:
    """No operator work; for CLI ``--full --dry-run`` and tests only."""
    if cfg.profile_name != "full":
        raise ValueError("full_profile_dry_run_report requires a full ProductDiscretizedConfig")
    return {
        "profile_name": "full",
        "expected_case_count": int(estimate_product_discretized_case_count(cfg)),
        "grid_dimensions": {
            "seeds": len(cfg.seeds),
            "q_values": len(cfg.q_values),
            "s1_families": len(cfg.s1_families),
            "s1_sizes": len(cfg.s1_sizes),
            "alpha_values": len(cfg.alpha_values),
            "w_values": len(cfg.w_values),
            "low_energy_count_values": len(cfg.low_energy_count_values),
        },
        "estimated_run_dir_suffix": "_s2_s1_product_discretized_full",
        "baseline_informational": "v0.1.14-mvp-s2-s1-discretization-v2-full (unchanged; not a promotion)",
    }


def _v3_failure_bucket_key(c: ProductDiscretizedCaseResult) -> str:
    return (
        f"family={c.s1_family}|W={c.disorder_strength}|alpha={c.alpha}|"
        f"s1_size={c.s1_size}|q={c.q}|seed={c.seed}"
    )


def _extended_product_discretized_aggregates(
    cases: tuple[ProductDiscretizedCaseResult, ...],
) -> dict[str, Any]:
    """Medium-style aggregates; safe for tiny runs (same schema)."""
    v3_fail_by_bucket: dict[str, int] = {}
    v2_v3_disagree = 0
    ring_a0_cases = 0
    ring_a0_fail = 0
    q0_fp = 0
    for c in cases:
        if c.localization_gate_v2_passed != c.window_robust_localization_passed:
            v2_v3_disagree += 1
        if not c.window_robust_localization_passed:
            k = _v3_failure_bucket_key(c)
            v3_fail_by_bucket[k] = v3_fail_by_bucket.get(k, 0) + 1
        if c.s1_family == "ring" and np.isclose(c.alpha, 0.0) and c.disorder_strength > 0.0:
            ring_a0_cases += 1
            if not (
                c.kernel_only_localization_gate_passed
                and c.fixed_window_localization_gate_passed
                and c.window_robust_localization_passed
            ):
                ring_a0_fail += 1
        if c.q == 0 and c.disorder_strength > 0.0 and not c.q0_control_passed:
            q0_fp += 1
    return {
        "v3_failure_counts_by_bucket": dict(sorted(v3_fail_by_bucket.items())),
        "v2_vs_v3_disagreement_count": int(v2_v3_disagree),
        "ring_alpha0_cases_count": int(ring_a0_cases),
        "ring_alpha0_failure_count": int(ring_a0_fail),
        "q0_false_positive_count": int(q0_fp),
    }


def build_s2_proxy_hermitian(*, q: int, cutoff: int, radius: float) -> np.ndarray:
    d_s2, _chi = build_dirac_monopole_operator(q=int(q), cutoff=int(cutoff), radius=float(radius))
    d = np.asarray(d_s2, dtype=float)
    return d @ d


def build_product_discretized_operator(
    *,
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float,
    s1_family: str,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    if s1_family not in S1_DISCRETIZATION_FAMILIES:
        raise ValueError(f"unknown S1 family: {s1_family}")
    d_s2, chi_s2 = build_dirac_monopole_operator(q=int(q), cutoff=int(cutoff), radius=float(radius))
    d = np.asarray(d_s2, dtype=float)
    h_s2 = d @ d
    p_s1 = build_s1_operator(
        size=int(s1_size),
        alpha=float(alpha),
        family=str(s1_family),
        mode=str(mode),
        disorder_strength=float(disorder_strength),
        seed=seed,
        radius=float(radius),
    )
    p_s1 = np.asarray(p_s1, dtype=complex)
    s2_dim = int(h_s2.shape[0])
    eye_s2 = np.eye(s2_dim, dtype=complex)
    eye_s1 = np.eye(int(s1_size), dtype=complex)
    h_total = np.kron(np.asarray(h_s2, dtype=complex), eye_s1) + np.kron(eye_s2, p_s1)
    h_total = _hermitize(h_total)
    lifted = np.kron(np.asarray(chi_s2, dtype=float), np.ones(int(s1_size), dtype=float))
    meta: dict[str, Any] = {
        "q": int(q),
        "cutoff": int(cutoff),
        "s1_family": str(s1_family),
        "s1_size": int(s1_size),
        "alpha": float(alpha),
        "mode": str(mode),
        "disorder_strength": float(disorder_strength),
        "seed": None if seed is None else int(seed),
        "radius": float(radius),
        "s2_dimension": s2_dim,
        "total_dimension": int(h_total.shape[0]),
        "operator_schema": "H = kron(D_S2^2, I) + kron(I, P_S1)",
    }
    return h_total, lifted, meta


def _single_spectrum_observation(
    *,
    operator: np.ndarray,
    lifted_s2_chirality: np.ndarray,
    s2_dimension: int,
    s1_size: int,
    zero_tolerance: float,
    low_energy_count: int,
    chirality_tolerance: float,
    q: int,
    alpha: float,
) -> dict[str, Any]:
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    abs_ev = np.abs(eigenvalues)
    kernel_idx = np.flatnonzero(abs_ev <= zero_tolerance)
    kc = int(kernel_idx.size)
    min_abs = float(np.min(abs_ev)) if abs_ev.size else float("nan")
    pos = eigenvalues[eigenvalues > zero_tolerance]
    mean_r = float(mean_adjacent_gap_ratio(pos)) if pos.size >= 2 else float("nan")
    low_idx = _select_low_energy_indices(abs_ev, kernel_idx, low_energy_count)
    fix_idx = _select_fixed_window_low_energy_indices(abs_ev, low_energy_count)
    ipr_low = _mean_s1_marginal_ipr(eigenvectors, low_idx, s2_dimension, s1_size)
    ipr_fix = _mean_s1_marginal_ipr(eigenvectors, fix_idx, s2_dimension, s1_size)
    n_plus, n_minus, amb = _kernel_chirality_content(
        eigenvectors, kernel_idx, lifted_s2_chirality, chirality_tolerance
    )
    return {
        "kernel_count": kc,
        "min_abs_eigenvalue": min_abs,
        "s1_low_energy_ipr": float(ipr_low),
        "s1_fixed_window_ipr": float(ipr_fix),
        "mean_r_positive": mean_r,
        "s2_n_plus_in_kernel": n_plus,
        "s2_n_minus_in_kernel": n_minus,
        "ambiguous_kernel_states": amb,
        "kernel_pattern": _classify_kernel_pattern(q, alpha, kc),
    }


def _low_energy_signature_product(
    *,
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float,
    s1_family: str,
    zero_tolerance: float,
    low_energy_count: int,
) -> np.ndarray:
    op, lifted, meta = build_product_discretized_operator(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        s1_family=s1_family,
    )
    obs = _single_spectrum_observation(
        operator=op,
        lifted_s2_chirality=lifted,
        s2_dimension=int(meta["s2_dimension"]),
        s1_size=int(meta["s1_size"]),
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        chirality_tolerance=0.5,
        q=q,
        alpha=alpha,
    )
    return np.asarray(
        [obs["min_abs_eigenvalue"], obs["s1_low_energy_ipr"], obs["s1_fixed_window_ipr"]],
        dtype=float,
    )


def _compare_localization_gate_v3_product(
    *,
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    seed: int | None,
    radius: float,
    disordered_strength: float,
    ipr_margin: float,
    s1_family: str,
    low_energy_count_values: tuple[int, ...],
    reference_low_energy_count: int,
    zero_tolerance: float,
    chirality_tolerance: float,
) -> dict[str, Any]:
    if reference_low_energy_count not in low_energy_count_values:
        raise ValueError("reference_low_energy_count must be in low_energy_count_values")
    ipr_delta_by_window: dict[int, float] = {}
    pass_by_window: dict[int, bool] = {}
    clean_by_k: dict[int, dict[str, Any]] = {}
    dis_by_k: dict[int, dict[str, Any]] = {}

    for k in low_energy_count_values:
        kk = int(k)
        op_c, lift_c, meta_c = build_product_discretized_operator(
            q=q,
            cutoff=cutoff,
            s1_size=s1_size,
            alpha=alpha,
            mode="clean",
            disorder_strength=0.0,
            seed=seed,
            radius=radius,
            s1_family=s1_family,
        )
        clean = _single_spectrum_observation(
            operator=op_c,
            lifted_s2_chirality=lift_c,
            s2_dimension=int(meta_c["s2_dimension"]),
            s1_size=int(meta_c["s1_size"]),
            zero_tolerance=zero_tolerance,
            low_energy_count=kk,
            chirality_tolerance=chirality_tolerance,
            q=q,
            alpha=alpha,
        )
        op_d, lift_d, meta_d = build_product_discretized_operator(
            q=q,
            cutoff=cutoff,
            s1_size=s1_size,
            alpha=alpha,
            mode="geometric_weight",
            disorder_strength=disordered_strength,
            seed=seed,
            radius=radius,
            s1_family=s1_family,
        )
        disordered = _single_spectrum_observation(
            operator=op_d,
            lifted_s2_chirality=lift_d,
            s2_dimension=int(meta_d["s2_dimension"]),
            s1_size=int(meta_d["s1_size"]),
            zero_tolerance=zero_tolerance,
            low_energy_count=kk,
            chirality_tolerance=chirality_tolerance,
            q=q,
            alpha=alpha,
        )
        delta = float(disordered["s1_fixed_window_ipr"] - clean["s1_fixed_window_ipr"])
        ipr_delta_by_window[kk] = delta
        pass_by_window[kk] = bool(delta > ipr_margin)
        clean_by_k[kk] = clean
        dis_by_k[kk] = disordered

    n_win = len(low_energy_count_values)
    p_pass = int(sum(1 for v in pass_by_window.values() if v))
    pass_rate = float(p_pass) / float(n_win)
    deltas = [ipr_delta_by_window[int(k)] for k in low_energy_count_values]
    median_delta = float(median(deltas))
    min_delta = float(min(deltas))
    window_sensitivity_score = float(1.0 - pass_rate)

    ref_k = int(reference_low_energy_count)
    clean_ref = clean_by_k[ref_k]
    dis_ref = dis_by_k[ref_k]
    kernel_only_localization_gate_passed = bool(
        dis_ref["s1_low_energy_ipr"] > clean_ref["s1_low_energy_ipr"] + ipr_margin
    )
    fixed_window_localization_gate_passed = bool(
        dis_ref["s1_fixed_window_ipr"] > clean_ref["s1_fixed_window_ipr"] + ipr_margin
    )
    unstable: list[dict[str, Any]] = []
    for kk in low_energy_count_values:
        k_int = int(kk)
        if not pass_by_window[k_int]:
            unstable.append(
                {
                    "low_energy_count": k_int,
                    "ipr_delta": float(ipr_delta_by_window[k_int]),
                    "passed": False,
                }
            )

    if p_pass < 2:
        classification = "fail"
    elif p_pass >= 4 and median_delta > ipr_margin:
        classification = "window_robust_pass"
    elif 2 <= p_pass <= 3:
        classification = "fragile_pass"
    elif p_pass >= 4 and median_delta <= ipr_margin:
        classification = "window_sensitive"
    else:
        classification = "window_sensitive"

    window_robust_localization_passed = bool(classification == "window_robust_pass")

    return {
        "low_energy_count_values": tuple(int(x) for x in low_energy_count_values),
        "ipr_delta_by_window": {
            int(k): float(ipr_delta_by_window[int(k)]) for k in low_energy_count_values
        },
        "pass_by_window": {int(k): bool(pass_by_window[int(k)]) for k in low_energy_count_values},
        "pass_rate_across_windows": pass_rate,
        "min_ipr_delta": min_delta,
        "median_ipr_delta": median_delta,
        "window_sensitivity_score": window_sensitivity_score,
        "window_robust_localization_passed": window_robust_localization_passed,
        "unstable_window_cases": unstable,
        "kernel_only_localization_gate_passed": kernel_only_localization_gate_passed,
        "fixed_window_localization_gate_passed": fixed_window_localization_gate_passed,
        "localization_gate_v2_passed": bool(fixed_window_localization_gate_passed),
        "classification": classification,
        "clean_observation_ref": clean_ref,
        "disordered_observation_ref": dis_ref,
    }


def analyze_product_discretized_case(
    *,
    cfg: ProductDiscretizedConfig,
    q: int,
    s1_family: str,
    s1_size: int,
    alpha: float,
    disorder_strength: float,
    seed: int,
) -> ProductDiscretizedCaseResult:
    op, lifted, meta = build_product_discretized_operator(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode=cfg.s1_mode_clean,
        disorder_strength=0.0,
        seed=seed,
        radius=cfg.radius,
        s1_family=s1_family,
    )
    op_d, lifted_d, meta_d = build_product_discretized_operator(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode=cfg.s1_mode_disordered,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=cfg.radius,
        s1_family=s1_family,
    )
    res = max(
        float(np.max(np.abs(op - op.conj().T))),
        float(np.max(np.abs(op_d - op_d.conj().T))),
    )
    s2d = int(meta["s2_dimension"])
    clean = _single_spectrum_observation(
        operator=op,
        lifted_s2_chirality=lifted,
        s2_dimension=s2d,
        s1_size=s1_size,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.reference_low_energy_count,
        chirality_tolerance=cfg.chirality_tolerance,
        q=q,
        alpha=alpha,
    )
    disordered = _single_spectrum_observation(
        operator=op_d,
        lifted_s2_chirality=lifted_d,
        s2_dimension=s2d,
        s1_size=s1_size,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.reference_low_energy_count,
        chirality_tolerance=cfg.chirality_tolerance,
        q=q,
        alpha=alpha,
    )
    v3 = _compare_localization_gate_v3_product(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=alpha,
        seed=seed,
        radius=cfg.radius,
        disordered_strength=disorder_strength,
        ipr_margin=cfg.localization_ipr_margin,
        s1_family=s1_family,
        low_energy_count_values=cfg.low_energy_count_values,
        reference_low_energy_count=cfg.reference_low_energy_count,
        zero_tolerance=cfg.zero_tolerance,
        chirality_tolerance=cfg.chirality_tolerance,
    )
    ref_sig = _low_energy_signature_product(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode=cfg.s1_mode_clean,
        disorder_strength=0.0,
        seed=seed,
        radius=cfg.radius,
        s1_family=s1_family,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.reference_low_energy_count,
    )
    probe_sig = _low_energy_signature_product(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=cfg.flux_alpha_probe,
        mode=cfg.s1_mode_disordered,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=cfg.radius,
        s1_family=s1_family,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.reference_low_energy_count,
    )
    flux_delta = float(np.linalg.norm(ref_sig - probe_sig))
    flux_response_observed = bool(flux_delta > cfg.flux_response_tolerance)

    small_sig = _low_energy_signature_product(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=cfg.spectator_small_s1,
        alpha=alpha,
        mode=cfg.s1_mode_disordered,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=cfg.radius,
        s1_family=s1_family,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.reference_low_energy_count,
    )
    large_sig = _low_energy_signature_product(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=cfg.spectator_large_s1,
        alpha=alpha,
        mode=cfg.s1_mode_disordered,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=cfg.radius,
        s1_family=s1_family,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.reference_low_energy_count,
    )
    s1_not_spectator = bool(float(np.linalg.norm(small_sig - large_sig)) > cfg.spectator_tolerance)

    op_pb, lift_pb, _ = build_product_discretized_operator(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=0.0,
        mode=cfg.s1_mode_disordered,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=cfg.radius,
        s1_family=s1_family,
    )
    pbc_c = _single_spectrum_observation(
        operator=op_pb,
        lifted_s2_chirality=lift_pb,
        s2_dimension=s2d,
        s1_size=s1_size,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.reference_low_energy_count,
        chirality_tolerance=cfg.chirality_tolerance,
        q=q,
        alpha=0.0,
    )
    op_ap, lift_ap, _ = build_product_discretized_operator(
        q=q,
        cutoff=cfg.cutoff,
        s1_size=s1_size,
        alpha=0.5,
        mode=cfg.s1_mode_disordered,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=cfg.radius,
        s1_family=s1_family,
    )
    apbc_c = _single_spectrum_observation(
        operator=op_ap,
        lifted_s2_chirality=lift_ap,
        s2_dimension=s2d,
        s1_size=s1_size,
        zero_tolerance=cfg.zero_tolerance,
        low_energy_count=cfg.reference_low_energy_count,
        chirality_tolerance=cfg.chirality_tolerance,
        q=q,
        alpha=0.5,
    )
    pbc_apbc_difference = bool(
        pbc_c["kernel_count"] != apbc_c["kernel_count"]
        or abs(pbc_c["min_abs_eigenvalue"] - apbc_c["min_abs_eigenvalue"])
        > cfg.flux_response_tolerance
    )

    # W=0: geometric_weight collapses to clean in build_s1_operator — no disordered
    # mixture; do not apply the "no spurious q=0 disordered kernel" rule here.
    if float(disorder_strength) <= 0.0:
        q0_control_passed = True
    else:
        q0_control_passed = bool(not (q == 0 and disordered["kernel_count"] > 0))
    ring_alpha0_caveat_detected = bool(
        s1_family == "ring" and np.isclose(alpha, 0.0) and disorder_strength > 0.0
    )

    kernel_only_pass = bool(v3["kernel_only_localization_gate_passed"])
    fixed_pass = bool(v3["fixed_window_localization_gate_passed"])
    window_sel = bool(kernel_only_pass != fixed_pass)

    return ProductDiscretizedCaseResult(
        q=int(q),
        cutoff=int(cfg.cutoff),
        s1_family=str(s1_family),
        s1_size=int(s1_size),
        alpha=float(alpha),
        disorder_strength=float(disorder_strength),
        seed=int(seed),
        s2_dimension=s2d,
        total_dimension=int(meta["total_dimension"]),
        hermiticity_max_residual=float(res),
        clean_kernel_count=int(clean["kernel_count"]),
        disordered_kernel_count=int(disordered["kernel_count"]),
        clean_min_abs_eigenvalue=float(clean["min_abs_eigenvalue"]),
        disordered_min_abs_eigenvalue=float(disordered["min_abs_eigenvalue"]),
        clean_s1_low_energy_ipr=float(clean["s1_low_energy_ipr"]),
        disordered_s1_low_energy_ipr=float(disordered["s1_low_energy_ipr"]),
        clean_s1_fixed_window_ipr=float(clean["s1_fixed_window_ipr"]),
        disordered_s1_fixed_window_ipr=float(disordered["s1_fixed_window_ipr"]),
        kernel_only_localization_gate_passed=kernel_only_pass,
        fixed_window_localization_gate_passed=fixed_pass,
        localization_gate_v2_passed=bool(v3["localization_gate_v2_passed"]),
        localization_window_mode="fixed_low_energy_window",
        window_selection_sensitivity=window_sel,
        pass_rate_across_windows=float(v3["pass_rate_across_windows"]),
        window_sensitivity_score=float(v3["window_sensitivity_score"]),
        localization_gate_v3_classification=str(v3["classification"]),
        window_robust_localization_passed=bool(v3["window_robust_localization_passed"]),
        unstable_window_cases=tuple(v3["unstable_window_cases"]),
        ipr_delta_by_window={int(k): float(v) for k, v in v3["ipr_delta_by_window"].items()},
        pass_by_window={int(k): bool(v) for k, v in v3["pass_by_window"].items()},
        flux_response_observed=flux_response_observed,
        s1_not_spectator=s1_not_spectator,
        pbc_apbc_difference=pbc_apbc_difference,
        q0_control_passed=q0_control_passed,
        ring_alpha0_caveat_detected=ring_alpha0_caveat_detected,
        clean_kernel_pattern=str(clean["kernel_pattern"]),
        disordered_kernel_pattern=str(disordered["kernel_pattern"]),
        mean_r_positive_disordered=float(disordered["mean_r_positive"]),
    )


def _case_to_public_dict(c: ProductDiscretizedCaseResult) -> dict[str, Any]:
    d = asdict(c)
    d["unstable_window_cases"] = list(c.unstable_window_cases)
    return d


def serialize_product_discretized_case(c: ProductDiscretizedCaseResult) -> dict[str, Any]:
    """JSON-friendly dict for progress logs / partial JSONL (same shape as metrics per-case rows)."""
    return _case_to_public_dict(c)


ProductDiscretizedCaseProgressHook = Callable[
    [Literal["primary", "repro"], int, ProductDiscretizedCaseResult],
    None,
]


def _run_product_discretized_grid(
    cfg: ProductDiscretizedConfig,
    *,
    after_each_case: ProductDiscretizedCaseProgressHook | None = None,
) -> ProductDiscretizedAssessment:
    expected = estimate_product_discretized_case_count(cfg)
    cases: list[ProductDiscretizedCaseResult] = []
    idx = 0
    for seed in cfg.seeds:
        for q in cfg.q_values:
            for fam in cfg.s1_families:
                for n1 in cfg.s1_sizes:
                    for alpha in cfg.alpha_values:
                        for w in cfg.w_values:
                            c = analyze_product_discretized_case(
                                cfg=cfg,
                                q=int(q),
                                s1_family=str(fam),
                                s1_size=int(n1),
                                alpha=float(alpha),
                                disorder_strength=float(w),
                                seed=int(seed),
                            )
                            cases.append(c)
                            if after_each_case is not None:
                                after_each_case("primary", idx, c)
                            idx += 1
    if len(cases) != expected:
        raise RuntimeError(
            f"case grid mismatch: got {len(cases)}, expected {expected} for profile {cfg.profile_name!r}"
        )

    herm = all(c.hermiticity_max_residual <= cfg.hermiticity_tol for c in cases)
    shapes = all(c.total_dimension == c.s2_dimension * c.s1_size for c in cases)
    q0_ok = all(c.q0_control_passed for c in cases if c.q == 0)

    dup_cases: list[ProductDiscretizedCaseResult] = []
    jdx = 0
    for seed in cfg.seeds:
        for q in cfg.q_values:
            for fam in cfg.s1_families:
                for n1 in cfg.s1_sizes:
                    for alpha in cfg.alpha_values:
                        for w in cfg.w_values:
                            c2 = analyze_product_discretized_case(
                                cfg=cfg,
                                q=int(q),
                                s1_family=str(fam),
                                s1_size=int(n1),
                                alpha=float(alpha),
                                disorder_strength=float(w),
                                seed=int(seed),
                            )
                            dup_cases.append(c2)
                            if after_each_case is not None:
                                after_each_case("repro", jdx, c2)
                            jdx += 1
    repro = all(
        abs(a.disordered_min_abs_eigenvalue - b.disordered_min_abs_eigenvalue) < 1e-12
        and a.disordered_kernel_count == b.disordered_kernel_count
        for a, b in zip(cases, dup_cases)
    )

    notes = (
        "Product-discretized Kronecker-sum Hamiltonian; coupling_terms default off.",
        "No global chiral index headline; kernel metrics are toy diagnostics only.",
    )
    if cfg.profile_name == "tiny":
        classification = "tiny_product_discretized_diagnostic_complete"
    elif cfg.profile_name == "medium":
        classification = "product_discretized_medium_diagnostic_complete"
    elif cfg.profile_name == "full":
        classification = "product_discretized_full_diagnostic_complete"
    else:
        raise ValueError(f"unknown profile_name: {cfg.profile_name!r}")
    return ProductDiscretizedAssessment(
        config=cfg,
        cases=tuple(cases),
        baseline_tag="v0.1.14-mvp-s2-s1-discretization-v2-full",
        operator_family="product_discretized_kronecker_sum_D2_plus_P1",
        hermiticity_all_passed=bool(herm),
        shape_all_passed=bool(shapes),
        reproducibility_passed=bool(repro),
        q0_controls_all_passed=bool(q0_ok),
        classification=classification,
        notes=notes,
    )


def run_product_discretized_tiny(cfg: ProductDiscretizedConfig) -> ProductDiscretizedAssessment:
    if cfg.profile_name != "tiny":
        raise ValueError("run_product_discretized_tiny requires profile_name='tiny'")
    return _run_product_discretized_grid(cfg)


def run_product_discretized_medium(cfg: ProductDiscretizedConfig) -> ProductDiscretizedAssessment:
    if cfg.profile_name != "medium":
        raise ValueError("run_product_discretized_medium requires profile_name='medium'")
    return _run_product_discretized_grid(cfg)


def run_product_discretized_full(
    cfg: ProductDiscretizedConfig,
    *,
    after_each_case: ProductDiscretizedCaseProgressHook | None = None,
) -> ProductDiscretizedAssessment:
    """Run the full product-discretized grid (6615 outer cases). Expensive: call only with explicit CLI guard."""
    if cfg.profile_name != "full":
        raise ValueError("run_product_discretized_full requires profile_name='full'")
    n = estimate_product_discretized_case_count(cfg)
    if n != 6615:
        raise ValueError(f"full profile must have expected_case_count=6615, got {n}")
    return _run_product_discretized_grid(cfg, after_each_case=after_each_case)


def assess_product_discretized_results(assessment: ProductDiscretizedAssessment) -> dict[str, Any]:
    cases = assessment.cases
    clean_n = sum(1 for c in cases if float(c.disorder_strength) == 0.0)
    dis_n = sum(1 for c in cases if float(c.disorder_strength) > 0.0)
    has_clean = clean_n > 0
    has_dis = dis_n > 0
    extended = _extended_product_discretized_aggregates(cases)
    return {
        "baseline_tag": assessment.baseline_tag,
        "operator_family": assessment.operator_family,
        "profile_name": assessment.config.profile_name,
        "case_count": len(cases),
        "clean_control_cases_count": int(clean_n),
        "disordered_cases_count": int(dis_n),
        "has_clean_control": bool(has_clean),
        "has_disordered_control": bool(has_dis),
        "disorder_contrast_available": bool(has_clean and has_dis),
        **extended,
        "hermiticity_all_passed": assessment.hermiticity_all_passed,
        "shape_all_passed": assessment.shape_all_passed,
        "reproducibility_passed": assessment.reproducibility_passed,
        "q0_controls_all_passed": assessment.q0_controls_all_passed,
        "classification": assessment.classification,
        "notes": list(assessment.notes),
        "cases": [_case_to_public_dict(c) for c in cases],
    }


def save_product_discretized_artifacts(
    assessment: ProductDiscretizedAssessment,
    run_dir: Path,
) -> dict[str, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    cfg_payload = asdict(assessment.config)
    (run_dir / "config.json").write_text(
        json.dumps(cfg_payload, indent=2, sort_keys=True), encoding="utf-8"
    )
    metrics = assess_product_discretized_results(assessment)
    (run_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8"
    )
    cases = assessment.cases
    np.savez_compressed(
        run_dir / "data.npz",
        q=np.asarray([c.q for c in cases], dtype=int),
        s1_family=np.asarray([c.s1_family for c in cases], dtype=str),
        s1_size=np.asarray([c.s1_size for c in cases], dtype=int),
        alpha=np.asarray([c.alpha for c in cases], dtype=float),
        disorder=np.asarray([c.disorder_strength for c in cases], dtype=float),
        seed=np.asarray([c.seed for c in cases], dtype=int),
        v3_class=np.asarray([c.localization_gate_v3_classification for c in cases], dtype=str),
        v3_robust=np.asarray([c.window_robust_localization_passed for c in cases], dtype=bool),
    )
    summary = _build_summary_markdown(assessment, metrics)
    (run_dir / "summary.md").write_text(summary, encoding="utf-8")
    (run_dir / "figures" / ".placeholder").write_text(
        "figures not generated for product-discretized diagnostic scaffold\n", encoding="utf-8"
    )
    return {
        "run_dir": run_dir,
        "config": run_dir / "config.json",
        "metrics": run_dir / "metrics.json",
        "data": run_dir / "data.npz",
        "summary": run_dir / "summary.md",
    }


def _build_summary_markdown(
    assessment: ProductDiscretizedAssessment, metrics: dict[str, Any]
) -> str:
    profile = assessment.config.profile_name
    if profile == "tiny":
        title = "# Product-discretized S2 x S1 — tiny diagnostic"
    elif profile == "medium":
        title = "# Product-discretized S2 x S1 — medium diagnostic"
    elif profile == "full":
        title = "# Product-discretized S2 x S1 — full diagnostic"
    else:
        title = f"# Product-discretized S2 x S1 — {profile} diagnostic"
    lines = [
        title,
        "",
        "**Scientific non-claims:** this does not prove continuum compactification; "
        "does not validate `S6` or `S3 x S6`; does not derive the Standard Model; "
        "does not prove physical chirality; does not bypass Witten/Lichnerowicz.",
        "",
        f"**Baseline (informational):** `{assessment.baseline_tag}`",
        f"**Operator family:** `{assessment.operator_family}`",
        f"**Profile:** `{profile}`",
        "",
        "## Gate summary",
        "",
        f"- clean_control_cases_count: `{metrics['clean_control_cases_count']}`",
        f"- disordered_cases_count: `{metrics['disordered_cases_count']}`",
        f"- has_clean_control: `{metrics['has_clean_control']}`",
        f"- has_disordered_control: `{metrics['has_disordered_control']}`",
        f"- disorder_contrast_available: `{metrics['disorder_contrast_available']}`",
        f"- v2_vs_v3_disagreement_count: `{metrics['v2_vs_v3_disagreement_count']}`",
        f"- ring_alpha0_cases_count: `{metrics['ring_alpha0_cases_count']}`",
        f"- ring_alpha0_failure_count: `{metrics['ring_alpha0_failure_count']}`",
        f"- q0_false_positive_count: `{metrics['q0_false_positive_count']}`",
        f"- hermiticity_all_passed: `{metrics['hermiticity_all_passed']}`",
        f"- shape_all_passed: `{metrics['shape_all_passed']}`",
        f"- reproducibility_passed: `{metrics['reproducibility_passed']}`",
        f"- q0_controls_all_passed: `{metrics['q0_controls_all_passed']}`",
        f"- classification: `{metrics['classification']}`",
        "",
        "## Extended aggregates",
        "",
        "See `metrics.json` keys `v3_failure_counts_by_bucket` (v3 non-robust cases by grid bucket), "
        "and per-case localization fields below.",
        "",
        "## Metrics JSON",
        "",
        "See `metrics.json` for per-case `kernel_only_localization_gate_passed`, "
        "`fixed_window_localization_gate_passed`, `pass_rate_across_windows`, "
        "`window_sensitivity_score`, `localization_gate_v3_classification`, "
        "`window_robust_localization_passed`, `flux_response_observed`, "
        "`s1_not_spectator`, `pbc_apbc_difference`, `q0_control_passed`, "
        "`ring_alpha0_caveat_detected`.",
        "",
    ]
    return "\n".join(lines) + "\n"
