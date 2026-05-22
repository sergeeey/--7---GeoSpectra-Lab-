# S³×S¹ Gate 4B FSS & Robustness Pre-Registration — v0.1.21 (Metric-Corrected)

**Дата:** 2026-05-22 10:30 Almaty  
**Статус:** PRE-REGISTERED (before execution)  
**Версия:** v0.1.21 — Metric-corrected rerun of v0.1.20  
**Цель:** Gate 4B finite-size scaling with corrected TRUE IPR metric  
**Предшествующий статус:** Gate 4A v0.1.20 WEAK_OR_INCONCLUSIVE (primary metric invalid)  

---

## 0. Version History & Motivation

**Gate 4A v0.1.20 execution (2026-05-21 to 2026-05-22):**
- **Status:** COMPLETED (216/216 cases, 0 failures)
- **Critical finding:** IPR metric implementation mismatch discovered post-execution
- **Pre-registered metric:** IPR = Σ|ψᵢ|⁴ (eigenvector-based)
- **Implemented metric:** mean_low_ipr = mean(bottom 10% eigenvalues)
- **Root cause:** `np.linalg.eigvalsh(H)` used (eigenvalues only) instead of `eigh` (eigenvalues + eigenvectors)
- **Impact:** Primary verdict criterion (≥2.0× IPR contrast) unmeasurable
- **Verdict:** WEAK_OR_INCONCLUSIVE (based on secondary metric r-statistic only)
- **Documentation:** S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md

**v0.1.21 changes:**
1. ✅ **Metric correction:** Implement true eigenvector-based IPR = Σ|ψᵢ|⁴
2. ✅ **Code change:** `eigvalsh → eigh` in run_gate4_batched.py line 216
3. ✅ **Unit tests:** 3 ground-truth test cases (localized, uniform, random)
4. ✅ **Storage policy:** Save true_ipr scalar per case, optional eigenvector storage
5. ✅ **Runtime benchmark:** Estimate 16h for 216 cases before full commit
6. ✅ **Grid unchanged:** Same 216-case grid as v0.1.20 (no parameter changes)
7. ✅ **Thresholds unchanged:** Same decision rules and PASS criteria (no post-hoc tuning)

**What does NOT change:**
- ❌ Scientific grid parameters (families, W, sizes, j_max, seeds) — LOCKED
- ❌ Decision rules and PASS thresholds — LOCKED
- ❌ Claim language (allowed/forbidden statements) — LOCKED
- ❌ Protocol immutability rules — LOCKED

**Critical constraint:**
> **NO PASS CLAIM until metric-corrected full analysis complete.**
> Even if v0.1.21 results look strong, verdict requires full 216-case execution with corrected metric.

---

## 1. Purpose

**Gate 4B tests whether the Gate 3C W=20 finite-lattice localization signal is robust under:**
1. Finite-size scaling (s1_size = 16, 32, 64, 128)
2. Expanded family coverage (spectral_circle, ring, wilson_ring)
3. Level-spacing diagnostics (adjacent gap ratio r-statistic)
4. Intermediate disorder strength (W=12)

**Scientific question:**
Does the W=20 absolute IPR contrast signal persist, strengthen, or saturate across increasing S¹ discretization sizes, or does it weaken/collapse?

**Scope:**
- Finite-lattice only (no thermodynamic limit claim)
- Anderson disorder only (no general disorder claim)
- S³×S¹ only (no FL generalization)
- Pre-registered grid only (no post-hoc expansion without new pre-registration)

---

## 2. Protocol Immutability (CRITICAL)

**This pre-registration protocol becomes LOCKED after git commit.**

**Forbidden changes after commit:**
1. ❌ Grid parameters: families, W values, sizes, j_max, seeds.
2. ❌ Decision rules: PASS/FAIL thresholds and verdict conditions.
3. ❌ Metric definitions: primary/secondary split, formulas, spectral windows.
4. ❌ Claim language: allowed/forbidden statements.

**Allowed changes after commit:**
1. ✅ Implementation bugfixes, only if they fix broken execution rather than change experimental design.
   - Must be documented in the results report under "Protocol Deviations".
   - Must justify why the bugfix does not invalidate the pre-registered protocol.
2. ✅ Runtime optimizations, only if they preserve the full grid, metrics, thresholds, and decision rules.
   - Must be documented in "Protocol Deviations".

**If any design change is needed, create a new pre-registration version:**
- Example: `S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.22.md`
- The original version remains in git history.
- Results must cite the exact protocol version used.

**Violation of protocol immutability makes the results exploratory, not confirmatory.**

---

## 3. Non-Goals (Explicit Forbidden Claims)

**Gate 4B does NOT and CANNOT establish:**

1. ❌ **Physical compactification** — finite-lattice evidence ≠ continuum physics
2. ❌ **FL generalization** — S³×S¹ result does not prove S²×S¹, S⁷×S¹, or arbitrary products
3. ❌ **W=20 optimality** — contrast maximization NOT tested, W=20 is exploratory choice
4. ❌ **Thermodynamic limit** — finite N ≤ 3712 (at s1_size=128, j_max=3) ≠ N→∞
5. ❌ **"S³×S¹ validated"** — validation theater forbidden, use "finite-lattice robustness evidence"
6. ❌ **Threshold tuning** — decision rules fixed before results, no post-hoc adjustment
7. ❌ **Family cherry-picking** — cannot use partial/family-only pass as full pass
8. ❌ **Ratio IPR verdict** — ratio metric deprecated, never verdict-driving
9. ❌ **v0.1.20 result reinterpretation** — eigenvalue-based metric ≠ true IPR, cannot retrofit

**If any forbidden claim appears in results or discussion → immediate correction required.**

---

## 4. Prior Evidence (Context for Gate 4B)

**Pre-Gate 4B state of knowledge:**

### 4.1 Gate 3C Confirmatory Replication (v0.1.20)
- **Date:** 2026-05-21 09:00–10:00
- **Pre-registration:** S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md (2026-05-10)
- **Grid:** W=20 × 3 families × 216 parameter combinations = 648 cases
- **Metric status:** ⚠️ Unknown (may also use eigenvalue proxy — requires audit)
- **Result:** 2.68x "IPR contrast" (if eigenvalue-based, NOT true IPR)
- **Verdict:** PASS_WITH_CAVEATS (validity pending metric audit)
- **Action required:** Audit Gate 3C metric implementation before citing as prior evidence

### 4.2 Gate 4A v0.1.20 Execution
- **Date:** 2026-05-21 to 2026-05-22
- **Grid:** 216 cases (9 batches × 24 cases)
- **Completion:** 216/216 cases, 0 failures
- **Runtime:** 96.1 minutes
- **Metric:** ❌ mean_low_ipr = mean(eigenvalues) — NOT true IPR
- **Valid metrics:**
  - ✅ r-statistic: W=0: 0.605 → W=20: 0.437 (shift toward Poisson)
  - ✅ Eigenvalue trend: W=0: -27.60 → W=20: -94.23 (lowering consistent with bound states)
- **Verdict:** WEAK_OR_INCONCLUSIVE
- **Reason:** Primary metric (IPR contrast) unmeasurable, verdict based on r-statistic only
- **Documentation:** 
  - S3_S1_GATE4_FSS_RESULTS_v0.1.20.md
  - S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md
  - GATE4_TRUE_IPR_RECOVERY_CHECK_v0.1.20.md

### 4.3 Recovery Analysis
- **Question:** Can true IPR be recomputed from v0.1.20 artifacts without rerun?
- **Finding:** Eigenvectors were NEVER computed in runtime
  - Code used `np.linalg.eigvalsh(H)` (eigenvalues only)
  - No binary vector files (.npz, .pkl, .h5) saved
  - JSON outputs contain only scalar summaries
- **Verdict:** FULL_RERUN_REQUIRED
- **Estimate:** ~16 hours for 216 cases (10× overhead for eigenvector computation)

### 4.4 Codebase-Wide IPR Audit
- **Scope:** All scripts using `mean_low_ipr` field
- **Finding:** 
  - ✅ 2 scripts compute true IPR correctly (S¹ calibration pilots)
  - ❌ 5 scripts confirmed eigenvalue proxy (Gate 3, Gate 4, disorder sweep)
  - ⚠️ 7 scripts unclear (Anderson 3D benchmarks, README tables)
  - ❌ 0 unit tests for IPR validation
- **Action required:** README.md IPR tables require verification before citing
- **Documentation:** IPR_IMPLEMENTATION_AUDIT_v0.1.20.md

---

## 5. Pre-Registered Grid (Gate 4B — Same as v0.1.20)

**Grid parameters (UNCHANGED from v0.1.20):**

```yaml
geometry: S3xS1
families:
  - spectral_circle
  - ring
  - wilson_ring

disorder_strengths:
  - W: 0      # No disorder (localized baseline, geometric effect)
  - W: 12     # Intermediate disorder
  - W: 20     # Gate 3C verified strength

s1_discretization_sizes:
  - 16        # Small (baseline)
  - 32        # Medium
  - 64        # Gate 3C size
  - 128       # Large

j_max_values:
  - 2         # Lower spectral density
  - 3         # Gate 3C standard

random_seeds:
  - 123
  - 456
  - 789

total_cases: 3 families × 3 W × 4 sizes × 2 j_max × 3 seeds = 216 cases
```

**Why grid unchanged:**
- v0.1.21 is a METRIC CORRECTION, not a new experiment
- Changing grid would invalidate comparison with v0.1.20 execution robustness
- Scientific design is sound, implementation was flawed

**Excluded from Gate 4B:**
- `s1_size=256` — runtime prohibitive (would require 48+ hours)
- `W values outside {0,12,20}` — focus on verified W=20 and controls
- `j_max=1` — low spectral density, not scientifically interesting
- `Additional families` — current 3 families cover design space

---

## 6. Metrics (Pre-Registered, Metric Formula CORRECTED)

### 6.1 Primary Metrics (Verdict-Driving)

**1. Absolute IPR Contrast (CORRECTED METRIC)**

**Definition (TRUE IPR):**

```python
# For each eigenstate ψᵢ (eigenvector):
IPR_i = Σⱼ |ψᵢⱼ|⁴  # Sum over all Hilbert space basis states j

# Mean IPR over bottom 10% of spectrum:
low_indices = np.argsort(eigenvalues)[: int(0.1 * N)]
IPRs = [np.sum(np.abs(eigenvectors[:, i])**4) for i in low_indices]
mean_low_ipr = np.mean(IPRs)

# Contrast:
contrast = mean_low_ipr(W=20) / mean_low_ipr(W=0)
```

**Physical interpretation:**
- IPR = 1.0 → fully localized (δ-function)
- IPR = 1/N → fully delocalized (uniform over N states)
- IPR ∈ (1/N, 1) → partially localized

**Spectral window:** Bottom 10% of eigenspectrum (same as v0.1.20)

**Threshold:** ≥2.0× for PASS_WITH_CAVEATS (UNCHANGED)

**Rationale:** 
- Gate 3C validated 2.68× contrast (if metric is corrected — pending audit)
- Conservative threshold below prior result
- Allows comparison with v0.1.20 r-statistic evidence

**Gate 4B question:** Does true IPR contrast persist, strengthen, or weaken as s1_size increases?

---

**2. Finite-Size Trend**
- **Definition:** Slope and stability of IPR contrast vs s1_size
- **Possible outcomes:**
  - **Saturating/strengthening:** Contrast stable or increasing → robust signal
  - **Weakening but stable:** Contrast decreases but remains >2.0× → finite-size effect, still localized
  - **Collapsing:** Contrast drops to <1.5× → artifact interpretation
- **Verdict impact:** Saturating/strengthening → PASS; weakening but stable → PASS with stronger caveat; collapsing → FAIL

---

**3. Family Consistency**
- **Definition:** How many families show W=20 contrast ≥2.0×?
- **Threshold:** ≥2/3 families must pass (no single-family carry)
- **Rationale:** Prevents cherry-picking, ensures robustness across discretization choices

---

**4. Level-Spacing Adjacent Gap Ratio (r-statistic)**
- **Definition:** `r = min(δₙ, δₙ₊₁) / max(δₙ, δₙ₊₁)` where `δₙ = Eₙ₊₁ - Eₙ`
- **Expected behavior:**
  - W=0: r ≈ 0.53 (GOE, ergodic)
  - W=20: r → 0.39 (Poisson, localized)
- **Gate 4B test:** Does r-statistic shift confirm localization interpretation of IPR contrast?
- **Verdict impact:** r-shift contradicts IPR → FAIL; r-shift supports IPR → PASS; r-ambiguous → weaken verdict
- **Note:** r-statistic computation UNCHANGED (eigenvalue gaps only, no eigenvectors needed)

---

### 6.2 Secondary Metrics (Diagnostic, Not Verdict-Driving)

**5. W=12 Intermediate Response**
- **Purpose:** Check monotonicity (W=0 < W=12 < W=20 in IPR)
- **Not verdict-driving:** W=12 failure does NOT invalidate W=20 result
- **Use:** Sanity check, helps interpret finite-size trend

**6. Runtime & Numerical Stability**
- **Purpose:** Detect implementation issues, guide future grid design
- **Tracked:** Eigenvalue solver convergence, matrix condition numbers
- **Not verdict-driving:** Stability issues → INCOMPLETE, not FAIL

**7. Eigenvalue Trend (v0.1.20 diagnostic)**
- **Definition:** Mean of bottom 10% eigenvalues
- **Purpose:** Compare with v0.1.20 eigenvalue-based metric
- **Status:** Diagnostic only, NOT verdict-driving
- **Use:** Verify that eigenvector IPR trend differs from eigenvalue trend

**8. Ratio IPR (deprecated, backward compatibility only)**
- **Definition:** `IPR_ratio = IPR(localized) / IPR(ergodic)`
- **Status:** Retired in Gate 3C (Wilson/s64 caveat exposed family dependence)
- **Use:** Report for comparison with prior results only
- **NEVER verdict-driving:** Ratio metric does NOT contribute to PASS/FAIL decision

---

## 7. Implementation Changes (v0.1.21 Specific)

### 7.1 Code Changes Required

**File:** `scripts/run_gate4_batched.py`

**Line 216 (CHANGE FROM):**
```python
eigvals = np.linalg.eigvalsh(H)
```

**Line 216 (CHANGE TO):**
```python
eigvals, eigvecs = np.linalg.eigh(H)
```

**Lines 220-221 (CHANGE FROM):**
```python
low_eigvals = eigvals[: int(0.1 * N)]
mean_low_ipr = float(np.mean(low_eigvals))
```

**Lines 220-230 (CHANGE TO):**
```python
# Sort by eigenvalue, get bottom 10% indices
low_indices = np.argsort(eigvals)[: int(0.1 * N)]
low_eigvecs = eigvecs[:, low_indices]

# Compute true IPR for each low eigenstate
iprs = []
for i in range(low_eigvecs.shape[1]):
    psi = low_eigvecs[:, i]
    ipr = np.sum(np.abs(psi)**4)
    iprs.append(ipr)

mean_low_ipr = float(np.mean(iprs))  # Now TRUE mean IPR
```

**Additional diagnostic (optional but recommended):**
```python
# Store eigenvalue-based metric for comparison with v0.1.20
mean_low_eigenvalue = float(np.mean(eigvals[low_indices]))
```

---

### 7.2 Unit Tests (REQUIRED before full execution)

**File:** `tests/test_ipr_metric.py`

**Test 1: Fully localized state (δ-function)**
```python
def test_ipr_fully_localized():
    """IPR of δ-function should be 1.0"""
    N = 100
    psi = np.zeros(N)
    psi[0] = 1.0  # Localized at site 0
    ipr = np.sum(np.abs(psi)**4)
    assert np.isclose(ipr, 1.0, atol=1e-10)
```

**Test 2: Fully delocalized state (uniform)**
```python
def test_ipr_fully_delocalized():
    """IPR of uniform state should be 1/N"""
    N = 100
    psi = np.ones(N) / np.sqrt(N)  # Normalized uniform state
    ipr = np.sum(np.abs(psi)**4)
    expected_ipr = 1.0 / N
    assert np.isclose(ipr, expected_ipr, rtol=1e-6)
```

**Test 3: Random normalized state**
```python
def test_ipr_random_normalized():
    """IPR of random state should be between 1/N and 1"""
    N = 100
    np.random.seed(42)
    psi = np.random.randn(N) + 1j * np.random.randn(N)
    psi /= np.linalg.norm(psi)  # Normalize
    ipr = np.sum(np.abs(psi)**4)
    assert 1.0 / N <= ipr <= 1.0, f"IPR={ipr} outside valid range [1/N, 1]"
```

**Required before execution:**
- All 3 tests must pass: `pytest tests/test_ipr_metric.py -v`
- No test skips or xfails allowed
- CI must run tests before batched execution starts

---

### 7.3 Storage Policy

**Per-case JSON output (same structure as v0.1.20):**
```json
{
  "case_id": int,
  "family": str,
  "disorder_strength": int,
  "s1_size": int,
  "j_max": int,
  "seed": int,
  "runtime_sec": float,
  "mean_low_ipr": float,          # ← NOW true IPR (eigenvector-based)
  "mean_low_eigenvalue": float,   # ← NEW diagnostic (for v0.1.20 comparison)
  "r_stat": float,
  "r_stat_available": bool,
  "r_stat_reason": null | str,
  "error": null | str
}
```

**Eigenvector storage (OPTIONAL):**
- **Default:** Do NOT save full eigenvectors (storage prohibitive: ~23 GB uncompressed for 216 cases)
- **If needed for future analysis:** Save bottom 10% eigenvectors per case as compressed .npz
  ```python
  np.savez_compressed(f"case_{case_id}_eigvecs.npz", 
                      eigvals=low_eigvals, 
                      eigvecs=low_eigvecs)
  ```
- **Rationale:** IPR scalar sufficient for verdict, eigenvectors recoverable if full rerun needed

**Field naming:**
- `mean_low_ipr` field name UNCHANGED (backward compatibility)
- **Documentation required:** Results report must state:
  > "v0.1.21: mean_low_ipr = true eigenvector-based IPR"
  > "v0.1.20: mean_low_ipr = mean eigenvalue (NOT true IPR)"

---

### 7.4 Runtime Benchmark (REQUIRED before full grid)

**Before executing 216-case grid:**

**Step 1: Single-case benchmark**
```bash
python scripts/run_gate4_batched.py \
  --family spectral_circle \
  --disorder 20 \
  --s1-size 64 \
  --j-max 3 \
  --seed 123 \
  --benchmark
```
- Measure wall-clock time with eigenvectors
- Compare to v0.1.20 time without eigenvectors (from timing.json)
- Compute overhead ratio: `overhead = time_v0.1.21 / time_v0.1.20`

**Step 2: Extrapolate to full grid**
```
estimated_total_time = overhead × 96.1 minutes (v0.1.20 actual runtime)
```

**Decision rule:**
- If `estimated_total_time < 24 hours` → proceed with full 216-case grid
- If `24 hours ≤ estimated_total_time < 48 hours` → batch over 2 days
- If `estimated_total_time ≥ 48 hours` → reduce grid:
  1. Drop s1_size=128 (keep 16/32/64)
  2. Reduce seeds to {123, 456} (drop 789)
  3. Document as protocol deviation

**Estimate from recovery check:** ~16 hours (10× overhead, conservative)

**Action:** Execute benchmark, commit benchmark results before full run

---

## 8. Decision Rules (Fixed Before Execution, UNCHANGED from v0.1.20)

**Four mutually exclusive verdicts:**

### 8.1 GATE4_FSS_PASS_WITH_CAVEATS

**Conditions (ALL must hold):**
1. **Aggregate W=20 contrast ≥2.0×** across all families and sizes
2. **Family consistency:** ≥2/3 families show W=20 contrast ≥2.0× independently
3. **No single-family domination:** No one family carries >80% of aggregate contrast
4. **Finite-size trend:** Contrast stable, saturating, or strengthening (not collapsing)
5. **Level-spacing supports localization:** r-statistic shift toward Poisson at W=20, or at least not contradicting IPR
6. **No broad failure cluster:** No systematic failures across all families at large sizes
7. **Controls pass:** W=0 baseline stable, no control failures

**Claim allowed:**
> "S³×S¹ Gate 4B supports finite-lattice robustness of the W=20 localization signal under finite-size scaling from s1_size=16 to 128, with absolute IPR contrast ≥2.0× and family consistency ≥2/3."

**Caveats required:**
- Finite-lattice only (no thermodynamic limit)
- Anderson disorder only (no general disorder)
- S³×S¹ only (no FL generalization)
- W=20 exploratory choice (not optimal-W claim)
- N ≤ 3712 (largest lattice, s1_size=128, j_max=3)

---

### 8.2 GATE4_FSS_WEAK_OR_INCONCLUSIVE

**Conditions (ANY can trigger):**
1. **Aggregate W=20 contrast 1.5×–2.0×** (below PASS threshold but above artifact)
2. **Family dependence strong:** Only 1/3 families pass, or one family dominates (>80% of contrast)
3. **Finite-size trend weakens but does not collapse:** Contrast decreases with size but remains >1.5×
4. **Level-spacing ambiguous:** r-statistic does not clearly support or contradict localization
5. **Partial grid completion:** 50–99% of pre-registered cases completed

**Claim allowed:**
> "S³×S¹ Gate 4B shows weak or inconclusive evidence for finite-lattice robustness of the W=20 signal. Finite-size scaling trend is ambiguous or family-dependent."

**Caveats required:**
- All PASS_WITH_CAVEATS caveats PLUS:
- Strong family dependence noted
- Finite-size trend weakening (if applicable)
- Recommend additional diagnostics or replication

**Action:** Re-evaluate experiment design, consider expanded grid or alternative metrics.

---

### 8.3 GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED

**Conditions (ANY can trigger):**
1. **Aggregate W=20 contrast <1.5×** (artifact interpretation likely)
2. **Single-family carry:** Only one family shows W=20 contrast ≥2.0×, others fail
3. **Finite-size collapse:** Contrast drops to <1.5× at larger sizes (s1_size=128)
4. **Level-spacing contradiction:** r-statistic does NOT shift toward Poisson at W=20, or shifts opposite direction
5. **Broad instability:** wilson_ring/s64 caveat reappears at larger sizes across multiple families
6. **Controls fail:** W=0 baseline unstable, random matrix theory nulls violated
7. **Post-hoc threshold change required:** Results only pass if thresholds adjusted after seeing data

**Claim allowed:**
> "S³×S¹ Gate 4B does NOT support finite-lattice robustness of the W=20 signal. Results are consistent with finite-size artifact or discretization dependence."

**Caveats required:**
- Finite-lattice result does NOT generalize
- W=20 signal may be family-specific artifact
- Recommend abandoning S³×S¹ W=20 track or redesigning experiment

**Action:** Do NOT proceed to Gate 5. Re-evaluate hypothesis or geometry.

---

### 8.4 GATE4_FSS_INCOMPLETE

**Conditions (ANY can trigger):**
1. **Grid completion <50%** of pre-registered cases
2. **Critical outputs missing:** Metrics cannot be computed for verdict
3. **Runtime timeout:** Execution exceeds acceptable budget before finishing
4. **Numerical instability blocks verdict:** Eigenvalue solver failures across multiple families prevent aggregation

**Claim allowed:**
> "S³×S¹ Gate 4B incomplete. Results cannot be used for verdict without full pre-registered grid."

**Caveats required:**
- Partial data NOT used for scientific claims
- Re-run required with adjusted runtime plan or reduced grid

**Action:** Fix implementation issues, adjust grid if needed, re-run with new pre-registration.

---

## 9. Runtime & Batch Plan

### 9.1 Benchmark-Driven Execution

**Step 1: Runtime benchmark (REQUIRED FIRST)**
1. Run single case with eigenvectors enabled
2. Measure overhead vs v0.1.20 eigenvalue-only execution
3. Extrapolate to 216 cases
4. Commit benchmark results before proceeding

**Step 2: Batch execution (if benchmark confirms feasibility)**

**Option A: Full sequential execution (if <24h estimate)**
- Execute all 216 cases in order
- Checkpoint every 24 cases (same as v0.1.20 batch size)
- Save intermediate outputs to RUNS/gate4_fss_v0.1.21/batches/

**Option B: Split over 2 days (if 24-48h estimate)**
- Day 1: Batches 1-5 (120 cases)
- Day 2: Batches 6-9 (96 cases)
- No change to grid parameters

**Option C: Reduced grid (if >48h estimate)**
- Drop s1_size=128 (reduce to 162 cases)
- Document as protocol deviation
- Verdict becomes INCOMPLETE if <180 cases completed

---

### 9.2 Checkpointing & Partial Outputs

**Save outputs after each batch:**
- `reports/RUNS/gate4_fss_v0.1.21/batches/batch_01/results.json`
- `reports/RUNS/gate4_fss_v0.1.21/batches/batch_01/timing.json`
- etc.

**Partial data policy:**
- **Allowed:** Review partial outputs to check implementation correctness
- **Forbidden:** Use partial outputs for verdict before full pre-registered grid completes
- **Exception:** If FAIL_OR_ARTIFACT_DOMINATED is obvious in first 2 batches → stop early, report FAIL

---

## 10. Output Artifacts (Expected After Execution)

**Primary outputs:**

1. **Results report:**
   - `reports/S3_S1_GATE4_FSS_RESULTS_v0.1.21.md`
   - Structure: Version note → Summary → Metrics → Verdict → Caveats → Figures → v0.1.20 comparison
   - Must include: 
     - Aggregate contrast (true IPR)
     - Family breakdown
     - Finite-size trend
     - r-statistic analysis
     - Comparison with v0.1.20 eigenvalue-based metric

2. **Run data:**
   - `reports/RUNS/gate4_fss_v0.1.21/config.json` — pre-registered grid parameters
   - `reports/RUNS/gate4_fss_v0.1.21/merged/metrics.json` — all computed metrics per case
   - `reports/RUNS/gate4_fss_v0.1.21/merged/summary.md` — human-readable summary
   - `reports/RUNS/gate4_fss_v0.1.21/figures/` — all generated plots

3. **Figures (minimum required):**
   - `ipr_contrast_vs_size.png` — True IPR contrast vs s1_size, faceted by family
   - `ipr_comparison_v0.1.20_vs_v0.1.21.png` — Side-by-side: eigenvalue metric vs true IPR
   - `r_statistic_vs_W.png` — Level-spacing r vs disorder strength, faceted by size
   - `family_comparison.png` — True IPR contrast by family at W=20
   - `finite_size_trend.png` — Aggregate contrast vs s1_size with error bars

4. **Supporting data:**
   - `gate4_decision_matrix.csv` — All cases with pass/fail per condition
   - `gate4_family_breakdown.csv` — Per-family metrics
   - `gate4_runtime_log.txt` — Execution timestamps and convergence warnings
   - `benchmark_results.json` — Single-case benchmark overhead measurement

---

## 11. Pre-Execution Checklist (BLOCKING)

**Before executing ANY batches:**

- [ ] **Unit tests pass:** `pytest tests/test_ipr_metric.py -v` → all green
- [ ] **Code review:** run_gate4_batched.py lines 216-230 implement true IPR formula
- [ ] **Benchmark complete:** Single-case overhead measured and documented
- [ ] **Runtime estimate:** Extrapolated total time < 48 hours OR grid reduction plan approved
- [ ] **Protocol committed:** This file committed to git with message `docs(gate-4b): pre-register v0.1.21 metric-corrected protocol`
- [ ] **No execution started:** Verify RUNS/gate4_fss_v0.1.21/ does not exist yet

**DO NOT PROCEED with execution until all checkboxes ticked.**

---

## 12. Post-Execution Requirements

**After 216-case execution completes:**

1. **Scientific analysis** (same as v0.1.20):
   - Aggregate metrics across all cases
   - Apply decision rules
   - Compute verdict
   - Generate figures

2. **v0.1.20 comparison analysis:**
   - Compare true IPR trend vs eigenvalue trend
   - Check if verdict changes (WEAK → PASS or vice versa)
   - Document any qualitative differences

3. **Results report:**
   - Create S3_S1_GATE4_FSS_RESULTS_v0.1.21.md
   - Executive summary: caveat-first, verdict-clear
   - Comparison section with v0.1.20
   - Allowed/forbidden claims explicitly listed

4. **Atomic commit:**
   ```
   results(gate-4b): S3xS1 finite-size scaling with corrected IPR metric
   ```
   - Commit all artifacts together (report + RUNS/ + figures)

5. **NO PASS CLAIM without full analysis:**
   - Even if results look strong, verdict requires full report
   - No external communication until results report finalized

---

## 13. Success Criteria Summary

**Gate 4B succeeds if:**
1. ✅ True eigenvector-based IPR contrast ≥2.0× at W=20
2. ✅ Family consistency ≥2/3
3. ✅ Finite-size trend does not collapse
4. ✅ r-statistic supports or does not contradict IPR
5. ✅ No forbidden claims made
6. ✅ Full pre-registered grid executed (≥180/216 cases)

**Gate 4B is inconclusive if:**
- Contrast 1.5×–2.0× (weak signal)
- Family dependence strong
- Finite-size trend weakens

**Gate 4B fails if:**
- Contrast <1.5× (artifact likely)
- r-statistic contradicts IPR
- Finite-size collapse at s1_size=128

---

## 14. Final Notes

**Critical reminders:**

1. **This is a METRIC CORRECTION, not a new experiment**
   - Grid unchanged, thresholds unchanged
   - Only implementation fix: eigvalsh → eigh

2. **v0.1.20 was NOT invalid execution**
   - 216/216 cases completed successfully
   - r-statistic results remain valid
   - Eigenvalue trend diagnostic
   - Execution robustness demonstrated

3. **v0.1.21 measures DIFFERENT quantity**
   - v0.1.20: mean eigenvalue (energy-based)
   - v0.1.21: mean IPR (wavefunction localization)
   - Results may differ qualitatively

4. **No retrospective claims**
   - Cannot reinterpret v0.1.20 results as IPR
   - Cannot claim "metric fixed, verdict upgraded"
   - Must execute v0.1.21 grid to completion

5. **Unit tests are NON-NEGOTIABLE**
   - 3 ground-truth tests must pass before execution
   - Prevents repeat of metric implementation mismatch

---

**Pre-registration status:** LOCKED after git commit  
**Version:** v0.1.21  
**Date:** 2026-05-22  
**Next step:** Commit this protocol, then execute benchmark, then full grid
