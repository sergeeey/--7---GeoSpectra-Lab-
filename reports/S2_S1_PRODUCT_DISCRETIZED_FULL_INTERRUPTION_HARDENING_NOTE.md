# Product-discretized full runner — interruption hardening

## Context

- **Informational baseline (unchanged, not a promotion):** `v0.1.14-mvp-s2-s1-discretization-v2-full`
- A real guarded full run was launched with  
  `python scripts/s2_s1_product_discretized.py --full --confirm-full-run` (with stdout/stderr redirected to a log).
- That run **did not complete** (host reboot / interruption).

## Evidence from the interrupted attempt

- Log contained only the startup warning.
- No `run_path=...`, `classification=...`, or `s2_s1_product_discretized_full complete` lines.
- No `reports/RUNS/*_s2_s1_product_discretized_full/` directory was created in time.

## Root cause

The CLI created the timestamped run directory **only after** `run_product_discretized_full` returned.  
Heavy work ran with **no persistent run root**, so an interruption before completion left **no structured artifacts** (no `config.json`, no status, no progress).

## New behavior (this change set)

1. **Early run directory:** For `--full --confirm-full-run`,  
   `reports/RUNS/<timestamp>_s2_s1_product_discretized_full/` is created **before** the main grid work.
2. **Initial artifacts:** `config.json` and `run_status.json` (`status=running`, expected count 6615, command, timestamps, warnings) are written immediately.
3. **Progress:** `progress.json` is updated after each completed analyzer invocation (primary 6615-case grid plus reproducibility duplication pass; see `expected_step_count` in the file).
4. **Partial primary grid:** `partial_results.jsonl` receives one JSON line per completed **primary** grid case (same serialization shape as per-case rows elsewhere). **Automatic resume** from this file is **not implemented** in this step; a future change would need explicit resume semantics and tests.
5. **Final status:** On success, `run_status.json` is updated to `status=completed` with `classification` and `completed_at`. On failure, `status=failed` with `error` and last known primary/repro counts when available.

## What was not done in this task

- **No real full 6615-case run** was executed as part of this hardening work (too expensive for CI / this patch).
- **Baseline tag** and **scientific interpretation rules** (v2/v3, metrics definitions) were **not** altered.
- **No** claim of continuum compactification, S6 / S3×S6 validation, Standard Model, physical chirality, or Witten/Lichnerowicz bypass.

## Operator note

Historical logs and any partial console output from the interrupted attempt are **not** deleted by this change; new runs use a new timestamped directory under `reports/RUNS/`.
