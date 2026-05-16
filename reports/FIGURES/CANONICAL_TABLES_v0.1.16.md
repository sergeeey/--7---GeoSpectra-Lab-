# Canonical Tables and Figures — v0.1.16 Methodology Paper

**Date:** 2026-05-17  
**Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Purpose:** Centralized reference tables/figures for compressed methodology paper draft

---

## Table 1. v0.1.15 Validation Chain: Timeline and Milestones

| Stage | Date | Cases | Duration | Verdict | Key Result |
|-------|------|-------|----------|---------|------------|
| Full Diagnostic | 2026-05-15 | 6615 | 16 hours | PASS_WITH_CAVEATS | 99.1% localized, 51 ring/alpha=0 failures |
| Reproducibility | 2026-05-15 | 6615 | 16 hours | PASS | 6615/6615 matched |
| Independent Audit | 2026-05-16 | - | 1 hour | CONFIRMED | Classification verified, 3 corrections |
| Ring/alpha=0 Follow-Up | 2026-05-16 | 1349 | 2.5 hours | ARTIFACT | 0/252 at s1_size≥64 |
| Integrity Audit | 2026-05-16 | - | 30 min | PASS | All checks confirmed |
| Baseline Promotion | 2026-05-16 | - | - | v0.1.15 | v0.1.14 → v0.1.15 |

**Caption:**  
Six-stage validation workflow from full diagnostic (6615 cases) to baseline promotion. Full diagnostic: 99.1% of disordered cases localized, 51 ring/alpha=0 failures detected. Reproducibility: independent re-run matched all 6615 cases identically. Independent audit: classification confirmed after 3 minor corrections. Ring/alpha=0 follow-up (1349 cases): extended s1_size grid to 64, 96 → all 51 failures vanished (SMALL_LATTICE_ARTIFACT verdict). Integrity audit: all cross-file checks passed. Baseline promoted: v0.1.14 → v0.1.15-s2-s1-product-discretized-full. **Non-claim:** This workflow validates discretized toy operators, NOT continuum compactification or physical mechanism.

---

## Table 3. Core Gates Pass Rate: Full Diagnostic v0.1.15

| Gate | Total | Passed | Pass Rate | Purpose |
|------|-------|--------|-----------|---------|
| Hermiticity | 6615 | 6615 | 100.0% | Operator validity (H† = H, max residual ≤1e-9) |
| Shape Consistency | 6615 | 6615 | 100.0% | Dimension correctness (dim = dim_S2 × s1_size) |
| Reproducibility | 6615 | 6615 | 100.0% | Independent re-run matched identically |
| Positive Control (W=0) | 945 | 945 | 100.0% | Expected delocalization (disorder=0) |
| Negative Control (q=0) | 945 | 945 (0 FP) | 100.0% | False positive protection (q=0 → delocalized) |

**FP = False Positives**  
**All gates passed at 100% rate. Zero false positives detected.**

**Caption:**  
Pass rate for 5 core validation gates across 6615 cases (product-discretized S²×S¹ operators). All gates passed at 100%. Positive control: 945 clean cases (W=0) delocalized as expected. Negative control: 0 false positives among 945 q=0 disordered cases (all delocalized as expected). Reproducibility: independent re-run matched all 6615 cases identically. **Non-claim:** Core gates validate discretized toy operators, NOT continuum compactification or physical mechanism.

---

## Figure 7. Ring/alpha=0 Lattice-Size Scaling: Convergence at s1_size≥64

**Data:**

| s1_size | Total Cases | Failures | Failure Rate (%) | Interpretation |
|---------|-------------|----------|------------------|----------------|
| 8 | 126 | 25 | 19.8 | Small lattice, high failure rate |
| 16 | 126 | 1 | 0.8 | Sharp drop after s1_size=8 |
| 24 | 126 | 19 | 15.1 | Non-monotonic (secondary peak) |
| 32 | 126 | 3 | 2.4 | Near convergence threshold |
| 48 | 126 | 3 | 2.4 | Below Decision Rule 1 threshold (2%) |
| **64** | **126** | **0** | **0.0** ✅ | **Converged** |
| **96** | **126** | **0** | **0.0** ✅ | **Converged** |
| | | | | |
| **s1_size < 64** | **630** | **51** | **8.1%** | Small-lattice artifact zone |
| **s1_size ≥ 64** | **252** | **0** | **0.0%** | Convergence confirmed |

**Decision Rule 1:** If failure_rate(s1_size≥64) < 2% → SMALL_LATTICE_ARTIFACT.  
**Result:** 0.0% < 2% → **Verdict: SMALL_LATTICE_ARTIFACT** ✅

**Production Guideline:** Ring/alpha=0 requires s1_size≥64 for robustness.

**Caption:**  
Failure rate (%) vs. s1_size for ring discretization of S¹ at periodic boundary condition (alpha=0.0). Disordered cases only (W>0). Data from targeted follow-up (882 ring/alpha=0 disordered cases). All 51 failures from full run (6615 cases) vanish at s1_size≥64 (0/252 = 0.0%). Decision Rule 1 threshold (2%) exceeded only at s1_size<64. Verdict: SMALL_LATTICE_ARTIFACT. **Non-claim:** This shows discretized toy operator convergence, NOT continuum extrapolation or physical compactification.

**Plot Specifications:**
- X-axis: s1_size [8, 16, 24, 32, 48, 64, 96]
- Y-axis: Failure rate (%) [0, 25%]
- Main series: Line + markers (blue circles)
- Threshold lines: Horizontal red dashed at 2% (Decision Rule 1), Vertical green dashed at s1_size=64 (convergence)
- Annotations: "Converged: 0/252 = 0.0%" at (64, 0.0), "Small-lattice artifact zone" at (8-48 region)

---

## Table 9.1. Scientific Non-Claims: What v0.1.15 Does NOT Prove or Claim

| # | Non-Claim | Reason (Why NOT Validated) |
|---|-----------|---------------------------|
| **1** | **Continuum compactification** | All operators discretized on finite lattices (S²: q≤106, S¹: s1_size≤96). No continuum extrapolation (q→∞, s1_size→∞) performed. |
| **2** | **S⁶ or S³×S⁶ validation** | Only S², S³, S¹, and S²×S¹ product spaces tested. Higher-dimensional manifolds (S⁶: 6D, S³×S⁶: 9D) NOT constructed. |
| **3** | **Standard Model derivation** | No gauge group calculation (SU(3)×SU(2)×U(1)). No fermion generations, no gauge coupling, no Yukawa couplings. |
| **4** | **Physical chirality proof** | Dirac indices are topological toy counts on discretized manifolds, NOT physical chiral fermions. No anomaly cancellation, no electroweak breaking. |
| **5** | **Witten/Lichnerowicz bypass** | Numerical index computation ≠ rigorous Atiyah-Singer proof. Computational shortcuts ≠ mathematical theorem. |
| **6** | **Physical extra dimensions** | Anderson localization benchmark is numerical disorder test, NOT physical compactification mechanism. No radion stabilization, no moduli stabilization. |
| **7** | **Hierarchy problem solution** | Toy radion model (if used) does NOT address moduli stabilization or cosmological constant problem in string theory. |
| **8** | **Observable predictions** | Topological invariants (chiral index, localization metrics) are discretized toy analogs, NOT continuum field theory predictions. No particle masses, no cross-sections, no decay rates. |

**Caption:**  
Eight explicit scope boundaries defining what v0.1.15 does NOT prove or claim. These are permanent boundaries — no claim should extend beyond these limits without explicit justification and independent validation. v0.1.15 validates a falsification-first workflow for discretized toy operators on S²×S¹ finite lattices. This is a **methodological contribution**, NOT a physical compactification proof.

---

## Summary

**4 canonical artifacts created:**
1. Table 1 — Validation Chain (6 stages)
2. Table 3 — Core Gates Pass Rate (5 gates, 100% pass)
3. Figure 7 — Lattice-Size Scaling (ring/alpha=0 convergence at s1_size≥64)
4. Table 9.1 — Scientific Non-Claims (8 boundaries)

**Usage:**
- Reference these tables/figures throughout compressed manuscript (Sections 1-6) to eliminate duplication
- All quantitative results centralized here — narrative text should cite tables, not repeat numbers

**Next steps:**
1. Generate Figure 7 plot (Python script using matplotlib)
2. Insert tables into compressed manuscript draft
3. Update all section text to reference canonical tables (eliminate inline duplication)

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)  
**Non-claims preserved:** All 8 scientific non-claims from Table 9.1 remain in final manuscript
