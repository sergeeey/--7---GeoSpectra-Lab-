# Reviewer Questions — v0.1.16 Methodology Manuscript

**Purpose:** Domain-specific technical questions for external reviewers to guide their assessment.

**Three reviewer tracks:**
1. Lattice Field Theory
2. Differential Geometry
3. Numerical Analysis

---

## Track 1: Lattice Field Theory Reviewer Questions

### A. Wilson Term and Fermion Doubling

**Q1.1:** Is the Wilson term implementation (wilson_ring family) correctly constructed for S¹ discretization?
- **Context:** Wilson term adds $-\frac{1}{2} a \sum_\mu \nabla_\mu^2$ to suppress fermion doubling.
- **Manuscript claim:** wilson_ring family shows 0/2205 failures (100% robust), same as spectral_circle.
- **Review focus:** Does wilson_ring correctly suppress fermion doubling, or is 0 failures suspicious (too aggressive suppression)?

**Q1.2:** Should there be explicit fermion-doubling diagnostics beyond localization gates?
- **Context:** ring/alpha=0 shows 51 failures at s1_size<64, but spectral_circle and wilson_ring show 0 failures.
- **Manuscript interpretation:** Ring periodic BC is more sensitive to finite-lattice artifacts.
- **Alternative interpretation:** Could ring be detecting fermion-doubling modes that wilson_ring suppresses too aggressively?
- **Review question:** Should there be a separate diagnostic for fermion-doubling artifacts (e.g., counting spurious low-energy modes)?

**Q1.3:** Is the wilson_ring implementation validated elsewhere, or is this the first numerical test?
- **Review focus:** Literature precedent for Wilson term on S¹ product manifolds. Is this standard or novel?

---

### B. Twisted Boundary Conditions

**Q2.1:** Are three twist angles (alpha=0, 0.25, 0.5) sufficient to test BC sensitivity?
- **Context:** alpha=0 (periodic) shows 51 failures; alpha=0.25, 0.5 (twisted) show 0 failures.
- **Manuscript interpretation:** Periodic BC is special case with stronger finite-lattice artifacts.
- **Review question:** Should alpha be swept continuously (e.g., alpha ∈ [0, 1] with 20 samples) to map failure boundary?

**Q2.2:** Is ring/alpha=0 failure mode physically interpretable in lattice field theory?
- **Context:** 51 failures at s1_size<64, converging to 0 at s1_size≥64.
- **Manuscript interpretation:** Small-lattice artifact (insufficient resolution for periodic BC).
- **Alternative interpretation:** Could this indicate a fundamental issue with periodic BC on coarse grids?
- **Review question:** Is there lattice field theory literature on periodic BC failure modes at finite lattice spacing?

**Q2.3:** Should antiperiodic BC (alpha=0.5 exactly) be explicitly tested and labeled?
- **Context:** alpha=0.5 is labeled "twisted BC" but is specifically antiperiodic (fermion sign flip).
- **Review focus:** Antiperiodic BC has special significance in lattice field theory (thermal QCD, finite-temperature). Should it be highlighted?

---

### C. Discretization Family Comparison

**Q3.1:** Are spectral_circle, ring, wilson_ring representative of standard lattice methods?
- **Context:** spectral_circle = Fourier modes (exact for circle), ring = finite differences, wilson_ring = finite differences + Wilson term.
- **Review question:** Should other discretization families be included (staggered fermions, domain-wall fermions, overlap operator)?

**Q3.2:** Is the Kronecker-sum construction (D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1) standard for product manifolds?
- **Context:** Product-discretization treats S² and S¹ separately, then combines via Kronecker sum.
- **Review focus:** Is this standard in lattice field theory, or is it a simplification that could miss coupling effects?

**Q3.3:** Should there be cross-checks against analytical results for S²×S¹ Dirac spectrum?
- **Context:** S²×S¹ Dirac operator has known analytical spectrum for certain q, alpha configurations.
- **Review question:** Are there known exact results that should be reproduced as a validation benchmark?

---

### D. Convergence and Continuum Limit

**Q4.1:** Does "convergence at s1_size≥64" mean continuum limit, or just finite-lattice stability?
- **Manuscript claim:** "Convergence on finite lattices — NOT continuum extrapolation."
- **Review question:** Is this distinction clear enough? Should there be explicit statement: "s1_size=96 is still finite, NOT s1_size→∞"?

**Q4.2:** Should there be a continuum extrapolation (1/s1_size → 0) to establish true continuum limit?
- **Context:** Manuscript stops at s1_size=96 (largest tested) without extrapolation.
- **Review focus:** Is omitting continuum extrapolation a limitation, or is it acceptable for a methodology paper?

**Q4.3:** Is Decision Rule 1 (failure_rate < 2% → SMALL_LATTICE_ARTIFACT) too lenient?
- **Context:** 0/252 failures at s1_size≥64 easily passes 2% threshold.
- **Review question:** Should threshold be stricter (e.g., 0.5%), or is 2% industry-standard for lattice field theory?

---

## Track 2: Differential Geometry Reviewer Questions

### A. Dirac Operator Construction on S²

**Q5.1:** Are monopole harmonics correctly used for S² spherical components?
- **Context:** S² Dirac operator uses monopole harmonics with charge q.
- **Review focus:** Is the monopole harmonic basis standard, and are boundary conditions at poles handled correctly?

**Q5.2:** Is the monopole charge q parameterization standard?
- **Context:** q ∈ {0, 1, 2, 3, 4, 6, 26} tested.
- **Review question:** Why these specific values? Should q be swept continuously, or is discrete sampling sufficient?

**Q5.3:** Should there be additional checks for Dirac operator self-adjointness beyond Hermiticity gate?
- **Context:** Hermiticity gate checks H† = H (tolerance 1e-9).
- **Review question:** Is Hermiticity sufficient, or should there be checks for:
  - Domain of definition (Sobolev space H¹)
  - Essential self-adjointness (deficiency indices)
  - Spectral properties (real eigenvalues, orthogonal eigenvectors)

---

### B. Product-Discretization Methodology

**Q6.1:** Is the Kronecker-sum D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1 mathematically sound?
- **Context:** Product-discretization separates S² and S¹ operators, combines via Kronecker sum.
- **Review focus:** Does this preserve:
  - Self-adjointness of Dirac operator?
  - Clifford algebra relations?
  - Topological invariants (index)?

**Q6.2:** Does product-discretization miss coupling effects between S² and S¹?
- **Context:** Kronecker sum treats S² and S¹ independently.
- **Review question:** Are there known pathologies in product-discretized operators (e.g., spurious zero modes, index defects)?

**Q6.3:** Should there be validation against continuum Atiyah-Singer index theorem?
- **Context:** Dirac indices are computed numerically (kernel dimension).
- **Review question:** For known (q, alpha) configurations with analytical index, does discretized operator reproduce exact value?

---

### C. Geometry Generalization

**Q7.1:** Is the statement "S²×S¹ success does NOT imply S³×S⁶ success" conservative enough?
- **Context:** Manuscript warns against automatic transfer to higher dimensions.
- **Review question:** Should there be specific warnings about:
  - Dimensional scaling (S⁶ has ~10⁶ grid points)
  - Topological complexity (Calabi-Yau vs product manifolds)
  - Discretization family dependence (what works on S¹ may fail on S⁶)

**Q7.2:** Should there be explicit discussion of why S²×S¹ is NOT a Calabi-Yau?
- **Context:** S²×S¹ is chosen as diagnostic test geometry, NOT physical compactification target.
- **Review focus:** Is it clear that:
  - S²×S¹ has wrong dimension (3D, not 6D)
  - S²×S¹ is NOT Ricci-flat (not Calabi-Yau)
  - S²×S¹ is NOT a candidate for physical extra dimensions

**Q7.3:** Are there specific higher-dimensional manifolds where product-discretization is expected to fail?
- **Review question:** Should manuscript include "known failure modes" section for product-discretization (e.g., non-product manifolds, nontrivial fiber bundles)?

---

### D. Toy Geometry vs Physical Compactification

**Q8.1:** Is the distinction between "diagnostic test geometry" and "physical compactification target" clear?
- **Review question:** Should there be a table comparing:
  - Test geometry (S²×S¹): low-dimensional, product structure, chosen for tractability
  - Physical target (S³×S⁶, Calabi-Yau): high-dimensional, nontrivial topology, Ricci-flat

**Q8.2:** Should there be explicit statement: "S²×S¹ is NOT a candidate for Kaluza-Klein compactification"?
- **Context:** Manuscript states "toy diagnostics, NOT physical extra dimensions" (Table 3, non-claim 6).
- **Review focus:** Is this strong enough, or should Kaluza-Klein be explicitly ruled out?

**Q8.3:** Are the 8 scientific non-claims sufficient from a differential geometry perspective?
- **Review question:** Should additional non-claims be added:
  - No holonomy group calculation (Calabi-Yau SU(3))
  - No Kähler moduli analysis
  - No G₂ manifolds tested (M-theory compactification)

---

## Track 3: Numerical Analysis Reviewer Questions

### A. Finite-Size Scaling Methodology

**Q9.1:** Is Decision Rule 1 (failure_rate < 2% at s1_size≥64 → SMALL_LATTICE_ARTIFACT) sound?
- **Context:** 0/252 failures at s1_size≥64 vs 51/630 failures at s1_size<64.
- **Review questions:**
  - Is 2% threshold justified, or arbitrary?
  - Should threshold be stricter (e.g., 0.5% for high-confidence convergence)?
  - Is single threshold appropriate across all parameter regimes?

**Q9.2:** Should there be additional convergence checks (e.g., Richardson extrapolation)?
- **Context:** Manuscript shows failure rate drops to 0% at s1_size≥64, declares convergence.
- **Review question:** Should there be quantitative convergence tests:
  - Eigenvalue convergence (max |λ(s1_size=96) - λ(s1_size=64)| / λ)
  - Localization metric convergence
  - Index convergence (kernel dimension)

**Q9.3:** Is the distinction between "discretized operator convergence" and "continuum limit" clear?
- **Manuscript claim:** "Failures vanish at s1_size≥64 — finite-lattice convergence, NOT continuum extrapolation."
- **Review focus:** Is this phrasing unambiguous? Should there be explicit:
  - "s1_size=96 is still finite"
  - "No 1/s1_size → 0 extrapolation performed"
  - "Continuum limit requires separate study (out of scope)"

---

### B. Convergence Evidence Sufficiency

**Q10.1:** Is 0/252 failures at s1_size≥64 sufficient evidence for convergence?
- **Context:** Two lattice sizes tested above threshold (s1_size=64, 96).
- **Review questions:**
  - Should s1_size=128, 192 be tested for convergence confirmation?
  - Is two-point convergence (s1_size=64, 96) sufficient, or should there be three+ points?
  - Should there be error bars / confidence intervals on failure rate?

**Q10.2:** Should there be explicit convergence rate analysis (e.g., O(1/s1_size²))?
- **Context:** Manuscript shows failures drop from 8.1% (<64) to 0.0% (≥64), but no rate analysis.
- **Review question:** Should there be power-law fit to quantify convergence rate?

**Q10.3:** Are there edge cases where s1_size=64 might be insufficient?
- **Review question:** Should manuscript include sensitivity analysis:
  - Larger disorder (W=16, 32) at s1_size=64
  - Smaller twist angles (alpha=0.05, 0.1 near periodic)
  - Larger monopole charges (q=50, 100)

---

### C. Reproducibility and Numerical Stability

**Q11.1:** Is bit-identical reproducibility (6615/6615 matched) the right test?
- **Context:** Reproducibility run matched all 6615 cases bit-identically (SHA256 checksums).
- **Review questions:**
  - Is bit-identical too strict (could mask valid rounding differences)?
  - Should there be tolerance-based reproducibility (e.g., max relative error < 1e-12)?
  - Does bit-identical reproducibility guarantee numerical stability, or just determinism?

**Q11.2:** Should there be numerical stability checks beyond reproducibility?
- **Review question:** Should manuscript include:
  - Condition number analysis (operator matrix condition number)
  - Eigenvalue sensitivity (perturbation bounds)
  - Floating-point precision impact (float64 vs float128)

**Q11.3:** Are there scenarios where reproducibility could be misleading?
- **Context:** Reproducible wrong operator is still wrong.
- **Review question:** Should there be independent cross-checks:
  - Different eigenvalue solvers (scipy vs LAPACK vs iterative methods)
  - Different programming languages (Python vs C++ vs Julia)
  - Different numerical libraries (NumPy vs JAX vs PyTorch)

---

### D. Decision Rule Justification

**Q12.1:** Is 2% threshold in Decision Rule 1 justified by literature, or ad-hoc?
- **Review question:** Should manuscript cite precedent for 2% threshold, or justify via:
  - Statistical significance (binomial test)
  - Industry standard (lattice QCD convergence criteria)
  - Cost-benefit analysis (2% acceptable given compute cost)

**Q12.2:** Should there be multiple decision rules for different artifact types?
- **Context:** Decision Rule 1 classifies SMALL_LATTICE_ARTIFACT.
- **Review question:** Should there be separate rules for:
  - DISCRETIZATION_PATHOLOGY (failures persist at all s1_size)
  - BOUNDARY_ARTIFACT (failures depend on BC only)
  - DISORDER_THRESHOLD (failures depend on W range)

**Q12.3:** How would Decision Rule 1 handle marginal cases (failure_rate = 1.8%, just below 2%)?
- **Review question:** Should there be confidence intervals or Bayesian updating for near-threshold cases?

---

## Cross-Cutting Questions (All Reviewers)

### E. Workflow Reusability

**Q13.1:** Could another group replicate this workflow on a different toy geometry (e.g., S³×S²)?
- **Review focus:** Are implementation details sufficient for independent replication?

**Q13.2:** Are there missing steps in the Falsification Ladder that should be added?
- **Context:** 9 rungs: Operator Construction → Hermiticity/Shape Gates → Controls → Progressive Profiles → Full Diagnostic → Audit → Targeted Follow-Up → Release Integrity → Baseline Promotion.
- **Review question:** Should there be additional rungs:
  - Analytical validation (compare to known exact results)
  - Cross-method validation (compare to different numerical methods)
  - Sensitivity analysis (parameter perturbations)

**Q13.3:** Is the independent audit protocol (8-aspect framework) reproducible by external groups?
- **Review question:** Could a third-party auditor apply the same 8 aspects without access to project context?

---

### F. Scope Protection

**Q14.1:** Are the 8 scientific non-claims sufficient to prevent misinterpretation?
- **Review question:** Should additional non-claims be added:
  - No loop quantum gravity application
  - No string theory connection
  - No AdS/CFT correspondence

**Q14.2:** Is the phrase "methodological contribution, NOT physical compactification proof" repeated enough?
- **Review focus:** Does manuscript risk being misinterpreted as physical theory paper despite non-claims?

**Q14.3:** Should there be a separate "Common Misinterpretations" appendix?
- **Review question:** Should manuscript preemptively address:
  - "Does this prove extra dimensions?" → NO (Table 3, non-claim 6)
  - "Does this derive Standard Model?" → NO (Table 3, non-claim 3)
  - "Does this bypass Witten's theorem?" → NO (Table 3, non-claim 5)

---

## Summary: Key Review Questions by Domain

**Lattice Field Theory:**
1. Is Wilson term correctly implemented?
2. Should fermion-doubling diagnostics be added?
3. Is continuum extrapolation omission acceptable?

**Differential Geometry:**
1. Is product-discretization mathematically sound?
2. Is S²×S¹ vs Calabi-Yau distinction clear?
3. Should Atiyah-Singer index validation be added?

**Numerical Analysis:**
1. Is Decision Rule 1 (2% threshold) justified?
2. Is 0/252 failures sufficient convergence evidence?
3. Should s1_size=128, 192 be tested?

**All Reviewers:**
1. Is workflow reusable on different geometries?
2. Are 8 scientific non-claims sufficient?
3. Is scope protection strong enough?

---

**These questions guide domain expert review** — reviewers should feel free to add additional questions or challenge framing.
