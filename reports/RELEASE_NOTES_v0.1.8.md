# Release Notes — v0.1.8-mvp-dirac-localization-full

## Summary

This release promotes the toy Dirac/geometric localization benchmark from
quick mode to the configured full run. The benchmark applies the calibrated
r-statistics and IPR diagnostics to finite chiral block toy operators:

```text
D = [[0, A], [A^dagger, 0]]
```

The run covers `clean`, `random_mass`, `gauge_phase`, and `geometric_weight`
modes.

## New in this release

- Full toy Dirac/geometric localization run.
- Full-mode coverage of the `clean` reference mode.
- Updated spectral and validation reports.
- Updated scientific issue wording for near-zero modes.
- Baseline promoted to `v0.1.8-mvp-dirac-localization-full`.

## Verified full results

Command:

```powershell
python scripts/dirac_localization_benchmark.py --full
```

Run directory:

```text
reports/RUNS/20260512-130351_dirac_localization_full
```

Key flags:

| Metric | Value |
| --- | --- |
| `all_symmetry_checks_passed` | `True` |
| `any_near_zero_modes` | `True` |
| `pytest -q` | `49 passed` |

Final `size=96` mode assessment:

| mode | weak W | strong W | weak IPR | strong IPR | weak `<r>` | strong `<r>` | IPR increases | r toward Poisson | near-zero signal |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| clean | 0 | 8 | 0.0104167 | 0.0104167 | 0.9259 | 0.9259 | False | False | True |
| gauge_phase | 0 | 8 | 0.0104167 | 0.00520833 | 0.9259 | 0.3329 | False | True | True |
| geometric_weight | 0 | 8 | 0.0104167 | 0.135186 | 0.9259 | 0.3798 | True | True | True |
| random_mass | 0 | 8 | 0.0104167 | 0.315382 | 0.9259 | 0.3785 | True | True | True |

Artifacts:

- `reports/RUNS/20260512-130351_dirac_localization_full/config.json`
- `reports/RUNS/20260512-130351_dirac_localization_full/metrics.json`
- `reports/RUNS/20260512-130351_dirac_localization_full/data.npz`
- `reports/RUNS/20260512-130351_dirac_localization_full/summary.md`
- `reports/RUNS/20260512-130351_dirac_localization_full/figures/dirac_spectrum.png`
- `reports/RUNS/20260512-130351_dirac_localization_full/figures/dirac_ipr_vs_disorder.png`
- `reports/RUNS/20260512-130351_dirac_localization_full/figures/dirac_r_statistics.png`
- `reports/RUNS/20260512-130351_dirac_localization_full/figures/dirac_near_zero_count.png`

## Scientific meaning

The full run preserves the quick-mode qualitative pattern:

- `clean` remains a no-localization reference.
- `random_mass` and `geometric_weight` show near-zero IPR growth and
  r-statistics movement toward Poisson.
- `gauge_phase` shows r-statistics movement toward Poisson, but near-zero IPR
  does not increase.
- `+-lambda` spectral symmetry passes across the configured benchmark.

This strengthens the bridge between calibrated Anderson-style localization
diagnostics and finite toy Dirac-like/geometric operators.

## Scientific non-claims

This release does not prove:

- physical chirality;
- protected zero modes;
- Witten/Lichnerowicz no-go bypass;
- covariant compactification;
- Standard Model fermions;
- `SU(3) x SU(2) x U(1)` derivation.

Near-zero modes remain numerical signals only unless protected by a separate
index/chirality diagnostic.

## Known limitations

- Finite toy operator, not a continuum Dirac operator.
- No chirality/index protection check inside this localization benchmark.
- Near-zero modes may be accidental.
- `gauge_phase` does not increase near-zero IPR in the configured full run.
- No direct compactification geometry has been validated by this benchmark.

## Next recommended action

Primary:

Add chirality/index diagnostics to the toy Dirac localization pipeline to
separate accidental near-zero modes from protected/index-controlled modes.

Secondary:

Connect the toy Dirac localization pipeline to less artificial geometric
operators and compare against the verified `S2` Dirac monopole index control.
