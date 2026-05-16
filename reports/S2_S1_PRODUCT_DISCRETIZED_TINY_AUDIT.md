# S2 × S1 Product-Discretized Tiny Diagnostic — Pre-Scaling Audit

**Baseline (informational, не промоция):** `v0.1.14-mvp-s2-s1-discretization-v2-full`  
**Аудируемый прогон:** `reports/RUNS/20260514-100826_s2_s1_product_discretized_tiny`  
**Классификация прогона:** `tiny_product_discretized_diagnostic_complete`

## Verdict

**confirmed with caveats**

Каркас оператора, ворота и артефакты **структурно согласованы** со spec и с ограничением «toy / не континуум»; перед full/stress scaling зафиксированы осмысленные **ограничения по сетке параметров** (в первую очередь отсутствие вариации по `W` в фактическом tiny-прогоне и «плоская» v3-картина на этой сетке).

---

## 1. Объём и источники

Просмотрены:

| Артефакт / файл | Назначение |
|-----------------|------------|
| `reports/S2_S1_PRODUCT_DISCRETIZED_REFINEMENT_SPEC.md` | Контракт Option A, наблюдаемые, ворота, non-claims |
| `cc_toy_lab/spectral/s2_s1_product_discretized.py` | Построение `H`, анализ кейса, tiny runner, артефакты |
| `scripts/s2_s1_product_discretized.py` | CLI только `--tiny` |
| `tests/test_s2_s1_product_discretized.py` | Форма, Hermiticity, seed, q0, поля JSON, язык claims |
| `.../metrics.json` (36 кейсов) | Численная сверка вариации и полей |
| `.../summary.md` | Ворота и non-claims в шапке |

Исторические ограничения v0.1.14 (v2 stress, v3 ring/alpha=0, kernel-only mixed и т.д.) **не пересматриваются** этим аудитом и остаются внешним слоем правды (spec + milestone).

---

## 2. Структурные проверки

| Проверка | Статус | Доказательство / комментарий |
|----------|--------|-------------------------------|
| **Hermitian оператор** | Pass | `H = kron(D²,I) + kron(I,P)` с последующим `_hermitize`; в прогоне `hermiticity_max_residual == 0` для кейсов в выборке; агрегат `hermiticity_all_passed: true`. |
| **Детерминированная форма** | Pass | `total_dimension == s2_dimension * s1_size`; `shape_all_passed: true`; дублирование прогона для `reproducibility_passed`. |
| **Контроль q=0** | Pass | Логика: `q0_control_passed = not (q==0 and disordered_kernel_count>0)`; в `metrics.json` все кейсы с `q=0` имеют `q0_control_passed: true`; агрегат `q0_controls_all_passed: true`. |
| **Различия семейств S1** реально используются | Pass | В `build_product_discretized_operator` передаётся `family` в `build_s1_operator`; при фиксированных `q=1`, `s1_size=8`, `alpha=0`, `W=8` наблюдаются различные `disordered_s1_low_energy_ipr` (напр. `ring` vs `spectral_circle`); спектральные скаляры меняются по сетке (`disordered_min_abs_eigenvalue` имеет 19 различных значений с округлением). |
| **Поля v2/v3** присутствуют | Pass | В каждом кейсе: `kernel_only_localization_gate_passed`, `fixed_window_localization_gate_passed`, `localization_gate_v2_passed`, `pass_rate_across_windows`, `window_sensitivity_score`, `localization_gate_v3_classification`, `window_robust_localization_passed`, `ipr_delta_by_window`, `pass_by_window`. |
| **Кейвят ring / alpha=0 не стёрт** | Pass | Флаг `ring_alpha0_caveat_detected` выставляется при `(family==ring, alpha==0, W>0)`; в прогоне **6 / 36** кейсов с `true` — кейвят **виден**, даже при прохождении остальных ворот. |
| **Нет headline «global chiral index» как метрики** | Pass | В `metrics.json` / `summary.md` нет ключей `global_chiral_index` или `physical_chirality_proven`; явно зафиксирован отказ от global chiral index headline в `notes` и в тексте summary (non-claim). |
| **Нет физического overclaim в артефактах** | Pass | Summary открывается scientific non-claims (compactification, S6/S3×S6, SM, physical chirality, Witten/Lichnerowicz). |

---

## 3. Вариация по параметрам tiny-прогона (реальные данные)

| Ось | Есть вариация? | Комментарий |
|-----|----------------|-------------|
| **q** | Да | `q ∈ {-1,0,1}`; меняются `clean_kernel_count`, `disordered_min_abs_eigenvalue` и паттерны (пример: при `spectral_circle`, `s1_size=8`, `alpha=0`: разные `clean_kernel_count` и `d_min` по `q`). |
| **S1 family** | Да | Три семейства в сетке; спектры и IPR различаются (см. п.2). |
| **alpha** | Да | `0.0` и `0.5`; наблюдаются различия в `disordered_min_abs_eigenvalue` и связанных полях. |
| **W (disorder_strength)** | **Нет в этом прогоне** | В `run_product_discretized_tiny` значения `w==0.0` **пропускаются**; в сохранённом `metrics.json` у всех кейсов `disorder_strength: 8.0` **только**. Вариации по силе беспорядка **в этом артефакте не проверяются** — это **caveat** перед scaling: следующий шаг должен явно решить, нужен ли отдельный мини-срез по `W` (включая малые `W`) или отдельный stress-профиль, не смешивая с baseline. |

Дополнительно: на данной сетке все кейсы получили `localization_gate_v3_classification: window_robust_pass` и `pass_rate_across_windows: 1.0` — это **не** доказательство устойчивости на расширенной сетке; это признак того, что **tiny слишком узок**, чтобы ловить v3-чувствительность как в исторических v3 stress кейсах для `ring`.

---

## 4. Ограничения перед scaling (честно)

1. **Один уровень W=8** в сохранённом tiny — нет сравнения «чистый vs слабый disorder» внутри product-discretized ветки.  
2. **Нет full/stress** — аудит не заменяет v2/v3 stress-историю legacy-моста.  
3. **Hamiltonian Kronecker-sum** ≠ Dirac product в континуумном смысле — spec это формулирует; масштабирование должно классифицировать расхождения как *operator-refinement limitation*, а не как опровержение v0.1.14.  
4. Spec всё ещё указывает «latest documented tests: 132»; фактический репозиторий может иметь **144** теста — рассинхрон документации spec, не влияющий на корректность кода, но стоит поправить при следующем проходе документации (вне baseline promotion).

---

## 5. Scientific non-claims (повтор)

Аудит **не** утверждает:

- континуумную компактификацию;  
- физическую валидацию **S6** или **S3×S6**;  
- вывод **Standard Model**;  
- доказательство **физической хиральности**;  
- обход **Witten/Lichnerowicz**.

---

## 6. Итоговая формулировка вердикта

| Вариант | Применимость |
|---------|----------------|
| tiny scaffold confirmed | Частично: реализация соответствует задуманному tiny scaffold. |
| **confirmed with caveats** | **Выбрано:** ворота и структура ОК; вариация по `W` в прогоне отсутствует; v3 «всё robust» на tiny не переносимо на stress без доп. доказательств. |
| structurally weak / needs redesign | Не выбрано: нет противоречия Hermiticity/shape/q0/полям. |
| contradicted | Не выбрано. |

**Baseline не промотирован.** Исторические v2/v3 ограничения и mixed kernel-only результат **не оспариваются** этим отчётом.
