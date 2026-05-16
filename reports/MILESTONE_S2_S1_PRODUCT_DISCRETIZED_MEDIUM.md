# Milestone — S2 x S1 Product-Discretized Medium

## Executive Summary

Ветка **product-discretized refinement** для toy **S2 × S1** дошла до **завершения medium-profile диагностики** (`classification=product_discretized_medium_diagnostic_complete`, **1080/1080** кейсов). Агрегаты ворот и контраст **clean / disordered** выполняются; **q0** остаётся чистым. Ограничения **локализованы**: при **W > 0** только **6** кейсов **v3 non-robust**, все **`ring`**, все при **W = 4**; при **W = 8 и 12** для disordered-слоя **non-robust нет** — интерпретация: **чувствительность transition-regime (слабый disorder)** плюс **локальный ring / α=0 caveat**. Это **не** промоция baseline и **не** доказательство континuum-физики.

## Baseline

**Без изменений:** `v0.1.14-mvp-s2-s1-discretization-v2-full` (информационная привязка в артефактах; **без** смены baseline и **без** перезаписи исторических слоёв v0.1.14 / v2 / v3).

## Source Artifacts

| Документ / прогон | Путь |
|-------------------|------|
| Spec | `reports/S2_S1_PRODUCT_DISCRETIZED_REFINEMENT_SPEC.md` |
| Tiny (первый задокументированный прогон) | `reports/RUNS/20260514-100826_s2_s1_product_discretized_tiny` |
| Tiny с явным W=0 / W=8 | `reports/RUNS/20260514-110115_s2_s1_product_discretized_tiny` |
| Tiny audit | `reports/S2_S1_PRODUCT_DISCRETIZED_TINY_AUDIT.md` |
| Tiny audit addendum (W=0) | `reports/S2_S1_PRODUCT_DISCRETIZED_TINY_AUDIT_ADDENDUM_W0.md` |
| Medium plan | `reports/S2_S1_PRODUCT_DISCRETIZED_MEDIUM_PLAN.md` |
| Medium run | `reports/RUNS/20260514-125211_s2_s1_product_discretized_medium` |
| Medium note | `reports/S2_S1_PRODUCT_DISCRETIZED_MEDIUM_NOTE.md` |
| Medium failure analysis | `reports/S2_S1_PRODUCT_DISCRETIZED_MEDIUM_FAILURE_ANALYSIS.md` |
| W4 smoke diagnostic (transition-regime follow-up) | `reports/RUNS/20260514-141503_s2_s1_product_discretized_w4_diagnostic` |
| W4 diagnostic memo | `reports/S2_S1_PRODUCT_DISCRETIZED_W4_DIAGNOSTIC.md` |

## Medium Run Summary

| Показатель | Значение |
|------------|----------|
| `classification` | `product_discretized_medium_diagnostic_complete` |
| `profile_name` | `medium` |
| Ожидаемые / фактические кейсы | **1080 / 1080** |
| `clean_control_cases_count` | **270** |
| `disordered_cases_count` | **810** |
| `disorder_contrast_available` | **true** |
| `q0_false_positive_count` | **0** |
| `ring_alpha0_cases_count` | **90** |
| `ring_alpha0_failure_count` | **4** |
| `v2_vs_v3_disagreement_count` | **1** |
| Агрегаты ворот (Hermiticity / shape / repro / q0) | **все пройдены** в этом прогоне |
| `pytest -q` (зафиксированный статус репозитория) | **187 passed** |

*Примечание:* **276** кейсов с `window_robust_localization_passed == false` в агрегате включают **ожидаемые** **W = 0** clean-control строки; для интерпретации disorder-слоя см. failure analysis (**6** при **W > 0**).

## Failure Analysis

- **W > 0**, **v3 non-robust:** **6** кейсов.
- **Семейство:** все **6 — `ring`**.
- **Сила беспорядка:** все **6 — при `W = 4`**; при **`W = 8` и `W = 12`** число **W > 0** non-robust = **0** (в этом прогоне).
- **Интерпретация:** **transition-regime sensitivity** (слабый disorder) **+** **localized ring / α=0 caveat** (4 из 6 с `alpha = 0`; 2 с `alpha = 0.5`, малый `s1_size` — см. детальный отчёт).

## What This Validates

- Каркас **product-discretized** вышел за пределы **tiny-only** и отработал **medium**-сетку.
- В medium присутствует явный **clean / disorder контраст** (`disorder_contrast_available=true`).
- **q0**-контроль остаётся **без ложных срабатываний** в агрегате (`q0_false_positive_count=0`).
- Эффекты **семейств S1** и разнесение по параметрам сетки **наблюдаемы** в метриках.
- Диагностика **v2 / v3** перенесена в слой refinement и **согласована** с артефактным контрактом (per-case поля + агрегаты).

## What This Does Not Validate

- **Нет** континуумной компактификации.
- **Нет** физической валидации **S6** или **S3×S6**.
- **Нет** вывода **Standard Model**.
- **Нет** доказательства **физической хиральности**.
- **Нет** обхода **Witten/Lichnerowicz**.
- **Нет** full/stress валидации product-discretized ветки в этом milestone.

## Readiness Assessment

| Критерий | Оценка |
|----------|--------|
| Engineering lab | **9.8 / 10** |
| Scientific honesty | **10 / 10** |
| Product-discretized refinement | **8.3 / 10** |
| Readiness for full/stress product-discretized run | **7.5 / 10** |
| Readiness for next geometry | **8 / 10** |
| Physical theory proof | **3 / 10** |

## Recommended Next Step

- **Не** переходить сразу к **S6 / S3×S6**.
- **A (smoke):** выполнена целевая **W4 smoke** диагностика (`reports/RUNS/20260514-141503_s2_s1_product_discretized_w4_diagnostic`, классификация `transition_regime_sensitivity_ring_low_W_band`): в smoke **все** non-robust — **`ring`**; при **W=6** и **W=8** в этом прогоне **0** non-robust; **q0** без ложных срабатываний. Это **поддерживает** интерпретацию **transition-regime sensitivity**, но **не снимает** medium-caveat и **не заменяет** полный профиль / стресс.
- Остаётся **опционально / в ожидании:** полный W4 sweep **`--full`** (~3600 кейсов) и дальнейший выбор масштабирования.
- Выбор дальше:
  - **A′.** Уточнение мини-профиля / при необходимости **`--full` W4`**.
  - **B.** Проектирование **full-profile** product-discretized (расширение сетки / стресс-контракт) **после** снижения caveats.
- **Предпочтительно A′**, если цель — **уменьшить caveats до масштабирования** full/stress.

---

**pytest:** для этого milestone-документа **не запускался** (только markdown).

**Baseline:** **без изменений.**
