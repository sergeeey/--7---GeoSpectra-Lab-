# Negative Controls Implementation Check — v0.1.22

**Date:** 2026-05-22  
**Status:** IMPLEMENTATION_COMPLETE  
**Pilot Execution:** NOT STARTED (awaiting explicit command)  
**Gate 4B Status:** UNCHANGED (f7eff32)

---

## Purpose

Verify v0.1.22 negative controls infrastructure is implemented correctly and ready for pilot execution.

**Scope:** Implementation check ONLY. No experiments executed.

---

## Files Added/Modified

### New Module: cc_toy_lab/controls/

**Created:**
- `cc_toy_lab/controls/__init__.py` — Package exports
- `cc_toy_lab/controls/negative_controls.py` — Control builders (3 controls)

**Purpose:** Isolated module for falsification controls. Separate from S³×S¹ operators.

**Controls implemented:**
1. **random_hermitian** — Generic random Hermitian baseline with disorder
2. **scrambled_geometry** — S³×S¹ with permuted indices (broken coupling)
3. **broken_wilson_term** — Wilson term disabled (pure ring)

---

### New Execution Script

**Created:**
- `scripts/run_negative_controls_v0_1_22.py` — 54-case pilot grid runner

**Features:**
- Default mode: `--print-plan` (does NOT execute)
- Execution requires explicit `--run-pilot` flag
- Grid: 54 cases (3 controls × 2 W × 3 sizes × 1 j_max × 3 seeds)
- Batching: 6 batches × 9 cases
- Metrics: `true_ipr_mean` (v0.1.21 canonical), `r_stat`

**Safety guards:**
- No default execution (prevents accidental pilot run)
- No mutation of Gate 4B code paths
- Output to separate directory: `reports/RUNS/negative_controls_v0.1.22/`

---

### New Tests

**Created:**
- `tests/test_negative_controls_grid_v0_1_22.py` — Grid integrity tests (13 tests)
- `tests/test_negative_controls_no_gate4b_mutation.py` — Gate 4B protection tests (7 tests)

**Test coverage:**
- Grid: 54 cases, no duplicates, correct parameters
- Batches: 6 batches, 9 cases each, full coverage
- Controls: Hermitian, correct dimension, deterministic
- Gate 4B: unchanged after importing negative controls
- Default execution: does NOT start pilot

---

## Control Builders Implemented

### Control A: random_hermitian

**Constructor:**
```python
build_random_hermitian_control(
    j_max=3, s1_size=128, disorder_strength=20.0, seed=123, radius=1.0
)
```

**Structure:**
- Dimension: `N = s3_dimension(j_max) × s1_size` (same as S³×S¹)
- Diagonal: `U(r) ∈ [-W, W]` (uniform disorder)
- Off-diagonal: Gaussian random couplings (scale ~ 1.0)
- NO geometric structure (no S³ harmonics, no S¹ twist)

**Expected outcome:** Should NOT reproduce Gate 4B PASS pattern.

**Verification:**
- Hermiticity residual: <1e-10 ✓
- Dimension for j_max=3, s1_size=128: 13824 ✓
- Deterministic with fixed seed ✓

---

### Control B: scrambled_geometry

**Constructor:**
```python
build_scrambled_geometry_control(
    j_max=3, s1_size=128, alpha=0.0, disorder_strength=20.0, seed=123,
    radius=1.0, scramble_mode='permutation'
)
```

**Structure:**
- Builds standard S³×S¹ operator first
- Applies random permutation of basis indices
- Breaks geometric coupling while preserving dimension

**Expected outcome:** Should weaken or destabilize localization signal.

**Verification:**
- Hermiticity residual: <1e-10 ✓
- Dimension matches S³×S¹ ✓
- Deterministic with fixed seed ✓

---

### Control C: broken_wilson_term

**Constructor:**
```python
build_broken_wilson_term_control(
    j_max=3, s1_size=128, alpha=0.0, disorder_strength=20.0, seed=123,
    radius=1.0, wilson_mode='disabled'
)
```

**Structure:**
- Uses `s1_family='ring'` (no Wilson term)
- Wilson correction disabled (coefficient = 0)
- Tests whether Wilson term is load-bearing

**Expected outcome:** Should NOT reproduce wilson_ring robustness (8.49× contrast).

**Verification:**
- Hermiticity residual: <1e-10 ✓
- Dimension matches S³×S¹ ✓
- Deterministic with fixed seed ✓

---

## Pilot Grid Verification

**Grid parameters (locked v0.1.22):**
- Controls: `['random_hermitian', 'scrambled_geometry', 'broken_wilson_term']` ✓
- Disorder W: `[0, 20]` (skip W=12) ✓
- S¹ sizes: `[16, 64, 128]` (skip 32) ✓
- j_max: `[3]` (max dimension only) ✓
- seeds: `[123, 456, 789]` ✓
- alpha: `0.0` (PBC) ✓
- radius: `1.0` ✓

**Total cases:** 54 (3 × 2 × 3 × 1 × 3) ✓

**Batching:**
- Batch 1: random_hermitian, W=0 → 9 cases ✓
- Batch 2: random_hermitian, W=20 → 9 cases ✓
- Batch 3: scrambled_geometry, W=0 → 9 cases ✓
- Batch 4: scrambled_geometry, W=20 → 9 cases ✓
- Batch 5: broken_wilson_term, W=0 → 9 cases ✓
- Batch 6: broken_wilson_term, W=20 → 9 cases ✓

**Coverage:** All 54 cases covered, no duplicates, no overlap ✓

---

## Metric Schema

**Canonical metric:** `true_ipr_mean` (v0.1.21 eigenvector-based IPR)

**Computation:**
```python
eigenvalues, eigenvectors = eigh(operator)
n_low = int(0.1 * len(eigenvalues))  # Bottom 10%
low_eigvecs = eigenvectors[:, :n_low]
ipr_values = inverse_participation_ratio(low_eigvecs)
true_ipr_mean = np.mean(ipr_values)
```

**Additional metric:** `r_stat` (level-spacing adjacent gap ratio)

**Metric version tag:** `v0.1.22_negative_controls_true_ipr`

**Schema consistency:** Same as Gate 4B v0.1.21 ✓

---

## Tests Run and Results

### Grid Integrity Tests (test_negative_controls_grid_v0_1_22.py)

**Results:** 13/13 PASSED (1.24s)

| Test | Status |
|------|--------|
| test_grid_total_cases | PASSED ✓ |
| test_grid_no_duplicates | PASSED ✓ |
| test_grid_controls_set | PASSED ✓ |
| test_grid_disorder_values | PASSED ✓ |
| test_grid_sizes | PASSED ✓ |
| test_grid_j_max | PASSED ✓ |
| test_grid_seeds | PASSED ✓ |
| test_batch_count | PASSED ✓ |
| test_batch_sizes | PASSED ✓ |
| test_batch_coverage | PASSED ✓ |
| test_control_dimension_consistency | PASSED ✓ |
| test_alpha_fixed | PASSED ✓ |
| test_radius_fixed | PASSED ✓ |

---

### Gate 4B Non-Mutation Tests (test_negative_controls_no_gate4b_mutation.py)

**Results:** 7/7 PASSED (12.86s)

| Test | Status |
|------|--------|
| test_s3s1_operator_still_hermitian | PASSED ✓ |
| test_s3s1_dimension_unchanged | PASSED ✓ |
| test_controls_in_separate_module | PASSED ✓ |
| test_control_hermiticity | PASSED ✓ |
| test_control_dimension_matches_s3s1 | PASSED ✓ |
| test_control_deterministic_with_seed | PASSED ✓ |
| test_default_execution_does_not_start_pilot | PASSED ✓ |

**Total:** 20/20 tests PASSED ✓

---

## Confirmation: No Experiments Executed

**Verification:**
- Output directory `reports/RUNS/negative_controls_v0.1.22/` does NOT exist ✓
- No pilot execution triggered ✓
- No 54-case grid run ✓
- No metrics computed on real controls ✓

**--print-plan output:** 54 cases, 6 batches, execution disabled ✓

**Execution guard working:** Default behavior is `--print-plan`, NOT `--run-pilot` ✓

---

## Confirmation: Gate 4B Outputs Not Modified

**Verification:**
- Gate 4B results directory unchanged: `reports/RUNS/gate4_fss_v0.1.21/` ✓
- Gate 4B reports unchanged (commit f7eff32) ✓
- S³×S¹ operator Hermiticity unchanged (residual <1e-10) ✓
- S³×S¹ dimension formula unchanged ✓
- Controls in separate module (no cross-contamination) ✓

**Immutability test:** Gate 4B tests still pass after importing negative controls ✓

---

## Remaining Steps

**Implementation complete. Next: code review before execution.**

**DO NOT execute pilot without:**
1. ✓ Code review of commit c733f7e (this implementation)
2. ✓ Explicit user approval after review
3. ✓ Optional: single-case smoke test first

**Optional smoke test (one case only):**
```bash
# Test random_hermitian control, W=0, s1_size=16, seed=123 (smallest case)
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 1 --case-limit 1
```

**Full pilot execution (only after review + approval):**
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot
```

**Estimated runtime:** ~1.5 hours for full 54 cases

**Steps after pilot execution (NOT before review):**
1. Aggregate results (`scripts/aggregate_negative_controls_results.py`)
2. Apply decision rules (`scripts/apply_negative_controls_decision_rules.py`)
3. Write results report (`reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`)

---

## Success Criteria

**Implementation phase (COMPLETE):**
- [x] 3 control constructors implemented
- [x] Execution script runs without errors
- [x] All tests pass (grid coverage, no Gate 4B mutation)
- [x] --print-plan produces valid output
- [x] Default execution does NOT start pilot

**Execution phase (PENDING):**
- [ ] 54-case pilot grid executed
- [ ] Aggregation script produces merged JSON files
- [ ] Decision script produces verdict
- [ ] Results report written

---

## Files Ready for Commit

**New files:**
- `cc_toy_lab/controls/__init__.py`
- `cc_toy_lab/controls/negative_controls.py`
- `scripts/run_negative_controls_v0_1_22.py`
- `tests/test_negative_controls_grid_v0_1_22.py`
- `tests/test_negative_controls_no_gate4b_mutation.py`
- `reports/NEGATIVE_CONTROLS_IMPLEMENTATION_CHECK_v0.1.22.md` (this file)

**Modified files:** None

**Gate 4B files (unchanged):**
- `cc_toy_lab/spectral/s3_s1_product_discretized.py` ✓
- `scripts/run_gate4_batched.py` ✓
- `reports/RUNS/gate4_fss_v0.1.21/` ✓

---

**Implementation Date:** 2026-05-22  
**Implementation Status:** COMPLETE  
**Test Status:** 20/20 PASSED  
**Pilot Execution Status:** NOT STARTED (blocked on explicit user command)  
**Gate 4B Status:** UNCHANGED (immutability verified)

**Next Review:** After user approves pilot execution or requests modifications
