# S2 x S1 Product-Discretized Full Runbook

## Purpose

This document is a **concise operational checklist** for launching the **guarded**
real **full** product-discretized diagnostic (`6615` outer cases). It does **not**
replace the planning contract (`reports/S2_S1_PRODUCT_DISCRETIZED_FULL_PROFILE_PLAN.md`)
or the interpretation rules there; it sequences **human and shell steps** so a
long job is not started accidentally, duplicated, or misread mid-flight.

**Baseline (informational):** `v0.1.14-mvp-s2-s1-discretization-v2-full` — unchanged
unless a separate review explicitly promotes it.

## Preconditions

- **Power:** laptop on AC where applicable; avoid battery-only for multi-hour jobs.
- **Sleep / hibernate:** disabled for the session (or run on a host that will not sleep).
- **Disk:** enough free space for `config.json`, `metrics.json`, `data.npz`,
  `summary.md`, figures, and an optional multi-MB log (plan for **GB** headroom).
- **No duplicate Python runs:** before launch, confirm no other
  `s2_s1_product_discretized.py --full --confirm-full-run` is already active.
- **Branch / worktree:** acceptable to attribute results to the current commit
  (note SHA in your operator memo).
- **Latest `pytest` status recorded:** informational full suite
  **`pytest -q` → 187 passed** (as of guarded-runner wiring); re-run if the repo
  changed materially since last record (`reports/VALIDATION_STATUS.md`).
- **Dry-run repeated immediately before launch** (same commit, same environment):

  ```powershell
  python scripts/s2_s1_product_discretized.py --full --dry-run
  ```

  Confirm **`expected_case_count=6615`** and **`profile_name=full`** in stdout.

## Commands

**1. Dry-run (mandatory gate immediately before real run):**

```powershell
python scripts/s2_s1_product_discretized.py --full --dry-run
```

**2. Real guarded full (long job — optional stdout/stderr log redirect):**

```powershell
python scripts/s2_s1_product_discretized.py --full --confirm-full-run > reports/RUNS/product_discretized_full_<timestamp>.log 2>&1
```

Replace `<timestamp>` with a sortable stamp (e.g. `20260514-200000`). The script
also prints `run_path=...` pointing to the canonical artifact directory:

`reports/RUNS/<timestamp>_s2_s1_product_discretized_full/`

(If `CC_TOY_LAB_RUNS_ROOT` / `CC_TOY_LAB_FIXED_TIMESTAMP` are set, behavior follows
those environment variables — document any override in your operator memo.)

**Rejected (do not use for real work):**

```powershell
python scripts/s2_s1_product_discretized.py --full
```

(exit code **2** — bare `--full` is disabled.)

## Monitoring (PowerShell)

**List Python processes (filter by script name):**

```powershell
Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
  Select-Object ProcessId, CommandLine |
  Where-Object { $_.CommandLine -match 's2_s1_product_discretized' }
```

**Inspect full command line for a PID:**

```powershell
(Get-CimInstance Win32_Process -Filter "ProcessId = <PID>").CommandLine
```

**List newest `reports/RUNS` directories:**

```powershell
Get-ChildItem -Path reports/RUNS -Directory |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 8 Name, LastWriteTime
```

**After the process exits — check `metrics.json` exists (example):**

```powershell
$run = "reports/RUNS/<timestamp>_s2_s1_product_discretized_full"
Test-Path (Join-Path $run "metrics.json")
```

**Reminder:** do **not** treat partial `metrics.json` or truncated logs as the
final scientific record until the process has **exited**, **`s2_s1_product_discretized_full complete`**
(or equivalent) appears in stdout/log, and artifact set is complete.

## Duplicate Handling

If **two** full processes are running:

1. **Identify** both PIDs and **full command lines** (see Monitoring).
2. **Stop** the **newer duplicate** or the run that has **not** yet created a stable
   `run_path` / is clearly the mistaken second launch.
3. Keep **one** authoritative run directory; rename or quarantine the abandoned
   partial directory with a `_aborted` suffix in your notes (do not delete silently
   until you are sure nothing worth keeping).

## Reboot / Interruption Handling

- If the **PC reboots** or the job is **killed**: mark the run **interrupted** in
  your operator log.
- **Do not** use **partial** `metrics.json` / `data.npz` as a final result.
- **Trust** only a run that **completed** with a coherent artifact set:
  `config.json`, `metrics.json`, `data.npz`, `summary.md`, `figures/.placeholder`,
  plus **exit code 0** from the Python process and a clear completion line in the log.

## Artifact Verification

After completion, verify under
`reports/RUNS/<timestamp>_s2_s1_product_discretized_full/`:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/.placeholder`
- Optional: companion **`product_discretized_full_<timestamp>.log`** if you used shell redirect

## Post-Run Extraction

From `metrics.json` / `summary.md` (and operator notes), extract at least:

- **`classification`**
- **`case_count`** (expect **6615** outer cases) vs dry-run expectation
- **`clean_control_cases_count`** / **`disordered_cases_count`**
- **`q0_false_positive_count`**
- **`transition_band_failure_count`** (if present in metrics or derivable from case rows / plan buckets)
- **`strong_disorder_failure_count`** (same)
- **`ring_alpha0_cases_count`** / **`ring_alpha0_failure_count`**
- **`v2_vs_v3_disagreement_count`**
- **`v3_failure_counts_by_bucket`** (or equivalent stratification by family / W /
  alpha / `s1_size` / q / seed)

If some bucket fields are not yet top-level keys in `metrics.json`, derive them
from per-case rows **before** writing a milestone — do not invent aggregates.

## Interpretation Rules

(Aligned with `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_PROFILE_PLAN.md`.)

- **`q0_false_positive_count > 0`:** **control failure** — stop positive localization
  interpretation until resolved.
- **Strong-disorder failures spread across families at `W >= 8`:** classify as
  **`unresolved_product_discretized_strong_disorder_limitation`** (or equivalent wording).
- **Failures only in `ring` with `W ∈ {2, 4}`** while strong-disorder is clean:
  **transition-regime ring caveat** (consistent with medium / W4 smoke narrative).
- **Full run supports medium / W4 smoke structure** with no new control failure:
  **`v0.1.15` bookkeeping candidate only after independent audit** and explicit
  release process — not from a single unattended run.

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** physical validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.

## Final Checklist

- [ ] **Run path** recorded (`run_path=...` from stdout/log).
- [ ] **Completion status** confirmed (process exit **0**, completion line, full artifacts).
- [ ] **Optional:** run `pytest -q` after any **post-run documentation** edits; keep
  validation docs consistent with the new run memo.
- [ ] **Baseline** remains **`v0.1.14-mvp-s2-s1-discretization-v2-full`** unless a
  separate reviewed promotion says otherwise.
