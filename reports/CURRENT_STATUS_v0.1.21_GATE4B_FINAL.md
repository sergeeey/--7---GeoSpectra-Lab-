# Current Status — v0.1.21 Gate 4B Final

**Date:** 2026-05-22  
**Latest Commit:** 84210c8  
**Branch:** main (synced with origin/main)  
**Status:** GATE4B_FSS_PASS_WITH_CAVEATS

---

## Executive Summary

Gate 4B v0.1.21 metric-corrected finite-size scaling campaign ЗАВЕРШЁН с вердиктом **PASS_WITH_CAVEATS**.

**Ключевое достижение:**  
Продемонстрирована finite-lattice robustness W=20 Anderson disorder localization signal на S³×S¹ product manifold при finite-size scaling с использованием TRUE eigenvector-based IPR метрики.

**Контекст метрической коррекции:**  
Gate 4A v0.1.20 использовал неправильную метрику (mean eigenvalues вместо true IPR). Gate 4B v0.1.21 — полный 216-case rerun с исправленной метрикой.

---

## Current Repo State

**Branch:** main  
**Latest commit:** 84210c8 (docs: add pre-push audit report)  
**Results commit:** f7eff32 (results: analyze metric-corrected S3×S1 FSS grid)  
**Working tree:** clean ✅  
**Remote sync:** origin/main up-to-date ✅

**Key commits (reverse chronological):**
```
84210c8 — docs(gate-4b): add pre-push audit report
f7eff32 — results(gate-4b): analyze metric-corrected S3xS1 FSS grid
57c5174 — feat(gate-4): add true IPR runtime benchmark (v0.1.21)
ad6936f — fix(gate-4): implement true eigenvector-based IPR metric
5e5ffc9 — docs(gate-4b): pre-register v0.1.21 metric-corrected protocol
```

---

## Gate 4B Result

### Execution Summary

| Metric | Value |
|--------|-------|
| **Cases completed** | 216/216 (100%) |
| **Failures** | 0 |
| **Batches** | 9/9 |
| **Runtime** | 1.83 hours |
| **true_ipr_mean availability** | 216/216 (100%) |
| **r_stat availability** | 216/216 (100%) |
| **Metric version** | v0.1.21_true_eigenvector_ipr |

**Grid:**
- 3 families (spectral_circle, ring, wilson_ring)
- 3 disorder strengths (W = 0, 12, 20)
- 4 S¹ sizes (16, 32, 64, 128)
- 2 j_max values (2, 3)
- 3 seeds (123, 456, 789)

**Matrix dimensions:** N = (2×j_max + 1) × s1_size  
**Max N:** 896 (j_max=3, s1_size=128)

---

## Key Metrics

### Aggregate True IPR Contrast

**W=20 vs W=0 aggregate contrast:** **7.15×**  
- mean(IPR, W=0) = 0.0326  
- mean(IPR, W=20) = 0.2333  
- Threshold: ≥2.0× for PASS ✅

**Interpretation:** W=20 Anderson disorder increases IPR by 7.15× relative to W=0 baseline, indicating localization enhancement.

---

### Family-Level Contrasts

| Family | IPR(W=0) | IPR(W=20) | Contrast Ratio | Verdict |
|--------|----------|-----------|----------------|---------|
| **spectral_circle** | 0.0224 | 0.0953 | **4.25×** | ✅ PASS |
| **ring** | 0.0346 | 0.2874 | **8.31×** | ✅ PASS |
| **wilson_ring** | 0.0259 | 0.2194 | **8.49×** | ✅ PASS |

**Family consistency:** 3/3 families PASS (threshold: ≥2/3) ✅

**Key finding:** All three discretization families independently confirm W=20 localization signal. No single-family domination (all ≤36% of aggregate contrast).

---

### Finite-Size Scaling Trend

**Contrast ratio vs s1_size:**

| s1_size | N (j_max=3) | Contrast Ratio | Trend |
|---------|-------------|----------------|-------|
| 16      | 112         | 3.76×          | —     |
| 32      | 224         | 6.73×          | ↑     |
| 64      | 448         | 11.93×         | ↑     |
| 128     | 896         | **24.90×**     | ↑     |

**FSS verdict:** STRENGTHENING ✅

**Interpretation:** IPR contrast increases with lattice size, indicating localization signal is NOT a finite-size artifact. Signal strengthens (not collapses) as N → larger within tested range N ≤ 896.

---

### r-Statistic (Level-Spacing Diagnostic)

**Adjacent gap ratio:**

| W | r-statistic (mean) | Expected | Interpretation |
|---|-------------------|----------|----------------|
| 0 | 0.606             | ≈0.53 (GOE) | Ergodic |
| 20 | 0.443            | ≈0.39 (Poisson) | Localized |
| **Shift** | **-0.163** | negative | ✅ Toward localization |

**r-statistic verdict:** consistent_with_localization ✅

**Interpretation:** r-statistic shift is consistent with the true-IPR localization interpretation.

**Diagnostic consistency:** Both IPR and r-statistic agree on W=20 localization direction.

---

### Control Baseline (W=0)

**Stability check (coefficient of variation within each size):**

| s1_size | IPR(W=0) mean | CV | Verdict |
|---------|---------------|----|---------|
| 16      | 0.06821       | 0.121 | stable |
| 32      | 0.03533       | 0.163 | stable |
| 64      | 0.01795       | 0.183 | stable |
| 128     | 0.00903       | 0.190 | stable |

**Max CV:** 0.190 (threshold: <0.2 for stable) ✅

**Control verdict:** stable ✅

---

## Final Verdict

**Verdict:** **GATE4B_FSS_PASS_WITH_CAVEATS**

**All 7 pre-registered decision conditions satisfied:**
1. ✅ Aggregate contrast ≥2.0× (actual: 7.15×)
2. ✅ Family consistency ≥2/3 (actual: 3/3)
3. ✅ No single-family domination (max 36% < 80%)
4. ✅ FSS trend stable/saturating/strengthening (actual: STRENGTHENING)
5. ✅ r-statistic consistent with localization interpretation (Δr = -0.163)
6. ✅ No broad failure cluster (0 failures)
7. ✅ Controls stable (max CV 0.190 < 0.2)

**Scientific statement:**
> S³×S¹ Gate 4B supports finite-lattice robustness of the W=20 Anderson disorder localization signal under finite-size scaling from s1_size=16 to 128 (N = 112 to 896), with true eigenvector-based IPR contrast ≥2.0× and family consistency ≥2/3.

---

## Required Caveats (Non-Negotiable)

### 1. Finite-Lattice Only
- **N ≤ 896** (largest lattice: s1_size=128, j_max=3)
- NO thermodynamic limit (N→∞) claim
- Trend strengthening ≠ proof of infinite-N behavior
- Extrapolation beyond N=896 requires additional data

### 2. Anderson Disorder Only
- Disorder model: diagonal on-site potential U(r) ∈ [-W, W]
- NO generalization to:
  - Correlated disorder
  - Off-diagonal disorder
  - Time-dependent disorder
  - Quasiperiodic potentials

### 3. S³×S¹ Only
- Geometry: 3-sphere cross circle product manifold
- NO generalization to:
  - S²×S¹ (lower-dimensional sphere)
  - S⁷×S¹ (higher-dimensional sphere)
  - Arbitrary FL×S¹ products
  - Non-product manifolds

### 4. W=20 Exploratory
- W=20 chosen from Gate 3C finding
- NO claim: "W=20 is optimal"
- NO systematic W-sweep conducted
- Intermediate W=12 diagnostic only

### 5. True IPR Metric
- v0.1.21: IPR = mean(Σ|ψᵢ|⁴) for bottom 10% eigenstates
- v0.1.20: INVALID (used eigenvalue mean)
- Results NOT comparable with v0.1.20
- NO retroactive reinterpretation of v0.1.20 allowed

### 6. No Physical Compactification Claim
- Finite-lattice discretization ≠ continuum S³×S¹
- NO claim about physical 4D spacetime
- NO claim about Kaluza-Klein compactification
- Computational model only

### 7. No Standard Model / Chirality Claim
- NO claim about Standard Model physics
- NO claim about chiral fermions
- NO claim about gauge field coupling
- Toy Hamiltonian only

---

## Next Recommended Branches

### 1. Gate 5: Larger Scaling (если ресурсы позволяют)
**Goal:** Extend finite-size scaling to larger N  
**Grid:** s1_size = 256, 512 (N = 1792, 3584 for j_max=3)  
**Expected:** Check if FSS trend continues strengthening or saturates  
**Decision:** Proceed only if Gate 4B trend holds stable after 2-week review

### 2. Negative Controls
**Goal:** Verify localization signal vanishes without disorder or with wrong geometry  
**Tests:**
- W=0 at all sizes (already done, but formalize as negative control)
- S¹ only (no S³) — should show delocalized
- Random graph (non-geometric) — compare with S³×S¹
**Expected:** No localization signal without geometric disorder coupling

### 3. Cross-Geometry Transfer
**Goal:** Test if W=20 localization transfers to S²×S¹ or other FL×S¹  
**Scope:** Pilot grid (16, 32 sizes only, 3 seeds)  
**Threshold:** ≥50% of S³×S¹ contrast for PASS  
**Caveat:** Even if passes, NO "FL generalized" claim without ≥3 geometries

### 4. Structural Geometry Monitor
**Goal:** Track how geometric properties (curvature, volume, spectral gap) correlate with localization  
**Metrics:** Spectral gap, effective dimension, Ricci curvature diagnostics  
**Output:** Structural hypothesis for why S³×S¹ shows localization  
**NOT a new experiment:** Analysis of existing Gate 4B data

### 5. Methodology Report (High Priority)
**Goal:** Document metric correction incident, recovery protocol, lessons learned  
**Audience:** Internal review, future campaigns  
**Sections:**
- Gate 4A metric mismatch root cause
- Recovery protocol (audit, rerun, verification)
- Updated checklist for future experiments
- EstimandOps L0 integration (if applied)
**Deliverable:** `reports/GATE4_METHODOLOGY_REPORT_v0.1.21.md`

---

## Key Documents (See REPORT_INDEX_v0.1.21.md)

**Protocol & Pre-registration:**
- S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md
- S3_S1_GATE4_BATCH_PROTOCOL_v0.1.21.md

**Execution & Results:**
- S3_S1_GATE4B_RAW_EXECUTION_FREEZE_v0.1.21.md
- S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md

**Audit & Integrity:**
- GATE4B_PRE_PUSH_AUDIT_v0.1.21.md

**Metric Correction Chain:**
- S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md
- GATE4_TRUE_IPR_RECOVERY_CHECK_v0.1.20.md
- IPR_IMPLEMENTATION_AUDIT_v0.1.20.md

**Claims:**
- CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md

---

## Archive Notice

**v0.1.20 Status:** ARCHIVED with verdict WEAK_OR_INCONCLUSIVE  
**Reason:** Primary metric invalid (eigenvalue mean instead of true IPR)  
**No retroactive upgrade:** v0.1.20 verdict remains WEAK regardless of v0.1.21 result

---

**Status Date:** 2026-05-22  
**Status Type:** FINAL  
**Next Review:** 2026-06-05 (2-week stability window before Gate 5 decision)
