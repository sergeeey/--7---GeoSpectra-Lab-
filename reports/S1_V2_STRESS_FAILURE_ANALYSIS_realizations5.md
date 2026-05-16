# S1 v2 Stress Failure Analysis (realizations=5)

## Executive Summary

При увеличении числа реализаций до `5` картина в целом совпадает с прогоном
`realizations=3` (см. `reports/S1_V2_STRESS_FAILURE_ANALYSIS.md`), но
**появился ровно один** fixed-window v2 failure при `W=8`.

Классификация по заранее заданному правилу ветвления:

- при `W>=8` failures **> 0** → `unresolved_strong_disorder_v2_limitation`
  (с перечислением кейсов), без отмены того факта, что основная масса
  отказов по-прежнему в `W=0` и слабом/переходном режиме `W∈{1,2,4}`.

Этот memo не меняет метрику, baseline и исторический kernel-only run; только
фиксирует артефакты stress-прогона `realizations=5`.

## Source Run

Run path:

```text
reports/RUNS/20260513-001436_s1_discretization_v2_stress
```

Artifacts:

- `metrics.json`, `summary.md`, `config.json`, `data.npz`, каталог `figures/`
  (figures — placeholder, `figures_generated=false` в метриках).

Ключевые поля:

- `stress_classification=v2_limitation`
- `comparison_classification=robust_across_discretizations`
- `case_level_fixed_window_all_passed=False`
- `fixed_window_failure_case_count=2376`
- `kernel_only_vs_fixed_window_disagreement_count=157`
- `ring_doubler_sensitive_case_count=157`
- `realizations=5` (полный stress-прогон)

## Failure Split by Disorder Regime

| Regime | Disorder values | Failure count |
| --- | --- | ---: |
| `W=0` | `0` | `1800` |
| `W=1-4` | `1, 2, 4` | `575` (`315+213+47`) |
| `W>=8` | `8` (в сетке только эта точка) | `1` |

Binary decision:

- Были ли fixed-window v2 failures при `W>=8`? **Да (1 кейс).**

## Единственный кейс `W=8` (fixed-window failure)

Из `metrics.json` → `stress_diagnostics.fixed_window_failure_cases`:

| Поле | Значение |
| --- | --- |
| `family` | `ring` |
| `disorder_strength` | `8.0` |
| `alpha` | `0.0` |
| `perturbation` | `0.0` |
| `q` | `-1` |
| `s1_size` | `8` |
| `seed` | `9836055` |
| `kernel_only_localization_gate_passed` | `true` |
| `fixed_window_localization_gate_passed` | `false` |
| `window_selection_sensitivity` | `true` |

Интерпретация в терминах уже сохранённых диагностик: это согласуется с веткой
**kernel-only vs fixed-window disagreement / ring doubler sensitivity**, а не
с массовым «провалом семьи» на агрегате (family-level gates остаются passed).

## Stress-level rule vs targeted mechanistic diagnosis (May 2026)

**Stress-level (pre-declared binary rule), unchanged:** because this run has
`W>=8` fixed-window failures **> 0** (exactly one case), the memo branch label
`unresolved_strong_disorder_v2_limitation` remains the **bookkeeping / gate-rule**
classification for the `realizations=5` stress artifact. **This does not erase
the `r=5` stress limitation** (`stress_classification=v2_limitation`,
`case_level_fixed_window_all_passed=False`, and the saved failure inventory).

**Targeted follow-up (mechanistic reclassification), additive:** a separate
targeted diagnostic run and memo refine **only** the isolated `W=8` outlier:

- Run: `reports/RUNS/20260513-082348_s1_v2_w8_failure_diagnostic`
- Memo: `reports/S1_V2_W8_FAILURE_DIAGNOSTIC.md`
- Mechanistic label: `threshold_or_window_definition_artifact`

That targeted result **narrows the interpretation**: no evidence here of a
**widespread** strong-disorder breakdown across families and larger `s1_size` on
the diagnostic `W>=8` sweep; the primary grid still shows **one** fixed-window
failure at `W>=8`. The remaining mechanism is **sensitivity of fixed-window
localization to `low_energy_count` / fixed low-energy window definition** on a
**ring, small-`s1_size`, anchor** case (`ipr_margin` down to `1e-4` does not
rescue it; nearby seeds `±10` fail only at the anchor seed `9836055`).

**Distinction to preserve in all downstream docs:** stress-level **rule
classification** (binary `W>=8` failure flag) **vs** targeted **mechanistic
diagnosis** (window-definition / threshold coupling on one anchor). The
historical mixed kernel-only full comparison remains preserved; baseline
`v0.1.14-mvp-s2-s1-discretization-v2-full` is unchanged.

## Сравнение с прогоном `realizations=3`

| Величина | `20260512-225834` (r=3) | `20260513-001436` (r=5) |
| --- | ---: | ---: |
| fixed-window failures | 1429 | 2376 |
| `W>=8` failures | 0 | 1 |

Вывод для планирования следующих шагов: усиление статистики по реализациям
**не подтвердило** гипотезу «ноль при `W>=8` всегда»; один редкий outlier
зафиксирован и должен оставаться видимым в отчётах.

## Scientific Non-Claims

- not continuum compactification
- not S6 / S3×S6 / Standard Model
- not physical chirality
- not Witten/Lichnerowicz bypass
