# Gate 4B True IPR Implementation Check — v0.1.21

**Date:** 2026-05-22 11:00 Almaty  
**Purpose:** Verify metric-corrected implementation before Gate 4B rerun  
**Status:** IMPLEMENTATION COMPLETE (rerun NOT executed)

---

## 1. Summary

**Metric correction implemented and verified:**
- ✅ Unit tests created: `tests/test_ipr_metric.py` (17 tests, ALL GREEN)
- ✅ Code updated: `scripts/run_gate4_batched.py` (eigvalsh → eigh)
- ✅ Helper function confirmed: `cc_toy_lab.spectral.metrics.inverse_participation_ratio`
- ✅ Dry check passed: 216 cases, 9 batches, 0 duplicates
- ⏳ Runtime benchmark: NOT executed (next step)
- ❌ Full rerun: NOT executed (awaiting benchmark)

**Critical change:**
```python
# v0.1.20 (WRONG):
eigvals = np.linalg.eigvalsh(H)
mean_low_ipr = np.mean(eigvals[:int(0.1*N)])

# v0.1.21 (CORRECT):
eigvals, eigvecs = np.linalg.eigh(H)
iprs = inverse_participation_ratio(eigvecs[:, low_indices])
mean_low_ipr = np.mean(iprs)  # TRUE IPR = Σ|ψᵢ|⁴
```

---

## 2. Unit Tests (17 tests, 17 passed)

**File:** `tests/test_ipr_metric.py`

**Ground truth tests:**
1. ✅ `test_ipr_fully_localized_real` — δ-function: IPR = 1.0
2. ✅ `test_ipr_fully_localized_other_site` — localization at any site: IPR = 1.0
3. ✅ `test_ipr_fully_delocalized_real` — uniform state: IPR = 1/N
4. ✅ `test_ipr_fully_localized_complex` — complex δ-function: IPR = 1.0
5. ✅ `test_ipr_complex_superposition` — two-site superposition: IPR = 5/9
6. ✅ `test_ipr_random_normalized_real` — random vector: 1/N < IPR ≤ 1
7. ✅ `test_ipr_random_normalized_complex` — complex random: 1/N < IPR ≤ 1
8. ✅ `test_ipr_reproducible_with_seed` — deterministic for fixed seed
9. ✅ `test_ipr_matrix_input_multiple_eigenvectors` — 2D matrix (5 eigenvectors)
10. ✅ `test_ipr_zero_vector_fails_gracefully` — zero vector → nan/inf (no silent failure)
11. ✅ `test_ipr_unnormalized_vector` — normalization term in formula
12. ✅ `test_ipr_half_half_state` — (|0⟩+|1⟩)/√2: IPR = 0.5

**Edge cases:**
13. ✅ `test_ipr_large_hilbert_space` — N=4000 (larger than Gate 4 max N=3712)
14. ✅ `test_ipr_very_small_values` — numerical stability for small |ψ|²
15. ✅ `test_ipr_single_element_vector` — N=1: IPR = 1.0

**Gate 4 consistency:**
16. ✅ `test_ipr_bottom_10_percent_eigenvectors` — simulate Gate 4 workflow
17. ✅ `test_ipr_vs_eigenvalue_mean_not_equal` — verify mean(IPR) ≠ mean(eigenvalues)

**pytest output:**
```
============================= test session starts =============================
platform win32 -- Python 3.11.13, pytest-8.4.2
collected 17 items

tests/test_ipr_metric.py::TestIPRGroundTruth::... PASSED [ 5%]
...
tests/test_ipr_metric.py::TestIPRGate4Consistency::... PASSED [100%]

======================== 17 passed, 1 warning in 0.27s ======================
```

**Warning (expected):**
- `RuntimeWarning: invalid value encountered in scalar divide` in `test_ipr_zero_vector_fails_gracefully`
- This is intentional: test verifies graceful NaN handling for zero vector

---

## 3. Helper Function (Already Existed)

**File:** `cc_toy_lab/spectral/metrics.py`

**Function:** `inverse_participation_ratio(vector)`

**Signature:**
```python
def inverse_participation_ratio(vector: np.ndarray) -> float | np.ndarray:
    """IPR = sum |psi|^4 / (sum |psi|^2)^2.
    
    If a 2D matrix is passed, columns are treated as eigenvectors.
    """
```

**For normalized vectors:**
- sum |ψ|² = 1 → IPR = sum |ψ|⁴ / 1² = sum |ψ|⁴ ✓
- Matches protocol definition: IPR = Σ|ψᵢ|⁴

**Handles:**
- 1D vectors (single eigenstate)
- 2D matrices (multiple eigenvectors as columns)
- Complex vectors
- Unnormalized vectors (via denominator term)

**No new function needed:** existing implementation is correct.

---

## 4. Code Changes (scripts/run_gate4_batched.py)

### 4.1 Imports Added

**Line 37:**
```python
from cc_toy_lab.spectral.metrics import mean_adjacent_gap_ratio, inverse_participation_ratio
```

### 4.2 Metric Computation Replaced

**Lines 215-230 (OLD v0.1.20):**
```python
# Compute eigenvalues (required for both IPR and r-statistic)
eigvals = np.linalg.eigvalsh(H)

# IPR metric (from dry-run)
N = H.shape[0]
low_eigvals = eigvals[: int(0.1 * N)]  # Bottom 10%
mean_low_ipr = float(np.mean(low_eigvals))
```

**Lines 215-232 (NEW v0.1.21):**
```python
# Compute eigenvalues AND eigenvectors (v0.1.21: corrected from eigvalsh)
eigvals, eigvecs = np.linalg.eigh(H)

# True IPR metric (v0.1.21: eigenvector-based, corrected from eigenvalue mean)
N = H.shape[0]
n_low = int(0.1 * N)  # Bottom 10%
low_indices = np.argsort(eigvals)[:n_low]
low_eigvals = eigvals[low_indices]
low_eigvecs = eigvecs[:, low_indices]

# Compute true IPR = Σ|ψᵢ|⁴ for each low eigenstate
iprs = inverse_participation_ratio(low_eigvecs)  # Returns array
mean_low_ipr = float(np.mean(iprs))

# Diagnostic: eigenvalue mean (for v0.1.20 comparison)
mean_low_eigenvalue = float(np.mean(low_eigvals))
```

**Key changes:**
1. `eigvalsh(H)` → `eigh(H)` — now computes eigenvectors
2. Extract bottom 10% eigenvectors (`low_eigvecs`)
3. Compute true IPR via `inverse_participation_ratio()` for each eigenstate
4. Store `mean_low_eigenvalue` for v0.1.20 comparison

### 4.3 Error Handling Updated

**Lines 250-256:**
```python
except Exception as e:
    error = str(e)
    mean_low_ipr = None
    mean_low_eigenvalue = None  # NEW: initialize diagnostic field
    r_stat = None
    r_stat_available = False
    r_stat_reason = "case_execution_failed"
```

### 4.4 Output Schema Updated

**Lines 272-292:**
```python
result = {
    "case_id": case["id"],
    "family": case["family"],
    "disorder_strength": case["disorder_strength"],
    "s1_size": case["s1_size"],
    "j_max": case["j_max"],
    "seed": case["seed"],
    "runtime_sec": elapsed,
    # v0.1.21 canonical metric fields
    "true_ipr_mean": mean_low_ipr,  # Canonical: mean of true IPR = Σ|ψᵢ|⁴
    "uses_eigenvectors": True,  # Confirms eigenvector-based computation
    # Diagnostic fields
    "mean_low_eigenvalue": mean_low_eigenvalue,  # For v0.1.20 comparison
    # Deprecated compatibility alias (v0.1.20 field name)
    "mean_low_ipr": mean_low_ipr,  # DEPRECATED: use true_ipr_mean (v0.1.21+)
    # Metadata
    "ipr_metric_version": "v0.1.21_true_eigenvector_ipr",
    # r-statistic (unchanged)
    "r_stat": r_stat,
    "r_stat_available": r_stat_available,
    "r_stat_reason": r_stat_reason,
    "error": error,
}
```

**Canonical v0.1.21 fields:**
- `true_ipr_mean` — **CANONICAL** metric field (mean of Σ|ψᵢ|⁴ over bottom 10%)
- `uses_eigenvectors` — boolean flag confirming eigenvector-based computation

**Diagnostic fields:**
- `mean_low_eigenvalue` — eigenvalue mean (for v0.1.20 comparison)
- `ipr_metric_version` — explicit version marker for reproducibility

**Deprecated compatibility alias:**
- `mean_low_ipr` — **DEPRECATED** (kept for v0.1.20 backward compatibility)
  - v0.1.21+: use `true_ipr_mean` instead
  - Contains TRUE IPR (eigenvector-based), NOT eigenvalue mean
  - Will be removed in future versions

**Field naming convention:**
- **Canonical metric:** `true_ipr_mean`
- **Deprecated alias:** `mean_low_ipr` (backward compatibility only)

### 4.5 Version Constants Updated

**Lines 52-58 (OLD):**
```python
PROTOCOL_COMMIT = "1f4173c"
DRY_RUN_RESULTS_COMMIT = "52d221f"
BATCH_PROTOCOL_VERSION = "v0.1.20"

OUTPUT_BASE = Path("reports/RUNS/gate4_fss_v0.1.20")
```

**Lines 52-58 (NEW):**
```python
PROTOCOL_COMMIT = "1f4173c"  # Original v0.1.20 protocol
DRY_RUN_RESULTS_COMMIT = "52d221f"
BATCH_PROTOCOL_VERSION = "v0.1.21"  # Metric-corrected: true IPR

# Output directory (v0.1.21: metric-corrected rerun)
OUTPUT_BASE = Path("reports/RUNS/gate4_fss_v0.1.21")
```

**Changed:**
- `BATCH_PROTOCOL_VERSION` → `"v0.1.21"`
- `OUTPUT_BASE` → `gate4_fss_v0.1.21/` (separate from v0.1.20 results)

### 4.6 Docstring Updated

**Lines 1-32:**
- Added version header: `v0.1.21 (Metric-Corrected)`
- Added critical change summary
- Updated date: `2026-05-22`
- Added related documents references
- Clarified pre-requisites: unit tests + benchmark required

---

## 5. Dry Check Verification

**Command:**
```bash
python scripts/run_gate4_batched.py --print-plan
```

**Output:**
```
================================================================================
Gate 4 Full Grid Plan — S³×S¹ Finite-Size Scaling
================================================================================

Total cases: 216
Total batches: 9
Cases per batch: 24 (expected)

Grid parameters (locked, commit 1f4173c):
  Families: ['spectral_circle', 'ring', 'wilson_ring']
  Disorder W: [0, 12, 20]
  S¹ sizes: [16, 32, 64, 128]
  j_max: [2, 3]
  Seeds: [123, 456, 789]

Breakdown:
  3 families × 3 W × 4 sizes × 2 j_max × 3 seeds = 216 cases

--------------------------------------------------------------------------------
Batch assignments:
--------------------------------------------------------------------------------
Batch  1: spectral_circle      W= 0 → 24 cases
Batch  2: spectral_circle      W=12 → 24 cases
Batch  3: spectral_circle      W=20 → 24 cases
Batch  4: ring                 W= 0 → 24 cases
Batch  5: ring                 W=12 → 24 cases
Batch  6: ring                 W=20 → 24 cases
Batch  7: wilson_ring          W= 0 → 24 cases
Batch  8: wilson_ring          W=12 → 24 cases
Batch  9: wilson_ring          W=20 → 24 cases

--------------------------------------------------------------------------------
Coverage verification:
--------------------------------------------------------------------------------
Total assigned cases: 216
Unique cases: 216
Duplicates: 0
Missing cases: 0

✅ Coverage check PASSED: all 216 cases covered exactly once
```

**Verification:**
- ✅ Grid unchanged: 3 families × 3 W × 4 sizes × 2 j_max × 3 seeds = 216
- ✅ Batch structure preserved: 9 batches × 24 cases
- ✅ No duplicates
- ✅ No missing cases
- ✅ No execution triggered (--print-plan is read-only)

---

## 6. What Was NOT Changed

**Grid parameters (LOCKED):**
- ❌ Families: still `[spectral_circle, ring, wilson_ring]`
- ❌ Disorder W: still `[0, 12, 20]`
- ❌ Sizes: still `[16, 32, 64, 128]`
- ❌ j_max: still `[2, 3]`
- ❌ Seeds: still `[123, 456, 789]`

**Decision rules (LOCKED):**
- ❌ PASS threshold: still ≥2.0× IPR contrast
- ❌ Family consistency: still ≥2/3 families
- ❌ Verdict conditions: unchanged

**Claim language (LOCKED):**
- ❌ Forbidden claims: still forbidden
- ❌ Allowed claims: unchanged

**v0.1.21 is a METRIC CORRECTION, not a new experiment.**

---

## 7. Remaining Blockers Before Rerun

### 7.1 Runtime Benchmark (REQUIRED NEXT)

**Not executed:** Single-case benchmark to estimate 216-case runtime

**Protocol requirement (Section 7.4):**

⚠️ **Benchmark implementation NOT YET AVAILABLE**

CLI currently supports:
- `--print-plan` — grid verification (dry check)
- `--batch-id N` — run specific batch (1-9)
- `--run-all` — run all batches (full 216-case grid)
- `--resume` — skip completed batches
- `--force` — overwrite existing results

**Benchmark approach (manual for now):**
1. Run single batch (24 cases) with `--batch-id 1`
2. Measure elapsed time from batch output
3. Extrapolate: `total_time = (elapsed_time / 24) × 216`

**Theoretical overhead estimate:** ~10× (eigenvector computation adds O(N³) vs O(N²))

**Unmeasured estimate:** ~16 hours (10× × 96.1 min v0.1.20 runtime)  
**Status:** Estimate NOT confirmed by measurement

**Decision rule (after real benchmark):**
- If <24h → proceed with full grid
- If 24-48h → batch over 2 days
- If >48h → reduce grid (drop s1_size=128)

**Current status:** ⏳ BENCHMARK NOT EXECUTED (implementation pending OR manual batch timing)

### 7.2 Full Grid Rerun (AFTER BENCHMARK)

**Command:**
```bash
python scripts/run_gate4_batched.py --run-all
```

**Status:** ❌ NOT EXECUTED

**Reason:** Protocol requires benchmark first

**Output location:** `reports/RUNS/gate4_fss_v0.1.21/`

---

## 8. Pre-Execution Checklist (v0.1.21 Protocol Section 11)

**Before executing ANY batches:**

- [x] **Unit tests pass:** `pytest tests/test_ipr_metric.py -v` → 17/17 green
- [x] **Code review:** run_gate4_batched.py lines 215-232 implement true IPR formula
- [ ] **Benchmark complete:** Single-case overhead measured and documented
- [ ] **Runtime estimate:** Extrapolated total time < 48 hours OR grid reduction plan approved
- [x] **Protocol committed:** v0.1.21 protocol committed (commit 5e5ffc9)
- [x] **No execution started:** Verified `RUNS/gate4_fss_v0.1.21/` does not exist yet

**Status:** 4/6 complete — **BENCHMARK REQUIRED** before proceeding

---

## 9. File Manifest

**Created:**
- `tests/test_ipr_metric.py` — 17 unit tests (17 passed)
- `reports/GATE4_TRUE_IPR_IMPLEMENTATION_CHECK_v0.1.21.md` — this file

**Modified:**
- `scripts/run_gate4_batched.py` — metric-corrected implementation

**Unchanged (used existing):**
- `cc_toy_lab/spectral/metrics.py` — `inverse_participation_ratio()` already correct

**Not created (optional):**
- Eigenvector storage `.npz` files — disabled by default (storage prohibitive)

---

## 10. Comparison with v0.1.20

| Aspect | v0.1.20 | v0.1.21 |
|--------|---------|---------|
| **Eigenvalue computation** | `eigvalsh(H)` | `eigh(H)` |
| **Eigenvector computation** | ❌ None | ✅ All eigenvectors |
| **IPR definition** | ❌ mean(eigenvalues) | ✅ mean(Σ\|ψᵢ\|⁴) |
| **Primary metric** | ❌ Eigenvalue proxy | ✅ True IPR |
| **Grid** | 216 cases | 216 cases (UNCHANGED) |
| **Thresholds** | ≥2.0× contrast | ≥2.0× contrast (UNCHANGED) |
| **Runtime** | 96.1 min | Unmeasured (benchmark pending, ~10× overhead expected) |
| **Storage** | 5 MB (JSON scalars) | ~5 MB (JSON scalars, no eigenvectors saved) |
| **Unit tests** | ❌ None | ✅ 17 ground truth tests |
| **Verdict** | WEAK_OR_INCONCLUSIVE | TBD (after rerun) |

**Key difference:** v0.1.21 measures LOCALIZATION (wavefunction spread), v0.1.20 measured ENERGY (eigenvalue mean)

---

## 11. Next Steps

### Immediate (DO NOT PROCEED WITHOUT):
1. **Execute runtime benchmark** (single case)
   - Measure overhead: time_v0.1.21 / time_v0.1.20
   - Extrapolate to 216 cases
   - Decide: full grid / batch over 2 days / reduce grid

2. **Commit implementation changes**
   ```bash
   git add tests/test_ipr_metric.py
   git add scripts/run_gate4_batched.py
   git add reports/GATE4_TRUE_IPR_IMPLEMENTATION_CHECK_v0.1.21.md
   git commit -m "fix(gate-4): implement true eigenvector-based IPR metric"
   ```

### After Benchmark:
3. **Execute full rerun** (if benchmark <48h)
   ```bash
   python scripts/run_gate4_batched.py --run-all
   ```

4. **Scientific analysis** (after 216 cases complete)
   - Aggregate metrics
   - Apply decision rules
   - Compare with v0.1.20
   - Generate figures
   - Create results report

5. **Verdict determination**
   - Check: aggregate contrast ≥2.0×?
   - Check: family consistency ≥2/3?
   - Check: finite-size trend stable?
   - Check: r-statistic supports?
   - Issue verdict: PASS / WEAK / FAIL / INCOMPLETE

---

## 12. Success Criteria Summary

**Implementation complete if:**
- ✅ Unit tests pass (17/17)
- ✅ Dry check passes (216 cases, 0 duplicates)
- ✅ Code uses `eigh` not `eigvalsh`
- ✅ True IPR computed via `inverse_participation_ratio()`
- ✅ Output schema includes `mean_low_eigenvalue` for comparison
- ✅ Version marker `v0.1.21_true_eigenvector_ipr` in results

**All criteria met.** Implementation ready for benchmark → rerun.

---

**Implementation check status:** ✅ COMPLETE  
**Runtime benchmark status:** ⏳ NOT EXECUTED (next step)  
**Full rerun status:** ❌ NOT EXECUTED (awaiting benchmark)  
**Date:** 2026-05-22  
**Version:** v0.1.21 (Metric-Corrected)

---

**Related documents:**
- reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md (protocol)
- reports/S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md (erratum)
- reports/GATE4_TRUE_IPR_RECOVERY_CHECK_v0.1.20.md (recovery analysis)
- reports/IPR_IMPLEMENTATION_AUDIT_v0.1.20.md (codebase audit)
