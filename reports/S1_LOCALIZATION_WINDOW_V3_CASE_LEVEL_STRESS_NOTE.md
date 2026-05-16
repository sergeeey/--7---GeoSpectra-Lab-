# S1 localization gate v3 — case-level stress diagnostic note

**Baseline reference (unchanged):** `v0.1.14-mvp-s2-s1-discretization-v2-full`

This note records the **completed** case-level v3 stress run. It is diagnostic metadata only: **no baseline promotion**, no erasure of historical v2 / kernel-only / prior stress records, and **no physical claims** (see non-claims below).

## Command

```bash
python scripts/s2_s1_discretization_v2_stress.py --realizations 5 --enable-v3
```

## Run path

`reports/RUNS/20260513-213053_s1_discretization_v2_stress_v3`

## Artifact check

Present under the run directory: `config.json`, `metrics.json`, `data.npz`, `summary.md`, `figures/`.

## Top-level outcomes

- `stress_classification`: `v2_limitation`
- `comparison_classification`: `robust_across_discretizations`
- `v3_case_level_result_available`: `true`
- `v3_case_level_all_passed`: `false`

## Case-level v3 aggregates (from `metrics.json` → `stress_diagnostics`)

- `v3_failure_cases` length: **2524**
- `v3_failure_count_by_family`: `ring=1060`, `spectral_circle=864`, `wilson_ring=600`
- `v3_failure_count_by_disorder`: `0→1800`, `1→414`, `2→246`, `4→58`, `8→4`, `12→1`, `16→1`
- `v3_failure_count_by_s1_size`: `8→649`, `16→628`, `24→620`, `32→627`
- `v3_failure_count_by_alpha`: `0.0→1039`, `0.25→739`, `0.5→746`
- `v3_failure_count_by_q`: `-1→480`, `-2→486`, `0→569`, `1→535`, `2→454`
- `v3_window_sensitive_cases` count: **0**
- `v3_fragile_pass_cases` count: **297**
- `v2_vs_v3_disagreement_count_by_family`: `ring=106`, `spectral_circle=82`, `wilson_ring=0` (implicit; absent key = 0)

Per-case `v2_vs_v3_disagreement` is stored on each case in `all_cases` / `data.npz` arrays; family-level disagreement counts are above.

## W-split on v3 failures (disorder axis)

From `v3_failure_count_by_disorder`:

| Split | Count |
| --- | ---: |
| W = 0 | 1800 |
| W = 1–4 (keys 1, 2, 4) | 718 |
| W ≥ 8 | 6 |

## Verdict (interpretation rules)

- `v3_case_level_all_passed` is **false**.
- There are **v3 failures at W ≥ 8** (total **6** across `8`, `12`, `16`).

**Verdict:** **unresolved v3 strong-disorder limitation** (rule: any W ≥ 8 v3 failure).  
There is additionally a large **W = 0** failure mass (transition / clean-disorder contrast in this toy diagnostic), but the W ≥ 8 tail is decisive for the stated verdict class.

## Scientific non-claims

This run and note do **not** claim continuum compactification, **S6** / **S3×S6**, the **Standard Model**, **physical chirality**, or a **Witten/Lichnerowicz bypass**.

## Regression check

`pytest -q` after follow-up: **124 passed** (run on 2026-05-13 in this workspace).

## Background jobs note

A later duplicate stress invocation was **terminated without completing** (no new run directory / no `run_path=` line). The authoritative completed artifact for this task is **`20260513-213053_s1_discretization_v2_stress_v3`**.

Operational note (2026-05-14): the duplicate termination is **consistent with a non-graceful system shutdown / reboot** overnight **13→14 May** (Windows `Kernel-Power` / unexpected shutdown around local midnight, then a normal morning boot). That event **does not invalidate** the completed stress artifact above: the interrupted duplicate was **not** used as a data source, and **baseline was not changed** on that account.
