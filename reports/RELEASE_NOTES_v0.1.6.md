# Release Notes - v0.1.6-mvp-spectrum-window-quick

## Summary

This release adds spectrum-window diagnostics for the 3D Anderson benchmark and
verifies quick mode.

The goal is to test whether the basic Anderson localization diagnostic depends
on the spectral region used for r-statistics and IPR. In quick mode, center,
lower-band, and upper-band windows agree with the basic localization diagnostic.

## New In This Release

- Added `cc_toy_lab/spectral/anderson_windows.py`.
- Added `scripts/anderson_3d_spectrum_windows.py`.
- Added `tests/test_anderson_windows.py`.
- Added quick and full CLI modes:
  - `python scripts/anderson_3d_spectrum_windows.py --quick`
  - `python scripts/anderson_3d_spectrum_windows.py --full`
- Ran and verified quick-mode spectrum-window diagnostics.
- Updated README, spectral report, validation status, and null-result context.

## Verified Metrics

Verified command:

```powershell
python scripts/anderson_3d_spectrum_windows.py --quick
```

Run directory:

```text
reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick
```

Quick result summary:

- `all_windows_basic_checks_passed=True`
- `window_choice_changes_conclusion=False`
- Window choice did not change the basic localization diagnostic in this run.

Final `L=6` window assessment:

| window | weak `<r>` | strong `<r>` | weak IPR | strong IPR | passed |
| --- | ---: | ---: | ---: | ---: | --- |
| center | `0.5187` | `0.4280` | `0.0158342` | `0.344868` | True |
| lower | `0.5357` | `0.4181` | `0.0190603` | `0.434601` | True |
| upper | `0.5808` | `0.3960` | `0.0204236` | `0.344342` | True |

Test suite:

```text
40 passed in 4.85s
```

Saved artifacts:

- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/config.json`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/metrics.json`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/data.npz`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/summary.md`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/figures/r_by_window.png`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/figures/ipr_by_window.png`
- `reports/RUNS/20260512-081650_anderson_3d_spectrum_windows_quick/figures/window_comparison_heatmap.png`

## Scientific Meaning

The quick run suggests that center, lower, and upper spectral windows agree
with the basic 3D Anderson localization diagnostic. This reduces the specific
concern that the previous configured 3D Anderson result was only a center-window
artifact.

The historical 1D Anderson quick null-result remains preserved:

```text
W=0.5, <r>=0.2631
```

## Scientific Non-Claims

- This does not prove target physical localization.
- This does not prove chirality.
- This does not bypass Witten/Lichnerowicz no-go theorems.
- This does not validate covariant compactification.
- This does not derive Standard Model fermions or the gauge group
  `SU(3) x SU(2) x U(1)`.

## Known Limitations

- Full spectrum-window mode has not been run.
- Quantile windows are pending.
- The quick run uses limited `L` and seed count.
- Open-vs-periodic boundary comparison has not been run.
- Mobility-edge-style analysis has not been run.
- This remains benchmark validation, not target physical model validation.

## Next Recommended Action

Primary:

1. Run spectrum-window diagnostics in full mode.

Secondary:

2. Compare open and periodic boundary conditions.
3. Increase `L`, seed count, and W-grid resolution.
4. Run mobility-edge-style analysis across spectral windows.
5. Connect localization diagnostics to toy Dirac or geometric operators only
   after benchmark diagnostics remain stable.
