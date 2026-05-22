# Current Status — v0.1.22 Negative Controls Planning

**Date:** 2026-05-22  
**Phase:** PLANNING  
**Status:** PRE-REGISTERED  
**Gate 4B Status:** CLOSED (f7eff32, PASS_WITH_CAVEATS)

---

## Executive Summary

**v0.1.22 planning phase завершён:**  
Negative controls protocol pre-registered. Implementation plan готов. Execution и code implementation отложены до явной команды пользователя.

**Why negative controls:**  
Gate 4B v0.1.21 demonstrated 7.15× IPR contrast with family consistency and strengthening FSS trend on S³×S¹ finite lattice. Before concluding this is geometry-specific, we must verify the harness can reject non-geometric baselines (random Hermitian, scrambled geometry, broken Wilson).

**Scope:**  
Falsification-first specificity test. NOT a new positive validation claim. Purpose: test harness discrimination power.

---

## Gate 4B Final Status (Closed)

**Last commit:** 0c78263 (closeout package)  
**Results commit:** f7eff32  
**Verdict:** GATE4B_FSS_PASS_WITH_CAVEATS  
**Grid:** 216 cases (3 families, 3 W, 4 sizes, 2 j_max, 3 seeds)  
**Aggregate contrast:** 7.15× (W=20 vs W=0)  
**FSS trend:** STRENGTHENING (3.76× → 24.90×)  
**Family consistency:** 3/3 PASS  
**r-statistic:** Δr = -0.163 (toward Poisson)

**Key documents:**
- `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md`
- `reports/GATE4B_PRE_PUSH_AUDIT_v0.1.21.md`
- `reports/CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md`

**Immutability:**  
Gate 4B is NOT being modified. v0.1.22 is independent validation layer.

---

## v0.1.22 Planning Output

**Documents created:**

### 1. Pre-Registration Protocol
**File:** `reports/S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md`

**Contents:**
- Purpose: test harness specificity (can it reject broken controls?)
- 3 negative controls: random Hermitian, scrambled geometry, broken Wilson
- Pilot grid: 54 cases (3 controls × 2 W × 3 sizes × 1 j_max × 3 seeds)
- Expected outcome: controls should fail (NOT reproduce Gate 4B PASS pattern)
- Decision rules: same ≥2.0× threshold, control consistency check
- False-pass danger: if ANY control shows Gate 4B-like robustness

---

### 2. Implementation Plan
**File:** `reports/NEGATIVE_CONTROLS_IMPLEMENTATION_PLAN_v0.1.22.md`

**Contents:**
- Architecture: separate module `cc_toy_lab/geometry/negative_controls.py`
- Execution script: `scripts/run_negative_controls_v0_1_22.py`
- Tests: grid coverage, no Gate 4B mutation
- Risk assessment: control too artificial, metric artifact, false pass
- Time estimate: ~3 hours implementation, ~1 hour execution
- Success criteria: 3 constructors, 54-case grid, tests pass

---

### 3. Status Document (This File)
**File:** `reports/CURRENT_STATUS_v0.1.22_NEGATIVE_CONTROLS_PLANNING.md`

**Purpose:** Handoff note for next session or next command.

---

## What v0.1.22 Will Test

**Scientific question:**  
Does Gate 4B signal reflect specific S³×S¹ geometric disorder coupling, OR can similar PASS-like results be produced by broken/random/scrambled controls?

**Falsification hypothesis:**  
If harness is specific, negative controls should:
- Show <2.0× contrast (below Gate 4B threshold)
- Show weak or collapsing FSS trend (not strengthening)
- Show inconsistent r-statistic (not toward Poisson)
- Fail ≥2/3 control consistency check

**Danger result:**  
If ANY control reproduces the full Gate 4B-like PASS pattern (≥2.0× contrast, stable/strengthening FSS, r-stat shift consistent with localization, reproducible across seeds/sizes — not isolated), harness lacks specificity.

---

## What v0.1.22 Will NOT Claim

**Explicitly forbidden:**
- "Negative controls prove S³×S¹" (falsification ≠ validation)
- "Negative controls prove physical compactification" (computational model only)
- "Negative controls prove FL generalization" (specificity ≠ generalization)
- "Negative controls guarantee no artifacts" (test SOME failure modes, not all)

**Correct framing:**  
Negative controls test harness discrimination power. They do NOT validate S³×S¹ geometry or prove Gate 4B correctness.

---

## Proposed Negative Controls

### Control A: Random Hermitian Baseline
**Purpose:** Check if generic random matrix with disorder fakes IPR contrast  
**Construction:** Diagonal U(r) ∈ [-W, W], Gaussian off-diagonal, NO geometric structure  
**Expected:** Should NOT reproduce the full Gate 4B-like robust pattern

### Control B: Scrambled Geometry
**Purpose:** Preserve dimension/scale but break S³×S¹ geometric coupling  
**Construction:** S³ indices permuted OR S³/S¹ decoupled OR wrong spectrum  
**Expected:** Should weaken or destabilize signal, not reproduce full robust pattern

### Control C: Broken Wilson Term
**Purpose:** Test if Wilson correction is load-bearing  
**Construction:** Wilson coefficient = 0 OR Wilson structure scrambled  
**Expected:** Should NOT reproduce wilson_ring robustness pattern

---

## Pilot Grid

**Size:** 54 cases (25% of Gate 4B 216-case grid)

| Parameter | Gate 4B | v0.1.22 Pilot |
|-----------|---------|---------------|
| Families/Controls | 3 families | 3 controls |
| W values | 0, 12, 20 | 0, 20 |
| s1_size | 16, 32, 64, 128 | 16, 64, 128 |
| j_max | 2, 3 | 3 only |
| seeds | 123, 456, 789 | 123, 456, 789 |
| **Total** | 216 | 54 |

**Execution mode:** Batched (6 batches × 9 cases)  
**Runtime estimate:** ~27 minutes

---

## Implementation Status

**Current state:** PLANNING ONLY  
**Code written:** None  
**Tests written:** None  
**Execution:** Not started

**Next step options:**

### Option 1: Implement Controls (Conservative, Recommended)
1. Read dependencies (`s3_s1_product.py`, `s1_families.py`)
2. Write `cc_toy_lab/geometry/negative_controls.py`
3. Write `scripts/run_negative_controls_v0_1_22.py`
4. Write tests (`test_negative_controls_*.py`)
5. Dry-run (single case verification)
6. Ask user: "Ready to execute 54-case pilot?"

**Time:** ~3 hours implementation + verification

---

### Option 2: Execute Gate 5 Instead (Alternative Path)
If user prefers to extend S³×S¹ scaling (s1_size=256, 512) before negative controls, Gate 5 can be pursued first.

**Trade-off:**  
Gate 5 = more S³×S¹ data (strengthen positive claim)  
v0.1.22 = specificity check (strengthen confidence in existing claim)

---

### Option 3: Pause and Review (Wait)
If user wants to review Gate 4B for 2 weeks before next step, planning documents are ready for future use.

---

## Key Design Questions (Need Dependency Audit)

**Before implementation, resolve:**
1. What is exact S³ dimension formula? (Should be `N_S3 = 2*j_max + 1` per Gate 4B, verify from code)
2. How are S³ and S¹ sectors coupled? (Kronecker product? Additive?)
3. What is Wilson term formula? (Need to read `s1_families.py`)
4. What scale should random Hermitian off-diagonal have? (Match S³×S¹ coupling scale)
5. Should random baseline be flat matrix or block-diagonal? (Depends on S³×S¹ structure)

**Resolution path:**  
Read `cc_toy_lab/geometry/s3_s1_product.py` and related files (Step 1 of implementation plan).

---

## Risks and Mitigations

### Risk 1: Control Too Artificial
**Concern:** Random Hermitian may be too different (no block structure)  
**Mitigation:** Match dimension N, disorder W, preserve some structure  
**Detection:** If contrast <0.5×, control under-constrained

### Risk 2: False Pass Due to Metric Artifact
**Concern:** IPR may increase with ANY disorder, not just geometric  
**Mitigation:** Compare W=0 baselines (random vs S³×S¹ should differ)  
**Detection:** If random shows SAME 7.15× contrast, metric non-specific

### Risk 3: Accidentally Modifying Gate 4B
**Concern:** Adding controls breaks S³×S¹ operator  
**Mitigation:** Separate module, separate script, unit test immutability  
**Detection:** Run Gate 4B test suite after adding controls

### Risk 4: Scrambled Geometry Still Geometric
**Concern:** Permutation may not destroy structure (eigenvalue distribution preserved)  
**Mitigation:** Verify scrambled eigenvalue distribution ≠ S³×S¹  
**Detection:** If scrambled W=0 baseline = S³×S¹ W=0, scramble too weak

---

## Success Criteria

**Planning phase (COMPLETE):**
- [x] Pre-registration protocol written
- [x] Implementation plan written
- [x] Status/handoff note written
- [x] No overclaim language (verified in next section)

**Implementation phase (PENDING):**
- [ ] Dependency audit complete
- [ ] Control module written
- [ ] Execution script written
- [ ] Tests written and passing
- [ ] Dry-run successful

**Execution phase (PENDING):**
- [ ] 54-case pilot grid executed
- [ ] Aggregation + decision rules applied
- [ ] Results report written
- [ ] Verdict: PASS_AS_EXPECTED or FALSE_PASS or WEAK

---

## Overclaim Check (Planning Documents)

**Forbidden terms searched:**
```
validated, generalized, optimal, thermodynamic, compactification.*proven, 
physical.*proven, paradigm, breakthrough, Standard Model, chirality
```

**Results:** ✅ ALL CLEAN

**Forbidden terms found only in:**
- Forbidden-claims sections (explicitly forbidden)
- Non-goals sections (explicitly prohibited)
- Caveat headers

**No forbidden claims in positive sections.**

**Safe wording used:**
- "test harness specificity" ✅
- "falsification-first" ✅
- "negative controls are NOT validation" ✅
- "computational model only" ✅

---

## Next Recommended Action

**Recommended:** Implement controls (Option 1)

**Rationale:**  
Negative controls are low-risk, high-value falsification layer. Pilot grid is small (54 cases, ~27 min). If controls fail as expected, confidence in Gate 4B strengthened. If false pass detected, avoids premature scaling to Gate 5.

**Command to proceed:**
```
Start v0.1.22 implementation:
1. Read dependencies (s3_s1_product.py, s1_families.py)
2. Write negative_controls.py
3. Write run_negative_controls_v0_1_22.py
4. Write tests
5. Dry-run verification
```

**Alternative:** User can specify different priority (Gate 5, methodology report, cross-geometry, etc.)

---

## Commit Plan (After Planning Phase)

**Files to commit:**
- `reports/S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md`
- `reports/NEGATIVE_CONTROLS_IMPLEMENTATION_PLAN_v0.1.22.md`
- `reports/CURRENT_STATUS_v0.1.22_NEGATIVE_CONTROLS_PLANNING.md`

**Commit message:**
```
docs(controls): pre-register v0.1.22 negative controls

- Define falsification-first negative controls after Gate 4B PASS_WITH_CAVEATS
- Specify random, scrambled, and broken-Wilson controls
- Add pilot grid and false-pass decision rules
- Preserve Gate 4B result boundaries and no-overclaim language
- Defer execution and implementation to later commands

Gate 4B (f7eff32) remains unchanged.
```

**Push:** NO (per user instruction, commit but do not push)

---

## Integration with Existing Reports

**Gate 4B reports (unchanged):**
- `CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md`
- `S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md`
- `CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md`

**v0.1.22 reports (new):**
- `S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md`
- `NEGATIVE_CONTROLS_IMPLEMENTATION_PLAN_v0.1.22.md`
- `CURRENT_STATUS_v0.1.22_NEGATIVE_CONTROLS_PLANNING.md` (this file)

**Future v0.1.22 reports (pending execution):**
- `S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`
- `NEGATIVE_CONTROLS_COVERAGE_v0.1.22.md`
- `NEGATIVE_CONTROLS_FALSE_PASS_AUDIT_v0.1.22.md` (if needed)

---

## README Update (Deferred)

**After v0.1.22 execution completes:**  
Update README.md with:
- New validation status row: "Negative Controls (v0.1.22)" with verdict
- Brief interpretation (1-2 sentences)
- Reference to results report

**Do NOT update README now** (planning only, no results yet).

---

**Status Date:** 2026-05-22  
**Status Type:** PLANNING_COMPLETE  
**Next Review:** When user requests implementation or execution  
**Gate 4B Status:** CLOSED (no further modification)  
**v0.1.22 Status:** PRE-REGISTERED (ready for implementation)
