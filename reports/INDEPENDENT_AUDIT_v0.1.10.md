# Independent Audit — v0.1.10 Dirac Chirality Full

## Executive Summary

The current `v0.1.10-mvp-dirac-chirality-full` result was independently
reproduced.

- `pytest -q` passed: `53 passed`.
- `python scripts/dirac_chirality_diagnostic.py --quick` completed and saved the
  expected run artifacts in
  `reports/RUNS/20260512-135933_dirac_chirality_quick`.
- `python scripts/dirac_chirality_diagnostic.py --full` completed and saved the
  expected run artifacts in
  `reports/RUNS/20260512-135933_dirac_chirality_full`.
- The reproduced full run reports:
  - `gamma_algebra_passed=True`
  - `anticommutation_preserved=True`
  - `all_indices_zero=True`
  - `any_near_zero_modes=True`

Main audit conclusion: the reported result is reproducible, mathematically
consistent, and scientifically conservative. However, the present toy block
construction is structurally biased toward zero index because the off-diagonal
block `A` is finite-dimensional and square in every current localization mode.
This means the reproduced zero-index result is best interpreted as a validated
negative control for accidental/paired near-zero modes, not as a candidate
chirality-generating mechanism.

No implementation bug was found in the core chirality/index formulas during
this audit.

## Reproducibility

Commands run during the audit:

```powershell
pytest -q
python scripts/dirac_chirality_diagnostic.py --quick
python scripts/dirac_chirality_diagnostic.py --full
python scripts/dirac_monopole_s2.py --quick
```

Observed command results:

- `pytest -q` -> `53 passed`
- quick chirality diagnostic -> completed successfully, with
  `all_indices_zero=True`
- full chirality diagnostic -> completed successfully, with
  `all_indices_zero=True`
- quick S2 monopole positive control -> completed successfully, with
  `q=1 -> numerical index 1` and `q=2 -> numerical index 2`

Expected chirality artifact files were verified for both fresh quick and fresh
full runs:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/chirality_expectations.png`
- `figures/index_vs_disorder.png`
- `figures/near_zero_chirality_scatter.png`
- `figures/anticommutator_error.png`

Determinism check:

- Re-running the quick configuration twice with the same seed produced identical
  observation tuples and identical summary text.
- The seed schedule is deterministic and encoded directly in the diagnostic
  loops.

Operational caveat:

- The official CLI scripts update living markdown reports unless
  `CC_TOY_LAB_SKIP_REPORT_UPDATE=1` is set.
- This is not a mathematical bug, but it means reproduction runs are not
  side-effect free at the documentation layer.

## Mathematical Audit

### Block construction

In `cc_toy_lab/spectral/dirac_localization.py`, every current mode constructs a
finite matrix `A` and then builds

```text
D = [[0, A],
     [A^dagger, 0]]
```

This guarantees Hermiticity of `D` and algebraic chiral block structure by
construction.

### Gamma operator

In `cc_toy_lab/spectral/dirac_chirality.py`, the chirality operator is

```text
Gamma = diag(+I, -I)
```

for the `2 * size` chiral block space.

### Verified algebraic properties

The implementation and reproduced runs are consistent with the intended
algebra:

- `Gamma^2 = I`
- `Gamma` is Hermitian
- `{D, Gamma} = D Gamma + Gamma D ~= 0`
- the localization benchmark separately checks `+-lambda` spectral symmetry

The quick and full chirality reruns both reported zero anticommutator error at
the printed precision for all audited mode summaries.

### Chirality expectations and index counting

The code computes chirality expectations as the real part of
`<psi|Gamma|psi>`, column-wise over eigenvectors:

```text
chiralities = Re(psi^dagger Gamma psi)
```

Then it restricts index counting to eigenvectors whose eigenvalues satisfy

```text
|lambda| <= near_zero_tol
```

and defines:

```text
n_plus  = count(chirality >= +threshold)
n_minus = count(chirality <= -threshold)
numerical_index = n_plus - n_minus
```

This implementation is internally correct and consistent with the tests in
`tests/test_dirac_chirality.py`.

### Positive control contrast

The positive control in `cc_toy_lab/spectral/dirac_monopole_s2.py` was checked
as well. The quick rerun produced:

- `q=0 -> numerical index 0`
- `q=1 -> numerical index 1`
- `q=2 -> numerical index 2`

This confirms that the index-counting pipeline can detect nonzero index when a
nontrivial chiral imbalance is built into the control model.

## Structural Zero-Index Analysis

This is the central caveat of the current toy localization construction.

### What the code currently does

In every current localization mode (`clean`, `random_mass`, `gauge_phase`,
`geometric_weight`), the off-diagonal block `A` is square:

- `_base_forward_derivative(size)` returns a `size x size` matrix
- `_forward_derivative_with_phases(size, phases)` returns a `size x size` matrix
- `_weighted_forward_derivative(size, weights)` returns a `size x size` matrix
- disorder terms are added as square diagonal matrices

Therefore the full operator always uses equal positive and negative chiral block
dimensions.

### Mathematical consequence

For finite-dimensional square `A`,

```text
index(A) = dim ker(A) - dim ker(A^dagger) = 0
```

because:

- `rank(A) = rank(A^dagger)`
- `dim ker(A) = n - rank(A)`
- `dim ker(A^dagger) = n - rank(A^dagger)`

with the same domain/codomain dimension `n`.

For the block operator

```text
D = [[0, A],
     [A^dagger, 0]]
```

the exact zero modes split into the kernels of `A` and `A^dagger`, so an exact
chiral zero-mode imbalance is not expected in this finite square construction.

### Audit interpretation

Yes: the current toy localization construction is mathematically biased toward
zero index.

This does not mean the current code is wrong. It means the reproduced
`numerical_index = 0` result is not only an empirical observation; it is also
strongly structurally expected from the present construction.

Possible loopholes are limited to numerical/tolerance artifacts, not stable
protected index generation. In other words, the current model may produce:

- exact paired zero modes,
- near-zero modes,
- tolerance-dependent ambiguous cases,

but not a robust nonzero protected index without changing the construction
itself.

This is sharply contrasted by the positive `S2` monopole control, where the
code explicitly uses unequal chiral-sector sizes for nonzero monopole charge and
therefore allows nonzero index.

## Near-Zero Mode Audit

Fresh full rerun outcome:

- No nonzero numerical index appeared anywhere in the configured full grid.
- `clean` mode preserves exact paired zero modes.
- Disorder modes typically remove exact near-zero modes under the default
  tolerance.
- The localization benchmark and the chirality/index diagnostic remain separate:
  stronger localization-style signals do not generate nonzero index in the
  current model.

Classification audit:

- `clean` mode: paired exact zero modes, zero index
- `random_mass`: zero index throughout; exact zeros present only at zero
  disorder
- `gauge_phase`: zero index throughout; exact zeros present only at zero
  disorder
- `geometric_weight`: zero index throughout; exact zeros present only at zero
  disorder

Across the configured full grid, the reproduced classification is:

- exact clean-mode zero modes are paired, not chiral in the index sense
- disorder-induced near-zero/localization behavior is not converted into
  protected nonzero index
- the current toy benchmark behaves as a negative control for accidental or
  paired near-zero structure

No evidence was found for a protected nonzero index under the existing full
configuration.

## Threshold Sensitivity

The full configured chirality grid was re-run with three tolerances:

- `1e-7` (10x smaller than default)
- `1e-6` (default)
- `1e-5` (10x larger than default)

### Aggregate results

| near_zero_tol | all_indices_zero | observations with near-zero modes | total near-zero count | nonzero-index observations | dominant classifications |
| ---: | --- | ---: | ---: | ---: | --- |
| `1e-7` | True | 240 | 480 | 0 | `432 no_exact_near_zero_modes`, `240 paired_accidental_or_symmetry_zero_modes` |
| `1e-6` | True | 240 | 480 | 0 | identical to `1e-7` |
| `1e-5` | True | 245 | 490 | 0 | `427 no_exact_near_zero_modes`, `240 paired_accidental_or_symmetry_zero_modes`, `5 unresolved_ambiguous_chirality` |

### Interpretation

- The numerical index remains zero for all three tolerances.
- The default tolerance is stable under a 10x decrease.
- A 10x increase does not generate nonzero index, but it does admit five
  borderline cases whose eigenvalues are around `6e-6` to `9e-6`.
- Those five cases become `unresolved_ambiguous_chirality`, not
  `potentially_protected_unverified_nonzero_index`.

Ambiguous cases at `1e-5` were limited to:

- `random_mass`, size `48`, disorder `4.0`, three seeds
- `random_mass`, size `96`, disorder `4.0`, one seed
- `geometric_weight`, size `96`, disorder `8.0`, one seed

In all such cases:

- `numerical_index` still remained `0`
- exact-zero chirality expectations were extremely small (`~1e-11` to `~1e-10`)
- the change was tolerance-driven, not evidence of protected chirality

Conclusion: threshold sensitivity can change the classification boundary for a
small number of near-zero states, but it does not overturn the zero-index
result.

## Mode-by-Mode Results

The table below summarizes the reproduced full-grid behavior at final size
(`size=96`) and default tolerance.

| mode | exact near-zero count at weak disorder | exact near-zero count at strong disorder | numerical index (weak -> strong) | chirality behavior | max `{D,Gamma}` error | disorder preserves chiral block structure | localization trend separate from index generation |
| --- | ---: | ---: | --- | --- | ---: | --- | --- |
| `clean` | `2` | `2` | `0 -> 0` | exact zero modes split as `n_plus=1`, `n_minus=1` | `0` | yes | yes; no localization trend and no index generation |
| `random_mass` | `2` | `0` | `0 -> 0` | strong-disorder near-window chirality stays near `0`, not near `+-1` | `0` | yes | yes; localization indicators can grow while index stays zero |
| `gauge_phase` | `2` | `0` | `0 -> 0` | strong-disorder near-window chirality stays near `0` | `0` | yes | yes; r-statistics can move without producing index |
| `geometric_weight` | `2` | `0` | `0 -> 0` | strong-disorder near-window chirality stays near `0` | `0` | yes | yes; stronger localization-style behavior does not produce index |

Mode-level audit conclusion:

- Disorder does not break the algebraic chiral block structure.
- Localization and index generation are empirically separable in this model.
- No current mode converts disorder/localization into protected nonzero chirality.

## Documentation Audit

Inspected files:

- `reports/SPECTRAL_REPORT.md`
- `reports/VALIDATION_STATUS.md`
- `reports/ISSUES_SCIENTIFIC.md`
- `reports/NULL_RESULTS.md`
- `reports/RELEASE_NOTES_v0.1.10.md`

### Overclaim audit

No overclaim was found in the inspected documentation.

The documentation consistently avoids claiming:

- physical chirality
- protected zero modes
- Witten/Lichnerowicz bypass
- covariant compactification validation
- Standard Model fermions
- `SU(3) x SU(2) x U(1)` derivation

### What the documentation does claim, correctly

The inspected docs do correctly state that the current result is only:

- a toy diagnostic
- a case where near-zero modes are observed
- a case where numerical index remains zero
- a case where the modes are classified as paired/accidental
- a contrast with the separate positive `S2` monopole index control

### Documentation contrast to positive control

The contrast is documented correctly:

- `S2` monopole control = positive nonzero-index control
- toy Dirac localization/chirality diagnostic = negative control for accidental
  or paired near-zero modes

### Documentation caveat

The official reproduction scripts rewrite living markdown reports with the new
run directory paths. This is an operational side effect worth remembering in
future audits, but it is not a scientific overclaim.

## Final Verdict

**confirmed with caveats**

Why:

1. The reported quick and full chirality results were reproduced successfully.
2. The Gamma algebra, anticommutator, chirality expectation, and index formula
   are implemented consistently.
3. No nonzero numerical index appears in the configured full grid.
4. Documentation remains scientifically cautious.
5. The most important caveat is structural: the current finite square-`A`
   construction strongly predisposes the model to zero index.

So the reported claim is supported:

> The toy Dirac localization benchmark produces near-zero modes, but the
> chirality/index diagnostic shows `numerical_index = 0` across the configured
> full grid. Therefore these modes are classified as paired/accidental, not
> protected/chiral zero modes.

This statement is reproduced and consistent with the current implementation.

## Recommended Next Step

**preserve this model as negative control**

Reason:

- the current construction is useful because it cleanly separates localization
  signals from true index generation
- it correctly demonstrates that near-zero modes alone are insufficient for a
  chirality claim
- its structural square-`A` form makes it a good accidental-zero-mode control,
  not a promising chirality mechanism

This audit does **not** recommend forcing this model to produce nonzero index.
