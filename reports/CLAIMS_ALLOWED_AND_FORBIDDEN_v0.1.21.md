# Claims Allowed and Forbidden — v0.1.21

**Date:** 2026-05-22  
**Scope:** Gate 4B v0.1.21 metric-corrected results  
**Verdict:** GATE4B_FSS_PASS_WITH_CAVEATS  
**Status:** FINAL

---

## Allowed Claim (Canonical Statement)

**Primary claim:**

> **"S³×S¹ Gate 4B supports finite-lattice robustness of the W=20 Anderson disorder localization signal under finite-size scaling from s1_size=16 to 128 (N = 112 to 896), with true eigenvector-based IPR contrast ≥2.0× and family consistency ≥2/3."**

**With mandatory caveats:**
- Finite-lattice only (N ≤ 896)
- Anderson disorder only (diagonal on-site U(r) ∈ [-W, W])
- S³×S¹ only (no FL generalization)
- W=20 exploratory (not optimal)
- True IPR metric (v0.1.21, not comparable with v0.1.20)
- No physical compactification claim

---

## Allowed Claims (Expanded)

### 1. Finite-Lattice Robustness ✅

**Allowed:**
- "Gate 4B supports finite-lattice robustness of W=20 localization signal on S³×S¹"
- "True IPR contrast strengthens with lattice size (N = 112 → 896)"
- "No finite-size collapse observed in tested range"
- "Signal is NOT a finite-size artifact within N ≤ 896"

**Rationale:** FSS trend STRENGTHENING (3.76× → 24.90×), all pre-registered conditions satisfied.

---

### 2. Family Consistency ✅

**Allowed:**
- "All three discretization families confirm W=20 contrast ≥2.0×"
- "spectral_circle: 4.25×, ring: 8.31×, wilson_ring: 8.49×"
- "No single-family domination (max 36% of aggregate contrast)"

**Rationale:** 3/3 families PASS independently, no discretization artifact.

---

### 3. r-Statistic Diagnostic ✅

**Allowed:**
- "r-statistic diagnostic consistent with localization interpretation"
- "r-statistic is consistent with the true-IPR localization interpretation"
- "r-statistic does not contradict the true-IPR signal"
- "Level-spacing statistics agree with IPR finding on W=20 direction"

**Rationale:** r-statistic shifts from near-GOE (W=0) toward Poisson (W=20), consistent with IPR contrast.

**Forbidden wording:**
- ❌ "r-statistic confirms localization" (too strong)
- ❌ "r-statistic proves localization" (too strong)
- ❌ "r-statistic supports localization" (prefer "consistent with")
- Use: "consistent with" or "does not contradict"

---

### 4. Metric Correction ✅

**Allowed:**
- "v0.1.21 measures true eigenvector-based IPR (Σ|ψᵢ|⁴)"
- "v0.1.20 used invalid metric (eigenvalue mean)"
- "v0.1.21 results NOT comparable with v0.1.20"
- "v0.1.20 verdict remains WEAK (no retroactive upgrade)"

**Rationale:** Metric mismatch documented, recovery protocol executed, no confusion between versions allowed.

---

### 5. Control Baseline ✅

**Allowed:**
- "W=0 baseline stable (max CV = 0.190 < 0.2)"
- "W=0 shows expected 1/N scaling"
- "No numerical instability in controls"

**Rationale:** Controls passed stability check, no implementation errors detected.

---

## Forbidden Claims (Hard Block)

### 1. ❌ "S³×S¹ Validated"

**Why forbidden:** "Validated" implies no further testing needed, universal applicability, or gold-standard confirmation. Gate 4B is ONE finite-lattice grid with ONE disorder model at ONE W value. NOT validation.

**Correct alternative:** "Gate 4B supports finite-lattice robustness"

---

### 2. ❌ "FL Generalized" / "Arbitrary FL×S¹"

**Why forbidden:** Only S³×S¹ tested. No data for S²×S¹, S⁷×S¹, or other FL geometries.

**Correct alternative:** "S³×S¹ only (no FL generalization)"

---

### 3. ❌ "W=20 Optimal"

**Why forbidden:** W=20 chosen from Gate 3C exploratory finding, NOT from systematic W-sweep. No data for W=25, W=30, etc.

**Correct alternative:** "W=20 exploratory (not optimal)"

---

### 4. ❌ "Thermodynamic Limit Proven" / "N→∞"

**Why forbidden:** Max N = 896. Thermodynamic limit requires N→∞ analysis (e.g., finite-size scaling extrapolation, which was NOT done). Trend strengthening ≠ proof of infinite-N behavior.

**Correct alternative:** "Finite-lattice only (N ≤ 896, no thermodynamic limit)"

---

### 5. ❌ "Physical Compactification" / "4D Spacetime"

**Why forbidden:** Finite-lattice discretization ≠ continuum S³×S¹ manifold. No claim about physical Kaluza-Klein compactification, 4D gravity, or Standard Model physics.

**Correct alternative:** "Computational model only (no physical compactification claim)"

---

### 6. ❌ "Standard Model" / "Chirality" / "Gauge Fields"

**Why forbidden:** Toy Hamiltonian with scalar wavefunctions. No chiral fermions, no gauge field coupling, no electroweak/strong interactions.

**Correct alternative:** Do not mention Standard Model, chirality, or gauge fields in any positive claim context.

---

### 7. ❌ "Paradigm Shift" / "Breakthrough" / "Revolutionary"

**Why forbidden:** Validation theater. Gate 4B is an exploratory finite-lattice grid, not a paradigm shift.

**Correct alternative:** "Exploratory finding" or "Pilot result"

---

### 8. ❌ "Localization Proven"

**Why forbidden:** Gate 4B measures IPR contrast and r-statistic diagnostics. These are consistent with localization interpretation, but do NOT prove localization in the mathematical sense (e.g., exponential decay of eigenfunctions).

**Correct alternative:** "IPR contrast supports localization interpretation"

---

### 9. ❌ "v0.1.20 Reinterpreted" / "v0.1.20 Confirms v0.1.21"

**Why forbidden:** v0.1.20 metric was invalid. Cannot retroactively reinterpret eigenvalue mean as IPR. v0.1.20 verdict remains WEAK regardless of v0.1.21 result.

**Correct alternative:** "v0.1.20 invalid, v0.1.21 independent rerun with corrected metric"

---

### 10. ❌ "Disorder Generalized" / "All Disorder Models"

**Why forbidden:** Only Anderson diagonal disorder tested. No data for correlated disorder, off-diagonal disorder, time-dependent disorder, quasiperiodic potentials.

**Correct alternative:** "Anderson disorder only (diagonal on-site U(r) ∈ [-W, W])"

---

## Claim Expansion Rules

When expanding the canonical claim for presentations, papers, or reports:

### Rule 1: Caveats FIRST
Always lead with caveats before presenting positive results. Example:

**Correct:**
> "Within finite-lattice N ≤ 896, Anderson disorder only, S³×S¹ only — Gate 4B supports W=20 localization signal robustness."

**Wrong:**
> "Gate 4B supports W=20 localization signal robustness. [caveats buried at end]"

### Rule 2: Quantify Confidence
Use "supports" (medium confidence), NOT "confirms" (high confidence) or "proves" (definitive).

### Rule 3: State What Does NOT Follow
After each positive claim, state ≥1 non-interpretation. Example:

**Positive claim:**
> "IPR contrast strengthens with lattice size (3.76× → 24.90×)."

**Non-interpretation:**
> "Does NOT prove thermodynamic limit behavior (N→∞ unknown)."

### Rule 4: Cite Pre-Registration
Always reference that grid, thresholds, and decision rules were pre-registered (commit 5e5ffc9).

**Example:**
> "All 7 pre-registered conditions satisfied (no post-hoc tuning)."

### Rule 5: Acknowledge Metric Correction
When citing v0.1.21 results, acknowledge v0.1.20 metric error upfront.

**Example:**
> "Gate 4B v0.1.21 metric-corrected rerun (v0.1.20 used invalid eigenvalue-based metric)."

---

## Audience-Specific Guidelines

### For Internal Reports (This Repo)
- Full caveats required
- Allowed to discuss limitations and next steps
- Allowed to mention v0.1.20 incident as lesson learned

### For External Presentations (Conferences, Preprints)
- Caveats MUST appear in abstract and conclusion
- Use "exploratory" or "pilot" framing
- Do NOT hide caveats in supplementary material
- **Submission Gate protocol applies** (see `~/.claude/rules/integrity.md`)

### For Grant Applications
- Allowed to present as "preliminary evidence"
- Caveats required in "Limitations" section
- Allowed to propose Gate 5 / cross-geometry / negative controls as "next steps"
- Do NOT claim "validated method" or "proven approach"

### For Casual Discussion (Slack, Emails)
- Shorthand allowed: "Gate 4B passed with caveats"
- Full claim not required every time
- BUT: if someone asks "what does it mean?" → redirect to canonical claim + caveats

---

## Violation Examples (Real-World Anti-Patterns)

### ❌ Example 1: Overgeneralization
**Claim:** "Our method validates localization on curved manifolds."  
**Why wrong:** Only S³×S¹ tested, NOT "curved manifolds" in general.  
**Correct:** "Our method supports localization on S³×S¹ finite lattice."

### ❌ Example 2: Causal Language Without Causation
**Claim:** "W=20 disorder causes localization."  
**Why wrong:** Observed correlation (IPR increases with W), NOT causal proof.  
**Correct:** "W=20 disorder is associated with higher IPR (localization diagnostic)."

### ❌ Example 3: Thermodynamic Leap
**Claim:** "Signal persists in thermodynamic limit."  
**Why wrong:** No N→∞ extrapolation performed.  
**Correct:** "Signal strengthens with N up to 896 (thermodynamic limit unknown)."

### ❌ Example 4: Metric Confusion
**Claim:** "Gate 4A and Gate 4B both show 7× contrast."  
**Why wrong:** Gate 4A metric invalid, Gate 4B metric corrected — NOT comparable.  
**Correct:** "Gate 4B (v0.1.21 true IPR) shows 7.15× contrast. Gate 4A (v0.1.20 eigenvalue mean) invalid."

---

## Change Log

| Date | Change |
|------|--------|
| 2026-05-22 | Initial version (v0.1.21 results finalized) |
| | 10 forbidden claims documented |
| | 5 expansion rules added |
| | Audience-specific guidelines added |

---

**Last Updated:** 2026-05-22  
**Status:** FINAL  
**Next Review:** Before any external communication (Submission Gate applies)

---

## Quick Reference

**✅ USE:** supports, consistent with, exploratory, finite-lattice, pilot, N ≤ 896  
**❌ AVOID:** validated, generalized, optimal, proven, thermodynamic limit, physical compactification, paradigm shift
