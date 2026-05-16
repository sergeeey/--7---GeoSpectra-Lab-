# S1 localization gate v3 — quick diagnostic note

**Baseline reference (unchanged):** `v0.1.14-mvp-s2-s1-discretization-v2-full`

This note records a single **v3 quick** comparison run. It is **diagnostic metadata only** and does **not** constitute v3 full validation, baseline promotion, or a new physical result.

## Command

```bash
python scripts/s2_s1_discretization_comparison.py --quick --include-wilson --enable-v3
```

## Run path

`reports/RUNS/20260513-110216_s1_discretization_comparison_quick_v3`

## Per-family summary (v2 classification / v3 classification)

| Family           | v2 (`classification`) | v3 (`localization_gate_v3_classification`) |
| ---------------- | ----------------------- | ------------------------------------------- |
| spectral_circle  | `quick_bridge_passed`   | `window_robust_pass`                        |
| ring             | `quick_bridge_passed`   | `window_robust_pass`                        |
| wilson_ring      | `quick_bridge_passed`   | `window_robust_pass`                        |

**`v2_vs_v3_disagreement`:** `False` for all three families on this run.

**Test suite at time of note:** `pytest -q` → 121 passed.

## What v3 means here

The v3 path runs the **toy window sweep** (`compare_localization_gate_v3`) over configured `low_energy_count` values. It is a **diagnostic layer** on top of the existing benchmark: it does not replace v2 gates or redefine the project baseline.

## Quick profile vs ring window-sensitivity anchor

The **quick** comparison profile (grid implied by the CLI quick preset) **does not reproduce** the **known ring window-sensitivity anchor** seen under broader grids / stress-style settings (where kernel-only vs fixed-window gates can diverge and classifications such as `window_selection_sensitivity` appear). On this quick+v3 run, ring still showed aligned kernel-only and fixed-window conclusions in family metrics; treat this run as a **lightweight sanity slice**, not as evidence that ring sensitivity is absent in all regimes.

## Full / stress v3

**Full comparison and stress-style v3 coverage remain pending** (not covered by this note). Follow-up runs should be planned explicitly; this document does not schedule or certify them.

## Scientific non-claims

This diagnostic note and the underlying toy comparison:

- do **not** claim continuum compactification;
- do **not** claim **S6** or **S3 × S6** as the internal space;
- do **not** claim the **Standard Model**;
- do **not** claim a **physical chirality proof**;
- do **not** claim a **Witten/Lichnerowicz bypass**.
