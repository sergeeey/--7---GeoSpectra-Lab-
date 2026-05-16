from __future__ import annotations

import numpy as np

S1_INHOMOGENEITY_MODES = ("clean", "gauge_phase", "geometric_weight")
S1_DISCRETIZATION_FAMILIES = ("spectral_circle", "ring", "wilson_ring")


def build_s1_ring_operator(size: int, alpha: float, radius: float = 1.0) -> np.ndarray:
    """Build a Hermitian nearest-neighbor ring operator with twisted boundary phase."""
    _validate_size_and_radius(size=size, radius=radius)
    shift = _twisted_shift_matrix(size=size, alpha=alpha)
    scale = float(size) / float(radius)
    operator = (-0.5j * scale) * (shift - shift.conj().T)
    return _hermitize(operator)


def build_s1_wilson_operator(
    size: int,
    alpha: float,
    radius: float = 1.0,
    wilson_strength: float = 0.5,
) -> np.ndarray:
    """Build a Hermitian Wilson-like ring operator with a Laplacian correction."""
    _validate_size_and_radius(size=size, radius=radius)
    if wilson_strength < 0:
        raise ValueError("wilson_strength must be non-negative")

    shift = _twisted_shift_matrix(size=size, alpha=alpha)
    identity = np.eye(size, dtype=complex)
    ring = build_s1_ring_operator(size=size, alpha=alpha, radius=radius)
    scale = float(size) / float(radius)
    wilson_term = 0.5 * wilson_strength * scale * (2.0 * identity - shift - shift.conj().T)
    return _hermitize(ring + wilson_term)


def build_s1_operator(
    size: int,
    alpha: float,
    family: str,
    mode: str,
    disorder_strength: float,
    seed: int | None,
    radius: float = 1.0,
    wilson_strength: float = 0.5,
) -> np.ndarray:
    """Build a dense Hermitian toy S1 operator for one discretization family."""
    _validate_size_and_radius(size=size, radius=radius)
    if disorder_strength < 0:
        raise ValueError("disorder_strength must be non-negative")
    if family not in S1_DISCRETIZATION_FAMILIES:
        raise ValueError(f"unknown S1 discretization family: {family}")
    if mode not in S1_INHOMOGENEITY_MODES:
        raise ValueError(f"unknown S1 inhomogeneity mode: {mode}")

    if family == "spectral_circle":
        clean = _build_spectral_circle_operator(size=size, alpha=alpha, radius=radius)
    elif family == "ring":
        clean = build_s1_ring_operator(size=size, alpha=alpha, radius=radius)
    else:
        clean = build_s1_wilson_operator(size=size, alpha=alpha, radius=radius, wilson_strength=wilson_strength)

    if mode == "clean" or disorder_strength == 0.0:
        return clean

    rng = np.random.default_rng(seed)
    if mode == "gauge_phase":
        onsite = rng.normal(loc=0.0, scale=disorder_strength / 2.0, size=size)
        operator = clean + np.diag(onsite.astype(float))
    else:
        eta = np.clip(rng.normal(loc=0.0, scale=0.12 * disorder_strength, size=size), -2.0, 2.0)
        g_inv_sqrt = np.diag(np.exp(-0.5 * eta))
        weighted = g_inv_sqrt @ clean @ g_inv_sqrt
        operator = 0.5 * (weighted + weighted.conj().T)
    return _hermitize(operator)


def _build_spectral_circle_operator(size: int, alpha: float, radius: float) -> np.ndarray:
    modes = np.fft.fftfreq(size, d=1.0 / size)
    twisted_momenta = (modes + float(alpha)) / float(radius)
    dft = _unitary_dft_matrix(size)
    operator = dft.conj().T @ np.diag(twisted_momenta.astype(float)) @ dft
    return _hermitize(operator)


def _twisted_shift_matrix(size: int, alpha: float) -> np.ndarray:
    phase = np.exp(2j * np.pi * float(alpha) / float(size))
    shift = np.zeros((size, size), dtype=complex)
    for index in range(size):
        shift[index, (index + 1) % size] = phase
    return shift


def _unitary_dft_matrix(size: int) -> np.ndarray:
    grid = np.arange(size, dtype=float)
    phase = np.exp(2j * np.pi * np.outer(grid, grid) / float(size))
    return phase / np.sqrt(float(size))


def _validate_size_and_radius(size: int, radius: float) -> None:
    if size < 1:
        raise ValueError("size must be >= 1")
    if radius <= 0:
        raise ValueError("radius must be positive")


def _hermitize(matrix: np.ndarray) -> np.ndarray:
    dense = np.asarray(matrix, dtype=complex)
    return 0.5 * (dense + dense.conj().T)
