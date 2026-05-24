# Operator Decision Checklist — v0.1.23

**Quick-reference checklist для resolution operator-level inconsistencies.**

---

## Critical Path (Mandatory Before Heavy Experiments)

### 1. S³ Dirac Operator Decision

- [ ] Read arXiv:1103.4097 page 15 independently
- [ ] Verify paper formula interpretation
- [ ] Choose convention:
  - [ ] Convention A (symmetric ±(n+3/2)) — standard physics
  - [ ] Convention B (asymmetric +(k+1/2), -(k+3/2)) — representation theory
- [ ] Document chosen convention in `docs/OPERATOR_SPECIFICATIONS.md`
- [ ] IF Convention B chosen → update tests to asymmetric expectations
- [ ] IF Convention A chosen → fix dirac_s3.py to symmetric formula
- [ ] Add analytic spectrum unit tests
- [ ] All tests passing

### 2. S¹ Ring Scaling Convention

- [ ] Clarify ring scale: N/R vs N/(2πR)
- [ ] Document physical meaning of scale
- [ ] Investigate ring(alpha=0) behavior (collapse or not)
- [ ] IF normalization fix needed → apply and verify
- [ ] Update family-consistency interpretation
- [ ] Document in `docs/OPERATOR_SPECIFICATIONS.md`

### 3. Anderson 3D Dense Window Fix

- [ ] Fix anderson_3d.py line 120: median → closest-to-zero
- [ ] Add test for shifted spectrum case
- [ ] Verify dense/sparse path consistency
- [ ] Tests passing

### 4. Rerun Decision

- [ ] IF S³ Dirac code changed → v0.1.24 rerun mandatory
- [ ] IF S¹ ring scale changed → decide rerun necessity
- [ ] IF only documentation → no rerun, unfreeze interpretation
- [ ] Create rerun plan (if needed)

### 5. Claims and Documentation

- [ ] Update `docs/CLAIMS_AND_CAVEATS.md`
- [ ] Add forbidden claims (operator-level uncertainties)
- [ ] Update README.md status section
- [ ] Document operator audit lessons

---

## Decision Scenarios

### Scenario 1: Documentation Mismatch Only
- Tests wrong, code correct
- Timeline: 2-3 days
- Actions: update tests, documentation, unfreeze interpretation

### Scenario 2: Code Bug, No Gate 4B Impact
- S¹ or Anderson fix, S³ correct
- Timeline: 3-5 days
- Actions: fix, test, targeted validation

### Scenario 3: Code Bug Affects Gate 4B
- S³ Dirac wrong, symmetric fix needed
- Timeline: 7-10 days
- Actions: fix, test, v0.1.24 MANDATORY rerun

### Scenario 4: Corrected Operator Preserves Signal
- v0.1.24 rerun → signal persists
- Outcome: project strengthens

### Scenario 5: Corrected Operator Removes Signal
- v0.1.24 rerun → signal disappears
- Outcome: pivot required (methodology focus or abandon S³×S¹)

---

## Resume Criteria (Heavy Experiments)

**Before starting Gate 5 / negative controls batches 3-6 / new gates:**

✅ S³ Dirac decision finalized  
✅ S¹ scaling convention documented  
✅ Anderson dense window fix applied (if needed)  
✅ Rerun decision made  
✅ Claims updated  
✅ Tests passing

---

## Forbidden Until Decision

❌ Run Gate 5  
❌ Continue negative controls batches 3-6  
❌ Start v0.1.23 or new milestone  
❌ Heavy experiments (>100 cases)  
❌ Claim "S³×S¹ validated"  
❌ Interpret Gate 4B as theoretical validation  
❌ Submit papers / preprints  
❌ Delete or modify Gate 4B outputs

---

## Allowed During Decision Period

✅ Read and analyze existing Gate 4B outputs  
✅ Research arXiv references  
✅ Draft operator decision documents  
✅ Add analytic spectrum unit tests  
✅ Run small verification tests (<10 cases)  
✅ Update caveats in reports (без изменения raw results)

---

**Status:** OPERATOR_DECISION_REQUIRED_BEFORE_FIX  
**Next action:** Human decision on S³ Dirac convention (read arXiv:1103.4097 page 15)  
**Timeline:** 2-10 days (зависит от decision outcome)
