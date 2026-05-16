# Geometric Localization — Graph-Laplacian Pre-Control Plan

**Status:** planning-only (no implementation commitment in this document).  
**Methodology:** GeoSpectra Falsification Ladder — falsify artifact hypotheses before interpreting results as geometry-driven localization.  
**Baseline:** unchanged by this plan; existing v2 / v3 / product-discretized caveats remain on record.

---

## 1. Purpose

Test whether **curvature- or geometry-induced localization** (in the sense intended for later dumbbell / throat studies) can be **distinguished from** false signals produced by:

- **Graph Laplacian** construction on unstructured or semi-structured samples,
- **Sampling-density** gradients (more points where “interesting” geometry is sampled),
- **kNN** graph artifacts (degree imbalance, border effects, discrete connectivity jumps),
- **ε-neighborhood / kernel-width** choices when such graphs are used.

This is a **pre-control** layer: it does **not** prove geometric localization; it **gates** whether a dumbbell/throat diagnostic is interpretable at all on the chosen graph operator.

---

## 2. Pre-control Geometries

| Geometry | Role | Run order |
| --- | --- | --- |
| **Straight cylinder** | **Null geometry:** nearly constant curvature along the axis; expected absence of curvature-driven localization in low Laplacian modes if the operator and sampling are sane. | **First** |
| **Variable-radius cylinder** | **Semi-analytic geometry control:** known modulation of effective “width” / metric variation along the axis; used to check that **refinement in N** and **k / ε** sweeps produce **stable** qualitative spectral and IPR behavior in the region where geometry varies, without spurious jumps tied only to mesh irregularities. | **Second** |
| **Dumbbell / throat** | **Future target** for geometric localization hypothesis tests; **not** the first graph-Laplacian run. Only after null + variable-radius **gates** (Section 5) pass may this geometry be exercised under the same artifact battery. | **After** gates |

Optional **tiny-control** scope (if implemented later): minimal N grids, single k (or small k ladder), fixed seeds, write-only artifacts under `reports/RUNS/` with explicit `precontrol` in the name.

---

## 3. Required Checks

Execute (when implementing) in a documented order; each check should have pass/fail criteria recorded in run metadata.

1. **Graph connectedness** — single connected component (or documented exception with isolated boundary handling); no accidental splits from kNN or ε-thresholds.
2. **Sampling-density uniformity** — quantify deviation from uniform / from the intended density model; flag correlated density vs. curvature regions.
3. **kNN sensitivity** — sweep **k** (or equivalent local connectivity); localization measures should not flip solely at k jumps without geometric explanation.
4. **ε / kernel sensitivity** (if applicable) — sweep neighborhood radius or kernel bandwidth; same stability expectation as for k.
5. **Refinement in N** — increase sample count / mesh resolution along a defined ladder; low-mode observables should converge in a documented sense or fail explicitly (Section 4).
6. **Low-mode spectrum stability** — smallest eigenvalues / gap structure vs. N and k; no pathological drift from discretization-only effects.
7. **IPR stability** — inverse participation ratio (or chosen participation measure) on low modes vs. N, k, ε.
8. **Localization center stability** — if a “center of mass” of |ψ|² is defined on the graph or embedded coordinates, track it under refinement; it should not chase sampling holes.

---

## 4. Failure Modes (Artifact Kill-Signals)

Treat any of the following as **pre-control failure** (do not proceed to dumbbell as primary read):

- **Localization disappears as N increases** while geometry is fixed — suggests mesh- or finite-size artifact.
- **Localization moves with sampling density** rather than with a fixed geometric feature — suggests density coupling, not curvature.
- **Localization depends strongly on k** (or ε) without a plateau region — suggests graph artifact, not robust geometric signal.
- **Graph disconnects near throat** (when eventually tested) — invalid Laplacian regime for localization claims.
- **Low modes localize at mesh irregularities** (e.g., clustering artifacts, boundary clumps) **not** at the intended curvature region — falsifies “geometry-first” interpretation until graph construction is revised.

---

## 5. Gates (Sequential)

1. **Null cylinder:** must **not** produce **artificial** low-mode localization above a documented noise / null band (IPR and regional mass concentration stay within pre-declared thresholds under N and k refinement).
2. **Variable-radius cylinder:** must show **stable** behavior under **N** and **k** (and **ε** if used) refinement — spectrum and localization metrics cohere with semi-analytic expectations or with an explicit “inconclusive but non-artifact” bracket, **not** with density-driven drift.
3. **Only after** (1) and (2) pass may **dumbbell / throat** geometry be tested as the **next** localization target, using the **same** graph construction recipe and artifact checks.

Failure at any gate stops the ladder at planning/implementation review; **baseline is not promoted** and **no** geometric localization proof is asserted.

---

## 6. Metrics

| Metric | Use in pre-control |
| --- | --- |
| **IPR** (or equivalent participation ratio) | Primary scalar to detect false localization on few nodes. |
| **Low-mode mass concentration by region** | Bin nodes by intrinsic coordinate or embedded axis; compare mass in throat vs. bulk **after** null checks. |
| **Graph degree distribution** | Detect kNN imbalance, boundary spikes, disconnected-like hubs. |
| **Connected components** | Must match design (typically 1); document if not. |
| **Spectral gap** (low end of graph Laplacian) | Stability vs. N, k, ε; pathological gap collapse or explosion flags bad graphs. |
| **r-statistics** (if relevant to project pipeline) | Only where already defined for comparable ensembles; optional cross-check, not a substitute for IPR/regional mass gates. |

All thresholds should be **pre-registered** in run configs or memos (Falsification Ladder: declare falsification before peeking).

---

## 7. Non-claims

This plan and any future implementation driven by it:

- **Is not** physical compactification or continuum geometry validation.
- **Is not** `S6` / `S3 × S6` validation or higher-dimensional physical space claims.
- **Is not** Standard Model physics or gauge-sector derivation.
- **Is not** proof of physical localization or of Anderson-type physics on the manifold.
- **Does not** change the repository baseline tag.
- **Does not** erase or supersede existing **v2**, **v3**, or **product-discretized** caveats; it adds an orthogonal **graph Laplacian / sampling** falsification layer before dumbbell-style geometric localization tests.

---

## Acceptance (this deliverable)

- [x] Planning document exists at `reports/GEOMETRIC_LOCALIZATION_PRECONTROL_PLAN.md`.
- [x] No code or baseline change required for acceptance of this task.
