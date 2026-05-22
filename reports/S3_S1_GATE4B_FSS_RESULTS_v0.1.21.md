# S³×S¹ Gate 4B FSS Results — v0.1.21 (Metric-Corrected)

**Date:** 2026-05-22 14:30 Almaty  
**Status:** PASS_WITH_CAVEATS  
**Version:** v0.1.21 — Metric-corrected rerun with TRUE IPR  
**Execution:** 216/216 cases, 0 failures, 1.83 hours  
**Verdict:** GATE4B_FSS_PASS_WITH_CAVEATS

---

## Executive Summary (Caveat-First)

**PASS verdict with mandatory caveats:**

Gate 4B v0.1.21 demonstrates **finite-lattice robustness** of the W=20 Anderson disorder localization signal under finite-size scaling on S³×S¹ product manifold.

**Key findings:**
- **True IPR contrast:** 7.15× aggregate (W=20 vs W=0)
- **Family consistency:** 3/3 families PASS independently (spectral_circle 4.25×, ring 8.31×, wilson_ring 8.49×)
- **Finite-size trend:** STRENGTHENING (s1_size 16→128: contrast 3.76× → 24.90×)
- **Level-spacing diagnostic:** r-statistic shift supports localization (Δr = -0.163)
- **Grid completion:** 216/216 cases (100%)

**Mandatory caveats (non-negotiable):**
1. **Finite-lattice only** — no thermodynamic limit (N ≤ 896)
2. **Anderson disorder only** — no general disorder claim
3. **S³×S¹ only** — no FL generalization (S²×S¹, S⁷×S¹, etc.)
4. **W=20 exploratory** — not optimal-W claim
5. **True IPR metric** — v0.1.21 measures eigenvector localization, NOT eigenvalue mean
6. **No physical compactification claim** — finite-lattice evidence ≠ continuum physics

**Forbidden claims:**
- ❌ "S³×S¹ validated"
- ❌ "FL generalized"
- ❌ "W=20 optimal"
- ❌ "Thermodynamic limit"
- ❌ "Physical compactification"

---

## Protocol Reference

**Pre-registration:** reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md  
**Commit:** `5e5ffc9` (protocol), `ad6936f` (true IPR implementation), `57c5174` (benchmark)  
**Execution freeze:** reports/S3_S1_GATE4B_RAW_EXECUTION_FREEZE_v0.1.21.md  
**Decision rules:** Section 8 of preregistration (UNCHANGED)  
**Thresholds:** UNCHANGED (≥2.0× for PASS, all families pre-registered)

**Protocol immutability:** No grid, threshold, or claim language changes after commit `5e5ffc9`.

---

## Why Gate 4B Was Needed

**Gate 4A v0.1.20 finding (2026-05-22):**
- 216/216 cases completed successfully
- **Critical bug:** Primary metric = mean(eigenvalues), NOT true IPR = mean(Σ|ψᵢ|⁴)
- Root cause: `np.linalg.eigvalsh(H)` returns eigenvalues only (no eigenvectors)
- True IPR unmeasurable from v0.1.20 outputs → full rerun required
- Verdict: WEAK_OR_INCONCLUSIVE (based on r-statistic only, primary metric invalid)

**v0.1.21 correction:**
- Changed `eigvalsh → eigh` (compute eigenvectors)
- Implemented true IPR = Σ|ψᵢ|⁴ for bottom 10% eigenstates
- Grid UNCHANGED (same 216 cases)
- Thresholds UNCHANGED (same decision rules)
- Claim language UNCHANGED
- **Only difference:** Metric formula correction

**Documentation:**
- S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md
- GATE4_TRUE_IPR_RECOVERY_CHECK_v0.1.20.md
- IPR_IMPLEMENTATION_AUDIT_v0.1.20.md

---

## Execution Summary

**Grid:**
- 3 families: spectral_circle, ring, wilson_ring
- 3 disorder strengths: W = 0, 12, 20
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

**Coverage verification:**
- ✅ 216 unique case combinations
- ✅ 0 duplicates
- ✅ 0 missing combinations
- ✅ All (family, W, size, j_max, seed) tuples present exactly once

---

## True IPR Results

### Aggregate Contrast

**W=20 vs W=0:**
- mean(IPR, W=0) = 0.0326
- mean(IPR, W=20) = 0.2333
- **Contrast ratio:** **7.15×**
- Threshold: ≥2.0× for PASS ✅

**Interpretation:** W=20 Anderson disorder increases IPR by 7.15× relative to W=0 baseline, indicating localization enhancement.

---

### Family-Level Contrasts

| Family | IPR(W=0) | IPR(W=20) | Contrast Ratio | Absolute Δ | Verdict |
|--------|----------|-----------|----------------|------------|---------|
| **spectral_circle** | 0.0224 | 0.0953 | **4.25×** | 0.0952 | ✅ PASS |
| **ring** | 0.0346 | 0.2874 | **8.31×** | 0.2874 | ✅ PASS |
| **wilson_ring** | 0.0259 | 0.2194 | **8.49×** | 0.2194 | ✅ PASS |

**Family consistency:** 3/3 families PASS (threshold: ≥2/3) ✅

**Domination check:**
- spectral_circle: 11.9% of aggregate absolute contrast
- ring: 35.9%
- wilson_ring: 27.4%
- **No single-family domination** (all ≤80%) ✅

**Key finding:** All three discretization families independently confirm W=20 localization signal. Ring and wilson_ring show stronger response than spectral_circle, but all exceed 2.0× threshold.

---

### Finite-Size Scaling Trend

**Contrast ratio vs s1_size:**

| s1_size | N (j_max=3) | Contrast Ratio | Trend |
|---------|-------------|----------------|-------|
| 16      | 112         | 3.76×          | —     |
| 32      | 224         | 6.73×          | ↑     |
| 64      | 448         | 11.93×         | ↑     |
| 128     | 896         | **24.90×**     | ↑     |

**Trend verdict:** STRENGTHENING ✅

**Interpretation:** IPR contrast increases with lattice size, indicating that localization signal is **not** a finite-size artifact. The signal strengthens rather than collapses as N → larger (within tested range N ≤ 896).

**Caveat:** Trend analysis limited to N ≤ 896. Thermodynamic limit (N→∞) behavior unknown.

---

## r-Statistic Results

**Level-spacing adjacent gap ratio:**

| W | r-statistic (mean) | Expected | Interpretation |
|---|-------------------|----------|----------------|
| 0 | 0.606             | ≈0.53 (GOE) | Ergodic (slightly above GOE) |
| 20 | 0.443            | ≈0.39 (Poisson) | Localized (between GOE and Poisson) |
| **Shift** | **-0.163** | negative | ✅ Toward localization |

**r-statistic verdict:** supports_localization ✅

**Interpretation:** r-statistic shifts from near-GOE (W=0) toward Poisson (W=20), consistent with localization interpretation of IPR contrast. The shift is substantial (-0.163), and level-spacing statistics are consistent with the IPR finding.

**Diagnostic consistency:** Both IPR and r-statistic agree on W=20 localization direction.

---

## Control Baseline (W=0)

**Stability check (coefficient of variation within each size):**

| s1_size | IPR(W=0) mean | CV | Verdict |
|---------|---------------|----|---------|
| 16      | 0.06821       | 0.121 | stable |
| 32      | 0.03533       | 0.163 | stable |
| 64      | 0.01795       | 0.183 | stable |
| 128     | 0.00903       | 0.190 | stable |

**Max CV:** 0.190 (threshold: <0.2 for stable) ✅

**Control verdict:** stable ✅

**Interpretation:** W=0 baseline shows expected 1/N scaling (IPR decreases with lattice size). Variability within each size is acceptable (CV <0.2), indicating no numerical instability or implementation errors.

---

## Decision Rule Application

**Pre-registered conditions (Section 8.1 of preregistration):**

| Condition | Threshold | Result | Status |
|-----------|-----------|--------|--------|
| 1. Aggregate contrast | ≥2.0× | 7.15× | ✅ PASS |
| 2. Family consistency | ≥2/3 families | 3/3 | ✅ PASS |
| 3. No single-family domination | ≤80% | max 35.9% | ✅ PASS |
| 4. Finite-size trend | stable/saturating/strengthening | STRENGTHENING | ✅ PASS |
| 5. r-statistic supports localization | shift toward Poisson | Δr = -0.163 | ✅ PASS |
| 6. No broad failure cluster | — | 0 failures | ✅ PASS |
| 7. Controls stable | CV <0.2 | max CV 0.190 | ✅ PASS |

**All 7 conditions satisfied → GATE4B_FSS_PASS_WITH_CAVEATS**

---

## Final Verdict

**Verdict:** **GATE4_FSS_PASS_WITH_CAVEATS**

**Reason:** All 7 pre-registered PASS conditions satisfied.

**Scientific statement:**
> S³×S¹ Gate 4B supports finite-lattice robustness of the W=20 Anderson disorder localization signal under finite-size scaling from s1_size=16 to 128 (N = 112 to 896), with true eigenvector-based IPR contrast ≥2.0× and family consistency ≥2/3.

---

## Caveats (Mandatory)

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

---

## Allowed Claims

**✅ ALLOWED:**
1. "Gate 4B supports finite-lattice robustness of W=20 localization signal on S³×S¹"
2. "True IPR contrast strengthens with lattice size (N = 112 → 896)"
3. "All three discretization families confirm W=20 contrast ≥2.0×"
4. "r-statistic diagnostic consistent with localization interpretation"
5. "No finite-size collapse observed in tested range"

**❌ FORBIDDEN:**
1. "S³×S¹ validated" (validation theater)
2. "FL generalized" (only S³×S¹ tested)
3. "W=20 optimal" (not tested)
4. "Thermodynamic limit confirmed" (N finite)
5. "Physical compactification" (lattice model only)
6. "v0.1.20 result reinterpreted" (metric incompatible)

---

## Comparison with v0.1.20

**v0.1.20 (eigenvalue-based):**
- Primary metric: mean(eigenvalues) for bottom 10% ❌
- Result: "contrast" NOT measurable as IPR
- Verdict: WEAK_OR_INCONCLUSIVE
- Valid outputs: r-statistic, eigenvalue trend (diagnostic)

**v0.1.21 (eigenvector-based):**
- Primary metric: mean(Σ|ψᵢ|⁴) for bottom 10% eigenstates ✅
- Result: 7.15× IPR contrast
- Verdict: PASS_WITH_CAVEATS
- All outputs valid: true IPR, r-statistic, eigenvalue diagnostic

**Key difference:** v0.1.21 measures wavefunction localization (physical quantity), v0.1.20 measured energy spectrum mean (unrelated to IPR).

**No retroactive upgrade:** v0.1.20 verdict remains WEAK. Cannot claim "v0.1.21 validates v0.1.20 finding" — different metrics, independent verdicts.

---

## Next Steps

**Immediate:**
1. ✅ Commit v0.1.21 results (this report + merged/ outputs)
2. Archive v0.1.20 outputs with erratum reference
3. Update README.md with v0.1.21 findings (replace v0.1.20 claims)

**Future work (not Gate 4B scope):**
1. **Gate 5 (if pursued):** Extend to larger N (s1_size=256, 512) to check saturation
2. **W-sweep:** Systematic W = 0, 5, 10, 15, 20, 25 to find optimal disorder strength
3. **Alternative geometries:** Test S²×S¹, other FL×S¹ products
4. **Thermodynamic limit extrapolation:** Finite-size scaling analysis to estimate N→∞ behavior
5. **Correlated disorder:** Beyond Anderson diagonal model
6. **Eigenvector structure:** Analyze spatial decay profiles, not just IPR scalar

**Scientific communication:**
- Use "finite-lattice robustness" language
- Always cite all 6 mandatory caveats
- Never use forbidden claim phrases
- Reference both preregistration and results commits

---

## Figures (Optional — Not Generated)

**Recommended figures (for future publication):**
1. `ipr_contrast_vs_size.png` — True IPR contrast vs s1_size, faceted by family
2. `family_comparison.png` — Bar chart: family-level contrast ratios
3. `r_statistic_vs_W.png` — Level-spacing r vs disorder strength, faceted by size
4. `finite_size_trend.png` — Aggregate contrast vs s1_size with error bars

**Note:** Figures not generated in this report due to time constraints. Data available in `reports/RUNS/gate4_fss_v0.1.21/merged/*.json`.

---

## Audit Trail

**Pre-registration commits:**
- `1f4173c` — v0.1.20 original protocol
- `5e5ffc9` — v0.1.21 metric-corrected protocol (grid unchanged)
- `ad6936f` — true IPR implementation
- `57c5174` — runtime benchmark

**Execution artifacts:**
- `reports/RUNS/gate4_fss_v0.1.21/batches/` — 9 batch outputs (216 cases)
- `reports/RUNS/gate4_fss_v0.1.21/merged/` — aggregated metrics + verdict analysis
- `reports/S3_S1_GATE4B_RAW_EXECUTION_FREEZE_v0.1.21.md` — execution freeze (before analysis)

**Protocol compliance:**
- ✅ Grid unchanged from preregistration
- ✅ Thresholds unchanged (≥2.0× for PASS)
- ✅ Decision rules unchanged (Section 8 applied verbatim)
- ✅ Claim language unchanged (allowed/forbidden lists enforced)
- ✅ No post-hoc tuning

**Date:** 2026-05-22 14:30 Almaty  
**Status:** FINAL  
**Verdict:** GATE4B_FSS_PASS_WITH_CAVEATS  
**Commit:** [pending]
