# S2 × S1 Product-Discretized Refinement Spec

## Purpose

This refinement phase sits **after** milestone `v0.1.14` (`reports/MILESTONE_v0.1.14_S2_S1_VALIDATION_SUMMARY.md`) and **before** any serious move toward higher-dimensional targets such as `S6` or `S3 x S6`. The existing `S2 x S1` bridge (`cc_toy_lab/spectral/s2_s1_product.py`) is a controlled **finite-mode product-operator toy** with explicit v2/v3 localization bookkeeping. The product-discretized layer asks a narrower question:

> If the S1 factor enters through an **additive Kronecker-sum Hamiltonian** built from the same validated S2 monopole proxy and the same `S1` discretization families, do the **same classes of toy observables** (kernels, IPR, localization gates, twist response) remain coherent — without pretending the construction is a continuum Dirac proof?

This is a **refinement bridge**, not physical compactification.

## Current Baseline

- **Baseline (unchanged in this phase):** `v0.1.14-mvp-s2-s1-discretization-v2-full`
- **Latest documented tests:** `pytest -q` → **132 passed** (see `reports/VALIDATION_STATUS.md`).

## Prior Results Preserved

The following remain **authoritative historical layers** and must **not** be erased or contradicted by the refinement scaffold:

- **Kernel-only mixed** full `S1` discretization comparison (`reports/RUNS/20260512-191838_s1_discretization_comparison_full`).
- **v2 fixed-window** family-level rerun and `window_selection_sensitivity` bookkeeping for `ring`.
- **v2 stress** limitation (`realizations=5`, case-level `v2_limitation`) and targeted **W=8** diagnostic memos.
- **v3 quick/full** comparison narrative and **v3 case-level stress** (`reports/RUNS/20260513-213053_s1_discretization_v2_stress_v3`) with **six** localized `W>=8` failures (**all `ring`**, **`alpha=0` concentration**).
- **Targeted ring diagnostic** (`reports/RUNS/20260514-085316_s1_v3_ring_failure_diagnostic`, heuristic label `candidate_ring_alpha0_regime_artifact`).
- **Analytic spectrum** unit-test hardening against circular validation (`tests/test_analytic_spectra.py`).

The refinement adds a **parallel operator family** for comparison; it does not replace `s2_s1_product` metrics definitions.

## Proposed Operator (Option A — first implementation)

**Toy product-discretized Hamiltonian** (Kronecker sum, **no default coupling terms**):

\[
H_{\text{product}} = H_{S2,\text{proxy}} \otimes I_{S1} + I_{S2} \otimes P_{S1}
\]

- **`H_{S2,proxy}`**: Hermitian proxy built from the **existing finite-mode** monopole Dirac operator `D_{S2}(q)` as  
  \(H_{S2,\text{proxy}} = D_{S2}(q)^2\)  
  (same `q` / `cutoff` / `radius` pipeline as the positive-control sector; **not** a new continuum lattice Dirac construction).
- **`P_{S1}`**: Hermitian `S1` operator from `cc_toy_lab.spectral.s1_discretizations.build_s1_operator` for  
  `spectral_circle` | `ring` | `wilson_ring`, with the same toy disorder modes used elsewhere (`clean`, `geometric_weight`, …).
- **`coupling_terms`**: reserved; **default off** (zero).

**Odd-dimensional note:** do **not** headline a **global chiral index** on the full `S2 x S1` product (odd total dimension). Report **kernel counts**, **S2 kernel chirality content** lifted from the monopole chirality vector (diagnostic only), and **S1** localization / spectator diagnostics.

**Option B (future only):** geometric sampled `S2` graph × `S1` — document-only here; no heavy graph-`S2` implementation in this milestone.

## Observables

Each assessed grid cell (after clean vs disordered pairing) should surface (names aligned with existing JSON fields **where possible**):

| Observable | Role |
| --- | --- |
| `kernel_count` | near-null space of `H_product` at chosen tolerance |
| `min_abs_eigenvalue` | spectral floor |
| `s1_low_energy_ipr` / `s1_fixed_window_ipr` | S1 marginal IPR (same projection geometry as `s2_s1_product`) |
| `kernel_only_localization_gate_passed` | clean vs `geometric_weight` IPR (kernel-augmented low-energy selection) |
| `fixed_window_localization_gate_passed` | fixed-window low-energy IPR gate |
| `localization_gate_v2_passed` | alias of fixed-window gate for compatibility |
| `pass_rate_across_windows` | v3-style sweep over `low_energy_count_values` |
| `window_sensitivity_score` | `1 - pass_rate` |
| `localization_gate_v3_classification` | aggregated v3 label (`fail` / `fragile_pass` / …) |
| `window_robust_localization_passed` | robust pass flag |
| `s1_not_spectator` | response to `s1_size` change at matched parameters |
| `flux_response_observed` | response to twist / `alpha` probe |
| `pbc_apbc_difference` | diagnostic delta between `alpha=0` and `alpha=0.5` slices (APBC-style twist proxy) |
| `q0_control_passed` | `q=0` must not show a spurious “inherited kernel” success pattern |
| `ring_alpha0_caveat_detected` | explicit flag when `(family==ring, alpha==0, W>0)` — keeps the v0.1.14 caveat visible |

## Gates (tiny profile)

| Gate | Rule |
| --- | --- |
| Hermiticity | \(\|H - H^\dagger\|_\infty \le 10^{-10}\) (float noise budget) |
| Shape | `H.shape == (n_s2 * n_s1,) * 2` deterministic from `(q, cutoff, s1_size, family)` |
| Reproducibility | fixed `seed` reproduces identical `min_abs_eigenvalue` / `kernel_count` for same case |
| `q=0` control | no false inherited-kernel headline; kernel bookkeeping consistent with toy `q=0` monopole slice |
| `S1` non-spectator | `s1_not_spectator` computed and stored |
| Flux / twist | `flux_response_observed` computed |
| Localization fields | v2 + v3-compatible keys present in `metrics.json` |
| No global chiral index headline | metrics and `summary.md` must not claim `global_chiral_index` or `physical_chirality_proven` |

## Tiny Profile (implemented first)

| Parameter | Values |
| --- | --- |
| `q_values` | `(0, 1, -1)` |
| `s1_families` | `("spectral_circle", "ring", "wilson_ring")` |
| `s1_sizes` | `(8, 16)` |
| `alpha_values` | `(0.0, 0.5)` |
| `W_values` | `(0.0, 8.0)` |
| `seeds` | `(123,)` |
| `low_energy_count_values` | `(4, 6, 8, 10, 12)` |
| `cutoff` | `2` |
| `s1_mode_clean` | `"clean"` |
| `s1_mode_disordered` | `"geometric_weight"` |

## Full Profile

**Document only.** No full-grid or stress runs in this phase; do not promote baseline on partial grids.

## Failure Interpretation

If the product-discretized refinement shows systematic gate failures:

- classify as **operator-refinement limitation** or **representation mismatch** between Dirac-product and Hamiltonian-sum toy;
- **do not** erase or downgrade validated `v0.1.14` `s2_s1_product` results;
- **do not** claim “theory failure” of compactification — the scope is toy diagnostics only.

## Scientific Non-Claims

This refinement **does not**:

- prove **continuum compactification**;
- physically validate **`S6`** or **`S3 x S6`**;
- derive the **Standard Model**;
- prove **physical chirality**;
- bypass **Witten/Lichnerowicz** no-go theorems.
