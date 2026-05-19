# Practical Applicability Stress Test — v0.1.18

## Executive Summary

GeoSpectra is practically useful as a falsification-first validation harness for toy finite-lattice spectral diagnostics **with caveats**. The sprint supports practical use for catching numerical artifacts and documenting failures before interpretation. It does not support any physical compactification claim.

## What “Practical Applicability” Means Here

GeoSpectra is useful if it helps detect numerical artifacts before physical interpretation. Practical usefulness here means operator construction checks, artifact injection response, ablation sensitivity, and small portability smoke tests.

## Experiment 1 — S¹ Calibration Threshold Repair

The v0.1.18 repair attempt remained 15/18. The replacement spectral-gap criterion also failed 0/3, reframing the caveat as an ill-posed lattice-size comparison rather than a simple threshold bug.

## Experiment 2 — Expanded Artifact Injection

3/8 artifact classes were caught; 5 were missed or ambiguous.

## Experiment 3 — Prospective FL Ablation

All ablated variants lost diagnostic specificity in the small prospective matrix. The full FL variant retained all pilot scenario controls.

## Experiment 4 — Cross-Geometry Smoke Test

S3xS1_toy_proxy: 60/60 constructed; S2xS2_toy_proxy: 60/60 constructed. These are portability smoke tests only.

## What Passed

- S¹ Hermiticity, spectral symmetry, and no-false-localization checks remain passing.
- Expanded artifact injection caught 3/8 deliberately injected artifact classes and exposed 5 missed/ambiguous classes.
- Prospective ablation showed each removed rung loses a diagnostic scenario.
- Cross-geometry toy proxy operators constructed and passed basic shape/Hermiticity gates in smoke tests.

## What Failed or Remains Ambiguous

- S¹ lattice-size comparison remains failed/ill-posed for calibration.
- Any expanded artifact marked `missed_or_ambiguous` requires follow-up before stronger harness claims.
- Cross-geometry tests do not validate geometry or physics; they only test harness portability.

## What GeoSpectra Is Practically Useful For

- Detecting numerical/operator artifacts in toy finite-lattice spectral diagnostics.
- Making failed checks visible instead of hiding them.
- Comparing validation-ladder controls against known injected failures.
- Producing falsification-first reports before physical interpretation.

## What GeoSpectra Is NOT Yet Useful For

- Physical compactification validation.
- S6 or S3xS6 validation.
- Standard Model derivation.
- Chirality proof.
- Witten/Lichnerowicz bypass.
- Continuum convergence claims.

## Questions for Tom / CAMP

1. Should S¹ calibration drop cross-size stability entirely and keep only within-size gates?
2. Which artifact classes should be promoted into a maintained regression suite?
3. Are toy S3xS1/S2xS2 proxies useful as harness smoke tests, or should they be replaced by stricter analytic fixtures?
4. What minimum external-review evidence is needed before calling this a public methodology result?

## Final Verdict

`practical_applicability_supported_with_caveats`

The harness is practically useful for falsification-first toy diagnostics, but only with explicit caveats and no physical overclaims.
