# Release Notes — v0.1.3-mvp-dirac-index-control

## Summary

This release adds the first chirality-related control test to GeoSpectra Lab /
Covariant Compactification Toy Lab: a finite-mode `S2` Dirac monopole index
control. The purpose is to verify the project can count zero modes by chirality
against a known toy index result before making any chirality-related claims in
project-specific models.

## New In This Release

- Added `cc_toy_lab/spectral/dirac_monopole_s2.py`.
- Added `scripts/dirac_monopole_s2.py`.
- Added quick and full CLI modes:
  - `python scripts/dirac_monopole_s2.py --quick`
  - `python scripts/dirac_monopole_s2.py --full`
- Added `tests/test_dirac_monopole_s2.py`.
- Added `reports/CHIRALITY_INDEX_REPORT.md`.
- Updated `reports/VALIDATION_STATUS.md`.
- Updated `README.md`.

## Verified Metrics

Explicit convention:

```text
q > 0 has positive-chirality zero modes
q < 0 has negative-chirality zero modes
index(D) = n_plus - n_minus = q
```

Verified full command:

```powershell
python scripts/dirac_monopole_s2.py --full
```

Latest full run:

```text
reports/RUNS/20260511-230305_dirac_monopole_s2_full
```

Full final-cutoff results:

| q | cutoff | expected index | numerical index | n_plus | n_minus | passed |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| -3 | 5 | -3 | -3 | 0 | 3 | yes |
| -2 | 5 | -2 | -2 | 0 | 2 | yes |
| -1 | 5 | -1 | -1 | 0 | 1 | yes |
| 0 | 5 | 0 | 0 | 0 | 0 | yes |
| 1 | 5 | 1 | 1 | 1 | 0 | yes |
| 2 | 5 | 2 | 2 | 2 | 0 | yes |
| 3 | 5 | 3 | 3 | 3 | 0 | yes |

Test suite:

```text
31 passed in 3.12s
```

Saved artifacts:

- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/config.json`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/metrics.json`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/data.npz`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/summary.md`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/figures/dirac_monopole_s2_eigenvalues.png`
- `reports/RUNS/20260511-230305_dirac_monopole_s2_full/figures/dirac_monopole_s2_index.png`

## Scientific Meaning

The project now has a verified toy index-counting pipeline. In the finite-mode
`S2` monopole control, the numerical index tracks the monopole charge under the
documented convention `index(D) = n_plus - n_minus = q`.

## Scientific Non-Claims

- This does not prove physical chiral fermions in covariant compactification.
- This does not bypass Witten/Lichnerowicz no-go theorems.
- This does not derive Standard Model fermions.
- This does not validate `SU(3) x SU(2) x U(1)`.
- This does not validate real cosmology.
- This does not validate Anderson localization physics.
- Localization and near-zero modes remain insufficient evidence for protected
  chiral zero modes.

The Anderson quick null-result remains preserved:

```text
W = 0.5, <r> = 0.2631
```

## Known Limitations

- The index control is a finite-mode toy model.
- It is not a full continuum proof.
- It is not a geometric discretization of spinor bundles on `S2`.
- It has no Standard Model representations.
- It has no hypercharge assignments.
- It has no anomaly checks.
- It is not connected yet to covariant compactification geometry.

## Next Recommended Action

Primary:

1. Upgrade the Anderson benchmark to a 3D or quasi-dimensional model.

Secondary:

2. Extend index tests to less artificial Dirac discretizations and gauge
   bundles.
3. Add convergence-strengthening tests, heat-kernel checks, or spectral-flow
   checks for the `S2` monopole convention.
4. Connect the index pipeline to deformed or geometric Dirac operators only
   after the control tests remain stable.

