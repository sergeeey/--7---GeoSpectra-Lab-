# Geometric Localization — Dumbbell Tiny Specification

**Status:** planning-only. **No** dumbbell implementation in this deliverable.  
**Baseline:** `v0.1.14-mvp-s2-s1-discretization-v2-full` (unchanged).  
**Pre-control milestone:** `reports/MILESTONE_GEOMETRIC_LOCALIZATION_PRECONTROLS.md`.

---

## Purpose

The **dumbbell / throat** geometry is the **first** geometry where a **localized**
low-mode signal might be **compatible** with an intuitive “mass in the throat
or bulbs” picture — but it is also where **kNN graph Laplacian** artifacts
(disconnects, seam pinning, density coupling) are most likely. Per the
**GeoSpectra Falsification Ladder**, dumbbell diagnostics are **gated** behind:

1. **Straight cylinder null** — must not show spurious strong low-mode
   localization from the pipeline alone.
2. **Variable-radius cylinder control** — same pipeline on a **smooth,
   nontrivial** `r(z)` without pathological gates failing.

Only after both pre-controls pass (as recorded for the **tiny** runs below) is a
**dumbbell tiny** spec justified. This document defines **what** a future
implementation should do; it does **not** assert that geometric localization
exists.

---

## Current Pre-Control Evidence

| Stage | Run directory | Recorded verdict |
| --- | --- | --- |
| Straight cylinder (null) | `reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny` | `straight_cylinder_null_consistent` |
| Variable-radius cylinder (control) | `reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny` | `variable_radius_cylinder_precontrol_pass` (`radial_extent_ratio≈0.44`) |

These runs **validate the measurement pipeline** (graph build, spectrum, IPR,
z-mass gates) at the **tiny** level only. They **do not** validate dumbbell
physics, continuum compactification, or geometric localization in a proof sense.

**Latest documented tests (repository snapshot):** `pytest -q` → **169 passed**.

---

## Dumbbell Geometry Proposal

**Surface model (axisymmetric, embedded in R³):** points

`(x, y, z) = (r(z) cos θ, r(z) sin θ, z)`

with `z ∈ [-L/2, L/2]`, `θ ∈ [0, 2π)`, and a **smooth** radius profile `r(z) > 0`.

### Alternative template (parameterize with positivity check)

A form in the same family as the milestone discussion (implementers **must**
verify `min_z r(z) > 0` on the sampled grid; the raw expression can dip unless
`A_bulb` and `σ` are constrained):

```text
r(z) = r_throat
     + A_bulb * ( 1 - exp(-((z - z_L)^2) / σ^2) - exp(-((z - z_R)^2) / σ^2) )
```

If this template violates positivity, **reduce** `A_bulb`, **widen** `σ`, or
**increase** `r_throat` before any graph build.

### Suggested safe profile (two bulbs + throat)

One convenient **C∞-leaning** family (parameters to be fixed in `config.json`):

```text
r(z) = r_throat
     + A_bulb * ( exp(-((z - z_L)^2) / σ^2) + exp(-((z - z_R)^2) / σ^2) )
```

with:

- `z_L = -L/4`, `z_R = +L/4` (or symmetric offsets documented per run),
- `r_throat`, `A_bulb`, `σ` chosen so that **`r(z) ≥ r_min > 0`** everywhere on the grid,
- **no** jumps, **no** creases: if a piecewise profile is ever used, it must be
  **C¹** at joins; prefer Gaussians as above.

**Alternative** (if implementation prefers closed form without nested exponentials):
a smooth **two-bump** superposition of the same kind used in the variable-radius
control, with **additional** Gaussian bumps at `z_L`, `z_R` only (document
chosen formula in `config.json`).

### Hard requirements

- **Radius strictly positive** on every sampled `(z, θ)` after any optional
  `jitter` (pre-check `min r(z)` before building the graph).
- **No discontinuities** in `r(z)` or in the first derivative where the graph
  sees distances (smooth profile).
- **No disconnected graph** under the intended kNN recipe: if a candidate
  profile risks neck too narrow relative to point spacing, **shrink** `σ`,
  **increase** `r_throat`, or **increase** `n_z` / `n_theta` before running — do
  not “fix” by silently changing `k` without recording it.
- **Avoid sharp kNN artifacts at the throat:** throat width should be **several
  times** the typical nearest-neighbor distance on the surface (document
  heuristic in run `summary.md`).

---

## Tiny Grid

**Suggested default ladder** (small Cartesian product; each combo is one
`metrics.json` row or one run directory with a `cases` array — implementation choice):

| Parameter | Suggested values |
| --- | --- |
| `length` | `6.0` |
| `n_z` | `32` |
| `n_theta` | `32` |
| `throat_radius` | `0.35`, `0.5` |
| `bulb` scale | Hold `A_bulb` or equivalent so max radius ≈ **`1.0`** (single bulb scale row) |
| `k_neighbors` | `8`, `12` |
| `seeds` | `(123,)` |
| `num_modes` | `10` |
| `jitter` | `(0.0,)` initially; optional `(1e-4,)` sensitivity row **after** null-jitter baseline |

**Total tiny cases (if full grid):**  
`2 (throat_radius) × 2 (k_neighbors) × 1 (bulb) × 1 (jitter) = 4` core rows  
(expand only with explicit plan revision).

---

## Required Metrics

Each case (or aggregate) should record at least:

- **`graph_connected`** (bool) and **`connected_components`** (int).
- **Degree stats:** `degree_min`, `degree_max`, `degree_mean`, `degree_std`.
- **`spectral_gap`** (heuristic: smallest positive eigen-subgap among computed
  spectrum, same convention as pre-control).
- **Low eigenvalues** for the first `num_modes` **nontrivial** modes (after
  dropping near-null constant mode).
- **`ipr`** per low mode (project definition: `sum |ψ|⁴ / (sum |ψ|²)²`).
- **`z_center_of_mass`** per low mode (mass = `|ψ|²`).
- **Regional masses** (partition surface nodes by **intrinsic** z into three
  zones aligned to geometry):
  - **`mass_left_bulb`** — mass in z-region containing left bump center `z_L`
    (document bin edges in config).
  - **`mass_throat`** — mass in central throat band (avoid overlap with bulb
    bins; document).
  - **`mass_right_bulb`** — mass in z-region containing `z_R`.
- **`localization_region_label`** — enum such as
  `throat` / `left_bulb` / `right_bulb` / `delocalized` / `ambiguous`, from a
  rule applied to the dominant mass fraction among the three regions for that
  mode (document rule in code comments + `summary.md`).
- **`mode_symmetry_left_right`** — e.g. mass imbalance score between left and
  right bulb regions for that mode (scalar); flag if geometry is symmetric but
  mode is strongly asymmetric without disorder.
- **`throat_mass_fraction`**, **`bulb_mass_fraction`** — for the mode used as
  headline (e.g. first nontrivial mode), or per-mode as needed.
- **`k_sensitivity_check`** — bool or enum: agreement of `localization_region_label`
  (and IPR within a documented tolerance) between `k=8` and `k=12` at matched
  geometry/seed.

---

## Required Gates

All must be evaluated and recorded; failing any is a **stop** for strong
interpretation (artifact or inconclusive).

1. **`graph_connected=True`** (`connected_components == 1`).
2. **Degree distribution not pathological** — reuse pre-control style bounds
   (min degree ≥ 1, max < N, coefficient-of-variation cap; exact numbers must
   match the implemented helper or be re-declared in this spec’s implementation PR).
3. **No boundary-pinned artificial mode** — not all low modes have
   `z_center_of_mass` in the outer 10% z-extent (same style gate as pre-control).
4. **k stability:** for each `(geometry, seed)` pair, low-mode headline labels
   (and IPR) must be **stable** across **`k_neighbors ∈ {8, 12}`** within
   documented tolerances (`k_sensitivity_check=True`).
5. **Geometric alignment:** dominant localization (if any) must **not** track
   only a **known mesh irregularity** (e.g. duplicate z rings, index seam); if
   the implementation uses structured `(z, θ)` ordering, log a **seam index** and
   exclude it from the “throat” bin or add a control row with rotated θ offset.
6. **Pre-control citations** — `summary.md` must cite both completed runs:
   - `reports/RUNS/20260514-120000_geometric_localization_precontrol_straight_cylinder_tiny`
   - `reports/RUNS/20260514-121500_geometric_localization_precontrol_variable_radius_cylinder_tiny`

---

## Failure Modes

Treat as **kill signals** for a “dumbbell signal” read (implementation should log
which fired):

- **Graph disconnects at throat** — `connected_components > 1` or isolated nodes.
- **Low modes localize at a grid seam** — mass spikes on a **θ** or **z**
  index seam not explained by geometry bins.
- **Localization disappears or flips region when `k` changes** — fails
  `k_sensitivity_check`.
- **Localization only at the most extreme `throat_radius`** — suggests threshold
  / discretization sensitivity rather than robust geometric read.
- **Localization tracks sampling density** (e.g. more points where radius is
  larger) without matching **labeled** geometric regions — `sampling_artifact_risk`.
- **Left/right asymmetry** in modes when geometry and seed are symmetric —
  `sampling_artifact_risk` unless explained by degeneracy / multiplicity.

---

## Interpretation Rules

Record **one** primary classification string per case (or per run aggregate):

| Verdict | When to use |
| --- | --- |
| `dumbbell_null_or_weak_signal` | No stable low-mode localization pattern; or only marginal mass shifts. |
| `dumbbell_signal_candidate` | Stable across `k`, aligned with throat/bulb bins, passes gates; still **not** a physics proof. |
| `graph_artifact_risk` | Connectivity, degree, seam, or k-sensitivity failures. |
| `threshold_geometry_sensitivity` | Signal exists only at narrowest throat or vanishes with tiny parameter moves. |
| `sampling_artifact_risk` | Density coupling, unexplained L/R asymmetry, or mesh-driven mass. |

These labels are **toy diagnostic vocabulary** only.

---

## Artifacts for Future Implementation

Each future run directory (pattern TBD, e.g.
`reports/RUNS/<timestamp>_geometric_localization_dumbbell_tiny/`) should save:

- `config.json` — full geometry, grid, `k`, seeds, bin edges, profile formula.
- `metrics.json` — per-case rows with all metrics and verdict fields above.
- `data.npz` — at least `points`, `z`, `r_xy`, optional `theta_index`, low eigenpairs
  if size allows.
- `summary.md` — tables, gate table, verdict, **Scientific non-claims**, citations
  to both pre-control runs + this spec.
- `figures/.placeholder` — reserved until plots are defined without overclaim.

---

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.
- Passing dumbbell tiny gates would **not** prove **geometric localization** in a
  physical or continuum sense.

---

## Acceptance Criteria for Future Implementation

- [x] Spec exists at `reports/GEOMETRIC_LOCALIZATION_DUMBBELL_TINY_SPEC.md`.
- [x] No code changed as part of authoring this spec.
- [x] Baseline unchanged (`v0.1.14-mvp-s2-s1-discretization-v2-full`).
- [x] Dumbbell implementation remains **future** work until a separate implementation task.
