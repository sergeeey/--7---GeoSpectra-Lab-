# Report Index — v0.1.21 Gate 4B

**Date:** 2026-05-22  
**Scope:** Gate 4B v0.1.21 metric-corrected campaign documentation  
**Status:** FINAL

---

## Navigation Guide

This index organizes all key documents for Gate 4B v0.1.21 metric-corrected finite-size scaling campaign, from metric mismatch discovery through final results and audit.

**Reading order for newcomers:**
1. CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md (start here)
2. S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md (why v0.1.21 was needed)
3. S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md (main results)
4. CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md (what can be claimed)

---

## 1. Current Status & Summary

### CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md
**Type:** Executive summary  
**Date:** 2026-05-22  
**Purpose:** One-page overview of Gate 4B final state, key metrics, verdict, caveats, and next steps

**Key sections:**
- Executive summary
- Repo state (commits, branches)
- Gate 4B result (216/216 cases, 0 failures)
- Key metrics (7.15× aggregate contrast, family contrasts, FSS trend)
- Final verdict (GATE4B_FSS_PASS_WITH_CAVEATS)
- Required caveats (6 mandatory)
- Next recommended branches (Gate 5, negative controls, cross-geometry, methodology report)

**Audience:** Internal review, quick reference, newcomer onboarding

---

### CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md
**Type:** Claims protocol  
**Date:** 2026-05-22  
**Purpose:** Canonical allowed claim, forbidden overclaims, expansion rules, audience-specific guidelines

**Key sections:**
- Allowed claim (canonical statement with caveats)
- Allowed claims (5 categories: finite-lattice robustness, family consistency, r-statistic, metric correction, controls)
- Forbidden claims (10 hard blocks: S³×S¹ validated, FL generalized, W=20 optimal, thermodynamic limit, physical compactification, etc.)
- Claim expansion rules (5 rules)
- Audience-specific guidelines (internal, external, grants, casual)
- Violation examples (real-world anti-patterns)

**Audience:** Anyone communicating Gate 4B results externally or internally

---

## 2. Metric Correction Chain (v0.1.20 → v0.1.21)

### S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md
**Type:** Erratum  
**Date:** 2026-05-22  
**Purpose:** Document Gate 4A v0.1.20 metric mismatch discovery and root cause

**Key findings:**
- Gate 4A used `np.linalg.eigvalsh(H)` → returns eigenvalues ONLY
- Primary metric was mean(eigenvalues), NOT true IPR = mean(Σ|ψᵢ|⁴)
- True IPR unmeasurable from v0.1.20 outputs
- Gate 4A verdict: WEAK_OR_INCONCLUSIVE (r-statistic valid, primary metric invalid)
- Full 216-case rerun required (NO recovery from v0.1.20 outputs)

**Root cause:** Performance optimization (eigvalsh faster than eigh) invalidated metric

**Audience:** Postmortem, methodology review, lesson learned

---

### GATE4_TRUE_IPR_RECOVERY_CHECK_v0.1.20.md
**Type:** Recovery feasibility analysis  
**Date:** 2026-05-22  
**Purpose:** Determine if v0.1.20 outputs can be salvaged or full rerun needed

**Conclusion:** Full rerun required (eigenvalues alone cannot recover true IPR)

**Alternatives considered:**
- ❌ Approximate IPR from eigenvalues → mathematically invalid
- ❌ Use r-statistic only → insufficient for primary metric
- ✅ Full rerun with `eigh` (compute eigenvectors) → chosen path

**Audience:** Decision record, methodology

---

### IPR_IMPLEMENTATION_AUDIT_v0.1.20.md
**Type:** Implementation audit  
**Date:** 2026-05-22 (before v0.1.21 execution)  
**Purpose:** Verify true IPR implementation before v0.1.21 rerun

**Checks:**
- IPR formula correctness (Σ|ψᵢ|⁴ / (Σ|ψᵢ|²)²)
- Eigenvector computation (`eigh` not `eigvalsh`)
- Unit tests (17 tests covering localized, delocalized, random, zero, batching)
- Output schema (true_ipr_mean, uses_eigenvectors flag)

**Verdict:** Implementation correct, ready for v0.1.21 rerun

**Audience:** Pre-execution verification, quality gate

---

## 3. Protocol & Pre-Registration

### S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md
**Type:** Pre-registration protocol  
**Commit:** 5e5ffc9  
**Date:** 2026-05-22 (before execution)  
**Purpose:** Lock grid, thresholds, decision rules BEFORE seeing results

**Pre-registered elements:**
- Grid: 216 cases (3 families × 3 W × 4 sizes × 2 j_max × 3 seeds)
- Thresholds: ≥2.0× aggregate contrast for PASS, ≥2/3 family consistency
- Decision rules: 7 conditions (Section 8.1)
- Claim language: allowed/forbidden lists
- Metric version: v0.1.21_true_eigenvector_ipr

**Immutability:** NO post-hoc changes to grid, thresholds, or decision rules after commit 5e5ffc9

**Audience:** Protocol compliance, reproducibility, anti-p-hacking

---

### S3_S1_GATE4_BATCH_PROTOCOL_v0.1.21.md
**Type:** Execution protocol  
**Date:** 2026-05-22 (before execution)  
**Purpose:** Batching strategy, runtime estimates, scheduling

**Batching:**
- 9 batches × 24 cases
- Sequential execution (one batch at a time)
- Estimated total: 1.5–2.5 hours

**Checklist:**
- Pre-run checklist (12 items)
- Per-batch checklist (5 items)
- Post-run checklist (8 items)

**Audience:** Execution guide, reproducibility

---

### S3_S1_GATE4_BATCH_EXECUTION_PROGRESS_v0.1.20.md ⚠️
**Type:** Execution log (v0.1.20, ARCHIVED)  
**Status:** Historical record only  
**Purpose:** Document v0.1.20 execution (before metric error discovery)

**Note:** This is v0.1.20 progress, NOT v0.1.21. Keep for historical context but DO NOT use for v0.1.21 results.

**Audience:** Historical reference

---

## 4. Execution & Results (v0.1.21)

### S3_S1_GATE4B_RAW_EXECUTION_FREEZE_v0.1.21.md
**Type:** Execution freeze  
**Date:** 2026-05-22 13:15 Almaty (after execution, BEFORE analysis)  
**Purpose:** Freeze raw execution state BEFORE scientific interpretation

**Key facts:**
- 216/216 cases completed (100%)
- 0 failures
- 9/9 batches completed
- 1.83 hours runtime (109.8 min, 6587.7 sec)
- true_ipr_mean availability: 216/216 (100%)
- r_stat availability: 216/216 (100%)

**Principle:** "Execution completion ≠ scientific PASS verdict"

**Audience:** Audit trail, execution integrity

---

### S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md
**Type:** Final scientific results report  
**Date:** 2026-05-22 14:30 Almaty  
**Commit:** f7eff32  
**Purpose:** Full scientific analysis, verdict, caveats

**Key sections:**
- Executive summary (caveat-first)
- Protocol reference
- Why Gate 4B was needed (v0.1.20 metric error)
- Execution summary (216/216 cases)
- True IPR results (aggregate 7.15×, family contrasts, FSS trend)
- r-statistic results (Δr = -0.163)
- Control baseline (W=0 stability)
- Decision rule application (7/7 PASS)
- Final verdict (GATE4B_FSS_PASS_WITH_CAVEATS)
- Caveats (6 mandatory)
- Allowed/forbidden claims
- Comparison with v0.1.20
- Next steps

**Audience:** Primary scientific record, external communication source

---

### reports/RUNS/gate4_fss_v0.1.21/
**Type:** Raw execution artifacts  
**Date:** 2026-05-22  
**Purpose:** Raw batch outputs, merged aggregations, config

**Structure:**
```
reports/RUNS/gate4_fss_v0.1.21/
├── config.json                          # Execution config
├── batches/
│   ├── batch_01/ ... batch_09/          # 9 batch folders
│   │   ├── batch_config.json            # Batch parameters
│   │   ├── results.json                 # 24 case results per batch
│   │   ├── status.json                  # Batch status
│   │   ├── summary.md                   # Batch summary
│   │   └── timing.json                  # Batch timing
└── merged/
    ├── coverage.json                    # 216 unique cases, 0 duplicates
    ├── failure_summary.json             # 0 failures
    ├── family_summary.json              # 3 families
    ├── metrics.json                     # 216 true_ipr_mean + r_stat values
    ├── r_stat_summary.json              # 36 groups (family × W × size)
    ├── size_scaling_summary.json        # 4 sizes
    ├── timing_summary.json              # 1.83h total
    ├── true_ipr_contrast_summary.json   # 72 per-seed + 24 aggregate contrasts
    └── verdict_analysis.json            # GATE4B_FSS_PASS_WITH_CAVEATS
```

**Audience:** Raw data analysis, reproducibility, audit

---

## 5. Audit & Integrity

### GATE4B_PRE_PUSH_AUDIT_v0.1.21.md
**Type:** Pre-push scientific audit  
**Date:** 2026-05-22 15:45 Almaty  
**Commit:** 84210c8 (audit report commit)  
**Audited commit:** f7eff32 (results commit)  
**Purpose:** Final pre-push integrity check

**Audit checks (8 points):**
1. ✅ Git / raw artifact integrity (9 batches, merged files, git clean)
2. ✅ Metric implementation (true IPR = Σ|ψ|⁴, 17 tests passed, eigh verified)
3. ✅ Metric separation (no v0.1.20 eigenvalue proxy confusion)
4. ✅ Contrast verification (7.15× aggregate, family contrasts correct)
5. ✅ N caveat (896 everywhere, N=7424 errors corrected)
6. ✅ Wording audit (no forbidden overclaims, r-stat uses "supports")
7. ✅ Caveats preserved (all 6 mandatory caveats present)
8. ✅ Audit report created

**Verdict:** SAFE_TO_PUSH (0 blocking issues, 0 minor issues)

**Audience:** Final quality gate, push decision record

---

## 6. Scripts & Implementation

### scripts/run_gate4_batched.py
**Type:** Execution script  
**Purpose:** Run batched Gate 4B execution with eigenvector computation

**Key implementation:**
- Line 228: `eigvals, eigvecs = np.linalg.eigh(H)` (NOT eigvalsh)
- Computes true IPR from eigenvectors
- Outputs: true_ipr_mean, r_stat, eigenvalue diagnostics

**Audience:** Implementation review, reproducibility

---

### scripts/aggregate_gate4b_results.py
**Type:** Aggregation script (210 lines)  
**Purpose:** Merge 9 batch outputs into aggregated metrics

**Key functions:**
- `load_all_results()` — load 216 results from 9 batches
- `compute_family_summary()` — aggregate by family
- `compute_size_scaling_summary()` — aggregate by s1_size
- `compute_r_stat_summary()` — aggregate r-statistic
- `compute_true_ipr_contrast_summary()` — compute W=20 vs W=0 contrasts

**Audience:** Data processing pipeline, reproducibility

---

### scripts/apply_gate4b_decision_rules.py
**Type:** Decision rules script (461 lines)  
**Purpose:** Apply pre-registered decision rules from protocol

**Key functions:**
- `check_aggregate_contrast()` — verify ≥2.0×
- `check_family_consistency()` — verify ≥2/3 families PASS
- `analyze_finite_size_trend()` — compute ratio contrasts per size
- `check_controls()` — verify W=0 stability within each size
- `apply_decision_rules()` — apply all 7 conditions

**Verdict logic:** ALL 7 conditions PASS → GATE4B_FSS_PASS_WITH_CAVEATS

**Bug fixes (v0.1.21):**
- Fixed FSS trend to use ratio contrasts (not absolute)
- Fixed control stability to check within-size (not mixed sizes)

**Audience:** Decision logic, reproducibility

---

### cc_toy_lab/spectral/metrics.py
**Type:** Core metric implementation  
**Lines:** 21-45 (IPR function)  
**Purpose:** True IPR computation

**Implementation:**
```python
def inverse_participation_ratio(vector: np.ndarray) -> float | np.ndarray:
    """IPR = sum |psi|^4 / (sum |psi|^2)^2."""
    arr = np.asarray(vector)
    if arr.ndim == 1:
        norm_sq = np.sum(np.abs(arr) ** 2)
        if norm_sq < 1e-15:
            raise ValueError("Cannot compute IPR for zero vector")
        denom = norm_sq**2
        return float(np.sum(np.abs(arr) ** 4) / denom)
    # ... batching logic for 2D arrays
```

**Audience:** Implementation review, unit tests

---

### tests/test_ipr_metric.py
**Type:** Unit tests  
**Purpose:** Test true IPR implementation

**17 tests:**
- test_ipr_fully_localized_real → IPR ≈ 1.0
- test_ipr_fully_delocalized_real → IPR ≈ 1/N
- test_ipr_random_normalized_real → IPR ∈ (1/N, 1)
- test_ipr_zero_vector_raises_error → ValueError
- test_ipr_matrix_input_multiple_eigenvectors → batching
- test_ipr_bottom_10_percent_eigenvectors → Gate 4B scenario
- test_ipr_vs_eigenvalue_mean_not_equal → metrics differ
- ... 10 more tests

**Audience:** Quality assurance, reproducibility

---

## 7. Historical Context (v0.1.20 ARCHIVED)

### S3_S1_GATE4A_FSS_RESULTS_v0.1.20.md ⚠️
**Type:** Historical results (ARCHIVED)  
**Status:** WEAK_OR_INCONCLUSIVE  
**Purpose:** Gate 4A results with invalid metric (eigenvalue mean)

**Verdict:** v0.1.20 verdict remains WEAK (NO retroactive upgrade)

**Note:** DO NOT cite as valid scientific result. Use v0.1.21 only.

**Audience:** Historical record, postmortem, lesson learned

---

## Document Lifecycle

| Document | Status | Mutability | Next Review |
|----------|--------|------------|-------------|
| CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md | FINAL | Frozen | 2026-06-05 (2-week window) |
| CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md | FINAL | Frozen | Before any external communication |
| S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md | FINAL | Frozen | — |
| GATE4B_PRE_PUSH_AUDIT_v0.1.21.md | FINAL | Frozen | — |
| S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md | LOCKED | Frozen (pre-registered) | — |
| reports/RUNS/gate4_fss_v0.1.21/ | ARCHIVED | Frozen (raw data) | — |

**Frozen:** No edits allowed without explicit version bump (v0.1.22)  
**LOCKED:** Pre-registered, no edits allowed ever (protocol immutability)

---

## Quick Lookup

**Need to know Gate 4B verdict?**  
→ CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md (section: Final Verdict)

**Need to know what can be claimed?**  
→ CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md (section: Allowed Claim)

**Need to know why v0.1.21 was needed?**  
→ S3_S1_GATE4_METRIC_MISMATCH_ERRATUM_v0.1.20.md

**Need to know key metrics?**  
→ CURRENT_STATUS_v0.1.21_GATE4B_FINAL.md (section: Key Metrics)

**Need to cite pre-registration?**  
→ S3_S1_GATE4_FSS_PREREGISTRATION_v0.1.21.md (commit: 5e5ffc9)

**Need to audit implementation?**  
→ GATE4B_PRE_PUSH_AUDIT_v0.1.21.md (section: Metric Implementation Check)

**Need raw data?**  
→ reports/RUNS/gate4_fss_v0.1.21/merged/*.json

---

**Index Version:** v0.1.21  
**Last Updated:** 2026-05-22  
**Status:** FINAL
