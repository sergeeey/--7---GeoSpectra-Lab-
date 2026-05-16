# S1 localization gate v3 — ring strong-disorder failure diagnostic

**Baseline (unchanged):** `v0.1.14-mvp-s2-s1-discretization-v2-full`

**Source slice:** `reports/S1_LOCALIZATION_WINDOW_V3_STRONG_DISORDER_FAILURE_ANALYSIS.md`  
**Source stress run:** `reports/RUNS/20260513-213053_s1_discretization_v2_stress_v3`

This memo describes a **targeted toy diagnostic** to separate small-`N` effects, `alpha=0` regime coupling, ring-only discretization artifacts, seed instability, and a broader unresolved v3 strong-disorder limitation.

## Scientific non-claims

No continuum compactification, **S6** / **S3×S6**, **Standard Model**, **physical chirality**, or **Witten/Lichnerowicz bypass**. No baseline promotion. No change to existing stress metrics definitions. Historical v2 / kernel-only / stress records remain authoritative for their runs.

## Six anchor cases (must reproduce in diagnostic)

| # | family | q | s1_size | alpha | W | seed |
|---:|---|---:|---:|---:|---:|---:|
| 1 | ring | 1 | 8 | 0.0 | 8.0 | 11836052 |
| 2 | ring | −1 | 8 | 0.0 | 8.0 | 9836055 |
| 3 | ring | 2 | 8 | 0.0 | 12.0 | 12837054 |
| 4 | ring | 2 | 8 | 0.0 | 16.0 | 12838052 |
| 5 | ring | 2 | 16 | 0.0 | 8.0 | 13636052 |
| 6 | ring | 2 | 24 | 0.0 | 8.0 | 14436152 |

## Script and artifacts

```text
python scripts/s1_v3_ring_failure_diagnostic.py
python scripts/s1_v3_ring_failure_diagnostic.py --seed-span 2
python scripts/s1_v3_ring_failure_diagnostic.py --tiny
```

- **Full sweep:** Cartesian product of  
  `family ∈ (ring, spectral_circle, wilson_ring)`,  
  `q ∈ {-2, -1, 1, 2}` (union of anchor charges and ±2, ±1),  
  `s1_size ∈ (8, 16, 24, 32, 48)`,  
  `alpha ∈ (0.0, 0.25, 0.5)`,  
  `W ∈ (8, 12, 16)`,  
  `seed ∈ {anchor seeds ± seed_span}` (default `seed_span=1` → 18 distinct seeds).
- **`--tiny`:** runs **only** the six anchor rows (CI smoke; no cross-family/size sweep).
- Artifacts under `reports/RUNS/<timestamp>_s1_v3_ring_failure_diagnostic/`:
  - `config.json`, `metrics.json`, `data.npz`, `summary.md`, `figures/.placeholder`

## Per-row observables

For each grid cell the script records (via `compare_localization_gate_v3` and reference observations at `low_energy_count=8`):

- `localization_gate_v3_classification`, `pass_rate_across_windows`, `window_sensitivity_score`
- `window_robust_localization_passed`, `unstable_window_cases`
- `localization_gate_v2_passed` / `fixed_window_localization_gate_passed` (v2 fixed-window rule)
- `kernel_only_localization_gate_passed`, `kernel_only_result`
- `v2_vs_v3_disagreement`
- `min_abs_eigenvalue_clean` / `min_abs_eigenvalue_disordered`, `kernel_count_clean` / `kernel_count_disordered`
- Low-energy / fixed-window IPR scalars and `ipr_delta_by_window` / `pass_by_window` (IPR profile across the v3 window sweep)

## Interpretation rubric (heuristic labels in `metrics.json`)

| Pattern | Suggested classification |
| --- | --- |
| Non-robust v3 mostly vanishes when `s1_size` grows; concentrated at 8 | Small `s1_size` ring artifact candidate |
| Non-robust v3 only (or overwhelmingly) at `alpha=0` | `alpha=0` boundary/twist regime artifact candidate |
| Non-robust v3 on `ring` but not on `spectral_circle` / `wilson_ring` at matched parameters | Ring discretization artifact candidate |
| Non-robust v3 flips across `seed±span` at fixed `(family,q,s1,alpha,W)` | Seed-specific instability candidate |
| Non-robust v3 across families and larger `s1_size` | Genuine unresolved v3 strong-disorder limitation candidate |

The script emits a compact `interpretation` block (`diagnostic_label`, `tags`, `reasons`) — **not** a theorem, only a structured reading aid.

## Regression

Automated smoke: `tests/test_s1_v3_ring_failure_diagnostic.py` (fixed timestamp `20990101-000031`, `--tiny`). After adding this pipeline, run `pytest -q` from the repository root.

## Latest completed full sweep (`--seed-span 0`)

```text
Command: python scripts/s1_v3_ring_failure_diagnostic.py --seed-span 0
Run directory: reports/RUNS/20260514-085316_s1_v3_ring_failure_diagnostic
Grid rows: 3240 (sweep only; anchor_exact block empty in this mode)
diagnostic_label: candidate_ring_alpha0_regime_artifact
```

Heuristic read (see `summary.md` / `metrics.json` → `interpretation`):

- **Failures are ring-only** (`failure_families: ["ring"]`).
- **All failures sit at `alpha=0.0`** (`failure_alpha_values: [0.0]`).
- **Not only `s1_size=8`:** sweep shows non-robust v3 cells up to **`s1_size=32`** (`failure_s1_sizes` includes 8, 16, 24, 32), so this is **not** classified as the narrow `candidate_ring_alpha0_small_s1_artifact` bucket by the script rubric.
- **Seed neighborhoods are mixed** at all six documented anchor tuples (`unstable_anchor_neighborhoods: 6`, tag `seed_neighborhood_mixed`).

Sweep failure counts (`failure_breakdown` in `metrics.json`): `sweep_failure_count=15` with breakdowns

- by family: `ring=15`
- by alpha: `0.0=15`
- by `s1_size`: `8→11`, `16→2`, `24→1`, `32→1`
- by `W`: `8.0→12`, `12.0→2`, `16.0→1`
- by seed: see `summary.md` (`by_seed` block)

Repository `pytest -q` after this diagnostic (2026-05-14): **132 passed** (one more test than the earlier **131** snapshot in `reports/VALIDATION_STATUS.md`; sync that file if you want a single authoritative count).
