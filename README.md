# GeoSpectra Lab / Covariant Compactification Toy Lab

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20252651.svg)](https://doi.org/10.5281/zenodo.20252651)

## Purpose

GeoSpectra Lab is a reproducible Python MVP for testing toy mechanisms related
to covariant compactification ideas. It is a scientific-computing workbench, not
a claim that covariant compactification has been proven.

The current MVP tests:

- Radion stabilization in explicitly defined toy potentials.
- Spectral localization diagnostics through Anderson-style benchmarks.
- Analytic spectra on simple compact spaces such as `S2`, `S3`, `S6`, and
  product spectra.
- Scientific logging of discoveries, null results, and unresolved caveats.

The project value is the reproducible filter: it should show where a toy
hypothesis survives, where it fails, and which unexpected signals need follow-up.

## What This Project Does NOT Prove

- It does not prove covariant compactification.
- It does not bypass Witten/Lichnerowicz no-go theorems.
- It does not prove chiral fermions.
- It does not prove protected chiral zero modes from near-zero modes.
- It does not derive the Standard Model gauge group `SU(3) x SU(2) x U(1)`.
- It does not validate real cosmology or real extra-dimensional stabilization.
- A future GOE -> Poisson signal, if observed, is a localization signal only.
  It is not evidence for chirality without an index calculation.

## Current Baseline: v0.1.15-s2-s1-product-discretized-full

**Previous baseline:** v0.1.14-mvp-s2-s1-discretization-v2-full (2026-05-14)

This baseline is the verified state after completing the full product-discretized
S² × S¹ diagnostic (6615 cases) and targeted ring/alpha=0 follow-up (1349 cases)
with refined caveat scope. The control ladder is now fixed as
follows: toy Dirac localization/chirality remains the negative control with
zero numerical index, the finite-mode `S2` monopole remains the positive
control with nonzero index, `S2 monopole x graph` remains the historical
artificial intermediate bridge, and `S2 x S1` is now the first geometric
product-operator bridge that passed the configured full profile.

| Area | Verified state |
| --- | --- |
| Package | `cc_toy_lab` exists with `geometry`, `spectral`, `radion`, `topology`, and `discovery` modules. Synthetic controls are in `cc_toy_lab/spectral/random_matrix_controls.py`; the S2 monopole control is in `cc_toy_lab/spectral/dirac_monopole_s2.py`; the 3D Anderson benchmark is in `cc_toy_lab/spectral/anderson_3d.py`; spectrum-window diagnostics are in `cc_toy_lab/spectral/anderson_windows.py`; toy Dirac localization is in `cc_toy_lab/spectral/dirac_localization.py`; toy chirality/index diagnostics are in `cc_toy_lab/spectral/dirac_chirality.py`; the historical artificial bridge is in `cc_toy_lab/spectral/s2_graph_intermediate.py`; the current geometric product-operator bridge is in `cc_toy_lab/spectral/s2_s1_product.py`. |
| Scripts | `scripts/radion_stabilization.py`, `scripts/spectral_localization.py`, `scripts/r_stat_controls.py`, `scripts/dirac_monopole_s2.py`, `scripts/anderson_3d_benchmark.py`, `scripts/anderson_3d_spectrum_windows.py`, `scripts/anderson_3d_boundary_comparison.py`, `scripts/anderson_3d_periodic_followup.py`, `scripts/dirac_localization_benchmark.py`, `scripts/dirac_chirality_diagnostic.py`, `scripts/s2_graph_intermediate.py`, `scripts/s2_s1_product.py`, `scripts/s2_s1_discretization_comparison.py`, `scripts/run_all_mvp.py`. |
| Tests | `tests/` exists. Latest documented `pytest -q` status after v0.1.15 promotion (product-discretized full + ring/alpha=0 follow-up): **203 passed, 1 warning** (`reports/VALIDATION_STATUS.md`, `reports/RELEASE_NOTES_v0.1.15.md`). Older README snapshots below may still cite earlier counts for specific historical runs. |
| Reports | `reports/RADION_REPORT.md`, `reports/SPECTRAL_REPORT.md`, `reports/CHIRALITY_INDEX_REPORT.md`, `reports/VALIDATION_STATUS.md`, `reports/DISCOVERY_LEDGER.md`, `reports/NULL_RESULTS.md`, `reports/ISSUES_SCIENTIFIC.md`. |
| Figures | Dashboards are saved in `reports/FIGURES/`. |
| Git | The folder is not currently a git repository. |

Verified radion metrics:

| Metric | Value |
| --- | ---: |
| `R0_B` from `scripts/radion_stabilization.py` | `1.189207` |
| MFG relative error from verified script run | `0.000671543` |
| Last recorded radion run | `reports/RUNS/20260511-221223_radion_stabilization` |
| `R0_B_numeric` | `1.1892071179` |
| `R0_C_numeric` | `1.2850196686` |
| `R0_D_numeric` | `1.2959657202` |
| Max multitrajectory error | `5.666e-05` |
| Estimated `alpha_c` | `1.345` |

Verified spectral quick-smoke state:

| Metric | Value |
| --- | ---: |
| Command | `python scripts/spectral_localization.py --quick` |
| Dashboard | `reports/FIGURES/spectral_localization_dashboard.png` |
| Weak-disorder result | `W=0.5`, `<r>=0.2631` |
| Interpretation | Null/limiting result: this is not closer to GOE than to Poisson. |

Verified synthetic r-statistics controls:

| Ensemble | Expected `<r>` | Measured `<r>` | Tolerance | Passed |
| --- | ---: | ---: | ---: | --- |
| Poisson | `0.3863` | `0.3817` | `0.0350` | yes |
| GOE | `0.5307` | `0.5309` | `0.0400` | yes |
| GUE optional | `0.5996` | `0.5960` | `0.0450` | yes |

Latest synthetic-control run:

- `reports/RUNS/20260511-224352_r_stat_controls_full`
- Saved artifacts: `metrics.json`, `config.json`, `data.npz`, `summary.md`,
  `figures/r_stat_control_histograms.png`.
- `python scripts/r_stat_controls.py --quick` passed.
- `python scripts/r_stat_controls.py --full` passed.

## Current Validation Status

| Block | Status |
| --- | --- |
| Radion toy model | verified |
| r-statistics controls | verified |
| S2 Dirac monopole index | verified positive control |
| Toy Dirac localization/chirality | verified negative control |
| S2 x graph intermediate bridge | historical artificial bridge |
| S2 x S1 product-operator bridge | configured full profile passed |
| **S³×S¹ Gate 4B FSS (v0.1.21)** | **GATE4B_FSS_PASS_WITH_CAVEATS** |
| Continuum product geometry | not yet validated |
| `S6` / `S3 x S6` | not yet validated |
| Standard Model physics | not validated |

**Gate 4B Update (2026-05-22):** S³×S¹ finite-size scaling campaign completed with metric-corrected true IPR. 216/216 cases, 0 failures, aggregate contrast 7.15× (W=20 vs W=0), FSS trend STRENGTHENING (3.76× → 24.90×). Verdict: GATE4B_FSS_PASS_WITH_CAVEATS. Full report: `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md`. Status: `reports/CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md`.

Verified finite-mode S2 Dirac monopole index control:

| q | cutoff | expected index | numerical index | n_plus | n_minus | passed |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| -3 | 5 | -3 | -3 | 0 | 3 | yes |
| -2 | 5 | -2 | -2 | 0 | 2 | yes |
| -1 | 5 | -1 | -1 | 0 | 1 | yes |
| 0 | 5 | 0 | 0 | 0 | 0 | yes |
| 1 | 5 | 1 | 1 | 1 | 0 | yes |
| 2 | 5 | 2 | 2 | 2 | 0 | yes |
| 3 | 5 | 3 | 3 | 3 | 0 | yes |

Latest S2 monopole index runs:

- Quick: `reports/RUNS/20260511-225920_dirac_monopole_s2_quick`
- Full: `reports/RUNS/20260511-230305_dirac_monopole_s2_full`
- Report: `reports/CHIRALITY_INDEX_REPORT.md`
- Convention: `q > 0` has positive-chirality zero modes, so
  `index = n_plus - n_minus = q`.

Saved full-run artifacts:

- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/config.json`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/metrics.json`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/data.npz`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/summary.md`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/figures/dirac_monopole_s2_eigenvalues.png`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/figures/dirac_monopole_s2_index.png`

Verified 3D Anderson configured full benchmark:

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

3D Anderson full run:

- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full`
- Saved artifacts:
  - `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/config.json`
  - `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/metrics.json`
  - `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/data.npz`
  - `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/summary.md`
  - `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/figures/anderson_3d_r_statistics.png`
  - `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/figures/anderson_3d_ipr.png`
- Basic checks passed: weak reference closer to GOE than Poisson, strong
  reference moved toward Poisson, and IPR increased.
- This is stronger than quick mode, but it is still a configured benchmark on
  small lattices. It does not prove localization in a target physical model.

Pending:

- Full spectrum-window diagnostics remain pending: quantile windows are
  implemented in `--full` mode but have not been verified.
- Larger 3D Anderson scaling remains pending: bigger `L`, more seeds, finer
  W-grid, and boundary-condition comparison.

## 3D Anderson Full Benchmark

The 3D benchmark replaces the old weak 1D quick smoke as the next localization
diagnostic. The configured full mode uses `L = 4, 5, 6, 7`, eight disorder
values, and eight realizations per point. It uses a cubic lattice with open
boundaries by default:

```text
H_ij = epsilon_i delta_ij + t * nearest_neighbor_terms
epsilon_i ~ Uniform[-W/2, W/2]
```

Command:

```powershell
python scripts/anderson_3d_benchmark.py --full
```

Run path:

```text
reports/RUNS/20260511-232546_anderson_3d_benchmark_full
```

Final-size `L=7` full results:

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

Basic checks passed:

- Weak reference `W=4` is closer to GOE than Poisson.
- Strong reference `W=24` moved close to Poisson relative to weak reference.
- IPR increased from weak to strong disorder.

Limitations:

- This is benchmark validation only, not proof of a target physical model.
- Lattices are still small and realizations remain limited.
- Open boundary conditions are used by default; periodic boundaries still need
  comparison.
- Larger finite-size scaling is still needed.
- Spectrum-window diagnostics are quick-verified for center/lower/upper windows;
  full quantile-window validation is pending.
- This does not prove localization in the target physical model, chirality, or
  covariant compactification.

## 3D Anderson Spectrum-Window Diagnostics

Spectrum-window diagnostics test whether the Anderson localization diagnostic
depends on the selected spectral region. Quick mode checks center, lower-band,
and upper-band windows.

Quick command:

```powershell
python scripts/anderson_3d_spectrum_windows.py --quick
```

Full command:

```powershell
python scripts/anderson_3d_spectrum_windows.py --full
```

Full mode has been run and produced a mixed/limiting result. It did not promote
the baseline at the time; the historical promotion baseline then remained
`v0.1.8-mvp-dirac-localization-full`. It adds quantile windows
`quantile_0.1`, `quantile_0.3`, `quantile_0.5`, `quantile_0.7`, and
`quantile_0.9`.

Verified quick run:

```text
reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick
```

Final `L=6` window assessment:

| window | weak `<r>` | strong `<r>` | weak IPR | strong IPR | passed |
| --- | ---: | ---: | ---: | ---: | --- |
| center | `0.5187` | `0.4280` | `0.0158342` | `0.344868` | True |
| lower | `0.5357` | `0.4181` | `0.0190603` | `0.434601` | True |
| upper | `0.5808` | `0.3960` | `0.0204236` | `0.344342` | True |

Quick result summary:

- `all_windows_basic_checks_passed=True`
- `window_choice_changes_conclusion=False`
- Window choice did not change the basic localization diagnostic in this run.

Saved artifacts:

- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/config.json`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/metrics.json`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/data.npz`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/summary.md`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/figures/r_by_window.png`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/figures/ipr_by_window.png`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/figures/window_comparison_heatmap.png`

Interpretation:

The quick run reduces concern that the configured 3D Anderson result is only a
center-window artifact. It still does not prove target physical localization,
chirality, covariant compactification, Witten/Lichnerowicz bypass, or Standard
Model physics.

Full run:

```text
reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full
```

Full `L=7` window assessment:

| window | weak `<r>` | strong `<r>` | weak IPR | strong IPR | passed |
| --- | ---: | ---: | ---: | ---: | --- |
| center | `0.5200` | `0.4424` | `0.0100626` | `0.305547` | True |
| lower | `0.5399` | `0.4093` | `0.0128243` | `0.351711` | True |
| upper | `0.5327` | `0.4130` | `0.0128753` | `0.35176` | True |
| quantile_0.1 | `0.5540` | `0.3977` | `0.0133127` | `0.367085` | True |
| quantile_0.3 | `0.5011` | `0.3853` | `0.0108976` | `0.313394` | True |
| quantile_0.5 | `0.5363` | `0.4601` | `0.00994604` | `0.29276` | False |
| quantile_0.7 | `0.5370` | `0.4347` | `0.0110571` | `0.29539` | True |
| quantile_0.9 | `0.5037` | `0.4242` | `0.0130484` | `0.336491` | True |

Full result summary:

- `all_windows_basic_checks_passed=False`
- `window_choice_changes_conclusion=True`
- `quantile_0.5` is the anomalous window under the implemented basic check.
- IPR increases from weak to strong disorder in all listed windows, including
  `quantile_0.5`.
- Strong disorder moves toward Poisson in seven of eight windows; `quantile_0.5`
  remains slightly closer to GOE than Poisson at `W=24`.

Full-run artifacts:

- `reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full/config.json`
- `reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full/metrics.json`
- `reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full/data.npz`
- `reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full/summary.md`
- `reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full/figures/r_by_window.png`
- `reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full/figures/ipr_by_window.png`
- `reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full/figures/window_comparison_heatmap.png`

Follow-up targeted diagnostic:

```text
reports/RUNS/20260512-091720_anderson_quantile05_diagnostics
```

Classification:

```text
likely statistical/finite-size/seed-count effect: quantile_0.5 at W=24 becomes Poisson-like in the targeted rerun
```

At final `L=8`, `quantile_0.5` is closer to Poisson for all targeted
strong-disorder values:

| W | q0.5 `<r>` | q0.5 IPR | closer to Poisson |
| ---: | ---: | ---: | --- |
| 20 | `0.4531` | `0.203311` | True |
| 24 | `0.4127` | `0.287083` | True |
| 28 | `0.4052` | `0.347418` | True |
| 32 | `0.3981` | `0.437972` | True |
| 36 | `0.3973` | `0.480156` | True |

## 3D Anderson Boundary Comparison

This diagnostic compares the same configured 3D Anderson benchmark under open
and periodic boundary conditions. It tests benchmark stability only.

Command:

```powershell
python scripts/anderson_3d_boundary_comparison.py
```

Run:

```text
reports/RUNS/20260512-093014_anderson_3d_boundary_comparison
```

Final `L=7` boundary assessments:

| boundary | window | weak `<r>` | strong `<r>` | weak IPR | strong IPR | passed |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| open | center | `0.5389` | `0.4436` | `0.00990934` | `0.304479` | True |
| open | quantile_0.5 | `0.5082` | `0.4527` | `0.00995662` | `0.290984` | True |
| periodic | center | `0.5481` | `0.4670` | `0.00916441` | `0.190352` | False |
| periodic | quantile_0.5 | `0.5482` | `0.4620` | `0.00908064` | `0.174754` | False |

Summary:

- `all_boundary_basic_checks_passed=False`
- `boundary_changes_basic_diagnostic=True`
- `max_abs_delta_r=0.0804`
- `max_abs_delta_ipr=0.116229`
- Interpretation: open and periodic boundaries disagree under the current
  strong-disorder pass/fail criterion, so this is a recorded limitation.
- Historical null-result remains preserved: `W=0.5`, `<r>=0.2631`.

Saved artifacts:

- `reports/RUNS/20260512-093014_anderson_3d_boundary_comparison/config.json`
- `reports/RUNS/20260512-093014_anderson_3d_boundary_comparison/metrics.json`
- `reports/RUNS/20260512-093014_anderson_3d_boundary_comparison/data.npz`
- `reports/RUNS/20260512-093014_anderson_3d_boundary_comparison/summary.md`
- `reports/RUNS/20260512-093014_anderson_3d_boundary_comparison/figures/r_open_vs_periodic.png`
- `reports/RUNS/20260512-093014_anderson_3d_boundary_comparison/figures/ipr_open_vs_periodic.png`
- `reports/RUNS/20260512-093014_anderson_3d_boundary_comparison/figures/boundary_delta_heatmap.png`

This does not prove target-model localization, chirality, covariant
compactification, Witten/Lichnerowicz bypass, or Standard Model physics.

## 3D Anderson Periodic-Boundary Follow-Up

This targeted diagnostic follows up the periodic-boundary failures from
`reports/RUNS/20260512-093014_anderson_3d_boundary_comparison`.

Command:

```powershell
python scripts/anderson_3d_periodic_followup.py
```

Run:

```text
reports/RUNS/20260512-094128_anderson_periodic_followup
```

Classification:

```text
likely insufficient disorder range at W=24 with finite-size/seed-count sensitivity: periodic boundaries become Poisson-like for W>=32 at the final lattice size
```

Final `L=8` periodic strong-disorder summary:

| W | center `<r>` | q0.5 `<r>` | center IPR | q0.5 IPR | q0.5 closer to Poisson |
| ---: | ---: | ---: | ---: | ---: | --- |
| 24 | `0.4567` | `0.4590` | `0.194963` | `0.193183` | False |
| 32 | `0.4275` | `0.4473` | `0.33069` | `0.329627` | True |
| 36 | `0.4009` | `0.4106` | `0.418799` | `0.424562` | True |
| 40 | `0.4037` | `0.4150` | `0.435981` | `0.438452` | True |

Summary:

- `stronger_disorder_makes_periodic_poisson_like=True`
- `ipr_mostly_monotonic_all=True`
- `spectrum_window_artifact_suspected=False`
- This did not promote the baseline at the time; the historical promotion
  baseline then remained `v0.1.8-mvp-dirac-localization-full`.
- This updates the boundary limitation but does not erase the earlier failed
  open-vs-periodic comparison.

Saved artifacts:

- `reports/RUNS/20260512-094128_anderson_periodic_followup/config.json`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/metrics.json`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/data.npz`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/summary.md`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/figures/periodic_r_vs_w.png`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/figures/periodic_ipr_vs_w.png`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/figures/periodic_distance_to_poisson_goe.png`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/figures/periodic_open_comparison_optional.png`

This is still benchmark diagnosis only. It does not prove target-model
localization, chirality, covariant compactification, Witten/Lichnerowicz
bypass, or Standard Model physics.

## Full Toy Dirac/Geometric Localization Benchmark

This benchmark applies the calibrated localization diagnostics to finite chiral
block toy operators:

```text
D = [[0, A], [A^dagger, 0]]
```

Supported modes are `clean`, `random_mass`, `gauge_phase`, and
`geometric_weight`.

Command:

```powershell
python scripts/dirac_localization_benchmark.py --full
python scripts/dirac_chirality_diagnostic.py --full
python scripts/s2_graph_intermediate.py --quick
```

Run:

```text
reports/RUNS/20260512-130351_dirac_localization_full
```

Final `size=96` mode assessment:

| mode | weak W | strong W | weak IPR | strong IPR | weak `<r>` | strong `<r>` | IPR increases | r toward Poisson | near-zero signal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| clean | 0 | 8 | `0.0104167` | `0.0104167` | `0.9259` | `0.9259` | False | False | True |
| gauge_phase | 0 | 8 | `0.0104167` | `0.00520833` | `0.9259` | `0.3329` | False | True | True |
| geometric_weight | 0 | 8 | `0.0104167` | `0.135186` | `0.9259` | `0.3798` | True | True | True |
| random_mass | 0 | 8 | `0.0104167` | `0.315382` | `0.9259` | `0.3785` | True | True | True |

Summary:

- `all_symmetry_checks_passed=True`
- `any_near_zero_modes=True`
- IPR increases in `random_mass` and `geometric_weight`.
- r-statistics moves toward Poisson in `random_mass`, `gauge_phase`, and
  `geometric_weight`.
- `clean` remains a no-localization reference.
- `gauge_phase` moves r-statistics toward Poisson, but near-zero IPR does not
  increase.
- Near-zero modes are numerical signals only, not protected chiral zero modes.
- Historical promotion baseline: `v0.1.8-mvp-dirac-localization-full`.

Saved artifacts:

- `reports/RUNS/20260512-130351_dirac_localization_full/config.json`
- `reports/RUNS/20260512-130351_dirac_localization_full/metrics.json`
- `reports/RUNS/20260512-130351_dirac_localization_full/data.npz`
- `reports/RUNS/20260512-130351_dirac_localization_full/summary.md`
- `reports/RUNS/20260512-130351_dirac_localization_full/figures/dirac_spectrum.png`
- `reports/RUNS/20260512-130351_dirac_localization_full/figures/dirac_ipr_vs_disorder.png`
- `reports/RUNS/20260512-130351_dirac_localization_full/figures/dirac_r_statistics.png`
- `reports/RUNS/20260512-130351_dirac_localization_full/figures/dirac_near_zero_count.png`

This connects benchmark diagnostics to toy Dirac-like operators, but it does
not prove physical chirality, Witten/Lichnerowicz bypass, covariant
compactification, or Standard Model fermions.

## Installation

Python 3.11+ is expected.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS/Linux shell:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Quick Verification

Run these commands from the repository root:

```powershell
pytest -q
python scripts/radion_stabilization.py
python scripts/r_stat_controls.py --full
python scripts/dirac_monopole_s2.py --quick
python scripts/anderson_3d_benchmark.py --quick
python scripts/anderson_3d_spectrum_windows.py --quick
python scripts/anderson_3d_boundary_comparison.py
python scripts/anderson_3d_periodic_followup.py
python scripts/dirac_localization_benchmark.py --full
python scripts/dirac_chirality_diagnostic.py --full
python scripts/s2_graph_intermediate.py --quick
python scripts/s2_s1_product.py --quick
python scripts/s2_s1_product.py --full
```

Additional smoke commands:

```powershell
python scripts/dirac_monopole_s2.py --full
python scripts/spectral_localization.py --quick
python scripts/run_all_mvp.py
```

Expected quick verification:

- `pytest -q` should report **203 passed, 1 warning** (latest documented after v0.1.15 promotion; see `reports/VALIDATION_STATUS.md`, `reports/RELEASE_NOTES_v0.1.15.md`).
- `radion_stabilization.py` should generate the radion dashboard and report
  `R0_B` near `1.189207`.
- `r_stat_controls.py --full` should validate the same synthetic controls with
  the larger full configuration.
- `dirac_monopole_s2.py --quick` should verify that the finite-mode index
  tracks monopole charge for the quick charge set.
- `anderson_3d_benchmark.py --quick` should run the 3D cubic Anderson benchmark
  and save r-statistics/IPR artifacts.
- `anderson_3d_spectrum_windows.py --quick` should run center/lower/upper
  spectrum-window diagnostics and save window-resolved artifacts.
- `anderson_3d_boundary_comparison.py` should run open-vs-periodic comparison,
  save comparison artifacts, and record the current boundary-sensitive
  limitation.
- `anderson_3d_periodic_followup.py` should rerun targeted periodic-boundary
  strong-disorder diagnostics and keep the baseline unchanged.
- `dirac_localization_benchmark.py --full` should run toy Dirac/geometric
  localization diagnostics, check `+-lambda` symmetry, and save IPR/r-statistic
  artifacts.
- `dirac_chirality_diagnostic.py --full` should verify `Gamma` algebra,
  preserve `{D,Gamma}=0`, and report zero numerical index for the current toy
  localization modes.
- `s2_graph_intermediate.py --quick` should run the intermediate `S2 monopole x
  graph` toy bridge, preserve the inherited nonzero index under the configured
  chiral perturbation, and show graph-selector IPR growth with disorder.
- `s2_s1_product.py --quick` should run the first `S2 x S1` product-operator
  quick bridge, save run artifacts, and report benchmark-level gate flags
  without claiming continuum compactification or a full-product global chiral
  theorem.
- `s2_s1_product.py --full` should keep the same toy/non-claim framing while
  checking the configured full profile and saving the full run artifacts.
- `dirac_monopole_s2.py --full` should verify the same convention for
  `q = -3, -2, -1, 0, 1, 2, 3`.
- `spectral_localization.py --quick` should generate the spectral dashboard.
- `run_all_mvp.py` should complete the quick MVP smoke run.

## Expected Outputs

The main generated artifacts are:

- `reports/FIGURES/radion_stabilization_dashboard.png`
- `reports/FIGURES/spectral_localization_dashboard.png`
- `reports/RUNS/<timestamp>_r_stat_controls_quick/`
- `reports/RUNS/<timestamp>_r_stat_controls_full/`
- `reports/RUNS/<timestamp>_dirac_monopole_s2_quick/`
- `reports/RUNS/<timestamp>_dirac_monopole_s2_full/`
- `reports/RUNS/<timestamp>_anderson_3d_benchmark_quick/`
- `reports/RUNS/<timestamp>_anderson_3d_spectrum_windows_quick/`
- `reports/RUNS/<timestamp>_anderson_3d_boundary_comparison/`
- `reports/RUNS/<timestamp>_dirac_localization_full/`
- `reports/RUNS/<timestamp>_s2_graph_intermediate_quick/`
- `reports/RUNS/<timestamp>_s2_s1_product_quick/`
- `reports/RUNS/<timestamp>_s2_s1_product_full/`
- `reports/RUNS/<timestamp>_radion_stabilization/`
- `reports/RUNS/<timestamp>_spectral_localization/`
- `reports/RADION_REPORT.md`
- `reports/SPECTRAL_REPORT.md`
- `reports/CHIRALITY_INDEX_REPORT.md`
- `reports/VALIDATION_STATUS.md`
- `reports/DISCOVERY_LEDGER.md`
- `reports/NULL_RESULTS.md`
- `reports/ISSUES_SCIENTIFIC.md`

Each run directory is expected to contain:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/`

## Radion Module

The radion module implements a reproducible toy stabilization experiment.

Files:

- `cc_toy_lab/radion/potentials.py`
- `cc_toy_lab/radion/dynamics.py`
- `cc_toy_lab/radion/mfg.py`
- `cc_toy_lab/radion/phase_transition.py`
- `cc_toy_lab/radion/dashboard.py`
- `scripts/radion_stabilization.py`

Implemented toy potentials:

| Potential | Form | Purpose |
| --- | --- | --- |
| A | `a/R^2` | Unstable baseline; no stabilizing finite minimum. |
| B | `a/R^2 + b R^2` | Minimal stabilizing potential. |
| C | `a/R^2 + b R^2 + c/R^4` | Stabilizing potential with Casimir-like correction. |
| D | `B + toy-regularized KK tower` | Toy KK correction; not a full quantum effective energy. |

Default target and controls:

- `R0_B` target: approximately `1.1892`.
- `alpha_c`: `1.345`.
- MFG dynamics use agents attracted to `1/R`.
- The phase scan checks a toy threshold transition near `alpha_c`.

Current assert checks cover:

- Potential B minimum near `R0_B`.
- Positive curvature at the B minimum.
- Five stable trajectories converging to the same attractor.
- MFG self-consistency against `1/R0_B`.
- Grid-invariant alpha-threshold smoke check.

Dashboard panels:

1. Effective potentials A-D.
2. Curvature / stability at minima.
3. Stable trajectories for potential B.
4. Potential A trajectories showing no false stabilization.
5. MFG self-consistency: `R(t)` and mean field `x_bar(t)`.
6. Toy phase transition: `R0(alpha)` and order parameter.

Interpretation limits:

- The radion result proves only that the specified toy equations stabilize under
  the chosen parameters.
- It does not prove real extra-dimensional stabilization.
- It does not prove a correct quantum effective action.
- It does not remove the need for physical model-building and stability checks.

## Spectral Module

The spectral module implements localization diagnostics and toy Dirac checks.

Files:

- `cc_toy_lab/spectral/anderson.py`
- `cc_toy_lab/spectral/metrics.py`
- `cc_toy_lab/spectral/toy_dirac.py`
- `cc_toy_lab/spectral/unfolding.py`
- `cc_toy_lab/spectral/localization.py`
- `scripts/spectral_localization.py`

Implemented diagnostics:

- Anderson benchmark.
- Adjacent-gap ratio `<r>`.
- IPR, inverse participation ratio.
- Toy Dirac block symmetry check.
- Finite-size smoke plotting.

Reference values used for interpretation:

| Ensemble | Expected `<r>` |
| --- | ---: |
| Poisson | about `0.3863` |
| GOE | about `0.5307` |
| GUE | about `0.5996` |

Current quick-mode null result:

- `python scripts/spectral_localization.py --quick` was run.
- It created `reports/FIGURES/spectral_localization_dashboard.png`.
- In quick mode, weak disorder `W=0.5` produced `<r>=0.2631`.
- This is not closer to GOE than to Poisson.
- The result is logged as a null/limiting result, not hidden as success.

Why this should not be overinterpreted:

- Quick mode is a smoke test, not full spectral validation.
- The current benchmark is a compact 1D Anderson-style control. Weak-disorder
  behavior in this setup should not be treated as a general GOE claim.
- Localization metrics do not prove chirality.
- Near-zero modes do not prove protected chiral zero modes.
- A GOE -> Poisson transition, if later observed in a stronger model, would
  still be only a localization signal unless a Dirac index and chiral quantum
  numbers are checked.

Pending full spectral work:

- Full default sweep: `N=512`, `30` disorder values, `30` realizations.
- Stronger Anderson model: 3D or quasi-dimensional geometry.
- Dirac index control before any chirality claims.

Synthetic r-statistics controls:

- `python scripts/r_stat_controls.py --quick` validates the statistic pipeline on
  Poisson, GOE, and optional GUE synthetic spectra.
- `python scripts/r_stat_controls.py --full` runs the larger synthetic control
  configuration. This mode is verified in the current baseline.
- This control validates the statistic implementation only. It is not a physics
  result and does not validate Anderson localization by itself.

Current full control results:

| Ensemble | Expected `<r>` | Measured `<r>` | Tolerance | Passed |
| --- | ---: | ---: | ---: | --- |
| Poisson | `0.3863` | `0.3817` | `0.0350` | yes |
| GOE | `0.5307` | `0.5309` | `0.0400` | yes |
| GUE optional | `0.5996` | `0.5960` | `0.0450` | yes |

Why this matters: `mean_adjacent_gap_ratio` now passes independent synthetic
Poisson/GOE/GUE controls in quick and full modes. This reduces the risk that the Anderson
quick null-result comes from a broken r-statistics implementation.

What this does not prove: no Anderson localization claim, no chirality claim,
no physics validation, no Witten/Lichnerowicz no-go bypass, and no covariant
compactification claim follows from these synthetic controls.

## S2 Dirac Monopole Index Control

The S2 monopole control is the first chirality-related validation layer in the
project. It is a finite-mode spectral toy model with a documented convention:

```text
q > 0 has positive-chirality zero modes
q < 0 has negative-chirality zero modes
index(D) = n_plus - n_minus = q
```

Commands:

```powershell
python scripts/dirac_monopole_s2.py --quick
python scripts/dirac_monopole_s2.py --full
```

The full run checks `q = -3, -2, -1, 0, 1, 2, 3` over cutoffs
`1, 2, 3, 5`. The latest verified full run is:

```text
reports/RUNS/20260511-230305_dirac_monopole_s2_full
```

This validates index-counting infrastructure and chirality bookkeeping on a
known finite-mode toy control. It does not prove physical chiral fermions,
does not bypass Witten/Lichnerowicz no-go theorems, and does not derive
Standard Model fermions.

## Geometry Module

The geometry module provides analytic controls for compact spaces:

- Scalar curvature of round spheres.
- Laplacian eigenvalues on `S^n_R`.
- Degeneracies of spherical harmonics.
- Product spectrum sum rules, including `S3 x S6`.
- Sphere sampling and graph-Laplacian helpers for later numerical checks.

Interpretation limits:

- Reproducing `S3 x S6` product spectra does not show that `S3 x S6` is a
  cosmological vacuum.
- It does not derive gauge fields or the Standard Model.
- Graph Laplacian approximations on high-dimensional spheres are sensitive to
  sampling, kNN choices, and scale parameters.

## Scientific Logs

The project keeps scientific bookkeeping separate from code output.

| File | Purpose |
| --- | --- |
| `reports/DISCOVERY_LEDGER.md` | Unexpected findings, hypotheses, suspected artifacts, and toy signals. |
| `reports/NULL_RESULTS.md` | Negative results and failed hypotheses. These are first-class results. |
| `reports/ISSUES_SCIENTIFIC.md` | Scientific caveats, contested assumptions, and overclaiming risks. |

Rules for interpretation:

- Do not call a finding an observation until the data and config are saved.
- Do not call an observation a toy signal until it is reproduced across seeds or controls.
- Do not call a toy signal a physical result without the relevant physical
  invariant, such as an index calculation for chirality.

## Known Limitations

- The current spectral quick mode produced a null/limiting weak-disorder result.
- Synthetic r-statistics controls validate the statistic pipeline, not Anderson
  physics.
- The configured full 3D Anderson benchmark passed basic checks, but larger
  scaling remains pending.
- Full quantile-window diagnostics produced a mixed `quantile_0.5` result;
  targeted follow-up reduced that concern but did not remove the need for
  larger scaling.
- Open-vs-periodic boundary comparison produced a boundary-sensitive limitation:
  open boundaries passed the current check, while periodic boundaries did not.
- The periodic-boundary follow-up suggests the earlier periodic failure is
  likely an insufficient-disorder-range issue at `W=24`, with finite-size and
  seed-count sensitivity. This reduces the concern but does not promote the
  baseline.
- The full `S1` discretization comparison with `spectral_circle`, `ring`, and
  `wilson_ring` is mixed/limiting: `ring` fails
  `localization_gate_passed=False` on the full profile while the reference
  `spectral_circle` and `wilson_ring` remain clean. This blocks promotion to a
  discretization-robust full baseline.
- Anderson model physics is not fully validated.
- The toy Dirac/geometric localization benchmark is quick-only so far. It
  reports localization diagnostics on finite chiral block operators, not
  physical chirality or an index result.
- Physical chirality in a compactification model is not validated.
- The S2 monopole result is a finite-mode index-pipeline control, not a
  physical chiral-fermion construction.
- The legacy `scripts/spectral_localization.py` default sweep has not been
  rerun after the 3D benchmark upgrade.
- Spectrum-window diagnostics are quick-verified for center/lower/upper windows.
  The full quantile-window run produced a mixed result driven by `quantile_0.5`;
  targeted follow-up classifies it as likely statistical/finite-size/seed-count
  sensitivity.
- The spectral benchmark still needs boundary-sensitivity diagnosis and
  larger-size controls before it can support broad localization conclusions.
- The radion phase transition is a toy threshold model pinned to `alpha_c=1.345`,
  not a derived physical critical point.
- Potential D uses toy regularization of a KK tower, not a complete one-loop
  quantum effective energy.
- The toy Dirac/geometric localization operator checks finite block symmetry and
  numerical localization metrics. It is not an index test.
- No result in this MVP establishes protected chiral zero modes.
- No result in this MVP derives `SU(3) x SU(2) x U(1)`.
- The folder is not currently a git repository, so baseline versioning is
  documented by file state and reports rather than commits or tags.

## Next Validation Steps

Priority order:

1. Diagnose why `ring` fails `localization_gate_passed` on the full
   `S1`-discretization comparison while `spectral_circle` and `wilson_ring`
   pass.
2. Add product-level figures if they improve interpretation without overclaim.
3. Move to product-discretized geometric refinements before any `S6` or
   `S3 x S6` step.
4. Repeat periodic-boundary follow-up with larger `L` if feasible, more seeds,
   and explicit open-reference matching at the same resolution.
5. Increase `L`, seed count, and W-grid resolution.
6. Test window-width sensitivity for `quantile_0.5`.
7. Test mobility-edge behavior across spectral windows.
8. Check dense/sparse eigensolver consistency for the larger Anderson runs.
9. Add geometry spectrum validation for `S2`, `S3`, `S6`, and `S3 x S6`.

The strongest next chirality-related step is an independent geometric
discretization of the `S2` Dirac monopole operator. It should test whether the
index-counting result survives a construction less directly tied to the known
finite-mode spectrum.

## Toy Dirac Chirality/Index Diagnostic

This diagnostic adds `Gamma = diag(+I, -I)` to the toy Dirac localization
operators and checks whether near-zero modes carry a nonzero numerical index.

Command:

```powershell
python scripts/dirac_chirality_diagnostic.py --full
```

Run:

```text
reports\RUNS\20260512-135933_dirac_chirality_full
```

Summary:

- `gamma_algebra_passed=True`
- `anticommutation_preserved=True`
- `all_indices_zero=True`
- `any_near_zero_modes=True`
- Historical promotion baseline: `v0.1.10-mvp-dirac-chirality-full`

Interpretation:

The current toy localization near-zero modes are classified as paired or
accidental under this diagnostic because the numerical index remains zero. This
does not contradict the verified `S2` monopole index control; it says the toy
localization modes have not produced protected/chiral zero modes.

## S2 Monopole x Graph Intermediate Bridge

This is the first intermediate toy bridge where a nonzero index and a
localization diagnostic coexist in one controlled model.

Role of the three controls:

- Negative control: toy Dirac localization/chirality has near-zero modes, but
  the numerical index remains `0`, so the modes are classified as paired or
  accidental rather than protected/chiral zero modes.
- Positive control: finite-mode `S2` monopole verifies `index(D) = q` and shows
  that the index pipeline can detect nonzero topological index.
- Intermediate bridge: finite-mode `S2 monopole x graph` combines the verified
  nonzero-index `S2` sector with graph-sector localization diagnostics in one
  toy bridge.

The index is inherited from the verified `S2` monopole sector, while the graph
sector acts as an artificial localization selector inside the zero-mode sector.

Command:

```powershell
python scripts/s2_graph_intermediate.py --quick
```

Run:

```text
reports\RUNS\20260512-141913_s2_graph_intermediate_quick
```

Summary:

- `all_index_checks_passed=True`
- `all_anticommutators_preserved=True`
- `ipr_growth_observed=True`
- Baseline: `v0.1.11-mvp-s2-graph-intermediate-quick`

Saved artifacts:

- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/config.json`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/metrics.json`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/data.npz`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/summary.md`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/figures/index_vs_disorder.png`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/figures/zero_mode_ipr_vs_disorder.png`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/figures/perturbation_stability.png`
- `reports/RUNS/20260512-141913_s2_graph_intermediate_quick/figures/chirality_counts.png`

Interpretation:

This toy bridge shows index plus localization diagnostics simultaneously in a
controlled intermediate model. It is not continuum `S2 x S1`, not `S6`, not
`S3 x S6`, not a physical compactification claim, and not a Standard Model
fermion derivation. It does not validate covariant compactification and does
not bypass Witten/Lichnerowicz no-go results.

## S2 × S1 Product-Operator Benchmark

This is the first bridge where the auxiliary `S1` factor enters the toy
operator itself rather than appearing only as an external selector.

Progression of controls:

- Negative control: toy Dirac localization/chirality has near-zero modes, but
  the numerical index remains `0`.
- Positive control: finite-mode `S2` monopole verifies `index(D)=q`.
- Historical artificial bridge: `S2 monopole x graph` preserves inherited index
  while the graph sector acts as a localization selector.
- First geometric product-operator bridge: `S2 x S1` inserts the circle factor
  directly into the operator:

```text
D_{S2xS1} = D_{S2}(q) ⊗ I_{S1} + Γ_{S2} ⊗ P_{S1}(α, W)
```

Verified commands:

```powershell
python scripts/s2_s1_product.py --quick
python scripts/s2_s1_product.py --full
```

Latest full run:

```text
reports/RUNS/20260512-180321_s2_s1_product_full
```

Historical quick run:

```text
reports/RUNS/20260512-172546_s2_s1_product_quick
```

Full-run status:

- Baseline: `v0.1.13-mvp-s2-s1-product-full`
- `classification=quick_bridge_passed`
- `all_basic_gates_passed=True`
- `total_observations=6750`
- `q_control_passed=True`
- `pbc_gate_passed=True`
- `apbc_gate_passed=True`
- `flux_response_observed=True`
- `s1_not_spectator=True`
- `localization_gate_passed=True`
- `threshold_stable=True`
- `pytest -q: 100 passed` (snapshot when this run was recorded; current suite: **132 passed**, `reports/VALIDATION_STATUS.md`)
- Runtime-safe full config recorded in `config.json`: `cutoff=2`,
  `s1_sizes=(8, 16, 24)`, `boundary_twists=(0.0, 0.25, 0.5)`,
  `realizations=5`

Saved artifacts:

- `reports/RUNS/20260512-180321_s2_s1_product_full/config.json`
- `reports/RUNS/20260512-180321_s2_s1_product_full/metrics.json`
- `reports/RUNS/20260512-180321_s2_s1_product_full/data.npz`
- `reports/RUNS/20260512-180321_s2_s1_product_full/summary.md`
- `reports/RUNS/20260512-180321_s2_s1_product_full/figures/`

Interpretation:

This is a toy product diagnostic. It checks inherited `S2` monopole kernel
behavior together with `S1` twist and localization response inside one toy
operator. The full configured profile retained the same benchmark-level
classification and passed all basic gates. Full-product global chiral index is
not the headline metric here.

Explicit non-claims:

- no continuum compactification;
- no `S6` / `S3 x S6`;
- no Standard Model derivation;
- no physical chirality proof;
- no Witten/Lichnerowicz bypass.

Next steps:

1. Diagnose why the full-profile `ring` family loses
   `localization_gate_passed`.
2. Add figures if they help interpretation.
3. Explore product-discretized geometric refinements.
4. Only then move toward `S6` or `S3 x S6`.
5. Keep the historical negative control, positive control, and `S2 x graph`
   bridge visible when interpreting the new `S2 x S1` full baseline.

## S1 Discretization Robustness Quick Comparison

This follow-up checks whether the current toy `S2 x S1` bridge depends strongly
on the `spectral_circle` construction or survives first alternative `S1`
families.

Verified command:

```powershell
python scripts/s2_s1_discretization_comparison.py --quick --include-wilson
```

Run:

```text
reports/RUNS/20260512-185254_s1_discretization_comparison_quick
```

Quick comparison status:

- Baseline preserved: `v0.1.13-mvp-s2-s1-product-full`
- `comparison_classification=robust_across_discretizations`
- `reference_family=spectral_circle`
- `all_families_match_reference=True`
- `all_families_pass_basic_gates=True`
- Compared families: `spectral_circle`, `ring`, `wilson_ring`
- `spectral_circle`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=72`
- `ring`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=72`
- `wilson_ring`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=72`
- `pytest -q: 100 passed` (snapshot when this run was recorded; current suite: **132 passed**, `reports/VALIDATION_STATUS.md`)

Per-family gate summary:

- `spectral_circle`: `q_control_passed=True`, `pbc_gate_passed=True`,
  `apbc_gate_passed=True`, `flux_response_observed=True`,
  `s1_not_spectator=True`, `localization_gate_passed=True`,
  `threshold_stable=True`
- `ring`: `q_control_passed=True`, `pbc_gate_passed=True`,
  `apbc_gate_passed=True`, `flux_response_observed=True`,
  `s1_not_spectator=True`, `localization_gate_passed=True`,
  `threshold_stable=True`
- `wilson_ring`: `q_control_passed=True`, `pbc_gate_passed=True`,
  `apbc_gate_passed=True`, `flux_response_observed=True`,
  `s1_not_spectator=True`, `localization_gate_passed=True`,
  `threshold_stable=True`

Saved artifacts:

- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/config.json`
- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/metrics.json`
- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/data.npz`
- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/summary.md`
- `reports/RUNS/20260512-185254_s1_discretization_comparison_quick/figures/`

Interpretation:

This is a discretization-robustness test, not a new product-geometry claim. On
the current quick comparison profile, both alternative families, `ring` and
`wilson_ring`, match the reference `spectral_circle` benchmark-level conclusion
and preserve all basic gates.

Explicit non-claims:

- no continuum compactification;
- no `S6` / `S3 x S6`;
- no Standard Model derivation;
- no physical chirality proof;
- no Witten/Lichnerowicz bypass.

Full comparison follow-up:

```powershell
python scripts/s2_s1_discretization_comparison.py --full --include-wilson
```

Run:

```text
reports/RUNS/20260512-191838_s1_discretization_comparison_full
```

Full comparison status:

- Baseline preserved: `v0.1.13-mvp-s2-s1-product-full`
- Promotion to `v0.1.14-mvp-s2-s1-discretization-robustness-full`: not made
- `comparison_classification=mixed_or_limiting`
- `reference_family=spectral_circle`
- `all_families_match_reference=False`
- `all_families_pass_basic_gates=False`
- Compared families: `spectral_circle`, `ring`, `wilson_ring`
- `spectral_circle`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=6750`
- `ring`: `classification=partial_or_ambiguous`,
  `all_basic_gates_passed=False`, `total_observations=6750`
- `wilson_ring`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=6750`

Per-family gate summary:

- `spectral_circle`: `q_control_passed=True`, `pbc_gate_passed=True`,
  `apbc_gate_passed=True`, `flux_response_observed=True`,
  `s1_not_spectator=True`, `localization_gate_passed=True`,
  `threshold_stable=True`
- `ring`: `q_control_passed=True`, `pbc_gate_passed=True`,
  `apbc_gate_passed=True`, `flux_response_observed=True`,
  `s1_not_spectator=True`, `localization_gate_passed=False`,
  `threshold_stable=True`
- `wilson_ring`: `q_control_passed=True`, `pbc_gate_passed=True`,
  `apbc_gate_passed=True`, `flux_response_observed=True`,
  `s1_not_spectator=True`, `localization_gate_passed=True`,
  `threshold_stable=True`

Saved artifacts:

- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/config.json`
- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/metrics.json`
- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/data.npz`
- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/summary.md`
- `reports/RUNS/20260512-191838_s1_discretization_comparison_full/figures/`

Interpretation:

This is a mixed discretization-robustness result, not a new baseline. The full
profile stays clean for `spectral_circle` and `wilson_ring`, but `ring` loses
the localization gate while preserving the rest of the benchmark checks. The
safest classification is full-profile discretization sensitivity in the current
toy `S2 x S1` benchmark, not continuum compactification and not a physical
chirality result.

Next diagnostic step:

```powershell
python scripts/s2_s1_product.py --full
```

with targeted follow-up on the `ring` family to localize why
`localization_gate_passed` fails under the full comparison grid.
