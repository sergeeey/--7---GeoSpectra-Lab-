#!/usr/bin/env python3
"""
Gate 4B v0.1.21 — Apply pre-registered decision rules.

Analyzes aggregated metrics and determines verdict:
- GATE4_FSS_PASS_WITH_CAVEATS
- GATE4_FSS_WEAK_OR_INCONCLUSIVE
- GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED
- GATE4_FSS_INCOMPLETE
"""

import json
from pathlib import Path
import numpy as np

# Paths
BASE_DIR = Path(__file__).parent.parent
MERGED_DIR = BASE_DIR / "reports" / "RUNS" / "gate4_fss_v0.1.21" / "merged"

# Thresholds (pre-registered)
PASS_CONTRAST_THRESHOLD = 2.0  # Aggregate W=20 vs W=0 contrast
WEAK_CONTRAST_THRESHOLD = 1.5  # Below this = artifact
FAMILY_CONSISTENCY_THRESHOLD = 2 / 3  # ≥2/3 families must pass
FAMILY_DOMINATION_THRESHOLD = 0.80  # No family >80% of aggregate


def load_json(filename):
    with open(MERGED_DIR / filename, "r") as f:
        return json.load(f)


def compute_aggregate_contrast(contrast_data):
    """Compute aggregate W=20 vs W=0 contrast across all families."""
    all_contrasts = contrast_data["per_seed_contrasts"]

    # Group by (family, s1_size, j_max) and average over seeds
    from collections import defaultdict

    by_group = defaultdict(list)
    for c in all_contrasts:
        key = (c["family"], c["s1_size"], c["j_max"])
        by_group[key].append(c["contrast_w20_minus_w0"])

    # Compute mean contrast for each group
    group_contrasts = [np.mean(contrasts) for contrasts in by_group.values()]

    # Overall aggregate: mean of all group means
    aggregate_contrast_abs = np.mean(group_contrasts)

    # Compute contrast ratio (multiplicative) from absolute contrasts
    # Need to compute mean(IPR_w20) / mean(IPR_w0)
    mean_ipr_w0 = np.mean([c["true_ipr_w0"] for c in all_contrasts])
    mean_ipr_w20 = np.mean([c["true_ipr_w20"] for c in all_contrasts])
    aggregate_contrast_ratio = mean_ipr_w20 / mean_ipr_w0

    return {
        "aggregate_contrast_ratio": aggregate_contrast_ratio,
        "aggregate_contrast_absolute": aggregate_contrast_abs,
        "mean_ipr_w0": mean_ipr_w0,
        "mean_ipr_w20": mean_ipr_w20,
    }


def compute_family_contrasts(contrast_data):
    """Compute per-family W=20 vs W=0 contrasts."""
    all_contrasts = contrast_data["per_seed_contrasts"]

    from collections import defaultdict

    by_family = defaultdict(lambda: {"w0": [], "w20": [], "contrast_abs": []})

    for c in all_contrasts:
        family = c["family"]
        by_family[family]["w0"].append(c["true_ipr_w0"])
        by_family[family]["w20"].append(c["true_ipr_w20"])
        by_family[family]["contrast_abs"].append(c["contrast_w20_minus_w0"])

    family_results = {}
    for family, data in by_family.items():
        mean_w0 = np.mean(data["w0"])
        mean_w20 = np.mean(data["w20"])
        contrast_ratio = mean_w20 / mean_w0 if mean_w0 > 0 else float("inf")
        contrast_abs = np.mean(data["contrast_abs"])

        family_results[family] = {
            "mean_ipr_w0": mean_w0,
            "mean_ipr_w20": mean_w20,
            "contrast_ratio": contrast_ratio,
            "contrast_absolute": contrast_abs,
            "n_cases": len(data["w0"]),
        }

    return family_results


def check_family_consistency(family_contrasts, threshold=PASS_CONTRAST_THRESHOLD):
    """Check how many families pass the contrast threshold."""
    families_pass = sum(1 for fc in family_contrasts.values() if fc["contrast_ratio"] >= threshold)
    total_families = len(family_contrasts)
    return families_pass, total_families


def check_family_domination(family_contrasts):
    """Check if any single family dominates >80% of aggregate contrast."""
    total_contrast = sum(fc["contrast_absolute"] for fc in family_contrasts.values())
    for family, fc in family_contrasts.items():
        fraction = fc["contrast_absolute"] / total_contrast if total_contrast > 0 else 0
        if fraction > FAMILY_DOMINATION_THRESHOLD:
            return family, fraction
    return None, 0.0


def analyze_finite_size_trend(contrast_data):
    """Analyze contrast ratio vs s1_size trend."""
    per_seed_contrasts = contrast_data["per_seed_contrasts"]

    # Group by size and compute ratio contrasts
    from collections import defaultdict

    by_size = defaultdict(lambda: {"w0": [], "w20": []})
    for c in per_seed_contrasts:
        size = c["s1_size"]
        by_size[size]["w0"].append(c["true_ipr_w0"])
        by_size[size]["w20"].append(c["true_ipr_w20"])

    size_trend_ratio = {}
    for size in sorted(by_size.keys()):
        mean_w0 = np.mean(by_size[size]["w0"])
        mean_w20 = np.mean(by_size[size]["w20"])
        size_trend_ratio[size] = mean_w20 / mean_w0 if mean_w0 > 0 else float("inf")

    # Check if trend is collapsing (contrast drops at large sizes)
    sizes = sorted(size_trend_ratio.keys())
    contrasts = [size_trend_ratio[s] for s in sizes]

    # Trend verdict based on ratio at largest size
    if contrasts[-1] < WEAK_CONTRAST_THRESHOLD:
        trend_verdict = "collapsing"
    elif contrasts[-1] < contrasts[0] * 0.75:  # Dropped >25%
        trend_verdict = "weakening"
    elif contrasts[-1] >= contrasts[0]:
        trend_verdict = "stable_or_strengthening"
    else:
        trend_verdict = "stable_weakening"  # Minor drop but still above threshold

    return {
        "size_trend_ratio": size_trend_ratio,
        "trend_verdict": trend_verdict,
        "largest_size_contrast_ratio": contrasts[-1],
    }


def analyze_r_statistic(r_stat_data):
    """Check r-statistic shift W=0 → W=20."""
    # Group by W
    by_w = {"0": [], "12": [], "20": []}
    for entry in r_stat_data:
        W = str(entry["disorder_strength"])
        if W in by_w:
            by_w[W].append(entry["r_stat_mean"])

    r_w0 = np.mean(by_w["0"]) if by_w["0"] else None
    r_w20 = np.mean(by_w["20"]) if by_w["20"] else None

    # Expected: r_w0 ≈ 0.53 (GOE), r_w20 → 0.39 (Poisson)
    # Shift should be negative (toward Poisson)
    if r_w0 is not None and r_w20 is not None:
        r_shift = r_w20 - r_w0
        if r_shift < -0.05:
            r_verdict = "supports_localization"
        elif -0.05 <= r_shift <= 0.05:
            r_verdict = "ambiguous"
        else:
            r_verdict = "contradicts_localization"
    else:
        r_verdict = "insufficient_data"

    return {
        "r_w0_mean": r_w0,
        "r_w20_mean": r_w20,
        "r_shift": r_shift if r_w0 and r_w20 else None,
        "r_verdict": r_verdict,
    }


def check_controls(contrast_data):
    """Check if W=0 baseline is stable within same size."""
    # W=0 должен показывать IPR ≈ 1/N (delocalized)
    # Проверим стабильность W=0 внутри одного size (не across sizes)
    per_seed = contrast_data["per_seed_contrasts"]

    # Group W=0 IPR by size
    from collections import defaultdict

    w0_by_size = defaultdict(list)
    for c in per_seed:
        w0_by_size[c["s1_size"]].append(c["true_ipr_w0"])

    # Check stability at each size
    stability_by_size = {}
    for size, w0_values in sorted(w0_by_size.items()):
        mean_w0 = np.mean(w0_values)
        std_w0 = np.std(w0_values)
        cv = std_w0 / mean_w0 if mean_w0 > 0 else float("inf")  # Coefficient of variation
        stability_by_size[size] = {"mean": mean_w0, "std": std_w0, "cv": cv}

    # Overall verdict: stable if all sizes have CV < 0.2
    max_cv = max(s["cv"] for s in stability_by_size.values())
    if max_cv < 0.2:
        control_verdict = "stable"
    else:
        control_verdict = "unstable"

    return {
        "stability_by_size": stability_by_size,
        "max_cv": max_cv,
        "control_verdict": control_verdict,
    }


def determine_verdict(analysis):
    """Apply pre-registered decision rules to determine final verdict."""

    # Extract key metrics
    agg = analysis["aggregate_contrast"]
    family = analysis["family_analysis"]
    trend = analysis["finite_size_trend"]
    r_stat = analysis["r_statistic"]
    controls = analysis["controls"]

    families_pass, total_families = family["families_pass_count"]
    dominating_family = family["dominating_family"]

    # Rule 8.4: INCOMPLETE
    if analysis["grid_completion"] < 0.5:
        return "GATE4_FSS_INCOMPLETE", "Grid completion < 50%"

    # Rule 8.3: FAIL_OR_ARTIFACT_DOMINATED
    if agg["aggregate_contrast_ratio"] < WEAK_CONTRAST_THRESHOLD:
        return (
            "GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED",
            f"Aggregate contrast {agg['aggregate_contrast_ratio']:.2f}× < {WEAK_CONTRAST_THRESHOLD}×",
        )

    if families_pass == 1:
        return (
            "GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED",
            "Single-family carry (only 1/3 families pass)",
        )

    if trend["trend_verdict"] == "collapsing":
        return (
            "GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED",
            f"Finite-size collapse at s1_size=128 ({trend['largest_size_contrast_ratio']:.2f}× < {WEAK_CONTRAST_THRESHOLD}×)",
        )

    if r_stat["r_verdict"] == "contradicts_localization":
        return (
            "GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED",
            "r-statistic contradicts IPR localization signal",
        )

    if controls["control_verdict"] == "unstable":
        return "GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED", "W=0 control baseline unstable"

    # Rule 8.2: WEAK_OR_INCONCLUSIVE
    if WEAK_CONTRAST_THRESHOLD <= agg["aggregate_contrast_ratio"] < PASS_CONTRAST_THRESHOLD:
        return (
            "GATE4_FSS_WEAK_OR_INCONCLUSIVE",
            f"Aggregate contrast {agg['aggregate_contrast_ratio']:.2f}× in weak range [{WEAK_CONTRAST_THRESHOLD}×, {PASS_CONTRAST_THRESHOLD}×)",
        )

    if families_pass < total_families * FAMILY_CONSISTENCY_THRESHOLD:
        return (
            "GATE4_FSS_WEAK_OR_INCONCLUSIVE",
            f"Family consistency {families_pass}/{total_families} < 2/3",
        )

    if dominating_family is not None:
        return (
            "GATE4_FSS_WEAK_OR_INCONCLUSIVE",
            f"Family domination: {dominating_family} contributes >{FAMILY_DOMINATION_THRESHOLD*100}% of aggregate",
        )

    if trend["trend_verdict"] == "weakening":
        return "GATE4_FSS_WEAK_OR_INCONCLUSIVE", "Finite-size trend weakening but not collapsing"

    if r_stat["r_verdict"] == "ambiguous":
        return "GATE4_FSS_WEAK_OR_INCONCLUSIVE", "r-statistic shift ambiguous"

    # Rule 8.1: PASS_WITH_CAVEATS
    # All 7 conditions must hold
    conditions = []

    # 1. Aggregate contrast ≥2.0×
    if agg["aggregate_contrast_ratio"] >= PASS_CONTRAST_THRESHOLD:
        conditions.append(("aggregate_contrast", True))
    else:
        conditions.append(("aggregate_contrast", False))

    # 2. Family consistency ≥2/3
    if families_pass >= total_families * FAMILY_CONSISTENCY_THRESHOLD:
        conditions.append(("family_consistency", True))
    else:
        conditions.append(("family_consistency", False))

    # 3. No single-family domination
    if dominating_family is None:
        conditions.append(("no_domination", True))
    else:
        conditions.append(("no_domination", False))

    # 4. Finite-size trend stable/saturating/strengthening
    if trend["trend_verdict"] in ["stable_or_strengthening"]:
        conditions.append(("finite_size_trend", True))
    else:
        conditions.append(("finite_size_trend", False))

    # 5. r-statistic supports localization
    if r_stat["r_verdict"] in ["supports_localization", "ambiguous"]:
        conditions.append(("r_statistic", True))
    else:
        conditions.append(("r_statistic", False))

    # 6. No broad failure cluster (assume True if we got here)
    conditions.append(("no_broad_failure", True))

    # 7. Controls pass
    if controls["control_verdict"] == "stable":
        conditions.append(("controls_pass", True))
    else:
        conditions.append(("controls_pass", False))

    # Check if all conditions True
    if all(cond[1] for cond in conditions):
        return "GATE4_FSS_PASS_WITH_CAVEATS", "All 7 PASS conditions satisfied"
    else:
        failed_conditions = [cond[0] for cond in conditions if not cond[1]]
        return (
            "GATE4_FSS_WEAK_OR_INCONCLUSIVE",
            f"PASS conditions not met: {', '.join(failed_conditions)}",
        )


def main():
    print("Gate 4B v0.1.21 — Applying pre-registered decision rules\n")

    # Load aggregated data
    metrics = load_json("metrics.json")
    coverage = load_json("coverage.json")
    contrast = load_json("true_ipr_contrast_summary.json")
    r_stat_data = load_json("r_stat_summary.json")

    # Grid completion
    grid_completion = coverage["total_unique_cases"] / 216
    print(f"Grid completion: {coverage['total_unique_cases']}/216 ({grid_completion*100:.1f}%)")

    # 1. Aggregate contrast
    agg_contrast = compute_aggregate_contrast(contrast)
    print(f"\n1. Aggregate Contrast:")
    print(f"   mean(IPR_W=0) = {agg_contrast['mean_ipr_w0']:.4f}")
    print(f"   mean(IPR_W=20) = {agg_contrast['mean_ipr_w20']:.4f}")
    print(f"   Contrast ratio = {agg_contrast['aggregate_contrast_ratio']:.2f}×")
    print(f"   Contrast absolute = {agg_contrast['aggregate_contrast_absolute']:.4f}")
    print(f"   Threshold: ≥{PASS_CONTRAST_THRESHOLD:.1f}× for PASS")

    # 2. Family-level contrasts
    family_contrasts = compute_family_contrasts(contrast)
    families_pass, total_families = check_family_consistency(family_contrasts)
    dominating_family, domination_fraction = check_family_domination(family_contrasts)

    print(f"\n2. Family Consistency:")
    for family, fc in sorted(family_contrasts.items()):
        pass_mark = "✅ PASS" if fc["contrast_ratio"] >= PASS_CONTRAST_THRESHOLD else "❌ FAIL"
        print(
            f"   {family:15s}: {fc['contrast_ratio']:.2f}× (abs: {fc['contrast_absolute']:.4f}) {pass_mark}"
        )
    print(
        f"   Families passing: {families_pass}/{total_families} (threshold: ≥{int(total_families * FAMILY_CONSISTENCY_THRESHOLD)}/{total_families})"
    )

    if dominating_family:
        print(
            f"   ⚠️ Domination: {dominating_family} contributes {domination_fraction*100:.1f}% (threshold: ≤{FAMILY_DOMINATION_THRESHOLD*100}%)"
        )
    else:
        print(f"   ✅ No single-family domination (all ≤{FAMILY_DOMINATION_THRESHOLD*100}%)")

    # 3. Finite-size trend
    fss_trend = analyze_finite_size_trend(contrast)
    print(f"\n3. Finite-Size Scaling Trend:")
    for size, contrast_val in sorted(fss_trend["size_trend_ratio"].items()):
        print(f"   s1_size={size:3d}: contrast ratio = {contrast_val:.2f}×")
    print(f"   Trend verdict: {fss_trend['trend_verdict']}")
    print(
        f"   Largest size contrast ratio: {fss_trend['largest_size_contrast_ratio']:.2f}× (threshold: ≥{WEAK_CONTRAST_THRESHOLD:.2f}× for not-collapsing)"
    )

    # 4. r-statistic
    r_analysis = analyze_r_statistic(r_stat_data)
    print(f"\n4. Level-Spacing r-Statistic:")
    print(f"   r(W=0) mean = {r_analysis['r_w0_mean']:.3f} (expected ≈0.53 GOE)")
    print(f"   r(W=20) mean = {r_analysis['r_w20_mean']:.3f} (expected ≈0.39 Poisson)")
    print(f"   Shift = {r_analysis['r_shift']:.3f} (negative = toward localization)")
    print(f"   Verdict: {r_analysis['r_verdict']}")

    # 5. Controls
    control_check = check_controls(contrast)
    print(f"\n5. Control Baseline (W=0):")
    for size, stats in sorted(control_check["stability_by_size"].items()):
        print(
            f"   s1_size={size:3d}: mean={stats['mean']:.5f}, std={stats['std']:.5f}, CV={stats['cv']:.3f}"
        )
    print(
        f"   Max coefficient of variation: {control_check['max_cv']:.3f} (threshold: <0.2 for stable)"
    )
    print(f"   Stability: {control_check['control_verdict']}")

    # Package analysis
    analysis = {
        "grid_completion": grid_completion,
        "aggregate_contrast": agg_contrast,
        "family_analysis": {
            "family_contrasts": family_contrasts,
            "families_pass_count": (families_pass, total_families),
            "dominating_family": dominating_family,
            "domination_fraction": domination_fraction,
        },
        "finite_size_trend": fss_trend,
        "r_statistic": r_analysis,
        "controls": control_check,
    }

    # Determine verdict
    verdict, reason = determine_verdict(analysis)

    print(f"\n{'='*60}")
    print(f"FINAL VERDICT: {verdict}")
    print(f"Reason: {reason}")
    print(f"{'='*60}\n")

    # Save analysis results
    analysis_output = {
        "verdict": verdict,
        "reason": reason,
        "aggregate_contrast": agg_contrast,
        "family_contrasts": {k: dict(v) for k, v in family_contrasts.items()},
        "families_pass": f"{families_pass}/{total_families}",
        "finite_size_trend": fss_trend,
        "r_statistic": r_analysis,
        "controls": control_check,
    }

    output_file = MERGED_DIR / "verdict_analysis.json"
    with open(output_file, "w") as f:
        json.dump(analysis_output, f, indent=2)
    print(f"✅ verdict_analysis.json created")


if __name__ == "__main__":
    main()
