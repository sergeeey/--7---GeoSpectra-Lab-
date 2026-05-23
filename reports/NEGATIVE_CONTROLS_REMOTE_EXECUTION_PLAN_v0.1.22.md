# Negative Controls Remote Execution Plan — v0.1.22

**Purpose:** Complete batches 3–6 (36 remaining cases) on remote infrastructure  
**Prerequisite:** Local thermal constraint prevents further heavy execution  
**Target coverage:** 54/54 cases (100%)

---

## Execution Summary

**Completed locally:**
- Batch 1 (random_hermitian, W=0): 9 cases ✅
- Batch 2 (random_hermitian, W=20): 9 cases ✅

**Remaining to execute remotely:**
- Batch 3 (scrambled_geometry, W=0): 9 cases
- Batch 4 (scrambled_geometry, W=20): 9 cases
- Batch 5 (broken_wilson_term, W=0): 9 cases
- Batch 6 (broken_wilson_term, W=20): 9 cases

**Total remote workload:** 36 cases  
**Expected runtime:** ~3–4 hours (depends on remote hardware)

---

## Remote Infrastructure Options

### Option A: Google Colab (Free Tier)
**Pros:** Free, GPU available (not needed but fast CPU fallback), Jupyter interface  
**Cons:** 12-hour session timeout, cannot run overnight without interaction  
**Setup time:** ~15 minutes

### Option B: Google Colab Pro ($10/month)
**Pros:** 24-hour sessions, background execution, faster CPUs  
**Cons:** Cost  
**Setup time:** ~15 minutes

### Option C: University / Research Cluster
**Pros:** No cost, high-performance nodes, long runtimes allowed  
**Cons:** Requires account, queue wait time, unfamiliar environment  
**Setup time:** ~30–60 minutes (including SSH setup, conda env)

### Option D: AWS EC2 / Azure VM
**Pros:** Full control, on-demand scaling, persistent storage  
**Cons:** Cost (~$0.10–0.50/hour depending on instance type)  
**Setup time:** ~30 minutes

**Recommended:** **Option A (Google Colab Free)** for quick turnaround, or **Option C (cluster)** if available and familiar.

---

## Setup Steps (Google Colab Example)

### 1. Clone Repository
```python
!git clone https://github.com/<your-username>/N-7-GeoSpectra-Lab.git
%cd N-7-GeoSpectra-Lab
!git checkout main
!git pull origin main
```

### 2. Install Dependencies
```python
!pip install -q numpy scipy matplotlib
# Verify installation
import numpy as np
import scipy
print(f"NumPy: {np.__version__}, SciPy: {scipy.__version__}")
```

### 3. Verify Codebase Integrity
```python
# Check Gate 4B untouched
!git log --oneline -5
# Should show: 2ec84ab test(controls): complete batch 2 negative controls pilot

# Check batch 1-2 exist
!ls -lh reports/RUNS/negative_controls_v0.1.22/batch_01/ | head -5
!ls -lh reports/RUNS/negative_controls_v0.1.22/batch_02/ | head -5

# Verify no batch_03 (removed due to thermal issue)
!ls reports/RUNS/negative_controls_v0.1.22/
# Should show: batch_01, batch_02, config.json
```

---

## Execution Commands

### Batch 3: scrambled_geometry, W=0
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3
```

**Expected output:**
- 9 files: `reports/RUNS/negative_controls_v0.1.22/batch_03/case_018.json` ... `case_026.json`
- Runtime: ~30–40 minutes
- Last case (s1_size=128) will take ~5 minutes

**Validation after batch 3:**
```python
import json
import glob

batch_03_files = sorted(glob.glob("reports/RUNS/negative_controls_v0.1.22/batch_03/case_*.json"))
print(f"Batch 3 cases: {len(batch_03_files)}/9")

# Check for r_stat anomaly (local batch had r_stat=1.0, should be 0.39-0.53)
for f in batch_03_files[:3]:  # spot check first 3
    with open(f) as fp:
        data = json.load(fp)
    print(f"{f.split('/')[-1]}: r_stat={data['r_stat']:.4f}, ipr={data['true_ipr_mean']:.6f}")

# Expected: r_stat in range 0.35–0.55 (NOT 1.0), ipr ~ 0.001–0.02
```

**⚠️ If any case shows r_stat > 0.95 or r_stat < 0.2:** STOP, report issue, do NOT proceed to batch 4.

---

### Batch 4: scrambled_geometry, W=20
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 4
```

**Expected output:**
- 9 files: `case_027.json` ... `case_035.json`
- Runtime: ~30–40 minutes

---

### Batch 5: broken_wilson_term, W=0
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 5
```

**Expected output:**
- 9 files: `case_036.json` ... `case_044.json`
- Runtime: ~30–40 minutes

---

### Batch 6: broken_wilson_term, W=20
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 6
```

**Expected output:**
- 9 files: `case_045.json` ... `case_053.json`
- Runtime: ~30–40 minutes

---

## Post-Execution Validation

### Coverage Check
```bash
find reports/RUNS/negative_controls_v0.1.22 -name "case_*.json" | wc -l
# Expected: 54
```

### Case Numbering Check
```bash
ls reports/RUNS/negative_controls_v0.1.22/batch_*/case_*.json | sort | tail -5
# Last file should be: batch_06/case_053.json
```

### Metric Completeness Check
```python
import json
import glob

all_cases = sorted(glob.glob("reports/RUNS/negative_controls_v0.1.22/batch_*/case_*.json"))
missing_metrics = []

for f in all_cases:
    with open(f) as fp:
        data = json.load(fp)
    required = ["true_ipr_mean", "r_stat", "runtime_seconds", "control", "disorder_strength"]
    for key in required:
        if key not in data:
            missing_metrics.append((f, key))

if missing_metrics:
    print(f"⚠️ Missing metrics: {missing_metrics}")
else:
    print("✅ All 54 cases have required metrics")
```

---

## Download and Commit Results

### On Remote Machine (Colab / cluster)

**Configure git:**
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

**Commit batches 3–6:**
```bash
git add -f reports/RUNS/negative_controls_v0.1.22/batch_03/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_04/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_05/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_06/
git commit -m "test(controls): complete batches 3-6 negative controls (remote execution)"
```

**Push to origin:**
```bash
git push origin main
```

### On Local PC (after remote push)

**Pull remote results:**
```bash
git pull origin main
```

**Verify local presence:**
```bash
ls -lh reports/RUNS/negative_controls_v0.1.22/batch_0*/
# Should show batches 01, 02, 03, 04, 05, 06
```

---

## Aggregation and Decision Rules

**After all 54 cases committed and pulled locally:**

### 1. Aggregate Results
```bash
python scripts/aggregate_negative_controls_results.py
```

**Expected output:**
- `reports/RUNS/negative_controls_v0.1.22/aggregate_summary.json`
- Per-control statistics: mean IPR, mean r_stat, FSS trend
- Comparison to Gate 4B thresholds

### 2. Apply Decision Rules
```bash
python scripts/apply_negative_controls_decision_rules.py
```

**Expected output:**
- `reports/RUNS/negative_controls_v0.1.22/decision_verdict.txt`
- Per-control verdict: PASS (control rejected baseline) / FAIL (control mimics Gate 4B)
- Overall protocol verdict: HARNESS_SPECIFIC / HARNESS_NONSPECIFIC

### 3. Write Final Report
**Manual task:**  
Create `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md` with:
- Execution summary (54/54 cases)
- Per-control results (random_hermitian, scrambled_geometry, broken_wilson_term)
- Decision rule application
- Interpretation: does harness distinguish S³×S¹ from broken controls?
- Limitations and caveats
- Next steps (if controls PASS: proceed to publication; if FAIL: investigate harness specificity)

---

## Gate 4B Protection

**CRITICAL:** Do NOT modify any Gate 4B files during remote execution.

**Protected directories:**
- `reports/RUNS/gate4_fss_v0.1.21/`
- `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md`
- `reports/GATE4B_PRE_PUSH_AUDIT_v0.1.21.md`
- `reports/CLAIMS_ALLOWED_AND_FORBIDDEN_v0.1.21.md`

**Protected commits:**
- f7eff32 (Gate 4B results)
- 0c78263 (Gate 4B closeout)

**Verification after remote work:**
```bash
git log --oneline f7eff32..HEAD | grep -i "gate.*4"
# Should return NOTHING (no commits modifying Gate 4B after closeout)

git diff f7eff32 HEAD -- reports/RUNS/gate4_fss_v0.1.21/
# Should return NOTHING (no diffs in Gate 4B results)
```

---

## Timeline Estimate

**Setup (first time):** 15–30 minutes  
**Batch 3 execution:** ~35 minutes  
**Batch 4 execution:** ~35 minutes  
**Batch 5 execution:** ~35 minutes  
**Batch 6 execution:** ~35 minutes  
**Validation + commit + push:** ~10 minutes

**Total remote session time:** ~2.5–3 hours  
**Local pull + aggregation:** ~5 minutes  
**Final report writing:** ~30–60 minutes

**End-to-end:** ~4 hours to complete negative controls protocol.

---

## Troubleshooting

### Issue: Batch fails with "No module named 'cc_toy_lab'"
**Fix:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3
```

### Issue: r_stat = 1.0 or r_stat = NaN
**Diagnosis:** Numerical issue in level spacing calculation (likely all eigenvalues identical or near-degenerate)  
**Action:** Check control constructor implementation:
```python
# For scrambled_geometry:
python -c "from cc_toy_lab.geometry.negative_controls import build_scrambled_geometry_hamiltonian; import numpy as np; H = build_scrambled_geometry_hamiltonian(16, 3, 0.0, 123, 1.0, 0.0); eigvals = np.linalg.eigvalsh(H); print(f'Eigenvalue range: {eigvals.min():.4f} to {eigvals.max():.4f}, unique: {len(np.unique(eigvals))}/{len(eigvals)}')"
```
**Expected:** Eigenvalue range should span ~10–100, unique count should equal total (no degeneracies).  
**If degenerate:** Bug in scrambled_geometry constructor, STOP and report.

### Issue: Session timeout before all batches complete
**Workaround (Colab):**
```python
# Run batches in one command to minimize interruptions
!python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3 && \
 python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 4 && \
 python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 5 && \
 python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 6
```
**Or:** Use Colab Pro (24-hour sessions).

---

## Success Criteria

✅ 54/54 cases executed (18 local + 36 remote)  
✅ All cases have complete metrics (true_ipr_mean, r_stat, runtime_seconds)  
✅ No r_stat anomalies (all values in 0.2–0.6 range)  
✅ Batches 3–6 committed and pushed to origin/main  
✅ Gate 4B files unchanged (verified via git diff)  
✅ Aggregate results generated  
✅ Decision rules applied  
✅ Final report written

**After success:** Update `reports/CURRENT_STATUS_v0.1.22_NEGATIVE_CONTROLS_PLANNING.md` to:
- Phase: COMPLETED
- Status: RESULTS_AVAILABLE
- Coverage: 54/54 (100%)

---

**Document status:** ACTIVE  
**Last updated:** 2026-05-23 22:03  
**Next action:** Choose remote infrastructure (Option A/B/C/D) and begin setup
