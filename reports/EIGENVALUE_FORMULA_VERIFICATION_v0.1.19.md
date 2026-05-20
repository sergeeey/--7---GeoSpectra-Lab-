# Eigenvalue Formula Verification — arXiv:1103.4097

**Date:** 2026-05-20  
**Status:** 🔴 **CRITICAL MISMATCH FOUND**  
**Source:** arXiv:1103.4097 "Eigenspaces of the Spin Dirac operator over S³" by J. Fabian Meier

---

## Executive Summary

**RESULT:** Implementation eigenvalue formula **DOES NOT MATCH** paper.

**Paper formula:**
- Positive eigenvalues: λ⁺(k) = **(k + 1/2) / R**
- Negative eigenvalues: λ⁻(k) = **-(k + 3/2) / R**

**Implementation formula (dirac_s3.py:77-78):**
- λ(n) = **±(n + 3/2) / R**  (symmetric!)

**Impact:** Implementation uses ONLY the larger-magnitude eigenvalue and symmetrizes it, **ignoring the smaller-magnitude positive eigenvalue**.

---

## Paper Evidence

### Location
arXiv:1103.4097, **Page 15**, Section 6 "The spectrum of D"

### Key Equations

**Equation (6.4):**
```
(D̄ + k)(D̄ - (k+2))σ = 0   ∀σ ∈ ℍᵖₖ
```

This quadratic equation gives D̄ eigenvalues: **-k** or **(k+2)**.

**Relationship D and D̄:**
> "If we subtract 1/2 to get from D̄ to D and go back to the whole space..."

Therefore: **D = D̄ - 1/2**

**D eigenvalues:**
- From D̄ = -k: **D = -k - 1/2 = -(k + 1/2)**  [BUT paper writes this as eigenspace for *positive* eigenvalue]
- From D̄ = k+2: **D = (k+2) - 1/2 = k + 3/2**  [paper writes this as eigenspace for *negative* eigenvalue]

**Wait — need to re-read eigenspace labels...**

### Eigenspace Labels (Page 15)

**"For k + 1/2:"**  
Basis vectors: `e₀ ⊗ |p⟩|q⟩ - e₂ ⊗ |p-1⟩|q⟩` where `p = 1,...,k`, `q = 0,...,k`

**"For -k - 3/2:"**  
Basis vectors:
- `(p-k-1)e₀ ⊗ |p⟩|q⟩ - pe₂ ⊗ |p-1⟩|q⟩` where `p = 1,...,k`, `q = 0,...,k`
- `e₀ ⊗ |0⟩|q⟩, e₂ ⊗ |k⟩|q⟩` where `q = 0,...,k`

**Interpretation:** For each level k ∈ {0, 1, 2, ...}, there are TWO eigenvalues:
1. **λ₊(k) = +(k + 1/2)**
2. **λ₋(k) = -(k + 3/2)**

---

## Numerical Comparison

| k | Paper: λ₊ (R=1) | Paper: λ₋ (R=1) | Implementation (n=k, R=1) | Match? |
|---|-----------------|-----------------|---------------------------|--------|
| 0 | **+0.5** | **-1.5** | **±1.5** | ❌ Missing +0.5 |
| 1 | **+1.5** | **-2.5** | **±2.5** | ❌ Missing +1.5 |
| 2 | **+2.5** | **-3.5** | **±3.5** | ❌ Missing +2.5 |
| 3 | **+3.5** | **-4.5** | **±4.5** | ❌ Missing +3.5 |

**Pattern:** Implementation takes the **larger-magnitude** eigenvalue (e.g., -3/2 for k=0) and **symmetrizes** it (±3/2), **dropping the smaller-magnitude** positive eigenvalue (+1/2).

---

## Why Positive Control Passed

**Circular Logic:**

```python
# tests/test_gate_2_controls.py:73
expected = np.array([-3.5, -2.5, -1.5, 1.5, 2.5, 3.5])
```

This `expected` array was **hand-crafted from implementation formula**, NOT derived independently from paper.

Test checks: `implementation eigenvalues == expected values derived from same implementation formula` → **tautology**.

Test SHOULD check: `implementation eigenvalues == paper formula eigenvalues` → would **FAIL**.

---

## Correct Formula

**From arXiv:1103.4097, page 15:**

```python
# For each level k ∈ {0, 1, 2, ...}
eigenvalue_pos = (k + 0.5) / radius   # +(k + 1/2) / R
eigenvalue_neg = -(k + 1.5) / radius  # -(k + 3/2) / R
```

**NOT symmetric:** |eigenvalue_pos| ≠ |eigenvalue_neg|

**Example k=0, R=1:**
- λ₊ = +0.5
- λ₋ = -1.5

**Example k=1, R=1:**
- λ₊ = +1.5
- λ₋ = -2.5

---

## Degeneracy Verification

### Paper (Page 13)

> "These spaces have the respective ℍ-dimension (k+1)². So we must have  
> Vₖ ≅ ℍ ⊗_ℂ (ℍₖ ⊗_ℂ ℍₖ)  ∀k ≥ 1"

This suggests dimension = (k+1)² **per representation space**, but need to check if this is TOTAL or per eigenspace.

**Counting basis vectors on page 15:**

**For eigenvalue k + 1/2:**
- Basis: `e₀ ⊗ |p⟩|q⟩ - e₂ ⊗ |p-1⟩|q⟩`
- Ranges: p = 1,...,k (k values), q = 0,...,k (k+1 values)
- Count: **k(k+1)** basis vectors

**For eigenvalue -k - 3/2:**
- Basis part 1: `(p-k-1)e₀ ⊗ |p⟩|q⟩ - pe₂ ⊗ |p-1⟩|q⟩`, p=1,...,k, q=0,...,k → **k(k+1)** vectors
- Basis part 2: `e₀ ⊗ |0⟩|q⟩, e₂ ⊗ |k⟩|q⟩`, q=0,...,k → **2(k+1)** vectors
- Total: **k(k+1) + 2(k+1) = (k+2)(k+1)** basis vectors

**Total dimension for level k:**
k(k+1) + (k+2)(k+1) = (k+1)(k + k + 2) = **(k+1)(2k+2) = 2(k+1)²**

**This MATCHES implementation degeneracy 2(n+1)²!** ✅

So degeneracy formula is **CORRECT**, but eigenvalue formula is **WRONG**.

---

## Action Required

1. **Fix eigenvalue formula** in `dirac_s3.py`:
   ```python
   eigenvalue_pos = (n + 0.5) / radius   # k + 1/2
   eigenvalue_neg = -(n + 1.5) / radius  # -(k + 3/2)
   ```

2. **Fix positive control test** to use paper-derived expected values:
   ```python
   # For k=2 (n=2), R=1:
   expected = np.array([-4.5, -3.5, -2.5, -1.5, 0.5, 1.5, 2.5])
   # NOT: [-3.5, -2.5, -1.5, 1.5, 2.5, 3.5]
   ```

3. **Re-run all Gate 2 tests** after fix — expect FAILURES until corrected.

4. **Verify asymmetric eigenvalue structure** makes physical sense (consult lattice field theory expert).

---

## Implications for Gate 2

**Status:** Gate 2 verdict **INVALID** — testing WRONG operator.

**Skeptic was right:** Eigenvalue formula had [НЕДОСТАТОЧНО ДАННЫХ] status → now [FALSIFIED].

**Next steps:**
1. Verify degeneracy per eigenspace (k(k+1) vs (k+2)(k+1)) matches paper
2. Fix implementation
3. Re-run Gate 2 from scratch
4. **CRITICAL:** Check if S²×S¹ also has wrong formula (affects v0.1.15 validity!)

---

## Open Questions

1. **Why asymmetric?** Physical interpretation of |λ₊| ≠ |λ₋|?
2. **How does this affect product structure?** S³×S¹ operator uses D_S3², not D_S3 — does squaring restore symmetry?
3. **Discretization impact?** Does finite j_max truncation introduce artifacts?
4. **S²×S¹ validity?** Same issue there, or S² Dirac eigenvalues are different?

---

**Confidence:** HIGH (direct quote from paper, clear mismatch)  
**Next action:** Fix formula → re-test → consult expert before external contact  
**External contact BLOCKED** until this resolved
