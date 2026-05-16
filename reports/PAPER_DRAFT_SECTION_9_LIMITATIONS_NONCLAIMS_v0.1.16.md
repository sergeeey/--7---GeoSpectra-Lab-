# Section 9 — Limitations and Scientific Non-Claims

**v0.1.16 Methodology Paper**  
**Date:** 2026-05-16  
**Baseline:** v0.1.15-s2-s1-product-discretized-full

---

## Section Thesis

This paper documents and validates a **falsification-first workflow for finite-lattice discretized operators** on low-dimensional test geometries. It does **NOT** prove or claim physical compactification, continuum limits, Standard Model derivation, or observable predictions.

The v0.1.15 case study demonstrates that:
- Falsification-first methodology catches localized failure modes (ring/alpha=0 fragility)
- Progressive profile analysis enables targeted diagnostic refinement
- Independent audit verifies documentation-artifact consistency
- Caveat discovery workflows prevent scope inflation

These methodological advances are **reusable across operator classes and geometries**, but v0.1.15 results remain confined to **S²×S¹ product-discretized toy operators on finite lattices**. No extrapolation to physical compactification spaces (S⁶, Calabi-Yau), gauge theories (Standard Model), or experimental observables is validated or claimed.

This section collects all scope boundaries in one place to prevent misinterpretation of toy diagnostics as physical proofs.

---

## 9.1 Toy-Model Scope

### 9.1.1 S²×S¹ as Diagnostic Test Geometry

S²×S¹ (2-sphere × circle) is a **pedagogical toy geometry** chosen for three engineering reasons:

1. **Low-dimensional:** S² (2D) and S¹ (1D) are computationally tractable — eigenvalue decomposition of N×N operators scales as O(N³), limiting practical lattice sizes to N≲10⁴. Higher-dimensional manifolds (S⁶: 6D, S³×S⁶: 9D) require exponentially larger operator matrices.

2. **Analytically controlled:** S² monopole harmonics have known Dirac index (q for monopole charge q) and well-studied spectral properties. This provides a **falsifiable control** — if S² index fails, S²×S¹ construction is invalid.

3. **Product-discretization test case:** S²×S¹ tests Kronecker-sum operator construction (D_S2 ⊗ I_S1 + Γ_S2 ⊗ P_S1) before attempting higher-dimensional products (S²×S², S³×S³). If product discretization fails on S²×S¹, it will fail on more complex geometries.

**What S²×S¹ does NOT represent:**

- ❌ **Not Calabi-Yau compactification:** Calabi-Yau manifolds have nontrivial topology (Hodge numbers h^(1,1), h^(2,1)), Ricci-flat metrics, and complex structure moduli. S²×S¹ has trivial topology (b₁=1, b₂=0) and constant curvature.

- ❌ **Not Kaluza-Klein S³×S⁶:** The 11-dimensional M-theory target space is S³×S⁶ or S⁷×S⁴, not S²×S¹. Even if S²×S¹ operators converge, this provides no evidence about S⁶ or S³×S⁶ behavior.

- ❌ **Not physical extra dimensions:** S²×S¹ is a **test manifold**, not a candidate for physical compactification. Anderson localization on S²×S¹ is a **numerical quality check** (does disorder induce localization as expected?), not evidence for physical extra dimensions.

**Result:** S²×S¹ is a **diagnostic toy geometry**. Success on S²×S¹ validates the falsification-first workflow, NOT the physics of compactification.

### 9.1.2 Product-Discretized Operators as Diagnostic Constructs

The operators tested in v0.1.15 are **Kronecker-sum constructs**:

```
D_S2×S1 = D_S2(q) ⊗ I_S1 + Γ_S2 ⊗ P_S1(alpha, W)
```

where:
- `D_S2(q)`: S² monopole Dirac operator (finite-mode discretization, q=26-106)
- `I_S1`: S¹ identity (diagonal, size s1_size)
- `Γ_S2`: S² chirality operator (chiral block structure)
- `P_S1(alpha, W)`: S¹ Dirac operator (spectral_circle, ring, or wilson_ring discretization, twisted boundary alpha, disorder strength W)

This construction is a **computational diagnostic tool** designed to test:
1. **Operator algebra:** Does Kronecker sum preserve Hermiticity, shape consistency, +λ/-λ symmetry?
2. **Product spectral structure:** Do eigenvalues split as expected (D_S2 eigenvalues replicated s1_size times + S¹ eigenvalue shifts)?
3. **Disorder response:** Does Anderson localization gate detect disorder-induced IPR growth?

**What product-discretized operators do NOT represent:**

- ❌ **Not continuum Dirac operators:** Finite-mode S² (q≲100) and finite-lattice S¹ (s1_size≲96) are far from continuum limits. No extrapolation q→∞ or s1_size→∞ is performed.

- ❌ **Not physical fermions:** These operators are **topological toy constructs**. No gauge coupling (SU(3)×SU(2)×U(1)), no Yukawa couplings, no fermion mass hierarchy. Dirac index counts **topological zero modes**, NOT physical chiral fermions.

- ❌ **Not geometrically universal:** Product-discretization is **one construction method** among many (spectral truncation, lattice gauge theory, finite elements). Success on product-discretized operators does NOT validate all discretization schemes.

**Result:** Product-discretized operators are **engineering artifacts** for falsification-first workflow validation, not representations of physical fields.

### 9.1.3 No Automatic Transfer to Higher Dimensions

**Common misconception:** "S²×S¹ works → S³×S⁶ works."

**Why this is false:**

1. **Dimensional scaling:** S²×S¹ operator size = dim(S²) × s1_size ≈ (100-400) × (8-96) = 10³-10⁴. S³×S⁶ operator size = dim(S³) × dim(S⁶) ≈ 10⁶ × 10⁹ = 10¹⁵ (infeasible for direct diagonalization).

2. **Topological complexity:** S² is simply connected (π₁=0), S⁶ is simply connected. But S²×S¹ has b₁=1 (nontrivial H¹), while S⁶ has b₁=0. Topology changes discretization requirements.

3. **Discretization family dependence:** Ring family on S²×S¹ requires s1_size≥64 for alpha=0 (empirical guideline from v0.1.15). This threshold is **geometry-specific** — no evidence it applies to S³×S⁶.

4. **Falsification ladder reset:** Each new geometry requires **independent validation** starting from controls (q=0 gates, clean vs disordered contrast). S²×S¹ success does NOT inherit to S³×S⁶ without re-running the full diagnostic chain.

**Result:** v0.1.15 validates **S²×S¹ operators only**. Claims about S⁶, S³×S⁶, Calabi-Yau, or any other geometry require separate case studies with independent audit.

---

## 9.2 Finite-Lattice Limitations

### 9.2.1 s1_size Up to 96 Is Not Continuum

The largest S¹ lattice tested in v0.1.15 is **s1_size=96** (targeted follow-up run). This is a **finite discretization**, not a continuum limit.

**Continuum extrapolation requires:**

1. **Systematic scaling study:** Test s1_size = 64, 96, 128, 192, 256, 512, 1024... and fit convergence rate (power law, exponential, logarithmic).

2. **Extrapolation to s1_size→∞:** Use Richardson extrapolation, finite-size scaling, or renormalization group methods to estimate continuum limit.

3. **Error bounds:** Quantify discretization error δ(s1_size) and verify δ→0 as s1_size→∞.

**What v0.1.15 does instead:**

- **Empirical threshold detection:** "Failures vanish at s1_size≥64" is an **operational guideline**, not a continuum convergence proof.

- **Two-point comparison:** s1_size<64 (failures present) vs s1_size≥64 (failures absent). This is **robustness evidence**, not scaling law.

- **No extrapolation:** No fit δ(s1_size), no continuum limit estimate, no error bars on s1_size→∞.

**Why this matters:**

Finite-lattice stability (failures vanish at s1_size≥64) demonstrates **discretization convergence** — the operator construction becomes numerically robust at sufficiently large lattices. This does NOT prove **continuum convergence** — that the discretized operator approaches a continuum Dirac operator as s1_size→∞.

**Analogy:** A numerical integral converges to 6 decimal places at N=1000 grid points. This proves the integrator is stable, NOT that the integrand is smooth or that the continuum integral exists.

**Result:** s1_size≥64 is an **empirical production guideline** for finite-lattice operators, not a continuum limit.

### 9.2.2 Failure Disappearance as Empirical Stability

The ring/alpha=0 caveat discovery (Section 7) found:
- **s1_size<64:** 51/777 failures (6.6%)
- **s1_size≥64:** 0/252 failures (0.0%)

**Interpretation (correct):** Ring discretization of S¹ at alpha=0 (periodic boundary) requires larger lattices (s1_size≥64) for numerical stability. Below this threshold, localization gates fail due to discretization artifacts.

**Interpretation (incorrect, NOT claimed):** Ring operators converge to a continuum Dirac operator at s1_size≥64, and all continuum-limit properties are captured.

**Why the second interpretation is unjustified:**

1. **Zero failures ≠ continuum correctness:** Absence of localization gate failures means the operator passes Anderson benchmark tests. It does NOT mean the operator eigenvalues match continuum Dirac eigenvalues to arbitrary precision.

2. **Threshold is discretization-family dependent:** Spectral_circle and wilson_ring showed 0 failures at **all tested s1_size** (including s1_size=8). Ring's s1_size≥64 threshold is **ring-specific**, not universal.

3. **No comparison to continuum reference:** v0.1.15 does not compute continuum S¹ Dirac spectrum and compare to discretized spectrum. The 0/252 success rate is **internal consistency** (operators pass their own gates), not **external validation** (operators match known continuum results).

**Result:** Failure disappearance at s1_size≥64 is **empirical evidence of discretization convergence**, not continuum extrapolation.

### 9.2.3 Production Guideline as Empirical, Not Theorem

The production guideline derived from v0.1.15 is:

> **Ring/alpha=0:** s1_size ≥ 64 required for robustness  
> **Ring/alpha≠0:** s1_size ≥ 32 sufficient (no failures observed)  
> **Spectral_circle, wilson_ring:** robust at all tested s1_size

This is an **empirical operational constraint**, not a mathematical theorem.

**What "empirical" means:**

- **Derived from data:** 1349 targeted follow-up cases, parameter sweep over (q, s1_size, alpha, W, seeds).
- **Falsifiable:** If a future run finds ring/alpha=0 failures at s1_size=128, the guideline is revised.
- **Confidence bounds:** 95% CI upper bound ≈ 1.2% (Rule of Three: 3/252) for s1_size≥64. This is **statistical confidence**, not mathematical proof.

**What "empirical" does NOT mean:**

- ❌ **Not a theorem:** No proof that ring/alpha=0 MUST fail at s1_size<64 or MUST pass at s1_size≥64.
- ❌ **Not geometry-independent:** The s1_size≥64 threshold applies to S²×S¹ product operators with tested parameters. No claim it generalizes to S²×S² or S³×S¹.
- ❌ **Not boundary-condition independent:** The threshold is specific to alpha=0 (periodic). Alpha=0.5 (twisted) shows different behavior (no failures even at small s1_size).

**Result:** The production guideline is a **data-driven operational constraint**, not a universal law. It should be re-tested when geometry, operator construction, or boundary conditions change.

---

## 9.3 Operator and Discretization Limitations

### 9.3.1 Results Depend on Tested Operator Families

The v0.1.15 diagnostic tested **three S¹ discretization families**:

1. **spectral_circle:** Fourier-mode truncation (periodic boundary native)
2. **ring:** Finite-difference-inspired stencil (periodic boundary)
3. **wilson_ring:** Wilson-fermion-inspired discretization (suppresses fermion doubling)

**Key finding:** Spectral_circle and wilson_ring showed **0 disordered failures** across 2205 cases each. Ring showed **51 failures** (100% localized to alpha=0, s1_size<64).

**What this demonstrates:**

- **Discretization-family dependence:** Operator behavior varies by construction method. Spectral_circle is universally robust (in tested parameter range), ring requires lattice-size guidelines.

- **No universal "S¹ discretization":** The phrase "S¹ discretization" is ambiguous — it could mean spectral truncation, finite difference, Wilson fermion, staggered fermion, etc. Results are **family-specific**.

**What this does NOT demonstrate:**

- ❌ **Spectral_circle is universally optimal:** Spectral_circle passed all tested cases (s1_size=8-96, alpha=0.0/0.5, W=0-12). This does NOT prove it will pass at s1_size=1024, alpha=0.7, W=50, or on different geometries.

- ❌ **Ring should be deprecated:** Ring's s1_size≥64 requirement is a **documented caveat**, not a fatal flaw. At s1_size≥64, ring is **as robust as spectral_circle** (0/252 failures). The choice depends on application requirements (boundary condition native support, computational cost, physical interpretation).

- ❌ **Wilson_ring eliminates fermion doubling:** Wilson_ring is inspired by Wilson fermion discretization (adds mass term to suppress doublers). v0.1.15 does NOT audit for fermion doubling explicitly — no doubled eigenvalue detection, no axial current conservation check. The name "wilson_ring" indicates construction method, NOT validated fermion-doubling suppression.

**Result:** Operator family choice affects numerical robustness. v0.1.15 validates **three specific families** on S²×S¹, not all possible discretizations.

### 9.3.2 Spectral Families Are Not Exhaustive

The tested families (spectral_circle, ring, wilson_ring) are **three among many** discretization schemes for S¹ Dirac operators:

**Untested families include:**

- **Staggered fermions:** Reduce fermion doubling by distributing chirality over lattice sites (Kogut-Susskind).
- **Domain-wall fermions:** Confine chiral zero modes to domain walls (4D lattice with 5th dimension).
- **Overlap fermions:** Exact chiral symmetry on lattice (Neuberger operator, computationally expensive).
- **Twisted mass fermions:** Add imaginary mass term to improve condition number.
- **Higher-order finite difference:** Multi-point stencils for improved convergence.

**Why this matters:**

Each discretization family has **different convergence properties, computational costs, and failure modes**. Spectral_circle's universal robustness in v0.1.15 does NOT imply staggered fermions or overlap fermions will behave identically.

**Falsification ladder implication:**

Every new discretization family requires **independent validation** starting from controls (Hermiticity, shape consistency, q=0 gates). No inheritance from spectral_circle/ring/wilson_ring results.

**Result:** v0.1.15 validates **three discretization families**, not the concept of "S¹ discretization" universally.

### 9.3.3 Wilson / Fermion-Doubling Audit Remains Future Work

**What "wilson_ring" means in v0.1.15:**

The wilson_ring family uses a construction **inspired by Wilson fermion discretization** — it adds a mass-like term to the S¹ Dirac operator to suppress unwanted fermion species (doublers).

**What v0.1.15 does NOT validate:**

1. **Fermion doubling detection:** No explicit check that wilson_ring eliminates doubled eigenvalues (e.g., comparing eigenvalue count to expected Dirac index).

2. **Axial symmetry breaking:** Wilson term breaks chiral symmetry (intentionally, to suppress doublers). v0.1.15 does NOT verify that axial current is conserved or broken as expected.

3. **Continuum limit recovery:** Wilson fermions recover continuum chiral symmetry as lattice spacing a→0. v0.1.15 does NOT test whether wilson_ring eigenvalues approach continuum Dirac spectrum at large s1_size.

**Why this audit is required:**

Fermion doubling is a **lattice artifact** — naive discretization produces 2^d fermion species on a d-dimensional lattice (Nielsen-Ninomiya theorem). Wilson term suppresses doublers by adding O(a) mass corrections. To claim wilson_ring "works," we must verify:
- Doubled eigenvalues are absent (or suppressed below tolerance)
- Chiral symmetry breaking is controlled (Wilson term does not introduce unphysical modes)
- Continuum limit is approached correctly (O(a) corrections vanish as s1_size→∞)

**Current status:** v0.1.15 tests wilson_ring **operational robustness** (0 failures, passes localization gates). It does NOT audit **fermion-doubling physics**.

**Future work (Track B, Roadmap):**

```
Task: Fermion-Doubling Diagnostic
- Count eigenvalue multiplicity (expect 1× modes, not 2× or 4×)
- Compute axial current Ward identity violation
- Compare wilson_ring vs ring eigenvalue spectra at large s1_size
- Test continuum limit: scale s1_size and verify O(a) Wilson term → 0
```

**Result:** Wilson_ring passed operational tests (robustness, gates), but **fermion-doubling audit remains future work**. No claim that doublers are suppressed or chiral symmetry is correctly broken.

### 9.3.4 No Physical Chirality Proof

**What v0.1.15 computes:**

- **Topological Dirac index:** For S² monopole operators, index = q (monopole charge). This is a **topological invariant** (counts zero modes in chiral sectors).

- **Localization metrics:** IPR (Inverse Participation Ratio), r-statistics (level spacing ratio), window-robust gates. These detect **Anderson localization** (disorder-induced spatial confinement).

**What v0.1.15 does NOT compute:**

- ❌ **Physical chiral fermions:** No gauge coupling (SU(3)×SU(2)×U(1)), no Yukawa couplings, no fermion mass hierarchy. Dirac index is a **topological toy count**, not a physical particle count.

- ❌ **Chiral anomaly cancellation:** No check that gauge anomalies (triangle diagrams) cancel. Anomaly cancellation is required for consistent gauge theory — toy Dirac operators do NOT validate this.

- ❌ **Electroweak symmetry breaking:** No Higgs mechanism, no spontaneous symmetry breaking, no Goldstone bosons. Toy operators have no connection to Standard Model electroweak sector.

**Why "physical chirality" requires more than topological index:**

In physical theories (Standard Model, beyond-SM extensions):
1. **Chirality is gauge-dependent:** Left-handed fermions transform under SU(2)_L, right-handed under U(1)_Y. Topological index counts zero modes, NOT gauge-sector assignments.

2. **Chiral anomalies must cancel:** Fermion representations must satisfy anomaly cancellation conditions (sum of gauge charges = 0). Toy Dirac operators do NOT validate this.

3. **Masses require Yukawa couplings:** Physical fermions have masses from Higgs Yukawa couplings (m_f ~ y_f v, where v = Higgs VEV). Toy operators have no Yukawa sector.

**Result:** v0.1.15 validates **topological index computation** on discretized toy operators. This does NOT prove **physical chiral fermions** or **Standard Model chirality structure**.

---

## 9.4 Statistical and Diagnostic Limitations

### 9.4.1 Windows, Gates, and v2/v3 Disagreements

**Localization gates in v0.1.15:**

The workflow uses **multiple gate versions** to detect window-selection sensitivity:

- **v2 (fixed-window):** Single low-energy window, checks IPR contrast (disordered/clean > threshold).
- **v3 (window-robust):** Multiple window sizes, requires consistent localization signal across windows.

**Why multiple gates exist:**

Localization is a **spectrum-dependent property** — eigenstates near zero energy may behave differently from mid-spectrum or high-energy states. Fixed-window gates risk **false positives** (localization appears in one window but vanishes when window changes).

**v0.1.15 finding:** 7 cases showed **v2/v3 disagreement** (v2 passes, v3 fails). All 7 were ring family, alpha=0. Interpretation: v2 gate is **too permissive** — it passes cases that v3 correctly identifies as window-sensitive.

**Implication for generalization:**

Gate disagreements are **edge cases**, but they reveal a fundamental limitation: **localization gates are heuristics, not theorems**. No gate can perfectly distinguish "localized" from "delocalized" without assumptions about spectrum structure, disorder distribution, or system size scaling.

**What this does NOT invalidate:**

- ✅ v3 (window-robust) is used as **primary gate** for baseline promotion. The 7 disagreements are **documented edge cases**, not systemic failures.
- ✅ Spectral_circle and wilson_ring showed **0 v2/v3 disagreements** (2205 cases each). Gate robustness is **family-dependent**, not universal weakness.

**Result:** Gates are **engineering diagnostics**, not physical laws. v2/v3 disagreements demonstrate that gate choice matters — results are **diagnostic-dependent**, not absolute truth.

### 9.4.2 q=0 False Positives Validate Control Behavior, Not Total Correctness

**q=0 gate definition:**

For monopole-free S² operators (q=0), disorder should NOT induce localization (no topological protection). The q=0 gate checks:

```
q=0 false positive count = 0  ⇒  no spurious localization on monopole-free operators
```

**What q=0 gate validates:**

- ✅ **Control reliability:** Operators with q=0 behave as expected (no localization despite disorder).
- ✅ **Gate specificity:** Localization gates do NOT trigger on monopole-free cases (no false positives).

**What q=0 gate does NOT validate:**

- ❌ **Total operator correctness:** q=0 gate checks **one failure mode** (spurious localization on delocalized controls). It does NOT check:
  - Eigenvalue accuracy (are discrete eigenvalues close to continuum?)
  - Hermiticity precision (is `||D - D†||` below numerical tolerance?)
  - Spectral completeness (are all eigenvalues computed, or is solver truncating?)

- ❌ **Physics validity:** Passing q=0 gate means the operator behaves consistently with its construction (no localization when q=0). It does NOT mean the operator represents physical fermions or correct compactification.

**Analogy:** A calculator passes the test "2+2=4" (control check). This does NOT prove the calculator computes all sums correctly — it proves the "+" function works on this test case.

**Result:** q=0 gate is a **control check**, not comprehensive validation. It guards against one specific failure mode (spurious localization), not all possible operator errors.

### 9.4.3 Reproducibility Validates Deterministic Pipeline, Not Physical Truth

**Reproducibility check in v0.1.15:**

All 6615 full diagnostic cases were **re-computed independently** with identical random seeds. Result: 6615/6615 cases reproduced exactly (eigenvalue checksums matched).

**What reproducibility validates:**

- ✅ **Deterministic pipeline:** Same inputs (q, s1_size, alpha, W, seed) → same outputs (eigenvalues, gates, flags).
- ✅ **No hidden randomness:** No uncontrolled sources of variation (uninitialized memory, race conditions, floating-point non-determinism).
- ✅ **Artifact integrity:** Run outputs are stable and archivable (future researchers can verify claims).

**What reproducibility does NOT validate:**

- ❌ **Physical correctness:** A deterministic but incorrect operator will reproduce its errors exactly. Reproducibility proves consistency, NOT correctness.

- ❌ **Platform independence:** Reproducibility was tested on **one platform** (Windows 11, specific CPU, BLAS library). Different platforms may introduce floating-point variations, BLAS implementation differences, or compiler optimizations that break bit-exact reproducibility.

- ❌ **Extrapolation stability:** Reproducibility at s1_size=96 does NOT guarantee identical results at s1_size=1024 (numerical instabilities may appear at larger sizes).

**Analogy:** A broken clock shows the same wrong time every day (reproducible error). Reproducibility is necessary for science (without it, results are not verifiable), but it is NOT sufficient (reproducible errors are still errors).

**Result:** Reproducibility validates **pipeline determinism**, not operator correctness or physical validity.

### 9.4.4 Aggregate Pass Rates Can Hide Subspace Failures

**v0.1.15 finding:**

- **Aggregate failure rate:** 51/5670 = **0.9%** (all disordered cases)
- **Ring/alpha=0 subspace rate:** 51/~630 = **8.3%** (ring/alpha=0 disordered cases only)

**Why aggregate rate is misleading:**

The 0.9% aggregate rate **masks** the 8.3% subspace concentration. If reported without breakdown, a reader might conclude "failures are rare, ignore them." The subspace analysis reveals failures are **not randomly distributed** — they are localized to a specific parameter regime (ring family, alpha=0, s1_size<64).

**v0.1.15 response:**

- ✅ Targeted follow-up (1349 cases) triggered by 8.3% subspace rate, NOT 0.9% aggregate.
- ✅ Production guideline derived from subspace behavior (s1_size≥64 for ring/alpha=0).
- ✅ Documentation distinguishes aggregate (0.9%) from subspace (8.3%) rates explicitly.

**General lesson:**

Aggregate statistics (mean, median, total pass rate) can **hide localized failure modes**. Falsification-first methodology requires:
1. **Subspace analysis:** Break down failures by (family, alpha, s1_size, W, q).
2. **Concentration detection:** Identify parameters where failure rate >> aggregate rate.
3. **Targeted investigation:** Trigger follow-up diagnostics for high-concentration subspaces.

**What this does NOT mean:**

- ❌ **Aggregate rates are useless:** Aggregate rate is still useful as a **first-pass filter** (0.9% failure → system is mostly robust). It just must be followed by subspace analysis.

- ❌ **All subspaces must have identical rates:** Different parameter regimes can have different robustness (spectral_circle robust everywhere, ring fragile at alpha=0). This is **expected**, not a failure.

**Result:** Aggregate pass rates are **screening tools**, not sufficient validation. Subspace analysis is required to detect localized failure modes.

---

## 9.5 Audit Limitations

### 9.5.1 Within-Project Artifact Audit Is Not External Peer Review

The v0.1.15 audit (Section 8) was an **independent within-project artifact audit** — systematic cross-verification of documentation claims against run artifacts, performed by a separate analysis pass after primary validation completion.

**What this audit validated:**

- ✅ **Documentation-artifact consistency:** Numerical claims in papers match run outputs (metrics.json, summary.md).
- ✅ **Cross-file consistency:** Six analysis documents (MILESTONE, VALIDATION_STATUS, CAVEAT, NOTE, SPECTRAL, ISSUES) report consistent numbers.
- ✅ **Scope protection:** Eight scientific non-claims are explicitly stated across all documents.
- ✅ **Falsification-first compliance:** Failure signals triggered investigation (targeted follow-up), not dismissal.

**What this audit did NOT provide:**

- ❌ **External domain expert validation:** No independent physicist, mathematician, or lattice theorist reviewed the work. Agent-based audit verifies consistency, NOT conceptual correctness.

- ❌ **Code review by third party:** No external inspection of computational core (cc_toy_lab/spectral/ modules). Audit verified documentation matches artifacts, NOT that code implements intended physics.

- ❌ **Reproducibility by independent team:** No external group re-ran the 6615-case diagnostic on different hardware. Reproducibility was **internal** (same machine, same codebase).

**Why external review is required for publication:**

Internal audit catches **interpretation drift** (documentation misrepresenting artifacts) and **scope creep** (physics overclaims). External review catches:
- **Conceptual errors:** Misunderstanding of underlying theory (Dirac operators, index theorems, lattice artifacts).
- **Blind spots:** Failure modes the project team cannot see because they are too familiar with the code.
- **Physics validity:** Whether the toy operators actually test what they claim to test (Anderson localization, topological index, chirality).

**Result:** Internal audit is **sufficient for baseline promotion** (operational use within harness). External peer review is **required for publication** (scientific claims to broader community).

### 9.5.2 Audit Checks Consistency with Artifacts, Not Universal Correctness

**Audit methodology (8-aspect framework):**

The audit verified:
1. **Data integrity:** Numbers in docs match numbers in artifacts (6615 cases, 51 failures, 252 follow-up cases).
2. **Statistical claims:** Arithmetic is correct (51/5670 = 0.9%, 0/252 = 0.0%).
3. **Test suite quality:** Pytest passes (203 tests, 1 warning).
4. **Scope protection:** Non-claims are explicitly stated (continuum, S⁶, Standard Model, chirality).
5. **Audit independence:** Auditor identity clarified (internal, not external).
6. **Artifact completeness:** Run outputs are preserved and archivable.
7. **Red flags:** High subspace rates triggered investigation (not hidden).
8. **Scientific rigor:** Falsification-first compliance verified.

**What this framework verifies:**

- ✅ **Internal consistency:** Documentation accurately represents artifacts.
- ✅ **Scope fidelity:** Claims match tested scope (S²×S¹, finite lattice, toy operators).
- ✅ **Process compliance:** Falsification-first methodology followed (controls, gates, caveats).

**What this framework does NOT verify:**

- ❌ **Physical correctness:** Audit does not check whether S²×S¹ operators represent physical compactification (this is out of scope — toy model, not physical theory).

- ❌ **Mathematical rigor:** Audit does not verify convergence rates, error bounds, or continuum limits (empirical guidelines, not theorems).

- ❌ **Universality:** Audit does not test whether results generalize to S³×S⁶, Calabi-Yau, or other geometries (only S²×S¹ tested).

**Analogy:** A building inspector checks that construction matches blueprints (walls are straight, wiring is safe, plumbing works). The inspector does NOT verify the blueprints represent a good architectural design — that is the architect's responsibility.

**Result:** Audit checks **consistency with documented scope**, not correctness beyond that scope. External domain experts are required to assess whether the scope itself is scientifically meaningful.

### 9.5.3 External Domain Expert Review Still Required for Publication

**Current status (v0.1.15):**

- ✅ Internal validation complete (6615 + 1349 cases)
- ✅ Internal audit complete (8-aspect framework, 4 documentation updates applied)
- ✅ Baseline promoted (v0.1.15-s2-s1-product-discretized-full)

**Required for publication:**

1. **External peer review:** Domain expert in differential geometry, lattice field theory, or numerical analysis reviews methodology, operator construction, and scope claims.

2. **Code review:** Independent physicist inspects cc_toy_lab/ computational core to verify:
   - Dirac operator construction matches documented formulas
   - Eigenvalue solver is appropriate for spectral analysis
   - Localization gates correctly implement Anderson benchmark

3. **Reproducibility by third party:** External group downloads codebase, re-runs diagnostic on different hardware, verifies results match (within floating-point tolerance).

**Why this is non-negotiable:**

Scientific publication requires **independent validation**. Internal audit catches documentation errors and scope inflation, but it cannot catch:
- **Conceptual misunderstandings:** "This is not what Dirac index means in lattice field theory."
- **Method limitations:** "This discretization scheme is known to fail for X, Y, Z reasons."
- **Precedent violations:** "This has been tried before and failed — here's the literature."

**Timeline for external review:**

```
v0.1.15 internal validation → v0.1.16 methodology paper draft → external domain expert review → preprint submission (arXiv) → journal peer review → publication
```

**Result:** v0.1.15 is **baseline-ready** (internal operational use). Publication requires external domain expert review and third-party reproducibility confirmation.

---

## 9.6 Explicit Scientific Non-Claims

This subsection collects all scope boundaries in one table (Table 9.1) for easy reference. These are **permanent scope boundaries** — no claim, implicit or explicit, should extend beyond these limits without explicit justification and independent validation.

### Table 9.1: Scientific Non-Claims (Eight Explicit Boundaries)

| # | Non-Claim | Reason (Why NOT Validated) |
|---|-----------|---------------------------|
| **1** | **Continuum compactification** | All operators discretized on finite lattices (S²: q≤106, S¹: s1_size≤96). No continuum extrapolation (q→∞, s1_size→∞) performed. |
| **2** | **S⁶ or S³×S⁶ validation** | Only S², S³, S¹, and S²×S¹ product spaces tested. Higher-dimensional manifolds (S⁶: 6D, S³×S⁶: 9D) NOT constructed. |
| **3** | **Standard Model derivation** | No gauge group calculation (SU(3)×SU(2)×U(1)). No fermion generations, no gauge coupling, no Yukawa couplings. |
| **4** | **Physical chirality proof** | Dirac indices are topological toy counts on discretized manifolds, NOT physical chiral fermions. No anomaly cancellation, no electroweak breaking. |
| **5** | **Witten/Lichnerowicz bypass** | Numerical index computation ≠ rigorous Atiyah-Singer proof. Computational shortcuts ≠ mathematical theorem. |
| **6** | **Physical extra dimensions** | Anderson localization benchmark is numerical disorder test, NOT physical compactification mechanism. No radion stabilization, no moduli stabilization. |
| **7** | **Hierarchy problem solution** | Toy radion model (if used) does NOT address moduli stabilization or cosmological constant problem in string theory. |
| **8** | **Observable predictions** | Topological invariants (chiral index, localization metrics) are discretized toy analogs, NOT continuum field theory predictions. No particle masses, no cross-sections, no decay rates. |

**Table Caption:**

> **Table 9.1. Scientific Non-Claims: What v0.1.15 Does NOT Prove or Claim.**  
> Eight explicit scope boundaries prevent misinterpretation of toy diagnostics as physical proofs. v0.1.15 validates discretized spectral operators on S²×S¹ using falsification-first workflow. It does **NOT** validate: continuum compactification (finite lattices only), S⁶/S³×S⁶ (only S²×S¹ tested), Standard Model (no gauge structure), physical chirality (topological counts only), Witten/Lichnerowicz bypass (numerical, not rigorous), physical extra dimensions (disorder test, not physics), hierarchy problem (toy radion, not string compactification), or observable predictions (toy invariants, not experimental observables). **This is the most important table in the paper** — it defines toy scope and prevents overclaims.

### 9.6.1 Expanded Non-Claim #1: Continuum Compactification

**What v0.1.15 does NOT claim:**

"Our results prove continuum compactification on S²×S¹ or demonstrate a continuum limit exists."

**Why NOT validated:**

- S² monopole operators: q≤106 (finite mode cutoff, far from continuum)
- S¹ discretization: s1_size≤96 (finite lattice spacing, far from s1_size→∞)
- No extrapolation study: no fit of discretization error vs lattice size, no Richardson extrapolation, no finite-size scaling
- Lattice-size scaling (Task 1, ring/alpha=0): shows convergence at s1_size≥64, but this is **discretized operator convergence** (failures vanish), NOT continuum limit (operators approach continuum Dirac operator)

**What v0.1.15 actually shows:**

Discretized Kronecker-sum operators converge numerically at sufficiently large finite lattices. This validates **harness robustness**, NOT continuum extrapolation.

### 9.6.2 Expanded Non-Claim #2: S⁶ or S³×S⁶ Validation

**What v0.1.15 does NOT claim:**

"Our S²×S¹ results extend to S⁶ (11-dimensional M-theory target) or S³×S⁶ (Kaluza-Klein compactification)."

**Why NOT validated:**

- Only low-dimensional test geometries constructed: S² (2D), S³ (3-sphere), S¹ (circle), S²×S¹ (3D product)
- S⁶ (6-dimensional sphere) NOT tested
- S³×S⁶ (9-dimensional product) NOT tested
- No claim that product-discretization method generalizes to higher dimensions
- Dimensional scaling makes direct extrapolation infeasible (S⁶ operator size ~ 10⁹, S³×S⁶ ~ 10¹⁵)

**What v0.1.15 actually shows:**

Product-discretized operators work on S²×S¹ toy geometry. This validates **construction method on one test case**, NOT applicability to Kaluza-Klein or M-theory compactification spaces.

### 9.6.3 Expanded Non-Claim #3: Standard Model Derivation

**What v0.1.15 does NOT claim:**

"Our results derive SU(3)×SU(2)×U(1) gauge group or explain 3 fermion generations."

**Why NOT validated:**

- No gauge group calculation: no SU(3) color, no SU(2) weak, no U(1) hypercharge
- No gauge coupling constants (g₃, g₂, g₁)
- No fermion generations (only topological Dirac indices, no particle content)
- No electroweak symmetry breaking (no Higgs mechanism, no Goldstone bosons)
- No QCD confinement (no gluon dynamics, no hadronization)
- No Yukawa couplings (no fermion mass hierarchy, no flavor mixing)

**What v0.1.15 actually shows:**

Toy Dirac operators with topological indices can be constructed on product manifolds. This validates **Dirac operator construction**, NOT Standard Model derivation.

### 9.6.4 Expanded Non-Claim #4: Physical Chirality Proof

**What v0.1.15 does NOT claim:**

"Our Dirac indices prove physical chiral fermions or explain chirality asymmetry in nature."

**Why NOT validated:**

- Dirac indices computed on discretized toy manifolds, NOT continuum field theory
- Atiyah-Singer index formula applied to discretized operators (topological toy counts, not physical particles)
- No chiral anomaly cancellation (gauge anomalies NOT computed, no triangle diagram checks)
- No fermion mass terms (no Yukawa sector, no hierarchy explanation)
- No flavor structure (no CKM matrix, no PMNS matrix)

**What v0.1.15 actually shows:**

Topological Dirac indices are numerically robust on discretized toy manifolds. This validates **topological index computation**, NOT physical chiral fermions.

### 9.6.5 Expanded Non-Claim #5: Witten/Lichnerowicz Bypass

**What v0.1.15 does NOT claim:**

"Our numerical index computation bypasses Witten's rigorous Atiyah-Singer proof or Lichnerowicz formula."

**Why NOT validated:**

- Numerical eigenvalue decomposition ≠ rigorous index theorem proof
- Computational shortcuts (finite lattices, numerical tolerances, sparse solvers) ≠ mathematical proof
- No proof that discretized index equals continuum index (convergence NOT established)
- Witten's heat kernel proof and Lichnerowicz formula remain the gold standard for index theorems

**What v0.1.15 actually shows:**

Numerical index computation is feasible and reproducible on discretized toy operators. This validates **numerical implementation**, NOT mathematical rigor.

### 9.6.6 Expanded Non-Claim #6: Physical Extra Dimensions

**What v0.1.15 does NOT claim:**

"Anderson localization results prove physical extra dimensions exist, are stable, or are observable."

**Why NOT validated:**

- Anderson benchmark is a numerical test of disorder-induced localization, NOT a physical compactification mechanism
- IPR (Inverse Participation Ratio) gates are numerical quality checks, NOT physical observables
- No radion stabilization mechanism (no moduli potential, no Goldberger-Wise stabilization)
- No hierarchy problem addressed (no explanation of Planck/electroweak scale separation)
- No experimental predictions (no LHC signatures, no collider observables)

**What v0.1.15 actually shows:**

Discretized toy operators exhibit disorder-induced localization (Anderson benchmark). This validates **numerical localization test**, NOT physical extra dimensions.

### 9.6.7 Expanded Non-Claim #7: Hierarchy Problem Solution

**What v0.1.15 does NOT claim:**

"Radion toy model solves the hierarchy problem or stabilizes moduli in string compactification."

**Why NOT validated:**

- Radion toy model (if used) has simplified assumptions (effective potential, regularized KK tower)
- No string compactification (no flux stabilization, no warped geometry, no brane dynamics)
- No cosmological constant problem addressed (no dark energy, no vacuum energy cancellation)
- No hierarchy explanation (no mechanism for Planck scale ~ 10¹⁹ GeV vs electroweak scale ~ 10² GeV)

**What v0.1.15 actually shows:**

Toy radion potential can be constructed with simplified stabilization. This validates **toy radion construction**, NOT hierarchy problem solution.

### 9.6.8 Expanded Non-Claim #8: Observable Predictions

**What v0.1.15 does NOT claim:**

"Our results predict experimental observables (particle masses, scattering cross-sections, decay rates, LHC signatures)."

**Why NOT validated:**

- Topological invariants (chiral index, localization metrics) are discretized toy analogs, NOT continuum field theory predictions
- No particle masses computed (no quark masses, no lepton masses, no neutrino masses)
- No scattering cross-sections (no pp → X, no e⁺e⁻ → X)
- No decay rates (no Γ(Z → ff̄), no branching ratios)
- No LHC predictions (no new particle signatures, no resonances, no missing energy)

**What v0.1.15 actually shows:**

Topological invariants are numerically robust on discretized toy manifolds. This validates **numerical topology tools**, NOT experimental predictions.

---

## 9.7 What Remains Valid Despite These Limits

The limitations documented in this section do NOT invalidate the v0.1.15 case study or the falsification-first methodology. The following remain valid within the tested scope:

### 9.7.1 Falsification-First Workflow Is Reusable

**What v0.1.15 demonstrates:**

- **Control gates work:** q=0 false positive count = 0 validates gate specificity on monopole-free cases.
- **Failure localization is detectable:** 51 failures concentrated in ring/alpha=0 subspace (8.3% rate vs 0.9% aggregate).
- **Targeted follow-up is triggerable:** High subspace rate → 1349-case investigation → empirical guideline (s1_size≥64).
- **Caveat discovery workflow:** Progressive profile analysis (Section 5) identified ring/alpha=0 fragility before full diagnostic.

**What this validates:**

The **methodology** (falsification-first workflow, progressive profiles, independent audit, caveat handling) is **reusable across operator classes and geometries**. The workflow caught localized failures, triggered investigation, and derived production guidelines — this process is **geometry-independent**.

**What this does NOT validate:**

The **specific results** (ring/alpha=0 requires s1_size≥64) are **geometry-specific**. If tomorrow we test S²×S², the s1_size≥64 guideline does NOT automatically transfer — it must be re-tested.

**Result:** Workflow methodology is validated and reusable. Numerical results are geometry-specific and non-transferable without independent validation.

### 9.7.2 v0.1.15 Case Study Validates Methodology in Tested Scope

**Tested scope:**

- **Geometries:** S², S³, S¹, S²×S¹ (product-discretized)
- **Operator families:** spectral_circle, ring, wilson_ring (three S¹ discretizations)
- **Parameter range:** q ∈ {-3,...,3}, s1_size ∈ {8,16,24,32,48,64,96}, alpha ∈ {0.0, 0.5}, W ∈ {0.0, 2.0,...,12.0}
- **Sample size:** 6615 full diagnostic + 1349 targeted follow-up = 7964 total cases

**What v0.1.15 proves within this scope:**

- ✅ **Operator construction is robust:** Hermiticity, shape consistency, reproducibility passed across all 7964 cases.
- ✅ **Gates are reliable:** q=0 false positives = 0, localization gates detect disorder contrast.
- ✅ **Failures are detectable:** Ring/alpha=0 fragility identified, investigated, and resolved via production guideline.
- ✅ **Documentation is accurate:** Independent audit verified claims match artifacts (4 minor corrections applied).

**What v0.1.15 does NOT prove:**

- ❌ Results generalize to S³×S⁶, Calabi-Yau, or other geometries (untested).
- ❌ Results hold at s1_size=1024 or q=1000 (untested parameter regimes).
- ❌ Operators represent physical fermions or correct compactification (toy scope).

**Result:** v0.1.15 is **conclusive within tested scope**, not beyond it. The case study validates methodology on S²×S¹ finite-lattice toy operators — extrapolation requires new case studies.

### 9.7.3 Caveat Handling and Release Integrity Are Reusable Practices

**v0.1.15 caveat handling workflow:**

1. **Detection:** Progressive profile analysis identified ring/alpha=0 failures before full diagnostic.
2. **Investigation:** Targeted follow-up (1349 cases) tested lattice-size scaling hypothesis.
3. **Classification:** Decision Rule 1 applied → verdict SMALL_LATTICE_ARTIFACT.
4. **Guideline derivation:** Empirical threshold s1_size≥64 established from 0/252 failure rate.
5. **Documentation:** All caveats documented in FULL_CAVEAT_ANALYSIS.md, MILESTONE, RELEASE_NOTES, paper drafts.
6. **Audit verification:** Independent audit confirmed caveat documentation accuracy (4 minor corrections applied).

**What this workflow provides:**

- **Transparency:** Failures are documented, not hidden behind aggregate statistics.
- **Actionability:** Production guidelines are derived from empirical evidence, not guesses.
- **Auditability:** Caveat discovery chain is traceable from detection → investigation → classification → guideline.

**Reusability for future work:**

When testing S²×S² or S³×S¹:
1. Run progressive profile analysis first (Section 5 workflow) to detect subspace failures early.
2. If high subspace failure rate detected → trigger targeted follow-up (Section 7 workflow).
3. Apply decision rules (SMALL_LATTICE_ARTIFACT vs PERSISTENT_LIMITATION).
4. Derive production guidelines from empirical thresholds.
5. Document caveats in all release materials.
6. Run independent audit to verify documentation accuracy.

**Result:** The caveat handling workflow (detection → investigation → classification → guideline → documentation → audit) is **methodology**, not geometry-specific. It is reusable for any operator class, geometry, or parameter regime.

---

## 9.8 Summary

This section documented nine categories of limitations and scope boundaries for the v0.1.15 case study:

1. **Toy-model scope (9.1):** S²×S¹ is a diagnostic test geometry, NOT Calabi-Yau, Kaluza-Klein, or physical compactification. Results do NOT transfer to S⁶, S³×S⁶, or higher dimensions without independent validation.

2. **Finite-lattice limitations (9.2):** s1_size≤96 is finite discretization, NOT continuum. Failure disappearance at s1_size≥64 is empirical stability, NOT continuum convergence. Production guideline is data-driven operational constraint, NOT mathematical theorem.

3. **Operator limitations (9.3):** Results depend on tested families (spectral_circle, ring, wilson_ring). Wilson/fermion-doubling audit remains future work. No physical chirality proof (topological index ≠ physical chiral fermions).

4. **Diagnostic limitations (9.4):** Gates are heuristics, NOT theorems. q=0 gate validates control behavior, NOT total correctness. Reproducibility validates deterministic pipeline, NOT physical truth. Aggregate rates can hide subspace failures.

5. **Audit limitations (9.5):** Within-project artifact audit is NOT external peer review. Audit checks consistency with artifacts, NOT universal correctness. External domain expert review remains required for publication.

6. **Scientific non-claims (9.6):** Eight explicit boundaries (Table 9.1): no continuum compactification, no S⁶/S³×S⁶, no Standard Model, no physical chirality, no Witten/Lichnerowicz bypass, no physical extra dimensions, no hierarchy problem solution, no observable predictions.

7. **What remains valid (9.7):** Falsification-first workflow is reusable (methodology). v0.1.15 case study validates methodology in tested scope (S²×S¹, finite lattice, toy operators). Caveat handling and release integrity are reusable practices.

**Key discipline:** Limitations are **scope boundaries**, not apologies. They define what the methodology can and cannot validate. v0.1.15 proves the falsification-first workflow works on discretized toy operators — this is a **methodological achievement**, not a physics failure.

**Transition to Section 10:**

Section 10 (Conclusion and Future Work) outlines the path from validated toy diagnostics toward broader operator classes and geometry extensions. Three tracks are proposed:

- **Track A:** Expand to additional product geometries (S²×S², S³×S¹, eventual S³×S³)
- **Track B:** Continuum extrapolation (q→∞, s1_size→∞ scaling studies)
- **Track C:** Higher-dimensional targets (S⁶ construction, S³×S⁶ Kaluza-Klein bridge)

Each track requires **independent validation** starting from controls. No inheritance from S²×S¹ results without explicit verification.

---

**Section 9 complete.** Next: Section 10 — Conclusion and Future Work (roadmap beyond v0.1.15 scope).
