# Product-Discretized W≈4 Transition-Regime Diagnostic

## Purpose

Целевой сдвиг по **W** вокруг medium-caveat (**`ring`**, **v3 non-robust при `W=4`**, ноль при **`W=8`/`12`** в medium-прогоне). Диагностика отвечает на вопрос: это **transition-regime**, **артефакт размера/α/seed**, **ring discretization**, или **неразрешённое ограничение** product-discretized слоя.

**Baseline (informational, без промоции):** `v0.1.14-mvp-s2-s1-discretization-v2-full`.

## Запуск

```bash
# Smoke (по умолчанию): компактная сетка для CI / быстрый осмотр
python scripts/s2_s1_product_discretized_w4_diagnostic.py

# Full: полная сетка из milestone (≈3600 кейсов; долго)
python scripts/s2_s1_product_discretized_w4_diagnostic.py --full
```

Артефакты: `reports/RUNS/<timestamp>_s2_s1_product_discretized_w4_diagnostic/` — `config.json`, `metrics.json`, `data.npz`, `summary.md`, `figures/.placeholder`.

## Сетки

### Full (флаг `--full`)

| Параметр | Значения |
|----------|----------|
| `families` | `("ring", "spectral_circle", "wilson_ring")` |
| `q_values` | `(-2, -1, 0, 1, 2)` (как в medium + расширение) |
| `s1_sizes` | `(8, 16, 24, 32, 48)` |
| `alpha_values` | `(0.0, 0.25, 0.5)` |
| `w_values` | `(2.0, 4.0, 6.0, 8.0)` |
| `seeds` | `(122, 123, 124, 456)` (123 из medium-case + «соседи» + 456) |

Ожидаемое число кейсов: **3600**.

### Smoke (по умолчанию; для pytest и быстрого прогона)

Усечённая сетка с тем же **набором `W`**: `(2.0, 4.0, 6.0, 8.0)`; семейства `ring` + `spectral_circle`; `q=(0,1)`, `s1_size=(8)`, `alpha=(0.0, 0.5)`, `seed=(123)` → **32** кейса.

## Поля кейса (в `metrics.json`)

Для каждой ячейки сохраняются (совместимо с product-discretized):  
`localization_gate_v3_classification`, `pass_rate_across_windows`, `window_sensitivity_score`, `unstable_window_cases`, `window_robust_localization_passed`, `localization_gate_v2_passed`, `kernel_only_localization_gate_passed`, IPR-поля, `clean_kernel_count` / `disordered_kernel_count`, `clean_min_abs_eigenvalue` / `disordered_min_abs_eigenvalue`, вычисляемое **`v2_vs_v3_disagreement`**.

Агрегаты: `w4_diagnostic_classification`, `w4_diagnostic_evidence`, плюс стандартные поля из `assess_product_discretized_results` на том же наборе кейсов.

## Правила интерпретации (код)

| Условие | Классификация |
|---------|----------------|
| `q0_false_positive_count` > 0 на сетке | `w4_diagnostic_control_failure` |
| Нет disordered non-robust | `w4_diagnostic_no_disordered_non_robust` |
| Все non-robust — `ring`, есть провалы при **W=4**, нет при **W=6** и **W=8** | `transition_regime_sensitivity_ring_w4_only` или `..._ring_low_W_band` (если есть провалы при **W=2**) |
| Все non-robust — `ring`, но есть провалы при **W=6** или **W=8** | `ring_family_v3_limitation_with_persistence_at_higher_W` |
| Non-robust не только `ring` | `multi_family_non_robust_investigate_further` |
| Иначе | `w4_diagnostic_mixed_pattern` |

## Scientific Non-Claims

- Нет континуумной компактификации.
- Нет физической валидации **S6** / **S3×S6**.
- Нет вывода **Standard Model**.
- Нет доказательства **физической хиральности**.
- Нет обхода **Witten/Lichnerowicz**.

## Связанные отчёты

- Medium milestone: `reports/MILESTONE_S2_S1_PRODUCT_DISCRETIZED_MEDIUM.md`
- Medium failure analysis: `reports/S2_S1_PRODUCT_DISCRETIZED_MEDIUM_FAILURE_ANALYSIS.md`

## Latest smoke run (recorded)

| Поле | Значение |
|------|----------|
| Команда | `python scripts/s2_s1_product_discretized_w4_diagnostic.py` |
| `run_path` | `reports/RUNS/20260514-141503_s2_s1_product_discretized_w4_diagnostic` |
| Режим | `smoke=True`, **32** кейса |
| `w4_diagnostic_classification` | `transition_regime_sensitivity_ring_low_W_band` |
| Evidence (кратко) | `disordered_non_robust_count=4`, все **`ring`**; по **W:** `2.0`→2, `4.0`→2; при **W=6** и **W=8** в этом smoke **0** non-robust |

Классификация **`..._ring_low_W_band`**: non-robust есть и при **W=2**, и при **W=4**, при **нуле** non-robust на **W=6/W=8** в данной smoke-сетке — в духе **transition-regime** на слабых **W**, без «залипания» на высоких **W** в этом срезе.

Полный прогон **`--full`** (3600 кейсов) в этой задаче **не** запускался; при необходимости выполните локально и допишите новую строку в этот раздел.
