from __future__ import annotations


def known_sphere_betti(dimension: int) -> dict[int, int]:
    if dimension < 1:
        raise ValueError("dimension must be >= 1")
    return {0: 1, dimension: 1}
