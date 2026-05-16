# Variable-Radius Cylinder Tiny — Graph Laplacian Pre-Control Note

**Purpose:** second step on the **GeoSpectra Falsification Ladder** (after the
straight-cylinder null): same **kNN graph Laplacian** machinery on a
**semi-analytic** surface with nontrivial ``r(z)``, to check that low-mode
metrics remain in the **non-pathological** band recorded for the null geometry
(see `reports/GEOMETRIC_LOCALIZATION_PRECONTROL_PLAN.md`).

**Implementation:** `cc_toy_lab/geometry/geometric_localization_precontrol.py`  
**CLI:** `python scripts/geometric_localization_precontrol.py --variable-radius-cylinder --tiny`

**Geometry (default tiny):**

``r(z) = r0 * (1 + a * cos(2*pi*z/length))`` with `r0=1.0`, `length=4.0`,
`a=0.22`; grid `n_z=24`, `n_theta=32`, `k_neighbors=12`, `num_modes=8`,
`seeds=(123,)`.

**Artifacts directory pattern:**

```text
reports/RUNS/<timestamp>_geometric_localization_precontrol_variable_radius_cylinder_tiny/
```

Contents: `config.json`, `metrics.json`, `data.npz` (includes `r_xy`),
`summary.md`, `figures/.placeholder`.

**Example documented run:**

```text
reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny/
```

**Recorded verdict for that run:** `control_verdict=variable_radius_cylinder_precontrol_pass`
(`radial_extent_ratio≈0.44` on the default tiny sample).

**Verdict field:** `control_verdict` in `metrics.json` (e.g.
`variable_radius_cylinder_precontrol_pass`, `graph_artifact_risk`,
`variable_radius_geometry_invalid`).

**Next (still not implemented here):** dumbbell / throat geometry only after
both straight-null and this control are acceptable under the same gate recipe.

## Scientific non-claims

- Not proof of **geometric localization**.
- Not **continuum compactification**.
- Not **`S6` / `S3 × S6`** physical validation.
- Not **Standard Model** derivation.
- Not **physical chirality** proof.
- Not **Witten/Lichnerowicz** bypass.
- **Baseline** tag is **not** promoted by this diagnostic.
