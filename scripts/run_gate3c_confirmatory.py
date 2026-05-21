"""Gate 3C Confirmatory Replication — S³×S¹

Purpose: Convert exploratory W=20 signal into confirmatory evidence or documented false-positive.

Pre-registered protocol: reports/S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md

Date: 2026-05-21
Status: CONFIRMATORY (pre-registered, no post-hoc changes allowed)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import numpy as np
import scripts.s3_s1_product_discretized_ipr_smoke as smoke
import scripts.s3_s1_gate3_profiles as profiles


def main():
    """Run Gate 3C confirmatory replication."""

    print("=" * 80)
    print("S³×S¹ Gate 3C — Confirmatory Replication")
    print("=" * 80)
    print()
    print("Purpose: Convert exploratory W=20 signal (4.68x) into confirmatory evidence")
    print("Protocol: PRE-REGISTERED (no post-hoc changes allowed)")
    print()
    print("Pre-flight: reports/S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md")
    print()

    output_dir = Path("reports/RUNS/gate3c_confirmatory_v0.1.20")
    output_dir.mkdir(parents=True, exist_ok=True)

    profile = profiles.PROFILE_GATE3C
    n_cases = profiles.estimate_cases(profile)
    time_est = profiles.estimate_time(profile)

    print(f"Configuration: {n_cases} cases, ~{time_est/60:.1f}min estimated")
    print(f"W values: {profile['disorder_values']} (clean + Gate 3 baseline + exploratory)")
    print(f"Output: {output_dir}")
    print()
    print("-" * 80)

    start = time.time()

    agg, results = smoke.run_ipr_smoke(output_dir, profile)

    elapsed = time.time() - start

    print("-" * 80)
    print()
    print(f"✅ Gate 3C complete: {n_cases} cases in {elapsed/60:.1f}min")
    print()

    # Extract per-W statistics
    clean_cases = [r for r in results if r["disorder_strength"] == 0.0 and "error" not in r]
    w12_cases = [r for r in results if r["disorder_strength"] == 12.0 and "error" not in r]
    w20_cases = [r for r in results if r["disorder_strength"] == 20.0 and "error" not in r]

    clean_mean = np.mean([r["mean_low_ipr"] for r in clean_cases])
    w12_mean = np.mean([r["mean_low_ipr"] for r in w12_cases])
    w20_mean = np.mean([r["mean_low_ipr"] for r in w20_cases])

    contrast_w12 = w12_mean / clean_mean if clean_mean > 0 else 0
    contrast_w20 = w20_mean / clean_mean if clean_mean > 0 else 0

    print("=" * 80)
    print("T4 — Absolute IPR Confirmation")
    print("=" * 80)
    print()
    print(f"Clean (W=0):      mean IPR = {clean_mean:.4f} ({len(clean_cases)} cases)")
    print(f"W=12 (Gate 3):    mean IPR = {w12_mean:.4f} ({len(w12_cases)} cases)")
    print(f"W=20 (exploratory): mean IPR = {w20_mean:.4f} ({len(w20_cases)} cases)")
    print()
    print(f"Contrast W=12 vs clean: {contrast_w12:.2f}x")
    print(f"Contrast W=20 vs clean: {contrast_w20:.2f}x")
    print()

    # Pre-registered threshold: W=20 ≥ 2.0x
    threshold = 2.0
    print(f"Pre-registered threshold: ≥ {threshold:.1f}x")
    print()

    if contrast_w20 >= threshold:
        print(f"✅ T4 PRIMARY CRITERION MET: {contrast_w20:.2f}x ≥ {threshold:.1f}x")
        t4_verdict = "PASS"
    else:
        print(f"❌ T4 PRIMARY CRITERION FAILED: {contrast_w20:.2f}x < {threshold:.1f}x")
        t4_verdict = "FAIL"

    print()

    # Reproducibility breakdown
    print("-" * 80)
    print("T4 — Reproducibility Breakdown")
    print("-" * 80)
    print()

    # Per-family
    families = sorted(set(r["family"] for r in w20_cases))
    print("Per-Family (W=20):")
    family_pass = 0
    for fam in families:
        fam_w20 = [r for r in w20_cases if r["family"] == fam]
        fam_clean = [r for r in clean_cases if r["family"] == fam]
        fam_w20_mean = np.mean([r["mean_low_ipr"] for r in fam_w20])
        fam_clean_mean = np.mean([r["mean_low_ipr"] for r in fam_clean])
        fam_contrast = fam_w20_mean / fam_clean_mean if fam_clean_mean > 0 else 0

        status = "✅" if fam_contrast >= threshold else "❌"
        print(f"  {fam:20s}: {fam_contrast:.2f}x  {status}")
        if fam_contrast >= threshold:
            family_pass += 1

    print(f"\nFamilies passing: {family_pass}/{len(families)} (criterion: ≥2/3)")
    print()

    # Per-s1_size
    sizes = sorted(set(r["s1_size"] for r in w20_cases))
    print("Per-s1_size (W=20):")
    size_pass = 0
    for size in sizes:
        size_w20 = [r for r in w20_cases if r["s1_size"] == size]
        size_clean = [r for r in clean_cases if r["s1_size"] == size]
        size_w20_mean = np.mean([r["mean_low_ipr"] for r in size_w20])
        size_clean_mean = np.mean([r["mean_low_ipr"] for r in size_clean])
        size_contrast = size_w20_mean / size_clean_mean if size_clean_mean > 0 else 0

        status = "✅" if size_contrast >= threshold else "❌"
        print(f"  s1={size:3d}: {size_contrast:.2f}x  {status}")
        if size_contrast >= threshold:
            size_pass += 1

    print(f"\nSizes passing: {size_pass}/{len(sizes)} (criterion: ≥3/4)")
    print()

    # Per-seed
    seeds = sorted(set(r["seed"] for r in w20_cases))
    print("Per-Seed (W=20):")
    seed_pass = 0
    for seed in seeds:
        seed_w20 = [r for r in w20_cases if r["seed"] == seed]
        seed_clean = [r for r in clean_cases if r["seed"] == seed]
        seed_w20_mean = np.mean([r["mean_low_ipr"] for r in seed_w20])
        seed_clean_mean = np.mean([r["mean_low_ipr"] for r in seed_clean])
        seed_contrast = seed_w20_mean / seed_clean_mean if seed_clean_mean > 0 else 0

        status = "✅" if seed_contrast >= 1.8 else "❌"  # Relaxed: within 10% of threshold
        print(f"  seed={seed}: {seed_contrast:.2f}x  {status}")
        if seed_contrast >= 1.8:
            seed_pass += 1

    print(f"\nSeeds passing (≥1.8x): {seed_pass}/{len(seeds)} (criterion: all ≥1.8x)")
    print()

    # T4 final verdict
    print("=" * 80)
    print("T4 — Final Verdict")
    print("=" * 80)
    print()

    t4_criteria = {
        "Mean contrast ≥ 2.0x": contrast_w20 >= threshold,
        "Families ≥ 2/3": family_pass >= 2,
        "Sizes ≥ 3/4": size_pass >= 3,
        "Seeds all ≥ 1.8x": seed_pass == len(seeds),
    }

    for criterion, passed in t4_criteria.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {criterion:30s}: {status}")

    print()

    if all(t4_criteria.values()):
        t4_final = "T4_PASS"
        print("✅ T4 PASS: All criteria met")
    elif t4_criteria["Mean contrast ≥ 2.0x"] and sum(t4_criteria.values()) >= 3:
        t4_final = "T4_PASS_WITH_CAVEATS"
        print("⚠️ T4 PASS WITH CAVEATS: Mean ≥2.0x but one subcriterion failed")
    elif contrast_w20 < threshold:
        t4_final = "T4_FAIL"
        print(f"❌ T4 FAIL: Mean contrast {contrast_w20:.2f}x < {threshold:.1f}x")
    else:
        t4_final = "T4_WEAK_OR_INCONCLUSIVE"
        print("⚠️ T4 WEAK: Signal inconsistent across subgroups")

    print()
    print("=" * 80)
    print()
    print(f"Results saved: {output_dir}/")
    print()
    print(f"Next: Run T1 and T5 tests, assign final Gate 3C verdict")
    print()

    return t4_final


if __name__ == "__main__":
    verdict = main()
    print(f"T4 verdict: {verdict}")
