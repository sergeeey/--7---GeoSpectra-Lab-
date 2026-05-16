from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median

import numpy as np

from cc_toy_lab.spectral.dirac_monopole_s2 import build_dirac_monopole_operator
from cc_toy_lab.spectral.metrics import mean_adjacent_gap_ratio
from cc_toy_lab.spectral.s1_discretizations import (
    S1_DISCRETIZATION_FAMILIES,
    S1_INHOMOGENEITY_MODES,
    build_s1_operator,
)

DEFAULT_S1_FAMILY = "spectral_circle"
S1_SPECTRAL_MODES = S1_INHOMOGENEITY_MODES


@dataclass(frozen=True)
class S2S1ProductConfig:
    """Configuration shell for the toy S2 x S1 spectral-circle product."""

    q_values: tuple[int, ...] = (0, 1, -1)
    cutoff: int = 2
    s1_sizes: tuple[int, ...] = (8, 16)
    boundary_twists: tuple[float, ...] = (0.0, 0.5)
    s1_family: str = DEFAULT_S1_FAMILY
    s1_modes: tuple[str, ...] = S1_SPECTRAL_MODES
    disorder_values: tuple[float, ...] = (0.0, 2.0, 8.0)
    perturbation_values: tuple[float, ...] = (0.0, 1e-5)
    realizations: int = 3
    seed: int = 12051
    s1_radius: float = 1.0
    zero_tolerance: float = 1e-7
    zero_tolerance_scan: tuple[float, ...] = (1e-8, 1e-7, 1e-6)
    chirality_threshold: float = 0.5
    low_energy_count: int = 8
    localization_gate_v3_enabled: bool = False
    localization_gate_v3_low_energy_count_values: tuple[int, ...] = (4, 6, 8, 10, 12)
    localization_ipr_margin: float = 1e-6
    note: str = (
        "Toy S2 x S1 spectral-circle product. This module constructs the operator "
        "core only and does not claim continuum compactification or a full-product "
        "chiral theorem."
    )


@dataclass(frozen=True)
class S2S1Observation:
    """Observation-level metrics for one toy S2 x S1 product run-point."""

    q: int
    cutoff: int
    s1_size: int
    alpha: float
    mode: str
    disorder_strength: float
    seed: int | None
    perturbation: float
    zero_tolerance: float
    kernel_count: int
    s2_n_plus_in_kernel: int
    s2_n_minus_in_kernel: int
    ambiguous_kernel_states: int
    min_abs_eigenvalue: float
    max_kernel_abs_eigenvalue: float
    mean_r_positive: float
    s1_low_energy_ipr: float
    s1_fixed_window_ipr: float
    classification: str
    s1_family: str = DEFAULT_S1_FAMILY


@dataclass(frozen=True)
class S2S1Assessment:
    """Benchmark-level diagnostic assessment for the toy S2 x S1 product."""

    config: S2S1ProductConfig
    observations: tuple[S2S1Observation, ...]
    total_observations: int
    q_control_passed: bool
    pbc_gate_passed: bool
    apbc_gate_passed: bool
    flux_response_observed: bool
    s1_not_spectator: bool
    localization_gate_passed: bool
    kernel_only_localization_gate_passed: bool
    fixed_window_localization_gate_passed: bool
    localization_gate_v2_passed: bool
    localization_window_mode: str
    threshold_stable: bool
    all_basic_gates_passed: bool
    classification: str
    notes: tuple[str, ...]
    localization_gate_v3_classification: str | None = None
    pass_rate_across_windows: float | None = None
    window_sensitivity_score: float | None = None
    window_robust_localization_passed: bool | None = None
    unstable_window_cases: tuple[dict[str, object], ...] | None = None
    v2_vs_v3_disagreement: bool | None = None


def build_s1_spectral_operator(
    size: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float = 1.0,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> np.ndarray:
    """Build a dense Hermitian toy spectral operator for the S1 factor.

    The clean operator is constructed in Fourier space with twisted momenta
    `k_m = (m + alpha) / radius`, then transformed back to the position basis.
    The disordered modes are toy Hermitian deformations of that circle operator.
    """
    if s1_family not in S1_DISCRETIZATION_FAMILIES:
        raise ValueError(f"unknown S1 discretization family: {s1_family}")
    return build_s1_operator(
        size=size,
        alpha=alpha,
        family=s1_family,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
    )


def build_s2_s1_product_operator(
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float = 1.0,
    perturbation: float = 0.0,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """Build the toy S2 x S1 product operator core.

    This function assembles

    `D_total = D_S2(q) ⊗ I_S1 + Gamma_S2 ⊗ P_S1(alpha, W)`.

    It returns the product operator, the lifted S2 chirality vector, and
    metadata needed by later analysis stages. It does not compute or expose a
    full-product global chiral observable.
    """
    if perturbation < 0:
        raise ValueError("perturbation must be non-negative")

    s2_operator, s2_chirality = build_dirac_monopole_operator(q=q, cutoff=cutoff, radius=radius)
    s1_operator = build_s1_spectral_operator(
        size=s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        s1_family=s1_family,
    )
    gamma_s2 = np.diag(s2_chirality.astype(float))
    d_total = np.kron(s2_operator.astype(complex), np.eye(s1_size, dtype=complex)) + np.kron(gamma_s2, s1_operator)
    d_total = _hermitize(d_total)

    lifted_s2_chirality = np.kron(s2_chirality.astype(float), np.ones(s1_size, dtype=float))
    metadata = {
        "q": int(q),
        "cutoff": int(cutoff),
        "alpha": float(alpha),
        "mode": str(mode),
        "s1_family": str(s1_family),
        "disorder_strength": float(disorder_strength),
        "seed": None if seed is None else int(seed),
        "radius": float(radius),
        "s1_size": int(s1_size),
        "s2_dimension": int(len(s2_chirality)),
        "total_dimension": int(d_total.shape[0]),
        "perturbation": float(perturbation),
        "perturbation_applied": False,
        "s2_zero_chirality_sign": 1 if q > 0 else -1 if q < 0 else 0,
        "s2_positive_dimension": int(np.count_nonzero(s2_chirality > 0)),
        "s2_negative_dimension": int(np.count_nonzero(s2_chirality < 0)),
    }
    return d_total, lifted_s2_chirality, metadata


def analyze_s2_s1_product(
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float = 1.0,
    perturbation: float = 0.0,
    zero_tolerance: float = 1e-7,
    low_energy_count: int = 8,
    chirality_tolerance: float = 0.5,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> S2S1Observation:
    """Analyze one toy S2 x S1 product operator at a single parameter point."""
    if zero_tolerance <= 0:
        raise ValueError("zero_tolerance must be positive")
    if low_energy_count < 1:
        raise ValueError("low_energy_count must be >= 1")
    if chirality_tolerance < 0:
        raise ValueError("chirality_tolerance must be non-negative")

    operator, lifted_s2_chirality, metadata = build_s2_s1_product_operator(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        s1_family=s1_family,
    )

    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    abs_eigenvalues = np.abs(eigenvalues)
    kernel_indices = np.flatnonzero(abs_eigenvalues <= zero_tolerance)
    kernel_count = int(len(kernel_indices))
    min_abs_eigenvalue = float(np.min(abs_eigenvalues))
    max_kernel_abs = float(np.max(abs_eigenvalues[kernel_indices])) if kernel_count else float("nan")

    s2_n_plus, s2_n_minus, ambiguous = _kernel_chirality_content(
        eigenvectors=eigenvectors,
        kernel_indices=kernel_indices,
        lifted_s2_chirality=lifted_s2_chirality,
        chirality_tolerance=chirality_tolerance,
    )
    positive_eigenvalues = eigenvalues[eigenvalues > zero_tolerance]
    mean_r_positive = float(mean_adjacent_gap_ratio(positive_eigenvalues))

    low_energy_indices = _select_low_energy_indices(abs_eigenvalues, kernel_indices, low_energy_count)
    fixed_window_indices = _select_fixed_window_low_energy_indices(abs_eigenvalues, low_energy_count)
    s1_low_energy_ipr = _mean_s1_marginal_ipr(
        eigenvectors=eigenvectors,
        selected_indices=low_energy_indices,
        s2_dimension=metadata["s2_dimension"],
        s1_size=s1_size,
    )
    s1_fixed_window_ipr = _mean_s1_marginal_ipr(
        eigenvectors=eigenvectors,
        selected_indices=fixed_window_indices,
        s2_dimension=metadata["s2_dimension"],
        s1_size=s1_size,
    )

    classification = _classify_observation(q=q, alpha=alpha, kernel_count=kernel_count)
    return S2S1Observation(
        q=int(q),
        cutoff=int(cutoff),
        s1_size=int(s1_size),
        alpha=float(alpha),
        mode=str(mode),
        disorder_strength=float(disorder_strength),
        seed=None if seed is None else int(seed),
        perturbation=float(perturbation),
        zero_tolerance=float(zero_tolerance),
        kernel_count=kernel_count,
        s2_n_plus_in_kernel=s2_n_plus,
        s2_n_minus_in_kernel=s2_n_minus,
        ambiguous_kernel_states=ambiguous,
        min_abs_eigenvalue=min_abs_eigenvalue,
        max_kernel_abs_eigenvalue=max_kernel_abs,
        mean_r_positive=mean_r_positive,
        s1_low_energy_ipr=s1_low_energy_ipr,
        s1_fixed_window_ipr=s1_fixed_window_ipr,
        classification=classification,
        s1_family=str(metadata["s1_family"]),
    )


def threshold_scan_s2_s1_product(
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float = 1.0,
    perturbation: float = 0.0,
    low_energy_count: int = 8,
    zero_tolerances: tuple[float, ...] = (1e-8, 1e-7, 1e-6),
    chirality_tolerance: float = 0.5,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> dict:
    """Run a tolerance scan for kernel classification stability at one point."""
    if not zero_tolerances:
        raise ValueError("zero_tolerances must not be empty")

    observations_by_tolerance: dict[float, S2S1Observation] = {}
    for zero_tolerance in zero_tolerances:
        observation = analyze_s2_s1_product(
            q=q,
            cutoff=cutoff,
            s1_size=s1_size,
            alpha=alpha,
            mode=mode,
            disorder_strength=disorder_strength,
            seed=seed,
            radius=radius,
            perturbation=perturbation,
            zero_tolerance=float(zero_tolerance),
            low_energy_count=low_energy_count,
            chirality_tolerance=chirality_tolerance,
            s1_family=s1_family,
        )
        observations_by_tolerance[float(zero_tolerance)] = observation

    kernel_counts_by_tolerance = {tol: obs.kernel_count for tol, obs in observations_by_tolerance.items()}
    classifications_by_tolerance = {tol: obs.classification for tol, obs in observations_by_tolerance.items()}
    kernel_presence = [count > 0 for count in kernel_counts_by_tolerance.values()]
    classification_values = list(classifications_by_tolerance.values())
    threshold_stable = all(flag == kernel_presence[0] for flag in kernel_presence) and all(
        value == classification_values[0] for value in classification_values
    )
    return {
        "observations_by_tolerance": observations_by_tolerance,
        "kernel_counts_by_tolerance": kernel_counts_by_tolerance,
        "classifications_by_tolerance": classifications_by_tolerance,
        "threshold_stable": bool(threshold_stable),
    }


def compare_pbc_apbc_lifting(
    q: int,
    cutoff: int,
    s1_size: int,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float = 1.0,
    perturbation: float = 0.0,
    zero_tolerance: float = 1e-7,
    low_energy_count: int = 8,
    chirality_tolerance: float = 0.5,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> dict:
    """Compare PBC and APBC as a single-point kernel-lifting diagnostic gate."""
    pbc = analyze_s2_s1_product(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=0.0,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        chirality_tolerance=chirality_tolerance,
        s1_family=s1_family,
    )
    apbc = analyze_s2_s1_product(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=0.5,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        chirality_tolerance=chirality_tolerance,
        s1_family=s1_family,
    )
    apbc_lifts_kernel = apbc.kernel_count < pbc.kernel_count and apbc.min_abs_eigenvalue > pbc.min_abs_eigenvalue
    return {
        "pbc_kernel_count": pbc.kernel_count,
        "apbc_kernel_count": apbc.kernel_count,
        "pbc_min_abs_eigenvalue": pbc.min_abs_eigenvalue,
        "apbc_min_abs_eigenvalue": apbc.min_abs_eigenvalue,
        "apbc_lifts_kernel": bool(apbc_lifts_kernel),
        "pbc_observation": pbc,
        "apbc_observation": apbc,
    }


def detect_flux_response(
    q: int,
    cutoff: int,
    s1_size: int,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float = 1.0,
    perturbation: float = 0.0,
    zero_tolerance: float = 1e-7,
    low_energy_count: int = 8,
    alpha_reference: float = 0.0,
    alpha_probe: float = 0.25,
    response_tolerance: float = 1e-10,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> dict:
    """Detect whether a twist changes the low-energy spectrum in the toy product."""
    reference_signature = _low_energy_signature(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=alpha_reference,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        s1_family=s1_family,
    )
    probe_signature = _low_energy_signature(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=alpha_probe,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        s1_family=s1_family,
    )
    low_energy_delta = float(np.linalg.norm(reference_signature - probe_signature))
    return {
        "flux_response_observed": bool(low_energy_delta > response_tolerance),
        "low_energy_delta": low_energy_delta,
    }


def detect_s1_not_spectator(
    q: int,
    cutoff: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float = 1.0,
    perturbation: float = 0.0,
    zero_tolerance: float = 1e-7,
    low_energy_count: int = 8,
    small_s1_size: int = 1,
    large_s1_size: int = 16,
    response_tolerance: float = 1e-10,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> dict:
    """Detect whether the S1 factor changes low-energy structure beyond spectator status."""
    small_obs = analyze_s2_s1_product(
        q=q,
        cutoff=cutoff,
        s1_size=small_s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        s1_family=s1_family,
    )
    large_obs = analyze_s2_s1_product(
        q=q,
        cutoff=cutoff,
        s1_size=large_s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        s1_family=s1_family,
    )
    small_signature = _low_energy_signature(
        q=q,
        cutoff=cutoff,
        s1_size=small_s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        s1_family=s1_family,
    )
    large_signature = _low_energy_signature(
        q=q,
        cutoff=cutoff,
        s1_size=large_s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        s1_family=s1_family,
    )
    spectral_delta = float(np.linalg.norm(small_signature - large_signature))
    low_energy_delta = float(
        spectral_delta
        + abs(small_obs.min_abs_eigenvalue - large_obs.min_abs_eigenvalue)
        + abs(small_obs.s1_low_energy_ipr - large_obs.s1_low_energy_ipr)
    )
    return {
        "s1_not_spectator": bool(low_energy_delta > response_tolerance),
        "low_energy_delta": low_energy_delta,
        "small_observation": small_obs,
        "large_observation": large_obs,
    }


def compare_localization_gate(
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    seed: int | None,
    radius: float = 1.0,
    perturbation: float = 0.0,
    zero_tolerance: float = 1e-7,
    low_energy_count: int = 8,
    disordered_strength: float = 8.0,
    ipr_margin: float = 1e-6,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> dict:
    """Compare clean and geometric_weight modes as a toy localization gate."""
    clean = analyze_s2_s1_product(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode="clean",
        disorder_strength=0.0,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        s1_family=s1_family,
    )
    disordered = analyze_s2_s1_product(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode="geometric_weight",
        disorder_strength=disordered_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        zero_tolerance=zero_tolerance,
        low_energy_count=low_energy_count,
        s1_family=s1_family,
    )
    kernel_only_localization_gate_passed = bool(disordered.s1_low_energy_ipr > clean.s1_low_energy_ipr + ipr_margin)
    fixed_window_localization_gate_passed = bool(
        disordered.s1_fixed_window_ipr > clean.s1_fixed_window_ipr + ipr_margin
    )
    return {
        "clean_ipr": clean.s1_low_energy_ipr,
        "disordered_ipr": disordered.s1_low_energy_ipr,
        "clean_fixed_window_ipr": clean.s1_fixed_window_ipr,
        "disordered_fixed_window_ipr": disordered.s1_fixed_window_ipr,
        "localization_gate_passed": bool(kernel_only_localization_gate_passed),
        "kernel_only_localization_gate_passed": bool(kernel_only_localization_gate_passed),
        "fixed_window_localization_gate_passed": bool(fixed_window_localization_gate_passed),
        "localization_gate_v2_passed": bool(fixed_window_localization_gate_passed),
        "localization_window_mode": "fixed_low_energy_window",
        "window_selection_sensitivity": bool(
            kernel_only_localization_gate_passed != fixed_window_localization_gate_passed
        ),
        "clean_observation": clean,
        "disordered_observation": disordered,
    }


def _worst_localization_v3_classification(labels: tuple[str, ...]) -> str:
    """Pick the most severe v3 label across localization cells (fail is worst)."""
    if not labels:
        return "not_applicable"
    severity = {"fail": 0, "window_sensitive": 1, "fragile_pass": 2, "window_robust_pass": 3}
    unknown = [c for c in labels if c not in severity]
    if unknown:
        raise ValueError(f"unknown v3 classification label: {unknown!r}")
    return str(min(labels, key=lambda c: severity[str(c)]))


def compare_localization_gate_v3(
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    seed: int | None,
    radius: float = 1.0,
    perturbation: float = 0.0,
    zero_tolerance: float = 1e-7,
    disordered_strength: float = 8.0,
    ipr_margin: float = 1e-6,
    s1_family: str = DEFAULT_S1_FAMILY,
    low_energy_count_values: tuple[int, ...] = (4, 6, 8, 10, 12),
    reference_low_energy_count: int = 8,
) -> dict:
    """Fixed-window localization gate with a sweep over ``low_energy_count``.

    Aggregates pass/fail across several fixed-window widths to reduce sensitivity
    to a single ``low_energy_count`` choice. This is a toy ``S2 x S1`` diagnostic
    only; it does not assert continuum compactification or a full-product chiral
    observable.
    """
    if ipr_margin < 0:
        raise ValueError("ipr_margin must be non-negative")
    if not low_energy_count_values:
        raise ValueError("low_energy_count_values must not be empty")
    if any(int(k) < 1 for k in low_energy_count_values):
        raise ValueError("each low_energy_count must be >= 1")
    if reference_low_energy_count not in low_energy_count_values:
        raise ValueError("reference_low_energy_count must be one of low_energy_count_values")

    ipr_delta_by_window: dict[int, float] = {}
    pass_by_window: dict[int, bool] = {}
    clean_by_k: dict[int, S2S1Observation] = {}
    disordered_by_k: dict[int, S2S1Observation] = {}

    for k in low_energy_count_values:
        kk = int(k)
        clean = analyze_s2_s1_product(
            q=q,
            cutoff=cutoff,
            s1_size=s1_size,
            alpha=alpha,
            mode="clean",
            disorder_strength=0.0,
            seed=seed,
            radius=radius,
            perturbation=perturbation,
            zero_tolerance=zero_tolerance,
            low_energy_count=kk,
            s1_family=s1_family,
        )
        disordered = analyze_s2_s1_product(
            q=q,
            cutoff=cutoff,
            s1_size=s1_size,
            alpha=alpha,
            mode="geometric_weight",
            disorder_strength=disordered_strength,
            seed=seed,
            radius=radius,
            perturbation=perturbation,
            zero_tolerance=zero_tolerance,
            low_energy_count=kk,
            s1_family=s1_family,
        )
        delta = float(disordered.s1_fixed_window_ipr - clean.s1_fixed_window_ipr)
        ipr_delta_by_window[kk] = delta
        pass_by_window[kk] = bool(delta > ipr_margin)
        clean_by_k[kk] = clean
        disordered_by_k[kk] = disordered

    deltas = [ipr_delta_by_window[int(k)] for k in low_energy_count_values]
    n_win = len(low_energy_count_values)
    p_pass = int(sum(1 for v in pass_by_window.values() if v))
    pass_rate = float(p_pass) / float(n_win)
    median_delta = float(median(deltas))
    min_delta = float(min(deltas))
    window_sensitivity_score = float(1.0 - pass_rate)

    ref_k = int(reference_low_energy_count)
    clean_ref = clean_by_k[ref_k]
    disordered_ref = disordered_by_k[ref_k]
    kernel_only_localization_gate_passed = bool(
        disordered_ref.s1_low_energy_ipr > clean_ref.s1_low_energy_ipr + ipr_margin
    )
    fixed_window_localization_gate_passed = bool(
        disordered_ref.s1_fixed_window_ipr > clean_ref.s1_fixed_window_ipr + ipr_margin
    )

    unstable_window_cases: list[dict[str, object]] = []
    for kk in low_energy_count_values:
        k_int = int(kk)
        if not pass_by_window[k_int]:
            unstable_window_cases.append(
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
        "ipr_delta_by_window": {int(k): float(ipr_delta_by_window[int(k)]) for k in low_energy_count_values},
        "pass_by_window": {int(k): bool(pass_by_window[int(k)]) for k in low_energy_count_values},
        "pass_rate_across_windows": pass_rate,
        "min_ipr_delta": min_delta,
        "median_ipr_delta": median_delta,
        "window_sensitivity_score": window_sensitivity_score,
        "window_robust_localization_passed": window_robust_localization_passed,
        "unstable_window_cases": unstable_window_cases,
        "kernel_only_localization_gate_passed": kernel_only_localization_gate_passed,
        "fixed_window_localization_gate_passed": fixed_window_localization_gate_passed,
        "classification": classification,
        "clean_observation_ref": clean_ref,
        "disordered_observation_ref": disordered_ref,
    }


def run_s2_s1_product_benchmark(config: S2S1ProductConfig) -> S2S1Assessment:
    """Run the toy S2 x S1 benchmark grid in memory and aggregate gate diagnostics."""
    observations: list[S2S1Observation] = []
    mode_to_index = {mode: idx for idx, mode in enumerate(config.s1_modes)}
    nonzero_q_values = [q for q in config.q_values if q != 0]
    min_disorder = min(config.disorder_values)
    max_disorder = max(config.disorder_values)
    representative_alpha = 0.0 if 0.0 in config.boundary_twists else float(min(config.boundary_twists))
    flux_probe_alpha = _select_flux_probe_alpha(config.boundary_twists, representative_alpha)
    representative_perturbation = min(config.perturbation_values)

    for q in config.q_values:
        for s1_size in config.s1_sizes:
            for alpha in config.boundary_twists:
                for mode in config.s1_modes:
                    mode_index = mode_to_index[mode]
                    for disorder_index, disorder_strength in enumerate(config.disorder_values):
                        for perturbation_index, perturbation in enumerate(config.perturbation_values):
                            for realization in range(config.realizations):
                                run_seed = _benchmark_seed(
                                    base_seed=config.seed,
                                    q=q,
                                    s1_size=s1_size,
                                    mode_index=mode_index,
                                    disorder_index=disorder_index,
                                    perturbation_index=perturbation_index,
                                    realization=realization,
                                )
                                observations.append(
                                    analyze_s2_s1_product(
                                        q=q,
                                        cutoff=config.cutoff,
                                        s1_size=s1_size,
                                        alpha=alpha,
                                        s1_family=config.s1_family,
                                        mode=mode,
                                        disorder_strength=disorder_strength,
                                        seed=run_seed,
                                        radius=config.s1_radius,
                                        perturbation=perturbation,
                                        zero_tolerance=config.zero_tolerance,
                                        low_energy_count=config.low_energy_count,
                                        chirality_tolerance=config.chirality_threshold,
                                    )
                                )

    q_zero_rows = [row for row in observations if row.q == 0]
    q_control_passed = bool(q_zero_rows) and all(row.classification != "inherited_kernel_signal" for row in q_zero_rows)

    pbc_results: list[bool] = []
    apbc_results: list[bool] = []
    threshold_results: list[bool] = []
    flux_results: list[bool] = []
    localization_results: list[bool] = []
    fixed_window_localization_results: list[bool] = []
    localization_window_sensitivity_results: list[bool] = []

    if "clean" in config.s1_modes and 0.0 in config.boundary_twists and 0.5 in config.boundary_twists and nonzero_q_values:
        for q in nonzero_q_values:
            for s1_size in config.s1_sizes:
                lifting = compare_pbc_apbc_lifting(
                    q=q,
                    cutoff=config.cutoff,
                    s1_size=s1_size,
                    s1_family=config.s1_family,
                    mode="clean",
                    disorder_strength=min_disorder,
                    seed=config.seed,
                    radius=config.s1_radius,
                    perturbation=representative_perturbation,
                    zero_tolerance=config.zero_tolerance,
                    low_energy_count=config.low_energy_count,
                    chirality_tolerance=config.chirality_threshold,
                )
                pbc_results.append(lifting["pbc_kernel_count"] >= 1)
                apbc_results.append(lifting["apbc_lifts_kernel"])

                threshold = threshold_scan_s2_s1_product(
                    q=q,
                    cutoff=config.cutoff,
                    s1_size=s1_size,
                    alpha=0.0,
                    s1_family=config.s1_family,
                    mode="clean",
                    disorder_strength=min_disorder,
                    seed=config.seed,
                    radius=config.s1_radius,
                    perturbation=representative_perturbation,
                    low_energy_count=config.low_energy_count,
                    zero_tolerances=config.zero_tolerance_scan,
                    chirality_tolerance=config.chirality_threshold,
                )
                threshold_results.append(threshold["threshold_stable"])

                if flux_probe_alpha is not None:
                    flux = detect_flux_response(
                        q=q,
                        cutoff=config.cutoff,
                        s1_size=s1_size,
                        s1_family=config.s1_family,
                        mode="clean",
                        disorder_strength=min_disorder,
                        seed=config.seed,
                        radius=config.s1_radius,
                        perturbation=representative_perturbation,
                        zero_tolerance=config.zero_tolerance,
                        low_energy_count=config.low_energy_count,
                        alpha_reference=representative_alpha,
                        alpha_probe=flux_probe_alpha,
                    )
                    flux_results.append(flux["flux_response_observed"])

    if len(config.s1_sizes) >= 2 and "clean" in config.s1_modes and nonzero_q_values:
        smallest_s1 = min(config.s1_sizes)
        largest_s1 = max(config.s1_sizes)
        spectator_results: list[bool] = []
        for q in nonzero_q_values:
            spectator = detect_s1_not_spectator(
                q=q,
                cutoff=config.cutoff,
                alpha=representative_alpha,
                s1_family=config.s1_family,
                mode="clean",
                disorder_strength=min_disorder,
                seed=config.seed,
                radius=config.s1_radius,
                perturbation=representative_perturbation,
                zero_tolerance=config.zero_tolerance,
                low_energy_count=config.low_energy_count,
                small_s1_size=smallest_s1,
                large_s1_size=largest_s1,
            )
            spectator_results.append(spectator["s1_not_spectator"])
        s1_not_spectator = bool(spectator_results) and all(spectator_results)
    else:
        s1_not_spectator = False

    if "clean" in config.s1_modes and "geometric_weight" in config.s1_modes and nonzero_q_values:
        for q in nonzero_q_values:
            for s1_size in config.s1_sizes:
                localization = compare_localization_gate(
                    q=q,
                    cutoff=config.cutoff,
                    s1_size=s1_size,
                    alpha=representative_alpha,
                    s1_family=config.s1_family,
                    seed=config.seed,
                    radius=config.s1_radius,
                    perturbation=representative_perturbation,
                    zero_tolerance=config.zero_tolerance,
                    low_energy_count=config.low_energy_count,
                    disordered_strength=max_disorder,
                    ipr_margin=config.localization_ipr_margin,
                )
                localization_results.append(localization["localization_gate_passed"])
                fixed_window_localization_results.append(localization["fixed_window_localization_gate_passed"])
                localization_window_sensitivity_results.append(localization["window_selection_sensitivity"])

    v3_classification: str | None = None
    v3_pass_rate_min: float | None = None
    v3_window_sensitivity_score: float | None = None
    v3_robust_all: bool | None = None
    v3_unstable: tuple[dict[str, object], ...] | None = None
    v3_v2_disagree: bool | None = None
    if (
        config.localization_gate_v3_enabled
        and "clean" in config.s1_modes
        and "geometric_weight" in config.s1_modes
        and nonzero_q_values
    ):
        ref_vals = tuple(int(x) for x in config.localization_gate_v3_low_energy_count_values)
        if int(config.low_energy_count) not in ref_vals:
            raise ValueError(
                "localization_gate_v3_enabled requires config.low_energy_count to appear in "
                "localization_gate_v3_low_energy_count_values"
            )
        v3_cell_labels: list[str] = []
        v3_pass_rates: list[float] = []
        v3_scores: list[float] = []
        v3_robust_flags: list[bool] = []
        disagree: list[bool] = []
        unstable_records: list[dict[str, object]] = []
        for q in nonzero_q_values:
            for s1_size in config.s1_sizes:
                loc_v2 = compare_localization_gate(
                    q=q,
                    cutoff=config.cutoff,
                    s1_size=s1_size,
                    alpha=representative_alpha,
                    s1_family=config.s1_family,
                    seed=config.seed,
                    radius=config.s1_radius,
                    perturbation=representative_perturbation,
                    zero_tolerance=config.zero_tolerance,
                    low_energy_count=config.low_energy_count,
                    disordered_strength=max_disorder,
                    ipr_margin=config.localization_ipr_margin,
                )
                loc_v3 = compare_localization_gate_v3(
                    q=q,
                    cutoff=config.cutoff,
                    s1_size=s1_size,
                    alpha=representative_alpha,
                    seed=config.seed,
                    radius=config.s1_radius,
                    perturbation=representative_perturbation,
                    zero_tolerance=config.zero_tolerance,
                    disordered_strength=max_disorder,
                    ipr_margin=config.localization_ipr_margin,
                    s1_family=config.s1_family,
                    low_energy_count_values=tuple(int(x) for x in config.localization_gate_v3_low_energy_count_values),
                    reference_low_energy_count=int(config.low_energy_count),
                )
                v2_pass = bool(loc_v2["fixed_window_localization_gate_passed"])
                v3_robust = bool(loc_v3["window_robust_localization_passed"])
                disagree.append(v2_pass != v3_robust)
                v3_cell_labels.append(str(loc_v3["classification"]))
                v3_pass_rates.append(float(loc_v3["pass_rate_across_windows"]))
                v3_scores.append(float(loc_v3["window_sensitivity_score"]))
                v3_robust_flags.append(bool(loc_v3["window_robust_localization_passed"]))
                unstable = loc_v3["unstable_window_cases"]
                if unstable:
                    unstable_records.append(
                        {"q": int(q), "s1_size": int(s1_size), "unstable_window_cases": list(unstable)}
                    )
        v3_classification = _worst_localization_v3_classification(tuple(v3_cell_labels))
        v3_pass_rate_min = float(min(v3_pass_rates)) if v3_pass_rates else None
        v3_window_sensitivity_score = float(max(v3_scores)) if v3_scores else None
        v3_robust_all = bool(all(v3_robust_flags)) if v3_robust_flags else None
        v3_unstable = tuple(unstable_records)
        v3_v2_disagree = bool(any(disagree)) if disagree else None

    pbc_gate_passed = bool(pbc_results) and all(pbc_results)
    apbc_gate_passed = bool(apbc_results) and all(apbc_results)
    flux_response_observed = bool(flux_results) and all(flux_results)
    localization_gate_passed = bool(localization_results) and all(localization_results)
    kernel_only_localization_gate_passed = bool(localization_results) and all(localization_results)
    fixed_window_localization_gate_passed = bool(fixed_window_localization_results) and all(
        fixed_window_localization_results
    )
    localization_gate_v2_passed = bool(fixed_window_localization_gate_passed)
    localization_window_mode = "fixed_low_energy_window"
    window_selection_sensitivity = bool(localization_window_sensitivity_results) and any(
        localization_window_sensitivity_results
    )
    threshold_stable = bool(threshold_results) and all(threshold_results)
    all_basic_gates_passed = all(
        (
            q_control_passed,
            pbc_gate_passed,
            apbc_gate_passed,
            flux_response_observed,
            s1_not_spectator,
            localization_gate_passed,
            threshold_stable,
        )
    )

    if all_basic_gates_passed:
        classification = "quick_bridge_passed"
    elif not q_control_passed or not pbc_gate_passed or not apbc_gate_passed:
        classification = "failed"
    elif (
        q_control_passed
        and pbc_gate_passed
        and apbc_gate_passed
        and flux_response_observed
        and s1_not_spectator
        and threshold_stable
        and (not kernel_only_localization_gate_passed)
        and fixed_window_localization_gate_passed
    ):
        classification = "window_selection_sensitivity"
    else:
        classification = "partial_or_ambiguous"

    notes = _benchmark_notes(
        total_observations=len(observations),
        q_control_passed=q_control_passed,
        pbc_gate_passed=pbc_gate_passed,
        apbc_gate_passed=apbc_gate_passed,
        flux_response_observed=flux_response_observed,
        s1_not_spectator=s1_not_spectator,
        localization_gate_passed=localization_gate_passed,
        kernel_only_localization_gate_passed=kernel_only_localization_gate_passed,
        fixed_window_localization_gate_passed=fixed_window_localization_gate_passed,
        localization_gate_v2_passed=localization_gate_v2_passed,
        localization_window_mode=localization_window_mode,
        window_selection_sensitivity=window_selection_sensitivity,
        threshold_stable=threshold_stable,
    )
    if config.localization_gate_v3_enabled and v3_classification is not None:
        notes = notes + (f"localization_gate_v3_classification={v3_classification}",)

    return S2S1Assessment(
        config=config,
        observations=tuple(observations),
        total_observations=len(observations),
        q_control_passed=bool(q_control_passed),
        pbc_gate_passed=bool(pbc_gate_passed),
        apbc_gate_passed=bool(apbc_gate_passed),
        flux_response_observed=bool(flux_response_observed),
        s1_not_spectator=bool(s1_not_spectator),
        localization_gate_passed=bool(localization_gate_passed),
        kernel_only_localization_gate_passed=bool(kernel_only_localization_gate_passed),
        fixed_window_localization_gate_passed=bool(fixed_window_localization_gate_passed),
        localization_gate_v2_passed=bool(localization_gate_v2_passed),
        localization_window_mode=str(localization_window_mode),
        threshold_stable=bool(threshold_stable),
        all_basic_gates_passed=bool(all_basic_gates_passed),
        classification=classification,
        notes=notes,
        localization_gate_v3_classification=v3_classification,
        pass_rate_across_windows=v3_pass_rate_min,
        window_sensitivity_score=v3_window_sensitivity_score,
        window_robust_localization_passed=v3_robust_all,
        unstable_window_cases=v3_unstable,
        v2_vs_v3_disagreement=v3_v2_disagree,
    )


def save_s2_s1_run_artifacts(assessment: S2S1Assessment, run_dir: Path | str) -> dict:
    """Save reproducible toy S2 x S1 benchmark artifacts under one run directory."""
    run_path = Path(run_dir)
    run_path.mkdir(parents=True, exist_ok=True)
    figures_dir = run_path / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    config_path = run_path / "config.json"
    metrics_path = run_path / "metrics.json"
    data_path = run_path / "data.npz"
    summary_path = run_path / "summary.md"

    config_payload = asdict(assessment.config)
    metrics_payload = _assessment_metrics_payload(assessment)
    numeric_arrays = _observation_numeric_arrays(assessment.observations)
    text_arrays = _observation_text_arrays(assessment.observations)
    assessment_arrays = _assessment_data_payload(assessment)

    config_path.write_text(json.dumps(config_payload, indent=2, sort_keys=True), encoding="utf-8")
    metrics_path.write_text(json.dumps(metrics_payload, indent=2, sort_keys=True), encoding="utf-8")
    np.savez_compressed(data_path, **numeric_arrays, **text_arrays, **assessment_arrays)
    summary_path.write_text(_build_summary_markdown(assessment), encoding="utf-8")

    return {
        "config": str(config_path),
        "metrics": str(metrics_path),
        "data": str(data_path),
        "summary": str(summary_path),
        "figures_dir": str(figures_dir),
    }


def _build_clean_s1_spectral_operator(size: int, alpha: float, radius: float) -> np.ndarray:
    modes = np.fft.fftfreq(size, d=1.0 / size)
    twisted_momenta = (modes + float(alpha)) / float(radius)
    dft = _unitary_dft_matrix(size)
    operator = dft.conj().T @ np.diag(twisted_momenta.astype(float)) @ dft
    return _hermitize(operator)


def _unitary_dft_matrix(size: int) -> np.ndarray:
    grid = np.arange(size, dtype=float)
    phase = np.exp(2j * np.pi * np.outer(grid, grid) / float(size))
    return phase / np.sqrt(float(size))


def _hermitize(matrix: np.ndarray) -> np.ndarray:
    dense = np.asarray(matrix, dtype=complex)
    return 0.5 * (dense + dense.conj().T)


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


def _select_low_energy_indices(
    abs_eigenvalues: np.ndarray,
    kernel_indices: np.ndarray,
    low_energy_count: int,
) -> np.ndarray:
    if kernel_indices.size:
        return kernel_indices
    count = min(int(low_energy_count), abs_eigenvalues.size)
    return np.argsort(abs_eigenvalues)[:count]


def _select_fixed_window_low_energy_indices(abs_eigenvalues: np.ndarray, low_energy_count: int) -> np.ndarray:
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


def _classify_observation(q: int, alpha: float, kernel_count: int) -> str:
    if q != 0 and np.isclose(alpha, 0.0) and kernel_count > 0:
        return "inherited_kernel_signal"
    if q == 0 and kernel_count == 0:
        return "q_zero_no_inherited_kernel"
    if not np.isclose(alpha, 0.0) and kernel_count == 0:
        return "lifted_or_no_kernel"
    return "ambiguous"


def _low_energy_signature(
    q: int,
    cutoff: int,
    s1_size: int,
    alpha: float,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float,
    perturbation: float,
    zero_tolerance: float,
    low_energy_count: int,
    s1_family: str = DEFAULT_S1_FAMILY,
) -> np.ndarray:
    operator, _lifted_s2_chirality, _metadata = build_s2_s1_product_operator(
        q=q,
        cutoff=cutoff,
        s1_size=s1_size,
        alpha=alpha,
        mode=mode,
        disorder_strength=disorder_strength,
        seed=seed,
        radius=radius,
        perturbation=perturbation,
        s1_family=s1_family,
    )
    eigenvalues = np.linalg.eigvalsh(operator)
    abs_eigenvalues = np.abs(eigenvalues)
    count = min(int(low_energy_count), abs_eigenvalues.size)
    selected = np.argsort(abs_eigenvalues)[:count]
    signature = np.asarray(abs_eigenvalues[np.asarray(selected, dtype=int)], dtype=float)
    if signature.size == 0:
        return np.zeros(0, dtype=float)
    scale = max(float(np.max(signature)), 1.0)
    return signature / scale


def _benchmark_seed(
    base_seed: int,
    q: int,
    s1_size: int,
    mode_index: int,
    disorder_index: int,
    perturbation_index: int,
    realization: int,
) -> int:
    return (
        int(base_seed)
        + 1_000_000 * int(q + 10)
        + 100_000 * int(s1_size)
        + 10_000 * int(mode_index)
        + 1_000 * int(disorder_index)
        + 100 * int(perturbation_index)
        + int(realization)
    )


def _select_flux_probe_alpha(boundary_twists: tuple[float, ...], alpha_reference: float) -> float | None:
    for candidate in (0.25, 0.5):
        if candidate in boundary_twists and not np.isclose(candidate, alpha_reference):
            return candidate
    for candidate in boundary_twists:
        if not np.isclose(candidate, alpha_reference):
            return float(candidate)
    return None


def _benchmark_notes(
    total_observations: int,
    q_control_passed: bool,
    pbc_gate_passed: bool,
    apbc_gate_passed: bool,
    flux_response_observed: bool,
    s1_not_spectator: bool,
    localization_gate_passed: bool,
    kernel_only_localization_gate_passed: bool,
    fixed_window_localization_gate_passed: bool,
    localization_gate_v2_passed: bool,
    localization_window_mode: str,
    window_selection_sensitivity: bool,
    threshold_stable: bool,
) -> tuple[str, ...]:
    failed = [
        name
        for name, passed in (
            ("q_control_passed", q_control_passed),
            ("pbc_gate_passed", pbc_gate_passed),
            ("apbc_gate_passed", apbc_gate_passed),
            ("flux_response_observed", flux_response_observed),
            ("s1_not_spectator", s1_not_spectator),
            ("localization_gate_passed", localization_gate_passed),
            ("threshold_stable", threshold_stable),
        )
        if not passed
    ]
    notes = [
        f"total_observations={int(total_observations)}",
        f"kernel_only_localization_gate_passed={bool(kernel_only_localization_gate_passed)}",
        f"fixed_window_localization_gate_passed={bool(fixed_window_localization_gate_passed)}",
        f"localization_gate_v2_passed={bool(localization_gate_v2_passed)}",
        f"localization_window_mode={str(localization_window_mode)}",
    ]
    if window_selection_sensitivity:
        notes.append("window_selection_sensitivity=True")
    if failed:
        notes.append("failed_gates=" + ",".join(failed))
    else:
        notes.append("all_basic_gates_passed=True")
    return tuple(notes)


def _assessment_metrics_payload(assessment: S2S1Assessment) -> dict:
    classification_counts = Counter(row.classification for row in assessment.observations)
    mode_counts = Counter(row.mode for row in assessment.observations)
    family_counts = Counter(row.s1_family for row in assessment.observations)
    return {
        "total_observations": int(assessment.total_observations),
        "s1_family": str(assessment.config.s1_family),
        "q_control_passed": bool(assessment.q_control_passed),
        "pbc_gate_passed": bool(assessment.pbc_gate_passed),
        "apbc_gate_passed": bool(assessment.apbc_gate_passed),
        "flux_response_observed": bool(assessment.flux_response_observed),
        "s1_not_spectator": bool(assessment.s1_not_spectator),
        "localization_gate_passed": bool(assessment.localization_gate_passed),
        "kernel_only_localization_gate_passed": bool(assessment.kernel_only_localization_gate_passed),
        "fixed_window_localization_gate_passed": bool(assessment.fixed_window_localization_gate_passed),
        "localization_gate_v2_passed": bool(assessment.localization_gate_v2_passed),
        "localization_window_mode": str(assessment.localization_window_mode),
        "threshold_stable": bool(assessment.threshold_stable),
        "all_basic_gates_passed": bool(assessment.all_basic_gates_passed),
        "classification": str(assessment.classification),
        "notes": list(assessment.notes),
        "localization_gate_v3_classification": assessment.localization_gate_v3_classification,
        "pass_rate_across_windows": assessment.pass_rate_across_windows,
        "window_sensitivity_score": assessment.window_sensitivity_score,
        "window_robust_localization_passed": assessment.window_robust_localization_passed,
        "unstable_window_cases": (
            [dict(entry) for entry in assessment.unstable_window_cases]
            if assessment.unstable_window_cases is not None
            else None
        ),
        "v2_vs_v3_disagreement": assessment.v2_vs_v3_disagreement,
        "classification_counts": dict(sorted(classification_counts.items())),
        "mode_counts": dict(sorted(mode_counts.items())),
        "family_counts": dict(sorted(family_counts.items())),
    }


def _observation_numeric_arrays(observations: tuple[S2S1Observation, ...]) -> dict[str, np.ndarray]:
    rows = tuple(observations)
    return {
        "q": np.asarray([row.q for row in rows], dtype=int),
        "cutoff": np.asarray([row.cutoff for row in rows], dtype=int),
        "s1_size": np.asarray([row.s1_size for row in rows], dtype=int),
        "alpha": np.asarray([row.alpha for row in rows], dtype=float),
        "disorder_strength": np.asarray([row.disorder_strength for row in rows], dtype=float),
        "perturbation": np.asarray([row.perturbation for row in rows], dtype=float),
        "zero_tolerance": np.asarray([row.zero_tolerance for row in rows], dtype=float),
        "kernel_count": np.asarray([row.kernel_count for row in rows], dtype=int),
        "s2_n_plus_in_kernel": np.asarray([row.s2_n_plus_in_kernel for row in rows], dtype=int),
        "s2_n_minus_in_kernel": np.asarray([row.s2_n_minus_in_kernel for row in rows], dtype=int),
        "ambiguous_kernel_states": np.asarray([row.ambiguous_kernel_states for row in rows], dtype=int),
        "min_abs_eigenvalue": np.asarray([row.min_abs_eigenvalue for row in rows], dtype=float),
        "max_kernel_abs_eigenvalue": np.asarray([row.max_kernel_abs_eigenvalue for row in rows], dtype=float),
        "mean_r_positive": np.asarray([row.mean_r_positive for row in rows], dtype=float),
        "s1_low_energy_ipr": np.asarray([row.s1_low_energy_ipr for row in rows], dtype=float),
        "s1_fixed_window_ipr": np.asarray([row.s1_fixed_window_ipr for row in rows], dtype=float),
    }


def _observation_text_arrays(observations: tuple[S2S1Observation, ...]) -> dict[str, np.ndarray]:
    rows = tuple(observations)
    return {
        "s1_family": np.asarray([row.s1_family for row in rows], dtype=str),
        "mode": np.asarray([row.mode for row in rows], dtype=str),
        "classification_label": np.asarray([row.classification for row in rows], dtype=str),
    }


def _assessment_data_payload(assessment: S2S1Assessment) -> dict[str, np.ndarray]:
    return {
        "assessment_q_control_passed": np.asarray([assessment.q_control_passed], dtype=bool),
        "assessment_pbc_gate_passed": np.asarray([assessment.pbc_gate_passed], dtype=bool),
        "assessment_apbc_gate_passed": np.asarray([assessment.apbc_gate_passed], dtype=bool),
        "assessment_flux_response_observed": np.asarray([assessment.flux_response_observed], dtype=bool),
        "assessment_s1_not_spectator": np.asarray([assessment.s1_not_spectator], dtype=bool),
        "assessment_localization_gate_passed": np.asarray([assessment.localization_gate_passed], dtype=bool),
        "assessment_kernel_only_localization_gate_passed": np.asarray(
            [assessment.kernel_only_localization_gate_passed], dtype=bool
        ),
        "assessment_fixed_window_localization_gate_passed": np.asarray(
            [assessment.fixed_window_localization_gate_passed], dtype=bool
        ),
        "assessment_localization_gate_v2_passed": np.asarray([assessment.localization_gate_v2_passed], dtype=bool),
        "assessment_threshold_stable": np.asarray([assessment.threshold_stable], dtype=bool),
        "assessment_all_basic_gates_passed": np.asarray([assessment.all_basic_gates_passed], dtype=bool),
        "assessment_total_observations": np.asarray([assessment.total_observations], dtype=int),
        "assessment_localization_window_mode": np.asarray([assessment.localization_window_mode], dtype=str),
        "assessment_classification": np.asarray([assessment.classification], dtype=str),
        "assessment_pass_rate_across_windows": np.asarray(
            [np.nan if assessment.pass_rate_across_windows is None else float(assessment.pass_rate_across_windows)],
            dtype=float,
        ),
        "assessment_window_sensitivity_score": np.asarray(
            [np.nan if assessment.window_sensitivity_score is None else float(assessment.window_sensitivity_score)],
            dtype=float,
        ),
        "assessment_window_robust_localization_passed": np.asarray(
            [np.nan if assessment.window_robust_localization_passed is None else float(assessment.window_robust_localization_passed)],
            dtype=float,
        ),
        "assessment_v2_vs_v3_disagreement": np.asarray(
            [np.nan if assessment.v2_vs_v3_disagreement is None else float(assessment.v2_vs_v3_disagreement)],
            dtype=float,
        ),
    }


def _build_summary_markdown(assessment: S2S1Assessment) -> str:
    gate_rows = (
        ("q_control_passed", assessment.q_control_passed),
        ("pbc_gate_passed", assessment.pbc_gate_passed),
        ("apbc_gate_passed", assessment.apbc_gate_passed),
        ("flux_response_observed", assessment.flux_response_observed),
        ("s1_not_spectator", assessment.s1_not_spectator),
        ("localization_gate_passed", assessment.localization_gate_passed),
        ("kernel_only_localization_gate_passed", assessment.kernel_only_localization_gate_passed),
        ("fixed_window_localization_gate_passed", assessment.fixed_window_localization_gate_passed),
        ("localization_gate_v2_passed", assessment.localization_gate_v2_passed),
        ("threshold_stable", assessment.threshold_stable),
        ("all_basic_gates_passed", assessment.all_basic_gates_passed),
    )
    gate_table = "\n".join(
        f"| `{name}` | {'PASS' if passed else 'FAIL'} |" for name, passed in gate_rows
    )
    notes_block = "\n".join(f"- {note}" for note in assessment.notes) if assessment.notes else "- none"
    return (
        "# S2 x S1 Product Benchmark Summary\n\n"
        "This is a toy S2 x S1 product diagnostic, not continuum compactification.\n\n"
        "Full-product global chiral index is not the headline metric.\n\n"
        f"S1 discretization family: `{assessment.config.s1_family}`\n\n"
        f"Localization window mode: `{assessment.localization_window_mode}`\n\n"
        f"Baseline context: `v0.1.11-mvp-s2-graph-intermediate-quick`\n\n"
        f"Assessment classification: `{assessment.classification}`\n\n"
        f"Total observations: `{assessment.total_observations}`\n\n"
        "## Gate Table\n"
        "| Gate | Status |\n"
        "| --- | --- |\n"
        f"{gate_table}\n\n"
        "## Notes\n"
        f"{notes_block}\n\n"
        "## Key Non-Claims\n"
        "- not S6\n"
        "- not S3 x S6\n"
        "- not Standard Model\n"
        "- not Witten/Lichnerowicz bypass\n"
        "- not physical compactification proof\n"
    )

