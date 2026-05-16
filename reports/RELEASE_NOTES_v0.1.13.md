# Release Notes — v0.1.13-mvp-s2-s1-product-full

## Summary
This release promotes the configured full `S2 x S1` product-operator benchmark
to the current MVP baseline.

## New in this release
- configured full `S2 x S1` benchmark run
- full run artifacts
- low-energy flux-response signature fix for higher-charge full-grid points
- documentation updates for the promoted full baseline

## Verified full results
- `classification=quick_bridge_passed`
- `all_basic_gates_passed=True`
- `total_observations=6750`
- `q_control_passed=True`
- `pbc_gate_passed=True`
- `apbc_gate_passed=True`
- `flux_response_observed=True`
- `s1_not_spectator=True`
- `localization_gate_passed=True`
- `threshold_stable=True`
- `pytest -q: 90 passed in 38.97s`

Verified command:

```powershell
python scripts/s2_s1_product.py --full
```

Run path:

```text
reports/RUNS/20260512-180321_s2_s1_product_full
```

Saved artifacts:

- `config.json`
- `metrics.json`
- `data.npz`
- `summary.md`
- `figures/`

## Scientific meaning
This is the first successful configured full benchmark for the toy `S2 x S1`
product-operator bridge.

Progression:

- toy Dirac localization/chirality = negative control;
- finite-mode `S2` monopole = positive index control;
- `S2 monopole x graph` = historical artificial intermediate bridge;
- `S2 x S1` = first geometric product-operator bridge stable under the
  configured full profile.

The bridge improves over `S2 x graph` because the circle factor now enters the
toy operator directly:

```text
D_{S2xS1} = D_{S2}(q) ⊗ I_{S1} + Γ_{S2} ⊗ P_{S1}(α, W)
```

The benchmark checks inherited `S2` monopole kernel behavior together with `S1`
twist and localization response. Full-product global chiral index is not the
headline metric here.

## Scientific non-claims
This is a toy product diagnostic, not continuum compactification.
This is not `S6` or `S3 x S6`.
This does not derive Standard Model physics.
This does not prove physical chirality.
This does not validate covariant compactification.
This does not bypass Witten/Lichnerowicz no-go results.

## Known limitations
- full profile is runtime-safe rather than continuum-like: `cutoff=2`;
- figures directory is currently a placeholder;
- spectral-circle is only one `S1` discretization choice;
- no anomaly/hypercharge checks;
- no `SU(3) x SU(2) x U(1)` derivation.

## Next recommended action
Add figures if useful, compare spectral-circle against ring/Wilson-like `S1`
discretizations, and only then move toward product-discretized refinements
before any `S6` or `S3 x S6` step.
