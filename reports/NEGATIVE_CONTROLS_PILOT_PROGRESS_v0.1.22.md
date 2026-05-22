# Negative Controls Pilot Progress — v0.1.22

**Protocol:** Falsification-first specificity test  
**Expected:** Controls should FAIL to reproduce Gate 4B PASS pattern  
**Danger:** False-pass if ANY control shows Gate 4B-like robustness

---

## Execution Status

**Total Plan:** 54 cases, 6 batches  
**Completed:** 18 cases, 2 batches (33.3%)  
**Status:** BATCH_2_COMPLETED

| Batch | Control | W | Cases | Status | Runtime |
|-------|---------|---|-------|--------|---------|
| **1** | random_hermitian | 0 | 9/9 | ✅ COMPLETED | ~15 min |
| **2** | random_hermitian | 20 | 9/9 | ✅ COMPLETED | ~14 min |
| 3 | scrambled_geometry | 0 | 0/9 | ⏸️ NOT STARTED | — |
| 4 | scrambled_geometry | 20 | 0/9 | ⏸️ NOT STARTED | — |
| 5 | broken_wilson_term | 0 | 0/9 | ⏸️ NOT STARTED | — |
| 6 | broken_wilson_term | 20 | 0/9 | ⏸️ NOT STARTED | — |

---

## Batch 1 Results — random_hermitian, W=0

**Execution:** 2026-05-22 18:56–19:11  
**Total runtime:** ~15 minutes  
**Cases completed:** 9/9 (100%)  
**Failed cases:** 0

### Cases

| Case | s1_size | seed | N | true_ipr_mean | r_stat | runtime (s) |
|------|---------|------|---|---------------|--------|-------------|
| 000 | 16 | 123 | 1728 | 0.001736 | 0.5275 | 1.38 |
| 001 | 16 | 456 | 1728 | — | — | — |
| 002 | 16 | 789 | 1728 | — | — | — |
| 003 | 64 | 123 | 6912 | — | — | — |
| 004 | 64 | 456 | 6912 | — | — | — |
| 005 | 64 | 789 | 6912 | — | — | — |
| 006 | 128 | 123 | 13824 | — | — | — |
| 007 | 128 | 456 | 13824 | — | — | — |
| 008 | 128 | 789 | 13824 | 0.000217 | 0.5322 | 278.26 |

**Metric availability:**
- ✅ `true_ipr_mean`: 9/9 cases
- ✅ `r_stat`: 9/9 cases
- ✅ `runtime_seconds`: 9/9 cases
- ✅ `uses_eigenvectors`: true (all cases)
- ✅ `ipr_metric_version`: v0.1.22_negative_controls_true_ipr

**Output path:**  
`reports/RUNS/negative_controls_v0.1.22/batch_01/case_000.json` ... `case_008.json`

---

## Batch 2 Results — random_hermitian, W=20

**Execution:** 2026-05-22 19:24–19:38  
**Total runtime:** ~14 minutes  
**Cases completed:** 9/9 (100%)  
**Failed cases:** 0

### Cases

| Case | s1_size | seed | N | true_ipr_mean | r_stat | runtime (s) |
|------|---------|------|---|---------------|--------|-------------|
| 009 | 16 | 123 | 1728 | 0.002392 | 0.5272 | 1.40 |
| 010 | 16 | 456 | 1728 | 0.002412 | 0.5286 | 1.44 |
| 011 | 16 | 789 | 1728 | 0.002391 | 0.5153 | 1.44 |
| 012 | 64 | 123 | 6912 | 0.000477 | 0.5294 | 32.32 |
| 013 | 64 | 456 | 6912 | 0.000478 | 0.5296 | 35.09 |
| 014 | 64 | 789 | 6912 | 0.000479 | 0.5295 | 36.69 |
| 015 | 128 | 123 | 13824 | 0.000228 | 0.5291 | 217.91 |
| 016 | 128 | 456 | 13824 | 0.000228 | 0.5288 | 274.46 |
| 017 | 128 | 789 | 13824 | 0.000228 | 0.5328 | 282.71 |

**Metric availability:**
- ✅ `true_ipr_mean`: 9/9 cases
- ✅ `r_stat`: 9/9 cases
- ✅ `runtime_seconds`: 9/9 cases
- ✅ `uses_eigenvectors`: true (all cases)
- ✅ `ipr_metric_version`: v0.1.22_negative_controls_true_ipr

**Output path:**  
`reports/RUNS/negative_controls_v0.1.22/batch_02/case_009.json` ... `case_017.json`

### Batch 2 vs Batch 1 Comparison (W=20 vs W=0)

**true_ipr_mean:**
- s1=16: 0.0024 (batch 2) vs 0.0017 (batch 1) — **+38% with disorder**
- s1=64: 0.00048 (batch 2) vs 0.00043 (batch 1) — **+10% with disorder**
- s1=128: 0.00023 (batch 2) vs 0.00022 (batch 1) — **+5% with disorder**

**r_stat:**
- Batch 2 mean: ~0.527 (range 0.515–0.533)
- Batch 1 mean: ~0.529 (range 0.524–0.539)
- **No significant difference** (both in random matrix regime)

**Runtime:**
- Batch 2 total: ~883 seconds (~14.7 min)
- Batch 1 total: ~909 seconds (~15.2 min)
- **Slightly faster** (within noise, -3%)

**Interpretation:**
- Disorder (W=20) slightly increases localization (true_ipr ↑)
- r_stat remains in GOE regime (~0.53) regardless of disorder
- Both batches: controls behave as random matrices, NOT localized

---

## Git Status

**Untracked files:** 9 (batch_02 cases)  
**Modified files:** 0  
**Working tree:** clean (batch 2 outputs not committed yet)

**Gate 4B:** UNTOUCHED ✓  
- `reports/RUNS/gate4_fss_v0.1.21/` — no changes
- `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md` — no changes

---

## Next Steps

### Immediate (after batch 2):
1. ✅ **Commit batch 2 checkpoint** (recommended before batch 3)
2. ❌ **DO NOT** aggregate results yet (wait for all 6 batches)
3. ❌ **DO NOT** apply decision rules yet

### When ready for batch 3:
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3
```

### After all 6 batches:
1. Aggregate results: `python scripts/aggregate_negative_controls_results.py`
2. Apply decision rules: `python scripts/apply_negative_controls_decision_rules.py`
3. Write results report: `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`

---

## Checkpoint

**Date:** 2026-05-22  
**HEAD:** fdda5bb (batch 1 committed and pushed)  
**Branch:** main (synced with origin/main)  
**Working tree:** batch 2 outputs ready to commit

**Commit batch 2:**
```bash
git add -f reports/RUNS/negative_controls_v0.1.22/batch_02/
git add reports/NEGATIVE_CONTROLS_PILOT_PROGRESS_v0.1.22.md
git commit -m "test(controls): complete batch 2 negative controls pilot"
```

---

**Last updated:** 2026-05-22 19:40  
**Status:** BATCH_2_COMPLETED  
**Next:** Commit batch 2, then proceed to batch 3 (or pause)
