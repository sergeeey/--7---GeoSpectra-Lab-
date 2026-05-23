# Negative Controls Server Handoff — v0.1.22

**Purpose:** Execute remaining negative controls batches 3–6 on remote/cloud infrastructure  
**Reason:** Local PC thermal instability prevents further heavy numerical execution  
**Target:** Complete 36 remaining cases (54 total, 18 already done)

---

## 1. Purpose

**What needs to be done:**  
Execute negative controls batches 3–6 (scrambled_geometry and broken_wilson_term with W=0 and W=20) on a remote server or cloud VM, because local PC overheats and reboots during eigenvalue decomposition.

**What this is:**  
Falsification test for GeoSpectra harness specificity. Negative controls should FAIL to reproduce Gate 4B PASS pattern. This is a validation layer, NOT a new physics claim.

**Why remote:**  
Local thermal constraint blocks sustained heavy numerical workloads (full eigendecomposition on N=13824 Hermitian matrices across parameter grid).

---

## 2. Current State

**Repository:**  
https://github.com/sergeeey/N-7-GeoSpectra-Lab

**Latest commit:**  
32d8298 — docs(controls): suspend local execution due to thermal instability

**Branch:**  
main (synced with origin/main)

**Completed batches (already pushed to origin/main):**

| Batch | Control | W | Cases | Status | Commit |
|-------|---------|---|-------|--------|--------|
| 1 | random_hermitian | 0 | 9/9 | ✅ COMPLETED | fdda5bb |
| 2 | random_hermitian | 20 | 9/9 | ✅ COMPLETED | 2ec84ab |

**Coverage:** 18/54 cases (33.3%)

**Remaining batches (to execute remotely):**

| Batch | Control | W | Cases | Status |
|-------|---------|---|-------|--------|
| 3 | scrambled_geometry | 0 | 9 | ⏸️ NOT STARTED |
| 4 | scrambled_geometry | 20 | 9 | ⏸️ NOT STARTED |
| 5 | broken_wilson_term | 0 | 9 | ⏸️ NOT STARTED |
| 6 | broken_wilson_term | 20 | 9 | ⏸️ NOT STARTED |

**Target coverage after remote run:** 54/54 cases (100%)

**Critical constraint:**  
Gate 4B outputs must NOT be modified. Gate 4B is closed (commit f7eff32, verdict PASS_WITH_CAVEATS). v0.1.22 negative controls are independent validation layer.

---

## 3. Server Requirements

### Minimum Specification

**OS:** Linux Ubuntu 22.04 / 24.04 preferred (Debian, RHEL, CentOS also work)  
**vCPU:** 8 cores minimum, 16+ cores preferred  
**RAM:** 32 GB minimum, 64 GB preferred  
**Disk:** 20–50 GB (mostly for dependencies and outputs)  
**Python:** 3.10, 3.11, or 3.12  
**Git:** 2.x  
**Network:** SSH access, GitHub clone access (public repo)

**NOT required:**  
- GPU (all computation CPU-only)
- CUDA / ROCm
- Docker (optional but not needed)

### Recommended Cloud Options

- **Google Colab Pro:** $10/month, 24-hour sessions, fast setup
- **AWS EC2:** t3.2xlarge (8 vCPU, 32 GB), ~$0.33/hour, ~$10 for full run
- **Azure VM:** Standard_D8s_v3 (8 vCPU, 32 GB), similar cost
- **University cluster:** Free if available, may have queue wait time

**Expected runtime:** 3–4 hours for all 4 batches (depends on CPU performance)

---

## 4. Access Models

### Model A: Server Has GitHub Push Access

**Workflow:**
1. Clone repo
2. Run batches 3–6
3. Commit outputs directly to repo
4. Push to origin/main

**Pros:** Cleanest workflow, outputs immediately available in repo  
**Cons:** Requires GitHub credentials (SSH key or token)

**When to use:** If operator has GitHub account with push access, or can set up SSH key.

---

### Model B: Server Has No Push Access

**Workflow:**
1. Clone public repo (read-only)
2. Run batches 3–6
3. Create archive of outputs
4. Send archive back to Sergey via email / cloud storage

**Pros:** No GitHub credentials needed  
**Cons:** Manual transfer step, Sergey must commit outputs locally

**When to use:** If operator has no GitHub account, or server is temporary/ephemeral.

---

### Model C: Relative Runs Locally (Different PC)

**Workflow:**
1. Clone repo on relative's PC (not Sergey's overheating PC)
2. Run batches 3–6
3. Send outputs back (git push if has access, or archive)

**Pros:** No cloud cost  
**Cons:** Requires access to another PC with sufficient cooling

**When to use:** If Sergey has access to family/friend PC with better thermal management.

---

## 5. Setup Commands — Linux

### Clone Repository

```bash
git clone https://github.com/sergeeey/N-7-GeoSpectra-Lab.git
cd N-7-GeoSpectra-Lab
git checkout main
git pull origin main
git log --oneline -5
```

**Expected output:**  
Latest commit should be 32d8298 (thermal suspension docs).

### Create Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Install Dependencies

**If `requirements.txt` exists:**
```bash
pip install -r requirements.txt
```

**If `requirements.txt` does NOT exist:**
```bash
pip install numpy scipy pytest matplotlib
```

**Verify installation:**
```bash
python -c "import numpy as np; import scipy; print(f'NumPy {np.__version__}, SciPy {scipy.__version__}')"
```

**Expected output:**  
NumPy 1.24+, SciPy 1.11+

### Run Tests (Critical Validation)

```bash
pytest tests/test_ipr_metric.py -v
pytest tests/test_negative_controls_grid_v0_1_22.py -v
pytest tests/test_negative_controls_no_gate4b_mutation.py -v
```

**All tests MUST pass.** If any test fails → STOP, report issue to Sergey.

### Print Execution Plan

```bash
python scripts/run_negative_controls_v0_1_22.py --print-plan
```

**Expected output:**  
Grid summary showing 54 total cases, batches 1–2 completed, batches 3–6 pending.

---

## 6. Environment Variables

**For stable numerical execution, set:**

```bash
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
export OPENBLAS_NUM_THREADS=8
export NUMEXPR_NUM_THREADS=8
```

**If server has fewer than 8 cores:**  
Use `4` instead of `8`.

**If server has 16+ cores:**  
Can use `16`, but `8` is sufficient and more stable.

**Why:** Prevents thread oversubscription and numerical instability in BLAS/LAPACK operations.

---

## 7. Execution Commands

### Batch 3: scrambled_geometry, W=0

```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3
```

**Expected runtime:** ~30–40 minutes  
**Expected output:** 9 files in `reports/RUNS/negative_controls_v0.1.22/batch_03/`

**After batch 3 completes, validate:**

```bash
ls reports/RUNS/negative_controls_v0.1.22/batch_03/case_*.json | wc -l
# Should return: 9

# Spot-check first case
python -c "
import json
with open('reports/RUNS/negative_controls_v0.1.22/batch_03/case_018.json') as f:
    data = json.load(f)
print(f\"r_stat: {data['r_stat']:.4f}, ipr: {data['true_ipr_mean']:.6f}\")
"
```

**Expected r_stat range:** 0.35–0.55 (GOE or Poisson regime, NOT 1.0)  
**If r_stat > 0.95 or r_stat < 0.2:** STOP, report issue to Sergey (numerical artifact).

---

### Batch 4: scrambled_geometry, W=20

```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 4
```

**Expected runtime:** ~30–40 minutes  
**Expected output:** 9 files in `batch_04/` (case_027.json ... case_035.json)

---

### Batch 5: broken_wilson_term, W=0

```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 5
```

**Expected runtime:** ~30–40 minutes  
**Expected output:** 9 files in `batch_05/` (case_036.json ... case_044.json)

---

### Batch 6: broken_wilson_term, W=20

```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 6
```

**Expected runtime:** ~30–40 minutes  
**Expected output:** 9 files in `batch_06/` (case_045.json ... case_053.json)

---

## 8. Output Expected

**After all 4 batches complete:**

```bash
find reports/RUNS/negative_controls_v0.1.22 -name "case_*.json" | wc -l
# Should return: 54
```

**Directory structure:**

```
reports/RUNS/negative_controls_v0.1.22/
├── batch_01/  (9 cases, already committed)
├── batch_02/  (9 cases, already committed)
├── batch_03/  (9 cases, NEW from remote)
├── batch_04/  (9 cases, NEW from remote)
├── batch_05/  (9 cases, NEW from remote)
├── batch_06/  (9 cases, NEW from remote)
└── config.json
```

**Each case JSON must contain:**
- `control`: control type (scrambled_geometry or broken_wilson_term)
- `disorder_strength`: 0 or 20
- `s1_size`: 16, 64, or 128
- `seed`: 123, 456, or 789
- `true_ipr_mean`: float (localization metric)
- `r_stat`: float (level spacing ratio)
- `runtime_seconds`: float
- `uses_eigenvectors`: true
- `ipr_metric_version`: "v0.1.22_negative_controls_true_ipr"

---

## 9. Commit Commands (If Server Has Git Access)

**After all 4 batches complete, commit outputs:**

```bash
git status --short
# Should show new files in batch_03, batch_04, batch_05, batch_06

git add -f reports/RUNS/negative_controls_v0.1.22/batch_03/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_04/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_05/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_06/

# Optional: update progress document if modified
git add reports/NEGATIVE_CONTROLS_PILOT_PROGRESS_v0.1.22.md

git commit -m "test(controls): complete batches 3-6 negative controls (remote execution)"

git push origin main
```

**Verify push succeeded:**

```bash
git log --oneline -3
# Should show new commit on top of 32d8298
```

**Notify Sergey:** Send message that batches 3–6 are pushed to origin/main.

---

## 10. Archive Commands (If Server Has No Git Access)

**Create archive of outputs:**

### Option A: tar.gz (preferred on Linux)

```bash
tar -czf negative_controls_v0.1.22_remote_outputs.tar.gz \
  reports/RUNS/negative_controls_v0.1.22/batch_03 \
  reports/RUNS/negative_controls_v0.1.22/batch_04 \
  reports/RUNS/negative_controls_v0.1.22/batch_05 \
  reports/RUNS/negative_controls_v0.1.22/batch_06 \
  reports/NEGATIVE_CONTROLS_PILOT_PROGRESS_v0.1.22.md
```

### Option B: zip (if tar not available)

```bash
zip -r negative_controls_v0.1.22_remote_outputs.zip \
  reports/RUNS/negative_controls_v0.1.22/batch_03 \
  reports/RUNS/negative_controls_v0.1.22/batch_04 \
  reports/RUNS/negative_controls_v0.1.22/batch_05 \
  reports/RUNS/negative_controls_v0.1.22/batch_06 \
  reports/NEGATIVE_CONTROLS_PILOT_PROGRESS_v0.1.22.md
```

**Transfer archive to Sergey:**  
- Email (if < 25 MB)
- Google Drive / Dropbox link
- Cloud storage (AWS S3, Azure Blob)
- SCP / rsync to Sergey's local PC

**Sergey will:**  
Extract archive locally, commit outputs, push to origin/main.

---

## 11. Forbidden Actions

**DO NOT:**

❌ **Modify Gate 4B outputs**  
  Files: `reports/RUNS/gate4_fss_v0.1.21/`, `reports/S3_S1_GATE4B_FSS_RESULTS_v0.1.21.md`  
  Reason: Gate 4B is closed and immutable. Any modification breaks protocol integrity.

❌ **Edit protocol or thresholds**  
  Files: `reports/S3_S1_NEGATIVE_CONTROLS_PREREGISTRATION_v0.1.22.md`, `scripts/run_negative_controls_v0_1_22.py`  
  Reason: Protocol is pre-registered. Changes invalidate falsification test.

❌ **Change scripts without Sergey's approval**  
  Reason: Even "bug fixes" can introduce bias. Report issues, do not patch.

❌ **Make scientific verdict**  
  Example: "Controls passed", "harness is specific", "validation successful"  
  Reason: Decision rules and aggregation happen AFTER all 54 cases collected.

❌ **Delete batches 1–2**  
  Reason: Already committed and pushed. Deletion breaks coverage.

❌ **Claim novelty or physics interpretation**  
  Forbidden terms: "new physics", "Standard Model", "compactification", "thermodynamic limit"  
  Reason: This is a validation test, not a discovery claim.

**IF IN DOUBT:** Ask Sergey before proceeding.

---

## 12. After Remote Execution

**Sergey will perform locally (DO NOT do on server):**

1. **Verify coverage:**
   ```bash
   find reports/RUNS/negative_controls_v0.1.22 -name "case_*.json" | wc -l
   # Must return: 54
   ```

2. **Aggregate results:**
   ```bash
   python scripts/aggregate_negative_controls_results.py
   ```

3. **Apply decision rules:**
   ```bash
   python scripts/apply_negative_controls_decision_rules.py
   ```

4. **Write final report:**  
   `reports/S3_S1_NEGATIVE_CONTROLS_RESULTS_v0.1.22.md`

5. **Scientific verdict:**  
   Only after aggregation and decision rules: HARNESS_SPECIFIC or HARNESS_NONSPECIFIC.

**Operator's job ends when:**  
- All 54 cases executed (18 local + 36 remote)
- Outputs committed to repo OR archive sent back to Sergey
- No errors reported

---

## 13. Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'cc_toy_lab'`

**Fix:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3
```

---

### Issue: `r_stat = 1.0` or `r_stat = NaN`

**Diagnosis:** Numerical issue in level spacing calculation (eigenvalues degenerate or near-identical).

**Action:**
1. Check eigenvalue distribution:
   ```python
   from cc_toy_lab.geometry.negative_controls import build_scrambled_geometry_hamiltonian
   import numpy as np
   H = build_scrambled_geometry_hamiltonian(16, 3, 0.0, 123, 1.0, 0.0)
   eigvals = np.linalg.eigvalsh(H)
   print(f"Eigenvalue range: {eigvals.min():.4f} to {eigvals.max():.4f}")
   print(f"Unique eigenvalues: {len(np.unique(eigvals))}/{len(eigvals)}")
   ```

2. **If degenerate (unique count << total):** Bug in control constructor. STOP and report to Sergey.

3. **If normal distribution but r_stat still 1.0:** Numerical precision issue. Try different seed or report.

---

### Issue: Session timeout (Colab / cloud)

**Workaround:** Chain all batches in one command to minimize interruptions:

```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3 && \
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 4 && \
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 5 && \
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 6
```

**Or:** Use Colab Pro (24-hour sessions) or persistent VM.

---

### Issue: Test failures during setup

**If `test_negative_controls_grid_v0_1_22.py` fails:**  
Grid definition mismatch. Pull latest commit and retry.

**If `test_negative_controls_no_gate4b_mutation.py` fails:**  
Gate 4B outputs were modified. DO NOT PROCEED. Report to Sergey immediately.

---

## 14. Contact

**Operator should contact Sergey if:**

- Any test fails during setup
- Batch execution produces errors
- r_stat values outside 0.2–0.6 range
- Unexpected file structure
- Unsure whether to proceed

**Sergey's email:** sergeikuch80@gmail.com

**Do NOT:**  
- Proceed with execution if tests fail
- Modify code to "fix" errors
- Make assumptions about protocol

---

## 15. Success Criteria

✅ All 4 batches executed (36 cases)  
✅ Total coverage: 54/54 cases (18 local + 36 remote)  
✅ All cases have required metrics (true_ipr_mean, r_stat, runtime_seconds)  
✅ No r_stat anomalies (all values in 0.2–0.6 range)  
✅ Outputs committed to origin/main OR archive sent to Sergey  
✅ Gate 4B files unchanged (verified via `git status`)  
✅ No protocol modifications  
✅ No scientific verdict made by operator

**When all criteria met:** Remote execution phase complete. Sergey proceeds to aggregation and analysis.

---

**Document status:** ACTIVE  
**Last updated:** 2026-05-23  
**Next action:** Choose access model (A/B/C), set up server, begin batch 3 execution
