# S2 x S1 Product Implementation Spec

## Status

- Project: `GeoSpectra Lab / Covariant Compactification Toy Lab`
- Baseline context: `v0.1.11-mvp-s2-graph-intermediate-quick`
- Scope: implementation specification only
- This document does not change the project baseline and does not make a new scientific claim.

## Purpose

The current `S2 x graph` bridge is useful because it combines:

- the verified `S2` monopole positive control;
- the verified toy Dirac negative control;
- a first combined index-plus-localization toy benchmark.

However, the graph sector is still artificial. In the current bridge, the
product operator is effectively `D_S2(q) ⊗ I_graph`, while the graph
localization diagnostic is external to the operator rather than a true
geometric product direction.

The next experiment should replace that artificial selector with a toy
`S2 x S1` spectral-circle product:

```text
D_{S2xS1} = D_{S2}(q) ⊗ I_{S1} + Gamma_{S2} ⊗ P_{S1}(alpha, W)
```

This is the next logical step because it:

1. keeps the verified `S2` monopole sector as the topological anchor;
2. introduces a real product-space factor instead of a graph selector;
3. tests whether low-energy structure responds to boundary twist and circle
   inhomogeneity;
4. stays below any `S6` or `S3 x S6` claim.

## Conceptual Constraint

`S2 x S1` is odd-dimensional. Therefore, the old full-product global chiral
index used in the `S2 x graph` bridge must not be the headline metric here.

The implementation must not present the result as:

- a global chiral index theorem for the full product;
- a protected physical chirality claim;
- a compactification proof.

Instead, the primary observables are:

- `kernel_count`;
- `s2_zero_mode_chirality_content`;
- PBC/APBC lifting behavior;
- `min_abs_eigenvalue`;
- `s1_low_energy_ipr`;
- mean `r`-statistics on positive eigenvalues;
- `flux_response_observed`;
- `s1_not_spectator`.

## Operator Definition

### S2 Sector

Reuse the existing finite-mode monopole control from
`cc_toy_lab/spectral/dirac_monopole_s2.py`:

```text
(D_S2(q), Gamma_S2) = build_dirac_monopole_operator(q=q, cutoff=cutoff)
```

This remains the only source of inherited topological zero modes.

### S1 Sector

Implement a Hermitian spectral-circle operator:

```text
P_S1(alpha, W) = P_clean(alpha) + V_mode(W)
```

Where:

- `alpha = 0.0` means periodic boundary conditions (PBC);
- `alpha = 0.5` means antiperiodic boundary conditions (APBC);
- `W` controls inhomogeneity strength.

### Clean Spectral-Circle Operator

Use a size-`N` Fourier basis on the circle. Let:

- `N = s1_size`;
- `R = s1_radius`;
- Fourier mode labels `m`;
- twisted momenta `k_m = (m + alpha) / R`.

Define the dense unitary DFT matrix `F` and build:

```text
P_clean(alpha) = F^* diag(k_m) F
```

Properties required:

- Hermitian to numerical tolerance;
- exact dependence on `alpha`;
- no disorder or inhomogeneity in `clean` mode.

### S1 Inhomogeneity Modes

The MVP should support:

#### `clean`

```text
V_mode(W) = 0
```

Notes:

- `W` is accepted but ignored;
- use this as the zero-inhomogeneity reference.

#### `gauge_phase`

Interpret this as a static circle connection added in position space:

```text
V_mode(W) = diag(A_j)
```

Where:

- `A_j` is a real-valued zero-mean random field on `S1`;
- scale of `A_j` is proportional to `W`;
- the operator remains Hermitian.

This mode is intended to test whether a circle-sector background field shifts
the low-energy structure without introducing a fake inherited kernel.

#### `geometric_weight`

Interpret this as a nonuniform circle metric density:

```text
G = diag(exp(eta_j))
A = G^{-1/2} P_clean G^{-1/2}
P_weighted = 0.5 * (A + A^*)
V_mode(W) = P_weighted - P_clean
```

Operationally, the implementation may use any equivalent Hermitian weighted
construction, provided it is recorded clearly in `summary.md` and
`metrics.json`.

This mode is the primary localization/inhomogeneity mode for the MVP and is
expected to drive `S1` low-energy IPR growth.

### Full Product Operator

Build:

```text
D_total = kron(D_S2(q), I_S1) + kron(diag(Gamma_S2), P_S1(alpha, W))
```

Requirements:

- Hermitian to numerical tolerance;
- shape `(dim_S2 * N_S1, dim_S2 * N_S1)`;
- explicit dependence on `q`, `cutoff`, `s1_size`, `alpha`, `mode`, `W`;
- optional tiny `S2`-chiral perturbation for stability checks.

### Optional Perturbation

Retain the existing tiny chiral-preserving perturbation logic from the `S2`
sector benchmark:

- `perturbation = 0.0` reference;
- `perturbation = 1e-5` stress test.

This perturbation must:

- preserve Hermiticity;
- preserve the `S2` chirality bookkeeping;
- not be used to manufacture or remove the inherited kernel signal.

## Primary Observables

### Observation-Level Metrics

Each observation should record at least:

| Field | Meaning |
| --- | --- |
| `q` | Monopole charge from the `S2` sector. |
| `cutoff` | Finite-mode `S2` cutoff. |
| `s1_size` | Number of circle degrees of freedom. |
| `boundary_twist` | `0.0` for PBC, `0.5` for APBC. |
| `s1_mode` | `clean`, `gauge_phase`, or `geometric_weight`. |
| `disorder` | Circle inhomogeneity strength `W`. |
| `perturbation` | Small `S2`-sector perturbation magnitude. |
| `seed` | Realization seed. |
| `kernel_count` | Number of eigenvalues with `abs(lambda) <= zero_tolerance`. |
| `s2_n_plus_in_kernel` | Count of kernel states with positive `S2` chirality expectation above threshold. |
| `s2_n_minus_in_kernel` | Count of kernel states with negative `S2` chirality expectation below threshold. |
| `ambiguous_kernel_states` | Kernel states not classifiable by the chirality threshold. |
| `min_abs_eigenvalue` | Smallest absolute eigenvalue of the full operator. |
| `max_kernel_abs_eigenvalue` | Largest `abs(lambda)` among states classified as kernel. |
| `mean_r_positive` | Mean adjacent-gap ratio on filtered positive eigenvalues. |
| `s1_low_energy_ipr` | Mean IPR of `S1` marginals for the low-energy window. |
| `flux_response` | Magnitude of lowest-mode shift under a small `alpha` change. |
| `zero_tolerance` | Numerical threshold used to define kernel. |
| `classification` | Human-readable status label for this observation. |

### How To Compute `s1_low_energy_ipr`

For each low-energy eigenvector `psi`:

1. reshape `psi` into `(dim_S2, N_S1)`;
2. compute the `S1` marginal probability:

```text
rho_S1(j) = sum_a |psi[a, j]|^2
```

3. compute:

```text
IPR_S1 = sum_j rho_S1(j)^2
```

4. average over the low-energy window.

This is the main replacement for the old graph-selector IPR.

### Low-Energy Window Rule

The implementation must use one explicit rule and save it:

- first include exact-kernel states if any;
- otherwise choose the `k` states with smallest `abs(lambda)`;
- recommended default: `k = min(low_energy_window, dimension)`.

## Headline Assessments

Each aggregated assessment should answer:

1. Does `q = 0` remain a null inherited-kernel control?
2. Does PBC preserve a kernel signal for `q != 0` in the clean circle sector?
3. Does APBC lift the exact zero sector?
4. Does `alpha` move the lowest modes?
5. Does the circle sector show low-energy IPR growth under `geometric_weight`?
6. Does increasing `s1_size` change structure beyond trivial multiplicity?

## Dataclasses

### `S2S1ProductConfig`

Required fields:

| Field | Proposed type | Proposed default |
| --- | --- | --- |
| `q_values` | `tuple[int, ...]` | `(0, 1, -1)` |
| `cutoff` | `int` | `2` |
| `s1_sizes` | `tuple[int, ...]` | `(8, 16)` |
| `boundary_twists` | `tuple[float, ...]` | `(0.0, 0.5)` |
| `s1_modes` | `tuple[str, ...]` | `("clean", "gauge_phase", "geometric_weight")` |
| `disorder_values` | `tuple[float, ...]` | `(0.0, 2.0, 8.0)` |
| `perturbation_values` | `tuple[float, ...]` | `(0.0, 1e-5)` |
| `realizations` | `int` | `3` |
| `seed` | `int` | project-specific fixed seed |
| `s1_radius` | `float` | `1.0` |
| `zero_tolerance` | `float` | `1e-7` |
| `zero_tolerance_scan` | `tuple[float, ...]` | `(1e-8, 1e-7, 1e-6)` |
| `chirality_threshold` | `float` | `0.5` |
| `positive_floor` | `float` | `1e-8` |
| `low_energy_window` | `int` | `8` |
| `flux_probe_delta` | `float` | `0.05` |
| `algebra_tolerance` | `float` | `1e-8` |
| `note` | `str` | short scientific warning |

### `S2S1Observation`

This dataclass should represent one concrete run point and contain the metrics
listed in the observation table above.

### `S2S1Assessment`

Required fields:

| Field | Meaning |
| --- | --- |
| `q` | `S2` monopole charge. |
| `s1_size` | Circle resolution used for the assessment. |
| `s1_mode` | Circle inhomogeneity mode. |
| `weak_disorder` | Reference weak `W`. |
| `strong_disorder` | Reference strong `W`. |
| `pbc_kernel_count` | Mean kernel count at `alpha=0.0`. |
| `apbc_kernel_count` | Mean kernel count at `alpha=0.5`. |
| `pbc_min_abs_eigenvalue` | Mean smallest absolute eigenvalue under PBC. |
| `apbc_min_abs_eigenvalue` | Mean smallest absolute eigenvalue under APBC. |
| `weak_s1_ipr` | Low-energy `S1` IPR at weak disorder. |
| `strong_s1_ipr` | Low-energy `S1` IPR at strong disorder. |
| `flux_response_observed` | Whether the flux/twist probe changes lowest modes. |
| `pbc_gate_passed` | Whether PBC preserves the expected inherited kernel signal. |
| `apbc_gate_passed` | Whether APBC lifts the exact zero sector. |
| `localization_gate_passed` | Whether `S1` low-energy IPR increases under `geometric_weight`. |
| `s1_not_spectator` | Whether circle resolution changes low-energy structure beyond multiplicity. |
| `threshold_stable` | Whether kernel conclusions survive the tolerance scan. |
| `classification` | Final assessment label. |

## Required Functions

### `build_s1_spectral_operator(...)`

Responsibility:

- build `P_S1(alpha, W)` for one `s1_size`, `alpha`, `mode`, and `seed`;
- return a dense Hermitian matrix and optional metadata if helpful.

Inputs should include:

- `s1_size`;
- `boundary_twist`;
- `mode`;
- `disorder`;
- `seed`;
- `s1_radius`.

Hard requirements:

- deterministic for a fixed seed;
- explicit mode handling;
- Hermitian to numerical tolerance;
- records enough information to explain the construction in `summary.md`.

### `build_s2_s1_product_operator(...)`

Responsibility:

- reuse `build_dirac_monopole_operator`;
- assemble the full product operator;
- optionally apply the tiny perturbation;
- return the operator plus the lifted `S2` chirality observable.

Return shape:

```text
(operator, s2_chirality_lifted)
```

Where `s2_chirality_lifted` is a length-`dim_total` vector suitable for kernel
chirality expectation calculations.

### `analyze_s2_s1_product(...)`

Responsibility:

- diagonalize the operator;
- classify kernel states by `zero_tolerance`;
- compute `S2` chirality content of the kernel;
- compute `min_abs_eigenvalue`;
- compute positive-spectrum `r`-statistics;
- compute `S1` low-energy IPR;
- compute a small `alpha -> alpha + flux_probe_delta` response diagnostic;
- emit one `S2S1Observation`.

### `run_s2_s1_product_benchmark(...)`

Responsibility:

- loop over `q`, `s1_size`, `alpha`, `mode`, `W`, `perturbation`, `realization`;
- collect observations;
- aggregate points and assessments;
- compute global gates;
- optionally call artifact saving.

Expected pattern:

- mirror the existing style of `run_s2_graph_product_benchmark(...)`;
- return a result object or a simple dataclass wrapper if needed later.

### `save_s2_s1_run_artifacts(...)`

Responsibility:

- create output directory;
- write `config.json`, `metrics.json`, `data.npz`, `summary.md`;
- save required figures;
- save enough run metadata for reproducibility.

## File and Module Layout

### `cc_toy_lab/spectral/s2_s1_product.py`

This module should contain:

- dataclasses;
- `build_s1_spectral_operator(...)`;
- `build_s2_s1_product_operator(...)`;
- `analyze_s2_s1_product(...)`;
- `run_s2_s1_product_benchmark(...)`;
- `save_s2_s1_run_artifacts(...)`;
- helper functions for:
  - `S1` marginal IPR;
  - positive-spectrum `r` calculation;
  - kernel chirality bookkeeping;
  - threshold-scan stability;
  - aggregation and assessment classification;
  - figure generation;
  - markdown summary tables.

### `scripts/s2_s1_product.py`

This CLI should:

- expose `--quick` and `--full`;
- construct mode-specific `S2S1ProductConfig`;
- create a timestamped run directory;
- run the benchmark;
- print a concise terminal summary;
- optionally update reports later, but only after a successful implementation
  phase and not as part of this specification change.

### `tests/test_s2_s1_product.py`

This test file should cover:

- operator construction;
- PBC/APBC behavior;
- `q=0` null control;
- spectator detection;
- flux response;
- artifact saving;
- CLI smoke behavior.

### `reports/S2_S1_PRODUCT_IMPLEMENTATION_SPEC.md`

This file is the authoritative design note for the future implementation and
must be kept as a planning document until code is actually added and verified.

## CLI Specification

Required commands:

```powershell
python scripts/s2_s1_product.py --quick
python scripts/s2_s1_product.py --full
```

Recommended optional flags for the future implementation:

```powershell
python scripts/s2_s1_product.py --quick --seed 12345
python scripts/s2_s1_product.py --full --q-values 0,1,-1
python scripts/s2_s1_product.py --full --s1-sizes 8,16,24
python scripts/s2_s1_product.py --full --boundary-twists 0.0,0.5
```

## Proposed Quick/Full Configs

### Quick Mode

| Parameter | Value |
| --- | --- |
| `q_values` | `(0, 1, -1)` |
| `cutoff` | `2` |
| `s1_sizes` | `(8, 16)` |
| `boundary_twists` | `(0.0, 0.5)` |
| `s1_modes` | `("clean", "gauge_phase", "geometric_weight")` |
| `disorder_values` | `(0.0, 2.0, 8.0)` |
| `perturbation_values` | `(0.0, 1e-5)` |
| `realizations` | `3` |
| `low_energy_window` | `8` |
| `zero_tolerance_scan` | `(1e-8, 1e-7, 1e-6)` |

Quick mode goal:

- prove that the operator is coupled to `S1`;
- verify the PBC/APBC contrast;
- verify at least one inhomogeneity-driven `S1` IPR effect.

### Full Mode

Recommended future expansion:

| Parameter | Value |
| --- | --- |
| `q_values` | `(0, 1, -1, 2, -2)` |
| `cutoff` | `2` or `3` if feasible |
| `s1_sizes` | `(8, 16, 24)` |
| `boundary_twists` | `(0.0, 0.25, 0.5)` |
| `s1_modes` | `("clean", "gauge_phase", "geometric_weight")` |
| `disorder_values` | `(0.0, 1.0, 2.0, 4.0, 8.0)` |
| `perturbation_values` | `(0.0, 1e-5)` |
| `realizations` | `4` or `5` |
| `low_energy_window` | `8` or `12` |
| `zero_tolerance_scan` | keep explicit and recorded |

Full mode goal:

- check sign symmetry for `q = +/-1, +/-2`;
- test stronger size dependence in the circle factor;
- confirm threshold robustness and flux sensitivity more carefully.

## Required Artifacts

Each run must write:

```text
reports/RUNS/<timestamp>_s2_s1_product_<mode>/
```

Required files:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/kernel_count_vs_twist.png`
- `figures/min_abs_eigenvalue_vs_twist.png`
- `figures/s1_ipr_vs_disorder.png`
- `figures/s2_chirality_content.png`
- `figures/flux_response.png`

Recommended additional figures:

- `figures/r_statistics_vs_disorder.png`
- `figures/kernel_count_vs_tolerance.png`
- `figures/s1_size_comparison.png`

## `metrics.json` Contract

At minimum, `metrics.json` should contain:

- serialized config;
- raw observations;
- aggregated assessments;
- global gate flags;
- explicit warning strings;
- threshold-scan results;
- enough metadata to reconstruct:
  - `S1` operator mode;
  - twist schedule;
  - seed schedule;
  - low-energy window rule.

Recommended top-level keys:

| Key | Meaning |
| --- | --- |
| `observations` | Serialized `S2S1Observation` rows. |
| `assessments` | Serialized `S2S1Assessment` rows. |
| `all_q_controls_passed` | Global null-control result. |
| `all_pbc_gates_passed` | Global PBC result. |
| `all_apbc_gates_passed` | Global APBC result. |
| `flux_response_observed` | Any valid flux response in the run. |
| `localization_growth_observed` | Any valid `S1` IPR growth under `geometric_weight`. |
| `s1_not_spectator_observed` | Whether the circle factor is active. |
| `threshold_stability_observed` | Whether kernel conclusions are tolerance-stable. |
| `summary_statement` | Human-readable summary. |
| `scientific_warning` | Explicit non-claim text. |

## Success Gates

### 1. `q`-control gate

`q = 0` must not produce an inherited protected kernel signal.

Minimum interpretation:

- `kernel_count` should not mimic the `q != 0` PBC pattern;
- any apparent kernel under `q = 0` must be marked numerical or threshold
  sensitive unless independently justified.

### 2. PBC gate

PBC with `q != 0` should give `kernel_count` close to `|q|` in the clean
circle sector at small perturbation.

This is the finite-mode inherited-kernel analogue of the positive control.

### 3. APBC gate

APBC should lift the exact zero sector:

- `kernel_count` should drop relative to PBC;
- `min_abs_eigenvalue` should move away from zero.

### 4. `S1` spectator gate

`N_S1 = 1` and `N_S1 = 16` must not be equivalent up to trivial multiplicity.

At least one of the following must hold:

- normalized low-energy spacing structure changes;
- flux response changes;
- `S1` low-energy IPR changes;
- APBC/PBC contrast depends on circle resolution.

If none of these occur, `S1` is a spectator and the experiment fails.

### 5. Flux gate

Changing `alpha` must move the lowest modes.

Recommended probe:

- compare `alpha` and `alpha + flux_probe_delta`;
- record the shift in the smallest `k` absolute eigenvalues.

### 6. Localization gate

`clean` `S1` should have low `S1` IPR, while `geometric_weight` at strong
disorder should increase low-energy `S1` IPR.

This is the main replacement for the old graph-sector localization statement.

### 7. Threshold gate

Kernel conclusions must not depend on a tiny change of `zero_tolerance`.

Required:

- rerun kernel classification for at least three tolerances;
- record whether the PBC/APBC gate conclusions change.

### 8. No-overclaim gate

The summary text, CLI text, markdown summary, and future reports must never
describe the result as:

- continuum compactification;
- `S6`;
- `S3 x S6`;
- Witten/Lichnerowicz bypass;
- Standard Model result;
- physical chirality proof.

## Failure / Null Criteria

Record the experiment as null, limiting, or unresolved if any of the following
occurs:

1. PBC/APBC do not differ.
2. Twist does not move lowest modes.
3. `q = 0` produces a false inherited-kernel signal.
4. `N_S1` only multiplies degeneracy without changing low-energy structure.
5. `S1` IPR conclusions appear to be basis artifacts.
6. Kernel conclusions depend strongly on `zero_tolerance`.

Where to record later if this happens:

- `reports/NULL_RESULTS.md` for failed or limiting hypotheses;
- `reports/ISSUES_SCIENTIFIC.md` for unresolved interpretation risks;
- `reports/VALIDATION_STATUS.md` only after an actual implementation run.

## Test Plan

The future implementation should include at least these tests.

### Unit Tests

1. `build_s1_spectral_operator(clean)` returns a Hermitian matrix of shape
   `(N, N)`.
2. `build_s1_spectral_operator` depends on `alpha`; `alpha=0.0` and `alpha=0.5`
   are not identical.
3. `build_s2_s1_product_operator` returns the expected total dimension.
4. `q=0` clean PBC does not show the inherited `|q|` kernel pattern.
5. `q=1` clean PBC gives `kernel_count` near `1`.
6. `q=1` clean APBC lifts the exact zero sector.
7. `q=-1` flips the `S2` chirality content relative to `q=1`.
8. `geometric_weight` strong disorder raises `S1` low-energy IPR relative to
   clean.
9. Flux probe changes the lowest eigenvalues by a measurable amount.
10. Threshold scan does not flip the main PBC/APBC conclusion in the clean
    `q != 0` case.

### Integration Tests

1. `run_s2_s1_product_benchmark(...)` produces nonempty observations and
   assessments.
2. `save_s2_s1_run_artifacts(...)` writes all required artifacts.
3. CLI quick smoke:

```powershell
python scripts/s2_s1_product.py --quick
```

must complete successfully and print the summary flags.

## Implementation Sequence

Recommended order:

1. Implement `build_s1_spectral_operator(...)`.
2. Verify Hermiticity and twist dependence in unit tests.
3. Implement `build_s2_s1_product_operator(...)`.
4. Implement observation-level analysis.
5. Add threshold-scan logic.
6. Add aggregation and assessments.
7. Add artifact saving and plots.
8. Add CLI.
9. Run quick mode first.
10. Only after passing quick gates, consider full mode.

## Scientific Interpretation Rules

Correct interpretation:

```text
This experiment tests whether a finite-mode S2 monopole sector coupled to a
spectral S1 factor shows inherited kernel behavior under PBC, lifting under
APBC, flux sensitivity, and S1-sector low-energy structure beyond a trivial
spectator factor.
```

Incorrect interpretation:

```text
The project has proven physical compactification, physical chirality, S6,
S3 x S6, Witten/Lichnerowicz bypass, or Standard Model fermions.
```

## Scientific Non-Claims

This experiment does not prove:

- continuum `S2 x S1` compactification;
- physical protected chirality;
- a global full-product chiral index theorem;
- `S6` or `S3 x S6`;
- Witten/Lichnerowicz bypass;
- Standard Model fermions;
- `SU(3) x SU(2) x U(1)` derivation;
- covariant compactification as a physical theory.

## What Counts As Success

The MVP counts as a real upgrade over `S2 x graph` if all of the following are
true:

1. the operator contains a genuine `S1` factor, not an external selector;
2. PBC and APBC differ in the expected low-energy way;
3. `q = 0` remains a null inherited-kernel control;
4. low-energy states carry measurable `S1` structure;
5. `geometric_weight` produces stronger `S1` low-energy IPR than `clean`;
6. the effect survives a small threshold scan;
7. the write-up keeps all scientific non-claims explicit.

## What Counts As Failure

The MVP should be considered unsuccessful if it turns out to be merely:

- `S2 ⊗ I` with a decorative circle label;
- a threshold artifact;
- a basis artifact;
- a zero-mode counting trick without flux or boundary sensitivity;
- a path that revives global chiral-index rhetoric for an odd-dimensional
  product.

## Final Scope Reminder

This specification authorizes a future implementation of:

- `cc_toy_lab/spectral/s2_s1_product.py`
- `scripts/s2_s1_product.py`
- `tests/test_s2_s1_product.py`

It does not authorize:

- baseline promotion;
- code changes outside that scope unless needed by implementation;
- any scientific claim beyond a finite-mode toy product experiment.
