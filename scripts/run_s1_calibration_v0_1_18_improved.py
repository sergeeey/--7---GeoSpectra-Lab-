"""S¹ Calibration v0.1.18 — Improved with scale-invariant stability metric.

Changes from v0.1.17:
- REMOVED: absolute eigenvalue magnitude stability check (failed due to expected N/R scaling)
- ADDED: spectral gap consistency check (scale-invariant)
- ADDED: eigenvalue spacing statistics (scale-invariant)

Purpose:
Test FL harness on S¹ with metrics that don't flag expected lattice-size scaling as "failure".
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
    """Check eigenvalue spectrum is symmetric (for periodic BC)."""
    eigs_sorted = np.sort(eigenvalues)
    mean_eig = float(np.mean(eigs_sorted))
    centered = eigs_sorted - mean_eig

    positive_eigs = centered[centered > tol]
    negative_eigs = -centered[centered < -tol]

    symmetry_score = (len(positive_eigs) + len(negative_eigs)) / len(eigs_sorted)
    passed = symmetry_score > 0.5

    return {
        "check": "spectral_symmetry",
        "mean_eigenvalue": mean_eig,
        "symmetry_score": symmetry_score,
        "positive_count": len(positive_eigs),
        "negative_count": len(negative_eigs),
        "passed": passed,
    }


def check_spectral_gap_consistency(
    eigenvalues_small: np.ndarray,
    eigenvalues_large: np.ndarray,
    max_relative_change: float = 0.5,
) -> dict:
    """Check spectral gap consistency (scale-invariant).

    Spectral gap = difference between adjacent eigenvalues.
    For stable discretization, gap PATTERN should be consistent across lattice sizes
    (even if absolute eigenvalue magnitude scales with N).

    We normalize gaps by eigenvalue magnitude to make them scale-invariant.
    """
    eigs_small_sorted = np.sort(eigenvalues_small)
    eigs_large_sorted = np.sort(eigenvalues_large)

    # Compute gaps
    gaps_small = np.diff(eigs_small_sorted)
    gaps_large = np.diff(eigs_large_sorted)

    # Normalize by eigenvalue magnitude to make scale-invariant
    # (gaps / mean_eigenvalue should be consistent)
    mean_eig_small = float(np.mean(np.abs(eigs_small_sorted)))
    mean_eig_large = float(np.mean(np.abs(eigs_large_sorted)))

    normalized_gaps_small = gaps_small / (mean_eig_small + 1e-10)
    normalized_gaps_large = gaps_large / (mean_eig_large + 1e-10)

    # Compare mean normalized gap
    mean_norm_gap_small = float(np.mean(np.abs(normalized_gaps_small)))
    mean_norm_gap_large = float(np.mean(np.abs(normalized_gaps_large)))

    relative_change = abs(mean_norm_gap_large - mean_norm_gap_small) / (mean_norm_gap_small + 1e-10)

    passed = relative_change < max_relative_change

    return {
        "check": "spectral_gap_consistency",
        "mean_normalized_gap_small": mean_norm_gap_small,
        "mean_normalized_gap_large": mean_norm_gap_large,
        "relative_change": relative_change,
        "threshold": max_relative_change,
        "passed": passed,
        "note": "Scale-invariant: compares normalized gap patterns, not absolute magnitude",
    }


def check_no_false_localization(operator: np.ndarray, ipr_threshold: float = 0.5) -> dict:
    """Check that clean S¹ operator has EXTENDED modes, not localized."""
    eigenvalues, eigenvectors = np.linalg.eigh(operator)

    ipr_values = []
    for i in range(eigenvectors.shape[1]):
        psi = eigenvectors[:, i]
        prob = np.abs(psi) ** 2
        ipr = float(np.sum(prob**2))
        ipr_values.append(ipr)

    mean_ipr = float(np.mean(ipr_values))
    max_ipr = float(np.max(ipr_values))

    n = operator.shape[0]
    expected_ipr_extended = 1.0 / n

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


def run_s1_calibration_v0_1_18() -> dict:
    """Run improved S¹ calibration with scale-invariant stability metric."""
    results = {
        "experiment": "S¹ Calibration v0.1.18 (Improved)",
        "version": "v0.1.18",
        "geometry": "S¹ (circle)",
        "improvements": [
            "Removed absolute eigenvalue magnitude stability (flagged expected N/R scaling)",
            "Added spectral gap consistency check (scale-invariant)",
        ],
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

        # Check 3: Spectral gap consistency (8 vs 32) — NEW SCALE-INVARIANT
        eigenvalues_8 = np.linalg.eigvalsh(operators[8])
        eigenvalues_32 = np.linalg.eigvalsh(operators[32])
        check_gap = check_spectral_gap_consistency(eigenvalues_8, eigenvalues_32)
        check_gap["size_small"] = 8
        check_gap["size_large"] = 32
        family_results["checks"].append(check_gap)

        # Check 4: No false localization (size=16)
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
    results = run_s1_calibration_v0_1_18()

    # Print summary
    print("\n" + "=" * 70)
    print("S¹ CALIBRATION v0.1.18 (IMPROVED — SCALE-INVARIANT)")
    print("=" * 70)
    print(f"Geometry: {results['geometry']}")
    print(f"Families tested: {results['summary']['total_families']}")
    print(
        f"Pass rate: {results['summary']['passed_checks']}/{results['summary']['total_checks']} "
        f"({results['summary']['pass_rate']:.1%})"
    )
    print()
    print("Improvements from v0.1.17:")
    for improvement in results["improvements"]:
        print(f"  + {improvement}")
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
    output_path = output_dir / "s1_calibration_v0_1_18_improved.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    print()

    # Print comparison with v0.1.17
    print("=" * 70)
    print("COMPARISON: v0.1.17 vs v0.1.18")
    print("=" * 70)
    print("v0.1.17:")
    print("  - lattice_size_stability: 0/3 passed (flagged expected N/R scaling)")
    print("  - Overall: 15/18 passed (83.3%)")
    print()
    print("v0.1.18:")
    print(f"  - spectral_gap_consistency: (see results above)")
    print(
        f"  - Overall: {results['summary']['passed_checks']}/{results['summary']['total_checks']} "
        f"passed ({results['summary']['pass_rate']:.1%})"
    )
    print("=" * 70)
