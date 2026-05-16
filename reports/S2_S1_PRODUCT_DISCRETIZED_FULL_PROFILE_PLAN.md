# S2 x S1 Product-Discretized Full Profile Plan

## Purpose

This document defines a **planning-only** contract for the **next** product-discretized
refinement stage: a **full-profile** grid on the toy **S2 × S1** Kronecker-sum
Hamiltonian layer (`cc_toy_lab/spectral/s2_s1_product_discretized.py`,
`scripts/s2_s1_product_discretized.py`). It is written **after**:

- **Tiny** scaffold completion and audit (including **W = 0 / W = 8** clean–disorder
  contrast);
- **Medium** diagnostic completion (**1080 / 1080** cases,
  `reports/RUNS/20260514-125211_s2_s1_product_discretized_medium`);
- **Medium failure analysis** (`reports/S2_S1_PRODUCT_DISCRETIZED_MEDIUM_FAILURE_ANALYSIS.md`);
- **W4 smoke** transition-regime diagnostic
  (`reports/RUNS/20260514-141503_s2_s1_product_discretized_w4_diagnostic`);
- **Closure** of the **geometric-localization** branch at **tiny** resolution with a
  **null / weak** dumbbell verdict (`reports/MILESTONE_GEOMETRIC_LOCALIZATION_BRANCH_SUMMARY.md`).

The geometric-localization line did **not** strengthen into a positive toy signal at
tiny scale; the **product-discretized** line already carries **richer, recorded**
gate-level behavior (medium + W4 smoke). This plan therefore prioritizes **returning
planning and optional execution** to product-discretized **full-profile** work **without**
erasing historical **v2 / v3 / medium** limitations or promoting baseline from a plan
alone.

## Current Evidence

| Layer | Status (summary) |
| --- | --- |
| **Tiny scaffold** | Product-discretized tiny completed and audited; establishes operator wiring, artifact shape, and basic aggregates. |
| **W = 0 / W = 8 contrast** | Explicit clean–disordered contrast on tiny; supports interpreting disorder gates without conflating `W = 0` with disordered rows. |
| **Medium** | **1080 / 1080** cases completed; `classification=product_discretized_medium_diagnostic_complete`; localized caveats (e.g. **ring**, **v3** non-robust band) documented in medium milestone and failure analysis. |
| **W4 smoke** | Completed; supports **transition-regime sensitivity** reading for medium caveat; **does not** remove medium limitations or replace full-profile/stress planning. |
| **Geometric branch (tiny)** | Closed with **null / weak** dumbbell signal; **not** a reason to abandon product-discretized work — rather a reason to **re-focus** effort on the line with stronger existing toy diagnostics. |

**Baseline (unchanged in this plan):** `v0.1.14-mvp-s2-s1-discretization-v2-full`.

**Latest documented test suite (informational):** `pytest -q` → **187 passed**
(after product-discretized guarded full-runner tests; wall clock varies by machine).

## Proposed Full Grid

All combinations are **one analysis cell** per tuple
`(q, s1_family, s1_size, alpha, W, seed)` with **`low_energy_count`** swept **inside**
the same contract as medium (see **Caveat Tracking** for per–`low_energy_count`
bookkeeping in metrics, not as a separate outer axis in the **6615** count — implementers
must align with existing `ProductDiscretizedConfig` / runner semantics).

| Parameter | Values |
| --- | --- |
| `q_values` | `(0, 1, -1, 2, -2, 3, -3)` |
| `s1_families` | `("spectral_circle", "ring", "wilson_ring")` |
| `s1_sizes` | `(8, 16, 24, 32, 48)` |
| `alpha_values` | `(0.0, 0.25, 0.5)` |
| `W_values` | `(0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0)` |
| `seeds` | `(123, 456, 789)` |
| `low_energy_count_values` | `(4, 6, 8, 10, 12)` |

**Note:** The **6615** count below is the Cartesian size of the **outer** grid
**(q, family, size, alpha, W, seed)**. The implementation must record how
`low_energy_count_values` are applied (same pattern as medium: **per-cell sweep**
inside metrics, **not** multiplying 6615 by 5 unless explicitly decided and
documented in a future revision of this plan).

## Estimated Size

**Outer grid (explicit):**

`7` **q** × `3` **families** × `5` **s1_sizes** × `3` **alpha** × `7` **W** × `3` **seeds**
**= 6615** cases.

This is **much heavier** than medium (**1080** cells). It **must not** be launched
accidentally: require **`--full --dry-run`**, explicit case-count confirmation, and
operator sign-off before any long run.

## Caveat Tracking

Future full-profile **metrics** (and/or derived summaries) should expose or support
derivation of at least:

| Metric / bucket | Role |
| --- | --- |
| `q0_false_positive_count` | `q = 0` must not fake inherited-kernel / twist signals. |
| `ring_alpha0_cases_count` | Denominator for ring at `alpha = 0` scrutiny. |
| `ring_alpha0_failure_count` | Failures concentrated in ring / `alpha = 0` (historical stress pattern). |
| `transition_band_failure_count` | Failures with **`W` in `{2.0, 4.0}`** (transition band). |
| `mid_band_failure_count` | Failures with **`W = 6.0`** (mid band). |
| `strong_disorder_failure_count` | Failures with **`W >= 8.0`**. |
| `v2_vs_v3_disagreement_count` | Where v2 and v3 localization bookkeeping disagree. |
| `v3_failure_counts_by_family/W/alpha/s1_size/q/seed` | Stratified tables for localization window v3. |

These buckets **preserve** medium / W4 smoke **interpretation** and avoid collapsing
distinct failure modes into a single scalar.

## Required Gates

Full-profile runs must continue to enforce the same **toy diagnostic** gates as the
refinement layer (non-exhaustive list aligned with medium / spec narrative):

- **Hermiticity** (numerical tolerance documented in config).
- **Shape consistency** (dimensions, per-family operator layout).
- **Reproducibility** (seeded spectra / recorded tolerances).
- **`q` control** (nonzero `q` inherited-kernel / monopole proxy behavior per family).
- **`q = 0` control** (`q0_false_positive_count` must remain **zero** for promotion
  discussions).
- **Disorder contrast** (`W = 0` vs `W > 0` rows where applicable).
- **S1 non-spectator** (twist / flux nontriviality where defined).
- **Flux response** (twist knobs change observables in the expected toy sense).
- **v2 fixed-window localization** (`localization_gate_v2_passed` bookkeeping).
- **v3 window-sweep localization** (case-level v3 stress semantics as already used
  in medium / W4 narrative).
- **No global chiral index headline** for this odd-dimensional product toy (same
  non-claim as existing bridge documentation).

## Decision Rules

1. **If `q0_false_positive_count > 0`:** **stop** — treat as **control failure**;
   no interpretation of localization bands until resolved.
2. **If `strong_disorder_failure_count = 0`** and remaining failures are concentrated
   in **`ring`** with **`W ∈ {2, 4}`**:** classify as **transition-regime ring caveat**
   (consistent with medium / W4 smoke story); do **not** generalize to “all families
   broken.”
3. **If failures spread across families at `W >= 8`:** label **`unresolved_product_discretized_strong_disorder_limitation`** (or equivalent) — distinct from ring-only
   transition caveat.
4. **If full-profile contradicts medium / W4 smoke** (e.g. new failure modes or
   opposite band structure): **targeted follow-up** required before any baseline
   promotion talk.
5. **If full-profile supports medium / W4 smoke** (same buckets, no new control
   failure): **consider** a **`v0.1.15`** bookkeeping tag **only after** an
   **independent audit** and explicit release process — **not** from this plan alone.

## Runtime Plan

Recommended execution order for a **future** implementation (not executed by this
document):

1. Implement **`--full`** and **`--full --dry-run`** in
   `scripts/s2_s1_product_discretized.py` (or equivalent entrypoint).
2. Confirm **`--full --dry-run` reports exactly `6615` cases** (outer grid above).
3. Optionally run a **smoke / subset** full-profile (e.g. one seed, reduced sizes)
   before the main job.
4. Run the **background full** job with **structured logging** and a **single**
   canonical output directory (no accidental duplicate full runs).
5. Enforce **no duplicate runs** for the same grid hash (config + code version).
6. **Artifact verification** (`config.json`, `metrics.json`, `data.npz`,
   `summary.md`, figures policy) **before** narrative interpretation or milestone
   updates.

## Future Artifacts

Expected under `reports/RUNS/<timestamp>_s2_s1_product_discretized_full/` (or the
project’s chosen naming convention):

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/.placeholder` (or real figures if enabled)
- Optional **run log** (stdout/stderr capture) for long jobs

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** physical validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.

## Acceptance Criteria for Future Implementation

When the full-profile feature is implemented (separate change set from this plan):

- **`--full`** and **`--full --dry-run`** exist on the product-discretized runner.
- **`--full --dry-run`** reports **`6615`** outer-grid cases (per this plan).
- **Medium** behavior and artifacts **unchanged** by default (no silent regression of
  medium code paths).
- After a real run: **artifacts saved** and checksum / presence checks documented.
- **Baseline unchanged** unless a separate review explicitly promotes it.
- **`pytest`** passes at repo standard (e.g. **187** tests after guarded-runner wiring).
- **No overclaim** in milestones or validation status updates.

---

**Historical layers preserved on purpose:** kernel-only mixed full comparison,
v2 fixed-window rerun and `window_selection_sensitivity` for `ring`, v2 stress
limitations, v3 case-level stress, medium caveat, W4 smoke — this plan **adds** a
full-profile contract; it does **not** erase prior limitations or conclusions.
