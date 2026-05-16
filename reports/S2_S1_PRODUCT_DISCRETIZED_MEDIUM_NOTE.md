# S2 x S1 Product-Discretized Medium Diagnostic

## Summary

Первый **реальный** прогон **medium**-профиля product-discretized toy-моста `S2 × S1` (Kronecker-sum Hamiltonian proxy). Это **диагностический** прогон средней сетки, **не** промоция baseline и **не** замена результатов **v0.1.14** или исторических ограничений v2/v3.

## Source Run

- **Команда:** `python scripts/s2_s1_product_discretized.py --medium`
- **Путь прогона (от корня репозитория):** `reports/RUNS/20260514-125211_s2_s1_product_discretized_medium`
- **Статус выполнения:** завершён успешно (один прогон, без прерывания; wall-clock порядка **~47 мин** на использованной машине).

## Case Count and Controls

| Поле | Значение |
|------|-----------|
| Ожидаемое число ячеек (dry-run / план) | **1080** |
| Фактическое `case_count` | **1080** |
| `profile_name` | `medium` |
| `clean_control_cases_count` (`W=0`) | **270** |
| `disordered_cases_count` (`W>0`) | **810** |
| `disorder_contrast_available` | **true** |

Артефакты в каталоге: `config.json`, `metrics.json`, `data.npz`, `summary.md`, `figures/.placeholder`.

## Gate Summary

Агрегаты из `metrics.json` / `summary.md`:

| Gate / поле | Значение |
|-------------|----------|
| `classification` | `product_discretized_medium_diagnostic_complete` |
| Hermiticity (`hermiticity_all_passed`) | **true** |
| Shape (`shape_all_passed`) | **true** |
| Reproducibility (`reproducibility_passed`) | **true** |
| q0 aggregate (`q0_controls_all_passed`) | **true** |
| `q0_false_positive_count` | **0** |
| `disorder_contrast_available` | **true** |

По **всем 1080** кейсам:

| Поле | Значение |
|------|----------|
| `s1_not_spectator` | **true** для каждого кейса |
| `flux_response_observed` | **false** у **90** кейсов, **true** у остальных (см. интерпретацию: не агрегированный «gate fail» в текущей схеме, но факт зафиксирован) |

Per-case поля v2/v3 присутствуют в `metrics.json`: `kernel_only_localization_gate_passed`, `fixed_window_localization_gate_passed`, `localization_gate_v2_passed`, `pass_rate_across_windows`, `window_sensitivity_score`, `localization_gate_v3_classification`, `window_robust_localization_passed`, и др.

## Ring / alpha=0 Tracking

| Метрика | Значение |
|---------|-----------|
| `ring_alpha0_cases_count` | **90** (ячейки `family=ring`, `alpha=0`, `W>0`) |
| `ring_alpha0_failure_count` | **4** (по определению в коде: среди этих ячеек не проходят одновременно kernel-only, fixed-window и v3-robust ворота) |

## v2/v3 Diagnostics

| Метрика | Значение |
|---------|-----------|
| `v2_vs_v3_disagreement_count` | **1** |
| `v3_failure_counts_by_bucket` | **276** уникальных ключей-бакетов; сумма счётчиков по бакетам = **276** (число кейсов с `window_robust_localization_passed == false`) |

**Уточнение по смыслу v3 «failure» на этой сетке:** все **270** кейсов с **`W=0`** дают **«non-robust»** по v3 (ожидаемо: чистый и «зашумлённый» оператор совпадают при нулевой силе беспорядка, IPR-дельта по окнам не проходит порог). Среди кейсов с **`W>0`** только **6** кейсов с `window_robust_localization_passed == false`, **все** с `family=ring`.

## Interpretation

По правилам из medium-плана:

1. **`q0_false_positive_count > 0`** → **нет** (0). Контроль q=0 **не** классифицируется как провал; **масштабирование дальше не блокируется** этим критерием.
2. **`disorder_contrast_available == false`** → **нет** (true). **Не** «profile design failure».
3. **Сконцентрированы ли сбои в ring / alpha≈0** при **реальном беспорядке (`W>0`)** → да: **6 / 810** disordered-кейсов non-robust, **все `ring`**. Это согласуется с классификацией **localized ring / alpha0 caveat** для disorder-части (в духе v0.1.14 narrative), без необходимости объявлять «полный провал» product-discretized на всех семействах.
4. **«Распределены по семействам» в сыром счёте v3** → агрегат **276** смешивает **структурные** W=0 кейсы с disorder-кейсами; **честная** выжимка для интерпретации ограничений оператора — смотреть подмножество **`W>0`**, где non-robust **только ring** (6 кейсов), а не равномерно по всем трём семействам.

## Limitations

- Только **medium**-сетка; **нет** full/stress профиля и нет сравнения с legacy `s2_s1_product` stress в этом note.
- Оператор остаётся **toy / refinement scaffold**, не доказательством континuum-Дирака или физической компактификации.

## Scientific Non-Claims

- Нет утверждения о **континуумной** компактификации.
- Нет **S6** или **S3×S6** физической валидации.
- Нет вывода **Standard Model**.
- Нет доказательства **физической хиральности**.
- Нет обхода **Witten/Lichnerowicz**.

**Baseline (informational):** `v0.1.14-mvp-s2-s1-discretization-v2-full` — **без промоции**.
