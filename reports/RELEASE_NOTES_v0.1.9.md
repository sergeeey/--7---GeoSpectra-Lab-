# Release Notes — v0.1.9-mvp-dirac-chirality-diagnostic

## Summary

This release adds a chirality/index diagnostic for the toy Dirac localization
operators. It checks the block chirality operator `Gamma = diag(+I, -I)`,
the anticommutator `{D, Gamma}`, chirality expectations, and the numerical
index of exact near-zero modes.

## New in this release

- `cc_toy_lab/spectral/dirac_chirality.py`
- `scripts/dirac_chirality_diagnostic.py`
- `tests/test_dirac_chirality.py`
- Run artifacts for the chirality diagnostic.
- Documentation updates for spectral, validation, null-result, and issue logs.

## Verified results

Command:

```powershell
python scripts/dirac_chirality_diagnostic.py --quick
```

Run directory:

```text
reports\RUNS\20260512-132501_dirac_chirality_quick
```

Flags:

| Metric | Value |
| --- | --- |
| `gamma_algebra_passed` | `True` |
| `anticommutation_preserved` | `True` |
| `all_indices_zero` | `True` |
| `any_near_zero_modes` | `True` |

Mode assessments:

| mode | weak W | strong W | weak index | strong index | weak zeros | strong zeros | index stays zero | {D,Gamma} preserved | classification |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| clean | 0 | 8 | 0 | 0 | 2 | 2 | True | True | paired_or_accidental_zero_index |
| gauge_phase | 0 | 8 | 0 | 0 | 2 | 0 | True | True | paired_or_accidental_zero_index |
| geometric_weight | 0 | 8 | 0 | 0 | 2 | 0 | True | True | paired_or_accidental_zero_index |
| random_mass | 0 | 8 | 0 | 0 | 2 | 0 | True | True | paired_or_accidental_zero_index |

## Scientific meaning

The diagnostic separates numerical near-zero modes from index-protected modes
in the current finite toy localization benchmark. The observed near-zero modes
have zero numerical index and are classified as paired or accidental.

## Scientific non-claims

This does not prove physical chirality, protected zero modes,
Witten/Lichnerowicz bypass, covariant compactification, Standard Model fermions,
or `SU(3) x SU(2) x U(1)`.

## Known limitations

- Finite toy block operator.
- Quick mode unless a full run is separately executed.
- Gamma is the algebraic block chirality of the toy construction, not a
  physical compactification chirality operator.
- Zero numerical index in this diagnostic does not invalidate the separate
  positive `S2` monopole index control.

## Next recommended action

Run `python scripts/dirac_chirality_diagnostic.py --full`, then connect the
chirality diagnostic to a less artificial geometric Dirac discretization.
