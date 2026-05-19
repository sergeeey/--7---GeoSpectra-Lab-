# Expanded Artifact Injection Matrix — v0.1.18

**Scope:** practical applicability stress test for toy finite-lattice spectral diagnostics.  
**Claims boundary:** No physical compactification claim. No S6 or S3xS6 validation. No Standard Model derivation. No chirality proof. No Witten/Lichnerowicz bypass. No continuum convergence claim.

## Summary

- Artifacts tested: 8
- Caught: 3
- Missed or ambiguous: 5

| Artifact | Expected failure mode | Expected gate/control | Observed metric | Verdict | Notes |
|---|---|---|---|---|---|
| near-Hermitian perturbation | Tiny anti-Hermitian component should trip strict Hermiticity residual if above 1e-9. | Hermiticity gate | hermiticity_residual=1.07e-07; window_relative_shift=1.62e-08; low_energy_max_ipr=0.129; operator_norm_ratio=1 | caught | Subtle perturbation deliberately set at 1e-8 scale. |
| eigenvalue window manipulation | Low-energy window is shifted without breaking Hermiticity. | Window-shift diagnostic | hermiticity_residual=0; window_relative_shift=0.138; low_energy_max_ipr=0.129; operator_norm_ratio=1.01 | missed_or_ambiguous |  |
| seed instability | Strong seed dependence in low-energy statistic. | Reproducibility / multi-seed control | seed_window_relative_shift=0.04 | missed_or_ambiguous | Prospective two-seed stress only; not a full distributional test. |
| boundary-condition flip | PBC/APBC swap changes low-energy window; flux/boundary response should notice. | Boundary/flux response control | pbc_apbc_window_relative_shift=0.121 | missed_or_ambiguous | This checks sensitivity, not physical boundary validation. |
| spectral degeneracy injection | Artificial exact degeneracy should be visible as near-zero adjacent gap. | Degeneracy/min-gap diagnostic | hermiticity_residual=0; window_relative_shift=1.3e-15; low_energy_max_ipr=0.129; operator_norm_ratio=1 | caught |  |
| fake localized eigenvector | Localized low-energy vector should raise low-energy IPR. | IPR/localization control | hermiticity_residual=0; window_relative_shift=2.17e-16; low_energy_max_ipr=0.157; operator_norm_ratio=1 | missed_or_ambiguous |  |
| random sparse noise | Sparse Hermitian noise may preserve basic gates but perturb windows. | Window-shift / reproducibility controls | hermiticity_residual=0; window_relative_shift=0.00993; low_energy_max_ipr=0.128; operator_norm_ratio=1 | missed_or_ambiguous | If missed, subtle Hermitian sparse noise may require stronger multi-seed/window controls. |
| operator scaling distortion | Global scaling preserves eigenvectors and many shape/Hermiticity gates but distorts absolute scales. | Operator norm / scale policy gate | hermiticity_residual=0; window_relative_shift=2; low_energy_max_ipr=0.129; operator_norm_ratio=3 | caught | This is a policy gate, not a physics claim; scale-invariant analyses may intentionally ignore it. |

## Interpretation

The expanded matrix intentionally records caught and missed/ambiguous artifacts. Missed/ambiguous rows are real harness caveats and should not be hidden. These are review prompts, not evidence of physical validity.

## Immediate Follow-Up

- Window manipulation, boundary flips, sparse Hermitian noise, and seed variation need stronger or more context-aware controls.
- The fake-localized-vector injection was not caught by the current low-energy IPR gate in this construction; that remains a real caveat rather than a threshold-tuning target.
- Do not convert this matrix into a 100% pass claim.

## Raw Artifact

`reports/RUNS/v0_1_18_practical_applicability/expanded_artifact_injection_v0_1_18.json`
