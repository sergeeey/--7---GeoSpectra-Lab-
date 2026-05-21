# S³×S¹ Gate 4 FSS — Raw Execution Freeze Report

**Version:** v0.1.20  
**Execution Completed:** 2026-05-22 00:31 UTC  
**Protocol Commit:** 1f4173c (locked, pre-registered)  
**Status:** EXECUTION_COMPLETE

---

## Purpose

This report **freezes the raw execution outputs** of Gate 4 Finite-Size Scaling (FSS) batched grid execution for S³×S¹ geometry validation **before scientific interpretation**.

**CRITICAL DISTINCTION:**
- ✅ Execution completion is confirmed
- ❌ Execution completion is **NOT** itself a Gate 4 PASS verdict
- Scientific interpretation and verdict determination follow in separate analysis phase

---

## Execution Summary

### Batches Completed

| Batch | Family | W | Cases | Failures | r-stat unavailable | Runtime (min) | Status |
|-------|--------|---|-------|----------|-------------------|---------------|--------|
| 01 | spectral_circle | 0 | 24 | 0 | 0 | 10.9 | ✅ completed |
| 02 | spectral_circle | 12 | 24 | 0 | 0 | 10.7 | ✅ completed |
| 03 | spectral_circle | 20 | 24 | 0 | 0 | 10.4 | ✅ completed |
| 04 | ring | 0 | 24 | 0 | 0 | 11.3 | ✅ completed |
| 05 | ring | 12 | 24 | 0 | 0 | 11.3 | ✅ completed |
| 06 | ring | 20 | 24 | 0 | 0 | 10.3 | ✅ completed |
| 07 | wilson_ring | 0 | 24 | 0 | 0 | 10.4 | ✅ completed |
| 08 | wilson_ring | 12 | 24 | 0 | 0 | 10.5 | ✅ completed |
| 09 | wilson_ring | 20 | 24 | 0 | 0 | 10.3 | ✅ completed |

**Totals:**
- **Batches:** 9/9 completed
- **Cases:** 216/216 completed
- **Failures:** 0/216 (0%)
- **r-statistic availability:** 216/216 (100%)
- **Total runtime:** 96.1 minutes

---

## Grid Coverage Verification

### Parameter Space

**Full factorial grid:**
- **Families:** spectral_circle, ring, wilson_ring (3)
- **Disorder strengths (W):** 0, 12, 20 (3)
- **S¹ sizes (s1_size):** 16, 32, 64, 128 (4)
- **Maximum angular momenta (j_max):** 2, 3 (2)
- **Random seeds:** 123, 456, 789 (3)

**Expected total:** 3 × 3 × 4 × 2 × 3 = 216 cases

### Coverage Status

✅ **216/216 unique cases executed**
- Case ID range: 0–215 (continuous, no gaps)
- No missing combinations
- No duplicate case_id values
- All parameter combinations covered

---

## Output Directory Structure

```
reports/RUNS/gate4_fss_v0.1.20/
├── batches/
│   ├── batch_01/  (spectral_circle W=0)
│   │   ├── batch_config.json
│   │   ├── results.json      [24 cases]
│   │   ├── status.json
│   │   ├── summary.md
│   │   └── timing.json
│   ├── batch_02/  (spectral_circle W=12)
│   ├── batch_03/  (spectral_circle W=20)
│   ├── batch_04/  (ring W=0)
│   ├── batch_05/  (ring W=12)
│   ├── batch_06/  (ring W=20)
│   ├── batch_07/  (wilson_ring W=0)
│   ├── batch_08/  (wilson_ring W=12)
│   └── batch_09/  (wilson_ring W=20)
```

Each batch directory contains:
- `batch_config.json` — batch parameters
- `results.json` — 24 case results (case_id, metrics, errors)
- `status.json` — batch completion status
- `summary.md` — human-readable summary
- `timing.json` — per-case timing breakdown

---

## Raw Metrics Summary

### Execution Stability

- **All cases completed without crashes**
- **All r-statistics computed successfully** (no eigenvalue degeneracies reported)
- **Consistent runtime profile across batches** (~10-11 minutes per 24-case batch)

### Data Integrity

- ✅ No null values in critical fields (mean_low_ipr, r_stat)
- ✅ No NaN values reported
- ✅ All case_id values unique and sequential
- ✅ All batches report status="completed"

---

## Execution Timeline

| Event | Timestamp |
|-------|-----------|
| Batch 01 completed | 2026-05-21 20:47 |
| Batch 02 completed | 2026-05-21 21:21 |
| Batch 03 completed | 2026-05-21 21:49 |
| Batch 04 completed | 2026-05-21 22:05 |
| Batch 05 completed | 2026-05-21 22:24 |
| Batch 06 completed | 2026-05-21 23:36 |
| Batch 07 completed | 2026-05-21 23:54 |
| Batch 08 completed | 2026-05-22 00:10 |
| Batch 09 completed | 2026-05-22 00:31 |

**Total wall-clock time:** ~3.7 hours (sequential batch execution)

---

## Freeze Statement

**This report freezes raw execution outputs before scientific interpretation.**

The presence of 216 completed cases with 0 failures confirms:
1. **Technical execution robustness** — code ran without crashes
2. **Grid coverage completeness** — all parameter combinations tested
3. **Metric availability** — all required outputs (IPR, r-statistic) computed

The presence of completed execution does **NOT** confirm:
1. ❌ Gate 4 PASS verdict
2. ❌ S³×S¹ validation
3. ❌ Localization signal robustness
4. ❌ Finite-size scaling behavior
5. ❌ Family consistency

**Scientific interpretation follows in:**
- `reports/S3_S1_GATE4_FSS_RESULTS_v0.1.20.md` (verdict determination)

---

## Locked Protocol Reference

- **Pre-registration document:** `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md`
- **Pre-registration commit:** 1f4173c
- **Batch protocol document:** `docs/gate4_batch_protocol.md`
- **Batch infrastructure commits:** a359097, bd2d600, 80dc509
- **Dry-run feasibility commit:** 52d221f

**No protocol modifications occurred during execution.**

---

## Next Steps (Scientific Analysis Phase)

1. **Merge batch outputs** → `reports/RUNS/gate4_fss_v0.1.20/merged/`
2. **Compute aggregate metrics** (IPR contrast, r-statistic distributions, size trends)
3. **Apply pre-registered decision rules** (from preregistration doc)
4. **Generate Gate 4 verdict** with caveats
5. **Atomic commit** of all results + verdict

**Analysis begins in Step 3.**

---

**Execution freeze timestamp:** 2026-05-22 00:31 UTC  
**Report generated:** 2026-05-22 (post-execution analysis phase)  
**Frozen output directory:** `reports/RUNS/gate4_fss_v0.1.20/batches/`
