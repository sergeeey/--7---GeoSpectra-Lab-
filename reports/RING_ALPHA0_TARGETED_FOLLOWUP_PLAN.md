# Ring / Alpha=0 Targeted Follow-Up Plan

**Purpose:** Investigate ring family alpha=0 fragility before v0.1.15 baseline promotion  
**Baseline:** `v0.1.14-mvp-s2-s1-discretization-v2-full` (unchanged)  
**Status:** Planning-only (implementation pending decision)  
**Date:** 2026-05-16

---

## Purpose

This targeted follow-up is required before v0.1.15 promotion per **Option C** (stricter baseline promotion criteria) from `reports/V0_1_15_CANDIDATE_REVIEW.md`.

**Primary questions:**
1. Are the 37 complete failures a **small-lattice artifact** (s1_size≤24) or **persistent** at larger sizes (64, 96)?
2. Are the 14 window-sensitive cases **fixable** (like historical seeds 12051/12053/9836055) or **inherent** to ring discretization?
3. Does ring failure rate **decrease** with lattice size (scaling toward continuum) or **persist** (fundamental discretization limitation)?
4. Is the 8.3% failure rate **acceptable** for a documented caveat, or does it indicate a **systemic issue** requiring ring deprecation at alpha=0?

**Decision impact:**
- If failures vanish at s1_size≥64 → promote with minimal caveat label (small-lattice artifact documented)
- If failures persist → promote with explicit `-ring-alpha0-caveat` label OR deprecate ring for alpha=0
- If window-sensitive cases fixable → apply fixes, reduce caveat scope
- If v2/v3 disagreement resolved → strengthen gate confidence

**Estimated effort:** 1–2 weeks (targeted diagnostic + analysis + documentation)

---

## Source Evidence

### Full-Run Result (6615 cases)

**Completed:** `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/` (2026-05-15)

**Overall verdict:** `PASS_WITH_LOCAL_CAVEATS`

**Core gates:**
- ✅ q=0 false positives: 0
- ✅ Hermiticity: all passed
- ✅ Reproducibility: all passed
- ✅ q=0 controls: all passed

**Cross-family robustness:**
- `spectral_circle`: **0 disordered failures** (5670 cases tested)
- `wilson_ring`: **0 disordered failures** (5670 cases tested)
- `ring`: **51 disordered failures** (5670 cases tested) — **100% localized to alpha=0.0**

### Caveat Breakdown (Verified from Independent Audit)

**Ring alpha=0 failures:** 51 out of ~630 ring alpha=0 disordered cases (8.3% failure rate, 0.77% of total grid)

**Breakdown:**
- **37 complete failures (73%):** kernel_only=False AND fixed_window=False
- **14 window-sensitive (27%):** kernel_only=False, fixed_window=True (historical window-selection pattern)

**Parameter concentration (all 51 failures):**
- **s1_size:** Small lattices (s1_size≤24: 86% of failures)
- **Disorder:** Lower-to-moderate (W≤6.0: 82% of failures)
- **Monopole:** Spread across all q values

**14 window-sensitive cases specifically:**
- **s1_size:** {8: 10, 24: 4}
- **Disorder:** W=12.0 (6 cases, 43% of window-sensitive) — notably at strong disorder

**v2/v3 disagreements:** 7 cases (all ring alpha=0, v2 passes but v3 fails)

**Source:** `reports/FULL_CAVEAT_ANALYSIS.md`, `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_INDEPENDENT_AUDIT.md`

---

## Hypotheses

### Hypothesis 1: Small-Lattice Artifact

**Claim:** Failures concentrate at s1_size≤24 due to insufficient spectral resolution or discretization artifacts at coarse resolution. Larger sizes (64, 96) will show lower failure rate.

**Evidence for:**
- 86% of failures at s1_size≤24
- Only 6% at s1_size=32, 6% at s1_size=48

**Evidence against:**
- Some failures persist at s1_size=48 (3 cases)
- Window-sensitive cases: 43% at W=12.0 (strong disorder) — not typical small-lattice pattern

**Test:** Run ring alpha=0 at s1_size={64, 96} with same disorder/q grid. If failure rate drops to <2%, confirm small-lattice artifact.

**Implication if confirmed:** Caveat label includes "small-lattice" qualifier. Ring acceptable for s1_size≥64 at alpha=0.

---

### Hypothesis 2: Alpha=0 Periodic Degeneracy

**Claim:** Alpha=0 (periodic boundary, closed circle) creates spectral degeneracy in ring discretization that breaks localization gate logic.

**Evidence for:**
- 100% of failures at alpha=0.0, 0% at alpha=0.5
- Ring discretization may have boundary condition implementation difference from spectral_circle/wilson_ring

**Evidence against:**
- Spectral_circle and wilson_ring also use alpha=0.0 periodic boundary — no failures
- If degeneracy were universal, would affect all families

**Test:** Compare ring vs spectral_circle eigenvalue spectra at matched (q, s1_size, alpha=0.0, W, seed) cases. Check for spectral degeneracy differences.

**Implication if confirmed:** Ring boundary condition implementation issue. May be fixable via numerical stability improvements (like historical seeds).

---

### Hypothesis 3: Ring Discretization Boundary Issue

**Claim:** Ring discretization construction at periodic boundary (alpha=0) has numerical instability or definition issue distinct from spectral_circle/wilson_ring.

**Evidence for:**
- Failures 100% ring, 0% spectral_circle/wilson_ring
- Historical window-selection sensitivity (seeds 12051/12053/9836055) was ring-specific, resolved via numerical stability improvements
- 14 window-sensitive cases exhibit same pattern at different seeds

**Evidence against:**
- Some cases pass (91.7% of ring alpha=0 disordered cases pass)
- Failures concentrate on specific parameter combinations (small sizes, moderate disorder), not uniformly

**Test:** Apply numerical stability improvements (as used for historical seeds) to 14 window-sensitive cases. If they resolve, confirms fixability.

**Implication if confirmed:** 14 window-sensitive cases fixable. 37 complete failures remain (may be Hypothesis 1 or 4).

---

### Hypothesis 4: Transition-Disorder Sensitivity (W=2.0–6.0)

**Claim:** Ring alpha=0 is numerically fragile in transition regime (W=2.0–6.0) where disorder is neither weak nor strong. Anderson localization threshold effects.

**Evidence for:**
- 82% of failures at W≤6.0
- Lower failure count at W=12.0 (9 cases, 18%)

**Evidence against:**
- 14 window-sensitive cases: 43% at W=12.0 (contradicts "low-moderate only" pattern)
- Spectral_circle and wilson_ring have no failures at W=2.0–6.0

**Test:** Extend disorder grid to W={16.0, 20.0, 24.0} to check if pattern continues. Compare ring vs spectral_circle at matched W=4.0 cases.

**Implication if confirmed:** Ring caveat includes "transition-regime" qualifier. May be acceptable if strong disorder (W≥12.0) is production use case.

---

### Hypothesis 5: Strong-Disorder Window Effect (14 window-sensitive)

**Claim:** 14 window-sensitive cases (43% at W=12.0) exhibit window definition issue at strong disorder, not fundamental failure.

**Evidence for:**
- Window-sensitive (kernel fail, fixed pass) pattern suggests gate threshold issue, not operator failure
- 43% at W=12.0 — different from 37 complete failures (concentrated at W≤6.0)

**Evidence against:**
- Only 14 cases total — small sample for separate hypothesis
- May be coincidental W=12.0 concentration

**Test:** Adjust window definition/thresholds at W=12.0 and re-test 14 window-sensitive cases. If they resolve, confirms gate calibration issue.

**Implication if confirmed:** v2/v3 gate policy revision. Window-sensitive cases not a ring limitation, but a gate definition artifact.

---

### Hypothesis 6: v2/v3 Gate Mismatch

**Claim:** 7 v2/v3 disagreements (v2 passes, v3 fails) indicate v2 gate is too permissive at ring alpha=0.

**Evidence for:**
- All 7 disagreements are ring alpha=0
- v3 (window-robust) gate tests multiple window sizes, v2 (fixed-window) uses single window
- v2 may miss window-selection sensitivity

**Evidence against:**
- Only 7 cases total (small sample)
- 6 of 7 overlap with the 51 ring alpha=0 failures — not independent issue

**Test:** Re-run v2 and v3 gates on matched spectral_circle cases at same parameters. If spectral_circle shows no v2/v3 disagreements, confirms ring-specific issue.

**Implication if confirmed:** v3 should be primary gate. v2 deprecated or recalibrated. Does not eliminate ring caveat.

---

## Proposed Grid

### Grid Design Philosophy

**Targeted, not comprehensive.** Focus on:
1. Lattice-size scaling (s1_size={64, 96} extension)
2. Failure seed reproduction (known failure seeds from full run)
3. Reference family comparison (spectral_circle/wilson_ring on matched subset only)

**NOT a full-grid re-run.** Total cases estimated: **~500–800** (vs 6615 in full run).

---

### Parameter Grid

| Parameter | Values | Count | Rationale |
|-----------|--------|-------|-----------|
| **s1_family** | `ring` (primary), `spectral_circle`, `wilson_ring` (reference on matched subset) | 3 | Ring is focus; references validate ring-specificity |
| **alpha** | `0.0` only | 1 | Failures 100% at alpha=0.0; no need to test alpha=0.5 |
| **q (monopole)** | `-3, -2, -1, 0, 1, 2, 3` | 7 | Full q range (failures spread across all q) |
| **s1_size** | `8, 16, 24, 32, 48, 64, 96` | 7 | **Key:** Add 64, 96 to test lattice-size scaling |
| **W (disorder)** | `0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0` | 7 | **Key:** Add W=16.0 to test strong-disorder continuation |
| **seed** | Failure seeds from full run + controls | ~5–10 per config | Include known-failure seeds for reproduction |

**Estimated cases (ring only):**
```
7 q × 7 s1_sizes × 7 W × 5 seeds (average) = ~1715 cases (too many)
```

**Reduction strategy:**

1. **Clean controls:** 1 seed per (q, s1_size) → 7 × 7 × 1 = **49 cases**
2. **Failure seed reproduction:** Known 51 failure seeds at original params + extended s1_size → 51 × 2 (original + s1_size=64 or 96) = **~100 cases**
3. **Targeted s1_size scaling:** (q, W, seed) subsets at s1_size={64, 96} → **~200 cases**
4. **Reference family comparison:** spectral_circle and wilson_ring on matched failure seeds only → 51 × 2 = **~100 cases**

**Total estimated:** **~450–500 cases** (ring + references)

---

### Concrete Grid Specification

**Ring primary grid (targeted):**

1. **Clean controls (W=0.0):**
   - q: all 7
   - s1_size: all 7 (8, 16, 24, 32, 48, 64, 96)
   - seed: 42 (single control seed)
   - Count: 7 × 7 × 1 = **49 cases**

2. **Failure seed reproduction at original parameters:**
   - Extract 51 failure (q, s1_size, W, seed) tuples from full-run metrics.json
   - Re-run at exact same parameters (validation check)
   - Count: **51 cases**

3. **Failure seed reproduction at s1_size=64:**
   - Same 51 failure seeds, but with s1_size → 64 (if original s1_size<64)
   - Count: **~40–50 cases** (some failures already at s1_size=48)

4. **Failure seed reproduction at s1_size=96:**
   - Same 51 failure seeds, but with s1_size → 96
   - Count: **51 cases**

5. **Window-sensitive seed reproduction with stability improvements:**
   - 14 window-sensitive seeds at original parameters
   - Apply numerical stability improvements (as used for historical seeds)
   - Count: **14 cases**

6. **Strong disorder extension (W=16.0):**
   - q: {-3, 0, 3} (sample)
   - s1_size: {8, 24, 64, 96}
   - seed: {42, 123} (controls)
   - Count: 3 × 4 × 2 = **24 cases**

**Ring total:** 49 + 51 + 50 + 51 + 14 + 24 = **~240 cases**

**Reference families (matched subset):**

7. **Spectral_circle on failure seeds:**
   - Same 51 failure seeds (q, s1_size, W, seed), spectral_circle family
   - Expect: 0 failures (validation of ring-specificity)
   - Count: **51 cases**

8. **Wilson_ring on failure seeds:**
   - Same 51 failure seeds, wilson_ring family
   - Expect: 0 failures
   - Count: **51 cases**

**Reference total:** 51 + 51 = **102 cases**

**Grand total:** 240 (ring) + 102 (references) = **~340–350 cases**

**Runtime estimate:** ~1–2 hours (vs 16 hours for full 6615-case run)

---

## Metrics

### Per-Case Metrics (All Cases)

| Metric | Type | Purpose |
|--------|------|---------|
| **kernel_only_localization_gate_passed** | bool | Primary gate (adaptive kernel window) |
| **fixed_window_localization_gate_passed** | bool | v2 gate (fixed low-energy window) |
| **localization_gate_v2_passed** | bool | v2 gate alias |
| **window_robust_localization_passed** | bool | v3 gate (multiple window sizes) |
| **localization_gate_v3_classification** | str | v3 classification: `robust_pass`, `fragile_pass`, `fail`, `window_sensitive` |
| **ipr_disordered_mean** | float | Mean IPR in disordered case |
| **ipr_clean_mean** | float | Mean IPR in matched clean control |
| **ipr_contrast_ratio** | float | disordered / clean ratio |
| **v2_vs_v3_disagree** | bool | True if v2=True and v3=False |
| **failure_type** | str | Classification: `complete_failure`, `window_sensitive`, `robust_pass`, `clean_control` |

### Aggregate Metrics (Per s1_size)

| Metric | Purpose |
|--------|---------|
| **failure_rate_by_size** | Track if failures decrease with s1_size |
| **complete_failure_rate_by_size** | Separate complete failures from window-sensitive |
| **window_sensitive_rate_by_size** | Track window-sensitivity scaling |
| **v2_v3_disagreement_rate_by_size** | Gate calibration check |

### Comparison Metrics (Ring vs References)

| Metric | Purpose |
|--------|---------|
| **ring_failure_seeds_in_spectral_circle** | Expect 0 (ring-specificity validation) |
| **ring_failure_seeds_in_wilson_ring** | Expect 0 |
| **eigenvalue_spectrum_diff** | Spectral comparison (degeneracy check) |

---

## Decision Rules

### Rule 1: Small-Lattice Artifact Test

**Condition:** Failure rate at s1_size=64 and s1_size=96 is **<2%** (vs 8.3% at s1_size≤48)

**Classification:** Small-lattice artifact

**Action:**
- Promote to v0.1.15 with minimal caveat label: `v0.1.15-s2-s1-product-discretized-full`
- Release notes: "Ring alpha=0 fragility at small lattices (s1_size≤48) documented. Robust at s1_size≥64."
- Recommendation: Use s1_size≥64 for ring alpha=0, or prefer spectral_circle/wilson_ring

**Threshold rationale:** <2% failure rate is within noise/edge-case tolerance for pedagogical baseline.

---

### Rule 2: Persistent Ring Limitation Test

**Condition:** Failure rate at s1_size=64/96 **remains ≥6%** (comparable to s1_size=32/48)

**Classification:** Persistent ring/alpha=0 discretization limitation

**Action:**
- Promote to v0.1.15 with explicit caveat label: `v0.1.15-s2-s1-product-discretized-full-ring-alpha0-caveat`
- Release notes: "Ring alpha=0 fragility persists across lattice sizes (8.3% failure rate). Spectral_circle and wilson_ring recommended for alpha=0 periodic boundary."
- Recommendation: Deprecate ring for alpha=0 OR document as "experimental, use with caution"

**Threshold rationale:** ≥6% failure rate across sizes indicates fundamental limitation, not artifact.

---

### Rule 3: Window-Sensitive Fixability Test

**Condition:** Numerical stability improvements resolve **≥10 of 14** window-sensitive cases

**Classification:** Window-sensitive cases are fixable (like historical seeds)

**Action:**
- Apply fixes to codebase
- Re-run full validation on fixed seeds
- Update caveat: "51 failures reduced to ~40 after numerical stability improvements"
- Reduce caveat scope in release notes

**Threshold rationale:** ≥71% fix rate (10/14) indicates fixability, not inherent limitation.

---

### Rule 4: Complete Failure Dominance Test

**Condition:** Complete failures (both gates fail) persist at s1_size≥64, window-sensitive cases do not

**Classification:** Complete failures are structural, window-sensitive are gate artifacts

**Action:**
- Accept complete failures as documented limitation
- Revise v2/v3 gate policy (prefer v3)
- Promote with caveat focused on complete failures only

**Implication:** Caveat scope: "37 complete failures at ring alpha=0, concentrated at small lattices and moderate disorder."

---

### Rule 5: Reference Family Clean Test

**Condition:** Spectral_circle and wilson_ring show **0 failures** on matched 51 failure seeds

**Classification:** Failures are ring-specific, not universal alpha=0 issue

**Action:**
- Confirm caveat is localized to ring family
- Recommend spectral_circle or wilson_ring for production at alpha=0
- Ring remains available with documented caveat

**Threshold rationale:** 0 reference failures validates ring-specificity (already observed in full run, but re-validated here).

---

### Rule 6: v2/v3 Gate Mismatch Resolution

**Condition:** v2/v3 disagreements remain at ring alpha=0, absent in spectral_circle/wilson_ring

**Classification:** v2 gate too permissive for ring alpha=0 (or ring has window-sensitivity)

**Action:**
- Establish v3 (window-robust) as primary gate for future validation
- Document v2 limitation in gate policy
- Consider v2 deprecation or recalibration

**Implication:** Gate policy change, not baseline blocking issue.

---

## Acceptance Criteria

### For This Planning Document

- ✅ **Plan created:** This document
- ✅ **No code changes:** Planning-only
- ✅ **No baseline promotion:** Baseline remains v0.1.14
- ✅ **No physical claims:** Scientific non-claims preserved
- ✅ **Next step documented:** Dry-run decision pending

### For Follow-Up Implementation (If Approved)

**Phase 1: Dry-Run (Recommended)**

1. Extract 51 failure seeds from full-run metrics.json
2. Implement targeted grid construction (ring + references)
3. Run on **subset only** (~50 cases) to validate harness
4. Review dry-run results (1–2 hours)
5. Decision: proceed to full targeted run OR revise plan

**Phase 2: Full Targeted Run**

1. Execute full targeted grid (~340–350 cases)
2. Runtime: ~1–2 hours
3. Save artifacts: config.json, metrics.json, data.npz, summary.md
4. Generate diagnostic report

**Phase 3: Analysis & Decision**

1. Apply decision rules (1–6 above)
2. Classify outcome: small-lattice artifact, persistent limitation, fixable, etc.
3. Document findings in RING_ALPHA0_TARGETED_FOLLOWUP_RESULT.md
4. Update V0_1_15_CANDIDATE_REVIEW.md with outcome
5. Make promotion decision

**Phase 4: Promotion (If Outcome Supports)**

1. Tag v0.1.15 with appropriate caveat label (or without if fixes applied)
2. Write release notes
3. Update VALIDATION_STATUS.md, SPECTRAL_REPORT.md, ISSUES_SCIENTIFIC.md
4. Commit and push

**Total timeline:** 1–2 weeks (as estimated in V0_1_15_CANDIDATE_REVIEW.md)

---

## Scientific Non-Claims

**This targeted follow-up investigates discrete operator behavior on toy product manifolds (cutoff=2). It does NOT:**

1. ❌ Prove **continuum compactification** (cutoff=2 far from continuum limit)
2. ❌ Validate **S⁶ or S³×S⁶** geometries (only S²×S¹ tested)
3. ❌ Derive **Standard Model** gauge structure (no chiral fermions, no SU(3)×SU(2)×U(1))
4. ❌ Prove **physical chirality** (topological index ≠ physical chirality without continuum + gauge coupling)
5. ❌ Bypass **Witten vanishing theorem** (toy construction, not rigorous proof)
6. ❌ Bypass **Lichnerowicz theorem** (toy model, not formal mathematical proof)
7. ❌ Validate **real extra-dimensional physics** (pedagogical toy only)

**Scope:** Numerical laboratory for covariant compactification toy mechanisms (Tom Lawrance's framework). Follow-up investigates ring discretization behavior at alpha=0, not physical theory validation.

---

## Next Steps

**Immediate (before implementation):**

1. ✅ **Planning document complete** (this file)
2. ⏳ **Review plan** with project stakeholders
3. ⏳ **Decision:** Implement dry-run OR revise plan OR skip follow-up (accept current caveat, promote with Option B)

**If dry-run approved:**

1. Extract failure seeds from full-run metrics.json
2. Implement grid construction script (modify existing s2_s1_product_discretized.py or create new targeted script)
3. Run dry-run (~50 cases, ~15 minutes)
4. Review dry-run results
5. Decision: proceed to full targeted run

**If full targeted run approved:**

1. Execute ~340–350 case grid (~1–2 hours)
2. Analyze results
3. Apply decision rules
4. Document outcome
5. Make v0.1.15 promotion decision

**If follow-up skipped (Option B from candidate review):**

1. Promote to v0.1.15 with caveated label immediately
2. Accept current caveat (51 failures, 37 both-fail + 14 window-sensitive) as documented limitation
3. Recommend spectral_circle/wilson_ring for production

---

## Baseline Status

**Current baseline:** `v0.1.14-mvp-s2-s1-discretization-v2-full` — **UNCHANGED**

**Awaiting:** Dry-run approval OR skip-to-promotion decision (Option B vs Option C)

---

**Plan completed:** 2026-05-16  
**Status:** Ready for implementation decision  
**Estimated effort:** 1–2 weeks (if full targeted follow-up executed)  
**Blocking issues:** None (plan-only, no code changes)  
**Recommendation:** Implement dry-run first (validate harness on ~50 cases before full ~340-case run)
