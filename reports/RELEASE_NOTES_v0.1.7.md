# Release Notes — v0.1.7-mvp-dirac-localization-quick

## Summary

This release connects the calibrated localization diagnostics to finite
toy Dirac-like/geometric operators. It is the first bridge from the Anderson
benchmark pipeline toward Dirac-style operators, while still preserving all
scientific non-claims.

## New in This Release

- `cc_toy_lab/spectral/dirac_localization.py`
- `scripts/dirac_localization_benchmark.py`
- `tests/test_dirac_localization.py`
- Quick-mode run artifacts for toy Dirac/geometric localization.
- Documentation updates in `README.md`, `reports/SPECTRAL_REPORT.md`,
  `reports/VALIDATION_STATUS.md`, and `reports/ISSUES_SCIENTIFIC.md`.

Toy operator:

```text
D = [[0, A],
     [A^dagger, 0]]
```

Supported modes:

- `clean`
- `random_mass`
- `gauge_phase`
- `geometric_weight`

## Verified Quick Results

Command:

```powershell
python scripts/dirac_localization_benchmark.py --quick
```

Run path:

```text
reports/RUNS/20260512-095213_dirac_localization_quick
```

Key flags:

| Metric | Value |
| --- | --- |
| `all_symmetry_checks_passed` | `True` |
| `any_near_zero_modes` | `True` |
| `pytest tests/test_dirac_localization.py -q` | `4 passed` |
| `pytest -q` | `49 passed in 10.27s` |

Mode assessment at final `size=48`:

| mode | weak W | strong W | weak IPR | strong IPR | weak `<r>` | strong `<r>` | IPR increases | r toward Poisson | near-zero signal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| clean | 0 | 8 | `0.0208333` | `0.0208333` | `0.8757` | `0.8757` | False | False | True |
| gauge_phase | 0 | 8 | `0.0208333` | `0.0104167` | `0.8757` | `0.3209` | False | True | True |
| geometric_weight | 0 | 8 | `0.0208333` | `0.147943` | `0.8757` | `0.3670` | True | True | True |
| random_mass | 0 | 8 | `0.0208333` | `0.29009` | `0.8757` | `0.3993` | True | True | True |

Artifacts:

- `reports/RUNS/20260512-095213_dirac_localization_quick/config.json`
- `reports/RUNS/20260512-095213_dirac_localization_quick/metrics.json`
- `reports/RUNS/20260512-095213_dirac_localization_quick/data.npz`
- `reports/RUNS/20260512-095213_dirac_localization_quick/summary.md`
- `reports/RUNS/20260512-095213_dirac_localization_quick/figures/dirac_spectrum.png`
- `reports/RUNS/20260512-095213_dirac_localization_quick/figures/dirac_ipr_vs_disorder.png`
- `reports/RUNS/20260512-095213_dirac_localization_quick/figures/dirac_r_statistics.png`
- `reports/RUNS/20260512-095213_dirac_localization_quick/figures/dirac_near_zero_count.png`

## Scientific Meaning

The release validates that the existing localization-measurement pipeline can be
applied to finite toy Dirac-like/geometric operators while preserving the
required `+-lambda` spectral symmetry. In quick mode:

- `random_mass` and `geometric_weight` show both near-zero IPR growth and
  r-statistics movement toward Poisson.
- `gauge_phase` shows r-statistics movement toward Poisson, but no near-zero
  IPR increase.
- `clean` preserves exact near-zero modes and does not show a localization
  trend.

## Scientific Non-Claims

- This does not prove physical chirality.
- This does not prove protected zero modes.
- This does not bypass Witten/Lichnerowicz no-go theorems.
- This does not validate covariant compactification.
- This does not derive Standard Model fermions.
- Near-zero modes are numerical signals only unless protected by an
  index/chirality check.

## Known Limitations

- Quick mode only.
- Finite toy operator only.
- No chirality/index protection check in this benchmark.
- Near-zero modes may be accidental.
- No direct geometric manifold operator has been validated yet.
- Full-mode scaling is pending.

## Next Recommended Action

Primary:

1. Run `python scripts/dirac_localization_benchmark.py --full`.

Secondary:

2. Add chirality/index diagnostics to distinguish accidental near-zero modes
   from protected modes.
3. Compare localization with and without geometric/gauge disorder.
4. Connect the toy Dirac operator to sphere, graph, or other geometric
   operators.
