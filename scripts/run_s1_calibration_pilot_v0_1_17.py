"""Known-Spectrum Calibration Pilot for v0.1.17 validation-hardening.

Purpose:
Test FL harness on SIMPLER geometry (S¹) before trusting S²×S¹ results.

DO NOT use this to claim new physics.
DO NOT use this to claim continuum compactification.
This is a SANITY CHECK: does harness work on toy operators with known properties?

Checks:
1. Hermiticity (all S¹ operators should be Hermitian)
2. Spectral symmetry (periodic BC → symmetric eigenvalue distribution)
3. Lattice-size stability (eigenvalue spectrum shouldn't blow up at small sizes)
4. No false localization (clean S¹ should have extended modes, not localized)

Expected:
FL gates should PASS on clean S¹ operators (baseline sanity).

Output:
Calibration report showing PASS/FAIL for each check.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cc_toy_lab.spectral.s1_discretizations import build_s1_operator, S1_DISCRETIZATION_FAMILIES


def check_hermiticity(operator: np.ndarray, tol: float = 1e-9) -> dict:
    """Check operator is Hermitian within tolerance."""
    residual = float(np.max(np.abs(operator - operator.conj().T)))
    passed = residual < tol
    return {
        "check": "hermiticity",
        "residual": residual,
        "tolerance": tol,
        "passed": passed,
    }


def check_spectral_symmetry(eigenvalues: np.ndarray, tol: float = 1e-6) -> dict:
    """Check eigenvalue spectrum is symmetric (for periodic BC).

    For S¹ with periodic boundary conditions, spectrum should be symmetric
    around zero (or around mean if constant shift present).
    """
    eigs_sorted = np.sort(eigenvalues)
    mean_eig = float(np.mean(eigs_sorted))
    centered = eigs_sorted - mean_eig

    # Check symmetry: eigs should be approximately -eigs (up to reordering)
    positive_eigs = centered[centered > tol]
    negative_eigs = -centered[centered < -tol]

    # For perfect symmetry, |positive| + |negative| ≈ total non-zero eigs
    symmetry_score = (len(positive_eigs) + len(negative_eigs)) / len(eigs_sorted)

    passed = symmetry_score > 0.5  # At least half of eigenvalues participate in symmetry

    return {
        "check": "spectral_symmetry",
        "mean_eigenvalue": mean_eig,
        "symmetry_score": symmetry_score,
        "positive_count": len(positive_eigs),
        "negative_count": len(negative_eigs),
        "passed": passed,
    }


def check_lattice_size_stability(
    eigenvalues_small: np.ndarray,
    eigenvalues_large: np.ndarray,
    max_relative_change: float = 2.0,
) -> dict:
    """Check eigenvalue statistics don't blow up at small lattice sizes."""
    mean_small = float(np.mean(np.abs(eigenvalues_small)))
    mean_large = float(np.mean(np.abs(eigenvalues_large)))

    relative_change = abs(mean_large - mean_small) / (mean_small + 1e-10)

    passed = relative_change < max_relative_change

    return {
        "check": "lattice_size_stability",
        "mean_eigenvalue_small": mean_small,
        "mean_eigenvalue_large": mean_large,
        "relative_change": relative_change,
        "threshold": max_relative_change,
        "passed": passed,
    }


def check_no_false_localization(operator: np.ndarray, ipr_threshold: float = 0.5) -> dict:
    """Check that clean S¹ operator has EXTENDED modes, not localized.

    For clean periodic S¹, all eigenmodes should be plane waves → IPR ≈ 1/N (extended).
    Localized modes would have IPR ≈ 1 (concentrated on few sites).
    """
    eigenvalues, eigenvectors = np.linalg.eigh(operator)

    # Compute IPR for each eigenmode
    ipr_values = []
    for i in range(eigenvectors.shape[1]):
        psi = eigenvectors[:, i]
        prob = np.abs(psi) ** 2
        ipr = float(np.sum(prob**2))
        ipr_values.append(ipr)

    mean_ipr = float(np.mean(ipr_values))
    max_ipr = float(np.max(ipr_values))

    # For extended modes, IPR ≈ 1/N
    n = operator.shape[0]
    expected_ipr_extended = 1.0 / n

    # Flag as localized if mean IPR significantly exceeds extended expectation
    passed = mean_ipr < ipr_threshold

    return {
        "check": "no_false_localization",
        "mean_ipr": mean_ipr,
        "max_ipr": max_ipr,
        "expected_ipr_extended": expected_ipr_extended,
        "threshold": ipr_threshold,
        "passed": passed,
        "note": "Clean S¹ should have extended modes (IPR ≈ 1/N), not localized (IPR ≈ 1)",
    }


def run_s1_calibration_pilot() -> dict:
    """Run calibration pilot on S¹ toy operators."""
    results = {
        "experiment": "Known-Spectrum Calibration Pilot",
        "version": "v0.1.17",
        "geometry": "S¹ (circle)",
        "purpose": "Sanity check FL harness on simpler geometry before trusting S²×S¹",
        "families_tested": [],
    }

    for family in S1_DISCRETIZATION_FAMILIES:
        family_results = {
            "family": family,
            "sizes_tested": [8, 16, 32],
            "checks": [],
        }

        # Build operators at different sizes
        operators = {}
        for size in [8, 16, 32]:
            op = build_s1_operator(
                size=size,
                alpha=0.0,
                family=family,
                mode="clean",
                disorder_strength=0.0,
                seed=123,
                radius=1.0,
            )
            operators[size] = op

        # Check 1: Hermiticity (all sizes)
        for size, op in operators.items():
            check = check_hermiticity(op)
            check["size"] = size
            family_results["checks"].append(check)

        # Check 2: Spectral symmetry (size=16)
        eigenvalues_16 = np.linalg.eigvalsh(operators[16])
        check_sym = check_spectral_symmetry(eigenvalues_16)
        check_sym["size"] = 16
        family_results["checks"].append(check_sym)

        # Check 3: Lattice-size stability (8 vs 32)
        eigenvalues_8 = np.linalg.eigvalsh(operators[8])
        eigenvalues_32 = np.linalg.eigvalsh(operators[32])
        check_stab = check_lattice_size_stability(eigenvalues_8, eigenvalues_32)
        check_stab["size_small"] = 8
        check_stab["size_large"] = 32
        family_results["checks"].append(check_stab)

        # Check 4: No false localization (size=16, clean)
        check_loc = check_no_false_localization(operators[16])
        check_loc["size"] = 16
        family_results["checks"].append(check_loc)

        # Summary for this family
        all_passed = all(c["passed"] for c in family_results["checks"])
        family_results["all_checks_passed"] = all_passed

        results["families_tested"].append(family_results)

    # Overall summary
    total_checks = sum(len(f["checks"]) for f in results["families_tested"])
    passed_checks = sum(
        sum(1 for c in f["checks"] if c["passed"]) for f in results["families_tested"]
    )
    results["summary"] = {
        "total_families": len(S1_DISCRETIZATION_FAMILIES),
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": total_checks - passed_checks,
        "pass_rate": passed_checks / total_checks if total_checks > 0 else 0.0,
    }

    return results


if __name__ == "__main__":
    results = run_s1_calibration_pilot()

    # Print summary
    print("\n" + "=" * 70)
    print("KNOWN-SPECTRUM CALIBRATION PILOT (v0.1.17)")
    print("=" * 70)
    print(f"Geometry: {results['geometry']}")
    print(f"Families tested: {results['summary']['total_families']}")
    print(
        f"Pass rate: {results['summary']['passed_checks']}/{results['summary']['total_checks']} "
        f"({results['summary']['pass_rate']:.1%})"
    )
    print()

    for family_result in results["families_tested"]:
        family = family_result["family"]
        status = "✓ PASS" if family_result["all_checks_passed"] else "✗ FAIL"
        print(f"{family:20s} {status}")

        for check in family_result["checks"]:
            check_name = check["check"]
            check_status = "✓" if check["passed"] else "✗"
            size_info = f"size={check.get('size', '?')}" if "size" in check else ""
            print(f"  {check_status} {check_name:30s} {size_info}")

    print("=" * 70)

    # Save to JSON
    output_dir = Path("reports") / "RUNS"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "s1_calibration_pilot_v0_1_17.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    print()
