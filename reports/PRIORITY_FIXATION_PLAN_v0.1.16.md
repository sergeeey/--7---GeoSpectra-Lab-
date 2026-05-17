# Priority Fixation Plan — v0.1.16

**Date:** 2026-05-17  
**Project:** GeoSpectra / Covariant Compactification Toy Lab  
**Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Manuscript:** v0.1.16 compressed methodology paper (8,950 words)

---

## Purpose

Establish **public priority** for the GeoSpectra Falsification Ladder methodology before contacting external domain expert reviewers. Priority fixation through GitHub release + Zenodo DOI ensures:

1. **Timestamped public record** — methodology documented before external review
2. **Citable artifact** — reviewers can cite specific version (DOI)
3. **IP protection via publication** — establishes prior art (NOT patent protection)
4. **Academic integrity** — public preregistration of methods before peer review

**What priority fixation protects:**
- Methodological contribution (Falsification Ladder workflow)
- Case study evidence (S²×S¹ validation, 6615+6615+1349 cases)
- Caveat handling protocol (ring/alpha=0 resolution)
- Scientific non-claims framework (8 explicit scope boundaries)

**What priority fixation does NOT protect:**
- Commercial use of methods (NOT patent protection)
- Ideas or concepts without implementation
- Future extensions (only fixes current v0.1.16 state)
- Physical theories (toy diagnostics only, no physics claims)

---

## Current Repository State

**GitHub URL:** https://github.com/sergeeey/--7---GeoSpectra-Lab-.git

**Branch:** main  
**Latest commit:** 79f8f1c — Apply v0.1.16 Codex audit documentation fixes  
**Tag:** v0.1.15-s2-s1-product-discretized-full (computational baseline)

**Commit history (recent 5):**
1. **79f8f1c** — Apply v0.1.16 Codex audit documentation fixes (2026-05-17)
2. **da7c15a** — Add v0.1.16 external review package (2026-05-17)
3. **fee661a** — Add v0.1.16 compressed methodology manuscript (2026-05-17)
4. **c20b0b9** — Clarify v0.1.15 audit documentation (2026-05-16)
5. **65b6973** — Release v0.1.15: S2xS1 product-discretized full validation (2026-05-16)

**Working tree:** Clean ✓  
**Remote:** Synced with origin/main ✓  
**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged) ✓

---

## Manuscript State

**File:** `reports/METHODOLOGY_PAPER_COMPRESSED_v0.1.16.md`

**Title:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"

**Status:** READY FOR EXTERNAL REVIEW

**Metrics:**
- **Word count:** 8,950 words (80.2% compression from 45,100-word full draft)
- **Abstract:** 221 words (explicit evidence details, scope boundaries)
- **Sections:** 6 (Introduction, Motivation, Methods, Case Study, Audit/Limitations, Future Work)
- **Tables:** 8 (sequential numbering: Table 1-8)
- **Figures:** 1 (Figure 7: ring/alpha=0 lattice-size scaling)

**Key content:**
- Falsification Ladder (9 rungs: controls → gates → profiles → audit → follow-up → integrity)
- S²×S¹ case study (6615 full diagnostic + 6615 reproducibility + 1349 targeted follow-up)
- Ring/alpha=0 caveat resolution (failures vanish at s1_size≥64)
- Independent audit (3 corrections applied, classification confirmed)
- 8 scientific non-claims (Table 3: no continuum, no S⁶/S³×S⁶, no SM, no physical chirality, no Witten/Lichnerowicz bypass, no physical extra dimensions, no hierarchy solution, no observable predictions)

**Codex audit verdict:** audit_pass_with_minor_documentation_fixes (5 minor issues resolved)

---

## External Review Package State

**Directory:** `reports/EXTERNAL_REVIEW_PACKAGE_v0.1.16/`

**Files (6):**
1. `README_REVIEW_PACKAGE.md` — package overview, reading order, GitHub URL
2. `REVIEW_GUIDELINES.md` — review scope, focus areas, what NOT to evaluate
3. `SCIENTIFIC_NONCLAIMS.md` — 8 explicit scope boundaries (Table 3 extract)
4. `VALIDATION_EVIDENCE_SUMMARY.md` — 6615+6615+1349 evidence summary
5. `REVIEWER_QUESTIONS.md` — 40+ domain-specific questions (3 tracks)
6. `COVER_LETTER_TEMPLATE.md` — customizable review request template

**Three reviewer tracks:**
1. **Lattice Field Theory** — Wilson term, fermion doubling, twisted BC
2. **Differential Geometry** — Dirac operator, product-discretization, S²×S¹ vs Calabi-Yau
3. **Numerical Analysis** — finite-size scaling, Decision Rule 1, convergence criteria

**Status:** COMPLETE, committed (da7c15a), ready for distribution

---

## What Is Being Claimed (Methodological Contribution)

**This work claims:**

✅ **Falsification-first workflow for discretized toy operators** — reusable 9-rung validation harness  
✅ **S²×S¹ case study validates methodology** — 6615+6615+1349 cases evidence  
✅ **Controls + progressive profiles catch failures early** — smoke 5 min → full 16 hours  
✅ **Independent audit prevents interpretation drift** — 2 discrepancies corrected  
✅ **Targeted follow-ups resolve caveats efficiently** — 1349 cases, 2.5 hours vs 16-hour full re-run  
✅ **Ring/alpha=0 caveat converted to production guideline** — s1_size≥64 empirically derived  
✅ **Caveat handling workflow is reusable** — caveats are outputs, not bugs to suppress

**Scope:** Finite-lattice toy diagnostics on S²×S¹ (q≤106, s1_size≤96). Methodology validated, NOT physics.

---

## What Is Explicitly NOT Claimed (8 Scientific Non-Claims)

**This work does NOT claim:**

❌ **No continuum compactification** — all operators discretized on finite lattices (s1_size≤96), no continuum extrapolation  
❌ **No S⁶ or S³×S⁶ validation** — only S², S³, S¹, S²×S¹ tested; higher dimensions not constructed  
❌ **No Standard Model derivation** — no gauge group (SU(3)×SU(2)×U(1)), no fermion generations, no gauge coupling  
❌ **No physical chirality proof** — Dirac indices are topological toy counts, NOT physical chiral fermions  
❌ **No Witten/Lichnerowicz bypass** — numerical index ≠ rigorous Atiyah-Singer theorem, computational shortcuts ≠ mathematical theorem  
❌ **No physical extra dimensions** — Anderson benchmark is numerical disorder test, NOT physical compactification mechanism  
❌ **No hierarchy problem solution** — toy radion model (if used) does NOT address moduli stabilization or cosmological constant  
❌ **No observable predictions** — topological invariants are discretized toy analogs, NOT continuum field theory predictions

**Framing:** Toy spectral diagnostics are **diagnostic tools**, NOT physical theories. Success on S²×S¹ finite lattices validates the **workflow**, NOT the **physics**.

---

## GitHub Release Plan

### Release Details

**Release tag:** `v0.1.16-methodology-review-draft`  
**Target commit:** `79f8f1c` (Codex audit fixes applied)  
**Release type:** Pre-release (external review pending)

**Release title:** "v0.1.16 — Falsification-First Methodology Manuscript (Pre-Review Draft)"

**Release description template:**

```markdown
# v0.1.16 — Falsification-First Methodology Manuscript (Pre-Review Draft)

**Status:** READY FOR EXTERNAL REVIEW (Track A: lattice field theory, differential geometry, numerical analysis)

**Manuscript:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"

**Word count:** 8,950 words (80.2% compression from 45,100-word full draft)  
**Baseline:** v0.1.15-s2-s1-product-discretized-full (computational validation)

---

## What This Release Contains

**Compressed methodology manuscript:**
- `reports/METHODOLOGY_PAPER_COMPRESSED_v0.1.16.md` (8,950 words)
- 6 sections + 8 tables + 1 figure
- Abstract: 221 words (evidence details, scope boundaries)
- Codex audit: 0 blockers, 5 minor documentation fixes applied

**External review package:**
- `reports/EXTERNAL_REVIEW_PACKAGE_v0.1.16/` (6 files, 65 KB)
- README, review guidelines, reviewer questions, scientific non-claims, validation evidence, cover letter template
- Three reviewer tracks: lattice field theory, differential geometry, numerical analysis

**Audit documentation:**
- `reports/INDEPENDENT_CODEX_AUDIT_v0.1.16.md` — independent audit report
- `reports/INDEPENDENT_CODEX_AUDIT_FIXES_v0.1.16.md` — fixes applied

---

## Key Evidence (v0.1.15 Baseline)

- **Full diagnostic:** 6615 cases (16 hours runtime)
- **Reproducibility:** 6615/6615 bit-identical pass (100%)
- **Targeted follow-up:** 1349 cases (ring/alpha=0 convergence at s1_size≥64)
- **Core gates:** 100% pass rate (Hermiticity, Shape, Reproducibility, Controls)
- **Independent audit:** 3 corrections applied, classification confirmed
- **q=0 false positives:** 0

---

## What This Work Claims

✅ Falsification-first workflow for discretized toy operators (reusable methodology)  
✅ S²×S¹ case study validates workflow (6615+6615+1349 cases)  
✅ Ring/alpha=0 caveat resolved via targeted follow-up (s1_size≥64 guideline)  
✅ Caveat handling protocol (converts failures to production guidelines)

**Scope:** Finite-lattice toy diagnostics on S²×S¹ (s1_size≤96). Methodology validated, NOT physics.

---

## What This Work Does NOT Claim (8 Scientific Non-Claims)

❌ No continuum compactification (finite lattices only, no s1_size→∞)  
❌ No S⁶/S³×S⁶ validation (only S², S³, S¹, S²×S¹ tested)  
❌ No Standard Model derivation (no gauge group, no fermion generations)  
❌ No physical chirality proof (Dirac indices are toy counts, not physical fermions)  
❌ No Witten/Lichnerowicz bypass (numerical ≠ theorem)  
❌ No physical extra dimensions (diagnostic geometry, not physical target)  
❌ No hierarchy solution (toy radion, not moduli stabilization)  
❌ No observable predictions (toy diagnostics, not continuum field theory)

**Table 3 (manuscript):** 8 explicit scope boundaries to prevent misinterpretation.

---

## Next Steps (Track A: External Review)

**Timeline:** 4-6 months

1. Identify 3 domain experts (lattice field theory, differential geometry, numerical analysis)
2. Customize `COVER_LETTER_TEMPLATE.md` for each reviewer
3. Send review requests (GitHub link + external review package)
4. Compile feedback (4-6 weeks per reviewer)
5. Revise manuscript → v0.1.17 (post-review)
6. Convert to LaTeX for arXiv
7. Submit preprint → arXiv (computational methods section)
8. Submit to journal (SIAM Journal on Scientific Computing / Journal of Computational Physics)

---

## Citation

**BibTeX:**
```bibtex
@misc{geospectra_v0.1.16_2026,
  author = {Boyko, Sergey},
  title = {A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds},
  year = {2026},
  version = {v0.1.16-methodology-review-draft},
  url = {https://github.com/sergeeey/--7---GeoSpectra-Lab-.git},
  note = {Pre-review methodology manuscript. Baseline: v0.1.15-s2-s1-product-discretized-full}
}
```

**APA:**
Boyko, S. (2026). *A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds* (v0.1.16-methodology-review-draft) [Pre-review manuscript]. https://github.com/sergeeey/--7---GeoSpectra-Lab-.git

---

## Disclaimer

**This is a pre-review manuscript.** External domain expert peer review has not yet been performed. Do not cite as peer-reviewed work.

**Methodology paper, NOT physical compactification proof.** This work validates a falsification-first workflow for discretized toy operators on finite lattices. It does NOT prove continuum compactification, Standard Model derivation, physical chirality, or S⁶/Calabi-Yau validation.

**Baseline:** v0.1.15-s2-s1-product-discretized-full (computational validation, promoted 2026-05-16).

**Contact:** sergeikuch80@gmail.com  
**Repository:** https://github.com/sergeeey/--7---GeoSpectra-Lab-.git
```

**Release checklist before publishing:**
- [ ] Verify commit 79f8f1c is HEAD
- [ ] Verify tag v0.1.15-s2-s1-product-discretized-full exists
- [ ] Mark as "Pre-release" (NOT latest stable)
- [ ] Include CITATION.cff in repository
- [ ] Include .zenodo.json for Zenodo DOI integration
- [ ] Verify no sensitive data in release artifacts

---

## Zenodo DOI Plan

**Platform:** Zenodo (https://zenodo.org)  
**Integration:** GitHub release → automatic Zenodo archival

### Zenodo Metadata (.zenodo.json)

**File location:** `.zenodo.json` (repository root)

**Required metadata:**
- **Title:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds (v0.1.16 Pre-Review Draft)"
- **Creators:** Sergey Boyko (ORCID if available)
- **Description:** Methodology paper presenting GeoSpectra Falsification Ladder workflow validated through S²×S¹ case study (6615+6615+1349 cases). Pre-review manuscript ready for external domain expert feedback.
- **Keywords:** falsification-first validation, spectral operators, compact manifolds, Anderson localization, finite-lattice diagnostics, methodology paper, Dirac operators
- **License:** CC BY 4.0 (Creative Commons Attribution 4.0 International)
- **Related identifiers:** GitHub repository URL
- **Version:** v0.1.16-methodology-review-draft
- **Publication date:** 2026-05-17
- **Resource type:** Pre-review manuscript

**Zenodo workflow:**
1. Link GitHub repository to Zenodo account (one-time setup)
2. Create GitHub release v0.1.16-methodology-review-draft
3. Zenodo automatically creates DOI and archives release
4. DOI badge added to README.md
5. DOI cited in external review requests

**Expected DOI format:** `10.5281/zenodo.XXXXXXX` (assigned after Zenodo archival)

---

## arXiv Timing Recommendation

**Recommendation:** **DO NOT submit to arXiv before external review completion.**

**Rationale:**
1. **arXiv is permanent** — corrections require versioning (v1 → v2), not quiet fixes
2. **External reviewers expect pre-publication draft** — arXiv submission = public claim of readiness
3. **Review feedback may require substantial revisions** — better to incorporate feedback before arXiv v1
4. **arXiv submission signals peer-review bypass** — methodology papers benefit from domain expert validation first

**Correct timeline:**
1. **Now (v0.1.16):** GitHub release + Zenodo DOI (priority fixation, citable artifact for reviewers)
2. **After external review (v0.1.17, ~4-6 months):** Incorporate reviewer feedback, revise manuscript
3. **arXiv submission (v0.1.17):** Submit to arXiv after external review, cite Zenodo DOI as prior version
4. **Journal submission (v0.1.17+):** Submit to SIAM/JCP with arXiv preprint reference

**Exception:** If external reviewers require arXiv preprint for institutional compliance, submit after obtaining their agreement to review.

---

## Ronin Researcher Contact Recommendation

**Context:** Ronin Institute supports independent scholars without institutional affiliation.

**Recommendation:** **Contact Ronin researchers AFTER GitHub release + Zenodo DOI, BEFORE arXiv submission.**

**Why contact Ronin researchers:**
1. **Domain expertise** — Ronin network includes lattice field theorists, differential geometers, numerical analysts
2. **Independent perspective** — not constrained by institutional politics or publish-or-perish pressure
3. **Methodology focus** — Ronin scholars often value rigorous methods over trendy physics claims
4. **Review quality** — independent researchers tend to provide thorough, skeptical feedback

**When to contact:**
- **After:** GitHub release (v0.1.16-methodology-review-draft) + Zenodo DOI created
- **Before:** arXiv submission (wait for external review feedback first)
- **Timeline:** Within 1-2 weeks of GitHub release + Zenodo DOI

**How to contact:**
1. Search Ronin Institute directory for relevant expertise (lattice field theory, differential geometry, numerical analysis)
2. Email using `COVER_LETTER_TEMPLATE.md` (customized for Ronin context)
3. Cite Zenodo DOI as citable artifact
4. Emphasize methodology contribution, NOT physical compactification
5. Request 4-6 week review timeline

**Ronin-specific framing:**
- "This is a **methodology paper** (falsification-first workflow for toy spectral diagnostics), NOT a physical compactification proof."
- "I'm seeking domain expert review from independent scholars who value rigorous methods over hype."
- "Your expertise in [lattice field theory / differential geometry / numerical analysis] would be invaluable in assessing [Wilson term implementation / product-discretization soundness / finite-size scaling methodology]."
- "No institutional politics, no publish-or-perish pressure — just honest technical feedback."

---

## IP Caution: Publication ≠ Patent Protection

**What priority fixation (GitHub release + Zenodo DOI) provides:**

✅ **Prior art** — establishes public record of methodology before external review  
✅ **Academic priority** — timestamped claim of methodological contribution  
✅ **Citable artifact** — DOI for reviewers and future citations  
✅ **Defensive publication** — prevents others from patenting your published methods

**What priority fixation does NOT provide:**

❌ **Patent protection** — publication immediately forfeits patent rights in most jurisdictions  
❌ **Commercial exclusivity** — anyone can use published methods (subject to license terms)  
❌ **Idea protection** — only specific implementation is documented, not general concepts  
❌ **Trade secret protection** — publication destroys trade secret status

**Patent vs Publication Trade-off:**

| Aspect | Patent | Publication (Zenodo DOI) |
|--------|--------|--------------------------|
| **Exclusive rights** | Yes (20 years) | No (public domain or CC BY) |
| **Cost** | $5,000-$15,000+ | Free |
| **Time to protection** | 1-3 years | Immediate |
| **Disclosure requirement** | Full disclosure | Full disclosure |
| **Enforcement** | Legal action required | N/A (no exclusivity) |
| **Academic credibility** | Low (seen as mercenary) | High (standard practice) |
| **Best for** | Commercial products | Academic methods |

**Recommendation for GeoSpectra:**

**Do NOT pursue patent** for Falsification Ladder methodology. Reasons:

1. **Academic context** — methodology papers are published, not patented
2. **Prior art risk** — controls, progressive profiles, targeted follow-ups are incremental improvements, not novel inventions
3. **No commercial product** — Falsification Ladder is a workflow, not a sellable technology
4. **Patent poison** — attempting to patent academic methods damages reputation in research community
5. **Publication better serves goals** — establishes priority, enables citations, builds academic credibility

**If commercial application emerges later:**
- Patent the **specific product/tool**, not the published methodology
- Keep product-specific optimizations trade secret until patent filed
- Cite published methodology as foundation (prior art), claim novel product features

**Current action:** GitHub release + Zenodo DOI (publication) is correct choice. Establishes priority, enables review, builds credibility.

---

## Summary

**Priority fixation plan:**
1. ✅ Codex audit fixes applied and committed (79f8f1c)
2. ✅ External review package committed and pushed (da7c15a)
3. **Next:** Create GitHub release v0.1.16-methodology-review-draft
4. **Next:** Link repository to Zenodo for automatic DOI generation
5. **Next:** Add DOI badge to README.md
6. **Next:** Contact domain expert reviewers (1-2 weeks after DOI created)
7. **Next:** Contact Ronin researchers (within 1-2 weeks of DOI)
8. **Wait:** arXiv submission AFTER external review (4-6 months)

**Timeline:**
- **Now (Day 0):** GitHub release + Zenodo DOI
- **Day 3-7:** Contact external reviewers (3 domain experts)
- **Day 7-14:** Contact Ronin researchers
- **Month 1-2:** Initial review feedback
- **Month 2-4:** Revise manuscript based on feedback
- **Month 4-6:** Final review round, manuscript v0.1.17
- **Month 6+:** arXiv submission → journal submission

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged, computational validation complete)

**Manuscript:** v0.1.16 compressed methodology paper (8,950 words, READY FOR EXTERNAL REVIEW)

**Next exact step:** Create GitHub release v0.1.16-methodology-review-draft with Zenodo integration.
