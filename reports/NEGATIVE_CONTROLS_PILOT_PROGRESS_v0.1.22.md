# Negative Controls Pilot Progress — v0.1.22

**Protocol:** Falsification-first specificity test  
**Expected:** Controls should FAIL to reproduce Gate 4B PASS pattern  
**Danger:** False-pass if ANY control shows Gate 4B-like robustness

---

## Execution Status

**Total Plan:** 54 cases, 6 batches  
**Completed:** 9 cases, 1 batch (16.7%)  
**Status:** BATCH_1_COMPLETED

| Batch | Control | W | Cases | Status | Runtime |
|-------|---------|---|-------|--------|---------|
| **1** | random_hermitian | 0 | 9/9 | ✅ COMPLETED | ~15 min |
| 2 | random_hermitian | 20 | 0/9 | ⏸️ NOT STARTED | — |
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

## Git Status

**Modified files:** 1  
- `reports/RUNS/negative_controls_v0.1.22/batch_01/case_000.json` (overwritten from smoke test)

**Gate 4B:** UNTOUCHED ✓  
- `reports/RUNS/gate4_fss_v0.1.21/` — no changes
- `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md` — no changes

---

## Next Steps

### Immediate (before batch 2):
1. ❌ **DO NOT** aggregate results yet (wait for all 6 batches)
2. ❌ **DO NOT** apply decision rules yet
3. ⏸️ **PAUSE** — review batch 1 outputs before proceeding

### When ready for batch 2:
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 2
```

### After all 6 batches:
1. Aggregate results: `python scripts/aggregate_negative_controls_results.py`
2. Apply decision rules: `python scripts/apply_negative_controls_decision_rules.py`
3. Write results report: `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`

---

## Checkpoint

**Date:** 2026-05-22  
**HEAD:** 1bcabed (smoke test committed)  
**Branch:** main (synced with origin/main)  
**Working tree:** 1 file modified (case_000.json)

**Rollback:**
```bash
git checkout -- reports/RUNS/negative_controls_v0.1.22/batch_01/case_000.json
```

---

**Last updated:** 2026-05-22 19:15  
**Status:** BATCH_1_COMPLETED  
**Next:** Review batch 1, then proceed to batch 2 (or pause)
