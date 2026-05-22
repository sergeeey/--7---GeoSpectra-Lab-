#!/usr/bin/env python3
"""
Gate 4B v0.1.21 — Aggregate batch results for scientific analysis.

Creates:
- family_summary.json
- size_scaling_summary.json
- r_stat_summary.json
- true_ipr_contrast_summary.json
"""

import json
from pathlib import Path
import numpy as np
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).parent.parent
BATCHES_DIR = BASE_DIR / "reports" / "RUNS" / "gate4_fss_v0.1.21" / "batches"
MERGED_DIR = BASE_DIR / "reports" / "RUNS" / "gate4_fss_v0.1.21" / "merged"


def load_all_results():
    """Load all results from 9 batches."""
    all_results = []
    for i in range(1, 10):
        batch_dir = BATCHES_DIR / f"batch_{i:02d}"
        results_file = batch_dir / "results.json"
        with open(results_file, "r") as f:
            batch_results = json.load(f)
            all_results.extend(batch_results)
    return all_results


def compute_family_summary(results):
    """Aggregate by family (spectral_circle, ring, wilson_ring)."""
    by_family = defaultdict(lambda: {"true_ipr_mean": [], "r_stat": []})

    for r in results:
        family = r["family"]
        by_family[family]["true_ipr_mean"].append(r["true_ipr_mean"])
        by_family[family]["r_stat"].append(r["r_stat"])

    summary = {}
    for family, data in by_family.items():
        summary[family] = {
            "n_cases": len(data["true_ipr_mean"]),
            "true_ipr_mean": {
                "mean": float(np.mean(data["true_ipr_mean"])),
                "std": float(np.std(data["true_ipr_mean"])),
                "min": float(np.min(data["true_ipr_mean"])),
                "max": float(np.max(data["true_ipr_mean"])),
            },
            "r_stat": {
                "mean": float(np.mean(data["r_stat"])),
                "std": float(np.std(data["r_stat"])),
                "min": float(np.min(data["r_stat"])),
                "max": float(np.max(data["r_stat"])),
            },
        }
    return summary


def compute_size_scaling_summary(results):
    """Aggregate by s1_size (16, 32, 64, 128) for finite-size scaling."""
    by_size = defaultdict(lambda: {"true_ipr_mean": [], "r_stat": []})

    for r in results:
        size = r["s1_size"]
        by_size[size]["true_ipr_mean"].append(r["true_ipr_mean"])
        by_size[size]["r_stat"].append(r["r_stat"])

    summary = {}
    for size, data in sorted(by_size.items()):
        summary[str(size)] = {
            "n_cases": len(data["true_ipr_mean"]),
            "true_ipr_mean": {
                "mean": float(np.mean(data["true_ipr_mean"])),
                "std": float(np.std(data["true_ipr_mean"])),
                "min": float(np.min(data["true_ipr_mean"])),
                "max": float(np.max(data["true_ipr_mean"])),
            },
            "r_stat": {
                "mean": float(np.mean(data["r_stat"])),
                "std": float(np.std(data["r_stat"])),
                "min": float(np.min(data["r_stat"])),
                "max": float(np.max(data["r_stat"])),
            },
        }
    return summary


def compute_r_stat_summary(results):
    """Aggregate r-statistic by family, W, size."""
    by_family_w_size = defaultdict(list)

    for r in results:
        key = (r["family"], r["disorder_strength"], r["s1_size"])
        by_family_w_size[key].append(r["r_stat"])

    summary = []
    for (family, W, size), r_stats in sorted(by_family_w_size.items()):
        summary.append(
            {
                "family": family,
                "disorder_strength": W,
                "s1_size": size,
                "n_cases": len(r_stats),
                "r_stat_mean": float(np.mean(r_stats)),
                "r_stat_std": float(np.std(r_stats)),
                "r_stat_min": float(np.min(r_stats)),
                "r_stat_max": float(np.max(r_stats)),
            }
        )
    return summary


def compute_true_ipr_contrast_summary(results):
    """Compute W=20 vs W=0 contrasts by family, size, j_max."""
    # Organize by (family, s1_size, j_max, seed)
    by_key = defaultdict(dict)

    for r in results:
        key = (r["family"], r["s1_size"], r["j_max"], r["seed"])
        W = r["disorder_strength"]
        by_key[key][W] = r["true_ipr_mean"]

    contrasts = []
    for (family, size, j_max, seed), w_values in sorted(by_key.items()):
        if 0 in w_values and 20 in w_values:
            contrast = w_values[20] - w_values[0]
            contrasts.append(
                {
                    "family": family,
                    "s1_size": size,
                    "j_max": j_max,
                    "seed": seed,
                    "true_ipr_w0": w_values[0],
                    "true_ipr_w20": w_values[20],
                    "contrast_w20_minus_w0": float(contrast),
                }
            )

    # Aggregate by (family, size, j_max)
    by_group = defaultdict(list)
    for c in contrasts:
        key = (c["family"], c["s1_size"], c["j_max"])
        by_group[key].append(c["contrast_w20_minus_w0"])

    summary = {"per_seed_contrasts": contrasts, "aggregate_by_group": []}

    for (family, size, j_max), contrast_list in sorted(by_group.items()):
        summary["aggregate_by_group"].append(
            {
                "family": family,
                "s1_size": size,
                "j_max": j_max,
                "n_seeds": len(contrast_list),
                "contrast_mean": float(np.mean(contrast_list)),
                "contrast_std": float(np.std(contrast_list)),
                "contrast_min": float(np.min(contrast_list)),
                "contrast_max": float(np.max(contrast_list)),
            }
        )

    return summary


def main():
    print("Loading all 216 results from 9 batches...")
    results = load_all_results()
    print(f"Loaded {len(results)} results")

    # 1. Family summary
    family_summary = compute_family_summary(results)
    family_file = MERGED_DIR / "family_summary.json"
    with open(family_file, "w") as f:
        json.dump(family_summary, f, indent=2)
    print(f"✅ family_summary.json created ({len(family_summary)} families)")

    # 2. Size scaling summary
    size_summary = compute_size_scaling_summary(results)
    size_file = MERGED_DIR / "size_scaling_summary.json"
    with open(size_file, "w") as f:
        json.dump(size_summary, f, indent=2)
    print(f"✅ size_scaling_summary.json created ({len(size_summary)} sizes)")

    # 3. r-statistic summary
    r_stat_summary = compute_r_stat_summary(results)
    r_stat_file = MERGED_DIR / "r_stat_summary.json"
    with open(r_stat_file, "w") as f:
        json.dump(r_stat_summary, f, indent=2)
    print(f"✅ r_stat_summary.json created ({len(r_stat_summary)} family×W×size groups)")

    # 4. True IPR contrast summary
    contrast_summary = compute_true_ipr_contrast_summary(results)
    contrast_file = MERGED_DIR / "true_ipr_contrast_summary.json"
    with open(contrast_file, "w") as f:
        json.dump(contrast_summary, f, indent=2)
    n_contrasts = len(contrast_summary["per_seed_contrasts"])
    n_groups = len(contrast_summary["aggregate_by_group"])
    print(
        f"✅ true_ipr_contrast_summary.json created ({n_contrasts} per-seed contrasts, {n_groups} aggregated groups)"
    )

    print("\nMerge Step 2/3 complete: family, size, r_stat, contrast summaries created")


if __name__ == "__main__":
    main()
