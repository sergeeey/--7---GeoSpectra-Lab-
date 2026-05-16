# Addendum: tiny audit после явного контроля W=0

**Базовый аудит:** `reports/S2_S1_PRODUCT_DISCRETIZED_TINY_AUDIT.md`  
**Baseline (informational, без промоции):** `v0.1.14-mvp-s2-s1-discretization-v2-full`

---

## 1. Что изменилось

- В product-discretized **tiny**-прогоне ранее значение **`W=0` (disorder_strength)** пропускалось в цикле, поэтому в артефакте фактически оставался только слой **`W=8`**.
- После доработки tiny включает **оба** уровня из `w_values`: **`0.0`** и **`8.0`**.
- В агрегат `metrics.json` добавлены поля:  
  `clean_control_cases_count`, `disordered_cases_count`, `has_clean_control`, `has_disordered_control`, `disorder_contrast_available`.
- Для кейсов **`W=0`** зафиксирована семантика **q=0 control**, согласованная с тем, что `build_s1_operator` при нулевой силе беспорядка возвращает тот же clean-оператор (явный clean-control, а не проверка «ложного ядра от беспорядка»).

Код в этом addendum **не** меняется; документ фиксирует состояние после правок и прогона ниже.

---

## 2. Новый путь прогона

`reports/RUNS/20260514-110115_s2_s1_product_discretized_tiny`

(команда: `python scripts/s2_s1_product_discretized.py --tiny`)

---

## 3. Счётчики clean / disordered

Из `metrics.json` данного прогона:

| Поле | Значение |
|------|-----------|
| `case_count` | 72 |
| `clean_control_cases_count` | 36 |
| `disordered_cases_count` | 36 |
| `has_clean_control` | `true` |
| `has_disordered_control` | `true` |
| `disorder_contrast_available` | `true` |

---

## 4. Статус прежнего caveat

**Caveat из базового аудита** («tiny фактически только W=8; W=0 пропущен») — **снят** в том смысле, что в одном tiny-артефакте теперь **одновременно** присутствуют явные **clean-control (W=0)** и **disordered (W=8)** кейсы, и флаг **`disorder_contrast_available`** отражает доступность контраста на уровне сетки.

---

## 5. Оставшиеся ограничения

- По-прежнему только **tiny**-профиль; **нет** full/stress валидации product-discretized ветки.
- Оператор остаётся **toy / refinement scaffold** (Kronecker-sum Hamiltonian proxy), **не** доказательством континuum-компактификации и **не** заменой исторических слоёв v0.1.14 (v2/v3, kernel-only mixed и т.д. — внешние записи сохраняют силу).

---

## 6. Обновлённый вердикт

**confirmed with reduced caveats**

Обоснование: структурные ворота и поля совместимости сохранены; главный зарегистрированный в базовом аудите пробел по **W=0** устранён в артефакте и метриках. Ограничения п.5 остаются и переносятся на следующий этап (масштабирование / stress), а не на «отмену» предыдущего milestone.

---

## Scientific non-claims (без изменений)

Не утверждается: континуумная компактификация; физическая валидация **S6** / **S3×S6**; вывод **Standard Model**; доказательство **физической хиральности**; обход **Witten/Lichnerowicz**.

---

## Примечание по тестам

Для данного **docs-only** addendum повторный запуск `pytest -q` **не выполнялся** (политика: тесты при смене только markdown не обязательны). Зафиксированный в контексте репозитория статус: **145 passed** после внедрения W=0.

**Baseline не промотирован.**
