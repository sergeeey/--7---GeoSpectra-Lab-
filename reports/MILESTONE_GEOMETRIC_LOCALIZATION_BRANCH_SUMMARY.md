# Milestone — Geometric Localization Branch Summary

## Executive Summary

On the current toy graph-Laplacian ladder, the **geometric-localization branch**
completed **two cylinder pre-controls** (straight null + variable-radius
control) and a **dumbbell tiny** diagnostic whose aggregate verdict is
**`dumbbell_null_or_weak_signal`**. Together this shows a working **tiny**
measurement pipeline and a **weak or absent** dumbbell-scale localization-style
signal under the default profile — **not** a proof of geometric localization.

## Current Baseline

`v0.1.14-mvp-s2-s1-discretization-v2-full` (unchanged; this document is summary
only — no baseline promotion).

## Source Artifacts

**Plans**

- `reports/GEOMETRIC_LOCALIZATION_PRECONTROL_PLAN.md`

**Runs**

- `reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny`
- `reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny`
- `reports/RUNS/20260514-130000_geometric_localization_dumbbell_tiny`

**Notes**

- `reports/GEOMETRIC_LOCALIZATION_STRAIGHT_CYLINDER_TINY_NOTE.md`
- `reports/GEOMETRIC_LOCALIZATION_VARIABLE_RADIUS_CYLINDER_TINY_NOTE.md`
- `reports/GEOMETRIC_LOCALIZATION_DUMBBELL_TINY_NOTE.md`

**Specifications**

- `reports/GEOMETRIC_LOCALIZATION_DUMBBELL_TINY_SPEC.md`

**Milestones**

- `reports/MILESTONE_GEOMETRIC_LOCALIZATION_PRECONTROLS.md`
- `reports/MILESTONE_GEOMETRIC_LOCALIZATION_DUMBBELL_TINY.md`

**Implementation (reference only)**

- `cc_toy_lab/geometry/geometric_localization_precontrol.py`
- `scripts/geometric_localization_precontrol.py`
- `tests/test_geometric_localization_precontrol.py`

## Results

| Stage | Artifact | Verdict / status |
| --- | --- | --- |
| Straight cylinder (tiny) | `.../20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny` | `straight_cylinder_null_consistent` |
| Variable-radius cylinder (tiny) | `.../20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny` | `variable_radius_cylinder_precontrol_pass` |
| Dumbbell (tiny) | `.../20260514-130000_geometric_localization_dumbbell_tiny` | `aggregate_verdict=dumbbell_null_or_weak_signal`; `k_sensitivity_ok_by_throat={"0.35": true, "0.5": true}` |
| Test suite | `pytest -q` | **187 passed** (documented suite status after guarded full-runner wiring) |

## Interpretation

- The **kNN graph Laplacian measurement pipeline** behaves coherently at the
  **tiny** discretizations used for cylinders and dumbbell (connectivity, degree
  and IPR-style gates as encoded in the pre-control and dumbbell diagnostics).
- **Dumbbell tiny** did **not** yield **strong** evidence for geometric
  localization under the default grid; the recorded verdict is explicitly
  **null/weak**.
- That outcome is **useful falsification / null-result evidence** for this
  hypothesis at this resolution: the branch was exercised and did not sharpen
  into a strong positive signal here.
- **Refinement** (throat sweep, N/k ladders) is **optional**, not mandatory for
  project integrity — it only rises in priority if this research line stays
  top-ranked.

## Remaining Limitations

- **Tiny only:** default grids and profiles; no dense-refinement limit stated.
- **No systematic N/k refinement sweep** in the completed branch scope.
- **No continuum graph-Laplacian convergence proof** (toy discrete probe only).
- **No full dumbbell profile** (beyond tiny spec + single default-style run).
- **No physical compactification claim** from any of the above.

## Readiness Assessment

| Criterion | Score (0–10) |
| --- | ---: |
| Geometric measurement pipeline | **8.3** |
| Dumbbell signal strength | **4** |
| Readiness for dumbbell refinement | **7** |
| Readiness for S6 / S3×S6 work (as a *separate* future branch, not validated here) | **7** |
| Physical theory proof | **3** |

## Recommended Next Choices

- **A. (default)** Pause the geometric-localization branch and return to
  **product-discretized full-profile** planning and stress — that line currently
  carries **stronger recorded toy signal** in the main validation narrative.
- **B.** Continue the geometric branch with a **throat / N / k refinement sweep**
  **only if** geometric localization remains the explicit top hypothesis.

## Scientific Non-Claims

- No proof that **geometric localization** holds in a physical or continuum sense.
- No **continuum compactification**.
- No **`S6` / `S3 × S6`** physical validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.
