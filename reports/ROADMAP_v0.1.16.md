# Roadmap — v0.1.16

**Roadmap Date:** 2026-05-16  
**Previous Release:** v0.1.15-s2-s1-product-discretized-full  
**Planning Status:** CANDIDATE TRACKS EVALUATION

---

## Starting Point

### v0.1.15 Milestone Completed

**Current baseline:** v0.1.15-s2-s1-product-discretized-full

**Achievements:**
- **Full diagnostic:** 6615/6615 cases (product-discretized S²×S¹ operators)
- **Reproducibility pass:** 6615/6615 cases independently re-computed
- **Ring/alpha=0 targeted follow-up:** 1349 cases (lattice-size scaling investigation)
- **Verdict:** SMALL_LATTICE_ARTIFACT — all 51 failures vanish at s1_size≥64
- **Refined caveat:** Ring/alpha=0 requires s1_size≥64 for robustness
- **Pytest:** 203 passed, 1 warning
- **Release integrity audit:** release_integrity_confirmed
- **Git:** initialized, commit 65b6973, annotated tag created

**Scientific validation complete for:**
- S²×S¹ product-discretized operators (D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1)
- Three S¹ discretization families (spectral_circle, ring, wilson_ring)
- Anderson localization benchmark (disorder-induced localization test)
- Production guidelines for ring/alpha=0 (s1_size≥64)

**Repository state:**
- Code: stable, tested, committed
- Tests: 203 passing
- Reports: comprehensive (RELEASE_NOTES, VALIDATION_STATUS, SPECTRAL_REPORT, ISSUES_SCIENTIFIC)
- Run artifacts: 280MB RUNS directory ignored by git (preserved locally)
- Documentation: scientific non-claims maintained, caveats refined

---

## Candidate Tracks

### Track A: Publication-Readiness / Methodology Paper

**Goal:** Transform GeoSpectra Falsification Ladder workflow + v0.1.15 milestone into coherent technical report/preprint outline.

**Deliverables:**
1. Methodology paper outline (Falsification Ladder as scientific workflow)
2. v0.1.15 release narrative (S²×S¹ validation story)
3. Claim ladder (what is validated, what is NOT)
4. Figure/table inventory (from RUNS artifacts)
5. Public README cleanup (communicability for external readers)

**Pros:**
- ✅ Preserves v0.1.15 milestone by documenting it
- ✅ Low computational risk (no new runs)
- ✅ Improves external communicability
- ✅ Falsification Ladder is novel methodological contribution
- ✅ Forces clarity: what exactly was proven vs. tested

**Cons:**
- ⚠️ No new physics result
- ⚠️ Requires narrative synthesis skill (not just code)
- ⚠️ May expose gaps in current interpretation

**Effort estimate:** 2-3 weeks (docs + figure generation)

**Risk level:** LOW — documentation task, no experimental failure risk

---

### Track B: Wilson / Fermion-Doubling Audit

**Goal:** Strengthen Dirac operator / lattice chirality credibility before making stronger chirality-related claims.

**Deliverables:**
1. Wilson term audit spec (do current Dirac operators have Wilson terms?)
2. Fermion-doubling diagnostic (does S²×S¹ exhibit lattice doubling?)
3. Chirality consistency check (are Dirac indices topologically robust under discretization?)
4. Literature review (Wilson fermions, lattice QCD, chiral gauge theories)

**Pros:**
- ✅ Addresses major theoretical risk (lattice artifacts vs. physical chirality)
- ✅ Strengthens credibility of Dirac operator results
- ✅ Preempts skepticism before external review
- ✅ Natural prerequisite for S³×S³ or higher-dimensional product spaces

**Cons:**
- ⚠️ May expose limitations in current Dirac construction
- ⚠️ More technically demanding (lattice field theory)
- ⚠️ Could require Dirac operator redesign if Wilson term missing

**Effort estimate:** 3-4 weeks (literature + spec + diagnostic)

**Risk level:** MEDIUM — may uncover design flaw in Dirac operators

---

### Track C: S²×S² Product Geometry

**Goal:** Extend product-discretized validation to next product manifold after S²×S¹.

**Deliverables:**
1. S²×S² operator construction (D_S2 ⊗ I_S2 + Γ_S2 ⊗ D_S2)
2. Grid design (q1 × q2 × disorder × seeds)
3. Anderson benchmark validation (same protocol as v0.1.15)
4. Failure mode analysis (new caveats?)
5. Baseline promotion to v0.1.17 (if validation passes)

**Pros:**
- ✅ Natural scientific scaling after S²×S¹
- ✅ Tests robustness of product-discretized approach
- ✅ Opens path to S³×S³ and higher products
- ✅ Reuses validated workflow (low methodological risk)

**Cons:**
- ⚠️ Heavier computational load (q1 × q2 grid is larger)
- ⚠️ New operator construction (may introduce new failure modes)
- ⚠️ No theoretical novelty (incremental validation)
- ⚠️ Postpones Wilson audit and publication work

**Effort estimate:** 4-6 weeks (operator + grid + full run + audit)

**Risk level:** MEDIUM — new geometry may fail validation

---

### Track D: Geometric Localization Refinement

**Goal:** Improve dumbbell / variable-radius cylinder geometry branch after null/weak signal in previous milestones.

**Deliverables:**
1. Revisit geometric localization hypothesis (is the signal real?)
2. Refine dumbbell geometry parameters
3. Alternative geometries (torus neck, bottleneck, saddle point)
4. Localization metric comparison (IPR, r-stat, participation entropy)

**Pros:**
- ✅ Explores geometric localization hypothesis (beyond disorder)
- ✅ Could discover novel localization mechanism
- ✅ Uses existing spectral/localization tools

**Cons:**
- ⚠️ **Current signal is weak** (dumbbell_tiny showed minimal geometric effect)
- ⚠️ High risk of low return (null result replay)
- ⚠️ Theoretical mechanism unclear (why would geometry localize without disorder?)
- ⚠️ Diverts effort from validated S²×S¹ → S²×S² scaling path

**Effort estimate:** 3-4 weeks (geometry exploration + diagnostics)

**Risk level:** HIGH — weak signal suggests this may be a dead end

---

## Recommended Priority

### Priority 1: Track A (Publication-Readiness)

**Rationale:**
1. **Preserves milestone:** v0.1.15 validated S²×S¹ with refined caveat — this is a real result worth documenting
2. **Low risk:** documentation task, no experimental failure risk
3. **Communicability:** external readers need clear narrative (current reports are internal audit style)
4. **Falsification Ladder is novel:** methodological contribution beyond toy lab results
5. **Prerequisite for Track B/C:** clear claim ladder helps scope Wilson audit and S²×S² validation

**Immediate next step:** Create methodology paper outline skeleton.

---

### Priority 2: Track B (Wilson / Fermion-Doubling Audit)

**Rationale:**
1. **Theoretical risk mitigation:** lattice chirality is contentious — audit before stronger claims
2. **Credibility prerequisite:** Wilson audit strengthens Dirac operator results before external review
3. **Natural after Track A:** claim ladder (from Track A) clarifies what needs auditing
4. **Preempts skepticism:** reviewer will ask "did you check for Wilson terms?" — answer preemptively

**Defer until:** Track A completes (claim ladder guides audit scope).

---

### Priority 3: Track C (S²×S² Product Geometry)

**Rationale:**
1. **Scientific scaling:** natural next step after S²×S¹ validation
2. **Reuses validated workflow:** low methodological risk
3. **Opens higher products:** S²×S² → S³×S³ → eventual S³×S⁶ path
4. **Computational heavy:** defer until Track A (docs) and Track B (theory) complete

**Defer until:** Tracks A + B complete.

---

### Deprioritized: Track D (Geometric Localization Refinement)

**Rationale:**
1. **Weak signal:** dumbbell_tiny showed minimal geometric localization effect
2. **Unclear mechanism:** theory does not predict strong geometric localization without disorder
3. **High risk of null result:** effort likely better spent on validated S²×S¹ → S²×S² scaling
4. **Can revisit later:** if Track C (S²×S²) discovers geometric effects, revisit Track D

**Action:** Archive geometric localization branch to `parked/` with revival condition: "geometric signal observed in S²×S² or higher products."

---

## Proposed v0.1.16 Scope

### Default Scope: Track A (Publication-Readiness)

**Phase 1: Methodology Paper Outline (1 week)**
- [ ] Falsification Ladder section (workflow description)
- [ ] S²×S¹ validation case study
- [ ] Claim ladder (validated vs. NOT validated)
- [ ] Scientific non-claims section
- [ ] Future work roadmap

**Phase 2: Figure/Table Inventory (1 week)**
- [ ] Extract key figures from RUNS artifacts
- [ ] Lattice-size scaling table (ring/alpha=0)
- [ ] Failure rate comparison (3 families)
- [ ] Anderson localization IPR distributions
- [ ] Production guideline flowchart

**Phase 3: Public README Cleanup (3 days)**
- [ ] External reader perspective (assume no context)
- [ ] What is GeoSpectra Lab? (elevator pitch)
- [ ] What is validated? (claims + non-claims)
- [ ] How to reproduce? (run instructions)
- [ ] How to cite? (if methodology paper published)

**Phase 4: Optional Wilson Audit Spec (3 days, if time permits)**
- [ ] Wilson term definition (lattice QCD context)
- [ ] Current Dirac operator audit (does it have Wilson term?)
- [ ] Fermion-doubling diagnostic spec (how to detect it?)
- [ ] Literature review (Wilson fermions, chiral gauge theories)
- **No implementation yet** — spec only

**Total effort:** 2-3 weeks

**Success criteria:**
- Methodology paper outline complete
- Figure/table inventory extracted
- Public README communicable to external readers
- Optional: Wilson audit spec drafted

---

## Success Criteria

### Roadmap Acceptance
- [ ] ROADMAP_v0.1.16.md created
- [ ] Candidate tracks evaluated (A, B, C, D)
- [ ] Priority ranking justified (A → B → C, D deferred)
- [ ] v0.1.16 scope proposed (Track A default)

### Implementation Readiness
- [ ] No code changes (docs-only milestone)
- [ ] No baseline promotion (v0.1.15 remains current)
- [ ] Next implementation task clearly selected (methodology paper outline)
- [ ] Pytest NOT required (docs-only, no code changes)

### Git State
- [ ] Baseline unchanged: v0.1.15-s2-s1-product-discretized-full
- [ ] Commit: 65b6973 (v0.1.15 release)
- [ ] Tag: v0.1.15-s2-s1-product-discretized-full
- [ ] reports/RUNS/ ignored by git

### Clarity
- [ ] User understands recommended Track A (publication-readiness)
- [ ] User knows Track B (Wilson audit) is next after Track A
- [ ] User knows Track C (S²×S²) is deferred until Track A+B complete
- [ ] User knows Track D (geometric localization) is parked

---

## Scientific Non-Claims

v0.1.16 does **NOT** prove or claim:

1. **Continuum compactification** — all operators remain discretized toys, not continuum limits
2. **S⁶ or S³×S⁶ validation** — only S², S³, S¹, and low-dimensional products tested (S²×S¹ as of v0.1.15)
3. **Standard Model derivation** — no claim of deriving SU(3)×SU(2)×U(1) or fermion generations
4. **Physical chirality proof** — Dirac indices are topological toy counts, not physical chiral fermions
5. **Witten/Lichnerowicz index theorem bypass** — numerical index ≠ rigorous proof; computational shortcuts ≠ theorem
6. **Physical interpretation of localization** — Anderson benchmark is a numerical test, not a physical compactification mechanism
7. **Radion stabilization as physical mechanism** — radion toy model does not address hierarchy problem or moduli stabilization in string theory
8. **Global chiral index as physical observable** — topological invariants computed are discretized toy analogs, not continuum field theory predictions

This is a **numerical validation harness** for discretized operators on compact manifolds. All results are confined to the toy-model regime of covariant compactification hypothesis testing.

---

## Next Steps (After Roadmap Acceptance)

### Immediate (v0.1.16 kick-off)
1. Accept or modify this roadmap
2. If Track A accepted: create `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md`
3. If alternative track preferred: justify and proceed

### Medium-term (after Track A)
1. Track B (Wilson audit spec) — no implementation, spec only
2. Track C (S²×S²) planning — grid design, operator construction spec

### Long-term (v0.1.17+)
1. Implement Track B (Wilson audit) if spec reveals no blockers
2. Implement Track C (S²×S² validation) after Track A+B complete
3. Archive Track D (geometric localization) to `parked/` with revival condition

---

## Alternatives Considered

### Alternative 1: Jump to S²×S² (Track C) immediately
**Rejected:** Premature. v0.1.15 milestone deserves documentation before next validation. Wilson audit (Track B) is theoretical risk mitigation prerequisite.

### Alternative 2: Wilson audit (Track B) first, then Track A
**Rejected:** If Wilson audit reveals design flaw, v0.1.15 interpretation may change. Better to document v0.1.15 as-is (Track A), then audit (Track B), then revise if needed.

### Alternative 3: Geometric localization (Track D) revival
**Rejected:** Weak signal in dumbbell_tiny. No theoretical motivation for strong geometric localization without disorder. High risk of null result.

### Alternative 4: Pause scientific work, focus on tooling/infrastructure
**Rejected:** v0.1.15 is validated milestone worth preserving. Tooling improvements should serve Track A (figure generation, README automation).

---

## Risk Assessment

| Track | Success Probability | Failure Impact | Opportunity Cost |
|-------|---------------------|----------------|------------------|
| A (Publication) | HIGH (>90%) | LOW (docs-only) | LOW (2-3 weeks) |
| B (Wilson audit) | MEDIUM (60-70%) | MEDIUM (may require Dirac redesign) | MEDIUM (3-4 weeks) |
| C (S²×S²) | MEDIUM (70-80%) | MEDIUM (validation may fail) | HIGH (4-6 weeks) |
| D (Geometric) | LOW (30-40%) | LOW (null result acceptable) | HIGH (3-4 weeks, likely wasted) |

**Recommended risk mitigation:**
1. Track A first (low risk, high value)
2. Track B before Track C (preempts theoretical risk)
3. Track D deferred indefinitely (weak signal, unclear mechanism)

---

## Timeline Estimate

**v0.1.16 (Track A):** 2-3 weeks (docs-only)  
**v0.1.17 (Track B spec):** 3-4 weeks (Wilson audit spec, no implementation)  
**v0.1.18 (Track C):** 4-6 weeks (S²×S² validation full run)

**Total to S²×S²:** ~10-13 weeks (assuming Tracks A + B + C sequential)

---

## Open Questions

1. **Should Track A include preprint submission?**  
   - Pro: external review feedback  
   - Con: requires polishing beyond outline stage  
   - **Recommendation:** Outline only for v0.1.16, preprint submission in v0.1.17 (after Wilson audit)

2. **Should Wilson audit (Track B) be full implementation or spec-only?**  
   - **Recommendation:** Spec-only in v0.1.16, implementation in v0.1.17 if spec reveals no blockers

3. **Should S²×S² (Track C) wait for Wilson audit completion?**  
   - **Recommendation:** Yes. If Wilson audit reveals Dirac design flaw, S²×S² validation may be invalid.

4. **Should geometric localization (Track D) be archived to `parked/` or `null_results/`?**  
   - **Recommendation:** `parked/` (not falsified, just weak signal). Revival condition: geometric effect observed in higher products.

---

## Conclusion

**Recommended v0.1.16 track:** Track A (Publication-Readiness / Methodology Paper)

**Rationale:**
- Low risk (docs-only)
- High value (preserves v0.1.15 milestone)
- Prerequisite for Track B (Wilson audit) and Track C (S²×S²)
- Falsification Ladder is novel methodological contribution

**Next action:** Accept or modify this roadmap, then create `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md`.

**Baseline remains:** v0.1.15-s2-s1-product-discretized-full (no promotion until next scientific validation milestone).

---

**Roadmap status:** READY FOR REVIEW  
**Recommended decision:** Accept Track A, defer Tracks B+C, archive Track D to `parked/`.
