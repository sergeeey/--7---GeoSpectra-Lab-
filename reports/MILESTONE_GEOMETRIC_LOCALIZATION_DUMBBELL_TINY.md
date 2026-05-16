# Milestone — Geometric Localization Dumbbell Tiny

## Executive Summary

The **dumbbell tiny** graph-Laplacian diagnostic completed on the default tiny
profile with aggregate verdict **`dumbbell_null_or_weak_signal`**. The
measurement pipeline exercised a throat-like axisymmetric surface after the
straight-cylinder null and variable-radius cylinder pre-controls; the outcome
is **null or weak spectral/geometric signal at this resolution**, **not** a
positive localization theorem and **not** physical compactification evidence.

## Source Runs

| Stage | Run directory | Verdict / role |
| --- | --- | --- |
| Straight cylinder (null) | `reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny` | `straight_cylinder_null_consistent` |
| Variable-radius cylinder (control) | `reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny` | `variable_radius_cylinder_precontrol_pass` |
| Dumbbell tiny | `reports/RUNS/20260514-130000_geometric_localization_dumbbell_tiny` | `aggregate_verdict=dumbbell_null_or_weak_signal` |

**Planning / implementation pointers:** `reports/GEOMETRIC_LOCALIZATION_DUMBBELL_TINY_SPEC.md`,
`reports/GEOMETRIC_LOCALIZATION_DUMBBELL_TINY_NOTE.md`,
`cc_toy_lab/geometry/geometric_localization_precontrol.py`,
`scripts/geometric_localization_precontrol.py`, `tests/test_geometric_localization_precontrol.py`.

**Pre-control milestone:** `reports/MILESTONE_GEOMETRIC_LOCALIZATION_PRECONTROLS.md`.

## Dumbbell Result

- **`aggregate_verdict`:** `dumbbell_null_or_weak_signal`.
- **`k_sensitivity_ok_by_throat`:** `{"0.35": true, "0.5": true}` (string keys
  in metrics JSON; both throats pass the encoded k-sensitivity check).
- **Graph / sampling sanity:** per-case records include **`connected_components: 1`**
  and **`gate_graph_connected: true`** together with the shared degree / IPR /
  z-mass gates — **no** obvious disconnected-graph or coarse artifact failure
  pattern on this run; the aggregate verdict still does **not** support a
  **strong geometric-localization** claim.
- **No strong localization claim:** the verdict explicitly classifies the
  dumbbell response as null/weak at the configured tiny grid; absence of a
  strong signal is **evidence under this probe**, not proof of absence in other
  regimes.

## Interpretation

- **Measurement pipeline:** straight and variable-radius pre-controls already
  showed the kNN Laplacian pipeline behaving non-pathologically on simpler
  surfaces; dumbbell extends the same machinery to a throat-like profile with
  **pre-control-style gates satisfied** on the recorded cases.
- **Dumbbell tiny** did **not** produce a **strong** geometric-localization-style
  conclusion: the aggregate label is **null/weak** at the default tiny
  resolution.
- This is **useful falsification / negative-result bookkeeping** for the ladder
  (we ran the geometry and the verdict stayed weak) — **not** a project failure
  and **not** a positive physics proof.

## Remaining Limitations

- **Tiny only:** default `n_z`, `n_theta`, and single-profile sampling; no
  claim to dense refinement limit.
- **No N / k refinement sweep** beyond what is encoded in the diagnostic and
  tests.
- **No throat-radius sweep** beyond the tiny defaults and the two throat radii
  in the recorded `k_sensitivity_ok_by_throat` map.
- **No continuum conclusion:** graph Laplacian on a sampled surface remains a
  toy spectral probe.

## Recommended Next Step

Choose one path depending on priority:

- **A.** If **geometric localization** remains the top branch: run a **throat /
  refinement / k** sweep (larger `n_z`/`n_theta`, varying `k_neighbors`,
  additional throat radii) before any stronger wording.
- **B.** If product-scale work is more urgent: **pause** the geometric-localization
  refinement branch and return to **product-discretized full** planning and
  stress (per main validation narrative).

## Readiness Assessment

| Criterion | Score (0–10) |
| --- | ---: |
| Geometric pre-control readiness | **8** |
| Dumbbell tiny implementation | **8** |
| Dumbbell signal strength | **4** |
| Readiness for dumbbell refinement | **7** |
| Physical theory proof | **3** |

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** validation as physical extra dimensions.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.

## Current Baseline

`v0.1.14-mvp-s2-s1-discretization-v2-full` (unchanged; this milestone is diagnostic
documentation only).

## Test Suite Confirmation

Full suite after dumbbell wiring and product-discretized full dry-run tests:
`pytest -q` → **187 passed in 1178.60s** (~19m39s on reference machine; counts vary
with suite additions).
(~17m06s; confirmed 2026-05-14).
