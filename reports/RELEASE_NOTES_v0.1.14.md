# Release Notes — v0.1.14-mvp-s2-s1-discretization-v2-full

## Summary
This release promotes the `S2 x S1` full discretization comparison under the
explicit localization gate v2 / fixed-window diagnostic to the current toy
baseline.

## What changed in v2
- explicit historical kernel-only localization reporting
- explicit fixed-window low-energy localization reporting
- new metrics:
  - `kernel_only_localization_gate_passed`
  - `fixed_window_localization_gate_passed`
  - `localization_gate_v2_passed`
  - `localization_window_mode`
  - `window_selection_sensitivity`
- updated comparison summary/artifacts so localization-window disagreement is
  visible rather than silently folded into pass/fail

## Historical kernel-only limitation
The historical full comparison remains on record:

```text
reports/RUNS/20260512-191838_s1_discretization_comparison_full
```

Under the historical kernel-only localization gate:
- `comparison_classification=mixed_or_limiting`
- `ring.localization_gate_passed=False`
- baseline was not promoted from that run

This historical mixed result is preserved and not erased by the new release.

## New fixed-window v2 result
Verified command:

```powershell
python scripts/s2_s1_discretization_comparison.py --full --include-wilson
```

Reference run:

```text
reports/RUNS/20260512-203723_s1_discretization_comparison_full
```

Per-family v2 result:
- `spectral_circle`: passes kernel-only and fixed-window localization
- `ring`: fails historical kernel-only localization, passes fixed-window
  localization, classified as `window_selection_sensitivity`
- `wilson_ring`: passes kernel-only and fixed-window localization

Verification:
- `comparison_classification=mixed_or_limiting`
- `all_families_match_reference=False`
- `all_families_pass_basic_gates=False`
- `pytest -q: 107 passed`

## Interpretation of ring doubled kernel
The targeted diagnosis indicates that nearest-neighbor `ring` carries a
fermion-doubling-style doubled clean low-energy kernel in this toy setting:
`ring` shows clean `kernel_count=2`, while `spectral_circle` and `wilson_ring`
show `kernel_count=1`.

Under kernel-only comparison, this doubled clean kernel makes `ring`
sensitive to low-energy window selection. Under the explicit fixed-window v2
diagnostic, the same family passes localization and is therefore interpreted as
`window_selection_sensitivity`, not as a generic absence of localization
response.

## Scientific non-claims
This is a toy product diagnostic, not continuum compactification.
This is not `S6` or `S3 x S6`.
This does not derive Standard Model physics.
This does not prove physical chirality.
This does not validate covariant compactification.
This does not bypass Witten/Lichnerowicz no-go results.

## Next recommended step
Stress-test the localization gate v2 result with larger sizes, more seeds, and
future alternative `S1` discretizations, while continuing to document the
historical kernel-only mixed result side by side with the promoted v2 baseline.
