# Scientific Issues

## Initial Scope Warnings

- Anderson / GOE / Poisson diagnostics test localization only. They do not prove chirality.
- The radion potential D uses a toy-regularized KK tower. It is not a full quantum effective action.
- The phase transition model is a threshold toy model pinned to `alpha_c = 1.345`; it is a reproducibility target, not a derived physical critical point.
- Product spectra for `S3 x S6` verify analytic sum rules, not cosmological vacuum selection.

## 3D Anderson spectrum-window diagnostics need follow-up

Run directory: reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full

A window-dependent result should be diagnosed through eigenvalue solver checks, window-selection thresholds, degeneracy inspection, finite-size behavior, and open-vs-periodic boundary comparison before making stronger localization claims.

Full-mode detail:

- Run directory: reports\RUNS\20260512-090919_anderson_3d_spectrum_windows_full.
- `all_windows_basic_checks_passed=False`.
- `window_choice_changes_conclusion=True`.
- `quantile_0.5` failed the implemented basic check:
  - weak `<r>=0.5363`;
  - strong `<r>=0.4601`;
  - weak IPR `0.00994604`;
  - strong IPR `0.29276`.
- IPR still increases in `quantile_0.5`, so the issue is specifically the
  r-statistics/Poisson-shift criterion under this window definition.

Next diagnosis should test window width, quantile centering, seed stability,
larger `L`, open-vs-periodic boundaries, and dense/sparse eigensolver
consistency.

## Quantile_0.5 targeted follow-up

Run directory: reports\RUNS\20260512-091720_anderson_quantile05_diagnostics

Classification:

```text
likely statistical/finite-size/seed-count effect: quantile_0.5 at W=24 becomes Poisson-like in the targeted rerun
```

The targeted rerun used `L = 6, 7, 8`, `W = [20, 24, 28, 32, 36]`, windows
`center` and `quantile_0.5`, and `10` realizations. At final `L=8`,
`quantile_0.5` was closer to Poisson at every tested W, including
`W=24` with `<r>=0.4127`.

Remaining scientific issue: this was still open-boundary only. Before upgrading
confidence, compare open vs periodic boundaries, increase seeds further, and
check whether the conclusion is stable under window-width changes.

## 3D Anderson boundary comparison needs follow-up

Run directory: `reports\RUNS\20260512-093014_anderson_3d_boundary_comparison`

A boundary-sensitive result should be diagnosed through larger L, more seeds, spectrum-window refinement, eigenvalue-solver checks, and disorder-grid refinement before stronger localization statements are made.

## Periodic Boundary Follow-Up Interpretation

Run directory: `reports\RUNS\20260512-094128_anderson_periodic_followup`

Classification: likely insufficient disorder range at W=24 with finite-size/seed-count sensitivity: periodic boundaries become Poisson-like for W>=32 at the final lattice size

Remaining uncertainty:

- The benchmark remains finite-size limited.
- The pass/fail rule is a diagnostic threshold, not a theorem.
- Boundary-sensitive behavior should be retested with larger `L`, more seeds,
  solver checks, and window-width variation before stronger localization
  statements are made.
- No target compactification model has been validated.

## Near-zero modes in toy Dirac localization are not yet protected

Run directory: `reports\RUNS\20260512-130351_dirac_localization_full`

The toy Dirac/geometric localization benchmark reports r-statistics, IPR, and
near-zero counts for finite chiral block operators.

Observed full-mode facts:

- `any_near_zero_modes=True`.
- The `clean` mode has exact near-zero modes and no localization trend.
- `random_mass` and `geometric_weight` show both IPR growth and r-statistics
  movement toward Poisson.
- `gauge_phase` shows r-statistics movement toward Poisson but does not
  increase near-zero IPR.
- All `+-lambda` symmetry checks passed.

Near-zero modes in this benchmark are numerical signals only. They are not
protected zero modes unless an index/chirality check is also implemented and
passed.

Interpretation constraints:

- Localization is not an index.
- Near-zero modes are not protected chiral zero modes.
- This benchmark does not prove Witten/Lichnerowicz bypass.
- This benchmark does not derive Standard Model fermions.
- No physical chirality claim is allowed from this benchmark yet.

Required follow-up:

1. Add an explicit chirality operator for the localization modes.
2. Compute an index-like diagnostic where the toy construction permits it.
3. Test robustness of near-zero modes under perturbations.
4. Compare any zero-mode claim against the verified `S2` Dirac monopole index
   control.

Summary: Symmetry passed=True; IPR increases in ['random_mass', 'geometric_weight']; r-statistics moves toward Poisson in ['random_mass', 'gauge_phase', 'geometric_weight']; near-zero modes observed=True. Near-zero modes are numerical signals only, not protected chiral zero modes.

## Toy Dirac localization near-zero modes have zero numerical index

Run directory: `reports\RUNS\20260512-135933_dirac_chirality_full`

The toy Dirac chirality diagnostic checks `Gamma = diag(+I, -I)`, verifies
`Gamma^2 = I`, Hermiticity, and the anticommutator `{D, Gamma}`. It then
counts chirality-polarized eigenvectors inside the documented near-zero
tolerance.

Result summary:

- Gamma algebra passed=True; anticommutation preserved=True; all numerical indices zero=True; near-zero modes observed=True; nonzero-index modes=[]. Near-zero modes remain numerical signals unless an index diagnostic is stable across size, seeds, and perturbations.
- All numerical indices zero: `True`.
- Near-zero modes observed: `True`.

Interpretation:

Near-zero modes in the toy Dirac localization benchmark are paired or
accidental under this diagnostic. No physical chirality claim is allowed from
these modes.

Required follow-up:

1. Test a less artificial geometric Dirac discretization.
2. Compare any future nonzero-index signal against the verified `S2` monopole
   index control.
3. Check stability across size, seeds, perturbations, and a chirality operator
   tied to the target geometry before using the word protected.

## S2 x graph bridge is not yet a geometric compactification model

Run directory: `reports\RUNS\20260512-141913_s2_graph_intermediate_quick`

The benchmark combines the verified finite-mode `S2` monopole index control
with a graph-sector localization selector. This is useful as an intermediate
toy bridge, but it is not a continuum `S2 x S1` Dirac operator and not an
`S6` or `S3 x S6` compactification model.

Result summary:

- Index checks passed=True; anticommutators preserved=True; IPR growth observed=True. This is an intermediate S2 x graph toy bridge, not a physical compactification result.

Interpretation constraints:

- The graph sector selects localized bases inside an index-carrying zero-mode
  sector.
- Index stability here comes from the rectangular chiral block inherited from
  the finite-mode monopole control.
- No physical chirality or Standard Model fermion claim is allowed.
- Move to `S6` or `S3 x S6` only after a less artificial geometric product
  discretization is tested.

## S2 x S1 product bridge is still a toy diagnostic, not continuum compactification

Run directory: `reports/RUNS/20260512-172546_s2_s1_product_quick`

Observed facts:

- `classification=quick_bridge_passed`.
- `all_basic_gates_passed=True`.
- `total_observations=648`.
- `q_control_passed=True`.
- `pbc_gate_passed=True`.
- `apbc_gate_passed=True`.
- `flux_response_observed=True`.
- `s1_not_spectator=True`.
- `localization_gate_passed=True`.
- `threshold_stable=True`.

Why this is stronger than `S2 x graph`:

- The `S1` factor enters the operator directly:
  `D_{S2xS1} = D_{S2}(q) ⊗ I_{S1} + Γ_{S2} ⊗ P_{S1}(α, W)`.
- Twist response and localization response are therefore tested inside the toy
  product operator rather than through an external graph-sector selector.

Interpretation constraints:

- This is still a toy product diagnostic.
- Full-product global chiral index is not the headline metric for this
  odd-dimensional toy product.
- No continuum compactification claim is allowed.
- No `S6` / `S3 x S6` claim is allowed.
- No Standard Model or physical chirality claim is allowed.
- No Witten/Lichnerowicz bypass claim is allowed.

Required follow-up:

1. Run the `S2 x S1` full benchmark.
2. Add figures if they improve interpretation.
3. Compare spectral-circle against ring/Wilson-like `S1` discretizations.
4. Test product-discretized geometric refinements before any return to `S6` or
   `S3 x S6`.

## Full S1 discretization robustness is not yet established

Run directory: `reports/RUNS/20260512-191838_s1_discretization_comparison_full`

Observed facts:

- `comparison_classification=mixed_or_limiting`.
- `reference_family=spectral_circle`.
- `all_families_match_reference=False`.
- `all_families_pass_basic_gates=False`.
- `spectral_circle`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=6750`.
- `ring`: `classification=partial_or_ambiguous`,
  `all_basic_gates_passed=False`, `total_observations=6750`.
- `wilson_ring`: `classification=quick_bridge_passed`,
  `all_basic_gates_passed=True`, `total_observations=6750`.
- The distinguishing failed flag is `ring.localization_gate_passed=False`; the
  other recorded gate flags remain `True`.
- Follow-up diagnostic run: `reports/RUNS/20260512-194941_s1_ring_localization_diagnostic`.
- Diagnostic classification: likely `window_selection`.
- Diagnostic evidence:
  - `ring` representative clean kernel count is `2.0`; both passing families
    remain at `1.0`.
  - `ring` representative clean IPR is `0.081551`; both passing families stay
    at `0.041667`.
  - Ring target failure rate at `W=8`, `alpha=0.0` is `0.05` (`2/40` points).
  - Fixed-window recovery rate on failed target points is `1.0` (`2/2`).
  - Ring target pass rate at `W=12`, `alpha=0.0` is `1.0`.
- Implementation update:
  - The code now computes both historical kernel-only and secondary
    fixed-window localization diagnostics.
  - New explicit metrics are
    `kernel_only_localization_gate_passed`,
    `fixed_window_localization_gate_passed`,
    `localization_gate_v2_passed`, and `localization_window_mode`.
  - Kernel-only/fixed-window disagreement is surfaced as
    `window_selection_sensitivity`.
- Full v2 rerun:
  - Run directory: `reports/RUNS/20260512-203723_s1_discretization_comparison_full`.
  - `comparison_classification=mixed_or_limiting`.
  - `all_families_match_reference=False`.
  - `all_families_pass_basic_gates=False`.
  - `spectral_circle`: `kernel_only_localization_gate_passed=True`,
    `fixed_window_localization_gate_passed=True`,
    `localization_gate_v2_passed=True`,
    `window_selection_sensitivity=False`.
  - `ring`: `kernel_only_localization_gate_passed=False`,
    `fixed_window_localization_gate_passed=True`,
    `localization_gate_v2_passed=True`,
    `window_selection_sensitivity=True`.
  - `wilson_ring`: `kernel_only_localization_gate_passed=True`,
    `fixed_window_localization_gate_passed=True`,
    `localization_gate_v2_passed=True`,
    `window_selection_sensitivity=False`.

Interpretation constraints:

- The current toy `S2 x S1` bridge is not yet robust across all tested `S1`
  discretization families on the historical kernel-only full grid.
- The v2 fixed-window rerun is clean across the tested families, but this does
  not erase the historical kernel-only limitation.
- No continuum compactification claim is allowed.
- No `S6` / `S3 x S6` claim is allowed.
- No Standard Model or physical chirality claim is allowed.
- No Witten/Lichnerowicz bypass claim is allowed.

Required follow-up:

1. Keep the historical kernel-only mixed run and the promoted v2 fixed-window
   rerun documented side by side.
2. Test whether the ring-specific doubled clean kernel persists under further
   geometric refinements or alternative discretizations.
3. Re-check cross-family robustness only after the gate definition is fixed and
   documented; until then, treat the current result as a limitation of the toy
   benchmark rather than a continuum statement.
4. Stress-test the v2 localization gate with larger sizes, more seeds, and any
   future alternative `S1` discretizations before making stronger robustness
   claims.

## Localization gate v2 stress grid still has case-level failures

Run directory: `reports/RUNS/20260512-225834_s1_discretization_v2_stress`

Observed facts:

- The fallback stress profile used `realizations=3` after the requested
  `realizations=5` profile proved too expensive for an interactive run.
- `cutoff=2` remained unchanged.
- All three tested families were kept:
  `spectral_circle`, `ring`, `wilson_ring`.
- Family-aggregate benchmark output on this fallback profile is clean:
  - `comparison_classification=robust_across_discretizations`
  - all three families report `classification=quick_bridge_passed`
  - all three families report
    `kernel_only_localization_gate_passed=True`
  - all three families report
    `fixed_window_localization_gate_passed=True`
  - all three families report `localization_gate_v2_passed=True`
- Case-level stress diagnostics are not clean:
  - `stress_classification=v2_limitation`
  - `total_localization_cases=7560`
  - `fixed_window_failure_cases=1429`
  - `kernel_only_localization_gate_passed=False` on `1394` cases
  - `window_selection_sensitivity=True` on `93` cases
  - `ring_doubler_sensitive_cases=93`
- Fixed-window failures appear in all three families:
  - `spectral_circle=475`
  - `ring=594`
  - `wilson_ring=360`

Interpretation constraints:

- The fallback stress run does not erase the historical kernel-only mixed full
  comparison:
  `reports/RUNS/20260512-191838_s1_discretization_comparison_full`.
- It also does not invalidate the earlier full v2 reruns; instead it shows that
  denser case-level scanning is stricter than the family-aggregate benchmark
  gate summary.
- The stress result therefore counts as a `v2 limitation`, not as permission to
  promote the baseline further.
- No continuum compactification claim is allowed.
- No `S6` / `S3 x S6` claim is allowed.
- No Standard Model or physical chirality claim is allowed.
- No Witten/Lichnerowicz bypass claim is allowed.

Required follow-up:

1. Separate family-aggregate gate summaries from case-level stress diagnostics
   in future interpretations; do not treat one as equivalent to the other.
2. Decide whether `W=0` should remain inside the stress-failure count or be
   reported separately as an expected null-localization corner case.
3. Increase realizations again outside the interactive path and test whether the
   nonzero-disorder failures at `W=1,2,4` persist.
4. Check whether the remaining failures shrink with larger `S1` size or instead
   indicate a gate-definition issue across all families, not just `ring`.
5. Keep the historical kernel-only mixed result, the full v2 rerun, and the new
   stress limitation documented side by side.

## Localization gate v2 stress `realizations=5` and W=8 targeted diagnostic

Stress run:

```text
reports/RUNS/20260513-001436_s1_discretization_v2_stress
```

Stress memo:

```text
reports/S1_V2_STRESS_FAILURE_ANALYSIS_realizations5.md
```

Observed constraint (stress-level, unchanged):

- `stress_classification=v2_limitation` and `case_level_fixed_window_all_passed=False`
  remain on record.
- **Pre-declared binary rule:** `unresolved_strong_disorder_v2_limitation`
  because `W>=8` fixed-window failures **> 0** (one case).

Targeted diagnostic (mechanism for that single case only):

```text
reports/RUNS/20260513-082348_s1_v2_w8_failure_diagnostic
reports/S1_V2_W8_FAILURE_DIAGNOSTIC.md
```

Refinement:

- mechanistic label: `threshold_or_window_definition_artifact`;
- **does not erase** the `r=5` stress limitation;
- **narrows interpretation:** no evidence here of a widespread strong-disorder
  breakdown across families and larger `s1_size` on the diagnostic `W>=8` sweep;
  the dominant coupling is **fixed-window localization sensitivity to
  `low_energy_count` / window definition** on a **ring small-size anchor**
  (`ipr_margin` down to `1e-4` does not rescue; nearby seeds `±10` fail only at
  anchor seed `9836055`).

Documentation rule: keep **stress-level rule classification** and **targeted
mechanistic diagnosis** explicit as two layers. Historical kernel-only mixed run
and baseline `v0.1.14-mvp-s2-s1-discretization-v2-full` remain preserved.

Non-claims:

- no continuum compactification;
- no `S6` / `S3 x S6`;
- no Standard Model;
- no physical chirality;
- no Witten/Lichnerowicz bypass.

## Localization gate v3 case-level stress: localized strong-disorder tail

Case-level v3 stress run (toy diagnostic only):

```text
reports/RUNS/20260513-213053_s1_discretization_v2_stress_v3
```

Observed `W>=8` tail:

- **six** case-level v3 failures, **all** `ring` family;
- concentrated at `alpha=0`, mostly `s1_size=8`, distinct seeds;
- classification in memo: targeted artifact candidate / localized unresolved v3
  limitation — **not** a cross-family general v3 breakdown.

Memos:

- `reports/S1_LOCALIZATION_WINDOW_V3_CASE_LEVEL_STRESS_NOTE.md`
- `reports/S1_LOCALIZATION_WINDOW_V3_STRONG_DISORDER_FAILURE_ANALYSIS.md`

Completed targeted diagnostic (ring anchors + cross-family/size/twist sweep):

```text
python scripts/s1_v3_ring_failure_diagnostic.py --seed-span 0
reports/RUNS/20260514-085316_s1_v3_ring_failure_diagnostic
reports/S1_V3_RING_FAILURE_DIAGNOSTIC.md
```

Recorded read (heuristic only; not a theorem):

- `diagnostic_label`: `candidate_ring_alpha0_regime_artifact`.
- Non-robust v3 cells on this diagnostic grid are **ring-only** and restricted to
  **`alpha=0`**, but the pattern is **not** confined to `s1_size=8` alone (the
  sweep includes a non-robust cell at `s1_size=32`; see `summary.md` /
  `failure_breakdown` in `metrics.json`).
- All **six** stress-documented anchors still sit in the `fragile_pass` /
  non-robust bucket at their original `(family, q, s1_size, alpha, W, seed)`.
- Optional next grid step (not run automatically here): widen `seed_span` or
  expand the `(alpha, s1_size)` ladder if you need a sharper kill-test between
  `alpha=0` regime artifact vs an unresolved ring-only v3 limitation.

Interpretation constraints:

- Baseline remains `v0.1.14-mvp-s2-s1-discretization-v2-full` (not promoted by
  this documentation layer).
- Historical kernel-only mixed comparison, v2 fixed-window reruns, v2 stress
  limitation (`realizations=5`), W=8 targeted diagnostic memos, and the
  `20260514-085316` ring-only v3 targeted sweep remain on record alongside this
  v3 stress diagnostic.

Non-claims:

- no continuum compactification;
- no `S6` / `S3 x S6` physical validation;
- no Standard Model;
- no physical chirality proof;
- no Witten/Lichnerowicz bypass.

## Product-discretized W4 smoke diagnostic (transition-regime follow-up)

Completed **smoke** targeted diagnostic for the product-discretized refinement
layer (toy only; not a baseline promotion):

```text
python scripts/s2_s1_product_discretized_w4_diagnostic.py
reports/RUNS/20260514-141503_s2_s1_product_discretized_w4_diagnostic
reports/S2_S1_PRODUCT_DISCRETIZED_W4_DIAGNOSTIC.md
```

Recorded classification:

- `w4_diagnostic_classification=transition_regime_sensitivity_ring_low_W_band`.

Smoke facts:

- **4** disordered **v3 non-robust** cells in smoke; **all** **`ring`**.
- **W=2: 2**, **W=4: 2**, **W=6: 0**, **W=8: 0** non-robust in this smoke run.
- **q0** false positives: **none** in this run.

Interpretation constraints:

- W4 smoke **supports** the **transition-regime sensitivity** interpretation for
  the medium caveat; it **does not erase** the product-discretized medium caveat
  or replace full/stress product-discretized planning.
- **`--full` W4** sweep (~3600 cases) remains **optional/pending**.
- Baseline remains `v0.1.14-mvp-s2-s1-discretization-v2-full`.

Non-claims:

- no continuum compactification;
- no `S6` / `S3 x S6` physical validation;
- no Standard Model;
- no physical chirality proof;
- no Witten/Lichnerowicz bypass.

## Product-discretized FULL diagnostic caveats (6615-case comprehensive grid)

Completed **full** product-discretized diagnostic (2026-05-15):

```text
python scripts/s2_s1_product_discretized_full.py
reports/RUNS/20260515-201150_s2_s1_product_discretized_full
reports/S2_S1_PRODUCT_DISCRETIZED_FULL_NOTE.md
reports/FULL_CAVEAT_ANALYSIS.md
```

Grid scope: **6615 cases** (3 S1 families × 7 monopole charges × 5 s1_sizes × 2
alpha × 6 disorder strengths × multiple seeds), ~16 hours runtime.

Classification: `product_discretized_full_diagnostic_complete`.

Core gates **PASSED**:

- q=0 false positive count: **0** (no spurious localization on monopole-free control)
- Hermiticity: all passed
- Shape consistency: all passed
- Reproducibility: passed
- Clean controls: 945 cases
- Disordered cases: 5670 cases
- Disorder contrast: available

**Caveat 1: Ring family alpha=0 small-lattice artifact (REFINED 2026-05-16)**

**Original scope (full run, 2026-05-15):** **51 failures** out of ~630 ring alpha=0
disordered cases (8.3% failure rate at s1_size<64).

**Breakdown (verified from metrics.json):**
- **37 cases (73%):** BOTH gates fail (kernel_only=False AND fixed_window=False) — complete localization failure
- **14 cases (27%):** Window-sensitive (kernel_only=False, fixed_window=True) — historical window-selection pattern

Total: 51 ring alpha=0 disordered cases fail kernel-only gate; 37 also fail fixed-window gate.

**Targeted follow-up (2026-05-16):**

Run: `reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/`  
Cases: **1349** (1029 ring + 320 reference), extending s1_size to 64 and 96.

**Decision Rule 1 outcome:**
- Failures at s1_size < 64: 51/777 = **6.6%**
- Failures at s1_size ≥ 64: 0/252 = **0.0%** (252 cases tested)
- **Verdict:** SMALL_LATTICE_ARTIFACT

**Lattice-size scaling (ring/alpha=0):**

| s1_size | Failures | Failure Rate |
|---------|----------|--------------|
| 8       | 25       | ~17.0%       |
| 16      | 1        | ~0.7%        |
| 24      | 19       | ~12.9%       |
| 32      | 3        | ~2.0%        |
| 48      | 3        | ~2.0%        |
| **64**  | **0**    | **0.0%** ✅  |
| **96**  | **0**    | **0.0%** ✅  |

**Interpretation (after follow-up):**

All 51 ring/alpha=0 failures from full run are **small-lattice discretization artifacts**
that vanish at s1_size≥64. Ring/alpha=0 at s1_size≥64 is **as robust as spectral_circle
and wilson_ring** (0% failure rate).

Ring discretization at alpha=0 (periodic boundary) requires **larger lattices** for
convergence. NOT a persistent structural limitation — convergence achieved, threshold
shifted to s1_size≥64.

**Production guideline:**
- Ring/alpha=0: s1_size ≥ 64 recommended
- Ring/alpha≠0: s1_size ≥ 32 sufficient (no failures in full run)
- Spectral_circle, wilson_ring: robust at all tested s1_size

Distinction from historical window-selection sensitivity:

- **Historical issue (2026-05-14, seeds 12051/12053/9836055):** kernel fail,
  fixed pass → **resolved (2026-05-15)** via implementation improvements →
  those seeds now pass
- **Full grid (2026-05-15) reveals two patterns:**
  1. **37 complete failures:** Both gates fail (small-lattice regime)
  2. **14 window-sensitive:** Historical pattern at different seeds (small-lattice regime)
- **Targeted follow-up (2026-05-16) confirms:** Both patterns are **lattice-size artifacts** (vanish at s1_size≥64)

**Caveat 2: v2/v3 gate disagreement (7 cases, all ring)**

Scope: **7 cases** where v2 (fixed-window) passes but v3 (window-robust) fails.

Pattern: ALL ring family, alpha=0.0, disordered.

Interpretation: v2 gate too permissive — passes cases that v3 correctly
identifies as window-sensitive. Suggests v3 should be primary gate for
production validation.

Impact on baseline:

- **Baseline PROMOTED:** `v0.1.15-s2-s1-product-discretized-full` (2026-05-16)
- **Previous baseline:** v0.1.14-mvp-s2-s1-discretization-v2-full
- Full diagnostic completed: 6615/6615 cases
- Targeted follow-up completed: 1349 cases, verdict=SMALL_LATTICE_ARTIFACT
- Refined caveat: ring/alpha=0 failures vanish at s1_size≥64
- Total failure rate (after refinement): 0.0% at recommended s1_size≥64
- Pytest suite: **203 passed, 1 warning** (8 new tests for follow-up)
- **Independent audit:** `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_INDEPENDENT_AUDIT.md`
  (verdict: `confirmed_with_corrections_needed`, corrections applied 2026-05-16)
- **Release notes:** `reports/RELEASE_NOTES_v0.1.15.md`

Recommendations (COMPLETED):

1. ~~Investigate ring family construction for alpha=0 case~~ → **COMPLETED:** Targeted follow-up confirms small-lattice artifact
2. Consider v3 as primary gate for production validation (still recommended)
3. ~~Test ring at larger s1_size (64, 96) to check lattice-size scaling~~ → **COMPLETED:** 0% failure rate at s1_size≥64
4. ~~Consider whether ring should be deprecated for alpha=0 periodic boundary~~ → **RESOLVED:** Ring/alpha=0 robust at s1_size≥64, deprecation not needed

Non-claims:

- no continuum compactification;
- no `S6` / `S3 x S6` physical validation;
- no Standard Model;
- no physical chirality proof;
- no Witten/Lichnerowicz bypass.

## Analytic spectrum unit tests: circular-validation risk mitigated

Prior risk: analytic Laplace / product-spectrum tests could degenerate into
self-consistency checks against the same helpers under test.

Mitigation: `tests/test_analytic_spectra.py` now includes **hardcoded reference
values** for `S2`/`S3`/`S6` eigenvalues (`ell=0..4`), radius scaling,
degeneracies, scalar curvature, and `S3 x S6` product checks, with comments
stating the anti-circular-validation intent. Production code unchanged.

Latest documented suite status: `pytest -q` -> **203 passed, 1 warning in
469.86s** (~7m50s; confirmed full suite 2026-05-16 after v0.1.15 promotion).

Non-claims:

- hardcoded regressions are not physical validation of `S6` / `S3 x S6` in a
  compactification model;
- not Standard Model;
- not physical chirality proof;
- not Witten/Lichnerowicz bypass.

## Graph Laplacian dumbbell tiny: null/weak signal (not a localization theorem)

Run: `reports/RUNS/20260514-130000_geometric_localization_dumbbell_tiny` with
`aggregate_verdict=dumbbell_null_or_weak_signal` and
`k_sensitivity_ok_by_throat={"0.35": true, "0.5": true}` (see
`reports/MILESTONE_GEOMETRIC_LOCALIZATION_DUMBBELL_TINY.md`). Per-case metrics
show **single connected component** and **graph pre-control gates passed**; the
aggregate verdict still classifies the dumbbell throat response as **null or
weak at the tiny default grid** — useful falsification bookkeeping, **not**
evidence of strong geometric localization or compactification physics.

Non-claims (dumbbell diagnostic):

- not a theorem of localization on the continuum;
- not validation of `S6` / `S3 x S6` or Standard Model structure;
- not physical chirality or Witten/Lichnerowicz bypass.
