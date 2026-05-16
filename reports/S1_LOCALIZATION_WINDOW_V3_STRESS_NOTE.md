# S1 localization gate v3 - stress diagnostic note

**Baseline reference (unchanged):** `v0.1.14-mvp-s2-s1-discretization-v2-full`

This note records a stress-level toy diagnostic run with explicit v3 enablement. It does not auto-promote any baseline and does not replace historical records.

## Command

```bash
python scripts/s2_s1_discretization_v2_stress.py --realizations 5 --enable-v3
```

## Run path

`reports/RUNS/20260513-130413_s1_discretization_v2_stress_v3`

## Artifact check

Run directory contains:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/`

## Core stress status

- `stress_classification`: `v2_limitation`
- `comparison_classification`: `robust_across_discretizations`
- `case_level_fixed_window_all_passed`: `False`
- v3 case-level result availability: `False` (current stress diagnostics are family-aggregate for v3)

## Per-family v2/v3 snapshot

| Family | v2 classification | localization_gate_v3_classification | pass_rate_across_windows | window_sensitivity_score | window_robust_localization_passed | unstable_window_cases | v2_vs_v3_disagreement |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| `spectral_circle` | `quick_bridge_passed` | `window_robust_pass` | `1.0` | `0.0` | `True` | `[]` | `False` |
| `ring` | `quick_bridge_passed` | `window_robust_pass` | `1.0` | `0.0` | `True` | `[]` | `False` |
| `wilson_ring` | `quick_bridge_passed` | `window_robust_pass` | `1.0` | `0.0` | `True` | `[]` | `False` |

## Stress diagnostics requested in this run

- `v3_all_families_window_robust`: `True`
- `v3_failure_count_by_family`: `{}`
- `v2_vs_v3_disagreement_count_by_family`: `{}`
- `failure_count_by_family` (v2 case-level fixed-window): `{"ring": 988, "spectral_circle": 788, "wilson_ring": 600}`
- `failure_count_by_disorder` (v2 case-level fixed-window): `{"0": 1800, "1": 315, "2": 213, "4": 47, "8": 1}`
- Disorder split (from the same `failure_count_by_disorder`):
  - `W=0`: `1800`
  - `W=1-4`: `575` (`315 + 213 + 47`)
  - `W>=8`: `1` (`W=8: 1`, `W=12/16: 0`)

## Interpretation

- v3 aggregate diagnostics show **all families `window_robust_pass`**, no v3 family failures, and no v2-v3 disagreement counters.
- Relative to historical v2 stress limitation tracking, this is a **v3 stress improvement at family aggregate level**.
- At the same time, stress diagnostics still expose large v2 case-level fixed-window failure counts (including one `W>=8` case), and v3 case-level stress diagnostics are not yet implemented in this artifact.
- Therefore this note records **improvement, with scope limitation**, not a project-wide or physics-level proof.

## Regression checks

- `pytest -q`: **123 passed**

## Historical records preserved

This run/note does not erase or reinterpret prior records:

- kernel-only mixed result history
- v2 fixed-window result history
- v2 stress limitation history
- W=8 targeted diagnostic history
- v3 quick/full diagnostic notes

## Scientific non-claims

This diagnostic note and run do **not** claim:

- continuum compactification;
- `S6` / `S3xS6`;
- the Standard Model;
- physical chirality proof;
- Witten/Lichnerowicz bypass.

