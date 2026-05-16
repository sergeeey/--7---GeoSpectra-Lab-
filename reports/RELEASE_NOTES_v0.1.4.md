# Release Notes — v0.1.4-mvp-anderson3d-quick

## Summary

This release adds a 3D cubic Anderson benchmark to replace the weak 1D quick
smoke as the next localization diagnostic. It uses the already validated
`mean_adjacent_gap_ratio` and IPR implementations.

## New In This Release

- Added `cc_toy_lab/spectral/anderson_3d.py`.
- Added `scripts/anderson_3d_benchmark.py`.
- Added `tests/test_anderson_3d.py`.
- Updated `reports/SPECTRAL_REPORT.md`.
- Updated `reports/VALIDATION_STATUS.md`.
- Updated `reports/NULL_RESULTS.md`.
- Updated `README.md`.

## Model

```text
H_ij = epsilon_i delta_ij + t * nearest_neighbor_terms
epsilon_i ~ Uniform[-W/2, W/2]
```

Default boundary condition: open.

## Verified Metrics

Verified command:

```powershell
python scripts/anderson_3d_benchmark.py --quick
```

Run directory:

```text
reports/RUNS/20260511-231240_anderson_3d_benchmark_quick
```

Final-size `L=6` quick results:

| W | `<r>` | stderr_r | mean IPR | stderr_ipr |
| ---: | ---: | ---: | ---: | ---: |
| 1 | `0.4755` | `0.0130` | `0.0142385` | `0.00021` |
| 4 | `0.4880` | `0.0299` | `0.0156784` | `0.00023` |
| 8 | `0.5695` | `0.0082` | `0.0328376` | `0.0009` |
| 12 | `0.4930` | `0.0120` | `0.0718543` | `0.01` |
| 16 | `0.4666` | `0.0235` | `0.145835` | `0.0029` |
| 24 | `0.4334` | `0.0171` | `0.315832` | `0.024` |

Basic quick checks passed:

- Weak reference `W=4` is closer to GOE than Poisson.
- Strong reference `W=24` moved toward Poisson relative to weak reference.
- IPR increased from weak to strong disorder.

Test suite:

```text
36 passed in 6.07s
```

Saved artifacts:

- `reports/RUNS/20260511-231240_anderson_3d_benchmark_quick/config.json`
- `reports/RUNS/20260511-231240_anderson_3d_benchmark_quick/metrics.json`
- `reports/RUNS/20260511-231240_anderson_3d_benchmark_quick/data.npz`
- `reports/RUNS/20260511-231240_anderson_3d_benchmark_quick/summary.md`
- `reports/RUNS/20260511-231240_anderson_3d_benchmark_quick/figures/anderson_3d_r_statistics.png`
- `reports/RUNS/20260511-231240_anderson_3d_benchmark_quick/figures/anderson_3d_ipr.png`

## Scientific Meaning

The benchmark now shows more plausible weak-to-strong disorder behavior than
the previous 1D quick smoke:

- `W=4` is closer to GOE than Poisson.
- `W=24` moves toward Poisson relative to the weak reference.
- IPR increases with disorder.

## Scientific Non-Claims

- This is not full Anderson localization validation.
- This does not prove localization in the target physical model.
- This is not chirality.
- This does not bypass Witten/Lichnerowicz no-go theorems.
- This does not validate covariant compactification.
- This does not derive the Standard Model gauge group.

The old Anderson quick null-result remains preserved:

```text
W=0.5, <r>=0.2631
```

## Known Limitations

- Small lattices.
- Few realizations.
- Open boundary conditions are the default.
- Periodic-vs-open comparison is not yet complete.
- Full finite-size scaling has not been run.
- Spectrum-window diagnostics are still needed.

## Next Recommended Action

Primary:

1. Run full 3D Anderson finite-size scaling.

Secondary:

2. Add spectrum-window diagnostics.
3. Test periodic versus open boundary conditions.
4. Increase lattice size `L`, number of seeds, and W-grid resolution.
5. Then connect localization diagnostics to toy Dirac or geometric operators.

