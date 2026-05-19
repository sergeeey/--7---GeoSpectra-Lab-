# Prospective FL Ablation Pilot — v0.1.18

**Scope:** small prospective scenario matrix driven by the v0.1.18 injected-failure classes, not a full validation run.  
**Claims boundary:** No physical compactification claim. No S6 or S3xS6 validation. No Standard Model derivation. No chirality proof. No Witten/Lichnerowicz bypass. No continuum convergence claim.

## Variants

| Variant | Caught scenarios | Missed scenarios | Specificity proxy |
|---|---|---|---|
| full_FL | 5 | none | 1.00 |
| without_q0_negative_controls | 4 | q0_false_positive_risk | 0.80 |
| without_reproducibility | 4 | seed_instability | 0.80 |
| without_lattice_size_scaling | 4 | small_lattice_artifact | 0.80 |
| without_targeted_followup_logic | 3 | small_lattice_artifact, window_shift_artifact | 0.60 |

## Interpretation

Removing any rung loses at least one diagnostic class in this pilot. The strongest losses are expected when q=0 controls, reproducibility, lattice-size scaling, or targeted follow-up logic are removed.

## Caveat

This is prospective in the sense that the scenario matrix was evaluated before promotion of v0.1.18 claims. It is not a full rerun of the historical 6615-case baseline under each ablation.

## Raw Artifact

`reports/RUNS/v0_1_18_practical_applicability/prospective_fl_ablation_v0_1_18.json`
