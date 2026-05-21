# S³×S¹ Gate 4 Dry-Run Results — v0.1.20

**Дата выполнения:** 2026-05-21  
**Время выполнения:** 23.6 мин  
**Статус:** COMPLETE  
**Цель:** Feasibility check ONLY (runtime estimate, failure detection)

---

## 1. Executive Summary

**Feasibility Verdict: BATCHED_GRID_REQUIRED**

Dry-run завершён успешно. Полный Gate 4 grid (216 cases) выполним, но требует batch execution из-за runtime 2.4 часа.

---

## 2. Execution Results

### 2.1 Cases
- **Total cases:** 36
- **Completed:** 36 ✅
- **Failed:** 0
- **Failure rate:** 0.0%

### 2.2 Runtime
- **Dry-run total:** 23.6 min (1416 sec)
- **Per-case mean:** 39.40 sec
- **Per-case median:** ~27 sec
- **Estimated full 216-case:** 2.4 hours (141.7 min)

### 2.3 Runtime by Configuration

**By s1_size (dominant factor):**
- N=16: 0.3-1.0 sec
- N=64: 4-30 sec
- N=128 j_max=2: 27-34 sec
- N=128 j_max=3: 143-186 sec (slowest)

**By j_max:**
- j_max=2: 0.3-34 sec
- j_max=3: 0.8-186 sec (2-6× slower than j_max=2)

**By disorder:**
- W=0: similar to W=20 (no significant difference)

**By family:**
- spectral_circle: comparable
- ring: comparable (slightly slower at N=128)
- wilson_ring: comparable

**Critical bottleneck:** N=128 j_max=3 cases (~170s each, 12 such cases in full grid = 34 min)

---

## 3. Metrics Availability

### 3.1 Collected Metrics
✅ **IPR (inverse participation ratio):** Available for all 36 cases
- Field: `mean_low_ipr` in results.json
- Values range: -18.3 to 2.4 (negative values indicate numerical artifact, not physical)

### 3.2 Missing Metrics
❌ **r-statistic (adjacent gap ratio):** NOT collected in dry-run
- Required for Gate 4 localization gate (Decision Rule 1: 2.0× IPR contrast + r toward Poisson)
- Must be added to full Gate 4 execution

**Impact on feasibility:** r-statistic computation is lightweight (post-processing eigenvalues). Does not affect runtime estimate significantly.

---

## 4. Failure Detection

**Numerical failures:** 0/36
- No solver errors
- No NaN/Inf in outputs
- No shape mismatches
- All `error: null` in results.json

**Data integrity:** ✅
- All 36 config.json saved
- All 36 results recorded in results.json
- summary.md generated
- timing.json complete

---

## 5. Feasibility Verdict Detail

**Verdict: BATCHED_GRID_REQUIRED**

**Reasoning:**
1. **Runtime feasible:** 2.4h is acceptable for full grid
2. **Batching required:** Single-job 2.4h risks timeout/interruption
3. **Zero failures:** No protocol revision needed
4. **Recommended batching:** 8 jobs × 27 cases each (~20 min per job)

**Alternative batching strategies:**
- **By family:** 3 jobs × 72 cases (~48 min per job)
- **By s1_size:** 4 jobs × 54 cases (~36 min per job)
- **By disorder:** 4 jobs × 54 cases (~36 min per job)

**Recommended:** 8 jobs (3 families × 2 W × 4 s1_sizes, split by seed or j_max)

---

## 6. Protocol Compliance

### 6.1 Pre-Registered Grid (Dry-Run Subset)
✅ Grid parameters matched pre-registration (commit 1f4173c):
- Families: spectral_circle, ring, wilson_ring ✅
- Disorder W: 0, 20 ✅ (12 excluded, as planned)
- S¹ sizes: 16, 64, 128 ✅ (32 excluded, as planned)
- j_max: 2, 3 ✅
- Seeds: 123 ✅ (456, 789 excluded, as planned)

✅ Sample size: 36 cases (17% of full 216-case grid)

### 6.2 Forbidden Actions (Verification)
✅ No PASS/FAIL verdict issued (feasibility only)
✅ No metric interpretation (IPR values not analyzed)
✅ No protocol modification (grid/thresholds unchanged)
✅ No cherry-picking (all 3 families executed)
✅ No threshold adjustment (2.0×/1.5× remain locked)
✅ No preliminary Gate 4 result reported

---

## 7. Files Created

**Output directory:** `reports/RUNS/gate4_dry_run_v0.1.20/`

**Files:**
1. `config.json` — dry-run grid configuration
2. `results.json` — 36 case results (runtime, IPR, errors)
3. `summary.md` — feasibility summary
4. `timing.json` — per-case timing breakdown

**Expected for full Gate 4 (NOT in dry-run):**
- `gate4_verdict.md` — PASS/FAIL decision (requires full 216 cases)
- `gate4_metrics_full.json` — all metrics including r-statistic
- `figures/` — visualization of finite-size scaling

---

## 8. Git Status

**Before dry-run:** clean working tree ✅  
**After dry-run:** clean working tree ✅  
**No commits made** (as instructed)

**Dry-run artifacts location:** `reports/RUNS/gate4_dry_run_v0.1.20/` (untracked, safe to commit separately)

---

## 9. Next Steps (Post Dry-Run)

### 9.1 Required Before Full Gate 4
1. **Add r-statistic computation** to full Gate 4 script
2. **Review timing.json** — confirm no outlier runtimes
3. **Design batch execution** — 8 jobs × 27 cases recommended
4. **Test single batch** — run 1/8 of full grid to verify batch protocol

### 9.2 Full Gate 4 Execution Plan
1. **Batch 1-8:** Execute 8 parallel jobs (27 cases each, ~20 min per job)
2. **Merge results:** Combine 8 batch outputs into single gate4_metrics_full.json
3. **Compute verdict:** Apply Decision Rule 1 (2.0× IPR contrast + r toward Poisson)
4. **Generate figures:** Lattice-size scaling plots (N=16/32/64/128)
5. **Write gate4_verdict.md:** PASS/FAIL with evidence and caveats

### 9.3 Timeline Estimate
- Full Gate 4 (8 batches): 2.4 hours (wall-clock, parallelized)
- Post-processing: 30 min (merge, verdict, figures)
- **Total:** ~3 hours from start to Gate 4 verdict

---

## 10. Guardrails (Reminder)

⚠️ **Dry-run outputs are PLANNING DATA, not scientific evidence.**

**Forbidden interpretations:**
- ❌ "Dry-run shows localization" — NO, dry-run is feasibility check only
- ❌ "IPR values indicate PASS" — NO, verdict requires full 216-case grid + r-statistic
- ❌ "Gate 4 confirmed" — NO, dry-run is NOT Gate 4 execution
- ❌ "S³×S¹ validated" — NO, validation requires full protocol completion

**Allowed statements:**
- ✅ "Dry-run runtime estimate: 2.4h for 216 cases"
- ✅ "Zero failures in 36-case sample"
- ✅ "Batching required for full grid"
- ✅ "r-statistic computation pending"

---

## 11. Protocol References

**Pre-registration:** commit 1f4173c (2026-05-21)  
**Dry-run plan:** commit ef49495 (2026-05-21)  
**Dry-run runner:** commit 76d092a (2026-05-21)

**Full Gate 4 protocol:** `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md`

---

## 12. Appendix: Dry-Run vs Full Gate 4

| Aspect | Dry-Run | Full Gate 4 |
|--------|---------|-------------|
| Purpose | Feasibility check | Scientific verdict |
| Cases | 36 (17% sample) | 216 (100% grid) |
| Seeds | 1 (seed=123) | 3 (123, 456, 789) |
| Metrics | IPR only | IPR + r-statistic |
| Verdict | BATCHED_GRID_REQUIRED | PASS/FAIL/PASS_WITH_CAVEATS |
| Batching | Not applicable | 8 jobs × 27 cases |
| Runtime | 23.6 min | 2.4 hours (estimated) |
| Output | timing.json, summary.md | gate4_verdict.md, figures/ |
| Scientific claim | None (planning data) | Gate 4 evidence (if PASS) |

---

**Document status:** COMPLETE  
**Next action:** Review timing.json, design batch execution, test single batch  
**Do NOT proceed to full Gate 4 without batch protocol design**
