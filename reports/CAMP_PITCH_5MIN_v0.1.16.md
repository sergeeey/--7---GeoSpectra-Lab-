# CAMP Meeting 5-Minute Pitch
**Date:** 2026-05-20 (Tuesday 21:30 Almaty / 17:30 UK)  
**Speaker:** Sergey Boyko (Ronin Institute, Independent Researcher)  
**Topic:** GeoSpectra Falsification Ladder — Methodology for Detecting Discretization Artifacts

---

## 🎯 Problem (30 sec)

Finite-lattice spectral operator research faces **validation theater**: green tests that miss production failures.

Example: S²×S¹ product-discretized Dirac operators. Standard tests pass → but small lattices (s1_size=8-32) silently fail at operator ring index alpha=0. No diagnostic catches this until manual inspection.

**Core issue:** post-hoc validation retrofitted to existing code. No systematic falsification protocol.

---

## 🔬 Solution: Falsification Ladder (1 min)

**9-rung methodology** designed failure-mode-first:

| Rung | What It Catches |
|------|-----------------|
| 0-2 | Core gates (Hermiticity, shape, reproducibility) |
| 3-4 | Positive/negative controls (known-good/known-bad inputs) |
| 5 | Progressive profiles (boundary variation sensitivity) |
| 6 | Independent audit (external agent, no session history) |
| 7 | Targeted follow-up (convert failures → production guidelines) |
| 8 | Release integrity (backward compatibility, determinism) |

**Key difference from standard validation:** failures are NOT bugs to hide — they're **data** to extract empirical guidelines from.

---

## 📊 Case Study: S²×S¹ Full Diagnostic (2 min)

**Scope:** 6615 product-discretized Dirac operators on finite lattices (s1_size 8–96).

**Results:**

1. **Core gates (Rungs 0-2):** 100% pass rate (6615/6615)  
   - Hermiticity: exact conjugate transpose check  
   - Shape consistency: validated across all lattice sizes  
   - Reproducibility: zero stochastic drift

2. **Controls (Rungs 3-4):**  
   - Positive (q>0): 5670/5670 passed  
   - Negative (q=0): **0/945 false positives** ← critical: 0% FP rate

3. **Ring/alpha=0 caveat (Rung 7):**  
   - Small lattices (s1_size 8–32): 19.8% failure rate  
   - Large lattices (s1_size ≥64): 0.0% failure rate  
   - **Production guideline derived:** s1_size ≥64 for alpha=0 operators

**Visualization:** [Show Figure 7 — lattice-size scaling plot]

---

## 🚧 Scope Boundaries (1 min)

**8 explicit non-claims** (Table 3 in manuscript):

1. ❌ NOT continuum compactification proof  
2. ❌ NOT S⁶/Calabi-Yau validation  
3. ❌ NOT Standard Model derivation  
4. ❌ NOT physical chirality proof  
5. ❌ NOT Witten index bypass  
6. ❌ NOT physical extra dimensions claim  
7. ❌ NOT hierarchy problem solution  
8. ❌ NOT observable predictions

**What this IS:**  
✅ Methodology paper for finite-lattice toy diagnostics  
✅ S²×S¹ case study (N=1 geometry)  
✅ Proof-of-concept that FL workflow systematically detects discretization artifacts

**Honest limitation:** "Reusable across geometries" NOT yet proven. Track C (S³×S¹, S²×S²) required for statistical support (N≥3).

---

## 🤝 Ask: Technical Review (30 sec)

**Three questions for this group:**

1. **Gaps in 9-rung ladder?** — What failure modes does FL miss?  
2. **Track C geometry recommendations?** — Which S³×S¹ or S²×S² lattice configurations to prioritize?  
3. **Covariant compactification context?** — Does FL align with known constraints from your work?

**Repository:** [https://github.com/sergeeey/--7---GeoSpectra-Lab-.git](https://github.com/sergeeey/--7---GeoSpectra-Lab-.git)  
**DOI:** [10.5281/zenodo.20252651](https://doi.org/10.5281/zenodo.20252651)  
**Manuscript:** 8,950 words, pre-external-review draft (Track A pending)

---

## 📌 Closing (if time permits)

**Why Ronin + independent?** — This work sits between physics, differential geometry, and numerical methods. No institutional home captures all three. Ronin affiliation gives legitimacy without forcing disciplinary boundaries.

**Current status:** Baseline v0.1.15 (computational validation complete). v0.1.16 = methodology manuscript + external review package. Next: Track A (3 domain experts) → Track C (geometry generalization) → arXiv.

**Contact:** sergeikuch80@gmail.com | Ronin Institute Scholar

---

## Backup Slides (if Q&A needs detail)

### Backup 1: Why Falsification-First?

**Standard validation workflow:**  
Requirements → Code → Tests → "All passed" ✅ → Ship

**Problem:** Tests are post-hoc. They validate implementation, not requirements.

**FL workflow:**  
Requirements → Failure modes → Kill criteria → Code → Tests designed to BREAK

**Benefit:** Failures caught earlier = cheaper fixes.

### Backup 2: Ring/Alpha=0 Deep Dive

[Show Figure 7: lattice-size vs failure-rate plot]

**Key observation:**  
- s1_size=8: 19.8% fail  
- s1_size=16: 15.2% fail  
- s1_size=32: 8.1% fail  
- s1_size=64: 0.0% fail  
- s1_size=96: 0.0% fail

**Interpretation:** Small-lattice artifact, NOT fundamental operator flaw. Resolved by production guideline (s1_size≥64).

**Methodological value:** FL converted failure signal → actionable guideline via Rung 7 (targeted follow-up).

### Backup 3: What v0.1.15 Established

✅ **Established (with statistical support):**  
- 9-rung workflow detects discretization artifacts on S²×S¹  
- 0% false positive rate on negative controls  
- Targeted follow-up successfully derives empirical guidelines  
- Workflow is auditable by independent agents (Codex audit passed)

❓ **Open (Track C required):**  
- Generalization to S³×S¹, S²×S², higher-dimensional geometries  
- Operator classes beyond Dirac (Laplacian, d'Alembertian)  
- Continuum limit behavior (requires different mathematical framework)

---

**Total length:** ~5 minutes at normal speaking pace (750-900 words spoken).

**Tone:** Honest, rigorous, inviting critique. No overclaim. Frame as "validated proof-of-concept, seeking technical review before broader claims."
