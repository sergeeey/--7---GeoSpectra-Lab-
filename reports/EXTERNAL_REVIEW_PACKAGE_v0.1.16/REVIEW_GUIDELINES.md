# Review Guidelines — v0.1.16 Methodology Manuscript

**Paper Title:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"

**Manuscript:** `../METHODOLOGY_PAPER_COMPRESSED_v0.1.16.md` (8,950 words)

**Review request date:** 2026-05-17  
**Expected review duration:** 4-6 weeks

---

## Your Role as Reviewer

You are being asked to provide **technical domain expert review** of a **methodology paper** describing a falsification-first validation workflow for discretized spectral operators on toy manifolds.

**This is NOT a physical compactification paper.**  
**This is a methodology/computational methods paper.**

Your expertise is requested to evaluate:
1. Whether the methodology (Falsification Ladder workflow) is sound and reproducible
2. Whether the controls, gates, and progressive profiles are correctly designed
3. Whether the artifact handling (ring/alpha=0 caveat) is convincing
4. Whether the scope boundaries (scientific non-claims) are sufficient to prevent misinterpretation

**You are NOT being asked to:**
- Evaluate physical relevance of S²×S¹ compactification
- Assess whether this connects to Standard Model physics
- Judge continuum extrapolation validity (none performed)
- Validate S⁶ or Calabi-Yau applications (not tested)

---

## What This Paper Claims

### Methodological Contribution (What IS Claimed)

✅ **GeoSpectra Falsification Ladder is a reusable validation workflow** for computational toy-model investigations  
✅ **Controls + progressive profiles catch failures early** (smoke 5 min → full 16 hours)  
✅ **Independent audit prevents interpretation drift** (2 discrepancies corrected in v0.1.15)  
✅ **Targeted follow-ups resolve caveats efficiently** (1349 cases, 2.5 hours vs 16-hour full re-run)  
✅ **Ring/alpha=0 caveat converted to production guideline** (s1_size≥64 threshold empirically derived)  
✅ **Workflow validated in tested scope** (S²×S¹ finite lattices, three S¹ discretization families)

### Scope Boundaries (What IS NOT Claimed)

❌ **No continuum compactification** (all operators discretized on finite lattices, s1_size≤96)  
❌ **No S⁶ or S³×S⁶ validation** (only S², S³, S¹, S²×S¹ tested)  
❌ **No Standard Model derivation** (no gauge group, no fermion generations)  
❌ **No physical chirality proof** (Dirac indices are topological toy counts)  
❌ **No Witten/Lichnerowicz bypass** (numerical index ≠ rigorous Atiyah-Singer theorem)  
❌ **No physical extra dimensions** (Anderson benchmark is numerical test, not physical mechanism)  
❌ **No hierarchy problem solution** (toy radion model, if used, does not address moduli stabilization)  
❌ **No observable predictions** (topological invariants are discretized toy analogs)

---

## Review Focus Areas by Domain Expertise

### Lattice Field Theory Reviewer

**Focus on:**

1. **Wilson term implementation** (wilson_ring family)
   - Is the Wilson term correctly constructed for S¹ discretization?
   - Does it suppress fermion doubling as expected?
   - Should there be additional diagnostics for fermion-doubling artifacts?

2. **Twisted boundary conditions** (alpha=0, 0.25, 0.5)
   - Are the three twist angles sufficient to test BC sensitivity?
   - Is the ring/alpha=0 (periodic BC) failure mode physically interpretable?
   - Should alpha be swept continuously instead of 3 discrete values?

3. **Discretization family comparison**
   - Are spectral_circle, ring, wilson_ring representative of standard lattice methods?
   - Is the Kronecker-sum construction (D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1) standard for product manifolds?
   - Should staggered fermions or domain-wall fermions be included for comparison?

**Key question:** Does the paper correctly interpret ring/alpha=0 convergence at s1_size≥64 as a **small-lattice artifact** rather than a fundamental discretization failure?

---

### Differential Geometry Reviewer

**Focus on:**

1. **Dirac operator construction on S²**
   - Are monopole harmonics correctly used for S² spherical components?
   - Is the monopole charge q parameterization standard?
   - Should there be additional checks for Dirac operator self-adjointness beyond Hermiticity gate?

2. **Product-discretization methodology**
   - Is the Kronecker-sum D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1 mathematically sound?
   - Does this construction preserve key properties of continuum Dirac operators?
   - Are there known pathologies in product-discretized operators that should be tested?

3. **Geometry generalization claims**
   - The paper states "S²×S¹ success does NOT imply S³×S⁶ success" — is this conservative enough?
   - Are there specific warnings needed for higher-dimensional product manifolds?
   - Should there be explicit discussion of why S²×S¹ is NOT a Calabi-Yau?

**Key question:** Does the paper correctly frame S²×S¹ as a **diagnostic test geometry** rather than a physical compactification target?

---

### Numerical Analysis Reviewer

**Focus on:**

1. **Finite-size scaling methodology**
   - Is Decision Rule 1 (failure_rate<2% at s1_size≥64 → SMALL_LATTICE_ARTIFACT) sound?
   - Should there be additional convergence checks (e.g., Richardson extrapolation)?
   - Is the 2% threshold justified or arbitrary?

2. **Convergence interpretation**
   - The paper shows 0/252 failures at s1_size≥64 (Figure 7) — is this sufficient evidence for convergence?
   - Should there be larger lattice sizes tested (s1_size=128, 192)?
   - Is "convergence on finite lattices" vs "continuum limit" distinction clear enough?

3. **Reproducibility protocol**
   - 6615/6615 bit-identical reproducibility — is this the right test?
   - Should there be numerical stability checks (e.g., condition number, eigenvalue sensitivity)?
   - Are there edge cases where bit-identical reproducibility could be misleading?

**Key question:** Does the paper correctly distinguish **discretized operator convergence** (failures vanish at larger lattices) from **continuum extrapolation** (s1_size→∞)?

---

## What to Evaluate (Checklist)

### Methodology Soundness

- [ ] Are the 9 Falsification Ladder rungs logically ordered?
- [ ] Are controls (positive/negative) correctly designed?
- [ ] Do progressive profiles (smoke/standard/full/targeted) make sense as a detection strategy?
- [ ] Is independent audit protocol reproducible by other groups?
- [ ] Is caveat handling (ring/alpha=0 → targeted follow-up → production guideline) convincing?

### Technical Correctness

- [ ] Are operator constructions mathematically sound? (geometry reviewer)
- [ ] Are discretization methods standard? (lattice field theory reviewer)
- [ ] Are convergence criteria appropriate? (numerical analysis reviewer)
- [ ] Are there missing diagnostics or gates that should be included?
- [ ] Are failure mode classifications (SMALL_LATTICE_ARTIFACT, SYSTEMATIC_PATHOLOGY) reasonable?

### Scope Protection

- [ ] Are the 8 scientific non-claims (Table 3) sufficient to prevent misinterpretation?
- [ ] Is the distinction between "toy diagnostics" and "physical compactification" clear?
- [ ] Are limitations (Section 5.3) comprehensive?
- [ ] Is the phrase "methodological contribution, NOT physical one" repeated enough?

### Reproducibility

- [ ] Could another group replicate this workflow on a different toy geometry?
- [ ] Are artifacts (config.json, metrics.json, summary.md) well-specified?
- [ ] Is the baseline (v0.1.15) sufficiently documented for external reproduction?
- [ ] Are there missing implementation details that would block replication?

### Writing Quality

- [ ] Is the abstract clear and accurate? (221 words, evidence details included)
- [ ] Are tables and figures correctly numbered and referenced? (Table 1-8, Figure 7)
- [ ] Is Figure 7 caption accurate? (finite-lattice convergence, NOT continuum)
- [ ] Are there sections that are too compressed and need expansion?

---

## What NOT to Evaluate

**Do NOT spend time evaluating:**

❌ Physical relevance of S²×S¹ for real-world compactification  
❌ Whether this connects to LHC observables  
❌ Whether Dirac indices from toy operators relate to SM fermion generations  
❌ Whether this bypasses Witten or Lichnerowicz no-go theorems  
❌ Whether Anderson localization is the right physical mechanism for dimensional reduction  
❌ Continuum limit validity (none performed — out of scope)  
❌ S⁶ or Calabi-Yau applicability (not tested — out of scope)

**If you find yourself asking "but does this prove physical compactification?" → STOP.**

The answer is explicitly NO (see Table 3 — 8 scientific non-claims). This paper validates a **methodology**, not a **physical mechanism**.

---

## Review Output Format

**Please provide:**

1. **Overall verdict** (choose one):
   - **Accept as-is** — ready for preprint submission
   - **Minor revisions** — small fixes, no re-review needed
   - **Major revisions** — substantial changes required, re-review needed
   - **Reject** — fundamental flaws, not fixable within scope

2. **Strengths** (3-5 bullet points):
   - What does this paper do well?
   - What methodological contributions are valuable?

3. **Weaknesses** (3-5 bullet points):
   - What technical issues need addressing?
   - What claims are overstated or under-supported?

4. **Specific comments** (line-by-line or section-by-section):
   - Technical errors or ambiguities
   - Missing citations or references
   - Suggestions for clarity improvements

5. **Scope protection assessment**:
   - Are the 8 scientific non-claims sufficient?
   - Should additional non-claims be added?
   - Is there risk of misinterpretation as a physical compactification proof?

6. **Replication feasibility**:
   - Could you replicate this workflow on a different toy geometry?
   - Are there missing details that would block replication?

---

## Timeline

**Review period:** 4-6 weeks from receipt  
**Interim questions:** Open GitHub issue or email sergeikuch80@gmail.com  
**Final report:** Submit via email or GitHub issue

**After your review:**
- Authors will respond to feedback within 2 weeks
- Revisions will be completed within 2-4 weeks
- If major revisions requested, we will send updated manuscript for re-review

---

## Thank You

Your domain expertise is critical to ensuring this methodology paper meets the standards of lattice field theory / differential geometry / numerical analysis communities.

**Key reminder:** This is a **methodology paper** (falsification-first workflow for toy diagnostics), NOT a **physical compactification proof**. Your review focus should be on workflow soundness, technical correctness, and scope protection — NOT on physical relevance to Standard Model or observable predictions.

**Questions during review?** Open GitHub issue or email sergeikuch80@gmail.com
