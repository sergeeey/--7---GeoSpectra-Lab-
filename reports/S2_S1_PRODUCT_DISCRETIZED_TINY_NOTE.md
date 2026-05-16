# S2 x S1 Product-Discretized Tiny Diagnostic

## Summary

Однократный прогон **tiny**-профиля product-discretized toy-моста `S2 × S1` (Kronecker-сумма прокси `S2` и семейств `S1`). Это **диагностический** прогон для фиксации артефактов и ворот, **не** промоция baseline и **не** замена результатов v0.1.14 (v2/v3 история и ограничения сохраняются отдельно в спецификации и milestone-отчётах).

## Source Run

- **Команда:** `python scripts/s2_s1_product_discretized.py --tiny`
- **Путь прогона (от корня репозитория):** `reports/RUNS/20260514-100826_s2_s1_product_discretized_tiny`
- **Артефакты (проверено):** `config.json`, `metrics.json`, `data.npz`, `summary.md`, `figures/.placeholder`

## Gate Summary

| Gate | Результат |
|------|-----------|
| `classification` | `tiny_product_discretized_diagnostic_complete` |
| `hermiticity_all_passed` | `true` |
| `shape_all_passed` | `true` |
| `reproducibility_passed` | `true` (фиксированный seed в конфиге) |
| `q0_controls_all_passed` | `true` |

По **36** кейсам (агрегат из `metrics.json`):

| Поле | Сводка |
|------|--------|
| `q0_control_passed` | 36 / 36 |
| `s1_not_spectator` | 36 / 36 |
| `flux_response_observed` | 36 / 36 |
| `pbc_apbc_difference` | 36 / 36 |
| `kernel_only_localization_gate_passed` | 36 / 36 |
| `fixed_window_localization_gate_passed` | 36 / 36 |
| `localization_gate_v2_passed` | 36 / 36 |
| `localization_gate_v3_classification` | все кейсы: `window_robust_pass` |
| `window_robust_localization_passed` | 36 / 36 |
| `pass_rate_across_windows` | min = max = `1.0` |
| `window_sensitivity_score` | `0.0` во всех кейсах (см. per-case в `metrics.json`) |
| `ring_alpha0_caveat_detected` | **6 / 36** (кейвят остаётся видимым на подмножестве сетки) |

Совместимые с v2/v3 поля присутствуют в каждой записи кейса в `metrics.json`: `kernel_only_localization_gate_passed`, `fixed_window_localization_gate_passed`, `localization_gate_v2_passed`, `pass_rate_across_windows`, `window_sensitivity_score`, `localization_gate_v3_classification`, `window_robust_localization_passed`, `ipr_delta_by_window`, `pass_by_window`, и др.

## Relation to v0.1.14

Информационная привязка к baseline: `v0.1.14-mvp-s2-s1-discretization-v2-full` (см. `config.json` / `metrics.json`). Настоящий прогон — **refinement scaffold** после v0.1.14 (product-discretized ветка), **не** отмена и не перезапись документированных результатов v2/v3 и kernel-only mixed result.

## Limitations

- Только **tiny**-сетка параметров; **нет** full/stress-профиля и нет сравнения «на равных» с полным legacy-прогоном в этом note.
- Оператор — toy product-discretized диагностика (Option A из spec), не доказательство континuum-оператора Дирака на компактификации.

## Scientific Non-Claims

- Нет утверждения о **континуумной** компактификации.
- Нет **S6** или **S3×S6** физической валидации.
- Нет вывода **Standard Model**.
- Нет доказательства **физической хиральности**.
- Нет обхода **Witten/Lichnerowicz**.
