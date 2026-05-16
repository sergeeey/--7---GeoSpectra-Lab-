# S1 localization gate v3 — full comparison diagnostic note

**Baseline reference (unchanged):** `v0.1.14-mvp-s2-s1-discretization-v2-full`

This is a **diagnostic** note for a full-profile S1 discretization comparison with v3 window-sweep localization metrics enabled. It is not a baseline promotion and not a new physical claim.

## Command

```bash
python scripts/s2_s1_discretization_comparison.py --full --include-wilson --enable-v3
```

## Run path

`reports/RUNS/20260513-113314_s1_discretization_comparison_full_v3`

## Artifact check

Run directory contains:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/`

## Per-family v2/v3 diagnostic summary

| Family | v2 classification | localization_gate_v3_classification | pass_rate_across_windows | window_sensitivity_score | window_robust_localization_passed | unstable_window_cases | v2_vs_v3_disagreement |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| `spectral_circle` | `quick_bridge_passed` | `window_robust_pass` | `1.0` | `0.0` | `True` | `[]` | `False` |
| `ring` | `window_selection_sensitivity` | `window_robust_pass` | `1.0` | `0.0` | `True` | `[]` | `False` |
| `wilson_ring` | `quick_bridge_passed` | `window_robust_pass` | `1.0` | `0.0` | `True` | `[]` | `False` |

## Interpretation

- All families are `window_robust_pass` under v3 on this full comparison profile.
- Record this as: **v3 full diagnostic passed** (for this profile).
- `ring` still shows historical v2 behavior `window_selection_sensitivity`, while v3 reports robust window-sweep pass and `v2_vs_v3_disagreement=False` (no fixed-window v2 vs robust-v3 contradiction).
- This is a diagnostic result only; it does not invalidate historical v2 mixed/kernel-only and stress records.
- Full/stress v3 beyond this comparison run remains a separate scope item.

## Validation step

`pytest -q` after run: **121 passed**.

## Scientific non-claims

This note and run do **not** claim:

- continuum compactification;
- `S6` or `S3×S6`;
- the Standard Model;
- physical chirality proof;
- Witten/Lichnerowicz bypass.

