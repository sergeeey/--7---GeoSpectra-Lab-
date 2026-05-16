# S2 x S1 Product-Discretized Full Guarded Runner Note

## Summary

The **real** full-profile runner is now **implemented and guarded**: execution requires
**`--full --confirm-full-run`**. A **canonical** `6615`-case grid run was **not**
executed while authoring this note; only **dry-run**, **unit tests**, and a
**monkeypatched** CLI smoke path were used to validate wiring.

## Commands

**Dry-run (no operators, safe):**

```powershell
python scripts/s2_s1_product_discretized.py --full --dry-run
```

**Guarded real full (long job — do not run casually):**

```powershell
python scripts/s2_s1_product_discretized.py --full --confirm-full-run
```

**Rejected (exit code 2 — accidental full):**

```powershell
python scripts/s2_s1_product_discretized.py --full
```

**Rejected (exit code 2 — ambiguous flags):**

```powershell
python scripts/s2_s1_product_discretized.py --full --dry-run --confirm-full-run
```

**`--confirm-full-run` without `--full`:** rejected (exit code 2).

## Safety Contract

- **No accidental `--full`:** bare `--full` exits **2** with an explicit message; only
  **`--dry-run`** or **`--confirm-full-run`** may accompany **`--full`**.
- **`expected_case_count` check:** both CLI and `run_product_discretized_full` require
  **`6615`** before the heavy grid loop; mismatch **aborts** with a clear error.
- **`profile_name` check:** runner requires **`profile_name == "full"`**.
- **Long-run warning:** stderr prints *“This is a long full-profile run; do not start duplicates.”*
  immediately before computation when **`--confirm-full-run`** is used.
- **Artifacts path (intended):** `reports/RUNS/<timestamp>_s2_s1_product_discretized_full/`
  with `config.json`, `metrics.json`, `data.npz`, `summary.md`, `figures/.placeholder`.
- **Dry-run remains computation-free:** only config + `full_profile_dry_run_report`.
- **Baseline (informational):** `v0.1.14-mvp-s2-s1-discretization-v2-full` — **unchanged**
  by this wiring; no promotion.

## What Was Not Done

- **Real** `--full --confirm-full-run` was **not** executed as part of the implementation
  task that produced this note.
- **No baseline promotion** and **no release-note** updates tied to a full run.
- **No physics claims** from guard wiring alone.

## Test suite (informational)

- `pytest -q` → **187 passed** (full suite after this change set).

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** physical validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.
