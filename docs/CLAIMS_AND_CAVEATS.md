# Claims and Caveats — GeoSpectra Lab

**Purpose:** Explicit boundaries of what GeoSpectra Lab can and cannot claim based on current validation status.

**Last updated:** 2026-05-24

---

## ✅ What GeoSpectra Lab CAN Claim

### 1. Finite-Lattice Computational Validation

**Allowed:**
- GeoSpectra Lab is a reproducible falsification-first validation harness for finite-lattice spectral toy geometries
- Current case study: S³×S¹ finite lattice (N ≤ 896)
- Validation methodology includes: controls, progressive profiles, independent audit, targeted follow-up, negative controls

**Evidence:**
- 203 passing tests
- 1235+ git commits
- Zenodo DOI: 10.5281/zenodo.20252651
- Independent verification report (`VERIFICATION_REPORT.md`)

---

### 2. Gate 4B S³×S¹ Finite-Size Scaling Results

**Allowed (with mandatory caveats):**

> "S³×S¹ Gate 4B supports finite-lattice robustness of the W=20 Anderson disorder localization signal under finite-size scaling from s1_size=16 to 128 (N = 112 to 896), with true eigenvector-based IPR contrast ≥2.0× and family consistency ≥2/3."

**Mandatory caveats:**
- Finite-lattice only (N ≤ 896)
- Anderson disorder only (diagonal on-site U(r) ∈ [-W, W])
- S³×S¹ only (no generalization to other geometries)
- W=20 exploratory (not optimized)
- True IPR metric (v0.1.21, not comparable with v0.1.20)
- **No physical compactification claim**

**Evidence:**
- Full report: `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md`
- 216/216 cases executed, 0 failures
- Aggregate contrast: 7.15× (W=20 vs W=0)
- FSS trend: STRENGTHENING (3.76× → 24.90×)
- Family consistency: 3/3 PASS (spectral_circle, ring, wilson_ring)

---

### 3. Negative Controls (v0.1.22 — Partial)

**Allowed:**
- Negative controls protocol pre-registered
- Batches 1-2 completed locally (18/54 cases)
- Batches 3-6 pending remote execution (36/54 cases)

**NOT allowed (yet):**
- Final verdict on harness specificity (execution incomplete)
- Claim that controls fail as expected (results pending)

---

### 4. Null Results and Failures

**Allowed (transparency):**
- Weak-disorder GOE check: W=0.5, ⟨r⟩=0.2631 — not closer to GOE than Poisson (null result)
- v0.1.20 IPR metric implementation error (eigenvalue mean instead of eigenvector-based)
- Ring/alpha=0 small-lattice artifacts (s1_size < 64)
- Open vs periodic boundary sensitivity

**Evidence:**
- `reports/NULL_RESULTS.md`
- `reports/ISSUES_SCIENTIFIC.md`
- Metric correction transparency (v0.1.20 → v0.1.21)

---

## ❌ What GeoSpectra Lab CANNOT Claim

### 1. Physical Compactification ❌

**Forbidden:**
- "GeoSpectra validates covariant compactification"
- "GeoSpectra proves physical extra dimensions"
- "GeoSpectra demonstrates real compact product geometry"

**Why:**
- All results are finite-lattice (N ≤ 896)
- No thermodynamic limit (N → ∞)
- No continuum field theory
- Toy numerical operators, not physical Hamiltonians

---

### 2. Standard Model Physics ❌

**Forbidden:**
- "GeoSpectra derives SU(3) × SU(2) × U(1)"
- "GeoSpectra proves geometric origin of gauge groups"
- "GeoSpectra explains fermion generations"

**Why:**
- No gauge field construction
- No symmetry breaking mechanism
- No connection to real particle physics

---

### 3. Chiral Fermions ❌

**Forbidden:**
- "GeoSpectra proves chiral fermions"
- "GeoSpectra demonstrates protected chiral zero modes"
- "GeoSpectra bypasses Witten/Lichnerowicz no-go theorems"

**Why:**
- S² monopole index control is a **finite-mode toy model**, not physical
- Toy Dirac localization has near-zero modes but **numerical index = 0** (paired/accidental, not protected)
- No index calculation on full S³×S¹ geometry
- No demonstration of chirality protection mechanism

---

### 4. Continuum Limit ❌

**Forbidden:**
- "GeoSpectra validates continuum geometry"
- "GeoSpectra proves thermodynamic limit behavior"
- "Finite-lattice results extrapolate to N → ∞"

**Why:**
- Largest lattice: N = 896
- No rigorous N → ∞ extrapolation performed
- Finite-size effects not fully characterized

---

### 5. Generalization ❌

**Forbidden:**
- "Gate 4B results apply to other geometries (S⁶, S³×S⁶, T⁴)"
- "IPR robustness generalizes beyond S³×S¹"
- "Negative controls (if passed) validate all geometries"

**Why:**
- Current validation: S³×S¹ only
- Cross-geometry transfer tests: pending
- Each geometry requires independent validation

---

### 6. Endorsement / Affiliation ❌

**Forbidden:**
- "Tom Lawrence endorses this project"
- "GeoSpectra is affiliated with Tom Lawrence"
- "This project validates Tom Lawrence's theory"
- "Tom Lawrence reviewed these results"

**Why:**
- GeoSpectra is **independently developed** by Sergey Boyko
- Inspiration from Tom Lawrence's public work ≠ endorsement
- No collaboration or affiliation exists unless explicitly stated

---

## ⚠️ Careful Wording Required

### r-Statistic Diagnostic

**Allowed:**
- "r-statistic diagnostic is consistent with localization interpretation"
- "r-statistic does not contradict the IPR signal"
- "Level-spacing statistics agree with IPR finding on W=20 direction"

**Forbidden:**
- ❌ "r-statistic confirms localization" (too strong)
- ❌ "r-statistic proves localization" (too strong)
- ❌ "r-statistic supports localization" (prefer "consistent with")

**Why:**
- r-statistic is a secondary diagnostic
- True IPR is the primary metric
- Consistent-with ≠ proves

---

### Negative Controls (After Completion)

**Allowed (if controls fail as expected):**
- "Harness can distinguish S³×S¹ signal from random/scrambled baselines"
- "Negative controls did not reproduce Gate 4B robustness pattern"

**Forbidden (even if controls pass):**
- ❌ "Negative controls prove S³×S¹ geometry is correct"
- ❌ "Negative controls validate covariant compactification"

**Why:**
- Controls test harness discrimination power, not physics validity
- Falsification ≠ validation

---

## 🎯 Summary Table

| Domain | Can Claim | Cannot Claim |
|--------|-----------|--------------|
| **Scope** | Finite-lattice toy validation harness | Physical compactification |
| **Geometry** | S³×S¹ finite lattice (N ≤ 896) | Continuum / thermodynamic limit |
| **Physics** | Computational robustness checks | Standard Model / gauge groups |
| **Chirality** | S² monopole index (toy control) | Protected chiral zero modes |
| **Methodology** | Falsification-first validation | Physics theory proof |
| **Attribution** | Inspired by Tom Lawrence's work | Endorsed by / affiliated with |

---

## 📋 Claim Checklist (Before External Communication)

Before making any public statement about GeoSpectra Lab, verify:

- [ ] Claim is explicitly allowed in this document
- [ ] All mandatory caveats are included
- [ ] Forbidden terms are avoided
- [ ] Finite-lattice scope is clear
- [ ] No physics overclaim
- [ ] No false affiliation/endorsement
- [ ] Evidence files are cited

---

## 📚 References

For detailed claim boundaries by milestone:

- `reports/CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md` — Gate 4B specific boundaries
- `reports/VALIDATION_STATUS.md` — Current validation state
- `README.md` — "What This Project Does NOT Prove" section
- `docs/RESEARCH_CONTEXT.md` — Independence and attribution statement

---

**Principle:**

> GeoSpectra Lab is a **validation tool**, not a physics theory. Claims must reflect computational results, not extrapolate to physics conclusions.

**Last updated:** 2026-05-24  
**Status:** ACTIVE — enforce before all external communication
