# Gate 4B Pre-Push Audit — v0.1.21

**Date:** 2026-05-22 15:45 Almaty  
**Commit:** f7eff32 (amended from b6e5892)  
**Auditor:** Claude Sonnet 4.5  
**Purpose:** Pre-push scientific integrity audit

---

## Executive Summary

**Verdict:** **SAFE_TO_PUSH** ✅

Gate 4B v0.1.21 commit f7eff32 прошёл полную проверку:
- 0 blocking issues
- 0 minor issues
- Все 7 audit пунктов PASS

**Метрическая корректность подтверждена:**
- True eigenvector-based IPR = Σ|ψᵢ|⁴ реализован корректно
- 17 unit tests passed
- Contrast calculations верифицированы
- N caveat корректен (896)
- No metric separation violations
- No overclaim в wording

**Рекомендация:** Commit готов к push без изменений.

---

## Raw Artifact Integrity

**Git status:** ✅ CLEAN
- Working directory: clean (no uncommitted changes)
- Commit: f7eff32 (amended from b6e5892 after N caveat fix)
- Branch: main

**Commit structure:** ✅ VERIFIED
- 59 files changed, 7757 insertions(+)
- reports/RUNS/gate4_fss_v0.1.21/ included with -f flag
- 9 batch folders present: batch_01 through batch_09
- merged/ artifacts present: 9 JSON files
- No missing raw data behind reports

**Batch inventory:** ✅ COMPLETE
```
batch_01/  2026-05-22 10:58  (spectral_circle, W=0)
batch_02/  2026-05-22 11:13  (spectral_circle, W=12)
batch_03/  2026-05-22 11:29  (spectral_circle, W=20)
batch_04/  2026-05-22 11:47  (ring, W=0)
batch_05/  2026-05-22 12:02  (ring, W=12)
batch_06/  2026-05-22 12:16  (ring, W=20)
batch_07/  2026-05-22 12:30  (wilson_ring, W=0)
batch_08/  2026-05-22 12:45  (wilson_ring, W=12)
batch_09/  2026-05-22 13:14  (wilson_ring, W=20)
```

**Merged artifacts:** ✅ COMPLETE
- coverage.json (216 unique cases, 0 duplicates)
- failure_summary.json (0 failures)
- family_summary.json (3 families)
- metrics.json (216 true_ipr_mean values)
- r_stat_summary.json (36 groups)
- size_scaling_summary.json (4 sizes)
- timing_summary.json (1.83h total)
- true_ipr_contrast_summary.json (72 per-seed contrasts)
- verdict_analysis.json (GATE4B_FSS_PASS_WITH_CAVEATS)

---

## Metric Implementation Check

**IPR formula:** ✅ CORRECT
```python
# From cc_toy_lab/spectral/metrics.py
def inverse_participation_ratio(vector):
    """IPR = sum |psi|^4 / (sum |psi|^2)^2"""
    norm_sq = np.sum(np.abs(arr) ** 2)
    denom = norm_sq**2
    return float(np.sum(np.abs(arr) ** 4) / denom)
```

**Eigenvector computation:** ✅ VERIFIED
- scripts/run_gate4_batched.py line 228: `eigvals, eigvecs = np.linalg.eigh(H)`
- NOT using `np.linalg.eigvalsh` (eigenvalues-only)
- Eigenvectors computed for all 216 cases

**Output schema:** ✅ VERIFIED
```json
{
  "true_ipr_mean": float,  // Canonical metric (v0.1.21)
  "uses_eigenvectors": true,
  "ipr_metric_version": "v0.1.21_true_eigenvector_ipr",
  "mean_low_eigenvalue": float,  // Diagnostic only
  "mean_low_ipr": float  // DEPRECATED alias (same as true_ipr_mean)
}
```

**Unit tests:** ✅ 17 PASSED
```
tests/test_ipr_metric.py:
✅ test_ipr_fully_localized_real → IPR ≈ 1.0
✅ test_ipr_fully_delocalized_real → IPR ≈ 1/N
✅ test_ipr_random_normalized_real → IPR ∈ (1/N, 1)
✅ test_ipr_zero_vector_raises_error → ValueError
✅ test_ipr_matrix_input_multiple_eigenvectors → correct batching
✅ test_ipr_bottom_10_percent_eigenvectors → Gate 4B scenario
✅ test_ipr_vs_eigenvalue_mean_not_equal → metrics differ
... 10 more tests passed
```

---

## Metric Separation Check

**Final report analysis:** ✅ CLEAN

**mean_low_ipr occurrences:** 0 (not found in positive claims)
- Correctly absent from final report scientific statements
- Only present as DEPRECATED alias in implementation details

**true_ipr_mean occurrences:** 1 (availability metric only)
- Line 93: "true_ipr_mean availability: 216/216 (100%)"
- Used correctly as availability count, not as direct metric name in claims

**Eigenvalue proxy separation:** ✅ CLEAR
- v0.1.20 comparison section explicitly states:
  - v0.1.20: "mean(eigenvalues) for bottom 10% ❌"
  - v0.1.21: "mean(Σ|ψᵢ|⁴) for bottom 10% eigenstates ✅"
- "Key difference: v0.1.21 measures wavefunction localization (physical quantity), v0.1.20 measured energy spectrum mean (unrelated to IPR)"
- "NO retroactive upgrade: v0.1.20 verdict remains WEAK"

---

## Contrast Verification

**Source:** reports/RUNS/gate4_fss_v0.1.21/merged/verdict_analysis.json

**Aggregate contrast:** ✅ VERIFIED
- Reported: 7.15×
- Calculated: mean(IPR_W=20) / mean(IPR_W=0) = 0.2333 / 0.0326 = 7.15×
- Threshold: ≥2.0× → **PASS**

**Family contrasts:** ✅ VERIFIED

| Family | Reported | Calculated | W=0 | W=20 | Status |
|--------|----------|------------|-----|------|--------|
| spectral_circle | 4.25× | 0.1245/0.0293 = 4.25× | 0.0293 | 0.1245 | ✅ PASS |
| ring | 8.31× | 0.3267/0.0393 = 8.31× | 0.0393 | 0.3267 | ✅ PASS |
| wilson_ring | 8.49× | 0.2487/0.0293 = 8.49× | 0.0293 | 0.2487 | ✅ PASS |

**Finite-size scaling trend:** ✅ VERIFIED

| s1_size | Reported | Calculated | Source |
|---------|----------|------------|--------|
| 16 | 3.76× | verdict_analysis.json | ✅ |
| 32 | 6.73× | verdict_analysis.json | ✅ |
| 64 | 11.93× | verdict_analysis.json | ✅ |
| 128 | 24.90× | verdict_analysis.json | ✅ |

**Trend verdict:** STRENGTHENING (3.76× → 24.90×, no collapse)

**JSON fields used:**
- `aggregate_contrast.aggregate_contrast_ratio`
- `aggregate_contrast.mean_ipr_w0`, `mean_ipr_w20`
- `family_contrasts[family].contrast_ratio`
- `family_contrasts[family].mean_ipr_w0`, `mean_ipr_w20`
- `finite_size_trend.size_trend_ratio[size]`

**No data mixing:** ✅ VERIFIED
- Sizes not mixed (separate aggregation by s1_size)
- Seeds aggregated correctly (mean over 3 seeds per group)
- j_max values handled separately in contrast computation

---

## N / Dimension Caveat Check

**Max N calculation:** ✅ VERIFIED
```
N = (2×j_max + 1) × s1_size
N_max = (2×3 + 1) × 128 = 7 × 128 = 896
N_min (j_max=3) = 7 × 16 = 112
```

**All N mentions in final report:** ✅ CORRECT

| Line | Context | Value | Status |
|------|---------|-------|--------|
| 25 | Executive summary caveat | N ≤ 896 | ✅ |
| 156 | FSS interpretation | N ≤ 896 | ✅ |
| 158 | FSS caveat | N ≤ 896 | ✅ |
| 224 | Scientific statement | N = 112 to 896 | ✅ |
| 231 | Caveats section | N ≤ 896 | ✅ |
| 234 | Extrapolation caveat | N=896 | ✅ |
| 276 | Allowed claims | N = 112 → 896 | ✅ |

**FSS table dimensions:** ✅ VERIFIED

| s1_size | N (j_max=3) | Reported | Calculated |
|---------|-------------|----------|------------|
| 16 | 112 | 112 | ✅ |
| 32 | 224 | 224 | ✅ |
| 64 | 448 | 448 | ✅ |
| 128 | 896 | 896 | ✅ |

**Prior error corrected:** ✅
- Original commit b6e5892 had N=7424 and N=3712 (incorrect)
- Amended commit f7eff32 corrected all to N=896 (8 places fixed)

---

## Wording / Overclaim Audit

**Forbidden claims searched:**
```bash
grep -in "validated|generalized|thermodynamic limit.*proven|
          compactification.*proven|physical.*proven|
          r-statistic confirms|W=20.*optimal"
```

**Results:** ✅ ALL CLEAN

**Forbidden terms found only in forbidden-claims sections:**
- Line 28: "W=20 exploratory — not optimal-W claim" (caveat header)
- Line 33-35: Forbidden claims list (explicitly forbidden)
- Line 254: "NO claim: W=20 is optimal" (caveat detail)
- Line 282-284: Forbidden claims list (repeated in section)

**No forbidden claims in positive sections:** ✅ VERIFIED

**r-statistic wording analysis:** ✅ SAFE

| Line | Wording | Assessment |
|------|---------|------------|
| 21 | "r-statistic shift supports localization" | ✅ Safe ("supports" not "confirms") |
| 172 | "r-statistic verdict: supports_localization" | ✅ Safe (internal label) |
| 174 | "consistent with localization interpretation" | ✅ Safe |
| 174 | "level-spacing statistics are consistent with the IPR finding" | ✅ Safe |
| 176 | "IPR and r-statistic agree on W=20 localization direction" | ✅ Safe (directional agreement, not proof) |
| 209 | "r-statistic supports localization" | ✅ Safe (decision rule label) |
| 278 | "r-statistic diagnostic consistent with localization interpretation" | ✅ Safe |

**Preferred wording used:**
- "supports" ✅
- "consistent with" ✅
- "agree on direction" ✅

**Avoided wording:**
- "confirms" ❌ (not found)
- "proves" ❌ (not found)
- "demonstrates" ❌ (not found in r-stat context)

---

## Caveats Preserved

**Mandatory caveats checklist:** ✅ ALL PRESENT

### 1. Finite-Lattice Only ✅
- **Present:** Lines 230-234
- **Content:** N ≤ 896, no thermodynamic limit, trend ≠ proof, extrapolation requires data
- **Assessment:** Complete

### 2. Anderson Disorder Only ✅
- **Present:** Lines 236-242
- **Content:** Diagonal on-site U(r) ∈ [-W, W], no correlated/off-diagonal/time-dependent/quasiperiodic
- **Assessment:** Complete

### 3. S³×S¹ Only ✅
- **Present:** Lines 244-250
- **Content:** 3-sphere cross circle, no S²×S¹/S⁷×S¹/arbitrary FL×S¹/non-product
- **Assessment:** Complete

### 4. W=20 Exploratory ✅
- **Present:** Lines 252-256
- **Content:** Chosen from Gate 3C, not optimal, no W-sweep, W=12 diagnostic only
- **Assessment:** Complete

### 5. True IPR Metric ✅
- **Present:** Lines 258-262
- **Content:** v0.1.21 = Σ|ψᵢ|⁴, v0.1.20 invalid, not comparable, no retroactive reinterpretation
- **Assessment:** Complete

### 6. No Physical Compactification ✅
- **Present:** Lines 264-268
- **Content:** Finite-lattice ≠ continuum, no 4D spacetime claim, no Kaluza-Klein, computational only
- **Assessment:** Complete

**Additional caveats beyond mandatory:** ✅
- No Standard Model claim (implied by computational-only caveat)
- No chirality claim (not mentioned in positive claims)
- No FL generalization (explicit caveat)

---

## Files Reviewed

**Core results:**
- reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md (369 lines)
- reports/S3_S1_GATE4B_RAW_EXECUTION_FREEZE_v0.1.21.md (224 lines)

**Raw outputs:**
- reports/RUNS/gate4_fss_v0.1.21/batches/batch_01/ through batch_09/ (45 files)
- reports/RUNS/gate4_fss_v0.1.21/merged/*.json (9 files)
- reports/RUNS/gate4_fss_v0.1.21/config.json

**Scripts:**
- scripts/aggregate_gate4b_results.py (210 lines)
- scripts/apply_gate4b_decision_rules.py (461 lines)
- scripts/run_gate4_batched.py (line 228 verified)

**Implementation:**
- cc_toy_lab/spectral/metrics.py (IPR function lines 21-45)

**Tests:**
- tests/test_ipr_metric.py (17 tests, all passed)

**Total files in commit:** 59

---

## Required Fixes Before Push

**Blocking issues:** 0

**Minor issues:** 0

**All audit checks:** PASS

**No changes required.**

---

## Final Verdict

**Verdict:** **SAFE_TO_PUSH** ✅

**Summary:**
- Raw artifact integrity: ✅ VERIFIED
- Metric implementation: ✅ CORRECT (true IPR = Σ|ψ|⁴, 17 tests passed)
- Metric separation: ✅ CLEAN (no v0.1.20 proxy confusion)
- Contrast verification: ✅ VERIFIED (7.15× aggregate, all families PASS)
- N caveat: ✅ CORRECT (N=896, all mentions consistent)
- Wording audit: ✅ SAFE (no forbidden overclaims, r-stat wording appropriate)
- Caveats: ✅ COMPLETE (all 6 mandatory caveats present)

**Blocking issues:** 0  
**Minor issues:** 0  
**Files changed since audit start:** 0

**Commit ready for push:** f7eff32

**Recommendation:** Proceed with push to remote.

---

**Audit completed:** 2026-05-22 15:45 Almaty  
**Auditor signature:** Claude Sonnet 4.5 (scientific integrity audit)  
**Commit audited:** f7eff32  
**Branch:** main  
**Status:** SAFE_TO_PUSH
