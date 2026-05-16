"""CLI: toy product-discretized S2 x S1 tiny / medium / full diagnostic (Kronecker-sum scaffold)."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cc_toy_lab.spectral.s2_s1_product_discretized import (  # noqa: E402
    ProductDiscretizedCaseResult,
    ProductDiscretizedConfig,
    build_product_discretized_config,
    estimate_product_discretized_case_count,
    full_profile_dry_run_report,
    medium_profile_dry_run_report,
    run_product_discretized_full,
    run_product_discretized_medium,
    run_product_discretized_tiny,
    save_product_discretized_artifacts,
    serialize_product_discretized_case,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Toy product-discretized S2 x S1 diagnostic (tiny, medium, or full dry-run / guarded full)."
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--tiny", action="store_true", help="Run tiny profile (default grid; --seed applies).")
    g.add_argument("--medium", action="store_true", help="Run medium profile (fixed grid; seeds 123,456).")
    g.add_argument(
        "--full",
        action="store_true",
        help="Full profile grid: use --dry-run for counts only, or --confirm-full-run for real execution.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="With --medium or --full: print grid estimate without operator computations.",
    )
    p.add_argument(
        "--confirm-full-run",
        action="store_true",
        help="With --full only: execute the real 6615-case full profile (long job). Mutually exclusive with --dry-run.",
    )
    p.add_argument("--seed", type=int, default=123, help="RNG seed for tiny profile S1 disorder realizations.")
    p.add_argument(
        "--output-root",
        type=str,
        default=None,
        help="Optional root directory for reports/RUNS (default: repo reports/RUNS).",
    )
    return p.parse_args()


def make_run_dir(suffix: str) -> Path:
    root_override = os.environ.get("CC_TOY_LAB_RUNS_ROOT")
    base = Path(root_override) if root_override else ROOT / "reports" / "RUNS"
    stamp = os.environ.get("CC_TOY_LAB_FIXED_TIMESTAMP") or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = base / f"{stamp}_s2_s1_product_discretized_{suffix}"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def _write_initial_confirmed_full_files(
    run_dir: Path,
    cfg: ProductDiscretizedConfig,
    *,
    command: str,
    baseline_informational: str,
    started_at: str,
) -> None:
    _atomic_write_json(run_dir / "config.json", asdict(cfg))
    _atomic_write_json(
        run_dir / "run_status.json",
        {
            "status": "running",
            "profile_name": "full",
            "expected_case_count": 6615,
            "started_at": started_at,
            "baseline_informational": baseline_informational,
            "command": command,
            "incomplete_artifacts_warning": (
                "metrics.json, data.npz, and summary.md are incomplete until run_status.json "
                "reports status=completed."
            ),
            "resume_note": (
                "partial_results.jsonl records primary-grid cases in order; automatic resume "
                "from partial progress is not implemented yet — see "
                "reports/S2_S1_PRODUCT_DISCRETIZED_FULL_INTERRUPTION_HARDENING_NOTE.md."
            ),
        },
    )


def _write_run_status_failed(
    run_dir: Path,
    *,
    baseline_informational: str,
    command: str,
    started_at: str,
    error: str,
    primary_done: int,
    repro_done: int,
) -> None:
    _atomic_write_json(
        run_dir / "run_status.json",
        {
            "status": "failed",
            "profile_name": "full",
            "expected_case_count": 6615,
            "started_at": started_at,
            "failed_at": _utc_now_iso(),
            "baseline_informational": baseline_informational,
            "command": command,
            "error": error,
            "completed_primary_cases": int(primary_done),
            "completed_repro_cases": int(repro_done),
            "completed_cases": int(primary_done + repro_done),
            "incomplete_artifacts_warning": (
                "Run failed; metrics.json may be absent or incomplete. "
                "Inspect progress.json and partial_results.jsonl for partial progress."
            ),
        },
    )


def _write_run_status_completed(
    run_dir: Path,
    *,
    started_at: str,
    baseline_informational: str,
    command: str,
    classification: str,
) -> None:
    _atomic_write_json(
        run_dir / "run_status.json",
        {
            "status": "completed",
            "profile_name": "full",
            "expected_case_count": 6615,
            "completed_cases": 6615,
            "completed_primary_cases": 6615,
            "completed_repro_cases": 6615,
            "classification": classification,
            "started_at": started_at,
            "completed_at": _utc_now_iso(),
            "baseline_informational": baseline_informational,
            "command": command,
        },
    )


class _FullRunProgressWriter:
    """Disk-backed progress for guarded full runs (primary grid + reproducibility pass)."""

    def __init__(self, run_dir: Path, expected_case_count: int) -> None:
        self._run_dir = run_dir
        self._expected = int(expected_case_count)
        self._primary_done = 0
        self._repro_done = 0
        self._partial = (run_dir / "partial_results.jsonl").open("w", encoding="utf-8")

    def counts(self) -> tuple[int, int]:
        return (self._primary_done, self._repro_done)

    def close(self) -> None:
        if self._partial.closed:
            return
        self._partial.close()

    def __call__(self, phase: str, _index: int, case: ProductDiscretizedCaseResult) -> None:
        if phase == "primary":
            self._primary_done += 1
            self._partial.write(json.dumps(serialize_product_discretized_case(case), sort_keys=True) + "\n")
            self._partial.flush()
            self._write_progress("primary_grid", case)
        elif phase == "repro":
            self._repro_done += 1
            self._write_progress("reproducibility_pass", case)

    def _write_progress(self, grid_phase: str, case: ProductDiscretizedCaseResult) -> None:
        total_steps = 2 * self._expected
        done_steps = self._primary_done + self._repro_done
        pct = 100.0 * float(done_steps) / float(total_steps) if total_steps else 0.0
        payload: dict[str, Any] = {
            "expected_case_count": self._expected,
            "expected_step_count": total_steps,
            "completed_primary_cases": self._primary_done,
            "completed_repro_cases": self._repro_done,
            "completed_cases": done_steps,
            "completed_cases_note": (
                "completed_cases counts analyzer invocations across the primary grid and the "
                "reproducibility duplication pass (2 * expected_case_count when finished)."
            ),
            "percent_complete": round(pct, 6),
            "phase": grid_phase,
            "current": {
                "q": case.q,
                "s1_family": case.s1_family,
                "s1_size": case.s1_size,
                "alpha": case.alpha,
                "W": case.disorder_strength,
                "seed": case.seed,
            },
            "last_update_time": _utc_now_iso(),
        }
        _atomic_write_json(self._run_dir / "progress.json", payload)


def main() -> int:
    args = parse_args()

    if args.confirm_full_run and not args.full:
        print("error: --confirm-full-run requires --full", file=sys.stderr)
        return 2

    if args.full and args.dry_run and args.confirm_full_run:
        print("error: cannot combine --dry-run with --confirm-full-run", file=sys.stderr)
        return 2

    if args.full and not args.dry_run and not args.confirm_full_run:
        print(
            "error: --full requires --dry-run (grid estimate only) or --confirm-full-run "
            "(real 6615-case execution). Bare --full is disabled to prevent accidental long runs.",
            file=sys.stderr,
        )
        return 2

    if args.dry_run and not args.medium and not args.full:
        print("error: --dry-run requires --medium or --full", file=sys.stderr)
        return 2

    if args.output_root:
        os.environ["CC_TOY_LAB_RUNS_ROOT"] = str(Path(args.output_root).resolve())

    if args.full and args.dry_run:
        cfg = build_product_discretized_config(full=True)
        rep = full_profile_dry_run_report(cfg)
        print(f"profile_name={rep['profile_name']}")
        print(f"expected_case_count={rep['expected_case_count']}")
        print(f"grid_dimensions={json.dumps(rep['grid_dimensions'], sort_keys=True)}")
        print(f"estimated_run_dir_suffix={rep['estimated_run_dir_suffix']}")
        print(f"baseline_informational={rep['baseline_informational']}")
        print("warning: no operators were computed (dry-run only).")
        print(
            "warning: a real --full run is much heavier than medium and must be launched intentionally "
            "with logging and artifact checks."
        )
        print("full profile dry-run complete (no operators computed)")
        return 0

    if args.full and args.confirm_full_run:
        cfg = build_product_discretized_config(full=True)
        if cfg.profile_name != "full":
            print(f"error: full run aborted: expected profile_name='full', got {cfg.profile_name!r}", file=sys.stderr)
            return 2
        n = estimate_product_discretized_case_count(cfg)
        if n != 6615:
            print(f"error: full run aborted: expected_case_count must be 6615, got {n}", file=sys.stderr)
            return 2
        print(
            "warning: This is a long full-profile run; do not start duplicates.",
            file=sys.stderr,
        )
        dry_rep = full_profile_dry_run_report(cfg)
        baseline_informational = str(dry_rep["baseline_informational"])
        command = " ".join(shlex.quote(a) for a in sys.argv)
        started_at = _utc_now_iso()
        run_dir = make_run_dir("full")
        _write_initial_confirmed_full_files(
            run_dir,
            cfg,
            command=command,
            baseline_informational=baseline_informational,
            started_at=started_at,
        )
        print(f"run_path={run_dir}", flush=True)
        progress = _FullRunProgressWriter(run_dir, n)
        try:
            assessment = run_product_discretized_full(cfg, after_each_case=progress)
        except Exception as exc:
            p_done, r_done = progress.counts()
            progress.close()
            _write_run_status_failed(
                run_dir,
                baseline_informational=baseline_informational,
                command=command,
                started_at=started_at,
                error=f"{type(exc).__name__}: {exc}",
                primary_done=p_done,
                repro_done=r_done,
            )
            print(f"error: full run failed: {exc}", file=sys.stderr)
            return 1
        progress.close()
        save_product_discretized_artifacts(assessment, run_dir)
        _write_run_status_completed(
            run_dir,
            started_at=started_at,
            baseline_informational=baseline_informational,
            command=command,
            classification=assessment.classification,
        )
        print(f"baseline_informational={assessment.baseline_tag} (unchanged; not a promotion)")
        print(f"run_path={run_dir}")
        print(f"classification={assessment.classification}")
        print(
            "gates="
            f"hermiticity={assessment.hermiticity_all_passed};"
            f"shape={assessment.shape_all_passed};"
            f"repro={assessment.reproducibility_passed};"
            f"q0={assessment.q0_controls_all_passed}"
        )
        print("s2_s1_product_discretized_full complete")
        return 0

    if args.medium and args.dry_run:
        cfg = build_product_discretized_config(medium=True)
        rep = medium_profile_dry_run_report(cfg)
        print(f"expected_case_count={rep['expected_case_count']}")
        print(f"grid_dimensions={json.dumps(rep['grid_dimensions'], sort_keys=True)}")
        print(f"estimated_run_dir_suffix={rep['estimated_run_dir_suffix']}")
        print(f"baseline_informational={rep['baseline_informational']}")
        print("medium dry-run complete (no operators computed)")
        return 0

    if args.tiny:
        cfg = build_product_discretized_config(tiny=True, seed=int(args.seed))
        assessment = run_product_discretized_tiny(cfg)
        run_dir = make_run_dir("tiny")
        save_product_discretized_artifacts(assessment, run_dir)
        print(f"run_path={run_dir}")
        print(f"classification={assessment.classification}")
        print(
            "gates="
            f"hermiticity={assessment.hermiticity_all_passed};"
            f"shape={assessment.shape_all_passed};"
            f"repro={assessment.reproducibility_passed};"
            f"q0={assessment.q0_controls_all_passed}"
        )
        print("s2_s1_product_discretized_tiny complete")
        return 0

    cfg = build_product_discretized_config(medium=True)
    assessment = run_product_discretized_medium(cfg)
    run_dir = make_run_dir("medium")
    save_product_discretized_artifacts(assessment, run_dir)
    print(f"run_path={run_dir}")
    print(f"classification={assessment.classification}")
    print(
        "gates="
        f"hermiticity={assessment.hermiticity_all_passed};"
        f"shape={assessment.shape_all_passed};"
        f"repro={assessment.reproducibility_passed};"
        f"q0={assessment.q0_controls_all_passed}"
    )
    print("s2_s1_product_discretized_medium complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
