# S³×S¹ Gate 3C Triad Gate — PRE-FLIGHT PROTOCOL

**Date:** 2026-05-21  
**Type:** PRE-REGISTRATION (before execution)  
**Purpose:** Lock down Gate 3C parameters to prevent post-hoc changes

---

## Critical Rule

**NO PARAMETER CHANGES AFTER EXECUTION STARTS**

This document freezes:
- Test grid
- Thresholds
- Verdict decision rules
- Triad Gate acceptance criteria

Any deviation from this protocol = Gate 3C INVALID.

---

## Gate 3C Purpose

**Convert exploratory W=20 signal (4.68x) into confirmatory evidence OR documented false-positive.**

**NOT allowed after Gate 3C:**
- Claim "S³×S¹ validated" unless Gate 3C = CONFIRMATORY_PASS
- Claim "optimal W=20" (already incorrect, W=20 is local peak from 3-point sweep)
- Proceed to Gate 4 unless Gate 3C ≥ PASS_WITH_CAVEATS

---

## Pre-Registered Test Grid

### Fixed Parameters

| Parameter | Values | Count | Rationale |
|-----------|--------|-------|-----------|
| **Geometry** | S³×S¹ | 1 | Gate 3C scope |
| **Families** | spectral_circle, ring, wilson_ring | 3 | All 3 families |
| **j_max** | 1, 2, 3 | 3 | Full angular momentum range |
| **s1_sizes** | 8, 16, 32, 64 | 4 | Include s64 (wilson_ring resolved) |
| **alpha** | 0.0, 0.5 | 2 | Flux variation |
| **Disorder W** | **0.0, 12.0, 20.0** | 3 | Clean + Gate 3 baseline + exploratory peak |
| **Seeds** | 123, 456, 789 | 3 | 3rd seed for robustness |
| **n_low** | 5 | 1 | Lowest eigenmode IPR |
| **Mode** | geometric_weight | 1 | Same as Gate 3 |
| **Radius** | 1.0 | 1 | Standard |

**Total cases:** 3 × 3 × 4 × 2 × 3 × 3 = **648 cases**

**Estimated time:** ~11 minutes (648 × 1.0s average)

---

## Pre-Registered Thresholds

### Primary Threshold (LOCKED)

**Absolute IPR contrast at W=20:** ≥ **2.0x**

- Clean baseline: W=0
- Comparison: W=20 vs W=0
- Metric: absolute IPR (mean of 5 lowest eigenmodes)
- No post-hoc threshold adjustment allowed

### Secondary Metrics (INFORMATIVE)

- W=12 contrast (Gate 3 baseline comparison)
- IPR ratio contrast (deprecated, for backward compatibility only)
- Per-family breakdown (diagnostic, not pass/fail)
- Per-s1_size breakdown (finite-size scaling diagnostic)

---

## Triad Gate — Pre-Registered Acceptance Criteria

### T1 — Analytical S³ Eigenvalue Benchmark

**Purpose:** Verify S³ discretization produces correct eigenvalue structure

**Method:**
1. Extract lowest 10 eigenvalues from clean (W=0) S³×S¹ operator
2. Compare to analytical formula: λ = ±(n + 3/2) / R for SU(2) spin-1/2
3. Compute residuals: |λ_numerical - λ_analytical|

**Pre-registered tolerance:** Mean residual < 0.5 (discretization error acceptable)

**Pass criteria:**
- ✅ Mean residual < 0.5
- ✅ Eigenvalue structure shows discrete levels (not continuous)
- ✅ No unexpected degeneracies beyond SU(2) symmetry

**Fail criteria:**
- ❌ Mean residual > 1.0 (discretization broken)
- ❌ Continuous spectrum (geometry not S³)
- ❌ Eigenvalues all positive or all negative (sign error)

**If T1 FAILS → Gate 3C verdict = BLOCKED_BY_TRIAD_FAILURE**

---

### T4 — Absolute IPR Confirmation

**Purpose:** Confirm exploratory W=20 signal replicates in independent dataset

**Method:**
1. Compute absolute IPR for W=0, W=12, W=20
2. Compute contrast: IPR(W=20) / IPR(W=0)
3. Check reproducibility across families, seeds, s1_sizes

**Pre-registered threshold:** W=20 contrast ≥ **2.0x**

**Pass criteria:**
- ✅ Mean contrast (all cases) ≥ 2.0x
- ✅ At least 2/3 families show ≥ 2.0x
- ✅ At least 3/4 s1_sizes show ≥ 2.0x
- ✅ All 3 seeds show ≥ 1.8x (within 10% of threshold)

**Weak criteria (PASS_WITH_CAVEATS):**
- ⚠️ Mean contrast ≥ 2.0x BUT one family < 2.0x
- ⚠️ Mean contrast ≥ 2.0x BUT one s1_size < 2.0x (finite-size effect)

**Fail criteria:**
- ❌ Mean contrast < 2.0x
- ❌ Only 1/3 families ≥ 2.0x (family-specific artifact)
- ❌ Only 1/4 s1_sizes ≥ 2.0x (size-specific artifact)

**If T4 FAILS → Gate 3C verdict ≤ WEAK_OR_INCONCLUSIVE**

---

### T5 — Level-Spacing Statistics ⟨r⟩

**Purpose:** Sanity check that disorder affects spectral statistics (Anderson localization signature)

**Method:**
1. Compute adjacent gap ratio: r_i = min(δ_i, δ_{i+1}) / max(δ_i, δ_{i+1})
2. Mean over spectral window: ⟨r⟩ = mean(r_i)
3. Compare clean (W=0) vs disordered (W=20)

**Expected behavior:**
- Clean (W=0): ⟨r⟩ ≈ 0.53 (GOE, level repulsion)
- Disordered (W=20): ⟨r⟩ toward 0.39 (Poisson, localized)

**Pre-registered tolerance:** |Δ⟨r⟩| ≥ 0.05 (detectable shift)

**Pass criteria:**
- ✅ ⟨r⟩_clean - ⟨r⟩_disordered ≥ 0.05
- ✅ Direction correct (clean > disordered)
- ✅ No systematic NaN or instability

**Informative (not pass/fail):**
- ⟨r⟩ values are diagnostic, not proof of GOE/Poisson ensembles
- Finite-size effects may blur transition
- Strong disorder (W=20) may not reach full Poisson regime

**Fail criteria (ARTIFACT_RISK):**
- ❌ ⟨r⟩_disordered > ⟨r⟩_clean (wrong direction)
- ❌ ⟨r⟩ unstable (large variance across seeds)
- ❌ Systematic NaN (numerical precision breakdown)

**If T5 shows artifact risk → downgrade verdict, document caveat**

---

## Pre-Registered Decision Rules

### GATE3C_CONFIRMATORY_PASS

**All of:**
1. T1 passes (S³ eigenvalue structure correct)
2. T4 passes (W=20 ≥ 2.0x, all criteria met)
3. T5 passes (level-spacing shift detectable, stable)
4. Controls remain clean (test_s3_s1_controls.py still 6/6)
5. No new failure clusters
6. Result does NOT depend on post-hoc threshold changes

**Consequence:** Gate 4 allowed. Can claim "W=20 confirmatory evidence" (NOT "validated").

---

### GATE3C_PASS_WITH_CAVEATS

**All of:**
1. T1 passes
2. T4 passes (mean ≥ 2.0x) BUT one localized caveat:
   - One family < 2.0x (document which)
   - OR one s1_size < 2.0x (finite-size effect)
3. T5 passes or informative-only (not artifact risk)
4. Caveat is documented and understood

**Consequence:** Gate 4 allowed with documented caveat. Claim "W=20 confirmatory with [caveat]".

---

### GATE3C_WEAK_OR_INCONCLUSIVE

**Any of:**
1. T1 passes
2. T4 mean contrast < 2.0x (improvement over Gate 3 but below threshold)
3. OR inconsistent across families/seeds (no clear pattern)
4. T5 informative but not conclusive

**Consequence:** Gate 4 BLOCKED. Exploratory sweep was noise or unstable. Document as "exploratory signal did not replicate".

---

### GATE3C_FAIL_ARTIFACT_RISK

**Any of:**
1. T1 FAILS (S³ structure broken)
2. T4 depends on narrow subgroup only (1/3 families, 1/4 sizes)
3. T5 shows artifact risk (wrong direction, unstable)
4. Controls fail (test_s3_s1_controls.py < 6/6)

**Consequence:** Gate 4 BLOCKED. Exploratory sweep was false positive. Classify as numerical artifact.

---

### GATE3C_BLOCKED_BY_TRIAD_FAILURE

**Condition:** T1 FAILS before T4/T5 can be evaluated

**Consequence:** Stop execution, investigate discretization. Gate 3C invalid until T1 fixed.

---

## Pre-Registered NOT Allowed

After Gate 3C execution:

❌ Change threshold from 2.0x to lower value  
❌ Add exploratory W values (e.g., W=16, W=24) after seeing W=20 result  
❌ Exclude "inconvenient" families or s1_sizes post-hoc  
❌ Claim "S³×S¹ validated" unless verdict = CONFIRMATORY_PASS  
❌ Claim "optimal W=20" (already established as local peak, not optimum)  
❌ Proceed to Gate 4 if verdict < PASS_WITH_CAVEATS  
❌ Re-run Gate 3C with different parameters if result is FAIL (must document failure)

---

## Pre-Registered Allowed

✅ Document caveats honestly (family-specific, size-specific)  
✅ Classify exploratory sweep as false positive if Gate 3C FAILS  
✅ Proceed to Gate 4 if verdict ≥ PASS_WITH_CAVEATS  
✅ Claim "W=20 confirmatory evidence" if PASS (NOT "validated")  
✅ Run follow-up exploratory sweeps AFTER Gate 3C (clearly marked exploratory)

---

## Execution Protocol

1. Create test_s3_s1_gate3c_triad.py (T1, T5 implementations)
2. Create s3_s1_gate3c_confirmatory.py (run wrapper)
3. Execute Gate 3C (648 cases)
4. Evaluate T1, T4, T5 against pre-registered criteria
5. Assign verdict from decision rules (NO post-hoc changes)
6. Create GATE3C_CONFIRMATORY_REPLICATION report
7. Decision: Gate 4 allowed or blocked

---

## Integrity Commitment

**I commit to:**
- Follow this protocol exactly as written
- NOT change thresholds after seeing results
- NOT exclude data post-hoc
- Document any deviations as protocol violations
- Classify Gate 3C as INVALID if protocol violated

**Signed:** Claude Code Agent (pre-execution)  
**Date:** 2026-05-21  
**Timestamp:** (before Gate 3C execution)

---

## Deliverables Checklist

- [ ] This pre-flight protocol document
- [ ] tests/test_s3_s1_gate3c_triad_v0_1_20.py
- [ ] scripts/s3_s1_gate3c_confirmatory.py
- [ ] Gate 3C execution (648 cases)
- [ ] reports/S3_S1_GATE3C_CONFIRMATORY_REPLICATION_v0.1.20.md
- [ ] Verdict assigned from decision rules
- [ ] Gate 4 decision (allowed/blocked)

---

**Status:** PRE-REGISTERED (locked, execution pending)

**Next:** Create implementation files, execute Gate 3C, evaluate against criteria.
