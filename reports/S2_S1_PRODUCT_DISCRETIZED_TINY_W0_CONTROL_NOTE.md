# S2 × S1 Product-Discretized Tiny — явный контроль W=0

## Команда

```bash
python scripts/s2_s1_product_discretized.py --tiny
```

## Путь прогона (от корня репозитория)

`reports/RUNS/20260514-110115_s2_s1_product_discretized_tiny`

Артефакты: `config.json`, `metrics.json`, `data.npz`, `summary.md`, `figures/.placeholder`.

## Счётчики контроля беспорядка (из `metrics.json`)

| Поле | Значение |
|------|-----------|
| `clean_control_cases_count` | **36** (все комбинации с `disorder_strength == 0`) |
| `disordered_cases_count` | **36** (те же сетки с `disorder_strength == 8`) |
| `has_clean_control` | `true` |
| `has_disordered_control` | `true` |
| `disorder_contrast_available` | **`true`** (в одном прогоне есть и W=0, и W=8) |

`case_count`: **72** (раньше tiny пропускал W=0 и давал только 36 кейсов с W=8).

## Почему раньше не было W=0

В `run_product_discretized_tiny` стояло явное `if w == 0.0: continue`, чтобы не дублировать сетку до отдельного контракта «clean-control vs disordered». После аудита (`reports/S2_S1_PRODUCT_DISCRETIZED_TINY_AUDIT.md`) это признано недостатком: в артефакте не было явного слоя **W=0**. Теперь W=0 включён как **явный clean-control** рядом с W=8.

## q=0 и W=0

В `build_s1_operator` при `disorder_strength == 0.0` ветка беспорядка не применяется (возвращается тот же «clean» оператор, что и для `mode="clean"`). Для кейсов **W=0** правило «нет ложного наследуемого ядра от беспорядка» не интерпретируется как провал при совпадении чистого и «геометрического» спектра: `q0_control_passed` для таких кейсов задан как **true** (контроль беспорядка касается только **W>0**). Агрегат прогона: `q0_controls_all_passed: true`.

## Baseline

**Без промоции.** Информационная метка: `v0.1.14-mvp-s2-s1-discretization-v2-full`.

## Без физических claims

Toy-диагностика; не континуумная компактификация; не S6 / S3×S6; не Standard Model; не доказательство физической хиральности; не обход Witten/Lichnerowicz.

## Тесты

После изменений: `pytest tests/test_s2_s1_product_discretized.py -q` и полный `pytest -q` выполнялись успешно (**145 passed** на момент коммита изменений).
