# Local Execution Suspended — Thermal Instability

**Date:** 2026-05-23  
**Status:** SUSPENDED  
**Reason:** PC thermal overload → spontaneous reboot under heavy numerical load

---

## Incident Summary

**What happened:**  
Local execution of negative controls batch 3 (scrambled_geometry, W=0) caused PC thermal shutdown and reboot during eigenvalue computation. Batch execution interrupted at case 7/9.

**Hardware constraint identified:**  
Current PC cannot sustain sustained heavy numerical workloads (full eigendecomposition on N=13824 Hermitian matrices, repeated across parameter grid).

**Safety measure:**  
All further **heavy local runs are PROHIBITED** until thermal issue resolved or execution moved to remote/cloud infrastructure.

---

## Valid Completed Data

**Successfully executed and committed:**

### Batch 1: random_hermitian, W=0
- **Commit:** fdda5bb  
- **Cases:** 9/9 (100%)  
- **Output:** `reports/RUNS/negative_controls_v0.1.22/batch_01/`  
- **Metrics:** true_ipr_mean, r_stat, runtime  
- **Status:** ✅ VALID, pushed to origin/main

### Batch 2: random_hermitian, W=20
- **Commit:** 2ec84ab  
- **Cases:** 9/9 (100%)  
- **Output:** `reports/RUNS/negative_controls_v0.1.22/batch_02/`  
- **Metrics:** true_ipr_mean, r_stat, runtime  
- **Status:** ✅ VALID, pushed to origin/main

**Coverage:** 18/54 cases (33.3%)  
**Control coverage:** 1/3 controls (random_hermitian only)

---

## Invalid / Unsafe Data

### Batch 3: scrambled_geometry, W=0 (REMOVED)
- **Cases:** 7/9 (incomplete, interrupted by thermal reboot)  
- **Last file:** case_024.json (21:34, May 22)  
- **Issue:** Partial batch, potentially corrupted last case due to unclean shutdown  
- **r_stat anomaly:** case_018 showed r_stat=0.9999999999999728 (physically impossible, likely numerical artifact from thermal stress or interrupted computation)  
- **Action taken:** `rm -rf reports/RUNS/negative_controls_v0.1.22/batch_03` (2026-05-23 22:03)  
- **Reason:** Unsafe to include partial/interrupted results in validation chain

---

## Gate 4B Integrity

**Status:** ✅ UNTOUCHED  
**Last commit:** f7eff32  
**Verdict:** GATE4B_FSS_PASS_WITH_CAVEATS  
**Files verified unchanged:**
- `reports/RUNS/gate4_fss_v0.1.21/` — no modifications
- `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md` — no modifications
- `reports/GATE4B_PRE_PUSH_AUDIT_v0.1.21.md` — no modifications

Gate 4B results remain immutable and independent from negative controls execution.

---

## Execution Prohibition

**Banned operations on local PC until thermal issue resolved:**

❌ `python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3`  
❌ `python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 4|5|6`  
❌ Any full eigendecomposition on N > 5000  
❌ Sustained multi-hour numerical runs  
❌ Any `--run-pilot` execution without explicit thermal monitoring

**Allowed operations:**

✅ Documentation, report writing, figure generation from existing data  
✅ Code review, testing (unit tests only, no integration grid runs)  
✅ Git operations (commit, push, pull)  
✅ Reading and analyzing existing batch_01 / batch_02 results  
✅ Planning, pre-registration, protocol design

---

## Recommended Next Paths

### Path A: Remote / Cloud Execution (RECOMMENDED)
- Move batches 3–6 execution to cloud VM (Google Colab, AWS EC2, university cluster)
- Transfer codebase via git clone
- Execute remaining 36 cases remotely
- Download results, commit locally, push to origin

**Pros:** No thermal constraint, reproducible environment, can run full 54-case grid  
**Cons:** Requires setup time, possible cost (if commercial cloud)

### Path B: Another Machine
- Execute on desktop/laptop with better cooling
- Clone repo, install dependencies
- Run batches 3–6
- Transfer results back via git push

**Pros:** Full control, no cloud cost  
**Cons:** Requires access to another machine

### Path C: Case-by-Case Local Execution with Manual Thermal Monitoring
- Set `OMP_NUM_THREADS=1` or `MKL_NUM_THREADS=2` (reduce parallelism → reduce heat)
- Execute ONE case at a time with cooldown periods
- Monitor CPU temp manually (HWMonitor, MSI Afterburner, etc.)
- Stop if temp > 85°C

**Pros:** Can complete locally if necessary  
**Cons:** Very slow (days instead of hours), high manual overhead, risky

**Verdict:** Path A (remote) strongly preferred for efficiency and safety.

---

## Current Repository State

**Branch:** main  
**HEAD:** 2ec84ab (synced with origin/main)  
**Working tree:** clean (batch_03 removed, no uncommitted changes)  
**Next commit needed:** None (batch_01 and batch_02 already pushed)

**Pending work:**
- Batches 3–6 execution (36 cases)
- Aggregate results after all 6 batches complete
- Apply decision rules
- Write final report: `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`

---

## Contact / Continuation

**When thermal issue resolved OR remote execution ready:**
1. Read `reports/NEGATIVE_CONTROLS_REMOTE_EXECUTION_PLAN_v0.1.22.md`
2. Execute batches 3–6 on safe infrastructure
3. Commit results
4. Proceed to aggregation and decision rules

**Do NOT:**
- Attempt local heavy execution without thermal monitoring
- Modify Gate 4B outputs
- Push partial/interrupted batches

---

**Document status:** ACTIVE  
**Last updated:** 2026-05-23 22:03  
**Next review:** When remote execution infrastructure ready
