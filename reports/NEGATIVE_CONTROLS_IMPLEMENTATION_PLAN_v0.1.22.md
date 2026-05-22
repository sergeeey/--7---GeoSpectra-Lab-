# Negative Controls Implementation Plan — v0.1.22

**Date:** 2026-05-22  
**Status:** PLANNING  
**Pre-registration:** S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md  
**Target:** Create 3 negative controls (random Hermitian, scrambled geometry, broken Wilson)

---

## 1. Implementation Strategy

**Core principle:**  
Add controls WITHOUT touching Gate 4B code paths. Gate 4B results (commit f7eff32) must remain reproducible.

**Approach:**
1. Create NEW control constructors in separate module
2. Reuse existing metrics pipeline (true IPR, r_stat)
3. Create NEW execution script (NOT modify `run_gate4_batched.py`)
4. Reuse aggregation + decision scripts with control labels

**No modification zones:**
- `cc_toy_lab/geometry/s3_s1_product.py` — Gate 4B S³×S¹ operator
- `scripts/run_gate4_batched.py` — Gate 4B execution script
- `reports/RUNS/gate4_fss_v0.1.21/` — Gate 4B raw outputs

---

## 2. Code Architecture

### Current S³×S¹ Construction (Read-Only Reference)

**Key files to inspect:**
- `cc_toy_lab/geometry/s3_s1_product.py` — S³×S¹ Hamiltonian constructor
- `cc_toy_lab/geometry/spheres.py` — S³ spherical harmonics
- `cc_toy_lab/geometry/s1_families.py` — spectral_circle, ring, wilson_ring

**Entry point:**
```python
# From scripts/run_gate4_batched.py
from cc_toy_lab.geometry.s3_s1_product import build_s3_s1_hamiltonian

H = build_s3_s1_hamiltonian(
    j_max=3,
    s1_size=128,
    family='spectral_circle',
    alpha=0.5,
    W=20.0,
    seed=123
)
```

**S³ structure:**
- Eigenvalues: `l(l+2)` for `l = 0, 1, ..., j_max`
- Degeneracy: `2l + 1` per level
- Matrix dimension: `N_S3 = sum_{l=0}^{j_max} (2l + 1) = (j_max + 1)^2`

**S¹ structure:**
- Family: spectral_circle (analytic), ring (lattice), wilson_ring (lattice + Wilson term)
- Twist: boundary condition `ψ(2π) = exp(iα) ψ(0)`
- Matrix dimension: `N_S1 = s1_size`

**Full dimension:**
```
N_total = N_S3 × N_S1 = (j_max + 1)^2 × s1_size
N_max (j_max=3, s1_size=128) = 16 × 128 = 2048  # Wait, this is wrong
# Correction: N_S3 for j_max=3 is (2*0+1) + (2*1+1) + (2*2+1) + (2*3+1) = 1+3+5+7 = 16? No.
# Actually: l goes 0 to j_max, so 4 values. Sum = 1+3+5+7 = 16? 
# Let me recalculate: For j_max=3, we have l=0,1,2,3. Degeneracies: 1, 3, 5, 7 → sum = 16? 
# But Gate 4B says N_max = 896 for j_max=3, s1_size=128.
# 896 / 128 = 7. So N_S3 = 7 for j_max=3.
# Formula from Gate 4B: N_S3 = 2*j_max + 1 = 2*3 + 1 = 7. ✅
# So for j_max, we select ONE l value, not sum over all l.
# Need to verify exact S³ construction from code.
```

**Action:** Read `cc_toy_lab/geometry/s3_s1_product.py` to understand exact S³ sector construction.

---

### Proposed New Module

**File:** `cc_toy_lab/geometry/negative_controls.py`

**Contents:**
```python
"""
Negative control Hamiltonians for specificity testing.

DO NOT use these for positive S³×S¹ claims.
These are falsification controls to test harness discrimination power.
"""

def build_random_hermitian_control(N, W, seed):
    """
    Control A: Random Hermitian baseline.
    
    Structure:
    - Diagonal: U(r) ∈ [-W, W] (same disorder model as Gate 4B)
    - Off-diagonal: Gaussian random couplings with scale ~ 1.0
    - NO geometric structure
    
    Expected: Should NOT reproduce Gate 4B-like PASS pattern.
    """
    pass

def build_scrambled_geometry_control(j_max, s1_size, W, seed, scramble_mode='permutation'):
    """
    Control B: Scrambled geometry control.
    
    Options:
    - 'permutation': S³ harmonic indices randomly permuted
    - 'decoupled': S³ and S¹ sectors independent (no cross-coupling)
    - 'wrong_spectrum': Replace S³ eigenvalues with power-law or random
    
    Expected: Should weaken or destabilize localization signal.
    """
    pass

def build_broken_wilson_control(j_max, s1_size, alpha, W, seed, wilson_mode='disabled'):
    """
    Control C: Broken Wilson term control.
    
    Options:
    - 'disabled': Wilson coefficient = 0
    - 'scrambled': Wilson term structure randomized
    
    Expected: Should NOT reproduce wilson_ring Gate 4B result (8.49× contrast).
    """
    pass
```

**Design questions to resolve:**
1. What is exact S³ construction in Gate 4B? (single l-sector vs full harmonic sum)
2. How are S³ and S¹ sectors coupled? (Kronecker product? additive?)
3. What is Wilson term formula? (read `s1_families.py`)
4. What scale should random couplings have? (match S³×S¹ off-diagonal scale)

---

## 3. Files to Inspect (Dependency Audit)

### Core Geometry
- `cc_toy_lab/geometry/s3_s1_product.py` — S³×S¹ Hamiltonian builder
- `cc_toy_lab/geometry/spheres.py` — S³ eigenvalues, degeneracies
- `cc_toy_lab/geometry/s1_families.py` — spectral_circle, ring, wilson_ring definitions

### Disorder
- How is disorder applied in Gate 4B? (diagonal perturbation only? scale?)
- Check: `scripts/run_gate4_batched.py` lines near W parameter

### Metrics (Reuse, Do Not Modify)
- `cc_toy_lab/spectral/metrics.py` — true IPR (Σ|ψ|⁴), already correct
- `cc_toy_lab/spectral/r_statistics.py` — level-spacing diagnostic

### Execution Pipeline (Read-Only)
- `scripts/run_gate4_batched.py` — Gate 4B batched execution (DO NOT MODIFY)
- `scripts/aggregate_gate4b_results.py` — aggregation (reuse with control labels)
- `scripts/apply_gate4b_decision_rules.py` — decision logic (reuse, thresholds unchanged)

---

## 4. Implementation Steps

### Step 1: Dependency Audit (Read-Only)

**Read these files to understand structure:**
```bash
# S³×S¹ construction
Read cc_toy_lab/geometry/s3_s1_product.py

# S³ eigenvalue structure
Read cc_toy_lab/geometry/spheres.py

# S¹ family definitions
Read cc_toy_lab/geometry/s1_families.py

# Gate 4B execution script (disorder application)
Read scripts/run_gate4_batched.py:200-250
```

**Extract:**
- Exact S³ dimension formula
- S³×S¹ coupling mechanism
- Wilson term formula
- Disorder application method (how W is used)

---

### Step 2: Create Control Module

**File:** `cc_toy_lab/geometry/negative_controls.py`

**Implement:**
1. `build_random_hermitian_control(N, W, seed)` — Control A
2. `build_scrambled_geometry_control(j_max, s1_size, W, seed)` — Control B
3. `build_broken_wilson_control(j_max, s1_size, alpha, W, seed)` — Control C

**Design constraints:**
- Same dimension N as corresponding S³×S¹ case
- Same disorder strength W (for fair comparison)
- Same random seed mechanism (for reproducibility)
- NO geometric structure (for falsification)

---

### Step 3: Create Execution Script

**File:** `scripts/run_negative_controls_v0_1_22.py`

**Based on:** `scripts/run_gate4_batched.py` (copy structure, NOT modify original)

**Changes from Gate 4B script:**
- Replace `family` parameter with `control` parameter (random_hermitian, scrambled_geometry, broken_wilson)
- Replace `build_s3_s1_hamiltonian()` call with control constructor
- Keep same metrics pipeline (true IPR, r_stat)
- Keep same output schema (JSON per case)

**Grid:** 54 cases (3 controls × 2 W × 3 sizes × 1 j_max × 3 seeds)

**Execution mode:** Batched (6 batches × 9 cases)

---

### Step 4: Create Tests

**File:** `tests/test_negative_controls_grid_v0_1_22.py`

**Purpose:** Verify 54 unique cases, no duplicates, no missing combinations

**Tests:**
- `test_control_grid_coverage()` — 54 unique cases
- `test_no_control_duplicates()` — no repeated (control, W, size, j_max, seed)
- `test_control_dimension_matches_s3s1()` — N(random_hermitian) == N(spectral_circle) for same j_max, s1_size

---

**File:** `tests/test_negative_controls_no_gate4b_mutation.py`

**Purpose:** Verify Gate 4B results unchanged after adding controls

**Tests:**
- `test_s3s1_operator_unchanged()` — build_s3_s1_hamiltonian() produces same output as before
- `test_gate4b_results_immutable()` — Gate 4B f7eff32 outputs still reproducible
- `test_control_files_separate()` — controls in separate module, no cross-contamination

---

### Step 5: Aggregation (Reuse)

**Script:** `scripts/aggregate_negative_controls_results.py`

**Based on:** `scripts/aggregate_gate4b_results.py` (adapt for control labels)

**Changes:**
- Replace `family` with `control` in grouping
- Keep same aggregation logic (mean IPR by group)
- Keep same output schema (JSON per metric)

---

### Step 6: Decision Rules (Reuse)

**Script:** `scripts/apply_negative_controls_decision_rules.py`

**Based on:** `scripts/apply_gate4b_decision_rules.py` (thresholds unchanged)

**Decision logic:**
- Same ≥2.0× threshold for concern
- Same ≥2/3 consistency check (controls instead of families)
- Same FSS trend check (strengthening, saturating, collapsing)
- NEW verdict labels: NEGATIVE_CONTROL_FAILS_AS_EXPECTED, NEGATIVE_CONTROL_FALSE_PASS

---

## 5. Risk Assessment

### Risk 1: Control Too Artificial

**Risk:** Random Hermitian may be TOO different from S³×S¹ (dimension mismatch, no block structure)

**Mitigation:**
- Match dimension N exactly
- Match disorder strength W exactly
- Preserve some structure (e.g., block-diagonal if S³×S¹ has it)

**Detection:** If random Hermitian shows <0.5× contrast (too weak), control may be under-constrained

---

### Risk 2: Random Baseline Dimension Mismatch

**Risk:** S³×S¹ has product structure, random Hermitian is flat matrix → not comparable

**Mitigation:**
- Use same total dimension N
- OR: construct random baseline with same block structure (N_S3 blocks, each N_S1 × N_S1)

**Detection:** Compare eigenvalue distribution (random should be semicircle, S³×S¹ should be structured)

---

### Risk 3: False Pass Due to Metric Artifact

**Risk:** true IPR metric may increase with ANY disorder, not just geometric

**Mitigation:**
- Verify: Is W=0 baseline stable for controls? (should be ~1/N)
- Compare: IPR(random, W=20) vs IPR(S³×S¹, W=20) — should differ if geometric coupling matters

**Detection:** If random Hermitian shows SAME 7.15× contrast as S³×S¹, metric is non-specific

---

### Risk 4: Accidentally Modifying Gate 4B Pipeline

**Risk:** Adding controls breaks existing S³×S¹ operator

**Mitigation:**
- Separate module (`negative_controls.py`, not modify `s3_s1_product.py`)
- Separate script (`run_negative_controls_v0_1_22.py`, not modify `run_gate4_batched.py`)
- Unit test: `test_s3s1_operator_unchanged()` fails if Gate 4B path modified

**Detection:** Run Gate 4B test suite after adding controls — should still pass

---

### Risk 5: Scrambled Geometry Still Geometric

**Risk:** Permutation scramble may not fully destroy geometric structure (e.g., eigenvalue distribution preserved)

**Mitigation:**
- Verify: scrambled control eigenvalue distribution ≠ S³×S¹ eigenvalue distribution
- Compare: IPR(scrambled) should differ from IPR(S³×S¹) at W=0 (baseline check)

**Detection:** If scrambled shows SAME W=0 baseline as S³×S¹, scramble is too weak

---

## 6. Pre-Implementation Checklist

**Before writing code:**

- [ ] Read `cc_toy_lab/geometry/s3_s1_product.py` — understand S³×S¹ construction
- [ ] Read `cc_toy_lab/geometry/s1_families.py` — understand Wilson term formula
- [ ] Verify: What is exact S³ dimension for j_max=3? (should be 7, verify from code)
- [ ] Verify: How is disorder W applied? (diagonal perturbation U(r) ∈ [-W, W]?)
- [ ] Verify: What is S³×S¹ off-diagonal coupling scale? (for random Hermitian baseline)
- [ ] Design: Random Hermitian baseline dimension strategy (flat vs block-diagonal)
- [ ] Design: Scrambled geometry scramble mode (permutation vs decoupled vs wrong_spectrum)
- [ ] Design: Broken Wilson mode (disabled vs scrambled)

**After reading dependencies:**

- [ ] Write `cc_toy_lab/geometry/negative_controls.py`
- [ ] Write `scripts/run_negative_controls_v0_1_22.py`
- [ ] Write `tests/test_negative_controls_grid_v0_1_22.py`
- [ ] Write `tests/test_negative_controls_no_gate4b_mutation.py`
- [ ] Run tests: `pytest tests/test_negative_controls_*.py -v`
- [ ] Verify: Gate 4B tests still pass after adding controls

---

## 7. Execution Protocol (After Implementation)

**Step 1:** Dry-run (single case)
```bash
python scripts/run_negative_controls_v0_1_22.py \
  --control random_hermitian \
  --W 20 \
  --s1_size 16 \
  --j_max 3 \
  --seed 123 \
  --output reports/RUNS/negative_controls_v0.1.22/dryrun/
```

**Step 2:** Verify outputs
- `dryrun/case_*.json` contains `true_ipr_mean`, `r_stat`
- No errors, no NaN values
- Dimension matches expected N = (2*j_max + 1) × s1_size

**Step 3:** Run pilot grid (54 cases, 6 batches)
```bash
python scripts/run_negative_controls_v0_1_22.py \
  --mode batched \
  --output reports/RUNS/negative_controls_v0.1.22/
```

**Step 4:** Aggregate results
```bash
python scripts/aggregate_negative_controls_results.py \
  --input reports/RUNS/negative_controls_v0.1.22/batches/ \
  --output reports/RUNS/negative_controls_v0.1.22/merged/
```

**Step 5:** Apply decision rules
```bash
python scripts/apply_negative_controls_decision_rules.py \
  --input reports/RUNS/negative_controls_v0.1.22/merged/ \
  --output reports/RUNS/negative_controls_v0.1.22/merged/verdict_analysis.json
```

**Step 6:** Write results report
- `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`
- Include: verdict, control-level contrasts, FSS trends, false-pass audit if needed

---

## 8. Output Schema

**Per-case output:** Same as Gate 4B
```json
{
  "control": "random_hermitian",  // NOT "family"
  "W": 20.0,
  "s1_size": 128,
  "j_max": 3,
  "seed": 123,
  "N": 896,
  "true_ipr_mean": 0.234,
  "r_stat": 0.442,
  "uses_eigenvectors": true,
  "ipr_metric_version": "v0.1.21_true_eigenvector_ipr",
  "runtime_seconds": 28.4
}
```

**Merged outputs:** Adapted from Gate 4B
- `control_summary.json` — per-control aggregate (NOT family_summary.json)
- `true_ipr_contrast_summary.json` — control contrasts (NOT family contrasts)
- `verdict_analysis.json` — final verdict with false-pass check

---

## 9. Success Criteria (Implementation)

**Code complete when:**
- [ ] 3 control constructors implemented
- [ ] Execution script runs 54-case grid without errors
- [ ] All tests pass (grid coverage, no Gate 4B mutation)
- [ ] Dry-run produces valid outputs
- [ ] Aggregation script produces merged JSON files
- [ ] Decision script produces verdict

**NOT required for implementation phase:**
- Full 54-case execution (defer to execution command)
- Results report (defer to post-execution analysis)

---

## 10. Next Steps After Implementation

**If implementation succeeds:**
1. Commit implementation (scripts, tests, control module)
2. DO NOT commit results yet (results come from execution)
3. Ask user: "Ready to execute 54-case pilot grid?"

**If implementation blocked:**
1. Report: which step blocked, why
2. Ask user: design decision needed (e.g., random baseline dimension strategy)

---

## 11. Time Estimate

**Implementation phase:**
- Dependency audit: 30 min (read 3 files)
- Control module: 1 hour (3 constructors)
- Execution script: 30 min (adapt from Gate 4B)
- Tests: 30 min (2 test files)
- Dry-run + debug: 30 min
- **Total:** ~3 hours

**Execution phase (separate):**
- Pilot grid: ~27 min (54 cases)
- Aggregation + decision: ~5 min
- Results report: ~30 min
- **Total:** ~1 hour

---

**Plan Status:** READY  
**Next Action:** Read dependencies (Step 1) OR ask user for clarification  
**Blocked On:** None (can proceed immediately)
