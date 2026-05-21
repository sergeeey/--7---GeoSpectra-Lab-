"""S3 x S1 Product-Discretized IPR Smoke Test (Gate 2)

Quick spatial-localization sanity check for S3xS1 operators.

Representative grid: ~50 cases
- families: spectral_circle, ring, wilson_ring
- j_max: 1, 2, 3 (replaces S2 monopole charge q)
- s1_sizes: 8, 16, 24
- alpha: 0.0, 0.5
- W: 0.0, 4.0, 8.0
- seeds: 123, 456

Metrics:
- IPR for low modes
- mean/min/max low IPR
- IPR ratio to 1/N (delocalization baseline)
- j0 control flag (analog of q0 for S2xS1)

Verdict:
- pass: disordered IPR clearly > clean IPR
- weak: contrast small or family-dependent
- fail: no contrast or j0 anomalies
"""

import sys
from pathlib import Path

# Add project root to path (for standalone execution)
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import argparse
import json
import time

import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.s3_s1_product_discretized import build_s3_s1_product_operator


def compute_ipr_for_eigenvector(psi):
    """Inverse participation ratio: sum(|psi_i|^4)"""
    return np.sum(np.abs(psi) ** 4)


def run_ipr_smoke(output_dir: Path, config: dict):
    """Run IPR smoke test."""
    families = config["families"]
    j_max_values = config["j_max_values"]
    s1_sizes = config["s1_sizes"]
    alpha_values = config["alpha_values"]
    disorder_values = config["disorder_values"]
    seeds = config["seeds"]
    n_low = config.get("n_low", 5)  # number of low modes to analyze
    radius = config.get("radius", 1.0)
    mode = config.get("mode", "geometric_weight")  # Use mode that responds to disorder

    results = []
    case_count = 0
    total_cases = (
        len(families)
        * len(j_max_values)
        * len(s1_sizes)
        * len(alpha_values)
        * len(disorder_values)
        * len(seeds)
    )

    print(f"Starting S3xS1 IPR smoke test: {total_cases} cases")
    start_time = time.time()

    for family in families:
        for j_max in j_max_values:
            for s1_size in s1_sizes:
                for alpha in alpha_values:
                    for disorder in disorder_values:
                        for seed in seeds:
                            case_count += 1
                            print(
                                f"[{case_count}/{total_cases}] "
                                f"family={family} j_max={j_max} s1={s1_size} "
                                f"alpha={alpha:.1f} disorder={disorder:.1f} seed={seed}"
                            )

                            try:
                                # Build operator
                                H, _, meta = build_s3_s1_product_operator(
                                    j_max=j_max,
                                    s1_family=family,
                                    s1_size=s1_size,
                                    alpha=alpha,
                                    mode=mode,
                                    disorder_strength=disorder,
                                    seed=seed,
                                    radius=radius,
                                )

                                N = H.shape[0]

                                # Compute spectrum
                                eigvals, eigvecs = np.linalg.eigh(H)
                                sort_idx = np.argsort(np.abs(eigvals))
                                eigvals = eigvals[sort_idx]
                                eigvecs = eigvecs[:, sort_idx]

                                # Compute IPR for low modes
                                low_iprs = []
                                for i in range(min(n_low, len(eigvals))):
                                    ipr = compute_ipr_for_eigenvector(eigvecs[:, i])
                                    low_iprs.append(ipr)

                                mean_low_ipr = np.mean(low_iprs)
                                min_low_ipr = np.min(low_iprs)
                                max_low_ipr = np.max(low_iprs)

                                # Baseline: fully delocalized = 1/N
                                clean_expected = 1.0 / N
                                ipr_ratio = mean_low_ipr / clean_expected

                                # Record
                                result = {
                                    "family": family,
                                    "j_max": int(j_max),
                                    "s1_size": int(s1_size),
                                    "alpha": float(alpha),
                                    "disorder_strength": float(disorder),
                                    "seed": int(seed),
                                    "N": int(N),
                                    "low_eigenvalues": [float(e) for e in eigvals[:n_low]],
                                    "low_iprs": [float(ipr) for ipr in low_iprs],
                                    "mean_low_ipr": float(mean_low_ipr),
                                    "min_low_ipr": float(min_low_ipr),
                                    "max_low_ipr": float(max_low_ipr),
                                    "clean_expected_ipr_scale": float(clean_expected),
                                    "ipr_ratio_to_1_over_N": float(ipr_ratio),
                                    "is_clean": disorder == 0.0,
                                    "is_j0_control": j_max == 0,
                                }
                                results.append(result)

                            except Exception as e:
                                print(f"  ERROR: {e}")
                                results.append(
                                    {
                                        "family": family,
                                        "j_max": int(j_max),
                                        "s1_size": int(s1_size),
                                        "alpha": float(alpha),
                                        "disorder_strength": float(disorder),
                                        "seed": int(seed),
                                        "error": str(e),
                                    }
                                )

    elapsed = time.time() - start_time
    print(f"Completed {case_count} cases in {elapsed:.1f}s")

    # Aggregate analysis
    clean_results = [r for r in results if r.get("is_clean", False) and "error" not in r]
    disordered_results = [r for r in results if not r.get("is_clean", False) and "error" not in r]
    non_j0_clean = [r for r in clean_results if not r.get("is_j0_control", False)]
    non_j0_disordered = [r for r in disordered_results if not r.get("is_j0_control", False)]

    if non_j0_clean and non_j0_disordered:
        # OLD METRIC (IPR ratio - kept for backward compatibility)
        clean_mean_ratio = np.mean([r["ipr_ratio_to_1_over_N"] for r in non_j0_clean])
        dis_mean_ratio = np.mean([r["ipr_ratio_to_1_over_N"] for r in non_j0_disordered])
        contrast_ratio = dis_mean_ratio / clean_mean_ratio if clean_mean_ratio > 0 else 0

        # NEW METRIC (Absolute IPR - corrected from Gate 2 investigation)
        clean_mean_abs = np.mean([r["mean_low_ipr"] for r in non_j0_clean])
        dis_mean_abs = np.mean([r["mean_low_ipr"] for r in non_j0_disordered])
        contrast_abs = dis_mean_abs / clean_mean_abs if clean_mean_abs > 0 else 0

        # Verdict based on ABSOLUTE IPR (corrected metric)
        # Thresholds calibrated from S²×S¹ vs S³×S¹ comparison:
        # S²×S¹ W=8: 1.19x, S³×S¹ W=8: 1.46x → expect 1.5-2.5x range
        if contrast_abs > 2.0:
            verdict = "ipr_smoke_pass"
        elif contrast_abs > 1.3:
            verdict = "ipr_smoke_weak_or_inconclusive"
        else:
            verdict = "ipr_smoke_fail"
    else:
        clean_mean_ratio = 0
        dis_mean_ratio = 0
        contrast_ratio = 0
        clean_mean_abs = 0
        dis_mean_abs = 0
        contrast_abs = 0
        verdict = "ipr_smoke_insufficient_data"

    aggregate = {
        "total_cases": case_count,
        "clean_cases": len(clean_results),
        "disordered_cases": len(disordered_results),
        "non_j0_clean_cases": len(non_j0_clean),
        "non_j0_disordered_cases": len(non_j0_disordered),
        # OLD METRIC (deprecated, kept for backward compatibility)
        "clean_mean_ipr_ratio": float(clean_mean_ratio),
        "disordered_mean_ipr_ratio": float(dis_mean_ratio),
        "ipr_contrast_ratio": float(contrast_ratio),
        # NEW METRIC (absolute IPR - correct)
        "clean_mean_ipr_absolute": float(clean_mean_abs),
        "disordered_mean_ipr_absolute": float(dis_mean_abs),
        "ipr_contrast_absolute": float(contrast_abs),
        "ipr_smoke_verdict": verdict,
        "elapsed_seconds": float(elapsed),
        "metric_version": "v2_absolute_ipr",  # Track metric version
    }

    # Save
    metrics_path = output_dir / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump({"aggregate": aggregate, "per_case": results}, f, indent=2)

    # Save config
    config_path = output_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # Summary
    summary_path = output_dir / "summary.md"
    with open(summary_path, "w") as f:
        f.write("# S3 x S1 Product-Discretized IPR Smoke Test (Gate 3)\n\n")
        f.write(f"**Run directory:** `{output_dir}`\n\n")
        f.write(f"**Total cases:** {case_count}\n")
        f.write(f"**Elapsed:** {elapsed:.1f}s\n")
        f.write(f"**Metric:** Absolute IPR (corrected v2)\n\n")
        f.write("## Aggregate Verdict\n\n")
        f.write(f"**Verdict:** `{verdict}`\n\n")
        f.write("### Absolute IPR (Correct Metric)\n")
        f.write(f"- Clean mean IPR: {clean_mean_abs:.4f}\n")
        f.write(f"- Disordered mean IPR: {dis_mean_abs:.4f}\n")
        f.write(f"- **Absolute contrast: {contrast_abs:.2f}x**\n\n")
        f.write("### IPR Ratio (Deprecated, for backward compatibility)\n")
        f.write(f"- Clean mean IPR ratio: {clean_mean_ratio:.4f}\n")
        f.write(f"- Disordered mean IPR ratio: {dis_mean_ratio:.4f}\n")
        f.write(f"- Ratio contrast: {contrast_ratio:.2f}x\n\n")
        f.write("## Interpretation\n\n")
        if verdict == "ipr_smoke_pass":
            f.write(
                "Disordered cases show clearly larger absolute IPR than clean cases. "
                "Spatial localization diagnostic appears consistent.\n"
            )
        elif verdict == "ipr_smoke_weak_or_inconclusive":
            f.write(
                "Absolute IPR contrast exists but is below 2.0x threshold. "
                "May require stronger disorder or represents inherent geometry limitation.\n"
            )
        elif verdict == "ipr_smoke_fail":
            f.write("No clear IPR contrast. Potential artifact or measurement issue.\n")
        else:
            f.write("Insufficient data for verdict.\n")

    # Create figures placeholder
    fig_dir = output_dir / "figures"
    fig_dir.mkdir(exist_ok=True)
    placeholder = fig_dir / ".placeholder"
    placeholder.touch()

    # Simple scatter plot
    if non_j0_clean and non_j0_disordered:
        fig, ax = plt.subplots(figsize=(8, 6))
        clean_ratios = [r["ipr_ratio_to_1_over_N"] for r in non_j0_clean]
        dis_ratios = [r["ipr_ratio_to_1_over_N"] for r in non_j0_disordered]

        ax.scatter([0] * len(clean_ratios), clean_ratios, alpha=0.6, label="Clean")
        ax.scatter([1] * len(dis_ratios), dis_ratios, alpha=0.6, label="Disordered")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Clean", "Disordered"])
        ax.set_ylabel("IPR / (1/N)")
        ax.set_title("S3xS1 IPR Smoke: Spatial Localization Contrast")
        ax.legend()
        ax.grid(alpha=0.3)

        plot_path = fig_dir / "ipr_smoke_scatter.png"
        fig.savefig(plot_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

    print(f"\n✓ Results saved to {output_dir}")
    print(f"✓ Verdict: {verdict}")
    print(
        f"✓ Absolute IPR contrast: {contrast_abs:.2f}x (clean: {clean_mean_abs:.4f}, disordered: {dis_mean_abs:.4f})"
    )
    print(f"  [Legacy ratio contrast: {contrast_ratio:.2f}x for backward compatibility]")

    return aggregate, results


def main():
    parser = argparse.ArgumentParser(description="S3xS1 IPR smoke test")
    parser.add_argument(
        "--profile",
        type=str,
        default="reduced",
        choices=["reduced", "standard"],
        help="Test profile (reduced: ~50 cases, standard: ~200 cases)",
    )
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    args = parser.parse_args()

    # Config
    if args.profile == "reduced":
        config = {
            "families": ["spectral_circle", "ring", "wilson_ring"],
            "j_max_values": [1, 2, 3],
            "s1_sizes": [8, 16],
            "alpha_values": [0.0, 0.5],
            "disorder_values": [0.0, 4.0],
            "seeds": [123, 456],
            "n_low": 5,
            "radius": 1.0,
            "mode": "geometric_weight",
        }
    else:
        config = {
            "families": ["spectral_circle", "ring", "wilson_ring"],
            "j_max_values": [1, 2, 3, 4],
            "s1_sizes": [8, 16, 24, 32],
            "alpha_values": [0.0, 0.5],
            "disorder_values": [0.0, 2.0, 4.0, 8.0],
            "seeds": [123, 456, 789],
            "n_low": 5,
            "radius": 1.0,
            "mode": "geometric_weight",
        }

    # Output
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = make_run_dir("s3_s1_ipr_smoke")

    # Run
    aggregate, results = run_ipr_smoke(output_dir, config)

    return aggregate


if __name__ == "__main__":
    main()
