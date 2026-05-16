# S1 localization window v3 — design memo

## Status

**Design only.** No implementation in this change. Baseline remains
`v0.1.14-mvp-s2-s1-discretization-v2-full` and is **not** promoted or altered by
this memo.

## 1. Motivation

### What v2 fixed-window improved

The historical full multi-family comparison under the **kernel-only**
low-energy window remained `mixed_or_limiting` because `ring` disagreed with
the reference family on the kernel-selected low-energy IPR gate. The **v2**
diagnostic introduced an explicit **fixed-window** rule: compare disordered vs
clean localization using the same indices chosen by **smallest-|λ|** on each
side (`fixed_low_energy_window`), so family-level summaries could align with a
single, reproducible window choice.

That choice reduced ambiguity between “kernel-aware” and “spectral tail”
selection and produced a clean **family-level** `localization_gate_v2_passed`
picture on the promoted v2 full comparison profile.

### Why sensitivity to `low_energy_count` still appears

The fixed-window construction still depends on a **scalar hyperparameter**
`low_energy_count`: how many smallest-|λ| modes define the window. For product
operators with **near-null structure** and small `S1` discretization size, the
index set for the first `k` eigenvalues can cross a qualitative boundary as `k`
moves (e.g. inclusion/exclusion of modes that sit differently in the `S1`
marginal). The targeted `W=8` diagnostic showed that a single anchor case can
**flip** the fixed-window gate while kernel-only stays “passed”, purely by
moving `low_energy_count` within a modest sweep. That is not a claim of
physical localization failure; it is evidence that a **single-`k` gate** can be
**window-definition fragile** even when the physics-toy operator is smooth in
other senses.

**v3 goal:** define a localization diagnostic that does **not** hinge on one
value of `low_energy_count`, by aggregating evidence across a **small, explicit
window sweep** and surfacing **robustness vs fragility** as first-class outputs.

## 2. Proposed v3 metric (window sweep)

For each localization case (same tuple as today: family, `q`, `s1_size`,
twist `α`, disorder strength, perturbation, realization seed, mode pair
clean vs geometric_weight):

1. Fix a finite ordered list of window widths:

   ```text
   low_energy_count_values = (4, 6, 8, 10, 12)
   ```

2. For each `k` in that tuple, recompute the clean and disordered observations
   (or at minimum the IPR quantities needed for the gate) using the **same**
   fixed-window selection rule as v2, but with `low_energy_count = k`.

3. For each `k`, evaluate the **per-window fixed-window gate** using the same
   inequality shape as v2 (disordered fixed-window IPR vs clean fixed-window IPR,
   with the same `ipr_margin` policy as the project chooses for v2 — v3 does not
   redefine the margin in this memo unless a later spec says otherwise).

4. Optionally (future spec): apply the same sweep to **kernel-only** IPR if a
   dual-track summary is desired; v3 primary headline remains **fixed-window
   robustness across `k`**.

**Non-goals in v3:** changing the operator, disorder model, or `S2` factor;
changing the promoted baseline; erasing historical runs.

## 3. Proposed outputs (per case or aggregated)

Per case (and optionally rolled up by family / stress cell):

| Output | Definition (proposal) |
| --- | --- |
| `pass_rate_across_windows` | Fraction of `k` in `low_energy_count_values` for which the per-window fixed-window gate passes (e.g. `4/5`). |
| `min_ipr_delta` | `min_k ( disordered_fixed_window_ipr(k) - clean_fixed_window_ipr(k) )`. |
| `median_ipr_delta` | median of the same deltas over the sweep. |
| `window_sensitivity_score` | e.g. `1 - pass_rate_across_windows`, or `max_k delta(k) - min_k delta(k)`; final formula should be pinned in implementation spec so it is monotone with obvious fragility examples. |
| `window_robust_localization_passed` | Boolean from **decision rules** (section 4), not from a single `k`. |
| `unstable_window_cases` | List of `k` (and optional diagnostics) where the per-window gate fails; attach to stress-style case records for debugging. |

**Reporting hygiene:** always record `kernel_count` (clean and disordered)
**separately** from window sweep outcomes so near-null / doubling phenomena remain
visible and are not “averaged away” by robustness scores.

## 4. Decision rules (example — tunable before coding)

Let `N = len(low_energy_count_values)` (here `N = 5`). Let `P` be the number of
`k` that pass the per-window fixed-window gate. Let `margin` be the same IPR
margin policy as v2 unless a project-wide margin revision is approved separately.

**Robust pass (proposal):**

- `P >= ceil(0.8 * N)` (for `N=5`, at least **4/5** windows pass), **and**
- `median_ipr_delta > margin` (median taken over the sweep, comparing
  disordered vs clean fixed-window IPR at each `k`).

**Fragile pass (proposal):**

- `ceil(0.4 * N) <= P < ceil(0.8 * N)` (for `N=5`, **2–3/5** pass), **or**
- robust pass inequalities fail but `min_ipr_delta > 0` (all windows show the
  “right direction” but some miss strict margin).

**Fail (proposal):**

- `P < ceil(0.4 * N)` (for `N=5`, **fewer than 2/5** pass), **or**
- `min_ipr_delta <= 0` (at least one window contradicts the localization
  direction used by the gate).

**Always-on side channels:**

- Record `kernel_count` clean/disordered and any existing v2 side flags
  (`window_selection_sensitivity` between kernel-only vs fixed-window at the
  reference `k_ref`, if retained) **without** letting them overwrite the
  historical kernel-only record.

These thresholds are **design placeholders**; the first implementation should
expose them as named constants or config fields so stress profiles can tune
them without another memo revision.

## 5. Treatment of `ring` / fermion doubling

- **Kernel-only track** and **fixed-window track** must remain **separately
  reported** end-to-end. v3 is a refinement on how **fixed-window** evidence is
  aggregated across `k`; it must **not** erase or rewrite the historical
  kernel-only `mixed_or_limiting` full comparison artifact.
- **Ring / doubling:** any `ring`-specific sensitivity that appears as
  kernel-only vs fixed-window disagreement at a reference `k` should remain
  visible (today’s `window_selection_sensitivity` style diagnostics). v3 adds a
  **second axis**: sensitivity across **`k`**, not only across window *mode*
  (kernel vs fixed).
- v3 should **not** be interpreted as a new “global pass” that supersedes v2 on
  the baseline tag until a deliberate baseline review says so.

## 6. Test plan (acceptance-oriented)

1. **Anchor regression (known fragile point):** the exact `W=8` stress anchor
   (`ring`, small `s1_size`, stress-aligned seed family) should register as
   **window-sensitive** under v3: e.g. non-trivial `window_sensitivity_score`,
   `unstable_window_cases` non-empty, and `window_robust_localization_passed`
   false **or** fragile per rules — but the case should **not** be classified as
   a “generic fail all windows” unless the sweep actually shows that pattern.

2. **Reference stability:** `spectral_circle` and `wilson_ring` cells on the
   same toy grids used for stress/comparison should be **stable across windows**
   (high `pass_rate_across_windows`, bounded sensitivity score), modulo
   expected numerical noise limits to be set in tests.

3. **`q = 0` control:** the `q_control` / “no inherited kernel signal” logic must
   remain protected; v3 outputs must not introduce a new way to accidentally flip
   `q=0` conclusions.

4. **Language guard:** tests and docs for v3 must avoid **global chiral index**
  headline language for the `S2 x S1` toy product; v3 remains a **localization
  window robustness** diagnostic only.

5. **Regression harness:** golden tests on a **tiny** profile (small grid, 1–2
   seeds) before any full rerun.

## 7. Scientific non-claims

- Not continuum compactification.
- Not `S6` / `S3 x S6`.
- Not Standard Model physics.
- Not a proof of physical chirality.
- Not a bypass of Witten/Lichnerowicz-type obstructions.

## 8. Implementation order (when coding is allowed)

1. **Design lock** — freeze this memo’s outputs and decision rules (or explicitly
   version them as v3.0 / v3.1).
2. **Unit tests** — pure functions for sweep aggregation, decision boundaries,
   and monotonicity sanity on synthetic IPR vectors.
3. **Tiny runner / CLI stub** — optional `scripts/...` behind a test profile,
   writing minimal artifacts under `reports/RUNS/..._tiny`.
4. **Integration** — wire into comparison/stress pipelines only after (1)–(3)
   pass in CI.
5. **Full rerun** — only after tests pass; compare v2 vs v3 summaries side by
   side without deleting historical runs.

---

**References (context only, not modified by this memo):**

- Baseline: `v0.1.14-mvp-s2-s1-discretization-v2-full`
- Historical kernel-only full: `reports/RUNS/20260512-191838_s1_discretization_comparison_full`
- v2 full rerun: `reports/RUNS/20260512-203723_s1_discretization_comparison_full`
- Stress `realizations=5`: `reports/RUNS/20260513-001436_s1_discretization_v2_stress`,
  memo `reports/S1_V2_STRESS_FAILURE_ANALYSIS_realizations5.md`
- Targeted `W=8` diagnostic: `reports/RUNS/20260513-082348_s1_v2_w8_failure_diagnostic`,
  memo `reports/S1_V2_W8_FAILURE_DIAGNOSTIC.md`
