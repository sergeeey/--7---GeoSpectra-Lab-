# Negative Controls v0.1.22 — Smoke Test Report

**Date:** 2026-05-22  
**Status:** SMOKE TEST PASSED  
**Protocol version:** v0.1.22  

---

## Test Scope

**Executed:** 1 case из 54 (minimal smoke test)  
**Purpose:** Verify infrastructure before full pilot execution  

**Grid coverage:**
- Control: `random_hermitian`
- Disorder W: 0
- S¹ size: 16
- j_max: 3
- Seed: 123
- Alpha: 0.0 (PBC)

---

## Results Summary

### Case 000: random_hermitian, W=0, s1_size=16, seed=123

| Metric | Value | Status |
|--------|-------|--------|
| **Control type** | random_hermitian | ✓ |
| **Total dimension N** | 1728 | ✓ |
| **true_ipr_mean** | 0.001736 | ✓ present |
| **r_stat** | 0.527503 | ✓ present |
| **Runtime** | 1.55 sec | ✓ |
| **Uses eigenvectors** | true | ✓ |
| **Metric version** | v0.1.22_negative_controls_true_ipr | ✓ |

**Meta fields verified:**
- ✓ control = "random_hermitian"
- ✓ j_max = 3
- ✓ s1_size = 16
- ✓ disorder_strength = 0.0
- ✓ seed = 123
- ✓ s3_dimension = 108
- ✓ total_dimension = 1728
- ✓ construction = "diagonal disorder + Gaussian off-diagonal"
- ✓ status = "Control A: falsification baseline"

---

## Infrastructure Verification

### Files created
```
reports/RUNS/negative_controls_v0.1.22/
├── config.json                    ✓
└── batch_01/
    └── case_000.json             ✓
```

### Git status
```
M scripts/run_negative_controls_v0_1_22.py    (added --case-limit for smoke test)
```

**Gate 4B outputs:** NOT changed ✓

---

## Smoke Test Verdict

**PASS** — Infrastructure operational

### Verified components
1. ✓ Control construction (random_hermitian)
2. ✓ Spectral computation (eigh)
3. ✓ True IPR metric (bottom 10% eigenstates)
4. ✓ r-statistic computation
5. ✓ Output directory structure
6. ✓ JSON serialization
7. ✓ Metadata inclusion
8. ✓ Runtime measurement

### Not tested (out of smoke test scope)
- [ ] Other control types (scrambled_geometry, broken_wilson_term)
- [ ] Other disorder values (W=20)
- [ ] Other S¹ sizes (64, 128)
- [ ] Other seeds (456, 789)
- [ ] Batch parallelization
- [ ] Aggregation pipeline
- [ ] Decision rules application

---

## Next Steps

**DO NOT run full pilot without:**
1. Pre-registration review: `reports/S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md`
2. Implementation plan review: `reports/NEGATIVE_CONTROLS_IMPLEMENTATION_PLAN_v0.1.22.md`
3. Explicit command: `--run-pilot` (without --case-limit)

**Estimated runtime for full pilot:**
- 54 cases × 1.55 sec/case ≈ 84 sec (1.4 min) if no disorder
- Actual with W=20 cases: ~10–15 min (estimated)

**Batch structure:**
- Batch 1: random_hermitian, W=0 (9 cases)
- Batch 2: random_hermitian, W=20 (9 cases)
- Batch 3: scrambled_geometry, W=0 (9 cases)
- Batch 4: scrambled_geometry, W=20 (9 cases)
- Batch 5: broken_wilson_term, W=0 (9 cases)
- Batch 6: broken_wilson_term, W=20 (9 cases)

---

## Code Changes

**Added to `scripts/run_negative_controls_v0_1_22.py`:**
- `--case-limit` argument for smoke testing
- Modified `run_batch()` to accept `case_limit` parameter
- Smoke test warning in output

**Purpose:** Enable minimal infrastructure verification without full pilot execution.

**Scope:** Temporary testing aid, does NOT affect protocol immutability.

---

**End of smoke test report**  
**Status:** INFRASTRUCTURE VERIFIED — ready for full pilot when authorized
