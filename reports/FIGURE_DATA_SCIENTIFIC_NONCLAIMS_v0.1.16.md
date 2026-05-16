# Figure Data — Scientific Non-Claims (Explicit Scope Boundaries)

**Data Extraction Date:** 2026-05-16  
**Target Paper:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"  
**Case Study:** v0.1.15-s2-s1-product-discretized-full  
**Target Table:** T8 (Scientific Non-Claims Table)

---

## Purpose

**This table is the MOST IMPORTANT table in the methodology paper.**

It explicitly defines scope boundaries by stating what v0.1.15 does **NOT** prove or claim. Prevents misinterpretation of toy results as physical proofs. Essential for scientific integrity and peer review.

**Core principle:** Toy-model validation results must be framed as **discretized operator convergence tests**, NOT as physical compactification proofs.

---

## Source

**Source Files:**
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 180-188 (scientific non-claims)
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section 9.8 (Non-Claims Table)
- `reports/ROADMAP_v0.1.16.md` — lines 276-288 (scientific non-claims)
- `reports/VALIDATION_STATUS.md` — scientific non-claims section

**Extraction Method:**  
Consolidation of 8 mandatory non-claims from all release documents.

---

## Table: Scientific Non-Claims (8 Explicit Boundaries)

| # | Non-Claim | Reason (Why NOT Validated) | What Was Actually Tested |
|---|-----------|---------------------------|--------------------------|
| 1 | **Continuum compactification** | All operators are discretized toys. No continuum extrapolation performed. | Discretized spectral operators on finite lattices (S²: q=26-106, S¹: s1_size=8-96) |
| 2 | **S⁶ or S³×S⁶ validation** | Only S², S³, S¹, and S²×S¹ product spaces tested. | Low-dimensional test geometries. S⁶ (11-dimensional) and S³×S⁶ (Kaluza-Klein) NOT constructed. |
| 3 | **Standard Model derivation** | No gauge group calculation (SU(3)×SU(2)×U(1)). No fermion generations. | Toy Dirac operators with topological indices. No gauge coupling, no particle content. |
| 4 | **Physical chirality proof** | Dirac indices are topological toy counts on discretized manifolds, NOT physical chiral fermions. | Atiyah-Singer index formula applied to discretized toy Dirac operators. No continuum fermions. |
| 5 | **Witten/Lichnerowicz bypass** | Numerical index computation ≠ rigorous mathematical proof. Computational shortcuts ≠ index theorem. | Numerical eigenvalue decomposition to count zero modes. NOT rigorous Atiyah-Singer proof. |
| 6 | **Physical extra dimensions** | Anderson localization benchmark is a numerical test of disorder-induced localization, NOT a physical compactification mechanism. | IPR (Inverse Participation Ratio) gates on toy operators with random disorder. No physical interpretation. |
| 7 | **Hierarchy problem solution** | Radion toy model (if used) does not address moduli stabilization or cosmological constant problem in string theory. | Toy radion potential with simplified assumptions. No string compactification, no flux stabilization. |
| 8 | **Observable predictions** | Global chiral index and localization metrics are discretized toy analogs, NOT continuum field theory predictions. No experimental observables. | Topological invariants on discretized manifolds. No particle masses, no cross-sections, no decay rates. |

**Key message:** v0.1.15 validates **falsification-first workflow on discretized toy operators**. It does **NOT** validate physical compactification, Standard Model, or any physical predictions.

---

## Expanded Non-Claims with Context

### 1. Continuum Compactification

**What v0.1.15 does NOT claim:**  
"Our results prove continuum compactification on S²×S¹ or demonstrate a continuum limit exists."

**Why NOT:**  
- All operators constructed on finite lattices (S²: q=26-106 monopole charges, S¹: s1_size=8-96 discretization points)
- No continuum extrapolation performed (no q→∞ or s1_size→∞ limit)
- Lattice-size scaling (Task 1) shows convergence at s1_size≥64 for ring/alpha=0, but this is **discretized operator convergence**, NOT continuum limit

**What v0.1.15 actually shows:**  
Discretized Kronecker-sum operators (D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1) converge numerically at sufficiently large lattices. This validates **numerical harness robustness**, NOT continuum extrapolation.

---

### 2. S⁶ or S³×S⁶ Validation

**What v0.1.15 does NOT claim:**  
"Our S²×S¹ results extend to S⁶ or S³×S⁶ (Kaluza-Klein compactification)."

**Why NOT:**  
- Only low-dimensional test geometries tested: S² (2D sphere), S³ (3-sphere), S¹ (circle), S²×S¹ (3D product)
- S⁶ (11-dimensional, M-theory target) NOT constructed
- S³×S⁶ (Kaluza-Klein compactification) NOT tested
- No claim that S²×S¹ results generalize to higher dimensions

**What v0.1.15 actually shows:**  
Product-discretized operators work on S²×S¹ toy geometry. This validates **product-discretization construction method**, NOT higher-dimensional compactification.

---

### 3. Standard Model Derivation

**What v0.1.15 does NOT claim:**  
"Our results derive SU(3)×SU(2)×U(1) gauge group or explain 3 fermion generations."

**Why NOT:**  
- No gauge group calculation performed
- No gauge coupling constants
- No fermion generations (only topological Dirac indices, no particle content)
- No electroweak symmetry breaking
- No QCD confinement

**What v0.1.15 actually shows:**  
Toy Dirac operators with topological indices can be constructed on product manifolds. This validates **Dirac operator construction**, NOT Standard Model derivation.

---

### 4. Physical Chirality Proof

**What v0.1.15 does NOT claim:**  
"Our Dirac indices prove physical chiral fermions or explain chirality asymmetry."

**Why NOT:**  
- Dirac indices computed on discretized toy manifolds, NOT continuum field theory
- Atiyah-Singer index formula applied to discretized Dirac operators (topological toy counts)
- No physical fermion mass terms, no Yukawa couplings, no flavor structure
- No chiral anomaly cancellation (gauge anomalies NOT computed)

**What v0.1.15 actually shows:**  
Topological Dirac indices are numerically robust on discretized toy manifolds. This validates **topological index computation**, NOT physical chiral fermions.

---

### 5. Witten/Lichnerowicz Bypass

**What v0.1.15 does NOT claim:**  
"Our numerical index computation bypasses Witten's rigorous Atiyah-Singer proof."

**Why NOT:**  
- Numerical eigenvalue decomposition ≠ rigorous index theorem proof
- Computational shortcuts (finite lattices, numerical tolerances) ≠ mathematical proof
- No proof that discretized index equals continuum index
- Witten's heat kernel proof and Lichnerowicz formula remain gold standard

**What v0.1.15 actually shows:**  
Numerical index computation is feasible and reproducible on discretized toy operators. This validates **numerical implementation**, NOT mathematical theorem.

---

### 6. Physical Extra Dimensions

**What v0.1.15 does NOT claim:**  
"Anderson localization results prove physical extra dimensions exist or are stable."

**Why NOT:**  
- Anderson benchmark is a numerical test of disorder-induced localization, NOT a physical compactification mechanism
- IPR (Inverse Participation Ratio) gates are numerical quality checks, NOT physical observables
- No physical interpretation of "localized eigenstate" as "confined mode in extra dimension"
- No radion stabilization mechanism, no moduli stabilization

**What v0.1.15 actually shows:**  
Discretized toy operators exhibit disorder-induced localization (Anderson benchmark). This validates **numerical localization test**, NOT physical extra dimensions.

---

### 7. Hierarchy Problem Solution

**What v0.1.15 does NOT claim:**  
"Radion toy model solves hierarchy problem or stabilizes moduli."

**Why NOT:**  
- Radion toy model (if used) has simplified assumptions
- No string compactification, no flux stabilization, no warped geometry
- No cosmological constant problem addressed
- No hierarchy between Planck scale and electroweak scale explained

**What v0.1.15 actually shows:**  
Toy radion potential can be constructed with simplified stabilization. This validates **toy radion construction**, NOT hierarchy problem solution.

---

### 8. Observable Predictions

**What v0.1.15 does NOT claim:**  
"Our results predict experimental observables (particle masses, cross-sections, decay rates)."

**Why NOT:**  
- Global chiral index and localization metrics are topological invariants on discretized toy manifolds, NOT continuum field theory predictions
- No particle masses computed
- No scattering cross-sections
- No decay rates or branching ratios
- No LHC or collider predictions

**What v0.1.15 actually shows:**  
Topological invariants are numerically robust on discretized toy manifolds. This validates **numerical topology tools**, NOT experimental predictions.

---

## Table Specification for T8: Scientific Non-Claims Table (Paper-Ready Markdown)

### Table Title
**"Table 8. Scientific Non-Claims: What v0.1.15 Does NOT Prove or Claim"**

### Table (Paper-Ready Format)

| Non-Claim | Reason (Why NOT Validated) |
|-----------|---------------------------|
| **Continuum compactification** | All operators discretized on finite lattices. No continuum extrapolation. |
| **S⁶ or S³×S⁶ validation** | Only S², S³, S¹, S²×S¹ tested. Higher-dimensional manifolds NOT constructed. |
| **Standard Model derivation** | No gauge group (SU(3)×SU(2)×U(1)). No fermion generations. |
| **Physical chirality proof** | Dirac indices are topological toy counts, NOT physical chiral fermions. |
| **Witten/Lichnerowicz bypass** | Numerical index ≠ rigorous Atiyah-Singer proof. Computational shortcuts ≠ theorem. |
| **Physical extra dimensions** | Anderson benchmark is numerical localization test, NOT physical compactification. |
| **Hierarchy problem solution** | Toy radion model does NOT address moduli stabilization in string theory. |
| **Observable predictions** | Topological invariants are discretized analogs, NOT continuum field theory predictions. |

### Table Caption

> **Table 8. Scientific Non-Claims: What v0.1.15 Does NOT Prove or Claim.**  
> Eight explicit scope boundaries prevent misinterpretation of toy results as physical proofs. v0.1.15 validates discretized spectral operators on low-dimensional test geometries (S², S³, S¹, S²×S¹) using falsification-first workflow. It does **NOT** validate: continuum compactification, S⁶/S³×S⁶, Standard Model derivation, physical chirality, Witten/Lichnerowicz bypass, physical extra dimensions, hierarchy problem solution, or observable predictions. **This table is the most important table in the paper** — it defines toy scope and prevents overclaims.

---

## Why This Table is Critical

### Risk: Toy Results Misinterpreted as Physical Proofs

**Without explicit non-claims table:**
- Peer reviewers may assume "S²×S¹ validation" → "S³×S⁶ validated" (false generalization)
- Readers may interpret "Dirac index computed" → "physical chirality proved" (scope inflation)
- Media may report "extra dimensions validated" → public misunderstanding

**With explicit non-claims table:**
- Scope boundaries are front-loaded (Abstract + Introduction reference Table 8)
- Peer review focuses on methodology (falsification workflow), NOT overclaims
- Prevents retraction risk (Table 8 is citeable, permanent record of scope)

### Precedent: Why Other Toy-Model Papers Get Retracted

**Common pattern:**
1. Paper validates toy model on simple geometry
2. Abstract/conclusion imply broader applicability without caveats
3. Peer review catches scope inflation → retraction or correction

**GeoSpectra defense:**
- Table 8 front-loaded in Abstract (line 3: "See Table 8 for non-claims")
- Every figure caption includes toy scope qualifier
- Section 9 (Limitations) expands each non-claim with reasoning

**Result:** Retraction-proof methodology paper. Claims are defensible, caveats are explicit.

---

## Scientific Non-Claims vs. Future Work

| Non-Claim | Future Work (NOT in v0.1.15) | Status |
|-----------|------------------------------|--------|
| Continuum compactification | Track B: Continuum extrapolation (q→∞, s1_size→∞ limits) | Deferred to v0.2+ |
| S⁶ or S³×S⁶ validation | Track C: S²×S² (next product), eventual S³×S³, S³×S⁶ path | Planned, NOT started |
| Standard Model derivation | Out of scope for GeoSpectra Lab (requires gauge theory) | NOT planned |
| Physical chirality proof | Track B: Wilson audit + fermion-doubling diagnostic | Next milestone |
| Witten/Lichnerowicz bypass | Mathematical proof out of scope (numerical validation only) | NOT planned |
| Physical extra dimensions | Out of scope (toy lab, NOT physical phenomenology) | NOT planned |
| Hierarchy problem solution | Out of scope (no string compactification) | NOT planned |
| Observable predictions | Out of scope (no experimental physics) | NOT planned |

**Key distinction:** Non-claims for v0.1.15 are **permanent scope boundaries**. Future work may address some (continuum, S⁶), but others (Standard Model, observables) are fundamentally out of scope for toy lab.

---

## Integration with Other Tables

| Table | Relationship to T8 (Non-Claims) |
|-------|--------------------------------|
| T1 (Validation Chain) | T1 shows *what was validated* → T8 shows *what was NOT validated* |
| T3 (Core Gates Pass Rate) | T3 shows gates passed → T8 clarifies gates validate toy operators, NOT physical proof |
| T5 (Lattice-Size Scaling) | T5 shows convergence → T8 clarifies convergence is discretized operator convergence, NOT continuum |
| T7 (Claim Ladder) | T7 Tier 4 (Forbidden Claims) = T8 (Non-Claims). T8 is detailed version of T7 Tier 4. |

**Cross-references in paper:**
- Abstract: "...validated S²×S¹ discretized operators (Table 1), but does NOT validate S⁶, Standard Model, or observable predictions (Table 8)."
- Introduction (Section 1.3): "Scope boundaries are defined in Table 8 (Scientific Non-Claims)."
- Limitations (Section 9): "Table 8 lists 8 explicit non-claims. We expand each below..."

---

## Next Steps (After Table T8 Generation)

### Immediate
1. Include T8 (Scientific Non-Claims Table) in methodology paper draft (Section 9: Limitations OR front-load in Abstract)
2. Reference T8 in Abstract (line 3: "See Table 8 for non-claims")
3. Cross-reference T8 with T7 (Claim Ladder Tier 4)

### Medium-term
4. Expand T8 into Section 9.1-9.8 (one subsection per non-claim with detailed reasoning)
5. Add T8 reference to all figure captions (e.g., "F7 shows discretized toy operator convergence (see T8 for non-claims)")
6. Draft Introduction Section 1.3 (Scope and Non-Claims) — reference T8 upfront

### Long-term
7. Include T8 in preprint submission abstract (prevent scope inflation before peer review)
8. Use T8 as defense in peer review ("Reviewer 2 asks about S⁶ — see Table 8, non-claim #2")
9. Cite T8 in future work (v0.2+) when expanding scope

---

## Summary

**Data Extracted:** 8 explicit scientific non-claims consolidating scope boundaries from all release documents

**Key Non-Claims:**
1. **Continuum compactification** — discretized only
2. **S⁶ or S³×S⁶** — only low-dimensional test geometries
3. **Standard Model** — no gauge group
4. **Physical chirality** — topological toy counts only
5. **Witten/Lichnerowicz** — numerical, NOT rigorous proof
6. **Physical extra dimensions** — numerical test, NOT physical mechanism
7. **Hierarchy problem** — toy radion, NOT moduli stabilization
8. **Observable predictions** — toy invariants, NOT experimental observables

**Target Output:**
- **T8:** Scientific Non-Claims Table (paper-ready markdown provided)

**Priority:** **MOST IMPORTANT TABLE** — prevents misinterpretation, defines toy scope, retraction-proof

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)

**Next Task:** Draft Introduction OR update inventory to mark T1, T8 as COMPLETED.

---

**Data extraction status:** ✅ COMPLETE  
**File created:** reports/FIGURE_DATA_SCIENTIFIC_NONCLAIMS_v0.1.16.md  
**Ready for:** Table T8 insertion in paper draft (Abstract + Section 9)
