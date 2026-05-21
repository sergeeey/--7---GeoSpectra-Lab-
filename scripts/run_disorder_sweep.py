"""Disorder Sweep for S³×S¹ — Find Optimal W for Max Contrast

Purpose: Test W ∈ {16, 20, 24} to find disorder strength that maximizes
         absolute IPR contrast. Gate 3 tested W ≤ 12, got 1.75x (below 2.0x threshold).

Expected outcome: If contrast reaches ≥2.0x → optimal W found for Gate 4.
                  If not → document upper bound, proceed with W=12.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import scripts.s3_s1_product_discretized_ipr_smoke as smoke
import scripts.s3_s1_gate3_profiles as profiles


def main():
    """Run disorder sweep diagnostic."""

    print("=" * 70)
    print("S³×S¹ Disorder Sweep — W ∈ {16, 20, 24}")
    print("=" * 70)
    print()
    print("Purpose: Find optimal disorder strength for max IPR contrast")
    print("Context: Gate 3 tested W ≤ 12, got 1.75x (below 2.0x threshold)")
    print()

    output_dir = Path("reports/RUNS/disorder_sweep_v0.1.20")
    output_dir.mkdir(parents=True, exist_ok=True)

    profile = profiles.PROFILE_DISORDER_SWEEP
    n_cases = profiles.estimate_cases(profile)
    time_est = profiles.estimate_time(profile)

    print(f"Configuration: {n_cases} cases, ~{time_est:.1f}s estimated")
    print(f"Output: {output_dir}")
    print()
    print("-" * 70)

    start = time.time()

    agg, results = smoke.run_ipr_smoke(output_dir, profile)

    elapsed = time.time() - start

    print("-" * 70)
    print()
    print(f"✅ Disorder sweep complete: {n_cases} cases in {elapsed:.1f}s")
    print()
    print("Key Result:")
    print(f"  Clean IPR (W=0):     {agg['clean_mean_ipr_absolute']:.4f}")
    print(f"  Disordered IPR (all): {agg['disordered_mean_ipr_absolute']:.4f}")
    print(f"  Absolute contrast:    {agg['ipr_contrast_absolute']:.2f}x")
    print()

    verdict = agg.get("smoke_verdict", "unknown")
    print(f"Smoke Verdict: {verdict}")
    print()

    # Extract per-disorder results
    print("Per-Disorder Breakdown:")
    print()
    w_values = sorted(set(r["disorder_strength"] for r in results if "error" not in r))

    for w in w_values:
        w_cases = [r for r in results if r["disorder_strength"] == w and "error" not in r]
        w_mean_ipr = sum(r["mean_low_ipr"] for r in w_cases) / len(w_cases)
        print(f"  W={w:5.1f}: mean IPR = {w_mean_ipr:.4f} ({len(w_cases)} cases)")

    print()

    # Compute contrast for each W vs clean
    clean_cases = [r for r in results if r["disorder_strength"] == 0.0 and "error" not in r]
    clean_mean = sum(r["mean_low_ipr"] for r in clean_cases) / len(clean_cases)

    print("Contrast vs Clean (W=0):")
    print()

    for w in w_values:
        if w == 0.0:
            continue
        w_cases = [r for r in results if r["disorder_strength"] == w and "error" not in r]
        w_mean = sum(r["mean_low_ipr"] for r in w_cases) / len(w_cases)
        contrast = w_mean / clean_mean if clean_mean > 0 else 0

        status = "✅ PASS" if contrast >= 2.0 else "⚠️ WEAK" if contrast >= 1.3 else "❌ FAIL"
        print(f"  W={w:5.1f}: {contrast:.2f}x  {status}")

    print()
    print("=" * 70)
    print()

    # Recommendation: find W with BEST contrast (not highest W)
    best_contrast = 0
    best_w = 0

    for w in w_values:
        if w == 0.0:
            continue
        w_cases = [r for r in results if r["disorder_strength"] == w and "error" not in r]
        w_mean = sum(r["mean_low_ipr"] for r in w_cases) / len(w_cases)
        contrast = w_mean / clean_mean if clean_mean > 0 else 0

        if contrast > best_contrast:
            best_contrast = contrast
            best_w = w

    if best_contrast >= 2.0:
        print(f"✅ OPTIMAL W FOUND: W={best_w} achieves {best_contrast:.2f}x contrast (≥2.0x)")
        print(f"   → Use W={best_w} for Gate 4 full grid")
        print(f"   Improvement over Gate 3 (W=12, 1.75x): +{best_contrast - 1.75:.2f}x")
    elif best_contrast > agg["ipr_contrast_absolute"]:
        print(
            f"⚠️ IMPROVEMENT: W={best_w} achieves {best_contrast:.2f}x (vs {agg['ipr_contrast_absolute']:.2f}x Gate 3)"
        )
        print(f"   → Consider extending sweep to W ∈ {{28, 32}} or accept current best")
    else:
        print(f"⚠️ NO IMPROVEMENT: Best W={best_w} same as Gate 3 ({best_contrast:.2f}x)")
        print(f"   → Disorder strength not limiting factor, proceed with W=12 for Gate 4")

    print()
    print(f"Results saved: {output_dir}/")
    print()


if __name__ == "__main__":
    main()
