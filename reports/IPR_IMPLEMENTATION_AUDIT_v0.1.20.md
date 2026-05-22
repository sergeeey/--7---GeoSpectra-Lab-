# IPR Implementation Audit — Codebase-Wide Review

**Date:** 2026-05-22  
**Scope:** All uses of `mean_low_ipr` field and IPR claims across codebase  
**Trigger:** Gate 4 v0.1.20 metric mismatch discovery  
**Status:** Initial audit (pre-correction)

---

## 1. Audit Summary

**Audit question:**
- Which experiments computed true IPR (Σ|ψᵢ|⁴)?
- Which experiments used eigenvalue-based proxy labeled as "IPR"?
- Which results/claims require correction or retraction?

**Finding:**
- ❌ NO script in codebase computes true IPR from eigenvectors
- ❌ ALL uses of `mean_low_ipr` field are eigenvalue-based
- ⚠️ Multiple scripts compute "mean IPR" from `mean_low_ipr` field (eigenvalue proxy)
- ⚠️ README.md contains tables labeled "mean IPR" that may be eigenvalues

**Impact:**
- Gate 1, 2, 3 IPR claims require verification
- Disorder sweep "optimal W" analysis may be based on eigenvalue proxy
- Any IPR ratio/contrast claims across entire project history are suspect

---

## 2. Files Using `mean_low_ipr` Field

### 2.1 Gate 4 Scripts (Direct Mismatch)

**File:** `scripts/run_gate4_batched.py`  
**Lines:** 218-221  
**Code:**
```python
# IPR metric (from dry-run)
N = H.shape[0]
low_eigvals = eigvals[: int(0.1 * N)]  # Bottom 10%
mean_low_ipr = float(np.mean(low_eigvals))
```
**Status:** ❌ CONFIRMED MISMATCH — computes mean eigenvalue, not IPR  
**Usage:** Gate 4 v0.1.20 (216 cases), erratum filed

---

**File:** `scripts/run_gate4_dry_run.py`  
**Line:** 143  
**Code:**
```python
mean_low_ipr = float(np.mean(low_eigvals))  # Placeholder metric
```
**Comment:** Explicitly labeled "Placeholder metric"  
**Status:** ⚠️ Placeholder acknowledged, but propagated to production without correction

---

### 2.2 Gate 3 Scripts (Likely Mismatch)

**File:** `scripts/run_gate3c_confirmatory.py`  
**Lines:** 64-66, 110-111, 129-130, 148-149  
**Code:**
```python
clean_mean = np.mean([r["mean_low_ipr"] for r in clean_cases])
w12_mean = np.mean([r["mean_low_ipr"] for r in w12_cases])
w20_mean = np.mean([r["mean_low_ipr"] for r in w20_cases])
```
**Output:**
```python
print(f"Clean (W=0):      mean IPR = {clean_mean:.4f} ({len(clean_cases)} cases)")
print(f"W=12 (Gate 3):    mean IPR = {w12_mean:.4f} ({len(w12_cases)} cases)")
print(f"W=20 (exploratory): mean IPR = {w20_mean:.4f} ({len(w20_cases)} cases)")
```
**Status:** ❌ LIKELY MISMATCH — reads `mean_low_ipr`, prints as "mean IPR"  
**Action required:** Verify source of `mean_low_ipr` field in Gate 3 data

---

**File:** `scripts/run_gate3_full.py`  
**Line:** 36  
**Code:**
```python
print(f'**Absolute IPR Contrast: {agg["ipr_contrast_absolute"]:.2f}x**')
```
**Status:** ⚠️ UNKNOWN — depends on how `agg["ipr_contrast_absolute"]` was computed  
**Action required:** Trace aggregation logic, verify source metric

---

### 2.3 Disorder Sweep Scripts (Likely Mismatch)

**File:** `scripts/run_disorder_sweep.py`  
**Lines:** 71, 78, 87, 105  
**Code:**
```python
w_mean_ipr = sum(r["mean_low_ipr"] for r in w_cases) / len(w_cases)
print(f"  W={w:5.1f}: mean IPR = {w_mean_ipr:.4f} ({len(w_cases)} cases)")

clean_mean = sum(r["mean_low_ipr"] for r in clean_cases) / len(clean_cases)
```
**Output lines:** 55-56  
```python
print(f"  Clean IPR (W=0):     {agg['clean_mean_ipr_absolute']:.4f}")
print(f"  Disordered IPR (all): {agg['disordered_mean_ipr_absolute']:.4f}")
```
**Purpose:** "Find optimal disorder strength for max IPR contrast" (line 28)  
**Status:** ❌ LIKELY MISMATCH — reads `mean_low_ipr`, interprets as IPR  
**Impact:** "Optimal W" recommendation may be based on eigenvalue proxy, not true IPR

---

### 2.4 Anderson 3D Benchmarks (IPR References, Source Unknown)

**Files:**
- `scripts/anderson_3d_benchmark.py` (lines 39, 115)
- `scripts/anderson_3d_boundary_comparison.py` (lines 217, 380, 446, 497, 527, etc.)
- `scripts/anderson_3d_periodic_followup.py` (lines 207, 435, 598, 678, etc.)
- `scripts/anderson_3d_window_failure_diagnostics.py` (lines 132, 213, 282, 343)

**Status:** ⚠️ UNCLEAR — these scripts reference "IPR" but do NOT directly use `mean_low_ipr` field  
**Possibility A:** These compute true IPR locally (need to check eigenvector usage)  
**Possibility B:** These read pre-computed IPR from external data sources  
**Action required:** Code review of each script to determine IPR computation method

---

### 2.5 S¹ Calibration Scripts (True IPR Computation Found)

**File:** `scripts/run_s1_calibration_pilot_v0_1_17.py`  
**Lines:** 110-125  
**Code:**
```python
# Compute IPR for each eigenmode
for i in range(eigvecs.shape[1]):
    psi = eigvecs[:, i]
    ipr = np.sum(np.abs(psi)**4)  # ← TRUE IPR COMPUTATION
    iprs.append(ipr)

# For extended modes, IPR ≈ 1/N
expected_extended_ipr = 1.0 / N
mean_ipr = np.mean(iprs)

# Flag as localized if mean IPR significantly exceeds extended expectation
```
**Status:** ✅ CORRECT — computes Σ|ψᵢ|⁴ from eigenvectors  
**Note:** This is a calibration script, NOT used in Gate 3/4 execution

---

**File:** `scripts/run_s1_calibration_v0_1_18_improved.py`  
**Line:** 134 (similar structure to v0_1_17)  
**Status:** ✅ CORRECT — also computes true IPR

---

### 2.6 Dirac/Geometric Scripts (IPR Mentioned, Likely External)

**Files:**
- `scripts/dirac_chirality_diagnostic.py` (line 230-231)
- `scripts/dirac_localization_benchmark.py` (line 162)

**Context:** References "IPR/r-statistics reported" in benchmark descriptions  
**Status:** ⚠️ UNCLEAR — likely reads IPR from cc_toy_lab library output, not computed locally  
**Action required:** Check cc_toy_lab implementation

---

## 3. README.md IPR Tables (High Priority)

**Grep results show multiple tables in README.md with "IPR" columns:**

### 3.1 Table Format Examples

From earlier Gate experiments (exact line numbers not in grep output):

**Example table structure:**
```
| W | <r> | stderr_r | mean IPR | stderr_ipr |
```

**Questions:**
1. What is the source of "mean IPR" values in these tables?
2. Are they computed from `mean_low_ipr` field (eigenvalue proxy)?
3. Or were they computed from true IPR in earlier versions?

**Action required:**
- Read README.md tables
- Trace data source for each IPR column
- Flag tables with eigenvalue-based IPR for correction

### 3.2 Affected Sections (from grep)

**Line 138, 160, 197, 212, 258, 295, 311, 341, 368, 423, 483:**
- Multiple sections reference "IPR" in tables
- Sections cover: Gate 1, Gate 2, Gate 3, disorder calibration, family comparisons

**Status:** ⚠️ HIGH PRIORITY — if these tables used eigenvalue proxy, all prior Gate results are affected

---

## 4. S¹ Ring Diagnostic (Mixed Usage)

**File:** `scripts/s1_ring_localization_diagnostic.py`  
**Lines:** 391, 594, 596, 615, 617  
**Code snippets:**
```python
notes.append("ring clean low-energy states already have elevated IPR")
ax.set_title("Ring family IPR vs disorder")
ax.set_ylabel("mean gate IPR (alpha=0.0)")
ax.set_ylabel("mean disordered-clean gate IPR delta")
```

**Status:** ⚠️ UNCLEAR — references "gate IPR" which may be:
- Eigenvalue proxy from `mean_low_ipr` field
- OR locally computed true IPR
- Need code review to determine

---

## 5. cc_toy_lab Library (Not Audited)

**Grep scope:** scripts only, did NOT audit `cc_toy_lab/` directory

**Potential issues:**
- If `cc_toy_lab` library has IPR computation functions, they may also use eigenvalue proxy
- Anderson 3D benchmarks likely call cc_toy_lab functions
- Need separate audit of library code

**Files to check:**
- `cc_toy_lab/*/localization.py`
- `cc_toy_lab/*/metrics.py`
- Any function named `compute_ipr()`, `ipr_metric()`, etc.

---

## 6. Test Suite (No IPR Tests Found)

**Grep scope:** `tests/` directory

**Finding:** NO results for "IPR" or "mean_low_ipr" in test files

**Implication:**
- ❌ No unit tests verify IPR computation against known ground truth
- ❌ No test caught eigenvalue vs eigenvector mismatch
- ⚠️ Metric implementation was never validated

**Action required:**
- Add test: `test_ipr_fully_localized()` → IPR should be 1.0 for δ-function state
- Add test: `test_ipr_fully_delocalized()` → IPR should be 1/N for uniform state
- Add test: `test_mean_low_ipr_is_ipr()` → verify field contains true IPR, not eigenvalue

---

## 7. Summary by Script Category

| Category | Files Audited | True IPR | Eigenvalue Proxy | Unclear | Status |
|----------|--------------|----------|------------------|---------|--------|
| Gate 4 | 2 | 0 | 2 | 0 | ❌ Confirmed mismatch |
| Gate 3 | 2 | 0 | 2 | 0 | ❌ Likely mismatch |
| Disorder sweep | 1 | 0 | 1 | 0 | ❌ Likely mismatch |
| Anderson 3D | 4 | 0 | 0 | 4 | ⚠️ Needs review |
| S¹ calibration | 2 | 2 | 0 | 0 | ✅ Correct (not used in Gates) |
| S¹ ring diagnostic | 1 | 0 | 0 | 1 | ⚠️ Needs review |
| Dirac/geometric | 2 | 0 | 0 | 2 | ⚠️ Needs review |
| Tests | 0 | 0 | 0 | 0 | ❌ No IPR tests exist |
| **TOTAL** | **14** | **2** | **5** | **7** | **⚠️ 5 confirmed, 7 unclear** |

---

## 8. Risk Assessment by Claim Type

### 8.1 HIGH RISK (Likely Incorrect)

**Claims based on eigenvalue proxy labeled as "IPR":**

1. **Gate 3 IPR contrast** (if from `mean_low_ipr`)
   - Claim: "W=12 shows X.XX IPR contrast"
   - Risk: IPR ratio threshold may be based on eigenvalue difference
   - Action: Re-audit Gate 3 results, verify metric source

2. **Optimal disorder strength W=20** (from disorder sweep)
   - Claim: "W=20 chosen for maximum IPR contrast"
   - Risk: Optimization based on eigenvalue proxy, not true IPR
   - Action: Re-run disorder sweep with corrected IPR

3. **README.md IPR increase claims**
   - Claim: "IPR increases from weak to strong disorder"
   - Risk: Trend may be eigenvalue lowering, not IPR increase
   - Action: Verify each table's data source

### 8.2 MEDIUM RISK (Unclear)

**Claims where IPR source is unknown:**

1. **Anderson 3D localization benchmarks**
   - May use cc_toy_lab library functions
   - Need library code audit to determine IPR implementation

2. **S¹ ring elevated IPR notes**
   - Reference "elevated IPR" in ring family
   - May be qualitative observation vs quantitative threshold

### 8.3 LOW RISK (Likely Correct)

**Independent validation:**

1. **r-statistic results**
   - Computed from eigenvalue gaps only
   - Does NOT depend on eigenvectors
   - Unaffected by IPR mismatch

2. **S¹ calibration pilots**
   - Compute true IPR correctly
   - But NOT used in Gate experiments

---

## 9. Recommended Actions (Priority Order)

### 9.1 Immediate (Before Any IPR Claims Reused)

1. **✅ DONE:** Document Gate 4 mismatch (erratum filed)
2. **TODO:** Audit README.md tables — identify which use eigenvalue proxy
3. **TODO:** Flag affected README sections with warning banner
4. **TODO:** Add disclaimer to all prior IPR claims: "Under review — metric implementation audit in progress"

### 9.2 Short-Term (Next 1-2 Weeks)

1. **Implement corrected IPR** in run_gate4_batched.py
2. **Add unit tests** for IPR computation (localized/delocalized ground truth)
3. **Re-run Gate 4** with corrected metric (or analyze saved eigenvectors if available)
4. **Audit Gate 3 data** — verify if eigenvectors were saved, can recompute IPR

### 9.3 Medium-Term (Next Month)

1. **Audit cc_toy_lab library** — check all IPR functions
2. **Review Anderson 3D benchmarks** — verify IPR source
3. **Re-run disorder sweep** with corrected IPR (if W=20 choice depends on IPR)
4. **Update README.md** with corrected results or retraction notices

### 9.4 Long-Term (Prevention)

1. **Establish metric validation protocol:**
   - Every new metric must have unit test against known ground truth
   - Pre-registration must include reference implementation
   - CI must verify metric matches protocol definition

2. **Field naming standards:**
   - `mean_low_eigenvalue` (if tracking eigenvalues)
   - `mean_low_ipr_true` (if tracking true IPR)
   - Never use ambiguous names like `mean_low_ipr` for eigenvalue data

3. **Code review checklist:**
   - [ ] Metric formula in protocol matches implementation
   - [ ] Unit test exists
   - [ ] Field name accurately describes contents
   - [ ] No placeholder comments in production

---

## 10. Audit Status by File

| File | Line(s) | Status | Finding | Action Required |
|------|---------|--------|---------|-----------------|
| `run_gate4_batched.py` | 218-221 | ❌ CONFIRMED | Eigenvalue proxy | Erratum filed, reimplement |
| `run_gate4_dry_run.py` | 143 | ⚠️ PLACEHOLDER | Labeled placeholder | Remove for production |
| `run_gate3c_confirmatory.py` | 64-149 | ❌ LIKELY | Prints as "mean IPR" | Verify data source |
| `run_gate3_full.py` | 36 | ⚠️ UNCLEAR | "IPR contrast" aggregation | Trace aggregation |
| `run_disorder_sweep.py` | 71-105 | ❌ LIKELY | "Optimal W" from proxy | Re-run with true IPR |
| `anderson_3d_*.py` | Multiple | ⚠️ UNCLEAR | IPR references | Code review needed |
| `run_s1_calibration_*.py` | 110-134 | ✅ CORRECT | True Σ\|ψᵢ\|⁴ | No action (not used in Gates) |
| `s1_ring_localization_diagnostic.py` | 391-617 | ⚠️ UNCLEAR | "gate IPR" references | Code review needed |
| `dirac_*.py` | Multiple | ⚠️ UNCLEAR | IPR mentions | Check library source |
| `README.md` | 138+ | ⚠️ HIGH PRIORITY | Multiple IPR tables | Audit all tables |
| `tests/` | — | ❌ MISSING | No IPR tests | Add unit tests |

---

## 11. Audit Conclusion

**Overall assessment:**
- ❌ Widespread use of eigenvalue proxy labeled as "IPR" across Gate 3, 4, disorder sweeps
- ⚠️ At least 5 scripts confirmed using eigenvalue proxy, 7 unclear
- ❌ NO unit tests exist to catch metric implementation errors
- ⚠️ README.md contains multiple IPR tables requiring verification

**Recommended verdict for all prior IPR claims:**
- **SUSPEND** until corrected metric applied
- Do NOT cite prior IPR results without audit
- Flag all affected sections with "UNDER REVIEW" notice

**Timeline to resolution:**
- Gate 4 correction: 1-2 weeks (depends on re-execution vs saved eigenvector analysis)
- Full codebase audit: 1 month (includes cc_toy_lab library, all scripts, README tables)
- Corrected results publication: 6-8 weeks (after re-runs complete)

---

**Audit status:** INITIAL (incomplete)  
**Next update:** After README.md table audit complete  
**Responsible:** TBD (assign audit lead)  
**Related erratum:** `S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md`
