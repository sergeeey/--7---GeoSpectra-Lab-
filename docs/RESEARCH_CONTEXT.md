# Research Context

## Scientific Motivation

GeoSpectra Lab is an independent computational project focused on **falsification-first validation** of finite-lattice spectral toy geometries.

The broader research question:

> Can compact product geometries support localization-like spectral signals that are robust against disorder, discretization family, finite-size scaling, and artifact tests?

This question appears in multiple research contexts:

1. **Kaluza-Klein compactification** (historical framework, 1920s–present)
2. **Lattice field theory** (computational QFT, contemporary)
3. **Covariant compactification** (geometric approaches to extra dimensions)
4. **Anderson localization on curved spaces** (condensed matter physics)

GeoSpectra focuses on the **computational/numerical validation side**: falsification-first testing of finite-lattice toy geometries with explicit artifact controls.

---

## Inspiration and Attribution

This project was initially inspired by broader questions in compact product geometries, Kaluza–Klein-style reasoning, and geometric approaches to extra-dimensional compactification, including public work by **Tom Lawrence** on product manifolds and covariant compactification.

**Key distinction:**

GeoSpectra does **not** test or validate covariant compactification directly. It does **not** claim evidence for physical compactification, Standard Model structure, chirality, gauge-field derivation, or a thermodynamic/continuum limit.

Instead, the project asks a **narrower computational question**:

> Can a finite-lattice spectral validation harness distinguish a robust localization-like signal on a compact product toy geometry from artifacts of disorder strength, matrix sparsity, operator family, seed choice, spectral tails, metric handling, or geometry scrambling?

---

## What GeoSpectra Studies

### Current case study: S³×S¹

- **Geometry:** S³×S¹ finite-lattice toy geometry (N ≤ 896)
- **Disorder:** Anderson-style diagonal disorder (on-site U(r) ∈ [-W, W])
- **Main diagnostic:** True eigenvector-based IPR (inverse participation ratio)
- **Secondary diagnostic:** Adjacent gap ratio / r-statistic
- **Current milestone:** Gate 4B v0.1.21 — `GATE4B_FSS_PASS_WITH_CAVEATS`
- **Active validation branch:** v0.1.22 Negative Controls (artifact falsification)

### Why S³×S¹?

- **S³:** Simplest non-trivial compact 3-manifold
- **S¹:** Simplest compactification target
- **Product geometry:** Tests separability vs coupling
- **Finite lattice:** Computationally tractable (hours, not weeks)

---

## What GeoSpectra Does NOT Study

GeoSpectra does **not** study:

- Physical extra dimensions
- Thermodynamic limit (N → ∞)
- Continuum field theory
- Standard Model gauge group derivation
- Real cosmology or physical stabilization
- Chiral fermion construction (beyond toy index controls)
- Witten/Lichnerowicz no-go theorem bypass

**All results are finite-lattice, toy-model, computational.**

---

## Falsification-First Methodology

GeoSpectra uses a **falsification-first** validation harness:

1. **Pre-registration:** Define protocol before execution
2. **Negative controls:** Test if broken/random/scrambled baselines reproduce signal
3. **Artifact zoo:** Systematically test known failure modes
4. **Null results logging:** Failed hypotheses are first-class results
5. **Explicit claim boundaries:** Document what can/cannot be claimed

**Example (v0.1.22):**

Negative controls protocol:
- Random Hermitian baseline
- Scrambled geometry (broken S³×S¹ structure)
- Broken Wilson term

**Expected outcome:** Controls should fail (NOT reproduce Gate 4B robustness).  
**Danger result:** If ANY control shows Gate 4B-like pattern → harness lacks specificity.

---

## Computational Resources

Some planned experiments require larger computational resources than currently available on local hardware. Heavy runs are being executed remotely where possible (Google Colab, cloud instances, or university clusters).

Current bottleneck: Local thermal constraint prevents extended batch execution.

---

## Relationship to Other Work

### Independence Statement

GeoSpectra Lab was **independently developed** by Sergey Boyko.

Any errors, interpretations, numerical models, or claims in GeoSpectra are **entirely my own**.

GeoSpectra is **not affiliated with, endorsed by, or reviewed by** Tom Lawrence or any other researcher unless explicitly stated otherwise.

### Attribution Scope

The research direction was **partly inspired** by public work on compact product manifolds and covariant compactification by Tom Lawrence.

This inspiration pertains to:
- The choice of compact product geometries (S³×S¹, S²×S¹) as test cases
- The general question of spectral structure on compact products
- The motivation to explore finite-lattice toy models

This inspiration does **not** imply:
- Tom Lawrence endorses this project
- GeoSpectra validates his theory
- Tom Lawrence has reviewed the code or results
- Any affiliation or collaboration

---

## How This Work Differs

| Aspect | Covariant Compactification (conceptual) | GeoSpectra Lab (computational) |
|--------|----------------------------------------|-------------------------------|
| **Goal** | Theoretical framework for physical compactification | Finite-lattice validation harness |
| **Scope** | Continuum field theory, physical extra dimensions | Toy numerical operators (N ≤ 896) |
| **Claims** | Geometric approach to Standard Model | No physics claims; numerical robustness only |
| **Method** | Analytical/geometric reasoning | Falsification-first computational testing |
| **Outcome** | Conceptual framework | Pass/fail verdicts on toy diagnostics |

**GeoSpectra is a validation tool, not a physics theory.**

---

## Research Timeline

| Milestone | Date | Status |
|-----------|------|--------|
| v0.1.15 — S²×S¹ full diagnostic | 2026-05-15 | ✅ COMPLETED |
| v0.1.21 — Gate 4B metric-corrected S³×S¹ FSS | 2026-05-22 | ✅ COMPLETED |
| v0.1.22 — Negative controls planning | 2026-05-22 | ✅ PRE-REGISTERED |
| v0.1.22 — Negative controls execution | pending | 🔄 batches 1-2 done, 3-6 remote |
| Gate 5 — Extended FSS (s1_size=256/512) | future | 📋 PLANNED |
| Cross-geometry transfer (T⁴ null baseline) | future | 📋 PLANNED |

---

## Further Reading

### Project Documentation

- `README.md` — Quick overview, current validation status
- `docs/ROADMAP.md` — Detailed research plan
- `docs/CLAIMS_AND_CAVEATS.md` — Explicit claim boundaries
- `reports/VALIDATION_STATUS.md` — Authoritative validation state
- `reports/NULL_RESULTS.md` — Failed hypotheses and null results
- `reports/DISCOVERY_LEDGER.md` — Unexpected observations

### External References

For background on covariant compactification and related geometric approaches:

- Tom Lawrence's public work on product manifolds and covariant compactification (search: "Tom Lawrence covariant compactification")

For falsification-first methodology:

- Popper, K. (1959). *The Logic of Scientific Discovery*
- Platt, J. R. (1964). "Strong Inference." *Science*

For Anderson localization and spectral diagnostics:

- Anderson, P. W. (1958). "Absence of Diffusion in Certain Random Lattices." *Physical Review*
- Oganesyan, V., & Huse, D. A. (2007). "Localization of interacting fermions at high temperature." *Physical Review B*

---

**Last updated:** 2026-05-24  
**Author:** Sergey Boyko  
**Contact:** sergeikuch80@gmail.com
