# Release Notes — v0.1.11-mvp-s2-graph-intermediate-quick

## Summary
This release adds the first intermediate toy bridge combining a verified `S2` monopole index sector with a graph-sector localization diagnostic.

## New in this release
- `s2_graph_intermediate` module
- `s2_graph_intermediate` CLI
- tests
- quick run artifacts
- documentation updates

## Verified quick results
- `all_index_checks_passed=True`
- `all_anticommutators_preserved=True`
- `ipr_growth_observed=True`
- `pytest -q: 57 passed in 14.22s`

Verified command:

```powershell
python scripts/s2_graph_intermediate.py --quick
```

Run path:

```text
reports/RUNS/20260512-141913_s2_graph_intermediate_quick
```

Saved artifacts:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/index_vs_disorder.png`
- `figures/zero_mode_ipr_vs_disorder.png`
- `figures/perturbation_stability.png`
- `figures/chirality_counts.png`

## Scientific meaning
The model shows index plus localization diagnostics simultaneously in a controlled toy bridge.

## Scientific non-claims
This is not continuum compactification.
This is not `S6` or `S3 x S6`.
This does not prove physical chirality.
This does not derive Standard Model fermions.
This does not validate covariant compactification.
This does not bypass Witten/Lichnerowicz no-go results.

## Known limitations
- graph selector is artificial;
- quick mode only;
- no continuum product geometry yet;
- no anomaly/hypercharge checks;
- no `SU(3) x SU(2) x U(1)` derivation.

## Next recommended action
Replace the graph selector with `S2 x S1` or a product-discretized geometric Dirac operator.
