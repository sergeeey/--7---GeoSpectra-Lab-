# Section 10 — Conclusion and Future Work

**v0.1.16 Methodology Paper**  
**Date:** 2026-05-16  
**Baseline:** v0.1.15-s2-s1-product-discretized-full

---

## Section Thesis

GeoSpectra Lab demonstrates a **falsification-first validation workflow** for finite-lattice discretized spectral operators on compact toy manifolds. The v0.1.15 case study — S²×S¹ product-discretized full diagnostic (6615 cases + 1349 targeted follow-up) — validates the methodology in a confined scope: low-dimensional test geometries, finite lattices, and three S¹ discretization families.

This paper does **NOT** prove physical compactification, continuum limits, Standard Model derivation, or observable predictions. It documents a **reproducible methodology** for detecting localized failure modes, deriving empirical production guidelines, and maintaining scope discipline across multi-file artifact chains.

The contribution is **methodological**: a workflow that makes toy spectral diagnostics harder to fool by enforcing controls, progressive profiles, independent audit, and explicit non-claims. The S²×S¹ results are **toy evidence**, not physical claims — they demonstrate the workflow works, not that compactification physics is validated.

---

## 10.1 Summary of Contributions

This paper presents eight methodological advances validated through the v0.1.15 case study:

### 10.1.1 Falsification-First Validation Ladder

**Contribution:** A four-tier hierarchical validation chain (Section 3) that enforces:
- **Tier 0 (Controls):** q=0 gates prevent spurious localization on monopole-free operators.
- **Tier 1 (Baseline Gates):** Hermiticity, shape consistency, reproducibility validate operator construction.
- **Tier 2 (Diagnostic Gates):** Disorder contrast, localization metrics (IPR, r-statistics), window-robust gates detect Anderson localization.
- **Tier 3 (Cross-Family Robustness):** Spectral_circle and wilson_ring serve as reference families — if ring fails but both references pass, failure is family-specific artifact, not systemic.

**Evidence (v0.1.15):**
- Tier 0: q=0 false positives = 0 (945 clean control cases)
- Tier 1: 6615/6615 pass (Hermiticity, shape, reproducibility)
- Tier 2: 5619/5670 disordered cases show localization (99.1%)
- Tier 3: Spectral_circle and wilson_ring: 0 disordered failures (2205+2205 cases); ring: 51 failures (100% localized to alpha=0, s1_size<64)

**Reusability:** The ladder structure (controls → baseline → diagnostic → cross-family) is **geometry-independent** and applicable to any operator class or manifold.

### 10.1.2 Control and Gate Framework

**Contribution:** Explicit gate definitions with pass/fail criteria (Section 4):
- **q=0 gate:** No spurious localization on monopole-free S² operators.
- **Hermiticity gate:** `||D - D†|| < ε` for all operators.
- **Reproducibility gate:** Identical eigenvalue checksums across seeded re-runs.
- **Localization gate (v3):** Window-robust IPR contrast, requires consistent signal across multiple spectral windows.

**Evidence (v0.1.15):**
- q=0 gate: 0/945 false positives (100% specificity)
- Hermiticity gate: 6615/6615 pass (max residual ≤ 1e-9)
- Reproducibility gate: 6615/6615 identical re-computation
- Localization gate v3: 5619/5670 pass on disordered cases (51 failures, all ring/alpha=0)

**Reusability:** Gate framework is **operator-agnostic** — define gates for new operator classes by specifying pass/fail criteria and control cases.

### 10.1.3 Progressive Profile Analysis

**Contribution:** Pre-diagnostic exploration workflow (Section 5) that samples parameter space before committing to full grid:
- **Tiny smoke (≤10 cases):** Operator construction sanity check.
- **W0/W8 control (20-50 cases):** Clean vs strong disorder anchor points.
- **Medium diagnostic (1000-2000 cases):** Mid-scale parameter sweep.
- **Targeted smoke (50-200 cases):** Parameter-specific stress tests.

**Evidence (v0.1.15):**
- Progressive profiles detected ring/alpha=0 fragility **before full diagnostic** (1080-case medium run showed failures concentrated at ring/alpha=0).
- Targeted follow-up (1349 cases) refined caveat: failures vanish at s1_size≥64.

**Reusability:** Progressive profiles prevent wasted computation on fragile parameter regimes — detect failures early, investigate before scaling to full grid.

### 10.1.4 Full Diagnostic at Scale

**Contribution:** 6615-case overnight run (16 hours) demonstrated computational feasibility of exhaustive parameter sweeps on product manifolds.

**Evidence (v0.1.15):**
- 6615 total cases: 3 families × 7 monopole charges × 5 lattice sizes × 2 twist angles × 6 disorder strengths × multiple seeds
- 100% completion rate (guarded runner protocol with failure recovery)
- Artifacts preserved: config.json, metrics.json (13 MB), data.npz, summary.md, figures

**Reusability:** Guarded runner protocol (failure recovery, progress tracking, incremental artifact saving) is reusable for any large-scale diagnostic.

### 10.1.5 Independent Within-Project Artifact Audit

**Contribution:** Eight-aspect audit framework (Section 8) that verifies documentation-artifact consistency:
1. Data integrity (run completion, arithmetic)
2. Statistical claims (failure rates, sample sizes)
3. Test suite quality (regression protection)
4. Scope protection (scientific non-claims)
5. Audit independence (methodology transparency)
6. Artifact completeness (reproducibility requirements)
7. Red flags (subspace failure concentration)
8. Scientific rigor (falsification-first compliance)

**Evidence (v0.1.15):**
- Audit identified 2 interpretation discrepancies (ring/alpha=0 breakdown: 37 complete + 14 window-sensitive, not "all both-fail")
- 4 minor documentation updates applied (commit c20b0b9)
- Verdict: APPROVED WITH MINOR DOCUMENTATION UPDATES

**Reusability:** Eight-aspect framework catches interpretation drift and documentation-artifact divergence — reusable for any release baseline.

### 10.1.6 Caveat Discovery and Resolution Workflow

**Contribution:** Systematic investigation of localized failure modes (Section 7):
1. **Detection:** Progressive profiles or full diagnostic identifies subspace with high failure rate.
2. **Investigation:** Targeted follow-up tests parameter scaling hypothesis (e.g., lattice-size dependence).
3. **Classification:** Decision rules (SMALL_LATTICE_ARTIFACT vs PERSISTENT_LIMITATION) based on empirical thresholds.
4. **Guideline derivation:** Operational constraints derived from empirical evidence (s1_size≥64 for ring/alpha=0).
5. **Documentation:** Caveats recorded in all release materials with evidence chain.

**Evidence (v0.1.15):**
- Ring/alpha=0 subspace: 51/~630 failures (8.3% rate, not hidden by 0.9% aggregate)
- Targeted follow-up: 1349 cases, s1_size extended to 64, 96
- Result: 0/252 failures at s1_size≥64 → verdict SMALL_LATTICE_ARTIFACT
- Production guideline: s1_size≥64 for ring/alpha=0

**Reusability:** Detection → investigation → classification → guideline workflow applies to any localized failure mode in any geometry or operator class.

### 10.1.7 Release Integrity Gates

**Contribution:** Baseline promotion criteria (Section 8.7) that enforce falsification-first discipline:
- Critical gates passed (q=0, Hermiticity, reproducibility)
- Caveats documented and addressed (not hidden)
- Failure signals investigated (not dismissed)
- Scope protection maintained (eight scientific non-claims explicit)
- Documentation-artifact consistency verified (independent audit)

**Evidence (v0.1.15):**
- All 5 promotion criteria met
- Baseline promoted: v0.1.15-s2-s1-product-discretized-full
- Timeline: same-day audit (detection → correction → promotion within 24 hours)

**Reusability:** Promotion criteria are **baseline-agnostic** — any release must satisfy the same five criteria before operational use.

### 10.1.8 Claim Discipline and Explicit Non-Claims

**Contribution:** Eight scientific non-claims (Section 9.6, Table 9.1) prevent misinterpretation of toy diagnostics as physical proofs:
1. No continuum compactification
2. No S⁶/S³×S⁶ validation
3. No Standard Model derivation
4. No physical chirality proof
5. No Witten/Lichnerowicz bypass
6. No physical extra dimensions
7. No hierarchy problem solution
8. No observable predictions

**Evidence (v0.1.15):**
- All eight non-claims stated in release notes, milestone documents, paper drafts
- Audit verified consistency across six documentation files
- No physics overclaims detected in 25,650-word paper draft corpus

**Reusability:** Non-claims table is **mandatory** for any toy-model paper — prevents scope inflation and retraction risk.

---

## 10.2 What v0.1.15 Established

The v0.1.15 case study established the following **within tested scope** (S²×S¹ product-discretized, finite lattices, three S¹ families):

### 10.2.1 Quantitative Validation Results

**Full diagnostic (6615 cases):**
- **Total completion:** 6615/6615 cases (100%)
- **Reproducibility:** 6615/6615 seeded re-runs matched exactly
- **q=0 false positives:** 0/945 clean controls (100% specificity)
- **Hermiticity:** 6615/6615 operators (max residual ≤ 1e-9)
- **Disordered localization:** 5619/5670 cases (99.1%)
- **Cross-family robustness:** Spectral_circle: 0/2205 failures, wilson_ring: 0/2205 failures, ring: 51/1260 failures

**Targeted follow-up (1349 cases):**
- **Ring/alpha=0 at s1_size≥64:** 0/252 failures (0.0%)
- **Decision Rule 1 applied:** 0.0% < 2.0% threshold → verdict SMALL_LATTICE_ARTIFACT
- **Statistical confidence:** 95% CI upper bound ≈ 1.2% (Rule of Three: 3/252)

### 10.2.2 Empirical Production Guideline

**Derived from evidence:**

> **Ring/alpha=0:** s1_size ≥ 64 required for robustness (empirical threshold, not theorem)  
> **Ring/alpha≠0:** s1_size ≥ 32 sufficient (no failures observed in 6615-case grid)  
> **Spectral_circle, wilson_ring:** Robust at all tested s1_size (8-96)

**Caveat localization:**
- All 51 failures: ring family only (0 failures in spectral_circle or wilson_ring)
- All 51 failures: alpha=0.0 only (0 failures at alpha=0.5 twisted boundary)
- All 51 failures: s1_size<64 only (0 failures at s1_size≥64)

**Interpretation:** Ring discretization of S¹ at alpha=0 (periodic boundary) requires larger lattices for numerical stability. This is a **discretization convergence threshold**, not a fundamental limitation of ring construction.

### 10.2.3 Baseline Promotion

**Baseline:** v0.1.15-s2-s1-product-discretized-full

**Promotion justification:**
- All critical gates passed (q=0, Hermiticity, shape, reproducibility, disorder contrast)
- Caveats documented and addressed (ring/alpha=0 investigated via 1349-case follow-up)
- Failure rate 0.77% (51/6615 total) acceptable for toy harness
- Spectral_circle and wilson_ring fully robust (2205+2205 = 4410 cases, 0 failures)
- Independent audit verified documentation accuracy (4 minor corrections applied)

**Operational status:** Baseline approved for internal use within GeoSpectra Lab. External peer review required for publication.

### 10.2.4 Test Suite Status

**Pytest coverage:**
- **203 tests passed, 1 warning** (2026-05-16)
- Test categories: core geometry (S², S³, S⁶, products), spectral analysis (Dirac operators, localization gates), radion stabilization, topology (Chern numbers, Dirac indices), discovery ledger, product-discretized diagnostics

**Regression protection:**
- Historical window-selection seeds (12051, 12053, 9836055): all pass (resolution applied 2026-05-15)
- Full diagnostic results reproducible (6615/6615 seeded re-runs)

---

## 10.3 What Remains Open

The v0.1.15 case study does **NOT** establish the following — each requires independent validation before claims can be made:

### 10.3.1 Continuum Extrapolation Not Performed

**What is missing:**
- No systematic scaling study (s1_size = 64, 96, 128, 192, 256, 512, 1024...)
- No continuum limit extrapolation (fit δ(s1_size), Richardson extrapolation, finite-size scaling)
- No error bounds (quantify discretization error δ→0 as s1_size→∞)

**Current status:** s1_size≤96 is **finite-lattice evidence**. Failure disappearance at s1_size≥64 is **empirical stability** (discretization convergence), NOT continuum convergence (approach to continuum Dirac operator).

**Required for continuum claim:** Power-law fit of discretization error vs lattice size, extrapolation to s1_size→∞, verification that extrapolated value matches continuum reference (if known).

### 10.3.2 S²×S¹ Only — No Transfer to Higher Dimensions

**What is missing:**
- S⁶ (6-dimensional sphere) NOT constructed
- S³×S⁶ (9-dimensional Kaluza-Klein product) NOT tested
- Calabi-Yau manifolds NOT attempted
- No evidence that product-discretization method scales to higher dimensions

**Current status:** v0.1.15 validates **S²×S¹ operators only**. S² (2D), S³ (3-sphere), S¹ (circle) are low-dimensional test geometries. No claim that results transfer to S⁶, S³×S⁶, or physical compactification spaces.

**Required for generalization:** Independent case study for each new geometry starting from controls (q=0 gates, Hermiticity, reproducibility). Falsification ladder reset for every dimensional jump.

### 10.3.3 Wilson / Fermion-Doubling Audit Not Complete

**What is missing:**
- No explicit fermion-doubling detection (doubled eigenvalue count check)
- No axial symmetry check (Ward identity for axial current)
- No continuum limit recovery test (verify O(a) Wilson term → 0 as s1_size→∞)

**Current status:** Wilson_ring passed **operational robustness tests** (0 failures, localization gates passed). It does NOT validate **fermion-doubling physics** (whether doublers are suppressed as intended).

**Required for fermion-doubling claim:** Count eigenvalue multiplicity (expect 1× modes, not 2× or 4×), compute axial current violation, compare wilson_ring vs ring eigenvalue spectra at large s1_size.

### 10.3.4 No Physical Chirality Proof

**What is missing:**
- No gauge coupling (SU(3)×SU(2)×U(1))
- No Yukawa couplings (fermion masses)
- No chiral anomaly cancellation (triangle diagrams)
- No electroweak symmetry breaking (Higgs mechanism)

**Current status:** Dirac indices are **topological toy counts** on discretized manifolds. They validate **topological index computation**, NOT physical chiral fermions or Standard Model chirality structure.

**Required for physical chirality claim:** Gauge group calculation, anomaly cancellation check, fermion mass hierarchy from Yukawa sector, comparison to Standard Model fermion content.

### 10.3.5 No S⁶/S³×S⁶ Validation

**What is missing:**
- S⁶ manifold NOT constructed
- S³×S⁶ product NOT attempted
- No evidence of operator scaling to 6D or 9D geometries

**Current status:** Only low-dimensional test geometries (S²: 2D, S³: 3-sphere, S¹: circle, S²×S¹: 3D product) validated.

**Required for S⁶ claim:** Construct S⁶ discretization, run falsification ladder from scratch, validate gates independently. No inheritance from S²×S¹ results without verification.

### 10.3.6 No Standard Model Derivation

**What is missing:**
- No gauge group calculation
- No fermion generations (only topological zero-mode counts)
- No QCD confinement, no electroweak breaking
- No particle content (quarks, leptons, Higgs)

**Current status:** Toy Dirac operators with topological indices. No connection to Standard Model gauge structure or particle physics.

**Required for Standard Model claim:** Derive SU(3)×SU(2)×U(1) from geometry, compute fermion representations, verify anomaly cancellation, explain three generations.

### 10.3.7 No External Peer Review Yet

**What is missing:**
- No external domain expert review (differential geometry, lattice field theory, numerical analysis)
- No independent code review (third-party inspection of cc_toy_lab/ computational core)
- No third-party reproducibility (external group re-running 6615-case diagnostic)

**Current status:** v0.1.15 approved by **internal audit** (independent within-project artifact verification). This is sufficient for baseline promotion, NOT for publication.

**Required for publication:** External domain expert reviews methodology, operator construction, scope claims. Independent physicist inspects code. External team confirms reproducibility on different hardware.

---

## 10.4 Future Work Track A — Publication and Reproducibility

### 10.4.1 Assemble Full Draft

**Current status (v0.1.16):**
- 10 sections drafted: Introduction, Motivation, Falsification Ladder, Controls/Gates, Progressive Profiles, Case Study, Caveat Discovery, Audit, Limitations, Conclusion
- Supporting data files: 7 figure data documents (validation chain, core gates, lattice-size scaling, progressive profiles, scientific non-claims, controls gates, figures inventory)
- Paper outline: `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md`

**Next steps:**

1. **Integrate sections:** Merge 10 standalone section files into single manuscript (reports/METHODOLOGY_PAPER_DRAFT_v0.1.16.md).

2. **Generate minimal figures/tables:**
   - Table 1 (Validation Chain): 8 steps from controls to baseline promotion
   - Table 3 (Core Gates Pass Rate): q=0, Hermiticity, reproducibility results
   - Figure 5 (Progressive Profile): W0 vs W8 contrast detection
   - Figure 7 (Lattice-Size Scaling): ring/alpha=0 failures vs s1_size
   - Table 9.1 (Scientific Non-Claims): 8 explicit scope boundaries

3. **Abstract and acknowledgments:** Write 200-word abstract referencing Table 9.1 (non-claims), add acknowledgments section.

4. **Cross-reference audit:** Verify all figure/table citations are consistent, all section references resolve.

### 10.4.2 Public README Cleanup

**Purpose:** Make repository navigable for external reviewers and third-party reproducibility attempts.

**Tasks:**

1. **Root README.md:**
   - Project description (falsification-first validation harness for toy spectral operators)
   - Quick start (install cc_toy_lab, run pytest, reproduce v0.1.15 diagnostic)
   - Link to methodology paper draft
   - Link to scientific non-claims (Table 9.1)

2. **Installation guide:**
   - Dependencies (Python 3.11+, NumPy, SciPy, pytest)
   - Environment setup (conda environment.yml or requirements.txt)
   - Platform notes (tested on Windows 11, should work on Linux/Mac)

3. **Reproducibility guide:**
   - How to re-run full diagnostic (scripts/s2_s1_product_discretized.py)
   - Expected runtime (16 hours on 8-core CPU)
   - Artifact locations (reports/RUNS/)
   - Checksum verification (compare metrics.json checksums)

### 10.4.3 External Domain Expert Review

**Objective:** Submit methodology paper draft to external physicist for pre-publication review.

**Candidates:**
- Lattice field theory expert (fermion discretization, Wilson term, doubler suppression)
- Differential geometry expert (Dirac operators, Atiyah-Singer index, spectral methods)
- Numerical analysis expert (eigenvalue solvers, finite-size scaling, error bounds)

**Review focus:**
- **Methodology validity:** Is falsification-first workflow scientifically sound?
- **Operator construction:** Do product-discretized operators correctly represent toy Dirac operators?
- **Scope claims:** Are limitations and non-claims appropriate? Any overclaims?
- **Reproducibility:** Is documentation sufficient for third-party replication?

**Timeline:** Allow 4-6 weeks for external review, 2 weeks for revisions.

### 10.4.4 Artifact Archival and Git LFS Policy

**Current status:** Run artifacts (metrics.json: 13 MB, partial_results.jsonl: 9.9 MB) stored locally in reports/RUNS/.

**Future policy:**

1. **Git LFS (Large File Storage):**
   - Store artifacts >5 MB in Git LFS (metrics.json, data.npz, partial_results.jsonl)
   - Keep summary.md, config.json, figures/ in standard Git

2. **Long-term archival:**
   - Upload run artifacts to Zenodo or Figshare (DOI-backed permanent storage)
   - Include DOI in paper "Data Availability" section

3. **Minimal reproducibility package:**
   - Create tarball with: config.json, summary.md, minimal test subset (100 cases)
   - Upload to paper supplementary materials (<50 MB limit for most journals)

**Timeline:** Archive v0.1.15 artifacts before preprint submission (within 1 month).

---

## 10.5 Future Work Track B — Operator Credibility

### 10.5.1 Wilson / Fermion-Doubling Audit

**Objective:** Verify that wilson_ring discretization suppresses fermion doublers as intended.

**Tasks:**

1. **Eigenvalue multiplicity check:**
   - Count eigenvalues near zero (|λ| < tolerance)
   - Verify count matches Dirac index (q for monopole charge q)
   - Detect doubling: if count = 2q, doublers present; if count = q, doublers suppressed

2. **Axial current Ward identity:**
   - Compute axial current operator A_μ = ψ̄ γ_μ γ_5 ψ
   - Check ∂_μ A^μ = 2m ψ̄ γ_5 ψ (Wilson term breaks chiral symmetry)
   - Verify breaking is controlled (proportional to lattice spacing a)

3. **Continuum limit test:**
   - Scale s1_size: 64 → 96 → 128 → 192 → 256
   - Verify O(a) Wilson term correction → 0 as s1_size→∞
   - Compare wilson_ring vs ring eigenvalue spectra (should converge at large s1_size)

**Expected outcome:** Wilson_ring either passes fermion-doubling audit (doublers suppressed, axial breaking controlled) or requires construction refinement.

**Timeline:** 2-4 weeks (new diagnostic module, 500-1000 test cases).

### 10.5.2 Dirac Operator Checks

**Objective:** Verify that discretized Dirac operators satisfy expected algebraic properties beyond Hermiticity.

**Tasks:**

1. **Gamma matrix algebra:**
   - Verify {γ_μ, γ_ν} = 2g_μν (Clifford algebra)
   - Check γ_5^2 = 1 (chirality operator squares to identity)
   - Verify {D, γ_5} anticommutator structure (chirality blocks)

2. **Spectrum symmetry:**
   - Check +λ / -λ eigenvalue pairing (chiral symmetry)
   - Verify zero-mode count matches topological index (Atiyah-Singer)
   - Test degeneracy: eigenvalues should appear in ±λ pairs

3. **Gauge covariance:**
   - Test operator transformation under gauge transformations (if gauge coupling added in future)
   - Verify covariant derivative structure (currently minimal coupling only)

**Expected outcome:** Dirac operators pass algebraic checks (Clifford algebra, chirality, spectrum symmetry) or reveal construction errors.

**Timeline:** 1-2 weeks (extend existing test suite, no new runs required).

### 10.5.3 Near-Zero Mode Controls

**Objective:** Distinguish numerical near-zero modes (eigenvalues close to zero due to finite precision) from topological zero modes (protected by index theorem).

**Tasks:**

1. **Tolerance scan:**
   - Vary zero-mode threshold: |λ| < ε for ε = 1e-6, 1e-8, 1e-10, 1e-12
   - Count near-zero modes at each threshold
   - Verify count stabilizes (topological zeros) or grows (numerical noise)

2. **Perturbation stability:**
   - Add small random perturbation to operator: D → D + δ (||δ|| ~ 1e-6)
   - Re-compute eigenvalues
   - Verify near-zero modes move (numerical noise) or persist (topological protection)

3. **Index comparison:**
   - Compute topological index via Atiyah-Singer (analytical formula for S²)
   - Count numerical near-zero modes
   - Verify counts match: numerical zero count = topological index

**Expected outcome:** Near-zero modes are confirmed as topologically protected (match index, stable under perturbation) or classified as numerical noise (threshold-dependent, perturbation-sensitive).

**Timeline:** 1 week (extend existing chirality diagnostic).

### 10.5.4 Avoid Chirality Overclaim

**Objective:** Maintain clear distinction between topological index (toy count) and physical chirality (gauge-coupled fermions).

**Policy:**

1. **Terminology discipline:**
   - Use "topological index" or "zero-mode count," NOT "chiral fermions"
   - Use "discretized Dirac operator," NOT "physical fermion field"
   - Use "toy compactification diagnostic," NOT "Standard Model derivation"

2. **Required caveats (mandatory in all operator papers):**
   - No gauge coupling (SU(3)×SU(2)×U(1) NOT present)
   - No Yukawa sector (fermion masses NOT derived)
   - No anomaly cancellation (triangle diagrams NOT computed)
   - Topological index ≠ physical chirality (index counts zero modes, NOT particles)

3. **Peer review checkpoint:**
   - External domain expert must confirm: "This is topological index computation, NOT physical chirality proof"
   - Any reviewer concern about chirality overclaim → immediate revision

**Expected outcome:** All operator papers maintain toy scope discipline, no physics overclaims.

**Timeline:** Ongoing (policy enforcement in every draft, every review).

---

## 10.6 Future Work Track C — Geometry Generalization

### 10.6.1 S²×S² Product Geometry (Next Priority)

**Objective:** Extend product-discretization method to S²×S² (2-sphere × 2-sphere), validating that Kronecker-sum construction works on symmetric products.

**Why S²×S² before S³ or S⁶:**
- **Same dimensionality as S²×S¹:** Both are 4D (S²: 2D, S²: 2D). Operator size scaling similar.
- **Symmetric product test:** S²×S² tests whether construction works when both factors are spheres (no circle degeneracy).
- **Known topology:** S²×S² has b₁=0 (no H¹), b₂=2 (two H² generators). Simpler than S⁶ (b₃=1) or Calabi-Yau (nontrivial Hodge numbers).

**Tasks:**

1. **Operator construction:**
   ```
   D_S2×S2 = D_S2(q1) ⊗ I_S2 + Γ_S2 ⊗ D_S2(q2)
   ```
   where q1, q2 are monopole charges on each S² factor.

2. **Falsification ladder (from scratch):**
   - Tier 0: q1=0, q2=0 control (no topological charge on either factor)
   - Tier 1: Hermiticity, shape, reproducibility
   - Tier 2: Disorder contrast (add disorder to second S² factor)
   - Tier 3: Cross-family robustness (test three discretization families for second S²)

3. **Progressive profiles:**
   - Tiny: 10 cases (q1, q2) ∈ {0, 1, 2}
   - Medium: 500 cases (q1, q2 grid, disorder sweep)
   - Full: 3000-5000 cases (full parameter space)

**Expected challenges:**
- **Operator size:** S²×S² operator ~ (100-400) × (100-400) = 10⁴-10⁵ (larger than S²×S¹)
- **Diagonalization cost:** O(N³) ~ 10¹²-10¹⁵ FLOPs (may require sparse solvers or iterative methods)
- **Topology complexity:** Index formula for S²×S² more complex than S²×S¹ (two monopole charges interact)

**Timeline:** 2-3 months (construction + validation + audit).

### 10.6.2 S³ / S³×S¹ Products (Later Priority)

**Objective:** Extend to S³ (3-sphere) and S³×S¹ products after S²×S² validated.

**Why S³ is harder than S²:**
- **Dimension:** S³ is 3D, S² is 2D → operator size scales cubically vs quadratically.
- **Topology:** S³ has b₁=0, b₂=0, b₃=1 (one H³ generator) → index formula involves harmonic forms on S³.
- **Discretization:** Spherical harmonics on S³ are Wigner D-functions (more complex than S² spherical harmonics).

**Tasks:**

1. **S³ discretization family selection:**
   - Spectral truncation (Wigner D-functions)
   - Finite-element method (tetrahedral mesh on S³)
   - Hopf fibration coordinates (S³ as S¹ bundle over S²)

2. **Falsification ladder for S³:**
   - Controls: q=0 on S³ (no monopole analog, but topological charge exists)
   - Dirac operator construction: Use spin connection on S³
   - Index formula: Atiyah-Singer for S³ (depends on gauge field if present)

3. **S³×S¹ product:**
   - Combine S³ discretization with S¹ families (spectral_circle, ring, wilson_ring)
   - Test cross-family robustness (S³ discretization × S¹ family)

**Expected challenges:**
- **Operator size:** S³×S¹ operator ~ (10³-10⁴) × (10-100) = 10⁴-10⁶ (large-scale sparse diagonalization required)
- **Computational cost:** May require GPU acceleration or distributed computing
- **Topology:** Index formula more complex (S³ index + S¹ twist interaction)

**Timeline:** 6-12 months (after S²×S² complete).

### 10.6.3 No Direct Jump to S⁶/S³×S⁶

**Rationale:**

S⁶ (6-dimensional sphere) and S³×S⁶ (9-dimensional Kaluza-Klein product) are **NOT next priorities** because:

1. **Dimensional scaling:** S⁶ operator size ~ 10⁹, S³×S⁶ ~ 10¹⁵ (infeasible for direct diagonalization with current methods).

2. **Precedent required:** Must validate S²×S², S³×S¹ first to establish:
   - Product-discretization method works on symmetric products (S²×S²)
   - Method extends to 3D factors (S³)
   - Cross-family robustness holds for higher-dimensional products

3. **Physics gap:** Even if S⁶ operators were constructed, NO claim about physical compactification is justified without:
   - Continuum extrapolation (currently missing)
   - Gauge coupling (SU(3)×SU(2)×U(1) NOT present)
   - Fermion-doubling audit complete (Track B)

**Policy:** No S⁶ or S³×S⁶ work begins until:
- ✅ S²×S² validated (Track C.1)
- ✅ S³×S¹ validated (Track C.2)
- ✅ Wilson/fermion-doubling audit complete (Track B.1)
- ✅ External peer review approves methodology paper (Track A.3)

**Timeline:** 2-3 years minimum (after all prerequisites).

---

## 10.7 Future Work Track D — Anti-Artifact Robustness

### 10.7.1 Cross-Discretization Robustness

**Objective:** Verify that key results (localization, index counts, production guidelines) are **NOT artifacts of one discretization family**.

**Method:**

For any claimed result (e.g., "s1_size≥64 required for ring/alpha=0"), test across multiple discretization families:

1. **Spectral truncation** (spectral_circle for S¹)
2. **Finite difference** (ring for S¹)
3. **Wilson fermion** (wilson_ring for S¹)
4. **Alternative discretizations** (staggered, overlap, domain-wall if implemented)

**Pass criterion:** Result holds across ≥2 independent discretization families → **cross-discretization robust**.

**Fail criterion:** Result holds in one family but vanishes in another → **family-specific artifact**, NOT geometry property.

**Example (v0.1.15):**
- Ring/alpha=0 fragility: family-specific artifact (spectral_circle and wilson_ring: 0 failures)
- q=0 false positives = 0: cross-family robust (all three families pass)

**Timeline:** Ongoing (test each new result across families before claiming robustness).

### 10.7.2 Finite-Size Scaling

**Objective:** Distinguish **discretization convergence** (failures vanish at large lattice) from **continuum convergence** (operators approach continuum limit).

**Method:**

For any claimed convergence threshold (e.g., s1_size≥64), perform finite-size scaling:

1. **Extrapolation series:** Test s1_size = 32, 48, 64, 96, 128, 192, 256
2. **Fit scaling law:** δ(s1_size) = A / s1_size^α + B (power law) or δ(s1_size) = A exp(-s1_size/ξ) (exponential)
3. **Extrapolate to s1_size→∞:** Estimate continuum value δ(∞)
4. **Error bounds:** Quantify discretization error δ(s1_size) - δ(∞)

**Pass criterion:** δ(∞) converges to known continuum reference (if available) within error bars → **continuum convergence**.

**Current status (v0.1.15):** NO finite-size scaling performed. s1_size≥64 is **empirical stability threshold**, NOT continuum convergence.

**Timeline:** 3-6 months (requires large-scale runs at s1_size≥128).

### 10.7.3 Seed/Window Stability

**Objective:** Verify that results are **NOT artifacts of lucky seed or window choice**.

**Method:**

For any claimed localization signal:

1. **Seed sweep:** Test 10-50 random seeds (not just 4)
2. **Window sweep:** Test 5-10 spectral window definitions (quantile_0.1, quantile_0.3, quantile_0.5, quantile_0.7, quantile_0.9)
3. **Cross-stability:** Result holds across ≥80% seeds AND ≥3 windows → **seed/window stable**

**Fail criterion:** Result holds for one seed or one window but vanishes for others → **seed/window artifact**.

**Example (v0.1.15):**
- 14/51 ring/alpha=0 failures: window-sensitive (kernel-only fails, fixed-window passes)
- Classification: window artifact, NOT robust localization

**Timeline:** Ongoing (test each new result across seeds and windows).

### 10.7.4 Operator-Family Comparisons

**Objective:** Identify which operator properties are **universal** (hold across all families) vs **family-specific** (artifacts of construction method).

**Method:**

For any operator property (Hermiticity, index count, localization threshold):

1. **Test across families:** spectral_circle, ring, wilson_ring (minimum 3)
2. **Compare quantitatively:** Do eigenvalue spectra match? Do zero-mode counts agree? Do localization thresholds align?
3. **Classify:**
   - **Universal:** Property holds identically across all families → geometry property
   - **Family-dependent:** Property varies across families → construction artifact
   - **Family-specific:** Property present in one family, absent in others → family artifact

**Example (v0.1.15):**
- Hermiticity: universal (all families pass)
- Ring/alpha=0 fragility: family-specific (only ring fails)
- Localization gate pass: universal (all families detect disorder contrast)

**Goal:** Build a catalog of **universal vs family-dependent** properties to guide future geometry choices.

**Timeline:** Ongoing (operator-family comparison is mandatory for every new result).

---

## 10.8 Closing Statement

This paper presents a **falsification-first validation workflow** for finite-lattice discretized spectral operators on compact toy manifolds. The v0.1.15 case study — S²×S¹ product-discretized full diagnostic (6615 cases) with targeted follow-up (1349 cases) — validates the methodology in a confined scope: low-dimensional test geometries, finite lattices, and three S¹ discretization families.

**What has been established:**

The workflow **works** in the tested scope. It caught localized failure modes (ring/alpha=0 fragility), triggered investigation (targeted lattice-size scaling), derived empirical production guidelines (s1_size≥64), and maintained scope discipline (eight scientific non-claims explicit). Independent within-project audit verified documentation-artifact consistency (4 minor corrections applied). Baseline v0.1.15-s2-s1-product-discretized-full is approved for internal operational use.

**What has NOT been established:**

This is **NOT proof of physical compactification**. No continuum extrapolation, no S⁶ or S³×S⁶ validation, no Standard Model derivation, no physical chirality proof, no Witten/Lichnerowicz bypass, no observable predictions. The operators are **discretized toys** on **finite lattices** for **toy geometries** (S², S³, S¹, S²×S¹). Results do NOT transfer to higher dimensions, Calabi-Yau manifolds, or physical extra dimensions without independent validation.

**The contribution:**

The contribution is **methodological**, not physical. We have demonstrated a reproducible workflow for making toy spectral diagnostics **harder to fool**:

- **Controls prevent false positives** (q=0 gate: 0/945 spurious localization)
- **Progressive profiles detect failures early** (ring/alpha=0 fragility identified before full diagnostic)
- **Targeted follow-up refines caveats** (s1_size≥64 threshold empirically derived)
- **Independent audit catches interpretation drift** (37 complete + 14 window-sensitive breakdown, not "all both-fail")
- **Explicit non-claims prevent scope inflation** (eight boundaries stated in every release document)

This workflow is **reusable** across operator classes, geometries, and parameter regimes. The S²×S¹ results are **toy evidence** that the workflow catches failures and derives guidelines — they are **NOT physical predictions**.

**Future work:**

Four tracks outlined:
- **Track A (Publication):** External domain expert review, third-party reproducibility, artifact archival.
- **Track B (Operator Credibility):** Wilson/fermion-doubling audit, Dirac operator checks, near-zero mode controls.
- **Track C (Geometry Generalization):** S²×S² next, then S³×S¹, eventual S³×S³. No direct jump to S⁶/S³×S⁶ without prerequisites.
- **Track D (Anti-Artifact Robustness):** Cross-discretization, finite-size scaling, seed/window stability, operator-family comparisons.

Each track requires **independent validation**. No inheritance from S²×S¹ without explicit verification.

**Final discipline:**

Toy diagnostics are **diagnostic tools**, not physical theories. The validated workflow makes them more reliable, more falsifiable, and more transparent — but it does NOT make them physical. The contribution is a **better methodology** for exploring discretized operator behavior on compact manifolds, not a proof that nature works this way.

Future claims about continuum limits, higher dimensions, or physical predictions require:
1. Continuum extrapolation with error bounds (Track D.2)
2. External peer review by domain experts (Track A.3)
3. Third-party reproducibility confirmation (Track A.3)
4. Independent validation on target geometry (Track C)

Until then, **toy scope discipline is mandatory**. This is not modesty — it is **scientific integrity**.

---

**Section 10 complete.** Methodology paper draft (v0.1.16) now complete: 10 sections documenting falsification-first validation workflow for S²×S¹ product-discretized toy operators on finite lattices.

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)  
**Paper status:** Draft complete, pending external review (Track A)  
**Scientific scope:** Toy diagnostics, NOT physical compactification  
**Next milestone:** External domain expert review → preprint submission → journal peer review → publication
