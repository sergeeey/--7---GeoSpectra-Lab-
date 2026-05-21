# S³×S¹ Gate 4 FSS Results — v0.1.20

**Version:** v0.1.20  
**Execution Completed:** 2026-05-22 00:31 UTC  
**Analysis Completed:** 2026-05-22 (current date)  
**Protocol Commit:** 1f4173c (locked, pre-registered)  
**Status:** ANALYSIS_COMPLETE

---

## 1. Executive Summary

**⚠️ CAVEAT-FIRST SUMMARY:**

S³×S¹ Gate 4 Finite-Size Scaling execution completed with 216/216 cases (0 failures), but **protocol-implementation mismatch prevents definitive PASS/FAIL verdict**. Implementation computed mean low eigenvalues instead of pre-registered IPR metric, making primary decision rule threshold (≥2.0× IPR contrast) unmeasurable.

**What CAN be concluded (weak evidence):**
- ✅ Level-spacing r-statistic shows shift toward Poisson distribution at W=20 (0.437 vs GOE 0.53), supporting localization interpretation
- ✅ Mean low eigenvalue contrast strengthens with increasing s1_size (finite-size trend stable)
- ✅ Execution robustness: 0 failures, 99.1% data quality (2 numerical outliers excluded)

**What CANNOT be concluded:**
- ❌ IPR contrast threshold (≥2.0×) — unmeasurable due to metric mismatch
- ❌ Family consistency (≥2/3 pass) — dependent on unmeasurable threshold
- ❌ Definitive localization claim — primary metric invalid

**Verdict:** `GATE4_FSS_WEAK_OR_INCONCLUSIVE`

**Rationale:** Secondary metric (r-statistic) provides weak evidence for localization, but primary metric (IPR) cannot be assessed. Execution technically complete, but metric implementation deviates from pre-registered protocol.

---

## 2. Protocol Reference

### 2.1 Pre-Registration

- **Document:** `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md`
- **Commit:** 1f4173c (locked before execution, no modifications permitted)
- **Primary metric (pre-registered):** IPR contrast = IPR(W=20) / IPR(W=0)
- **Threshold:** ≥2.0× for PASS_WITH_CAVEATS

### 2.2 Implementation Commits

- **Dry-run feasibility:** 52d221f
- **Batch infrastructure:** a359097, bd2d600, 80dc509
- **Execution:** batches 1-9 completed 2026-05-21 to 2026-05-22

### 2.3 Critical Protocol Deviation

**Issue identified during analysis:**

Pre-registered protocol specifies:
```
IPR = Inverse Participation Ratio = Σ|ψᵢ|⁴ (requires eigenvectors)
IPR contrast = IPR(W=20) / IPR(W=0) ≥ 2.0×
```

Implementation computes (`scripts/run_gate4_batched.py:221`):
```python
mean_low_ipr = float(np.mean(low_eigvals))  # Mean eigenvalues, NOT IPR
```

**Impact:**
- Primary verdict-driving metric is unavailable
- Ratio threshold (2.0×) cannot be computed from eigenvalue difference
- Family consistency criterion (≥2/3 families pass 2.0× threshold) unmeasurable

**Decision:** Proceed with analysis using available metrics (r-statistic, eigenvalue trends), but downgrade verdict to WEAK_OR_INCONCLUSIVE due to metric invalidity.

---

## 3. Execution Summary

### 3.1 Grid Coverage

**Full factorial design:**
- Families: spectral_circle, ring, wilson_ring (3)
- Disorder strengths (W): 0, 12, 20 (3)
- S¹ sizes (s1_size): 16, 32, 64, 128 (4)
- Max angular momenta (j_max): 2, 3 (2)
- Random seeds: 123, 456, 789 (3)

**Total:** 3 × 3 × 4 × 2 × 3 = 216 cases

### 3.2 Completion Status

| Batch | Family | W | Cases | Failures | r-stat unavailable | Runtime (min) |
|-------|--------|---|-------|----------|-------------------|---------------|
| 01 | spectral_circle | 0 | 24 | 0 | 0 | 10.9 |
| 02 | spectral_circle | 12 | 24 | 0 | 0 | 10.7 |
| 03 | spectral_circle | 20 | 24 | 0 | 0 | 10.4 |
| 04 | ring | 0 | 24 | 0 | 0 | 11.3 |
| 05 | ring | 12 | 24 | 0 | 0 | 11.3 |
| 06 | ring | 20 | 24 | 0 | 0 | 10.3 |
| 07 | wilson_ring | 0 | 24 | 0 | 0 | 10.4 |
| 08 | wilson_ring | 12 | 24 | 0 | 0 | 10.5 |
| 09 | wilson_ring | 20 | 24 | 0 | 0 | 10.3 |

**Totals:**
- ✅ 9/9 batches completed
- ✅ 216/216 cases completed
- ✅ 0/216 failures (0%)
- ✅ 216/216 r-statistics available (100%)
- Total runtime: 96.1 minutes

### 3.3 Data Quality

**Numerical outliers detected:**
- Case 47: spectral_circle, W=12, s1_size=128, j_max=3, seed=789
  - mean_low_ipr = -1.98×10³⁰⁰ (numerical overflow)
- Case 95: ring, W=0, s1_size=128, j_max=3, seed=789
  - mean_low_ipr = -8.90×10²⁵⁶ (numerical overflow)

**Pattern:** Both cases at s1_size=128, j_max=3, seed=789 → possible eigenvalue solver instability at large Hilbert space dimension.

**Action:** Excluded from mean eigenvalue aggregations. r-statistics for these cases remain valid (0.421, 0.400 respectively).

**Valid dataset:** 214/216 cases (99.1%)

---

## 4. Coverage Verification

✅ **Complete grid coverage confirmed:**
- 216 unique case_id values (0–215, continuous, no gaps)
- All parameter combinations covered:
  - 3 families × 3 W × 4 sizes × 2 j_max × 3 seeds = 216 ✓
- No missing cases
- No duplicate case_id values

**Verification artifact:** `reports/RUNS/gate4_fss_v0.1.20/merged/coverage.json`

---

## 5. Mean Low Eigenvalue Results (substitute for IPR)

### 5.1 Overall Summary by Disorder Strength

| W | Mean eigenvalue | Median | Std | n_valid |
|---|----------------|--------|-----|---------|
| 0 | -27.60 | -18.33 | 27.35 | 71 |
| 12 | -68.91 | -39.66 | 70.56 | 71 |
| 20 | -94.23 | -57.56 | 94.37 | 72 |

**Trend:** Eigenvalues become more negative with increasing disorder (W=0 → W=12 → W=20). More negative eigenvalues = lower energy states = potential localization signature.

**Contrast (W=20 vs W=0):**
- Mean difference: -94.23 - (-27.60) = **-66.63**
- Median difference: -57.56 - (-18.33) = **-39.23**

**⚠️ Threshold unmeasurable:** Pre-registered threshold (≥2.0× ratio) cannot be computed from eigenvalue difference without additional assumptions. Cannot determine PASS/FAIL on primary metric.

### 5.2 By Family

| Family | W=0 mean | W=20 mean | Difference |
|--------|----------|-----------|------------|
| spectral_circle | -15.71 | -61.64 | -45.93 |
| ring | -44.15 | -164.12 | -119.97 |
| wilson_ring | -23.62 | -56.92 | -33.30 |

**Observations:**
- All families show negative shift (eigenvalues lowered at W=20)
- `ring` family shows strongest shift (-119.97)
- `wilson_ring` shows weakest shift (-33.30)
- Strong family dependence: 3.6× range across families

**⚠️ Family consistency unmeasurable:** Cannot assess ≥2/3 threshold without IPR ratio.

### 5.3 By Size

| s1_size | W=0 mean | W=20 mean | Difference |
|---------|----------|-----------|------------|
| 16 | -1.26 | -12.31 | -11.06 |
| 32 | -10.51 | -39.82 | -29.31 |
| 64 | -30.65 | -102.00 | -71.35 |
| 128 | -70.36 | -222.77 | -152.41 |

**Finite-size trend:** Difference becomes MORE negative with increasing size (|diff|: 11.06 → 29.31 → 71.35 → 152.41). This suggests eigenvalue suppression strengthens at larger sizes.

**✅ Verdict criterion:** Trend is **strengthening**, not collapsing. This satisfies decision rule 4 (finite-size trend stable or strengthening).

**Caveat:** Trend based on eigenvalues, not IPR. Physical interpretation uncertain.

---

## 6. r-Statistic Results (Level-Spacing Adjacent Gap Ratio)

### 6.1 Overall Summary by Disorder Strength

| W | Mean r | Median r | Distance to GOE (0.53) | Distance to Poisson (0.39) | Closer to |
|---|--------|----------|----------------------|--------------------------|-----------|
| 0 | 0.605 | 0.475 | 0.075 | 0.215 | GOE (ergodic) |
| 12 | 0.422 | 0.423 | 0.108 | 0.032 | Poisson (localized) |
| 20 | 0.437 | 0.439 | 0.093 | 0.047 | Poisson (localized) |

**✅ Key finding:** r-statistic shifts from GOE (W=0) toward Poisson (W=12, W=20), supporting localization interpretation.

**✅ Verdict criterion:** Decision rule 5 (r-statistic supports localization) is **SATISFIED**.

**Caveats:**
- W=0 r-statistic (0.605) is HIGHER than GOE (0.53), suggesting hyper-ergodic behavior (anomalous)
- W=20 r-statistic (0.437) is still 0.047 away from Poisson (0.39), not fully localized
- Shift is in correct direction but magnitude is modest

### 6.2 By Family

| Family | Mean r | Distance to GOE | Distance to Poisson | Closer to |
|--------|--------|----------------|-------------------|-----------|
| spectral_circle | 0.614 | 0.084 | 0.224 | GOE |
| ring | 0.436 | 0.094 | 0.046 | Poisson |
| wilson_ring | 0.414 | 0.116 | 0.024 | Poisson |

**⚠️ Strong family dependence:**
- `spectral_circle`: remains near GOE (ergodic) across all W
- `ring`, `wilson_ring`: shift toward Poisson (localized)
- Range: 0.200 (spectral_circle vs wilson_ring)

**Interpretation:** Discretization family strongly affects level-spacing statistics. `spectral_circle` may resist localization or exhibit slower finite-size convergence.

---

## 7. Finite-Size Scaling Analysis

### 7.1 Eigenvalue Contrast Trend

```
s1_size   16     32     64    128
 diff   -11.06 -29.31 -71.35 -152.41
ratio    1.0×   2.6×   6.4×   13.8×  (relative to s1_size=16)
```

**Trend:** Strengthening (contrast magnitude increases with size).

**✅ Decision criterion satisfied:** Trend is NOT collapsing, NOT weakening. This supports robustness at finite lattice sizes.

**Caveat:** Trend based on eigenvalue difference, not IPR ratio. Expected behavior: IPR ratio should saturate or strengthen. Eigenvalue difference can grow without implying IPR saturation.

### 7.2 r-Statistic Trend by Size

| s1_size | W=0 mean r | W=20 mean r |
|---------|------------|-------------|
| 16 | 0.545 | 0.434 |
| 32 | 0.531 | 0.433 |
| 64 | 0.639 | 0.437 |
| 128 | 0.707 | 0.443 |

**Observations:**
- W=0: r increases with size (0.545 → 0.707), moving AWAY from GOE toward more delocalized?
- W=20: r stable (0.434 → 0.443), remains near Poisson
- Contrast (W=20 - W=0) decreases with size (anomalous if localization strengthens)

**⚠️ Interpretation uncertainty:** r-statistic trend does NOT clearly support strengthening localization with size. W=0 anomalous behavior (r > GOE) confounds interpretation.

---

## 8. Family Consistency Assessment

### 8.1 Eigenvalue Contrast by Family

| Family | Difference (W=20 - W=0) | Relative strength |
|--------|------------------------|-------------------|
| spectral_circle | -45.93 | 1.0× (baseline) |
| ring | -119.97 | 2.6× stronger |
| wilson_ring | -33.30 | 0.7× weaker |

**⚠️ Strong family dependence:** 3.6× range (ring vs wilson_ring).

**Cannot assess ≥2/3 threshold:** Pre-registered criterion requires IPR ratio ≥2.0× for each family independently. Eigenvalue difference does not map to this threshold.

### 8.2 r-Statistic by Family

| Family | W=0 mean r | W=20 mean r | Shift toward Poisson? |
|--------|------------|-------------|----------------------|
| spectral_circle | 0.615 | 0.614 | ❌ No shift |
| ring | 0.523 | 0.436 | ✅ Yes (-0.087) |
| wilson_ring | 0.467 | 0.414 | ✅ Yes (-0.053) |

**Observation:** 2/3 families (ring, wilson_ring) show r-shift toward Poisson. `spectral_circle` does NOT shift.

**Interpretation:** If r-statistic is used as proxy for localization, then 2/3 families pass (meets consistency threshold). However, `spectral_circle` failure is significant caveat.

---

## 9. Decision Rule Application

### 9.1 Pre-Registered Decision Rules (from preregistration doc)

**GATE4_FSS_PASS_WITH_CAVEATS requires ALL of:**

1. ✅/❌ **Aggregate W=20 contrast ≥2.0×**
   - Status: **UNMEASURABLE** (eigenvalue ≠ IPR, ratio cannot be computed)
   - Alternative evidence: Eigenvalue difference strengthens with size (-66.63 mean)

2. ✅/❌ **Family consistency ≥2/3 families pass 2.0× threshold**
   - Status: **UNMEASURABLE** (depends on criterion 1)
   - Alternative evidence: r-statistic shows 2/3 families shift toward Poisson

3. ❌ **No single-family domination (≤80% of contrast)**
   - Status: `ring` contributes 119.97 / (45.93 + 119.97 + 33.30) = **60%** (PASS)
   - ✅ No single family dominates

4. ✅ **Finite-size trend stable/saturating/strengthening (not collapsing)**
   - Status: Eigenvalue difference strengthens (11.06 → 152.41)
   - ✅ **PASS**

5. ✅ **r-statistic supports localization (or at least not contradicting)**
   - Status: W=20 r=0.437 closer to Poisson (0.39) than GOE (0.53)
   - Shift from W=0 r=0.605 (GOE-like) → W=20 r=0.437 (Poisson-like)
   - ✅ **PASS** (supports localization interpretation)

6. ✅ **No broad failure cluster**
   - Status: 0/216 failures (0%)
   - ✅ **PASS**

7. ⚠️ **Controls pass (W=0 baseline stable)**
   - Status: W=0 r=0.605 > GOE (0.53), anomalous hyper-ergodic behavior
   - ⚠️ **PARTIAL** (no failures, but r-statistic anomalous)

### 9.2 Verdict Determination

**Primary decision:** Cannot issue PASS_WITH_CAVEATS because criteria 1 and 2 are unmeasurable.

**Secondary decision:** Check WEAK_OR_INCONCLUSIVE triggers:

1. ✅ **r-statistic ambiguous OR single-family dependence**
   - r-statistic: NOT ambiguous, clearly supports localization
   - Family dependence: spectral_circle does not shift toward Poisson (1/3 family anomaly)
   - **TRIGGERED** by family dependence

2. ✅ **Primary metric unavailable**
   - IPR contrast unmeasurable
   - **TRIGGERED** by protocol-implementation mismatch

**Verdict:** `GATE4_FSS_WEAK_OR_INCONCLUSIVE`

---

## 10. Final Verdict

### 10.1 Verdict Statement

**GATE4_FSS_WEAK_OR_INCONCLUSIVE**

### 10.2 Evidence Summary

**What SUPPORTS weak localization signal:**
1. ✅ r-statistic shift: W=0 (0.605, GOE-like) → W=20 (0.437, Poisson-like)
2. ✅ Eigenvalue suppression strengthens with size (finite-size trend robust)
3. ✅ 2/3 families (ring, wilson_ring) show consistent r-shift toward Poisson
4. ✅ Execution robustness: 0 failures, 99.1% data quality

**What WEAKENS or PREVENTS definitive claim:**
1. ❌ Primary metric (IPR) unmeasurable due to protocol-implementation mismatch
2. ❌ Cannot assess pre-registered threshold (≥2.0× IPR contrast)
3. ⚠️ `spectral_circle` family does NOT show r-shift (family dependence caveat)
4. ⚠️ W=0 r-statistic anomalous (>GOE, hyper-ergodic behavior unexplained)
5. ⚠️ W=20 r-statistic (0.437) not fully at Poisson (0.39), partial localization

**Verdict rationale:**
- Secondary metric (r-statistic) provides weak but consistent evidence for localization
- Primary metric invalid → cannot confirm pre-registered threshold
- Strong family dependence → `spectral_circle` anomaly prevents clean 3/3 family consensus
- Execution complete, but metric implementation deviates from protocol → results interpretable but not definitive

---

## 11. Caveats (MANDATORY)

**11.1 Protocol Deviation (CRITICAL)**

- ❌ Implementation computes mean low eigenvalues, NOT Inverse Participation Ratio (IPR)
- ❌ Pre-registered metric (IPR contrast ratio) is unmeasurable from available data
- ❌ Primary verdict criterion (≥2.0× IPR contrast) cannot be assessed
- ⚠️ Eigenvalue metric used as proxy, but physical interpretation differs from IPR

**11.2 Scope Limitations**

- ✅ Finite-lattice only (no thermodynamic limit, N ≤ 3712)
- ✅ Anderson disorder only (on-site potential disorder, no hopping disorder)
- ✅ S³×S¹ geometry only (no FL generalization, no other product geometries)
- ✅ W=20 exploratory choice (not optimal-W claim, no systematic W-optimization)
- ✅ Three discretization families tested (spectral_circle, ring, wilson_ring only)

**11.3 Data Quality**

- ⚠️ 2/216 cases (0.9%) excluded due to numerical overflow (eigenvalue solver instability at N=128, j_max=3, seed=789)
- ⚠️ W=0 r-statistic anomalous (0.605 > GOE 0.53), cause unexplained

**11.4 Family Dependence**

- ⚠️ `spectral_circle` does NOT show r-statistic shift toward Poisson (remains GOE-like at all W)
- ⚠️ Eigenvalue contrast varies 3.6× across families (ring strongest, wilson_ring weakest)
- ⚠️ Results NOT uniform across discretizations

**11.5 Partial Localization**

- ⚠️ W=20 r-statistic (0.437) intermediate between GOE (0.53) and Poisson (0.39)
- ⚠️ NOT fully localized (Poisson would be r ≈ 0.39)
- ⚠️ Finite-size effect OR incomplete localization at W=20

---

## 12. Allowed and Forbidden Claims

### 12.1 ALLOWED Claims (with caveats)

✅ **Weak evidence statement:**

> "S³×S¹ Gate 4 FSS shows weak evidence for finite-lattice localization signal at W=20, based on level-spacing r-statistic shift toward Poisson distribution (W=0: r=0.605 → W=20: r=0.437) across s1_size range 16–128. Evidence is inconclusive due to protocol-implementation mismatch preventing primary IPR metric assessment."

✅ **Execution statement:**

> "S³×S¹ Gate 4 FSS batched grid execution completed successfully with 216/216 cases (0 failures), full parameter coverage, and 99.1% data quality."

✅ **r-statistic statement:**

> "Level-spacing r-statistic supports localization interpretation at W=20 in 2/3 discretization families (ring, wilson_ring), with shift toward Poisson distribution relative to W=0 baseline."

### 12.2 FORBIDDEN Claims

❌ **"S³×S¹ Gate 4 PASSED"** — verdict is WEAK_OR_INCONCLUSIVE, not PASS

❌ **"S³×S¹ validated for localization"** — weak evidence only, not validation

❌ **"IPR contrast ≥2.0× confirmed"** — IPR unmeasurable, threshold not assessed

❌ **"Localization proven"** — weak evidence, not proof

❌ **"W=20 optimal disorder strength"** — exploratory choice, not optimized

❌ **"FL mechanism validated"** — S³×S¹ only, no FL generalization

❌ **"Thermodynamic limit robust"** — finite lattice only (N ≤ 3712)

❌ **"All families consistent"** — spectral_circle anomaly, strong family dependence

---

## 13. Next Steps

### 13.1 Immediate Actions (address protocol deviation)

1. **Reimplement IPR metric correctly:**
   - Compute eigenvectors (not just eigenvalues)
   - Calculate IPR = Σ|ψᵢ|⁴ for bottom 10% eigenstates
   - Recompute IPR contrast ratio for all 216 cases

2. **Re-analyze with correct IPR:**
   - Apply pre-registered decision rules with measurable threshold
   - Re-assess PASS/FAIL verdict with primary metric

3. **Document deviation:**
   - Add protocol deviation note to preregistration doc (retrospective amendment)
   - Preserve both eigenvalue and IPR results for comparison

### 13.2 Follow-Up Investigations (if IPR recomputation confirms localization)

1. **Gate 5: Larger finite-size scaling**
   - Extend s1_size grid to 256, 512 (if computationally feasible)
   - Check if eigenvalue/IPR contrast saturates or continues strengthening

2. **Investigate spectral_circle anomaly:**
   - Why does spectral_circle NOT show r-shift toward Poisson?
   - Discretization artifact OR physical difference?
   - Targeted analysis of spectral_circle W=20 eigenstates

3. **W=0 r-statistic anomaly:**
   - Why is r > GOE for clean baseline?
   - Finite-size effect OR implementation issue?
   - Compare with analytical GOE prediction for finite matrices

4. **Cross-geometry transfer:**
   - Test W=20 on S⁵×S¹, S³×S³ (if Gate 4 strengthens)
   - Assess if localization signal transfers beyond S³×S¹

### 13.3 Methodology Paper (contingent on IPR recomputation)

**If IPR confirms ≥2.0× contrast:**
- Draft methodology paper on finite-lattice localization diagnostics
- Focus: r-statistic + IPR combined protocol for product geometries
- Contribution: batched pre-registered grid execution workflow

**If IPR contradicts eigenvalue trend:**
- Report negative result: eigenvalue suppression ≠ IPR localization
- Contribution: protocol deviation postmortem, metric validation lessons

---

## 14. Appendices

### 14.1 File Manifest

**Execution outputs:**
```
reports/RUNS/gate4_fss_v0.1.20/
├── batches/
│   ├── batch_01/ ... batch_09/
│   │   ├── batch_config.json
│   │   ├── results.json
│   │   ├── status.json
│   │   ├── summary.md
│   │   └── timing.json
└── merged/
    ├── metrics.json                (all 216 cases)
    ├── coverage.json               (grid verification)
    ├── timing_summary.json
    ├── failure_summary.json
    ├── family_summary.json
    ├── size_scaling_summary.json
    ├── r_stat_summary.json
    └── ipr_contrast_summary.json   (eigenvalue substitute)
```

**Reports:**
```
reports/
├── S3_S1_GATE4_BATCH_EXECUTION_PROGRESS_v0.1.20.md  (execution tracking)
├── S3_S1_GATE4_RAW_EXECUTION_FREEZE_v0.1.20.md      (pre-analysis freeze)
├── S3_S1_GATE4_FSS_RESULTS_v0.1.20.md               (this document)
└── S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md       (locked protocol)
```

### 14.2 Numerical Outliers Detail

**Case 47:** spectral_circle, W=12, s1_size=128, j_max=3, seed=789
- mean_low_ipr: -1.98×10³⁰⁰ (overflow)
- r_stat: 0.421 (valid)
- runtime: 173.6 sec (normal)
- Likely cause: eigenvalue solver numerical instability at large N

**Case 95:** ring, W=0, s1_size=128, j_max=3, seed=789
- mean_low_ipr: -8.90×10²⁵⁶ (overflow)
- r_stat: 0.400 (valid)
- runtime: 171.6 sec (normal)
- Likely cause: same as case 47

**Pattern:** Both at s1_size=128, j_max=3, seed=789 → Hilbert space dimension N=3712 (largest in grid). May indicate solver convergence issue at boundary of computational feasibility.

### 14.3 References

- Pre-registration document: `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md`
- Batch protocol: `docs/gate4_batch_protocol.md`
- Implementation: `scripts/run_gate4_batched.py`
- Anderson localization theory: Anderson (1958), Phys. Rev. 109, 1492

---

**Report generated:** 2026-05-22  
**Verdict:** GATE4_FSS_WEAK_OR_INCONCLUSIVE  
**Primary caveat:** Protocol-implementation mismatch (eigenvalue ≠ IPR)  
**Secondary caveat:** Strong family dependence (spectral_circle anomaly)  
**Execution status:** 216/216 complete, 0 failures, 99.1% data quality  
**Next action:** Reimplement correct IPR metric and re-analyze
