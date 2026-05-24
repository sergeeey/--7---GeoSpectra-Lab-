# Agent Handoff Context — v0.1.22

**Date:** 2026-05-24  
**Phase:** POST-PLANNING, PRE-EXECUTION  
**Gate 4B Status:** CLOSED (PASS_WITH_CAVEATS)  
**v0.1.22 Status:** BATCHES 1-2 COMPLETE, BATCHES 3-6 PENDING REMOTE EXECUTION

---

## Executive Summary for Future Agents

**GeoSpectra Lab** is a **falsification-first validation harness** for testing toy mechanisms
related to compact product geometries. It is a reproducible Python MVP for scientific computing,
**not a claim that covariant compactification has been proven.**

Current milestone: v0.1.22 Negative Controls pilot — testing harness specificity
after Gate 4B v0.1.21 (S³×S¹ finite-size scaling) demonstrated 7.15× IPR contrast
with family consistency and strengthening FSS trend.

**Next active step:** Execute batches 3-6 (36 cases) on remote infrastructure
(Google Colab / AWS / cluster) due to local thermal constraint.

---

## Project Scope and Boundaries

### What GeoSpectra Lab IS

- **Falsification-first validation harness** for discretized spectral operators on compact product manifolds
- **Computational toy model** for testing localization-like signals in finite-lattice geometries
- **Reproducible diagnostic scaffold** with negative controls, positive controls, and null-results logging
- **Research tool** for exploring whether robust localization-like patterns survive artifact checks

### What GeoSpectra Lab IS NOT

**Forbidden claims (these statements are NEVER allowed in positive sections):**

- ❌ "Validated covariant compactification"
- ❌ "Proven physical compactification"
- ❌ "Generalized to thermodynamic/continuum limit"
- ❌ "Derived Standard Model gauge group SU(3)×SU(2)×U(1)"
- ❌ "Proven protected chiral zero modes"
- ❌ "Bypassed Witten/Lichnerowicz no-go theorems"
- ❌ "Established new physics paradigm"
- ❌ "Breakthrough in extra-dimensional stabilization"

**Allowed framing:**
- ✅ "Toy signal observed on finite lattice"
- ✅ "Diagnostic passed configured profile"
- ✅ "Localization-like pattern survived artifact checks"
- ✅ "Harness discrimination power tested"
- ✅ "Computational model only"

---

## Tom Lawrence Boundary (CRITICAL)

**Research context:**  
GeoSpectra Lab was initially inspired by broader questions in compact product geometries,
Kaluza-Klein-style reasoning, and covariant compactification, **including public work by
Tom Lawrence on product manifolds and covariant compactification.**

**Independence statement:**  
GeoSpectra does **not** test or validate covariant compactification directly. It asks
a narrower computational question:

> Can a finite-lattice spectral validation harness distinguish a robust localization-like
> signal on a compact product toy geometry from artifacts of disorder strength, matrix sparsity,
> operator family, seed choice, spectral tails, metric handling, or geometry scrambling?

**Attribution:**  
- Tom Lawrence ([ORCID: 0000-0002-2741-8226](https://orcid.org/0000-0002-2741-8226),
  Ronin Institute Research Scholar) — original covariant compactification framework
- Sergey Boyko — independent computational validation harness (GeoSpectra Lab)

**Scope boundary:**  
Any errors, interpretations, numerical models, or claims in GeoSpectra are entirely
Sergey Boyko's own. GeoSpectra is **not affiliated with, endorsed by, or reviewed by
Tom Lawrence** unless explicitly stated otherwise.

**For detailed attribution:** `docs/RESEARCH_CONTEXT.md`  
**For explicit claim boundaries:** `docs/CLAIMS_AND_CAVEATS.md`

---

## Gate 4B v0.1.21 — Final Status (IMMUTABLE)

**Last commit:** f7eff32 (results), 0c78263 (closeout package)  
**Verdict:** GATE4B_FSS_PASS_WITH_CAVEATS  
**Grid:** 216 cases (3 families × 3 W × 4 sizes × 2 j_max × 3 seeds)  
**Geometry:** S³×S¹ finite-lattice toy geometry  
**Disorder:** Anderson-style diagonal disorder  
**Main diagnostic:** True eigenvector-based IPR (metric-corrected)

**Key results:**
- **Aggregate contrast:** 7.15× (W=20 vs W=0)
- **FSS trend:** STRENGTHENING (3.76× → 24.90× across sizes)
- **Family consistency:** 3/3 PASS (spectral_s3, chiral_s3, wilson_s3)
- **r-statistic:** Δr = -0.163 (toward Poisson at strong disorder)
- **Baseline:** v0.1.21 (S³×S¹ Gate 4B FSS)

**Key documents:**
- `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md`
- `reports/GATE4B_PRE_PUSH_AUDIT_v0.1.21.md`
- `reports/CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md`
- `reports/CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md`

**Immutability:**  
Gate 4B is **CLOSED**. v0.1.22 is an independent validation layer (negative controls),
NOT a modification of Gate 4B results or protocol.

---

## v0.1.22 Negative Controls — Current Status

**Purpose:** Test harness specificity — can it reject non-geometric baselines?

**Scientific question:**  
Does Gate 4B signal reflect specific S³×S¹ geometric disorder coupling, OR can similar
PASS-like results be produced by broken/random/scrambled controls?

**Falsification hypothesis:**  
If harness is specific, negative controls should:
- Show <2.0× contrast (below Gate 4B threshold)
- Show weak or collapsing FSS trend (not strengthening)
- Show inconsistent r-statistic (not toward Poisson)
- Fail ≥2/3 control consistency check

**Danger result:**  
If ANY control reproduces the full Gate 4B-like PASS pattern (≥2.0× contrast,
stable/strengthening FSS, r-stat shift consistent with localization, reproducible
across seeds/sizes — not isolated), harness lacks specificity.

### Proposed Negative Controls

**Control A: Random Hermitian Baseline**  
Purpose: Check if generic random matrix with disorder fakes IPR contrast  
Construction: Diagonal U(r) ∈ [-W, W], Gaussian off-diagonal, NO geometric structure  
Expected: Should NOT reproduce the full Gate 4B-like robust pattern

**Control B: Scrambled Geometry**  
Purpose: Preserve dimension/scale but break S³×S¹ geometric coupling  
Construction: S³ indices permuted OR S³/S¹ decoupled OR wrong spectrum  
Expected: Should weaken or destabilize signal, not reproduce full robust pattern

**Control C: Broken Wilson Term**  
Purpose: Test if Wilson correction is load-bearing  
Construction: Wilson coefficient = 0 OR Wilson structure scrambled  
Expected: Should NOT reproduce wilson_ring robustness pattern

### Pilot Grid

**Size:** 54 cases (25% of Gate 4B 216-case grid)

| Parameter | Gate 4B | v0.1.22 Pilot |
|-----------|---------|---------------|
| Families/Controls | 3 families | 3 controls |
| W values | 0, 12, 20 | 0, 20 |
| s1_size | 16, 32, 64, 128 | 16, 64, 128 |
| j_max | 2, 3 | 3 only |
| seeds | 123, 456, 789 | 123, 456, 789 |
| **Total** | 216 | 54 |

### Execution Status

**Completed locally (2026-05-22):**
- ✅ Batch 1 (random_hermitian, W=0): 9 cases
- ✅ Batch 2 (random_hermitian, W=20): 9 cases
- **Subtotal:** 18/54 cases (33%)

**Remaining (remote execution required):**
- ⏳ Batch 3 (scrambled_geometry, W=0): 9 cases
- ⏳ Batch 4 (scrambled_geometry, W=20): 9 cases
- ⏳ Batch 5 (broken_wilson_term, W=0): 9 cases
- ⏳ Batch 6 (broken_wilson_term, W=20): 9 cases
- **Subtotal:** 36/54 cases (67%)

**Reason for remote execution:**  
Local thermal constraint (CPU overheating) blocks further heavy execution.
CPU thermal mitigation added (80% core limit + cooling pause), but insufficient
for remaining 36 cases.

**Remote infrastructure options:**
- Google Colab Free (recommended, ~15 min setup, 3-4 hour runtime)
- Research cluster (if available)
- AWS EC2 / Azure VM

**Execution command (batches 3-6):**
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id [3|4|5|6]
```

**Post-execution:**
- Aggregation + decision rules
- Results report: `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`
- Verdict: PASS_AS_EXPECTED / FALSE_PASS / WEAK

---

## Artifact Zoo Roadmap (Post-v0.1.22)

**Purpose:** Systematically rule out artifacts before stronger claims.

After negative controls (v0.1.22), future artifact checks include:

### 1. Metric-Volume Weighting Uncertainty
**Question:** Does IPR contrast depend on S³ metric-volume weighting choice?  
**Test:** Compare IPR with different metric prefactors in disorder term  
**Expected:** Robust signal should survive reasonable metric variations

### 2. Energy-Resolved Diagnostics
**Question:** Is signal confined to low-energy sector or spans full spectrum?  
**Test:** Compute IPR contrast in low/mid/high energy windows  
**Expected:** Localization-like pattern should strengthen at band edges

### 3. Directional IPR (Marginal S³ vs S¹)
**Question:** Is localization S¹-specific or affects both factors?  
**Test:** Compute marginal IPR on S³ sector separately from S¹  
**Expected:** Current S¹ marginal IPR should NOT transfer to S³ marginal

### 4. Operator Family Robustness
**Question:** Is signal specific to wilson_ring or survives alternative discretizations?  
**Test:** Compare against spectral_s3 and chiral_s3 (already done in Gate 4B)  
**Status:** ✅ Gate 4B showed 3/3 family consistency

### 5. Finite-Size Extrapolation
**Question:** Does FSS trend project to physically relevant scales?  
**Test:** Fit FSS curve, extrapolate to s1_size=256, 512  
**Status:** Planned for Gate 5 (if v0.1.22 passes)

---

## Known Limitations and Caveats

### Current Limitations (v0.1.21 + v0.1.22 planning)

1. **Finite lattice only** — no continuum limit validated
2. **Toy disorder model** — Anderson-style diagonal, not realistic potential
3. **S³ chirality placeholder** — vector of ones, not physical Γ₅ operator
4. **No global chiral index** — product-level topological index not computed
5. **Thermal constraint** — local execution blocked for large grids
6. **Negative controls incomplete** — 18/54 cases done, 36 pending

### What Gate 4B Does NOT Prove

- ❌ Physical compactification mechanism
- ❌ Continuum product geometry S³×S¹
- ❌ Standard Model gauge group derivation
- ❌ Protected chiral zero modes from near-zero modes
- ❌ Witten/Lichnerowicz no-go bypass
- ❌ Thermodynamic limit behavior
- ❌ Real cosmology or extra-dimensional stabilization

**If future GOE→Poisson signal observed:**  
It is a localization signal only. It is NOT evidence for chirality without
an index calculation.

---

## Next Active Step (Immediate)

**Task:** Execute negative controls batches 3-6 on remote infrastructure

**Prerequisites:**
1. Clone repo to remote environment
2. Install dependencies (`requirements.txt`)
3. Verify codebase integrity (`git log`, batch 1-2 outputs exist)

**Execution sequence:**
```bash
# Batch 3: scrambled_geometry, W=0
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3

# Batch 4: scrambled_geometry, W=20
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 4

# Batch 5: broken_wilson_term, W=0
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 5

# Batch 6: broken_wilson_term, W=20
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 6
```

**Expected runtime:** ~3-4 hours total (depends on hardware)

**Validation after each batch:**
```bash
# Check output files exist
ls reports/RUNS/negative_controls_v0.1.22/batch_0[3-6]/

# Verify case count (9 files per batch)
ls reports/RUNS/negative_controls_v0.1.22/batch_03/ | wc -l  # Should be 9
```

**Post-execution:**
1. Aggregate results: `python scripts/aggregate_negative_controls_v0_1_22.py`
2. Apply decision rules (threshold ≥2.0×, control consistency)
3. Write results report: `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`
4. Update README.md with verdict
5. Commit with message: `feat(controls): complete v0.1.22 negative controls pilot`

---

## Role of Future Agent

**You are a continuation agent** picking up where the previous session left off.

**Your responsibilities:**
1. **Execute remaining work** — batches 3-6 on remote infrastructure
2. **Preserve claim boundaries** — no forbidden claims in positive sections
3. **Respect immutability** — do NOT modify Gate 4B outputs or protocol
4. **Document honestly** — if control false-passes, report it transparently
5. **Follow pre-registration** — decision rules and grid are fixed in advance

**Your constraints:**
- Do NOT open v0.1.23 until v0.1.22 results are finalized
- Do NOT modify README.md until results report is complete
- Do NOT push to remote until user explicitly approves
- Do NOT bypass thermal constraint by forcing local execution
- Do NOT weaken decision rules if controls partially pass

**Your success criteria:**
- All 54 cases executed (18 local + 36 remote)
- Results aggregated with decision rules applied
- Verdict written: PASS_AS_EXPECTED / FALSE_PASS / WEAK
- No forbidden claims in results report
- Tom Lawrence attribution preserved

---

## Shortest Next Plan

**If you are the immediate next agent:**

1. **Setup remote environment** (Google Colab / cluster)
2. **Execute batch 3** (`--batch-id 3`)
3. **Validate output** (9 files in `batch_03/`)
4. **Execute batches 4-6** sequentially
5. **Aggregate results** (`aggregate_negative_controls_v0_1_22.py`)
6. **Write results report** (`S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`)
7. **Update README.md** with verdict
8. **Commit** with message: `feat(controls): complete v0.1.22 negative controls pilot`
9. **Report to user** — do NOT auto-push

**If results show FALSE_PASS:**
- Document which control(s) reproduced Gate 4B-like pattern
- Flag harness as lacking specificity
- Recommend harness refinement before Gate 5
- Do NOT proceed to larger S³×S¹ scaling

**If results show PASS_AS_EXPECTED:**
- Confidence in Gate 4B signal strengthened
- Harness discrimination power tested and confirmed
- Ready for Gate 5 (s1_size=256, 512 scaling) or Artifact Zoo next checks

---

## Key Documents for Context

**Gate 4B (v0.1.21):**
- `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md`
- `reports/CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md`
- `reports/CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md`

**v0.1.22 Planning:**
- `reports/S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md`
- `reports/NEGATIVE_CONTROLS_IMPLEMENTATION_PLAN_v0.1.22.md`
- `reports/CURRENT_STATUS_v0.1.22_NEGATIVE_CONTROLS_PLANNING.md`
- `reports/NEGATIVE_CONTROLS_REMOTE_EXECUTION_PLAN_v0.1.22.md`

**Attribution & Boundaries:**
- `docs/RESEARCH_CONTEXT.md`
- `docs/CLAIMS_AND_CAVEATS.md`
- `docs/ROADMAP.md`

**Codebase:**
- `cc_toy_lab/geometry/negative_controls.py` (controls module)
- `scripts/run_negative_controls_v0_1_22.py` (execution script)
- `tests/test_negative_controls_*.py` (test coverage)

---

**Status Date:** 2026-05-24  
**Handoff Type:** POST-PLANNING → PRE-EXECUTION  
**Next Agent Task:** Remote execution batches 3-6 (36 cases)  
**Gate 4B Status:** CLOSED (immutable)  
**v0.1.22 Status:** 18/54 complete, 36 pending  
**No new experiments:** This handoff is for execution of pre-registered protocol only
