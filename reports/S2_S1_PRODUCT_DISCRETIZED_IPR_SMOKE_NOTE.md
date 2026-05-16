# S2 x S1 Product-Discretized IPR Smoke Test — Note

**Date**: 2026-05-15  
**Run**: `reports/RUNS/ipr_smoke_improved/`  
**Status**: Completed  
**Verdict**: `ipr_smoke_weak_or_inconclusive`

---

## Purpose

Pre-full spatial-localization sanity check before 6615-case full run. Quick representative grid to validate that disorder increases IPR (Inverse Participation Ratio) as expected for Anderson-like localization diagnostic.

---

## Configuration

**Grid**: 144 cases (not full 324)

| Parameter | Values |
|-----------|--------|
| Families | spectral_circle, ring, wilson_ring (3) |
| q | 0, 1, -1 (3) |
| s1_sizes | 8, 16 (2, excluded 24) |
| alpha | 0.0, 0.5 (2) |
| disorder (W) | 0.0, 8.0 (2, excluded 4.0) |
| seeds | 123, 456 (2) |
| mode | gauge_phase (disorder-sensitive) |
| cutoff | 2 (toy resolution) |

**Rationale for reduction**: Focused on clean vs strong disorder (W=0.0 vs W=8.0) with both boundary twists and statistical replication (2 seeds), excluding intermediate disorder (W=4.0) and largest size (s1_size=24) to cap at ~150 cases for quick smoke test.

---

## Metrics

**IPR (Inverse Participation Ratio)**: `sum(|ψ_i|^4)` for eigenvectors  
- Localized state: IPR ≈ 1.0  
- Delocalized state: IPR ≈ 1/N  
- Expected: disorder → higher IPR (more localization)

**IPR ratio**: `mean_IPR / (1/N)` — scale-invariant measure  
**Contrast**: `disordered_mean_ratio / clean_mean_ratio`

**Verdict thresholds**:
- Pass: contrast > 2.0  
- Weak/inconclusive: 1.3 < contrast ≤ 2.0  
- Fail: contrast ≤ 1.3

---

## Results

### Aggregate

| Metric | Value |
|--------|-------|
| Total cases | 144 |
| Clean cases (W=0.0) | 72 |
| Disordered cases (W=8.0) | 72 |
| Non-q0 clean cases | 48 |
| Non-q0 disordered cases | 48 |
| Clean mean IPR ratio | 15.99 |
| Disordered mean IPR ratio | 22.41 |
| **Contrast** | **1.40x** |
| **Verdict** | **ipr_smoke_weak_or_inconclusive** |
| Elapsed | 5.1s |

### Interpretation

Disordered cases show **40% higher IPR** than clean cases (22.41 vs 15.99), confirming disorder increases spatial localization. However, contrast (1.40x) falls below the 2.0x threshold for clean pass, indicating:

1. **Signal exists but is weak**: IPR sensitivity to disorder is present but not strong at this toy resolution (cutoff=2, limited s1_sizes).
2. **Family/parameter dependence**: Averaged over all families, q-values, sizes, and twists, the localization signal is diluted.
3. **Requires full grid for robustness**: Mini-smoke with reduced parameters may underestimate contrast. Full 6615-case run with s1_size=24, intermediate disorder (W=4.0), and finer statistical sampling may show stronger signal.

---

## Comparison to Test Suite Mini Smoke

Test suite `test_ipr_smoke_run_mini` (pytest) showed **2.02x contrast** on a **single anchor case**:
- Config: q=1, s1_size=8, alpha=0.0, W=[0.0, 8.0], seed=123, family=spectral_circle
- Result: clean IPR ratio 17.0, disordered 34.4, contrast 2.02x → **pass**

This confirms that **specific cases can achieve strong contrast** (>2.0x), but **averaged across diverse parameter space**, contrast drops to 1.40x. This is expected: not all (q, family, size, twist) combinations show equally strong localization response.

---

## What This Does NOT Test

- **Full v3 gate**: This is IPR-only diagnostic, not the full v3 gate with window-selection robustness checks.
- **Window selection sensitivity**: All cases use the same low-energy window (5 lowest modes), no adaptive window selection.
- **Family-specific thresholds**: No per-family verdict breakdown (ring vs spectral_circle vs wilson_ring).
- **Physical localization**: IPR is a spatial-measure diagnostic, not a proof of Anderson localization physics or continuum compactification.
- **Chirality or index**: IPR measures spatial distribution, not chiral index or topological charge.

---

## Explicit Non-Claims

This IPR smoke test:
- **is NOT** a proof of Anderson localization in a physical system.
- **is NOT** validation of covariant compactification theory.
- **does NOT** claim S² × S¹ product operators represent continuum Dirac operators.
- **does NOT** validate Kaluza-Klein or Standard Model physics.
- **does NOT** claim physical chirality or gauge group derivation.
- **does NOT** bypass Witten or Lichnerowicz index theorems.
- **is NOT** a substitute for the full 6615-case discretized run or v3 gate validation.

**What it is**: A toy numerical diagnostic confirming that discretized S² × S¹ product operators with gauge_phase disorder mode show **weak but measurable IPR response** to disorder strength (1.40x contrast), consistent with spatial localization trend but below the 2.0x threshold for strong validation.

---

## Recommendation for Full Run

**Proceed with 6615-case full run**: Despite weak smoke result (1.40x), full grid with:
- s1_size=24 (larger lattice)
- W=[0.0, 2.0, 4.0, 6.0, 8.0] (finer disorder sweep)
- All 3 alpha values
- More seeds

...may show **stronger average contrast** and per-family breakdown. Weak smoke does NOT block full run; it sets realistic expectations that localization signal is **measurable but parameter-dependent**.

---

## Files Saved

```
reports/RUNS/ipr_smoke_improved/
├── config.json          # Full grid configuration
├── metrics.json         # Aggregate + per-case IPR data
├── summary.md           # Human-readable verdict
└── figures/
    └── ipr_smoke_scatter.png  # Clean vs disordered IPR scatter plot
```

---

## Baseline

Current baseline: `v0.1.14-mvp-s2-s1-discretization-v2-full` (unchanged)

This smoke test does NOT promote baseline. It is a pre-full diagnostic only.
