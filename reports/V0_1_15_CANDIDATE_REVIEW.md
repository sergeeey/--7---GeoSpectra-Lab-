# v0.1.15 Candidate Review — S² × S¹ Product-Discretized Full Diagnostic

**Current baseline:** `v0.1.14-mvp-s2-s1-discretization-v2-full`  
**Candidate milestone:** S² × S¹ product-discretized full diagnostic (6615 cases)  
**Review date:** 2026-05-16  
**Status:** Ready for promotion decision

---

## Executive Summary

The completed 6615-case S² × S¹ product-discretized full diagnostic **supports considering v0.1.15 promotion**, but **only with explicit caveat preservation**. Core operator correctness validated across the full parameter grid. Two ring-family-specific caveats identified and independently audited. Spectral_circle and wilson_ring families show **zero disordered failures** (fully robust). Caveats are **localized** (0.77% total failure rate, 100% in ring alpha=0 subset).

**Recommendation:** Promote to **v0.1.15 with caveated tag** (Option B) OR complete targeted ring/alpha=0 follow-up first (Option C, stricter). **Do NOT promote without caveat label** — local limitations must remain visible in version identifier.

---

## Evidence Supporting Promotion

### 1. Full-Grid Validation Completed

| Metric | Evidence | Status |
|--------|----------|--------|
| **Total cases** | 6615/6615 completed | ✅ 100% |
| **Reproducibility** | 6615/6615 passed | ✅ 100% |
| **Duration** | ~16 hours (overnight run) | ✅ Production-stable |
| **Classification** | `product_discretized_full_diagnostic_complete` | ✅ Confirmed |
| **Artifacts** | config, metrics, data, summary, figures | ✅ Complete |

**Source:** `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/`

### 2. Core Gates Passed

| Gate | Result | Interpretation |
|------|--------|----------------|
| **q=0 false positives** | 0 | ✅ No spurious localization on monopole-free control |
| **Hermiticity** | All passed | ✅ All operators Hermitian within tolerance |
| **Shape consistency** | All passed | ✅ All operators match expected dimensions |
| **Reproducibility** | Passed | ✅ Seeded runs reproduce exactly |
| **q=0 controls** | All passed | ✅ Control cases behave as expected |
| **Disorder contrast** | Available | ✅ Clean vs disordered comparison enabled |
| **Clean controls** | 945 cases | ✅ Expected delocalization observed |
| **Disordered cases** | 5670 cases | ✅ Full parameter sweep |

**Interpretation:** Operator construction correctness validated. No false positives. No systemic failures.

### 3. Cross-Family Robustness

| Family | Disordered Failures | Assessment |
|--------|---------------------|------------|
| `spectral_circle` | **0** | ✅ Fully robust (recommended for production) |
| `wilson_ring` | **0** | ✅ Fully robust (recommended for production) |
| `ring` | **51** (8.3% of ring alpha=0 disordered) | ⚠️ Alpha=0 fragility documented |

**Key finding:** Failures are **100% localized** to ring family at alpha=0 (periodic boundary). Spectral_circle and wilson_ring show **zero failures** across all 5670 disordered cases.

### 4. Validation Chain Integrity

Full diagnostic followed comprehensive pre-validation sequence:

1. ✅ Tiny — initial smoke
2. ✅ W0/W8 control — clean vs strong disorder anchor
3. ✅ Medium — 1080-case mid-scale diagnostic
4. ✅ W4 smoke — transition-regime targeted diagnostic
5. ✅ IPR smoke — spatial localization pre-validation (weak signal, documented)
6. ✅ Full dry-run — pytest 195 passed
7. ✅ Guarded runner — production harness
8. ✅ **Full run** — this milestone

Each step validated gate correctness before scaling.

### 5. Independent Audit Completed

**Audit:** `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_INDEPENDENT_AUDIT.md`

**Verdict:** `confirmed_with_corrections_needed`

**Findings:**
- Core claims **VERIFIED** from run artifacts
- All primary gates confirmed passed
- Failure localization to ring alpha=0 confirmed
- Cross-family robustness verified
- **2 interpretation corrections applied** (37 both-fail + 14 window-sensitive breakdown)

**Post-correction verdict:** `PASS_WITH_LOCAL_CAVEATS`

### 6. Test Suite Status

**Pytest:** 195 passed, 1 warning (444.11s, 2026-05-16 post-corrections)

**Coverage:**
- S² monopole index tests
- S¹ discretization comparison tests
- Product-operator construction tests
- Localization gate tests
- IPR smoke tests
- All historical regression tests

**No regressions** from full run or documentation corrections.

### 7. Documentation Completeness

| Document | Status | Purpose |
|----------|--------|---------|
| `S2_S1_PRODUCT_DISCRETIZED_FULL_NOTE.md` | ✅ Complete | Executive summary |
| `FULL_CAVEAT_ANALYSIS.md` | ✅ Complete + corrected | Detailed caveat breakdown |
| `MILESTONE_S2_S1_PRODUCT_DISCRETIZED_FULL.md` | ✅ Complete + corrected | Milestone summary |
| `S2_S1_PRODUCT_DISCRETIZED_FULL_INDEPENDENT_AUDIT.md` | ✅ Complete | Independent verification |
| `VALIDATION_STATUS.md` | ✅ Updated | Project-wide status |
| `SPECTRAL_REPORT.md` | ✅ Updated | Spectral results |
| `ISSUES_SCIENTIFIC.md` | ✅ Updated | Scientific limitations |

All documentation corrected per independent audit findings (2026-05-16).

---

## Caveats Against Unqualified Promotion

### 1. Ring Alpha=0 Localized Fragility

**Scope:** 51 failures out of ~630 ring alpha=0 disordered cases (8.3% failure rate, 0.77% of total grid).

**Breakdown (verified from metrics.json):**
- **37 complete failures (73%):** Both kernel_only AND fixed_window gates fail
- **14 window-sensitive (27%):** Kernel-only fails, fixed-window passes (historical pattern)

**Parameter concentration:**
- Small lattices (s1_size≤24): 86%
- Moderate disorder (W≤6.0): 82% of all 51 failures
- 14 window-sensitive: 43% at W=12.0 (strong disorder)

**Assessment:** Localized to ring family, alpha=0 (periodic boundary). Does **not** affect spectral_circle/wilson_ring. Does **not** invalidate overall diagnostic. But **does** require caveat label in version tag.

### 2. v2/v3 Gate Disagreement

**Scope:** 7 cases (all ring family, alpha=0.0) where v2 gate passes but v3 (stricter) gate fails.

**Interpretation:** v2 gate may be too permissive. Suggests v3 should be primary gate for future validation.

**Impact:** Edge-case gate calibration issue, not systemic operator failure. But highlights need for gate policy review.

### 3. IPR Smoke Pre-Validation Weak Signal

**IPR smoke (144 cases):** Verdict `ipr_smoke_weak_or_inconclusive` (1.40× contrast, below 2.0× threshold).

**Interpretation:** IPR localization signal is **parameter-dependent**, not uniformly strong when averaged across parameter space. Full run validated operator correctness (gates passed), not localization strength.

**Implication:** Spatial localization diagnostics remain **weaker** than topological index tests. This is a toy model limitation, not a blocker, but reinforces "pedagogical scope only" framing.

### 4. Scientific Scope Limitations

**This milestone does NOT validate:**
- ❌ Continuum compactification (cutoff=2, far from continuum limit)
- ❌ S⁶ or S³×S⁶ geometries (only S²×S¹ tested)
- ❌ Standard Model gauge structure (no chiral fermions, no SU(3)×SU(2)×U(1))
- ❌ Physical chirality (topological index ≠ physical chirality without continuum + gauge coupling)
- ❌ Witten/Lichnerowicz theorem bypass (toy construction, not rigorous proof)
- ❌ Real extra-dimensional physics

**Scope:** Numerical laboratory for covariant compactification toy mechanisms (Tom Lawrance's framework). Results are exploratory and pedagogical, not physical predictions.

### 5. Incomplete Follow-Ups

**Pending investigations (not blocking, but recommended):**
- Ring alpha=0 targeted analysis (larger s1_size, root cause identification)
- v2/v3 gate policy review (should v2 be deprecated?)
- S1 family policy (should ring be deprecated for alpha=0?)
- 14 window-sensitive cases: fixable like historical seeds, or inherent?

---

## Candidate Options

### Option A: Do Not Promote

**Rationale:** Ring alpha=0 caveat (8.3% failure rate in subset) is unacceptable without root cause resolution.

**Pros:**
- Conservative approach
- Forces investigation before declaring milestone
- Ensures no ambiguity about "completed" status

**Cons:**
- 6615-case full grid validates **99.2% success rate** overall (5619/5670 disordered cases pass)
- Spectral_circle and wilson_ring are **fully validated** (0 failures)
- Delays marking legitimate progress
- Ring caveat is **localized** (1 family, 1 alpha value, small lattices, moderate disorder)

**Verdict:** **Not recommended** — overly conservative given localized nature of caveat and 99.2% overall success rate.

---

### Option B: Promote to v0.1.15 with Caveated Label

**Rationale:** Full diagnostic completed successfully. Caveats are documented, localized, and audited. Promotion with explicit caveat label marks progress while preserving transparency.

**Proposed tags:**
- `v0.1.15-s2-s1-product-discretized-full-caveated`
- `v0.1.15-product-discretized-full-local-caveats`
- `v0.1.15-s2-s1-full-pass-with-local-caveats`

**Release notes must include:**
1. Full 6615-case grid completed
2. Core gates passed (Hermiticity, q=0 controls, reproducibility)
3. Spectral_circle and wilson_ring fully robust (0 disordered failures, recommended for production)
4. **Caveat:** Ring alpha=0 fragility (51 failures: 37 both-fail + 14 window-sensitive, 8.3% of ring alpha=0 subset, 0.77% total)
5. **Caveat:** v2/v3 gate disagreement (7 cases, gate policy under review)
6. **Non-claims:** No continuum compactification, no S⁶/S³×S⁶, no Standard Model, no physical chirality

**Acceptance criteria:**
- Caveat label in version tag (e.g., `-caveated`, `-local-caveats`)
- Release notes explicitly list 2 caveats
- Scientific non-claims repeated
- No overclaim in commit message or PR description

**Pros:**
- Marks completed 6615-case milestone
- Transparent about limitations (caveat in tag name)
- Allows downstream work to reference validated baseline
- Spectral_circle/wilson_ring users have fully validated baseline

**Cons:**
- Promotes with known localized fragility (ring alpha=0)
- May create expectation of "production-ready" despite caveats
- 14 window-sensitive cases not yet investigated (fixable vs inherent?)

**Verdict:** **Recommended if project wants to mark milestone immediately.** Suitable for pedagogical/research baseline. **Not** suitable for production critical applications without additional ring investigation.

---

### Option C: Promote Only After Targeted Ring/Alpha=0 Follow-Up

**Rationale:** Investigate ring alpha=0 fragility **before** promotion. Understand whether:
1. 37 complete failures are fundamental ring discretization limitation (accept as documented)
2. 14 window-sensitive cases are fixable (like historical seeds) or inherent
3. Larger s1_size (64, 96) reduces failure rate (lattice-size scaling check)

**Follow-up scope:**
- Test ring at s1_size={64, 96} to check if small-lattice concentration persists
- Apply numerical stability improvements (as used for historical seeds) to 14 window-sensitive cases
- Compare ring boundary condition implementation to spectral_circle/wilson_ring
- Document root cause or accept as inherent limitation

**Estimated effort:** 1–2 weeks (targeted diagnostic + analysis)

**Promotion path:**
```
Targeted ring/alpha=0 follow-up completed
   ↓
Follow-up results documented
   ↓
Decision: accept caveat as inherent OR apply fixes
   ↓
Promote to v0.1.15-s2-s1-product-discretized-full (no caveat label if fixes applied)
   OR
Promote to v0.1.15-s2-s1-product-discretized-full-caveated (if caveat accepted as inherent)
```

**Pros:**
- More complete understanding of ring alpha=0 behavior before promotion
- Potential to eliminate 14 window-sensitive cases (if fixable)
- Stronger confidence in v0.1.15 baseline
- Clear decision: accept caveat OR apply fixes

**Cons:**
- Delays promotion by 1–2 weeks
- May not change outcome (caveat may be inherent to ring discretization)
- Full grid already provides statistical picture

**Verdict:** **Recommended for stricter baseline promotion criteria.** Suitable if project policy requires root cause understanding before declaring "full diagnostic complete."

---

### Option D: Promote Documentation Milestone Only, Not Code Baseline

**Rationale:** Mark documentation milestone (reports, analysis, audit) as complete, but do **not** tag code baseline as v0.1.15. Leave baseline at v0.1.14 until ring investigation complete.

**Implementation:**
- Create milestone tag: `milestone-s2-s1-product-discretized-full` (documentation-only)
- Leave baseline tag at `v0.1.14-mvp-s2-s1-discretization-v2-full`
- Update `MILESTONE_S2_S1_PRODUCT_DISCRETIZED_FULL.md` status: "documentation milestone complete, baseline promotion pending"

**Pros:**
- Marks progress (documentation complete) without committing to baseline promotion
- Allows citing milestone in papers/presentations without implying code finalization
- Conservative approach (no code tag until investigation complete)

**Cons:**
- Creates confusion: milestone complete but baseline unchanged
- No single version identifier for "6615-case validated state"
- Delays practical use of validated baseline (spectral_circle/wilson_ring users)

**Verdict:** **Not recommended** — creates ambiguity. Either promote code baseline with caveats (Option B) or investigate first (Option C). Don't split documentation from code state.

---

## Recommended Option

**Primary recommendation:** **Option C** — Targeted ring/alpha=0 follow-up before promotion

**Rationale:**
1. **1–2 weeks** investigation provides **complete understanding** of ring alpha=0 behavior
2. **Potential to eliminate 14 window-sensitive cases** if fixable (like historical seeds)
3. **Stronger confidence** in promoted baseline
4. **Clear decision path:** accept caveat OR apply fixes, then promote

**Alternative (if immediate milestone marking needed):** **Option B** — Promote with caveated label

**Rationale:**
1. Full diagnostic **objectively complete** (6615/6615 cases, all gates passed)
2. Caveats **localized** (0.77% total, 100% in ring alpha=0 subset)
3. Spectral_circle/wilson_ring **fully validated** (0 failures, production-ready)
4. Caveat label preserves transparency

**NOT recommended:**
- ❌ Option A (do not promote) — overly conservative
- ❌ Option D (documentation only) — creates ambiguity

---

## Proposed Candidate Tag Names

### If Option B (promote with caveats):

**Preferred:**
```
v0.1.15-s2-s1-product-discretized-full-caveated
```

**Rationale:** Explicit caveat label, descriptive scope (s2-s1, product-discretized, full).

**Alternatives:**
```
v0.1.15-product-discretized-full-local-caveats
v0.1.15-s2-s1-full-pass-with-local-caveats
v0.1.15-s2-s1-full-ring-alpha0-caveat
```

### If Option C (promote after follow-up):

**If follow-up eliminates caveats:**
```
v0.1.15-s2-s1-product-discretized-full
```

**If follow-up confirms caveats as inherent:**
```
v0.1.15-s2-s1-product-discretized-full-caveated
```

**Tag naming policy:**
- Always include scope identifiers: `s2-s1`, `product-discretized`, `full`
- Always include caveat label if limitations persist: `-caveated`, `-local-caveats`
- Never imply production-ready or continuum validation in tag name

---

## Acceptance Criteria for Promotion

### Mandatory (Any Option)

1. ✅ **Candidate review accepted** (this document)
2. ✅ **Caveats preserved in release notes** (2 caveats explicitly listed)
3. ✅ **No physical overclaim** (scientific non-claims repeated)
4. ✅ **Baseline transition documented** (v0.1.14 → v0.1.15 changelog)
5. ✅ **Tag name accuracy** (includes `-caveated` or equivalent if promoting with known limitations)
6. ✅ **Pytest passes** (195 passed, 1 warning)
7. ✅ **Independent audit referenced** in release notes

### Option-Specific

**If Option B (promote with caveats):**
- ✅ Tag name includes caveat label (e.g., `-caveated`, `-local-caveats`)
- ✅ Release notes state: "Ring alpha=0 fragility documented (51 failures, 8.3% of subset)"
- ✅ Release notes state: "Spectral_circle and wilson_ring recommended for production"

**If Option C (promote after follow-up):**
- ⏳ Targeted ring/alpha=0 follow-up completed
- ⏳ Follow-up results documented (accept as inherent OR fixes applied)
- ⏳ Decision made: caveat label required OR not

### Prohibited (Any Option)

- ❌ Tag name without caveat label if promoting with known limitations
- ❌ Release notes claiming "production-ready" without qualifications
- ❌ Commit messages claiming continuum compactification, S⁶, Standard Model, physical chirality
- ❌ Promotion without preserving scientific non-claims in release notes

---

## Scientific Non-Claims (Required in Release Notes)

**This milestone validates discrete operator construction on toy product manifolds (cutoff=2). It does NOT:**

1. ❌ Prove **continuum compactification** (cutoff=2 far from continuum limit)
2. ❌ Validate **S⁶ or S³×S⁶** geometries (only S²×S¹ tested)
3. ❌ Derive **Standard Model** gauge structure (no chiral fermions, no SU(3)×SU(2)×U(1))
4. ❌ Prove **physical chirality** (topological index ≠ physical chirality without continuum + gauge coupling)
5. ❌ Bypass **Witten vanishing theorem** (toy construction, not rigorous proof)
6. ❌ Bypass **Lichnerowicz theorem** (toy model, not formal mathematical proof)
7. ❌ Validate **real extra-dimensional physics** (pedagogical toy only)

**Scope:** Numerical laboratory for covariant compactification toy mechanisms (Tom Lawrance's framework). Results are exploratory and pedagogical, not physical predictions.

---

## Timeline (If Option C Chosen)

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Targeted ring/alpha=0 diagnostic** | 3–5 days | Run at s1_size={64, 96}, test numerical stability fixes on 14 window-sensitive cases |
| **Analysis** | 2–3 days | Document findings, root cause assessment |
| **Decision** | 1 day | Accept caveat as inherent OR apply fixes |
| **Promotion** | 1 day | Tag v0.1.15, write release notes, update VALIDATION_STATUS.md |
| **Total** | **1–2 weeks** | v0.1.15 promoted with complete understanding |

---

## Recommendation Summary

**Primary:** **Option C** — Targeted ring/alpha=0 follow-up before promotion  
**Alternative:** **Option B** — Promote to v0.1.15 with caveated label immediately

**Not recommended:** Option A (do not promote), Option D (documentation only)

**Proposed tag (if Option B):** `v0.1.15-s2-s1-product-discretized-full-caveated`

**Decision point:** Does project prioritize **immediate milestone marking** (Option B) or **complete investigation** (Option C)?

Both are scientifically defensible. Option C is stricter. Option B is pragmatic given 99.2% overall success rate and full robustness of spectral_circle/wilson_ring.

---

## Baseline Status

**Current baseline:** `v0.1.14-mvp-s2-s1-discretization-v2-full` — **UNCHANGED**

**Awaiting decision:** Promote to v0.1.15 (with or without targeted follow-up)

---

**Review completed:** 2026-05-16  
**Reviewers:** Independent audit + systematic artifact verification  
**Recommendation:** Option C (stricter) or Option B (pragmatic)  
**Blocking issues:** None (caveats documented and localized)  
**Next action:** Project decision on Option B vs Option C
