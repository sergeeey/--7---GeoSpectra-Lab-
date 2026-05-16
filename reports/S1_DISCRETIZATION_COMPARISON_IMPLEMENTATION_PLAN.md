# S1 Discretization Comparison Implementation Plan

## Status

- Project: `GeoSpectra Lab / Covariant Compactification Toy Lab`
- Current baseline: `v0.1.13-mvp-s2-s1-product-full`
- Scope: implementation plan for discretization robustness comparison
- This document does not promote a new baseline and does not add a new physics claim.

## Purpose

The current `S2 x S1` benchmark passes with the `spectral_circle` `S1`
construction. The next validation stage must test whether that toy benchmark
conclusion is robust to the choice of `S1` discretization.

This comparison must happen before any move toward `S3`, `S6`, `S3 x S6`, or
`S2 x S1 x graph`, because a result that depends strongly on one `S1`
construction is not yet a stable geometric toy benchmark.

## Current Reference Model

The current reference implementation is the `S2 x S1` product benchmark in
`cc_toy_lab/spectral/s2_s1_product.py`, using the `spectral_circle` `S1`
family.

Reference benchmark status:

- `classification=quick_bridge_passed`
- `all_basic_gates_passed=True`
- `total_observations=6750`
- baseline remains `v0.1.13-mvp-s2-s1-product-full`

The comparison stage treats `spectral_circle` as the control family and checks
whether the same gate-level conclusions survive for alternative `S1`
discretizations.

## Proposed New S1 Discretizations

### Ring nearest-neighbor operator

Use a Hermitian nearest-neighbor ring operator with twist carried by a boundary
phase.

Required properties:

- Hermitian to numerical tolerance
- explicit `alpha` dependence
- PBC/APBC semantic compatibility with the existing benchmark gates
- clean zero-mode structure at `alpha=0.0` for the nonzero-`q` inherited-kernel
  control

### Wilson-like ring operator

Use the same ring construction plus a Hermitian Wilson-like correction term to
control lattice artifacts and spurious low-energy structure.

This is optional for the first quick comparison. The first required milestone is
the plain `ring` family.

## File Layout

The implementation should use the following files:

- `cc_toy_lab/spectral/s1_discretizations.py`
- `cc_toy_lab/spectral/s1_discretization_comparison.py`
- `cc_toy_lab/spectral/s2_s1_product.py`
- `scripts/s2_s1_discretization_comparison.py`
- `tests/test_s2_s1_discretization_comparison.py`
- `reports/S1_DISCRETIZATION_COMPARISON_IMPLEMENTATION_PLAN.md`

## API Design

### S1 builders

Implement:

- `build_s1_ring_operator(...)`
- `build_s1_wilson_operator(...)`
- `build_s1_operator(..., family: str, mode: str, ...)`

### Product benchmark compatibility

Do not overload the existing `mode` axis. Instead:

- `s1_family` selects the clean discretization family
- `mode` remains the inhomogeneity/deformation axis

The existing `S2 x S1` benchmark API remains the control path, with
`s1_family="spectral_circle"` as the default.

### Comparison layer

Implement:

- `compare_s1_discretizations(...)`
- `run_s1_discretization_comparison(...)`
- `save_s1_discretization_comparison_artifacts(...)`

The comparison layer should aggregate family-specific `S2S1Assessment` results
without breaking the current gate vocabulary.

## Required Comparison Gates

Use the same benchmark gates as the current `S2 x S1` product benchmark:

- `classification`
- `all_basic_gates_passed`
- `q_control_passed`
- `pbc_gate_passed`
- `apbc_gate_passed`
- `flux_response_observed`
- `s1_not_spectator`
- `localization_gate_passed`
- `threshold_stable`

## Test Plan

### Operator sanity

- Hermiticity for `ring` and `wilson_ring`
- PBC/APBC spectra differ
- twist moves low-energy modes

### Product benchmark compatibility

- `q=0` does not produce false inherited kernel signal
- `q!=0` preserves qualitative PBC/APBC lifting behavior
- `S1` remains non-spectator under family comparison
- localization gate remains meaningful for the intended inhomogeneity pair
- threshold stability survives

### Comparison reporting

- comparison script saves `config.json`, `metrics.json`, `data.npz`, `summary.md`,
  `figures/`
- comparison CLI uses the same gate/result vocabulary style as the current
  benchmark
- public summaries do not reintroduce full-product global chiral index language

## Success Criteria

The comparison counts as a success if:

1. `spectral_circle` and `ring` preserve the same benchmark-level qualitative
   conclusion on the declared quick comparison profile
2. `q_control_passed` remains true
3. `pbc_gate_passed`, `apbc_gate_passed`, `flux_response_observed`,
   `s1_not_spectator`, `localization_gate_passed`, and `threshold_stable`
   remain true for the reference family and at least one alternative family
4. no `q=0` false inherited signal appears

If `wilson_ring` is included later, it may either match the same qualitative
conclusion or be documented explicitly as `mixed` / `limiting`.

## Failure Criteria

Record the comparison as a limitation or mixed result if:

- `ring` or `wilson_ring` fails PBC/APBC lifting behavior
- twist no longer moves low-energy modes
- `S1` becomes spectator
- localization gate fails or becomes numerically unstable
- threshold stability fails
- the qualitative result depends strongly on discretization family

If any alternative family flips the headline toy-level interpretation, preserve
`v0.1.13` and document discretization sensitivity rather than promoting a new
baseline.

## Scientific Non-Claims

This comparison:

- is not continuum compactification
- is not `S6`
- is not `S3 x S6`
- does not derive Standard Model physics
- does not prove physical chirality
- does not bypass Witten/Lichnerowicz

The full-product global chiral index must not return as the headline metric.

## Recommended Implementation Order

1. Freeze the current `spectral_circle` benchmark contract.
2. Implement the `ring` operator only.
3. Add unit tests for Hermiticity, twist response, and `q=0` control.
4. Add the comparison runner and artifact writer.
5. Run the quick comparison first.
6. Only if the quick comparison is clean, add `wilson_ring`.
7. Only if the quick comparison remains clean, run the full comparison.
8. Update validation docs only after the comparison outcome is understood.

## Scope Reminder

This work strengthens the toy benchmark methodology only. It is not a license to
promote `S3`, `S6`, `S3 x S6`, or physical compactification claims before
discretization robustness is checked.
