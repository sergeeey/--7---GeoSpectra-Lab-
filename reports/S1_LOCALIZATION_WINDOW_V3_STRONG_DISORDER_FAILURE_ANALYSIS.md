# S1 localization gate v3 — strong-disorder failure case analysis (W ≥ 8)

**Baseline reference (unchanged):** `v0.1.14-mvp-s2-s1-discretization-v2-full`

**Source run:** `reports/RUNS/20260513-213053_s1_discretization_v2_stress_v3`

This document is a **toy diagnostic slice** on the six **case-level** v3 failures with disorder **W ≥ 8** taken from `stress_diagnostics.v3_failure_cases` in `metrics.json`. Arrays in `data.npz` were checked for the same case fields (`case_*`); **unstable windows** are only fully serialized per case in `metrics.json` (not as nested lists in `data.npz`).

## Scientific non-claims

No claim of continuum compactification, **S6** / **S3×S6**, **Standard Model**, **physical chirality**, or **Witten/Lichnerowicz bypass**. No baseline promotion; historical v2 / kernel-only / stress records are not reinterpreted or erased.

## Selection rule

Cases are rows in `v3_failure_cases` with `disorder_strength ≥ 8.0`. **Count = 6** (matches aggregate `v3_failure_count_by_disorder` tail: `8→4`, `12→1`, `16→1`).

## Compact case table

| # | family | q | s1_size | alpha | W | seed | v3 classification | pass_rate | w_sens_score | v2 fixed-window pass | v2 vs v3 disagree | unstable windows (summary) |
|---:|---|---:|---:|---:|---:|---:|---|---:|---:|:---|:---|:---|
| 1 | ring | 1 | 8 | 0.0 | 8.0 | 11836052 | fragile_pass | 0.6 | 0.4 | True | True | 2 failing windows (k=4,6) |
| 2 | ring | −1 | 8 | 0.0 | 8.0 | 9836055 | fragile_pass | 0.6 | 0.4 | False | False | 2 failing (k=8,10) |
| 3 | ring | 2 | 8 | 0.0 | 12.0 | 12837054 | fragile_pass | 0.6 | 0.4 | True | True | 2 failing (k=4,6) |
| 4 | ring | 2 | 8 | 0.0 | 16.0 | 12838052 | fragile_pass | 0.6 | 0.4 | True | True | 2 failing (k=10,12) |
| 5 | ring | 2 | 16 | 0.0 | 8.0 | 13636052 | fragile_pass | 0.4 | 0.6 | True | True | 3 failing (k=4,10,12) |
| 6 | ring | 2 | 24 | 0.0 | 8.0 | 14436152 | fragile_pass | 0.6 | 0.4 | True | True | 2 failing (k=4,6) |

Full `unstable_window_cases` payloads (ipr_delta, low_energy_count, passed) are in `metrics.json` on each listed case object.

## Cluster analysis (the six cases)

| Axis | Pattern |
| --- | --- |
| **Family** | **100% `ring`** — no `spectral_circle`, no `wilson_ring`. |
| **s1_size** | **4 / 6** at `8`, **1 / 6** at `16`, **1 / 6** at `24` — strong skew to **small N**, not exclusively N=8. |
| **W (disorder)** | **W = 8** on **4** cases, **W = 12** and **W = 16** on **one** each (both still on `s1_size = 8`). |
| **alpha** | **All `0.0`** — same boundary-twist slice within this stress grid. |
| **Seed** | **Six distinct seeds** — not a single-seed glitch; no duplicate `(family,q,s1,alpha,W,seed)` row. |
| **q** | One each `q ∈ {1, −1}`; **four** with `q = 2` (including both W>8 cases on size 8). |
| **v3 class** | **All `fragile_pass`** — no `window_sensitive` / `fail` in this W≥8 slice. |
| **v2 fixed-window** | **5 / 6** pass, **1 / 6** fail (case #2) — v2–v3 disagreement **4 / 6** `True` where v2 still passes fixed-window but v3 is not window-robust. |

## Interpretation (per project rules)

- **Not** “spread across families, sizes, seeds and W” — the signal is **localized to `ring`**, mostly **`alpha = 0`**, mostly **`s1_size = 8`**, with **distinct seeds**.
- **Strong-disorder tail** (`W = 12`, `16`) appears **only on `ring` / `s1_size = 8` / `alpha = 0` / `q = 2`** in this six-case set.
- **Classification:** **targeted artifact / regime candidate** (ring + low twist + small-N concentration), **and** within the agreed stress verdict vocabulary: **unresolved but localized v3 strong-disorder limitation** — i.e. not evidence of a clean universal “all discretizations pass” statement at strong disorder for this toy gate.

Possible **mechanistic tags** (hypothesis-level, not claims): ring-only discretization artifact; **low `s1_size` sensitivity** at the largest W; **window-definition / low-energy-count sweep** stress (all cases `fragile_pass` with documented unstable windows). A dedicated **window-definition** root cause would need further isolated experiments (out of scope here).

## Data loading notes

- **`metrics.json`:** `stress_diagnostics["v3_failure_cases"]` — used for the table and unstable-window detail.
- **`data.npz`:** case-level scalars align with the same stress case index order (`case_family`, `case_q`, `case_s1_size`, `case_disorder_strength`, `case_localization_gate_v3_classification`, …); nested `unstable_window_cases` are **not** duplicated as per-row objects in the npz.

## Regression

`pytest -q` was run after adding this report: **124 passed** (workspace check on 2026-05-13).
