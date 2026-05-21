# Gate 4 Pre-Run Thermal & Environment Checklist — v0.1.20

**Дата:** 2026-05-21  
**Статус:** EXECUTION ENVIRONMENT SAFETY PROTOCOL  
**Цель:** Ensure stable execution environment for full Gate 4 (NOT a scientific validity check)

---

## 1. Purpose

This checklist ensures execution environment stability and reproducibility context. It is **NOT** a scientific validity check or physics evidence.

**What this checks:**
- Thermal stability under sustained load
- Power management configuration
- System resource availability
- Execution environment reproducibility

**What this does NOT check:**
- Numerical stability of Gate 4 results (that's in the protocol)
- Physics validity of IPR or r-statistic (that's in the pre-registration)
- Scientific correctness of the experiment (that's locked in commit 1f4173c)

**Relationship to dry-run (commit 52d221f):**
- Dry-run completed without BSOD under current cooling profile
- Thermal stability appears improved (context: prior BSOD issues during development)
- Full Gate 4 requires same thermal environment for reproducibility

---

## 2. Thermal Configuration Checklist

### 2.1 MSI Center Cooling Profile
- [ ] MSI Center application installed and running
- [ ] Cooling profile set to **Extreme Performance** OR **Cooler Boost** OR **Advanced**
- [ ] Profile saved (not temporary setting)
- [ ] Fan speed override active (if using Advanced profile)
- [ ] Verify profile persists after reboot (if system was restarted)

**How to verify:**
1. Open MSI Center
2. Navigate to "Features" → "User Scenario"
3. Check that active profile shows "Extreme Performance" or custom profile
4. Fan speeds should show elevated RPM (not default/silent mode)

### 2.2 System Temperature Baseline
- [ ] System idle temperature acceptable (CPU < 50°C, GPU < 45°C)
- [ ] Monitor sensors available (HWiNFO64, MSI Center, or equivalent)
- [ ] No thermal throttling warnings in Event Viewer
- [ ] Check recent temperature history (last 24h) for anomalies

**How to check:**
```bash
# Windows Event Viewer
eventvwr.msc → Windows Logs → System → Filter: "thermal" OR "temperature"

# Or use HWiNFO64 sensors
# Look for: CPU Package, GPU Temperature, VRM temperatures
```

**Acceptable temperature ranges (under load):**
- CPU: < 85°C sustained
- GPU: < 80°C sustained
- VRM/chipset: < 95°C

**If temperatures exceed limits:** Clean dust filters, verify thermal paste, check case airflow

---

## 3. Power Management Checklist

### 3.1 Power Supply
- [ ] Power adapter plugged in (NOT running on battery)
- [ ] Power plan set to "High Performance" (not Balanced or Power Saver)
- [ ] Battery charge > 50% (backup if AC disconnects)
- [ ] Verify AC adapter wattage sufficient (check laptop specs)

**How to set High Performance:**
```bash
# Windows PowerShell (as Admin)
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

### 3.2 Sleep/Hibernation
- [ ] Sleep disabled during execution (minimum 3 hours)
- [ ] Hibernation disabled
- [ ] Screen timeout set to "Never" (or > 3 hours)
- [ ] Hard disk timeout disabled

**How to disable sleep:**
```bash
# PowerShell (as Admin)
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change monitor-timeout-ac 0
powercfg /change disk-timeout-ac 0
```

**Revert after Gate 4 completes:**
```bash
# Restore default timeouts (example: 30 min sleep)
powercfg /change standby-timeout-ac 30
```

---

## 4. System Resource Checklist

### 4.1 Close Heavy Applications
- [ ] Close browsers (Chrome, Firefox, Edge) with many tabs
- [ ] Close video/streaming applications
- [ ] Close other Python/Jupyter sessions
- [ ] Close IDEs (if not monitoring Gate 4 execution)
- [ ] Close games, rendering software, VMs

**Why:** Reduce CPU/GPU load competition, minimize thermal stress

### 4.2 Check Available Resources
- [ ] RAM usage < 60% (leave headroom for Gate 4)
- [ ] CPU usage < 20% idle (no background tasks hogging cycles)
- [ ] Disk I/O not saturated (no Windows Update or antivirus scan running)
- [ ] GPU available (if using GPU for matrix operations)

**How to check:**
```bash
# Task Manager: Ctrl+Shift+Esc
# Check: Performance tab → CPU, Memory, Disk
```

**If RAM > 60% idle:** Restart system before Gate 4

### 4.3 Disable Automatic Updates
- [ ] Windows Update set to manual (or scheduled outside Gate 4 window)
- [ ] Antivirus real-time scanning paused (if safe to do so)
- [ ] No scheduled tasks during Gate 4 execution window

**How to check scheduled tasks:**
```bash
# Task Scheduler: taskschd.msc
# Review: Task Scheduler Library → check for tasks in next 3 hours
```

---

## 5. Git and Code Environment Checklist

### 5.1 Repository State
- [ ] Git status clean (no uncommitted changes)
- [ ] Current branch: `main`
- [ ] Synchronized with origin/main (no unpushed commits)
- [ ] Pre-registration commit 1f4173c accessible

**How to verify:**
```bash
cd E:\Проверка\ Гипотез\работаю\ над\ проверкой\ гипотез\N-7-GeoSpectra-Lab
git status --short  # Should be empty
git log --oneline -5  # Should include 1f4173c or newer
git branch -vv  # Should show [origin/main] synchronized
```

### 5.2 Python Environment
- [ ] Correct Python environment activated (if using venv/conda)
- [ ] All dependencies installed (`pip list` or `conda list`)
- [ ] No version conflicts (`pip check`)

**How to verify:**
```bash
python --version  # Check Python version (expected: 3.10+)
python -c "import cc_toy_lab; print(cc_toy_lab.__file__)"  # Check package importable
python -c "import numpy, scipy; print('OK')"  # Check core dependencies
```

---

## 6. Pre-Run Validation

### 6.1 Dry-Run Results Review
- [ ] Dry-run results accessible (commit 52d221f)
- [ ] Dry-run verdict: BATCHED_GRID_REQUIRED ✅
- [ ] Estimated runtime: 2.4h (acceptable)
- [ ] Zero failures in dry-run (36/36 cases passed)

**How to verify:**
```bash
cat reports/S3_S1_GATE4_DRY_RUN_RESULTS_v0.1.20.md | grep "BATCHED_GRID_REQUIRED"
cat reports/RUNS/gate4_dry_run_v0.1.20/summary.md
```

### 6.2 Test Print Plan
- [ ] Run `--print-plan` to verify batch split
- [ ] Verify: 216 total cases
- [ ] Verify: 9 batches × 24 cases
- [ ] Verify: Coverage check PASSED (no gaps, no duplicates)

**Command:**
```bash
python scripts/run_gate4_batched.py --print-plan
```

**Expected output:**
```
Total cases: 216
Total batches: 9
Cases per batch: 24
...
✅ Coverage check PASSED: all 216 cases covered exactly once
```

**If coverage check FAILS:** DO NOT proceed, debug batch split logic

---

## 7. Execution Timeline

**Start time:** ___________ (record when starting)

**Estimated completion:** Start time + 2.4h (sequential batches)

**Intermediate checkpoints:**
- After batch 3 (~48 min): Check `batches/batch_03/status.json`
- After batch 6 (~96 min): Check `batches/batch_06/status.json`
- After batch 9 (~144 min): Verify all batches complete

**If BSOD/interruption occurs:**
1. Record time and batch number
2. Check Event Viewer for thermal/hardware errors
3. Verify cooling profile still active (may reset after BSOD)
4. Use `--resume` to continue from last incomplete batch

**Resume command:**
```bash
python scripts/run_gate4_batched.py --resume
```

---

## 8. Post-Execution Verification

### 8.1 Check All Batches Complete
- [ ] All 9 batches have `status.json` with `status: "completed"`
- [ ] No `"completed_with_failures"` status
- [ ] r-statistic available for all cases (or documented exceptions)

**How to check:**
```bash
# Check status of all batches
for i in {1..9}; do
    echo "Batch $i:"
    cat reports/RUNS/gate4_fss_v0.1.20/batches/batch_$(printf "%02d" $i)/status.json | grep "status"
done
```

### 8.2 Revert Power Settings (Post-Execution)
- [ ] Re-enable sleep timeout
- [ ] Re-enable hibernation (if desired)
- [ ] Restore screen timeout
- [ ] Re-enable Windows Update

---

## 9. Forbidden Interpretations (Critical)

**This checklist is execution context, NOT physics evidence.**

### ❌ Forbidden statements:
- "Thermal fix proves numerical stability"
- "BSOD root cause definitely solved"
- "Dry-run proves Gate 4 will pass"
- "Cooling profile validates physics results"

### ✅ Allowed statements:
- "Thermal checklist completed, proceeding with batch execution"
- "Thermal stability appears improved under dry-run load (execution context)"
- "Pre-run environment checks passed"
- "System configured for 2.4h sustained execution"

**Thermal stability ≠ scientific validity.**  
**Execution environment ≠ physics correctness.**

Gate 4 scientific verdict depends ONLY on:
1. Protocol compliance (commit 1f4173c)
2. Decision Rule 1 (2.0× IPR contrast + r toward Poisson)
3. All 216 cases completing successfully
4. Forbidden claims NOT made

---

## 10. Checklist Sign-Off

**Date:** ___________  
**Time:** ___________  
**User:** ___________

**Checklist status:**
- [ ] All thermal checks PASSED
- [ ] All power management checks PASSED
- [ ] All resource checks PASSED
- [ ] Git status clean
- [ ] --print-plan PASSED
- [ ] Ready to proceed with Gate 4 execution

**If any check FAILED:** DO NOT proceed until resolved.

**Execution command (after all checks PASSED):**
```bash
# Sequential execution (recommended)
python scripts/run_gate4_batched.py --run-all

# Or batch-by-batch (manual control)
python scripts/run_gate4_batched.py --batch-id 1
python scripts/run_gate4_batched.py --batch-id 2
# ... etc
```

---

**Document created:** 2026-05-21  
**Next action:** Complete this checklist before starting Gate 4 execution  
**Do NOT skip checklist** — thermal interruption = wasted 2.4h + incomplete results
