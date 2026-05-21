# S³×S¹ Gate 4 Batch Execution Protocol — v0.1.20

**Дата:** 2026-05-21  
**Статус:** IMPLEMENTATION PROTOCOL (does NOT modify pre-registered experimental design)  
**Цель:** Safe batched execution of locked 216-case Gate 4 grid  
**Locked protocol:** commit 1f4173c (S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md)  
**Dry-run results:** commit 52d221f (S3_S1_GATE4_DRY_RUN_RESULTS_v0.1.20.md)

---

## 1. Purpose

This document specifies the **execution infrastructure** for the pre-registered Gate 4 protocol. It does **NOT** change the experimental design, grid parameters, thresholds, or decision rules.

**What this protocol defines:**
- How 216 cases are split into 8 deterministic batches
- Resume/retry policy for interrupted execution
- Failure handling and merge policy
- Output file structure
- Pre-run environment checklist

**What this protocol does NOT change:**
- Grid parameters (families, W, sizes, j_max, seeds) — locked in 1f4173c
- Decision rules (2.0× IPR contrast, 1.5× lower bound) — locked in 1f4173c
- Metric definitions — locked in 1f4173c
- Allowed/forbidden claims — locked in 1f4173c

**Reason for batching:** Dry-run (commit 52d221f) estimated 2.4h full runtime. Single-job execution risks timeout/interruption. Batching improves robustness without changing scientific protocol.

---

## 2. Full Grid Specification (From Locked Pre-Registration)

**Source:** commit 1f4173c, Section 5.1

**Grid parameters:**
```python
families = ["spectral_circle", "ring", "wilson_ring"]  # 3
disorder_W = [0, 12, 20]  # 3
s1_sizes = [16, 32, 64, 128]  # 4
j_max_values = [2, 3]  # 2
seeds = [123, 456, 789]  # 3
```

**Total cases:** 3 × 3 × 4 × 2 × 3 = **216**

**Fixed parameters (all cases):**
- alpha = 0.0 (S¹ flux, PBC)
- mode = "geometric_weight" (disorder mode)
- radius = 1.0 (manifold radius)

---

## 3. Deterministic Batch Split

**Batching strategy:** Split by (family, disorder_W)

**Batch structure:**
```
Batch 1: spectral_circle, W=0   → 4 sizes × 2 j_max × 3 seeds = 24 cases
Batch 2: spectral_circle, W=12  → 24 cases
Batch 3: spectral_circle, W=20  → 24 cases
Batch 4: ring, W=0              → 24 cases
Batch 5: ring, W=12             → 24 cases
Batch 6: ring, W=20             → 24 cases
Batch 7: wilson_ring, W=0       → 24 cases
Batch 8: wilson_ring, W=12      → 24 cases
Batch 9: wilson_ring, W=20      → 24 cases
```

**Total:** 9 batches × 24 cases = 216 ✅

**Verification:**
- Coverage: All 216 cases covered exactly once ✅
- No overlap: Each case appears in exactly one batch ✅
- Deterministic: Batch assignment fully determined by (family, W) ✅

**Batch ordering:** Batches numbered 1-9 in the order above. Execution order does NOT affect results (all batches independent).

**Estimated runtime per batch:** 2.4h ÷ 9 ≈ 16 min (based on dry-run)

---

## 4. Output File Structure

**Base directory:** `reports/RUNS/gate4_fss_v0.1.20/`

**Directory structure:**
```
gate4_fss_v0.1.20/
├── config.json                      # Full grid configuration
├── batches/
│   ├── batch_01/
│   │   ├── batch_config.json        # Batch-specific grid subset
│   │   ├── results.json             # 24 case results
│   │   ├── timing.json              # Per-case timing
│   │   ├── summary.md               # Batch execution summary
│   │   └── status.json              # started/completed/failed/interrupted
│   ├── batch_02/
│   │   └── ...
│   └── batch_09/
│       └── ...
└── merged/
    ├── metrics.json                 # All 216 cases merged
    ├── timing_summary.json          # Aggregate timing stats
    ├── failure_summary.json         # Failed cases (if any)
    ├── coverage.json                # Grid coverage verification
    └── gate4_verdict.md             # PASS/FAIL decision (after all batches complete)
```

**File semantics:**
- `batch_config.json`: Stores (family, W, sizes, j_max, seeds) for this batch
- `results.json`: Array of 24 case results with (IPR, r-statistic, runtime, error)
- `timing.json`: Per-case timing breakdown
- `summary.md`: Human-readable batch summary
- `status.json`: Execution state (for resume logic)

**Merge policy:** `merged/` created ONLY after all 9 batches complete successfully.

---

## 5. Resume and Failure Handling

### 5.1 Resume Policy

**Scenario:** Batch execution interrupted (BSOD, timeout, manual stop)

**Resume behavior:**
1. Check `status.json` in batch directory
2. If `status == "completed"` → skip batch
3. If `status == "interrupted"` or missing → re-run batch from start
4. DO NOT skip individual cases within a batch (batch is atomic unit)

**Reason for batch-level resume (not case-level):**
- Simplifies state management
- Avoids partial-batch merge complexity
- Batch runtime (~16 min) is short enough to re-run safely

**Resume command:**
```bash
python scripts/run_gate4_batched.py --resume
```

### 5.2 Failure Handling

**Case failure:** Single case within batch fails (solver error, NaN, exception)

**Behavior:**
1. Record error in `results.json` for that case
2. Continue executing remaining cases in batch
3. At batch end: write `status == "completed_with_failures"`
4. DO NOT treat batch as fully successful

**Batch failure:** Multiple failures or critical error

**Behavior:**
1. Write `status == "failed"`
2. Record failure details in `batch_X/summary.md`
3. Stop batch execution
4. User decides: retry with --force or investigate

**Merge policy with failures:**
- If ANY batch has `status != "completed"` → merge BLOCKED
- `merged/gate4_verdict.md` cannot be generated
- Partial results NOT treated as confirmatory evidence

**Forbidden action:** Claiming PASS based on subset of successful batches

---

## 6. No Partial PASS Rule (Critical)

**Rule:** Gate 4 verdict requires ALL 216 cases to complete successfully.

**Forbidden:**
- ❌ "8/9 batches passed → Gate 4 PASS"
- ❌ "Family X passed → Gate 4 PASS for family X"
- ❌ "192/216 cases passed → Gate 4 likely PASS"

**Allowed:**
- ✅ "216/216 cases completed → proceed to verdict"
- ✅ "8/9 batches completed → Gate 4 incomplete, cannot issue verdict"
- ✅ "Batch 3 failed → re-run batch 3 before merge"

**If <216 cases available:** Gate 4 status = INCOMPLETE, no scientific verdict issued.

---

## 7. Merge Protocol

**Trigger:** All 9 batches have `status == "completed"`

**Merge process:**
1. Load all 9 `results.json` files
2. Concatenate into single array (216 elements)
3. Verify coverage: each (family, W, size, j_max, seed) appears exactly once
4. Compute aggregate statistics (mean IPR by W, r-statistic distribution)
5. Write `merged/metrics.json`
6. Generate `merged/coverage.json` (verification report)
7. Check Decision Rule 1 (2.0× IPR contrast + r toward Poisson)
8. Write `merged/gate4_verdict.md` with PASS/FAIL/PASS_WITH_CAVEATS

**Coverage verification (critical):**
```python
# Pseudocode
all_cases = load_all_batch_results()
expected_grid = generate_full_216_grid()
assert len(all_cases) == 216
assert set(all_cases) == set(expected_grid)  # No duplicates, no gaps
```

**If coverage check fails:** STOP, do not issue verdict, report missing/duplicate cases.

---

## 8. Pre-Run Checklist (Thermal and Environment)

**Purpose:** Ensure execution environment stability (NOT a scientific validity check)

**Checklist (run BEFORE starting batches):**
1. ✅ MSI Center cooling profile active (Extreme Performance / Cooler Boost)
2. ✅ System temperature acceptable under load (check sensors)
3. ✅ Power plugged in (not battery)
4. ✅ Sleep/hibernation disabled
5. ✅ Close unnecessary heavy applications
6. ✅ Confirm git status clean (no uncommitted changes)
7. ✅ Confirm pre-registration commit 1f4173c accessible

**Thermal note:**
- Dry-run completed without BSOD under current cooling profile
- Thermal stability appears improved (context: prior BSOD issues during development)
- Full Gate 4 execution requires same thermal environment

**Forbidden interpretation:**
- ❌ "Thermal fix proves numerical stability" — thermal is execution context, not physics evidence
- ❌ "Dry-run proves Gate 4 will pass" — dry-run is feasibility only

**Allowed statement:**
- ✅ "Thermal checklist completed, proceeding with batch execution"

**If BSOD/interruption occurs during batch:**
1. Check thermal sensors, ensure cooling profile active
2. Use `--resume` to continue from last incomplete batch
3. If repeated failures: investigate thermal/hardware issue before continuing

**Checklist location:** `reports/GATE4_PRERUN_THERMAL_CHECKLIST_v0.1.20.md`

---

## 9. Execution Commands

### Print plan (verify batch split without execution)
```bash
python scripts/run_gate4_batched.py --print-plan
```

**Expected output:**
- Total: 216 cases
- Batches: 9
- Per-batch: 24 cases
- Coverage: 100% (no gaps, no duplicates)

### Run single batch
```bash
python scripts/run_gate4_batched.py --batch-id 1
```

**Runtime:** ~16 min (estimated)

### Run all batches sequentially
```bash
python scripts/run_gate4_batched.py --run-all
```

**Runtime:** ~2.4h (estimated, based on dry-run)

**⚠️ Warning:** Use `--run-all` ONLY after verifying:
1. Pre-run thermal checklist completed
2. Git status clean
3. --print-plan output verified

### Resume after interruption
```bash
python scripts/run_gate4_batched.py --resume
```

**Behavior:** Skip completed batches, re-run interrupted/failed batches

### Force re-run (overwrite existing batch)
```bash
python scripts/run_gate4_batched.py --batch-id 3 --force
```

**Use case:** Re-run specific batch after fixing issue, intentionally overwrite previous results

---

## 10. Timeline Estimate

**Sequential execution (single machine):**
- 9 batches × 16 min/batch = 144 min = 2.4h
- Post-processing (merge, verdict) = 15 min
- **Total:** ~2.6h from start to Gate 4 verdict

**Parallel execution (if multiple machines available):**
- 9 batches in parallel = 16 min
- Post-processing = 15 min
- **Total:** ~31 min from start to Gate 4 verdict

**Recommended:** Sequential execution (simpler, no distributed coordination overhead)

---

## 11. Protocol Compliance Verification

### 11.1 Before Batch Execution
- [ ] Locked pre-registration accessible (commit 1f4173c)
- [ ] Batch grid verified: 9 batches × 24 cases = 216
- [ ] Coverage check passed: no gaps, no duplicates
- [ ] Thermal checklist completed
- [ ] Git status clean

### 11.2 During Batch Execution
- [ ] No grid parameter changes
- [ ] No threshold adjustments
- [ ] No cherry-picking (all batches executed)
- [ ] Failures recorded (not silently skipped)

### 11.3 After All Batches Complete
- [ ] All 9 batches `status == "completed"`
- [ ] Coverage verification passed (216 cases present)
- [ ] r-statistic available for all cases
- [ ] Decision Rule 1 applied (2.0× IPR contrast + r toward Poisson)
- [ ] Verdict issued: PASS / FAIL / PASS_WITH_CAVEATS

### 11.4 Forbidden Actions (Verification)
- [ ] No partial PASS based on <216 cases
- [ ] No preliminary verdict before all batches complete
- [ ] No forbidden claims ("S³×S¹ validated", "FL generalized", etc.)
- [ ] No protocol modification during execution

---

## 12. Protocol Status

**Status:** IMPLEMENTATION PROTOCOL  
**Scientific protocol:** LOCKED (commit 1f4173c)  
**Experimental design:** UNCHANGED  
**Batching rationale:** Runtime 2.4h requires safe execution strategy

**This protocol is NOT a protocol revision.** It implements the locked Gate 4 pre-registration using batch execution for robustness.

**If any batch execution detail needs revision:**
- Update this document (batch split, resume policy, etc.)
- Do NOT update pre-registration (that remains locked)
- Document changes in `GATE4_INFRASTRUCTURE_REVIEW_v0.1.20.md`

---

## 13. References

**Pre-registration:** commit 1f4173c (2026-05-21)  
**Dry-run plan:** commit ef49495 (2026-05-21)  
**Dry-run runner:** commit 76d092a (2026-05-21)  
**Dry-run results:** commit 52d221f (2026-05-21)

**Full protocol:** `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md`  
**Thermal checklist:** `reports/GATE4_PRERUN_THERMAL_CHECKLIST_v0.1.20.md` (to be created)  
**Infrastructure review:** `reports/GATE4_INFRASTRUCTURE_REVIEW_v0.1.20.md` (to be created)

---

**Document created:** 2026-05-21  
**Next action:** Implement batch runner script (`scripts/run_gate4_batched.py`)  
**Do NOT execute full Gate 4 until batch infrastructure verified**
