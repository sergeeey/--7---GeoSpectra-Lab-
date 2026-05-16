from __future__ import annotations

import argparse
import os
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s1_discretization_comparison import (  # noqa: E402
    S1DiscretizationComparisonAssessment,
    S1DiscretizationComparisonConfig,
    run_s1_discretization_comparison,
    save_s1_discretization_comparison_artifacts,
)
from cc_toy_lab.spectral.s2_s1_product import S2S1ProductConfig  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Toy S1 discretization robustness comparison CLI.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--quick", action="store_true", help="Configured quick S1 discretization comparison.")
    mode.add_argument("--full", action="store_true", help="Configured larger S1 discretization comparison.")
    parser.add_argument("--include-wilson", action="store_true", help="Include Wilson-like ring as an extra family.")
    parser.add_argument(
        "--enable-v3",
        action="store_true",
        help=(
            "Enable localization gate v3 window sweep in the embedded benchmark (diagnostic only; "
            "does not change default quick/full behavior when omitted)."
        ),
    )
    parser.add_argument("--seed", type=int, default=12051, help="Base RNG seed for reproducible runs.")
    return parser.parse_args()


def config_from_args(args: argparse.Namespace) -> tuple[str, S1DiscretizationComparisonConfig]:
    families = ("spectral_circle", "ring", "wilson_ring") if args.include_wilson else ("spectral_circle", "ring")
    if os.environ.get("CC_TOY_LAB_S1_DISCRETIZATION_CLI_TEST_PROFILE") == "tiny":
        return (
            "quick",
            S1DiscretizationComparisonConfig(
                benchmark_template=S2S1ProductConfig(
                    q_values=(0, 1),
                    cutoff=2,
                    s1_sizes=(4, 8),
                    boundary_twists=(0.0, 0.5),
                    s1_modes=("clean", "geometric_weight"),
                    disorder_values=(0.0, 8.0),
                    perturbation_values=(0.0,),
                    realizations=1,
                    seed=args.seed,
                    note=_note_with_cli_context("tiny test profile"),
                ),
                s1_families=families,
                reference_family="spectral_circle",
                note=_comparison_note("tiny test profile"),
            ),
        )
    if args.full:
        return (
            "full",
            S1DiscretizationComparisonConfig(
                benchmark_template=S2S1ProductConfig(
                    q_values=(0, 1, -1, 2, -2),
                    cutoff=2,
                    s1_sizes=(8, 16, 24),
                    boundary_twists=(0.0, 0.25, 0.5),
                    s1_modes=("clean", "gauge_phase", "geometric_weight"),
                    disorder_values=(0.0, 1.0, 2.0, 4.0, 8.0),
                    perturbation_values=(0.0, 1e-5),
                    realizations=5,
                    seed=args.seed,
                    note=_note_with_cli_context("full comparison profile uses cutoff=2 for runtime safety"),
                ),
                s1_families=families,
                reference_family="spectral_circle",
                note=_comparison_note("full comparison profile"),
            ),
        )
    return (
        "quick",
        S1DiscretizationComparisonConfig(
            benchmark_template=S2S1ProductConfig(
                q_values=(0, 1, -1),
                cutoff=2,
                s1_sizes=(8, 16),
                boundary_twists=(0.0, 0.25, 0.5),
                s1_modes=("clean", "geometric_weight"),
                disorder_values=(0.0, 8.0),
                perturbation_values=(0.0,),
                realizations=1,
                seed=args.seed,
                note=_note_with_cli_context("quick comparison profile"),
            ),
            s1_families=families,
            reference_family="spectral_circle",
            note=_comparison_note("quick comparison profile"),
        ),
    )


def _apply_v3_if_requested(
    config: S1DiscretizationComparisonConfig, enable_v3: bool
) -> S1DiscretizationComparisonConfig:
    if not enable_v3:
        return config
    extra = " localization_gate_v3 window sweep enabled (diagnostic only, not a new physical claim)."
    return replace(
        config,
        benchmark_template=replace(
            config.benchmark_template,
            localization_gate_v3_enabled=True,
            note=config.benchmark_template.note + extra,
        ),
        note=config.note + extra,
    )


def run(args: argparse.Namespace) -> tuple[Path, S1DiscretizationComparisonAssessment, dict]:
    mode, config = config_from_args(args)
    config = _apply_v3_if_requested(config, args.enable_v3)
    assessment = run_s1_discretization_comparison(config)
    run_dir = make_run_dir(mode, v3=args.enable_v3)
    artifacts = save_s1_discretization_comparison_artifacts(assessment, run_dir)
    print_summary(mode=mode, run_dir=run_dir, assessment=assessment, enable_v3=args.enable_v3)
    return run_dir, assessment, artifacts


def make_run_dir(mode: str, *, v3: bool = False) -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base_dir = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = "_v3" if v3 else ""
    run_dir = base_dir / f"{stamp}_s1_discretization_comparison_{mode}{suffix}"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def print_summary(
    mode: str, run_dir: Path, assessment: S1DiscretizationComparisonAssessment, *, enable_v3: bool
) -> None:
    print(f"run_path={run_dir}")
    print(f"comparison_classification={assessment.classification}")
    print(f"reference_family={assessment.reference_family}")
    print(f"all_families_match_reference={assessment.all_families_match_reference}")
    print(f"all_families_pass_basic_gates={assessment.all_families_pass_basic_gates}")
    print(f"family_count={len(assessment.family_results)}")
    if enable_v3:
        print(
            "localization_gate_v3_diagnostic=true "
            "(toy window sweep; not continuum compactification, not SM, not physical chirality proof)"
        )
        for result in assessment.family_results:
            fam = result.family
            a = result.assessment
            print(f"family={fam} classification_v2={a.classification}")
            print(
                f"family={fam} localization_gate_v3_classification={a.localization_gate_v3_classification} "
                f"pass_rate_across_windows={a.pass_rate_across_windows} "
                f"window_sensitivity_score={a.window_sensitivity_score} "
                f"window_robust_localization_passed={a.window_robust_localization_passed} "
                f"v2_vs_v3_disagreement={a.v2_vs_v3_disagreement}"
            )
    print(f"s1_discretization_comparison_{mode} complete")


def _comparison_note(extra_note: str) -> str:
    return (
        "Toy S1 discretization robustness comparison for the S2 x S1 product benchmark. "
        "This does not claim continuum compactification or a full-product global chiral "
        f"index theorem. CLI context: {extra_note}."
    )


def _note_with_cli_context(extra_note: str) -> str:
    return (
        "Toy S2 x S1 product benchmark used inside S1 discretization comparison. "
        "This module constructs the operator core only and does not claim continuum "
        f"compactification. CLI context: {extra_note}."
    )


def main() -> int:
    args = parse_args()
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
