# S2 x S1 Product-Discretized Medium Profile Plan

## Purpose

Слой **medium** — следующий контролируемый шаг **после** tiny с явным **W=0 / W=8** (`disorder_contrast_available`) и addendum-аудита (**confirmed with reduced caveats**), но **до** любых full/stress прогонов по product-discretized ветке. Цель: проверить, переносятся ли ворота и наблюдаемые на **расширенной, всё ещё конечной** сетке (дополнительные `q`, размеры `S1`, промежуточные `alpha` и `W`, второй seed) без претензии на континуум или физическую компактификацию. Medium **не** заменяет baseline **v0.1.14-mvp-s2-s1-discretization-v2-full** и **не** снимает исторические ограничения legacy v2/v3.

## Current Tiny Status

Ссылки:

- Прогон: `reports/RUNS/20260514-110115_s2_s1_product_discretized_tiny`
- Заметка W=0: `reports/S2_S1_PRODUCT_DISCRETIZED_TINY_W0_CONTROL_NOTE.md`
- Аудит addendum: `reports/S2_S1_PRODUCT_DISCRETIZED_TINY_AUDIT_ADDENDUM_W0.md`

Tiny сейчас: **72** кейса (`3×3×2×2×2` по `q`, семействам, `s1_size`, `alpha`, `W` с двумя уровнями `W`), агрегаты `clean_control_cases_count` / `disordered_cases_count` / `disorder_contrast_available` присутствуют.

## Proposed Medium Grid

Контролируемое расширение относительно tiny:

| Параметр | Значения |
|----------|----------|
| `q_values` | `(0, 1, -1, 2, -2)` |
| `s1_families` | `("spectral_circle", "ring", "wilson_ring")` |
| `s1_sizes` | `(8, 16, 24)` |
| `alpha_values` | `(0.0, 0.25, 0.5)` |
| `W_values` | `(0.0, 4.0, 8.0, 12.0)` |
| `seeds` | `(123, 456)` |
| `low_energy_count_values` | `(4, 6, 8, 10, 12)` |

**Число ячеек (кейсов):**  
`5 × 3 × 3 × 3 × 4 × 2` = **1080** комбинаций `(q, family, s1_size, alpha, W, seed)` при том же паттерне «один вызов `analyze_product_discretized_case` на ячейку», что и в tiny.

Остальные гиперпараметры (например `cutoff`, `s1_mode_clean` / `s1_mode_disordered`, `reference_low_energy_count`, толерансы) — **наследовать из текущего tiny-конфига**, если отдельный обзор не потребует их сузить.

## Expected Runtime Risk

- **1080** ячеек; каждая ячейка включает несколько спектральных разложений (`eigh`) и v3-логику по **5** окнам (`low_energy_count_values`), плюс чистый/«зашумлённый» оператор и вспомогательные сигнатуры (spectator, flux probe, PBC/APBC slice). Оценка: порядок **~15×** больше work-per-cell относительно одного seed в tiny (из-за второго seed, +`q`, +`s1_size`, +`alpha`, +`W`), и **~30×** относительно исходного 36-кейсового tiny только по числу ячеек до расширения W=0 — итог **существенно дольше** одного tiny-прогона на той же машине.
- Это профиль **medium**: он **не** stress (нет множества реализаций беспорядка на ячейку, нет произвольного размера сетки); тем не менее суммарное время может исчисляться **десятками минут и более** без оптимизаций и без параллелизации — планировать окно и логирование прогресса при будущей реализации.
- Риск **OOM** низкий при плотных матрицах текущих размеров, но `s1_size=24` и верхний `q` увеличивают размерность `n_s2 × n_s1`; при реализации medium стоит заранее логировать `total_dimension` по подвыборке ячеек.

## Required Gates

На уровне прогона (как в tiny) и агрегатов:

| Gate | Назначение |
|------|------------|
| Hermiticity | \(\|H - H^\dagger\|_\infty \le\) `hermiticity_tol` по каждой ячейке |
| Shape consistency | `total_dimension == s2_dimension × s1_size` |
| Reproducibility | повторный прогон с теми же seed даёт согласованные скаляры (как в tiny) |
| q=0 control | правило для **W>0** сохраняется; для **W=0** — явный clean-control (как после W=0 фикса) |
| S1 non-spectator | `s1_not_spectator` по-прежнему обязателен в метриках |
| Flux response | `flux_response_observed` (или эквивалентная сигнатура) |
| Disorder contrast | `has_clean_control`, `has_disordered_control`, `disorder_contrast_available` на сетке |
| v2 fixed-window localization | `fixed_window_localization_gate_passed` / `localization_gate_v2_passed` |
| v3 window-sweep localization | `pass_rate_across_windows`, `localization_gate_v3_classification`, `window_robust_localization_passed` |
| ring / alpha=0 caveat | `ring_alpha0_caveat_detected` по-прежнему в каждой строке кейса |

## Metrics

Обязательные **агрегаты** (дополнить к существующим tiny-полям):

| Метрика | Описание |
|---------|----------|
| `clean_control_cases_count` | число ячеек с `W == 0` |
| `disordered_cases_count` | число ячеек с `W > 0` |
| `disorder_contrast_available` | на сетке есть и те, и другие |
| `v3_failure_counts_by_bucket` | структурированный подсчёт: по `s1_family`, `W`, `alpha`, `s1_size`, `q`, `seed`, где `localization_gate_v3_classification` ∉ успешного класса (заранее зафиксировать enum успеха/неуспеха в реализации) |
| `v2_v3_disagreement_count` | число ячеек, где `localization_gate_v2_passed` ≠ согласованного агрегата по v3 (например `window_robust_localization_passed` или выбранное правило в коде — зафиксировать в PR) |
| `ring_alpha0_cases_count` | ячейки с `(family=="ring", alpha==0, W>0)` |
| `ring_alpha0_failure_count` | из них подмножество, где v2/v3 ворота не проходят (определение «failure» = тот же порог, что в tiny/medium контракте) |
| `q0_false_positive_count` | число ячеек с `q==0`, `W>0`, где `q0_control_passed == False` (сигнал к остановке масштабирования) |

Per-case поля остаются совместимыми с tiny (включая kernel counts, IPR, caveat-флаг).

## Interpretation Rules

- **Сконцентрированы** сбои в `ring` / `alpha≈0` / малых `s1_size` → классифицировать как **localized ring / alpha0 caveat** (преемственность с v0.1.14 narrative).
- **Распределены** по семействам и параметрам → **unresolved product-discretized limitation** (представление/ворота не переносятся на medium без доработки).
- Появление **`q0_false_positive_count` > 0** при валидной реализации контроля → **control failure**; **не** масштабировать дальше до разбора.
- Если на сетке **`disorder_contrast_available == false`** (ошибка конфигурации) → **profile design failure**.

## Artifacts

Будущий medium-прогон (когда будет реализован) должен сохранять тот же набор, что tiny:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/.placeholder`

Каталог: например `reports/RUNS/<timestamp>_s2_s1_product_discretized_medium` (имя согласовать при реализации).

## Acceptance Criteria for Future Implementation

- Существует **`ProductDiscretizedConfig`** (или эквивалент) с флагом **`medium`** и параметрами сетки из раздела «Proposed Medium Grid».
- В CLI (например `scripts/s2_s1_product_discretized.py`) появляется флаг **`--medium`**, взаимоисключающий с `--tiny` или с явной иерархией профилей.
- Поведение **`--tiny`** и число/смысл tiny-кейсов **неизменны** относительно текущего зафиксированного состояния.
- Medium-прогон **завершается** с полным артефактом **или** падает с **прозрачной** ошибкой/частичным отчётом (без молчаливого обрезания сетки).
- Baseline **не** меняется без отдельного review.
- Нет **physical overclaim** в summary и metrics notes.

## Scientific Non-Claims

План и будущий medium-прогон **не** доказывают и **не** утверждают:

- континуумную компактификацию;
- физическую валидацию **S6** или **S3×S6**;
- вывод **Standard Model**;
- доказательство **физической хиральности**;
- обход **Witten/Lichnerowicz**.

---

**pytest:** для этого документа **не запускался** (docs-only).

**Baseline:** без изменений, без промоции (`v0.1.14-mvp-s2-s1-discretization-v2-full`).
