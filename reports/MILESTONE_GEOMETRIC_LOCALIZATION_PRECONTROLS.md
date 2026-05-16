# Milestone — Geometric Localization Pre-Controls

## Executive Summary

The **straight-cylinder null** and **variable-radius cylinder** graph-Laplacian
pre-controls both **passed** at the **tiny** configuration documented below. This
means the **kNN graph Laplacian measurement pipeline** (connectivity, degree
sanity, low-mode spectrum, IPR, z-mass diagnostics, and coarse artifact gates)
behaves in a **non-pathological** way on these two control surfaces — **not**
that **geometric localization** is established, proven, or tied to continuum
physics.

## Current Baseline

`v0.1.14-mvp-s2-s1-discretization-v2-full` (unchanged; this milestone is
diagnostic documentation only).

## Source Runs

| Stage | Run directory | Verdict |
| --- | --- | --- |
| Straight cylinder (null) | `reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny` | `null_verdict=straight_cylinder_null_consistent` |
| Variable-radius cylinder (control) | `reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny` | `control_verdict=variable_radius_cylinder_precontrol_pass` (`radial_extent_ratio≈0.44`) |

**Implementation pointers:** `cc_toy_lab/geometry/geometric_localization_precontrol.py`,
`scripts/geometric_localization_precontrol.py`, `tests/test_geometric_localization_precontrol.py`.

**Planning / notes:** `reports/GEOMETRIC_LOCALIZATION_PRECONTROL_PLAN.md`,
`reports/GEOMETRIC_LOCALIZATION_STRAIGHT_CYLINDER_TINY_NOTE.md`,
`reports/GEOMETRIC_LOCALIZATION_VARIABLE_RADIUS_CYLINDER_TINY_NOTE.md`.

**Latest documented tests:** `pytest -q` → **187 passed in 1178.60s** (~19m39s;
full suite confirmed 2026-05-14).

## What Was Checked

- **Graph connectedness** (`connected_components == 1` on both tiny runs).
- **Degree statistics** (`degree_min`, `degree_max`, `degree_mean`, `degree_std`)
  and a coarse **non-pathological degree** gate.
- **Low eigenmodes** of the **normalized kNN graph Laplacian** (smallest nontrivial
  modes after dropping the near-zero constant mode).
- **IPR** (inverse participation ratio per project convention) vs an `~1/N`
  slack gate to flag spurious strong localization on few nodes.
- **Z-mass distribution** and **z center of mass** (tercile masses; boundary-pinning
  gate — not all low modes pinned to outer z-extent).
- **Radius profile nontriviality** (variable-radius stage): sample
  `radial_extent_ratio` confirms the surface is not accidentally degenerate to a
  straight cylinder in the sampled radii.
- **Artifact-risk style gates** shared with the falsification ladder plan
  (`graph_artifact_risk` / fail verdicts if mesh gates break).

## Interpretation

- **Straight cylinder:** on the tiny null setup, low nontrivial modes did **not**
  trigger the **graph-artifact** style failure pattern encoded in the gates;
  verdict **`straight_cylinder_null_consistent`** records that outcome.
- **Variable-radius cylinder:** the same pipeline on a **nontrivial** `r(z)`
  profile passed the extended pre-control gates; verdict
  **`variable_radius_cylinder_precontrol_pass`**.
- Together, these results supported **proceeding to dumbbell *tiny***; the
  follow-up dumbbell run and milestone are recorded under
  `reports/MILESTONE_GEOMETRIC_LOCALIZATION_DUMBBELL_TINY.md` — still **not**
  broad throat claims and **not** “full” geometric localization statements.

## Remaining Risks

- **Tiny resolution only** (`n_z=24`, `n_theta=32`, fixed `k_neighbors`, single
  seed ladder in the default profile).
- **No systematic N / k / ε refinement sweep** yet (plan-level follow-up).
- **Dumbbell tiny** exists (`reports/RUNS/20260514-130000_geometric_localization_dumbbell_tiny`);
  verdict **`dumbbell_null_or_weak_signal`** — refinement sweeps still absent.
- **Stronger curvature / neck features** may still expose kNN or sampling artifacts
  even if the current controls pass.
- **No continuum conclusion** — graph Laplacian on a point cloud remains a toy
  spectral probe.

## Readiness Assessment

| Criterion | Score (0–10) |
| --- | ---: |
| Geometric localization **pre-control** readiness | **8** |
| **Dumbbell tiny** spec + run readiness | **8** |
| **Full** geometric localization **claim** readiness | **4** |
| Physical theory **proof** | **3** |

## Recommended Next Step

Dumbbell tiny is **implemented and closed at diagnostic level** (see
`reports/MILESTONE_GEOMETRIC_LOCALIZATION_DUMBBELL_TINY.md`). Choose one:

- **A.** If geometric localization remains priority: throat / N / k refinement
  sweeps beyond the tiny default profile.
- **B.** Otherwise: pause this branch and return to **product-discretized full**
  planning (per main validation narrative).

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** physical validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.
- This milestone **does not** promote the baseline tag.
