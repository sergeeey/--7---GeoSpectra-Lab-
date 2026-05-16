# Anomaly Resolution — quantile_0.5 Spectrum Window

## Summary

During full spectrum-window diagnostics, the `quantile_0.5` window failed the
implemented basic localization diagnostic while seven of eight windows passed.

Targeted follow-up diagnostics suggest the failure was likely a
statistical/finite-size/seed-count effect rather than a stable contradiction of
the localization diagnostic. In the targeted rerun, `quantile_0.5` becomes
Poisson-like at `W=24` and remains Poisson-like for stronger disorder values.

Historical promotion baseline at the time remained:

```text
v0.1.6-mvp-spectrum-window-quick
```

The baseline is not promoted because boundary comparison, larger scaling, and
target physical model validation are still pending.

## Original Anomaly

Original full spectrum-window run:

```text
reports/RUNS/20260512-090919_anderson_3d_spectrum_windows_full
```

Problem window:

```text
quantile_0.5
```

Original metrics:

| metric | value |
| --- | ---: |
| weak `<r>` | `0.5363` |
| strong `<r>` | `0.4601` |
| weak IPR | `0.00994604` |
| strong IPR | `0.29276` |
| passed | `False` |

Pass/fail criterion:

1. Weak disorder must be closer to GOE than Poisson.
2. Strong disorder must be closer to Poisson than the weak reference and closer
   to Poisson than GOE.
3. IPR must increase from weak to strong disorder.

The original failure happened because strong-disorder `<r>=0.4601` remained
slightly closer to GOE than Poisson under the implemented check, despite strong
IPR growth.

The historical 1D Anderson quick null-result remains preserved elsewhere:

```text
W=0.5, <r>=0.2631
```

## Diagnostic Method

Targeted diagnostic command:

```powershell
python scripts/anderson_3d_window_failure_diagnostics.py
```

Targeted diagnostic run:

```text
reports/RUNS/20260512-091720_anderson_quantile05_diagnostics
```

Configuration:

| parameter | value |
| --- | --- |
| lattice sizes | `L = 6, 7, 8` |
| disorder values | `W = [20, 24, 28, 32, 36]` |
| windows | `center`, `quantile_0.5` |
| realizations | `10` |
| boundary condition | open |

Saved artifacts:

- `reports/RUNS/20260512-091720_anderson_quantile05_diagnostics/config.json`
- `reports/RUNS/20260512-091720_anderson_quantile05_diagnostics/metrics.json`
- `reports/RUNS/20260512-091720_anderson_quantile05_diagnostics/data.npz`
- `reports/RUNS/20260512-091720_anderson_quantile05_diagnostics/summary.md`
- `reports/RUNS/20260512-091720_anderson_quantile05_diagnostics/figures/r_vs_w_quantile05.png`
- `reports/RUNS/20260512-091720_anderson_quantile05_diagnostics/figures/ipr_vs_w_quantile05.png`
- `reports/RUNS/20260512-091720_anderson_quantile05_diagnostics/figures/r_histograms_w24_w32.png`

## Diagnostic Results

Classification:

```text
likely statistical / finite-size / seed-count effect
```

Final `L=8` diagnostic summary:

| W | center `<r>` | q0.5 `<r>` | center IPR | q0.5 IPR | q0.5 closer to Poisson |
| ---: | ---: | ---: | ---: | ---: | --- |
| 20 | `0.4484` | `0.4531` | `0.206944` | `0.203311` | True |
| 24 | `0.4106` | `0.4127` | `0.289352` | `0.287083` | True |
| 28 | `0.4052` | `0.4052` | `0.346512` | `0.347418` | True |
| 32 | `0.3976` | `0.3981` | `0.439372` | `0.437972` | True |
| 36 | `0.4029` | `0.3973` | `0.486625` | `0.480156` | True |

## Interpretation

The `quantile_0.5` window becomes Poisson-like in the targeted rerun, including
at `W=24`.

IPR increases consistently across the tested disorder range. The original
anomaly is therefore likely not a stable contradiction of the localization
diagnostic.

Safest current classification:

```text
likely statistical / finite-size / seed-count effect
```

This does not erase the original full-run mixed result. It narrows the likely
cause and identifies what should be tested next.

## Remaining Uncertainties

- The targeted run used open boundaries only.
- Maximum tested lattice size is still limited.
- Realization count is improved but still finite.
- Periodic boundary conditions have not been tested.
- Larger scaling remains pending.
- Window-width sensitivity for `quantile_0.5` remains pending.
- Target physical model localization has not been tested.

## Scientific Non-Claims

- This does not prove target-model localization.
- This does not prove chirality.
- This does not validate covariant compactification.
- This does not bypass Witten/Lichnerowicz no-go theorems.
- This does not derive Standard Model physics.
- This does not validate `SU(3) x SU(2) x U(1)`.

## Next Recommended Action

Primary:

1. Run open-vs-periodic boundary comparison for spectrum-window diagnostics.

Secondary:

2. Increase `L` and seed count for spectrum-window diagnostics.
3. Test `quantile_0.5` window-width sensitivity.
4. Check dense/sparse eigensolver consistency before stronger localization
   claims.
