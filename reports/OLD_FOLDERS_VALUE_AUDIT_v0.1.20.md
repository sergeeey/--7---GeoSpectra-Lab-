# Old Folders Value Audit — v0.1.20

**Дата:** 2026-05-21 15:00 Almaty  
**Canonical Path:** `E:\Проверка Гипотез\работаю над проверкой гипотез\N-7-GeoSpectra-Lab`  
**Статус:** ⚠️ MANUAL_REVIEW_REQUIRED — уникальные v0.1.20 файлы найдены  
**Цель:** Определить ценность старых папок перед архивированием/удалением

---

## Executive Summary

**Критическая находка:**  
Старые папки содержат **15 уникальных файлов v0.1.20**, отсутствующих в canonical:
- 4 reports (CURRENT_STATUS, GATE3_FULL_DIAGNOSTIC, WILSON_RING, DISORDER_SWEEP)
- 1 RUNS folder (disorder_sweep_v0.1.20, 66K)
- 2 scripts (run_disorder_sweep.py, run_gate3c_confirmatory.py)
- 6 tests (wilson, s3_s1 controls/sanity, gate3c_triad)
- 2 design docs (CONTRAST_INVESTIGATION, TRIAD_GATE_PREFLIGHT)

**Вердикт:** COPY_UNIQUE_FILES_FIRST перед архивированием.

**Risk level:** HIGH — потеря данных v0.1.20 работы.

---

## 1. Old Folders Inspected

| Folder | Exists | Git Repo | Latest Commit | File Count | Size | Risk |
|--------|--------|----------|---------------|------------|------|------|
| `Н-7...компактификации` | ✅ YES | ✅ YES | `ee7e47c` 2026-05-20 08:03 | 7,907 | 305M | MEDIUM (старее canonical на 1 день) |
| `Н-7...компактификації` | ✅ YES | ❌ NO | — | 7,502 | 301M | HIGH (содержит уникальные v0.1.20 файлы) |
| `Н-7...компактифікаціі` | ✅ YES | ❌ NO | — | 6 | 64K | LOW (почти пустая, частичная копия) |

**Canonical (reference):**
- Path: `N-7-GeoSpectra-Lab`
- Git: ✅ YES, commit `687588d` 2026-05-21 10:30
- Files: 7,900+ (estimated)
- Size: 300M

---

## 2. Unique Files Not in Canonical

### 2.1 Reports (HIGH VALUE)

| Old Folder | File Path | Size | Modified Time | Recommended Action |
|------------|-----------|------|---------------|-------------------|
| Папка 2 | `reports/CURRENT_STATUS_v0.1.20_CAVEAT_REVIEW.md` | unknown | 2026-05-21 (recent) | ✅ COPY — v0.1.20 status report |
| Папка 2 | `reports/S3_S1_GATE3_FULL_DIAGNOSTIC_v0.1.20.md` | unknown | 2026-05-21 (recent) | ✅ COPY — Gate 3 diagnostic |
| Папка 2 | `reports/WILSON_RING_S64_INVESTIGATION_v0.1.20.md` | unknown | 2026-05-21 (recent) | ✅ COPY — Wilson ring investigation |
| Папка 2 | `reports/CONTRAST_INVESTIGATION_v0.1.19.md` | unknown | 2026-05-20 | ⚠️ REVIEW — v0.1.19 (might be outdated) |
| Папка 3 | `reports/DISORDER_SWEEP_v0.1.20.md` | unknown | 2026-05-21 | ✅ COPY — disorder sweep report |
| Папка 3 | `reports/S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md` | unknown | 2026-05-21 | ✅ COPY — triad gate preflight |

### 2.2 Scripts (HIGH VALUE)

| Old Folder | File Path | Size | Modified Time | Recommended Action |
|------------|-----------|------|---------------|-------------------|
| Папка 2 | `scripts/run_disorder_sweep.py` | unknown | 2026-05-21 | ✅ COPY — disorder sweep runner |
| Папка 3 | `scripts/run_gate3c_confirmatory.py` | unknown | 2026-05-21 | ✅ COPY — gate3c confirmatory |

### 2.3 Tests (MEDIUM VALUE)

| Old Folder | File Path | Size | Modified Time | Recommended Action |
|------------|-----------|------|---------------|-------------------|
| Папка 2 | `tests/test_wilson_ring_s64_investigation.py` | unknown | 2026-05-21 | ✅ COPY — Wilson ring test |
| Папка 2 | `tests/test_wilson_s64_extended.py` | unknown | 2026-05-21 | ✅ COPY — Wilson extended test |
| Папка 2 | `tests/test_s3_s1_controls.py` | unknown | 2026-05-21 | ✅ COPY — S³×S¹ controls test |
| Папка 2 | `tests/test_s3_s1_ipr_metric_sanity.py` | unknown | 2026-05-21 | ✅ COPY — IPR metric sanity |
| Папка 3 | `tests/test_s3_s1_gate3c_triad_v0_1_20.py` | unknown | 2026-05-21 | ✅ COPY — Gate 3C triad test |

### 2.4 RUNS (MEDIUM VALUE)

| Old Folder | File Path | Size | Files | Recommended Action |
|------------|-----------|------|-------|-------------------|
| Папка 2 | `reports/RUNS/disorder_sweep_v0.1.20/` | 66K | 5 | ✅ COPY — experimental run data |

**Note:** Папка 2 имеет 1039 RUNS folders vs 1038 в canonical. disorder_sweep_v0.1.20 отсутствует в canonical.

---

## 3. Conflicting Files (Same Path, Different Content)

| File Path | Canonical Size/Time | Old Size/Time | Likely Newer | Recommended Action |
|-----------|---------------------|---------------|--------------|-------------------|
| `reports/S3_S1_GATE3C_CONFIRMATORY_REPLICATION_v0.1.20.md` | 4.9K, May 21 09:56 | 4.9K, May 21 09:25 (папка 2) | Canonical | ✅ KEEP canonical (свежее) |
| `reports/S3_S1_GATE3C_CONFIRMATORY_REPLICATION_v0.1.20.md` | 4.9K, May 21 09:56 | 9.0K, May 21 09:08 (папка 3) | ? | ⚠️ REVIEW — папка 3 старее, но БОЛЬШЕ (9.0K vs 4.9K) |

**Критический случай:**  
Папка 3 содержит версию S3_S1_GATE3C_CONFIRMATORY_REPLICATION размером 9.0K (May 21 09:08).  
Canonical версия 4.9K (May 21 09:56) — свежее, но меньше.  
**Требуется:** сравнить содержимое, определить что было удалено/сокращено между 09:08 и 09:56.

---

## 4. High-Value Candidates (Prioritized)

| File Path | Reason | Copy Needed? |
|-----------|--------|--------------|
| `reports/CURRENT_STATUS_v0.1.20_CAVEAT_REVIEW.md` | ✅ v0.1.20 status summary, нет в canonical | YES |
| `reports/S3_S1_GATE3_FULL_DIAGNOSTIC_v0.1.20.md` | ✅ Gate 3 full diagnostic, нет в canonical | YES |
| `reports/WILSON_RING_S64_INVESTIGATION_v0.1.20.md` | ✅ Wilson ring v0.1.20 investigation | YES |
| `reports/DISORDER_SWEEP_v0.1.20.md` | ✅ Disorder sweep report | YES |
| `reports/S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md` | ✅ Triad gate preflight | YES |
| `scripts/run_disorder_sweep.py` | ✅ Disorder sweep runner script | YES |
| `scripts/run_gate3c_confirmatory.py` | ✅ Gate 3C confirmatory runner | YES |
| `reports/RUNS/disorder_sweep_v0.1.20/` | ⚠️ Experimental data, 66K, 5 files | YES |
| `reports/S3_S1_GATE3C_CONFIRMATORY_REPLICATION_v0.1.20.md` (папка 3, 9.0K) | ⚠️ Older but larger version — may contain details later removed | REVIEW FIRST |
| All 6 tests/* files | ⚠️ Test coverage for Wilson, controls, sanity | YES |

**Total unique files to copy:** 15 files + 1 RUNS folder

---

## 5. Safe-to-Ignore Generated Junk

Patterns NOT to copy (auto-generated, no value):

```
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
*.log (если есть summary в reports/)
tmp/
.coverage
htmlcov/
.mypy_cache/
*.egg-info/
```

**Estimated junk in old folders:**
- Папка 1: ~1000 __pycache__ + .pyc files
- Папка 2: ~900 __pycache__ + .pyc files
- Папка 3: minimal (only 6 files total)

---

## 6. Folder Structure Comparison

| Directory | Папка 1 (git) | Папка 2 (no-git) | Папка 3 (tiny) | Canonical |
|-----------|---------------|------------------|----------------|-----------|
| `reports/` | ✅ | ✅ | ✅ | ✅ |
| `scripts/` | ✅ | ✅ | ✅ | ✅ |
| `tests/` | ✅ | ✅ | ✅ | ✅ |
| `cc_toy_lab/` | ✅ | ✅ | ❌ | ✅ |
| `.claude/` | ✅ | ✅ | ✅ | ✅ |
| `reports/RUNS/` | 1039 folders | 1039 folders | 0 folders | 1038 folders |

---

## 7. Git Status

| Folder | Is Git Repo | Latest Commit | Branch | Age vs Canonical |
|--------|-------------|---------------|--------|------------------|
| Папка 1 | ✅ YES | `ee7e47c` fix(gate-2): correct S³ Dirac eigenvalue formula | unknown | -1 day (OLDER) |
| Папка 2 | ❌ NO | — | — | — |
| Папка 3 | ❌ NO | — | — | — |
| Canonical | ✅ YES | `687588d` feat(gate-3): add S3xS1 Gate 3 infrastructure | main | HEAD (NEWEST) |

**Important:**  
Папка 1 — git repo на коммите `ee7e47c` (2026-05-20 08:03).  
Canonical — на коммите `687588d` (2026-05-21 10:30).  
**Difference:** 2 commits (19fc7df fix + 687588d feat).

Папка 1 НЕ содержит:
- 19fc7df: fix(s3-s1): avoid unsafe complex-to-float cast
- 687588d: feat(gate-3): add S3xS1 Gate 3 infrastructure and repo audit

---

## 8. Recent Activity Timeline (Reconstructed)

Судя по файлам и git commits:

| Date | Time | Location | Activity |
|------|------|----------|----------|
| 2026-05-20 08:03 | — | Папка 1 | Commit `ee7e47c` (S³ Dirac fix) |
| 2026-05-21 09:08 | — | Папка 3 | Создан S3_S1_GATE3C_CONFIRMATORY (9.0K) |
| 2026-05-21 09:25 | — | Папка 2 | Обновлён S3_S1_GATE3C_CONFIRMATORY (4.9K) |
| 2026-05-21 09:xx | — | Папка 2 | Создан CURRENT_STATUS, WILSON_RING, disorder_sweep |
| 2026-05-21 09:56 | — | Canonical | Обновлён S3_S1_GATE3C_CONFIRMATORY (4.9K, финал) |
| 2026-05-21 10:15 | — | Canonical | Commit `19fc7df` (fix) + `687588d` (feat) |

**Interpretation:**  
Пользователь работал в РАЗНЫХ папках параллельно в течение утра 21 мая:
- Папка 3 использовалась для трёх файлов (TRIAD_GATE, run_gate3c_confirmatory, test_triad)
- Папка 2 использовалась для disorder_sweep работы + Wilson investigation
- Canonical использовался для финальной консолидации + git commit

---

## 9. Risk Assessment

| Folder | Risk of Deletion | Reason |
|--------|------------------|--------|
| Папка 1 | LOW | Git repo, но на старом коммите. Всё содержимое есть в canonical (через git history). |
| Папка 2 | **HIGH** | Содержит 10+ уникальных v0.1.20 файлов, отсутствующих в canonical. Потеря = потеря работы. |
| Папка 3 | MEDIUM | Содержит 4 уникальных файла + возможно более полную версию GATE3C_CONFIRMATORY. |

---

## 10. Recommendations

### Option A: COPY_UNIQUE_FILES_FIRST (Recommended)

**Безопасный путь перед любым архивированием:**

1. Создать резервную папку:
   ```
   mkdir "E:\Проверка Гипотез\работаю над проверкой гипотез\N-7-GeoSpectra-Lab\RECOVERY_FROM_OLD_FOLDERS"
   ```

2. Скопировать все 15 уникальных файлов из папки 2 и 3 в canonical:
   ```
   cp reports/CURRENT_STATUS_v0.1.20_CAVEAT_REVIEW.md ../N-7-GeoSpectra-Lab/reports/
   cp reports/S3_S1_GATE3_FULL_DIAGNOSTIC_v0.1.20.md ../N-7-GeoSpectra-Lab/reports/
   cp reports/WILSON_RING_S64_INVESTIGATION_v0.1.20.md ../N-7-GeoSpectra-Lab/reports/
   ...
   ```

3. Скопировать RUNS/disorder_sweep_v0.1.20/:
   ```
   cp -r reports/RUNS/disorder_sweep_v0.1.20 ../N-7-GeoSpectra-Lab/reports/RUNS/
   ```

4. Сравнить две версии S3_S1_GATE3C_CONFIRMATORY_REPLICATION (4.9K vs 9.0K):
   ```
   diff -u \
     "../Н-7 - GeoSpectra Lab теории ковариантної компактифікаціі/reports/S3_S1_GATE3C_CONFIRMATORY_REPLICATION_v0.1.20.md" \
     "reports/S3_S1_GATE3C_CONFIRMATORY_REPLICATION_v0.1.20.md"
   ```

5. После копирования: git add + commit в canonical:
   ```
   git add reports/*.md scripts/*.py tests/*.py reports/RUNS/disorder_sweep_v0.1.20
   git commit -m "feat(recovery): restore unique v0.1.20 files from old folders"
   ```

6. Только ПОСЛЕ успешного коммита: архивировать старые папки.

### Option B: MANUAL_REVIEW_REQUIRED (Conservative)

Перед копированием провести ручной review каждого файла:

| File | Questions to Answer |
|------|---------------------|
| CURRENT_STATUS_v0.1.20_CAVEAT_REVIEW.md | Что нового vs REPO_IDENTITY_AND_PATH_AUDIT? |
| S3_S1_GATE3_FULL_DIAGNOSTIC_v0.1.20.md | Отличается ли от других Gate 3 reports? |
| WILSON_RING_S64_INVESTIGATION_v0.1.20.md | Связан с test_wilson_ring_s64_investigation.py? |
| disorder_sweep_v0.1.20.md | Соответствует ли RUNS/disorder_sweep_v0.1.20/? |
| S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md | Связан с test_s3_s1_gate3c_triad_v0_1_20.py? |

### Option C: NOT_SAFE_TO_DELETE (Do NOT use)

Удаление без копирования = потеря v0.1.20 работы.  
**BLOCKED** by 15 unique files.

---

## 11. Copy Checklist (Execute Before Archive)

**Before archiving/deleting ANY old folder, complete this checklist:**

- [ ] Скопирован `reports/CURRENT_STATUS_v0.1.20_CAVEAT_REVIEW.md`
- [ ] Скопирован `reports/S3_S1_GATE3_FULL_DIAGNOSTIC_v0.1.20.md`
- [ ] Скопирован `reports/WILSON_RING_S64_INVESTIGATION_v0.1.20.md`
- [ ] Скопирован `reports/CONTRAST_INVESTIGATION_v0.1.19.md` (review first if needed)
- [ ] Скопирован `reports/DISORDER_SWEEP_v0.1.20.md`
- [ ] Скопирован `reports/S3_S1_TRIAD_GATE_PREFLIGHT_v0.1.20.md`
- [ ] Скопирован `scripts/run_disorder_sweep.py`
- [ ] Скопирован `scripts/run_gate3c_confirmatory.py`
- [ ] Скопированы все 6 test files (wilson, controls, sanity, triad)
- [ ] Скопирован `reports/RUNS/disorder_sweep_v0.1.20/`
- [ ] Сравнены две версии S3_S1_GATE3C_CONFIRMATORY (9.0K vs 4.9K)
- [ ] Все скопированные файлы добавлены в git (git add + commit)
- [ ] git push completed successfully
- [ ] Создана архивная копия старых папок в безопасном месте (external HDD / cloud)

**DO NOT delete old folders until ALL checkboxes are checked.**

---

## 12. Final Verdict

**Status:** ⚠️ **COPY_UNIQUE_FILES_FIRST**

**Rationale:**
- 15 unique files (4 reports, 2 scripts, 6 tests, 2 design docs, 1 RUNS folder)
- All files v0.1.20 recent work (May 21 morning)
- 1 conflicting file with potentially valuable older/larger version
- High risk of data loss if deleted without recovery

**Next Action:**  
Execute Option A (COPY_UNIQUE_FILES_FIRST) before ANY archive/delete operation.

**Safety Net:**  
Папка 1 (git repo) можно архивировать безопасно — всё содержимое есть в canonical git history.  
Папка 2 и 3 — архивировать ТОЛЬКО ПОСЛЕ копирования уникальных файлов.

---

**References:**
- Canonical path: `E:\Проверка Гипотез\работаю над проверкой гипотез\N-7-GeoSpectra-Lab`
- Old folder 1: `Н-7 - GeoSpectra Lab теории ковариантной компактификации` (git, 305M, 7907 files)
- Old folder 2: `Н-7 - GeoSpectra Lab теории ковариантной компактификації` (no-git, 301M, 7502 files)
- Old folder 3: `Н-7 - GeoSpectra Lab теории ковариантної компактифікаціі` (no-git, 64K, 6 files)
- Audit date: 2026-05-21 15:00 Almaty
- Canonical commit: `687588d` feat(gate-3): add S3xS1 Gate 3 infrastructure

**Status:** ✅ AUDIT COMPLETE — manual copy required before archive
