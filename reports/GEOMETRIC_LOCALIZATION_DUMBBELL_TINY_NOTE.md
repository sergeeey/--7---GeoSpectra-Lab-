# Geometric Localization — Dumbbell Tiny Diagnostic

## Summary

This note documents the **first dumbbell / throat-like** graph-Laplacian **tiny**
diagnostic. It is a **controlled follow-up** after straight-cylinder and
variable-radius pre-controls (`reports/MILESTONE_GEOMETRIC_LOCALIZATION_PRECONTROLS.md`).
The run is **tiny-resolution only** and is **not** a proof of geometric
localization, continuum physics, or any higher-dimensional validation.

**Example run (fixed timestamp):**

```text
reports/RUNS/20260514-130000_geometric_localization_dumbbell_tiny/
```

**Recorded `aggregate_verdict` for that run:** `dumbbell_null_or_weak_signal`
(`k_sensitivity_ok_by_throat` true for both throat radii on the default tiny grid).

## Source Run

**Command:**

```text
python scripts/geometric_localization_precontrol.py --dumbbell --tiny
```

**Run directory pattern:**

```text
reports/RUNS/<timestamp>_geometric_localization_dumbbell_tiny/
```

## Geometry

Implemented axisymmetric surface `(r(z) cos θ, r(z) sin θ, z)` with a **smooth
two-Gaussian bump** profile (see `summary.md` / `config.json` field
`formula_documentation` in the run directory for the exact formula). Default tiny
grid: `length=6.0`, `n_z=n_theta=32`, `throat_radius ∈ {0.35, 0.5}`,
`bulb_radius=1.0`, `throat_width=0.8` (Gaussian σ), `k_neighbors ∈ {8, 12}`,
`num_modes=10`, `seeds=(123,)`, `jitter=0.0`.

## Gate Summary

Per case: **graph connectedness**, **degree statistics**, **IPR / z-pinning**
gates (same family as cylinder pre-controls), plus **k-sensitivity** across
`k=8` vs `k=12` for each `throat_radius` (mode0 label, IPR, throat mass fraction).

## k-Sensitivity

Compare `k=8` and `k=12` at matched `(throat_radius, seed, grid)`; see
`metrics.json` key `k_sensitivity_ok_by_throat` and the case table in
`summary.md`.

## Interpretation

Read **`aggregate_verdict`** from `metrics.json`. Allowed toy labels include:
`dumbbell_signal_candidate`, `dumbbell_null_or_weak_signal`, `graph_artifact_risk`,
`threshold_geometry_sensitivity`, `sampling_artifact_risk` (see
`reports/GEOMETRIC_LOCALIZATION_DUMBBELL_TINY_SPEC.md`).

## Relation to Pre-Controls

Mandatory prior evidence (unchanged):

- `reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny`
  — `straight_cylinder_null_consistent`.
- `reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny`
  — `variable_radius_cylinder_precontrol_pass`.

## Limitations

Tiny grid only; **no** systematic N/k refinement sweep; **no** full dumbbell
profile ladder; graph Laplacian remains a **discrete** probe — no continuum
conclusion.

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.
