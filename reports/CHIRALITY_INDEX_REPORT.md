# S² Dirac Monopole Index Test

## Purpose

This report records the first chirality-related control test in GeoSpectra Lab.
The goal is to verify that the code can reproduce a known index-theorem toy
result before any chirality-related claims are made elsewhere in the project.

## Mathematical Background

For a Dirac operator on `S2` coupled to a `U(1)` magnetic monopole of charge
`q`, the continuum index theorem predicts an index proportional to the monopole
charge. The convention implemented here is:

```text
q > 0 has positive-chirality zero modes
q < 0 has negative-chirality zero modes
Index(D) = n_plus - n_minus = q
```

## Numerical Implementation

This is a finite-mode spectral toy control, not a continuum lattice
discretization. It builds a chiral block operator `D = [[0, A^T], [A, 0]]`
with chirality operator `Gamma = diag(+1, -1)`. The nonzero finite-mode spectrum
is paired as `±lambda`, while `|q|` exact zero modes are assigned to the
chirality selected by the sign of `q`.

The nonzero toy levels use:

```text
lambda_n = sqrt(n * (n + |q|)) / R
degeneracy_n = 2n + |q|
n = 1, ..., cutoff
```

Zero-mode tolerance: `1e-08`.

## q Values Tested

Mode: `quick`

```text
q_values = (0, 1, 2)
cutoffs = (1, 2, 3)
```

Run directory:

```text
reports\RUNS\20260512-140230_dirac_monopole_s2_quick
```

## Index Results

| q | cutoff | expected index | numerical index | n_plus | n_minus | zero modes | passed |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 1 | 0 | 0 | 0 | 0 | 0 | True |
| 0 | 2 | 0 | 0 | 0 | 0 | 0 | True |
| 0 | 3 | 0 | 0 | 0 | 0 | 0 | True |
| 1 | 1 | 1 | 1 | 1 | 0 | 1 | True |
| 1 | 2 | 1 | 1 | 1 | 0 | 1 | True |
| 1 | 3 | 1 | 1 | 1 | 0 | 1 | True |
| 2 | 1 | 2 | 2 | 2 | 0 | 2 | True |
| 2 | 2 | 2 | 2 | 2 | 0 | 2 | True |
| 2 | 3 | 2 | 2 | 2 | 0 | 2 | True |

Overall status: `passed`.

## Convergence Behavior

The index is checked across the configured finite-mode cutoffs. Passing results
mean that increasing the cutoff did not destroy the index count under this toy
construction.

Historical note: this report records the verified quick control. Full mode has
since also been run and is documented in `reports/VALIDATION_STATUS.md` and
`README.md`.

## Limitations

- This is a finite-mode spectral toy model, not a geometric proof and not a
  full numerical discretization of spinor bundles on `S2`.
- Exact zero modes are built into the control using the known monopole spectral
  structure.
- This validates index-counting infrastructure and chirality bookkeeping only.
- It does not validate the Anderson model, spectral localization physics, or
  covariant compactification.

## What This Validates

- The code can count zero modes by chirality under an explicit convention.
- The numerical index `n_plus - n_minus` tracks monopole charge `q` in this
  known finite-mode toy control.
- The zero-mode tolerance and chirality threshold are documented and
  reproducible.

## What This Does NOT Validate

- It does not prove chiral fermions in covariant compactification.
- It does not bypass Witten/Lichnerowicz no-go theorems.
- It does not derive Standard Model fermions.
- It does not derive `SU(3) x SU(2) x U(1)`.
- It does not validate real cosmology or real extra-dimensional stabilization.

## Next Steps

1. Replace or complement this finite-mode control with a more geometric
   discretization of the `S2` Dirac operator.
2. Only after this index-control layer remains stable, investigate whether any
   project-specific toy Dirac operators have protected zero modes.
