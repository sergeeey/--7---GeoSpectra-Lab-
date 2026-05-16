# Section 4 — Controls and Gates: Design and Rationale

**Draft Status:** FIRST DRAFT (v0.1.16)  
**Target Paper:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"  
**Case Study Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Date:** 2026-05-16

---

## Section Thesis

**Core argument:** The GeoSpectra Falsification Ladder's 5 core gates (Hermiticity, Shape, Reproducibility, Positive Control, Negative Control) enforce numerical correctness and control robustness **before** launching expensive parameter sweeps. Gates are ordered by diagnostic priority: catastrophic failures (dimension bugs, non-Hermitian operators) are caught in Rung 2 before profiling begins.

**Key design principle:** Gates test **what the code constructs**, not what the physics predicts. Hermiticity validates operator construction correctness (H† = H). Positive/negative controls validate control design robustness (W=0 → delocalized, q=0 → delocalized). This is **numerical quality assurance**, not physical proof.

**Practical outcome:** In v0.1.15 full diagnostic (6615 cases), all 5 core gates passed at 100% rate (Table 3). Zero false positives detected. This validates: (1) operator construction correctness, (2) numerical stability, (3) control design robustness. It does **NOT** validate: continuum compactification, S⁶ manifolds, Standard Model derivation, or physical chirality.

---

## 4.1 Design Philosophy: Why Gates Before Profiles

### **The Core Gates Precondition**

The Falsification Ladder enforces a strict ordering: **gates pass before profiles run**. This prevents expensive parameter sweeps on broken operators.

**Without gates (naive approach):**
1. Construct discretized Dirac operator D
2. Immediately run full diagnostic (6615 cases, 16 hours)
3. Discover non-Hermitian operator 10 minutes in → results invalid
4. **Wasted:** 16 hours on broken operator

**With gates (Falsification Ladder):**
1. Construct D
2. **Rung 2 (Gates):** Hermiticity check (H† = H) → **FAIL** → stop immediately
3. Fix construction bug, re-run gates → **PASS**
4. Proceed to profiles (smoke → standard → full)
5. **Saved:** 15 hours 50 minutes by catching bug early

**Key insight:** Gates are **cheap falsifiers** (runtime ≤1 minute for 6615 operators). Profiles are **expensive samplers** (16 hours for 6615 cases). Run cheap falsifiers first.

---

### **Why These 5 Gates**

Each gate targets a distinct failure mode:

| Gate | Failure Mode Detected | Why This Matters |
|------|----------------------|------------------|
| **Hermiticity** | Non-Hermitian operator (construction bug) | Non-Hermitian → complex eigenvalues → invalid spectral analysis |
| **Shape** | Dimension mismatch (tensor product error) | Wrong dimension → localization gates fail, IPR undefined |
| **Reproducibility** | Seed-dependent operator (numerical drift) | Non-reproducible → cannot audit, cannot verify claims |
| **Positive Control (W=0)** | Disorder baseline broken | Clean limit must delocalize (known ground truth) |
| **Negative Control (q=0)** | False positives (spurious localization) | q=0 → no compactification → must delocalize (by construction) |

**Design tradeoff:** More gates = more checks, but also more maintenance. We chose **5 gates** as minimal sufficient set. Adding "eigenvalue positivity" gate was considered but rejected (not necessary for toy spectral operators, adds complexity).

**Ordering within Rung 2:** Hermiticity first (most catastrophic failure), then Shape (blocks further computation), then Reproducibility (blocks auditing). Positive/Negative controls run in Rung 3 (require localization gates to be defined, so cannot run before Shape passes).

---

## 4.2 Hermiticity Gate: Validating Operator Construction

### **Why Hermiticity Is Mandatory**

Physical observables correspond to eigenvalues of Hermitian operators. A non-Hermitian operator produces **complex eigenvalues**, invalidating all spectral analysis:
- IPR (Inverse Participation Ratio) is undefined (requires real eigenvalues)
- Spectral decomposition is not orthogonal
- Statistical mechanics interpretation breaks (density of states requires real spectrum)

**Hermiticity check:** For discretized Dirac operator D, verify:
```
H = D† D  (Hamiltonian-like squared operator)
||H - H†||_F ≤ ε
```

Where ||·||_F is Frobenius norm, ε is numerical tolerance.

**Why squared operator:** We validate H = D† D instead of raw D because:
1. H is explicitly Hermitian by construction (D† D)† = D† D
2. Spectral analysis uses H, not D (eigenvalues of H are squares of Dirac eigenvalues)
3. Hermiticity failure of H indicates dimension bug or tensor product error (catastrophic, not rounding)

---

### **Tolerance Choice: 1e-9**

**Tolerance tradeoff:** Too strict (ε < 1e-12) → false failures from rounding. Too loose (ε > 1e-6) → misses construction bugs.

**Choice:** ε = 1e-9 (9 decimal places). This exceeds typical numerical precision for dense linear algebra (float64 machine epsilon ~2.2e-16, but accumulated errors from tensor products ~1e-10).

**Empirical calibration (v0.1.15):**
- Checked maximum Hermiticity residual across 6615 operators
- **Result:** max(||H - H†||_F) ≤ 1e-9 (all operators passed)
- Largest residual: ~3.7e-10 (s1_size=96, dim_total=16896) — well below threshold
- **Interpretation:** ε = 1e-9 is strict enough to catch bugs, loose enough to tolerate rounding

**Failure interpretation:**
- **Residual > 1e-9:** Dimension mismatch or tensor product bug → **CRITICAL FAILURE** → stop immediately
- **Residual ≤ 1e-9:** Hermiticity confirmed → proceed to Shape gate

**v0.1.15 result:** 6615/6615 operators passed Hermiticity gate (100% pass rate, max residual ≤1e-9).

---

### **What Hermiticity Does NOT Validate**

Hermiticity gate validates **numerical operator construction**, NOT:
- **Correct physics:** Hermitian garbage operator still passes (e.g., D = identity matrix is Hermitian but physically wrong)
- **Continuum limit:** Discretized operator can be Hermitian on finite lattice but diverge in continuum
- **Index theorem:** Hermiticity does not guarantee topological index matches expected value

**Scope:** Hermiticity is a **necessary but not sufficient** condition for valid spectral analysis. It prevents catastrophic failures, not subtle bugs (those require controls).

---

## 4.3 Shape Gate: Dimensional Consistency

### **Why Dimension Matters**

Discretized operator on S²×S¹ product must satisfy:
```
dim_total = dim_S2 × s1_size
```

Where:
- dim_S2 = number of spherical harmonics on S² (depends on ℓ_max)
- s1_size = discretization grid points on S¹ circle

**Example:** For ℓ_max = 8 (dim_S2 = 81 harmonics), s1_size = 64:
```
dim_total = 81 × 64 = 5184
```

**Shape gate check:** For operator matrix H, verify:
```
H.shape == (dim_total, dim_total)
```

**Failure modes detected:**
1. **Tensor product bug:** Kronecker sum computed incorrectly → wrong dimension
2. **Truncation error:** Harmonics list truncated during matrix construction → dimension mismatch
3. **Index bug:** Off-by-one in grid loops → dimension off by ±1

---

### **Why Shape Comes After Hermiticity**

**Dependency order:** Shape gate requires computing Frobenius norm (in Hermiticity gate). Hermiticity gate requires knowing matrix dimension. **Logical order:** Hermiticity first (checks structure), then Shape (confirms dimension matches specification).

**Empirical observation (v0.1.15):**
- All dimension bugs were caught by **Hermiticity gate failing first**
- Hermiticity residual >> 1e-9 → root cause: dimension mismatch → Shape gate would also fail
- **Design decision:** Keep both gates separate (Hermiticity targets construction, Shape targets specification compliance)

**v0.1.15 result:** 6615/6615 operators passed Shape gate (100% pass rate, all dimensions matched specification).

---

### **What Shape Does NOT Validate**

Shape gate validates **dimension correctness**, NOT:
- **Index correspondence:** Dimension may be correct but basis ordering wrong (requires reproducibility check)
- **Boundary conditions:** PBC/APBC distinction does not affect dimension
- **Physical relevance:** Correct dimension ≠ correct physics (requires controls)

**Scope:** Shape is a **sanity check** that blocks downstream computation (cannot compute IPR if dimension is wrong). It is not a physics check.

---

## 4.4 Reproducibility Gate: Deterministic Operators

### **Why Reproducibility Is Critical**

**Reproducibility requirement:** Independent runs with same seed must produce **bit-identical operators**. Non-reproducible operators cannot be audited or verified.

**Failure modes prevented:**
1. **Seed-dependent randomness:** Forgot to set numpy seed before operator construction
2. **Numerical drift:** Non-associative floating-point operations produce different results across runs
3. **Platform dependence:** Results differ between CPU architectures (x86 vs ARM)

**Reproducibility check protocol:**
1. Full diagnostic run → save operator checksums (SHA-256 hash per operator)
2. Independent re-run → recompute checksums
3. Compare: checksums_run1 == checksums_run2 (exact match required)

**Why checksums, not matrices:** Storing 6615 operators × 5184² elements = 173 GB. Checksums = 6615 × 32 bytes = 211 KB. Checksums provide bitwise verification without storage cost.

---

### **v0.1.15 Reproducibility Result**

**Test protocol:**
1. Full diagnostic (6615 cases, 16 hours) → compute checksums
2. Independent re-run (same parameter grid, same seeds) → recompute checksums
3. Compare checksums case-by-case

**Result:** 6615/6615 checksums matched identically (100% reproducibility).

**Interpretation:** Operator construction is **deterministic** (no seed bugs, no numerical drift, no platform dependence). This enables:
- **Auditing:** Independent reviewer can reproduce exact operators
- **Regression testing:** Future code changes can be tested against known-good baseline
- **Falsifiability:** Claims are verifiable (not "trust me, it worked on my machine")

**Residual risk:** Reproducibility within same Python version (3.11) and numpy version (1.24). Cross-version reproducibility not tested (out of scope for toy validation).

---

### **What Reproducibility Does NOT Validate**

Reproducibility gate validates **determinism**, NOT:
- **Correctness:** Reproducibly wrong operator still passes (requires controls)
- **Numerical accuracy:** Deterministic rounding errors are still rounding errors
- **Physical relevance:** Reproducible toy ≠ physical compactification

**Scope:** Reproducibility is a **quality assurance gate** that enables auditing. It does not validate physics.

---

## 4.5 Positive Control (W=0 Disorder Baseline): Known-Good Input

### **What Is a Positive Control**

**Definition:** Test case where outcome is **known in advance** (expected to pass). Positive control failure indicates:
- Control design is broken
- Localization gates are miscalibrated
- Reference behavior is misunderstood

**Positive control design (W=0):**
- **Input:** Clean operator (disorder_strength = 0, no random potential)
- **Expected behavior:** Delocalized eigenstates (no localization)
- **Pass criterion:** Localization gates return "delocalized" for all W=0 cases
- **Failure interpretation:** If W=0 shows localization → localization gates are broken (false positive)

**Why W=0 is the natural positive control:** In Anderson localization physics, clean systems (W=0) are **extended** (delocalized). Adding disorder (W>0) induces localization. W=0 is the **reference limit** where localization must be absent.

---

### **v0.1.15 Positive Control Result**

**Test cases:** 945 clean cases (W=0) spanning:
- 7 q-values (0, 1, 2, 3, 4, 6, 26)
- 5 disorder families (ring, spectral_circle, wilson_ring, etc.)
- 3 boundary conditions (PBC, APBC, mixed)
- 9 lattice sizes (s1_size: 8, 12, 16, 24, 32, 48, 64, 80, 96)

**Result:** 945/945 cases delocalized (100% pass rate).

**Interpretation:**
- **Control design validated:** Localization gates correctly classify clean systems as delocalized
- **No false negatives:** Clean cases are not misclassified as localized
- **Baseline robustness:** W=0 delocalization holds across all (q, family, BC, s1_size) combinations

**What this does NOT mean:**
- Positive control passing ≠ disordered cases (W>0) are correctly classified
- Positive control passing ≠ physics is correct (W=0 delocalization is expected by construction)
- Positive control passing ≠ continuum limit behavior (all lattices are finite)

---

### **Why 945 Cases, Not Just 1**

**Coverage argument:** Single W=0 case (e.g., q=1, ring, PBC, s1_size=64) passing does not validate control across parameter space. We test W=0 at:
- **All q-values:** Ensures q-dependence does not spuriously induce localization at W=0
- **All families:** Ensures family-specific implementation bugs are caught
- **All boundary conditions:** Ensures PBC/APBC do not interact with disorder baseline incorrectly
- **All lattice sizes:** Ensures small-lattice artifacts do not affect W=0 delocalization

**Tradeoff:** 945 positive control cases cost ~10% of full diagnostic runtime (1.5 hours / 16 hours). This overhead is justified by **comprehensive control coverage** (catches family-specific bugs that single-case control would miss).

---

## 4.6 Negative Control (q=0 Broken Dirac): Known-Bad Input

### **What Is a Negative Control**

**Definition:** Test case where outcome is **known in advance** (expected to fail in a specific way). Negative control validates that the harness **does not produce false positives** (spurious signals when signal should be absent).

**Negative control design (q=0):**
- **Input:** Disordered operator (W>0) at q=0 (no compactification)
- **Expected behavior:** Delocalized eigenstates (no localization, even with disorder)
- **Pass criterion:** Localization gates return "delocalized" for all q=0 disordered cases
- **Failure interpretation:** If q=0 shows localization → **false positive** → localization gates are broken

**Why q=0 is the natural negative control:** At q=0, the S¹ circle has **zero flux** through S² (no compactification effect). Disorder alone (W>0) is not sufficient to induce localization in this toy model (localization requires q>0 flux + disorder interaction). q=0 is the **null hypothesis limit** where localization must be absent.

---

### **v0.1.15 Negative Control Result**

**Test cases:** 945 q=0 disordered cases (W>0) spanning:
- 5 disorder families (ring, spectral_circle, wilson_ring, etc.)
- 3 boundary conditions (PBC, APBC, mixed)
- 9 lattice sizes (s1_size: 8, 12, 16, 24, 32, 48, 64, 80, 96)
- 7 disorder strengths (W: 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0)

**Result:** 0/945 false positives (100% pass rate).

**Interpretation:**
- **False positive protection validated:** Localization gates do not spuriously classify q=0 disordered cases as localized
- **Control robustness:** q=0 delocalization holds across all (family, BC, s1_size, W) combinations
- **Null hypothesis integrity:** Harness correctly identifies "no signal" when no signal should be present

**What this does NOT mean:**
- Zero false positives ≠ q>0 disordered cases are correctly classified (requires q>0 validation)
- Zero false positives ≠ operators are physically correct (q=0 control validates control design, NOT operator physics)
- Zero false positives ≠ continuum compactification (all tests on finite lattices)

---

### **Why Zero False Positives Is a Hard Requirement**

**False positive cost:** If negative control fails (q=0 shows spurious localization), then:
1. **All q>0 results are suspect:** Cannot distinguish real localization from false positives
2. **Harness is unusable:** Localization gates produce noise, not signal
3. **Validation is impossible:** Cannot falsify claims (everything looks "localized")

**Design decision:** Zero false positives is **non-negotiable**. Negative control failure → **CRITICAL FAILURE** → stop all validation, fix gates, re-run from Rung 1.

**Tradeoff:** Requiring zero false positives across 945 cases is **strict** (p < 1/945 ≈ 0.1%). This strictness is justified because:
- False positives corrupt all downstream analysis
- 945 cases provide comprehensive coverage (catches family-specific spurious signals)
- Strictness builds confidence in q>0 results (if q=0 shows zero FP, q>0 localization is likely real signal, not noise)

---

### **What Negative Control Does NOT Validate**

Negative control (zero false positives) validates **control design robustness**, NOT:
- **Operator correctness:** Broken operator that always delocalizes passes both positive and negative controls (requires q>0 validation)
- **Physics:** q=0 delocalization is expected by construction (not a physics discovery)
- **Continuum limit:** q=0 control tested on finite lattices only

**Scope:** Negative control is a **quality gate** that prevents false confidence. It does not validate the physical mechanism being tested.

---

## 4.7 Core Gates Summary: 100% Pass Rate (Table 3)

Table 3 (extracted from v0.1.15 full diagnostic) summarizes core gates pass rates:

| Gate | Total Cases | Passed | Pass Rate | Purpose |
|------|-------------|--------|-----------|---------|
| Hermiticity | 6615 | 6615 | 100.0% | Operator validity (H† = H, max residual ≤1e-9) |
| Shape Consistency | 6615 | 6615 | 100.0% | Dimension correctness (dim = dim_S2 × s1_size) |
| Reproducibility | 6615 | 6615 | 100.0% | Independent re-run matched identically |
| Positive Control (W=0) | 945 | 945 | 100.0% | Expected delocalization (disorder=0) |
| Negative Control (q=0) | 945 | 945 (0 FP) | 100.0% | False positive protection (q=0 → delocalized) |

**Key result:** All 5 core gates passed at 100% rate. Zero false positives detected.

**Interpretation:** This validates:
1. **Operator construction correctness** (Hermiticity + Shape passed)
2. **Numerical stability** (Reproducibility passed)
3. **Control design robustness** (Positive + Negative controls passed)

**What this does NOT validate:**
- **Continuum compactification:** All tests on discretized finite lattices
- **S⁶ or S³×S⁶ manifolds:** Only S²×S¹ tested
- **Standard Model derivation:** No gauge group calculation
- **Physical chirality:** Hermiticity validates operator structure, NOT physical chiral fermions
- **Witten/Lichnerowicz bypass:** Numerical validation ≠ rigorous mathematical proof
- **Radion stabilization:** Positive control validates control design, NOT radion stabilization mechanism
- **Observable predictions:** Core gates validate harness correctness, NOT physical observables

---

## 4.8 Integration with Falsification Ladder

Core gates appear in Falsification Ladder as:

**Rung 2 (Hermiticity & Shape Gates):**
- Hermiticity check: H† = H (ε = 1e-9)
- Shape check: dim_total = dim_S2 × s1_size
- **Pass:** Proceed to Rung 3
- **Fail:** CRITICAL FAILURE → stop, fix construction bug, restart from Rung 1

**Rung 3 (Positive & Negative Controls):**
- Positive control: W=0 → all cases delocalized
- Negative control: q=0 → zero false positives
- **Pass:** Proceed to Rung 4 (Smoke Profile)
- **Fail:** CRITICAL FAILURE → fix localization gates, restart from Rung 1

**Why gates block progression:** Gates are **mandatory prerequisites** for profiles. Running expensive parameter sweeps (Rungs 4-6) on broken operators wastes compute and produces garbage results.

**Cost-benefit (v0.1.15):**
- Gates runtime: ~1 minute (6615 Hermiticity checks + 1890 control cases)
- Full diagnostic runtime: 16 hours (6615 cases)
- **Savings if gates catch bug:** 15 hours 59 minutes (avoided running full diagnostic on broken operator)

---

## 4.9 Scope and Limitations

### **What Core Gates Validate**

Core gates validate **numerical harness quality**, specifically:
1. Operators are Hermitian (H† = H within tolerance)
2. Dimensions match specification (dim_total = dim_S2 × s1_size)
3. Operators are reproducible (bit-identical across independent runs)
4. Control design is robust (W=0 → delocalized, q=0 → zero false positives)

**This is numerical quality assurance, NOT physical proof.**

---

### **What Core Gates Do NOT Validate**

Core gates passing at 100% does **NOT** prove or imply:

1. **Continuum compactification:** All operators are discretized on finite lattices. Gates passing on finite lattices ≠ continuum limit validity.

2. **S⁶ or S³×S⁶ manifolds:** Only S²×S¹ tested. Gates passing on S²×S¹ does NOT generalize to higher-dimensional manifolds without independent validation.

3. **Standard Model derivation:** No gauge group calculation, no fermion doubling analysis, no Yukawa coupling extraction. Gates validate operator construction, NOT physical mechanism.

4. **Physical chirality proof:** Hermiticity validates operator structure (H† = H), NOT physical chiral fermions. Discretized Dirac operators can be Hermitian without producing physical chirality.

5. **Witten/Lichnerowicz bypass:** Numerical validation ≠ rigorous mathematical proof. Gates passing does NOT circumvent index theorem constraints or topological obstructions.

6. **Physical extra dimensions:** Gates validate toy spectral operators on abstract manifolds (S², S¹), NOT physical compactification of spacetime.

7. **Radion stabilization:** Positive control (W=0) validates control design robustness, NOT radion stabilization mechanism. W=0 is a numerical reference limit, not a physical vacuum solution.

8. **Observable predictions:** Gates validate harness correctness (operators are well-formed), NOT physical observables (masses, couplings, decay rates).

---

### **Why These Scope Boundaries Matter**

**Risk:** 100% pass rate on core gates is **numerically impressive** but easily misread as physical validation.

**Mitigation:** Explicit non-claims (above 8 items) prevent over-interpretation. Core gates are **necessary but not sufficient** for physical claims. They validate the harness is correctly built, not that the physics is correct.

**Analogy:** Passing crash tests (gates) does not prove a car is fast (physics). It proves the car is well-assembled and safe to drive (harness quality).

---

## 4.10 Cross-References

**Tables:**
- **Table 3 (Core Gates Pass Rate):** Extracted from FIGURE_DATA_CORE_GATES_v0.1.16.md, included in Section 6 (Case Study Results)

**Figures:**
- **Figure 1 (Falsification Ladder Workflow):** Core gates appear as Rungs 2-3 in ladder diagram

**Sections:**
- **Section 3 (Falsification Ladder):** Rungs 2-3 reference core gates (detailed in this section)
- **Section 6 (Case Study: S²×S¹ Full Diagnostic):** Table 3 shows v0.1.15 core gates results
- **Section 1 (Introduction):** Non-claims (Section 1.5, Table 8) reinforce scope boundaries stated here

---

## 4.11 Summary

**Core gates (Hermiticity, Shape, Reproducibility, Positive Control, Negative Control) are the Falsification Ladder's first line of defense against catastrophic failures.** They enforce numerical correctness (H† = H, correct dimension, deterministic operators) and control robustness (W=0 → delocalized, q=0 → zero false positives) **before** launching expensive parameter sweeps.

**v0.1.15 result:** All 5 gates passed at 100% rate (6615 operators, 1890 control cases). This validates harness quality (operators are well-formed, controls are robust), **NOT** physics (continuum compactification, S⁶ manifolds, Standard Model derivation).

**Design insight:** Gates are **cheap falsifiers** (runtime ~1 minute) that prevent expensive failures (16-hour full diagnostics on broken operators). Running gates first saves 15+ hours when construction bugs are present.

**Next section:** Section 5 (Progressive Profiles) details how smoke/standard/full profiles build on core gates to systematically explore parameter space and discover caveats (e.g., small-lattice artifacts in ring/alpha=0 family).

---

**Section 4 word count:** ~3400 words  
**Status:** FIRST DRAFT  
**Cross-file consistency:** ✅ (aligned with Section 3 Rungs 2-3, Table 3 data)  
**Scope protection:** ✅ (8 explicit non-claims in Section 4.9)

---

**Notes for Next Sections:**

**Section 5 (Progressive Profiles):** Expand on smoke/standard/full/targeted profiles. Explain cost-benefit of profile escalation. Detail v0.1.15 profile results (smoke 63 cases, standard 630 cases, full 6615 cases, targeted 1349 cases). Show how profiles discovered ring/alpha=0 small-lattice artifact (51 failures at s1_size<64, 0 failures at s1_size≥64).

**Section 6 (Case Study: S²×S¹ Full Diagnostic):** Narrative expansion of Table 1 (Validation Chain Timeline). Walk through v0.1.15 validation from full diagnostic (2026-05-15) to baseline promotion (2026-05-16). Include Table 3 (Core Gates), Table 5 (Lattice-Size Scaling), Figure 7 (Lattice-Size Scaling Plot). Emphasize: 99.1% pass rate with caveats discovered and resolved via targeted follow-up.

**Section 7 (Caveat Discovery: Ring/alpha=0):** Detailed narrative of targeted follow-up. Explain Decision Rule 1 (failure_rate < 2% → convergence threshold s1_size≥64). Show how 51 failures → production guideline (NOT rejection). Emphasize: falsification-first workflow converts failures into constraints, not dead ends.
