# S³×S¹ Gate 4 Dry-Run Runtime Estimate Plan — v0.1.20

**Дата:** 2026-05-21 15:30 Almaty  
**Статус:** PLANNING (before dry-run execution)  
**Цель:** Estimate Gate 4 full grid runtime and check batch feasibility  
**Pre-registration:** S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md (commit 1f4173c)  

---

## 1. Purpose

**Dry-run estimates runtime and checks batch feasibility ONLY.**

**Specific goals:**
1. Measure wall-clock time per case by s1_size
2. Extrapolate to full 216-case Gate 4 grid
3. Verify r-statistic computation availability
4. Check output completeness (metrics computed, files saved)
5. Detect failure modes (numerical instability, solver errors)
6. Decide feasibility: FULL_GRID / BATCHED_GRID / PROTOCOL_REVISION / DRY_RUN_FAILED

**Scope:**
- Minimal representative subset (36 cases)
- No scientific claims
- No verdict
- No metric interpretation
- No protocol modification

---

## 2. Non-Goals (Explicit Forbidden)

**Dry-run does NOT and CANNOT:**

1. ❌ **Produce verdict** — no PASS/FAIL decision
2. ❌ **Interpret metrics** — no "W=20 shows localization" claim
3. ❌ **Change protocol** — grid/thresholds/metrics remain locked
4. ❌ **Use partial outputs as evidence** — dry-run is feasibility check, not scientific result
5. ❌ **Report preliminary Gate 4 result** — full pre-registered grid required for verdict
6. ❌ **Adjust thresholds** — 2.0x PASS and 1.5x FAIL remain fixed
7. ❌ **Cherry-pick families** — all 3 families must run

**If any forbidden action appears → immediate correction required.**

**Dry-run outputs are PLANNING DATA, not scientific evidence.**

---

## 3. Dry-Run Sample (Minimal Representative Subset)

**Grid parameters (subset of pre-registered Gate 4 grid):**

```yaml
geometry: S3xS1

families:
  - spectral_circle
  - ring
  - wilson_ring

disorder_strengths:
  - W: 0      # No disorder baseline
  - W: 20     # Gate 3C verified strength
  # W=12 excluded from dry-run (intermediate, less critical for runtime estimate)

s1_discretization_sizes:
  - 16        # Small (baseline)
  - 64        # Gate 3C standard (must reproduce)
  - 128       # Large (critical for runtime estimate)
  # s1_size=32 excluded from dry-run (interpolation, less critical)

j_max_values:
  - 2         # Lower spectral density
  - 3         # Gate 3C standard
  # Both included: runtime can differ significantly

random_seeds:
  - 123       # Single seed sufficient for runtime estimate
  # Seeds {456, 789} excluded from dry-run (statistical robustness not needed for timing)

total_cases: 3 families × 2 W × 3 sizes × 2 j_max × 1 seed = 36 cases
```

**Rationale for exclusions:**
- W=12: Intermediate disorder, similar runtime to W=0/W=20, not critical for estimate
- s1_size=32: Runtime between 16 and 64, can interpolate
- Seeds {456, 789}: Runtime nearly identical per seed, single seed sufficient

**Coverage:**
- All 3 families ✅
- Boundary W values (0, 20) ✅
- Full size range (16, 64, 128) ✅
- Both j_max values ✅
- ~17% of full grid (36/216) ✅

---

## 4. What to Measure (Runtime & Feasibility Metrics)

**Primary measurements:**

1. **Wall-clock time per case**
   - Measure: Total execution time from start to output save
   - Aggregate: Mean ± std by s1_size
   - Use: Extrapolate to full 216-case grid

2. **Runtime scaling by s1_size**
   - Measure: Time ratio t(128)/t(64), t(64)/t(16)
   - Expected: Quadratic or cubic scaling (eigenvalue solver complexity)
   - Critical: If t(128) > 30 min → batch execution required

3. **Memory usage (if available)**
   - Measure: Peak RSS (resident set size) per case
   - Aggregate: Max by s1_size
   - Critical: If RAM >16 GB → may need cluster resources

4. **Failure rate**
   - Measure: % of cases that fail to complete
   - Aggregate: By family and by s1_size
   - Critical: If failure rate >10% → implementation issues

5. **Output completeness**
   - Measure: Are all expected outputs present?
   - Check: config.json, metrics.json, figures/ (if applicable)
   - Critical: Missing outputs → cannot compute verdict later

6. **R-statistic computation availability**
   - Measure: Does level-spacing adjacent gap ratio compute successfully?
   - Check: `r_statistic` field in metrics.json
   - Critical: If unavailable → protocol may need revision (r-stat is primary metric)

**Secondary measurements:**

7. **Numerical stability**
   - Measure: Eigenvalue solver convergence warnings
   - Check: Log for "convergence failed" or "ill-conditioned matrix"
   - Use: Detect instability before full grid

8. **Disk usage**
   - Measure: Total size of RUNS/gate4_dry_run_v0.1.20/
   - Extrapolate: 216-case grid disk footprint
   - Use: Ensure sufficient disk space

---

## 5. What NOT to Report (Forbidden Claims)

**Do NOT report:**

1. ❌ **PASS/FAIL verdict** — dry-run is not scientific result
2. ❌ **Localization claim** — no "W=20 shows localization" statement
3. ❌ **IPR contrast interpretation** — can measure contrast but NOT interpret as evidence
4. ❌ **Family comparison** — no "spectral_circle outperforms ring" claim
5. ❌ **Preliminary Gate 4 result** — dry-run ≠ confirmatory replication
6. ❌ **Threshold adjustment suggestion** — 2.0x/1.5x remain fixed regardless of dry-run data
7. ❌ **Grid modification proposal based on partial data** — protocol is locked

**Allowed reporting:**
- ✅ Runtime estimate: "s1_size=128 takes ~15 min per case"
- ✅ Feasibility: "Full grid estimated 24 hours, batched execution required"
- ✅ Implementation check: "R-statistic computation successful"
- ✅ Failure detection: "wilson_ring at s1_size=128 shows 20% failure rate → investigate"

**Boundary between allowed and forbidden:**
- **Allowed:** "IPR contrast at W=20 is 2.5x (dry-run data, not evidence)"
- **Forbidden:** "W=20 localization signal confirmed by dry-run"

---

## 6. Gate 4 Feasibility Decision (Four Verdicts)

**After dry-run completes, classify as ONE of these:**

### 6.1 FULL_GRID_FEASIBLE

**Conditions (ALL must hold):**
1. Estimated full-grid runtime ≤24 hours (single session)
2. Failure rate <5% across all families and sizes
3. All metrics compute successfully (IPR, r-statistic, controls)
4. No numerical instability detected
5. Memory usage <16 GB (standard workstation RAM)
6. Output completeness 100%

**Action:** Proceed to full 216-case Gate 4 execution in single run.

**Example dry-run result:**
- t(16)=30s, t(64)=3min, t(128)=12min
- Full grid estimate: 216 × 5min avg = 18 hours ✅
- Failure rate: 0/36 = 0% ✅
- R-statistic: available ✅
- Memory: 8 GB peak ✅
- Verdict: FULL_GRID_FEASIBLE

### 6.2 BATCHED_GRID_REQUIRED

**Conditions (ANY can trigger):**
1. Estimated full-grid runtime 24–48 hours (too long for single session, acceptable for batches)
2. Failure rate 5–10% (manageable with retry logic)
3. Memory usage 16–32 GB (requires closing other applications, but feasible)
4. Numerical warnings present but not blocking (convergence slow but successful)

**Action:** Proceed to full 216-case Gate 4 execution in 4 batches per pre-registered plan (Section 8.2 of protocol).

**Example dry-run result:**
- t(16)=1min, t(64)=5min, t(128)=20min
- Full grid estimate: 216 × 8min avg = 28.8 hours ⚠️
- Failure rate: 2/36 = 5.6% ⚠️
- R-statistic: available ✅
- Memory: 20 GB peak ⚠️
- Verdict: BATCHED_GRID_REQUIRED

### 6.3 PROTOCOL_REVISION_REQUIRED

**Conditions (ANY can trigger):**
1. Estimated full-grid runtime >48 hours (prohibitive even with batches)
2. Failure rate >10% (implementation broken or grid too ambitious)
3. R-statistic computation unavailable (primary metric missing → protocol invalid)
4. Numerical instability widespread (solver fails on >20% of cases)
5. Memory usage >32 GB (requires cluster, not available)
6. s1_size=128 impossible to run (exceeds matrix size limits)

**Action:** Do NOT proceed to full Gate 4. Options:
- Reduce grid (e.g., drop s1_size=128)
- Fix implementation (e.g., enable r-statistic computation)
- Switch to cluster resources (if available)
- Abandon Gate 4 (if no viable path forward)

**Any grid reduction requires NEW pre-registration version:**
- Example: `S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20_REDUCED.md`
- Original protocol (commit 1f4173c) remains locked
- Results cite revised protocol

**Example dry-run result:**
- t(128)=45min per case
- Full grid estimate: 216 × 20min avg = 72 hours ❌
- Failure rate: 8/36 = 22% ❌
- R-statistic: NOT available ❌
- Verdict: PROTOCOL_REVISION_REQUIRED

### 6.4 DRY_RUN_FAILED

**Conditions (ANY can trigger):**
1. Dry-run cannot complete (≥50% of 36 cases fail)
2. Critical implementation bug detected (e.g., matrix dimension mismatch)
3. Output files corrupted or missing for >20% of cases
4. Eigenvalue solver fails on all s1_size=128 cases

**Action:** Fix implementation, re-run dry-run. Do NOT proceed to full Gate 4 until dry-run succeeds.

**Example dry-run result:**
- 20/36 cases failed ❌
- Error: "Hermitian check failed for S³ Dirac operator"
- Verdict: DRY_RUN_FAILED → fix bug, re-run dry-run

---

## 7. Stop Conditions (Abort Dry-Run Before Completion)

**Dry-run MUST STOP if ANY of these occur:**

### 7.1 Repeated Failure (Same Error >5 Times)
- **Trigger:** Same error message in ≥5 consecutive cases
- **Action:** Abort, debug, fix implementation, re-run dry-run
- **Example:** "Eigenvalue solver convergence failed" in 5/5 wilson_ring cases → STOP

### 7.2 Missing Critical Metrics
- **Trigger:** IPR or r-statistic unavailable in ≥3 cases
- **Action:** Abort, check implementation, ensure metrics compute
- **Example:** `r_statistic` field missing in 3/10 completed cases → STOP

### 7.3 Runtime Estimate Above Budget
- **Trigger:** After 10 cases, extrapolated full-grid runtime >72 hours
- **Action:** STOP dry-run, report PROTOCOL_REVISION_REQUIRED
- **Rationale:** No point continuing if full grid already known to be infeasible

### 7.4 Memory Exhaustion
- **Trigger:** RAM usage exceeds system limit (e.g., 32 GB workstation)
- **Action:** STOP, report PROTOCOL_REVISION_REQUIRED
- **Example:** s1_size=128, j_max=3 case uses 40 GB → STOP

### 7.5 Numerical Instability Widespread
- **Trigger:** ≥30% of cases show convergence warnings or ill-conditioned matrices
- **Action:** STOP, investigate implementation, check for bugs
- **Example:** 12/36 cases show "matrix near-singular" warning → STOP

**Do NOT continue dry-run if stop condition triggered.**  
**Report current state, document reason, plan corrective action.**

---

## 8. Output Artifacts (After Dry-Run Execution)

**Primary outputs:**

1. **Dry-run results report:**
   - `reports/S3_S1_GATE4_DRY_RUN_RESULTS_v0.1.20.md`
   - Structure: Summary → Runtime Estimates → Feasibility Decision → Next Steps
   - Must include: timing table, failure log, feasibility verdict, recommendation

2. **Run data:**
   - `reports/RUNS/gate4_dry_run_v0.1.20/config.json` — dry-run grid parameters
   - `reports/RUNS/gate4_dry_run_v0.1.20/timing.json` — per-case wall-clock times
   - `reports/RUNS/gate4_dry_run_v0.1.20/metrics.json` — computed metrics (IPR, r-stat) for feasibility check
   - `reports/RUNS/gate4_dry_run_v0.1.20/failure_log.txt` — error messages from failed cases

3. **Summary tables:**
   - `runtime_by_size.csv` — s1_size vs mean/std runtime
   - `failure_by_family.csv` — family vs failure count
   - `memory_usage.csv` — s1_size vs peak RAM

4. **Feasibility decision file:**
   - `gate4_feasibility_decision.txt` — ONE of: FULL_GRID_FEASIBLE / BATCHED_GRID_REQUIRED / PROTOCOL_REVISION_REQUIRED / DRY_RUN_FAILED

**All artifacts committed together in single atomic commit:**
```
feat(gate-4): dry-run runtime estimate and feasibility check
```

**Dry-run outputs do NOT include:**
- ❌ Scientific figures (no IPR contrast plots)
- ❌ Verdict files (no decision.md)
- ❌ Claim statements (no "localization confirmed")

---

## 9. Dry-Run Execution Checklist

**Before running dry-run, verify ALL of these:**

- [ ] Pre-registration committed (commit 1f4173c) and pushed
- [ ] Dry-run plan reviewed (this document)
- [ ] Implementation tested on single case (smoke test)
- [ ] Sufficient disk space (estimate 5 GB for 36 cases)
- [ ] No other heavy processes running (reserve RAM for dry-run)
- [ ] Timer ready to measure wall-clock time per case

**Dry-run command (example, actual command may differ):**
```bash
python scripts/run_gate4_dry_run.py \
  --families spectral_circle,ring,wilson_ring \
  --W-values 0,20 \
  --s1-sizes 16,64,128 \
  --j-max-values 2,3 \
  --seed 123 \
  --output reports/RUNS/gate4_dry_run_v0.1.20/
```

**After dry-run completes:**
- [ ] Review timing.json
- [ ] Check failure_log.txt
- [ ] Compute full-grid runtime estimate
- [ ] Classify feasibility verdict
- [ ] Write results report
- [ ] Commit dry-run artifacts
- [ ] Decide: proceed to full Gate 4 / revise protocol / fix implementation

---

## 10. Relationship to Pre-Registered Protocol

**Dry-run is a PLANNING step, not a SCIENTIFIC step.**

**Pre-registered protocol (commit 1f4173c):**
- Gate 4 full grid: 216 cases
- Decision rules: PASS ≥2.0x, FAIL <1.5x
- Metrics: IPR contrast, r-statistic, family consistency
- Status: LOCKED (no changes after commit)

**Dry-run (this plan):**
- Subset: 36 cases (17% of full grid)
- Decision rules: FEASIBLE / BATCHED / REVISION / FAILED (runtime/implementation check, NOT scientific verdict)
- Metrics: Same as protocol (to verify computation works)
- Status: PLANNING (does NOT modify protocol)

**Dry-run does NOT unlock protocol.**  
**Any grid change requires new protocol version, NOT dry-run modification.**

**If dry-run suggests grid reduction:**
1. Write new pre-registration: `S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20_REDUCED.md`
2. Commit new protocol before execution
3. Execute Gate 4 under new protocol
4. Results cite new protocol version

**Dry-run outputs are NOT used for scientific claims.**

---

## 11. Timeline

**Planned dry-run execution:**

| Milestone | Target Date | Deliverable |
|-----------|-------------|-------------|
| Dry-run plan commit | 2026-05-21 15:30 | This document in git |
| Dry-run execution | 2026-05-22 | 36 cases, ~2–4 hours estimate |
| Timing analysis | 2026-05-22 | Runtime table, extrapolation |
| Feasibility decision | 2026-05-22 | FULL_GRID / BATCHED / REVISION / FAILED |
| Results report | 2026-05-22 | S3_S1_GATE4_DRY_RUN_RESULTS_v0.1.20.md |
| Dry-run commit | 2026-05-22 | Artifacts + decision |
| Full Gate 4 start | 2026-05-23+ | (After feasibility confirmed) |

**Total duration:** 1 day (dry-run) + decision

**If dry-run verdict = PROTOCOL_REVISION_REQUIRED:**
- Pause Gate 4
- Write revised protocol
- Re-run dry-run on revised grid
- Do NOT proceed until feasibility confirmed

---

## 12. Success Criteria

**Dry-run succeeds if:**

✅ All 36 cases complete (failure rate <10%)  
✅ Runtime estimate computed for full 216-case grid  
✅ Feasibility verdict reached (one of 4 verdicts)  
✅ All metrics compute successfully (IPR, r-stat)  
✅ No stop conditions triggered  
✅ Artifacts committed to git  

**Dry-run fails if:**

❌ ≥50% of cases fail (DRY_RUN_FAILED)  
❌ Critical metrics unavailable (r-statistic missing)  
❌ Runtime estimate cannot be computed (too many failures)  
❌ Stop condition triggered before completion  

**Dry-run is NOT a Gate 4 result.**  
**Dry-run is a GO/NO-GO decision for full Gate 4 execution.**

---

## 13. References

**Pre-registration:**
- `reports/S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md` (commit 1f4173c)

**Prior dry-runs:**
- Gate 3C dry-run (informal, not documented)
- Gate 2 dry-run (informal, not documented)

**Gate 4 batch plan (from pre-registration):**
- Section 8.2: Batch Execution (4 batches, 189 cases total if all batches run)

**Timing baseline (Gate 3C):**
- s1_size=64, j_max=3: ~3 min per case (648 cases completed in ~30 hours)

**Expected scaling:**
- s1_size=16: ~30 sec (N=432, smaller than 64)
- s1_size=64: ~3 min (Gate 3C baseline)
- s1_size=128: ~10–15 min (N=3712, eigenvalue solver scales O(N²) or O(N³))

---

**Статус:** ✅ PLAN READY — ready for dry-run execution  
**Следующий шаг:** Execute dry-run (36 cases) → runtime estimate → feasibility decision  
**Запрет:** Запуск dry-run без commit этого плана

---

**Dry-run plan signature (commit hash will be added after git commit):**
```
git log --oneline --grep="GATE4.*DRY.*RUN" -1 --format="%H %ci %s"
```

This line will be filled after commit. Dry-run plan is NOT active until committed to git with timestamp before execution.
