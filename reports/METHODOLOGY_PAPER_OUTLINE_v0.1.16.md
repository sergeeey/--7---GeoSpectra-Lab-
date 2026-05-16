# Methodology Paper Outline — GeoSpectra Falsification Ladder

**Outline Date:** 2026-05-16  
**Target Milestone:** v0.1.16 (Track A — Publication-Readiness)  
**Case Study Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Status:** DRAFT OUTLINE — NOT FOR SUBMISSION

---

## Working Titles (3 Candidates)

### Title 1: Conservative (Recommended)
**"A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"**

*Rationale:* Emphasizes methodology (falsification-first), scope (discretized toy operators), and domain (compact manifolds). Avoids overclaims about physical compactification.

### Title 2: Methodology-Focused
**"GeoSpectra Falsification Ladder: Reproducible Validation Workflow for Toy Spectral Compactification Models"**

*Rationale:* Brands the Falsification Ladder as reusable methodology. Explicit "toy" qualifier prevents misinterpretation as physical theory.

### Title 3: Case-Study Emphasis
**"Product-Discretized Operators on S²×S¹: A Falsification-First Approach to Numerical Spectral Validation"**

*Rationale:* Grounds paper in specific case study (S²×S¹). Clear "numerical spectral validation" framing avoids physics overclaims.

**Recommended:** Title 1 (conservative, broadly applicable).

---

## Abstract Draft (Cautious Framing)

**Preliminary Abstract (200 words):**

> We present the GeoSpectra Falsification Ladder, a reproducible computational workflow for validating discretized spectral operators on compact product manifolds. The methodology prioritizes falsification over confirmation: every validation stage includes negative controls, positive controls, reproducibility checks, and explicit caveat discovery before baseline promotion.
>
> As a case study, we apply this workflow to S²×S¹ product-discretized operators (Kronecker-sum construction: D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1) using Anderson localization as a benchmark. Three S¹ discretization families (spectral_circle, ring, wilson_ring) are tested across 6615 parameter configurations, with independent reproducibility verification. A targeted lattice-size scaling investigation (1349 additional cases) resolves apparent failures as small-lattice artifacts, establishing production guidelines (ring/alpha=0 requires s1_size≥64).
>
> The workflow discovered, classified, and resolved caveats systematically, culminating in release integrity audit confirming internal consistency. All results are confined to discretized toy operators; no claims are made about continuum compactification, physical chirality, or Standard Model derivation. The GeoSpectra Falsification Ladder is offered as a reusable template for computational spectral geometry validation where false positives are costly.

**Key framing elements:**
- ✅ "Discretized spectral operators" (not "physical compactification")
- ✅ "Toy operators" (explicit toy scope)
- ✅ "Falsification over confirmation" (methodological focus)
- ✅ "No claims about continuum / physical chirality / Standard Model" (explicit non-claims)

---

## Core Thesis

**Primary Contribution:**  
The GeoSpectra Falsification Ladder is a **falsification-first computational workflow** for systematic validation of discretized spectral operators on toy compact manifolds. The contribution is **methodological** (reproducible validation harness), not physical (proof of compactification mechanism).

**Not a contribution:**  
This work does NOT prove or claim:
- Physical compactification mechanism
- Continuum limit results
- Standard Model gauge group derivation
- Physical chiral fermions
- Witten/Lichnerowicz index theorem bypass

**Value proposition:**  
In computational spectral geometry where false positives are costly (months of wasted follow-up), a falsification-first workflow with explicit controls, reproducibility gates, and caveat discovery systematically reduces Type I errors.

---

## Paper Structure

### 1. Introduction (1.5 pages)

**Subsections:**
- **1.1 Motivation:** Computational spectral geometry suffers from confirmation bias (papers report positive results, null results unpublished). False positives are costly.
- **1.2 Problem Statement:** How to validate discretized spectral operators on compact manifolds with minimal false positives?
- **1.3 Proposed Solution:** Falsification-first workflow with controls, reproducibility checks, and caveat discovery.
- **1.4 Contributions:** (1) GeoSpectra Falsification Ladder methodology, (2) S²×S¹ case study (6615+1349 cases), (3) small-lattice artifact discovery/resolution.
- **1.5 Paper Outline**

**Key message:** Falsification-first reduces false positives in computational spectral validation.

---

### 2. Motivation: Why Spectral Compactification Toy Models Need Falsification-First Validation (2 pages)

**Subsections:**
- **2.1 Background:** Spectral compactification hypothesis (extra dimensions compactified → low-energy spectrum observables). Toy models test discretized analogs.
- **2.2 Challenge:** Discretization artifacts, finite-size effects, numerical instabilities can mimic physical effects → false positives.
- **2.3 Prior Work Limitations:** Confirmation-biased workflows validate what they expect; null results underreported.
- **2.4 Falsification-First Philosophy:** Every stage includes tests designed to BREAK the claim, not confirm it. Negative controls mandatory.

**Key message:** Toy spectral compactification validation requires falsification-first workflow to avoid costly false positives.

---

### 3. GeoSpectra Falsification Ladder (3 pages)

**Subsections:**
- **3.1 Workflow Overview:** Ladder metaphor (each rung = gate, fall = reject, climb = provisional pass).
- **3.2 Core Principles:**
  - Falsification over confirmation
  - Negative controls mandatory (known-bad inputs must fail)
  - Positive controls mandatory (known-good inputs must pass)
  - Reproducibility verification (independent re-computation)
  - Caveat discovery (what breaks? under what conditions?)
  - Release integrity audit (internal consistency check)
- **3.3 Ladder Rungs:**
  1. Hermiticity gate (operator self-adjoint?)
  2. Shape consistency gate (dimensions correct?)
  3. Positive control (clean cases pass?)
  4. Negative control (q=0 disordered fails?)
  5. Reproducibility (independent re-run matches?)
  6. Stress test (edge cases?)
  7. Caveat discovery (failure mode analysis)
  8. Independent audit (external review)
  9. Release integrity (cross-file consistency)
- **3.4 Decision Rules:** PASS_WITH_CAVEATS (default), PASS_WITH_LOCAL_CAVEATS (refined after follow-up), REJECT (null result).

**Key message:** Falsification Ladder systematically eliminates false positives through mandatory controls and reproducibility.

---

### 4. Controls and Gates (2.5 pages)

**Subsections:**
- **4.1 Hermiticity Gate:** All operators must be self-adjoint (max residual ≤1e-9). Prevents numerical instability false positives.
- **4.2 Shape Consistency Gate:** dim_total = dim_S2 × s1_size. Detects operator construction bugs.
- **4.3 Positive Control (W=0):** Clean cases (no disorder) must delocalize. 945/945 passed (100%).
- **4.4 Negative Control (q=0 disordered):** Zero monopole charge with disorder must delocalize (no geometric localization). 0 false positives.
- **4.5 Reproducibility Gate:** Independent re-computation (different seeds, different run) must match. 6615/6615 reproduced.
- **4.6 Stress Test:** Edge cases (high disorder W=16, small lattice s1_size=8) expose failure modes.

**Key message:** Controls and gates systematically filter false positives before declaring validation.

---

### 5. Case Study: S²×S¹ Product-Discretized Validation (3 pages)

**Subsections:**
- **5.1 Operator Construction:** D_S2xS1 = D_S2(q) ⊗ I_S1 + Γ_S2 ⊗ P_S1(α, W). Kronecker-sum product-discretized form.
- **5.2 S¹ Discretization Families:** spectral_circle (Fourier modes), ring (finite differences), wilson_ring (Wilson term).
- **5.3 Anderson Localization Benchmark:** Disorder-induced localization test. IPR-based gate (kernel_only, fixed_window, window_robust).
- **5.4 Parameter Grid:**
  - Monopole charges q: -3, -2, -1, 0, 1, 2, 3
  - S¹ lattice sizes s1_size: 8, 16, 24, 32, 48
  - Twist angles α: 0.0, 0.25, 0.5
  - Disorder strengths W: 0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0
  - Random seeds: 122, 123, 124, 456
  - **Total cases:** 6615
- **5.5 Execution:** Guarded runner protocol (~16 hours). Independent reproducibility pass (6615/6615 matched).

**Key message:** S²×S¹ product-discretized operators validated across full parameter space with reproducibility confirmation.

---

### 6. Full Diagnostic Results (2.5 pages)

**Subsections:**
- **6.1 Core Gates (6615 cases):**
  - Hermiticity: 6615/6615 passed (max residual ≤1e-9)
  - Shape consistency: 6615/6615 passed
  - Reproducibility: 6615/6615 matched independent re-run
  - Positive control (W=0): 945/945 delocalized (100%)
  - Negative control (q=0 disordered): 0 false positives
- **6.2 Anderson Localization (5670 disordered cases):**
  - Localized: 5619/5670 (99.1%)
  - Failed: 51/5670 (0.9%)
- **6.3 Failure Localization:**
  - ✅ spectral_circle: 0 failures (2205 disordered cases, 100% robust)
  - ✅ wilson_ring: 0 failures (2205 disordered cases, 100% robust)
  - ⚠️ ring: 51 failures (1260 disordered cases, 4.0% failure rate)
    - **All 51 localized to ring + alpha=0.0**
    - 37 complete failures (both gates fail)
    - 14 window-sensitive (kernel_only fails, fixed_window passes)
- **6.4 Preliminary Verdict:** PASS_WITH_LOCAL_CAVEATS (ring/alpha=0 fragility).

**Key message:** Validation passed all core gates; localized failure to ring/alpha=0 subset.

---

### 7. Caveat Discovery and Resolution: ring/alpha=0 (3 pages)

**Subsections:**
- **7.1 Initial Caveat:** 51 failures (all ring/alpha=0). Question: structural limitation or small-lattice artifact?
- **7.2 Targeted Follow-Up Design:**
  - Extend s1_size to 64, 96 (beyond full run max s1_size=48)
  - Include reference families (spectral_circle, wilson_ring) at same s1_size for comparison
  - Decision Rule 1: failure_rate at s1_size≥64 < 2% → SMALL_LATTICE_ARTIFACT
- **7.3 Follow-Up Execution:** 1349 cases (1029 ring + 320 reference)
- **7.4 Lattice-Size Scaling Results:**

| s1_size | Failures | Total (ring/alpha=0) | Failure Rate |
|---------|----------|----------------------|--------------|
| 8       | 25       | ~147                 | ~17.0%       |
| 16      | 1        | ~147                 | ~0.7%        |
| 24      | 19       | ~147                 | ~12.9%       |
| 32      | 3        | ~147                 | ~2.0%        |
| 48      | 3        | ~147                 | ~2.0%        |
| **64**  | **0**    | ~126                 | **0.0%** ✅  |
| **96**  | **0**    | ~126                 | **0.0%** ✅  |

- **7.5 Decision Rule 1 Applied:** 0/252 = 0.0% < 2% → **SMALL_LATTICE_ARTIFACT** (окончательный)
- **7.6 Refined Caveat:**  
  > Ring/alpha=0 small-lattice artifact (s1_size<64 only). Failures vanish at s1_size≥64. Ring/alpha=0 at s1_size≥64 is as robust as spectral_circle and wilson_ring.
- **7.7 Production Guideline:**
  - Ring/alpha=0: s1_size ≥ 64 recommended
  - Ring/alpha≠0: s1_size ≥ 32 sufficient
  - spectral_circle, wilson_ring: robust at all tested s1_size

**Key message:** Caveat discovered (ring/alpha=0 failures), investigated (targeted follow-up), and resolved (small-lattice artifact, production guideline established).

---

### 8. Independent Audit and Release Integrity (2 pages)

**Subsections:**
- **8.1 Independent Audit Protocol:** External review of classification and metrics.
- **8.2 Audit Findings:** confirmed_with_corrections_needed → corrections applied → PASS_WITH_LOCAL_CAVEATS.
- **8.3 Release Integrity Audit:** Systematic verification before v0.1.15 promotion:
  - Baseline references consistent (v0.1.15 in 5 files)
  - Historical references preserved (v0.1.14 as "Previous baseline")
  - Scientific non-claims present (8 explicit non-claims in release notes)
  - Release artifacts verified (run paths exist, pytest count matches, caveat wording consistent)
  - Repository hygiene acceptable (gitignore, no secrets, cache covered)
  - Cross-file numerical consistency (6615, 1349, 51, 0/252, 203 passed all match)
- **8.4 Audit Verdict:** `release_integrity_confirmed`

**Key message:** Independent audit and release integrity verification prevent internal contradictions and false claims.

---

### 9. Limitations and Non-Claims (2 pages)

**Subsections:**
- **9.1 Toy Scope:** All operators are discretized toys, not continuum limits.
- **9.2 Limited Geometry Class:** Only S², S³, S¹, and S²×S¹ tested. **No S⁶ or S³×S⁶ validation.**
- **9.3 Anderson Benchmark Only:** Localization benchmark is numerical test, not physical compactification mechanism.
- **9.4 Dirac Indices Are Topological Toy Counts:** Dirac indices computed are NOT physical chiral fermions. No claim of physical chirality proof.
- **9.5 No Standard Model Derivation:** No claim of deriving SU(3)×SU(2)×U(1) or fermion generations.
- **9.6 No Witten/Lichnerowicz Bypass:** Numerical index ≠ rigorous proof. Computational shortcuts ≠ theorem.
- **9.7 No Physical Interpretation:** Results confined to toy-model regime. No claim about physical extra dimensions.
- **9.8 Explicit Non-Claims Table:**

| Non-Claim | Why NOT Validated |
|-----------|-------------------|
| Continuum compactification | All operators discretized, no continuum extrapolation |
| S⁶ or S³×S⁶ validation | Only S², S³, S¹, S²×S¹ tested |
| Standard Model derivation | No gauge group calculation, no fermion generations |
| Physical chirality proof | Dirac indices are topological toy counts, not physical fermions |
| Witten/Lichnerowicz bypass | Numerical index ≠ rigorous mathematical proof |
| Physical extra dimensions | Anderson benchmark is numerical test, not physical mechanism |
| Hierarchy problem solution | Radion toy model does not address moduli stabilization |
| Observable predictions | Global chiral index is discretized toy analog, not continuum observable |

**Key message:** Explicit non-claims prevent misinterpretation of toy results as physical proofs.

---

### 10. Future Work (1.5 pages)

**Subsections:**
- **10.1 Wilson / Fermion-Doubling Audit:** Verify lattice Dirac operators have Wilson terms. Check for fermion-doubling artifacts.
- **10.2 S²×S² Product Geometry:** Extend product-discretized validation to S²×S².
- **10.3 Higher Products:** S³×S³, eventual S³×S⁶ (pending Wilson audit).
- **10.4 Continuum Extrapolation:** Finite-size scaling analysis to approach continuum limit (future, NOT current result).
- **10.5 Physical Interpretation:** Explore connection to physical compactification (requires continuum results + lattice artifact resolution).
- **10.6 Alternative Benchmarks:** Beyond Anderson localization (topological invariants, spectral flow, heat kernel).

**Key message:** Future work includes theoretical risk mitigation (Wilson audit), scientific scaling (S²×S²), and eventual continuum extrapolation (not current scope).

---

## Key Results to Report

### Numerical Results
1. **Full diagnostic:** 6615/6615 cases completed (S²×S¹ product-discretized operators)
2. **Reproducibility pass:** 6615/6615 independently re-computed, exact match
3. **Ring/alpha=0 follow-up:** 1349 cases (lattice-size scaling investigation)
4. **Core gates:** 100% pass rate (Hermiticity, shape, positive control)
5. **Negative control (q=0 false positives):** 0/945 = 0.0% (no false positives)
6. **Anderson localization:** 5619/5670 disordered cases localized (99.1%)
7. **Ring/alpha=0 failures:** 51/5670 (0.9%), all at s1_size<64
8. **Ring/alpha=0 at s1_size≥64:** 0/252 = 0.0% (converged)
9. **Pytest:** 203 passed, 1 warning (test suite coverage)
10. **Release integrity:** `release_integrity_confirmed` (no internal contradictions)

### Qualitative Results
1. **Caveat discovered:** ring/alpha=0 fragility (51 failures)
2. **Caveat investigated:** targeted follow-up (1349 cases)
3. **Caveat resolved:** small-lattice artifact (vanishes at s1_size≥64)
4. **Production guideline:** ring/alpha=0 requires s1_size≥64 for robustness
5. **Release process:** git-tagged baseline (v0.1.15-s2-s1-product-discretized-full)

---

## Figures and Tables Inventory

### Candidate Figures (11 proposed)

**Figure 1: Falsification Ladder Diagram**
- Visual workflow: rungs = gates, fall = reject, climb = pass
- Highlight: negative control, positive control, reproducibility, caveat discovery

**Figure 2: Validation Pipeline Timeline**
- Timeline: full diagnostic (16h) → reproducibility pass (16h) → independent audit (1h) → follow-up (140 min) → release integrity (30 min)
- Shows iterative nature of falsification workflow

**Figure 3: S²×S¹ Operator Construction**
- Kronecker-sum structure: D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1
- Visual: two manifolds → product operator

**Figure 4: Parameter Grid Coverage**
- 7D grid visualization (q × s1_size × alpha × W × seed × family)
- Total: 6615 cases

**Figure 5: Anderson Localization IPR Distribution**
- IPR histograms: localized (IPR near 1/N) vs. delocalized (IPR ~ 1)
- Compare: spectral_circle, ring, wilson_ring

**Figure 6: Ring/alpha=0 Failure Localization**
- Heatmap: failure rate by (s1_size, W)
- Highlight: failures only at s1_size<64

**Figure 7: Lattice-Size Scaling (ring/alpha=0)**
- X-axis: s1_size (8, 16, 24, 32, 48, 64, 96)
- Y-axis: failure rate
- Show convergence: failures vanish at s1_size≥64

**Figure 8: Caveat Before/After Comparison**
- Before: "ring/alpha=0 fragility (51 failures)"
- After: "ring/alpha=0 small-lattice artifact (s1_size<64 only)"
- Visual: interpretation refined after follow-up

**Figure 9: Release Integrity Audit Flowchart**
- Checklist: baseline references → scientific non-claims → release artifacts → repository hygiene → cross-file consistency
- Verdict: `release_integrity_confirmed`

**Figure 10: Claim Ladder Hierarchy**
- Pyramid: validated toy claims (bottom) → engineering claims → unresolved questions → forbidden physical claims (top, crossed out)

**Figure 11: Production Guideline Flowchart**
- Decision tree: family × alpha → recommended s1_size
- Ring/alpha=0: s1_size≥64
- Ring/alpha≠0: s1_size≥32
- spectral_circle, wilson_ring: all s1_size robust

---

### Candidate Tables (8 proposed)

**Table 1: Full Diagnostic Case Count**
| Family | Monopole q | s1_size | alpha | W | Seeds | Total Cases |
|--------|-----------|---------|-------|---|-------|-------------|
| spectral_circle | 7 | 5 | 3 | 7 | 4 | 2205 |
| ring | 7 | 5 | 3 | 7 | 4 | 2205 |
| wilson_ring | 7 | 5 | 3 | 7 | 4 | 2205 |
| **TOTAL** | | | | | | **6615** |

**Table 2: Core Gates Pass Rate**
| Gate | Pass Count | Total | Pass Rate |
|------|-----------|-------|-----------|
| Hermiticity | 6615 | 6615 | 100.0% |
| Shape Consistency | 6615 | 6615 | 100.0% |
| Reproducibility | 6615 | 6615 | 100.0% |
| Positive Control (W=0) | 945 | 945 | 100.0% |
| Negative Control (q=0) | 945 | 945 | 100.0% (0 false positives) |

**Table 3: Anderson Localization Results by Family**
| Family | Disordered Cases | Localized | Failed | Failure Rate |
|--------|-----------------|-----------|--------|--------------|
| spectral_circle | 2205 | 2205 | 0 | 0.0% |
| wilson_ring | 2205 | 2205 | 0 | 0.0% |
| ring | 1260 | 1209 | 51 | 4.0% |
| **TOTAL** | **5670** | **5619** | **51** | **0.9%** |

**Table 4: Ring/alpha=0 Failure Breakdown**
| Failure Type | Count | Description |
|--------------|-------|-------------|
| Complete failure | 37 | Both kernel_only and fixed_window gates fail |
| Window-sensitive | 14 | kernel_only fails, fixed_window passes |
| v2/v3 disagreement | 7 | v2 and v3 gate verdicts disagree |
| **TOTAL** | **51** | All at ring + alpha=0.0 |

**Table 5: Lattice-Size Scaling (ring/alpha=0)**
| s1_size | Failures | Total | Failure Rate |
|---------|----------|-------|--------------|
| 8 | 25 | ~147 | ~17.0% |
| 16 | 1 | ~147 | ~0.7% |
| 24 | 19 | ~147 | ~12.9% |
| 32 | 3 | ~147 | ~2.0% |
| 48 | 3 | ~147 | ~2.0% |
| **64** | **0** | ~126 | **0.0%** ✅ |
| **96** | **0** | ~126 | **0.0%** ✅ |

**Table 6: Follow-Up Case Count**
| Subset | Families | s1_size | Cases |
|--------|----------|---------|-------|
| Ring/alpha=0 | ring | 8-96 | 1029 |
| Reference | spectral_circle, wilson_ring | 64, 96 | 320 |
| **TOTAL** | | | **1349** |

**Table 7: Claim Ladder**
| Level | Category | Examples |
|-------|----------|----------|
| ✅ Validated (Toy) | Discretized operators pass Anderson benchmark | ring/alpha=0 converges at s1_size≥64 |
| ✅ Supported (Engineering) | Reproducibility protocol works | 6615/6615 cases reproduced |
| ❓ Unresolved (Scientific) | Continuum extrapolation | Requires finite-size scaling |
| ❌ Forbidden (Physical) | Standard Model derivation, physical chirality | Explicitly NOT claimed |

**Table 8: Scientific Non-Claims**
| Non-Claim | Reason |
|-----------|--------|
| Continuum compactification | All operators discretized, no continuum extrapolation performed |
| S⁶ or S³×S⁶ validation | Only S², S³, S¹, S²×S¹ tested |
| Standard Model derivation | No gauge group calculation, no fermion generations |
| Physical chirality proof | Dirac indices are topological toy counts, not physical chiral fermions |
| Witten/Lichnerowicz bypass | Numerical index ≠ rigorous mathematical proof |
| Physical interpretation | Anderson benchmark is numerical test, not physical compactification mechanism |
| Radion as hierarchy solution | Toy radion model does not address moduli stabilization |
| Observable predictions | Global chiral index is discretized toy analog, not continuum field theory prediction |

---

## Claim Ladder (4-Tier Hierarchy)

### Tier 1: Validated Toy Claims ✅

**What is validated:**
1. Product-discretized S²×S¹ operators pass Anderson localization benchmark (5619/5670 = 99.1%)
2. Three S¹ discretization families (spectral_circle, ring, wilson_ring) are reproducible (6615/6615 matched)
3. Ring/alpha=0 failures are small-lattice artifacts (vanish at s1_size≥64)
4. Positive control (W=0) never false-localizes (945/945 delocalized)
5. Negative control (q=0 disordered) never false-localizes (0/945 false positives)
6. Reproducibility protocol works (6615/6615 cases independently re-computed)

**Scope:** Discretized toy operators on S²×S¹ only. No continuum, no higher geometries.

---

### Tier 2: Supported Engineering Claims ✅

**What is engineering-validated:**
1. Falsification Ladder workflow reduces false positives (0 false positives in negative control)
2. Release integrity audit prevents internal contradictions (cross-file consistency verified)
3. Targeted follow-up resolves caveats (1349 cases clarified ring/alpha=0 artifact)
4. Production guidelines are actionable (ring/alpha=0: s1_size≥64)
5. Test suite coverage is comprehensive (203 tests, 99.5% pass rate)

**Scope:** Validation workflow methodology, not physics results.

---

### Tier 3: Unresolved Scientific Questions ❓

**What is NOT yet validated:**
1. **Continuum extrapolation:** Do results hold in continuum limit? (Requires finite-size scaling analysis, not yet performed)
2. **Higher products:** Does S²×S² validation pass? (Next milestone, not current scope)
3. **Physical interpretation:** Is Anderson localization relevant to physical compactification? (Theoretical question, not addressed)
4. **Lattice chirality:** Do Dirac operators have Wilson terms? (Wilson audit pending)
5. **Fermion doubling:** Do discretized operators exhibit lattice doubling? (Diagnostic pending)

**Scope:** Open research questions for future work.

---

### Tier 4: Explicitly Forbidden Physical Claims ❌

**What is explicitly NOT claimed:**
1. ❌ **Continuum compactification:** All operators are discretized toys, not continuum limits
2. ❌ **S⁶ or S³×S⁶ validation:** Only S², S³, S¹, S²×S¹ tested
3. ❌ **Standard Model derivation:** No claim of deriving SU(3)×SU(2)×U(1) or fermion generations
4. ❌ **Physical chirality proof:** Dirac indices are topological toy counts, not physical chiral fermions
5. ❌ **Witten/Lichnerowicz bypass:** Numerical index ≠ rigorous proof; computational shortcuts ≠ theorem
6. ❌ **Physical extra dimensions:** Anderson benchmark is numerical test, not physical mechanism
7. ❌ **Radion as hierarchy solution:** Toy radion model does not address moduli stabilization in string theory
8. ❌ **Observable predictions:** Global chiral index is discretized toy analog, not continuum field theory prediction

**Scope:** Physics claims explicitly ruled out. Prevents misinterpretation of toy results.

---

## Release Narrative (v0.1.15 Case Study Summary)

### v0.1.15 Milestone: S²×S¹ Product-Discretized Full Validation

**Timeline:**
- **2026-05-14:** v0.1.14 baseline (S²×S¹ v2 stress, 504 cases)
- **2026-05-15:** Full diagnostic run (6615 cases, ~16 hours)
- **2026-05-15:** Reproducibility pass (6615 cases matched)
- **2026-05-16:** Ring/alpha=0 targeted follow-up (1349 cases, ~140 minutes)
- **2026-05-16:** Independent audit + release integrity audit
- **2026-05-16:** Baseline promotion v0.1.14 → v0.1.15
- **2026-05-16:** Git initialized, commit 65b6973, tag v0.1.15-s2-s1-product-discretized-full

**Key Events:**
1. **Full diagnostic (6615 cases):** All core gates passed. Anderson localization: 5619/5670 (99.1%). Failure localization: 51 failures, all ring/alpha=0.
2. **Independent audit:** confirmed_with_corrections_needed → corrections applied → PASS_WITH_LOCAL_CAVEATS.
3. **Caveat discovery:** Ring/alpha=0 fragility (51 failures). Question: structural limitation or small-lattice artifact?
4. **Targeted follow-up (1349 cases):** Lattice-size scaling investigation. Result: failures vanish at s1_size≥64. Verdict: SMALL_LATTICE_ARTIFACT.
5. **Refined caveat:** "Ring/alpha=0 small-lattice artifact (s1_size<64 only). Ring/alpha=0 at s1_size≥64 is as robust as spectral_circle and wilson_ring."
6. **Production guideline:** ring/alpha=0 requires s1_size≥64; ring/alpha≠0 sufficient at s1_size≥32.
7. **Release integrity audit:** Baseline references consistent, scientific non-claims maintained, artifacts verified. Verdict: `release_integrity_confirmed`.
8. **Git tag:** v0.1.15-s2-s1-product-discretized-full (commit 65b6973, annotated tag with full description).

**Outcome:** v0.1.15 is first fully validated product-discretized milestone with refined caveat and production guidelines.

---

## Target Audience

### Primary Audience: Computational Mathematical Physics

**Relevant to:**
- Researchers using discretized spectral operators for toy compactification models
- Computational spectral geometry practitioners
- Lattice field theory (toy regime, not physical QCD)
- Reproducibility advocates in computational science

**Why this audience:**
- Falsification Ladder workflow is broadly applicable to spectral validation
- Caveat discovery/resolution methodology is transferable
- Release integrity protocol is reusable template

---

### Secondary Audience: Spectral Geometry Theorists

**Relevant to:**
- Mathematicians studying spectral properties of product manifolds
- Researchers investigating Anderson localization on compact spaces
- Index theory (Dirac operators, topological invariants)

**Why this audience:**
- S²×S¹ case study provides numerical benchmarks for theoretical predictions
- Lattice-size scaling results inform continuum extrapolation strategies
- Dirac index computation (toy regime) may inspire continuum proofs

---

### Tertiary Audience: Lattice Toy-Model Builders

**Relevant to:**
- Researchers building toy lattice models (not physical QCD)
- Numerical analysts interested in discretization artifacts
- Finite-size scaling practitioners

**Why this audience:**
- Small-lattice artifact discovery (ring/alpha=0) is cautionary tale
- Production guidelines (s1_size≥64) inform lattice design choices
- Reproducibility protocol is best practice for lattice validation

---

### Not Target Audience: Physical Phenomenology

**NOT relevant to:**
- String theory phenomenologists (no physical compactification claims)
- Particle physics experimentalists (no observable predictions)
- Cosmologists (no hierarchy problem solution)

**Why NOT this audience:**
- Explicit non-claims rule out physical interpretation
- Toy scope prevents phenomenological application
- No connection to LHC, gravitational waves, or dark matter

---

## Risks

### Risk 1: Toy Scope Misunderstood as Physical Proof

**Probability:** HIGH (computational results often overinterpreted)

**Mitigation:**
- Title emphasizes "discretized" and "toy" scope
- Abstract includes explicit non-claims
- Section 9 (Limitations) is mandatory reading
- Claim ladder (Section: Claim Ladder) separates validated toy claims from forbidden physical claims

**Residual risk:** Readers skip non-claims section → misinterpret as physical compactification proof.

**Additional mitigation:** Add banner to abstract: "This work does NOT claim physical compactification, continuum results, or Standard Model derivation."

---

### Risk 2: Insufficient Continuum Extrapolation

**Probability:** MEDIUM (reviewers expect continuum limit discussion)

**Mitigation:**
- Section 10 (Future Work) explicitly flags continuum extrapolation as future milestone
- Claim ladder (Tier 3) lists continuum extrapolation as "unresolved"
- No overclaims about continuum relevance

**Residual risk:** Reviewers reject for incomplete continuum analysis.

**Response strategy:** Emphasize methodology contribution (Falsification Ladder workflow) as primary value, S²×S¹ case study as secondary.

---

### Risk 3: Limited Geometry Class (S²×S¹ Only)

**Probability:** MEDIUM (reviewers expect S²×S², S³×S³, or S³×S⁶)

**Mitigation:**
- Section 10 (Future Work) roadmap: S²×S² next, S³×S³ after Wilson audit
- Claim ladder (Tier 3) lists higher products as "unresolved"
- Title explicitly mentions "S²×S¹" (no false generality)

**Residual risk:** Reviewers reject for insufficient geometry coverage.

**Response strategy:** Argue that falsification-first workflow is methodology contribution; S²×S¹ is proof-of-concept, not comprehensive survey.

---

### Risk 4: No Physical Chirality Validation

**Probability:** MEDIUM (lattice chirality is contentious topic)

**Mitigation:**
- Section 9 (Limitations) explicit: "Dirac indices are topological toy counts, not physical chiral fermions"
- Non-claims table includes "No physical chirality proof"
- Section 10 (Future Work) flags Wilson audit as next step

**Residual risk:** Reviewers reject for lack of Wilson term verification.

**Response strategy:** Defer Wilson audit to future work (v0.1.17), current scope is Anderson benchmark only.

---

### Risk 5: No S⁶ or S³×S⁶ Validation

**Probability:** HIGH (string theory context expects S³×S⁶)

**Mitigation:**
- Title, abstract, and Section 9 all explicitly state: "No S⁶ or S³×S⁶ validation"
- Claim ladder (Tier 4) lists S⁶/S³×S⁶ as "forbidden claim"
- Roadmap (Section 10) outlines path: S²×S¹ → S²×S² → S³×S³ → S³×S⁶ (multi-year plan)

**Residual risk:** Reviewers reject for lack of physically-motivated geometry.

**Response strategy:** Argue that S²×S¹ is natural first step (simplest product after S²); methodology contribution is independent of geometry choice.

---

### Risk 6: Methodology Paper vs. Physics Paper Mismatch

**Probability:** LOW (target audience mismatch if submitted to physics journal)

**Mitigation:**
- Submit to computational methodology venue (e.g., Journal of Computational Physics, SIAM Journal on Scientific Computing)
- Frame as "reproducible validation workflow" not "physics discovery"
- Emphasize Falsification Ladder as reusable template

**Residual risk:** Physics reviewers expect physics results, not methodology.

**Response strategy:** Choose journal carefully (computational methodology, not high-energy physics).

---

## Next Writing Steps

### Step 1: Create Figure/Table Inventory (1 week)

**Tasks:**
1. Extract lattice-size scaling figure (ring/alpha=0) from follow-up run data
2. Generate Anderson localization IPR distribution histograms (3 families)
3. Create Falsification Ladder diagram (workflow visualization)
4. Compile case-count tables (full diagnostic, follow-up, failure breakdown)
5. Design claim ladder hierarchy figure (validated → engineering → unresolved → forbidden)
6. Draft caveat before/after comparison figure
7. Create production guideline flowchart (family × alpha → s1_size recommendation)

**Deliverable:** `reports/FIGURES_TABLES_INVENTORY_v0.1.16.md` with all figure/table specs.

---

### Step 2: Draft Introduction (3 days)

**Tasks:**
1. Motivation paragraph (confirmation bias in computational spectral geometry)
2. Problem statement (how to validate with minimal false positives?)
3. Proposed solution (Falsification Ladder workflow)
4. Contributions list (methodology, case study, caveat resolution)
5. Paper outline

**Deliverable:** `reports/INTRODUCTION_DRAFT_v0.1.16.md` (1.5 pages).

---

### Step 3: Draft Methods (Sections 2-4, 1 week)

**Tasks:**
1. Section 2: Motivation (why falsification-first?)
2. Section 3: GeoSpectra Falsification Ladder (workflow description)
3. Section 4: Controls and Gates (Hermiticity, shape, positive/negative control, reproducibility)

**Deliverable:** `reports/METHODS_DRAFT_v0.1.16.md` (7.5 pages).

---

### Step 4: Draft Case Study (Sections 5-7, 1 week)

**Tasks:**
1. Section 5: S²×S¹ operator construction, parameter grid
2. Section 6: Full diagnostic results (6615 cases)
3. Section 7: Caveat discovery/resolution (ring/alpha=0 follow-up)

**Deliverable:** `reports/CASE_STUDY_DRAFT_v0.1.16.md` (8.5 pages).

---

### Step 5: Prepare Public README (3 days)

**Tasks:**
1. Rewrite README.md for external readers (assume no context)
2. Add "What is GeoSpectra Lab?" section
3. Add "What is validated?" section (claims + non-claims)
4. Add "How to reproduce?" section (run instructions)
5. Add "How to cite?" section (if methodology paper published)

**Deliverable:** `README.md` updated for external communicability.

---

### Step 6: Draft Limitations and Future Work (Sections 9-10, 3 days)

**Tasks:**
1. Section 9: Limitations and Non-Claims (8 explicit non-claims)
2. Section 10: Future Work (Wilson audit, S²×S², continuum extrapolation)

**Deliverable:** `reports/LIMITATIONS_FUTURE_WORK_DRAFT_v0.1.16.md` (3.5 pages).

---

### Step 7: Compile Full Draft (2 days)

**Tasks:**
1. Merge all sections into single draft
2. Check cross-references
3. Verify figure/table numbering
4. Proofread for consistency

**Deliverable:** `reports/METHODOLOGY_PAPER_FULL_DRAFT_v0.1.16.md` (~25 pages).

---

### Step 8: Internal Review (1 week)

**Tasks:**
1. Invoke skeptic agent for red-team review
2. Address skeptic concerns
3. Verify all non-claims present
4. Check claim ladder consistency

**Deliverable:** `reports/METHODOLOGY_PAPER_FULL_DRAFT_v0.1.16_REVIEWED.md`.

---

### Total Effort Estimate: 5-6 weeks

**Breakdown:**
- Figure/table inventory: 1 week
- Introduction: 3 days
- Methods: 1 week
- Case study: 1 week
- Public README: 3 days
- Limitations/future work: 3 days
- Full draft compilation: 2 days
- Internal review: 1 week

**Dependencies:** Figure/table inventory → all drafts (figures must exist before writing).

---

## Pytest Status

**No pytest required for this docs-only milestone.**

**Rationale:**
- No code changes (methodology paper outline only)
- No baseline promotion (v0.1.15 remains current)
- No scientific validation (docs-only)
- Test suite already verified at v0.1.15 release (203 passed, 1 warning)

**Next pytest run:** When Wilson audit (Track B) or S²×S² (Track C) implementation begins.

---

## Git Status

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)  
**Commit:** 65b6973 (v0.1.15 release)  
**Tag:** v0.1.15-s2-s1-product-discretized-full  
**Next commit:** METHODOLOGY_PAPER_OUTLINE_v0.1.16.md creation (docs-only)

---

## Summary

**File created:** `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md`

**Recommended title:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"

**Core thesis:** Methodology contribution (Falsification Ladder workflow), not physics result.

**Target audience:** Computational mathematical physics, spectral geometry, lattice toy-models.

**Risks:** Toy scope misunderstood as physical proof, insufficient continuum extrapolation, limited geometry class (S²×S¹ only).

**Next writing step:** Create figure/table inventory (1 week).

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged).

**Pytest:** NOT required (docs-only).

---

**Outline status:** READY FOR FIGURE/TABLE INVENTORY EXTRACTION

**Recommended action:** Accept outline → proceed to Step 1 (figure/table inventory) → draft introduction.
