# S2 x S1 Product-Discretized Full Readiness Audit

**Audit type:** pre-enablement documentation + code review (no real `--full` run,
no CLI guard removal, no metrics changes).

**Baseline (informational):** `v0.1.14-mvp-s2-s1-discretization-v2-full` (unchanged).

**Audited artifacts (read):**

- `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_PROFILE_PLAN.md`
- `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_DRY_RUN_NOTE.md`
- `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_RUN_READINESS.md`
- `cc_toy_lab/spectral/s2_s1_product_discretized.py`
- `scripts/s2_s1_product_discretized.py`
- `tests/test_s2_s1_product_discretized.py`

## Checklist

| Check | Evidence | Result |
| --- | --- | --- |
| **Full grid matches plan** | `build_product_discretized_config(full=True)` sets `q_values=(0,1,-1,2,-2,3,-3)`, default `s1_families`, `s1_sizes=(8,16,24,32,48)`, `alpha_values=(0.0,0.25,0.5)`, `w_values=(0.0,2,4,6,8,12,16)`, `seeds=(123,456,789)`, `low_energy_count_values=(4,6,8,10,12)`, `spectator_large_s1=48` — matches plan table. | **Pass** |
| **`expected_case_count` = 6615** | `estimate_product_discretized_case_count`: `len(seeds)×len(q)×len(families)×len(sizes)×len(alpha)×len(W)` = `3×7×3×5×3×7` = **6615**; `full_profile_dry_run_report` uses same helper; tests assert `6615`. | **Pass** |
| **`low_energy_count_values` not outer multiplier** | Plan §Proposed Full Grid + §Estimated Size; dry-run note; `estimate_product_discretized_case_count` excludes `low_energy_count_values`; dry-run `grid_dimensions` includes `low_energy_count_values: 5` for transparency only. | **Pass** |
| **`--full --dry-run` does not compute operators** | CLI branch calls only `build_product_discretized_config(full=True)` and `full_profile_dry_run_report(cfg)` — no `build_product_discretized_operator`, no `run_product_discretized_*`. | **Pass** |
| **Real `--full` guarded** | `main()`: `if args.full and not args.dry_run:` → stderr message, **exit 2**. | **Pass** |
| **`--tiny` / `--medium` unchanged** | `tiny` → `run_product_discretized_tiny` + artifacts (unchanged path). `medium` without `--dry-run` → `run_product_discretized_medium` + artifacts. `medium --dry-run` → `medium_profile_dry_run_report` only. | **Pass** |
| **Mutually exclusive profiles** | `argparse` mutually exclusive group for `--tiny` / `--medium` / `--full`; tests enforce combinations. | **Pass** |
| **Caveat counters documented** | `FULL_PROFILE_PLAN.md` §Caveat Tracking lists `q0_false_positive_count`, ring/alpha0, transition/mid/strong bands, v2/v3 disagreement, v3 stratification. | **Pass** (full *runner* must emit these when implemented) |
| **`q0` control in contract** | `ProductDiscretizedCaseResult.q0_control_passed`; `analyze_product_discretized_case` sets `q0_control_passed`; assessment `q0_controls_all_passed`; summary/metrics surface. | **Pass** |
| **No global chiral index headline** | `ProductDiscretizedConfig.note` states not a global chiral index headline; `_build_summary_markdown` includes explicit non-claim line. | **Pass** |
| **Docs ↔ code alignment (dry-run)** | Dry-run note stdout matches CLI: `profile_name=full`, `expected_case_count=6615`, suffix `_s2_s1_product_discretized_full`, warnings. | **Pass** |
| **No physical overclaim in audited strings** | CLI/help and audited module docstring emphasize toy / diagnostic; non-claims in summary builder. | **Pass** |

## Gaps (non-blocking for guard removal design review)

1. **`run_product_discretized_full` (or equivalent)** is **not** implemented yet — only config + dry-run exist. Enabling real `--full` in CLI will require implementing the runner, artifact writer, and metrics parity with medium/tiny **before** removing the guard.
2. **README.md** may still cite older `pytest` counts elsewhere in the repo; authoritative validation remains `reports/VALIDATION_STATUS.md` (informational: **187 passed** after guarded-runner wiring).

## Interpretation Contract (unchanged)

Per `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_PROFILE_PLAN.md`: control failure on
`q0_false_positive_count > 0`; transition-regime ring caveat; unresolved
strong-disorder if failures spread at `W >= 8`; `v0.1.15` only after independent
audit if full supports medium/W4 structure without new control failures.

## Scientific Non-Claims (repeated)

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** physical validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.

## Verdict

**`ready_to_enable_guarded_full`**

Rationale: plan, dry-run note, readiness checkpoint, config grid, case-count math,
CLI dry-run path, rejection of bare `--full`, guarded **`--confirm-full-run`** path,
and regression tests are **consistent**. A **canonical** `6615`-case run remains an
**operator-time** choice, not part of this wiring commit.

## Post-audit pytest (recorded)

Executed in the same session as this audit (exit code **0**):

- `pytest tests/test_s2_s1_product_discretized.py -q` → **27 passed** in **1081.18 s**
- `pytest -q` → **187 passed** in **1178.60 s**
