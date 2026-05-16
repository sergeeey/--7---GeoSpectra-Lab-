# S1 v2 Stress Failure Analysis

## Executive Summary
Main classification: `weak_disorder_or_transition_regime_sensitivity`.

The stress artifacts support the following decision:

- fixed-window v2 failures are concentrated in `W=0` and the weak/transition
  disorder regime `W=1,2,4`;
- no fixed-window v2 failures occur at `W>=8`;
- therefore the current stress limitation is better classified as
  `weak_disorder_or_transition_regime_sensitivity`, not as an
  `unresolved_strong_disorder_v2_limitation`.

This memo does not change the metric, baseline, or historical record. It only
analyzes the already saved stress artifacts.

## Document status update (May 2026)

This file remains the decision memo for the **`realizations=3`** stress artifact
(`reports/RUNS/20260512-225834_s1_discretization_v2_stress`). Its headline
classification stays **`weak_disorder_or_transition_regime_sensitivity`**
because that run had **zero** fixed-window failures at `W>=8`.

For the completed **`realizations=5`** stress follow-up (one fixed-window failure
at `W=8`), see `reports/S1_V2_STRESS_FAILURE_ANALYSIS_realizations5.md`. There,
the **pre-declared binary stress rule** still labels the run
`unresolved_strong_disorder_v2_limitation` because `W>=8` failures **> 0**,
while a **separate targeted diagnostic** refines the single `W=8` outlier
mechanistically as `threshold_or_window_definition_artifact` (run
`reports/RUNS/20260513-082348_s1_v2_w8_failure_diagnostic`, memo
`reports/S1_V2_W8_FAILURE_DIAGNOSTIC.md`). That refinement **does not erase** the
`r=5` stress limitation; it **narrows interpretation** (no observed widespread
strong-disorder breakdown on the diagnostic sweep; dominant coupling to
`low_energy_count` / fixed-window definition on one ring small-size anchor).

Historical kernel-only mixed full comparison and current baseline
`v0.1.14-mvp-s2-s1-discretization-v2-full` remain documented separately and are
not rewritten by this cross-reference.

## Source Run
Run path:

```text
reports/RUNS/20260512-225834_s1_discretization_v2_stress
```

Artifacts loaded:

- `reports/RUNS/20260512-225834_s1_discretization_v2_stress/metrics.json`
- `reports/RUNS/20260512-225834_s1_discretization_v2_stress/data.npz`
- `reports/RUNS/20260512-225834_s1_discretization_v2_stress/summary.md`

Key stress metrics:

- `stress_classification=v2_limitation`
- `comparison_classification=robust_across_discretizations`
- `case_level_fixed_window_all_passed=False`
- `fixed_window_failure_cases=1429`
- `failure_count_by_family={"ring": 594, "spectral_circle": 475, "wilson_ring": 360}`
- `failure_count_by_disorder={"0": 1080, "1": 193, "2": 125, "4": 31}`
- `kernel_only_vs_fixed_window_disagreements=93`
- `ring_doubler_sensitive_cases=93`
- run used fallback `realizations=3`, not the originally requested `5`

Cross-check:

- `metrics.json` reports `1429` fixed-window failure cases
- `data.npz` also yields `1429` fixed-window failure cases
- `summary.md` matches the saved stress classification and run metadata

## Failure Split by Disorder Regime
| Regime | Disorder values | Failure count |
| --- | --- | ---: |
| `W=0` | `0` | `1080` |
| `W=1-4` | `1, 2, 4` | `349` |
| `W>=8` | `8, 12, 16` | `0` |

Binary decision input:

- Did any fixed-window v2 failures occur at `W>=8`? `No`

## Failure Tables
### By Family
| Family | Failure count |
| --- | ---: |
| `ring` | `594` |
| `spectral_circle` | `475` |
| `wilson_ring` | `360` |

### By W
| W | Failure count |
| --- | ---: |
| `0` | `1080` |
| `1` | `193` |
| `2` | `125` |
| `4` | `31` |
| `>=8` | `0` |

### By Family x W
| Family | `W=0` | `W=1` | `W=2` | `W=4` | `W>=8` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `spectral_circle` | `360` | `63` | `49` | `3` | `0` |
| `ring` | `360` | `130` | `76` | `28` | `0` |
| `wilson_ring` | `360` | `0` | `0` | `0` | `0` |

### By Alpha
| Alpha | Failure count |
| --- | ---: |
| `0.0` | `570` |
| `0.25` | `431` |
| `0.5` | `428` |

### By q
| q | Failure count |
| --- | ---: |
| `-2` | `277` |
| `-1` | `269` |
| `0` | `333` |
| `1` | `287` |
| `2` | `263` |

### By S1 Size
| S1 size | Failure count |
| --- | ---: |
| `8` | `353` |
| `16` | `366` |
| `24` | `356` |
| `32` | `354` |

### By Seed
Seed information is available in the saved artifacts.

Observed seed summary:

- unique failure seeds: `348`
- no single seed dominates the failure set
- highest repeated failure count per seed in this run: `9`

Compact top repeated seeds:

| Seed | Failure count |
| --- | ---: |
| `10832051` | `9` |
| `10832052` | `9` |
| `10832053` | `9` |
| `10832151` | `9` |
| `10832152` | `9` |
| `10832153` | `9` |
| `11632051` | `9` |
| `11632052` | `9` |
| `11632053` | `9` |
| `11632151` | `9` |

## Strong-Disorder Decision
Did any fixed-window v2 failures occur at `W>=8`?

**No.**

Direct evidence:

- `failure_count_by_disorder` contains only `W=0,1,2,4`
- the `data.npz` case-level array also gives `0` fixed-window failures at
  `W>=8`

Decision classification:

```text
weak_disorder_or_transition_regime_sensitivity
```

## Interpretation
The stress limitation is dominated by two regimes:

1. `W=0`, which should not be interpreted as failure of localization under
   disorder because there is no disorder.
2. weak/transition disorder `W=1,2,4`, which is the only nonzero-disorder
   regime where fixed-window v2 failures appear in this run.

What this means:

- the saved stress limitation is real at the case level;
- but it is not currently a strong-disorder limitation;
- the present evidence points to no-disorder / weak-disorder /
  transition-regime sensitivity rather than failure of the v2 gate inside the
  stronger scanned disorder regime.

Ring interpretation remains separate:

- `ring_doubler_sensitive_cases=93` should stay classified as a
  kernel-window artifact;
- these disagreement cases must not be confused with fixed-window v2 failure;
- they do not change the strong-disorder decision because fixed-window failures
  at `W>=8` are absent.

## Historical Results Preserved
The historical record remains unchanged:

- the historical kernel-only full comparison remains
  `mixed_or_limiting`:
  `reports/RUNS/20260512-191838_s1_discretization_comparison_full`
- the `v0.1.14` fixed-window family-level result remains valid:
  `reports/RUNS/20260512-203723_s1_discretization_comparison_full`
- the later independent rerun remains valid:
  `reports/RUNS/20260512-211633_s1_discretization_comparison_full`
- the stress-test adds a case-level limitation; it is not a rewrite of the
  older family-level or historical kernel-only results
- the baseline is not promoted by this memo

## Scientific Non-Claims
This does not prove continuum compactification.
This does not prove `S6` or `S3 x S6`.
This does not derive Standard Model physics.
This does not prove physical chirality.
This does not bypass Witten/Lichnerowicz.

## Recommended Next Step

Completed outside the interactive path:

1. `realizations=5` stress rerun is saved as
   `reports/RUNS/20260513-001436_s1_discretization_v2_stress` (memo:
   `reports/S1_V2_STRESS_FAILURE_ANALYSIS_realizations5.md`).
2. The isolated `W=8` outlier received a targeted diagnostic
   (`reports/RUNS/20260513-082348_s1_v2_w8_failure_diagnostic`,
   `reports/S1_V2_W8_FAILURE_DIAGNOSTIC.md`).

Ongoing hygiene:

1. keep the current metric unchanged unless a separate, explicit baseline review
   promotes a new tag;
2. preserve the historical kernel-only mixed result and the current baseline
   unchanged when interpreting stress vs family-aggregate summaries;
3. treat stress-level binary labels and targeted mechanistic diagnoses as
   **different layers** of documentation (see the `realizations=5` memo).
