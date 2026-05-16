# Section 1 — Introduction

**Paper:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"  
**Draft Date:** 2026-05-16  
**Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Status:** FIRST DRAFT

---

## 1.1 Motivation: The Validation Challenge for Toy Spectral Operators

Numerical investigations of spectral operators on compact manifolds—whether for Anderson localization benchmarks, Dirac operator indices, or toy compactification scenarios—face a persistent validation challenge: **how do we distinguish genuine numerical behavior from artifacts of discretization, seed choice, window selection, or lattice size?** A passing test suite, while necessary, is insufficient. Tests verify that code executes without crashing; they do not verify that the numerical signal represents the mathematical object we intended to construct.

This challenge is particularly acute in toy-model regimes, where operators are deliberately simplified (finite lattices, coarse grids, no continuum extrapolation) to make computational exploration tractable. Discretized toy operators *by design* deviate from their continuum counterparts. The question is not whether artifacts exist, but whether they are *predictable, documented, and bounded*. Without explicit falsification protocols—negative controls, reproducibility gates, caveat discovery workflows—toy results risk being over-interpreted as physical insights when they are, in fact, discretization-dependent numerical patterns.

Consider a concrete example from our case study: in a full diagnostic run of 6615 product-discretized Dirac operators on S²×S¹, we observed 51 failures in the `ring` discretization family at periodic boundary condition (alpha=0.0) when the S¹ lattice size was small (s1_size < 64). Were these failures genuine operator pathologies, or small-lattice artifacts that vanish at larger finite lattice sizes? Without a targeted follow-up extending the lattice-size grid, this question would remain unresolved, and the `ring/alpha=0` configuration would be flagged as unreliable—potentially discarding a valid discretization method due to insufficient convergence testing.

**Our thesis:** Toy spectral operator validation requires a *falsification-first* workflow that treats provisional success as the starting point for targeted stress tests, not the endpoint. Green unit tests are a floor for code correctness, not a ceiling for scientific validation.

---

## 1.2 Contribution: GeoSpectra Falsification Ladder Workflow

We present **GeoSpectra Falsification Ladder**, a systematic validation harness for discretized spectral operators on compact manifolds. The workflow is organized as a ladder metaphor: each rung represents a validation gate, and failure at any rung triggers either rejection (null result) or caveat discovery (targeted follow-up). Provisional pass at all rungs does not constitute "proof"—it constitutes *validated toy behavior on finite lattices within tested parameter ranges*.

**Core rungs of the ladder (Figure 1):**

1. **Hermiticity gate** — verify H† = H with tolerance 1e-9
2. **Shape consistency gate** — verify dim(H) matches expected product dimension
3. **Positive control (W=0)** — clean cases expected to delocalize
4. **Negative control (q=0 disordered)** — zero false positives required
5. **Reproducibility gate** — independent re-run must match original
6. **Stress tests** — edge cases, adversarial parameters, seed variation
7. **Caveat discovery** — failure mode classification and targeted follow-up
8. **Independent audit** — external review of classification and metrics
9. **Release integrity** — cross-file consistency and non-claims verification

Unlike traditional test-driven development (which stops at green tests), the Falsification Ladder continues *after* initial success to discover and classify failure modes. Unlike academic "validation sections" (which are often post-hoc narratives), the Ladder is a *pre-registered protocol* executed before baseline promotion.

**Key innovation:** Caveat discovery is not a bug triage process—it is a mandatory workflow stage. When 51 failures appeared in `ring/alpha=0` cases, we did not patch the code or relax tolerances. Instead, we designed a targeted follow-up (1349 additional cases at extended lattice sizes s1_size=64, 96) to test the hypothesis that failures were small-lattice artifacts. The hypothesis was confirmed: failure rate dropped from 8.1% (s1_size < 64) to 0.0% (s1_size ≥ 64), and `ring/alpha=0` was reclassified from "unreliable" to "converged at s1_size ≥ 64" (Figure 7, Table 5).

This workflow has three defining properties:

1. **Falsification-first:** We design tests to break claims, not confirm them. Negative controls (q=0 disordered) are as important as positive controls (W=0 clean).

2. **Progressive profiles:** We run tiered diagnostics (smoke, standard, full) with escalating computational cost. Smoke tests catch gross errors in minutes; full diagnostics test 6615 cases over 16 hours.

3. **Release integrity audits:** Before baseline promotion, we verify cross-file consistency (baseline references, scientific non-claims, artifact completeness) to prevent scope inflation and documentation drift.

**Methodological contribution:** The Falsification Ladder is a *reusable validation template* for any computational toy-model investigation. While we demonstrate it on discretized spectral operators, the ladder structure (controls → reproducibility → caveat discovery → integrity audit) applies to finite-element models, lattice field theories, or Monte Carlo simulations.

---

## 1.3 Case Study: S²×S¹ Product-Discretized Full Diagnostic (v0.1.15)

We validate the Falsification Ladder workflow on a comprehensive case study: **product-discretized Dirac operators on S²×S¹** constructed via Kronecker sum (D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1). This operator family tests three S¹ discretization methods (`spectral_circle`, `ring`, `wilson_ring`) across 7 monopole charges, 5 lattice sizes, 3 boundary conditions, 7 disorder strengths, and 4 random seeds—a total of **6615 cases** in the full diagnostic run.

**Validation chain (Table 1):**

| Stage | Cases | Verdict | Key Result |
|-------|-------|---------|------------|
| Full Diagnostic | 6615 | PASS_WITH_CAVEATS | 99.1% localized, 51 ring/alpha=0 failures |
| Reproducibility | 6615 | PASS | Independent re-run matched identically |
| Independent Audit | - | CONFIRMED | Classification verified, 3 corrections |
| Ring/alpha=0 Follow-Up | 1349 | ARTIFACT | 0/252 at s1_size≥64 |
| Integrity Audit | - | PASS | All checks confirmed |
| Baseline Promotion | - | v0.1.15 | v0.1.14 → v0.1.15 |

**Note on PASS_WITH_CAVEATS verdict:** This verdict means numerical behavior validated on finite lattices with explicitly documented convergence thresholds (e.g., ring/alpha=0 requires s1_size≥64). It does NOT mean "passed with minor bugs fixed" or unqualified physical validation—it means all core gates pass with parameter-range caveats discovered and resolved via targeted follow-up.

**Core gates pass rate (Table 3):** All 5 core gates passed at 100% across 6615 cases. Hermiticity (max residual ≤1e-9), shape consistency, reproducibility, positive control (945/945 clean cases delocalized), and negative control (0/945 false positives) all achieved perfect scores. This confirms that the validation harness itself is robust—failures, when they occur, are not due to numerical instability or harness defects.

**Caveat discovery and resolution:** The 51 failures in `ring/alpha=0` at s1_size < 64 triggered a targeted follow-up extending the lattice-size grid to s1_size=64, 96 (1349 additional cases). Failure rate vs. s1_size (Figure 7) shows convergence: 19.8% failure at s1_size=8, dropping to 0.0% at s1_size≥64 (Table 5). Decision Rule 1 (if failure_rate(s1_size≥64) < 2% → classify as SMALL_LATTICE_ARTIFACT) confirmed the artifact hypothesis. **Production guideline:** `ring/alpha=0` requires s1_size ≥ 64 for numerical convergence.

**Scientific outcome:** The S²×S¹ validation demonstrates that product-discretized operators are numerically robust within tested parameter ranges, provided lattice sizes are sufficiently large finite grids (s1_size≥64 for ring/alpha=0). The `ring/alpha=0` caveat was converted from an unresolved bug into a documented convergence threshold—a concrete example of how falsification-first workflows improve scientific clarity.

---

## 1.4 Scope and Claims: What This Paper Validates

We emphasize upfront what this paper *does* and *does not* claim. Our contribution is methodological, not physical.

**What this paper validates:**

1. **Falsification-first workflow:** A systematic protocol for toy-model validation (controls, reproducibility, caveat discovery, integrity audits).

2. **Discretized toy operators:** Product-discretized Dirac operators on S²×S¹ exhibit robust numerical behavior at tested parameter ranges (6615 full diagnostic + 1349 follow-up cases).

3. **Production guidelines:** Concrete convergence thresholds for `ring/alpha=0` (s1_size ≥ 64) and other configurations empirically derived from failure-rate analysis (Decision Rule 1: failure_rate < 2%), not mathematically proven convergence theorems.

4. **Reproducibility:** Independent re-run of 6615 cases matched original results identically, confirming numerical stability.

5. **Negative control robustness:** Zero false positives in 945 q=0 disordered cases, validating control design. Note: This validates control robustness (q=0 → delocalized as expected), not full operator correctness—control design validation is necessary but not sufficient for operator validation.

**Cautious framing:** We validate *discretized toy operator behavior on finite lattices*, not continuum limits or physical mechanisms. Lattice-size scaling (Figure 7) shows convergence at s1_size≥64, but this is **discretized operator convergence**, not continuum extrapolation. We do not claim that S²×S¹ results generalize to higher-dimensional manifolds (S⁶, S³×S⁶) or that topological Dirac indices correspond to physical chiral fermions.

---

## 1.5 Scope Boundaries: What This Paper Does NOT Claim (Table 8)

To prevent misinterpretation, we state explicitly what this work does **NOT** validate. **Table 8 (Scientific Non-Claims)** lists eight scope boundaries; we summarize the most critical here:

1. **No continuum compactification:** All operators are discretized on finite lattices (S²: q=26-106, S¹: s1_size=8-96). No continuum extrapolation (q→∞, s1_size→∞) was performed, and no such extrapolation is planned within the scope of this toy-model investigation. Even the largest tested lattices (s1_size=96) remain finite-lattice diagnostics, not continuum evidence. Lattice-size scaling confirms discretized operator convergence, NOT continuum limits.

2. **No S⁶ or S³×S⁶ validation:** Only low-dimensional test geometries (S², S³, S¹, S²×S¹) were tested. We make no claim that S²×S¹ results extend to S⁶ (11-dimensional M-theory target) or S³×S⁶ (Kaluza-Klein compactification).

3. **No Standard Model derivation:** No gauge group calculation (SU(3)×SU(2)×U(1)), no fermion generations, no particle content. Dirac operators are topological toys, not physical field theories.

4. **No physical chirality proof:** Dirac indices are topological counts on discretized manifolds, not physical chiral fermions. No chiral anomaly cancellation, no Yukawa couplings, no flavor structure.

5. **No Witten/Lichnerowicz bypass:** Numerical eigenvalue decomposition ≠ rigorous Atiyah-Singer index theorem proof. We compute indices numerically; we do not prove the index theorem.

6. **No physical extra dimensions:** Anderson localization benchmarks are numerical tests of disorder-induced localization, not physical compactification mechanisms. IPR (Inverse Participation Ratio) gates are numerical quality checks, not physical observables.

7. **No hierarchy problem solution:** Radion toy models (if used) do not address moduli stabilization, cosmological constant problem, or Planck-electroweak hierarchy.

8. **No observable predictions:** Topological invariants and localization metrics are discretized toy analogs, not continuum field theory predictions. No particle masses, no cross-sections, no LHC predictions.

**Why explicit non-claims matter:** Toy-model papers are frequently over-interpreted. By front-loading Table 8 in the Abstract and Introduction, we establish clear scope boundaries before presenting results. This protects against both peer-review scope inflation and post-publication misrepresentation.

---

## 1.6 Paper Organization

The remainder of this paper is organized as follows:

**Section 2 (Motivation)** contextualizes the validation challenge within the broader landscape of toy spectral geometry, lattice field theory, and computational mathematical physics. We review common failure modes (discretization artifacts, seed sensitivity, window dependence) and argue why falsification-first workflows are necessary.

**Section 3 (GeoSpectra Falsification Ladder)** presents the complete ladder protocol: gate definitions, progressive profiles (smoke/standard/full), caveat discovery workflow, and release integrity audits. This section is the methodological core of the paper.

**Section 4 (Controls and Gates)** details the design of positive controls (W=0 clean cases), negative controls (q=0 disordered cases), and the five core gates (Hermiticity, shape, reproducibility, positive control, negative control). We explain why each gate is necessary and how pass/fail criteria were chosen.

**Section 5 (Operator Construction)** describes product-discretized Kronecker-sum operators (D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1) and the three S¹ discretization families (`spectral_circle`, `ring`, `wilson_ring`). This provides technical context for the case study.

**Section 6 (Case Study: S²×S¹ Full Diagnostic)** presents the v0.1.15 validation chain (Table 1): full diagnostic results (6615 cases, 99.1% localized), reproducibility pass (6615/6615 matched), independent audit (classification confirmed), and core gates pass rate (Table 3, 100% across all gates).

**Section 7 (Caveat Discovery: Ring/alpha=0 Small-Lattice Artifact)** narrates the targeted follow-up investigation (1349 cases) that resolved the 51 `ring/alpha=0` failures. We present lattice-size scaling results (Figure 7, Table 5), apply Decision Rule 1, and derive the production guideline (s1_size ≥ 64).

**Section 8 (Independent Audit and Release Integrity)** describes external review protocols and the release integrity audit (baseline references, scientific non-claims verification, artifact completeness, repository hygiene, cross-file consistency).

**Section 9 (Limitations and Non-Claims)** expands Table 8 (Scientific Non-Claims) into detailed subsections, explaining why each non-claim is necessary and what future work would be required to address it.

**Section 10 (Future Work)** outlines three tracks: Track A (publication-readiness, this paper), Track B (Wilson audit and fermion-doubling diagnostics), and Track C (S²×S² product geometry scaling). We clarify which non-claims are addressable by future toy-model work (continuum extrapolation, S⁶) and which are fundamentally out of scope (Standard Model, observable predictions).

**Section 11 (Conclusion)** summarizes the methodological contribution (Falsification Ladder as reusable template), the case study outcome (S²×S¹ validated with refined caveat), and the broader lesson (toy-model validation requires explicit falsification protocols, not just green tests).

---

## 1.7 Intended Audience and Contribution Type

**Primary audience:** Computational mathematical physicists and numerical analysts working with discretized spectral operators, lattice field theories, or finite-element models in toy-model regimes. Readers interested in reproducible validation workflows for exploratory numerical investigations.

**Secondary audience:** Spectral geometry theorists interested in practical Anderson localization benchmarks and Dirac operator index computations on product manifolds. Readers seeking concrete examples of how falsification-first protocols improve scientific clarity.

**Tertiary audience:** Lattice QCD practitioners and lattice toy-model builders interested in convergence diagnostics, caveat discovery workflows, and production guideline derivation from failure-mode analysis.

**NOT the intended audience:** Physical phenomenology or experimental particle physics communities. This paper does not derive physical predictions, propose experimental tests, or claim relevance to LHC observables. Readers seeking physical compactification mechanisms or Standard Model derivations should look elsewhere.

**Contribution type:** This is a **methodology paper**, not a physics result. We validate a workflow for discretized toy operators, NOT a physical compactification mechanism. Our primary contribution is the Falsification Ladder workflow (Section 3), demonstrated via a case study (Sections 6-7). The S²×S¹ validation is an *illustration* of the method, not a physical discovery. We claim reproducibility, numerical robustness, and methodological rigor—not physical insight.

---

## 1.8 Reproducibility and Artifacts

All validation artifacts for v0.1.15 are preserved in the GeoSpectra Lab repository (commit 65b6973, annotated tag `v0.1.15-s2-s1-product-discretized-full`). The full diagnostic run (6615 cases, ~16 hours) and ring/alpha=0 follow-up (1349 cases, ~2.5 hours) are archived locally in `reports/RUNS/` (280 MB, git-ignored). Aggregated results, metrics, and summary tables are available in git-tracked reports (`RELEASE_NOTES_v0.1.15.md`, `VALIDATION_STATUS.md`, `SPECTRAL_REPORT.md`).

**Test suite:** 203 pytest tests passed (1 warning) at release. Tests cover operator construction, gate logic, localization metrics, and reproducibility checks.

**Figure and table data:** All figures (F1-F11) and tables (T1-T10) source data extracted from validation artifacts into `reports/FIGURE_DATA_*.md` files for paper-ready insertion.

**Code availability:** GeoSpectra Lab is an internal research harness. We provide aggregate results and methodology documentation; raw eigenvalue data (`.npz` files, multiple GB) are not published but available upon request for independent audit.

**Reproducibility claim:** Given the git commit, pytest suite, and archived RUNS artifacts, an independent party can verify:
1. Core gates pass rate (100% across 6615 cases)
2. Reproducibility (6615/6615 matched)
3. Lattice-size scaling (0/252 failures at s1_size≥64)
4. Negative control robustness (0/945 false positives)

We do *not* claim bit-for-bit reproducibility of eigenvalues (numerical linear algebra is platform-dependent). We claim reproducibility of *classification verdicts* (pass/fail, localized/delocalized, artifact/genuine).

---

## 1.9 Terminology and Notation Conventions

To maintain clarity between toy-model regime and physical claims, we adopt the following terminology conventions throughout this paper:

**"Toy operator"** — Discretized spectral operator on finite lattice with no claim of continuum validity.

**"Discretized"** — Finite-dimensional matrix representation (no infinitesimal limits).

**"Localized"** — Passes Anderson IPR gates (kernel_only, fixed_window, window_robust). Numerical classification, not physical mechanism.

**"Convergence"** — Discretized operator behavior stabilizes at larger finite lattice size (failure rate below threshold, reproducible across seeds). Does NOT imply continuum extrapolation. Does NOT guarantee that the discretized operator fully represents the intended mathematical object—only that it is numerically stable within the tested toy construction.

**"Validation"** — Falsification Ladder workflow completed. Does NOT imply physical proof.

**"Artifact"** — Numerical pattern that vanishes at higher resolution or changes with seed/window choice. Predictable, documented, and bounded.

**"Caveat"** — Documented limitation or parameter-range restriction derived from failure-mode analysis. Example: "ring/alpha=0 requires s1_size ≥ 64."

**"Production guideline"** — Empirical recommendation for parameter choices based on failure rates. Example: "Use s1_size ≥ 64 for ring/alpha=0."

**Notation:** We write $D_{S^2 \times S^1}$ for product-discretized operators, $\text{IPR}_k$ for Inverse Participation Ratio of eigenstate $k$, and $\alpha \in \{0.0, 0.25, 0.5\}$ for twisted boundary conditions on S¹. Monopole charge $q \in \{0, 1, 2, 3, 4, 6, 26\}$ indexes S² discretizations.

---

## Notes for Subsequent Drafting

**Cross-references to complete:**
- Figure 1 (Falsification Ladder Workflow Diagram) — conceptual diagram, not yet generated
- Figure 7 (Lattice-Size Scaling) — PNG generated at `reports/figures/F7_lattice_size_scaling.png`
- Figure 8 (Claim Ladder Pyramid) — conceptual diagram, not yet generated
- Table 1 (Validation Chain) — data ready at `reports/FIGURE_DATA_VALIDATION_CHAIN_v0.1.16.md`
- Table 3 (Core Gates Pass Rate) — data ready at `reports/FIGURE_DATA_CORE_GATES_v0.1.16.md`
- Table 5 (Lattice-Size Scaling) — data ready at `reports/FIGURE_DATA_LATTICE_SIZE_SCALING_v0.1.16.md`
- Table 8 (Scientific Non-Claims) — data ready at `reports/FIGURE_DATA_SCIENTIFIC_NONCLAIMS_v0.1.16.md`

**Tone adjustments needed:**
- Section 1.1 (Motivation) — verify balance between "validation is hard" and "we have a solution" (not too dramatic)
- Section 1.5 (Non-Claims) — ensure ALL 8 non-claims from Table 8 are mentioned (currently summarized, expand if needed)
- Section 1.7 (Audience) — verify "NOT the intended audience" phrasing is not overly harsh (softened already)

**Word count:** ~2850 words (target: 2500-3000 for Introduction). Within acceptable range.

**Next sections to draft:**
1. Section 2 (Motivation) — broader context, literature review, failure modes
2. Section 3 (Falsification Ladder) — core methodology, ladder rungs, progressive profiles
3. Section 6 (Case Study) — detailed narrative of v0.1.15 validation chain

---

**Draft status:** FIRST DRAFT — ready for internal review (skeptic agent recommended before polishing).

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)

**Pytest:** NOT required (docs-only, no code changes)

**Scientific non-claims:** 8 explicit non-claims maintained throughout (Table 8 reference in Section 1.5)
