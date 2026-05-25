# CODE FIX PLAN v0.1.24 — S³ Dirac Branch Indexing

**Дата:** 2026-05-25  
**Версия:** v0.1.24  
**Статус:** DRAFT — docs-only, no code changes yet  
**Checkpoint:** commit 3766913, main = origin/main, working tree clean

---

## 1. ПРОБЛЕМА

### 1.1. Active Implementation
**File:** `cc_toy_lab/spectral/dirac_s3.py`  
**Function:** `build_s3_dirac_operator(j_max, radius=1.0)`  
**Reference:** arXiv:1103.4097 page 15, equation (6.4)

### 1.2. Current Spectrum (verified by diagnostic)
```
Negative: -9/2, -7/2, -5/2
Positive: +3/2, +5/2, +7/2
```

**Code formula (lines 81-82):**
- Positive: `λ₊ = +(k + 1/2) / R` for k ≥ 1
- Negative: `λ₋ = -(k + 3/2) / R` for k ≥ 1

**Result:** k starts from 1 → lowest negative is -5/2, NOT -3/2.

### 1.3. Symptom
Gate 4B v0.1.23 source verification suggested:
- **Expected low spectrum:** `±3/2, ±5/2, ±7/2` (symmetric 6 branches)
- **Actual low spectrum:** `-9/2, -7/2, -5/2, +3/2, +5/2, +7/2` (asymmetric)

**Observation:** **-3/2 is missing** from negative branch.

### 1.4. Root Cause (hypothesis requiring source verification)
Two possibilities:

**A) Code bug:** k should start from 0 for negative branch
- If k=0 allowed: `λ₋ = -(0 + 3/2) = -3/2` ✓
- Current code: k ≥ 1 only → misses k=0

**B) Paper interpretation:** arXiv:1103.4097 eq (6.4) states k ≥ 1
- Formula: "eigenvalues k+1/2 and -(k+3/2) for k ≥ 1"
- If paper is correct → -3/2 should NOT exist
- If Gate 4B expected spectrum wrong → current code is correct

**CRITICAL:** Must verify paper eq (6.4) before declaring bug.

### 1.5. Impact (conditional on root cause)
**If A) code bug confirmed:**
- Gate 4B S³ Dirac: asymmetric spectrum → may affect source verification
- W-sweep: missing -3/2 level → incomplete scan
- Negative Controls S³: testing asymmetric spectrum

**If B) paper correct (k ≥ 1):**
- Current code is correct
- Gate 4B expected spectrum was wrong
- No fix needed, only documentation update

---

## 2. FIX STRATEGY

### 2.1. Этапы (строгая последовательность)

#### Этап 1: Unit Tests FIRST (TDD) — Source-Verified Expected Spectrum

**Файл:** `tests/cc_toy_lab/spectral/test_dirac_s3_branches.py` (новый)

**Purpose:** Fix expected spectrum based on paper verification, then test against code.

**Tests to add:**
1. **Current spectrum documentation (baseline):**
   - Verify current code produces: `-9/2, -7/2, -5/2, +3/2, +5/2, +7/2`
   - This test should PASS (documents current state)

2. **Presence of -3/2 (critical test):**
   - Check if `-3/2` exists in eigenvalues
   - Expected: FAIL if k ≥ 1 enforced (current code)
   - Expected: PASS if k=0 added (after fix)

3. **Presence of +3/2 (baseline):**
   - Check if `+3/2` exists in eigenvalues
   - Expected: PASS (already present in current code)

4. **Radius scaling:**
   - Verify eigenvalues scale as `1/R`
   - Test R=1.0 vs R=2.0: eigenvalues should halve

**RED фаза:** Test #2 (-3/2 presence) should FAIL on current code IF we decide -3/2 is required.  
**Source verification:** Must check arXiv:1103.4097 eq (6.4) before writing test expectations.

#### Этап 2: Code Fix (CONDITIONAL on paper verification)

**File:** `cc_toy_lab/spectral/dirac_s3.py`

**If k=0 is physically valid (option A):**
- Line 67: change `range(1, ...)` to `range(0, ...)`
- Add k=0 case handling for negative branch only
- Positive branch: keep k ≥ 1 (already correct)

**If paper says k ≥ 1 only (option B):**
- No code change
- Update documentation to clarify asymmetric spectrum is correct

**GREEN фаза:** Test #2 should PASS after fix (if option A)

#### Этап 3: Source Verification + Diagnostic

**Step 3A: Check arXiv:1103.4097 equation (6.4)**
- Verify: does k=0 case exist for negative branch?
- Document: what paper actually says about k range

**Step 3B: Diagnostic script (if fix applied)**
```python
"""Verify S³ Dirac low spectrum after fix."""
import sys
sys.path.insert(0, 'cc_toy_lab')
from spectral.dirac_s3 import build_s3_dirac_operator
import numpy as np

operator, _ = build_s3_dirac_operator(j_max=2, radius=1.0)
eigenvalues = np.linalg.eigvalsh(operator)
unique_eigs = np.unique(np.round(eigenvalues, 6))

expected_low = {-3.5, -2.5, -1.5, 1.5, 2.5, 3.5}  # ±7/2, ±5/2, ±3/2
actual_low = set(unique_eigs[:6])

print(f"Expected: {sorted(expected_low)}")
print(f"Actual:   {sorted(actual_low)}")
assert actual_low == expected_low, "FAIL: spectrum mismatch"
print("✓ S³ Dirac low spectrum correct")
```

**Outcome:** Either `✓ correct` or `FAIL` with specific mismatch

#### Этап 4: Rerun Decision для Gate 4B
**НЕ автоматически.**

После fix нужно решить:
- **Option A:** rerun Gate 4B v0.1.24 на S³ Dirac с исправленным spectrum
- **Option B:** отметить v0.1.23 как INCOMPLETE, продолжить с v0.1.24 как baseline

**Факторы:**
- Если fix меняет S³ Dirac eigenvalues → rerun обязателен
- Если меняет только indexing (порядок branches) → rerun опционален
- Если меняет low spectrum (добавляет ±3/2) → rerun КРИТИЧЕН

**Решение:** принимается ПОСЛЕ Этапа 3 (когда точно знаем масштаб изменений)

---

## 3. CONSTRAINTS (что НЕ делать)

### 3.1. Паузы (остаются до принятия решения)
- ❌ Batch 3–6 (W-sweep, phase space, band structure)
- ❌ Gate 4B rerun (до принятия решения)
- ❌ Gate 5 (negative controls)
- ❌ Remote/server execution

### 3.2. Сохранность данных
- ✓ Gate 4B raw outputs (`results/v0.1.23/`) — НЕ трогать
- ✓ Gate 4B interpretation frozen — НЕ пересматривать без rerun
- ✓ Negative Controls S³ — остаются paused (зависят от Dirac fix)

### 3.3. Scope
- ✓ Fix только Dirac branch indexing
- ❌ НЕ менять другие operators (ScalarLaplacian, Maxwell, etc.)
- ❌ НЕ оптимизировать производительность
- ❌ НЕ рефакторить архитектуру

---

## 4. VERIFICATION PROTOCOL

### 4.1. Pre-Fix Checklist
- [ ] Unit tests написаны и FAIL на текущем коде (RED фаза)
- [ ] Диагностический скрипт написан (не запущен)
- [ ] Commit: `test: add S3 Dirac branch indexing tests (RED)`

### 4.2. Post-Fix Checklist
- [ ] Unit tests PASS (GREEN фаза)
- [ ] `pytest tests/operators/test_dirac_branches.py -v` — 0 failures
- [ ] Diagnostic script выдает `✓ S³ Dirac branches correct`
- [ ] Commit: `fix(operators): correct S3 Dirac branch indexing for k=0`

### 4.3. Rerun Decision Checklist
- [ ] Сравнить старый vs новый low spectrum S³ Dirac
- [ ] Если eigenvalues изменились → Gate 4B rerun REQUIRED
- [ ] Если только порядок изменился → Gate 4B rerun OPTIONAL
- [ ] Документировать решение в `reports/GATE_4B_RERUN_DECISION_v0.1.24.md`

---

## 5. TIMELINE (estimate)

| Этап | Время | Токены Claude | Action |
|------|-------|---------------|--------|
| 1. Unit tests (RED) | 15 min | ~3K | Write tests, verify FAIL |
| 2. Code fix | 10 min | ~2K | Fix indexing, verify PASS |
| 3. Diagnostic | 5 min | ~1K | Run script, verify ✓ |
| 4. Rerun decision | 30 min | ~5K | Compare, document, decide |
| **Total** | **60 min** | **~11K** | — |

**Note:** реальный rerun Gate 4B (если нужен) — отдельная задача, ~6 hours + ~50K tokens.

---

## 6. SUCCESS CRITERIA

### 6.1. Минимальный успех (required)
- ✓ Unit tests PASS
- ✓ Low spectrum S³ содержит `±3/2, ±5/2, ±7/2`
- ✓ Diagnostic script выдает `✓ correct`

### 6.2. Полный успех (desired)
- ✓ Все выше
- ✓ Gate 4B rerun decision документирована
- ✓ v0.1.24 checkpoint pushed
- ✓ Negative Controls S³ готовы к запуску (если rerun не нужен)

---

## 7. ROLLBACK PLAN

Если fix сломает что-то неожиданное:
1. `git revert <commit>` — откатить fix
2. Вернуть тесты в SKIP режим
3. Документировать проблему в `reports/DIRAC_FIX_FAILURE_LOG.md`
4. Обсудить альтернативный подход (может быть проблема не в indexing)

---

## 8. NEXT STEPS (после этого плана)

1. **Validate plan** — user review этого документа
2. **Approve to proceed** — явное разрешение начать Этап 1
3. **Execute Этап 1–3** — unit tests → fix → diagnostic
4. **Gate 4B rerun decision** — отдельный документ с аргументацией
5. **Resume Negative Controls** — если rerun не нужен или завершен

---

## СТАТУС: DRAFT

Этот план документирует **ЧТО чинить** и **КАК чинить**, но:
- ❌ Код НЕ изменен
- ❌ Тесты НЕ созданы
- ❌ Commit НЕ сделан
- ❌ Push НЕ выполнен

**Waiting for:** user approval to proceed с Этапом 1.

---

**Автор:** Claude Sonnet 4.5  
**Контекст:** GeoSpectra Lab v0.1.24 development, Gate 4B postmortem
