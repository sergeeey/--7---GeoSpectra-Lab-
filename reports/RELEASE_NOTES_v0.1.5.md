# Release Notes — v0.1.5-mvp-anderson3d-full-scaling

## Summary

This release runs the configured full 3D cubic Anderson benchmark. It upgrades
the localization diagnostic beyond the quick 3D run while keeping the scientific
scope limited: this is benchmark evidence, not proof of localization in a target
physical model.

## New In This Release

- Ran `python scripts/anderson_3d_benchmark.py --full`.
- Verified the configured full benchmark for `L = 4, 5, 6, 7`.
- Used eight disorder values and eight realizations per point.
- Updated `reports/SPECTRAL_REPORT.md`.
- Updated `reports/VALIDATION_STATUS.md`.
- Updated `reports/NULL_RESULTS.md`.
- Updated `README.md`.
- Fixed full-mode report wording so it no longer describes the full run as
  quick results.

## Verified Metrics

Verified command:

```powershell
python scripts/anderson_3d_benchmark.py --full
```

Run directory:

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
- Strong reference `W=24` is close to Poisson relative to the weak reference.
- IPR increased from weak to strong disorder.

Test suite:

```text
36 passed in 6.53s
```

Saved artifacts:

- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/config.json`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/metrics.json`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/data.npz`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/summary.md`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/figures/anderson_3d_r_statistics.png`
- `reports/RUNS/20260511-232546_anderson_3d_benchmark_full/figures/anderson_3d_ipr.png`

## Scientific Meaning

The configured full 3D Anderson benchmark shows a plausible weak-to-strong
disorder pattern: r-statistics are closer to GOE at weak reference disorder,
move toward Poisson at strong disorder, and IPR increases with disorder.

## Scientific Non-Claims

- This is not proof of localization in the target physical model.
- This is not chirality.
- This does not bypass Witten/Lichnerowicz no-go theorems.
- This does not validate covariant compactification.
- This does not derive the Standard Model gauge group.

The old 1D Anderson quick null-result remains preserved:

```text
W=0.5, <r>=0.2631
```

## Known Limitations

- Lattices remain small.
- Eight realizations per point is still limited.
- Open boundary conditions are the default.
- Periodic-vs-open comparison is not complete.
- Spectrum-window diagnostics are still needed.
- Larger `L`, more seeds, and finer W-grid are needed before stronger physics
  claims.

## Next Recommended Action

1. Add spectrum-window diagnostics.
2. Compare open and periodic boundary conditions.
3. Increase `L`, seed count, and W-grid resolution.
4. Test mobility-edge behavior across spectral windows.
5. Only then connect localization diagnostics to toy Dirac or geometric
   operators.
