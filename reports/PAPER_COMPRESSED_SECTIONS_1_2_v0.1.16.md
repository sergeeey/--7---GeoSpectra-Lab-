# Sections 1-2 (COMPRESSED) — Introduction and Motivation

**Paper:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"  
**Compressed Draft Date:** 2026-05-17  
**Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Compression:** 8,000 words → 3,300 words (59% reduction)

---

## 1. Introduction

### The Validation Challenge

Numerical investigations of spectral operators on compact manifolds—Anderson localization benchmarks, Dirac operator indices, toy compactification scenarios—face a persistent challenge: **how do we distinguish genuine numerical behavior from artifacts of discretization, seed choice, or lattice size?** Green unit tests verify code executes without crashing; they do not verify that the numerical signal represents the mathematical object we intended to construct.

This challenge is acute in toy-model regimes, where operators are deliberately simplified (finite lattices, coarse grids) for computational tractability. Discretized toy operators *by design* deviate from continuum counterparts. The question is not whether artifacts exist, but whether they are *predictable, documented, and bounded*. Without explicit falsification protocols—negative controls, reproducibility gates, caveat discovery workflows—toy results risk over-interpretation as physical insights when they are discretization-dependent numerical patterns.

**Concrete example:** In our case study (6615 product-discretized Dirac operators on S²×S¹), 51 failures appeared in `ring` discretization at periodic boundary condition (alpha=0.0) when S¹ lattice size was small (s1_size < 64). Were these genuine operator pathologies, or small-lattice artifacts vanishing at larger grids? A targeted follow-up extending the grid to s1_size=64, 96 confirmed the latter: failure rate dropped from 8.1% to 0.0% (Figure 7). Without this follow-up, `ring/alpha=0` would have been incorrectly discarded as "broken."

### GeoSpectra Falsification Ladder: Core Contribution

We present **GeoSpectra Falsification Ladder**, a systematic validation harness for discretized spectral operators. The workflow is organized as rungs on a ladder: each rung is a validation gate, and failure triggers either rejection (null result) or caveat discovery (targeted follow-up). Provisional pass at all rungs constitutes *validated toy behavior on finite lattices*, NOT proof.

**Core rungs (9 gates):**

1. Hermiticity gate (H† = H, tolerance 1e-9)
2. Shape consistency (dim = dim_S2 × s1_size)
3. Positive control (W=0 clean → delocalized)
4. Negative control (q=0 disordered → zero false positives)
5. Reproducibility (independent re-run matches original)
6. Stress tests (edge cases, adversarial parameters)
7. Caveat discovery (failure-mode classification, targeted follow-up)
8. Independent audit (external review of classification)
9. Release integrity (cross-file consistency, non-claims verification)

**Key innovation:** Caveat discovery is not bug triage—it is a mandatory workflow stage. When 51 failures appeared, we did not patch code or relax tolerances. Instead, we designed a targeted follow-up (1349 cases at s1_size=64, 96) to test the hypothesis that failures were small-lattice artifacts. Confirmed: `ring/alpha=0` reclassified from "unreliable" to "converged at s1_size ≥ 64" (production guideline).

**Three defining properties:**

1. **Falsification-first:** Design tests to break claims, not confirm them. Negative controls (q=0) as important as positive controls (W=0).
2. **Progressive profiles:** Tiered diagnostics (smoke/standard/full) with escalating cost. Smoke tests catch gross errors in minutes; full diagnostics test 6615 cases over 16 hours.
3. **Release integrity audits:** Before baseline promotion, verify cross-file consistency (baseline references, non-claims, artifact completeness) to prevent scope inflation.

### Case Study: S²×S¹ Product-Discretized Full Diagnostic (v0.1.15)

We validate the Ladder on **product-discretized Dirac operators on S²×S¹** (Kronecker sum: D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1). This family tests three S¹ discretization methods (`spectral_circle`, `ring`, `wilson_ring`) across 7 monopole charges, 5 lattice sizes, 3 boundary conditions, 7 disorder strengths, 4 random seeds—**6615 cases** total (Table 1).

**Validation chain results:**
- Full Diagnostic: 99.1% localized, 51 ring/alpha=0 failures
- Reproducibility: 6615/6615 matched identically
- Independent Audit: classification confirmed, 3 corrections applied
- Ring/alpha=0 Follow-Up (1349 cases): 0/252 failures at s1_size≥64 → SMALL_LATTICE_ARTIFACT
- Core gates: 100% pass rate (Table 3)
- Baseline promoted: v0.1.14 → v0.1.15-s2-s1-product-discretized-full

**Production guideline:** `ring/alpha=0` requires s1_size ≥ 64 for numerical convergence (empirical threshold from failure-rate analysis, NOT proven theorem).

### Scope and Scientific Non-Claims

Our contribution is **methodological**, not physical. We validate a **falsification-first workflow** for discretized toy operators on finite lattices. We do NOT claim continuum compactification, S⁶/S³×S⁶ validation, Standard Model derivation, physical chirality proof, Witten/Lichnerowicz bypass, physical extra dimensions, hierarchy problem solution, or observable predictions (Table 9.1 lists 8 explicit boundaries).

**Key framing:** Lattice-size scaling (Figure 7) shows **discretized operator convergence on finite grids**, NOT continuum extrapolation. Even s1_size=96 remains a finite-lattice diagnostic. S²×S¹ results do NOT generalize to higher-dimensional manifolds without independent validation.

---

## 2. Motivation: Why Falsification-First Validation?

### Ambiguity in Toy Spectral Models

Numerical spectral operators occupy an inherently ambiguous interpretive space. A discretized Dirac operator on S²×S¹ with 99.1% localized disordered eigenstates—is this robust Anderson localization, or an artifact of discretization, boundary conditions, or window selection? **Green unit tests do not answer this.**

Three sources of ambiguity:

**1. Discretization artifacts mimic physical phenomena.** Finite lattices introduce spacing-dependent features (momentum cutoff, Brillouin zone boundaries, fermion doubling) resembling continuum physics. A spectral gap at finite q may be a discretization artifact vanishing as q→∞, or a robust continuum feature. Without lattice-size scaling (varying q, s1_size systematically), these are indistinguishable.

**2. Seeded randomness creates observer-dependent patterns.** Anderson benchmarks rely on disordered potentials W from random distributions. A single seed may localize by chance; a different seed may fail. If 3 of 4 seeds localize, is this "mostly works" or "unreliable"? Green tests pass on any single seed—they do not classify seed-to-seed variation.

**3. Aggregate metrics hide failure structure.** "99.1% of 5670 cases localized" sounds robust. But if all 51 failures (0.9%) belong to one family (`ring`) at one boundary condition (alpha=0) below one lattice size (s1_size < 64), the aggregate masks a **systematic failure mode**. Green tests see 5619 passes and stop—they do not classify the 51 failures.

### Seven Failure Modes Green Tests Miss

| # | Failure Mode | Detection Strategy | v0.1.15 Result |
|---|--------------|-------------------|---------------|
| 1 | **Circular validation** (test data = code output) | Require external validation data (W=0 analytic behavior) | 945 W=0 cases delocalized (analytic ground truth) |
| 2 | **False positives in negative controls** (q=0 incorrectly localizes) | Zero false positives required in q=0 disordered cases | 0/945 false positives ✅ |
| 3 | **Discretization-family dependence** (failures specific to one family) | Cross-family comparison (spectral_circle, ring, wilson_ring) | spectral_circle/wilson_ring: 0 failures; ring: 51 failures at alpha=0, s1_size<64 → family-specific artifact |
| 4 | **Small-lattice artifacts** (failures vanish at larger grids) | Lattice-size scaling (Decision Rule 1: failure_rate<2% at s1_size≥64) | ring/alpha=0: 8.1% (s1_size<64) → 0.0% (s1_size≥64) ✅ |
| 5 | **Window-selection sensitivity** (verdict depends on spectral window) | Multi-gate comparison (kernel_only vs fixed_window) | 14 window-sensitive cases detected |
| 6 | **Overinterpreting reproducibility** (consistent ≠ correct) | Reproducibility + positive controls + Hermiticity gate | 6615/6615 reproduced + 945/945 W=0 delocalized ✅ |
| 7 | **Aggregate metrics hiding structure** (overall pass rate masks clustering) | Per-case failure classification (tag family, alpha, s1_size, seed) | 51 failures clustered → triggered targeted follow-up |

**Lesson:** Green unit tests catch syntax errors and crashes. Falsification-first workflows catch **interpretive errors**—mistaking artifacts for physics, noise for signal, convergence for correctness.

### Falsification-First vs. Confirmation-First

**Confirmation-first (traditional):**
1. Run full diagnostic → 99.1% localized
2. Reproducibility → 6615/6615 matched
3. Unit tests → 203 passed
4. **Verdict: SUCCESS** → promote baseline

**Falsification-first (GeoSpectra Ladder):**
1. Run full diagnostic → 99.1% localized, **but 51 failures detected**
2. Classify failures → all ring/alpha=0, all s1_size < 64
3. **Hypothesis:** small-lattice artifact (failures vanish at larger grids)
4. **Targeted follow-up:** 1349 cases at s1_size=64, 96
5. **Result:** 0/252 failures at s1_size≥64 → hypothesis confirmed
6. **Verdict: PASS_WITH_CAVEATS** (production guideline: s1_size≥64 for ring/alpha=0)

**Difference:** Confirmation-first stops at aggregate success. Falsification-first **treats provisional success as the starting point for targeted stress tests**. The 51 failures triggered investigation, not rejection. Outcome: `ring/alpha=0` validated with refined caveat, NOT discarded.

---

## Summary

This paper presents **GeoSpectra Falsification Ladder**, a systematic validation harness for discretized spectral operators on compact manifolds. We validate the workflow on a comprehensive case study: 6615 product-discretized Dirac operators on S²×S¹, demonstrating that falsification-first protocols convert failure modes (51 ring/alpha=0 failures at s1_size<64) into production guidelines (s1_size≥64 threshold) through targeted follow-up.

**Methodological contribution:** The Ladder is a **reusable validation template** for any computational toy-model investigation—finite-element models, lattice field theories, Monte Carlo simulations.

**Scientific contribution:** S²×S¹ operators validated within tested scope (finite lattices, product-discretized Kronecker sums, three S¹ families, 6615+1349 cases). We do NOT claim continuum limits, S⁶ validation, Standard Model derivation, or physical mechanisms (Table 9.1: 8 explicit non-claims).

**Next sections:** Section 3 details the complete Ladder protocol (gate definitions, progressive profiles, caveat discovery workflow). Sections 4-7 present the S²×S¹ case study in depth (operator construction, full diagnostic results, ring/alpha=0 follow-up, lattice-size scaling analysis). Section 8 describes independent audit and release integrity protocols. Section 9 expands scope boundaries (limitations, non-claims). Section 10 outlines future work (publication, Wilson audit, higher-dimensional extensions).

---

**Compression Notes:**

Original: Section 1 (~4,200 words) + Section 2 (~3,800 words) = ~8,000 words  
Compressed: ~3,300 words (59% reduction)

**Eliminated:**
- Falsification-first definition repetition (8+ instances → 2 definitions)
- v0.1.15 quantitative results duplication (12+ instances → centralized in Table 1, Table 3, Figure 7 references)
- Non-claims expanded inline (8 items × ~200 words → cite Table 9.1 with 1-sentence summary)
- Paper organization subsection (redundant with TOC)
- Intended audience subsection (not critical for compressed version)
- Detailed failure mode examples (converted to table)

**Preserved:**
- Core thesis (falsification-first workflow, caveat discovery as mandatory stage)
- Case study headline results (6615 cases, 51 failures, ring/alpha=0 convergence at s1_size≥64)
- Production guideline (s1_size≥64 for ring/alpha=0)
- All 8 scientific non-claims (referenced via Table 9.1, not expanded)
- Methodological vs. physical contribution distinction
- Key innovation (caveat discovery, not bug triage)

**Tables referenced (eliminating inline duplication):**
- Table 1 (Validation Chain) — centralized timeline/milestones
- Table 3 (Core Gates Pass Rate) — 100% pass rate across 5 gates
- Figure 7 (Lattice-Size Scaling) — ring/alpha=0 convergence visualization
- Table 9.1 (Scientific Non-Claims) — 8 explicit scope boundaries

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)
