"""Graph-Laplacian geometric localization pre-control (cylinders + dumbbell tiny).

Toy / falsification layer only. Does not prove geometric localization.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

from cc_toy_lab.geometry.graph_laplacian import GraphLaplacianResult, build_knn_graph_laplacian
from cc_toy_lab.spectral.metrics import inverse_participation_ratio


@dataclass(frozen=True)
class StraightCylinderRunConfig:
    radius: float = 1.0
    length: float = 4.0
    n_z: int = 24
    n_theta: int = 32
    k_neighbors: int = 12
    num_modes: int = 8
    seeds: tuple[int, ...] = (123,)
    jitter: float = 0.0
    epsilon: float | None = None
    """If None, epsilon is chosen inside `build_knn_graph_laplacian`."""


@dataclass
class ModeDiagnostics:
    index: int
    eigenvalue: float
    ipr: float
    z_center_of_mass: float
    z_mass_left: float
    z_mass_center: float
    z_mass_right: float


@dataclass(frozen=True)
class VariableRadiusCylinderRunConfig:
    """Axisymmetric cylinder with radius ``r(z) = r0 * (1 + a * cos(2*pi*z/length))``."""

    r0: float = 1.0
    length: float = 4.0
    n_z: int = 24
    n_theta: int = 32
    relative_radius_modulation: float = 0.22
    """Amplitude ``a`` in ``r(z)=r0*(1+a*cos(...))``; must satisfy ``|a|<1`` for positive radius."""
    k_neighbors: int = 12
    num_modes: int = 8
    seeds: tuple[int, ...] = (123,)
    jitter: float = 0.0
    epsilon: float | None = None


@dataclass
class StraightCylinderPrecontrolResult:
    config: StraightCylinderRunConfig
    n_points: int
    connected_components: int
    degree_min: float
    degree_max: float
    degree_mean: float
    degree_std: float
    epsilon: float
    spectral_gap: float | None
    modes: list[ModeDiagnostics]
    gate_graph_connected: bool
    gate_degree_non_pathological: bool
    gate_ipr_not_extreme: bool
    gate_z_center_not_all_boundary_pinned: bool
    null_verdict: str
    points: np.ndarray = field(repr=False)


@dataclass
class VariableRadiusCylinderPrecontrolResult:
    config: VariableRadiusCylinderRunConfig
    n_points: int
    connected_components: int
    degree_min: float
    degree_max: float
    degree_mean: float
    degree_std: float
    epsilon: float
    spectral_gap: float | None
    modes: list[ModeDiagnostics]
    gate_graph_connected: bool
    gate_degree_non_pathological: bool
    gate_ipr_not_extreme: bool
    gate_z_center_not_all_boundary_pinned: bool
    gate_radius_profile_nontrivial: bool
    control_verdict: str
    points: np.ndarray = field(repr=False)
    radial_extent_ratio: float = 0.0
    """(r_max - r_min) / mean r on the sample."""


@dataclass(frozen=True)
class DumbbellTinyRunConfig:
    length: float = 6.0
    n_z: int = 32
    n_theta: int = 32
    throat_radii: tuple[float, ...] = (0.35, 0.5)
    bulb_radius: float = 1.0
    throat_width: float = 0.8
    k_values: tuple[int, ...] = (8, 12)
    seeds: tuple[int, ...] = (123,)
    num_modes: int = 10
    jitter: float = 0.0
    epsilon: float | None = None


@dataclass
class DumbbellModeDiagnostics:
    index: int
    eigenvalue: float
    ipr: float
    z_center_of_mass: float
    z_mass_left: float
    z_mass_center: float
    z_mass_right: float
    mass_left_bulb: float
    mass_throat: float
    mass_right_bulb: float
    throat_mass_fraction: float
    bulb_mass_fraction: float
    localization_region_label: str
    mode_symmetry_left_right: float


@dataclass
class DumbbellCaseResult:
    throat_radius: float
    bulb_radius: float
    throat_width: float
    k_neighbors: int
    length: float
    n_points: int
    connected_components: int
    degree_min: float
    degree_max: float
    degree_mean: float
    degree_std: float
    epsilon: float
    spectral_gap: float | None
    modes: list[DumbbellModeDiagnostics]
    gate_graph_connected: bool
    gate_degree_non_pathological: bool
    gate_ipr_not_extreme: bool
    gate_z_center_not_all_boundary_pinned: bool
    mean_ipr_low_modes: float


@dataclass
class DumbbellTinyDiagnosticResult:
    config: DumbbellTinyRunConfig
    cases: list[DumbbellCaseResult]
    aggregate_verdict: str
    k_sensitivity_ok_by_throat: dict[str, bool]
    formula_documentation: str
    precontrol_straight_run: str
    precontrol_variable_run: str


def build_straight_cylinder_points(
    radius: float,
    length: float,
    n_z: int,
    n_theta: int,
    jitter: float = 0.0,
    seed: int | None = None,
) -> np.ndarray:
    """Sample points on a straight cylinder surface embedded in R^3.

    z runs from ``-length/2`` to ``+length/2``; theta in ``[0, 2*pi)``.
    """
    if radius <= 0 or length <= 0:
        raise ValueError("radius and length must be positive")
    if n_z < 2 or n_theta < 3:
        raise ValueError("n_z must be >= 2 and n_theta must be >= 3")
    rng = np.random.default_rng(seed)
    z = np.linspace(-0.5 * length, 0.5 * length, n_z, dtype=np.float64)
    theta = np.linspace(0.0, 2.0 * np.pi, n_theta, endpoint=False, dtype=np.float64)
    zz, tt = np.meshgrid(z, theta, indexing="ij")
    x = radius * np.cos(tt).ravel()
    y = radius * np.sin(tt).ravel()
    zc = zz.ravel()
    pts = np.column_stack([x, y, zc])
    if jitter != 0.0:
        pts = pts + rng.normal(0.0, jitter, size=pts.shape)
    return pts.astype(np.float64, copy=False)


def build_variable_radius_cylinder_points(
    r0: float,
    length: float,
    n_z: int,
    n_theta: int,
    relative_radius_modulation: float,
    jitter: float = 0.0,
    seed: int | None = None,
) -> np.ndarray:
    """Sample points on a variable-radius cylinder ``r(z)=r0*(1+a*cos(2*pi*z/L))`` in R^3.

    ``z`` runs from ``-length/2`` to ``+length/2``; ``theta`` in ``[0, 2*pi)``.
    Requires ``|relative_radius_modulation| < 1`` so that ``r(z) > 0`` everywhere.
    """
    if r0 <= 0 or length <= 0:
        raise ValueError("r0 and length must be positive")
    a = float(relative_radius_modulation)
    if abs(a) >= 1.0:
        raise ValueError("relative_radius_modulation must satisfy |a| < 1 for positive radius")
    if n_z < 2 or n_theta < 3:
        raise ValueError("n_z must be >= 2 and n_theta must be >= 3")
    rng = np.random.default_rng(seed)
    z = np.linspace(-0.5 * length, 0.5 * length, n_z, dtype=np.float64)
    theta = np.linspace(0.0, 2.0 * np.pi, n_theta, endpoint=False, dtype=np.float64)
    zz, tt = np.meshgrid(z, theta, indexing="ij")
    rz = r0 * (1.0 + a * np.cos(2.0 * np.pi * zz / length))
    x = (rz * np.cos(tt)).ravel()
    y = (rz * np.sin(tt)).ravel()
    zc = zz.ravel()
    pts = np.column_stack([x, y, zc])
    if jitter != 0.0:
        pts = pts + rng.normal(0.0, jitter, size=pts.shape)
    return pts.astype(np.float64, copy=False)


DUMBBELL_RADIUS_FORMULA_DOC = (
    "Two-bulb smooth axisymmetric profile. Let z_L = -length/4, z_R = +length/4, "
    "σ = throat_width. Define S(z) = exp(-((z-z_L)/σ)²) + exp(-((z-z_R)/σ)²), "
    "S_max = max_z S(z). Then r(z) = throat_radius + (bulb_radius - throat_radius) * S(z) / S_max, "
    "so throat_radius ≤ r(z) ≤ bulb_radius on the sampled axis."
)


def build_dumbbell_cylinder_points(
    length: float,
    throat_radius: float,
    bulb_radius: float,
    n_z: int,
    n_theta: int,
    throat_width: float,
    jitter: float = 0.0,
    seed: int | None = None,
) -> np.ndarray:
    """Axisymmetric dumbbell-like surface: two Gaussian bumps in r(z), throat at center.

    Uses ``DUMBBELL_RADIUS_FORMULA_DOC`` normalization so ``r`` stays in
    ``[throat_radius, bulb_radius]`` on the construction grid (before jitter).
    """
    if length <= 0 or throat_width <= 0:
        raise ValueError("length and throat_width must be positive")
    if throat_radius <= 0 or bulb_radius <= throat_radius:
        raise ValueError("require 0 < throat_radius < bulb_radius")
    if n_z < 2 or n_theta < 3:
        raise ValueError("n_z must be >= 2 and n_theta must be >= 3")
    rng = np.random.default_rng(seed)
    z1d = np.linspace(-0.5 * length, 0.5 * length, n_z, dtype=np.float64)
    theta = np.linspace(0.0, 2.0 * np.pi, n_theta, endpoint=False, dtype=np.float64)
    zz, tt = np.meshgrid(z1d, theta, indexing="ij")
    zc = zz.astype(np.float64)
    sigma = float(throat_width)
    z_l = -0.25 * length
    z_r = 0.25 * length
    bump = np.exp(-((zc - z_l) / sigma) ** 2) + np.exp(-((zc - z_r) / sigma) ** 2)
    s_max = float(np.max(bump))
    if s_max <= 0:
        raise ValueError("degenerate bump profile")
    rz = throat_radius + (bulb_radius - throat_radius) * (bump / s_max)
    r_min = float(np.min(rz))
    if r_min <= 0:
        raise ValueError("radius profile non-positive before jitter")
    x = (rz * np.cos(tt)).ravel()
    y = (rz * np.sin(tt)).ravel()
    z_flat = zc.ravel()
    pts = np.column_stack([x, y, z_flat])
    if jitter != 0.0:
        pts = pts + rng.normal(0.0, jitter, size=pts.shape)
    return pts.astype(np.float64, copy=False)


def _degree_stats(weights: sparse.csr_matrix) -> tuple[float, float, float, float]:
    deg = np.asarray(weights.sum(axis=1), dtype=np.float64).ravel()
    return float(deg.min()), float(deg.max()), float(deg.mean()), float(deg.std(ddof=0))


def _z_tercile_masses(z: np.ndarray, mass: np.ndarray) -> tuple[float, float, float]:
    """Mass fractions in z-low / z-mid / z-high thirds (by coordinate range)."""
    zmin = float(z.min())
    zmax = float(z.max())
    span = zmax - zmin + 1e-15
    t1 = zmin + span / 3.0
    t2 = zmin + 2.0 * span / 3.0
    m = mass / (np.sum(mass) + 1e-15)
    left = float(np.sum(m[z < t1]))
    center = float(np.sum(m[(z >= t1) & (z < t2)]))
    right = float(np.sum(m[z >= t2]))
    return left, center, right


def _z_center_of_mass(z: np.ndarray, mass: np.ndarray) -> float:
    m = mass / (np.sum(mass) + 1e-15)
    return float(np.sum(z * m))


def _nontrivial_mode_indices(evals: np.ndarray, *, tol: float = 1e-6) -> np.ndarray:
    return np.where(np.asarray(evals, dtype=float) > tol)[0]


def _compute_graph_modes(
    points: np.ndarray,
    k_neighbors: int,
    num_modes: int,
    epsilon: float | None,
) -> tuple[
    GraphLaplacianResult,
    list[ModeDiagnostics],
    np.ndarray,
    float | None,
    float,
    float,
    float,
    float,
]:
    n_points = points.shape[0]
    graph = build_knn_graph_laplacian(
        points,
        k=k_neighbors,
        epsilon=epsilon,
        normalized=True,
    )
    deg_min, deg_max, deg_mean, deg_std = _degree_stats(graph.weights)
    k_eig = min(n_points - 2, max(num_modes + 6, num_modes + 2))
    k_eig = max(k_eig, min(6, n_points - 2))
    evals, evecs = eigsh(graph.laplacian, k=k_eig, which="SM")
    evals = np.real(evals)
    evecs = np.real(evecs)
    order = np.argsort(evals)
    evals = evals[order]
    evecs = evecs[:, order]
    idx_nt = _nontrivial_mode_indices(evals, tol=1e-6)
    modes: list[ModeDiagnostics] = []
    z = points[:, 2]
    for j in idx_nt[:num_modes]:
        psi = evecs[:, int(j)]
        mass = psi * psi
        ipr = float(inverse_participation_ratio(psi))
        zl, zc, zr = _z_tercile_masses(z, mass)
        zcom = _z_center_of_mass(z, mass)
        modes.append(
            ModeDiagnostics(
                index=int(j),
                eigenvalue=float(evals[int(j)]),
                ipr=ipr,
                z_center_of_mass=zcom,
                z_mass_left=zl,
                z_mass_center=zc,
                z_mass_right=zr,
            )
        )
    gap: float | None = None
    pos = evals[evals > 1e-8]
    if pos.size >= 2:
        gap = float(pos[1] - pos[0])
    return graph, modes, z, gap, deg_min, deg_max, deg_mean, deg_std


def _common_mesh_gates(
    *,
    n_points: int,
    connected_components: int,
    degree_min: float,
    degree_max: float,
    degree_mean: float,
    degree_std: float,
    modes: list[ModeDiagnostics],
    z_coords: np.ndarray,
) -> tuple[bool, bool, bool, bool]:
    gate_graph = connected_components == 1
    cv = degree_std / (degree_mean + 1e-15)
    gate_deg = degree_min >= 1.0 and degree_max < n_points and cv <= 3.0
    inv_n = 1.0 / float(n_points)
    ipr_cap = max(120.0 * inv_n, 0.12)
    gate_ipr = all(m.ipr <= ipr_cap for m in modes) if modes else False
    zmin, zmax = float(z_coords.min()), float(z_coords.max())
    span = zmax - zmin + 1e-15
    edge_lo = zmin + 0.1 * span
    edge_hi = zmax - 0.1 * span

    def pinned(zc: float) -> bool:
        return zc < edge_lo or zc > edge_hi

    if not modes:
        gate_z = False
    else:
        all_pinned = all(pinned(m.z_center_of_mass) for m in modes)
        gate_z = not all_pinned
    return gate_graph, gate_deg, gate_ipr, gate_z


def assess_straight_cylinder_null(
    *,
    n_points: int,
    connected_components: int,
    degree_min: float,
    degree_max: float,
    degree_mean: float,
    degree_std: float,
    modes: list[ModeDiagnostics],
    z_coords: np.ndarray,
) -> tuple[bool, bool, bool, bool, str]:
    """Return gates and a short null-test verdict string."""
    g1, g2, g3, g4 = _common_mesh_gates(
        n_points=n_points,
        connected_components=connected_components,
        degree_min=degree_min,
        degree_max=degree_max,
        degree_mean=degree_mean,
        degree_std=degree_std,
        modes=modes,
        z_coords=z_coords,
    )
    if g1 and g2 and g3 and g4:
        verdict = "straight_cylinder_null_consistent"
    elif not g3 or not g4:
        verdict = "graph_artifact_risk"
    else:
        verdict = "straight_cylinder_precontrol_fail"
    return g1, g2, g3, g4, verdict


def assess_variable_radius_cylinder_control(
    *,
    n_points: int,
    connected_components: int,
    degree_min: float,
    degree_max: float,
    degree_mean: float,
    degree_std: float,
    modes: list[ModeDiagnostics],
    z_coords: np.ndarray,
    radial_extent_ratio: float,
) -> tuple[bool, bool, bool, bool, bool, str]:
    """Semi-analytic geometry control: mesh gates plus nontrivial radius profile."""
    g1, g2, g3, g4 = _common_mesh_gates(
        n_points=n_points,
        connected_components=connected_components,
        degree_min=degree_min,
        degree_max=degree_max,
        degree_mean=degree_mean,
        degree_std=degree_std,
        modes=modes,
        z_coords=z_coords,
    )
    g5 = radial_extent_ratio > 1e-3
    if not g5:
        verdict = "variable_radius_geometry_invalid"
    elif g1 and g2 and g3 and g4:
        verdict = "variable_radius_cylinder_precontrol_pass"
    elif not g3 or not g4:
        verdict = "graph_artifact_risk"
    else:
        verdict = "variable_radius_cylinder_precontrol_fail"
    return g1, g2, g3, g4, g5, verdict


def run_straight_cylinder_precontrol(cfg: StraightCylinderRunConfig) -> StraightCylinderPrecontrolResult:
    seed0 = cfg.seeds[0] if cfg.seeds else None
    points = build_straight_cylinder_points(
        cfg.radius,
        cfg.length,
        cfg.n_z,
        cfg.n_theta,
        jitter=cfg.jitter,
        seed=seed0,
    )
    n_points = points.shape[0]
    graph, modes, z, gap, deg_min, deg_max, deg_mean, deg_std = _compute_graph_modes(
        points,
        cfg.k_neighbors,
        cfg.num_modes,
        cfg.epsilon,
    )
    g1, g2, g3, g4, verdict = assess_straight_cylinder_null(
        n_points=n_points,
        connected_components=graph.connected_components,
        degree_min=deg_min,
        degree_max=deg_max,
        degree_mean=deg_mean,
        degree_std=deg_std,
        modes=modes,
        z_coords=z,
    )

    return StraightCylinderPrecontrolResult(
        config=cfg,
        n_points=n_points,
        connected_components=graph.connected_components,
        degree_min=deg_min,
        degree_max=deg_max,
        degree_mean=deg_mean,
        degree_std=deg_std,
        epsilon=float(graph.epsilon),
        spectral_gap=gap,
        modes=modes,
        gate_graph_connected=g1,
        gate_degree_non_pathological=g2,
        gate_ipr_not_extreme=g3,
        gate_z_center_not_all_boundary_pinned=g4,
        null_verdict=verdict,
        points=points,
    )


def run_variable_radius_cylinder_precontrol(
    cfg: VariableRadiusCylinderRunConfig,
) -> VariableRadiusCylinderPrecontrolResult:
    seed0 = cfg.seeds[0] if cfg.seeds else None
    points = build_variable_radius_cylinder_points(
        cfg.r0,
        cfg.length,
        cfg.n_z,
        cfg.n_theta,
        cfg.relative_radius_modulation,
        jitter=cfg.jitter,
        seed=seed0,
    )
    n_points = points.shape[0]
    r_xy = np.hypot(points[:, 0], points[:, 1])
    radial_extent_ratio = float((float(r_xy.max()) - float(r_xy.min())) / (float(r_xy.mean()) + 1e-15))
    graph, modes, z, gap, deg_min, deg_max, deg_mean, deg_std = _compute_graph_modes(
        points,
        cfg.k_neighbors,
        cfg.num_modes,
        cfg.epsilon,
    )
    g1, g2, g3, g4, g5, verdict = assess_variable_radius_cylinder_control(
        n_points=n_points,
        connected_components=graph.connected_components,
        degree_min=deg_min,
        degree_max=deg_max,
        degree_mean=deg_mean,
        degree_std=deg_std,
        modes=modes,
        z_coords=z,
        radial_extent_ratio=radial_extent_ratio,
    )
    return VariableRadiusCylinderPrecontrolResult(
        config=cfg,
        n_points=n_points,
        connected_components=graph.connected_components,
        degree_min=deg_min,
        degree_max=deg_max,
        degree_mean=deg_mean,
        degree_std=deg_std,
        epsilon=float(graph.epsilon),
        spectral_gap=gap,
        modes=modes,
        gate_graph_connected=g1,
        gate_degree_non_pathological=g2,
        gate_ipr_not_extreme=g3,
        gate_z_center_not_all_boundary_pinned=g4,
        gate_radius_profile_nontrivial=g5,
        control_verdict=verdict,
        points=points,
        radial_extent_ratio=radial_extent_ratio,
    )


def _dumbbell_zone_masses(z: np.ndarray, mass: np.ndarray, length: float) -> tuple[float, float, float]:
    """Left bulb / throat / right bulb mass fractions (symmetric z-bins, throat at center)."""
    hw = 0.125 * float(length)
    m = mass / (np.sum(mass) + 1e-15)
    left = float(np.sum(m[z < -hw]))
    throat = float(np.sum(m[(z >= -hw) & (z <= hw)]))
    right = float(np.sum(m[z > hw]))
    return left, throat, right


def _dumbbell_localization_label(left: float, throat: float, right: float) -> str:
    pairs = [("left_bulb", left), ("throat", throat), ("right_bulb", right)]
    pairs_sorted = sorted(pairs, key=lambda x: -x[1])
    top, second = pairs_sorted[0][1], pairs_sorted[1][1]
    if top < 0.34:
        return "delocalized"
    if top - second < 0.04:
        return "ambiguous"
    return str(pairs_sorted[0][0])


def _compute_graph_modes_dumbbell(
    points: np.ndarray,
    length: float,
    k_neighbors: int,
    num_modes: int,
    epsilon: float | None,
) -> tuple[
    GraphLaplacianResult,
    list[DumbbellModeDiagnostics],
    np.ndarray,
    float | None,
    float,
    float,
    float,
    float,
    float,
]:
    n_points = points.shape[0]
    graph = build_knn_graph_laplacian(
        points,
        k=k_neighbors,
        epsilon=epsilon,
        normalized=True,
    )
    deg_min, deg_max, deg_mean, deg_std = _degree_stats(graph.weights)
    k_eig = min(n_points - 2, max(num_modes + 6, num_modes + 2))
    k_eig = max(k_eig, min(6, n_points - 2))
    evals, evecs = eigsh(graph.laplacian, k=k_eig, which="SM")
    evals = np.real(evals)
    evecs = np.real(evecs)
    order = np.argsort(evals)
    evals = evals[order]
    evecs = evecs[:, order]
    idx_nt = _nontrivial_mode_indices(evals, tol=1e-6)
    modes: list[DumbbellModeDiagnostics] = []
    z = points[:, 2]
    for j in idx_nt[:num_modes]:
        psi = evecs[:, int(j)]
        mass = psi * psi
        ipr = float(inverse_participation_ratio(psi))
        zl, zc, zr = _z_tercile_masses(z, mass)
        zcom = _z_center_of_mass(z, mass)
        ml, mt, mr = _dumbbell_zone_masses(z, mass, length)
        tot = ml + mt + mr + 1e-15
        throat_frac = mt / tot
        bulb_frac = (ml + mr) / tot
        label = _dumbbell_localization_label(ml, mt, mr)
        sym = abs(ml - mr) / (ml + mr + 1e-15)
        modes.append(
            DumbbellModeDiagnostics(
                index=int(j),
                eigenvalue=float(evals[int(j)]),
                ipr=ipr,
                z_center_of_mass=zcom,
                z_mass_left=zl,
                z_mass_center=zc,
                z_mass_right=zr,
                mass_left_bulb=ml,
                mass_throat=mt,
                mass_right_bulb=mr,
                throat_mass_fraction=throat_frac,
                bulb_mass_fraction=bulb_frac,
                localization_region_label=label,
                mode_symmetry_left_right=float(sym),
            )
        )
    gap: float | None = None
    pos = evals[evals > 1e-8]
    if pos.size >= 2:
        gap = float(pos[1] - pos[0])
    mean_ipr = float(np.mean([m.ipr for m in modes])) if modes else float("nan")
    return graph, modes, z, gap, deg_min, deg_max, deg_mean, deg_std, mean_ipr


def _dumbbell_modes_to_jsonable(modes: list[DumbbellModeDiagnostics]) -> list[dict[str, Any]]:
    return [asdict(m) for m in modes]


def _run_single_dumbbell_case(
    *,
    length: float,
    throat_radius: float,
    bulb_radius: float,
    throat_width: float,
    n_z: int,
    n_theta: int,
    k_neighbors: int,
    num_modes: int,
    jitter: float,
    seed: int | None,
    epsilon: float | None,
) -> DumbbellCaseResult:
    pts = build_dumbbell_cylinder_points(
        length,
        throat_radius,
        bulb_radius,
        n_z,
        n_theta,
        throat_width,
        jitter=jitter,
        seed=seed,
    )
    n_points = pts.shape[0]
    graph, modes, z, gap, dmin, dmax, dmean, dstd, mean_ipr = _compute_graph_modes_dumbbell(
        pts,
        length,
        k_neighbors,
        num_modes,
        epsilon,
    )
    g1, g2, g3, g4 = _common_mesh_gates(
        n_points=n_points,
        connected_components=graph.connected_components,
        degree_min=dmin,
        degree_max=dmax,
        degree_mean=dmean,
        degree_std=dstd,
        modes=modes,
        z_coords=z,
    )
    return DumbbellCaseResult(
        throat_radius=throat_radius,
        bulb_radius=bulb_radius,
        throat_width=throat_width,
        k_neighbors=k_neighbors,
        length=length,
        n_points=n_points,
        connected_components=graph.connected_components,
        degree_min=dmin,
        degree_max=dmax,
        degree_mean=dmean,
        degree_std=dstd,
        epsilon=float(graph.epsilon),
        spectral_gap=gap,
        modes=modes,
        gate_graph_connected=g1,
        gate_degree_non_pathological=g2,
        gate_ipr_not_extreme=g3,
        gate_z_center_not_all_boundary_pinned=g4,
        mean_ipr_low_modes=mean_ipr,
    )


def _aggregate_dumbbell_tiny_verdict(cases: list[DumbbellCaseResult], throat_radii: tuple[float, ...]) -> tuple[str, dict[str, bool]]:
    """Return (aggregate_verdict, k_sensitivity_ok_by_throat_str)."""
    k_ok: dict[str, bool] = {}
    if any(not c.gate_graph_connected or not c.gate_degree_non_pathological for c in cases):
        return "graph_artifact_risk", {str(t): False for t in throat_radii}
    if any(not c.gate_ipr_not_extreme or not c.gate_z_center_not_all_boundary_pinned for c in cases):
        return "graph_artifact_risk", {str(t): False for t in throat_radii}

    by_t: dict[float, list[DumbbellCaseResult]] = {}
    for c in cases:
        by_t.setdefault(c.throat_radius, []).append(c)

    for t, rows in by_t.items():
        r8 = next((x for x in rows if x.k_neighbors == 8), None)
        r12 = next((x for x in rows if x.k_neighbors == 12), None)
        if r8 is None or r12 is None or not r8.modes or not r12.modes:
            k_ok[str(t)] = False
            continue
        m8, m12 = r8.modes[0], r12.modes[0]
        label_match = m8.localization_region_label == m12.localization_region_label
        ipr_tol = max(0.03, 0.25 * max(m8.ipr, m12.ipr, 1e-9))
        ipr_close = abs(m8.ipr - m12.ipr) <= ipr_tol
        throat_close = abs(m8.throat_mass_fraction - m12.throat_mass_fraction) <= 0.08
        k_ok[str(t)] = bool(label_match and ipr_close and throat_close)

    if not all(k_ok.values()):
        return "graph_artifact_risk", k_ok

    def first_signal(c: DumbbellCaseResult) -> bool:
        if not c.modes:
            return False
        m0 = c.modes[0]
        return m0.localization_region_label == "throat" and m0.throat_mass_fraction >= 0.32

    sig_by_t: dict[float, bool] = {}
    for t in throat_radii:
        row8 = next((x for x in cases if x.throat_radius == t and x.k_neighbors == 8), None)
        row12 = next((x for x in cases if x.throat_radius == t and x.k_neighbors == 12), None)
        sig_by_t[t] = bool(row8 and row12 and first_signal(row8) and first_signal(row12))

    tr_sorted = sorted(throat_radii)
    min_t, max_t = tr_sorted[0], tr_sorted[-1]
    if sig_by_t.get(min_t) and not sig_by_t.get(max_t):
        return "threshold_geometry_sensitivity", k_ok
    if sig_by_t.get(max_t) or (sig_by_t.get(min_t) and sig_by_t.get(max_t)):
        if any(c.modes and c.modes[0].mode_symmetry_left_right > 0.42 for c in cases):
            return "sampling_artifact_risk", k_ok
        return "dumbbell_signal_candidate", k_ok

    if any(c.modes and c.modes[0].mode_symmetry_left_right > 0.42 for c in cases):
        return "sampling_artifact_risk", k_ok
    return "dumbbell_null_or_weak_signal", k_ok


def run_dumbbell_tiny_diagnostic(cfg: DumbbellTinyRunConfig) -> DumbbellTinyDiagnosticResult:
    seed0 = cfg.seeds[0] if cfg.seeds else None
    cases: list[DumbbellCaseResult] = []
    for tr in cfg.throat_radii:
        for k in cfg.k_values:
            cases.append(
                _run_single_dumbbell_case(
                    length=cfg.length,
                    throat_radius=float(tr),
                    bulb_radius=cfg.bulb_radius,
                    throat_width=cfg.throat_width,
                    n_z=cfg.n_z,
                    n_theta=cfg.n_theta,
                    k_neighbors=int(k),
                    num_modes=cfg.num_modes,
                    jitter=cfg.jitter,
                    seed=seed0,
                    epsilon=cfg.epsilon,
                )
            )
    verdict, k_ok = _aggregate_dumbbell_tiny_verdict(cases, cfg.throat_radii)
    return DumbbellTinyDiagnosticResult(
        config=cfg,
        cases=cases,
        aggregate_verdict=verdict,
        k_sensitivity_ok_by_throat=k_ok,
        formula_documentation=DUMBBELL_RADIUS_FORMULA_DOC,
        precontrol_straight_run="reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny",
        precontrol_variable_run="reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny",
    )


def save_dumbbell_tiny_diagnostic_artifacts(result: DumbbellTinyDiagnosticResult, run_dir: Path) -> dict[str, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    (run_dir / "figures" / ".placeholder").write_text(
        "Figures reserved for dumbbell / throat localization diagnostics.\n", encoding="utf-8"
    )

    cfg_out: dict[str, Any] = {
        "profile": "dumbbell_tiny",
        "baseline_tag": "v0.1.14-mvp-s2-s1-discretization-v2-full",
        "bulb_radius": result.config.bulb_radius,
        "epsilon_override": result.config.epsilon,
        "formula_documentation": result.formula_documentation,
        "jitter": result.config.jitter,
        "k_values": list(result.config.k_values),
        "length": result.config.length,
        "n_theta": result.config.n_theta,
        "n_z": result.config.n_z,
        "num_modes": result.config.num_modes,
        "precontrol_straight_run": result.precontrol_straight_run,
        "precontrol_variable_run": result.precontrol_variable_run,
        "seeds": list(result.config.seeds),
        "throat_radii": list(result.config.throat_radii),
        "throat_width": result.config.throat_width,
    }
    (run_dir / "config.json").write_text(json.dumps(cfg_out, indent=2, sort_keys=True), encoding="utf-8")

    case_rows: list[dict[str, Any]] = []
    for c in result.cases:
        case_rows.append(
            {
                "throat_radius": c.throat_radius,
                "bulb_radius": c.bulb_radius,
                "throat_width": c.throat_width,
                "k_neighbors": c.k_neighbors,
                "length": c.length,
                "n_points": c.n_points,
                "connected_components": c.connected_components,
                "degree_min": c.degree_min,
                "degree_max": c.degree_max,
                "degree_mean": c.degree_mean,
                "degree_std": c.degree_std,
                "epsilon": c.epsilon,
                "spectral_gap": c.spectral_gap,
                "mean_ipr_low_modes": c.mean_ipr_low_modes,
                "gate_graph_connected": c.gate_graph_connected,
                "gate_degree_non_pathological": c.gate_degree_non_pathological,
                "gate_ipr_not_extreme": c.gate_ipr_not_extreme,
                "gate_z_center_not_all_boundary_pinned": c.gate_z_center_not_all_boundary_pinned,
                "low_modes": _dumbbell_modes_to_jsonable(c.modes),
            }
        )

    metrics: dict[str, Any] = {
        "aggregate_verdict": result.aggregate_verdict,
        "cases": case_rows,
        "formula_documentation": result.formula_documentation,
        "k_sensitivity_ok_by_throat": result.k_sensitivity_ok_by_throat,
        "precontrol_straight_run": result.precontrol_straight_run,
        "precontrol_variable_run": result.precontrol_variable_run,
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")

    ref = next(
        (c for c in result.cases if c.throat_radius == max(result.config.throat_radii) and c.k_neighbors == 12),
        result.cases[-1],
    )
    pts = build_dumbbell_cylinder_points(
        result.config.length,
        ref.throat_radius,
        ref.bulb_radius,
        result.config.n_z,
        result.config.n_theta,
        result.config.throat_width,
        jitter=result.config.jitter,
        seed=result.config.seeds[0] if result.config.seeds else None,
    )
    r_xy = np.hypot(pts[:, 0], pts[:, 1])
    np.savez_compressed(
        run_dir / "data.npz",
        points=pts,
        z=pts[:, 2],
        r_xy=r_xy,
        reference_case_throat_radius=ref.throat_radius,
        reference_case_k_neighbors=ref.k_neighbors,
    )

    summary = _render_dumbbell_tiny_summary_md(result)
    (run_dir / "summary.md").write_text(summary, encoding="utf-8")

    return {
        "config": run_dir / "config.json",
        "metrics": run_dir / "metrics.json",
        "data": run_dir / "data.npz",
        "summary": run_dir / "summary.md",
        "figures": run_dir / "figures",
    }


def _render_dumbbell_tiny_summary_md(result: DumbbellTinyDiagnosticResult) -> str:
    rows = []
    for c in result.cases:
        m0 = c.modes[0] if c.modes else None
        lab = m0.localization_region_label if m0 else "n/a"
        tm = m0.throat_mass_fraction if m0 else float("nan")
        ipr0 = m0.ipr if m0 else float("nan")
        rows.append(
            f"| {c.throat_radius} | {c.k_neighbors} | {c.connected_components} | "
            f"{c.mean_ipr_low_modes:.5g} | {ipr0:.5g} | {lab} | {tm:.4f} | {c.gate_graph_connected} |"
        )
    table = "\n".join(rows)
    krows = "\n".join(f"| `{t}` | **{ok}** |" for t, ok in sorted(result.k_sensitivity_ok_by_throat.items()))
    return f"""# Geometric localization — dumbbell tiny diagnostic

## Geometry formula (implemented)

{DUMBBELL_RADIUS_FORMULA_DOC}

## Configuration

- `length`: {result.config.length}
- `n_z`, `n_theta`: {result.config.n_z}, {result.config.n_theta}
- `throat_radii`: {list(result.config.throat_radii)}
- `bulb_radius`: {result.config.bulb_radius}
- `throat_width` (Gaussian σ): {result.config.throat_width}
- `k_values`: {list(result.config.k_values)}
- `num_modes`: {result.config.num_modes}
- `seeds`: {list(result.config.seeds)}
- `jitter`: {result.config.jitter}

## Pre-control references (must remain on record)

- Straight null: `{result.precontrol_straight_run}` (`straight_cylinder_null_consistent`).
- Variable-radius control: `{result.precontrol_variable_run}`
  (`variable_radius_cylinder_precontrol_pass`).

## Case summary

| throat_radius | k | components | mean IPR (low modes) | mode0 IPR | mode0 label | mode0 throat_mass_frac | graph_ok |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
{table}

## k-sensitivity (mode0 label + IPR + throat mass, k=8 vs k=12)

| throat_radius | k_sensitivity_ok |
| --- | ---: |
{krows}

## Aggregate verdict

**`{result.aggregate_verdict}`**

## Scientific non-claims

- Not geometric localization proof.
- Not continuum compactification.
- Not `S6` / `S3 x S6` validation.
- Not Standard Model physics.
- Not physical chirality proof.
- Not Witten/Lichnerowicz bypass.
- Baseline tag is **not** promoted by this diagnostic.
"""


def _modes_to_jsonable(modes: list[ModeDiagnostics]) -> list[dict[str, Any]]:
    return [asdict(m) for m in modes]


def save_straight_cylinder_precontrol_artifacts(
    result: StraightCylinderPrecontrolResult,
    run_dir: Path,
) -> dict[str, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    (run_dir / "figures" / ".placeholder").write_text(
        "Figures reserved for future geometric localization diagnostics.\n", encoding="utf-8"
    )

    cfg_out = {
        "profile": "straight_cylinder_tiny",
        "radius": result.config.radius,
        "length": result.config.length,
        "n_z": result.config.n_z,
        "n_theta": result.config.n_theta,
        "k_neighbors": result.config.k_neighbors,
        "num_modes": result.config.num_modes,
        "seeds": list(result.config.seeds),
        "jitter": result.config.jitter,
        "epsilon_override": result.config.epsilon,
        "baseline_tag": "v0.1.14-mvp-s2-s1-discretization-v2-full",
    }
    (run_dir / "config.json").write_text(json.dumps(cfg_out, indent=2, sort_keys=True), encoding="utf-8")

    metrics: dict[str, Any] = {
        "connected_components": result.connected_components,
        "degree_min": result.degree_min,
        "degree_max": result.degree_max,
        "degree_mean": result.degree_mean,
        "degree_std": result.degree_std,
        "epsilon": result.epsilon,
        "n_points": result.n_points,
        "spectral_gap": result.spectral_gap,
        "gate_graph_connected": result.gate_graph_connected,
        "gate_degree_non_pathological": result.gate_degree_non_pathological,
        "gate_ipr_not_extreme": result.gate_ipr_not_extreme,
        "gate_z_center_not_all_boundary_pinned": result.gate_z_center_not_all_boundary_pinned,
        "null_verdict": result.null_verdict,
        "low_modes": _modes_to_jsonable(result.modes),
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")

    low_evals = np.array([m.eigenvalue for m in result.modes], dtype=np.float64)
    np.savez_compressed(
        run_dir / "data.npz",
        points=result.points,
        z=result.points[:, 2],
        low_eigenvalues=low_evals,
    )

    summary = _render_summary_md(result)
    (run_dir / "summary.md").write_text(summary, encoding="utf-8")

    return {
        "config": run_dir / "config.json",
        "metrics": run_dir / "metrics.json",
        "data": run_dir / "data.npz",
        "summary": run_dir / "summary.md",
        "figures": run_dir / "figures",
    }


def save_variable_radius_cylinder_precontrol_artifacts(
    result: VariableRadiusCylinderPrecontrolResult,
    run_dir: Path,
) -> dict[str, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    (run_dir / "figures" / ".placeholder").write_text(
        "Figures reserved for future geometric localization diagnostics.\n", encoding="utf-8"
    )

    cfg_out = {
        "profile": "variable_radius_cylinder_tiny",
        "r0": result.config.r0,
        "length": result.config.length,
        "n_z": result.config.n_z,
        "n_theta": result.config.n_theta,
        "relative_radius_modulation": result.config.relative_radius_modulation,
        "k_neighbors": result.config.k_neighbors,
        "num_modes": result.config.num_modes,
        "seeds": list(result.config.seeds),
        "jitter": result.config.jitter,
        "epsilon_override": result.config.epsilon,
        "baseline_tag": "v0.1.14-mvp-s2-s1-discretization-v2-full",
    }
    (run_dir / "config.json").write_text(json.dumps(cfg_out, indent=2, sort_keys=True), encoding="utf-8")

    metrics: dict[str, Any] = {
        "connected_components": result.connected_components,
        "degree_min": result.degree_min,
        "degree_max": result.degree_max,
        "degree_mean": result.degree_mean,
        "degree_std": result.degree_std,
        "epsilon": result.epsilon,
        "n_points": result.n_points,
        "spectral_gap": result.spectral_gap,
        "radial_extent_ratio": result.radial_extent_ratio,
        "gate_graph_connected": result.gate_graph_connected,
        "gate_degree_non_pathological": result.gate_degree_non_pathological,
        "gate_ipr_not_extreme": result.gate_ipr_not_extreme,
        "gate_z_center_not_all_boundary_pinned": result.gate_z_center_not_all_boundary_pinned,
        "gate_radius_profile_nontrivial": result.gate_radius_profile_nontrivial,
        "control_verdict": result.control_verdict,
        "low_modes": _modes_to_jsonable(result.modes),
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")

    low_evals = np.array([m.eigenvalue for m in result.modes], dtype=np.float64)
    r_xy = np.hypot(result.points[:, 0], result.points[:, 1])
    np.savez_compressed(
        run_dir / "data.npz",
        points=result.points,
        z=result.points[:, 2],
        r_xy=r_xy,
        low_eigenvalues=low_evals,
    )

    summary = _render_variable_radius_summary_md(result)
    (run_dir / "summary.md").write_text(summary, encoding="utf-8")

    return {
        "config": run_dir / "config.json",
        "metrics": run_dir / "metrics.json",
        "data": run_dir / "data.npz",
        "summary": run_dir / "summary.md",
        "figures": run_dir / "figures",
    }


def _render_summary_md(result: StraightCylinderPrecontrolResult) -> str:
    modes_rows = "\n".join(
        f"| {m.index} | {m.eigenvalue:.6g} | {m.ipr:.6g} | {m.z_center_of_mass:.6g} | "
        f"{m.z_mass_left:.4f} | {m.z_mass_center:.4f} | {m.z_mass_right:.4f} |"
        for m in result.modes
    )
    return f"""# Geometric localization pre-control — straight cylinder (tiny)

## Purpose

Null geometry on a **straight cylinder** point cloud: check that the **kNN graph
Laplacian** pipeline does not show **stable artificial** low-mode localization
from sampling / graph construction alone (see
`reports/GEOMETRIC_LOCALIZATION_PRECONTROL_PLAN.md`).

## Configuration

- `n_points`: {result.n_points}
- `k_neighbors`: {result.config.k_neighbors}
- `epsilon` (heat kernel scale): {result.epsilon:.6g}
- `connected_components`: {result.connected_components}

## Graph degree statistics

| stat | value |
| --- | ---: |
| degree_min | {result.degree_min:.6g} |
| degree_max | {result.degree_max:.6g} |
| degree_mean | {result.degree_mean:.6g} |
| degree_std | {result.degree_std:.6g} |

## Spectrum (low nontrivial modes)

Spectral gap (smallest positive eigen-subgap heuristic): `{result.spectral_gap}`.

| mode_idx | eigenvalue | IPR | z_center_of_mass | z_mass_left | z_mass_center | z_mass_right |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{modes_rows}

## Gates

- `gate_graph_connected`: **{result.gate_graph_connected}**
- `gate_degree_non_pathological`: **{result.gate_degree_non_pathological}**
- `gate_ipr_not_extreme` (vs ~1/N slack): **{result.gate_ipr_not_extreme}**
- `gate_z_center_not_all_boundary_pinned`: **{result.gate_z_center_not_all_boundary_pinned}**

## Null-test verdict

**`{result.null_verdict}`**

If this reads `graph_artifact_risk`, treat later dumbbell / variable-radius runs
as **not interpretable** until the graph construction is revised. If
`straight_cylinder_null_consistent`, the **next** planned step is the
**variable-radius cylinder** control (`--variable-radius-cylinder --tiny` on
this CLI).

## Scientific non-claims

- Not geometric localization proof.
- Not continuum compactification.
- Not `S6` / `S3 x S6` validation.
- Not Standard Model physics.
- Not physical chirality proof.
- Not Witten/Lichnerowicz bypass.
- Baseline tag is **not** promoted by this diagnostic.
"""


def _render_variable_radius_summary_md(result: VariableRadiusCylinderPrecontrolResult) -> str:
    modes_rows = "\n".join(
        f"| {m.index} | {m.eigenvalue:.6g} | {m.ipr:.6g} | {m.z_center_of_mass:.6g} | "
        f"{m.z_mass_left:.4f} | {m.z_mass_center:.4f} | {m.z_mass_right:.4f} |"
        for m in result.modes
    )
    return f"""# Geometric localization pre-control — variable-radius cylinder (tiny)

## Purpose

**Semi-analytic geometry control** after the straight-cylinder null: same kNN
graph Laplacian pipeline on a surface with **nontrivial** ``r(z)`` profile
(see `reports/GEOMETRIC_LOCALIZATION_PRECONTROL_PLAN.md`). Records low-mode IPR
and z-mass diagnostics; does **not** assert curvature-driven localization.

## Geometry

Axisymmetric modulation: ``r(z) = r0 * (1 + a * cos(2*pi*z/length))`` with
``r0={result.config.r0}``, ``a={result.config.relative_radius_modulation}``,
``length={result.config.length}``.

- Sample ``radial_extent_ratio`` (max-min)/mean on points: **{result.radial_extent_ratio:.6g}**

## Configuration

- `n_points`: {result.n_points}
- `k_neighbors`: {result.config.k_neighbors}
- `epsilon` (heat kernel scale): {result.epsilon:.6g}
- `connected_components`: {result.connected_components}

## Graph degree statistics

| stat | value |
| --- | ---: |
| degree_min | {result.degree_min:.6g} |
| degree_max | {result.degree_max:.6g} |
| degree_mean | {result.degree_mean:.6g} |
| degree_std | {result.degree_std:.6g} |

## Spectrum (low nontrivial modes)

Spectral gap (smallest positive eigen-subgap heuristic): `{result.spectral_gap}`.

| mode_idx | eigenvalue | IPR | z_center_of_mass | z_mass_left | z_mass_center | z_mass_right |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{modes_rows}

## Gates

- `gate_graph_connected`: **{result.gate_graph_connected}**
- `gate_degree_non_pathological`: **{result.gate_degree_non_pathological}**
- `gate_ipr_not_extreme` (vs ~1/N slack): **{result.gate_ipr_not_extreme}**
- `gate_z_center_not_all_boundary_pinned`: **{result.gate_z_center_not_all_boundary_pinned}**
- `gate_radius_profile_nontrivial`: **{result.gate_radius_profile_nontrivial}**

## Control verdict

**`{result.control_verdict}`**

- `variable_radius_cylinder_precontrol_pass`: mesh gates satisfied and radius
  profile is nontrivial; **dumbbell** remains **future** work with the same
  artifact battery.
- `graph_artifact_risk`: same interpretation as straight-cylinder pre-control.
- `variable_radius_geometry_invalid`: modulation too small or degenerate
  sampling; fix parameters before interpreting spectra.

## Scientific non-claims

- Not geometric localization proof.
- Not continuum compactification.
- Not `S6` / `S3 x S6` validation.
- Not Standard Model physics.
- Not physical chirality proof.
- Not Witten/Lichnerowicz bypass.
- Baseline tag is **not** promoted by this diagnostic.
"""


def tiny_straight_cylinder_config() -> StraightCylinderRunConfig:
    return StraightCylinderRunConfig(
        radius=1.0,
        length=4.0,
        n_z=24,
        n_theta=32,
        k_neighbors=12,
        num_modes=8,
        seeds=(123,),
        jitter=0.0,
        epsilon=None,
    )


def tiny_variable_radius_cylinder_config() -> VariableRadiusCylinderRunConfig:
    return VariableRadiusCylinderRunConfig(
        r0=1.0,
        length=4.0,
        n_z=24,
        n_theta=32,
        relative_radius_modulation=0.22,
        k_neighbors=12,
        num_modes=8,
        seeds=(123,),
        jitter=0.0,
        epsilon=None,
    )


def tiny_dumbbell_config() -> DumbbellTinyRunConfig:
    return DumbbellTinyRunConfig()
