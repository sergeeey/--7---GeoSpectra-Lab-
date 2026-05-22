# S³×S¹ Gate 4 — Metric Implementation Mismatch Erratum

**Version:** v0.1.20  
**Date:** 2026-05-22  
**Type:** Post-Execution Protocol Deviation Notice  
**Status:** BLOCKING — requires corrective action before PASS verdict

---

## 1. Summary

**Gate 4 execution status:**
- ✅ Execution completed: 216/216 cases, 0 failures
- ✅ Full grid coverage: 3 families × 3 W × 4 sizes × 2 j_max × 3 seeds
- ✅ r-statistic availability: 216/216 (100%)

**Scientific verdict:**
- **GATE4_FSS_WEAK_OR_INCONCLUSIVE**

**Primary reason for verdict downgrade:**
- ❌ Implemented metric was mean eigenvalue, NOT true IPR
- ❌ Pre-registered threshold (≥2.0× IPR contrast) is unmeasurable
- ❌ Primary verdict-driving criterion cannot be assessed

**Impact:**
- Gate 4 PASS verdict is **BLOCKED**
- Secondary metric (r-statistic) provides weak evidence for localization
- Eigenvalue trend can be reported, but NOT as IPR localization signal
- Prior results using `mean_low_ipr` field require audit

---

## 2. Exact Mismatch

### 2.1 Pre-Registered Metric (Protocol)

**Document:** `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md`  
**Commit:** 1f4173c (locked before execution)

**Definition:**
```
IPR (Inverse Participation Ratio) = Σᵢ |ψᵢ|⁴

where:
- ψ = eigenvector (eigenstate wavefunction)
- i = spatial site index
- Sum over all sites in Hilbert space

Physical interpretation:
- Large IPR (→1) = localized (wavefunction concentrated on few sites)
- Small IPR (→1/N) = delocalized (wavefunction spread over many sites)

Gate 4 metric:
IPR contrast = IPR(W=20) / IPR(W=0)
Threshold: ≥2.0× for PASS_WITH_CAVEATS
```

### 2.2 Implemented Field (Code)

**File:** `scripts/run_gate4_batched.py`  
**Lines:** 215-221

**Implementation:**
```python
# Compute eigenvalues (required for both IPR and r-statistic)
eigvals = np.linalg.eigvalsh(H)

# IPR metric (from dry-run)
N = H.shape[0]
low_eigvals = eigvals[: int(0.1 * N)]  # Bottom 10%
mean_low_ipr = float(np.mean(low_eigvals))
```

**What was actually computed:**
- `np.linalg.eigvalsh(H)` returns eigenvalues ONLY (no eigenvectors)
- `mean_low_ipr = mean(low_eigvals)` = mean of bottom 10% eigenvalues
- This is **NOT** IPR = Σ|ψᵢ|⁴

### 2.3 Why the Mismatch Occurred

**Comment on line 218:**
```python
# IPR metric (from dry-run)
```

**Likely cause:** 
- Dry-run phase (commit 52d221f) used placeholder metric
- Comment label "IPR metric" carried over without implementation correction
- `eigvalsh` (eigenvalues only) used instead of `eigh` (eigenvalues + eigenvectors)
- Mean eigenvalue substituted for true IPR computation

**Result:**
- Field name `mean_low_ipr` suggests IPR, but contains eigenvalue mean
- Pre-registered IPR contrast threshold cannot be evaluated
- All 216 cases contain eigenvalue data, not IPR data

---

## 3. Scope of Impact

### 3.1 Gate 4 Verdict Impact

**BLOCKED:**
- ❌ Cannot assess primary criterion: IPR contrast ≥2.0×
- ❌ Cannot assess family consistency: ≥2/3 families pass 2.0× threshold
- ❌ Cannot issue GATE4_FSS_PASS_WITH_CAVEATS verdict

**DOWNGRADED TO:**
- ⚠️ GATE4_FSS_WEAK_OR_INCONCLUSIVE (based on r-statistic only)

**Why r-statistic alone is insufficient:**
- r-statistic is secondary diagnostic, not primary verdict driver (per preregistration)
- r-statistic shows shift toward Poisson, but magnitude is modest (W=20: 0.437 vs Poisson 0.39)
- Strong family dependence (spectral_circle does NOT shift)
- Pre-registered protocol requires BOTH IPR contrast AND r-statistic confirmation

### 3.2 Eigenvalue Data Interpretation

**What eigenvalue trend shows:**
- W=0 → W=20: eigenvalues become more negative (-27.60 → -94.23)
- Finite-size trend: eigenvalue suppression strengthens with size
- Physically: lower energies at W=20 may suggest bound states

**What eigenvalue trend CANNOT show:**
- IPR localization (requires wavefunction spatial concentration)
- Participation ratio (requires |ψᵢ|⁴ computation)
- Pre-registered 2.0× contrast threshold (defined for IPR ratio, not eigenvalue difference)

**Conclusion:**
- Eigenvalue trend is consistent with localization expectation
- BUT cannot substitute for IPR measurement
- Cannot claim "IPR contrast ≥2.0×" from eigenvalue data

### 3.3 Prior Results Requiring Audit

**Gate 3 and disorder sweep results:**
- README.md contains tables labeled "mean IPR" from earlier experiments
- If earlier runs also used `mean_low_ipr` field, those may be eigenvalues, not IPR
- All prior claims of "IPR increases with disorder" require verification

**Files to audit:**
- `scripts/run_disorder_sweep.py` (uses `mean_low_ipr`)
- `scripts/run_gate3c_confirmatory.py` (uses `mean_low_ipr`)
- README.md tables citing "IPR" values
- Any publications or reports referencing IPR from this codebase

**Action required:**
- Trace `mean_low_ipr` field origin across all experiments
- Determine if ANY experiment computed true IPR or all used eigenvalue proxy
- Correct or retract prior IPR claims if based on eigenvalue data

---

## 4. What Remains Valid

### 4.1 Execution Robustness

✅ **Valid claims:**
- 216/216 cases completed successfully
- 0 execution failures (0%)
- Full parameter grid coverage (no missing combinations)
- Batched execution infrastructure operates correctly
- 99.1% data quality (2 numerical outliers excluded for analysis)

✅ **Technical achievements:**
- Pre-registered protocol followed for execution (grid, batching, no post-hoc changes)
- Reproducible workflow (commit-locked protocol, documented deviations)
- Complete audit trail (batch configs, timings, status tracking)

### 4.2 r-Statistic Results

✅ **Valid r-statistic findings:**
- W=0: r=0.605 (GOE-like, ergodic)
- W=20: r=0.437 (closer to Poisson than GOE, shift toward localization)
- Finite-size stability: r-statistic trend consistent across sizes
- 2/3 families (ring, wilson_ring) show r-shift toward Poisson

✅ **Why r-statistic is unaffected:**
- r-statistic = min(δₙ, δₙ₊₁) / max(δₙ, δₙ₊₁) computed from eigenvalue gaps only
- Does NOT require eigenvectors
- Implementation correct (uses `mean_adjacent_gap_ratio` function)
- Independent verification of localization tendency

**Limitation:**
- r-statistic alone is insufficient for PASS verdict (per preregistration)
- Provides weak evidence, not definitive confirmation

### 4.3 No-Overclaim Discipline

✅ **Maintained throughout:**
- Final report correctly identifies verdict as WEAK_OR_INCONCLUSIVE
- No claims of "S³×S¹ validated" or "FL generalized"
- No claims of "Gate 4 PASSED"
- All caveats prominently disclosed (protocol deviation, family dependence, finite lattice)
- Forbidden claims list enforced in results document

### 4.4 Weak Evidence Interpretation

✅ **Supported by available data:**
- r-statistic shift toward Poisson is real (0.605 → 0.437)
- Eigenvalue suppression at W=20 is real (consistent with bound states)
- Finite-size trend strengthening is real (eigenvalue contrast grows with size)

**What this means:**
- Weak evidence that W=20 induces changes consistent with localization physics
- NOT definitive proof (primary metric missing)
- Sufficient for INCONCLUSIVE verdict, not PASS

---

## 5. What Is NOT Valid

### 5.1 Blocked Claims

❌ **FORBIDDEN (unmeasurable without correct IPR):**

1. **"Gate 4 IPR contrast ≥2.0× confirmed"**
   - Threshold is unmeasurable from eigenvalue data
   - Cannot claim this criterion is satisfied

2. **"S³×S¹ validated for localization"**
   - Primary metric invalid → validation incomplete
   - Only weak evidence from secondary metric

3. **"FL mechanism generalized to S³×S¹"**
   - Already forbidden by scope (S³×S¹ only, no FL generalization)
   - Additionally blocked by metric mismatch

4. **"Gate 4 PASS_WITH_CAVEATS"**
   - Primary criterion unmeasurable → PASS verdict blocked
   - Downgraded to WEAK_OR_INCONCLUSIVE

5. **"IPR localization signal robust across families"**
   - IPR was not measured → cannot claim IPR signal exists
   - Eigenvalue signal exists, but eigenvalue ≠ IPR

### 5.2 Field Usage Restrictions

❌ **FORBIDDEN (until corrected):**

1. **Using `mean_low_ipr` field as true IPR in any analysis**
   - Field contains eigenvalue mean, not IPR
   - Label is misleading

2. **Citing prior results labeled "IPR" without verification**
   - Prior experiments may have same mismatch
   - Audit required before reuse

3. **Computing IPR ratio from eigenvalue difference**
   - log(IPR_W20) - log(IPR_W0) = log(IPR_W20 / IPR_W0) only if both are true IPR
   - Eigenvalue difference does not map to IPR ratio threshold

4. **Comparing Gate 4 results to literature IPR values**
   - Literature IPR = Σ|ψᵢ|⁴
   - Our `mean_low_ipr` = mean(eigenvalues)
   - Not comparable

---

## 6. Required Next Steps

### 6.1 Immediate Corrective Action

**Step 1: Implement true IPR computation**

**Required changes in `scripts/run_gate4_batched.py`:**

```python
# BEFORE (incorrect):
eigvals = np.linalg.eigvalsh(H)
low_eigvals = eigvals[: int(0.1 * N)]
mean_low_ipr = float(np.mean(low_eigvals))

# AFTER (correct):
eigvals, eigvecs = np.linalg.eigh(H)  # Get eigenvectors too
low_indices = np.argsort(eigvals)[: int(0.1 * N)]  # Bottom 10% indices
low_eigvecs = eigvecs[:, low_indices]  # Extract bottom 10% eigenvectors

# Compute true IPR for each low eigenstate
iprs = []
for i in range(low_eigvecs.shape[1]):
    psi = low_eigvecs[:, i]
    ipr = np.sum(np.abs(psi)**4)  # IPR = Σ|ψᵢ|⁴
    iprs.append(ipr)

mean_low_ipr = float(np.mean(iprs))  # Now this is TRUE mean IPR
```

**Step 2: Add unit tests**

Create `tests/test_ipr_metric.py`:
```python
def test_ipr_fully_localized():
    """IPR of δ-function state should be 1.0"""
    psi = np.zeros(100)
    psi[50] = 1.0  # Fully localized at site 50
    ipr = np.sum(np.abs(psi)**4)
    assert np.isclose(ipr, 1.0), f"Expected IPR=1.0 for localized, got {ipr}"

def test_ipr_fully_delocalized():
    """IPR of uniform state should be 1/N"""
    N = 100
    psi = np.ones(N) / np.sqrt(N)  # Uniform wavefunction
    ipr = np.sum(np.abs(psi)**4)
    expected = 1.0 / N
    assert np.isclose(ipr, expected), f"Expected IPR={expected} for delocalized, got {ipr}"
```

**Step 3: Decide on re-execution strategy**

**Option A: Re-run Gate 4 with corrected metric**
- If eigenvectors were NOT saved during original execution
- Requires full 216-case re-execution (~96 minutes)
- Creates v0.1.21 with corrected IPR
- Can directly assess ≥2.0× threshold

**Option B: Analyze saved eigenvectors (if available)**
- If eigenvectors were saved but not processed
- No re-execution needed
- Faster correction path

**Option C: Targeted re-execution**
- Re-run only key cases (e.g., s1_size=64, all families, all W)
- Quick sanity check before full re-run decision
- Verify IPR ≠ eigenvalue empirically

### 6.2 Analysis Phase (after corrected metric available)

**Step 4: Recompute IPR contrast**
- Load corrected IPR values for all 216 cases
- Compute IPR(W=20) / IPR(W=0) ratio for each family and size
- Assess ≥2.0× threshold per pre-registered decision rules

**Step 5: Re-apply Gate 4 decision rules**
- Primary criterion now measurable
- Family consistency assessable
- Determine final verdict: PASS_WITH_CAVEATS, WEAK_OR_INCONCLUSIVE, or FAIL

**Step 6: Document correction**
- Create `reports/S3_S1_GATE4_METRIC_CORRECTED_v0.1.21.md`
- Preserve v0.1.20 results for comparison (eigenvalue vs IPR trends)
- Publish erratum alongside corrected results

### 6.3 Audit Prior Results

**Step 7: Audit all prior IPR claims**
- Trace `mean_low_ipr` field across Gate 1, 2, 3, disorder sweeps
- Identify which results are eigenvalues vs true IPR
- Correct or retract affected claims in README.md

**Step 8: Prevent recurrence**
- Add CI test: verify IPR implementation against known test cases
- Rename misleading field: `mean_low_eigenvalue` (if keeping eigenvalue tracking)
- Add separate field: `mean_low_ipr_corrected` (for true IPR)

---

## 7. Lessons for Protocol Design

### 7.1 What Went Wrong

1. **Placeholder metric in dry-run propagated to production**
   - Dry-run used eigenvalue mean as temporary placeholder
   - Placeholder never replaced with true IPR implementation
   - Comment "IPR metric" gave false confidence

2. **Field naming misleading**
   - `mean_low_ipr` suggests IPR, but contains eigenvalue
   - No unit test caught discrepancy
   - No explicit check: "does this field compute Σ|ψᵢ|⁴?"

3. **Pre-registration did not specify implementation details**
   - Protocol defined mathematical formula (Σ|ψᵢ|⁴)
   - Did not specify: use `np.linalg.eigh` (not `eigvalsh`)
   - Gap between protocol and implementation

### 7.2 Prevention for Future Gates

**Recommendation 1: Metric implementation checklist**
- [ ] Mathematical definition written
- [ ] Implementation code matches definition
- [ ] Unit test against known ground truth (localized, delocalized)
- [ ] Field name accurately describes contents
- [ ] No placeholder comments in production code

**Recommendation 2: Pre-registration code review**
- Include implementation code snippet in preregistration doc
- Reviewer verifies: formula → code → test
- Lock both protocol AND reference implementation

**Recommendation 3: Dry-run validation**
- Explicitly test metric on synthetic localized/delocalized states
- Compare computed metric vs analytical expectation
- Document: "Metric validated against ground truth on [date]"

---

## 8. Verdict Stability

### 8.1 Current Verdict

**GATE4_FSS_WEAK_OR_INCONCLUSIVE**

**Basis:**
- r-statistic shift toward Poisson (secondary metric)
- Eigenvalue suppression consistent with localization
- Primary metric (IPR) unmeasurable

**Stability:** LOW (awaits IPR correction)

### 8.2 Possible Outcomes After IPR Correction

**Scenario A: IPR confirms ≥2.0× contrast**
- Verdict upgrades to **GATE4_FSS_PASS_WITH_CAVEATS**
- Weak evidence → confirmed evidence
- r-statistic + IPR both support localization

**Scenario B: IPR shows <2.0× contrast but >1.5×**
- Verdict remains **GATE4_FSS_WEAK_OR_INCONCLUSIVE**
- r-statistic supports, but IPR below threshold
- Consistent with current weak evidence assessment

**Scenario C: IPR contradicts (W=20 IPR < W=0 IPR)**
- Verdict downgrades to **GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED**
- Eigenvalue trend ≠ IPR localization
- r-statistic shift insufficient without IPR confirmation

**Scenario D: IPR shows strong family dependence**
- Verdict remains **WEAK_OR_INCONCLUSIVE**
- Only 1/3 families pass → family consistency fails
- Already observed in r-statistic (spectral_circle anomaly)

### 8.3 No Retroactive PASS Allowed

**Hard rule:**
- Even if corrected IPR shows ≥2.0× contrast, verdict applies to v0.1.21 (corrected run)
- v0.1.20 verdict remains WEAK_OR_INCONCLUSIVE (archived, not upgraded)
- No retroactive promotion of invalid metric data

**Reason:**
- Scientific integrity: verdict based on metrics actually measured
- v0.1.20 did NOT measure IPR → cannot claim v0.1.20 passed IPR threshold

---

## 9. Communication Guidelines

### 9.1 Internal Use

**When referencing Gate 4 v0.1.20:**
- ✅ "Gate 4 execution completed successfully (216/216 cases)"
- ✅ "r-statistic shows weak evidence for localization"
- ✅ "Eigenvalue trend consistent with bound states at W=20"
- ❌ "Gate 4 passed IPR threshold"
- ❌ "S³×S¹ localization validated"

### 9.2 External Communication

**If asked about Gate 4 status before correction:**
- "Gate 4 execution completed, but primary metric (IPR) implementation deviated from protocol. Currently re-implementing corrected metric. Results pending."

**If asked about S³×S¹ validation:**
- "Weak evidence from level-spacing statistics, but definitive validation requires IPR correction. Status: in progress."

**If publishing interim findings:**
- Cite r-statistic results only
- Disclose IPR metric mismatch prominently
- Label verdict as INCONCLUSIVE, not PASS

---

## 10. Erratum Status

**Issue identified:** 2026-05-22 (during post-execution analysis)  
**Root cause:** Placeholder metric (eigenvalue mean) never replaced with true IPR (Σ|ψᵢ|⁴)  
**Impact:** Primary verdict criterion unmeasurable, PASS verdict blocked  
**Corrective action:** Reimplement IPR, add unit tests, re-analyze or re-execute  
**Timeline:** TBD (depends on re-execution strategy decision)  

**Erratum applies to:**
- Gate 4 v0.1.20 execution (commit 66a0f4e)
- All results using `mean_low_ipr` field from this codebase
- Potentially Gate 1, 2, 3 if same field was used

**Erratum does NOT apply to:**
- r-statistic results (independently valid)
- Execution robustness (216/216 cases completed)
- Batched infrastructure (operates correctly)

---

**Document status:** ACTIVE  
**Next update:** After IPR correction implementation decision  
**Related documents:**
- `reports/S3_S1_GATE4_FSS_RESULTS_v0.1.20.md` (analysis with mismatch disclosed)
- `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md` (original protocol)
- `reports/IPR_IMPLEMENTATION_AUDIT_v0.1.20.md` (codebase-wide audit, TBD)
