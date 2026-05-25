# S³ Dirac Branch Indexing Source Addendum — v0.1.24

**Date:** 2026-05-25  
**Status:** 🟢 **SOURCE_CONFIRMS_NEGATIVE_K0_VALID**  
**Purpose:** RED test results + source verification summary for code fix decision  
**Parent document:** `S3_DIRAC_SOURCE_VERIFICATION_v0.1.23.md`

---

## VERDICT: SOURCE_CONFIRMS_NEGATIVE_K0_VALID

**Primary source:** arXiv:1103.4097 v2, Section 6 "The spectrum of D", pages 14-15  
**Verification date:** 2026-05-25 (completed in v0.1.23 document)  
**Evidence level:** [VERIFIED-REAL] — PDF directly verified

---

## 1. Source Verification Summary

**From parent document `S3_DIRAC_SOURCE_VERIFICATION_v0.1.23.md` (lines 288-292):**

### Paper Formula (arXiv:1103.4097 Section 6)

| Branch | Formula | **k range** | First eigenvalues (R=1) |
|--------|---------|-------------|------------------------|
| **Negative** | λ₋ = −(k + 3/2) / R | **k ≥ 0** | **−3/2**, −5/2, −7/2 |
| **Positive** | λ₊ = +(k + 1/2) / R | **k ≥ 1** | +3/2, +5/2, +7/2 |

**Combined canonical spectrum:** ±3/2, ±5/2, ±7/2, ±9/2, ... (symmetric)

### Code Bug (dirac_s3.py line 67)

```python
k_values = list(range(1, int(j_max) + 2))  # Both branches start k=1
```

**Problem:** Negative branch **starts at k=1** instead of k=0 → **missing λ = −3/2**

**Expected:** Negative k=0 → λ = −(0 + 3/2) = **−3/2** ✓

---

## 2. RED Test Results (2026-05-25)

**Test file:** `tests/cc_toy_lab/spectral/test_dirac_s3_branches.py`  
**Tests run:** 6 total  
**Results:** 1 FAIL (expected), 5 PASS

### Critical RED Test (test_negative_3_2_presence)

```
FAILED tests/.../test_dirac_s3_branches.py::...::test_negative_3_2_presence

AssertionError: FAIL: -3/2 eigenvalue not found in spectrum.
Current low spectrum: [-4.5 -3.5 -2.5  1.5  2.5  3.5]
Expected: -3/2 present (for symmetric ±3/2, ±5/2, ±7/2 structure)
Likely cause: k starts from 1 instead of 0 for negative branch
```

**Evidence:** -3/2 missing from current code output ✓  
**Expected behavior:** Test should FAIL on k ≥ 1 code (RED phase) ✓  
**After fix:** Test should PASS when k ≥ 0 implemented (GREEN phase)

### Baseline Tests (all PASSED)

1. ✅ `test_current_spectrum_baseline` — documents current `-9/2, -7/2, -5/2, +3/2, +5/2, +7/2`
2. ✅ `test_positive_3_2_presence` — +3/2 exists (positive branch correct)
3. ✅ `test_radius_scaling` — eigenvalues ∝ 1/R verified
4. ✅ `test_low_spectrum_count` — 6 unique eigenvalues present
5. ✅ `test_hermiticity` — operator Hermitian, eigenvalues real

**TDD Status:** RED phase confirmed — fix can proceed to GREEN phase ✓

---

## 3. Source-Verified Fix Specification

### Required Code Change (cc_toy_lab/spectral/dirac_s3.py)

**Current (INCORRECT):**
```python
# Line 67: Both branches start at k=1
k_values = list(range(1, int(j_max) + 2))

# Lines 79-90: Same k_values used for both branches
for k in k_values:
    eigenvalue_pos = (k + 0.5) / radius   # k ≥ 1 ✓
    eigenvalue_neg = -(k + 1.5) / radius  # k ≥ 1 ✗ (should be k ≥ 0)
```

**Correct (source-verified):**
```python
# Negative branch: k ≥ 0 (includes k=0 giving λ = −3/2)
k_neg = list(range(0, int(j_max) + 2))

# Positive branch: k ≥ 1 (starts from k=1 giving λ = +3/2)
k_pos = list(range(1, int(j_max) + 2))

# Apply formulas with correct ranges:
# - Negative: λ₋ = -(k + 3/2) for k in k_neg
# - Positive: λ₊ = +(k + 1/2) for k in k_pos
```

### Expected Low Spectrum After Fix (R=1.0, j_max=2)

**Before fix:** `[-4.5, -3.5, -2.5, +1.5, +2.5, +3.5]` (6 unique, asymmetric)  
**After fix:** `[-3.5, -2.5, -1.5, +1.5, +2.5, +3.5]` (6 unique, symmetric ±3/2, ±5/2, ±7/2)

**Critical difference:** λ = −1.5 (−3/2) will appear after fix ✓

---

## 4. Source Verification Chain

```
arXiv:1103.4097 v2 (2011)
    ↓ [PDF verified 2026-05-25]
S3_DIRAC_SOURCE_VERIFICATION_v0.1.23.md
    ↓ [Branch k-ranges confirmed]
CODE_FIX_PLAN_v0.1.24_S3_BRANCH_INDEXING.md
    ↓ [Fix strategy documented]
test_dirac_s3_branches.py (RED tests)
    ↓ [Bug confirmed: -3/2 missing]
This addendum (v0.1.24)
    ↓ [Verdict: SOURCE_CONFIRMS_NEGATIVE_K0_VALID]
```

**Traceability:** Full chain from paper → diagnosis → test → verdict ✓

---

## 5. Decision Matrix

| Question | Answer | Evidence |
|----------|--------|----------|
| **Does paper allow k=0 for negative branch?** | ✅ **YES** | v0.1.23 lines 288-292 |
| **Is -3/2 part of canonical S³ Dirac spectrum?** | ✅ **YES** | v0.1.23 lines 353-354 |
| **Does current code include k=0?** | ❌ **NO** | Line 67: `range(1, ...)` |
| **Is -3/2 present in current code output?** | ❌ **NO** | RED test confirmed |
| **Should code be fixed?** | ✅ **YES** | Source + tests align |

**Verdict:** **SOURCE_CONFIRMS_NEGATIVE_K0_VALID**

---

## 6. Authorization to Proceed

**APPROVAL GATES:**
- ✅ **Source verified:** arXiv:1103.4097 PDF checked (v0.1.23)
- ✅ **Bug confirmed:** RED test shows -3/2 missing
- ✅ **Fix scope clear:** Add negative k=0 only, preserve positive k ≥ 1
- ✅ **Tests written:** GREEN phase ready (test will PASS after fix)

**NEXT STEP:** Proceed to **Этап 2: Code Fix** per `CODE_FIX_PLAN_v0.1.24_S3_BRANCH_INDEXING.md`

**CONSTRAINTS:**
- ❌ NO batch 3-6 execution until fix verified
- ❌ NO Gate 4B rerun decision until fix tested
- ❌ NO Negative Controls resume until spectrum validated
- ✅ ONLY code fix → unit test → diagnostic → then decide rerun

---

## 7. Impact Summary

**What changes:**
- Lowest negative eigenvalue: **−5/2 → −3/2**
- Low spectrum structure: **asymmetric → symmetric** (±3/2, ±5/2, ±7/2)
- Eigenvalue count at j_max=0: **8 unchanged** (degeneracy formula separate issue)

**What remains:**
- Positive branch: unchanged (already correct k ≥ 1)
- Dimension formula: unchanged (2(k+1)² per level)
- Higher eigenvalues: shifted by one k-level for negative branch

**Gate 4B impact:**
- Computational outputs v0.1.21-23: **PRESERVED** (historical record)
- Interpretation: **REMAINS FROZEN** until v0.1.24 fix verified
- Rerun decision: **DEFERRED** to post-fix diagnostic (Этап 3-4)

---

## 8. References

1. **arXiv:1103.4097 v2** — "Eigenspaces of the Spin Dirac operator over S³", J. Fabian Meier
   - Section 6 "The spectrum of D", pages 14-15
   - Eigenvalue formulas and branch structure

2. **S3_DIRAC_SOURCE_VERIFICATION_v0.1.23.md** — Primary source verification document
   - PDF verification completed 2026-05-25
   - Branch indexing analysis (lines 276-406)
   - Verdict: BRANCH_INDEXING_FIX_REQUIRED

3. **CODE_FIX_PLAN_v0.1.24_S3_BRANCH_INDEXING.md** — Implementation plan
   - TDD workflow: RED tests → fix → GREEN tests → diagnostic
   - Fix scope and constraints

4. **tests/cc_toy_lab/spectral/test_dirac_s3_branches.py** — Unit tests
   - RED phase: 1 FAIL (critical), 5 PASS (baseline)
   - GREEN target: all 6 PASS after fix

---

**VERDICT:** ✅ **SOURCE_CONFIRMS_NEGATIVE_K0_VALID**

**Authorization:** Proceed to code fix (Этап 2).

**Author:** Claude Sonnet 4.5  
**Date:** 2026-05-25  
**Session type:** READ-ONLY verification + test execution  
**No code changed, no commits made.**

---

**END OF ADDENDUM**
