# Operator Consistency Audit — v0.1.23

**Дата:** 2026-05-25  
**Статус:** REMOTE_EXECUTION_PAUSED_OPERATOR_AUDIT_REQUIRED  
**Триггер:** External operator audit + canonical repo verification

---

## 1. Purpose

Verify whether implemented spectral operators match declared analytic formulas and pre-registered test expectations.

**Scope:**
- S²×S¹ product operator construction
- S³ Dirac operator spectrum structure
- S¹ discretization family scaling (ring/wilson_ring vs spectral_circle)
- 3D Anderson central window selection

**Method:**
- External audit claims verified against canonical repo
- Analytic spectrum comparisons
- Scale ratio measurements
- Code tracing vs documentation/test expectations

---

## 2. Trigger

**External audit reported (2026-05-25):**
- 4 potential operator-level inconsistencies (2 HIGH, 2 MEDIUM severity)
- Claims ranged from spurious kernel modes to spectrum formula mismatches

**Verification performed:**
- Canonical repo diagnostics executed
- Eigenvalue computations for claimed cases
- Cross-check against pre-registered test expectations
- Scale ratio measurements for S¹ families

---

## 3. Findings Summary

| # | Finding | Status | Severity | Evidence | Affected Scope | Recommended Action |
|---|---------|--------|----------|----------|----------------|-------------------|
| **1** | S²×S¹ spurious zeros from D_S2² + P_S1 cancellation | ❌ NOT_CONFIRMED | Needs Review | Canonical test: q=0, cutoff=1, s1_size=8, alpha=0, clean, spectral_circle → 0 near-zeros (not 4 as claimed). P_S1 eigenvalues: [-4.0, ~0, ~0, ...] do not produce exact cancellation with D_S2²=1. | S²×S¹ product (legacy) | Keep as watch item; do not treat as confirmed bug until reproducible |
| **2** | S³ Dirac spectrum asymmetric (±(k+0.5) expected, but +(k+0.5), -(k+1.5) implemented) | ✅ VERIFIED | **HIGH** | j_max=0: eigenvalues [-2.5(×6), +1.5(×2)] vs expected ±1.5 (symmetric). j_max=1: [-3.5, -2.5, +1.5, +2.5] vs expected ±[1.5, 2.5]. Code (dirac_s3.py:81-82) implements asymmetric branches: +(k+0.5), -(k+1.5). Test (test_s3_s1_gate3c_triad_v0_1_20.py:30) expects symmetric λ = ±(n + 3/2). | **Gate 4B v0.1.21 (S³×S¹)**, Gate 3C, all S³-based results | Freeze physical/theoretical interpretation of S³×S¹ results pending operator decision (code fix or documentation update) |
| **3** | S¹ ring/wilson_ring scale ~2π larger than spectral_circle | ✅ VERIFIED | **MEDIUM/HIGH** | N=64, alpha=0.5: ring max eigenvalue 3.14, spectral_circle 0.50 → ratio 6.28 ≈ 2π. **Additional:** ring(alpha=0) collapses to zero operator (anti-Hermitian structure + hermitization). spectral_circle uses (m+alpha)/R, ring uses size/radius derivative scale. | Gate 4B family-consistency claims (ring vs spectral_circle vs wilson_ring), S¹ discretization comparisons | Audit S¹ ring scaling convention; decide if physical or units mismatch. Review Wilson term scale separately. Clarify before using "family consistency" as strong evidence |
| **4** | 3D Anderson dense path uses median index, not E=0 | ✅ VERIFIED | **MEDIUM** | Dense path (anderson_3d.py:120): `center = len(values)//2` (median index). Sparse path (anderson_3d.py:127): `sigma=0.0` (closest to E=0). For shifted spectrum: median ≠ E=0 (example: -2.42 vs 0.00). | 3D Anderson quick diagnostics (L≤6), anderson_3d baseline tests | Fix dense window selection to match E=0 before cubic/baseline Anderson comparisons |

---

## 4. Impact on Existing Results

### Gate 4B v0.1.21 (S³×S¹ Finite-Size Scaling)

**Статус результатов:** RAW OUTPUTS PRESERVED (IMMUTABLE)

**Что остаётся валидным:**
- ✅ Вычислительные выходы Gate 4B (216 cases, eigenvalues, eigenvectors, IPR values) остаются сохранёнными
- ✅ Numerical consistency: все расчёты выполнены на одном операторе (consistency внутри Gate 4B)
- ✅ Finite-size scaling trend (3.76× → 24.90×) остаётся фактом для **implemented operator**
- ✅ Family consistency (3/3 families PASS) остаётся фактом для **implemented discretizations**
- ✅ Hermiticity tests (Gate 1) остаются валидными — operator Hermitian как заявлено

**Что требует замораживания интерпретации:**

**❌ FORBIDDEN до operator decision:**
- "Gate 4B validates S³×S¹ **theoretical** operator" — operator formula не соответствует expected spectrum
- "S³ Dirac spectrum проявляет expected ±(k+1/2) structure" — actual spectrum asymmetric
- "Family consistency подтверждает geometric robustness" — ring масштаб в 2π раз отличается от spectral_circle
- "Results generalize to continuum S³×S¹" — implemented operator может не быть правильным discretization
- Любые claims про **physical interpretation** S³×S¹ results

**✅ ALLOWED (careful phrasing):**
- "Gate 4B показал 7.15× IPR contrast для **implemented S³×S¹ operator**"
- "Finite-size scaling trend strengthening для **implemented discretization**"
- "Hermiticity и dimension formula verified"
- "Computational consistency внутри Gate 4B grid"
- "Further operator validation required перед физической интерпретацией"

**Рекомендуемая формулировка:**
> Gate 4B v0.1.21 представляет вычислительно корректные результаты для **implemented S³×S¹ operator** с сохранёнными numerical outputs. Физическая и теоретическая интерпретация этих результатов заморожена до resolution оператор-уровня inconsistency (S³ Dirac spectrum asymmetry, S¹ ring scaling). Raw data сохранены для повторного анализа после operator decision.

### v0.1.22 Negative Controls

**Статус:** REMOTE EXECUTION PAUSED

**Обоснование:**
- Negative controls построены на тех же S³×S¹ operators с S³ Dirac spectrum issue
- `scrambled_geometry` и `broken_wilson` controls используют `build_s3_s1_product_operator()` (затронуто Finding #2)
- S¹ ring/wilson_ring scale issue (Finding #3) влияет на `broken_wilson` control интерпретацию
- Batches 1-2 (18 cases) уже выполнены — outputs сохраняются как implemented-operator baseline
- Batches 3-6 (36 cases) **не запускаются** до operator decision

**Действие:**
- ❌ НЕ продолжать remote execution batches 3-6
- ✅ Сохранить batches 1-2 results как implemented-operator reference
- ⏸️ Пауза до operator consistency resolution

### 3D Anderson Baseline Tests

**Статус:** FIX REQUIRED перед использованием

- Finding #4 (dense window median-index issue) влияет на quick diagnostics (L≤6)
- anderson_3d.py должен быть исправлен перед cubic/baseline Anderson comparisons
- Не блокирует S³×S¹ работу, но блокирует 3D Anderson reference

---

## 5. Immediate Decision

**Вердикт:** `REMOTE_EXECUTION_PAUSED_OPERATOR_AUDIT_REQUIRED`

**Rationale:**
- 3/4 external findings verified (1 HIGH, 2 MEDIUM)
- HIGH-severity finding (#2) влияет на центральный S³×S¹ operator interpretation
- Further heavy experiments (Gate 5, negative controls batches 3-6) могут accumulate results на potentially incorrect operator
- Operator-level issue требует design decision (code fix vs documentation update), не просто bug patch

**Recommended pause duration:** до operator decision (estimated 1-3 days analysis + decision)

---

## 6. Recommended Next Actions

### Priority A — Immediate (Before Any Further Experiments)

**A1. Operator Decision Meeting**
- **Question:** Is S³ Dirac asymmetric spectrum (+(k+0.5), -(k+1.5)) **correct** or **bug**?
- **Sources to check:**
  - arXiv:1103.4097 page 15 (referenced in code comments)
  - SU(2) Dirac on S³ analytic formula
  - Pre-registered test expectations (test_s3_s1_gate3c_triad_v0_1_20.py:30)
- **Decision tree:**
  - If **code correct:** update tests, documentation, pre-registration expectations
  - If **code wrong:** fix dirac_s3.py, rerun Gate 4B as v0.1.24, archive v0.1.21 as "implemented-operator baseline"

**A2. Add Analytic Spectrum Unit Tests**
- `test_s3_dirac_analytic_spectrum.py`:
  ```python
  def test_s3_dirac_eigenvalues_vs_analytic():
      # Compare numerical eigenvalues to expected ±(k+1/2) or +(k+1/2), -(k+3/2)
      # Include expected degeneracies
      # MUST match paper/theory, not just pass existing tests
  ```
- Gate spectrum tests до любых heavy experiments

**A3. S¹ Ring Scaling Audit**
- **Question:** Is ring scale = size/radius **intended** (2π factor vs spectral_circle)?
- **Check:**
  - Physical meaning of ring derivative discretization
  - Wilson term scale convention
  - Whether "family consistency" should normalize scales or test raw operators
- **Action:** Document scaling convention; decide if fix needed or WAI (working as intended)

**A4. Fix 3D Anderson Dense Window**
- Patch `anderson_3d.py:120` to use E≈0 selection, not median index
- Add test for shifted spectrum case
- Not urgent for S³×S¹ work, but blocks Anderson baseline comparisons

### Priority B — After Operator Decision

**B1. If S³ Dirac Code Is Correct:**
- Update all test expectations (test_s3_s1_gate3c_triad_v0_1_20.py)
- Update documentation (arXiv reference clarity)
- Update pre-registration language
- Unfreeze Gate 4B interpretation (с правильной symmetric/asymmetric формулировкой)
- Resume negative controls batches 3-6
- Proceed to Gate 5 with correct operator understanding

**B2. If S³ Dirac Code Is Wrong:**
- Fix `dirac_s3.py` eigenvalue formula
- Rerun Gate 1 Hermiticity tests (should still pass)
- Rerun Gate 4B as v0.1.24 (новый operator, новые results)
- Archive Gate 4B v0.1.21 as "implemented-operator baseline (asymmetric Dirac)"
- Rerun negative controls batches 1-6 (fresh start)
- Update all affected reports with v0.1.24 numbers

**B3. S¹ Scaling Decision:**
- If fix needed: normalize ring to match spectral_circle physical scale
- If WAI: document convention; clarify "family consistency" не означает identical scales
- Rerun affected gates если normalization changes results significantly

### Priority C — Documentation Hardening

**C1. Operator Specification Documents**
- Create `docs/OPERATOR_SPECIFICATIONS.md`:
  - S³ Dirac: expected eigenvalues, degeneracies, references
  - S¹ discretizations: scale conventions, normalization choices
  - Product construction: tensor product formula, disorder application
- Make this THE reference для любых operator changes

**C2. Pre-Registration Updates**
- Update future pre-registrations с explicit operator spectrum expectations
- Include analytic formula checks в gate protocols

**C3. Forbidden Claims List Update**
- Add to `docs/CLAIMS_AND_CAVEATS.md`:
  - "Validated theoretical S³×S¹ operator" (pending operator audit)
  - "Physical interpretation confirmed" (pending operator decision)

---

## 7. Forbidden Actions (CRITICAL — Non-Negotiable)

### Строго запрещено до operator decision:

**❌ Execution:**
- Run Gate 5 (any scale, any grid)
- Continue v0.1.22 negative controls batches 3-6
- Run any S³×S¹ heavy experiments (>100 cases)
- Start v0.1.23 или любой новый milestone

**❌ Interpretation:**
- Claim "S³×S¹ validated" или "S³×S¹ operator confirmed"
- Interpret Gate 4B results как theoretical S³×S¹ properties (только как implemented-operator results)
- Use "family consistency" как strong evidence без addressing scale mismatch
- Generalize к continuum limit
- Make physical claims про S³ Dirac zero modes

**❌ Data Manipulation:**
- Delete или modify Gate 4B raw outputs (reports/RUNS/gate_4b_v0.1.21/)
- Rewrite Gate 4B reports (preserve original, add caveats separately)
- Modify test expectations чтобы match current code без decision

**❌ External Communication:**
- Submit preprints или papers про S³×S¹ results
- Present Gate 4B как validated theoretical result
- Share negative controls results как operator validation

### Разрешено (с осторожностью):

**✅ Analysis:**
- Read и analyze existing Gate 4B outputs
- Compare implemented operator spectrum к analytic formulas
- Research arXiv references для operator formulas
- Draft operator decision documents

**✅ Testing:**
- Add analytic spectrum unit tests
- Run small operator verification tests (<10 cases)
- Test proposed operator fixes на toy cases

**✅ Documentation:**
- Update caveats в existing reports (без изменения raw results)
- Write operator audit documents
- Update CLAIMS_AND_CAVEATS.md

---

## 8. Communication Protocol

### Internal (Team/Advisors)

**Status message:**
> GeoSpectra Lab v0.1.22 remote execution paused due to operator consistency audit. External review identified potential S³ Dirac spectrum formula mismatch (verified HIGH severity). Gate 4B computational outputs preserved; interpretation frozen pending operator decision. Estimated resolution: 1-3 days. No data loss. Careful scientific diligence in action.

### External (If Asked)

**Public-facing statement:**
> We are conducting an operator-level consistency audit following external code review. Computational results remain valid for the implemented operators; physical interpretation is under review. This is standard scientific verification practice. Updates will follow operator decision.

**What NOT to say:**
- "We found bugs in our operators" (may be documentation mismatch, not bug)
- "Gate 4B results are wrong" (computational results valid for implemented operator)
- "We're restarting the project" (only targeted fixes needed)

---

## 9. Success Criteria for Resuming Execution

**Before resuming v0.1.22 batches 3-6 or starting any new heavy experiments:**

- [ ] S³ Dirac operator decision finalized (code fix OR documentation update)
- [ ] Analytic spectrum unit tests added and passing
- [ ] S¹ ring scaling convention documented (fix OR WAI documented)
- [ ] If code fixes applied: affected gates rerun with corrected operators
- [ ] Documentation updated with correct operator formulas
- [ ] CLAIMS_AND_CAVEATS.md updated with operator audit lessons
- [ ] Team consensus: operator consistency sufficient for heavy experiments

**Estimated timeline:** 2-5 days (1 day analysis, 1 day decision, 0-3 days reruns if needed)

---

## 10. Appendix — Detailed Evidence

### Finding #2: S³ Dirac Spectrum Mismatch (HIGH)

**Code (cc_toy_lab/spectral/dirac_s3.py:81-82):**
```python
eigenvalue_pos = (k + 0.5) / radius  # +(k + 1/2) / R
eigenvalue_neg = -(k + 1.5) / radius  # -(k + 3/2) / R
```

**Test Expectation (tests/test_s3_s1_gate3c_triad_v0_1_20.py:30):**
```python
# Analytical SU(2) Dirac on S³:
# λ = ±(n + (2j+1)/2) / R
# For spin-1/2 (j=1/2): λ = ±(n + 3/2) / R
# Expected lowest eigenvalues (R=1):
# ±1.5, ±2.5, ±3.5, ±4.5, ...
```

**Verification Output:**
```
j_max=0 eigenvalues: [-2.5(×6), +1.5(×2)]
Expected: ±1.5 (symmetric)

j_max=1 eigenvalues: [-3.5, -2.5, +1.5, +2.5]
Expected: ±[1.5, 2.5] (symmetric)
```

**Contradiction:**
- Code implements **asymmetric** branches: +(k+0.5), -(k+1.5)
- Test expects **symmetric**: ±(k+0.5)
- Difference: negative branch shifted down by 1

**Paper Reference (code comment line 64):**
> arXiv:1103.4097, page 15: Positive λ₊ = +(k + 1/2) / R, Negative λ₋ = -(k + 3/2) / R

**Conclusion:** Code matches paper citation (asymmetric), but test expects symmetric. Either:
- Paper formula wrong / misread → fix code
- Test expectation wrong → fix test
- Different conventions → clarify documentation

### Finding #3: S¹ Ring Scaling (MEDIUM/HIGH)

**spectral_circle (s1_discretizations.py:79):**
```python
modes = np.fft.fftfreq(size, d=1.0 / size)  # Integer modes
twisted_momenta = (modes + alpha) / radius  # Scale: 1/R
```

**ring (s1_discretizations.py:13-14):**
```python
scale = float(size) / float(radius)  # Scale: N/R
operator = (-0.5j * scale) * (shift - shift.conj().T)
```

**Verification Output (N=64, alpha=0.5, R=1.0):**
```
spectral_circle max eigenvalue: 0.50
ring max eigenvalue: 3.14
Ratio: 6.28 ≈ 2π
```

**Physical Interpretation:**
- spectral_circle: momentum eigenvalues (m+α)/R — natural quantum number
- ring: finite-difference derivative scale N/R — lattice spacing related

**Issue:** Comparing ring vs spectral_circle "family consistency" без accounting for 2π scale difference может mislead interpretation.

**Additional:** ring(alpha=0) collapses to zero operator because:
```python
operator = -0.5j * scale * (shift - shift.H)  # Anti-Hermitian
hermitize: 0.5 * (A + A†) = 0.5 * (A - A) = 0  # If A anti-Hermitian
```

### Finding #4: 3D Anderson Dense Window (MEDIUM)

**Dense path (anderson_3d.py:118-124):**
```python
values, vectors = np.linalg.eigh(hamiltonian.toarray())
center = len(values) // 2  # Median index
half = min(eigen_count // 2, center, len(values) - center)
start = max(0, center - half)
stop = min(len(values), center + half)
return values[start:stop], vectors[:, start:stop]
```

**Sparse path (anderson_3d.py:127):**
```python
values, vectors = eigsh(hamiltonian, k=k, sigma=0.0, which="LM")
# sigma=0.0: find eigenvalues near E=0
```

**Issue:** For symmetric spectrum, median ≈ E=0. For shifted spectrum (e.g., non-zero onsite disorder average), median ≠ E=0.

**Example:**
```
Shifted spectrum: [-10, -9, ..., 5]
Median: E ≈ -2.5
Near E=0: E ≈ 0.0
Difference: 2.5σ (significant for band-center diagnostics)
```

---

## 11. Metadata

**Дата аудита:** 2026-05-25  
**Метод:** External operator audit verification + canonical repo diagnostics  
**Verified findings:** 3/4 (1 HIGH, 2 MEDIUM confirmed; 1 NOT_CONFIRMED)  
**Affected gates:** Gate 4B v0.1.21 (interpretation), v0.1.22 Negative Controls (execution paused)  
**Статус проекта:** OPERATOR AUDIT IN PROGRESS (no data loss, computational integrity preserved)

**Документы:**
- `AUDIT_VERIFICATION_REPORT.md` (2026-05-24) — 10 code bugs verification
- `CODE_MATERIALITY_AUDIT_v0.1.22.md` (2026-05-24) — bug triage by active pipeline
- `CODE_AUDIT_HARDENING_v0.1.22.md` (2026-05-25) — 10-layer trust audit
- `OPERATOR_CONSISTENCY_AUDIT_v0.1.23.md` (этот документ) — operator-level verification

**Следующий документ:** `OPERATOR_DECISION_v0.1.23.md` (после operator formula resolution)

---

**Вердикт:** Честная научная диligence. Оператор-уровень inconsistency выявлен рано, до масштабного accumulation potentially incorrect results. Gate 4B outputs сохранены как implemented-operator baseline. Decision required перед продолжением.
