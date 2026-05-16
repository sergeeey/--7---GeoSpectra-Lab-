---

## Appendices

### Appendix A: Operator Construction Details

**[TODO: Add operator construction formulas]**

- S² monopole Dirac operator: D_S2(q) construction
- S¹ discretization families: spectral_circle, ring, wilson_ring
- Product-discretized Kronecker sum: D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1(alpha, W)
- Hermiticity verification protocol
- Shape consistency checks

### Appendix B: Gate Definitions and Pass Criteria

**[TODO: Formalize gate definitions]**

- q=0 gate: No spurious localization on monopole-free operators
- Hermiticity gate: ||D - D†|| < 1e-9
- Reproducibility gate: Seeded eigenvalue checksum matching
- Localization gate v3 (window-robust): IPR contrast across multiple windows
- Cross-family robustness: Spectral_circle and wilson_ring as reference families

### Appendix C: Audit Protocol (8-Aspect Framework)

**[TODO: Expand audit methodology]**

Eight-aspect framework from Section 8:
1. Data integrity
2. Statistical claims
3. Test suite quality
4. Scope protection
5. Audit independence
6. Artifact completeness
7. Red flags
8. Scientific rigor

### Appendix D: Data Availability Statement

**[TODO: Add data availability]**

Run artifacts for v0.1.15 baseline:
- Full diagnostic: reports/RUNS/20260515-201150_s2_s1_product_discretized_full/
- Targeted follow-up: reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/
- Test suite: 203 tests (pytest)
- Source code: cc_toy_lab/ module (Python 3.11+)

Artifact archival: [TODO: Zenodo DOI or Figshare link after external review]

---

## TODO List for External Review

### High Priority (Blocking Publication)

1. **[ ] External domain expert review**
   - [ ] Lattice field theory expert (fermion discretization, Wilson term)
   - [ ] Differential geometry expert (Dirac operators, Atiyah-Singer index)
   - [ ] Numerical analysis expert (eigenvalue solvers, finite-size scaling)

2. **[ ] Generate minimal figures/tables**
   - [ ] Table 1 (Validation Chain): CSV → Markdown table
   - [ ] Table 3 (Core Gates Pass Rate): Extract from summary.md
   - [ ] Figure 7 (Lattice-Size Scaling): Python plot from FIGURE_DATA_LATTICE_SIZE_SCALING_v0.1.16.md
   - [ ] Table 9.1 (Scientific Non-Claims): Already drafted, convert to paper format

3. **[ ] Draft 200-word abstract**
   - [ ] Reference Table 9.1 (non-claims) in line 3
   - [ ] State v0.1.15 case study scope explicitly
   - [ ] Clarify toy scope (finite lattices, NOT continuum)

4. **[ ] Reference cleanup**
   - [ ] Add citations for: Anderson localization (Anderson 1958), Atiyah-Singer index (Atiyah & Singer 1968), Wilson fermions (Wilson 1977)
   - [ ] Cross-check all section references (Figure 1, Table 3, Section 7.2)
   - [ ] Verify no broken internal links

### Medium Priority (Post-Review)

5. **[ ] Reduce duplication across sections**
   - [ ] Sections 1, 2, 10 repeat "falsification-first" definition → consolidate
   - [ ] Sections 6, 7, 8 repeat v0.1.15 quantitative results → centralize in Table 3
   - [ ] Section 9 expands each non-claim; consider moving details to Appendix

6. **[ ] Word count trimming**
   - [ ] Current draft: ~41,000 words + front matter = ~42,000 words total
   - [ ] Target for submission: 8,000-12,000 words (journal methodology paper)
   - [ ] Strategy: Move operator construction details to Appendix A, condense Sections 5-7

7. **[ ] Public README cleanup**
   - [ ] Quick start guide (install, run pytest, reproduce v0.1.15)
   - [ ] Link to methodology paper draft
   - [ ] Scientific non-claims upfront (Table 9.1 reference)

### Low Priority (Nice-to-Have)

8. **[ ] Supplementary materials**
   - [ ] Minimal reproducibility package (<50 MB): config.json, summary.md, 100-case subset
   - [ ] Upload to Zenodo or Figshare (DOI-backed archival)

9. **[ ] Acknowledgments section**
   - [ ] Thank external reviewers (after review complete)
   - [ ] Acknowledge computational resources (hardware, runtime)
   - [ ] Cite Tom Lawrance's covariant compactification framework (inspirational source)

10. **[ ] Preprint submission checklist**
    - [ ] arXiv subject class: physics.comp-ph (Computational Physics) or math.NA (Numerical Analysis)
    - [ ] Include "toy model" and "finite lattice" in title/abstract
    - [ ] Reference Table 9.1 (non-claims) in abstract to prevent misinterpretation

---

## Duplication Hotspots (Identified During Assembly)

**[TODO: Address in post-assembly editing pass]**

1. **"Falsification-first" definition repeated 8+ times**
   - Sections 1.1, 1.2, 2.1, 3.1, 10.1
   - **Fix:** Define once in Section 1.2, reference thereafter

2. **v0.1.15 quantitative results (6615 cases, 51 failures, s1_size≥64) repeated 12+ times**
   - Sections 1.1, 6.1, 6.2, 7.1, 8.3, 10.2
   - **Fix:** Centralize in Table 3 (Core Gates Pass Rate), reference in text

3. **Scientific non-claims (8 items) repeated in Sections 1, 9, 10**
   - Section 1.3: Brief mention
   - Section 9.6: Full table with expansions
   - Section 10.8: Recap in closing statement
   - **Fix:** Keep Table 9.1 as canonical reference, condense Sections 1 and 10

4. **Audit methodology (8-aspect framework) described in Sections 8.2 and 10.1.5**
   - **Fix:** Full description in Section 8.2, summary bullet list in Section 10.1.5

5. **Ring/alpha=0 caveat narrative appears in Sections 6, 7, 8, 9, 10**
   - **Fix:** Full narrative in Section 7 (Caveat Discovery), brief mentions elsewhere

---

## Assembly Statistics

**Word Count Breakdown:**

| Section | Approx. Words | % of Total |
|---------|--------------|-----------|
| Section 1 (Introduction) | ~4,200 | 10% |
| Section 2 (Motivation) | ~3,800 | 9% |
| Section 3 (Falsification Ladder) | ~4,100 | 10% |
| Section 4 (Controls/Gates) | ~4,500 | 11% |
| Section 5 (Progressive Profiles) | ~3,900 | 9% |
| Section 6 (Case Study) | ~4,700 | 11% |
| Section 7 (Caveat Discovery) | ~4,300 | 10% |
| Section 8 (Audit) | ~5,200 | 12% |
| Section 9 (Limitations) | ~7,800 | 19% |
| Section 10 (Conclusion) | ~5,900 | 14% |
| **Subtotal (10 sections)** | **~41,000** | **98%** |
| Front matter + TODOs | ~1,200 | 3% |
| **Total Draft** | **~42,200** | **100%** |

**Compression targets for journal submission:**
- Remove ~30,000 words (70% reduction)
- Strategy: Move operator construction to Appendix, condense case study narrative, streamline Section 9 expansions

---

## Next Steps (Post-Assembly)

### Immediate (This Week)

1. **Generate minimal figures/tables** (Track A, Section 10.4)
   - Table 1: Validation Chain (8 steps)
   - Table 3: Core Gates Pass Rate (extract from summary.md)
   - Figure 7: Lattice-Size Scaling (Python plot from figure data)
   - Table 9.1: Scientific Non-Claims (already drafted, format for paper)

2. **Draft 200-word abstract**
   - Reference Table 9.1 (non-claims) explicitly
   - State v0.1.15 scope (S²×S¹, finite lattices, three families)
   - Clarify contribution is methodological, NOT physical

3. **First-pass duplication reduction**
   - Consolidate "falsification-first" definitions
   - Centralize v0.1.15 quantitative results in Table 3
   - Move operator construction details to Appendix A

### Medium-Term (Next 2-4 Weeks)

4. **External domain expert review** (Track A, Section 10.4.3)
   - Submit draft to lattice field theory expert
   - Submit draft to differential geometry expert
   - Submit draft to numerical analysis expert
   - Allow 4-6 weeks for review, 2 weeks for revisions

5. **Public README cleanup** (Track A, Section 10.4.2)
   - Installation guide (Python 3.11+, dependencies)
   - Quick start (run pytest, reproduce v0.1.15 diagnostic)
   - Link to methodology paper draft
   - Scientific non-claims upfront (Table 9.1)

6. **Artifact archival** (Track A, Section 10.4.4)
   - Upload v0.1.15 run artifacts to Zenodo (DOI)
   - Create minimal reproducibility package (<50 MB)
   - Update Appendix D with DOI link

### Long-Term (After External Review)

7. **Preprint submission** (arXiv)
   - Subject class: physics.comp-ph or math.NA
   - Include "toy model" and "finite lattice" in title
   - Reference Table 9.1 (non-claims) in abstract

8. **Journal submission**
   - Target: journal specializing in computational physics or numerical methods
   - Expected page limit: 20-30 pages (8,000-12,000 words)
   - Supplementary materials: reproducibility package, extended appendices

---

## Document Status

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)

**Paper Draft Status:**
- ✅ All 10 sections assembled
- ✅ Front matter added (title, abstract placeholder, TOC, table/figure list)
- ✅ TODO markers for external review
- ✅ Duplication hotspots identified
- ⚠️ Abstract: placeholder only (needs 200-word draft)
- ⚠️ Tables/figures: placeholders only (needs generation)
- ⚠️ References: not yet added (needs citation cleanup)
- ⚠️ Word count: 42,200 words (needs 70% reduction for journal submission)

**Scientific Scope Discipline:**
- ✅ Scientific non-claims (Table 9.1) preserved across all sections
- ✅ Toy scope explicit (finite lattices, NOT continuum)
- ✅ No physical overclaims (continuum, S⁶, Standard Model, chirality, Witten, extra dimensions, hierarchy, observables)
- ✅ Methodology contribution clearly stated (falsification-first workflow, NOT physical theory proof)

**Next Milestone:** External domain expert review (Track A) → preprint submission → journal peer review → publication

---

**Methodology Paper Draft v0.1.16 — Assembly Complete**

**Date:** 2026-05-17  
**Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Total Word Count:** ~42,200 words  
**Status:** Internal draft assembled, pending external review

**Recommended Next Step:** Generate minimal figures/tables (Table 1, Table 3, Figure 7, Table 9.1) → draft 200-word abstract → submit to external domain expert for pre-publication review (Track A).
