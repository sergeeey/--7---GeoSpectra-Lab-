# Repo Identity and Path Audit — v0.1.20

**Дата:** 2026-05-21 05:45 Almaty  
**Статус:** 🔍 AUDIT COMPLETE — cleanup done, rename BLOCKED  
**Цель:** Стабилизация локального репозитория после миграции + оценка возможности переименования remote

---

## Executive Summary

**Текущее состояние:**
- ✅ Локальная папка стабилизирована: `N-7-GeoSpectra-Lab` (чистый ASCII)
- ✅ Generated junk очищен (cache, logs, backups)
- ⚠️ Remote URL содержит закодированную кириллицу: `--7---GeoSpectra-Lab-`
- 🔴 **Rename BLOCKED:** uncommitted changes (1 modified + 4 untracked files)

**Рекомендация:** Сначала commit текущие изменения, затем переименовать remote

---

## 1. Canonical Local Path

```
E:\Проверка Гипотез\работаю над проверкой гипотез\N-7-GeoSpectra-Lab
```

**Характеристики:**
- ✅ Чистый ASCII (без кириллицы)
- ✅ Git repository (branch: main)
- ✅ Синхронизирован с origin (последний коммит: 9be68c5)
- ⚠️ Uncommitted changes: 7 файлов

---

## 2. Old Folders Found

### 2.1 Git Repositories (Same Remote)

| Path | Git Status | Remote | Files |
|------|------------|--------|-------|
| `Н-7 - GeoSpectra Lab теории ковариантной компактификации` | ✅ Git repo | `https://github.com/sergeeey/--7---GeoSpectra-Lab-.git` | Кириллица в имени |

**Риск:** Дублирование репозитория, возможны конфликты при работе

### 2.2 Non-Git Directories

| Path | Status | Size |
|------|--------|------|
| `Н-7 - GeoSpectra Lab теории ковариантной компактификації` | Not a git repo | Unknown |
| `Н-7 - GeoSpectra Lab теории ковариантної компактифікаціі` | Not a git repo | Unknown |

**Тип:** Копии папок (украинская транскрипция), вероятно созданы ошибочно

---

## 3. Current Remote URL

**Origin:**
```
https://github.com/sergeeey/--7---GeoSpectra-Lab-.git
```

**Проблема:** Кириллица "Н-7" закодирована как `--7--` (URL encoding artifacts)

**Branch:** `main`

**Tags (последние 5):**
- `v0.1.19-track-c-gate-1`
- `v0.1.18-practical-applicability`
- `v0.1.17-validation-hardening`
- `v0.1.16-methodology-review-draft`
- `v0.1.15-s2-s1-product-discretized-full`

---

## 4. Recommended Clean Remote/Repo Name

**Текущее (ПЛОХО):**
```
https://github.com/sergeeey/--7---GeoSpectra-Lab-.git
```

**Рекомендуемое (ХОРОШО):**
```
https://github.com/sergeeey/N-7-GeoSpectra-Lab.git
```

**Обоснование:**
1. Чистый ASCII (без URL encoding)
2. Соответствует локальному имени `N-7-GeoSpectra-Lab`
3. Кириллица "Н" заменена на латинскую "N"
4. Короткое, читаемое, без артефактов

**Альтернативные варианты:**
- `geospectra-lab` (короткое, без префикса)
- `n7-geospectra` (lowercase, дефис вместо числа)
- `covariant-compactification-lab` (описательное, без кода)

---

## 5. Is Rename Safe Now?

**Статус:** 🔴 **BLOCKED**

### Blocking Reasons

| # | Reason | Impact | Resolution |
|---|--------|--------|------------|
| 1 | **Uncommitted changes** | 7 файлов (1 M + 4 ?? + 2 D) | Commit or stash before rename |
| 2 | **Old git repo exists** | `Н-7 - GeoSpectra...` points to same remote | Archive or delete before rename |
| 3 | **GitHub repo rename requires admin** | Must rename on GitHub first | Manual GitHub UI operation |

### Current Uncommitted Changes

```
 D .claude/settings.local.json
 D .claude/verification_plan.md
 M cc_toy_lab/spectral/s3_s1_product_discretized.py
?? scripts/run_gate3_full.py
?? scripts/s3_s1_gate3_profiles.py
?? scripts/s3_s1_product_discretized_ipr_smoke.py
?? tests/test_s3_s1_product_discretized_ipr_smoke.py
```

**Recommended:** Commit Gate 3 infrastructure first (eigenvalue fix + scripts/tests)

---

## 6. Cleanup Status

### ✅ Completed

| Item | Status | Details |
|------|--------|---------|
| Critical files restored | ✅ DONE | `.gitignore`, `.zenodo.json`, `GATE_2_PROGRESS_v0.1.19.md` |
| `__pycache__/` removed | ✅ DONE | 0 directories remaining |
| `*.pyc` removed | ✅ DONE | 0 files remaining |
| `ipr_smoke_reduced.log` removed | ✅ DONE | — |
| Backup files removed | ✅ DONE | `*.backup` deleted |
| `tmp/` removed | ✅ DONE | — |
| Duplicate `gate3c_confirmatory_v0.1.20/` | ✅ NOT FOUND | No duplicate outside RUNS |
| Generated junk | ✅ CLEAN | All cache/logs removed |

### 📋 Preserved

| Item | Status | Reason |
|------|--------|--------|
| `reports/RUNS/*` | ✅ KEPT | Ignored by `.gitignore`, not deleted |
| `reports/RUNS/.gitkeep` | ✅ KEPT | Tracks empty RUNS directory |
| `reports/*.md` | ✅ KEPT | All reports preserved |
| `scripts/*.py` | ✅ KEPT | 4 new Gate 3 scripts |
| `tests/*.py` | ✅ KEPT | 1 new Gate 3 test |

---

## 7. Remaining Uncommitted Changes

### Modified Files (1)

| File | Change Type | Classification | Commit Ready? |
|------|-------------|----------------|---------------|
| `cc_toy_lab/spectral/s3_s1_product_discretized.py` | Eigenvalue fix | ✅ KEEP_AND_COMMIT | YES |

**Diff:**
```diff
- d = np.asarray(d_s3, dtype=float)
+ # S³ Dirac is Hermitian (complex dtype) but eigenvalues are real
+ assert np.allclose(d_s3.imag, 0, atol=1e-14), "S³ Dirac operator should be real-valued"
+ d = d_s3.real
```

### Untracked Files (4)

| File | Size | Classification | Commit Ready? |
|------|------|----------------|---------------|
| `scripts/run_gate3_full.py` | 1.3K | ✅ KEEP_AND_COMMIT | YES |
| `scripts/s3_s1_gate3_profiles.py` | 2.8K | ✅ KEEP_AND_COMMIT | YES |
| `scripts/s3_s1_product_discretized_ipr_smoke.py` | 14K | ✅ KEEP_AND_COMMIT | YES |
| `tests/test_s3_s1_product_discretized_ipr_smoke.py` | 4.8K | ✅ KEEP_AND_COMMIT | YES |

**Purpose:** Gate 3 full diagnostic infrastructure (S³×S¹ smoke test + profiles)

### Deleted Files (2)

| File | Status | Classification | Action |
|------|--------|----------------|--------|
| `.claude/settings.local.json` | D | SAFE_TO_DELETE | Do not commit deletion |
| `.claude/verification_plan.md` | D | SAFE_TO_DELETE | Do not commit deletion (v0.1.15 plan, project on v0.1.19) |

---

## 8. Next Steps

### Step 1: Commit Current Work (REQUIRED before rename)

```bash
# Stage only valid changes
git add cc_toy_lab/spectral/s3_s1_product_discretized.py
git add scripts/run_gate3_full.py scripts/s3_s1_gate3_profiles.py scripts/s3_s1_product_discretized_ipr_smoke.py
git add tests/test_s3_s1_product_discretized_ipr_smoke.py

# Commit
git commit -m "feat(gate-3): add Gate 3 infrastructure and eigenvalue fix

- Fix S³ Dirac operator: explicit .real extraction with assert
- Add Gate 3 full diagnostic runner (1440 cases)
- Add Gate 3 profiles (tiny/medium/full)
- Add S³×S¹ IPR smoke test script and pytest tests

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### Step 2: Clean Unstaged Deletions

```bash
# Reset deleted files from staging (do not commit deletion)
git restore --staged .claude/settings.local.json .claude/verification_plan.md
```

### Step 3: Archive/Delete Old Folders

**Option A: Archive old git repo**
```bash
# Move to archive location (outside work directory)
mv "../Н-7 - GeoSpectra Lab теории ковариантной компактификации" "E:/Archive/GeoSpectra-old-$(date +%Y%m%d)"
```

**Option B: Delete old git repo (after backup confirmation)**
```bash
# ONLY if you have recent backup or pushed to GitHub
rm -rf "../Н-7 - GeoSpectra Lab теории ковариантной компактификации"
```

**Delete non-git copies:**
```bash
rm -rf "../Н-7 - GeoSpectra Lab теории ковариантной компактификації"
rm -rf "../Н-7 - GeoSpectra Lab теории ковариантної компактифікаціі"
```

### Step 4: Rename GitHub Repository (MANUAL)

1. Open: `https://github.com/sergeeey/--7---GeoSpectra-Lab-`
2. Go to: Settings → Repository name
3. Rename: `--7---GeoSpectra-Lab-` → `N-7-GeoSpectra-Lab`
4. Confirm: Rename button

**GitHub auto-redirects:** Old URL will redirect to new for ~1 year

### Step 5: Update Local Remote

```bash
# After GitHub rename, update local remote
git remote set-url origin https://github.com/sergeeey/N-7-GeoSpectra-Lab.git

# Verify
git remote -v
```

### Step 6: Push (ONLY after rename complete)

```bash
git push origin main --tags
```

---

## 9. Risks and Mitigations

### Risk 1: Old Git Repo Causes Confusion

**Probability:** High (если не удалить)  
**Impact:** Accidental commits to wrong repo

**Mitigation:**
1. Archive or delete `Н-7 - GeoSpectra...` folder
2. Always check `pwd` before git commands
3. Add bookmark/shortcut to canonical `N-7-GeoSpectra-Lab`

### Risk 2: GitHub Rename Breaks Clone Links

**Probability:** Low (GitHub redirects)  
**Impact:** External links may break after 1 year

**Mitigation:**
1. GitHub auto-redirects old URL → new URL
2. Update links in papers/docs manually
3. Notify collaborators (if any)

### Risk 3: Uncommitted Changes Lost During Rename

**Probability:** Zero (if follow Step 1)  
**Impact:** Data loss

**Mitigation:**
1. **Commit before rename** (Step 1 mandatory)
2. Never rename with dirty working tree
3. Backup `.git` folder before major operations

---

## 10. Decision Matrix

| Condition | Can Rename Now? | Action |
|-----------|-----------------|--------|
| Uncommitted changes exist | ❌ NO | Commit first (Step 1) |
| Old git repo exists | ⚠️ CAUTION | Archive/delete first (Step 3) |
| Working tree clean | ✅ YES | Proceed with GitHub rename (Step 4) |
| Already pushed to GitHub | ✅ SAFE | Rename preserves history |

**Current state:** ❌ **BLOCKED** (uncommitted changes)

---

## 11. Summary

**Local path:** ✅ Stabilized (`N-7-GeoSpectra-Lab`)  
**Remote URL:** ⚠️ Contains encoding artifacts (`--7---GeoSpectra-Lab-`)  
**Old folders:** 🔴 3 duplicates found (1 git repo, 2 copies)  
**Uncommitted changes:** 🔴 7 files (1 M + 4 ?? + 2 D)  
**Rename status:** 🔴 **BLOCKED** until commit + old folder cleanup

**Next action:** Commit Gate 3 infrastructure (Step 1), then proceed with Steps 2-6

---

**References:**
- Last commit: `9be68c5 feat(gate-3c): confirmatory finite-lattice evidence at W=20`
- Current tag: `v0.1.19-track-c-gate-1`
- Branch: `main`
- Remote: `https://github.com/sergeeey/--7---GeoSpectra-Lab-.git`

**Status:** AUDIT COMPLETE — ready for commit and rename workflow
