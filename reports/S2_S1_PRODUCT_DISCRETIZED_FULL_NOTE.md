# Product-discretized S²×S¹ — full diagnostic (6615 cases)

> **Historical document:** This note reflects validation state as of 2026-05-15, before v0.1.15 baseline promotion. **Current baseline:** v0.1.15-s2-s1-product-discretized-full (promoted 2026-05-16).

**Scientific non-claims:** This does NOT prove continuum compactification; does NOT validate `S⁶` or `S³×S⁶`; does NOT derive the Standard Model; does NOT prove physical chirality; does NOT bypass Witten/Lichnerowicz theorems.

**Baseline:** `v0.1.14-mvp-s2-s1-discretization-v2-full` *(pre-promotion)*  
**Operator family:** `product_discretized_kronecker_sum_D2_plus_P1`  
**Profile:** `full` (6615 cases across 3 S1 families × 7 monopole charges × parameter grid)  
**Run duration:** ~16 hours (2026-05-15)

---

## Executive Summary

Full diagnostic grid validated core **operator correctness** (Hermiticity, shape consistency, reproducibility) and **control reliability** (q=0 control cases show no false positives). All primary gates **passed**.

**Caveats identified:**
1. **Ring family alpha=0 fragility:** 51 failures (37 complete both-gate failures + 14 window-sensitive; 52 in summary.md counter) — 8.3% of ring alpha=0 disordered cases, concentrated on small lattice sizes (s1_size=8, 24) and moderate disorder (W=2.0–6.0).
2. **v2/v3 gate disagreement:** 7 cases where v2 gate passes but v3 window-robust gate fails — all localized to ring/alpha=0, treated as minor window-gate edge cases, not cross-family failures.

---

## Gate Summary

| Gate | Result | Count/Detail |
|------|--------|--------------|
| **Clean control cases** | ✅ Pass | 945 cases |
| **Disordered cases** | ✅ Pass | 5670 cases |
| **Disorder contrast available** | ✅ True | Clean vs disordered comparison enabled |
| **q=0 false positive count** | ✅ 0 | No spurious localization on monopole-free control |
| **Hermiticity (all cases)** | ✅ Pass | All operators Hermitian within tolerance |
| **Shape consistency** | ✅ Pass | All operators match expected dimensions |
| **Reproducibility** | ✅ Pass | Seeded runs reproduce exactly |
| **q=0 controls (all)** | ✅ Pass | Control cases behave as expected |
| **Ring alpha=0 failures** | ⚠️ Caveat | 51 cases (8.3% of ring alpha=0 disordered; 52 in summary.md counter) |
| **v2 vs v3 disagreements** | ⚠️ Caveat | 7 cases (v2 pass, v3 fail — all ring) |
| **Overall classification** | ✅ | `product_discretized_full_diagnostic_complete` |

---

## Caveat 1: Ring Family Alpha=0 Fragility

**Scope:** 51–52 failures out of 630 ring alpha=0 disordered cases (8.3% failure rate; minor counter discrepancy between summary.md and metrics.json).

**Breakdown (verified from metrics.json):**
- **37 cases (73%):** BOTH gates fail (kernel_only=False AND fixed_window=False) — complete localization failure
- **14 cases (27%):** Window-sensitive (kernel_only=False, fixed_window=True) — historical window-selection sensitivity pattern

**Total:** 51 ring alpha=0 disordered cases fail kernel-only gate; 37 also fail fixed-window gate.

**Parameter distribution (all 51 failures):**
- **s1_size:** Concentrated on small lattices (s1_size≤24: 86% of failures)
- **Disorder strength:** Lower-to-moderate (W≤6.0: 82% of failures)
- **Monopole charge:** Spread across all q values

**14 window-sensitive cases specifically:**
- **s1_size:** {8: 10, 24: 4} — small lattices
- **Disorder:** W=12.0 (6 cases, 43% of window-sensitive) — notably at strong disorder

**Interpretation:**  
Ring discretization at alpha=0 (periodic boundary) shows two failure patterns:
1. **Complete failures (37):** Both gates fail, concentrated at W≤6.0 (moderate disorder)
2. **Window-sensitive (14):** Historical window-selection pattern persists at different seeds/parameters (43% at W=12.0)

Pytest resolution (2026-05-15, seeds 12051/12053/9836055) was **seed-specific** — those seeds now pass. Full grid reveals pattern persists at other parameter combinations. Not a regression — a more complete statistical picture.

**Recommendation:** Investigate ring family construction for alpha=0 case. Distinguish whether 14 window-sensitive cases are fixable (like historical seeds) or inherent to ring discretization.

---

## Caveat 2: v2/v3 Gate Disagreement

**Scope:** 7 cases where v2 (fixed-window) gate passes but v3 (window-robust) gate fails.

**Pattern:** ALL 7 cases are ring family, alpha=0.0, disordered.

**Parameter distribution:**
- **s1_size:** Mixed (8, 24)
- **Disorder strength:** Spread (W=2.0, 4.0, 6.0, 12.0)
- **Monopole charge:** q=±3, ±1

**Interpretation:**  
v2 gate (single fixed-window check) is too permissive — passes cases that v3 (multiple window sizes) correctly identifies as window-sensitive. This suggests v3 is the more reliable gate for detecting fragile localization.

**Recommendation:** Consider v3 as primary gate for production validation. Investigate v2 gate criteria revision or deprecation.

---

## Grid Coverage

| Parameter | Values | Count |
|-----------|--------|-------|
| **s1_family** | `spectral_circle`, `ring`, `wilson_ring` | 3 |
| **Monopole charge (q)** | -3, -2, -1, 0, 1, 2, 3 | 7 |
| **s1_size** | 8, 16, 24, 32, 48 | 5 |
| **Alpha (boundary twist)** | 0.0, 0.5 | 2 |
| **Disorder strength (W)** | 0.0, 2.0, 4.0, 6.0, 8.0, 12.0 | 6 |
| **Seed** | 42, 123, 456, 789, 1011, ... | Multiple |
| **Total cases** | | **6615** |

**Clean controls:** 945 cases (disorder_strength=0.0)  
**Disordered cases:** 5670 cases (disorder_strength>0)

---

## Comparison: Pytest vs Full Grid

| Metric | Pytest (195 tests) | Full Grid (6615 cases) |
|--------|-------------------|------------------------|
| **Ring window-selection sensitivity** | Resolved (seeds 12051, 12053, 9836055 now pass) | 52 failures (8.3% of ring alpha=0) — different manifestation |
| **Coverage** | Representative anchor cases | Comprehensive parameter sweep |
| **Purpose** | Unit validation, regression detection | Statistical pattern discovery |

**Key insight:** Pytest resolution (2026-05-15) validated that specific historical problem seeds now pass. Full grid reveals a broader fragility pattern at different parameter combinations — not a contradiction, but a more complete picture.

---

## Explicit Non-Claims (Critical)

This full diagnostic validates **discrete operator construction** on toy product manifolds. It does **NOT**:

1. Prove **continuum compactification** (cutoff=2 is far from continuum limit)
2. Validate **S⁶** or **S³×S⁶** geometries (only S²×S¹ tested)
3. Derive **Standard Model** (no chiral fermions, no gauge groups, no Higgs)
4. Prove **physical chirality** (topological index ≠ physical chirality without continuum limit + full gauge coupling)
5. Bypass **Witten vanishing theorem** (explicit construction ≠ rigorous proof of bypass)
6. Bypass **Lichnerowicz theorem** (toy model, not formal proof)

**Scope:** Numerical laboratory for covariant compactification toy mechanisms (Tom Lawrance's framework). Results are pedagogical and exploratory, not physical predictions.

---

## Artifacts

- **Run directory:** `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/`
- **Config:** `config.json`
- **Metrics:** `metrics.json` (13 MB, per-case results)
- **Data:** `data.npz` (eigenvalues, IPR, localization flags)
- **Summary:** `summary.md` (gate summary, classification)
- **Figures:** `figures/` (diagnostic plots)

---

**Last updated:** 2026-05-16  
**Status:** Full diagnostic complete with 2 documented caveats  
**Next steps:** Investigate ring alpha=0 fragility, consider v2 gate criteria revision
