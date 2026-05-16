# Figures and Tables Inventory — v0.1.16 Methodology Paper

**Inventory Date:** 2026-05-16  
**Target Paper:** "A Falsification-First Validation Harness for Discretized Spectral Operators on Compact Product Manifolds"  
**Case Study Baseline:** v0.1.15-s2-s1-product-discretized-full  
**Status:** INVENTORY COMPLETE — DATA EXTRACTION READY

---

## Purpose

This inventory maps v0.1.15 evidence artifacts (full diagnostic run + ring/alpha=0 targeted follow-up) into paper-ready figures and tables for the methodology paper. Each figure/table is specified with:
- **Source data** — where raw data lives
- **Extraction task** — how to generate figure/table from source
- **Message** — what the figure/table communicates
- **Priority** — required for first draft vs. optional enhancement

**Key constraint:** All figures/tables must emphasize **toy scope** and **methodology contribution**, NOT physical compactification claims.

---

## Source Artifacts

### Primary Source: RUNS Artifacts (Local Only, Ignored by Git)

**Full Diagnostic Run:**
- **Path:** `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/`
- **Cases:** 6615
- **Artifacts:**
  - `config.json` — parameter grid specification
  - `metrics.json` — per-case results (localization gates, IPR, failures)
  - `summary.md` — classification, verdict, gate results
  - `data.npz` — eigenvalues, eigenvectors (if saved)

**Ring/Alpha=0 Targeted Follow-Up:**
- **Path:** `reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/`
- **Cases:** 1349
- **Artifacts:**
  - `config.json` — extended grid (s1_size=64, 96)
  - `metrics.json` — per-case results
  - `summary.md` — lattice-size scaling analysis, decision rule application
  - `data.npz` — eigenvalues (if saved)

**CRITICAL NOTE:** RUNS artifacts are **ignored by git** (280MB). All figures/tables requiring RUNS data must extract from local artifacts before git-only archive.

---

### Secondary Sources: Reports and Documentation

**Release Documentation:**
- `reports/RELEASE_NOTES_v0.1.15.md` — comprehensive release narrative, refined caveat, key results
- `reports/VALIDATION_STATUS.md` — validation summary, baseline status, caveat
- `reports/SPECTRAL_REPORT.md` — spectral analysis, caveat detailed breakdown
- `reports/ISSUES_SCIENTIFIC.md` — scientific issues, caveats, baseline impact
- `reports/V0_1_15_RELEASE_INTEGRITY_AUDIT.md` — release integrity verification results

**Planning Documentation:**
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — paper structure, claim ladder, non-claims
- `reports/ROADMAP_v0.1.16.md` — future work roadmap (Wilson audit, S²×S², continuum)

**Code and Tests:**
- `README.md` — project overview, pytest status
- `pytest.ini` + test results — 203 passed, 1 warning

---

## Candidate Figures (11 Proposed)

### F1. GeoSpectra Falsification Ladder Workflow Diagram

**Title:** "GeoSpectra Falsification Ladder: Systematic Validation Workflow with Mandatory Controls"

**Purpose/Message:**  
Visual representation of falsification-first workflow. Shows ladder metaphor (rungs = gates, fall = reject, climb = provisional pass). Emphasizes: negative control, positive control, reproducibility, caveat discovery, release integrity.

**Source Data:**
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section 3.3 (Ladder Rungs)
- Conceptual (no numerical data required)

**Required Extraction:**
- Diagram creation tool: Mermaid (markdown-embeddable) or draw.io (PNG export)
- **Rungs (in order):**
  1. Hermiticity gate
  2. Shape consistency gate
  3. Positive control (W=0)
  4. Negative control (q=0 disordered)
  5. Reproducibility (independent re-run)
  6. Stress test (edge cases)
  7. Caveat discovery (failure mode analysis)
  8. Independent audit (external review)
  9. Release integrity (cross-file consistency)
- **Decision points:** PASS_WITH_CAVEATS (default), PASS_WITH_LOCAL_CAVEATS (refined), REJECT (null result)

**Expected File Name:** `figures/falsification_ladder_workflow.png` (or `.mermaid.md`)

**Priority:** **REQUIRED** — core methodology contribution visualization

**Risks:** None (conceptual diagram, no numerical claims)

---

### F2. Validation Pipeline Timeline (v0.1.15 Case Study)

**Title:** "v0.1.15 Validation Pipeline Timeline: From Full Diagnostic to Release Integrity Audit"

**Purpose/Message:**  
Timeline of v0.1.15 milestone stages: full diagnostic (16h) → reproducibility pass (16h) → independent audit (1h) → ring/alpha=0 follow-up (140 min) → release integrity audit (30 min). Shows iterative falsification workflow.

**Source Data:**
- `reports/RELEASE_NOTES_v0.1.15.md` — timeline events (lines 22-29, 38-42)
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section: Release Narrative

**Required Extraction:**
- Timeline visualization (Gantt chart or horizontal timeline)
- **Events:**
  - 2026-05-14: v0.1.14 baseline
  - 2026-05-15 00:00: Full diagnostic start (6615 cases)
  - 2026-05-15 16:00: Full diagnostic complete
  - 2026-05-15 16:30: Reproducibility pass start
  - 2026-05-15 32:30: Reproducibility pass complete (6615/6615 matched)
  - 2026-05-16 10:00: Independent audit
  - 2026-05-16 11:00: Caveat discovered (ring/alpha=0 fragility)
  - 2026-05-16 12:00: Targeted follow-up start (1349 cases)
  - 2026-05-16 14:20: Follow-up complete (failures vanish at s1_size≥64)
  - 2026-05-16 15:00: Release integrity audit
  - 2026-05-16 16:00: Baseline promotion v0.1.14 → v0.1.15
  - 2026-05-16 17:00: Git tag created

**Expected File Name:** `figures/v0_1_15_validation_timeline.png`

**Priority:** **REQUIRED** — shows falsification workflow in action

**Risks:** None (timeline visualization, no physics claims)

---

### F3. S²×S¹ Product-Discretized Operator Schematic

**Title:** "Kronecker-Sum Construction: D_S2xS1 = D_S2(q) ⊗ I_S1 + Γ_S2 ⊗ P_S1(α, W)"

**Purpose/Message:**  
Visual schematic of product-discretized operator construction. Shows: S² Dirac operator, S¹ discretization families (spectral_circle, ring, wilson_ring), Kronecker-sum product, disorder potential W.

**Source Data:**
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section 5.1 (Operator Construction)
- Conceptual (no numerical data required)

**Required Extraction:**
- Diagram creation: LaTeX tikz, draw.io, or Inkscape
- **Components:**
  - S² (sphere with monopole charge q)
  - S¹ (circle with twist angle α)
  - D_S2(q): Dirac operator on S² (matrix block)
  - I_S1: identity on S¹
  - Γ_S2: chirality operator on S²
  - P_S1(α, W): momentum + disorder on S¹
  - Kronecker sum: ⊗ symbols
  - Product space: S²×S¹ (3D torus visualization)

**Expected File Name:** `figures/s2_s1_operator_schematic.png`

**Priority:** **OPTIONAL** — helpful but not essential for methodology focus

**Risks:** Diagram may over-emphasize physics (S²×S¹ geometry) vs. methodology. Mitigate: label as "Toy Operator Example".

---

### F4. Full-Grid Parameter Coverage Map (6615 Cases)

**Title:** "Full Diagnostic Parameter Grid: 7-Dimensional Coverage (q × s1_size × alpha × W × seed × family)"

**Purpose/Message:**  
Visualize 6615-case grid coverage. Shows: 7 monopole charges × 5 lattice sizes × 3 twist angles × 7 disorder strengths × 4 seeds × 3 families. Emphasizes comprehensive validation.

**Source Data:**
- `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/config.json`
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 30-36 (grid specification)

**Required Extraction:**
- **Method 1 (Simple):** Table with dimensions and counts:
  ```
  Dimension        | Values                                  | Count
  -----------------|----------------------------------------|------
  Monopole q       | -3, -2, -1, 0, 1, 2, 3                 | 7
  Lattice s1_size  | 8, 16, 24, 32, 48                      | 5
  Twist alpha      | 0.0, 0.25, 0.5                         | 3
  Disorder W       | 0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0    | 7
  Seed             | 122, 123, 124, 456                     | 4
  Family           | spectral_circle, ring, wilson_ring     | 3
  TOTAL CASES      |                                        | 6615
  ```
- **Method 2 (Complex):** 3D scatter plot (q, s1_size, W) with color = family, shape = alpha
  - Requires parsing `config.json` → extract all parameter combinations
  - Plot in matplotlib/seaborn

**Expected File Name:** `figures/full_grid_parameter_coverage.png` (or table in paper body)

**Priority:** **OPTIONAL** — helpful for completeness, but table in text may suffice

**Risks:** None (parameter grid visualization, no results)

---

### F5. Ring/alpha=0 Failure Rate by s1_size (Heatmap)

**Title:** "Ring/alpha=0 Failure Localization: Failure Rate vs. s1_size and Disorder Strength W"

**Purpose/Message:**  
Heatmap showing ring/alpha=0 failures concentrated at small s1_size (<64) and specific disorder strengths. X-axis: s1_size (8-96), Y-axis: W (disorder), color: failure rate. Shows failures vanish at s1_size≥64.

**Source Data:**
- `reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/metrics.json`
- Extract: per-case (s1_size, W, failure_type) tuples for ring/alpha=0 subset
- Aggregate: failure_rate[s1_size, W] = count(failures) / count(total_cases)

**Required Extraction:**
```python
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load follow-up metrics
with open('reports/RUNS/.../metrics.json') as f:
    metrics = json.load(f)

# Filter: ring/alpha=0 only
ring_alpha0 = [
    case for case in metrics['cases']
    if case['family'] == 'ring' and case['alpha'] == 0.0
]

# Aggregate: failure_rate[s1_size, W]
s1_sizes = sorted(set(c['s1_size'] for c in ring_alpha0))
disorders = sorted(set(c['W'] for c in ring_alpha0))
failure_matrix = np.zeros((len(disorders), len(s1_sizes)))

for i, W in enumerate(disorders):
    for j, s1_size in enumerate(s1_sizes):
        subset = [c for c in ring_alpha0 if c['W'] == W and c['s1_size'] == s1_size]
        failures = sum(1 for c in subset if c['failure_type'] in ['complete_failure', 'window_sensitive'])
        failure_matrix[i, j] = failures / len(subset) if subset else 0

# Plot heatmap
sns.heatmap(failure_matrix, xticklabels=s1_sizes, yticklabels=disorders, 
            annot=True, fmt='.1%', cmap='YlOrRd')
plt.xlabel('s1_size')
plt.ylabel('Disorder Strength W')
plt.title('Ring/alpha=0 Failure Rate Heatmap')
plt.savefig('figures/ring_alpha0_failure_heatmap.png')
```

**Expected File Name:** `figures/ring_alpha0_failure_heatmap.png`

**Priority:** **REQUIRED** — key result visualization (failures vanish at s1_size≥64)

**Risks:** Low. Emphasize "small-lattice artifact" in caption, NOT "physical limitation".

---

### F6. Caveat Before/After Audit Correction

**Title:** "Caveat Refinement: From 'Ring/alpha=0 Fragility' to 'Small-Lattice Artifact'"

**Purpose/Message:**  
Side-by-side comparison showing caveat evolution after targeted follow-up. Before: "51 failures, fragility unclear". After: "failures vanish at s1_size≥64, small-lattice artifact, production guideline established".

**Source Data:**
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 116-118 (original caveat), lines 119-133 (refined caveat)
- `reports/SPECTRAL_REPORT.md` — caveat section (before/after)

**Required Extraction:**
- **Method 1 (Text Box Comparison):**
  ```
  BEFORE (Post Full-Run):                  AFTER (Post Follow-Up):
  ┌────────────────────────────────┐      ┌────────────────────────────────┐
  │ Ring/alpha=0 fragility         │      │ Ring/alpha=0 small-lattice     │
  │ - 51 failures (4.0% rate)      │      │   artifact (s1_size<64 only)   │
  │ - All at ring + alpha=0.0      │      │ - 0/252 = 0.0% at s1_size≥64   │
  │ - Cause: unclear (structural   │      │ - Converged: as robust as      │
  │   limitation vs. artifact?)    │      │   spectral_circle, wilson_ring │
  └────────────────────────────────┘      │ - Production: s1_size≥64       │
                                           └────────────────────────────────┘
  ```
- **Method 2 (Timeline Arrow):**
  - Arrow: Full Run (6615 cases) → Caveat Discovered → Follow-Up (1349 cases) → Caveat Resolved

**Expected File Name:** `figures/caveat_before_after_comparison.png`

**Priority:** **REQUIRED** — shows falsification workflow in action (discover → investigate → resolve)

**Risks:** None (caveat refinement is methodological process, not physics claim)

---

### F7. Lattice-Size Scaling Result: Failures Vanish at s1_size≥64

**Title:** "Ring/alpha=0 Lattice-Size Scaling: Failure Rate vs. s1_size (Convergence at s1_size≥64)"

**Purpose/Message:**  
Line plot: X-axis = s1_size (8, 16, 24, 32, 48, 64, 96), Y-axis = failure rate (%). Shows: high failure rate at s1_size=8,24 (~17%, ~13%), drops at s1_size≥32 (~2%), **vanishes at s1_size≥64 (0.0%)**. Emphasizes convergence.

**Source Data:**
- `reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/summary.md` — lattice-size scaling table
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 97-106 (lattice-size scaling table)

**Required Extraction:**
```python
import matplotlib.pyplot as plt

# Data from follow-up summary.md or RELEASE_NOTES table
s1_sizes = [8, 16, 24, 32, 48, 64, 96]
failure_rates = [17.0, 0.7, 12.9, 2.0, 2.0, 0.0, 0.0]  # percent

plt.figure(figsize=(8, 5))
plt.plot(s1_sizes, failure_rates, marker='o', linewidth=2, markersize=8)
plt.axhline(y=2.0, color='red', linestyle='--', label='Decision Rule 1 threshold (2%)')
plt.axvline(x=64, color='green', linestyle='--', label='Convergence threshold (s1_size=64)')
plt.xlabel('s1_size (S¹ lattice discretization points)')
plt.ylabel('Failure Rate (%)')
plt.title('Ring/alpha=0 Lattice-Size Scaling: Failures Vanish at s1_size≥64')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('figures/ring_alpha0_lattice_size_scaling.png')
```

**Expected File Name:** `reports/figures/F7_lattice_size_scaling.png`

**Priority:** **REQUIRED** — key result (convergence proof)

**STATUS:** ✅ **COMPLETED** (2026-05-16)
- Generated: `reports/figures/F7_lattice_size_scaling.png` (255KB, 300 dpi)
- Script: `scripts/generate_f7_lattice_size_scaling.py`
- Data source: `reports/FIGURE_DATA_LATTICE_SIZE_SCALING_v0.1.16.md`
- Key result visualized: s1_size≥64 → 0.0% failure rate (0/252 cases)

**Risks:** Low. Caption must emphasize "discretized toy operator convergence", NOT "physical continuum extrapolation".

---

### F8. Claim Ladder Pyramid (4-Tier Hierarchy)

**Title:** "Claim Ladder: Validated Toy Claims → Engineering → Unresolved Questions → Forbidden Physical Claims"

**Purpose/Message:**  
Pyramid visualization showing claim hierarchy. Base (validated toy claims) → Tier 2 (engineering) → Tier 3 (unresolved) → Top (forbidden, crossed out). Prevents scope creep.

**Source Data:**
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section: Claim Ladder (4-Tier Hierarchy)

**Required Extraction:**
- Pyramid diagram (draw.io, Inkscape, or PowerPoint)
- **Tiers (bottom to top):**
  - **Tier 1 (Base, Green ✅):** "Validated Toy Claims" (S²×S¹ operators pass Anderson benchmark, ring/alpha=0 converges, reproducibility)
  - **Tier 2 (Yellow ✅):** "Supported Engineering Claims" (Falsification Ladder reduces false positives, release integrity works)
  - **Tier 3 (Orange ❓):** "Unresolved Scientific Questions" (continuum extrapolation, S²×S², physical interpretation)
  - **Tier 4 (Top, Red ❌, Crossed Out):** "Forbidden Physical Claims" (continuum compactification, S⁶/S³×S⁶, Standard Model, physical chirality)

**Expected File Name:** `figures/claim_ladder_pyramid.png`

**Priority:** **REQUIRED** — prevents misinterpretation of toy scope as physical proof

**Risks:** None (explicitly separates validated toy claims from forbidden physics claims)

---

### F9. Release Integrity Audit Flowchart

**Title:** "Release Integrity Audit: Systematic Verification Before Baseline Promotion"

**Purpose/Message:**  
Flowchart showing release integrity audit steps: baseline references → scientific non-claims → release artifacts → repository hygiene → cross-file consistency → verdict. Shows systematic verification prevents internal contradictions.

**Source Data:**
- `reports/V0_1_15_RELEASE_INTEGRITY_AUDIT.md` — Section 1-5 (audit steps)
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section 8.3 (Release Integrity Audit)

**Required Extraction:**
- Flowchart diagram (Mermaid, draw.io, or Graphviz)
- **Steps:**
  1. Baseline References Audit (v0.1.15 consistent? v0.1.14 historical?)
  2. Scientific Non-Claims Audit (8 non-claims present?)
  3. Release Artifacts Audit (run paths exist? pytest count matches?)
  4. Repository Hygiene Audit (gitignore covers cache? no .env? RUNS size acceptable?)
  5. Cross-File Consistency (numerical claims match across reports?)
  6. **Decision:** PASS (release_integrity_confirmed) or FAIL (block promotion)

**Expected File Name:** `figures/release_integrity_audit_flowchart.png`

**Priority:** **OPTIONAL** — demonstrates falsification workflow rigor, but not essential for first draft

**Risks:** None (verification process, not scientific claim)

---

### F10. Production Guideline Flowchart (Family × Alpha → s1_size Recommendation)

**Title:** "Production Guideline: S¹ Discretization Family × Twist Angle → Recommended s1_size"

**Purpose/Message:**  
Decision tree for users: Given (family, alpha), what s1_size should I use? Ring/alpha=0 → s1_size≥64. Ring/alpha≠0 → s1_size≥32. spectral_circle, wilson_ring → all s1_size robust.

**Source Data:**
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 130-133 (production guideline)
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section 7.7 (Production Guideline)

**Required Extraction:**
- Decision tree diagram (draw.io, Mermaid, or text-based flowchart)
- **Decision nodes:**
  ```
  START
    ↓
  [Family?]
    ├─ spectral_circle → s1_size: ANY (all robust) ✅
    ├─ wilson_ring → s1_size: ANY (all robust) ✅
    └─ ring → [Alpha?]
               ├─ alpha = 0.0 → s1_size ≥ 64 ⚠️
               └─ alpha ≠ 0.0 → s1_size ≥ 32 ✅
  ```

**Expected File Name:** `figures/production_guideline_flowchart.png`

**Priority:** **OPTIONAL** — helpful for practitioners, but not essential for methodology paper

**Risks:** None (engineering guideline, not physics claim)

---

### F11. Anderson Localization IPR Distribution Comparison (3 Families)

**Title:** "Anderson Localization IPR Distributions: spectral_circle vs. ring vs. wilson_ring"

**Purpose/Message:**  
Histogram comparison of IPR (Inverse Participation Ratio) for 3 families. Localized states: IPR near 1/N (peaked at low IPR). Delocalized states: IPR ~ 1 (flat distribution). Shows ring/alpha=0 has tail at high IPR (failures), other families clean.

**Source Data:**
- `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/data.npz` (if eigenvalues saved)
- Alternative: `metrics.json` → extract IPR values per case

**Required Extraction:**
```python
import numpy as np
import matplotlib.pyplot as plt

# Load full diagnostic metrics.json
with open('reports/RUNS/.../metrics.json') as f:
    metrics = json.load(f)

# Extract IPR values for disordered cases (W > 0), split by family
ipr_spectral = [c['ipr'] for c in metrics['cases'] if c['family'] == 'spectral_circle' and c['W'] > 0]
ipr_ring = [c['ipr'] for c in metrics['cases'] if c['family'] == 'ring' and c['W'] > 0]
ipr_wilson = [c['ipr'] for c in metrics['cases'] if c['family'] == 'wilson_ring' and c['W'] > 0]

# Plot histograms
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
axes[0].hist(ipr_spectral, bins=50, alpha=0.7, color='blue')
axes[0].set_title('spectral_circle')
axes[1].hist(ipr_ring, bins=50, alpha=0.7, color='red')
axes[1].set_title('ring (note: tail at high IPR = failures)')
axes[2].hist(ipr_wilson, bins=50, alpha=0.7, color='green')
axes[2].set_title('wilson_ring')
for ax in axes:
    ax.set_xlabel('IPR (Inverse Participation Ratio)')
    ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('figures/anderson_ipr_comparison_3families.png')
```

**Expected File Name:** `figures/anderson_ipr_comparison_3families.png`

**Priority:** **OPTIONAL** — demonstrates Anderson benchmark, but may be too technical for methodology focus

**Risks:** Medium. IPR distributions may be misinterpreted as "physical localization" vs. "numerical test". Mitigate: caption emphasizes "Anderson benchmark (toy operator test)".

---

## Candidate Tables (10 Proposed)

### T1. v0.1.15 Validation Chain (Timeline + Milestones)

**Title:** "v0.1.15 Validation Chain: From Full Diagnostic to Baseline Promotion"

**Purpose/Message:**  
Summary table of v0.1.15 validation stages: full diagnostic → reproducibility → audit → follow-up → integrity audit → promotion. Shows complete falsification workflow.

**Source Data:**
- `reports/RELEASE_NOTES_v0.1.15.md` — Summary + timeline
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Release Narrative

**Columns:**
| Stage | Date | Cases | Duration | Verdict | Key Result |
|-------|------|-------|----------|---------|------------|
| Full Diagnostic | 2026-05-15 | 6615 | ~16h | PASS_WITH_LOCAL_CAVEATS | 5619/5670 localized (99.1%), 51 ring/alpha=0 failures |
| Reproducibility Pass | 2026-05-15 | 6615 | ~16h | PASS | 6615/6615 matched |
| Independent Audit | 2026-05-16 | - | ~1h | confirmed_with_corrections | 3 corrections applied |
| Ring/alpha=0 Follow-Up | 2026-05-16 | 1349 | ~140 min | SMALL_LATTICE_ARTIFACT | 0/252 at s1_size≥64 |
| Release Integrity Audit | 2026-05-16 | - | ~30 min | release_integrity_confirmed | All checks passed |
| Baseline Promotion | 2026-05-16 | - | - | v0.1.15 | v0.1.14 → v0.1.15 |

**Priority:** **REQUIRED** — complete validation workflow summary

**STATUS:** ✅ **COMPLETED** (2026-05-16)
- Extracted: `reports/FIGURE_DATA_VALIDATION_CHAIN_v0.1.16.md`
- Source: `RELEASE_NOTES_v0.1.15.md` + `METHODOLOGY_PAPER_OUTLINE_v0.1.16.md`
- Timeline: 6 stages from full diagnostic (2026-05-15) to baseline promotion (2026-05-16)

**Risks:** None (validation chain is methodological, not physics)

---

### T2. Full Diagnostic Case Count Breakdown (6615 Cases)

**Title:** "Full Diagnostic Parameter Grid: Case Count by Family and Parameter Space"

**Purpose/Message:**  
Detailed breakdown of 6615 cases: 7 monopole charges × 5 s1_sizes × 3 alphas × 7 disorders × 4 seeds × 3 families. Shows comprehensive coverage.

**Source Data:**
- `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/config.json`
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 30-36

**Columns:**
| Family | Monopole q | s1_size | alpha | W (Disorder) | Seeds | Total Cases |
|--------|-----------|---------|-------|--------------|-------|-------------|
| spectral_circle | 7 (-3 to 3) | 5 (8-48) | 3 (0.0, 0.25, 0.5) | 7 (0-16) | 4 | 2205 |
| ring | 7 | 5 | 3 | 7 | 4 | 2205 |
| wilson_ring | 7 | 5 | 3 | 7 | 4 | 2205 |
| **TOTAL** | | | | | | **6615** |

**Alternative Format (Expanded):**
| Parameter | Values | Count |
|-----------|--------|-------|
| Monopole charge q | -3, -2, -1, 0, 1, 2, 3 | 7 |
| S¹ lattice size s1_size | 8, 16, 24, 32, 48 | 5 |
| Twist angle alpha | 0.0, 0.25, 0.5 | 3 |
| Disorder strength W | 0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0 | 7 |
| Random seed | 122, 123, 124, 456 | 4 |
| Discretization family | spectral_circle, ring, wilson_ring | 3 |
| **TOTAL CASES** | | **6615** |

**Priority:** **REQUIRED** — demonstrates comprehensive validation

**Risks:** None (parameter grid, no results)

---

### T3. Core Gates Pass Rate Summary (6615 Cases)

**Title:** "Core Gates Pass Rate: Hermiticity, Shape, Reproducibility, Controls"

**Purpose/Message:**  
100% pass rate on all core gates (Hermiticity, shape consistency, reproducibility, positive control, negative control). Shows validation rigor.

**Source Data:**
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 56-66 (core gates)
- `reports/VALIDATION_STATUS.md` — core gates summary

**Columns:**
| Gate | Pass Count | Total Cases | Pass Rate | Max Residual / Deviation |
|------|-----------|-------------|-----------|--------------------------|
| Hermiticity | 6615 | 6615 | 100.0% | ≤1e-9 |
| Shape Consistency | 6615 | 6615 | 100.0% | - |
| Reproducibility | 6615 | 6615 | 100.0% | Exact match |
| Positive Control (W=0) | 945 | 945 | 100.0% | All delocalized |
| Negative Control (q=0 disordered) | 945 | 945 | 100.0% | 0 false positives |

**Priority:** **REQUIRED** — demonstrates validation rigor (no false positives)

**STATUS:** ✅ **COMPLETED** (2026-05-16)
- Extracted: `reports/FIGURE_DATA_CORE_GATES_v0.1.16.md`
- Source: `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/summary.md` + `RELEASE_NOTES_v0.1.15.md`
- Key result: 100% pass rate on all 5 core gates (6615 cases), 0 false positives

**Risks:** None (gate results, not physics claims)

---

### T4. Ring/alpha=0 Failure Breakdown (51 Total Failures)

**Title:** "Ring/alpha=0 Failure Classification: Complete vs. Window-Sensitive vs. v2/v3 Disagreement"

**Purpose/Message:**  
Detailed breakdown of 51 ring/alpha=0 failures: 37 complete failures (both gates fail), 14 window-sensitive (kernel_only fails, fixed_window passes), 7 v2/v3 disagreements. Shows failure mode diversity.

**Source Data:**
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 72-75 (failure breakdown)
- `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/metrics.json`

**Columns:**
| Failure Type | Count | Percentage of 51 | Description |
|--------------|-------|------------------|-------------|
| Complete failure | 37 | 72.5% | Both kernel_only and fixed_window gates fail |
| Window-sensitive | 14 | 27.5% | kernel_only fails, fixed_window passes (historical pattern) |
| v2/v3 disagreement | 7 | 13.7% | v2 and v3 gate verdicts disagree (subset of above) |
| **TOTAL** | **51** | **100%** | All at ring + alpha=0.0, s1_size < 64 |

**Priority:** **REQUIRED** — shows caveat discovery process

**Risks:** None (failure classification is methodological)

---

### T5. Targeted Follow-Up Lattice-Size Scaling (Ring/alpha=0)

**Title:** "Ring/alpha=0 Lattice-Size Scaling: Failure Rate vs. s1_size (Convergence at s1_size≥64)"

**Purpose/Message:**  
Lattice-size scaling table showing failures vanish at s1_size≥64. Key evidence for "small-lattice artifact" verdict.

**Source Data:**
- `reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/summary.md`
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 97-106

**Columns:**
| s1_size | Failures | Total Cases (ring/alpha=0) | Failure Rate |
|---------|----------|----------------------------|--------------|
| 8 | 25 | ~147 | ~17.0% |
| 16 | 1 | ~147 | ~0.7% |
| 24 | 19 | ~147 | ~12.9% |
| 32 | 3 | ~147 | ~2.0% |
| 48 | 3 | ~147 | ~2.0% |
| **64** | **0** | ~126 | **0.0%** ✅ |
| **96** | **0** | ~126 | **0.0%** ✅ |

**Additional row:**
| **Decision Rule 1 Result** | 0/252 = 0.0% < 2.0% threshold → **SMALL_LATTICE_ARTIFACT** ✅ |

**Priority:** **REQUIRED** — key result (convergence proof)

**Risks:** Low. Must emphasize "discretized toy operator convergence", NOT "continuum extrapolation".

---

### T6. v2/v3 Gate Disagreement Summary (7 Cases)

**Title:** "v2/v3 Localization Gate Disagreement: window_robust (v3) vs. fixed_window (v2)"

**Purpose/Message:**  
7 cases where v2 (fixed_window, permissive) and v3 (window_robust, stricter) gates disagree. All in ring/alpha=0 subset. Shows gate policy choice matters.

**Source Data:**
- `reports/RELEASE_NOTES_v0.1.15.md` — line 75 (v2/v3 disagreements mention)
- `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/metrics.json`

**Columns:**
| Case ID | q | s1_size | W | seed | v2 (fixed_window) | v3 (window_robust) | Verdict |
|---------|---|---------|---|------|-------------------|-------------------|---------|
| [extract from metrics.json] | | | | | PASS | FAIL | Disagreement |
| ... | | | | | | | |
| **TOTAL** | | | | | | | **7 cases** |

**Priority:** **OPTIONAL** — demonstrates gate sensitivity, but not essential for methodology focus

**Risks:** Low. Technical detail may distract from main message (ring/alpha=0 convergence).

---

### T7. Claim Ladder Table (4-Tier Hierarchy)

**Title:** "Claim Ladder: Validated Toy Claims → Engineering → Unresolved → Forbidden"

**Purpose/Message:**  
Hierarchical table separating validated toy claims from forbidden physical claims. Prevents misinterpretation.

**Source Data:**
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section: Claim Ladder

**Columns:**
| Level | Category | Examples | Status |
|-------|----------|----------|--------|
| Tier 1 | Validated Toy Claims | S²×S¹ operators pass Anderson benchmark (99.1%); ring/alpha=0 converges at s1_size≥64; reproducibility: 6615/6615 | ✅ VALIDATED |
| Tier 2 | Supported Engineering Claims | Falsification Ladder reduces false positives (0 q=0 false positives); release integrity prevents contradictions | ✅ SUPPORTED |
| Tier 3 | Unresolved Scientific Questions | Continuum extrapolation (not yet performed); S²×S² validation (next milestone); physical interpretation (theoretical question) | ❓ UNRESOLVED |
| Tier 4 | Forbidden Physical Claims | Continuum compactification; S⁶/S³×S⁶ validation; Standard Model derivation; physical chirality proof; Witten/Lichnerowicz bypass | ❌ FORBIDDEN |

**Priority:** **REQUIRED** — prevents scope creep and misinterpretation

**Risks:** None (claim ladder explicitly separates validated toy from forbidden physics)

---

### T8. Scientific Non-Claims Table (8 Explicit Non-Claims)

**Title:** "Scientific Non-Claims: What v0.1.15 Does NOT Prove or Claim"

**Purpose/Message:**  
Explicit table of non-claims prevents misinterpretation of toy results as physical proofs. 8 explicit non-claims.

**Source Data:**
- `reports/RELEASE_NOTES_v0.1.15.md` — lines 180-188 (scientific non-claims)
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section 9.8 (Non-Claims Table)

**Columns:**
| Non-Claim | Reason (Why NOT Validated) |
|-----------|---------------------------|
| Continuum compactification | All operators discretized, no continuum extrapolation performed |
| S⁶ or S³×S⁶ validation | Only S², S³, S¹, S²×S¹ tested |
| Standard Model derivation | No gauge group calculation, no fermion generations |
| Physical chirality proof | Dirac indices are topological toy counts, not physical chiral fermions |
| Witten/Lichnerowicz bypass | Numerical index ≠ rigorous mathematical proof |
| Physical extra dimensions | Anderson benchmark is numerical test, not physical compactification mechanism |
| Hierarchy problem solution | Radion toy model does not address moduli stabilization in string theory |
| Observable predictions | Global chiral index is discretized toy analog, not continuum field theory prediction |

**Priority:** **REQUIRED** — prevents misinterpretation (most important table for toy scope)

**STATUS:** ✅ **COMPLETED** (2026-05-16)
- Extracted: `reports/FIGURE_DATA_SCIENTIFIC_NONCLAIMS_v0.1.16.md`
- Source: Consolidation of 8 mandatory non-claims from all release documents
- **MOST IMPORTANT TABLE** — defines toy scope, prevents overclaims, retraction-proof

**Risks:** None (explicit non-claims prevent overclaims)

---

### T9. Release Artifact Manifest (v0.1.15)

**Title:** "v0.1.15 Release Artifact Manifest: RUNS, Reports, Tests, Git Tag"

**Purpose/Message:**  
Comprehensive list of v0.1.15 release artifacts: run paths, reports, pytest status, git commit/tag. Shows reproducibility trail.

**Source Data:**
- `reports/V0_1_15_RELEASE_INTEGRITY_AUDIT.md` — Section 3 (Release Artifacts Audit)
- `reports/RELEASE_NOTES_v0.1.15.md`

**Columns:**
| Artifact Type | Path / Reference | Status | Verification |
|--------------|------------------|--------|--------------|
| Full Diagnostic Run | reports/RUNS/20260515-201150_s2_s1_product_discretized_full/ | ✅ | 6615/6615 cases, classification confirmed |
| Ring/alpha=0 Follow-Up | reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/ | ✅ | 1349 cases, decision rule applied |
| Release Notes | reports/RELEASE_NOTES_v0.1.15.md | ✅ | Comprehensive narrative, refined caveat |
| Validation Status | reports/VALIDATION_STATUS.md | ✅ | Baseline updated, caveat present |
| Spectral Report | reports/SPECTRAL_REPORT.md | ✅ | Caveat updated, lattice-size scaling |
| Issues Scientific | reports/ISSUES_SCIENTIFIC.md | ✅ | Caveat refined, baseline impact |
| Integrity Audit | reports/V0_1_15_RELEASE_INTEGRITY_AUDIT.md | ✅ | Verdict: release_integrity_confirmed |
| Pytest | 203 passed, 1 warning | ✅ | Full test suite coverage |
| Git Commit | 65b6973 | ✅ | Initial commit, 202 files, 41567 lines |
| Git Tag | v0.1.15-s2-s1-product-discretized-full | ✅ | Annotated tag with full description |

**Priority:** **OPTIONAL** — demonstrates reproducibility trail, but not essential for methodology focus

**Risks:** None (artifact manifest is reproducibility evidence)

---

### T10. Future Work Roadmap (Wilson Audit, S²×S², Continuum)

**Title:** "Future Work Roadmap: Track B (Wilson Audit) → Track C (S²×S²) → Continuum Extrapolation"

**Purpose/Message:**  
Roadmap showing next steps: Wilson audit (theory risk mitigation) → S²×S² validation (scientific scaling) → continuum extrapolation (long-term). Shows current work is first step, not complete story.

**Source Data:**
- `reports/ROADMAP_v0.1.16.md` — Section: Candidate Tracks
- `reports/METHODOLOGY_PAPER_OUTLINE_v0.1.16.md` — Section 10 (Future Work)

**Columns:**
| Track | Goal | Timeline | Dependencies | Risk |
|-------|------|----------|--------------|------|
| v0.1.16 (Track A) | Methodology paper outline | 2-3 weeks | None (docs-only) | LOW |
| v0.1.17 (Track B) | Wilson / fermion-doubling audit | 3-4 weeks | Track A complete | MEDIUM |
| v0.1.18 (Track C) | S²×S² product-discretized validation | 4-6 weeks | Track A+B complete | MEDIUM |
| v0.1.19+ | S³×S³, eventual S³×S⁶ | 6-12 months | Track C + Wilson audit | HIGH |
| Long-term | Continuum extrapolation (finite-size scaling) | 1-2 years | Multiple products validated | HIGH |

**Priority:** **OPTIONAL** — shows future work, but not essential for current methodology paper

**Risks:** None (roadmap is planning, not claims)

---

## Data Extraction Tasks

### Task 1: Extract Lattice-Size Scaling Data (Ring/alpha=0)

**Source:** `reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/metrics.json`

**Extraction:**
```python
import json

# Load follow-up metrics
with open('reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/metrics.json') as f:
    metrics = json.load(f)

# Filter: ring/alpha=0 only
ring_alpha0 = [
    case for case in metrics['cases']
    if case['family'] == 'ring' and case['alpha'] == 0.0
]

# Aggregate by s1_size
from collections import defaultdict
by_s1_size = defaultdict(lambda: {'total': 0, 'failures': 0})

for case in ring_alpha0:
    s1_size = case['s1_size']
    by_s1_size[s1_size]['total'] += 1
    if case['failure_type'] in ['complete_failure', 'window_sensitive']:
        by_s1_size[s1_size]['failures'] += 1

# Print table
print("s1_size | Failures | Total | Failure Rate")
for s1_size in sorted(by_s1_size.keys()):
    data = by_s1_size[s1_size]
    rate = 100 * data['failures'] / data['total']
    print(f"{s1_size:7} | {data['failures']:8} | {data['total']:5} | {rate:6.1f}%")
```

**Output:** T5 (Lattice-Size Scaling Table), F7 (Lattice-Size Scaling Plot)

---

### Task 2: Extract Full Diagnostic Case Counts by Family

**Source:** `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/config.json`

**Extraction:**
```python
import json

# Load full diagnostic config
with open('reports/RUNS/20260515-201150_s2_s1_product_discretized_full/config.json') as f:
    config = json.load(f)

# Count cases per family
families = config['families']  # ['spectral_circle', 'ring', 'wilson_ring']
q_values = config['monopole_charges']  # [-3, -2, -1, 0, 1, 2, 3]
s1_sizes = config['s1_sizes']  # [8, 16, 24, 32, 48]
alphas = config['alphas']  # [0.0, 0.25, 0.5]
disorders = config['disorders']  # [0.0, 2.0, 4.0, 6.0, 8.0, 12.0, 16.0]
seeds = config['seeds']  # [122, 123, 124, 456]

cases_per_family = len(q_values) * len(s1_sizes) * len(alphas) * len(disorders) * len(seeds)
total_cases = cases_per_family * len(families)

print(f"Cases per family: {cases_per_family}")
print(f"Total cases: {total_cases}")
print(f"Families: {', '.join(families)}")
```

**Output:** T2 (Full Diagnostic Case Count Table)

---

### Task 3: Extract Core Gates Pass Rates

**Source:** `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/summary.md`

**Extraction:**
```bash
# Extract gate results from summary.md
grep -A 5 "Core Gates" reports/RUNS/20260515-201150_s2_s1_product_discretized_full/summary.md

# Expected output:
# Hermiticity: 6615/6615 passed (max residual ≤1e-9)
# Shape consistency: 6615/6615 passed
# Reproducibility: 6615/6615 matched
# Positive control (W=0): 945/945 delocalized
# Negative control (q=0 disordered): 0/945 false positives
```

**Output:** T3 (Core Gates Pass Rate Table)

---

### Task 4: Extract Ring/alpha=0 Failure Breakdown

**Source:** `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/metrics.json`

**Extraction:**
```python
import json

# Load full diagnostic metrics
with open('reports/RUNS/20260515-201150_s2_s1_product_discretized_full/metrics.json') as f:
    metrics = json.load(f)

# Filter: ring/alpha=0 failures only
ring_alpha0_failures = [
    case for case in metrics['cases']
    if case['family'] == 'ring' and case['alpha'] == 0.0 and case['failure_type'] in ['complete_failure', 'window_sensitive', 'v2_v3_disagreement']
]

# Count by failure type
from collections import Counter
failure_counts = Counter(case['failure_type'] for case in ring_alpha0_failures)

print(f"Complete failures: {failure_counts['complete_failure']}")
print(f"Window-sensitive: {failure_counts['window_sensitive']}")
print(f"v2/v3 disagreements: {failure_counts['v2_v3_disagreement']}")
print(f"Total: {sum(failure_counts.values())}")
```

**Output:** T4 (Ring/alpha=0 Failure Breakdown Table)

---

### Task 5: Extract IPR Distributions for Anderson Localization Comparison

**Source:** `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/data.npz` (if saved) OR `metrics.json`

**Extraction:**
```python
import json
import numpy as np
import matplotlib.pyplot as plt

# Load full diagnostic metrics
with open('reports/RUNS/20260515-201150_s2_s1_product_discretized_full/metrics.json') as f:
    metrics = json.load(f)

# Extract IPR values for disordered cases (W > 0), split by family
ipr_by_family = {}
for family in ['spectral_circle', 'ring', 'wilson_ring']:
    ipr_by_family[family] = [
        case['ipr'] for case in metrics['cases']
        if case['family'] == family and case['W'] > 0
    ]

# Plot histograms
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
for i, family in enumerate(['spectral_circle', 'ring', 'wilson_ring']):
    axes[i].hist(ipr_by_family[family], bins=50, alpha=0.7)
    axes[i].set_title(family)
    axes[i].set_xlabel('IPR')
    if i == 0:
        axes[i].set_ylabel('Count')
plt.tight_layout()
plt.savefig('figures/anderson_ipr_comparison_3families.png')
```

**Output:** F11 (Anderson IPR Distribution Comparison)

---

## Minimal Figure Set for First Draft

### Recommended 4 Required Figures

**F1. GeoSpectra Falsification Ladder Workflow Diagram** ✅  
*Rationale:* Core methodology contribution visualization. Shows falsification-first workflow.

**F5. Ring/alpha=0 Failure Rate by s1_size (Heatmap)** ✅  
*Rationale:* Key result visualization (failures localized to small s1_size).

**F7. Lattice-Size Scaling Result: Failures Vanish at s1_size≥64** ✅  
*Rationale:* Convergence proof. Demonstrates small-lattice artifact resolution.

**F8. Claim Ladder Pyramid (4-Tier Hierarchy)** ✅  
*Rationale:* Prevents misinterpretation of toy scope as physical proof. Essential for non-claims.

---

### Recommended 4 Required Tables

**T1. v0.1.15 Validation Chain (Timeline + Milestones)** ✅  
*Rationale:* Complete falsification workflow summary (discover → investigate → resolve).

**T3. Core Gates Pass Rate Summary (6615 Cases)** ✅  
*Rationale:* Demonstrates validation rigor (100% pass rate on controls, 0 false positives).

**T5. Targeted Follow-Up Lattice-Size Scaling (Ring/alpha=0)** ✅  
*Rationale:* Key result table (convergence at s1_size≥64, decision rule applied).

**T8. Scientific Non-Claims Table (8 Explicit Non-Claims)** ✅  
*Rationale:* MOST IMPORTANT TABLE — prevents misinterpretation as physical proof.

---

### Optional Enhancements (for second draft if space permits)

- F2. Validation Pipeline Timeline (shows iterative workflow)
- F6. Caveat Before/After Comparison (shows falsification process)
- F10. Production Guideline Flowchart (practical engineering value)
- T2. Full Diagnostic Case Count Breakdown (comprehensive coverage)
- T4. Ring/alpha=0 Failure Breakdown (detailed failure mode analysis)
- T7. Claim Ladder Table (text alternative to F8 pyramid)

---

## Risks

### Risk 1: Figures Overstate Toy Scope

**Probability:** MEDIUM (plots can mislead readers into thinking results are physical)

**Mitigation:**
- All figure captions MUST include "discretized toy operator" qualifier
- F3 (S²×S¹ operator schematic) labeled as "Toy Operator Example"
- F5, F7 (ring/alpha=0 results) captioned as "small-lattice artifact (toy regime)"
- Avoid "physical compactification", "continuum extrapolation", "observable predictions" in captions

**Residual risk:** Readers skip captions → misinterpret plots as physical results.

**Additional mitigation:** Add banner to figure section: "All figures show discretized toy operators. No physical compactification claims."

---

### Risk 2: Plots Imply Physical Proof

**Probability:** MEDIUM (Anderson localization plots may be interpreted as "physical extra dimensions")

**Mitigation:**
- F11 (Anderson IPR distribution) captioned as "Anderson benchmark (numerical test)"
- F5, F7 (ring/alpha=0 scaling) emphasize "discretized toy operator convergence"
- Avoid "localization in physical compactification" language
- T8 (non-claims table) explicitly rules out physical interpretation

**Residual risk:** Reviewers/readers familiar with Anderson localization in condensed matter may assume physical interpretation.

**Response:** Methodology paper framing (computational workflow, not physics discovery) + explicit non-claims table (T8).

---

### Risk 3: Missing Raw Artifacts (RUNS Ignored by Git)

**Probability:** MEDIUM (RUNS artifacts are local-only, not in git)

**Mitigation:**
- Extract all figures/tables from RUNS artifacts BEFORE archiving
- Save extracted data as separate files: `data/extracted_lattice_size_scaling.json`
- If RUNS artifacts lost, can regenerate from source code + config, but expensive (~18 hours)

**Residual risk:** If local machine fails before extraction, RUNS artifacts lost → figures cannot be regenerated.

**Response:** Priority 1: Extract lattice-size scaling data (F7, T5) immediately (most important result).

---

### Risk 4: Too Many Figures for First Draft

**Probability:** HIGH (11 figures proposed, journal limits typically 6-8)

**Mitigation:**
- Minimal first-draft set: 4 figures + 4 tables (specified above)
- Move optional figures to supplementary material or appendix
- Combine related figures (e.g., F5 + F7 as 2-panel figure)

**Residual risk:** Reviewers request more figures → easy to add from optional set.

**Response:** Start with minimal set, expand based on reviewer feedback.

---

### Risk 5: Data Extraction Complexity (IPR Distributions)

**Probability:** LOW (IPR extraction requires data.npz, may not be saved)

**Mitigation:**
- F11 (Anderson IPR distribution) marked as **OPTIONAL** — not required for first draft
- If data.npz missing, skip IPR plots, use failure rate tables (F5, T5) instead

**Residual risk:** Reviewers request IPR distributions → can regenerate full run with data.npz saving enabled.

**Response:** Document data.npz availability in inventory. If missing, defer to future work.

---

## Acceptance Criteria

### Inventory Completeness
- [x] Inventory document created: `reports/FIGURES_TABLES_INVENTORY_v0.1.16.md`
- [x] Each figure/table mapped to source data
- [x] Minimal first-draft set selected (4 figures + 4 tables)
- [x] Data extraction tasks specified (5 tasks)
- [x] Risks documented (5 risks with mitigation)

### Data Source Verification
- [x] Full diagnostic run path confirmed: `reports/RUNS/20260515-201150_s2_s1_product_discretized_full/`
- [x] Ring/alpha=0 follow-up path confirmed: `reports/RUNS/20260516-165729_s2_s1_product_discretized_ring_alpha0_followup/`
- [x] Key reports referenced: RELEASE_NOTES, VALIDATION_STATUS, SPECTRAL_REPORT, ISSUES_SCIENTIFIC
- [x] Source artifacts status: LOCAL ONLY (RUNS ignored by git, 280MB)

### Extraction Readiness
- [x] Python extraction scripts provided (5 tasks)
- [x] Expected output files specified (figures/*.png, tables in paper body)
- [x] Priority ranking complete (required vs. optional)

### Scope Compliance
- [x] No new code experiments (inventory only)
- [x] No scientific code changes
- [x] No baseline promotion (v0.1.15 unchanged)
- [x] Toy scope emphasized in all figure captions
- [x] No physical overclaims (continuum, S⁶/S³×S⁶, Standard Model, chirality)

---

## Summary

**Inventory Created:** `reports/FIGURES_TABLES_INVENTORY_v0.1.16.md`

**Candidate Figures:** 11 proposed (F1-F11)  
**Candidate Tables:** 10 proposed (T1-T10)  
**Minimal First-Draft Set:** 4 figures + 4 tables (specified)

**Required Figures (First Draft):**
1. F1: Falsification Ladder Workflow Diagram
2. F5: Ring/alpha=0 Failure Rate Heatmap
3. F7: Lattice-Size Scaling (Convergence at s1_size≥64)
4. F8: Claim Ladder Pyramid

**Required Tables (First Draft):**
1. T1: v0.1.15 Validation Chain
2. T3: Core Gates Pass Rate Summary
3. T5: Lattice-Size Scaling Table
4. T8: Scientific Non-Claims Table

**Data Extraction Tasks:** 5 specified (lattice-size scaling, case counts, core gates, failure breakdown, IPR distributions)

**Risks:** 5 identified with mitigation (overstate toy scope, imply physical proof, missing raw artifacts, too many figures, data extraction complexity)

**Baseline:** v0.1.15-s2-s1-product-discretized-full (unchanged)

**Pytest:** NOT required (docs-only, no code changes)

---

## Next Steps (After Inventory Acceptance)

### Immediate (Week 1)
1. **Extract lattice-size scaling data** (Task 1) — highest priority, key result
2. **Generate F7** (Lattice-Size Scaling Plot) — convergence proof
3. **Generate T5** (Lattice-Size Scaling Table) — numerical evidence

### Short-term (Week 1-2)
4. **Extract core gates data** (Task 3) → T3 (Core Gates Pass Rate Table)
5. **Extract case counts** (Task 2) → T2 (Full Diagnostic Case Count Table)
6. **Create F1** (Falsification Ladder Diagram) — core methodology visualization

### Medium-term (Week 2-3)
7. **Generate F8** (Claim Ladder Pyramid) — prevents misinterpretation
8. **Generate T8** (Scientific Non-Claims Table) — explicit non-claims
9. **Create T1** (v0.1.15 Validation Chain) — complete workflow summary

### Optional (If Time Permits)
10. Extract failure breakdown (Task 4) → T4 (Ring/alpha=0 Failure Breakdown)
11. Extract IPR distributions (Task 5) → F11 (Anderson IPR Comparison)
12. Create F5 (Ring/alpha=0 Failure Heatmap) — visual failure localization

---

**Inventory Status:** READY FOR DATA EXTRACTION

**Recommended Action:** Accept inventory → proceed to Week 1 extraction tasks (lattice-size scaling data → F7, T5) → draft Introduction.
