# Gate 4 True IPR Recovery Check

**Date:** 2026-05-22  
**Purpose:** Determine if true eigenvector-based IPR can be recomputed from existing Gate 4 artifacts  
**Status:** RECOVERY CHECK COMPLETE

---

## Question

Can true eigenvector-based IPR be recomputed from existing Gate 4 artifacts without full rerun?

**Context:**
- Gate 4 execution completed: 216/216 cases, 0 failures
- Metric mismatch discovered: `mean_low_ipr` was eigenvalue-derived, not true IPR
- True IPR requires eigenvectors: IPR = Σ|ψᵢ|⁴

---

## Starting State

### Gate 4 Execution Status
- **Completed:** 216/216 cases (9 batches × 24 cases)
- **Failures:** 0/216 (0%)
- **r-statistic availability:** 216/216 (100%)
- **Execution duration:** 96.1 minutes
- **Execution period:** 2026-05-21 to 2026-05-22

### Current Git Status
```
Working directory: CLEAN (no uncommitted changes)

Recent commits:
0187e4f docs(gate-4): document IPR metric implementation mismatch
66a0f4e results(gate-4): analyze S3xS1 finite-size scaling grid
80dc509 docs(gate-4): document batch scheduling deviation
```

### Relevant Commits
- **a359097:** Gate 4 batched infrastructure
- **52d221f:** Gate 4 dry-run (placeholder metric)
- **66a0f4e:** Gate 4 execution + analysis (216 cases)
- **0187e4f:** Metric mismatch erratum

---

## Artifact Directories Checked

**Main directory:**
```
reports/RUNS/gate4_fss_v0.1.20/
```

**Subdirectories:**
```
reports/RUNS/gate4_fss_v0.1.20/batches/        (9 batch directories)
reports/RUNS/gate4_fss_v0.1.20/batches/batch_01/ ... batch_09/
reports/RUNS/gate4_fss_v0.1.20/merged/         (aggregated summaries)
reports/RUNS/gate4_fss_v0.1.20/figures/        (3 PNG figures)
```

**Total files checked:** 60 files

---

## File Types Found

### JSON Files (60 total)

**Per batch (9 batches × 5 files = 45 files):**
- `batch_config.json` — batch parameters (family, W, n_cases)
- `results.json` — 24 case results per batch
- `status.json` — batch completion status
- `timing.json` — per-case timing breakdown
- `summary.md` — human-readable batch summary

**Merged summaries (8 files):**
- `metrics.json` — all 216 cases aggregated
- `coverage.json` — grid verification
- `timing_summary.json` — runtime statistics
- `failure_summary.json` — failure tracking (0 failures)
- `family_summary.json` — by family aggregations
- `size_scaling_summary.json` — by s1_size aggregations
- `r_stat_summary.json` — r-statistic distributions
- `ipr_contrast_summary.json` — eigenvalue contrast (NOT true IPR)

**Other:**
- `config.json` — run configuration
- `figures/*.png` — 3 visualization plots

### Binary/Vector Files (NPZ, HDF5, Pickle)

**Result:** ❌ NONE FOUND

**Searched for:**
- `*.npz` (NumPy compressed arrays)
- `*.pkl` / `*.pickle` (Python pickle format)
- `*.h5` / `*.hdf5` (HDF5 format)
- `*.parquet` (Parquet columnar format)
- `*.csv` (CSV — checked, none found)

**Conclusion:** No binary vector storage used. Only JSON scalar outputs saved.

---

## NPZ Keys Found

**Status:** N/A — no NPZ files exist

---

## JSON/CSV Fields Found

### results.json Structure (per case)

**File checked:** `reports/RUNS/gate4_fss_v0.1.20/batches/batch_01/results.json`

**Fields per case (12 total):**
```json
{
  "case_id": int,
  "family": str,
  "disorder_strength": int,
  "s1_size": int,
  "j_max": int,
  "seed": int,
  "runtime_sec": float,
  "mean_low_ipr": float,          ← eigenvalue-based (NOT true IPR)
  "r_stat": float,                ← valid (from eigenvalue gaps)
  "r_stat_available": bool,
  "r_stat_reason": null | str,
  "error": null | str
}
```

**Fields NOT present:**
- ❌ `eigenvectors`
- ❌ `eigvecs`
- ❌ `vectors`
- ❌ `psi`
- ❌ `true_ipr`
- ❌ `ipr` (distinct from `mean_low_ipr`)
- ❌ `eigenvalues` (only mean computed, not full spectrum)

**Conclusion:** Only scalar summaries saved. No vector data.

---

## Eigenvector Availability

### Code Path Analysis

**File:** `scripts/run_gate4_batched.py`  
**Critical line:** 216

**Implementation:**
```python
eigvals = np.linalg.eigvalsh(H)
```

**Function used:** `numpy.linalg.eigvalsh`
- Returns: eigenvalues ONLY
- Does NOT return: eigenvectors

**Contrast with correct implementation:**
```python
# What was used (incorrect):
eigvals = np.linalg.eigvalsh(H)  # eigenvalues only

# What should have been used (correct):
eigvals, eigvecs = np.linalg.eigh(H)  # eigenvalues + eigenvectors
```

**Dry-run also used `eigvalsh`:**
- File: `scripts/run_gate4_dry_run.py`, line 138
- Same issue: `eigvals = np.linalg.eigvalsh(H)`
- Comment on line 143: `# Placeholder metric`

### Runtime Eigenvector Status

**Verdict:** ❌ EIGENVECTORS WERE **NEVER COMPUTED** IN RUNTIME

**Evidence:**
1. `eigvalsh` computes eigenvalues only, no eigenvector computation occurs
2. No assignment of form `eigvals, eigvecs = ...` in code
3. No eigenvector variable referenced anywhere in Gate 4 scripts
4. No eigenvector storage code present

**Implication:**
- Eigenvectors do NOT exist in memory during execution
- Eigenvectors were NOT discarded after computation
- Eigenvectors were NEVER created in the first place

### Comparison with Other Scripts

**Scripts that CORRECTLY compute eigenvectors:**

1. **anderson_3d_boundary_comparison.py (line 109):**
   ```python
   eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian.toarray())
   selected_vectors = eigenvectors[:, indices]
   ```

2. **run_s1_calibration_pilot_v0_1_17.py (lines 108-113):**
   ```python
   eigenvalues, eigenvectors = np.linalg.eigh(operator)
   for i in range(eigenvectors.shape[1]):
       psi = eigenvectors[:, i]
       ipr = np.sum(np.abs(psi)**4)  # ← TRUE IPR computation
   ```

3. **run_practical_applicability_v0_1_18.py (lines 47-51):**
   ```python
   def mean_ipr(eigenvectors: np.ndarray, count: int = 4) -> float:
       for idx in range(use):
           prob = np.abs(eigenvectors[:, idx]) ** 2
           ipr_values.append(1.0 / np.sum(prob**2))
   ```

**Gate 4 did NOT use these patterns.**

---

## Code Path Audit

### Full Gate 4 Execution Flow

**File:** `scripts/run_gate4_batched.py`

**Lines 215-221 (critical section):**
```python
215:        # Compute eigenvalues (required for both IPR and r-statistic)
216:        eigvals = np.linalg.eigvalsh(H)
217:
218:        # IPR metric (from dry-run)
219:        N = H.shape[0]
220:        low_eigvals = eigvals[: int(0.1 * N)]  # Bottom 10%
221:        mean_low_ipr = float(np.mean(low_eigvals))
```

**Comment on line 218:**  
`# IPR metric (from dry-run)`

**Analysis:**
- Comment suggests "IPR metric" but implementation is eigenvalue mean
- Likely inherited from dry-run placeholder without correction
- `eigvalsh` choice optimizes performance (faster than `eigh`)
- BUT optimization invalidated the metric

**Lines 224-226 (r-statistic computation):**
```python
224:        # Use spectral window for localization analysis (bottom 10% same as IPR)
225:        try:
226:            r_stat = mean_adjacent_gap_ratio(low_eigvals)
```

**Analysis:**
- r-statistic correctly computed from eigenvalue gaps
- Does NOT require eigenvectors
- This metric remains valid

### Why `eigvalsh` Was Used

**Performance consideration:**
- `eigvalsh`: O(N²) time, returns eigenvalues only
- `eigh`: O(N³) time, returns eigenvalues + eigenvectors
- For N=3712 (largest case: s1_size=128, j_max=3), eigenvector computation adds ~10× overhead

**Cost estimate:**
- Current runtime: 96.1 minutes (216 cases)
- With eigenvectors: ~960 minutes (16 hours) for 216 cases
- Additional storage: ~216 × 3712² × 8 bytes ≈ 23 GB uncompressed

**Trade-off:**
- Optimization saved 14+ hours of compute time
- BUT invalidated primary metric (IPR)
- r-statistic (secondary metric) was sufficient for performance optimization
- IPR should NOT have been optimized away

---

## Recovery Verdict

**FULL_RERUN_REQUIRED**

### Rationale

1. **Eigenvectors were never computed:**
   - `eigvalsh` used instead of `eigh`
   - No eigenvector data exists in runtime or storage

2. **No saved artifacts contain vector data:**
   - All outputs are JSON scalars
   - No NPZ, HDF5, or pickle files with vectors

3. **True IPR cannot be approximated from eigenvalues:**
   - IPR = Σ|ψᵢ|⁴ requires wavefunction |ψᵢ|
   - Eigenvalue mean does not encode spatial localization
   - No mathematical relationship: eigenvalue → IPR

4. **Recomputation requires Hamiltonians:**
   - Hamiltonians not saved (only eigenvalue summaries)
   - Must regenerate H for all 216 cases
   - Must solve `eigh(H)` to get eigenvectors
   - Equivalent to full rerun

### Cannot Use Partial Recompute

**Why partial recompute is impossible:**

❌ **"Recompute IPR from saved eigenvalues"**
- Eigenvalues do NOT contain spatial wavefunction information
- IPR measures spatial concentration, not energy

❌ **"Recompute a subset of cases"**
- Pre-registered protocol requires ALL 216 cases
- Family consistency criterion needs full grid
- Cannot cherry-pick favorable cases

❌ **"Approximate IPR from eigenvalue statistics"**
- No validated approximation formula exists
- Would introduce additional uncertainty
- Would NOT satisfy pre-registered IPR definition

---

## Impact on Gate 4

### What Remains Valid

✅ **Execution completeness:**
- 216/216 cases completed
- 0 failures
- Full parameter grid coverage
- Batched infrastructure operates correctly

✅ **r-statistic results:**
- Computed from eigenvalue gaps (no eigenvectors needed)
- W=0: r=0.605 → W=20: r=0.437 (shift toward Poisson)
- Supports weak localization interpretation
- Independent of IPR mismatch

✅ **Eigenvalue trend:**
- W=0: mean=-27.60 → W=20: mean=-94.23 (lowering)
- Finite-size strengthening (s1_size 16→128)
- Consistent with bound-state formation
- BUT: eigenvalue lowering ≠ IPR localization

✅ **Verdict (WEAK_OR_INCONCLUSIVE):**
- Based on r-statistic evidence only
- Correctly acknowledges IPR metric invalidity
- No overclaims made

✅ **No-overclaim discipline:**
- No "S³×S¹ validated" claim
- No "FL generalized" claim
- No "Gate 4 PASSED" claim
- All caveats disclosed

### What Remains Blocked

❌ **Primary verdict criterion:**
- IPR contrast ≥2.0× threshold unmeasurable
- Cannot assess family consistency (≥2/3 pass)
- Cannot issue GATE4_FSS_PASS_WITH_CAVEATS

❌ **S³×S¹ validation claim:**
- Primary metric invalid → validation incomplete
- Only weak evidence from secondary metric
- Forbidden until IPR corrected

❌ **IPR-based comparisons:**
- Cannot compare to Gate 3 IPR results (if also eigenvalue-based)
- Cannot compare to literature IPR values
- Cannot cite "IPR increases with disorder" (if from same metric)

---

## Recommended Next Step

### Option A: Full Rerun with Corrected Metric (Recommended)

**Implementation changes required:**

**File:** `scripts/run_gate4_batched.py`

**Line 216 (change from):**
```python
eigvals = np.linalg.eigvalsh(H)
```

**Line 216 (change to):**
```python
eigvals, eigvecs = np.linalg.eigh(H)
```

**Lines 220-221 (change from):**
```python
low_eigvals = eigvals[: int(0.1 * N)]
mean_low_ipr = float(np.mean(low_eigvals))
```

**Lines 220-225 (change to):**
```python
low_indices = np.argsort(eigvals)[: int(0.1 * N)]  # Bottom 10% indices
low_eigvecs = eigvecs[:, low_indices]

# Compute true IPR for each low eigenstate
iprs = []
for i in range(low_eigvecs.shape[1]):
    psi = low_eigvecs[:, i]
    ipr = np.sum(np.abs(psi)**4)
    iprs.append(ipr)

mean_low_ipr = float(np.mean(iprs))  # Now TRUE mean IPR
```

**Additional changes:**
1. Add unit test: `tests/test_ipr_metric.py`
   - Test localized state (IPR=1.0)
   - Test delocalized state (IPR=1/N)

2. Update field name (optional but recommended):
   - Keep `mean_low_ipr` for backward compatibility
   - Document: "v0.1.21+: true IPR; v0.1.20: eigenvalue mean"

3. Create new protocol version:
   - `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md`
   - Document: metric corrected, grid unchanged

**Estimated runtime:**
- Current (eigenvalues only): 96.1 minutes
- With eigenvectors: ~16 hours (10× overhead estimate)
- Storage: ~23 GB uncompressed (optional: save eigenvectors for future use)

**Estimated effort:**
- Code changes: 1 hour
- Unit tests: 2 hours
- Rerun execution: 16 hours (overnight)
- Analysis: 4 hours (reuse existing analysis pipeline)
- **Total:** ~1-2 days

### Option B: Targeted Rerun (Faster Validation)

**Subset grid:**
- 1 family (e.g., wilson_ring) × 3 W × 4 sizes × 2 j_max × 3 seeds = 72 cases
- Estimated runtime: ~5 hours
- Purpose: Verify IPR ≠ eigenvalue empirically before full rerun

**Use case:**
- Quick sanity check
- Compare eigenvalue-based vs eigenvector-based IPR
- Decide if full rerun investment is justified

### Option C: Archive and Move to Gate 5 (Not Recommended)

**Action:**
- Accept Gate 4 v0.1.20 as WEAK_OR_INCONCLUSIVE (permanent)
- Implement corrected metric in Gate 5 (larger sizes, new geometry)
- Use Gate 4 r-statistic as weak prior evidence

**Rationale:**
- Avoid rerun cost
- Move forward with corrected protocol

**Downside:**
- ❌ Gate 4 IPR question remains unanswered
- ❌ W=20 choice based on eigenvalue proxy (disorder sweep audit needed)
- ❌ Prior claims in README require audit regardless

**Verdict:** NOT RECOMMENDED — better to correct Gate 4 than skip

---

## Summary

**Can true IPR be recomputed from existing artifacts?**  
**Answer:** ❌ NO — eigenvectors were never computed in runtime

**Why not?**
- Gate 4 used `np.linalg.eigvalsh` (eigenvalues only)
- No eigenvector data exists in storage (only JSON scalars)
- Hamiltonians not saved → must regenerate + re-solve

**What is required?**
- Full rerun with `np.linalg.eigh` (eigenvalues + eigenvectors)
- Add true IPR computation: IPR = Σ|ψᵢ|⁴
- Estimated rerun time: ~16 hours

**What remains valid from v0.1.20?**
- ✅ Execution robustness (216/216 complete)
- ✅ r-statistic results (weak localization evidence)
- ✅ Eigenvalue trend (consistent with bound states)
- ❌ IPR contrast (unmeasurable)

**Recommended action:**
- Option A: Full rerun with corrected metric (1-2 days effort)

---

**Check status:** COMPLETE  
**Recovery verdict:** FULL_RERUN_REQUIRED  
**Estimated correction time:** 1-2 days (code + rerun + analysis)  
**Related documents:**
- `S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md`
- `IPR_IMPLEMENTATION_AUDIT_v0.1.20.md`
- `S3_S1_GATE4_FSS_RESULTS_v0.1.20.md`
