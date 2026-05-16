# S2 x S1 Product-Discretized Full Run Readiness

## Executive Summary

The **full** product-discretized profile is **specified** and **dry-run verified**
(`expected_case_count=6615`, no operator work). A **real** `--full` execution is
**not** enabled in the current CLI build, remains **pending**, and must only be
turned on after explicit implementation review plus the preconditions below.
This checkpoint is **documentation only** — it does not launch computation.

## Current Baseline

`v0.1.14-mvp-s2-s1-discretization-v2-full` (unchanged; no promotion from this document).

## Dry-Run Evidence

| Item | Recorded state |
| --- | --- |
| **Plan** | `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_PROFILE_PLAN.md` |
| **Command** | `python scripts/s2_s1_product_discretized.py --full --dry-run` |
| **`profile_name`** | `full` |
| **`expected_case_count`** | **6615** |
| **`grid_dimensions` (representative)** | `q_values=7`, `s1_families=3`, `s1_sizes=5`, `alpha_values=3`, `w_values=7`, `seeds=3`, `low_energy_count_values=5` (outer grid = 6615; low-energy axis is bookkeeping, not a multiplier of 6615 in the dry-run contract) |
| **`estimated_run_dir_suffix`** | `_s2_s1_product_discretized_full` |
| **Operators computed** | **No** (dry-run only) |
| **Test suite (informational)** | `pytest -q` → **187 passed** (after guarded full-runner wiring; wall clock varies) |
| **Note** | `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_DRY_RUN_NOTE.md` |

## Why Full Is Heavy

- **6615 outer cells** on the Cartesian grid `(q, family, s1_size, alpha, W, seed)`.
- **Each cell** triggers toy **spectral / eigen** work (Kronecker-sum Hamiltonian,
  Hermitian eigensolve, IPR and localization bookkeeping).
- **v3** localization logic uses **multiple** `low_energy_count` window passes per
  case (see medium / tiny schema), multiplying internal work **per outer cell**.
- A real run should be treated as a **long background job** (tens of minutes to
  hours depending on machine, power settings, and I/O), not an interactive smoke.

## Preconditions Before Enabling Real Full

1. **Stable power** and OS **sleep/hibernate disabled** for the job window (or use a server session).
2. **Enough disk space** for `config.json`, `metrics.json`, `data.npz`, `summary.md`, figures policy, and optional logs (order **GB** safer than assuming MB).
3. **No duplicate** `python ... product_discretized ... --full` processes for the same grid.
4. **Logging** to a dedicated file (stdout/stderr redirect) plus timestamped run directory under `reports/RUNS/`.
5. **Working tree** clean enough to attribute results to a known commit hash (tag or note the SHA in the run memo).
6. **Avoid concurrent** conflicting edits to validation docs while a long run is in flight (reduces merge/rebase risk on the branch that will interpret results).
7. **Repeat dry-run immediately before** the real job: `python scripts/s2_s1_product_discretized.py --full --dry-run` must still print **`expected_case_count=6615`** on the same commit.

## Recommended Command Pattern

**Do not execute the second line until `--full` is explicitly enabled in code and reviewed.**

1. **Dry-run (safe, current CLI):**

   ```powershell
   python scripts/s2_s1_product_discretized.py --full --dry-run
   ```

2. **Future real run (placeholder — not valid until CLI allows `--full` without `--dry-run`):**

   ```powershell
   python scripts/s2_s1_product_discretized.py --full > reports/RUNS/product_discretized_full_<timestamp>.log 2>&1
   ```

   Replace `<timestamp>` with an ISO-like stamp. Prefer instead writing under
   `reports/RUNS/<timestamp>_s2_s1_product_discretized_full/` once the runner
   creates that directory automatically (align with `FULL_PROFILE_PLAN.md`).

## Monitoring Plan (PowerShell)

**Find Python processes (filter by path / cwd as needed):**

```powershell
Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
  Select-Object ProcessId, CommandLine |
  Where-Object { $_.CommandLine -match 's2_s1_product_discretized' }
```

**Inspect command line for a PID:**

```powershell
(Get-CimInstance Win32_Process -Filter "ProcessId = <PID>").CommandLine
```

**List newest run directories (tail of sorted list):**

```powershell
Get-ChildItem -Path reports/RUNS -Directory |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 5 Name, LastWriteTime
```

**Wait until process exits, then verify `metrics.json` exists (example path):**

```powershell
$run = "reports/RUNS/<timestamp>_s2_s1_product_discretized_full"
while (Get-Process -Id <PID> -ErrorAction SilentlyContinue) { Start-Sleep -Seconds 30 }
Test-Path (Join-Path $run "metrics.json")
```

Do **not** treat partial `metrics.json` writes as authoritative until the writer
finishes and exit code is known.

## Failure Handling

- **Interrupted job:** record as **partial**; **do not** interpret localization
  aggregates unless the runner completed with **exit code 0** and full artifacts.
- **Duplicate run detected:** keep **one** canonical process; **terminate** extras;
  document which PID was kept.
- **PC reboot mid-run:** use only runs with **exit code 0** and **complete**
  artifact set; otherwise discard or mark **invalid**.
- **`q0_false_positive_count > 0`:** **control failure** — stop interpretation of
  localization bands until fixed (per full plan).
- **Strong-disorder failures spread across families at `W >= 8`:** classify
  **`unresolved_product_discretized_strong_disorder_limitation`** (or equivalent),
  distinct from ring-only transition story.

## Interpretation Contract

Align with `reports/S2_S1_PRODUCT_DISCRETIZED_FULL_PROFILE_PLAN.md` **Decision Rules**
and medium / W4 narrative:

1. **Transition-regime ring caveat:** if `strong_disorder_failure_count = 0` and
   residual failures concentrate in **`ring`** with **`W ∈ {2, 4}`**, treat as
   transition-regime sensitivity — **not** “all families broken.”
2. **Ring / `alpha = 0` caveat:** keep explicit bookkeeping (`ring_alpha0_*`
   counters) consistent with prior v3 stress and ring diagnostics.
3. **Unresolved strong-disorder limitation:** failures **across families** at
   **`W >= 8`** imply a broader product-discretized limitation, not just ring
   transition band.
4. **Control failure:** any **`q0`** false-positive signal halts positive
   localization interpretation.
5. **`v0.1.15` candidate:** only if full run **supports** medium / W4 smoke
   structure **and** passes control gates — **after independent audit** and
   explicit release process, **not** from a single unattended run.
6. **Contradiction with medium / W4 smoke:** require **targeted follow-up** before
   any baseline promotion discussion.

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** physical validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.

## Readiness Verdict

`ready_for_guarded_full_enablement_with_caution`

Meaning: dry-run and planning artifacts are in place; operators are **not** yet run
at full scale; enabling real `--full` remains **opt-in**, requires code change plus
the preconditions above, and must stay bounded by the interpretation contract.
