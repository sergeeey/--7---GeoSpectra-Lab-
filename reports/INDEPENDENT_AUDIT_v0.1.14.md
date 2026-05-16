# Independent Audit — v0.1.14 S2 x S1 Discretization v2 Full

## Executive Summary
Independent audit result: **confirmed with caveats**.

The current baseline `v0.1.14-mvp-s2-s1-discretization-v2-full` is supported by
the checked artifacts, by an independent local rerun, and by a clean local test
suite run. The historical kernel-only full comparison remains explicitly mixed,
the `ring` family still fails the historical kernel-only localization gate, and
the v2 interpretation correctly reclassifies `ring` as
`window_selection_sensitivity` rather than a generic localization failure.

## Reproducibility
Commands run during this audit:

```powershell
pytest -q
python scripts/s2_s1_discretization_comparison.py --full --include-wilson
```

Observed local results:

- `pytest -q` -> `107 passed in 94.11s`
- independent rerun -> `reports/RUNS/20260512-211633_s1_discretization_comparison_full`
- rerun exit status -> `0`
- rerun summary:
  - `comparison_classification=mixed_or_limiting`
  - `reference_family=spectral_circle`
  - `all_families_match_reference=False`
  - `all_families_pass_basic_gates=False`

Independent rerun agreement with the release reference run
`reports/RUNS/20260512-203723_s1_discretization_comparison_full`:

- same top-level classification: `mixed_or_limiting`
- same reference family: `spectral_circle`
- same failing family under historical kernel-only gate: `ring`
- same v2 interpretation: `ring -> window_selection_sensitivity`
- same per-family v2 pass state for fixed-window localization

This audit did not modify scientific code and did not add new scientific
features. The only new artifact produced by the audit is this report and the
independent rerun output directory.

## Historical Kernel-Only Result
The historical kernel-only full comparison remains documented and visible:

- historical run:
  `reports/RUNS/20260512-191838_s1_discretization_comparison_full`
- `comparison_classification=mixed_or_limiting`
- `ring.classification=partial_or_ambiguous`
- `ring.localization_gate_passed=False`

This historical mixed result is still present in the checked documentation and
is not erased by the v2 release framing. It remains explicitly discussed in:

- `reports/VALIDATION_STATUS.md`
- `reports/SPECTRAL_REPORT.md`
- `reports/NULL_RESULTS.md`
- `reports/ISSUES_SCIENTIFIC.md`
- `reports/RELEASE_NOTES_v0.1.14.md`

## New v2 Fixed-Window Result
Reference v2 run checked:

- `reports/RUNS/20260512-203723_s1_discretization_comparison_full`

Independent rerun checked:

- `reports/RUNS/20260512-211633_s1_discretization_comparison_full`

Per-family v2 result is confirmed as follows:

- `spectral_circle`
  - `kernel_only_localization_gate_passed=True`
  - `fixed_window_localization_gate_passed=True`
  - `localization_gate_v2_passed=True`
  - `classification=quick_bridge_passed`
- `ring`
  - `kernel_only_localization_gate_passed=False`
  - `fixed_window_localization_gate_passed=True`
  - `localization_gate_v2_passed=True`
  - `classification=window_selection_sensitivity`
- `wilson_ring`
  - `kernel_only_localization_gate_passed=True`
  - `fixed_window_localization_gate_passed=True`
  - `localization_gate_v2_passed=True`
  - `classification=quick_bridge_passed`

Therefore the audit confirms claim (3): under the explicit fixed-window v2
localization diagnostic, all three tested families pass the v2 localization
criterion.

## Ring Interpretation
The checked artifacts support the interpretation that `ring` is best classified
as `window_selection_sensitivity`, not as a generic localization failure.

Confirmed facts:

- historical kernel-only run keeps `ring.localization_gate_passed=False`
- v2 runs keep `ring.kernel_only_localization_gate_passed=False`
- v2 runs also show `ring.fixed_window_localization_gate_passed=True`
- v2 runs show `ring.localization_gate_v2_passed=True`
- v2 runs mark `ring.window_selection_sensitivity=True`
- v2 runs classify `ring` as `window_selection_sensitivity`

This preserves the negative historical fact while narrowing its mechanism.

## Documentation Audit
Checked files:

- `README.md`
- `reports/VALIDATION_STATUS.md`
- `reports/SPECTRAL_REPORT.md`
- `reports/NULL_RESULTS.md`
- `reports/ISSUES_SCIENTIFIC.md`
- `reports/RELEASE_NOTES_v0.1.14.md`

Audit result: documentation is **scientifically cautious** in the checked files.

No audited document was found to claim:

- continuum compactification
- `S6` or `S3 x S6` as a validated physical result
- Standard Model derivation
- physical chirality proof
- Witten/Lichnerowicz bypass

Instead, the checked files repeatedly frame the result as a toy/product
diagnostic and explicitly preserve non-claims.

## Caveats
- This remains a toy/product-diagnostic result, not a continuum compactification
  result.
- The top-level comparison classification still remains
  `mixed_or_limiting`; v2 resolves the localization-window interpretation, not
  every benchmark gate into a clean all-family pass.
- The historical kernel-only mixed result must continue to be shown alongside
  the v2 fixed-window interpretation.
- `README.md` still shows a top-level current-baseline header for `v0.1.13`;
  this is a documentation synchronization lag, not a scientific overclaim.
- No statement here validates physical chirality, Standard Model derivation, or
  any Witten/Lichnerowicz bypass.

## Final Verdict
**confirmed with caveats**
