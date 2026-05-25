# Gate 4B Rerun Protocol — v0.1.24

**Date:** 2026-05-25  
**Status:** 📋 **PRE-RERUN CHECKPOINT**  
**Purpose:** Protocol for Gate 4B v0.1.24 rerun with corrected S³ Dirac operator  
**Commit:** 093573b `fix(operator): restore S3 Dirac negative k0 branch`

---

## 1. RERUN OBJECTIVE

**Goal:** Execute Gate 4B toy-lab validation campaign (216 cases) using **corrected S³ Dirac operator** (negative k ≥ 0, includes -3/2 eigenvalue).

**Why rerun required:**
- v0.1.21-23 used **incomplete operator** (missing -3/2 eigenvalue)
- Operator spectrum changed (restored canonical symmetric ±3/2, ±5/2, ±7/2)
- Hilbert space dimension changed (+2 per truncation level)
- v0.1.21 results cannot be interpreted as "canonical S³ Dirac operator validation"

**Source verification:** arXiv:1103.4097 Section 6 (negative branch k ≥ 0, positive branch k ≥ 1)

**Decision document:** `reports/GATE_4B_RERUN_DECISION_v0.1.24.md`

---

## 2. CORRECTED OPERATOR SUMMARY

### 2.1 What Changed (v0.1.21 → v0.1.24)

**Code change:** `cc_toy_lab/spectral/dirac_s3.py`
- Added k=0 negative branch (λ = -3/2, degeneracy 2)
- Dimension formula: `total_dim = k0_neg_degeneracy + sum(dimensions)`

**Spectrum change:**

| j_max | Before (v0.1.21) | After (v0.1.24) | Δ |
|-------|------------------|-----------------|---|
| 0 | `[-2.5(×6), +1.5(×2)]` (dim=8) | `[-2.5(×6), -1.5(×2), +1.5(×2)]` (dim=10) | **+2** |
| 1 | `[-3.5(×12), -2.5(×6), +1.5(×2), +2.5(×6)]` (dim=26) | `[-3.5(×12), -2.5(×6), -1.5(×2), +1.5(×2), +2.5(×6)]` (dim=28) | **+2** |
| 2 | 6 unique eigenvalues (dim=58) | 7 unique eigenvalues (dim=60) | **+2** |

**Key restoration:** λ = **-3/2** now present (was missing in v0.1.21)

### 2.2 Smoke Diagnostic (2026-05-25)

✅ **All checks PASS:**
- -3/2 eigenvalue present
- +3/2 eigenvalue present
- Radius scaling: λ(R=2) = λ(R=1)/2
- Dimension: 10/28/60 for j_max=0/1/2
- Hermiticity preserved
- Eigenvalues real

**Verdict:** Corrected operator ready for rerun.

---

## 3. FROZEN STATUS: Gate 4B v0.1.21

### 3.1 What Remains Preserved

**v0.1.21 computational outputs:**
- Location: `results/v0.1.21/` (if exists) or archived location
- Status: **PRESERVED** (do NOT delete, do NOT overwrite)
- Label: "Gate 4B v0.1.21 — incomplete operator (missing -3/2)"

**What v0.1.21 validated:**
- Computational integrity: 216/216 cases executed correctly
- Internal consistency: finite-size scaling trends for **v0.1.21 operator**
- Methodological value: falsification-first harness demonstrated

### 3.2 What Is Frozen

**v0.1.21 interpretation:**
- ❌ Cannot claim "validates canonical S³ Dirac spectrum"
- ❌ Cannot use for external communication (papers, grants)
- ❌ Cannot compare directly to v0.1.24 (different operators)

**Status:** FROZEN until v0.1.24 rerun complete and comparison documented.

---

## 4. RERUN PARAMETERS

### 4.1 Grid Specification

**CRITICAL:** Use **same parameter grid** as v0.1.21 for comparison.

**S³×S¹ toy-lab grid:**
- Geometry: S³×S¹ product
- S³ discretization: toy-lab (finite-mode truncation)
- S¹ discretization: 3 methods (uniform, adaptive, hybrid)
- Parameter sweep: [specific j_max, n_max, radii values from v0.1.21]
- Total cases: **216**

**Source:** Gate 4B v0.1.21 campaign specification (retrieve exact parameters from v0.1.21 run log)

### 4.2 Output Directory

**NEW directory (do NOT overwrite v0.1.21):**
```
results/gate4b_v0.1.24/
```

**Structure:**
```
results/gate4b_v0.1.24/
├── raw/                    # Raw eigenvalue/eigenvector data
├── metrics/                # IPR, FSS, aggregate metrics
├── plots/                  # Visualization outputs
├── logs/                   # Execution logs
└── metadata.json           # Run parameters, commit hash, timestamp
```

**Metadata fields:**
- `commit`: `093573b`
- `operator_version`: `v0.1.24 (corrected, negative k≥0)`
- `timestamp`: run start/end
- `total_cases`: 216
- `dimension_formula`: `k0_neg_degeneracy + sum(dimensions)`

### 4.3 Expected Runtime

**Estimate:** ~6 hours (same as v0.1.21)
- Per-case time: ~100 seconds
- Total: 216 cases × 100s ≈ 21600s ≈ 6h
- Plus overhead: plotting, aggregation

**Constraint:** LOCAL_EXECUTION_PROHIBITED (thermal limit)
- Use remote execution if available
- Or wait for local thermal budget recovery

---

## 5. REQUIRED OUTPUTS

### 5.1 Primary Metrics (Same as v0.1.21)

**Per-case outputs:**
1. **IPR (Inverse Participation Ratio)**
   - True IPR (normalized by corrected dimension)
   - False IPR (if applicable)
   - IPR contrast ratio

2. **Finite-Size Scaling (FSS)**
   - Size trend slope
   - Extrapolation to infinite limit

3. **Family Consistency**
   - 3-family comparison (uniform/adaptive/hybrid S¹)
   - Consistency score

4. **r-statistic**
   - Availability flag
   - Value (if available)

**Aggregate outputs:**
1. **Aggregate true IPR contrast** (primary signal metric)
2. **Family contrast ratios**
3. **Size trend summary**
4. **Failure count**

### 5.2 Comparison Outputs (New for v0.1.24)

**v0.1.21 vs v0.1.24 comparison:**
1. **Dimension change impact**
   - Per j_max: dimension difference (+2)
   - IPR normalization shift

2. **Eigenvalue spectrum shift**
   - Old spectrum (missing -3/2) vs new spectrum (includes -3/2)
   - Impact on IPR distribution

3. **Signal stability**
   - Aggregate contrast: v0.1.21 value vs v0.1.24 value
   - Qualitative verdict: preserved / weaker / disappeared

4. **Failure rate comparison**
   - v0.1.21: X/216 failures
   - v0.1.24: Y/216 failures

---

## 6. COMPARISON METRICS

### 6.1 Primary Comparison Table

| Metric | v0.1.21 (incomplete) | v0.1.24 (corrected) | Δ | Verdict |
|--------|---------------------|---------------------|---|---------|
| **Aggregate true IPR contrast** | [value] | [value] | [Δ%] | [preserved/weaker/lost] |
| **Family contrasts** | [3 values] | [3 values] | [Δ] | [consistent/shifted] |
| **Size trend** | [slope] | [slope] | [Δ] | [stable/changed] |
| **r-stat availability** | [X/216] | [Y/216] | [Δ] | [same/improved/degraded] |
| **Failures** | [X/216] | [Y/216] | [Δ] | [same/more/fewer] |
| **Dimension (j_max=2)** | 58 | 60 | +2 | [expected] |

### 6.2 Qualitative Verdict Impact

**Signal preserved:**
- Aggregate contrast v0.1.24 ≈ v0.1.21 (within ±20%)
- Qualitative interpretation unchanged
- **Outcome:** Project strengthened (corrected operator validates signal)

**Signal weaker:**
- Aggregate contrast v0.1.24 < v0.1.21 (drop >20%, still >1.0)
- Qualitative interpretation: PASS → PASS/WEAK
- **Outcome:** Honest weakening, scientifically valuable

**Signal disappears:**
- Aggregate contrast v0.1.24 ≈ 1.0 (no signal)
- Qualitative interpretation: PASS → FAIL
- **Outcome:** Honest negative result (v0.1.21 was operator-artifact contaminated)

**Run fails:**
- Execution errors, numerical instabilities
- **Outcome:** Debugging required, no scientific conclusion yet

---

## 7. FORBIDDEN ACTIONS

**During rerun:**
- ❌ DO NOT overwrite `results/v0.1.21/` directory
- ❌ DO NOT modify v0.1.21 archived outputs
- ❌ DO NOT change parameter grid mid-run
- ❌ DO NOT cherry-pick cases (run all 216)
- ❌ DO NOT declare verdict before comparison complete

**After rerun:**
- ❌ DO NOT claim "Gate 4B v0.1.21 validated canonical operator" (it didn't)
- ❌ DO NOT ignore dimension change in IPR interpretation
- ❌ DO NOT present v0.1.24 as "same as v0.1.21" (they are different operators)

---

## 8. POST-RERUN REQUIRED REPORT

**Document:** `reports/GATE_4B_v0.1.24_COMPARISON_v0.1.21_vs_v0.1.24.md`

**Required sections:**
1. **Executive Summary**
   - One-sentence verdict: signal preserved / weaker / disappeared
   - Primary metric change: aggregate contrast Δ
   - Qualitative interpretation shift

2. **Operator Difference Summary**
   - Spectrum change (missing -3/2 → restored -3/2)
   - Dimension change (+2 per truncation level)
   - Source verification (arXiv:1103.4097 Section 6)

3. **Metric-by-Metric Comparison**
   - Aggregate true IPR contrast
   - Family contrasts
   - Size trends
   - r-stat availability
   - Failures

4. **Dimension Impact Analysis**
   - IPR normalization shift due to +2 dimension
   - Whether shift explains observed Δ

5. **Signal Stability Assessment**
   - Preserved: corrected operator strengthens project
   - Weaker: honest weakening, caveats added
   - Disappeared: honest negative result, v0.1.21 was artifact

6. **Updated Claims/Caveats**
   - What can be claimed after v0.1.24
   - What cannot be claimed (remove v0.1.21-based claims)
   - Explicit boundaries

7. **Next Steps**
   - If signal preserved/weaker: resume Negative Controls
   - If signal disappeared: postmortem analysis
   - If run failed: debugging protocol

---

## 9. POSSIBLE OUTCOMES (4 SCENARIOS)

### Outcome 1: Signal Preserved

**Evidence:**
- Aggregate contrast v0.1.24 ≈ v0.1.21 (within ±20%)
- Family contrasts stable
- Size trend qualitatively same

**Interpretation:**
- Corrected operator **validates signal**
- v0.1.21 incompleteness did not critically affect result
- Project **strengthened** (canonical operator confirms)

**Next steps:**
- Unfreeze Gate 4B interpretation (use v0.1.24 results)
- Resume Negative Controls batches 3-6
- Update external documents to reference v0.1.24

### Outcome 2: Signal Weaker

**Evidence:**
- Aggregate contrast v0.1.24 < v0.1.21 (drop >20%, still >1.0)
- Qualitative verdict: PASS → PASS/WEAK

**Interpretation:**
- Missing -3/2 eigenvalue **inflated** v0.1.21 signal
- Corrected operator gives **honest weaker signal**
- Still scientifically valuable (true positive, not false positive)

**Next steps:**
- Document honest weakening in comparison report
- Add caveats to claims
- Resume Negative Controls with updated expectations

### Outcome 3: Signal Disappears

**Evidence:**
- Aggregate contrast v0.1.24 ≈ 1.0 (no signal)
- Qualitative verdict: PASS → FAIL

**Interpretation:**
- v0.1.21 signal was **operator-artifact contaminated**
- Missing -3/2 created false positive
- **Honest negative result** (scientific integrity preserved)

**Next steps:**
- Write postmortem: why incomplete operator gave false signal
- Negative Controls: validate that artifact zoo detects this type
- Update project claims: v0.1.21 invalidated, v0.1.24 correct

### Outcome 4: Run Fails

**Evidence:**
- Execution errors (numerical instabilities, crashes)
- <216 cases completed

**Interpretation:**
- **No scientific conclusion yet**
- Debugging required (not operator issue, likely technical)

**Next steps:**
- Debug execution environment
- Fix numerical stability issues
- Retry rerun after fix

---

## 10. EXECUTION CHECKLIST

### Pre-Run (COMPLETED)
- [x] Source verification (arXiv:1103.4097 Section 6)
- [x] Code fix committed (093573b)
- [x] Tests GREEN (6/6 PASS)
- [x] Smoke diagnostic PASS
- [x] Rerun decision documented
- [x] Protocol written (this document)

### Run Preparation (NEXT)
- [ ] Retrieve v0.1.21 exact parameter grid
- [ ] Create output directory: `results/gate4b_v0.1.24/`
- [ ] Verify thermal constraint status (local vs remote)
- [ ] Backup v0.1.21 results (if not already archived)
- [ ] Initialize metadata.json with commit hash

### During Run
- [ ] Monitor progress (cases completed / 216)
- [ ] Log any failures or warnings
- [ ] Do NOT modify parameters mid-run
- [ ] Do NOT overwrite v0.1.21 outputs

### Post-Run
- [ ] Verify 216/216 cases completed (or document failures)
- [ ] Generate comparison metrics
- [ ] Write comparison report
- [ ] Update claims/caveats
- [ ] Decide: resume Negative Controls or postmortem

---

## 11. RISK MITIGATION

### Risk 1: Overwrite v0.1.21 Results

**Mitigation:**
- Use separate output directory: `results/gate4b_v0.1.24/`
- Archive v0.1.21 before rerun (if not already done)
- Add write-protection to v0.1.21 directory

### Risk 2: Parameter Grid Mismatch

**Mitigation:**
- Retrieve exact v0.1.21 parameters from run log
- Document parameters in metadata.json
- Verify match before declaring comparison valid

### Risk 3: Premature Verdict

**Mitigation:**
- Do NOT declare verdict before comparison complete
- Require comparison report before any external communication
- Freeze interpretation until all 4 metrics compared

### Risk 4: Cherry-Picking Cases

**Mitigation:**
- Run all 216 cases (no exceptions)
- Document all failures explicitly
- Do NOT exclude "outliers" without justification

---

## 12. SUCCESS CRITERIA

### Minimum Success
- ✅ 216/216 cases completed (or failures documented)
- ✅ Comparison report written
- ✅ Updated claims/caveats documented
- ✅ v0.1.21 results preserved

### Full Success
- ✅ All above
- ✅ Signal stability assessed (one of 4 outcomes)
- ✅ Next steps clear (Negative Controls or postmortem)
- ✅ External documents updated (if any)

---

## 13. CONSTRAINTS

**What remains PAUSED until v0.1.24 rerun + comparison complete:**
- ❌ Negative Controls batches 3-6
- ❌ Gate 5 (full diagnostic)
- ❌ W-sweep (if depends on S³ Dirac)
- ❌ External communication (preprints, grants) using Gate 4B results

**What can proceed independently:**
- ✅ Gate 4A analysis (S²×S¹, independent geometry)
- ✅ Documentation updates (code comments)
- ✅ Unrelated experiments (not S³ Dirac dependent)

---

## 14. AUTHORIZATION

**Status:** 📋 **PROTOCOL READY**

**Awaiting:**
- [ ] User authorization to execute Gate 4B v0.1.24 rerun (216 cases, ~6h)
- [ ] Thermal constraint clearance (local vs remote decision)

**Prerequisites satisfied:**
- ✅ Corrected operator validated (smoke diagnostic PASS)
- ✅ Protocol documented (this file)
- ✅ v0.1.21 preservation plan clear
- ✅ Comparison metrics defined

**Next step:** Execute rerun after explicit authorization.

---

**Author:** Claude Sonnet 4.5  
**Date:** 2026-05-25  
**Session:** Pre-rerun checkpoint  
**Commit:** 093573b `fix(operator): restore S3 Dirac negative k0 branch`

---

**END OF PROTOCOL**
