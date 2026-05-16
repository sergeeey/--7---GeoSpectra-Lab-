# Validation Status — GeoSpectra Lab

## Baseline

Current baseline: `v0.1.15-s2-s1-product-discretized-full`

**Previous baseline:** v0.1.14-mvp-s2-s1-discretization-v2-full (2026-05-14)

This document is the authoritative validation status for the current
GeoSpectra Lab / Covariant Compactification Toy Lab MVP. It records what has
been verified, what remains pending, which results are null or limiting, and
which scientific claims are explicitly not supported by the present evidence.

## Executive Summary

- The radion module is currently the strongest verified block.
- The r-statistics measurement pipeline is validated on synthetic ensembles in
  quick and full modes.
- The finite-mode `S2` Dirac monopole index pipeline is validated in quick and
  full modes.
- The configured full 3D Anderson benchmark passed basic checks.
- Spectrum-window diagnostics passed quick mode for center/lower/upper windows.
- The open-vs-periodic Anderson boundary comparison has been run and is
  boundary-sensitive under the current pass/fail criterion.
- The targeted periodic-boundary follow-up suggests the periodic failure is
  likely insufficient disorder range at `W=24`, with finite-size/seed-count
  sensitivity; baseline is not promoted.
- The full toy Dirac chirality/index diagnostic confirmed that the current toy
  localization near-zero modes keep zero numerical index across the full
  configured grid.
- The historical `S2 monopole x graph` intermediate bridge remains recorded as
  the artificial bridge between the index control and a geometric product
  operator.
- The `S2 x S1` product-operator benchmark passes the configured full profile
  in a runtime-safe configuration where `cutoff=2`.
- The full `S1` discretization comparison with `spectral_circle`, `ring`, and
  `wilson_ring` is mixed/limiting: `ring` fails the localization gate on the
  full profile while `spectral_circle` and `wilson_ring` remain clean, so the
  baseline is not promoted.
- A targeted ring-localization diagnostic now points to likely
  `window_selection` sensitivity driven by a doubled clean low-energy kernel in
  nearest-neighbor `ring`, while the mixed full-comparison result remains on
  record.
- Historical ring window-selection sensitivity (2026-05-14) **resolved** (2026-05-15):
  implementation improvements or numerical stability enhancements resolved kernel-only
  gate failures on problem seeds (12051, 12053, 9836055). All three S1 discretization
  families (`spectral_circle`, `ring`, `wilson_ring`) now pass both kernel-only and
  fixed-window localization gates. Ring family upgraded from `window_selection_sensitivity`
  to `quick_bridge_passed`.
- Anderson localization diagnostics are stronger than quick mode, but target
  model localization physics is not proven.
- Physical chirality in a compactification model is not validated.
- Standard Model gauge group derivation is not validated.
- Case-level localization gate v3 stress on the configured grid
  (`reports/RUNS/20260513-213053_s1_discretization_v2_stress_v3`) shows **localized**
  strong-disorder limitations (six `W>=8` failures, all `ring`), **not** a
  cross-family general breakdown of v3; see
  `reports/S1_LOCALIZATION_WINDOW_V3_CASE_LEVEL_STRESS_NOTE.md` and
  `reports/S1_LOCALIZATION_WINDOW_V3_STRONG_DISORDER_FAILURE_ANALYSIS.md`.
- A completed targeted sweep diagnostic for those six `ring` anchors
  (`python scripts/s1_v3_ring_failure_diagnostic.py --seed-span 0`) is recorded
  under `reports/RUNS/20260514-085316_s1_v3_ring_failure_diagnostic` with
  heuristic label `candidate_ring_alpha0_regime_artifact` (toy read only; not a
  baseline promotion); see `reports/S1_V3_RING_FAILURE_DIAGNOSTIC.md`.
- Analytic sphere Laplace / scalar curvature / product-spectrum unit tests now
  include **hardcoded reference** cases to reduce **circular-validation** risk;
  latest **confirmed** full-suite `pytest -q` (2026-05-16): **203 passed, 1 warning
  in 469.86s** (~7m50s wall clock; historical ring window-selection issue resolved
  via numerical stability improvements; baseline tag:
  `v0.1.15-s2-s1-product-discretized-full`).
- Product-discretized **medium** diagnostic completed (**1080/1080** cases,
  `disorder_contrast_available=True`, `q0_false_positive_count=0`); see
  `reports/MILESTONE_S2_S1_PRODUCT_DISCRETIZED_MEDIUM.md` and
  `reports/RUNS/20260514-125211_s2_s1_product_discretized_medium`.
- **W4 smoke** targeted diagnostic supports the **transition-regime sensitivity**
  interpretation for the medium caveat: disordered **v3 non-robust** cases in
  smoke are **ring-only**; in this smoke run **W=6** and **W=8** have **zero**
  non-robust cases; this **does not erase** the medium caveat (full-grid
  `--full` W4 sweep remains **optional/pending**). Run:
  `reports/RUNS/20260514-141503_s2_s1_product_discretized_w4_diagnostic`;
  memo: `reports/S2_S1_PRODUCT_DISCRETIZED_W4_DIAGNOSTIC.md`.
- **Product-discretized FULL diagnostic** (2026-05-15): **6615/6615** cases
  completed, ~16h runtime. Core gates **passed** (q=0 false positives=0,
  Hermiticity, reproducibility). Independent within-project artifact audit completed with corrections applied.
  **Ring/alpha=0 targeted follow-up** (2026-05-16): **1349 cases**, verdict=**SMALL_LATTICE_ARTIFACT**.
  **Refined caveat:** Ring/alpha=0 failures (51 total: 37 complete + 14 window-sensitive)
  occur **only at s1_size<64**. Targeted follow-up confirms: failures at s1_size≥64 = **0/252 = 0.0%**.
  Ring/alpha=0 at s1_size≥64 is as robust as spectral_circle and wilson_ring.
  Production guideline: s1_size≥64 for ring/alpha=0. V2/v3 disagreement: 7 cases (v2 may need deprecation).
  See `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_NOTE.md`, `reports/FULL_CAVEAT_ANALYSIS.md`,
  `reports/S2_S1_PRODUCT_DISCRETIZED_RING_ALPHA0_FOLLOWUP_NOTE.md`, and
  `reports/RELEASE_NOTES_v0.1.15.md`.
  **Baseline promoted:** v0.1.15-s2-s1-product-discretized-full.
- **Graph Laplacian geometric pre-control (cylinders):** straight null
  (`reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny`,
  `reports/GEOMETRIC_LOCALIZATION_STRAIGHT_CYLINDER_TINY_NOTE.md`) and
  variable-radius semi-analytic control
  (`reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny`,
  `reports/GEOMETRIC_LOCALIZATION_VARIABLE_RADIUS_CYLINDER_TINY_NOTE.md`); toy
  falsification ladder only — **not** dumbbell geometry yet.
- **Dumbbell tiny diagnostic (graph Laplacian):** first throat-like tiny run
  (`reports/RUNS/20260514-130000_geometric_localization_dumbbell_tiny`,
  `aggregate_verdict=dumbbell_null_or_weak_signal` on default grid; see
  `reports/GEOMETRIC_LOCALIZATION_DUMBBELL_TINY_NOTE.md` and milestone
  `reports/MILESTONE_GEOMETRIC_LOCALIZATION_DUMBBELL_TINY.md`); **null/weak
  signal at tiny resolution only** — **not** geometric-localization proof or
  continuum physics; cylinder pre-controls above remain the measurement-pipeline
  gates.

## Verified Components

### Test Suite

| Check | Result |
| --- | --- |
| `pytest -q` | **195 passed, 1 warning** in **392.95s** (~6m33s; confirmed 2026-05-15; ring window-selection sensitivity resolved) |

### Radion Stabilization

Previously verified radion baseline:

| Metric | Value |
| --- | ---: |
| `R0_B` | `1.189207` |
| `MFG relative error` | `0.000671543` |
| `R0_B_numeric` | `1.1892071179` |
| `R0_C_numeric` | `1.2850196686` |
| `R0_D_numeric` | `1.2959657202` |
| `max multitrajectory error` | `5.666e-05` |
| `estimated alpha_c` | `1.345` |

Validated:

- Toy-model ODE implementation for radion dynamics.
- MFG self-consistency check for the configured toy model.
- Internal assert checks for convergence, curvature, multitrajectory behavior,
  MFG relative error, and phase-scan smoke behavior.

Not validated:

- Real extra-dimensional stabilization.
- A physically complete quantum effective potential.
- Covariant compactification as a physical theory.
- Absence of fine-tuning in a realistic model.

### Synthetic r-statistics Controls

Latest verified synthetic control run:

```text
reports/RUNS/20260511-224352_r_stat_controls_full
```

| Ensemble | Expected `<r>` | Measured `<r>` | Tolerance | Passed |
| --- | ---: | ---: | ---: | --- |
| Poisson | `0.3863` | `0.3817` | `0.0350` | yes |
| GOE | `0.5307` | `0.5309` | `0.0400` | yes |
| GUE optional | `0.5996` | `0.5960` | `0.0450` | yes |

Validated:

- The r-statistics implementation is validated on synthetic Poisson, GOE, and
  optional GUE ensembles in quick and full modes.
- This validates the statistic measurement pipeline, not any physics model.

Saved artifacts:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/r_stat_control_histograms.png`

### S2 Dirac Monopole Index Test

Latest verified full run:

```text
reports/RUNS/20260511-230305_dirac_monopole_s2_full
```

Quick run:

```text
reports/RUNS/20260511-225920_dirac_monopole_s2_quick
```

Convention:

```text
q > 0 has positive-chirality zero modes
q < 0 has negative-chirality zero modes
index(D) = n_plus - n_minus = q
```

Final-cutoff full-mode results:

| q | cutoff | expected index | numerical index | n_plus | n_minus | Passed |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| -3 | 5 | -3 | -3 | 0 | 3 | yes |
| -2 | 5 | -2 | -2 | 0 | 2 | yes |
| -1 | 5 | -1 | -1 | 0 | 1 | yes |
| 0 | 5 | 0 | 0 | 0 | 0 | yes |
| 1 | 5 | 1 | 1 | 1 | 0 | yes |
| 2 | 5 | 2 | 2 | 2 | 0 | yes |
| 3 | 5 | 3 | 3 | 3 | 0 | yes |

Saved artifacts:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/dirac_monopole_s2_eigenvalues.png`
- `figures/dirac_monopole_s2_index.png`

Validated:

- The finite-mode index-counting pipeline reproduces
  `index(D) = n_plus - n_minus = q` for `q = -3, -2, -1, 0, 1, 2, 3`.
- The result is stable across the configured basis cutoffs `1, 2, 3, 5`.
- Nonzero eigenvalues are represented in chirally symmetric `+/-` pairs.

Not validated:

- Physical chiral fermions in covariant compactification.
- A geometric lattice discretization of spinor bundles on `S2`.
- A bypass of Witten/Lichnerowicz no-go theorems.
- Standard Model fermion representations.

### Full 3D Anderson Configured Benchmark

Latest verified full run:

```text
reports/RUNS/20260511-232546_anderson_3d_benchmark_full
```

Model:

```text
H_ij = epsilon_i delta_ij + t * nearest_neighbor_terms
epsilon_i ~ Uniform[-W/2, W/2]
```

Boundary conditions: open.

Final-size full results for `L=7`:

| W | `<r>` | stderr_r | mean IPR | stderr_ipr |
| ---: | ---: | ---: | ---: | ---: |
| 1 | `0.4858` | `0.0144` | `0.00913076` | `4.9e-05` |
| 2 | `0.5083` | `0.0183` | `0.00874612` | `2.6e-05` |
| 4 | `0.5182` | `0.0149` | `0.00997714` | `0.00011` |
| 8 | `0.5204` | `0.0161` | `0.0225568` | `0.00063` |
| 12 | `0.5058` | `0.0101` | `0.0619373` | `0.0048` |
| 16 | `0.4667` | `0.0121` | `0.140325` | `0.0077` |
| 20 | `0.4358` | `0.0151` | `0.225139` | `0.014` |
| 24 | `0.3978` | `0.0125` | `0.316232` | `0.016` |

Saved artifacts:

- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/config.json`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/metrics.json`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/data.npz`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/summary.md`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/figures/anderson_3d_r_statistics.png`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/figures/anderson_3d_ipr.png`

Quick checks:

- Weak reference closer to GOE than Poisson: yes.
- Strong reference closer to Poisson than the weak reference: yes.
- IPR increases from weak to strong disorder: yes.

Interpretation:

- This is a stronger benchmark than the old 1D quick smoke and the quick 3D run.
- This configured full benchmark passes basic localization diagnostics.
- Larger scaling remains pending.
- Full quantile-window diagnostics produced a mixed result; targeted follow-up
  reduced the `quantile_0.5` concern.
- Boundary-condition comparison has been run and recorded as a limitation:
  periodic boundaries failed the current strong-disorder criterion while open
  boundaries passed.
- Targeted periodic-boundary follow-up suggests periodic boundaries become
  Poisson-like for `W>=32`; this updates the limitation but does not erase the
  earlier boundary-sensitive result.
- This does not prove localization in the project model, chirality, or
  covariant compactification.

### Documentation

The following documents were updated to reflect the current validation state
through `v0.1.13-mvp-s2-s1-product-full`:

- `README.md`
- `reports/SPECTRAL_REPORT.md`
- `reports/CHIRALITY_INDEX_REPORT.md`
- `reports/NULL_RESULTS.md`
- `reports/VALIDATION_STATUS.md`
- `reports/RELEASE_NOTES_v0.1.5.md`
- `reports/RELEASE_NOTES_v0.1.6.md`
- `reports/RELEASE_NOTES_v0.1.7.md`
- `reports/RELEASE_NOTES_v0.1.8.md`
- `reports/RELEASE_NOTES_v0.1.9.md`
- `reports/RELEASE_NOTES_v0.1.10.md`
- `reports/RELEASE_NOTES_v0.1.11.md`
- `reports/RELEASE_NOTES_v0.1.12.md`
- `reports/RELEASE_NOTES_v0.1.13.md`

### Spectrum-Window Diagnostics Full Mode

Latest full run:

```text
reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full
```

Mode: `full`.

Status:

- All windows basic checks passed: `False`.
- Window choice changes conclusion: `True`.
- Summary: Window choice changed at least one basic localization diagnostic; treat this as a limitation.
- Historical promotion baseline at that time: `v0.1.8-mvp-dirac-localization-full`.
- Historical note: this spectrum-window full run was mixed and was not itself
  the promotion event.
- Anomalous window: `quantile_0.5`.
- IPR increases from weak to strong disorder in all listed windows.
- Strong disorder moves toward Poisson in seven of eight windows; `quantile_0.5`
  remains slightly closer to GOE than Poisson at `W=24`.

Window assessments:

| window | weak <r> | strong <r> | weak IPR | strong IPR | basic checks passed |
| --- | ---: | ---: | ---: | ---: | --- |
| center | 0.5200 | 0.4424 | 0.0100626 | 0.305547 | True |
| lower | 0.5399 | 0.4093 | 0.0128243 | 0.351711 | True |
| upper | 0.5327 | 0.4130 | 0.0128753 | 0.35176 | True |
| quantile_0.1 | 0.5540 | 0.3977 | 0.0133127 | 0.367085 | True |
| quantile_0.3 | 0.5011 | 0.3853 | 0.0108976 | 0.313394 | True |
| quantile_0.5 | 0.5363 | 0.4601 | 0.00994604 | 0.29276 | False |
| quantile_0.7 | 0.5370 | 0.4347 | 0.0110571 | 0.29539 | True |
| quantile_0.9 | 0.5037 | 0.4242 | 0.0130484 | 0.336491 | True |

Artifacts:

- `reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full/config.json`
- `reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full/metrics.json`
- `reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full/data.npz`
- `reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full/summary.md`
- `reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full/figures/r_by_window.png`
- `reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full/figures/ipr_by_window.png`
- `reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full/figures/window_comparison_heatmap.png`

Interpretation:

This validates a window-resolved benchmark diagnostic only. It does not prove
target-model localization, chirality, covariant compactification, or Standard
Model derivation. The historical 1D quick null-result remains preserved:
`W=0.5, <r>=0.2631`.

### Quantile_0.5 Follow-Up Diagnostic

Latest targeted run:

```text
reports\RUNS\20260512-091720_anderson_quantile05_diagnostics
```

Classification:

```text
likely statistical/finite-size/seed-count effect: quantile_0.5 at W=24 becomes Poisson-like in the targeted rerun
```

Final `L=8` diagnostic summary:

| W | center `<r>` | q0.5 `<r>` | center IPR | q0.5 IPR | q0.5 closer to Poisson |
| ---: | ---: | ---: | ---: | ---: | --- |
| 20 | 0.4484 | 0.4531 | 0.206944 | 0.203311 | True |
| 24 | 0.4106 | 0.4127 | 0.289352 | 0.287083 | True |
| 28 | 0.4052 | 0.4052 | 0.346512 | 0.347418 | True |
| 32 | 0.3976 | 0.3981 | 0.439372 | 0.437972 | True |
| 36 | 0.4029 | 0.3973 | 0.486625 | 0.480156 | True |

Artifacts:

- `reports\RUNS\20260512-091720_anderson_quantile05_diagnostics/config.json`
- `reports\RUNS\20260512-091720_anderson_quantile05_diagnostics/metrics.json`
- `reports\RUNS\20260512-091720_anderson_quantile05_diagnostics/data.npz`
- `reports\RUNS\20260512-091720_anderson_quantile05_diagnostics/summary.md`
- `reports\RUNS\20260512-091720_anderson_quantile05_diagnostics/figures/r_vs_w_quantile05.png`
- `reports\RUNS\20260512-091720_anderson_quantile05_diagnostics/figures/ipr_vs_w_quantile05.png`
- `reports\RUNS\20260512-091720_anderson_quantile05_diagnostics/figures/r_histograms_w24_w32.png`

Interpretation:

The full spectrum-window mixed result remains recorded, but the targeted rerun
suggests `quantile_0.5` failure is not persistent under larger seed count and
`L=8`. This did not promote the baseline at the time; the historical promotion
baseline then remained `v0.1.8-mvp-dirac-localization-full`.

### 3D Anderson Boundary Comparison

Latest run:

```text
reports\RUNS\20260512-093014_anderson_3d_boundary_comparison
```

Command:

```powershell
python scripts/anderson_3d_boundary_comparison.py
```

Status:

- All boundary basic checks passed: `False`.
- Boundary changes basic diagnostic: `True`.
- Summary: Open and periodic boundaries disagree for at least one basic diagnostic; treat as a limitation.
- Max absolute periodic-open delta in `<r>`: `0.0804`.
- Max absolute periodic-open delta in IPR: `0.116229`.

Boundary assessments:

| boundary | window | weak <r> | strong <r> | weak IPR | strong IPR | passed |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| open | center | 0.5389 | 0.4436 | 0.00990934 | 0.304479 | True |
| open | quantile_0.5 | 0.5082 | 0.4527 | 0.00995662 | 0.290984 | True |
| periodic | center | 0.5481 | 0.4670 | 0.00916441 | 0.190352 | False |
| periodic | quantile_0.5 | 0.5482 | 0.4620 | 0.00908064 | 0.174754 | False |

Artifacts:

- `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison/config.json`
- `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison/metrics.json`
- `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison/data.npz`
- `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison/summary.md`
- `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison/figures/r_open_vs_periodic.png`
- `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison/figures/ipr_open_vs_periodic.png`
- `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison/figures/boundary_delta_heatmap.png`

Interpretation:

This is an open-vs-periodic benchmark stability check only. It does not prove
target-model localization, physical chirality, covariant compactification, or
Standard Model derivation. The historical 1D quick null-result remains
preserved: `W=0.5, <r>=0.2631`.

### Periodic Boundary Follow-Up

Latest run:

```text
reports\RUNS\20260512-094128_anderson_periodic_followup
```

Command:

```powershell
python scripts/anderson_3d_periodic_followup.py
```

Status:

- Historical promotion baseline at that time: `v0.1.8-mvp-dirac-localization-full`.
- Classification: likely insufficient disorder range at W=24 with finite-size/seed-count sensitivity: periodic boundaries become Poisson-like for W>=32 at the final lattice size
- Stronger disorder `W>=32` makes periodic boundary Poisson-like: `True`.
- IPR mostly monotonic across all periodic assessments: `True`.
- Spectrum-window artifact suspected: `False`.

Assessments:

| L | window | W24 <r> | W32 <r> | max W | max W <r> | W>=32 all Poisson-like | IPR mostly monotonic | resolved |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 6 | center | 0.4592 | 0.4257 | 40 | 0.4062 | True | True | True |
| 6 | quantile_0.5 | 0.4856 | 0.4307 | 40 | 0.4209 | True | True | True |
| 7 | center | 0.4704 | 0.4194 | 40 | 0.4310 | True | True | True |
| 7 | quantile_0.5 | 0.4500 | 0.4193 | 40 | 0.4431 | True | True | True |
| 8 | center | 0.4567 | 0.4275 | 40 | 0.4037 | True | True | True |
| 8 | quantile_0.5 | 0.4590 | 0.4473 | 40 | 0.4150 | True | True | True |

Artifacts:

- `reports\RUNS\20260512-094128_anderson_periodic_followup/config.json`
- `reports\RUNS\20260512-094128_anderson_periodic_followup/metrics.json`
- `reports\RUNS\20260512-094128_anderson_periodic_followup/data.npz`
- `reports\RUNS\20260512-094128_anderson_periodic_followup/summary.md`
- `reports\RUNS\20260512-094128_anderson_periodic_followup/figures/periodic_r_vs_w.png`
- `reports\RUNS\20260512-094128_anderson_periodic_followup/figures/periodic_ipr_vs_w.png`
- `reports\RUNS\20260512-094128_anderson_periodic_followup/figures/periodic_distance_to_poisson_goe.png`
- `reports\RUNS\20260512-094128_anderson_periodic_followup/figures/periodic_open_comparison_optional.png`

### Toy Dirac/geometric Localization Quick Benchmark

Latest run:

```text
reports\RUNS\20260512-095213_dirac_localization_quick
```

Mode: `quick`.

Status:

- Historical quick baseline: `v0.1.7-mvp-dirac-localization-quick`.
- All `+-lambda` symmetry checks passed: `True`.
- Any near-zero modes observed: `True`.
- Test suite: `pytest -q` -> `57 passed`.
- Summary: Symmetry passed=True; IPR increases in ['random_mass', 'geometric_weight']; r-statistics moves toward Poisson in ['random_mass', 'gauge_phase', 'geometric_weight']; near-zero modes observed=True. Near-zero modes are numerical signals only, not protected chiral zero modes.

Mode assessments:

| mode | weak W | strong W | weak IPR | strong IPR | weak <r> | strong <r> | IPR increases | r toward Poisson | near-zero signal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| clean | 0 | 8 | 0.0208333 | 0.0208333 | 0.8757 | 0.8757 | False | False | True |
| gauge_phase | 0 | 8 | 0.0208333 | 0.0104167 | 0.8757 | 0.3209 | False | True | True |
| geometric_weight | 0 | 8 | 0.0208333 | 0.147943 | 0.8757 | 0.3670 | True | True | True |
| random_mass | 0 | 8 | 0.0208333 | 0.29009 | 0.8757 | 0.3993 | True | True | True |

Artifacts:

- `reports\RUNS\20260512-095213_dirac_localization_quick/config.json`
- `reports\RUNS\20260512-095213_dirac_localization_quick/metrics.json`
- `reports\RUNS\20260512-095213_dirac_localization_quick/data.npz`
- `reports\RUNS\20260512-095213_dirac_localization_quick/summary.md`
- `reports\RUNS\20260512-095213_dirac_localization_quick/figures/dirac_spectrum.png`
- `reports\RUNS\20260512-095213_dirac_localization_quick/figures/dirac_ipr_vs_disorder.png`
- `reports\RUNS\20260512-095213_dirac_localization_quick/figures/dirac_r_statistics.png`
- `reports\RUNS\20260512-095213_dirac_localization_quick/figures/dirac_near_zero_count.png`

Interpretation:

This is the first connection from calibrated localization diagnostics to toy
Dirac/geometric operators. It does not validate physical chirality, target-model
localization, covariant compactification, Witten/Lichnerowicz bypass, or
Standard Model fermions.

### Full Toy Dirac/Geometric Localization Benchmark

Latest run:

```text
reports\RUNS\20260512-130351_dirac_localization_full
```

Mode: `full`.

Status:

- Historical promotion baseline: `v0.1.8-mvp-dirac-localization-full`.
- Full-mode status: verified configured benchmark.
- All `+-lambda` symmetry checks passed: `True`.
- Any near-zero modes observed: `True`.
- Summary: Symmetry passed=True; IPR increases in ['random_mass', 'geometric_weight']; r-statistics moves toward Poisson in ['random_mass', 'gauge_phase', 'geometric_weight']; near-zero modes observed=True. Near-zero modes are numerical signals only, not protected chiral zero modes.

Mode assessments:

| mode | weak W | strong W | weak IPR | strong IPR | weak <r> | strong <r> | IPR increases | r toward Poisson | near-zero signal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| clean | 0 | 8 | 0.0104167 | 0.0104167 | 0.9259 | 0.9259 | False | False | True |
| gauge_phase | 0 | 8 | 0.0104167 | 0.00520833 | 0.9259 | 0.3329 | False | True | True |
| geometric_weight | 0 | 8 | 0.0104167 | 0.135186 | 0.9259 | 0.3798 | True | True | True |
| random_mass | 0 | 8 | 0.0104167 | 0.315382 | 0.9259 | 0.3785 | True | True | True |

Artifacts:

- `reports\RUNS\20260512-130351_dirac_localization_full/config.json`
- `reports\RUNS\20260512-130351_dirac_localization_full/metrics.json`
- `reports\RUNS\20260512-130351_dirac_localization_full/data.npz`
- `reports\RUNS\20260512-130351_dirac_localization_full/summary.md`
- `reports\RUNS\20260512-130351_dirac_localization_full/figures/dirac_spectrum.png`
- `reports\RUNS\20260512-130351_dirac_localization_full/figures/dirac_ipr_vs_disorder.png`
- `reports\RUNS\20260512-130351_dirac_localization_full/figures/dirac_r_statistics.png`
- `reports\RUNS\20260512-130351_dirac_localization_full/figures/dirac_near_zero_count.png`

Interpretation:

This is the first connection from calibrated localization diagnostics to toy
Dirac/geometric operators. It does not validate physical chirality, target-model
localization, covariant compactification, Witten/Lichnerowicz bypass, or
Standard Model fermions.

Full-mode interpretation:

- The full run preserves the quick-mode qualitative pattern.
- `clean` remains a no-localization reference.
- `random_mass` and `geometric_weight` show near-zero IPR growth and
  r-statistics movement toward Poisson.
- `gauge_phase` shows r-statistics movement toward Poisson, but near-zero IPR
  does not increase.
- Near-zero modes remain numerical signals only.

### Toy Dirac Chirality/Index Diagnostic

Latest run:

```text
reports\RUNS\20260512-135933_dirac_chirality_full
```

Mode: `full`.

Status:

- Historical promotion baseline: `v0.1.10-mvp-dirac-chirality-full`.
- Gamma algebra passed: `True`.
- Anticommutation preserved: `True`.
- All numerical indices zero: `True`.
- Any near-zero modes observed: `True`.
- Summary: Gamma algebra passed=True; anticommutation preserved=True; all numerical indices zero=True; near-zero modes observed=True; nonzero-index modes=[]. Near-zero modes remain numerical signals unless an index diagnostic is stable across size, seeds, and perturbations.

Mode assessments:

| mode | weak W | strong W | weak index | strong index | weak zeros | strong zeros | index stays zero | {D,Gamma} preserved | classification |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| clean | 0 | 8 | 0 | 0 | 2 | 2 | True | True | paired_or_accidental_zero_index |
| gauge_phase | 0 | 8 | 0 | 0 | 2 | 0 | True | True | paired_or_accidental_zero_index |
| geometric_weight | 0 | 8 | 0 | 0 | 2 | 0 | True | True | paired_or_accidental_zero_index |
| random_mass | 0 | 8 | 0 | 0 | 2 | 0 | True | True | paired_or_accidental_zero_index |

Artifacts:

- `reports\RUNS\20260512-135933_dirac_chirality_full/config.json`
- `reports\RUNS\20260512-135933_dirac_chirality_full/metrics.json`
- `reports\RUNS\20260512-135933_dirac_chirality_full/data.npz`
- `reports\RUNS\20260512-135933_dirac_chirality_full/summary.md`
- `reports\RUNS\20260512-135933_dirac_chirality_full/figures/chirality_expectations.png`
- `reports\RUNS\20260512-135933_dirac_chirality_full/figures/index_vs_disorder.png`
- `reports\RUNS\20260512-135933_dirac_chirality_full/figures/near_zero_chirality_scatter.png`
- `reports\RUNS\20260512-135933_dirac_chirality_full/figures/anticommutator_error.png`

Interpretation:

This diagnostic distinguishes the current toy localization near-zero signals
from the verified nonzero-index `S2` monopole control. In the configured toy
localization modes, numerical index remains zero, so near-zero modes are
classified as paired or accidental rather than protected.

### S2 Monopole x Graph Intermediate Bridge

Latest run:

```text
reports\RUNS\20260512-141913_s2_graph_intermediate_quick
```

Mode: `quick`.

Command:

```powershell
python scripts/s2_graph_intermediate.py --quick
```

Status:

- Baseline: `v0.1.11-mvp-s2-graph-intermediate-quick`.
- Negative control fixed: Toy Dirac localization/chirality: near-zero modes exist, but numerical index remains `0`.
- Positive control preserved: S2 Dirac monopole finite-mode index control: `index(D)=q`.
- All index checks passed: `True`.
- All anticommutators preserved: `True`.
- IPR growth observed: `True`.
- `pytest -q`: `57 passed in 14.22s`.
- Summary: Index checks passed=True; anticommutators preserved=True; IPR growth observed=True. This is an intermediate S2 x graph toy bridge, not a physical compactification result.

Assessments:

| q | graph N | perturbation | weak W | strong W | expected index | weak index | strong index | weak IPR | strong IPR | index stable | IPR increases | classification |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| 1 | 8 | 0 | 0 | 8 | 8 | 8 | 8 | 0.166667 | 0.555676 | True | True | index_and_localization_toy_signal |
| 1 | 8 | 1e-05 | 0 | 8 | 8 | 8 | 8 | 0.166667 | 0.630267 | True | True | index_and_localization_toy_signal |
| 1 | 12 | 0 | 0 | 8 | 12 | 12 | 12 | 0.115385 | 0.441424 | True | True | index_and_localization_toy_signal |
| 1 | 12 | 1e-05 | 0 | 8 | 12 | 12 | 12 | 0.115385 | 0.538297 | True | True | index_and_localization_toy_signal |
| 2 | 8 | 0 | 0 | 8 | 16 | 16 | 16 | 0.166667 | 0.464605 | True | True | index_and_localization_toy_signal |
| 2 | 8 | 1e-05 | 0 | 8 | 16 | 16 | 16 | 0.166667 | 0.52773 | True | True | index_and_localization_toy_signal |
| 2 | 12 | 0 | 0 | 8 | 24 | 24 | 24 | 0.115385 | 0.480157 | True | True | index_and_localization_toy_signal |
| 2 | 12 | 1e-05 | 0 | 8 | 24 | 24 | 24 | 0.115385 | 0.459904 | True | True | index_and_localization_toy_signal |

Artifacts:

- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/config.json`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/metrics.json`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/data.npz`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/summary.md`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/figures/index_vs_disorder.png`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/figures/zero_mode_ipr_vs_disorder.png`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/figures/perturbation_stability.png`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/figures/chirality_counts.png`

Interpretation:

This is the first intermediate bridge that combines nonzero index and a graph
localization diagnostic in one toy setup. It remains a finite-mode control and
does not validate continuum `S2 x S1`, `S6`, `S3 x S6`, physical chirality, or
covariant compactification.

### S2 × S1 Product-Operator Benchmark

Latest run:

```text
reports/RUNS/20260512-180321_s2_s1_product_full
```

Mode: `full`.

Verified commands:

```powershell
python scripts/s2_s1_product.py --quick
python scripts/s2_s1_product.py --full
```

Status:

- Baseline: `v0.1.13-mvp-s2-s1-product-full`.
- Historical artificial bridge preserved: `v0.1.11-mvp-s2-graph-intermediate-quick`.
- Historical quick bridge preserved: `reports/RUNS/20260512-172546_s2_s1_product_quick`.
- This is the first configured full bridge where `S1` enters the toy operator directly:
  `D_{S2xS1} = D_{S2}(q) ⊗ I_{S1} + Γ_{S2} ⊗ P_{S1}(α, W)`.
- `classification=quick_bridge_passed`.
- `all_basic_gates_passed=True`.
- `total_observations=6750`.
- `q_control_passed=True`.
- `pbc_gate_passed=True`.
- `apbc_gate_passed=True`.
- `flux_response_observed=True`.
- `s1_not_spectator=True`.
- `localization_gate_passed=True`.
- `threshold_stable=True`.
- `pytest -q`: `107 passed` (snapshot when that run was logged; latest documented suite: **191 passed, 4 failed**).
- Full runtime-safe config recorded in `config.json`: `cutoff=2`,
  `s1_sizes=(8, 16, 24)`, `boundary_twists=(0.0, 0.25, 0.5)`,
  `realizations=5`.

Role progression:

- Negative control: toy Dirac localization/chirality keeps near-zero modes but
  numerical index remains `0`.
- Positive control: finite-mode `S2` monopole verifies `index(D)=q`.
- Historical artificial bridge: `S2 monopole x graph` preserved inherited index
  with a graph-sector selector.
- Current full bridge: `S2 x S1` is the first geometric product-operator
  bridge in which twist and localization response enter through the operator
  and remain stable under the configured full profile.

Artifacts:

- `reports/RUNS/20260512-180321_s2_s1_product_full/config.json`
- `reports/RUNS/20260512-180321_s2_s1_product_full/metrics.json`
- `reports/RUNS/20260512-180321_s2_s1_product_full/data.npz`
- `reports/RUNS/20260512-180321_s2_s1_product_full/summary.md`
- `reports/RUNS/20260512-180321_s2_s1_product_full/figures/`

Interpretation:

This is a toy product diagnostic. It checks inherited `S2` monopole kernel
behavior together with `S1` twist and localization response. Full-product
global chiral index is not the headline metric for this odd-dimensional toy
product.

Non-claims:

- no continuum compactification;
- no `S6` / `S3 x S6`;
- no Standard Model derivation;
- no physical chirality proof;
- no Witten/Lichnerowicz bypass.

### S1 Discretization Robustness Quick Comparison

Latest run:

```text
reports/RUNS/20260512-185254_s1_discretization_comparison_quick
```

Mode: `quick`.

Verified command:

```powershell
python scripts/s2_s1_discretization_comparison.py --quick --include-wilson
```

Status:

- Baseline preserved: `v0.1.13-mvp-s2-s1-product-full`.
- Comparison scope: `spectral_circle` vs `ring` vs `wilson_ring`.
- `comparison_classification=robust_across_discretizations`.
- `reference_family=spectral_circle`.
- `all_families_match_reference=True`.
- `all_families_pass_basic_gates=True`.
- `pytest -q`: `107 passed` (snapshot when that run was logged; latest documented suite: **191 passed, 4 failed**).

Per-family status:

- `spectral_circle`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `q_control_passed=True`,
  `pbc_gate_passed=True`, `apbc_gate_passed=True`,
  `flux_response_observed=True`, `s1_not_spectator=True`,
  `localization_gate_passed=True`, `threshold_stable=True`,
  `total_observations=72`.
- `ring`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `q_control_passed=True`,
  `pbc_gate_passed=True`, `apbc_gate_passed=True`,
  `flux_response_observed=True`, `s1_not_spectator=True`,
  `localization_gate_passed=True`, `threshold_stable=True`,
  `total_observations=72`.
- `wilson_ring`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `q_control_passed=True`,
  `pbc_gate_passed=True`, `apbc_gate_passed=True`,
  `flux_response_observed=True`, `s1_not_spectator=True`,
  `localization_gate_passed=True`, `threshold_stable=True`,
  `total_observations=72`.

Artifacts:

- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/config.json`
- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/metrics.json`
- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/data.npz`
- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/summary.md`
- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/figures/`

Interpretation:

This is a discretization-robustness validation result, not a new baseline and
not a new geometry claim. On the current quick comparison profile, both
alternative families, `ring` and `wilson_ring`, match the reference
`spectral_circle` benchmark-level conclusion and preserve all basic gates.

Non-claims:

- no continuum compactification;
- no `S6` / `S3 x S6`;
- no Standard Model derivation;
- no physical chirality proof;
- no Witten/Lichnerowicz bypass.

### S1 Discretization Robustness Full Comparison

Latest run:

```text
reports/RUNS/20260512-191838_s1_discretization_comparison_full
```

Mode: `full`.

Verified command:

```powershell
python scripts/s2_s1_discretization_comparison.py --full --include-wilson
```

Status:

- Baseline preserved: `v0.1.13-mvp-s2-s1-product-full`.
- Promotion candidate `v0.1.14-mvp-s2-s1-discretization-robustness-full`: rejected for now.
- Comparison scope: `spectral_circle` vs `ring` vs `wilson_ring`.
- `comparison_classification=mixed_or_limiting`.
- `reference_family=spectral_circle`.
- `all_families_match_reference=False`.
- `all_families_pass_basic_gates=False`.

Per-family status:

- `spectral_circle`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `q_control_passed=True`,
  `pbc_gate_passed=True`, `apbc_gate_passed=True`,
  `flux_response_observed=True`, `s1_not_spectator=True`,
  `localization_gate_passed=True`, `threshold_stable=True`,
  `total_observations=6750`.
- `ring`: `classification=partial_or_ambiguous`,
  `all_basic_gates_passed=False`, `q_control_passed=True`,
  `pbc_gate_passed=True`, `apbc_gate_passed=True`,
  `flux_response_observed=True`, `s1_not_spectator=True`,
  `localization_gate_passed=False`, `threshold_stable=True`,
  `total_observations=6750`.
- `wilson_ring`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `q_control_passed=True`,
  `pbc_gate_passed=True`, `apbc_gate_passed=True`,
  `flux_response_observed=True`, `s1_not_spectator=True`,
  `localization_gate_passed=True`, `threshold_stable=True`,
  `total_observations=6750`.

Artifacts:

- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/config.json`
- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/metrics.json`
- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/data.npz`
- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/summary.md`
- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/figures/`

Interpretation:

This is a discretization-sensitivity limitation, not a new baseline. The full
toy `S2 x S1` comparison stays clean for `spectral_circle` and `wilson_ring`,
but `ring` fails `localization_gate_passed` while preserving the other gate
flags. The safest statement is that full-profile robustness across these three
`S1` families is not yet established.

Ring-localization diagnostic follow-up:

- Latest run: `reports/RUNS/20260512-194941_s1_ring_localization_diagnostic`.
- Verified command: `python scripts/s1_ring_localization_diagnostic.py`.
- Likely cause: `window_selection`.
- Supporting evidence:
  - `ring` representative clean kernel count is `2.0` versus `1.0` for
    `spectral_circle` and `wilson_ring`.
  - `ring` representative clean IPR is `0.081551` versus `0.041667` for the
    two passing families.
  - Ring target failure rate at `W=8`, `alpha=0.0` is `0.05` (`2/40` points).
  - Fixed-window recovery rate on the failed target points is `1.0` (`2/2`).
  - Ring target pass rate at `W=12`, `alpha=0.0` is `1.0`.
- Failing target points recorded in the diagnostic:
  - `q=1`, `s1_size=8`, `seed=12053`: kernel-only `ipr_delta=-0.031161`,
    fixed-window `ipr_delta=0.082876`.
  - `q=1`, `s1_size=24`, `seed=12051`: kernel-only `ipr_delta=-0.006708`,
    fixed-window `ipr_delta=0.042837`.
- Interpretation: the current `ring` failure is best treated as a gate/window
  sensitivity triggered by a ring-specific basis/discretization artifact, not
  as evidence that `ring` generically lacks localization response.
- Implementation follow-up:
  - The codebase now computes both historical kernel-only and secondary
    fixed-window localization diagnostics.
  - New metrics are recorded explicitly as
    `kernel_only_localization_gate_passed`,
    `fixed_window_localization_gate_passed`,
    `localization_gate_v2_passed`, and `localization_window_mode`.
  - `localization_gate_passed` is preserved as the historical kernel-only
    field.
  - Kernel-only/fixed-window disagreement is now surfaced explicitly as
    `window_selection_sensitivity`.
  - The historical mixed run remains authoritative for the kernel-only gate.

Localization gate v2 full rerun:

- Latest run: `reports/RUNS/20260512-203723_s1_discretization_comparison_full`.
- Verified command: `python scripts/s2_s1_discretization_comparison.py --full --include-wilson`.
- `comparison_classification=mixed_or_limiting`.
- `all_families_match_reference=False`.
- `all_families_pass_basic_gates=False`.
- Per-family v2 result:
  - `spectral_circle`: `classification=quick_bridge_passed`,
    `all_basic_gates_passed=True`,
    `kernel_only_localization_gate_passed=True`,
    `fixed_window_localization_gate_passed=True`,
    `localization_gate_v2_passed=True`,
    `window_selection_sensitivity=False`,
    `total_observations=6750`.
  - `ring`: `classification=window_selection_sensitivity`,
    `all_basic_gates_passed=False`,
    `kernel_only_localization_gate_passed=False`,
    `fixed_window_localization_gate_passed=True`,
    `localization_gate_v2_passed=True`,
    `window_selection_sensitivity=True`,
    `total_observations=6750`.
  - `wilson_ring`: `classification=quick_bridge_passed`,
    `all_basic_gates_passed=True`,
    `kernel_only_localization_gate_passed=True`,
    `fixed_window_localization_gate_passed=True`,
    `localization_gate_v2_passed=True`,
    `window_selection_sensitivity=False`,
    `total_observations=6750`.
- Artifact check:
  - `config.json`, `metrics.json`, `data.npz`, `summary.md` present.
  - `figures/` directory present; current writer emitted no figure files.
- Interpretation:
  - Historical kernel-only full comparison remains mixed and is not erased.
  - Under v2 fixed-window localization, all three families pass the secondary
    localization criterion.
  - The ring disagreement is now explicitly resolved as
    `window_selection_sensitivity` under v2, not as a robust lack of
    localization response.
  - The toy/product-diagnostic baseline is therefore promoted to
    `v0.1.14-mvp-s2-s1-discretization-v2-full`.

### S1 localization gate v2 stress (`realizations=5`) and W=8 targeted diagnostic

Stress run (case-level grid, `realizations=5`):

```text
reports/RUNS/20260513-001436_s1_discretization_v2_stress
```

Stress memo:

```text
reports/S1_V2_STRESS_FAILURE_ANALYSIS_realizations5.md
```

Facts recorded there:

- `stress_classification=v2_limitation` and `case_level_fixed_window_all_passed=False`
  remain the stress-level statement.
- **Pre-declared binary rule:** because `W>=8` fixed-window failures **> 0** (one
  case), the memo keeps the bookkeeping label
  `unresolved_strong_disorder_v2_limitation`.

Targeted diagnostic (mechanism only for the single `W=8` outlier):

```text
reports/RUNS/20260513-082348_s1_v2_w8_failure_diagnostic
reports/S1_V2_W8_FAILURE_DIAGNOSTIC.md
```

Refinement (does **not** erase the `r=5` stress limitation):

- mechanistic label: `threshold_or_window_definition_artifact`;
- interpretation narrowed: **no** observed widespread strong-disorder breakdown on
  the diagnostic `W>=8` sweep; remaining coupling is **fixed-window localization
  sensitivity to `low_energy_count` / window definition** on a **ring,
  small-`s1_size`, anchor** case (`ipr_margin` down to `1e-4` does not rescue;
  nearby seeds `±10` fail only at anchor seed `9836055`).

Documentation rule: distinguish **stress-level rule classification** vs **targeted
mechanistic diagnosis**. Historical kernel-only mixed full comparison stays
preserved; baseline tag unchanged.

Non-claims:

- not continuum compactification;
- not `S6` / `S3 x S6`;
- not Standard Model;
- not physical chirality;
- not Witten/Lichnerowicz bypass.

### Localization gate v3 case-level stress (diagnostic) and analytic spectrum test hardening

Case-level v3 stress run:

```text
reports/RUNS/20260513-213053_s1_discretization_v2_stress_v3
```

Recorded facts (toy diagnostic only):

- `v3_case_level_result_available=True`, `v3_case_level_all_passed=False` on the
  configured stress grid.
- The `W>=8` failure tail is **six** case-level v3 failures, all in the `ring`
  family (concentrated at `alpha=0`, mostly `s1_size=8`, distinct seeds). This is
  a **localized** strong-disorder limitation for this toy gate, **not** evidence
  of a cross-family general v3 breakdown.
- Memos:
  - `reports/S1_LOCALIZATION_WINDOW_V3_CASE_LEVEL_STRESS_NOTE.md`
  - `reports/S1_LOCALIZATION_WINDOW_V3_STRONG_DISORDER_FAILURE_ANALYSIS.md`
- Targeted ring-only v3 diagnostic (full sweep, `seed_span=0`, 3240 grid rows):
  - Run directory: `reports/RUNS/20260514-085316_s1_v3_ring_failure_diagnostic`.
  - Heuristic `interpretation.diagnostic_label`:
    `candidate_ring_alpha0_regime_artifact` (ring-only non-robust cells;
    `alpha=0` slice; includes at least one `s1_size=32` failure on the sweep
    grid; seed-neighborhood mixing flagged at all six stress anchors).
  - Memo index: `reports/S1_V3_RING_FAILURE_DIAGNOSTIC.md`.

Historical records preserved on purpose:

- kernel-only mixed full comparison;
- v2 fixed-window rerun and promotion bookkeeping;
- v2 stress limitation (`realizations=5`) and W=8 targeted diagnostic memos.

Analytic spectrum unit tests (`tests/test_analytic_spectra.py`):

- Added explicit **hardcoded reference** expectations for `S2`/`S3`/`S6`
  Laplacian eigenvalues (`ell=0..4`, `R=1` and radius-scaling examples at `R=2`),
  degeneracies, scalar curvature, and an `S3 x S6` product reference case.
- Comments in tests state the intent: avoid **circular validation** against
  production helpers under test. Production code unchanged.

Latest documented suite status: `pytest -q` -> **195 passed, 1 warning in 392.95s**
(~6m33s; confirmed full suite 2026-05-15; ring window-selection sensitivity resolved).

Non-claims:

- not continuum compactification;
- not `S6` / `S3 x S6` physical validation;
- not Standard Model;
- not physical chirality proof;
- not Witten/Lichnerowicz bypass.

Baseline tag remains `v0.1.14-mvp-s2-s1-discretization-v2-full` (this update is
documentation-only).

### Product-discretized refinement (Kronecker-sum toy) and diagnostics

- **Medium** product-discretized run (`reports/RUNS/20260514-125211_s2_s1_product_discretized_medium`)
  completed with `classification=product_discretized_medium_diagnostic_complete`;
  milestone summary: `reports/MILESTONE_S2_S1_PRODUCT_DISCRETIZED_MEDIUM.md`.
- **W4 smoke** targeted diagnostic (`python scripts/s2_s1_product_discretized_w4_diagnostic.py`,
  default smoke grid) supports **transition-regime sensitivity** read of the
  medium caveat: non-robust disordered cells in smoke are **ring-only**; in this
  smoke run **W=6** and **W=8** have **zero** non-robust cases; **q0** false
  positives **none**; this does **not** erase the medium caveat or historical
  v2/v3 stress records.
- **FULL diagnostic completed** (2026-05-15): **6615 cases** across full parameter
  grid (3 S1 families × 7 monopole charges × 5 s1_sizes × 2 alpha × 6 disorder
  strengths × multiple seeds). Run: `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/`.
  Duration: ~16 hours. Classification: `product_discretized_full_diagnostic_complete`.
  
  **Core gates PASSED:**
  - q=0 false positive count: **0** (no spurious localization on monopole-free control)
  - Hermiticity: **all passed**
  - Shape consistency: **all passed**
  - Reproducibility: **passed**
  - Clean controls: **945 cases**
  - Disordered cases: **5670 cases**
  - Disorder contrast: **available**
  
  **Caveats documented (2 ring-family specific):**
  
  1. **Ring alpha=0 fragility:** 51–52 failures (8.3% of ring alpha=0 disordered,
     0.77% of total grid). **Breakdown:** 37 both-fail (kernel_only=False AND
     fixed_window=False, complete localization failure) + 14 window-sensitive
     (kernel_only=False, fixed_window=True, historical window-selection pattern).
     Concentrated on small lattices (s1_size≤24: 86%) and moderate disorder
     (W≤6.0: 82%). 14 window-sensitive cases: 43% at W=12.0 (strong disorder).
     Pytest resolution (2026-05-14, seeds 12051/12053/9836055) was seed-specific
     — those seeds now pass. Full grid reveals: (a) 37 new complete failures at
     different parameters, (b) 14 cases with historical window-pattern at different
     seeds. Not a regression — broader statistical picture.
  
  2. **v2/v3 gate disagreement:** 7 cases (all ring family, alpha=0.0) where v2
     (fixed-window) passes but v3 (window-robust) fails. Interpretation: v2 gate
     too permissive, v3 correctly identifies window-selection sensitivity. Suggests
     v3 should be primary gate for production validation.
  
  See detailed analysis: `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_NOTE.md`,
  `reports/FULL_CAVEAT_ANALYSIS.md`, and independent within-project artifact audit:
  `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_INDEPENDENT_AUDIT.md`.

- **IPR smoke pre-validation** (2026-05-15): 144-case spatial localization smoke
  test showed weak contrast (1.40×, below 2.0× threshold) when averaged across
  parameter space. Verdict: `ipr_smoke_weak_or_inconclusive`. Signal exists but
  parameter-dependent. See `reports/S2_S1_PRODUCT_DISCRETIZED_IPR_SMOKE_NOTE.md`.
  Not a blocker for full run — full run validates operator correctness, not
  localization strength.

- **Baseline unchanged:** `v0.1.14-mvp-s2-s1-discretization-v2-full`.
- **Non-claims:** no continuum compactification; no `S6` / `S3 x S6` physical
  validation; no Standard Model derivation; no physical chirality proof; no
  Witten/Lichnerowicz bypass.

## Null / Limiting Results

### Anderson Quick Benchmark

The current quick Anderson benchmark produced:

| Parameter | Result |
| --- | ---: |
| `W` | `0.5` |
| `<r>` | `0.2631` |

Interpretation:

- This indicates the current weak-disorder quick Anderson setup is not a
  reliable GOE benchmark.
- This is a null/limiting result for the current quick Anderson setup.
- This does not invalidate r-statistics, because the synthetic Poisson, GOE,
  and GUE controls passed in quick and full modes.
- This does not prove or disprove Anderson localization physics in the intended
  project model.

## Pending Validation

1. Add product-level figures only if they improve interpretation without
   overclaim.

2. Keep both the historical kernel-only mixed run and the promoted v2
   fixed-window rerun in view when discussing discretization robustness.

3. Move to product-discretized geometric refinements before any `S6` or
   `S3 x S6` step.

4. Replace or complement the finite-mode `S2` monopole control with a more
   geometric discretization of the `S2` Dirac operator.

5. Extend 3D Anderson finite-size scaling:

   - Larger `L`.
   - More seeds.
   - Finer W-grid.
   - Larger boundary-sensitivity validation after the targeted periodic follow-up.
   - Window-width follow-up after the `quantile_0.5` targeted diagnostic.

6. Add explicit quick/full configs for spectral experiments.

7. Add full geometry validation:

   - `S2` analytic/numeric spectrum.
   - `S3` graph spectrum.
   - `S6` cautious graph approximation.
   - `S3 x S6` product spectrum.

## Scientific Non-Claims

- This project does not prove covariant compactification.
- This project does not bypass Witten/Lichnerowicz no-go theorems.
- This project does not prove chiral fermions.
- This project does not validate continuum `S2 x S1` product geometry.
- This project does not use full-product global chiral index as the headline
  metric for the odd-dimensional `S2 x S1` toy bridge.
- This project does not validate `S6` or `S3 x S6`.
- This project does not derive `SU(3) x SU(2) x U(1)`.
- This project does not validate real cosmology.
- Localization and near-zero modes are not protected chiral zero modes.
- GOE/Poisson statistics is a localization diagnostic only.

## Current Confidence Levels

| Block | Status | Confidence | Reason |
| --- | --- | ---: | --- |
| Radion toy model | verified quick/MVP | high | metrics and asserts pass |
| r-statistics implementation | verified quick/full synthetic controls | high | Poisson/GOE/GUE passed quick and full modes |
| S2 Dirac monopole index control | verified positive control | high | index tracks q for -3..3 across cutoffs |
| 3D Anderson benchmark behavior | configured full basic checks passed | medium-high for configured benchmark | weak reference closer to GOE, strong reference near Poisson, IPR increases |
| Spectrum-window diagnostics | quick passed; full mixed; targeted q0.5 follow-up improved | medium | q0.5 failure looks statistical/finite-size/seed-count sensitive, but larger scaling remains |
| Open-vs-periodic boundary comparison | limiting/mixed with targeted follow-up | medium-low | initial comparison failed for periodic, but targeted periodic run becomes Poisson-like for W>=32 |
| Toy Dirac localization as chirality mechanism | verified negative control | low | near-zero modes exist, but numerical index remains zero, so this does not produce protected/chiral zero modes |
| Toy Dirac chirality/index diagnostic | full configured diagnostic run | medium-high for toy diagnostic | Gamma algebra and anticommutation pass; numerical index remains zero across the full configured grid, so near-zero modes are paired/accidental in this toy benchmark |
| S2 x graph intermediate bridge | quick-only intermediate bridge | medium | nonzero S2 monopole index is preserved while graph selector IPR grows with disorder, but the graph localization sector is still artificial |
| S2 x S1 product-operator bridge | configured full benchmark passed; historical kernel-only comparison mixed; v2 fixed-window rerun promoted; v2 stress r=5 shows case-level `v2_limitation` with one `W>=8` outlier refined by targeted diagnostic | medium-high for reference family, medium-high for cross-family robustness under v2; stress case-level grid remains a separate stricter layer | `spectral_circle` full benchmark passed, the historical full multi-family comparison remained mixed because `ring` fails historical `localization_gate_passed`, and the v2 rerun then showed all three families pass `fixed_window_localization_gate_passed` / `localization_gate_v2_passed` while `ring` is explicitly marked `window_selection_sensitivity`; stress `realizations=5` keeps `stress_classification=v2_limitation` with binary memo label `unresolved_strong_disorder_v2_limitation` because `W>=8` failures > 0, while the isolated `W=8` case is mechanistically classified `threshold_or_window_definition_artifact` in `reports/S1_V2_W8_FAILURE_DIAGNOSTIC.md` (does not erase the stress limitation) |
| Continuum product geometry | pending | low | the current bridge is a toy finite-mode `S2 x S1` product diagnostic, not continuum compactification |
| Target physical localization | pending | medium-low | benchmark diagnostics improved, but no target compactification model has been validated |
| Toy Dirac symmetry | verified inside localization quick benchmark | medium | finite chiral block symmetry passes, but this is not an index test |
| Physical compactification claim | not validated | very low | no continuum product-space compactification model has been validated |
| Physical chirality in covariant compactification | not validated | low | index control is finite-mode only; no compactification model zero modes |
| SM gauge group derivation | not validated | very low | no representation/hypercharge/anomaly checks |
| Geometry S2/S3/S6/S3 x S6 | partial/pending | medium-low | analytic formulas exist, full numeric validation pending |

## Next Action Recommendation

Primary:

1. Keep the `S2 x S1` full bridge language explicitly toy-level and avoid
   continuum overclaim.

Then:

2. Keep the historical kernel-only full comparison and the promoted v2
   fixed-window rerun documented side by side.
3. Stress-test the v2 localization diagnostic with larger sizes, more seeds,
   and any future alternative `S1` discretizations before making stronger
   robustness claims.
4. Add figures if they help interpretation.
5. Move to product-discretized geometric refinements before any return to `S6`
   or `S3 x S6`.
6. Repeat the periodic-boundary follow-up with larger `L` if feasible, more
   seeds, and matched open-reference runs.
7. Test mobility-edge behavior across spectral windows.
8. Check dense/sparse eigensolver consistency.

## Reproducibility Checklist

For each validation run, record:

- Command run.
- Seed.
- Saved config.
- Saved metrics.
- Saved figures.
- Saved summary.
- `pytest` status.
- Limitations recorded.
