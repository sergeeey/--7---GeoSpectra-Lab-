# Operator Decision / Fix Plan — v0.1.23

**Дата:** 2026-05-25  
**Статус:** OPERATOR_DECISION_REQUIRED_BEFORE_FIX  
**Trigger:** Operator Consistency Audit v0.1.23  
**Scope:** S³ Dirac, S¹ ring/wilson_ring scaling, Anderson 3D dense window

---

## 1. Purpose

Этот документ определяет как продолжить работу после Operator Consistency Audit, который выявил operator-level inconsistencies.

**Ключевой принцип:** Этот документ НЕ меняет код и НЕ запускает эксперименты. Он только планирует decision path.

**Отличие от code-audit / code-materiality:**
- Code-audit проверял implementation bugs (логика, индексы, границы)
- Code-materiality определял какие bugs влияют на active pipeline
- **Operator Decision** определяет правильно ли implemented operator соответствует declared theoretical formula

**Stack position:**
```
Operator Decision (этот файл) → определяет WHAT operator we have
     ↓
Code Audit (завершён) → определял HOW operator implemented
     ↓
Gate results (заморожены) → computational outputs для implemented operator
```

---

## 2. Current Frozen State

**Gate 4B v0.1.21:**
- Статус: CLOSED (PASS_WITH_CAVEATS)
- Raw outputs: PRESERVED (reports/RUNS/gate_4b_v0.1.21/)
- Computational integrity: VALID для implemented S³×S¹ operator
- Physical interpretation: **FROZEN** до operator decision
- Commits: f7eff32 (results), 0c78263 (closeout), immutable

**v0.1.22 Negative Controls:**
- Batches 1-2 (18 cases): completed, outputs preserved as implemented-operator baseline
- Batches 3-6 (36 cases): **PAUSED**, не запускать до operator decision
- Remote execution: suspended

**Local heavy execution:**
- Thermal constraint: LOCAL_EXECUTION_PROHIBITED
- Никаких Gate 5, pilot runs, W-sweeps, cubic tests

**New scientific claims:**
- Forbidden до operator decision resolution

**Backup branch:**
- `backup/unsafe-code-fixes-before-cleanup`: exists, НЕ применять fixes

---

## 3. Findings Recap

| # | Finding | Status | Severity | Evidence | Affected Scope |
|---|---------|--------|----------|----------|----------------|
| **1** | S²×S¹ spurious zeros (D_S2² + P_S1 cancellation) | ❌ NOT_CONFIRMED | Watch Item | Canonical test: q=0, cutoff=1, s1_size=8, alpha=0 → 0 near-zeros (not 4 as claimed) | S²×S¹ product (legacy) |
| **2** | S³ Dirac spectrum asymmetric | ✅ **VERIFIED** | **CRITICAL** | j_max=0: [-2.5(×6), +1.5(×2)] vs expected ±1.5; j_max=1: [-3.5, -2.5, +1.5, +2.5] vs ±[1.5, 2.5]; Code: +(k+0.5), -(k+1.5); Test: ±(n+3/2) | **Gate 4B v0.1.21** (S³×S¹), Gate 3C, all S³-based results |
| **3** | S¹ ring/wilson_ring scale mismatch | ✅ **VERIFIED** | **MEDIUM/HIGH** | ring scale = N/R, spectral_circle = (m+α)/R; Different scaling conventions; ring(alpha=0) behavior unclear | Gate 4B family-consistency claims, S¹ discretization comparisons |
| **4** | Anderson 3D dense window median-index | ✅ **VERIFIED** | **MEDIUM** | Dense: center = len//2 (median index); Sparse: sigma=0.0 (E≈0); For shifted spectrum: median ≠ E=0 (diff ~2.5σ) | 3D Anderson quick diagnostics (L≤6), anderson_3d baseline tests |

**Ключевая находка:** Finding #2 (S³ Dirac asymmetry) имеет CRITICAL severity и влияет на центральный S³×S¹ operator interpretation.

---

## 4. S³ Dirac Decision — Priority A (CRITICAL)

### 4.1 Contradiction Triangle

**Три источника информации противоречат друг другу:**

| Source | Formula | Spectrum Structure |
|--------|---------|-------------------|
| **Code implementation** (dirac_s3.py:81-82) | λ₊ = +(k+0.5)/R<br>λ₋ = -(k+1.5)/R | **ASYMMETRIC**<br>k=1: [+1.5, -2.5] |
| **Paper citation** (dirac_s3.py:54, arXiv:1103.4097 page 15) | λ₊ = +(k+1/2)/R<br>λ₋ = -(k+3/2)/R | **ASYMMETRIC**<br>k=1: [+1.5, -2.5] |
| **Test expectations** (test_s3_s1_gate3c_triad_v0_1_20.py:30-35) | λ = ±(n + 3/2)/R | **SYMMETRIC**<br>n=0: [±1.5] |

**Code implementation formula matches the citation in code comments (arXiv:1103.4097 page 15), but conflicts with test expectations. Independent source verification required.**

### 4.2 Canonical S³ Dirac Spectrum (from standard sources)

**Standard SU(2) Dirac operator on S³:**

Спектр зависит от используемой формулировки. Наиболее распространённые conventions:

**Convention A (symmetric, most common in physics):**
```
λ = ±(n + 3/2) / R
n = 0, 1, 2, ...
Degeneracy per sign: (n+1)(n+2)
Lowest: ±1.5, ±2.5, ±3.5, ...
```

**Convention B (asymmetric, representation theory):**
```
λ₊ = +(k + 1/2) / R,  degeneracy k(k+1)
λ₋ = -(k + 3/2) / R,  degeneracy (k+2)(k+1)
k = 1, 2, 3, ...
Lowest: +1.5 (deg 2), -2.5 (deg 6)
```

**Verification results:**
```
j_max=0 (k=1):
  Actual: [-2.5(×6), +1.5(×2)]
  Matches: Convention B (asymmetric)
  Expected by tests: ±1.5 (symmetric)

j_max=1 (k=1,2):
  Actual: [-3.5(×12), -2.5(×6), +1.5(×2), +2.5(×6)]
  Matches: Convention B (asymmetric)
  Expected by tests: ±[1.5, 2.5] (symmetric)
```

### 4.3 Interpretation Options

**Option A: Code is correct (Convention B), tests are wrong**
- Code comments cite arXiv:1103.4097 for asymmetric formula (independent verification required)
- Code explicitly implements asymmetric branches (lines 81-82)
- Tests were written with wrong expectation (symmetric)
- **Action:** Update tests, documentation, pre-registration to reflect Convention B

**Option B: Code is wrong (should be Convention A), paper misread**
- Physics literature commonly uses symmetric ±(n+3/2) convention
- Tests were written based on standard physics convention
- Paper citation may have been misunderstood or applies to different context
- **Action:** Fix code to implement symmetric ±(n+3/2), rerun affected gates

**Option C: Code implements proxy operator, not canonical S³ Dirac**
- Current implementation is valid mathematical operator
- Does not correspond to standard S³ Dirac (either convention)
- Should be renamed and documented as proxy/toy operator
- **Action:** Rename, add caveats, do NOT claim "S³ Dirac" validation

**Option D: Both conventions are valid, need clarification**
- Convention B is mathematically valid representation-theory formula
- Convention A is standard physics Dirac operator
- Need to decide which one GeoSpectra intends to test
- **Action:** Choose convention explicitly, update all docs accordingly

### 4.4 Recommended Default Decision

**До independent verification arXiv:1103.4097:**

**Treat as P0 blocker. Default assumption: Code implements Convention B (asymmetric), which may or may not be the intended operator.**

**Required actions before resuming work:**
1. Independent verification: read arXiv:1103.4097 page 15 carefully
2. Check if Convention B is appropriate for GeoSpectra's scientific question
3. Decide: keep asymmetric (update tests) OR fix to symmetric (update code)
4. Document chosen convention in `docs/OPERATOR_SPECIFICATIONS.md`

**Estimated resolution time:** 1-2 days (reading paper + decision meeting)

### 4.5 Impact on Gate 4B

**Если code correct (Convention B):**
- Gate 4B results remain valid as Convention B operator results
- Update interpretation: "7.15× IPR contrast for asymmetric S³ Dirac (Convention B)"
- No rerun needed, только documentation updates
- Unfreeze interpretation с правильной convention формулировкой

**Если code wrong (should be Convention A):**
- Gate 4B results become "implemented-operator baseline (asymmetric proxy)"
- Archive as computational reference: "what happens with asymmetric operator"
- **MANDATORY v0.1.24 rerun** with corrected symmetric operator
- Compare v0.1.21 (asymmetric) vs v0.1.24 (symmetric)
- If signal persists → strengthens claim; if disappears → signal was operator artifact

**Если renamed to proxy operator:**
- Gate 4B results remain valid for "asymmetric proxy operator"
- Remove all "S³ Dirac" language from claims
- Downgrade theoretical relevance: computational toy only
- Decision needed: continue with proxy or abandon S³ work

---

## 5. S¹ Ring / Wilson Scaling Decision — Priority A

### 5.1 Scale Convention Mismatch

**Observed behavior:**

| Discretization | Scale Formula | Eigenvalue Range (N=64, R=1.0, α=0.5) |
|----------------|---------------|----------------------------------------|
| spectral_circle | (m + α) / R | m ∈ {-N/2, ..., N/2-1} → eigenvalues ~[-31.5, 31.5] |
| ring | N / R × derivative | lattice spacing related → eigenvalues ~[-64, 64] |
| wilson_ring | ring + Wilson term | different scale due to Wilson correction |

**Issue:** Comparing ring vs spectral_circle "family consistency" без accounting for scaling convention может mislead interpretation.

### 5.2 Physical Interpretation

**spectral_circle (s1_discretizations.py:79-80):**
```python
modes = np.fft.fftfreq(size, d=1.0 / size)  # Integer quantum numbers m
twisted_momenta = (modes + alpha) / radius  # (m + α) / R
```
- Physical meaning: momentum eigenvalues на circle длины L = 2πR
- Natural quantum number: m + twist α
- Scale: 1/R (natural для continuum circle)

**ring (s1_discretizations.py:13-14):**
```python
scale = float(size) / float(radius)  # N / R
operator = (-0.5j * scale) * (shift - shift.conj().T)
```
- Physical meaning: finite-difference derivative на lattice
- Lattice spacing h = 2πR / N
- Derivative scale: 1/h = N / (2πR)
- Code uses N/R (missing 2π factor explicitly)

### 5.3 Interpretation Options

**Option A: Scale bug — ring should include 2π normalization**
- Continuum derivative scale: 1/h = N/(2πR)
- Current code: N/R (missing 1/2π factor)
- **Action:** Normalize ring by 2π, rerun affected gates

**Option B: Convention mismatch — intentionally different discretization families**
- spectral_circle: Fourier-based (natural quantum numbers)
- ring: lattice-based (lattice spacing related)
- Different families may have different natural scales
- **Action:** Document convention, clarify "family consistency" does NOT mean identical scales

**Option C: Physical vs lattice units confusion**
- spectral_circle in physical units (momentum / R)
- ring in lattice units (without 2π conversion)
- Both valid, different unit systems
- **Action:** Add unit conversion factor in comparisons

### 5.4 Additional Finding: ring(alpha=0) Behavior

**Expected:** For α=0, ring should reduce to clean lattice Laplacian.

**Observed (audit report claimed):** ring(alpha=0) collapses to zero operator due to anti-Hermitian structure.

**Verification needed:**
```python
# Code (s1_discretizations.py:14):
operator = (-0.5j * scale) * (shift - shift.conj().T)  # Anti-Hermitian structure
# After hermitization (line 15):
return 0.5 * (operator + operator.conj().T)
# If operator anti-Hermitian: A + A† = A - A = 0 ✗
```

**Lightweight diagnostic performed (Phase 2.2):**
- ring(alpha=0, N=64, R=1.0): max |eigenvalue| = 6.40e+01 (NOT zero)
- Operator norm: 3.62e+02
- **Conclusion:** Collapse to zero NOT confirmed by diagnostic

**Requires further investigation:** Either:
- Diagnostic conditions different from audit report
- Audit report claim incorrect
- Collapse happens only for specific parameter regime

### 5.5 Recommended Action

**Before resuming S³×S¹ work:**

1. **Clarify physical meaning of ring scale:**
   - Is N/R intended (lattice count / radius)?
   - Should it be N/(2πR) (inverse lattice spacing)?
   - Document in `docs/OPERATOR_SPECIFICATIONS.md`

2. **Decide on family-consistency interpretation:**
   - If scales should match → normalize ring, rerun
   - If different scales intentional → document, weaken "family consistency" claims

3. **Investigate ring(alpha=0) behavior:**
   - Run targeted test: alpha=0 for multiple N, R values
   - Determine if collapse occurs and under what conditions
   - Document expected behavior

4. **Wilson term scale convention:**
   - Wilson term uses same N/R scale as ring
   - If ring scale changes, Wilson term must change consistently
   - Check Wilson strength parameter meaning after scale fix

**Impact on Gate 4B:**
- If scale fix required → family-consistency claims weakened until rerun
- If WAI (working as intended) → document convention, no rerun
- wilson_ring results may need re-interpretation if Wilson scale convention changes

---

## 6. Anderson 3D Dense Window Decision — Priority B

### 6.1 Issue Summary

**Code (anderson_3d.py:118-124):**
```python
# Dense path: full diagonalization, select center band
values, vectors = np.linalg.eigh(hamiltonian.toarray())
center = len(values) // 2  # Median index
half = min(eigen_count // 2, center, len(values) - center)
start = max(0, center - half)
stop = min(len(values), center + half)
return values[start:stop], vectors[:, start:stop]
```

**Code (anderson_3d.py:127):**
```python
# Sparse path: shift-invert around E=0
values, vectors = eigsh(hamiltonian, k=k, sigma=0.0, which="LM")
```

**Problem:** For symmetric spectrum (onsite=0), median ≈ E=0. For shifted spectrum (onsite≠0), median ≠ E=0.

**Example:**
```
Symmetric: [-5, ..., 0, ..., 5] → median = 0.00, E≈0 = 0.00 ✓
Shifted:   [-10, ..., -2.5, ..., 5] → median = -2.50, E≈0 = 0.05 ✗
Difference: 2.55 (significant for band-center diagnostics)
```

### 6.2 Robust Fix Recommendation

**Option A: Closest-to-zero selection for dense path**
```python
# Replace line 120:
# center = len(values) // 2
center = np.argmin(np.abs(values))  # Closest to E=0
```

**Option B: Shift-invert sigma=0 for both paths**
```python
# Use sparse shift-invert even for small lattices
# Ensures consistent E≈0 targeting
```

**Option C: Document assumption and add validation**
```python
# Keep median index, but validate spectrum is symmetric
# Raise warning if |median_value| > threshold
```

**Recommended:** **Option A** (closest-to-zero) — simple, robust, matches sparse path semantics.

### 6.3 Impact on Existing Work

**Gate 4B (S³×S¹):** NOT affected — does NOT use anderson_3d module.

**3D Anderson baseline tests:** Affected — quick diagnostics (L≤6) use dense path.

**Required before Anderson work:**
1. Fix dense window selection (Option A)
2. Add test for shifted spectrum case
3. Verify dense/sparse paths give consistent windows
4. Document E≈0 targeting requirement

**Priority:** MEDIUM — blocks future Anderson baseline comparisons, but does NOT block S³×S¹ operator decision.

---

## 7. Decision Matrix

**Сценарии в зависимости от operator decisions:**

### Scenario 1: Documentation Mismatch Only (S³ code correct, tests wrong)

**Actions:**
- [ ] Update test expectations (test_s3_s1_gate3c_triad_v0_1_20.py) to Convention B
- [ ] Update documentation (dirac_s3.py comments) to match asymmetric formula
- [ ] Create `docs/OPERATOR_SPECIFICATIONS.md` with Convention B formulas
- [ ] Update CLAIMS_AND_CAVEATS.md: "S³ Dirac uses asymmetric Convention B"
- [ ] Unfreeze Gate 4B interpretation с правильной convention формулировкой
- [ ] Resume negative controls batches 3-6 (no code changes)
- [ ] Proceed to Gate 5

**Gate 4B impact:** Interpretation unfrozen, no rerun needed.

**Timeline:** 2-3 days (documentation updates, test fixes, validation)

---

### Scenario 2: Code Bug But No Gate 4B Impact

**Condition:** S¹ ring scale fix OR Anderson dense window fix, but S³ Dirac correct.

**Actions:**
- [ ] Fix affected operators (ring normalization OR anderson dense window)
- [ ] Add targeted unit tests for fixed operators
- [ ] Rerun only affected validation tests (not full Gate 4B grid)
- [ ] Document fix in changelog
- [ ] Decide if Gate 4B rerun optional or skipped

**Gate 4B impact:** Preserved if S³ operator unchanged. Ring scale fix may weaken family-consistency claims.

**Timeline:** 3-5 days (fix, test, targeted validation)

---

### Scenario 3: Code Bug Affects Gate 4B Core Operator (S³ Dirac wrong)

**Condition:** S³ Dirac should be symmetric Convention A, current asymmetric is wrong.

**Actions:**
- [ ] Fix dirac_s3.py to implement ±(n+3/2) symmetric spectrum
- [ ] Add analytic spectrum unit tests (test_s3_dirac_analytic_spectrum.py)
- [ ] Rerun Gate 1 Hermiticity tests (should still pass)
- [ ] **MANDATORY: v0.1.24 corrected Gate 4B rerun** (full 216-case grid)
- [ ] Archive Gate 4B v0.1.21 as "implemented-operator baseline (asymmetric proxy)"
- [ ] Rerun negative controls batches 1-6 (fresh start with corrected operator)
- [ ] Update all affected reports with v0.1.24 numbers
- [ ] Compare v0.1.21 (asymmetric) vs v0.1.24 (symmetric) results

**Gate 4B impact:** v0.1.21 becomes historical baseline, v0.1.24 is new canonical result.

**Timeline:** 7-10 days (fix, test, full rerun, analysis, comparison)

---

### Scenario 4: Corrected Operator Preserves Signal

**Condition:** After v0.1.24 rerun with corrected symmetric S³ Dirac, signal persists.

**Outcome:**
- ✅ Project strengthens — signal robust to operator convention choice
- ✅ v0.1.24 becomes primary result
- ✅ v0.1.21 archived as "asymmetric sensitivity check"
- ✅ Claim: "7.15× IPR contrast survives symmetric operator correction"
- ✅ Proceed to Gate 5 with increased confidence

**Reports:**
- `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.24.md` (new primary)
- `reports/OPERATOR_CORRECTION_COMPARISON_v0.1.24.md` (v0.1.21 vs v0.1.24)
- Update README.md with v0.1.24 verdict

---

### Scenario 5: Corrected Operator Removes Signal

**Condition:** After v0.1.24 rerun with corrected symmetric S³ Dirac, signal disappears or weakens below threshold.

**Outcome:**
- ❌ Prior signal (v0.1.21) was implementation artifact
- ❌ Asymmetric operator created spurious localization-like pattern
- ⚠️ Major pivot required

**Interpretation:**
- v0.1.21 signal = asymmetric operator artifact, not geometric property
- GeoSpectra harness worked correctly (found operator-dependent behavior)
- Negative result for canonical symmetric S³ Dirac

**Options:**
1. **Pivot to methodology focus:**
   - Report: "Falsification-first validation harness caught operator-level artifact"
   - Emphasize: scientific rigor, operator sensitivity, negative controls importance
   - Publish as validation methodology case study

2. **Investigate asymmetric operator interest:**
   - Is Convention B (asymmetric) physically meaningful in different context?
   - Rename v0.1.21 → "asymmetric S³ Dirac toy model"
   - Narrow claims: "signal observed for asymmetric operator, not canonical Dirac"

3. **Abandon S³×S¹ work, pivot to other geometries:**
   - Test S²×S¹, T²×S¹, hyperbolic manifolds
   - Use lessons learned to avoid operator-level mistakes

**Reports:**
- `reports/OPERATOR_CORRECTION_NULL_RESULT_v0.1.24.md`
- `null_results/20260525-s3s1-operator-artifact.md`
- Update README.md with pivot decision

**Timeline:** 10-14 days (rerun, analysis, pivot planning, new direction)

---

## 8. Required Unit Tests Before Any Code Fix

**НЕ implement tests сейчас — только планирование.**

### S³ Dirac Operator Tests

**File:** `tests/test_s3_dirac_analytic_spectrum.py`

**Required tests:**
1. `test_s3_dirac_eigenvalues_vs_analytic_convention_A()`
   - Build operator j_max=0, 1, 2
   - Compare numerical eigenvalues to ±(n+3/2)/R formula
   - Check degeneracies: (n+1)(n+2) per sign
   - MUST match symmetric convention (if chosen)

2. `test_s3_dirac_eigenvalues_vs_analytic_convention_B()`
   - Build operator j_max=0, 1, 2
   - Compare numerical eigenvalues to +(k+1/2)/R, -(k+3/2)/R
   - Check degeneracies: k(k+1) and (k+2)(k+1)
   - MUST match asymmetric convention (if chosen)

3. `test_s3_dirac_radius_scaling()`
   - Build operator R=1.0, 2.0, 0.5
   - Verify eigenvalues scale as 1/R
   - Check dimension formula: 2(k+1)² per level

4. `test_s3_dirac_dimension_formula()`
   - Verify total dimension matches expected from j_max
   - Cross-check against representation theory formula

**Coverage target:** 100% for analytic spectrum properties.

---

### S¹ Discretization Tests

**File:** `tests/test_s1_ring_continuum_scaling.py`

**Required tests:**
1. `test_s1_ring_continuum_scaling_convention()`
   - Check if ring scale is N/R or N/(2πR)
   - Compare low modes to continuum derivative
   - Document expected scale convention

2. `test_s1_ring_vs_spectral_circle_scale_ratio()`
   - Measure eigenvalue ratio for N=32, 64, 128
   - Document expected ratio (2π or 1 or other)
   - Verify ratio stable across sizes

3. `test_s1_alpha_twist_behavior()`
   - Test alpha=0, 0.25, 0.5, 0.75
   - Verify twist shifts spectrum as expected
   - Check ring vs spectral_circle twist implementation

4. `test_s1_ring_alpha_zero_collapse()`
   - Build ring(alpha=0) for multiple N, R
   - Measure operator norm and max |eigenvalue|
   - Verify expected behavior (collapse to zero OR non-zero lattice operator)

5. `test_wilson_ring_scale_convention()`
   - Verify Wilson term scale matches ring scale
   - Test Wilson strength parameter effect
   - Check Wilson term = 0 reduces to ring

**Coverage target:** 90% for scale conventions and family consistency.

---

### Anderson 3D Window Tests

**File:** `tests/test_anderson_3d_window_selection.py`

**Required tests:**
1. `test_dense_window_closest_to_zero()`
   - Build symmetric spectrum Hamiltonian
   - Verify dense path selects E≈0 window
   - Check window centered at argmin(|E|), not median index

2. `test_dense_sparse_window_consistency()`
   - Build same Hamiltonian, run dense and sparse paths
   - Verify both select same eigenvalues (within tolerance)
   - Compare window centers

3. `test_shifted_onsite_disorder_window()`
   - Build Hamiltonian with shifted spectrum (onsite≠0)
   - Verify dense path does NOT use median index
   - Check window contains E≈0, not spectrum median

**Coverage target:** 100% for window selection logic.

---

## 9. Required Actions Before Remote Execution

**Remote Negative Controls batches 3-6 remain PAUSED until:**

### Gate 1: S³ Operator Decision

- [ ] arXiv:1103.4097 page 15 independently verified
- [ ] Convention chosen (A: symmetric OR B: asymmetric)
- [ ] Decision documented in `docs/OPERATOR_SPECIFICATIONS.md`
- [ ] Tests updated to match chosen convention
- [ ] If code fix needed: fix applied + tests passing

### Gate 2: S¹ Scaling Decision

- [ ] Ring scale convention clarified (N/R vs N/(2πR))
- [ ] ring(alpha=0) behavior documented (collapse or not)
- [ ] Family-consistency interpretation updated (if scales differ)
- [ ] If normalization fix needed: applied + verified

### Gate 3: Anderson Dense Window Fix

- [ ] anderson_3d.py dense path updated (closest-to-zero OR documented assumption)
- [ ] Unit tests for shifted spectrum added
- [ ] Dense/sparse path consistency verified

### Gate 4: Allowed Claims Updated

- [ ] `docs/CLAIMS_AND_CAVEATS.md` updated with operator audit lessons
- [ ] Forbidden claims list includes operator-level uncertainties
- [ ] README.md reflects current status (operator decision pending)

### Gate 5: Rerun Decision Made

- [ ] If S³ Dirac code changed → v0.1.24 rerun mandatory
- [ ] If S¹ ring scale changed → decide if rerun needed
- [ ] If only documentation updated → no rerun, unfreeze interpretation

**Only after ALL 5 gates passed:** Resume remote negative controls execution.

---

## 10. Gate 4B Impact Statement

### 10.1 What Remains Valid

✅ **Computational integrity preserved:**
- Gate 4B raw outputs (eigenvalues, eigenvectors, IPR values) remain mathematically correct
- All 216 cases executed on consistent implemented operator (v0.1.21 code snapshot)
- Hermiticity verified (Gate 1 passed)
- Dimension formula verified
- No numerical bugs in computation itself

✅ **Internal consistency:**
- Finite-size scaling trend (3.76× → 24.90×) is fact for implemented operator
- Family consistency (3/3 families PASS) is fact for implemented discretizations (with scaling caveat)
- r-statistic shift (Δr = -0.163) computed correctly
- All comparisons within Gate 4B grid are valid

✅ **Methodological value:**
- Falsification-first validation harness worked as designed
- Operator consistency audit caught operator-level issue before large-scale accumulation
- Negative controls protocol remains sound
- Null-results logging protocol demonstrated

### 10.2 What Requires Freezing

❌ **FORBIDDEN до operator decision:**

**Physical interpretation claims:**
- "Gate 4B validates S³×S¹ **canonical** Dirac operator" — operator formula uncertain
- "Results demonstrate S³×S¹ **geometric** compactification mechanism" — operator may be proxy
- "Spectrum exhibits expected ±(k+1/2) **physical** structure" — asymmetry not addressed
- "Family consistency confirms **theoretical** robustness" — scale mismatch unresolved
- "Signal generalizes to continuum S³×S¹" — implemented operator may differ from continuum limit

**Theoretical claims:**
- "Localization-like pattern specific to S³ **Dirac** coupling" — operator identity uncertain
- "Results consistent with covariant compactification framework" — requires correct operator
- "S³ chirality structure validated" — chirality placeholder only, not tested
- "Product geometry **physically** validated" — computational only, operator uncertain

**External communication:**
- Any paper/preprint submission про S³×S¹ validation
- Public statements claiming "S³×S¹ breakthrough"
- Grant proposals based on Gate 4B as theoretical validation
- Presentations claiming canonical operator tested

### 10.3 Allowed Careful Phrasing

✅ **Computational milestone framing:**
- "Gate 4B v0.1.21 produced 7.15× IPR contrast for **implemented S³×S¹ operator**"
- "Finite-size scaling trend strengthening observed for **implemented discretization**"
- "Hermiticity and dimensional structure verified for current implementation"
- "Computational consistency within Gate 4B 216-case grid confirmed"
- "Further operator validation required before theoretical interpretation"

✅ **Methodology claims:**
- "Falsification-first validation harness successfully identified operator-level uncertainty"
- "Operator consistency audit prevented premature claims"
- "Gate 4B computational outputs preserved for future re-analysis"
- "Negative controls protocol paused pending operator decision"

✅ **Process transparency:**
- "Independent code review identified operator formula mismatch"
- "Scientific rigor: interpretation frozen until operator verified"
- "Gate 4B remains valid computational baseline for implemented operator"
- "Honest scientific diligence in action"

### 10.4 Recommended Framing (Template)

**For internal status updates:**
> Gate 4B v0.1.21 completed successfully as computational milestone (216 cases, 7.15× IPR contrast, strengthening FSS trend). Operator consistency audit (v0.1.23) identified S³ Dirac spectrum formula mismatch (asymmetric implementation vs symmetric test expectations). Physical interpretation frozen pending operator decision. Raw computational outputs preserved. No data loss. Estimated resolution: 2-5 days.

**For external inquiries:**
> We are conducting operator-level verification following external code review. Gate 4B computational results remain valid for the implemented operators; physical interpretation is under review pending operator formula clarification. This is standard scientific verification practice. Further updates will follow operator decision.

**For future papers (after operator decision):**
> Gate 4B v0.1.21 served as implemented-operator baseline. Following operator consistency audit (v0.1.23), [Convention B asymmetric formula was confirmed / symmetric formula was corrected in v0.1.24]. Results presented here correspond to [v0.1.21 asymmetric / v0.1.24 symmetric] operator implementation. See `docs/OPERATOR_SPECIFICATIONS.md` for detailed operator formulas.

---

## 11. Allowed / Forbidden Claims

### 11.1 Allowed Claims (Safe Territory)

✅ **Computational achievements:**
- "Implemented falsification-first validation harness for spectral operators"
- "Executed 216-case finite-size scaling grid with metric-corrected IPR diagnostic"
- "Hermiticity and dimension formula verified for implemented operators"
- "Computational pipeline tested on S³×S¹ toy geometry"
- "Code audit and operator consistency verification completed"

✅ **Methodological contributions:**
- "Demonstrated negative controls protocol for spectral validation"
- "Operator consistency audit caught formula mismatch before large-scale execution"
- "Falsification-first approach prevented premature theoretical claims"
- "Null-results logging protocol established"
- "Independent code review integrated into workflow"

✅ **Conditional results (with operator caveat):**
- "Gate 4B showed 7.15× IPR contrast **for implemented S³×S¹ operator** (operator formula verification pending)"
- "Finite-size scaling trend strengthening **in computational model** (theoretical interpretation frozen)"
- "Family consistency observed **for implemented discretizations** (scale convention under review)"

✅ **Process transparency:**
- "Operator decision required before resuming heavy experiments"
- "Remote execution paused for operator verification"
- "Scientific rigor prioritized over speed"
- "Honest reporting of uncertainties"

### 11.2 Forbidden Claims (Red Lines)

❌ **Premature validation claims:**
- "S³×S¹ validated" / "S³×S¹ operator confirmed"
- "Covariant compactification validated"
- "Theoretical S³×S¹ Dirac spectrum verified"
- "Physical compactification mechanism demonstrated"
- "Canonical operator tested and passed"

❌ **Overclaims about physical interpretation:**
- "Results prove S³×S¹ geometric coupling"
- "Localization specific to S³ Dirac structure"
- "Standard Model connection established"
- "Chirality protection validated"
- "Thermodynamic limit behavior confirmed"

❌ **Unjustified generalization:**
- "Results generalize to continuum limit"
- "Signal robust across all operator conventions"
- "Family consistency proves theoretical correctness"
- "Negative controls completed and passed" (only 18/54 done)

❌ **External submission before operator decision:**
- Paper/preprint submission
- Conference presentation claiming validation
- Grant proposal based on Gate 4B validation
- Public blog post / social media claiming breakthrough

❌ **Undermining rigor:**
- "Operator issue is minor technicality"
- "We can skip operator decision and continue"
- "Tests are wrong, code is obviously correct" (before verification)
- "Let's just rerun and see what happens" (без decision plan)

### 11.3 Gray Zone (Requires Careful Wording)

⚠️ **Computational observations (allowed IF properly caveated):**
- "Observed localization-like pattern **in computational model**"
- "IPR contrast **for implemented operator** (interpretation pending)"
- "FSS trend **in finite-lattice toy geometry**"
- "Diagnostic **passed configured profile** (operator formula verification required)"

**Template for gray-zone claims:**
> [Computational observation] for [implemented operator/discretization]. Physical interpretation requires [operator decision / continuum validation / theoretical framework]. Current status: [computational milestone / pending verification / under review].

---

## 12. Recommended Next Step

**Final recommendation based on current evidence:**

### PRIMARY RECOMMENDATION: **OPERATOR_DECISION_REQUIRED_BEFORE_FIX**

**Rationale:**
1. Finding #2 (S³ Dirac asymmetry) has CRITICAL severity and affects core operator
2. Code implementation matches the formula cited in code comments as arXiv:1103.4097, but conflicts with test expectations (independent source verification required)
3. Cannot determine code correctness without independent verification of paper
4. Requires human decision: which convention (A or B) is appropriate for GeoSpectra's scientific question
5. Fix direction depends on convention choice (update tests OR fix code)

**Required human input:**
- Read arXiv:1103.4097 page 15 carefully
- Determine if Convention B (asymmetric) is correct interpretation
- Decide if Convention B serves GeoSpectra's scientific goals
- Choose: keep asymmetric (update tests) OR fix to symmetric (update code)

**Timeline:** 1-2 days (paper reading + decision meeting)

**Blocker for:** All heavy experiments (Gate 5, negative controls batches 3-6, new milestones)

**NOT a blocker for:** Lightweight analysis, documentation updates, test planning

---

### ALTERNATIVE OUTCOMES (depending on decision):

**If human decision: "Code correct (Convention B), tests wrong"**
→ Route to **Scenario 1** (documentation mismatch only)
→ Timeline: 2-3 days

**If human decision: "Code wrong (should be Convention A), fix needed"**
→ Route to **Scenario 3** (code bug affects Gate 4B)
→ Timeline: 7-10 days (includes v0.1.24 rerun)

**If human decision: "Inconclusive, needs domain expert"**
→ Escalate to **MANUAL_REVIEW_REQUIRED**
→ Contact: [theoretical physicist / representation theory expert / arXiv author]

---

## 13. Success Criteria for Resuming Heavy Experiments

**Before starting ANY of: Gate 5, negative controls batches 3-6, new gates, W-sweeps, cubic tests:**

### Critical Path (Must-Have):

- [ ] **S³ Dirac operator decision finalized**
  - Convention chosen (A or B) and documented
  - Either code fixed OR tests updated to match chosen convention
  - `docs/OPERATOR_SPECIFICATIONS.md` created with canonical formulas
  - Analytic spectrum unit tests added and passing

- [ ] **S¹ ring scaling convention documented**
  - Scale formula clarified (N/R vs N/(2πR))
  - ring(alpha=0) behavior documented
  - If fix applied: normalization verified and tested
  - Family-consistency interpretation updated (or documented as-is)

- [ ] **Rerun decision made**
  - If S³ Dirac changed → v0.1.24 mandatory rerun scheduled
  - If S¹ ring changed → rerun necessity decided
  - If only docs updated → interpretation unfrozen, no rerun

- [ ] **Claims and caveats updated**
  - `docs/CLAIMS_AND_CAVEATS.md` reflects operator audit lessons
  - Forbidden claims list includes operator uncertainties
  - Allowed claims templates provided
  - README.md status section updated

### Optional (Nice-to-Have before heavy experiments):

- [ ] Anderson 3D dense window fix applied (blocks Anderson work, not S³×S¹)
- [ ] S²×S¹ spurious zeros watch item investigated (low priority)
- [ ] Cross-validation against alternative S³ Dirac implementations (if available)
- [ ] External expert review of operator formulas (if accessible)

**Estimated total timeline:**

| Decision Outcome | Timeline |
|------------------|----------|
| Documentation mismatch only (Scenario 1) | 2-3 days |
| Code fix, no Gate 4B rerun (Scenario 2) | 3-5 days |
| Code fix, v0.1.24 rerun required (Scenario 3) | 7-10 days |
| Inconclusive, expert needed | 10-14 days |

---

## 14. Appendix — Detailed Diagnostic Evidence

### A. S³ Dirac Spectrum Verification (2026-05-25)

**Command:**
```python
from cc_toy_lab.spectral.dirac_s3 import build_s3_dirac_operator
import numpy as np

operator_0, _ = build_s3_dirac_operator(j_max=0, radius=1.0)
evals_0 = np.linalg.eigvalsh(operator_0)
# Result: [-2.5(×6), +1.5(×2)]

operator_1, _ = build_s3_dirac_operator(j_max=1, radius=1.0)
evals_1 = np.linalg.eigvalsh(operator_1)
# Result: [-3.5(×12), -2.5(×6), +1.5(×2), +2.5(×6)]
```

**Expected (tests/test_s3_s1_gate3c_triad_v0_1_20.py:30-35):**
- j_max=0: ±1.5 (symmetric)
- j_max=1: ±1.5, ±2.5 (symmetric)

**Actual (code dirac_s3.py:81-82):**
- j_max=0: [+1.5(×2), -2.5(×6)] (asymmetric)
- j_max=1: [+1.5(×2), +2.5(×6), -2.5(×6), -3.5(×12)] (asymmetric)

**Paper Citation (cited in code comment dirac_s3.py:54):**
> Code comments cite arXiv:1103.4097, page 15 for: eigenvalues k+1/2 and -(k+3/2) for k ≥ 1
> **Note:** Citation from code comments only — independent source verification required.

**Conclusion:** Code implements formula cited in comments as from arXiv:1103.4097 (asymmetric), tests expect symmetric (independent source verification required).

---

### B. S¹ Ring Scaling Verification (2026-05-25)

**Command:**
```python
from cc_toy_lab.spectral.s1_discretizations import (
    build_s1_ring_operator, _build_spectral_circle_operator
)
import numpy as np

N, alpha, R = 64, 0.5, 1.0
ring = build_s1_ring_operator(size=N, alpha=alpha, radius=R)
spectral = _build_spectral_circle_operator(size=N, alpha=alpha, radius=R)

evals_ring = np.linalg.eigvalsh(ring)
evals_spectral = np.linalg.eigvalsh(spectral)
# ring max: 63.9, spectral max: 31.5
# Ratio: 2.03 (audit report claimed 6.28 ≈ 2π)
```

**Code (s1_discretizations.py:13):**
```python
scale = float(size) / float(radius)  # N / R
```

**Code (s1_discretizations.py:79-80):**
```python
modes = np.fft.fftfreq(size, d=1.0 / size)
twisted_momenta = (modes + alpha) / radius  # (m + α) / R
```

**Issue:** Different scaling conventions. ring uses N/R (lattice count), spectral uses quantum number / R.

**Note:** Diagnostic eigenvalue ranges differ from audit report. Requires further investigation of parameter space.

---

### C. Anderson 3D Dense Window Verification (2026-05-25)

**Simulated Example:**
```python
import numpy as np

# Symmetric spectrum
spectrum_sym = np.linspace(-5, 5, 101)
median_value = spectrum_sym[len(spectrum_sym)//2]  # 0.00
closest_to_zero = spectrum_sym[np.argmin(np.abs(spectrum_sym))]  # 0.00
# Difference: 0.00 ✓

# Shifted spectrum
spectrum_shift = np.linspace(-10, 5, 101)
median_value = spectrum_shift[len(spectrum_shift)//2]  # -2.50
closest_to_zero = spectrum_shift[np.argmin(np.abs(spectrum_shift))]  # 0.05
# Difference: 2.55 ✗
```

**Code (anderson_3d.py:120):**
```python
center = len(values) // 2  # Median index, not E≈0
```

**Recommendation:** Replace with `center = np.argmin(np.abs(values))` for robust E≈0 targeting.

---

## 15. Metadata

**Дата создания:** 2026-05-25  
**Версия документа:** v0.1.23 (operator decision / fix plan)  
**Предыдущие документы:**
- `AGENT_HANDOFF_CONTEXT_v0.1.22.md` (2026-05-24)
- `OPERATOR_CONSISTENCY_AUDIT_v0.1.23.md` (2026-05-25)

**Статус проекта:** OPERATOR_DECISION_REQUIRED  
**Gate 4B:** FROZEN (interpretation), PRESERVED (outputs)  
**v0.1.22 Negative Controls:** PAUSED (batches 3-6)  
**Local execution:** PROHIBITED (thermal constraint)  
**Remote execution:** SUSPENDED (operator decision pending)

**Следующий документ (в зависимости от decision outcome):**
- Scenario 1 → `OPERATOR_DOCUMENTATION_UPDATE_v0.1.23.md`
- Scenario 2 → `OPERATOR_FIX_VALIDATION_v0.1.23.md`
- Scenario 3 → `GATE4B_RERUN_PLAN_v0.1.24.md`
- Scenario 5 → `OPERATOR_CORRECTION_NULL_RESULT_v0.1.24.md`

**Expected resolution:** 2-10 days (зависит от decision и rerun необходимости)

**Key files для operator decision:**
- `cc_toy_lab/spectral/dirac_s3.py` — implementation
- `tests/test_s3_s1_gate3c_triad_v0_1_20.py` — test expectations
- arXiv:1103.4097 page 15 — paper citation (external verification required)
- `docs/OPERATOR_SPECIFICATIONS.md` — to be created after decision

---

**Вердикт:** Operator decision документ готов. Не меняет код, не запускает эксперименты, не делает scientific verdict. Планирует decision path и предоставляет structured framework для resolution operator-level inconsistencies.

**Next human action:** Прочитать arXiv:1103.4097 page 15 + выбрать convention (A or B) + обновить соответствующие компоненты согласно chosen scenario.
