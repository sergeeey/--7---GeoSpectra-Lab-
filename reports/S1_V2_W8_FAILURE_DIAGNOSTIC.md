# S1 v2 W=8 fixed-window failure — targeted diagnostic

## Scope

Toy `S2 x S1` spectral product only. This memo does **not** promote the project
baseline, does not erase the `realizations=5` stress memo
(`reports/S1_V2_STRESS_FAILURE_ANALYSIS_realizations5.md`), and does not claim
continuum physics (see **Non-claims**).

**Stress-level vs this memo:** the `r=5` stress artifact keeps the pre-declared
binary memo label `unresolved_strong_disorder_v2_limitation` because `W>=8`
fixed-window failures **> 0**. This targeted memo adds only the **mechanistic**
layer `threshold_or_window_definition_artifact` for the single isolated case.

## Reference stress artifact

- Stress run: `reports/RUNS/20260513-001436_s1_discretization_v2_stress`
- Baseline tag (informational): `v0.1.14-mvp-s2-s1-discretization-v2-full`
- Isolated `W>=8` fixed-window failure (kernel-only passed, fixed-window failed,
  `window_selection_sensitivity=true`):
  - `family=ring`, `q=-1`, `s1_size=8`, `W=8.0`, `alpha=0.0`, `perturbation=0.0`,
    `seed=9836055`, `realization=4` (inferred from stress seed arithmetic).

## Diagnostic run (artifacts)

Script: `scripts/s1_v2_w8_failure_diagnostic.py`

Canonical saved run (full grid + anchor analysis):

```text
reports/RUNS/20260513-082348_s1_v2_w8_failure_diagnostic
```

Artifacts present: `config.json`, `metrics.json`, `data.npz`, `summary.md`,
`figures/.placeholder` (no plots generated).

### Grid design (high level)

- Families: `ring`, `spectral_circle`, `wilson_ring`
- `q ∈ {-1, 1}`, `s1_size ∈ {8,16,24,32}`, `alpha ∈ {0.0,0.25,0.5}`
- `W ∈ {6,8,10,12,16}` with `_benchmark_seed(..., mode_index=geometric_weight, ...)`
  aligned to stress mode ordering; `6.0` and `10.0` use appended disorder slots so
  stress indices for `{8,12,16}` stay identical.
- Default realization `4`, `perturbation=0`, `cutoff=2`, `low_energy_count=8`,
  `ipr_margin=1e-6` (same gate algebra as stress diagnostics).

## Anchor metrics (exact failing case)

From `metrics.json` → `anchor.anchor_base_row`:

| Quantity | clean | disordered (`W=8`) |
| --- | ---: | ---: |
| kernel-only IPR | 0.25 | 0.31457… |
| fixed-window IPR | 0.20774… | 0.20155… |
| Δ (kernel-only) | — | **+0.06457…** (passes `> 1e-6`) |
| Δ (fixed-window) | — | **−0.00619…** (fails `> 1e-6`) |
| `kernel_count` | 2 | 2 |
| `min_abs_eigenvalue` | ≈2.3e-16 | ≈3.0e-16 |

So the stress-visible failure is a **kernel-selected low-energy window vs
smallest-|λ| fixed window** disagreement, not a vanishing kernel count effect.

## Sensitivity findings (anchor)

### `ipr_margin` sweep

`ipr_margin_sensitivity`: fixed-window remains **failed** for every tested margin
from `0.0` through `1e-4`. Conclusion: this anchor is **not** rescued by relaxing
the IPR margin alone; the dominant issue is **not** a pure `1e-6` margin threshold
artifact.

### `low_energy_count` sweep

`low_energy_count_sensitivity`:

- `low_energy_count ∈ {4, 6, 12}` → `fixed_window_pass=true`
- `low_energy_count ∈ {8, 10}` → `fixed_window_pass=false`

Kernel-only stays passed for all tested `low_energy_count` values. Conclusion:
the gate outcome is **strongly coupled to the fixed-window definition**
(`_select_fixed_window_low_energy_indices` uses the lowest `|λ|` indices, which
need not track the kernel-selected window used for kernel-only IPR when a
near-null cluster is present).

## Primary grid + seed neighborhood

From `metrics.json` → `classification`:

- `primary_w8_ge_fixed_window_failures = 1` (only the ring / `s1_size=8` /
  stress-aligned `W>=8` corner in this sweep).
- `non_ring_w8_failures = 0`, `w8_failures_non_s1_8 = 0`.
- Seed sweep `seed ± 10` around `9836055`: `seed_sensitivity_anchor_fixed_window_failures = 1`
  out of `21` (only the anchor seed fails).

## Classification (interpretation rules)

Automated diagnostic label:
`threshold_or_window_definition_artifact`

Mapping to the user’s decision tree:

- **Not** “genuine strong-disorder v2 limitation” on this evidence: no spread to
  other families or larger `s1_size` at `W>=8` on the primary grid.
- **Not** primarily “`ipr_margin` threshold artifact”: margin sweep does not flip
  the fixed-window outcome.
- **Dominant mechanism**: **window-definition / `low_energy_count` sensitivity**
  (fixed smallest-|λ| window vs kernel-aware window), i.e. a **v2 metric
  definitional artifact** at this discrete point, **plus** the known
  ring / small-`N` / window-selection pathology (single primary-grid failure,
  localized seed sensitivity).

Residual label bucket: if one insists on the original menu, the closest secondary
tag is **ring small-size window-selection artifact**, but the quantitative smoking
gun here is the **`low_energy_count` flip**, not seed noise alone.

## Non-claims

- not continuum compactification
- not `S6` / `S3×S6`
- not Standard Model
- not physical chirality
- not Witten/Lichnerowicz bypass

## How to reproduce

```bash
python scripts/s1_v2_w8_failure_diagnostic.py
```

CI / smoke (tiny grid):

```bash
python scripts/s1_v2_w8_failure_diagnostic.py --tiny
```
