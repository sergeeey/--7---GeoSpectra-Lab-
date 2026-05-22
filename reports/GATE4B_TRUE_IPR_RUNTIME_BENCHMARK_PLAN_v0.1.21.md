# Gate 4B True IPR Runtime Benchmark Plan — v0.1.21

**Date:** 2026-05-22 12:00 Almaty  
**Purpose:** Measure true eigenvector-based IPR runtime overhead before Gate 4B full rerun  
**Status:** BENCHMARK PLAN (not scientific protocol)

---

## 1. Scope and Non-Goals

**What this benchmark IS:**
- ✅ Runtime feasibility check for v0.1.21 metric-corrected implementation
- ✅ Overhead measurement: `eigh` vs `eigvalsh` path
- ✅ Decision input: full grid feasible? batching required? pilot first?

**What this benchmark IS NOT:**
- ❌ Scientific evidence or validation
- ❌ PASS/FAIL verdict
- ❌ Protocol test (protocol is LOCKED)
- ❌ Grid exploration
- ❌ Threshold tuning
- ❌ Metric validation (already done via unit tests)

**Results used for:**
- Extrapolate 216-case runtime estimate
- Decide execution mode: full grid / batched / pilot-first
- Confirm no catastrophic failures at typical sizes

---

## 2. Benchmark Cases (3 total)

**Rationale:** Cover size range (N=16 to N=128) and family diversity.

### Case 1: Small (baseline)
```yaml
family: spectral_circle
disorder_W: 0
s1_size: 16
j_max: 2
seed: 123
Expected N: ~464 (16 × 29 j_max=2)
Purpose: Minimum overhead measurement
```

### Case 2: Medium (Gate 3C size)
```yaml
family: ring
disorder_W: 12
s1_size: 64
j_max: 3
seed: 123
Expected N: ~2432 (64 × 38 j_max=3)
Purpose: Typical case, comparable to Gate 3C
```

### Case 3: Worst-case-like (largest)
```yaml
family: wilson_ring
disorder_W: 20
s1_size: 128
j_max: 3
seed: 123
Expected N: ~3712 (128 × 29 j_max=3)
Purpose: Upper bound overhead, largest N in grid
```

**Total runtime budget:** <30 minutes (for 3 cases)

---

## 3. Measurements

**Per case:**
- `runtime_sec` — wall-clock time (primary metric)
- `matrix_size` — Hilbert space dimension N
- `true_ipr_mean` — verify field present and finite
- `mean_low_eigenvalue` — verify diagnostic field present
- `r_stat` — verify secondary metric computed
- `ipr_metric_version` — confirm "v0.1.21_true_eigenvector_ipr"
- `uses_eigenvectors` — confirm True
- `error` — capture any failures

**Aggregated:**
- Mean runtime per case
- Extrapolated 216-case runtime: `mean_runtime × 216`
- Overhead vs v0.1.20 (if v0.1.20 timing available)

**NOT measured:**
- Memory usage (nice-to-have, not critical)
- CPU utilization
- Disk I/O

---

## 4. Execution Method

**Option A: Dedicated benchmark script (preferred)**
```bash
python scripts/benchmark_gate4b_true_ipr.py
```

**Option B: Single-case execution via run_gate4_batched.py**
```bash
# Manually run 3 cases one by one
python scripts/run_gate4_batched.py --batch-id 1 --limit 1
```

**Output location:**
```
reports/RUNS/gate4b_true_ipr_benchmark_v0.1.21/
  benchmark_config.json
  benchmark_results.json
  case_001_small.json
  case_002_medium.json
  case_003_worst_case.json
```

**No writes to:**
- `reports/RUNS/gate4_fss_v0.1.20/` (old v0.1.20 outputs)
- `reports/RUNS/gate4_fss_v0.1.21/` (reserved for full 216-case rerun)

---

## 5. Success Criteria

**Benchmark succeeds if:**
- ✅ 3/3 cases complete without error
- ✅ All output fields present (`true_ipr_mean`, `uses_eigenvectors`, etc.)
- ✅ Runtime per case < 15 minutes (worst-case N=3712)
- ✅ Extrapolated 216-case runtime computable

**Benchmark fails if:**
- ❌ Any case errors (numerical instability, OOM, timeout)
- ❌ Missing output fields
- ❌ Runtime per case > 30 minutes (single case taking >30 min → full grid infeasible)

**Failure does NOT invalidate v0.1.21 metric:**
- Unit tests already validated correctness (17/17 passed)
- Benchmark failure = feasibility issue, not correctness issue
- Action on failure: reduce grid (drop s1_size=128) or optimize

---

## 6. Decision Rules (After Benchmark)

### 6.1 FULL_GRID_FEASIBLE
**Condition:** Extrapolated runtime < 18 hours  
**Action:** Execute full 216-case grid via `--run-all`  
**Batching:** Optional (can run overnight unattended)

### 6.2 BATCHED_GRID_REQUIRED
**Condition:** Extrapolated runtime 18-36 hours  
**Action:** Execute 216 cases in 2-3 batches over multiple days  
**Batching:** Required (split by family or disorder_W)

### 6.3 PILOT_REQUIRED_BEFORE_FULL_RERUN
**Condition:** Extrapolated runtime 36-72 hours  
**Action:** Run 72-case pilot first (1 family × full grid)  
**Rationale:** Validate metric + overhead before committing to full 216

### 6.4 GRID_REDUCTION_REQUIRED
**Condition:** Extrapolated runtime > 72 hours  
**Action:** Drop s1_size=128 from grid (reduces to 162 cases)  
**Protocol impact:** Document as deviation in results report

### 6.5 BENCHMARK_FAILED
**Condition:** Any case errors, missing fields, or timeout  
**Action:** Debug + rerun benchmark OR escalate to optimization

---

## 7. Comparison with v0.1.20 (If Available)

**v0.1.20 actual runtime:** 96.1 minutes (216 cases)  
**Per-case mean:** 96.1 / 216 ≈ 0.445 minutes ≈ 27 seconds

**Overhead factor calculation:**
```
overhead_factor = runtime_v0.1.21 / runtime_v0.1.20_comparable_case
```

**Expected overhead range:**
- Theoretical: 5-15× (eigenvector computation adds O(N³) vs O(N²))
- Practical: Depends on BLAS/LAPACK implementation, N size

**Note:** v0.1.20 runtime includes mixed sizes (16-128), so direct comparison requires size-matched case.

---

## 8. Protocol Compliance

**Grid parameters:** UNCHANGED (benchmark uses 3 cases from locked 216-case grid)

**Thresholds:** UNCHANGED (benchmark does NOT test PASS criteria)

**Claim language:** UNCHANGED (no scientific claims from benchmark)

**Metric implementation:** UNCHANGED (v0.1.21 already committed and tested)

**Benchmark is feasibility check, not protocol modification.**

---

## 9. Output Artifacts

**Required files:**
1. `reports/RUNS/gate4b_true_ipr_benchmark_v0.1.21/benchmark_config.json`
   - 3 case definitions
   - Execution timestamp
   - Version markers

2. `reports/RUNS/gate4b_true_ipr_benchmark_v0.1.21/benchmark_results.json`
   - Per-case runtime
   - Aggregated statistics
   - Extrapolated 216-case estimate
   - Decision recommendation

3. `reports/RUNS/gate4b_true_ipr_benchmark_v0.1.21/case_*.json`
   - Full output per case (same schema as full rerun)

4. `reports/GATE4B_TRUE_IPR_RUNTIME_BENCHMARK_RESULTS_v0.1.21.md`
   - Human-readable summary
   - Runtime table
   - Decision recommendation
   - Caveats

**Optional files:**
- `benchmark_log.txt` — execution log
- `benchmark_plot.png` — runtime vs N scatter plot

---

## 10. Timeline

**Execution:** <30 minutes (3 cases)

**Analysis:** <10 minutes (compute extrapolation, write report)

**Decision:** Immediate (based on decision rules)

**Total:** <1 hour from benchmark start to decision

---

## 11. Caveats

**Benchmark limitations:**

1. **Extrapolation uncertainty:**
   - 3 cases do NOT capture full runtime distribution
   - Size-dependent overhead (N³ scaling) not fully characterized
   - Seed-dependent variation not measured

2. **Not a substitute for pilot:**
   - Benchmark checks feasibility, not scientific validity
   - Pilot (72 cases) provides better runtime + metric validation

3. **Machine-specific:**
   - Runtime depends on CPU, BLAS library, system load
   - Results not transferable to different hardware

4. **No batching overhead:**
   - Benchmark runs sequentially
   - Full rerun batching may add file I/O overhead

**Recommendation:** Treat extrapolated runtime as **lower bound** (optimistic estimate).

Add 20-30% buffer for:
- Larger cases (s1_size=128 cases are 33% of grid)
- File I/O overhead
- Batch startup time

---

## 12. Pre-Execution Checklist

**Before running benchmark:**
- [x] v0.1.21 protocol committed and pushed (5e5ffc9)
- [x] True IPR implementation committed and pushed (ad6936f)
- [x] Unit tests passed: 17/17, 0 warnings
- [x] Dry check passed: 216 cases, 0 duplicates
- [ ] Benchmark script/mode ready
- [ ] Output directory created: `reports/RUNS/gate4b_true_ipr_benchmark_v0.1.21/`
- [ ] System idle (no competing workloads)

**DO NOT execute benchmark if:**
- ❌ Unit tests failing
- ❌ Protocol uncommitted
- ❌ Git working directory not clean
- ❌ System under heavy load

---

## 13. Post-Execution Actions

**If FULL_GRID_FEASIBLE:**
1. Commit benchmark results
2. Execute full 216-case rerun via `--run-all`
3. Scientific analysis after 216 cases complete

**If BATCHED_GRID_REQUIRED:**
1. Commit benchmark results
2. Execute batches 1-9 over 2-3 days
3. Scientific analysis after all batches complete

**If PILOT_REQUIRED:**
1. Commit benchmark results
2. Design 72-case pilot (1 family × full parameter grid)
3. Execute pilot first
4. Decide on full rerun after pilot

**If GRID_REDUCTION_REQUIRED:**
1. Commit benchmark results
2. Create v0.1.21_reduced protocol (drop s1_size=128)
3. Pre-register reduced grid
4. Execute 162-case grid

**If BENCHMARK_FAILED:**
1. Debug failure (check error logs)
2. Fix issue OR optimize implementation
3. Re-run benchmark
4. Do NOT proceed to full rerun until benchmark succeeds

---

**Benchmark plan status:** READY  
**Next step:** Execute 3 benchmark cases  
**Expected duration:** <30 minutes  
**Decision output:** Execution mode recommendation for 216-case rerun
