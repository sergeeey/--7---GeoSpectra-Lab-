# Methodology Paper Compression Plan — v0.1.16

**Date:** 2026-05-17  
**Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Current Draft:** reports/METHODOLOGY_PAPER_DRAFT_v0.1.16.md  
**Status:** Compression strategy for journal submission

---

## 1. Current State

### Manuscript Statistics

| Metric | Value |
|--------|-------|
| **Current word count** | 42,916 words |
| **Sections included** | 10 main sections + front matter + appendices |
| **Publication target** | 10,000-12,000 words (journal methodology paper) |
| **Required compression** | ~31,000 words (72% reduction) |

### Why Compression Is Needed

**Journal page limits:** Most computational physics / numerical methods journals enforce 20-30 page limits (8,000-12,000 words including figures/tables). Current draft at 42,916 words would exceed limits by 3.5×.

**Readability:** The current draft has substantial duplication:
- "Falsification-first" defined 8+ times
- v0.1.15 quantitative results (6615 cases, 51 failures, s1_size≥64) repeated 12+ times
- Scientific non-claims (8 items) repeated in Sections 1, 9, 10
- Audit methodology (8-aspect framework) described twice
- Ring/alpha=0 caveat narrative spans 5 sections

**External review feedback:** Domain experts will request tighter focus — methodology paper should emphasize **workflow**, not exhaustive case study details.

---

## 2. Target Structure

### Proposed Final Paper Structure (10,000-12,000 words)

| Section | Target Words | % of Total | Content Focus |
|---------|-------------|-----------|---------------|
| **Abstract** | 200-250 | 2% | Thesis + v0.1.15 case study + Table 9.1 non-claims reference |
| **1. Introduction** | 800-1000 | 8% | Challenge + thesis + contribution (no case study details) |
| **2. Motivation** | 800-1000 | 8% | Related work + gap (toy validation lacks falsification-first) |
| **3. Methods** | 1500-2000 | 16% | **Merged:** Falsification Ladder + Controls/Gates + Progressive Profiles |
| **4. Case Study** | 2000-2500 | 21% | **Merged:** S²×S¹ full diagnostic + ring/alpha=0 caveat discovery |
| **5. Audit and Limitations** | 1200-1500 | 12% | **Merged:** Independent audit + scientific non-claims (Table 9.1) |
| **6. Conclusion** | 700-1000 | 8% | Summary + 4 future work tracks (condensed) |
| **References** | — | — | Citations (not counted in word limit) |
| **Appendices** | (supplementary) | — | Operator construction, gate definitions, audit protocol, extended non-claims |
| **Total** | **10,000-12,000** | **100%** | |

### Key Structural Changes

1. **Merge Sections 3-4-5 → Section 3 (Methods):** Falsification Ladder, controls/gates, progressive profiles are all methodology — combine into single 1500-2000 word section.

2. **Merge Sections 6-7 → Section 4 (Case Study):** Full diagnostic and ring/alpha=0 caveat discovery are one narrative — condense into 2000-2500 words with quantitative results in tables.

3. **Merge Sections 8-9 → Section 5 (Audit and Limitations):** Audit findings and scientific non-claims are both scope discipline — combine into 1200-1500 words with Table 9.1 as centerpiece.

4. **Condense Section 10 → Section 6 (Conclusion):** Four future work tracks (A: Publication, B: Operator Credibility, C: Geometry Generalization, D: Anti-Artifact Robustness) reduce to 4 bullet lists, 700-1000 words total.

---

## 3. What to Keep in Main Text

### Critical Content (Cannot Be Cut)

**Core Thesis (Introduction):**
- Toy spectral operator validation requires falsification-first workflow
- Green unit tests are floor, not ceiling
- Provisional success is starting point for stress tests, not endpoint

**Falsification Ladder (Methods):**
- Four-tier structure: Controls → Baseline → Diagnostic → Cross-Family
- q=0 gate (negative control), W=0 gate (positive control)
- Progressive profiles (tiny → medium → full)
- Caveat discovery workflow (detection → investigation → classification → guideline)

**v0.1.15 Headline Results (Case Study):**
- 6615/6615 full diagnostic completed
- 51/6615 failures (0.8% total rate, 8.3% ring/alpha=0 subspace rate)
- Targeted follow-up: 1349 cases, 0/252 failures at s1_size≥64
- Verdict: SMALL_LATTICE_ARTIFACT
- Production guideline: s1_size≥64 for ring/alpha=0

**Ring/Alpha=0 Caveat Resolution (Case Study):**
- Subspace failure concentration detected (not hidden by aggregate rate)
- Targeted follow-up hypothesis: small-lattice artifact vs persistent limitation
- Evidence: failure rate 8.3% (s1_size<64) → 0.0% (s1_size≥64)
- Classification: empirical convergence threshold, not theorem

**Scientific Non-Claims (Table 9.1, Audit/Limitations):**
- All 8 non-claims preserved in table form
- Brief explanation: toy scope = finite lattices, NOT continuum
- No physical overclaims (continuum, S⁶, Standard Model, chirality, Witten, extra dimensions, hierarchy, observables)

**Production Guideline (Case Study):**
- Ring/alpha=0: s1_size ≥ 64
- Spectral_circle, wilson_ring: robust at all tested sizes
- Empirical threshold, not mathematical proof

**Audit Lesson (Audit/Limitations):**
- Independent within-project artifact audit caught interpretation drift
- 37 complete + 14 window-sensitive breakdown (not "all both-fail")
- 4 minor documentation updates applied (commit c20b0b9)
- Verdict: APPROVED WITH MINOR DOCUMENTATION UPDATES

---

## 4. What to Move to Appendix

### Detailed Content for Supplementary Materials

**Appendix A: Operator Construction Details**
- S² monopole Dirac operator: full formula D_S2(q) = ...
- S¹ discretization families: spectral_circle, ring, wilson_ring (implementation details)
- Product-discretized Kronecker sum: detailed matrix construction
- Hermiticity verification: numerical tolerance tests
- Shape consistency: expected dimension calculations

**Appendix B: Gate Definitions and Pass Criteria**
- Full gate specifications (q=0, Hermiticity, reproducibility, localization v3)
- Pass/fail thresholds with justifications
- Cross-family robustness criteria (spectral_circle and wilson_ring as references)
- Progressive profile tier definitions (tiny, medium, full)

**Appendix C: Audit Protocol (8-Aspect Framework)**
- Complete audit checklist (8 aspects × 5-10 checks each)
- Verification sources (transcript, run artifacts, documentation chain, test suite)
- Cross-file consistency protocol
- Red flag detection heuristics

**Appendix D: Extended Scientific Non-Claims**
- Full expansions of all 8 non-claims (currently in Section 9.6.1-9.6.8)
- "What v0.1.15 does NOT claim" + "Why NOT validated" + "What was actually tested"
- Move ~4,000 words of expanded non-claims to appendix, keep Table 9.1 in main text

**Appendix E: Future Work Details**
- Full Track A-D descriptions (currently Section 10.4-10.7)
- S²×S² next priority rationale
- Wilson/fermion-doubling audit methodology
- Cross-discretization robustness tests

---

## 5. What to Delete or Merge

### Identified Redundancies and Consolidation Targets

**Duplication 1: "Falsification-First" Definition (8+ occurrences)**

| Current Location | Action |
|------------------|--------|
| Section 1.1 (Introduction) | **Keep:** First definition with toy validation challenge context |
| Section 1.2 (Contribution) | **Merge:** Consolidate with 1.1, no separate definition |
| Section 2.1 (Motivation) | **Delete:** Reference Section 1.1 instead |
| Section 3.1 (Falsification Ladder) | **Brief reference:** "As defined in Section 1..." |
| Section 10.1 (Contributions Summary) | **Delete:** Redundant with Introduction |

**Savings:** ~1,200 words (eliminate 4 redundant definitions)

---

**Duplication 2: v0.1.15 Quantitative Results (12+ occurrences)**

| Current Location | Action |
|------------------|--------|
| Section 1.1 (Introduction example) | **Keep:** One sentence with forward reference to Table 3 |
| Section 6.1, 6.2 (Case Study) | **Centralize:** Full results in Table 3, narrative refers to table |
| Section 7.1 (Caveat Discovery) | **Reference:** "As shown in Table 3..." |
| Section 8.3 (Audit Findings) | **Reference:** Cross-check table, no duplication |
| Section 10.2 (Contributions) | **Delete:** Redundant with Case Study |

**Strategy:** Create **Table 3 (Core Gates Pass Rate)** with all quantitative results:
```
| Metric | Value | Source |
|--------|-------|--------|
| Total cases | 6615 | Full diagnostic |
| q=0 false positives | 0/945 | Control gate |
| Hermiticity pass | 6615/6615 | Baseline gate |
| Reproducibility | 6615/6615 | Seeded re-runs |
| Disordered localization | 5619/5670 (99.1%) | Diagnostic gate |
| Ring/alpha=0 failures | 51/~630 (8.3%) | Subspace analysis |
| s1_size≥64 failures | 0/252 (0.0%) | Targeted follow-up |
```

**Savings:** ~2,500 words (replace narrative repetitions with table references)

---

**Duplication 3: Scientific Non-Claims (3+ locations)**

| Current Location | Action |
|------------------|--------|
| Section 1.3 (Introduction) | **Brief mention:** "See Table 9.1 for complete non-claims" |
| Section 9.6 (Limitations) | **Keep:** Table 9.1 (8 rows, concise reasons) in main text |
| Section 9.6.1-9.6.8 (Expanded non-claims) | **Move to Appendix D:** Full expansions with "What does NOT claim" + "Why NOT" + "What was tested" |
| Section 10.8 (Closing Statement) | **Brief recap:** "As stated in Table 9.1..." |

**Savings:** ~4,000 words (move expanded non-claims to Appendix D, keep Table 9.1 in main text)

---

**Duplication 4: Audit Methodology (2 locations)**

| Current Location | Action |
|------------------|--------|
| Section 8.2 (Audit Protocol) | **Keep:** Brief description (200 words) + "See Appendix C for full protocol" |
| Section 8.2.2 (Eight-Aspect Framework) | **Table form:** 8 aspects × 2 columns (Focus, Critical Questions) = 100 words |
| Section 10.1.5 (Contributions Summary) | **Delete:** Redundant with Section 8 |

**Savings:** ~800 words (condense audit methodology, move full checklist to Appendix C)

---

**Duplication 5: Ring/Alpha=0 Caveat Narrative (5 locations)**

| Current Location | Action |
|------------------|--------|
| Section 1.1 (Introduction example) | **Keep:** One-sentence mention as motivation |
| Section 6 (Case Study) | **Brief:** Detection only (subspace concentration) |
| Section 7 (Caveat Discovery) | **Full narrative:** Investigation + classification + guideline (1200 words) |
| Section 8.3 (Audit Findings) | **Brief:** Audit verified breakdown (37 + 14), 100 words |
| Section 9.2 (Limitations) | **Brief:** Finite-lattice context, 100 words |
| Section 10.2 (Contributions) | **Delete:** Redundant with Section 7 |

**Savings:** ~1,500 words (eliminate redundant tellings, keep Section 7 as canonical)

---

**Total Savings from Duplication Elimination: ~10,000 words**

---

## 6. Section-by-Section Compression Targets

### Current → Target Word Counts

| Section | Current Words | Target Words | Reduction | Strategy |
|---------|--------------|-------------|-----------|----------|
| **1. Introduction** | ~4,200 | 800-1000 | -76% | Remove case study details, condense thesis, eliminate redundant definitions |
| **2. Motivation** | ~3,800 | 800-1000 | -74% | Focus on validation gap, trim related work, cut repetitive framing |
| **3. Falsification Ladder** | ~4,100 | — | -100% | **Merge into new Section 3 (Methods)** |
| **4. Controls/Gates** | ~4,500 | — | -100% | **Merge into new Section 3 (Methods)** |
| **5. Progressive Profiles** | ~3,900 | — | -100% | **Merge into new Section 3 (Methods)** |
| **→ New Section 3 (Methods)** | — | 1500-2000 | — | Ladder + gates + profiles combined, operator details to Appendix A |
| **6. Case Study** | ~4,700 | — | -100% | **Merge with Section 7 → new Section 4** |
| **7. Caveat Discovery** | ~4,300 | — | -100% | **Merge with Section 6 → new Section 4** |
| **→ New Section 4 (Case Study + Caveat)** | — | 2000-2500 | — | Full diagnostic + ring/alpha=0 caveat as single narrative, Table 3 for numbers |
| **8. Audit** | ~5,200 | — | -100% | **Merge with Section 9 → new Section 5** |
| **9. Limitations** | ~7,800 | — | -100% | **Merge with Section 8 → new Section 5** |
| **→ New Section 5 (Audit/Limitations)** | — | 1200-1500 | — | Audit findings + Table 9.1, expanded non-claims to Appendix D |
| **10. Conclusion** | ~5,900 | 700-1000 | -83% | Condense 4 future work tracks to bullet lists, remove duplication |
| **Front matter** | ~1,500 | 200-250 | -83% | Abstract only (TOC and lists auto-generated) |
| **Appendices (new)** | — | (supplementary) | — | Operator construction, gates, audit protocol, extended non-claims, future work details |
| **Total Main Text** | ~42,900 | 10,000-12,000 | -72% | Target achieved through merging, consolidation, and appendix relocation |

---

### Detailed Section Notes

**Section 1 (Introduction): 4,200 → 800-1000 words**

**Keep:**
- Motivation paragraph: validation challenge for toy operators (discretization vs genuine behavior)
- Core thesis: falsification-first workflow required
- GeoSpectra Ladder contribution: four-tier validation (controls → baseline → diagnostic → cross-family)
- Ring/alpha=0 example: one sentence ("51 failures at small lattice vanish at s1_size≥64")

**Cut:**
- Detailed case study results (move to Section 4)
- Repeated "falsification-first" definition (consolidate to one paragraph)
- Rung-by-rung ladder description (brief mention, full in Section 3)
- Caveat discovery workflow details (one sentence, full in Section 4)

**Merge:**
- Section 1.1 + 1.2 → single Introduction with thesis upfront

---

**Section 2 (Motivation): 3,800 → 800-1000 words**

**Keep:**
- Validation gap: toy models lack falsification discipline
- Related work: TDD stops at green tests, academic validation is post-hoc
- GeoSpectra contribution: pre-registered protocol, not post-hoc narrative

**Cut:**
- Repeated falsification-first definition (reference Section 1)
- Extended literature review (condense to 2-3 key citations)
- Detailed comparison to TDD/CI/CD (one paragraph sufficient)

---

**New Section 3 (Methods): 1500-2000 words**

**Merged from:** Sections 3 (Falsification Ladder) + 4 (Controls/Gates) + 5 (Progressive Profiles)

**Structure:**
- **3.1 Falsification Ladder Framework (500 words):** Four tiers (controls, baseline, diagnostic, cross-family), brief description
- **3.2 Controls and Gates (500 words):** q=0 gate, Hermiticity, reproducibility, localization v3, cross-family robustness
- **3.3 Progressive Profile Analysis (500 words):** Tiny → medium → full escalation, caveat discovery workflow (detection → investigation → classification → guideline)

**Cut:**
- Detailed operator construction (move to Appendix A)
- Full gate definitions (move to Appendix B)
- Rung-by-rung repetitive descriptions
- Extended progressive profile examples

**Reference:** "See Appendix A for operator construction details, Appendix B for gate definitions"

---

**New Section 4 (Case Study + Caveat): 2000-2500 words**

**Merged from:** Sections 6 (Case Study) + 7 (Caveat Discovery)

**Structure:**
- **4.1 S²×S¹ Full Diagnostic (800 words):** 6615 cases, all gates passed, 51 failures (Table 3 for numbers)
- **4.2 Subspace Failure Concentration (400 words):** Ring/alpha=0 subspace rate 8.3% vs 0.8% aggregate
- **4.3 Targeted Follow-Up (400 words):** 1349 cases, lattice-size scaling hypothesis, s1_size extended to 64, 96
- **4.4 Caveat Classification (400 words):** 0/252 failures at s1_size≥64 → verdict SMALL_LATTICE_ARTIFACT, production guideline derived
- **4.5 Lesson (200 words):** Aggregate rates hide subspace failures, targeted investigation required

**Cut:**
- Repeated quantitative results (centralize in Table 3)
- Full parameter distributions (s1_size, disorder, monopole charge) — keep high-level summary, move details to Appendix
- Redundant caveat narrative (eliminate 5-location repetition, single canonical telling)

**Key Figure:** Figure 7 (Lattice-Size Scaling) — ring/alpha=0 failure rate vs s1_size

---

**New Section 5 (Audit and Limitations): 1200-1500 words**

**Merged from:** Sections 8 (Audit) + 9 (Limitations)

**Structure:**
- **5.1 Independent Audit (400 words):** Eight-aspect framework (table form), 2 interpretation discrepancies identified, 4 minor documentation updates applied
- **5.2 Audit Findings (300 words):** 37 complete + 14 window-sensitive breakdown (not "all both-fail"), verdict APPROVED WITH MINOR DOCUMENTATION UPDATES
- **5.3 Scientific Non-Claims (Table 9.1) (300 words):** Table with 8 non-claims + brief context ("toy scope = finite lattices")
- **5.4 Limitations Summary (200 words):** Finite lattices (not continuum), S²×S¹ only (not S⁶), internal audit (not external peer review)

**Cut:**
- Full audit protocol (move to Appendix C)
- Expanded non-claims (8 subsections, ~4,000 words) → move to Appendix D
- Detailed limitation discussions (9.1-9.5) → condense to brief mentions, full details in Appendix D

**Key Table:** Table 9.1 (Scientific Non-Claims) — 8 rows, concise

---

**New Section 6 (Conclusion): 5,900 → 700-1000 words**

**Structure:**
- **6.1 Summary (300 words):** Falsification-first workflow validated on S²×S¹ toy operators, 6615+1349 cases, caveats documented, scope discipline maintained
- **6.2 Contribution (200 words):** Methodological (reusable workflow), NOT physical (toy diagnostics ≠ physical theories)
- **6.3 Future Work (300 words):** Four tracks as bullet lists (Track A: Publication, Track B: Operator Credibility, Track C: Geometry Generalization, Track D: Anti-Artifact Robustness)
- **6.4 Closing Statement (100 words):** Toy scope discipline is scientific integrity, not modesty

**Cut:**
- Repeated quantitative results (eliminate duplication with Introduction, Case Study)
- Detailed future work descriptions (move to Appendix E)
- Redundant closing statements (consolidate to one paragraph)

---

## 7. Risk Controls

### Critical Content That Must NOT Be Lost During Compression

**Risk 1: Caveat Erosion**

**Control:**
- [ ] Ring/alpha=0 caveat narrative preserved in Section 4.2-4.4 (full investigation + classification + guideline)
- [ ] Production guideline (s1_size≥64 for ring/alpha=0) stated explicitly in Case Study section
- [ ] Empirical threshold vs theorem distinction maintained ("empirical stability, NOT continuum convergence")
- [ ] Subspace failure concentration (8.3% vs 0.8% aggregate) documented to prevent "low rate = ignore" interpretation

**Risk 2: Non-Claims Weakening**

**Control:**
- [ ] Table 9.1 (Scientific Non-Claims) remains in main text (Section 5.3)
- [ ] All 8 non-claims preserved in table: continuum, S⁶, Standard Model, chirality, Witten, extra dimensions, hierarchy, observables
- [ ] Abstract references Table 9.1 explicitly ("See Table 9.1 for non-claims")
- [ ] Introduction and Conclusion reference Table 9.1 to prevent scope inflation
- [ ] Expanded non-claims moved to Appendix D (not deleted) for readers who want full reasoning

**Risk 3: Physical Overclaim via Omission**

**Control:**
- [ ] Every mention of "operator" qualified as "discretized toy operator"
- [ ] Every mention of "validation" qualified as "finite-lattice toy scope"
- [ ] "Continuum" never used without explicit caveat ("NOT continuum extrapolation")
- [ ] "S²×S¹" always followed by "product-discretized" or "toy geometry"
- [ ] "Guideline" always qualified as "empirical operational constraint, NOT theorem"

**Risk 4: Audit Corrections Hidden**

**Control:**
- [ ] Section 5.2 (Audit Findings) explicitly states: 37 complete + 14 window-sensitive breakdown
- [ ] Interpretation drift correction documented: initial "all both-fail" → corrected to "37 + 14"
- [ ] 4 minor documentation updates mentioned (commit c20b0b9)
- [ ] Verdict stated: APPROVED WITH MINOR DOCUMENTATION UPDATES (not "approved unconditionally")

**Risk 5: Production Guidance Lost**

**Control:**
- [ ] Production guideline stated explicitly in Section 4.4: "Ring/alpha=0: s1_size ≥ 64"
- [ ] Contrast guideline: spectral_circle and wilson_ring robust at all tested sizes
- [ ] Empirical nature emphasized: "data-driven operational constraint, NOT mathematical proof"
- [ ] Confidence bounds mentioned: 95% CI upper bound ≈ 1.2% (Rule of Three: 3/252)

---

## 8. Recommended Editing Order

### Sequential Compression Workflow (7 Steps)

**Step 1: Create Canonical Table/Figure Set**

**Objective:** Centralize quantitative results to prevent duplication in narrative text.

**Tasks:**
- [ ] Generate Table 1 (Validation Chain): 8 steps from controls to baseline promotion
- [ ] Generate Table 3 (Core Gates Pass Rate): All v0.1.15 quantitative results in one table
- [ ] Generate Figure 7 (Lattice-Size Scaling): Ring/alpha=0 failure rate vs s1_size plot
- [ ] Format Table 9.1 (Scientific Non-Claims): 8 rows, concise reasons column

**Output:** 3 tables + 1 figure, all referenced throughout compressed text

**Timeline:** 2-3 hours

---

**Step 2: Compress Sections 1-2 (Introduction + Motivation)**

**Objective:** Eliminate redundant definitions, consolidate thesis, remove case study details.

**Tasks:**
- [ ] Merge Section 1.1 + 1.2 → single Introduction with thesis upfront
- [ ] Remove repeated "falsification-first" definitions (keep one paragraph)
- [ ] Replace ring/alpha=0 case study details with one-sentence forward reference to Section 4
- [ ] Condense Section 2 (Motivation): focus on validation gap, trim related work to 2-3 citations
- [ ] Add "See Table 9.1 for scientific non-claims" in Introduction

**Target:** Section 1: 800-1000 words, Section 2: 800-1000 words

**Timeline:** 3-4 hours

---

**Step 3: Merge Sections 3-4-5 → New Section 3 (Methods)**

**Objective:** Combine Falsification Ladder + Controls/Gates + Progressive Profiles into unified methodology section.

**Tasks:**
- [ ] Write Section 3.1 (Falsification Ladder): Four tiers, brief description (500 words)
- [ ] Write Section 3.2 (Controls/Gates): q=0, Hermiticity, reproducibility, localization v3, cross-family (500 words)
- [ ] Write Section 3.3 (Progressive Profiles): Tiny → medium → full, caveat discovery workflow (500 words)
- [ ] Add forward references: "See Appendix A (operator construction), Appendix B (gate definitions)"
- [ ] Move detailed operator construction to Appendix A
- [ ] Move full gate specifications to Appendix B

**Target:** New Section 3: 1500-2000 words

**Timeline:** 4-5 hours

---

**Step 4: Merge Sections 6-7 → New Section 4 (Case Study + Caveat)**

**Objective:** Combine full diagnostic and ring/alpha=0 caveat discovery into single narrative.

**Tasks:**
- [ ] Write Section 4.1 (S²×S¹ Full Diagnostic): 6615 cases, all gates passed, 51 failures, reference Table 3 (800 words)
- [ ] Write Section 4.2 (Subspace Concentration): Ring/alpha=0 8.3% vs 0.8% aggregate (400 words)
- [ ] Write Section 4.3 (Targeted Follow-Up): 1349 cases, lattice-size scaling hypothesis (400 words)
- [ ] Write Section 4.4 (Caveat Classification): 0/252 at s1_size≥64 → SMALL_LATTICE_ARTIFACT, guideline (400 words)
- [ ] Write Section 4.5 (Lesson): Aggregate rates hide subspace failures (200 words)
- [ ] Replace repeated quantitative results with "As shown in Table 3..."
- [ ] Include Figure 7 (Lattice-Size Scaling) with caption

**Target:** New Section 4: 2000-2500 words

**Timeline:** 5-6 hours

---

**Step 5: Merge Sections 8-9 → New Section 5 (Audit and Limitations)**

**Objective:** Combine audit findings and scientific non-claims into scope discipline section.

**Tasks:**
- [ ] Write Section 5.1 (Independent Audit): Eight-aspect framework (table form), brief (400 words)
- [ ] Write Section 5.2 (Audit Findings): 37 + 14 breakdown, verdict APPROVED WITH MINOR UPDATES (300 words)
- [ ] Write Section 5.3 (Scientific Non-Claims): Include Table 9.1, brief context (300 words)
- [ ] Write Section 5.4 (Limitations Summary): Finite lattices, S²×S¹ only, internal audit (200 words)
- [ ] Move full audit protocol to Appendix C
- [ ] Move expanded non-claims (Section 9.6.1-9.6.8, ~4,000 words) to Appendix D

**Target:** New Section 5: 1200-1500 words

**Timeline:** 4-5 hours

---

**Step 6: Shorten Section 10 → New Section 6 (Conclusion)**

**Objective:** Condense future work tracks, eliminate duplication, tighten closing statement.

**Tasks:**
- [ ] Write Section 6.1 (Summary): Workflow validated, 6615+1349 cases, caveats documented (300 words)
- [ ] Write Section 6.2 (Contribution): Methodological, NOT physical (200 words)
- [ ] Write Section 6.3 (Future Work): Four tracks as bullet lists (300 words)
  - Track A: Publication (external review, preprint, journal)
  - Track B: Operator Credibility (Wilson audit, Dirac checks)
  - Track C: Geometry Generalization (S²×S² next, then S³×S¹)
  - Track D: Anti-Artifact Robustness (cross-discretization, finite-size scaling)
- [ ] Write Section 6.4 (Closing Statement): Toy scope discipline = scientific integrity (100 words)
- [ ] Move detailed future work descriptions to Appendix E
- [ ] Remove repeated quantitative results (already in Introduction, Case Study)

**Target:** New Section 6: 700-1000 words

**Timeline:** 3-4 hours

---

**Step 7: Final Scope Review and Abstract**

**Objective:** Verify all non-claims preserved, caveats intact, abstract references Table 9.1.

**Tasks:**
- [ ] Draft 200-word abstract:
  - Thesis (falsification-first workflow for toy operators)
  - v0.1.15 case study (S²×S¹, 6615+1349 cases, ring/alpha=0 caveat resolved)
  - Contribution (methodological, NOT physical)
  - **Reference Table 9.1 explicitly:** "See Table 9.1 for scientific non-claims"
- [ ] Cross-check all "discretized toy operator" qualifications
- [ ] Verify all "finite lattice" caveats present
- [ ] Confirm no physical overclaims (continuum, S⁶, Standard Model, chirality, Witten, extra dimensions, hierarchy, observables)
- [ ] Verify production guideline stated (s1_size≥64 for ring/alpha=0)
- [ ] Verify audit corrections documented (37 + 14 breakdown, 4 minor updates)

**Output:** Final compressed manuscript (10,000-12,000 words) + abstract + scope-verified

**Timeline:** 2-3 hours

---

**Total Editing Timeline:** 23-30 hours (3-4 working days)

---

## 9. Acceptance Criteria

### Compression Plan Success Metrics

**[ ] Plan created**
- ✅ Compression plan documented (this file)
- ✅ Target structure defined (6 main sections, 10k-12k words)
- ✅ Section-by-section targets specified
- ✅ Editing order workflow outlined (7 steps)

**[ ] Target 10k-12k feasible**
- ✅ Duplication elimination: ~10,000 words saved
- ✅ Section merging: 10 sections → 6 sections
- ✅ Appendix relocation: ~5,000 words moved to supplementary materials
- ✅ Total reduction: ~31,000 words (72%) achievable through systematic compression

**[ ] Non-claims preserved**
- ✅ Table 9.1 (Scientific Non-Claims) remains in main text (Section 5.3)
- ✅ All 8 non-claims preserved: continuum, S⁶, Standard Model, chirality, Witten, extra dimensions, hierarchy, observables
- ✅ Expanded non-claims moved to Appendix D (not deleted)
- ✅ Abstract references Table 9.1 explicitly

**[ ] Caveats preserved**
- ✅ Ring/alpha=0 caveat: full investigation + classification + guideline in Section 4.2-4.4
- ✅ Production guideline: s1_size≥64 for ring/alpha=0 explicitly stated
- ✅ Empirical threshold vs theorem distinction maintained
- ✅ Subspace concentration (8.3% vs 0.8%) documented

**[ ] Audit corrections not hidden**
- ✅ Section 5.2 documents 37 + 14 breakdown (not "all both-fail")
- ✅ Interpretation drift correction explicitly mentioned
- ✅ 4 minor documentation updates cited (commit c20b0b9)
- ✅ Verdict stated: APPROVED WITH MINOR DOCUMENTATION UPDATES

**[ ] Next edit pass clearly specified**
- ✅ Step 1: Create canonical table/figure set (3 tables + 1 figure)
- ✅ Step 2: Compress Sections 1-2 (Introduction + Motivation)
- ✅ Step 3: Merge Sections 3-5 → New Section 3 (Methods)
- ✅ Step 4: Merge Sections 6-7 → New Section 4 (Case Study + Caveat)
- ✅ Step 5: Merge Sections 8-9 → New Section 5 (Audit + Limitations)
- ✅ Step 6: Shorten Section 10 → New Section 6 (Conclusion)
- ✅ Step 7: Final scope review + abstract

---

## Document Status

**Compression Plan:** COMPLETE

**Current Manuscript:** 42,916 words  
**Target Manuscript:** 10,000-12,000 words (72% reduction)  
**Feasibility:** CONFIRMED (duplication elimination + section merging + appendix relocation)

**Risk Controls:** ALL IN PLACE
- ✅ Caveat preservation
- ✅ Non-claims preservation
- ✅ Physical overclaim prevention
- ✅ Audit corrections documentation
- ✅ Production guideline retention

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)

**Next Milestone:** Execute 7-step compression workflow (3-4 working days) → compressed manuscript v0.1.16-compressed → external domain expert review (Track A)

---

**Compression Plan v0.1.16 — Complete**

**Date:** 2026-05-17  
**Status:** Ready for execution  
**Estimated Timeline:** 3-4 working days (23-30 hours)  
**Next Step:** Step 1 — Generate canonical table/figure set (Table 1, Table 3, Figure 7, Table 9.1)
