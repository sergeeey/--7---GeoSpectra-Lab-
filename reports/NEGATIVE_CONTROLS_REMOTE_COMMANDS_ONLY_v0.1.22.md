# Negative Controls Remote Execution — Commands Only

**Purpose:** Quick command reference for remote batch execution  
**Target:** Batches 3–6 (36 cases)  
**Prerequisites:** Linux server, 8+ vCPU, 32+ GB RAM, Python 3.10+

---

## Setup

```bash
# Clone
git clone https://github.com/sergeeey/N-7-GeoSpectra-Lab.git
cd N-7-GeoSpectra-Lab
git checkout main
git pull origin main
git log --oneline -5

# Verify latest commit
# Expected: 32d8298 docs(controls): suspend local execution due to thermal instability

# Python env
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install numpy scipy pytest matplotlib

# Verify
python -c "import numpy, scipy; print('OK')"
```

---

## Pre-flight Tests

```bash
# Run validation tests
pytest tests/test_ipr_metric.py -v
pytest tests/test_negative_controls_grid_v0_1_22.py -v
pytest tests/test_negative_controls_no_gate4b_mutation.py -v

# All tests MUST pass. If any FAILED → STOP, report to Sergey.

# Print plan
python scripts/run_negative_controls_v0_1_22.py --print-plan
```

---

## Environment

```bash
# Set thread limits
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
export OPENBLAS_NUM_THREADS=8
export NUMEXPR_NUM_THREADS=8

# If <8 cores available: use 4
# If 16+ cores available: can use 16
```

---

## Execute Batches

```bash
# Batch 3: scrambled_geometry, W=0 (~30 min)
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3

# Batch 4: scrambled_geometry, W=20 (~30 min)
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 4

# Batch 5: broken_wilson_term, W=0 (~30 min)
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 5

# Batch 6: broken_wilson_term, W=20 (~30 min)
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 6
```

**Alternative: Chain all batches**
```bash
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 3 && \
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 4 && \
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 5 && \
python scripts/run_negative_controls_v0_1_22.py --run-pilot --batch-id 6
```

---

## Validation

```bash
# Check total cases
find reports/RUNS/negative_controls_v0.1.22 -name "case_*.json" | wc -l
# Expected: 54

# Check batch structure
ls reports/RUNS/negative_controls_v0.1.22/
# Expected: batch_01, batch_02, batch_03, batch_04, batch_05, batch_06, config.json

# Spot-check batch 3 first case
python -c "
import json
with open('reports/RUNS/negative_controls_v0.1.22/batch_03/case_018.json') as f:
    data = json.load(f)
print(f\"r_stat: {data['r_stat']:.4f}, ipr: {data['true_ipr_mean']:.6f}\")
"
# Expected r_stat: 0.35–0.55 (NOT 1.0, NOT 0.0)
```

---

## Commit & Push (If Git Access)

```bash
git status --short

git add -f reports/RUNS/negative_controls_v0.1.22/batch_03/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_04/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_05/
git add -f reports/RUNS/negative_controls_v0.1.22/batch_06/

git commit -m "test(controls): complete batches 3-6 negative controls (remote execution)"

git push origin main

# Verify
git log --oneline -3
```

---

## Archive (If No Git Access)

```bash
# Create archive
tar -czf negative_controls_v0.1.22_remote_outputs.tar.gz \
  reports/RUNS/negative_controls_v0.1.22/batch_03 \
  reports/RUNS/negative_controls_v0.1.22/batch_04 \
  reports/RUNS/negative_controls_v0.1.22/batch_05 \
  reports/RUNS/negative_controls_v0.1.22/batch_06

# Or zip
zip -r negative_controls_v0.1.22_remote_outputs.zip \
  reports/RUNS/negative_controls_v0.1.22/batch_03 \
  reports/RUNS/negative_controls_v0.1.22/batch_04 \
  reports/RUNS/negative_controls_v0.1.22/batch_05 \
  reports/RUNS/negative_controls_v0.1.22/batch_06

# Send to: sergeikuch80@gmail.com
```

---

## Forbidden

❌ Do NOT modify: `reports/RUNS/gate4_fss_v0.1.21/`  
❌ Do NOT edit: `scripts/run_negative_controls_v0_1_22.py`  
❌ Do NOT delete: `batch_01`, `batch_02`  
❌ Do NOT make scientific claims

---

## Contact

**If errors occur:** sergeikuch80@gmail.com  
**Subject:** "Negative controls remote execution — error at [step]"

---

## Success Criteria

✅ 54 total case files  
✅ All r_stat values in 0.2–0.6 range  
✅ No test failures  
✅ Outputs pushed OR archived and sent  
✅ Gate 4B unchanged
