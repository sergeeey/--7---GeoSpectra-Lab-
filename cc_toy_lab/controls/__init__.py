"""Negative control operators for specificity testing (v0.1.22).

DO NOT use these for positive S³×S¹ validation claims.
Purpose: falsification-first testing of harness discrimination power.
"""

from cc_toy_lab.controls.negative_controls import (
    build_random_hermitian_control,
    build_scrambled_geometry_control,
    build_broken_wilson_control,
)

__all__ = [
    "build_random_hermitian_control",
    "build_scrambled_geometry_control",
    "build_broken_wilson_control",
]
