# S2 x S1 Product-Discretized Full Dry-Run Note

## Summary

This note records **CLI dry-run validation only** for the **full** product-discretized
profile grid. **No** spectral operators were built and **no** `reports/RUNS/...`
artifact directory was written. This is **not** a full diagnostic run and **not**
evidence for or against toy gates beyond grid bookkeeping.

## Command

```powershell
python scripts/s2_s1_product_discretized.py --full --dry-run
```

## Dry-Run Output

Captured stdout (representative):

```text
profile_name=full
expected_case_count=6615
grid_dimensions={"alpha_values": 3, "low_energy_count_values": 5, "q_values": 7, "s1_families": 3, "s1_sizes": 5, "seeds": 3, "w_values": 7}
estimated_run_dir_suffix=_s2_s1_product_discretized_full
baseline_informational=v0.1.14-mvp-s2-s1-discretization-v2-full (unchanged; not a promotion)
warning: no operators were computed (dry-run only).
warning: a real --full run is much heavier than medium and must be launched intentionally with logging and artifact checks; not enabled in this CLI build.
full profile dry-run complete (no operators computed)
```

Outer-grid case count: **7 × 3 × 5 × 3 × 7 × 3 = 6615** (see
`reports/S2_S1_PRODUCT_DISCRETIZED_FULL_PROFILE_PLAN.md`). The `low_energy_count_values`
axis (**5** values) is reported for bookkeeping and matches the medium/tiny
analyzer pattern; it does **not** multiply the **6615** outer-cell count in the
dry-run summary.

## Relation to Medium

The latest **completed real** product-discretized diagnostic run on record remains
the **medium** profile:

`reports/RUNS/20260514-125211_s2_s1_product_discretized_medium`

This dry-run does **not** supersede medium metrics, failure analysis, or W4 smoke
interpretation.

## Guardrails

- **`python ... --full`** without **`--dry-run`** is **rejected** by the CLI with exit
  code **2** and an explanatory message (real full execution not enabled here).
- **Baseline** tag is unchanged: **`v0.1.14-mvp-s2-s1-discretization-v2-full`**.
- Historical **v2 / v3 / medium** limitations remain authoritative until a future
  audited full run exists.

## Test suite (post-change)

After guarded full-runner tests: `pytest -q` → **187 passed** (full suite
on 2026-05-14; wall clock order **~20 min** on reference machine).

## Scientific Non-Claims

- No **continuum compactification**.
- No **`S6` / `S3 × S6`** physical validation.
- No **Standard Model** derivation.
- No **physical chirality** proof.
- No **Witten/Lichnerowicz** bypass.
