"""S2 x S1 Product-Discretized IPR Smoke Test

Quick spatial-localization sanity check before 6615-case full run.

Representative grid: ~30-50 cases
- families: spectral_circle, ring, wilson_ring
- q: 0, 1, -1
- s1_sizes: 8, 16, 24
- alpha: 0.0, 0.5
- W: 0.0, 4.0, 8.0
- seeds: 123, 456

Metrics:
- IPR for low modes
- mean/min/max low IPR
- IPR ratio to 1/N (delocalization baseline)
- v3 classification if available
- q0 control flag

Verdict:
- pass: disordered IPR clearly > clean IPR
- weak: contrast small or family-dependent
- fail: no contrast or q0 anomalies
"""

import argparse
import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from cc_toy_lab.runs import make_run_dir
from cc_toy_lab.spectral.s2_s1_product import build_s2_s1_product_operator


def compute_ipr_for_eigenvector(psi):
    """Inverse participation ratio: sum(|psi_i|^4)"""
    return np.sum(np.abs(psi) ** 4)


def run_ipr_smoke(output_dir: Path, config: dict):
    """Run IPR smoke test."""
    families = config["families"]
    q_values = config["q_values"]
    s1_sizes = config["s1_sizes"]
    alpha_values = config["alpha_values"]
    disorder_values = config["disorder_values"]
    seeds = config["seeds"]
    n_low = config.get("n_low", 5)  # number of low modes to analyze
    cutoff = config.get("cutoff", 2)
    mode = config.get("mode", "gauge_phase")  # Use mode that responds to disorder

    results = []
    case_count = 0
    total_cases = (
        len(families)
        * len(q_values)
        * len(s1_sizes)
        * len(alpha_values)
        * len(disorder_values)
        * len(seeds)
    )

    print(f"Starting IPR smoke test: {total_cases} cases")
    start_time = time.time()

    for family in families:
        for q in q_values:
            for s1_size in s1_sizes:
                for alpha in alpha_values:
                    for disorder in disorder_values:
                        for seed in seeds:
                            case_count += 1
                            print(
                                f"[{case_count}/{total_cases}] "
                                f"family={family} q={q} s1={s1_size} "
                                f"alpha={alpha:.1f} disorder={disorder:.1f} seed={seed}"
                            )

                            try:
                                # Build operator
                                D, _, _ = build_s2_s1_product_operator(
                                    q=q,
                                    s1_family=family,
                                    s1_size=s1_size,
                                    alpha=alpha,
                                    mode=mode,
                                    disorder_strength=disorder,
                                    seed=seed,
                                    cutoff=cutoff,
                                )

                                N = D.shape[0]

                                # Compute spectrum
                                eigvals, eigvecs = np.linalg.eigh(D)
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
                                    "q": int(q),
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
                                    "is_q0_control": q == 0,
                                }
                                results.append(result)

                            except Exception as e:
                                print(f"  ERROR: {e}")
                                results.append(
                                    {
                                        "family": family,
                                        "q": int(q),
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
    non_q0_clean = [r for r in clean_results if not r.get("is_q0_control", False)]
    non_q0_disordered = [r for r in disordered_results if not r.get("is_q0_control", False)]

    if non_q0_clean and non_q0_disordered:
        clean_mean_ratio = np.mean([r["ipr_ratio_to_1_over_N"] for r in non_q0_clean])
        dis_mean_ratio = np.mean([r["ipr_ratio_to_1_over_N"] for r in non_q0_disordered])
        contrast = dis_mean_ratio / clean_mean_ratio if clean_mean_ratio > 0 else 0

        # Verdict
        if contrast > 2.0:
            verdict = "ipr_smoke_pass"
        elif contrast > 1.3:
            verdict = "ipr_smoke_weak_or_inconclusive"
        else:
            verdict = "ipr_smoke_fail"
    else:
        clean_mean_ratio = 0
        dis_mean_ratio = 0
        contrast = 0
        verdict = "ipr_smoke_insufficient_data"

    aggregate = {
        "total_cases": case_count,
        "clean_cases": len(clean_results),
        "disordered_cases": len(disordered_results),
        "non_q0_clean_cases": len(non_q0_clean),
        "non_q0_disordered_cases": len(non_q0_disordered),
        "clean_mean_ipr_ratio": float(clean_mean_ratio),
        "disordered_mean_ipr_ratio": float(dis_mean_ratio),
        "ipr_contrast_ratio": float(contrast),
        "ipr_smoke_verdict": verdict,
        "elapsed_seconds": float(elapsed),
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
        f.write("# S2 x S1 Product-Discretized IPR Smoke Test\n\n")
        f.write(f"**Run directory:** `{output_dir}`\n\n")
        f.write(f"**Total cases:** {case_count}\n")
        f.write(f"**Elapsed:** {elapsed:.1f}s\n\n")
        f.write("## Aggregate Verdict\n\n")
        f.write(f"**Verdict:** `{verdict}`\n\n")
        f.write(f"- Clean mean IPR ratio: {clean_mean_ratio:.4f}\n")
        f.write(f"- Disordered mean IPR ratio: {dis_mean_ratio:.4f}\n")
        f.write(f"- Contrast: {contrast:.2f}x\n\n")
        f.write("## Interpretation\n\n")
        if verdict == "ipr_smoke_pass":
            f.write(
                "Disordered cases show clearly larger IPR than clean cases. "
                "Spatial localization diagnostic appears consistent.\n"
            )
        elif verdict == "ipr_smoke_weak_or_inconclusive":
            f.write(
                "Contrast exists but is small. May be family-dependent or "
                "require stronger disorder.\n"
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
    if non_q0_clean and non_q0_disordered:
        fig, ax = plt.subplots(figsize=(8, 6))
        clean_ratios = [r["ipr_ratio_to_1_over_N"] for r in non_q0_clean]
        dis_ratios = [r["ipr_ratio_to_1_over_N"] for r in non_q0_disordered]

        ax.scatter([0] * len(clean_ratios), clean_ratios, alpha=0.6, label="Clean")
        ax.scatter([1] * len(dis_ratios), dis_ratios, alpha=0.6, label="Disordered")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Clean", "Disordered"])
        ax.set_ylabel("IPR / (1/N)")
        ax.set_title("IPR Smoke: Spatial Localization Contrast")
        ax.legend()
        ax.grid(alpha=0.3)

        fig_path = fig_dir / "ipr_smoke_scatter.png"
        plt.savefig(fig_path, dpi=150, bbox_inches="tight")
        plt.close()

    print(f"\nIPR Smoke Test Complete")
    print(f"Verdict: {verdict}")
    print(f"Run directory: {output_dir}")

    return aggregate


def main():
    parser = argparse.ArgumentParser(description="S2xS1 IPR Smoke Test")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: auto-generate)",
    )
    args = parser.parse_args()

    # Config
    config = {
        "families": ["spectral_circle", "ring", "wilson_ring"],
        "q_values": [0, 1, -1],
        "s1_sizes": [8, 16, 24],
        "alpha_values": [0.0, 0.5],
        "disorder_values": [0.0, 4.0, 8.0],
        "seeds": [123, 456],
        "n_low": 5,
        "cutoff": 2,
        "mode": "gauge_phase",
    }

    # Output
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = make_run_dir("s2_s1_product_discretized_ipr_smoke")

    # Run
    aggregate = run_ipr_smoke(output_dir, config)

    # Print summary
    print("\n" + "=" * 60)
    print("IPR SMOKE SUMMARY")
    print("=" * 60)
    print(f"Verdict: {aggregate['ipr_smoke_verdict']}")
    print(f"Clean mean ratio: {aggregate['clean_mean_ipr_ratio']:.4f}")
    print(f"Disordered mean ratio: {aggregate['disordered_mean_ipr_ratio']:.4f}")
    print(f"Contrast: {aggregate['ipr_contrast_ratio']:.2f}x")
    print("=" * 60)


if __name__ == "__main__":
    main()
