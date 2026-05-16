# Anomaly Resolution — Periodic Boundary Follow-up

## Summary

The previous open-vs-periodic boundary comparison showed that open boundary
conditions passed the configured 3D Anderson localization diagnostic, while
periodic boundary conditions failed it for both `center` and `quantile_0.5`
windows.

The targeted follow-up indicates that the periodic-boundary failure is likely
caused by using `W=24` as the strong-disorder reference in a finite-size
periodic setup. With stronger disorder, `W>=32`, periodic-boundary windows
become Poisson-like and IPR continues to rise strongly.

Historical promotion baseline at the time remained:

```text
v0.1.6-mvp-spectrum-window-quick
```

The baseline is not promoted because this is still Anderson benchmark diagnosis
only. Target-model localization is not validated, no toy Dirac/geometric
operator has been connected to this diagnostic, and larger scaling remains
useful.

## Original Boundary Anomaly

Original open-vs-periodic boundary comparison:

```text
reports/RUNS/20260512-093014_anderson_3d_boundary_comparison
```

Final `L=7` assessment:

| boundary | window | status |
| --- | --- | --- |
| open | center | passed |
| open | quantile_0.5 | passed |
| periodic | center | failed |
| periodic | quantile_0.5 | failed |

Original summary flags:

| flag | value |
| --- | --- |
| `all_boundary_basic_checks_passed` | `False` |
| `boundary_changes_basic_diagnostic` | `True` |
| `max_abs_delta_r` | `0.0804` |
| `max_abs_delta_ipr` | `0.116229` |

The historical 1D Anderson quick null-result remains preserved elsewhere:

```text
W=0.5, <r>=0.2631
```

## Follow-up Method

Command:

```powershell
python scripts/anderson_3d_periodic_followup.py
```

Follow-up run:

```text
reports/RUNS/20260512-094128_anderson_periodic_followup
```

Configuration:

| parameter | value |
| --- | --- |
| boundary | periodic |
| periodic lattice sizes | `L = 6, 7, 8` |
| disorder values | `W = [16, 20, 24, 28, 32, 36, 40]` |
| windows | `center`, `quantile_0.5` |
| realizations | `10` |
| seed | `6262` |
| strong-disorder check threshold | `W>=32` |
| open reference | enabled at `L=8`, `6` realizations |

Saved artifacts:

- `reports/RUNS/20260512-094128_anderson_periodic_followup/config.json`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/metrics.json`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/data.npz`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/summary.md`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/figures/periodic_r_vs_w.png`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/figures/periodic_ipr_vs_w.png`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/figures/periodic_distance_to_poisson_goe.png`
- `reports/RUNS/20260512-094128_anderson_periodic_followup/figures/periodic_open_comparison_optional.png`

## Follow-up Result

Classification:

```text
likely insufficient disorder range at W=24 with finite-size/seed-count sensitivity
```

Verified flags:

| flag | value |
| --- | --- |
| `stronger_disorder_makes_periodic_poisson_like` | `True` |
| `ipr_mostly_monotonic_all` | `True` |
| `spectrum_window_artifact_suspected` | `False` |

Final `L=8` periodic behavior:

| W | center `<r>` | q0.5 `<r>` | center IPR | q0.5 IPR | center closer to Poisson | q0.5 closer to Poisson |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 16 | `0.5076` | `0.4974` | `0.0542513` | `0.0522911` | False | False |
| 20 | `0.4849` | `0.4729` | `0.107141` | `0.108756` | False | False |
| 24 | `0.4567` | `0.4590` | `0.194963` | `0.193183` | True | False |
| 28 | `0.4221` | `0.4274` | `0.267112` | `0.269099` | True | True |
| 32 | `0.4275` | `0.4473` | `0.33069` | `0.329627` | True | True |
| 36 | `0.4009` | `0.4106` | `0.418799` | `0.424562` | True | True |
| 40 | `0.4037` | `0.4150` | `0.435981` | `0.438452` | True | True |

Assessment across `L=6, 7, 8`:

| L | window | `W=24` `<r>` | `W=32` `<r>` | max W | max W `<r>` | `W>=32` all Poisson-like | IPR mostly monotonic | resolved |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 6 | center | `0.4592` | `0.4257` | 40 | `0.4062` | True | True | True |
| 6 | quantile_0.5 | `0.4856` | `0.4307` | 40 | `0.4209` | True | True | True |
| 7 | center | `0.4704` | `0.4194` | 40 | `0.4310` | True | True | True |
| 7 | quantile_0.5 | `0.4500` | `0.4193` | 40 | `0.4431` | True | True | True |
| 8 | center | `0.4567` | `0.4275` | 40 | `0.4037` | True | True | True |
| 8 | quantile_0.5 | `0.4590` | `0.4473` | 40 | `0.4150` | True | True | True |

## Interpretation

Periodic boundaries become Poisson-like when stronger disorder `W>=32` is used.
IPR increases strongly across the tested disorder range.

The earlier periodic-boundary failure is therefore likely a
parameter-range/finite-size/seed-count sensitivity rather than a stable
contradiction of the localization diagnostic. In the original comparison,
`W=24` was too weak a strong-disorder reference for the finite-size periodic
setup, especially for the `quantile_0.5` window.

This follow-up updates the boundary-condition limitation; it does not erase the
previous failed open-vs-periodic comparison.

## Remaining Limitations

- Lattice sizes remain finite.
- Seed count remains finite.
- The result is still an Anderson benchmark diagnostic only.
- No target physical operator has been tested.
- Localization diagnostics have not yet been connected to toy Dirac or
  geometric operators.
- No Standard Model representation, hypercharge, or anomaly checks exist.
- No physical chirality claim follows from this benchmark.

## Scientific Non-Claims

- This does not prove covariant compactification.
- This does not prove physical localization in the target model.
- This does not prove chirality.
- This does not bypass Witten/Lichnerowicz no-go theorems.
- This does not derive `SU(3) x SU(2) x U(1)`.
- This does not validate Standard Model physics.

## Next Recommended Action

Primary:

1. Connect localization diagnostics to toy Dirac/geometric operators.

Secondary:

2. Run larger `L` and seed scaling if compute budget allows.
3. Repeat open-reference matching at the same resolution for periodic follow-up.
4. Test mobility-edge-style behavior across more spectral windows.
5. Check dense/sparse eigensolver consistency before stronger benchmark claims.
