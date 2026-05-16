# Straight Cylinder Tiny — Graph Laplacian Pre-Control Note

**Purpose:** null geometry for the **GeoSpectra Falsification Ladder** step in
`reports/GEOMETRIC_LOCALIZATION_PRECONTROL_PLAN.md`: before any dumbbell or
variable-radius localization read, confirm the **kNN graph Laplacian** pipeline
does not invent **strong low-mode localization** on a **straight cylinder** point
cloud.

**Implementation:** `cc_toy_lab/geometry/geometric_localization_precontrol.py`  
**CLI:** `python scripts/geometric_localization_precontrol.py --straight-cylinder --tiny`  
(Variable-radius control: `--variable-radius-cylinder --tiny`; see
`reports/GEOMETRIC_LOCALIZATION_VARIABLE_RADIUS_CYLINDER_TINY_NOTE.md`.)

**Tiny profile (default):**

| Parameter | Value |
| --- | ---: |
| `radius` | 1.0 |
| `length` | 4.0 |
| `n_z` | 24 |
| `n_theta` | 32 |
| `k_neighbors` | 12 |
| `num_modes` | 8 |
| `seeds` | `(123,)` |

**Artifacts directory pattern:**

```text
reports/RUNS/<timestamp>_geometric_localization_precontrol_straight_cylinder_tiny/
```

Expected contents: `config.json`, `metrics.json`, `data.npz`, `summary.md`,
`figures/.placeholder`.

**Example documented run (fixed timestamp for reproducibility):**

```text
reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny/
```

**Recorded verdict for that run:** `null_verdict=straight_cylinder_null_consistent` (see
`metrics.json` in the directory above).

**Verdict vocabulary (any run):**

- `straight_cylinder_null_consistent` — gates satisfied; **next** planned
  control is **variable-radius cylinder** (not dumbbell first).
- `graph_artifact_risk` — IPR and/or z-center pattern suggests **graph /
  sampling artifact**; **do not** proceed to dumbbell until construction is
  revised.

**Gates (summary):**

- Single connected component.
- Degree distribution within coarse sanity bounds.
- Low nontrivial-mode IPR not extreme vs `~1/N` slack (see code thresholds).
- Z center of mass **not** all pinned to the outer 10% z-extent for every low
  mode.

## Scientific non-claims

- Not proof of **geometric localization**.
- Not **continuum compactification**.
- Not **`S6` / `S3 × S6`** physical validation.
- Not **Standard Model** derivation.
- Not **physical chirality** proof.
- Not **Witten/Lichnerowicz** bypass.
- **Baseline** tag is **not** promoted by this diagnostic.
