# S³×S¹ Gate 4 FSS & Robustness Pre-Registration — v0.1.20

**Дата:** 2026-05-21 14:00 Almaty  
**Статус:** PRE-REGISTERED (before execution)  
**Цель:** Gate 4 finite-size scaling and robustness testing of Gate 3C W=20 signal  
**Предшествующий статус:** Gate 3C PASS_WITH_CAVEATS (2.68x contrast at W=20)  

---

## 1. Purpose

**Gate 4 tests whether the Gate 3C W=20 finite-lattice localization signal is robust under:**
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
- Example: `S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20_REVISED.md`
- The original version remains in git history.
- Results must cite the exact protocol version used.

**Violation of protocol immutability makes the results exploratory, not confirmatory.**

---

## 3. Non-Goals (Explicit Forbidden Claims)

**Gate 4 does NOT and CANNOT establish:**

1. ❌ **Physical compactification** — finite-lattice evidence ≠ continuum physics
2. ❌ **FL generalization** — S³×S¹ result does not prove S²×S¹, S⁷×S¹, or arbitrary products
3. ❌ **W=20 optimality** — contrast maximization NOT tested, W=20 is exploratory choice
4. ❌ **Thermodynamic limit** — finite N ≤ 3712 (at s1_size=128, j_max=3) ≠ N→∞
5. ❌ **"S³×S¹ validated"** — validation theater forbidden, use "finite-lattice robustness evidence"
6. ❌ **Threshold tuning** — decision rules fixed before results, no post-hoc adjustment
7. ❌ **Family cherry-picking** — cannot use partial/family-only pass as full pass
8. ❌ **Ratio IPR verdict** — ratio metric deprecated, never verdict-driving

**If any forbidden claim appears in results or discussion → immediate correction required.**

---

## 4. Prior Evidence (Context for Gate 4)

**Pre-Gate 4 state of knowledge:**

### 3.1 Gate 3 Full Diagnostic (exploratory, v0.1.20)
- **Date:** 2026-05-21 01:00–08:00
- **Grid:** 10 W values × 3 families × 9 configurations = 270 cases
- **Result:** W=20 showed 1.75x contrast (highest in grid)
- **Verdict:** WEAK_OR_INCONCLUSIVE
- **Reason:** Exploratory sweep, no pre-registration, family dependence detected
- **Status:** Hypothesis-generating only, NOT confirmatory

### 3.2 Exploratory W Sweep (v0.1.20)
- **Date:** 2026-05-21 08:00 (disorder_sweep)
- **Result:** W=20 showed 4.68x contrast (spectral_circle family)
- **Status:** Single family, exploratory only
- **Action:** Triggered Gate 3C confirmatory replication

### 3.3 Gate 3C Confirmatory Replication (v0.1.20)
- **Date:** 2026-05-21 09:00–10:00
- **Pre-registration:** S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md (2026-05-10)
- **Grid:** W=20 × 3 families × 216 parameter combinations = 648 cases
- **Result:** 2.68x absolute IPR contrast
- **Triad Gate:** T1/T4/T5 passed, T2/T3/T6 retired
- **Verdict:** PASS_WITH_CAVEATS
- **Caveats:**
  - Finite-lattice only (no thermodynamic limit)
  - Anderson disorder only (no general disorder)
  - N ≤ 3712 (s1_size=64, j_max=3)
  - W=20 exploratory choice (not optimal-W claim)
  - S³×S¹ only (no FL generalization)

### 3.4 Controls & Diagnostics (v0.1.20)
- **Wilson/s64 investigation:** Caveat resolved, asymptotic spectral_circle behavior explained
- **Metric sanity tests:** IPR metric validated against analytic controls
- **S³×S¹ controls:** Random matrix theory nulls passed
- **Contrast investigation:** Alternative metrics tested, absolute IPR confirmed as primary

### 3.5 Recovery Status (commit b7906c0)
- **Recovered artifacts:** 17 files (5 reports, 2 scripts, 5 tests, 5 RUNS files)
- **Pre-registration:** Triad Gate protocol preserved
- **Status:** Gate 3C confirmatory status maintained

---

## 5. Pre-Registered Grid (Gate 4 Conservative First Pass)

**Grid parameters (fixed before execution):**

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
  - 128       # Large (if runtime permits)

j_max_values:
  - 2         # Lower spectral density
  - 3         # Gate 3C standard

random_seeds:
  - 123
  - 456
  - 789

total_cases_estimate: 3 families × 3 W × 4 sizes × 2 j_max × 3 seeds = 216 cases
```

**Excluded from Gate 4 first pass:**
- `s1_size=256` — runtime prohibitive without cluster resources
- `W values outside {0,12,20}` — focus on verified W=20 and controls
- `j_max=1` — low spectral density, not scientifically interesting
- `Additional families` — spectral_circle/ring/wilson_ring cover design space

**If runtime estimate >24 hours → reduce grid:**
1. Drop s1_size=128 (keep 16/32/64)
2. Reduce seeds to {123, 456}
3. Keep all 3 families (no family exclusion permitted)

---

## 6. Metrics (Pre-Registered, No Post-Hoc Changes)

### 5.1 Primary Metrics (Verdict-Driving)

**1. Absolute IPR Contrast**
- **Definition:** `contrast = IPR(W=20) / IPR(W=0)` aggregated across families
- **Rationale:** Gate 3C validated this metric, 2.68x contrast at s1_size=64
- **Gate 4 question:** Does contrast persist, strengthen, or weaken as s1_size increases?
- **Threshold:** ≥2.0x for PASS_WITH_CAVEATS (conservative, below Gate 3C 2.68x)

**2. Finite-Size Trend**
- **Definition:** Slope and stability of IPR contrast vs s1_size
- **Possible outcomes:**
  - **Saturating/strengthening:** Contrast stable or increasing → robust signal
  - **Weakening but stable:** Contrast decreases but remains >2.0x → finite-size effect, still localized
  - **Collapsing:** Contrast drops to <1.5x → artifact interpretation
- **Verdict impact:** Saturating/strengthening → PASS; weakening but stable → PASS with stronger caveat; collapsing → FAIL

**3. Family Consistency**
- **Definition:** How many families show W=20 contrast ≥2.0x?
- **Threshold:** ≥2/3 families must pass (no single-family carry)
- **Rationale:** Prevents cherry-picking, ensures robustness across discretization choices

**4. Level-Spacing Adjacent Gap Ratio (r-statistic)**
- **Definition:** `r = min(δₙ, δₙ₊₁) / max(δₙ, δₙ₊₁)` where `δₙ = Eₙ₊₁ - Eₙ`
- **Expected behavior:**
  - W=0: r ≈ 0.53 (GOE, ergodic)
  - W=20: r → 0.39 (Poisson, localized)
- **Gate 4 test:** Does r-statistic shift confirm localization interpretation of IPR contrast?
- **Verdict impact:** r-shift contradicts IPR → FAIL; r-shift supports IPR → PASS; r-ambiguous → weaken verdict

### 5.2 Secondary Metrics (Diagnostic, Not Verdict-Driving)

**5. W=12 Intermediate Response**
- **Purpose:** Check monotonicity (W=0 < W=12 < W=20 in IPR)
- **Not verdict-driving:** W=12 failure does NOT invalidate W=20 result
- **Use:** Sanity check, helps interpret finite-size trend

**6. Runtime & Numerical Stability**
- **Purpose:** Detect implementation issues, guide future grid design
- **Tracked:** Eigenvalue solver convergence, matrix condition numbers
- **Not verdict-driving:** Stability issues → INCOMPLETE, not FAIL

**7. Ratio IPR (deprecated, backward compatibility only)**
- **Definition:** `IPR_ratio = IPR(localized) / IPR(ergodic)`
- **Status:** Retired in Gate 3C (Wilson/s64 caveat exposed family dependence)
- **Use:** Report for comparison with Gate 3 full diagnostic only
- **NEVER verdict-driving:** Ratio metric does NOT contribute to PASS/FAIL decision

---

## 7. Decision Rules (Fixed Before Execution)

**Four mutually exclusive verdicts:**

### 6.1 GATE4_FSS_PASS_WITH_CAVEATS

**Conditions (ALL must hold):**
1. **Aggregate W=20 contrast ≥2.0x** across all families and sizes
2. **Family consistency:** ≥2/3 families show W=20 contrast ≥2.0x independently
3. **No single-family domination:** No one family carries >80% of aggregate contrast
4. **Finite-size trend:** Contrast stable, saturating, or strengthening (not collapsing)
5. **Level-spacing supports localization:** r-statistic shift toward Poisson at W=20, or at least not contradicting IPR
6. **No broad failure cluster:** No systematic failures across all families at large sizes
7. **Controls pass:** W=0 baseline stable, no control failures

**Claim allowed:**
> "S³×S¹ Gate 4 supports finite-lattice robustness of the W=20 localization signal under finite-size scaling from s1_size=16 to 128, with absolute IPR contrast ≥2.0x and family consistency ≥2/3."

**Caveats required:**
- Finite-lattice only (no thermodynamic limit)
- Anderson disorder only (no general disorder)
- S³×S¹ only (no FL generalization)
- W=20 exploratory choice (not optimal-W claim)
- N ≤ 3712 (largest lattice, s1_size=128, j_max=3)

### 6.2 GATE4_FSS_WEAK_OR_INCONCLUSIVE

**Conditions (ANY can trigger):**
1. **Aggregate W=20 contrast 1.5x–2.0x** (below PASS threshold but above artifact)
2. **Family dependence strong:** Only 1/3 families pass, or one family dominates (>80% of contrast)
3. **Finite-size trend weakens but does not collapse:** Contrast decreases with size but remains >1.5x
4. **Level-spacing ambiguous:** r-statistic does not clearly support or contradict localization
5. **Partial grid completion:** 50–99% of pre-registered cases completed

**Claim allowed:**
> "S³×S¹ Gate 4 shows weak or inconclusive evidence for finite-lattice robustness of the W=20 signal. Finite-size scaling trend is ambiguous or family-dependent."

**Caveats required:**
- All PASS_WITH_CAVEATS caveats PLUS:
- Strong family dependence noted
- Finite-size trend weakening (if applicable)
- Recommend additional diagnostics or replication

**Action:** Re-evaluate experiment design, consider expanded grid or alternative metrics.

### 6.3 GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED

**Conditions (ANY can trigger):**
1. **Aggregate W=20 contrast <1.5x** (artifact interpretation likely)
2. **Single-family carry:** Only one family shows W=20 contrast ≥2.0x, others fail
3. **Finite-size collapse:** Contrast drops to <1.5x at larger sizes (s1_size=128)
4. **Level-spacing contradiction:** r-statistic does NOT shift toward Poisson at W=20, or shifts opposite direction
5. **Broad instability:** wilson_ring/s64 caveat reappears at larger sizes across multiple families
6. **Controls fail:** W=0 baseline unstable, random matrix theory nulls violated
7. **Post-hoc threshold change required:** Results only pass if thresholds adjusted after seeing data

**Claim allowed:**
> "S³×S¹ Gate 4 does NOT support finite-lattice robustness of the W=20 signal. Results are consistent with finite-size artifact or discretization dependence."

**Caveats required:**
- Finite-lattice result does NOT generalize
- W=20 signal may be family-specific artifact
- Recommend abandoning S³×S¹ W=20 track or redesigning experiment

**Action:** Do NOT proceed to Gate 5. Re-evaluate hypothesis or geometry.

### 6.4 GATE4_FSS_INCOMPLETE

**Conditions (ANY can trigger):**
1. **Grid completion <50%** of pre-registered cases
2. **Critical outputs missing:** Metrics cannot be computed for verdict
3. **Runtime timeout:** Execution exceeds acceptable budget before finishing
4. **Numerical instability blocks verdict:** Eigenvalue solver failures across multiple families prevent aggregation

**Claim allowed:**
> "S³×S¹ Gate 4 incomplete. Results cannot be used for verdict without full pre-registered grid."

**Caveats required:**
- Partial data NOT used for scientific claims
- Re-run required with adjusted runtime plan or reduced grid

**Action:** Fix implementation issues, adjust grid if needed, re-run with new pre-registration.

---

## 8. Runtime & Batch Plan

### 7.1 Dry-Run Estimate

**Before executing full grid:**
1. Run single case (spectral_circle, W=20, s1_size=64, j_max=3, seed=123)
2. Measure wall-clock time
3. Extrapolate to full 216 cases
4. If estimate >24 hours → reduce grid per Section 5

**Expected runtime per case (based on Gate 3C):**
- s1_size=16, j_max=2: ~30 sec
- s1_size=64, j_max=3: ~3 min (Gate 3C baseline)
- s1_size=128, j_max=3: ~10–15 min (estimate, not verified)

**Full grid estimate:**
- 216 cases × 3 min average ≈ 10.8 hours (optimistic)
- With s1_size=128 overhead: up to 24 hours

### 7.2 Batch Execution

**Do NOT run full grid in one session.**

**Batch strategy:**
1. **Batch 1 (baseline):** s1_size={16,32,64}, all families, all W, j_max=3, seed=123
   - Purpose: Reproduce Gate 3C at s1_size=64, test finite-size trend 16→32→64
   - Cases: 3 families × 3 W × 3 sizes × 1 j_max × 1 seed = 27 cases
   - Runtime estimate: ~2 hours

2. **Batch 2 (large size):** s1_size=128, all families, all W, j_max=3, seed=123
   - Purpose: Test finite-size trend 64→128
   - Cases: 3 families × 3 W × 1 size × 1 j_max × 1 seed = 9 cases
   - Runtime estimate: ~2–3 hours

3. **Batch 3 (j_max=2 robustness):** s1_size={16,32,64}, all families, all W, j_max=2, seed=123
   - Purpose: Test j_max sensitivity
   - Cases: 3 families × 3 W × 3 sizes × 1 j_max × 1 seed = 27 cases
   - Runtime estimate: ~1.5 hours

4. **Batch 4 (additional seeds):** Repeat Batches 1–3 with seeds {456, 789}
   - Purpose: Statistical robustness
   - Cases: (27 + 9 + 27) × 2 seeds = 126 cases
   - Runtime estimate: ~10 hours

**Total batches: 27 + 9 + 27 + 126 = 189 cases (if all batches executed)**

### 7.3 Checkpointing & Partial Outputs

**Save outputs after each batch:**
- `reports/RUNS/gate4_fss_v0.1.20_batch1/metrics.json`
- `reports/RUNS/gate4_fss_v0.1.20_batch2/metrics.json`
- etc.

**Partial data policy:**
- **Allowed:** Review partial outputs to check implementation correctness
- **Forbidden:** Use partial outputs for verdict before full pre-registered grid completes
- **Exception:** If FAIL_OR_ARTIFACT_DOMINATED is obvious in Batch 1 → stop early, report FAIL

### 7.4 Timeout Mitigation

**If execution exceeds 24 hours:**
1. Stop execution
2. Assess completion percentage
3. If <50% → verdict = INCOMPLETE
4. If ≥50% but <100% → report partial results, verdict = INCOMPLETE, recommend re-run with reduced grid
5. Never use partial data for PASS verdict

---

## 9. Output Artifacts (Expected After Execution)

**Primary outputs:**

1. **Results report:**
   - `reports/S3_S1_GATE4_FSS_RESULTS_v0.1.20.md`
   - Structure: Summary → Metrics → Verdict → Caveats → Figures → Appendices
   - Must include: aggregate contrast, family breakdown, finite-size trend, r-statistic analysis

2. **Run data:**
   - `reports/RUNS/gate4_fss_v0.1.20/config.json` — pre-registered grid parameters
   - `reports/RUNS/gate4_fss_v0.1.20/metrics.json` — all computed metrics per case
   - `reports/RUNS/gate4_fss_v0.1.20/summary.md` — human-readable summary
   - `reports/RUNS/gate4_fss_v0.1.20/figures/` — all generated plots

3. **Figures (minimum required):**
   - `ipr_contrast_vs_size.png` — IPR contrast vs s1_size, faceted by family
   - `r_statistic_vs_W.png` — Level-spacing r vs disorder strength, faceted by size
   - `family_comparison.png` — IPR contrast by family at W=20
   - `finite_size_trend.png` — Aggregate contrast vs s1_size with error bars

4. **Supporting data:**
   - `gate4_decision_matrix.csv` — All cases with pass/fail per condition
   - `gate4_family_breakdown.csv` — Per-family metrics
   - `gate4_runtime_log.txt` — Execution timestamps and convergence warnings

**All artifacts committed together in single atomic commit:**
```
feat(gate-4): S3xS1 finite-size scaling and robustness tests
```

---

## 10. Claim Language (Allowed vs Forbidden)

### 9.1 Allowed Claims (if PASS_WITH_CAVEATS)

✅ **Conservative, scientifically accurate:**

> "S³×S¹ Gate 4 supports finite-lattice robustness of the W=20 localization signal under finite-size scaling from s1_size=16 to 128."

> "Absolute IPR contrast at W=20 remains ≥2.0x across three S¹ discretization families, with family consistency ≥2/3."

> "Finite-size trend shows [saturating/stable/weakening but non-collapsing] behavior, consistent with finite-lattice localization under Anderson disorder."

> "Level-spacing r-statistic shift toward Poisson distribution supports localization interpretation of IPR contrast."

> "Gate 4 results strengthen Gate 3C confirmatory evidence within the pre-registered scope (finite lattice, Anderson disorder, S³×S¹, N≤3712)."

### 9.2 Forbidden Claims (validation theater)

❌ **Overclaiming, scope violation:**

> "S³×S¹ validated." — NO QUALIFIERS = FORBIDDEN

> "FL localization generalized to S³×S¹." — GENERALIZATION CLAIM = FORBIDDEN

> "W=20 is optimal." — OPTIMALITY CLAIM = FORBIDDEN (W=20 is exploratory choice)

> "Thermodynamic limit proven." — FINITE N ≠ N→∞

> "Physical compactification shown." — FINITE LATTICE ≠ CONTINUUM PHYSICS

> "S³×S¹ in the continuum established." — DISCRETIZED GEOMETRY ≠ CONTINUUM

> "FL transfer hypothesis confirmed." — SINGLE GEOMETRY ≠ GENERAL PRINCIPLE

**If any forbidden claim appears → immediate retraction and correction required.**

### 9.3 Minimal Qualifier Set (Always Required)

**Every Gate 4 claim MUST include ALL of these qualifiers:**

1. **Finite-lattice scope:** "finite-lattice" or "discretized" or "N≤3712"
2. **Anderson disorder scope:** "Anderson disorder" or "diagonal disorder" or "uncorrelated on-site"
3. **Geometry scope:** "S³×S¹" or "specific product geometry" (never "FL generalized")
4. **W=20 exploratory:** "at W=20" or "disorder strength W=20" (never "optimal W")
5. **Caveats explicit:** "with caveats" or "evidence" or "supports" (never "proven" or "validated")

**Example of minimally qualified claim:**
> "S³×S¹ finite-lattice Gate 4 evidence supports robustness of the W=20 Anderson disorder localization signal across s1_size scaling, with caveats: no thermodynamic limit, no FL generalization, exploratory W choice."

---

## 11. Stop Conditions (Abort Execution Before Completion)

**Execution MUST STOP if ANY of these occur:**

### 10.1 Runtime Budget Exceeded
- **Trigger:** Dry-run estimate >24 hours AND grid reduction not acceptable
- **Action:** Abort, report INCOMPLETE, redesign grid with new pre-registration

### 10.2 Numerical Instability Widespread
- **Trigger:** Eigenvalue solver failures in ≥2/3 families across multiple cases
- **Action:** Abort, report INCOMPLETE, fix implementation, re-run with new pre-registration

### 10.3 Early FAIL Signal (Batch 1 only)
- **Trigger:** Batch 1 shows aggregate W=20 contrast <1.5x AND all 3 families fail
- **Action:** STOP after Batch 1, report GATE4_FSS_FAIL_OR_ARTIFACT_DOMINATED
- **Rationale:** No point running Batches 2–4 if baseline fails
- **Exception:** If only 1/3 families fail → continue to check family dependence

### 10.4 Implementation Bug Detected Mid-Run
- **Trigger:** Outputs inconsistent with Gate 3C (e.g., s1_size=64 contrast differs by >20%)
- **Action:** Abort, debug, re-run with corrected implementation, new pre-registration NOT required if bug is implementation-only (not design)

### 10.5 Missing Outputs Prevent Metrics
- **Trigger:** ≥20% of cases in a batch produce no output or corrupted output
- **Action:** Abort, fix I/O issues, re-run batch

**Do NOT continue execution if stop condition triggered.**  
**Report current state as INCOMPLETE, document reason, plan corrective action.**

---

## 12. Relationship to Prior Gates

**Gate sequence (v0.1.20 Track C: S³×S¹):**

| Gate | Status | Verdict | Contrast | Grid Size | Purpose |
|------|--------|---------|----------|-----------|---------|
| Gate 1 | ✅ COMPLETE | PASS | 1.50x | 27 cases | Sanity check, controls |
| Gate 2 | ✅ COMPLETE | PASS | 1.67x | 135 cases | Expanded diagnostics, theory validation |
| Gate 3 Full | ✅ COMPLETE | WEAK_OR_INCONCLUSIVE | 1.75x | 270 cases | Exploratory W sweep |
| Gate 3C | ✅ COMPLETE | PASS_WITH_CAVEATS | 2.68x | 648 cases | Confirmatory replication (W=20) |
| **Gate 4 FSS** | 🔵 PRE-REGISTERED | — | — | 216 cases | Finite-size scaling, robustness |
| Gate 5 | ⏸️ NOT STARTED | — | — | TBD | (After Gate 4 results) |

**Gate 4 advances beyond Gate 3C by:**
1. Testing finite-size trend (s1_size = 16 → 32 → 64 → 128)
2. Adding level-spacing r-statistic diagnostic
3. Checking W=12 intermediate response
4. Expanding j_max robustness (j_max = 2, 3)
5. Multi-seed statistical robustness (3 seeds)

**Gate 4 does NOT test:**
- Disorder types beyond Anderson (Aubry-André, quasiperiodic, etc.)
- Geometries beyond S³×S¹ (S²×S¹, S⁷×S¹, etc.)
- Alternative metrics beyond IPR and r-statistic
- Optimal W search (W scan beyond {0,12,20})

**If Gate 4 passes → Gate 5 options:**
- Disorder type robustness (Aubry-André, quasiperiodic)
- Alternative geometries (S²×S¹ for comparison)
- Expanded size range (s1_size=256 if cluster available)
- Spectral flow / edge mode analysis

**If Gate 4 fails → stop S³×S¹ track, re-evaluate hypothesis.**

---

## 13. Pre-Registration Compliance Checklist

**Before executing Gate 4, verify ALL of these:**

- [ ] This pre-registration document committed to git before any Gate 4 execution
- [ ] Git commit shows pre-registration timestamp before RUNS/gate4_fss_v0.1.20/ created
- [ ] Grid parameters (Section 5) not changed after seeing partial results
- [ ] Decision rules (Section 7) not changed after seeing partial results
- [ ] Thresholds (2.0x for PASS, 1.5x for FAIL) not adjusted post-hoc
- [ ] Claim language (Section 10) reviewed and forbidden claims noted
- [ ] Stop conditions (Section 11) understood and agreed
- [ ] Dry-run estimate (Section 8.1) completed before full grid execution
- [ ] Batch plan (Section 8.2) prepared and checkpoints identified

**Pre-registration timestamp:**
```
git log --oneline --grep="GATE4.*PREREGISTRATION" -1
```

**This timestamp MUST be earlier than:**
```
ls -l reports/RUNS/gate4_fss_v0.1.20/
```

**If pre-registration timestamp is AFTER RUNS creation → results are exploratory, NOT confirmatory.**

---

## 14. Post-Execution Requirements

**After Gate 4 execution completes, the results report MUST include:**

1. **Exact pre-registration compliance statement:**
   - "Gate 4 executed according to pre-registration S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.20.md committed on [date] at [commit hash]."
   - "No grid parameters, decision rules, or thresholds were changed after seeing results."
   - "All deviations from pre-registered plan are documented below with justification."

2. **Deviations section (if any):**
   - List ANY differences between pre-registered plan and actual execution
   - Justify each deviation (e.g., "Batch 4 reduced from 3 seeds to 2 due to runtime timeout")
   - Mark verdict impact: "This deviation [does / does not] affect verdict."

3. **Decision matrix:**
   - Show which decision rule conditions (Section 7) were met
   - Show verdict derivation step-by-step
   - Show family breakdown (which families passed/failed)

4. **Caveats explicit:**
   - Repeat minimal qualifier set (Section 10.3) in summary
   - Add any new caveats discovered during execution

5. **Comparison to Gate 3C:**
   - Side-by-side: Gate 3C contrast (2.68x at s1_size=64) vs Gate 4 aggregate
   - Explain any discrepancy >10%

6. **Figures with captions:**
   - All 4 minimum required figures (Section 9)
   - Each figure caption includes: what is shown, what to look for, verdict interpretation

7. **Raw data availability:**
   - Confirm all RUNS data committed to git
   - Provide reproduction command for key figures

**Results report CANNOT be finalized without these 7 sections.**

---

## 15. Null Results Policy

**If Gate 4 verdict is WEAK_OR_INCONCLUSIVE or FAIL_OR_ARTIFACT_DOMINATED:**

1. **Full transparency required:**
   - Report negative results with same detail as positive results
   - Do NOT bury negative results in appendices or "future work"
   - Do NOT spin failure as "preliminary" or "needs more data"

2. **Scientific interpretation:**
   - WEAK_OR_INCONCLUSIVE → "Results do not provide strong evidence for finite-size robustness. Further investigation needed."
   - FAIL_OR_ARTIFACT_DOMINATED → "Results consistent with finite-size artifact. W=20 signal does NOT generalize across size scaling."

3. **No post-hoc rescue:**
   - Do NOT re-run with adjusted thresholds to get PASS
   - Do NOT exclude "problematic" families post-hoc
   - Do NOT add new metrics that weren't pre-registered

4. **Document in null_results/ (if FAIL):**
   - `null_results/gate4_fss_s3s1_w20_fail_v0.1.20.md`
   - Include: what was tested, why it failed, what we learned, what NOT to try next

5. **Update project status:**
   - Mark S³×S¹ W=20 track as "ABANDONED" or "REQUIRES_REDESIGN"
   - Do NOT proceed to Gate 5

**Null results are scientifically valuable.**  
**Failure to report null results = publication bias = scientific misconduct.**

---

## 16. Success Criteria Summary

**Gate 4 FSS succeeds (PASS_WITH_CAVEATS) if:**

✅ W=20 aggregate contrast ≥2.0x across all sizes and families  
✅ Family consistency ≥2/3 (at least 2 families pass independently)  
✅ Finite-size trend stable, saturating, or strengthening  
✅ Level-spacing r-statistic supports localization interpretation  
✅ No broad instability or control failures  
✅ Pre-registered grid ≥90% completed  
✅ No post-hoc threshold adjustments  

**Gate 4 FSS fails (FAIL_OR_ARTIFACT_DOMINATED) if:**

❌ W=20 aggregate contrast <1.5x  
❌ Only 1/3 families pass (single-family carry)  
❌ Finite-size trend collapses (contrast drops to <1.5x at large sizes)  
❌ Level-spacing r-statistic contradicts localization  
❌ wilson_ring/s64 instability reappears at s1_size=128  
❌ Controls fail  
❌ Post-hoc threshold change required to get PASS  

**Between PASS and FAIL:**

⚠️ WEAK_OR_INCONCLUSIVE (1.5x ≤ contrast < 2.0x, or strong family dependence)  
⚠️ INCOMPLETE (<50% grid completion, or missing critical outputs)

---

## 17. Timeline & Milestones

**Planned Gate 4 execution timeline:**

| Milestone | Target Date | Deliverable |
|-----------|-------------|-------------|
| Pre-registration commit | 2026-05-21 14:00 | This document in git |
| Dry-run estimate | 2026-05-22 | Runtime projection, grid confirmation |
| Batch 1 execution | 2026-05-23 | 27 cases, baseline finite-size trend |
| Batch 2 execution | 2026-05-24 | 9 cases, s1_size=128 extension |
| Batch 3 execution | 2026-05-25 | 27 cases, j_max=2 robustness |
| Batch 4 execution | 2026-05-26–27 | 126 cases, seeds {456, 789} |
| Results analysis | 2026-05-28 | Aggregate metrics, verdict derivation |
| Results report draft | 2026-05-29 | S3_S1_GATE4_FSS_RESULTS_v0.1.20.md |
| Internal review | 2026-05-30 | Skeptic agent audit, caveat check |
| Final commit | 2026-05-31 | Results + figures + RUNS data |

**Total duration:** ~10 days (conservative, includes debugging buffer)

**If timeline slips >2 weeks → escalate, assess blockers.**

---

## 18. References

**Pre-registration protocol sources:**
- EstimandOps 2.0 (ICH E9(R1), Binette & Reiter 2024)
- Falsification Ladder enforcement protocol (v0.1.20)
- Triad Gate pre-registration (S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md)

**Prior Gate reports:**
- `reports/GATE_1_SUMMARY_v0.1.19.md`
- `reports/GATE_2_PROGRESS_v0.1.19.md`
- `reports/S3_S1_GATE3_FULL_DIAGNOSTIC_v0.1.20.md`
- `reports/S3_S1_GATE3C_CONFIRMATORY_REPLICATION_v0.1.20.md`

**Supporting diagnostics:**
- `reports/WILSON_RING_S64_INVESTIGATION_v0.1.20.md`
- `reports/DISORDER_SWEEP_v0.1.20.md`
- `reports/CONTRAST_INVESTIGATION_v0.1.19.md`

**Controls & tests:**
- `tests/test_s3_s1_controls.py`
- `tests/test_s3_s1_ipr_metric_sanity.py`
- `tests/test_s3_s1_gate3c_triad_v0_1_20.py`

**Git commits:**
- `9be68c5` — Gate 3C confirmatory PASS_WITH_CAVEATS
- `b7906c0` — Recovery of v0.1.20 Track C artifacts
- `5e6ebb8` — Caveat language tightening

---

**Статус:** ✅ PRE-REGISTERED — ready for execution after dry-run estimate  
**Следующий шаг:** Dry-run single case → runtime estimate → batch execution plan  
**Запрет:** Запуск Gate 4 без commit этого pre-registration документа

---

**Pre-registration signature (commit hash will be added after git commit):**
```
git log --oneline --grep="GATE4.*PREREGISTRATION" -1 --format="%H %ci %s"
```

This line will be filled after commit. Pre-registration is NOT valid until committed to git with timestamp before execution.
