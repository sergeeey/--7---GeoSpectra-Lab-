# Section 3 (COMPRESSED) — Methods: GeoSpectra Falsification Ladder

**Paper:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"  
**Compressed Draft Date:** 2026-05-17  
**Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Compression:** Sections 3-5 (~12,500 words) → ~3,600 words (71% reduction)

---

## 3.1 Method Overview

GeoSpectra Falsification Ladder is a systematic validation harness for discretized spectral operators on compact manifolds. The workflow treats provisional success as the **starting point for targeted stress tests**, not the endpoint. Each rung represents a validation gate; failure triggers either rejection (null result) or caveat discovery (targeted follow-up). Provisional pass at all rungs constitutes *validated toy behavior on finite lattices within tested parameter ranges*, NOT proof.

**Five design principles:**

1. **Falsification-first:** Design tests to break claims (negative controls as important as positive controls)
2. **Negative controls mandatory:** Zero false positives required—one false positive = gate broken
3. **Progressive profiles:** Tiered diagnostics (smoke → standard → full → targeted) with escalating cost
4. **Caveats as outputs:** Failures discovered, classified, documented as parameter-range limitations (e.g., "ring/alpha=0 requires s1_size ≥ 64")
5. **Independent audit required:** External review of classification + release integrity audit before baseline promotion

---

## 3.2 Ladder Rungs

The Ladder consists of **9 rungs** executed sequentially. Failure at any rung triggers rejection or caveat discovery.

| Rung | Stage | Purpose | Artifact | Failure → |
|------|-------|---------|----------|-----------|
| **1** | Operator Construction | Verify operators construct without crashes, dimensions match expected | None (pre-diagnostic) | REJECT (fix code) |
| **2** | Hermiticity & Shape Gates | Verify H† = H (tolerance 1e-9), dim = dim_S2 × s1_size | Hermiticity residual, shape check | REJECT (design error) |
| **3** | Positive & Negative Controls | W=0 → delocalized (945 cases), q=0 disordered → zero FP (945 cases) | Control pass/fail flags | REJECT (gate broken) |
| **4** | Smoke Profile | 63 cases, 5 min → catch gross errors cheaply | config.json, metrics.json (tiny), summary.md | REJECT (fix code) |
| **5** | Standard Profile | 630 cases, 90 min → detect family-specific bugs, seed sensitivity | config.json, metrics.json (~500 KB), summary.md | PASS_WITH_CAVEATS or reject |
| **6** | Full Profile | 6615 cases, 16 hours → comprehensive parameter sweep, statistical failure structure | config.json, metrics.json (2.8 MB), summary.md, data.npz | PASS_WITH_CAVEATS or reject |
| **7** | Independent Audit | External review of classification, metrics, summary narratives | audit report, corrections list | confirmed_with_corrections |
| **8** | Targeted Follow-Up | Extended grid to test artifact hypothesis (conditional: only if Rung 6 detects caveats) | follow-up metrics.json, lattice-size scaling analysis | ARTIFACT or PERSISTENT_LIMITATION |
| **9** | Release Integrity & Promotion | Cross-file consistency, non-claims verification, artifact completeness | release notes, VALIDATION_STATUS.md | release_integrity_confirmed → promote |

**Sequential requirement:** Rungs 1-9 executed in order. Do NOT skip rungs. Exception: Rung 8 conditional on Rung 6 detecting caveats.

---

## 3.3 Core Gates (Rungs 2-3)

Five gates enforce numerical correctness and control robustness **before** expensive parameter sweeps.

### Gate Specifications

| Gate | Check | Tolerance | Purpose | v0.1.15 Result |
|------|-------|-----------|---------|----------------|
| **Hermiticity** | \|\|H - H†\|\| ≤ 1e-9 | 1e-9 (Frobenius norm) | Non-Hermitian → complex eigenvalues → invalid spectral analysis | 6615/6615 passed ✅ |
| **Shape** | dim(H) == dim_S2 × s1_size | Exact match | Dimension mismatch → localization gates undefined | 6615/6615 passed ✅ |
| **Reproducibility** | Independent re-run → bit-identical checksums | Exact match | Non-reproducible → cannot audit | 6615/6615 matched ✅ |
| **Positive Control** | W=0 (clean) → delocalized | All cases pass | Disorder baseline broken | 945/945 delocalized ✅ |
| **Negative Control** | q=0 disordered → delocalized | Zero FP required | False positives = gate broken | 0/945 FP ✅ |

**Design rationale:**
- **Hermiticity first** (most catastrophic failure: non-Hermitian blocks all downstream)
- **Shape second** (dimension bugs block localization gate computation)
- **Reproducibility third** (enables auditing, but not required for numerical correctness)
- **Controls last** (require localization gates defined, so cannot run before Shape)

**Pass rate:** 100% across all 5 gates (Table 3). Zero false positives. This validates: (1) operator construction correctness, (2) numerical stability, (3) control design robustness. It does NOT validate: continuum limits, S⁶ manifolds, Standard Model, physical chirality.

**Why zero FP is hard requirement:** One false positive means localization gate fires spuriously (harness defect). This invalidates ALL diagnostic results—no further testing until gate is fixed.

---

## 3.4 Progressive Profiles (Rungs 4-6, 8)

Staged escalation from cheap falsifiers (smoke: 5 min) to expensive characterization (full: 16 hours) prevents expensive false confidence.

### Profile Specifications

| Profile | Cases | Runtime | Parameter Coverage | Purpose | Failure Interpretation |
|---------|-------|---------|-------------------|---------|----------------------|
| **Smoke** | 63 | 5 min | 1 family, 3 q, 3 s1_sizes, 1 alpha, 7 W, 1 seed | Catch gross errors (crashes, Hermiticity failures, dimension bugs) | CRITICAL FAILURE → fix code, restart |
| **Standard** | 630 | 90 min | 3 families, 5 q, 5 s1_sizes, 3 alphas, 7 W, 2-3 seeds | Detect family-specific bugs, seed sensitivity, BC-dependence | Family failure >10% → investigate |
| **Full** | 6615 | 16 hours | 3 families, 7 q, 9 s1_sizes, 3 alphas, 7 W, 4 seeds, 3 BCs | Comprehensive sweep, statistical failure structure, rare edge cases | Aggregate <95% → REJECT; clustered failures → targeted follow-up |
| **Targeted** | 1349 | 2.5 hours | Focused grid along suspicious axis (v0.1.15: ring/alpha=0, s1_size=64-96 extended) | Resolve localized caveats, test artifact convergence hypothesis | Failure rate <2% at extended grid → SMALL_LATTICE_ARTIFACT |

**Cost-benefit (v0.1.15):**
- **Naive (no staging):** Full → discover bug → Full again = 32 hours
- **Progressive:** Smoke → Standard → Full → Targeted = 19 hours ✅ (**13 hours saved**)

**What gates cannot replace:** Gates run on few test cases (not full parameter space), return binary pass/fail (not statistical breakdown), find catastrophic bugs (not subtle small-lattice artifacts). Progressive profiles bridge the gap between gates (cheap binary checks) and full understanding (expensive statistical characterization).

---

## 3.5 Artifact Contract

Each profile produces structured artifacts enabling reproducibility and audit:

| Artifact | Content | Purpose |
|----------|---------|---------|
| **config.json** | Full parameter specification (families, q-values, s1_sizes, alphas, W, seeds, BCs) | Reproducibility: exact input for independent re-run |
| **metrics.json** | Per-case results (eigenvalues, IPR, gate flags, failure classifications) | Audit: raw data for external verification |
| **summary.md** | Aggregate statistics (pass rates, failure clustering, Decision Rule verdicts) | Human-readable report |
| **data.npz** | Eigenvalues, eigenstates (optional, storage-intensive) | Deep dive: numerical spectra for follow-up analysis |
| **run_status.json** | Real-time progress (completed/total cases, ETA) | Monitoring: track long-running full profiles |
| **RELEASE_NOTES.md** | Baseline promotion rationale, caveats, production guidelines | Documentation: what changed, what's validated, what's NOT claimed |

**Storage requirements (v0.1.15 full):**
- config.json: ~2 KB
- metrics.json: 2.8 MB (6615 cases × ~430 bytes/case)
- summary.md: ~50 KB
- data.npz: ~1.2 GB (optional, eigenvalues only)
- **Total:** ~3 MB (minimal), ~1.2 GB (with eigenvalues)

---

## 3.6 Decision Labels

Classification system for profile outcomes:

| Label | Meaning | Next Action |
|-------|---------|-------------|
| **PASS** | All gates passed, no caveats detected | Proceed to next rung |
| **PASS_WITH_LOCAL_CAVEATS** | Aggregate pass rate ≥95%, but localized failures detected (e.g., 51/6615 clustered in ring/alpha=0) | Trigger targeted follow-up (Rung 8) |
| **SMALL_LATTICE_ARTIFACT** | Failures vanish at larger grids (Decision Rule 1: failure_rate <2% at s1_size≥64) | Derive production guideline (e.g., "use s1_size≥64 for ring/alpha=0") |
| **PERSISTENT_LIMITATION** | Failures persist at all tested lattice sizes | Document as parameter-range boundary, exclude from production |
| **WINDOW_GATE_ISSUE** | Localization verdict depends on spectral window choice (historical pattern) | Flag for future investigation, NOT counted as hard failure |
| **FAIL_ARTIFACT_DOMINATED** | Aggregate pass rate <95%, failures distributed (not clustered) | REJECT → investigate root cause, do not promote |
| **INCONCLUSIVE** | Insufficient data to classify (e.g., follow-up run incomplete) | Extend follow-up, re-run with more cases |

**v0.1.15 classification chain:**
1. Full profile (Rung 6): **PASS_WITH_LOCAL_CAVEATS** (99.1% passed, 51 clustered failures)
2. Targeted follow-up (Rung 8): **SMALL_LATTICE_ARTIFACT** (0/252 failures at s1_size≥64)
3. Final verdict: **PASS_WITH_REFINED_CAVEAT** (production guideline: s1_size≥64 for ring/alpha=0)

---

## 3.7 Scope of the Method

### What the Method Validates

1. **Discretized toy operator robustness:** Operators construct correctly (Hermiticity, shape), behave consistently across seeds (reproducibility), pass controls (W=0, q=0)
2. **Finite-lattice convergence:** Localized artifacts vanish at sufficiently large finite grids (e.g., s1_size≥64 for ring/alpha=0)
3. **Empirical production guidelines:** Parameter-range thresholds derived from failure-rate analysis (Decision Rule 1: failure_rate <2%), NOT proven theorems
4. **Workflow reusability:** Ladder structure (controls → reproducibility → profiles → audit) applies to any computational toy-model investigation

### What the Method Does NOT Validate

1. **Continuum compactification:** All operators discretized on finite lattices (S²: q≤106, S¹: s1_size≤96). No continuum extrapolation (q→∞, s1_size→∞) performed. Lattice-size scaling shows **discretized operator convergence**, NOT continuum limits.
2. **S⁶ or S³×S⁶ validation:** Only low-dimensional test geometries tested (S², S³, S¹, S²×S¹). No claim that S²×S¹ results extend to higher-dimensional manifolds.
3. **Standard Model derivation:** No gauge group calculation (SU(3)×SU(2)×U(1)), no fermion generations, no particle content.
4. **Physical chirality proof:** Dirac indices are topological toy counts, NOT physical chiral fermions.
5. **Witten/Lichnerowicz bypass:** Numerical eigenvalue decomposition ≠ rigorous Atiyah-Singer index theorem proof.
6. **Physical extra dimensions:** Anderson localization benchmark is numerical disorder test, NOT physical compactification mechanism.
7. **Hierarchy problem solution:** Toy radion model (if used) does NOT address moduli stabilization or cosmological constant problem.
8. **Observable predictions:** Topological invariants and localization metrics are discretized toy analogs, NOT continuum field theory predictions.

*See Table 9.1 for complete list of 8 scientific non-claims with detailed rationales.*

### Methodological vs. Physical Contribution

**This paper validates:** A falsification-first workflow for discretized toy operators on finite lattices. The workflow is **reusable** (applies to finite-element models, lattice field theories, Monte Carlo simulations).

**This paper does NOT validate:** Physical compactification mechanisms, continuum limits, or experimental observables. All operators are **diagnostic constructs**, not physical field theories.

**Key framing:** Lattice-size scaling (Figure 7) shows **discretized operator convergence on finite grids** (failures vanish at s1_size≥64), NOT continuum extrapolation (operators approach continuum Dirac operator). Even s1_size=96 remains a **finite-lattice diagnostic**.

---

## Summary

GeoSpectra Falsification Ladder is a **9-rung sequential validation workflow** for discretized spectral operators:
- **Rungs 1-3:** Gates (Hermiticity, shape, reproducibility, controls) validate operator construction and control robustness (100% pass rate, Table 3)
- **Rungs 4-6:** Progressive profiles (smoke → standard → full) stage falsification from cheap error detection (5 min) to expensive statistical characterization (16 hours)
- **Rung 7:** Independent audit verifies classification correctness (3 corrections applied in v0.1.15)
- **Rung 8:** Targeted follow-up resolves localized caveats (1349 cases confirmed ring/alpha=0 convergence at s1_size≥64)
- **Rung 9:** Release integrity audit verifies cross-file consistency, non-claims preservation, artifact completeness → baseline promotion

**Methodological contribution:** Falsification-first workflow converts failure modes (51 ring/alpha=0 failures) into production guidelines (s1_size≥64 threshold) through targeted follow-up. Caveats are **outputs** (validated parameter-range boundaries), not bugs to patch away.

**Scientific scope:** All validation on **discretized toy operators on finite lattices**. No continuum limits, no S⁶/S³×S⁶, no Standard Model, no physical chirality, no observable predictions (Table 9.1: 8 explicit non-claims).

**Next sections:** Section 4 presents v0.1.15 case study results (full diagnostic, reproducibility, core gates 100% pass rate). Section 5 narrates ring/alpha=0 caveat discovery and resolution (targeted follow-up, lattice-size scaling, production guideline derivation). Section 6 describes independent audit and release integrity protocols.

---

**Compression Notes:**

**Original:** Section 3 (~4,100 words) + Section 4 (~4,500 words) + Section 5 (~3,900 words) = ~12,500 words  
**Compressed:** ~3,600 words (71% reduction)

**Eliminated:**
- Repeated "falsification-first" definitions (covered in Sections 1-2)
- Long prose examples (converted to compact tables)
- Detailed gate derivations (Hermiticity tolerance choice, shape dependency logic)
- Verbose profile narratives (smoke/standard/full descriptions compressed to table)
- V0.1.15 example repetition (quantitative results centralized in Table 3, Table 1 references)

**Preserved:**
- Core methodology logic (9 rungs, sequential execution)
- 5 design principles (falsification-first, negative controls, progressive profiles, caveats as outputs, independent audit)
- Gate specifications (Hermiticity, shape, reproducibility, positive/negative controls)
- Progressive profile ladder (smoke/standard/full/targeted with runtime, case counts, purposes)
- Artifact contract (config.json, metrics.json, summary.md, data.npz)
- Decision labels (PASS, PASS_WITH_CAVEATS, SMALL_LATTICE_ARTIFACT, etc.)
- Scope boundaries (what method validates vs. does NOT validate)
- All 8 scientific non-claims (referenced via Table 9.1, not expanded inline)

**Tables created:**
- Table 3.2: Ladder Rungs (9 rungs, purpose, artifact, failure action)
- Table 3.3: Core Gates (5 gates, specifications, v0.1.15 results)
- Table 3.4: Progressive Profiles (4 profiles, cases, runtime, purpose)
- Table 3.5: Artifact Contract (6 artifact types, content, purpose)
- Table 3.6: Decision Labels (7 labels, meaning, next action)

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)
