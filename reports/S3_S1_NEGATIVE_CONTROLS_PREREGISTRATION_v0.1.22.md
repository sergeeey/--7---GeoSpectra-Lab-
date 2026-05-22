# S³×S¹ Negative Controls Pre-Registration — v0.1.22

**Date:** 2026-05-22  
**Status:** PRE-REGISTERED  
**Scope:** Falsification-first specificity testing  
**Gate 4B Reference:** f7eff32 (GATE4B_FSS_PASS_WITH_CAVEATS)

---

## 1. Purpose

**Primary goal:**  
Test whether the validation harness can reject controls that should NOT reproduce the Gate 4B robust S³×S¹ signal.

**Scientific question:**  
Does the Gate 4B PASS_WITH_CAVEATS verdict reflect a specific finite-lattice S³×S¹ geometric disorder coupling, or can similar PASS-like results be produced by broken / random / scrambled controls?

**Why this matters:**  
Gate 4B demonstrated 7.15× IPR contrast with family consistency and strengthening FSS trend. Before concluding this is specific to S³×S¹ geometry, we must verify the harness can reject non-geometric baselines.

**Falsification layer:**  
This is a specificity test (negative controls), NOT a new positive validation claim. Purpose: demonstrate harness discrimination power, not expand S³×S¹ claims.

---

## 2. Relationship to Gate 4B

**Gate 4B final status:**
- Final commit: f7eff32
- Closeout commit: 0c78263
- Verdict: GATE4B_FSS_PASS_WITH_CAVEATS
- Grid: 216 cases (3 families, 3 W, 4 sizes, 2 j_max, 3 seeds)
- Aggregate contrast: 7.15× (W=20 vs W=0)
- Family consistency: 3/3 PASS
- FSS trend: STRENGTHENING (3.76× → 24.90×)

**Immutability:**  
Gate 4B is NOT being modified. No thresholds changed, no grid altered, no verdict reinterpreted.

**v0.1.22 scope:**  
New validation layer. Separate grid. Independent decision rules. Results do NOT retroactively affect Gate 4B verdict.

---

## 3. Non-Goals (Explicitly Forbidden)

**DO NOT use negative controls to:**
1. Prove S³×S¹ physically
2. Prove compactification (Kaluza-Klein, 4D spacetime)
3. Prove Fermat-Lichnerowicz generalization
4. Prove W=20 optimality
5. Change Gate 4B thresholds post-hoc
6. Inflate Gate 4B claims (e.g., "negative controls validate S³×S¹")
7. Claim Standard Model physics
8. Claim chirality

**Allowed use:**  
Negative controls may strengthen confidence in Gate 4B specificity IF controls fail as expected. But this is supporting evidence only, NOT a proof of correctness.

---

## 4. Negative Control Candidates

**Design principle:**  
Each control should preserve SOME structure (dimension, disorder strength) while breaking the geometric S³×S¹ coupling that Gate 4B tested.

### Control A: Random Hermitian Baseline

**Purpose:**  
Check whether a generic random Hermitian matrix with disorder-like structure can fake the true IPR contrast.

**Construction:**
```python
H_random = random_hermitian_matrix(N)
# Diagonal: U(r) ∈ [-W, W] (same as Gate 4B)
# Off-diagonal: Gaussian random couplings with fixed scale
# NO geometric structure (no S³ harmonics, no S¹ twist)
```

**Expected outcome:**  
Should NOT reproduce the full Gate 4B-like robust pattern. Random matrix ≠ geometric localization. Isolated contrast alone is not sufficient for concern.

**False-pass danger:**  
If random Hermitian reproduces the full Gate 4B-like pattern (≥2.0× contrast, stable/strengthening FSS, r-stat shift consistent with localization, reproducible across seeds/sizes), Gate 4B signal is NOT geometry-specific.

---

### Control B: Scrambled Geometry Control

**Purpose:**  
Preserve some dimensions and matrix scale but scramble geometric coupling so S³×S¹ structure is broken.

**Construction options:**
1. **Permutation scramble:** S³ harmonic indices randomly permuted, S¹ twist broken
2. **Wrong geometry:** Replace S³ with random 3-sphere-like spectrum (not true eigenvalue set)
3. **Decoupled product:** S³ sector independent of S¹ sector (no cross-coupling)

**Expected outcome:**  
Should weaken, randomize, or destabilize the localization signal. May show contrast in isolated seeds but NOT reproduce the full robust pattern with family/control consistency.

**False-pass danger:**  
If scrambled geometry reproduces the full Gate 4B-like robustness pattern (not just isolated contrast), the signal is NOT sensitive to geometric details.

---

### Control C: Broken Wilson Term Control

**Purpose:**  
Specifically perturb or disable the Wilson-ring correction structure to test whether the Wilson family result depends on meaningful implementation.

**Construction:**
```python
# wilson_ring: includes Wilson term for lattice artifact correction
# Broken: set Wilson coefficient to 0 or scramble Wilson term structure
```

**Expected outcome:**  
Should NOT produce consistent Gate 4B-like robustness across the same decision rules. Wilson-ring family in Gate 4B showed 8.49× contrast with strengthening FSS — broken Wilson should fail to reproduce this robust pattern.

**False-pass danger:**  
If broken Wilson term reproduces the wilson_ring robustness pattern (8.49× contrast with consistent FSS/r-stat, not isolated), the Wilson correction is NOT load-bearing.

---

### Optional Future Controls

**Lower priority (NOT v0.1.22 pilot):**
- **Wrong spectrum control:** Replace S³ eigenvalues with power-law or random spectrum
- **Noise-only baseline:** Disorder W present but NO lattice structure
- **Seed-scrambled operator:** Same operator but seeds shuffled → test reproducibility
- **Family-label permutation:** Test if family labels matter or are arbitrary

**Decision:** Start with A, B, C. Add others only if pilot shows ambiguity.

---

## 5. Proposed Pilot Grid

**Rationale for reduced grid:**  
Negative controls are falsification tests. Start small. If ANY control false-passes, stop and investigate before scaling.

**Full Gate 4B grid:** 216 cases  
**Proposed pilot grid:** 54 cases (25% of Gate 4B)

### Pilot Grid Parameters

| Parameter | Gate 4B | Pilot v0.1.22 | Rationale |
|-----------|---------|---------------|-----------|
| Families | 3 | 3 controls | A, B, C instead of spectral_circle, ring, wilson_ring |
| W values | 0, 12, 20 | 0, 20 | Skip W=12 (diagnostic), focus on endpoints |
| s1_size | 16, 32, 64, 128 | 16, 64, 128 | Skip 32 (preserve FSS endpoints, drop intermediate) |
| j_max | 2, 3 | 3 only | Max dimension only (N=896 max) |
| seeds | 123, 456, 789 | 123, 456, 789 | Same seeds for reproducibility check |

**Total:** 3 controls × 2 W × 3 sizes × 1 j_max × 3 seeds = **54 cases**

**Execution mode:** Batched (same as Gate 4B), 6 batches × 9 cases

**Runtime estimate:** ~27 minutes (50% of Gate 4B time, proportional to case count)

---

## 6. Metrics

**Use same core metrics as Gate 4B:**
- **true_ipr_mean:** Canonical metric (IPR = Σ|ψᵢ|⁴ for bottom 10% eigenstates)
- **r_stat:** Level-spacing adjacent gap ratio
- **Family/control consistency:** How many controls PASS independently
- **Finite-size trend:** Does contrast strengthen, saturate, or collapse with size?
- **Failure rate:** Execution robustness check

**Metric version:** v0.1.21_true_eigenvector_ipr (same as Gate 4B)

**CRITICAL — No deprecated metric:**  
DO NOT use `mean_low_ipr` or `mean_low_eigenvalue` as canonical metric. Use `true_ipr_mean` only.

---

## 7. Expected Outcomes

### Healthy Result (Controls Fail as Expected)

**Expected pattern:**
- Controls do NOT reproduce Gate 4B-like PASS pattern
- May show isolated contrast in single control/size/seed, but NOT robust
- No family/control consistency (≤1/3 controls PASS)
- FSS trend weak, noisy, or collapsing (not strengthening)
- Verdict: NEGATIVE_CONTROL_FAILS_AS_EXPECTED

**Interpretation:**  
Harness specificity confirmed. Gate 4B signal is NOT reproducible by broken/random baselines.

---

### Danger Result (False Pass)

**Danger pattern:**
- At least ONE control reproduces Gate 4B-like PASS pattern:
  - Aggregate contrast ≥2.0× (threshold from Gate 4B)
  - Stable or strengthening FSS trend
  - r_stat shift consistent with localization
  - NOT explainable as single-size or single-seed artifact
- Verdict: NEGATIVE_CONTROL_FALSE_PASS

**Interpretation:**  
Harness lacks specificity. Gate 4B signal may be artifact of measurement, NOT geometry.

**Action if danger result:**  
1. STOP execution (do not scale to full grid)
2. Diagnose false-passing control
3. Review Gate 4B decision rules
4. Consider Gate 4B verdict downgrade

---

### Weak/Inconclusive Result

**Weak pattern:**
- Controls show mixed signals
- Some controls show partial contrast (1.5× – 2.5×) but not robust
- FSS trend ambiguous (neither clearly strengthening nor clearly collapsing)
- Verdict: NEGATIVE_CONTROLS_WEAK_OR_INCONCLUSIVE

**Interpretation:**  
More controls or larger grid required. Pilot insufficient to confirm specificity.

**Action if weak result:**  
1. Add control D, E (wrong spectrum, noise-only)
2. Expand pilot grid (add W=12, add s1_size=32)
3. Increase seed count (5 or 10 seeds)

---

## 8. Decision Rules

### Rule 1: Aggregate Contrast Check

**For each control:**
- Compute: contrast_ratio = mean(IPR, W=20) / mean(IPR, W=0)
- Threshold: ≥2.0× for concern (same as Gate 4B PASS)

**Control-level verdict:**
- contrast_ratio ≥2.0× → FLAG as concerning
- contrast_ratio <2.0× → expected failure

---

### Rule 2: FSS Trend Check

**For each control with contrast_ratio ≥2.0×:**
- Compute: contrast_ratio at s1_size = 16, 64, 128
- Check trend: strengthening (16 < 64 < 128), saturating (flat), collapsing (16 > 64 > 128)

**FSS verdict:**
- Strengthening → DANGER (Gate 4B-like)
- Saturating or collapsing → less concerning (weak false pass)

---

### Rule 3: Control Consistency Check

**Across all 3 controls:**
- Count: how many controls have contrast_ratio ≥2.0× AND strengthening FSS trend
- Threshold: ≥2/3 for DANGER (same as Gate 4B family consistency)

**Consistency verdict:**
- ≥2/3 controls PASS-like → NEGATIVE_CONTROL_FALSE_PASS (harness lacks specificity)
- 1/3 controls PASS-like → AMBIGUOUS (investigate single false-passing control)
- 0/3 controls PASS-like → NEGATIVE_CONTROL_FAILS_AS_EXPECTED (healthy)

---

### Rule 4: r-Statistic Check

**For each control with contrast_ratio ≥2.0×:**
- Compute: Δr = r_stat(W=20) - r_stat(W=0)
- Gate 4B had: Δr = -0.163 (toward Poisson)
- Check: Is control r-stat shift consistent with localization interpretation?

**r-stat verdict:**
- Δr < -0.1 AND IPR contrast ≥2.0× → DANGER (both diagnostics agree)
- Δr ≈ 0 OR positive → less concerning (inconsistent diagnostics)

---

### Rule 5: Single-Size Artifact Check

**For each concerning control:**
- Check: Is contrast driven by single size? (e.g., only s1_size=128 shows contrast)
- Threshold: If ≥2 sizes show contrast ≥1.5× → NOT single-size artifact

**Artifact verdict:**
- Single-size only → downgrade to WEAK (not robust false pass)
- Multi-size → upgrade to DANGER (robust false pass)

---

### Final Verdict Logic

```python
if any_control_shows_gate4b_like_pattern:
    if control_consistency >= 2/3 and fss_strengthening and r_stat_consistent:
        return "NEGATIVE_CONTROL_FALSE_PASS"  # DANGER
    elif ambiguous_pattern:
        return "NEGATIVE_CONTROLS_WEAK_OR_INCONCLUSIVE"
    else:
        return "NEGATIVE_CONTROL_PARTIAL_FALSE_PASS"  # investigate
else:
    return "NEGATIVE_CONTROLS_PASS_AS_EXPECTED"  # healthy
```

**Tie-breaking:**  
If borderline (e.g., 1.9× contrast, weak FSS), default to WEAK verdict (do not claim false pass without strong evidence).

---

## 9. Stop Conditions

**Execution MUST stop immediately if:**
1. Random Hermitian baseline gives Gate 4B-like PASS pattern (≥2.0× contrast, strengthening FSS, r_stat consistent)
2. `true_ipr_mean` unavailable for ≥10% of cases (metric implementation error)
3. `r_stat` unavailable for ≥10% of cases
4. Implementation requires changing Gate 4B code in a way that affects historical f7eff32 results
5. Control definition is ambiguous (cannot construct operator without arbitrary choices)
6. Runtime unexpectedly exceeds safe bounds (>2× Gate 4B per-case time)

**Action on stop:**
- Write STOP reason to execution log
- Do NOT proceed to verdict
- Report: NEGATIVE_CONTROLS_INCOMPLETE

---

## 10. Output Artifacts

**Future execution (v0.1.22) should produce:**

### Primary Outputs
- `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md` — final verdict document
- `reports/RUNS/negative_controls_v0.1.22/config.json` — grid configuration
- `reports/RUNS/negative_controls_v0.1.22/batches/batch_01/` through `batch_06/` — raw outputs
- `reports/RUNS/negative_controls_v0.1.22/merged/*.json` — aggregated metrics

### Derived Analyses
- `reports/NEGATIVE_CONTROLS_COVERAGE_v0.1.22.md` — grid coverage verification
- `reports/NEGATIVE_CONTROLS_FALSE_PASS_AUDIT_v0.1.22.md` — if false pass detected

### NOT Generated in Planning Phase
- This pre-registration does NOT create results
- This document is protocol only
- Execution deferred to future command

---

## 11. Claim Language

### Allowed Claims (After Execution)

**If controls fail as expected:**
- "Negative controls confirm harness can reject non-geometric baselines"
- "Random Hermitian and scrambled geometry controls show <2.0× contrast (expected failure)"
- "Harness specificity strengthened by negative control layer"

**If false pass detected:**
- "Negative control X reproduced Gate 4B-like pattern, indicating potential specificity issue"
- "Harness requires refinement to discriminate geometric vs non-geometric signals"

---

### Forbidden Claims (Always)

**NEVER claim:**
- "Negative controls prove S³×S¹" (controls are falsification tests, not positive validation)
- "Negative controls prove physical compactification" (computational model only)
- "Negative controls prove generalization" (specificity ≠ generalization)
- "Negative controls guarantee no artifacts" (controls test SOME failure modes, not all)

**Correct framing:**  
Negative controls test harness discrimination power. They do NOT validate S³×S¹ geometry or prove correctness of Gate 4B.

---

## 12. Recommendation

**Next step after pre-registration:**

**Option A (Conservative):** Create implementation plan first  
- Document: `NEGATIVE_CONTROLS_IMPLEMENTATION_PLAN_v0.1.22.md`
- Identify: where S³×S¹ operator is built, how to add controls without touching Gate 4B
- Risk assessment: false-pass likelihood, metric artifact potential
- Then: implement controls

**Option B (Aggressive):** Implement controls immediately  
- Create: `scripts/run_negative_controls_v0_1_22.py`
- Execute: 54-case pilot grid
- Risk: May discover design flaws mid-execution

**Recommended:** **Option A** (implementation plan first)

**Rationale:**  
Negative controls are falsification tests. Design quality matters more than speed. Spend 1 hour planning to avoid wasting 2 hours re-running flawed controls.

---

## 13. Integration with Existing Protocols

### Falsification Ladder
- Negative controls = EstimandOps + FL Standard-Ladder
- EstimandOps L0: Descriptive (no causal claim)
- FL artifacts: claim.md, controls.md, decision.md in `experiments/20260522-negative-controls/`

### Evidence Policy
- All contrast claims: `[VERIFIED-REAL]` with true IPR metric
- Control construction: documented in `control_definitions.md`
- No synthetic validation theater

### Submission Gate
- Does NOT apply (internal validation layer only)
- IF results published externally later → Gate applies then

---

**Pre-registration Date:** 2026-05-22  
**Status:** FINAL  
**Next Review:** Before execution (after implementation plan created)
