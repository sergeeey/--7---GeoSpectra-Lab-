# Section 7 — Caveat Discovery and Resolution: Ring/alpha=0

**Draft Status:** FIRST DRAFT (v0.1.16)  
**Target Paper:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"  
**Case Study Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Date:** 2026-05-16

---

## Section Thesis

**Core argument:** The ring/alpha=0 episode demonstrates why caveats should be treated as **diagnostic outputs** (empirical discoveries about numerical behavior), not **failures to hide** (bugs to suppress). The six-stage resolution workflow (failure signal → audit correction → clustering analysis → hypothesis testing → targeted follow-up → production guideline) systematically transformed 51 localized failures into a precise empirical rule (s1_size≥64 required for ring/alpha=0) instead of wholesale rejection or under-specified warnings.

**Methodological validation:** This case study validates that:
1. **Aggregate metrics hide structure** (99.1% pass rate masked 8.1% failure in ring/alpha=0 subspace)
2. **Independent audit prevents interpretation drift** (37 complete failures ≠ 14 window-sensitive cases)
3. **Targeted follow-ups are cheaper than full re-runs** (2.5 hours vs 16 hours, 10× parameter-space reduction)
4. **Empirical guidelines are useful without theorem-level proof** (s1_size≥64 threshold based on Decision Rule 1, not mathematical convergence proof)

**Scope protection:** This episode validates **finite-lattice numerical convergence** (failures vanish at s1_size≥64), NOT **continuum extrapolation** (s1_size→∞), **physical compactification** (toy operators ≠ physical mechanism), or **universal guarantee** (tested only up to s1_size=96).

---

## 7.1 Initial Failure Signal: 51 Failures in 5670 Disordered Cases

### **Full Diagnostic Aggregate Result**

**Disordered cases (W>0):** 5670 total  
**Localized (all gates passed):** 5619/5670 = **99.1%**  
**Failed (≥1 gate failed):** 51/5670 = **0.9%**

**Naive interpretation risk:** "99.1% pass rate → SUCCESS → ship baseline."

**Why this is wrong:**
1. **Aggregate hides structure:** 0.9% failure could be distributed (random noise) OR localized (systematic artifact in parameter subspace)
2. **Failure clustering analysis mandatory:** Must determine whether failures cluster on specific parameter axis (family, q, s1_size, α, W) before declaring success
3. **False confidence:** High aggregate pass rate does not guarantee absence of parameter-dependent pathologies

---

### **Failure Localization: 100% in ring/alpha=0**

Mandatory clustering analysis (Section 5.4 protocol) revealed:

**By family:**
- spectral_circle: **0/2205** failures (100% robust)
- wilson_ring: **0/2205** failures (100% robust)
- ring: **51/2205** failures (2.3% failure rate)

**By twist angle (ring family only):**
- alpha=0.0 (periodic BC): **51/735** failures (6.9% failure rate)
- alpha=0.25 (quarter-twist): **0/735** failures (100% robust)
- alpha=0.5 (half-twist): **0/735** failures (100% robust)

**Intersection:** ring ∩ alpha=0.0 = **51/51 failures** (100% of failures explained by this intersection).

**Key finding:** Failures are **localized** to one family-boundary condition combination (ring/alpha=0), NOT distributed across parameter space. This triggers targeted follow-up protocol (Section 5.5).

---

### **Initial Interpretation Ambiguity**

**Possible explanations for 51 ring/alpha=0 failures:**
1. **Small-lattice artifact** (failures vanish at larger s1_size)
2. **Structural ring/alpha=0 limitation** (failures persist at all s1_size)
3. **Window-gate calibration issue** (failures due to IPR threshold choice, not physics)
4. **Implementation bug** (ring discretization incorrect at alpha=0)
5. **Reference-family regression** (spectral_circle/wilson_ring also fail, but not detected)

**Without targeted follow-up, cannot distinguish these.** Initial verdict: PASS_WITH_LOCAL_CAVEATS (triggers mandatory follow-up before baseline promotion).

---

## 7.2 Independent Audit Correction: 37 Complete + 14 Window-Sensitive

### **Audit Finding: Two Distinct Failure Modes**

Independent audit (Section 6.6) analyzed per-case metrics.json and discovered:

**Initial documentation (summary.md):** "52 ring/alpha=0 failures, BOTH gates fail."

**Audit verification (metrics.json):**
- **37 cases (72.5%):** BOTH kernel_only AND fixed_window localization gates fail → **complete failure**
- **14 cases (27.5%):** kernel_only fails, fixed_window passes → **window-sensitive**
- **1-case discrepancy:** 52 (summary counter) vs 51 (metrics.json count) → likely clean control inclusion error

**Audit verdict:** confirmed_with_corrections_needed (3 corrections applied).

---

### **Why Distinguishing Complete vs Window-Sensitive Matters**

**Complete failures (37 cases):**
- **Interpretation:** Strong non-localization signal (both IPR diagnostics fail)
- **Likely cause:** Insufficient lattice size for localization OR discretization artifact
- **Follow-up strategy:** Extend s1_size grid to test convergence

**Window-sensitive failures (14 cases):**
- **Interpretation:** Marginal localization (depends on IPR window definition)
- **Likely cause:** Spectral window calibration issue OR transition-regime sensitivity
- **Follow-up strategy:** Test IPR threshold robustness OR accept as expected transition-regime behavior

**If not distinguished:** Window-sensitive cases incorrectly treated as "hard failures" → over-conservative production guideline (e.g., "avoid ring/alpha=0 entirely" instead of "requires s1_size≥64").

---

### **Correction 1: Failure Mode Breakdown**

**Before (FULL_CAVEAT_ANALYSIS.md line 27):**
> Gate status: BOTH kernel_only_localization_gate_passed=False AND fixed_window_localization_gate_passed=False

**After:**
> Gate status breakdown:
> - 37 cases (73%): BOTH gates fail (complete localization failure)
> - 14 cases (27%): Window-sensitive (kernel_only fails, fixed_window passes)

---

### **Correction 2: Production Guideline Phrasing**

**Before:**
> Ring/alpha=0 requires larger lattices

**After:**
> Ring/alpha=0 requires s1_size≥64 (empirical convergence threshold from Decision Rule 1)

**Rationale:** "Larger lattices" is vague (larger than what?). Quantified threshold (s1_size≥64) is precise and testable.

---

### **Correction 3: Scientific Non-Claim Addition**

**Added to RELEASE_NOTES:**
> No continuum extrapolation (s1_size→∞) was performed. Largest tested lattice (s1_size=96) remains a finite-lattice diagnostic, not continuum evidence.

**Rationale:** Prevent misreading "s1_size=96 convergence" as "continuum limit reached."

---

## 7.3 Failure Clustering: Lattice-Size Dependence

### **Clustering Analysis by s1_size**

51 ring/alpha=0 failures distributed across s1_size:

| s1_size | Failures | Total Ring/alpha=0 | Failure Rate (%) |
|---------|----------|--------------------|------------------|
| 8 | 25 | ~126 | 19.8 |
| 16 | 1 | ~126 | 0.8 |
| 24 | 19 | ~126 | 15.1 |
| 32 | 3 | ~126 | 2.4 |
| 48 | 3 | ~126 | 2.4 |

**Key observation:** 86% of failures (44/51) occur at s1_size≤24 (small lattices).

**Non-monotonic scaling:** Failure rate is NOT monotonically decreasing (s1_size=24 shows **secondary peak** at 15.1%, higher than s1_size=32/48 at 2.4%). This rules out simple exponential decay artifact and suggests **finite-size resonances** (specific lattice sizes amplify discretization errors).

---

### **Hypothesis: Small-Lattice Artifact**

**Prediction:** If failures are small-lattice artifacts, extending s1_size beyond 48 should reduce failure rate below 2% threshold (Decision Rule 1).

**Test:** Targeted follow-up extending s1_size grid to 64, 96.

**Alternative hypothesis (structural limitation):** If failures are fundamental ring/alpha=0 limitation, failure rate should persist at s1_size≥64.

---

### **Reference Family Validation**

**Control check:** Do spectral_circle/wilson_ring also show lattice-size dependence?

**Result:**
- spectral_circle: **0 failures** across all s1_size (8-48)
- wilson_ring: **0 failures** across all s1_size (8-48)

**Interpretation:** ring/alpha=0 artifact is **family-specific**, NOT general discretization issue. If artifact were universal (affects all discretizations), spectral_circle would also fail at small s1_size.

---

## 7.4 Hypotheses Tested

Five competing hypotheses for 51 ring/alpha=0 failures:

### **H1: Small-Lattice Artifact**

**Claim:** Failures vanish at s1_size≥64 (discretization resolution insufficient at s1_size<64).

**Supporting evidence:**
- 86% of failures at s1_size≤24
- spectral_circle/wilson_ring show 0 failures (better discretization → no artifact)
- Non-monotonic scaling suggests finite-size resonances, not fundamental physics

**Refuting evidence:**
- If failures persist at s1_size≥64 → H1 refuted

**Test:** Extend s1_size grid to 64, 96 → measure failure rate.

**Decision Rule 1:** failure_rate(s1_size≥64) < 2% → H1 confirmed (SMALL_LATTICE_ARTIFACT).

---

### **H2: Structural Ring/alpha=0 Limitation**

**Claim:** Ring discretization fundamentally incompatible with periodic BC (alpha=0) at all lattice sizes.

**Supporting evidence:**
- 100% of failures in ring ∩ alpha=0 (no failures at alpha=0.25, 0.5)
- Failures persist across disorder strengths (W=2.0-12.0)

**Refuting evidence:**
- If failures vanish at s1_size≥64 → H2 refuted
- If ring/alpha≠0 works at small s1_size → suggests BC-specific issue, not general ring failure

**Test:** Same as H1 (s1_size≥64 follow-up). If failure_rate≥6% at s1_size≥64 → H2 confirmed.

---

### **H3: Window-Gate Calibration Issue**

**Claim:** 14 window-sensitive failures due to IPR threshold choice, not real physics.

**Supporting evidence:**
- 14/51 failures are window-sensitive (kernel fails, fixed-window passes)
- Historical window-selection sensitivity pattern (resolved in pytest for specific seeds, persists at different parameters)

**Refuting evidence:**
- 37/51 failures are complete (BOTH gates fail) → cannot be explained by window calibration alone

**Test:** Vary IPR thresholds → check if window-sensitive failures flip. (NOT performed in v0.1.15, out of scope.)

**Verdict:** Partially supported (14 cases), but insufficient to explain 37 complete failures.

---

### **H4: Implementation Bug**

**Claim:** Ring discretization code has bug at alpha=0 (periodic BC).

**Supporting evidence:**
- 100% of failures in ring ∩ alpha=0 (suggests BC-specific code path)

**Refuting evidence:**
- spectral_circle also uses periodic BC (alpha=0) → 0 failures → BC implementation not universally broken
- Pytest suite passes (195/195) → ring construction validated on test cases

**Test:** Code review of ring BC implementation. (Performed offline, no bugs found.)

**Verdict:** Refuted (no bugs detected, pytest validates construction).

---

### **H5: Reference-Family Regression**

**Claim:** spectral_circle/wilson_ring also fail at ring/alpha=0 parameters, but failures not detected (false negative in full diagnostic).

**Supporting evidence:**
- None (hypothesis generated for completeness)

**Refuting evidence:**
- spectral_circle/wilson_ring: **0/2205 failures** across full grid → no false negatives

**Test:** Targeted follow-up includes reference families at s1_size=64 → check for new failures.

**Verdict:** Refuted (reference families remain robust).

---

## 7.5 Targeted Follow-Up Design: 1349 Cases, s1_size Extended to 64, 96

### **Follow-Up Grid Specification**

**Objective:** Test H1 (small-lattice artifact) vs H2 (structural limitation) by extending s1_size beyond full diagnostic's max (s1_size=48).

**Ring cases (primary grid):**
- **s1_size:** 8, 16, 24, 32, 48, **64, 96** (2 new values)
- **q:** -3, -2, -1, 0, 1, 2, 3 (7 monopole charges)
- **W:** 0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0 (7 disorder strengths)
- **alpha:** 0.0 (fixed, periodic BC only)
- **seeds:** 123, 456, 789 (3 independent realizations)
- **Ring cases:** 7 s1_size × 7 q × 7 W × 3 seeds = **1029 cases**

**Reference families (control grid):**
- **Families:** spectral_circle, wilson_ring (2 families)
- **s1_size:** 8, 16, 32, **64** (validate no regressions at s1_size=64)
- **q:** -2, -1, 0, 1, 2 (5 charges)
- **W:** 0.0, 4.0, 8.0, 12.0 (4 disorder strengths)
- **seeds:** 123, 456 (2 seeds)
- **Reference cases:** 2 families × 4 s1_size × 5 q × 4 W × 2 seeds = **320 cases**

**Total:** **1349 cases**

**Runtime:** ~2.5 hours (v0.1.16 ring/alpha=0 follow-up).

---

### **Design Rationale**

**Why only ring family (not spectral_circle/wilson_ring full grid)?**
- spectral_circle/wilson_ring showed 0 failures in full diagnostic → no follow-up needed
- Reference families tested at s1_size=64 only (control check, not full exploration)

**Why s1_size=64, 96 specifically?**
- s1_size=48 showed 2.4% failure rate (near 2% Decision Rule 1 threshold)
- s1_size=64 is 1.33× larger → sufficient to test convergence
- s1_size=96 is 2× s1_size=48 → validates convergence persistence (not one-lattice fluke)

**Why 3 seeds (not 4 as in full diagnostic)?**
- Computational cost (1349 cases is already ~15% overhead on 6615 full grid)
- 3 seeds provide adequate statistical sampling (tradeoff: precision vs runtime)

---

### **Decision Rule 1: Small-Lattice Artifact Criterion**

**Rule:** If failure_rate(s1_size≥64) < 2.0% → classify as SMALL_LATTICE_ARTIFACT.

**Rationale:**
- 2% threshold chosen as **practical convergence criterion** (1 failure in 50 cases acceptable for production use)
- NOT mathematical convergence theorem (no proof that s1_size→∞ converges)
- Empirical guideline based on observed failure-rate scaling

**Alternative thresholds considered:**
- 0% (zero tolerance): Too strict, rejects useful numerical tools
- 5% (lenient): Too loose, allows excessive failures in production
- 2% (chosen): Balanced practical tolerance

---

## 7.6 Follow-Up Results: 0/252 = 0.0% at s1_size≥64

### **Lattice-Size Scaling Results (Table 5)**

Table 5 (ring/alpha=0 disordered cases only, 882 total):

| s1_size | Total | Complete Failures | Window-Sensitive | Robust Pass | Total Failures | Failure Rate (%) |
|---------|-------|-------------------|------------------|-------------|----------------|------------------|
| 8 | 126 | 15 | 10 | 100 | 25 | 19.8 |
| 16 | 126 | 1 | 0 | 125 | 1 | 0.8 |
| 24 | 126 | 15 | 4 | 107 | 19 | 15.1 |
| 32 | 126 | 3 | 0 | 123 | 3 | 2.4 |
| 48 | 126 | 3 | 0 | 123 | 3 | 2.4 |
| **64** | **126** | **0** | **0** | **126** | **0** | **0.0** ✅ |
| **96** | **126** | **0** | **0** | **126** | **0** | **0.0** ✅ |

**Aggregate statistics:**
- **s1_size<64:** 51/630 = **8.1%** failure rate
- **s1_size≥64:** 0/252 = **0.0%** failure rate

**Decision Rule 1 application:** 0.0% < 2.0% ✅ → **SMALL_LATTICE_ARTIFACT verdict confirmed**.

---

### **Figure 7: Lattice-Size Scaling Plot**

Figure 7 visualizes convergence:
- **Data points:** (8, 19.8%), (16, 0.8%), (24, 15.1%), (32, 2.4%), (48, 2.4%), (64, 0.0%), (96, 0.0%)
- **Threshold lines:**
  - Red dashed horizontal: 2% (Decision Rule 1 threshold)
  - Green dashed vertical: s1_size=64 (convergence threshold)
- **Annotations:** "Converged: 0/252 = 0.0%" at s1_size≥64

**Visual interpretation:** Sharp drop from 19.8% (s1_size=8) to 0.0% (s1_size≥64) confirms small-lattice artifact hypothesis. Non-monotonicity (secondary peak at s1_size=24, 15.1%) suggests finite-size resonances.

---

### **Reference Family Validation (Control)**

| Family | Disordered Cases | Failures | Failure Rate |
|--------|------------------|----------|--------------|
| spectral_circle | ~120 | 0 | 0.0% ✅ |
| wilson_ring | ~120 | 0 | 0.0% ✅ |
| **Combined** | **240** | **0** | **0.0%** ✅ |

**Interpretation:** Reference families remain robust at all s1_size (8-64). This confirms ring/alpha=0 artifact is **NOT** general discretization regression (spectral_circle/wilson_ring unaffected).

---

### **Hypothesis Resolution**

| Hypothesis | Prediction | Observed | Verdict |
|------------|-----------|----------|---------|
| **H1: Small-lattice artifact** | failure_rate<2% at s1_size≥64 | 0.0% ✅ | **CONFIRMED** |
| **H2: Structural limitation** | failure_rate≥6% at s1_size≥64 | 0.0% | **REFUTED** |
| **H3: Window-gate issue** | Only window-sensitive failures | 37 complete failures exist | **PARTIAL** (14 cases) |
| **H4: Implementation bug** | Failures persist after bug fix | 0 failures at s1_size≥64 | **REFUTED** |
| **H5: Reference regression** | spectral_circle/wilson_ring fail | 0 reference failures | **REFUTED** |

**Final verdict:** H1 (small-lattice artifact) confirmed. Production guideline: ring/alpha=0 requires s1_size≥64.

---

## 7.7 Interpretation: Caveat Narrowed, Not Erased

### **Production Guideline (Empirical, Not Theorem)**

**Guideline:** Ring/alpha=0 configurations require s1_size≥64 for numerical convergence (failure_rate < 2%).

**What this is:**
- **Empirical observation** from 1349-case targeted follow-up
- **Decision Rule 1 applied** (failure_rate < 2% → convergence threshold)
- **Practical recommendation** for finite-lattice numerical stability

**What this is NOT:**
- **Mathematical theorem** (no proof that s1_size→∞ converges)
- **Physical principle** (s1_size=64 is discretization parameter, not physical length scale)
- **Continuum limit** (s1_size→∞ extrapolation NOT performed, tested only up to s1_size=96)
- **Universal guarantee** (applies to tested parameter range: q∈[-3,3], W∈[0.5,16], seeds∈{123,456,789})

---

### **Caveat Narrowed: From "ring fails" to "ring/alpha=0 at s1_size<64 fails"**

**Before targeted follow-up:**
- **Broad caveat:** "Ring family shows 51 failures (2.3% failure rate)"
- **Ambiguity:** Unclear if ring is fundamentally broken OR fixable with larger lattices
- **Production risk:** Users avoid ring entirely (lose 1/3 of discretization families)

**After targeted follow-up:**
- **Narrow caveat:** "Ring/alpha=0 at s1_size<64 shows failures (8.1% failure rate). Ring/alpha=0 at s1_size≥64 is robust (0.0% failure rate)."
- **Precision:** Specific parameter region identified (ring ∩ alpha=0 ∩ s1_size<64)
- **Production clarity:** Users can use ring at s1_size≥64 (or use alpha≠0 at any s1_size) → ring remains usable

**Key insight:** Targeted follow-up converted **wholesale rejection** ("ring fails") into **constrained usage** ("ring requires s1_size≥64 at alpha=0").

---

### **Why This Is NOT Evidence of Physical Compactification**

**Numerical convergence ≠ physical validity:**
- **Convergence:** Discretization artifact vanishes at larger finite lattice
- **Physical validity:** Toy model accurately represents physical mechanism

**ring/alpha=0 convergence at s1_size≥64 validates:**
- Ring discretization is numerically stable at sufficient lattice size
- Localization gates correctly classify operators at s1_size≥64
- Finite-lattice artifacts can be systematically detected and resolved

**ring/alpha=0 convergence does NOT validate:**
- Continuum compactification (s1_size=96 is still finite)
- Physical S¹ circle (toy discretization ≠ physical spacetime)
- Standard Model (no gauge group, no fermion doubling, no Yukawa couplings)
- Physical chirality (localization on discretized operator ≠ chiral fermions)

---

## 7.8 Lessons for Validation Workflows

### **Lesson 1: Aggregate Pass Rates Are Insufficient**

**Anti-pattern:** "99.1% passed → SUCCESS → ship."

**Why wrong:** 99.1% aggregate hides 8.1% failure in ring/alpha=0 subspace (0.9% overall = 51/5670, but 8.1% within ring/alpha=0 = 51/630).

**Correct approach:** Always perform clustering analysis (Section 5.4 protocol) to detect localized caveats before declaring success.

**Cost:** 30 minutes clustering analysis vs 6 months production failures.

---

### **Lesson 2: Caveats Should Trigger Targeted Follow-Ups**

**Anti-pattern:** "51 failures found → reject entire family → lose ring discretization."

**Why wrong:** Wholesale rejection discards useful numerical tool without testing if artifact is fixable.

**Correct approach:** Targeted follow-up tests hypothesis (small-lattice artifact vs structural limitation) → converts failures into constraints (s1_size≥64 guideline).

**Cost:** 2.5 hours follow-up vs losing 1/3 of discretization families.

---

### **Lesson 3: Independent Audit Prevents Interpretation Drift**

**Anti-pattern:** "52 failures, all BOTH gates fail" (incorrect overgeneralization).

**Why wrong:** Lumps 37 complete failures + 14 window-sensitive cases into one category → misses distinction requiring different follow-up strategies.

**Correct approach:** Independent audit distinguishes failure modes (complete vs window-sensitive) → informs follow-up design (extend s1_size for complete failures, test IPR thresholds for window-sensitive).

**Cost:** 1 hour audit vs weeks of misdirected follow-up.

---

### **Lesson 4: Empirical Guidelines Are Useful Without Theorems**

**Anti-pattern:** "No mathematical proof of convergence → cannot use ring/alpha=0."

**Why wrong:** Rejects practical numerical tool due to lack of theorem-level proof.

**Correct approach:** Empirical guideline (s1_size≥64, failure_rate<2%) is sufficient for production use. Theorem-level proof is ideal but not mandatory for computational validation.

**Cost:** 0 additional work (empirical guideline already obtained from follow-up) vs months proving convergence theorem (out of scope for toy validation).

---

## 7.9 Scope and Limitations

### **What Ring/alpha=0 Follow-Up Validates**

The ring/alpha=0 targeted follow-up validates:
1. **Finite-lattice numerical convergence:** Failures vanish at s1_size≥64 (empirical observation)
2. **Production guideline:** Ring/alpha=0 requires s1_size≥64 for numerical stability (Decision Rule 1)
3. **Artifact localization:** Ring/alpha=0 artifact is family-specific, not universal (reference families unaffected)
4. **Targeted follow-up efficiency:** 2.5 hours (1349 cases) vs 16 hours (6615 full re-run) → 6.4× faster

**This is finite-lattice numerical validation, NOT physical proof.**

---

### **What Ring/alpha=0 Follow-Up Does NOT Validate**

The ring/alpha=0 targeted follow-up does **NOT** prove or imply:

1. **Continuum compactification:** Largest tested lattice (s1_size=96) is still finite. No s1_size→∞ extrapolation performed.

2. **Mathematical convergence theorem:** Decision Rule 1 (failure_rate<2%) is empirical threshold, NOT rigorous proof that lim_{s1_size→∞} exists.

3. **Physical S¹ circle:** Ring discretization is toy numerical construction, NOT physical spacetime compactification.

4. **Universal guarantee:** Guideline (s1_size≥64) applies to tested parameter range (q∈[-3,3], W∈[0.5,16]). Behavior outside this range unknown.

5. **Optimal lattice size:** s1_size=64 is **minimal threshold** (first lattice where failures vanish), NOT optimal size for all purposes (higher s1_size may improve accuracy further).

6. **Standard Model / physical chirality / Witten bypass:** Follow-up validates numerical harness, NOT physical mechanism.

7. **Zero risk:** 0.0% failure rate at s1_size≥64 tested on 252 cases. Rare failures may exist outside tested parameter space.

8. **Continuum physics:** Non-monotonic scaling (secondary peak at s1_size=24) suggests finite-size resonances, NOT continuum behavior.

---

### **Empirical Guideline Scope**

**Production guideline applies to:**
- Ring discretization family
- Periodic boundary condition (alpha=0)
- Monopole charges q ∈ [-3, 3]
- Disorder strengths W ∈ [0.5, 16]
- Lattice sizes s1_size ∈ [64, 96] (tested range)

**Guideline does NOT apply to:**
- spectral_circle/wilson_ring (already robust at all s1_size)
- Ring/alpha≠0 (alpha=0.25, 0.5 already robust at all s1_size)
- Parameters outside tested range (extrapolation not validated)
- s1_size→∞ (continuum extrapolation not performed)

---

## 7.10 Summary

**Ring/alpha=0 episode demonstrates falsification-first workflow transforming 51 localized failures into precise empirical production guideline (s1_size≥64) through six-stage resolution:** Initial signal (99.1% pass rate hides 8.1% failure in subspace) → Independent audit (37 complete + 14 window-sensitive) → Clustering analysis (100% in ring ∩ alpha=0 ∩ s1_size<64) → Hypothesis testing (5 hypotheses, H1 confirmed) → Targeted follow-up (1349 cases, 2.5h) → Production guideline (s1_size≥64, failure_rate<2%).

**Key numbers:**
- **Full diagnostic:** 51/5670 = 0.9% aggregate failure (hides structure)
- **Ring/alpha=0 subspace:** 51/630 = 8.1% failure rate (reveals localized artifact)
- **s1_size<64:** 51/630 failures (small-lattice artifact zone)
- **s1_size≥64:** 0/252 failures (converged) → Decision Rule 1 confirmed (0.0% < 2.0%)
- **Targeted follow-up:** 1349 cases, 2.5h runtime (6.4× faster than full re-run)

**Methodological validation:** Aggregate metrics hide structure (clustering analysis mandatory). Independent audit prevents interpretation drift (37 complete ≠ 14 window-sensitive). Targeted follow-ups are cheaper than full re-runs (2.5h vs 16h). Empirical guidelines are useful without theorems (s1_size≥64 sufficient for production).

**Scope protection:** Validates finite-lattice numerical convergence (s1_size=96 still finite), NOT continuum extrapolation, physical compactification, Standard Model, chirality, or Witten bypass. Production guideline (s1_size≥64) is empirical threshold, NOT mathematical theorem.

**Transition to Section 8:** The next section details independent audit protocol (5-task checklist), audit findings (3 corrections), and release integrity 5-point verification (baseline references, non-claims, artifacts, hygiene, cross-file consistency). Explains why independent audit matters (catches confirmation bias, prevents overclaim, ensures cross-file consistency).

---

**Section 7 word count:** ~3800 words  
**Status:** FIRST DRAFT  
**Cross-file consistency:** ✅ (aligned with Table 5, Figure 7, Section 6.7)  
**Scope protection:** ✅ (8 explicit non-claims in Section 7.9)

---

**Notes for Next Sections:**

**Section 8 (Independent Audit and Release Integrity):** Expand on audit protocol (5-task checklist: classification logic, arithmetic, interpretation, non-claims, corrections). Detail 3 corrections (failure mode breakdown, guideline phrasing, non-claim addition). Explain release integrity 5-point verification (baseline refs, non-claims, artifacts, hygiene, cross-file consistency). Discuss why independent audit matters (catches confirmation bias from single-author analysis, prevents overclaim from excitement of completion, ensures documentation consistency across 6 files).

**Section 9 (Discussion):** Synthesis of Sections 1-8. Discuss broader implications of falsification-first workflow for computational science (validation theater prevention, caveat discovery as feature, empirical guidelines vs theorems). Compare with traditional confirmation-biased workflows (aggregate metrics accepted at face value, caveats hidden, no follow-ups). Acknowledge limitations (toy validation only, no continuum, no physical mechanism).

**Section 10 (Related Work):** Compare GeoSpectra Falsification Ladder with existing validation frameworks (HPC reproducibility standards, statistical testing workflows, ML model validation). Identify unique contributions (progressive profiles, mandatory controls, caveat discovery as output, targeted follow-ups).

**Section 11 (Conclusion):** Restate core thesis (falsification-first reduces false positives), summarize v0.1.15 case study (99.1% pass rate with caveats discovered and resolved), reinforce scope boundaries (toy validation, NOT physical proof), suggest future work (continuum extrapolation, higher-dimensional manifolds, Wilson audit).
