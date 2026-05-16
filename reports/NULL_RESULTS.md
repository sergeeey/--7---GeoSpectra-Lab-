# Null Results

Negative results are evidence in this project. Record hypotheses that fail, signals that vanish under refinement, seed-dependent effects, graph disconnect artifacts, unstable phase transitions, and near-zero modes that disappear after regularization.

## Spectral weak-disorder GOE check

At W=0.5, <r>=0.2631, which is not closer to GOE than to Poisson. This is logged as a toy-model limitation, not hidden as success. Run directory: reports\RUNS\20260511-221224_spectral_localization

Clarification after synthetic controls:

- This indicates the current quick Anderson setup is not a reliable weak-disorder GOE benchmark.
- It is not evidence against the r-statistics implementation.
- Synthetic controls passed in full mode:
  - Poisson: expected 0.3863, measured 0.3817, tolerance 0.0350.
  - GOE: expected 0.5307, measured 0.5309, tolerance 0.0400.
  - GUE optional: expected 0.5996, measured 0.5960, tolerance 0.0450.
- Latest synthetic-control run: reports\RUNS\20260511-224352_r_stat_controls_full.

Since full synthetic controls passed, the issue was narrowed to the old
Anderson benchmark setup rather than the r-statistics implementation.

Follow-up after the 3D Anderson quick benchmark:

- Run directory: reports\RUNS\20260511-231240_anderson_3d_benchmark_quick.
- Basic quick checks passed in the 3D benchmark.
- Weak reference `W=4` was closer to GOE than Poisson.
- Strong reference `W=24` moved toward Poisson relative to the weak reference.
- IPR increased from weak to strong disorder.

This does not erase the old 1D null result. It reclassifies it as a limitation
of the previous quick setup. The later configured full 3D benchmark supersedes
this quick check as the stronger benchmark evidence, but larger-size scaling
and full spectrum-window diagnostics were still required before making stronger
Anderson localization claims.

Follow-up after the configured full 3D Anderson benchmark:

- Run directory: reports\RUNS\20260511-232546_anderson_3d_benchmark_full.
- Basic full benchmark checks passed.
- Final-size `L=7` weak reference `W=4` had `<r>=0.5182`, closer to GOE than
  Poisson.
- Final-size `L=7` strong reference `W=24` had `<r>=0.3978`, close to Poisson.
- Mean IPR increased from `0.00997714` at `W=4` to `0.316232` at `W=24`.

This still does not turn the old 1D null result into a success. The old result
remains historical evidence that the previous quick setup was weak. The full 3D
benchmark improves the localization diagnostic. The later spectrum-window quick
run reduces concern about a center-window artifact, but larger lattices, full
quantile-window diagnostics, and boundary-condition comparisons are still needed
before stronger physics claims.

Follow-up after spectrum-window quick diagnostics:

- Run directory: reports\RUNS\20260512-081650_anderson_3d_spectrum_windows_quick.
- Center, lower, and upper spectral windows all passed the same basic
  localization diagnostic in quick mode.
- `all_windows_basic_checks_passed=True`.
- `window_choice_changes_conclusion=False`.

This is not a null result. It reduces concern that the configured 3D Anderson
result was only a center-window artifact. The remaining uncertainty is full
spectrum-window validation: quantile windows, larger `L`, more seeds,
boundary-condition comparison, and mobility-edge-style analysis are still
pending.

## 3D Anderson spectrum-window diagnostic limitation

Run directory: reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full

Mode: `full`.

Summary: Window choice changed at least one basic localization diagnostic; treat this as a limitation.

All windows basic checks passed: False.
Window choice changes conclusion: True.

This is a limitation of the current window-resolved Anderson benchmark, not evidence against the already validated r-statistics implementation. The historical 1D quick null-result remains preserved: `W=0.5, <r>=0.2631`.

Detailed full-mode assessment:

| window | weak `<r>` | strong `<r>` | weak IPR | strong IPR | passed |
| --- | ---: | ---: | ---: | ---: | --- |
| center | 0.5200 | 0.4424 | 0.0100626 | 0.305547 | True |
| lower | 0.5399 | 0.4093 | 0.0128243 | 0.351711 | True |
| upper | 0.5327 | 0.4130 | 0.0128753 | 0.35176 | True |
| quantile_0.1 | 0.5540 | 0.3977 | 0.0133127 | 0.367085 | True |
| quantile_0.3 | 0.5011 | 0.3853 | 0.0108976 | 0.313394 | True |
| quantile_0.5 | 0.5363 | 0.4601 | 0.00994604 | 0.29276 | False |
| quantile_0.7 | 0.5370 | 0.4347 | 0.0110571 | 0.29539 | True |
| quantile_0.9 | 0.5037 | 0.4242 | 0.0130484 | 0.336491 | True |

Interpretation: the full run is a mixed/limiting result. IPR increases in all
listed windows, but `quantile_0.5` fails the implemented basic r-statistics
check because its strong-disorder `<r>=0.4601` remains slightly closer to GOE
than Poisson at `W=24`. At the time, this blocked promotion on spectrum-window
full validation until targeted diagnostics were run.

Follow-up targeted diagnostic:

- Run directory: reports\RUNS\20260512-091720_anderson_quantile05_diagnostics.
- Configuration: `L = 6, 7, 8`, `W = [20, 24, 28, 32, 36]`, windows
  `center` and `quantile_0.5`, `10` realizations, open boundary.
- Classification: likely statistical/finite-size/seed-count effect.
- At final `L=8`, `quantile_0.5` is closer to Poisson at every tested W:
  - W=20: `<r>=0.4531`
  - W=24: `<r>=0.4127`
  - W=28: `<r>=0.4052`
  - W=32: `<r>=0.3981`
  - W=36: `<r>=0.3973`

This follow-up does not erase the full-run mixed result; it narrows the likely
cause. The failure is now classified as likely statistical/finite-size/seed-count
sensitivity rather than confirmed persistent delocalized behavior at
`quantile_0.5`.

## 3D Anderson boundary-condition diagnostic limitation

Run directory: `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison`

Summary: Open and periodic boundaries disagree for at least one basic diagnostic; treat as a limitation.

All boundary basic checks passed: `False`.
Boundary changes basic diagnostic: `True`.
Max |delta <r>| periodic-open: `0.0804`.
Max |delta IPR| periodic-open: `0.116229`.

This is a limitation of the current Anderson boundary benchmark, not evidence against the already validated r-statistics implementation. The historical 1D quick null-result remains preserved: `W=0.5, <r>=0.2631`.

## Periodic Boundary Follow-Up Status

Run directory: `reports\RUNS\20260512-094128_anderson_periodic_followup`

Classification:

```text
likely insufficient disorder range at W=24 with finite-size/seed-count sensitivity: periodic boundaries become Poisson-like for W>=32 at the final lattice size
```

Summary:

- Periodic failure is resolved in this targeted diagnostic at stronger disorder,
  but it did not by itself promote the Anderson validation status.
- Stronger disorder `W>=32` makes periodic boundary Poisson-like: `True`.
- IPR mostly monotonic across all periodic assessments: `True`.
- Spectrum-window artifact suspected: `False`.
- Current project baseline has since advanced to `v0.1.8-mvp-dirac-localization-full`
  due to the full toy Dirac/geometric localization benchmark, not because this
  Anderson boundary limitation disappeared.
- Historical null-result preserved: `W=0.5, <r>=0.2631`.

This entry updates the boundary-condition limitation rather than erasing it.
The earlier open-vs-periodic disagreement remains part of the validation record.

## S1 discretization full comparison shows discretization sensitivity

Run directory: `reports\RUNS\20260512-191838_s1_discretization_comparison_full`

Command:

```powershell
python scripts/s2_s1_discretization_comparison.py --full --include-wilson
```

Summary:

- `comparison_classification=mixed_or_limiting`
- `reference_family=spectral_circle`
- `all_families_match_reference=False`
- `all_families_pass_basic_gates=False`
- `spectral_circle`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=6750`
- `ring`: `classification=partial_or_ambiguous`,
  `all_basic_gates_passed=False`, `total_observations=6750`
- `wilson_ring`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=6750`

Gate-level detail:

- `spectral_circle`: all listed gates passed.
- `ring`: all listed gates passed except `localization_gate_passed=False`.
- `wilson_ring`: all listed gates passed.

Interpretation:

This is a null/limiting result for full-profile discretization robustness across
the tested `S1` families. It does not invalidate the reference
`spectral_circle` full benchmark or the `wilson_ring` full benchmark; it shows
that the current `ring` discretization changes the conclusion under the same
full comparison grid. The failure is therefore recorded as discretization
sensitivity, not hidden as a baseline promotion.

Targeted localization diagnosis:

- Run directory: `reports\RUNS\20260512-194941_s1_ring_localization_diagnostic`.
- Likely cause: `window_selection`.
- Supporting mechanism: nearest-neighbor `ring` carries an extra clean
  low-energy kernel (`representative_clean_kernel_count=2.0`) and a higher
  clean IPR (`0.081551`) than `spectral_circle` and `wilson_ring`
  (`kernel_count=1.0`, `clean_ipr=0.041667`).
- Ring target failure rate at `W=8`, `alpha=0.0`: `0.05` (`2/40` points).
- Fixed-window recovery rate on the failed target points: `1.0` (`2/2`).
- Ring target pass rate at `W=12`, `alpha=0.0`: `1.0`.

Interpretation update:

This narrows the most likely cause of the `ring` full-profile failure to a
window-selection artifact triggered by ring-specific doubled clean kernel
structure. The negative full-comparison result remains valid and is still
recorded as discretization sensitivity; the diagnosis explains the failure
mechanism but does not erase the limitation or justify baseline promotion.

Localization gate v2 status:

- The code now records both historical kernel-only and secondary fixed-window
  localization outcomes.
- New metrics are explicit in benchmark/comparison artifacts:
  `kernel_only_localization_gate_passed`,
  `fixed_window_localization_gate_passed`,
  `localization_gate_v2_passed`, and `localization_window_mode`.
- Historical `localization_gate_passed` is preserved as the kernel-only field.
- Disagreement between the two localization windows is now exposed as
  `window_selection_sensitivity`, not silently reclassified as success.
- No new full comparison rerun has overridden the historical mixed result, so
  this null/limiting entry stays in force.

Full rerun under v2 metrics:

- Run directory: `reports\RUNS\20260512-203723_s1_discretization_comparison_full`.
- Historical kernel-only interpretation remains mixed:
  - `comparison_classification=mixed_or_limiting`
  - `ring.kernel_only_localization_gate_passed=False`
- Secondary v2 interpretation is now clean across families:
  - `spectral_circle.fixed_window_localization_gate_passed=True`
  - `ring.fixed_window_localization_gate_passed=True`
  - `wilson_ring.fixed_window_localization_gate_passed=True`
  - `spectral_circle.localization_gate_v2_passed=True`
  - `ring.localization_gate_v2_passed=True`
  - `wilson_ring.localization_gate_v2_passed=True`
- `ring` is classified as `window_selection_sensitivity`, not as a silent pass.

Interpretation update after the rerun:

The historical null/limiting result is preserved because the kernel-only full
comparison still disagrees for `ring`. The new rerun adds a second result on
top of that record: under the explicit fixed-window localization gate v2, the
three-family full comparison is clean. This resolves the mechanism as
window-selection sensitivity without erasing the old negative entry.

## Localization gate v2 stress grid shows case-level limitation

Run directory: `reports\RUNS\20260512-225834_s1_discretization_v2_stress`

Command:

```powershell
python scripts/s2_s1_discretization_v2_stress.py --realizations 3
```

Why `realizations=3`:

- The requested `realizations=5` stress profile was started first but proved
  too expensive for an interactive run.
- Per the documented fallback rule, the stress run was repeated with
  `cutoff=2` unchanged, all three `S1` families preserved, and
  `realizations=3`.

Summary:

- family-aggregate comparison result:
  - `comparison_classification=robust_across_discretizations`
  - `spectral_circle`, `ring`, `wilson_ring` each recorded
    `classification=quick_bridge_passed`
  - each family also recorded
    `kernel_only_localization_gate_passed=True`,
    `fixed_window_localization_gate_passed=True`,
    `localization_gate_v2_passed=True`
- case-level stress result:
  - `stress_classification=v2_limitation`
  - `total_localization_cases=7560`
  - `fixed_window_failure_cases=1429`
  - `kernel_only_vs_fixed_window_disagreements=93`
  - `ring_doubler_sensitive_cases=93`

Failure counts:

- by family:
  - `spectral_circle=475`
  - `ring=594`
  - `wilson_ring=360`
- by disorder:
  - `W=0 -> 1080`
  - `W=1 -> 193`
  - `W=2 -> 125`
  - `W=4 -> 31`
- by twist:
  - `alpha=0.0 -> 570`
  - `alpha=0.25 -> 431`
  - `alpha=0.5 -> 428`

Interpretation:

This stress run does not erase either earlier record:

- the historical kernel-only mixed run remains preserved:
  `reports\RUNS\20260512-191838_s1_discretization_comparison_full`;
- the full v2 comparison rerun remains preserved:
  `reports\RUNS\20260512-203723_s1_discretization_comparison_full`.

However, the denser stress grid shows that fixed-window localization gate v2 is
not uniformly stable across all scanned points. The family-level benchmark gates
remain clean on this fallback profile, but the case-level stress diagnostic
still produces explicit fixed-window failures across all three families.

This is therefore recorded as a `v2 limitation`, not as a baseline promotion or
as evidence for any physical compactification claim.

### Stress `realizations=5` follow-up and W=8 targeted diagnostic (May 2026)

Stress run:

```text
reports\RUNS\20260513-001436_s1_discretization_v2_stress
```

Stress memo:

```text
reports\S1_V2_STRESS_FAILURE_ANALYSIS_realizations5.md
```

Stress-level bookkeeping (unchanged):

- `stress_classification=v2_limitation` and `case_level_fixed_window_all_passed=False`
  remain the stress artifact.
- **Pre-declared binary rule:** `unresolved_strong_disorder_v2_limitation`
  because `W>=8` fixed-window failures **> 0** (one case). **This does not erase
  the `r=5` stress limitation.**

Targeted diagnostic (single `W=8` outlier only):

```text
reports\RUNS\20260513-082348_s1_v2_w8_failure_diagnostic
reports\S1_V2_W8_FAILURE_DIAGNOSTIC.md
```

Mechanistic refinement:

- label: `threshold_or_window_definition_artifact`;
- narrows interpretation: **no** observed widespread strong-disorder breakdown on
  the diagnostic sweep; remaining issue is **fixed-window localization
  sensitivity to `low_energy_count` / window definition** on one **ring,
  small-`s1_size`, anchor** case.

Historical kernel-only mixed run, full v2 rerun, and current baseline remain
preserved.

Non-claims:

- not continuum compactification;
- not `S6` / `S3 x S6`;
- not Standard Model;
- not physical chirality;
- not Witten/Lichnerowicz bypass.

## Toy Dirac near-zero modes have zero numerical index

Run directory: `reports\RUNS\20260512-135933_dirac_chirality_full`

The toy Dirac chirality/index diagnostic found near-zero modes, but the
numerical index remains zero across the configured localization modes.

Interpretation:

- This is a null result for protected/chiral zero-mode interpretation in the
  current toy Dirac localization benchmark.
- The near-zero modes are classified as paired or accidental under this
  diagnostic.
- This does not invalidate the separate `S2` Dirac monopole index control,
  which remains the positive control for nonzero index counting.
- Historical Anderson null-result remains preserved: `W=0.5, <r>=0.2631`.
