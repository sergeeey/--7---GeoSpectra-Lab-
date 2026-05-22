# S³×S¹ Gate 4B Raw Execution Freeze — v0.1.21

**Date:** 2026-05-22  
**Purpose:** Freeze raw execution outputs before scientific interpretation  
**Status:** EXECUTION COMPLETE — analysis pending

---

## Purpose

This document freezes the raw execution state of Gate 4B v0.1.21 metric-corrected rerun **before** applying scientific interpretation or decision rules.

**Key principle:** Execution completion ≠ scientific PASS verdict.

Scientific verdict requires:
1. Metric aggregation
2. Pre-registered decision rules application
3. Family consistency verification
4. Finite-size scaling analysis
5. Caveat documentation

---

## Execution Summary

**Grid:**
- 3 families: spectral_circle, ring, wilson_ring
- 3 disorder values: W = 0, 12, 20
- 4 S¹ sizes: 16, 32, 64, 128
- 2 j_max values: 2, 3
- 3 seeds: 123, 456, 789
- **Total:** 3 × 3 × 4 × 2 × 3 = **216 cases**

**Execution mode:** Batched (9 batches × 24 cases)

**Results:**
- **Batches completed:** 9/9 ✅
- **Cases completed:** 216/216 ✅
- **Failures:** 0
- **true_ipr_mean availability:** 216/216 (100%)
- **r_stat availability:** 216/216 (100%)
- **Total runtime:** 1.83 hours (109.8 min, 6587.7 sec)
- **Mean per batch:** 12.2 min
- **Mean per case:** 30.5 sec

**Metric version:** `v0.1.21_true_eigenvector_ipr`

---

## Output Directory

**Base path:**
```
reports/RUNS/gate4_fss_v0.1.21/
```

**Structure:**
```
gate4_fss_v0.1.21/
├── config.json
└── batches/
    ├── batch_01/ (spectral_circle, W=0)
    ├── batch_02/ (spectral_circle, W=12)
    ├── batch_03/ (spectral_circle, W=20)
    ├── batch_04/ (ring, W=0)
    ├── batch_05/ (ring, W=12)
    ├── batch_06/ (ring, W=20)
    ├── batch_07/ (wilson_ring, W=0)
    ├── batch_08/ (wilson_ring, W=12)
    └── batch_09/ (wilson_ring, W=20)
```

Each batch contains:
- `batch_config.json` — batch parameters
- `results.json` — 24 case outputs
- `status.json` — execution status
- `summary.md` — human-readable summary
- `timing.json` — runtime statistics

**Total files:** 46 (1 config + 9 batches × 5 files)

---

## Batch Inventory

| Batch | Family | W | Cases | Runtime (min) | Status |
|-------|--------|---|-------|---------------|--------|
| 1 | spectral_circle | 0 | 24 | 11.8 | ✅ completed |
| 2 | spectral_circle | 12 | 24 | 11.7 | ✅ completed |
| 3 | spectral_circle | 20 | 24 | 12.8 | ✅ completed |
| 4 | ring | 0 | 24 | 13.9 | ✅ completed |
| 5 | ring | 12 | 24 | 11.8 | ✅ completed |
| 6 | ring | 20 | 24 | 12.2 | ✅ completed |
| 7 | wilson_ring | 0 | 24 | 12.4 | ✅ completed |
| 8 | wilson_ring | 12 | 24 | 12.2 | ✅ completed |
| 9 | wilson_ring | 20 | 24 | 11.1 | ✅ completed |

**All batches:** status = completed, n_failed = 0, n_r_stat_unavailable = 0

---

## Coverage Verification

**Grid coverage check:**
- ✅ 216 unique case combinations
- ✅ 0 duplicates
- ✅ 0 missing combinations
- ✅ All (family, W, size, j_max, seed) tuples present exactly once

**Families:**
- spectral_circle: 72 cases (3 W × 4 sizes × 2 j_max × 3 seeds)
- ring: 72 cases
- wilson_ring: 72 cases

**Disorder values:**
- W=0: 72 cases (3 families × 4 sizes × 2 j_max × 3 seeds)
- W=12: 72 cases
- W=20: 72 cases

**Sizes:**
- s1_size=16: 54 cases (3 families × 3 W × 2 j_max × 3 seeds)
- s1_size=32: 54 cases
- s1_size=64: 54 cases
- s1_size=128: 54 cases

---

## Metric Implementation

**v0.1.21 change from v0.1.20:**

| Metric | v0.1.20 (WRONG) | v0.1.21 (CORRECTED) |
|--------|-----------------|---------------------|
| Eigenvalue computation | `np.linalg.eigvalsh(H)` | `np.linalg.eigh(H)` |
| Primary metric | `mean(eigenvalues)` ❌ | `mean(true_ipr)` ✅ |
| Uses eigenvectors? | No | Yes |
| IPR formula | N/A | Σ\|ψᵢ\|⁴ |

**Output fields (v0.1.21):**
- `true_ipr_mean` — canonical metric (mean of true IPR for bottom 10% eigenstates)
- `uses_eigenvectors` — always `true`
- `ipr_metric_version` — `"v0.1.21_true_eigenvector_ipr"`
- `mean_low_eigenvalue` — diagnostic field (for v0.1.20 comparison)
- `mean_low_ipr` — DEPRECATED alias (compatibility only)

**All 216 cases have canonical v0.1.21 output schema.**

---

## Runtime Performance

**Benchmark estimate vs actual:**
- Benchmark extrapolation: 4.0 hours
- Actual runtime: 1.83 hours
- **2.2× faster than benchmark estimate**

**Why faster:**
- Benchmark used 3 cases (limited sample)
- Actual grid had more small-N cases than benchmark anticipated
- Thermal throttling did not occur (High Performance mode sustained)

**Runtime by family:**
- spectral_circle: mean 12.1 min/batch
- ring: mean 12.6 min/batch
- wilson_ring: mean 11.9 min/batch

**Runtime by disorder:**
- W=0: mean 12.4 min/batch
- W=12: mean 11.9 min/batch
- W=20: mean 12.0 min/batch

**No systematic runtime degradation observed across 9 batches → no thermal throttling.**

---

## Protocol Compliance

**Pre-registration commits:**
- v0.1.20 protocol: `1f4173c` (original grid definition)
- v0.1.21 protocol: `5e5ffc9` (metric correction, grid UNCHANGED)
- True IPR implementation: `ad6936f`
- Runtime benchmark: `57c5174`

**Grid parameters:** UNCHANGED from v0.1.20 (same 216 cases)

**Thresholds:** UNCHANGED (same decision rules)

**Metric:** CHANGED (corrected from eigenvalue mean to true IPR)

**Claim language boundaries:**
- ✅ Allowed: "Gate 4B supports finite-lattice robustness..."
- ❌ Forbidden: "S³×S¹ validated", "FL generalized", "W=20 optimal"

---

## Important Boundary

**Execution completion is NOT a Gate 4B PASS verdict.**

Scientific verdict requires:
1. Metric aggregation across families, sizes, disorder strengths
2. Application of pre-registered decision rules (reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md)
3. Finite-size scaling analysis
4. Family consistency verification
5. r-statistic vs true IPR consistency check
6. Caveat documentation (finite lattice, Anderson disorder only, S³×S¹ only, no thermodynamic limit)

**This document freezes raw outputs BEFORE scientific interpretation.**

---

## Next Steps

1. **Merge batch outputs** into aggregated metrics (merged/)
2. **Apply pre-registered decision rules** from v0.1.21 protocol
3. **Generate scientific results report** with verdict and caveats
4. **Commit results** (NOT raw batch outputs — those stay in .gitignore)

---

**Freeze timestamp:** 2026-05-22 13:14 Almaty  
**Execution status:** COMPLETE  
**Scientific analysis status:** PENDING  
**Commit status:** NOT YET COMMITTED
