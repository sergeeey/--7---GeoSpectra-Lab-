# Next Experiment Plan — Spectrum-Window Diagnostics

## Purpose

The configured full 3D Anderson benchmark currently reports localization
diagnostics for a selected spectral region. That is not enough for a stronger
scientific interpretation, because localization behavior can depend on where
the eigenstates sit in the spectrum.

The next experiment should test whether the apparent weak-to-strong disorder
behavior is stable across spectral windows:

- band center;
- lower band;
- upper band;
- optional quantile windows that can expose mobility-edge-like behavior.

This plan is only for the next validation experiment. It does not update the
project baseline and does not make a new physics claim.

## Historical Baseline Context

Historical planning baseline: `v0.1.5-mvp-anderson3d-full-scaling`

Already verified:

- Radion toy model verified.
- Synthetic r-statistics controls verified in quick and full modes.
- `S2` Dirac monopole finite-mode index control verified.
- Configured full 3D Anderson benchmark completed.
- `pytest -q` passes with `36 passed`.

Latest full 3D Anderson run:

```text
reports/RUNS/20260511-232546_anderson_3d_benchmark_full
```

Final-size `L=7` results:

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

Known historical null/limiting result:

```text
W=0.5, <r>=0.2631
```

Interpretation at this baseline:

- The full 3D Anderson benchmark behaves more sensibly than the old 1D quick
  smoke.
- The r-statistics implementation itself is already validated by synthetic
  Poisson/GOE/GUE controls.
- Target physical localization is not yet validated.
- Spectrum-window diagnostics are the next required check.

## Scientific Question

Does the GOE-to-Poisson transition and IPR growth depend on the chosen spectral
window?

The experiment should distinguish these possibilities:

- the localization diagnostic is stable across windows;
- only the band center shows the expected trend;
- lower or upper band states localize earlier;
- window choice changes the conclusion enough to require a null or limiting
  result entry.

## Proposed Method

Use the existing 3D cubic Anderson Hamiltonian:

```text
H_ij = epsilon_i delta_ij + t * nearest_neighbor_terms
epsilon_i ~ Uniform[-W/2, W/2]
```

Use the already validated spectral metrics:

- `mean_adjacent_gap_ratio`;
- IPR implementation.

Do not change the r-statistics implementation unless a bug is found and
documented separately.

### Spectral Windows

Define at least these windows:

| Window | Definition | Purpose |
| --- | --- | --- |
| Center window | Eigenvalues closest to `E = 0` | Compare with the current band-center-style diagnostic. |
| Lower-band window | Lower `10-20%` of eigenvalues | Test edge/lower-band localization sensitivity. |
| Upper-band window | Upper `10-20%` of eigenvalues | Check symmetry or asymmetry against the lower band. |
| Optional quantile windows | Quantiles `q in [0.1, 0.3, 0.5, 0.7, 0.9]` | Probe mobility-edge-like behavior. |

For each `L`, `W`, seed, and spectral window, compute:

- `<r>`;
- `stderr_r`;
- mean IPR;
- `stderr_ipr`;
- number of eigenvalues used;
- number of disorder realizations;
- finite-size behavior if possible.

### Window Selection Rules

The implementation should save the exact rule used to choose eigenvalues.
Recommended rules:

- Center window: choose the `k` eigenvalues with smallest `abs(E)`.
- Lower-band window: choose eigenvalues in the lower quantile range, for
  example `0.00-0.20`.
- Upper-band window: choose eigenvalues in the upper quantile range, for
  example `0.80-1.00`.
- Quantile windows: choose narrow windows centered on configured quantiles,
  for example `q +/- 0.05`.

Every run should record:

- whether eigenvalues came from dense diagonalization or sparse solver;
- the spectral window definition;
- the number of levels used after filtering;
- boundary condition;
- seed schedule;
- disorder values;
- lattice sizes.

## Required CLI Design

Proposed future commands:

```powershell
python scripts/anderson_3d_spectrum_windows.py --quick
python scripts/anderson_3d_spectrum_windows.py --full
```

Quick mode:

| Parameter | Proposed value |
| --- | --- |
| Lattice sizes | `L = 5, 6` |
| Disorder values | `W = [4, 8, 12, 16, 24]` |
| Realizations | few seeds, enough for smoke behavior |
| Windows | center, lower band, upper band |
| Boundary condition | open by default |

Full mode:

| Parameter | Proposed value |
| --- | --- |
| Lattice sizes | `L = 5, 6, 7`, maybe `8` if feasible |
| Disorder values | denser W-grid than quick mode |
| Realizations | more seeds per `L/W/window` |
| Windows | center, lower, upper, and quantile windows |
| Boundary condition | open first, periodic comparison in a follow-up or optional flag |

Recommended optional flags:

```powershell
python scripts/anderson_3d_spectrum_windows.py --quick --boundary open
python scripts/anderson_3d_spectrum_windows.py --quick --boundary periodic
python scripts/anderson_3d_spectrum_windows.py --full --windows center,lower,upper,quantiles
```

## Expected Outputs

Each run should write to:

```text
reports/RUNS/<timestamp>_anderson_3d_spectrum_windows_<mode>/
```

Required artifacts:

- `config.json`;
- `metrics.json`;
- `data.npz`;
- `summary.md`;
- `figures/r_by_window.png`;
- `figures/ipr_by_window.png`;
- `figures/window_comparison_heatmap.png`.

Recommended additional artifacts:

- `figures/r_vs_W_by_L_and_window.png`;
- `figures/ipr_vs_W_by_L_and_window.png`;
- `figures/window_level_counts.png`;
- `figures/seed_stability_by_window.png`.

`metrics.json` should include a table-like structure with at least:

| Field | Meaning |
| --- | --- |
| `L` | Lattice size. |
| `W` | Disorder strength. |
| `window_name` | `center`, `lower`, `upper`, or quantile label. |
| `window_definition` | Exact quantile or energy-selection rule. |
| `mean_r` | Mean adjacent gap ratio. |
| `stderr_r` | Standard error of `<r>`. |
| `mean_ipr` | Mean IPR in the window. |
| `stderr_ipr` | Standard error of IPR. |
| `n_levels_used` | Number of eigenvalues used after window filtering. |
| `realizations` | Number of disorder realizations. |
| `boundary` | Open or periodic. |
| `seed_base` | Base seed or seed schedule. |

## Success Criteria

A useful result should show:

- whether the r-statistics transition differs by spectral window;
- whether IPR growth is strongest in specific windows;
- whether strong disorder moves all windows toward Poisson;
- whether center-window behavior is stable across `L`;
- whether the result is stable across seeds;
- whether lower and upper bands behave symmetrically or expose meaningful
  asymmetry.

Minimum quick-mode success:

- center-window `W=4` remains closer to GOE than Poisson;
- center-window `W=24` remains closer to Poisson than the weak reference;
- mean IPR increases from weak to strong disorder in the center window;
- lower and upper windows produce interpretable metrics with enough levels.

Full-mode success:

- the window dependence is quantified, not only visually inspected;
- finite-size behavior is reported by window;
- seed stability is reported by window;
- any window-specific anomaly is logged in `DISCOVERY_LEDGER.md`,
  `NULL_RESULTS.md`, or `ISSUES_SCIENTIFIC.md` as appropriate.

## Failure / Null Criteria

Record the result as null or limiting if:

- window choice radically changes the localization conclusion;
- strong disorder does not move toward Poisson in any window;
- IPR growth is inconsistent or reverses without explanation;
- results depend on one seed;
- results depend strongly on boundary conditions;
- small-`L` artifacts dominate;
- the number of eigenvalues per window is too small for stable r-statistics;
- degeneracies or solver artifacts distort the level-spacing distribution.

Where to record:

- `reports/NULL_RESULTS.md` for failed or limiting hypotheses;
- `reports/ISSUES_SCIENTIFIC.md` for unresolved scientific interpretation
  risks;
- `reports/DISCOVERY_LEDGER.md` for unexpected but reproducible patterns.

## Scientific Interpretation Rules

Spectrum-window diagnostics can strengthen localization evidence in the 3D
Anderson benchmark by showing whether the GOE-to-Poisson and IPR trends are
specific to a spectral region or stable across the spectrum.

They do not prove:

- covariant compactification;
- physical chirality;
- protected chiral zero modes;
- a bypass of Witten/Lichnerowicz no-go theorems;
- Standard Model fermions;
- the gauge group `SU(3) x SU(2) x U(1)`;
- localization in a target compactification model.

Correct interpretation:

```text
The 3D Anderson benchmark shows window-resolved localization diagnostics under
the configured toy Hamiltonian.
```

Incorrect interpretation:

```text
The project has proven physical localization, chirality, or covariant
compactification.
```

## Next Step After This Experiment

If spectrum-window diagnostics pass:

1. Compare open vs periodic boundary conditions.
2. Increase `L` and seed count.
3. Run mobility-edge-style analysis across spectral windows.
4. Connect diagnostics to toy Dirac/geometric operators only after the Anderson
   controls remain stable.

If diagnostics fail:

1. Inspect the eigenvalue solver and dense/sparse consistency.
2. Inspect window selection and level-count thresholds.
3. Inspect degeneracies and near-degeneracies.
4. Inspect finite-size artifacts.
5. Record the result in `NULL_RESULTS.md` and unresolved issues in
   `ISSUES_SCIENTIFIC.md`.

## Implementation Notes For The Future Change

This document is a plan, not an implementation. The future implementation
should be scoped to new experiment code and report updates, probably:

- `cc_toy_lab/spectral/anderson_3d_windows.py`;
- `scripts/anderson_3d_spectrum_windows.py`;
- `tests/test_anderson_3d_windows.py`;
- updates to `reports/SPECTRAL_REPORT.md`;
- updates to `reports/VALIDATION_STATUS.md`;
- updates to `reports/NULL_RESULTS.md` only if a limiting result appears.

Do not change the baseline label until a run is actually implemented and
verified.
