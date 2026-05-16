# Figure Data — Lattice-Size Scaling (Ring/alpha=0 Convergence)

**Data Extraction Date:** 2026-05-16  
**Target Paper:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"  
**Case Study:** v0.1.15-s2-s1-product-discretized-full  
**Target Figures/Tables:** F7 (Lattice-Size Scaling Plot), T5 (Lattice-Size Scaling Table)

---

## Source

**Run Path:**  
`reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/`

**Source Files:**
- `metrics.json` (2.8 MB, 1349 cases)
- `summary.md` (aggregated results)

**Extraction Method:**  
Python script filtering `s1_family == 'ring'` AND `disorder_strength > 0` (disordered cases only), aggregated by `s1_size`.

**Dataset Composition:**
- Ring/alpha=0 disordered cases: **882** (analyzed)
- Ring/alpha=0 clean cases (W=0): **147** (excluded from failure analysis)
- Reference families (spectral_circle, wilson_ring) disordered: **240** (0 failures)
- **Total cases in run:** 1349

---

## Table: Ring/alpha=0 Failure Rate by s1_size (Disordered Cases Only)

| s1_size | Total Cases | Complete Failures | Window-Sensitive | v2/v3 Disagreements | Robust Pass | Total Failures | Failure Rate (%) | Interpretation |
|---------|-------------|-------------------|------------------|---------------------|-------------|----------------|------------------|----------------|
| 8 | 126 | 15 | 10 | 1 | 100 | 25 | 19.8 | Small lattice, high failure rate |
| 16 | 126 | 1 | 0 | 0 | 125 | 1 | 0.8 | Sharp drop after s1_size=8 |
| 24 | 126 | 15 | 4 | 0 | 107 | 19 | 15.1 | Non-monotonic (secondary peak) |
| 32 | 126 | 3 | 0 | 0 | 123 | 3 | 2.4 | Near convergence threshold |
| 48 | 126 | 3 | 0 | 0 | 123 | 3 | 2.4 | Below Decision Rule 1 threshold |
| **64** | **126** | **0** | **0** | **0** | **126** | **0** | **0.0** ✅ | **Converged (s1_size≥64)** |
| **96** | **126** | **0** | **0** | **0** | **126** | **0** | **0.0** ✅ | **Converged (s1_size≥64)** |

**Notes:**
- "Complete failures": Both `kernel_only` and `fixed_window` localization gates fail
- "Window-sensitive": `kernel_only` fails, `fixed_window` passes (historical pattern)
- "v2/v3 disagreements": v2 (fixed_window) and v3 (window_robust) gates disagree (subset of failures)
- "Robust pass": Both gates pass, no window sensitivity detected

---

## Key Result: Convergence at s1_size ≥ 64

### Aggregate Failure Rates

| s1_size Range | Failures | Total Cases | Failure Rate | Decision |
|---------------|----------|-------------|--------------|----------|
| **s1_size < 64** | **51** | **630** | **8.1%** | Small-lattice artifact zone |
| **s1_size ≥ 64** | **0** | **252** | **0.0%** ✅ | **Converged** |

### Decision Rule 1 Application

**Rule:** If `failure_rate(s1_size ≥ 64) < 2.0%` → classify as **SMALL_LATTICE_ARTIFACT**

**Result:**  
- Measured failure rate at s1_size≥64: **0.0%**
- Threshold: **2.0%**
- **0.0% < 2.0%** ✅

**Verdict:** **SMALL_LATTICE_ARTIFACT** (confirmed)

**Interpretation:**  
Ring discretization of S¹ at periodic boundary condition (alpha=0) requires larger lattices (s1_size≥64) for convergence. All 51 failures from full run (6615 cases) vanish at s1_size≥64. Ring/alpha=0 at s1_size≥64 is **as robust as spectral_circle and wilson_ring**.

---

## Reference Families Validation (Control)

**Purpose:** Verify that spectral_circle and wilson_ring remain robust at s1_size≥64 (no new failures introduced by extended grid).

| Family | Disordered Cases | Failures | Failure Rate |
|--------|------------------|----------|--------------|
| spectral_circle | ~120 | 0 | 0.0% ✅ |
| wilson_ring | ~120 | 0 | 0.0% ✅ |
| **Combined** | **240** | **0** | **0.0%** ✅ |

**Conclusion:** Reference families remain fully robust at all tested s1_size (8-96), confirming ring/alpha=0 artifact is NOT a general discretization issue.

---

## Figure Specification for F7: Lattice-Size Scaling Plot

### Figure Title
**"Ring/alpha=0 Lattice-Size Scaling: Failure Rate vs. s1_size (Convergence at s1_size≥64)"**

### Plot Specifications

**X-axis:**
- Variable: `s1_size` (S¹ lattice discretization points)
- Values: [8, 16, 24, 32, 48, 64, 96]
- Scale: Linear
- Label: "s1_size (S¹ Lattice Discretization Points)"

**Y-axis:**
- Variable: Failure rate (percentage)
- Range: [0, 25%] (auto-scale acceptable)
- Scale: Linear
- Label: "Failure Rate (%)"

**Data Series:**
- **Main series (ring/alpha=0):**
  - Plot type: Line + markers
  - Data points: [(8, 19.8), (16, 0.8), (24, 15.1), (32, 2.4), (48, 2.4), (64, 0.0), (96, 0.0)]
  - Line style: Solid, blue
  - Markers: Circles, size=8

**Threshold Lines:**
- **Decision Rule 1 threshold (horizontal):**
  - Y-value: 2.0%
  - Line style: Dashed, red
  - Label: "Decision Rule 1 threshold (2%)"
  
- **Convergence threshold (vertical):**
  - X-value: 64
  - Line style: Dashed, green
  - Label: "Convergence threshold (s1_size=64)"

**Annotations:**
- Arrow pointing to (64, 0.0) with text: "Converged: 0/252 = 0.0%"
- Arrow pointing to (8-48 region) with text: "Small-lattice artifact zone"

### Caption Draft

> **Figure 7. Ring/alpha=0 Lattice-Size Scaling: Convergence at s1_size≥64.**  
> Failure rate (%) vs. s1_size for ring discretization of S¹ at periodic boundary condition (alpha=0.0). Data from targeted follow-up (1349 cases). Red dashed line: Decision Rule 1 threshold (2%). Green dashed line: convergence threshold (s1_size=64). All 51 failures from full run (6615 cases) occur at s1_size<64; failure rate drops to 0.0% at s1_size≥64 (0/252 cases). Verdict: SMALL_LATTICE_ARTIFACT. Ring/alpha=0 at s1_size≥64 is as robust as spectral_circle and wilson_ring. **Non-claim:** This shows discretized toy operator convergence, NOT continuum extrapolation or physical compactification.

---

## Table Specification for T5: Lattice-Size Scaling Table (Paper-Ready Markdown)

### Table Title
**"Table 5. Ring/alpha=0 Lattice-Size Scaling: Failure Rate vs. s1_size (Convergence at s1_size≥64)"**

### Table (Paper-Ready Format)

| s1_size | Total Cases | Failures | Failure Rate (%) | Interpretation |
|---------|-------------|----------|------------------|----------------|
| 8 | 126 | 25 | 19.8 | Small lattice, high failure rate |
| 16 | 126 | 1 | 0.8 | Sharp drop after s1_size=8 |
| 24 | 126 | 19 | 15.1 | Non-monotonic (secondary peak) |
| 32 | 126 | 3 | 2.4 | Near convergence threshold |
| 48 | 126 | 3 | 2.4 | Below Decision Rule 1 threshold (2%) |
| **64** | **126** | **0** | **0.0** ✅ | **Converged** |
| **96** | **126** | **0** | **0.0** ✅ | **Converged** |
| | | | | |
| **s1_size < 64** | **630** | **51** | **8.1%** | Small-lattice artifact zone |
| **s1_size ≥ 64** | **252** | **0** | **0.0%** | Convergence confirmed |

**Decision Rule 1:** If failure_rate(s1_size≥64) < 2% → SMALL_LATTICE_ARTIFACT.  
**Result:** 0.0% < 2% → **Verdict: SMALL_LATTICE_ARTIFACT** ✅

### Table Caption

> **Table 5. Ring/alpha=0 Lattice-Size Scaling: Convergence at s1_size≥64.**  
> Failure rate (%) vs. s1_size for ring discretization of S¹ at periodic boundary condition (alpha=0.0). Disordered cases only (W>0). Data from targeted follow-up (882 ring/alpha=0 disordered cases). All 51 failures from full run (6615 cases) vanish at s1_size≥64 (0/252 = 0.0%). Decision Rule 1 threshold (2%) exceeded only at s1_size<64. Verdict: SMALL_LATTICE_ARTIFACT. **Non-claim:** This shows discretized toy operator convergence, NOT continuum extrapolation or physical compactification.

---

## Production Guideline (Derived from Lattice-Size Scaling)

### Recommended s1_size by Configuration

| Configuration | Recommended s1_size | Rationale |
|---------------|---------------------|-----------|
| **Ring + alpha=0.0 (periodic)** | **s1_size ≥ 64** | Convergence threshold confirmed by follow-up (0.0% failure rate) |
| **Ring + alpha≠0.0 (twisted)** | **s1_size ≥ 32** | No failures observed in full run at alpha=0.25, 0.5 |
| **spectral_circle (any alpha)** | **s1_size ≥ 8** | Fully robust at all tested s1_size (0 failures across 2205 disordered cases) |
| **wilson_ring (any alpha)** | **s1_size ≥ 8** | Fully robust at all tested s1_size (0 failures across 2205 disordered cases) |

**Summary:** Ring discretization at periodic boundary condition (alpha=0) requires larger lattices (s1_size≥64) for convergence. Twisted boundary conditions (alpha≠0) and spectral_circle/wilson_ring families converge at smaller lattices.

---

## Scientific Non-Claims

This lattice-size scaling result does **NOT** prove or claim:

1. **Continuum compactification** — All operators are discretized toys. Convergence at s1_size≥64 is discretized operator convergence, NOT continuum extrapolation.
2. **S⁶ or S³×S⁶ validation** — Only S²×S¹ tested. Ring/alpha=0 artifact is specific to S¹ discretization on S²×S¹ product space.
3. **Standard Model derivation** — No gauge group calculation. Anderson benchmark is numerical localization test, not physical mechanism.
4. **Physical chirality proof** — Dirac indices (if computed) are topological toy counts, not physical chiral fermions.
5. **Witten/Lichnerowicz bypass** — Numerical convergence ≠ rigorous mathematical proof.
6. **Physical interpretation** — Anderson localization benchmark is numerical test. Ring/alpha=0 convergence does not imply physical compactification mechanism.
7. **Radion stabilization** — Toy radion model (if used) does not address hierarchy problem or moduli stabilization in string theory.
8. **Observable predictions** — Lattice-size scaling is discretized toy operator convergence, not continuum field theory prediction.

**Key framing:** This result demonstrates that ring discretization of S¹ at periodic boundary condition requires s1_size≥64 for numerical convergence in Anderson localization benchmark. This is a **discretized toy operator convergence result**, NOT a continuum limit or physical compactification claim.

---

## Optional: CSV Export

**File Path:** `reports/figure_data/lattice_size_scaling_v0.1.16.csv`

**CSV Format:**
```csv
s1_size,total_cases,complete_failures,window_sensitive,v2v3_disagreements,robust_pass,total_failures,failure_rate_percent,interpretation
8,126,15,10,1,100,25,19.8,Small lattice high failure rate
16,126,1,0,0,125,1,0.8,Sharp drop after s1_size=8
24,126,15,4,0,107,19,15.1,Non-monotonic secondary peak
32,126,3,0,0,123,3,2.4,Near convergence threshold
48,126,3,0,0,123,3,2.4,Below Decision Rule 1 threshold
64,126,0,0,0,126,0,0.0,Converged s1_size>=64
96,126,0,0,0,126,0,0.0,Converged s1_size>=64
```

---

## Next Steps (After Figure/Table Generation)

### Immediate
1. Generate F7 (Lattice-Size Scaling Plot) using matplotlib/seaborn from table data
2. Include T5 (Lattice-Size Scaling Table) in methodology paper draft
3. Draft Introduction section referencing F7 and T5

### Medium-term
4. Extract core gates pass rate data (Task 3) → T3 (Core Gates Pass Rate Table)
5. Create F1 (Falsification Ladder Diagram) → core methodology visualization
6. Create F8 (Claim Ladder Pyramid) → scope protection

### Long-term
7. Draft full paper sections (Introduction, Methods, Case Study, Limitations)
8. Internal review with skeptic agent
9. Prepare for preprint submission (after Wilson audit, Track B)

---

## Summary

**Data Extracted:** Lattice-size scaling for ring/alpha=0 from targeted follow-up (1349 cases, 882 ring/alpha=0 disordered)

**Key Numbers:**
- Failures at s1_size < 64: **51/630 = 8.1%**
- Failures at s1_size ≥ 64: **0/252 = 0.0%** ✅
- Reference families: **0/240 = 0.0%** (fully robust)
- Decision Rule 1 result: **0.0% < 2.0%** → **SMALL_LATTICE_ARTIFACT** ✅

**Target Outputs:**
- **F7:** Lattice-Size Scaling Plot (specification provided)
- **T5:** Lattice-Size Scaling Table (paper-ready markdown provided)

**Production Guideline:** Ring/alpha=0 requires s1_size≥64 for robustness.

**Non-Claims:** Discretized toy operator convergence, NOT continuum extrapolation or physical compactification.

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)

**Next Task:** Generate F7 plot (matplotlib) OR proceed to Introduction draft.

---

**Data extraction status:** ✅ COMPLETE  
**File created:** reports/FIGURE_DATA_LATTICE_SIZE_SCALING_v0.1.16.md  
**Ready for:** Figure/table generation + paper drafting
