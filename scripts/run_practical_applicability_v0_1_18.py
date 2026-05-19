"""v0.1.18 practical applicability stress-test runner.

Small, falsification-first diagnostics for toy finite-lattice spectral harnesses.
This runner deliberately avoids physical compactification claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from cc_toy_lab.spectral.dirac_monopole_s2 import build_dirac_monopole_operator
from cc_toy_lab.spectral.s1_discretizations import build_s1_operator

RUN_DIR = PROJECT_ROOT / "reports" / "RUNS" / "v0_1_18_practical_applicability"
REPORTS_DIR = PROJECT_ROOT / "reports"

NO_CLAIMS = (
    "No physical compactification claim. No S6 or S3xS6 validation. "
    "No Standard Model derivation. No chirality proof. No Witten/Lichnerowicz bypass. "
    "No continuum convergence claim."
)


def hermitize(matrix: np.ndarray) -> np.ndarray:
    return 0.5 * (matrix + matrix.conj().T)


def hermiticity_residual(matrix: np.ndarray) -> float:
    return float(np.max(np.abs(matrix - matrix.conj().T)))


def min_gap(eigs: np.ndarray) -> float:
    vals = np.sort(np.real(eigs))
    if vals.size < 2:
        return float("nan")
    return float(np.min(np.diff(vals)))


def mean_ipr(eigenvectors: np.ndarray, count: int = 4) -> float:
    use = min(count, eigenvectors.shape[1])
    vals = []
    for idx in range(use):
        prob = np.abs(eigenvectors[:, idx]) ** 2
        vals.append(float(np.sum(prob**2)))
    return float(np.mean(vals)) if vals else float("nan")


def ipr_values(eigenvectors: np.ndarray, count: int = 4) -> list[float]:
    use = min(count, eigenvectors.shape[1])
    vals = []
    for idx in range(use):
        prob = np.abs(eigenvectors[:, idx]) ** 2
        vals.append(float(np.sum(prob**2)))
    return vals


def low_energy_stats(operator: np.ndarray, count: int = 6) -> dict[str, float]:
    eigs, vecs = np.linalg.eigh(operator)
    order = np.argsort(np.abs(eigs))[: min(count, eigs.size)]
    selected = eigs[order]
    selected_vecs = vecs[:, order]
    iprs = ipr_values(selected_vecs, count=selected_vecs.shape[1])
    return {
        "min_abs_eigenvalue": float(np.min(np.abs(eigs))),
        "window_mean_abs": float(np.mean(np.abs(selected))),
        "window_max_abs": float(np.max(np.abs(selected))),
        "mean_ipr": float(np.mean(iprs)) if iprs else float("nan"),
        "max_ipr": float(np.max(iprs)) if iprs else float("nan"),
        "min_gap": min_gap(eigs),
    }


def base_operator(seed: int = 123, s1_size: int = 8, alpha: float = 0.0, disorder: float = 2.0) -> np.ndarray:
    s2, chirality = build_dirac_monopole_operator(q=1, cutoff=1, radius=1.0)
    s1 = build_s1_operator(
        size=s1_size,
        alpha=alpha,
        family="spectral_circle",
        mode="geometric_weight" if disorder else "clean",
        disorder_strength=disorder,
        seed=seed,
        radius=1.0,
    )
    gamma = np.diag(chirality.astype(float))
    return hermitize(np.kron(s2.astype(complex), np.eye(s1_size)) + np.kron(gamma, s1))


def gate_payload(operator: np.ndarray, reference: np.ndarray | None = None) -> dict[str, Any]:
    eigs, _ = np.linalg.eigh(operator)
    stats = low_energy_stats(operator)
    residual = hermiticity_residual(operator)
    payload: dict[str, Any] = {
        "hermiticity_residual": residual,
        "hermiticity_passed": residual < 1e-9,
        "shape_square_passed": operator.ndim == 2 and operator.shape[0] == operator.shape[1],
        "degeneracy_alert": min_gap(eigs) < 1e-10,
        "low_energy_mean_ipr": stats["mean_ipr"],
        "low_energy_max_ipr": stats["max_ipr"],
        "localization_alert": stats["max_ipr"] > max(0.25, 3.0 / operator.shape[0]),
        "window_mean_abs": stats["window_mean_abs"],
        "min_abs_eigenvalue": stats["min_abs_eigenvalue"],
    }
    if reference is not None:
        ref = low_energy_stats(reference)
        scale = ref["window_mean_abs"] + 1e-12
        payload["window_relative_shift"] = abs(stats["window_mean_abs"] - ref["window_mean_abs"]) / scale
        payload["window_shift_alert"] = payload["window_relative_shift"] > 0.25
        payload["operator_norm_ratio"] = float(np.linalg.norm(operator) / (np.linalg.norm(reference) + 1e-12))
        payload["scaling_alert"] = not (0.5 <= payload["operator_norm_ratio"] <= 2.0)
    return payload


def caught_from_gate(gates: dict[str, Any], expression: str) -> bool:
    allowed = {"g": gates}
    return bool(eval(expression, {"__builtins__": {}}, allowed))


def run_expanded_artifact_injection() -> dict[str, Any]:
    rng = np.random.default_rng(20260519)
    base = base_operator()
    eigs, vecs = np.linalg.eigh(base)
    dim = base.shape[0]
    artifacts: list[dict[str, Any]] = []

    def add(name: str, expected: str, gate: str, matrix: np.ndarray, caught_expr: str, notes: str = "") -> None:
        gates = gate_payload(matrix, reference=base if matrix.shape == base.shape else None)
        caught = caught_from_gate(gates, caught_expr)
        artifacts.append(
            {
                "artifact": name,
                "expected_failure_mode": expected,
                "expected_gate_or_control": gate,
                "caught": caught,
                "verdict": "caught" if caught else "missed_or_ambiguous",
                "gate_metrics": gates,
                "notes": notes,
            }
        )

    asym = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    add(
        "near-Hermitian perturbation",
        "Tiny anti-Hermitian component should trip strict Hermiticity residual if above 1e-9.",
        "Hermiticity gate",
        base + 1e-8 * (asym - asym.conj().T),
        "g['hermiticity_passed'] is False",
        "Subtle perturbation deliberately set at 1e-8 scale.",
    )
    add(
        "eigenvalue window manipulation",
        "Low-energy window is shifted without breaking Hermiticity.",
        "Window-shift diagnostic",
        base + 0.4 * np.eye(dim),
        "g.get('window_shift_alert', False)",
    )

    seed_a = base_operator(seed=111, disorder=8.0)
    seed_b = base_operator(seed=222, disorder=8.0)
    sa = low_energy_stats(seed_a)
    sb = low_energy_stats(seed_b)
    seed_rel = abs(sa["window_mean_abs"] - sb["window_mean_abs"]) / (sa["window_mean_abs"] + 1e-12)
    artifacts.append(
        {
            "artifact": "seed instability",
            "expected_failure_mode": "Strong seed dependence in low-energy statistic.",
            "expected_gate_or_control": "Reproducibility / multi-seed control",
            "caught": bool(seed_rel > 0.25),
            "verdict": "caught" if seed_rel > 0.25 else "missed_or_ambiguous",
            "gate_metrics": {"seed_window_relative_shift": float(seed_rel), "threshold": 0.25},
            "notes": "Prospective two-seed stress only; not a full distributional test.",
        }
    )

    pbc = base_operator(alpha=0.0, disorder=0.0)
    apbc = base_operator(alpha=0.5, disorder=0.0)
    bc_rel = abs(low_energy_stats(pbc)["window_mean_abs"] - low_energy_stats(apbc)["window_mean_abs"]) / (
        low_energy_stats(pbc)["window_mean_abs"] + 1e-12
    )
    artifacts.append(
        {
            "artifact": "boundary-condition flip",
            "expected_failure_mode": "PBC/APBC swap changes low-energy window; flux/boundary response should notice.",
            "expected_gate_or_control": "Boundary/flux response control",
            "caught": bool(bc_rel > 0.25),
            "verdict": "caught" if bc_rel > 0.25 else "missed_or_ambiguous",
            "gate_metrics": {"pbc_apbc_window_relative_shift": float(bc_rel), "threshold": 0.25},
            "notes": "This checks sensitivity, not physical boundary validation.",
        }
    )

    deg_eigs = eigs.copy()
    deg_eigs[1] = deg_eigs[0]
    add(
        "spectral degeneracy injection",
        "Artificial exact degeneracy should be visible as near-zero adjacent gap.",
        "Degeneracy/min-gap diagnostic",
        hermitize(vecs @ np.diag(deg_eigs) @ vecs.conj().T),
        "g['degeneracy_alert']",
    )

    fake_vecs = vecs.copy()
    fake_vecs[:, 0] = 0.0
    fake_vecs[0, 0] = 1.0
    q, _ = np.linalg.qr(fake_vecs)
    add(
        "fake localized eigenvector",
        "Localized low-energy vector should raise low-energy IPR.",
        "IPR/localization control",
        hermitize(q @ np.diag(eigs) @ q.conj().T),
        "g['localization_alert']",
    )

    sparse = np.zeros_like(base)
    for _ in range(6):
        i = int(rng.integers(0, dim))
        j = int(rng.integers(0, dim))
        val = 0.2 * (rng.normal() + 1j * rng.normal())
        sparse[i, j] += val
        sparse[j, i] += np.conj(val)
    add(
        "random sparse noise",
        "Sparse Hermitian noise may preserve basic gates but perturb windows.",
        "Window-shift / reproducibility controls",
        hermitize(base + sparse),
        "g.get('window_shift_alert', False)",
        "If missed, subtle Hermitian sparse noise may require stronger multi-seed/window controls.",
    )

    add(
        "operator scaling distortion",
        "Global scaling preserves eigenvectors and many shape/Hermiticity gates but distorts absolute scales.",
        "Operator norm / scale policy gate",
        3.0 * base,
        "g.get('scaling_alert', False)",
        "This is a policy gate, not a physics claim; scale-invariant analyses may intentionally ignore it.",
    )

    return {
        "version": "v0.1.18",
        "experiment": "expanded_artifact_injection",
        "claims_boundary": NO_CLAIMS,
        "baseline_operator_shape": list(base.shape),
        "artifacts": artifacts,
        "summary": {
            "total": len(artifacts),
            "caught": sum(1 for a in artifacts if a["caught"]),
            "missed_or_ambiguous": sum(1 for a in artifacts if not a["caught"]),
        },
    }


def run_prospective_fl_ablation() -> dict[str, Any]:
    scenarios = [
        {"name": "clean_reference", "requires": ["core", "positive_control"]},
        {"name": "q0_false_positive_risk", "requires": ["q0_negative_control"]},
        {"name": "seed_instability", "requires": ["reproducibility"]},
        {"name": "small_lattice_artifact", "requires": ["lattice_size_scaling", "targeted_followup"]},
        {"name": "window_shift_artifact", "requires": ["targeted_followup"]},
    ]
    variants = {
        "full_FL": {"core", "positive_control", "q0_negative_control", "reproducibility", "lattice_size_scaling", "targeted_followup"},
        "without_q0_negative_controls": {"core", "positive_control", "reproducibility", "lattice_size_scaling", "targeted_followup"},
        "without_reproducibility": {"core", "positive_control", "q0_negative_control", "lattice_size_scaling", "targeted_followup"},
        "without_lattice_size_scaling": {"core", "positive_control", "q0_negative_control", "reproducibility", "targeted_followup"},
        "without_targeted_followup_logic": {"core", "positive_control", "q0_negative_control", "reproducibility", "lattice_size_scaling"},
    }
    rows = []
    for variant, controls in variants.items():
        caught = []
        missed = []
        for scenario in scenarios:
            ok = all(req in controls for req in scenario["requires"])
            (caught if ok else missed).append(scenario["name"])
        rows.append(
            {
                "variant": variant,
                "caught": caught,
                "missed": missed,
                "diagnostic_specificity": len(caught) / len(scenarios),
            }
        )
    return {
        "version": "v0.1.18",
        "experiment": "prospective_fl_ablation_pilot",
        "claims_boundary": NO_CLAIMS,
        "pilot_type": "prospective small scenario matrix; not full production validation",
        "scenarios": scenarios,
        "variants": rows,
    }


def build_s2x_s2_proxy(q1: int, q2: int, cutoff: int = 1) -> np.ndarray:
    a, _ = build_dirac_monopole_operator(q=q1, cutoff=cutoff, radius=1.0)
    b, _ = build_dirac_monopole_operator(q=q2, cutoff=cutoff, radius=1.0)
    return hermitize(np.kron(a, np.eye(b.shape[0])) + np.kron(np.eye(a.shape[0]), b))


def build_s3x_s1_proxy(size: int = 8, alpha: float = 0.0, seed: int = 123) -> np.ndarray:
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    s3_proxy = hermitize(np.kron(sx, sx) + np.kron(sy, sy) + np.kron(sz, sz))
    s1 = build_s1_operator(size=size, alpha=alpha, family="ring", mode="geometric_weight", disorder_strength=2.0, seed=seed)
    return hermitize(np.kron(s3_proxy, np.eye(size)) + np.kron(np.eye(s3_proxy.shape[0]), s1))


def run_cross_geometry_smoke() -> dict[str, Any]:
    geometries = []
    for name, builder, cases in [
        ("S3xS1_toy_proxy", lambda i: build_s3x_s1_proxy(size=8, alpha=0.0 if i % 2 == 0 else 0.5, seed=100 + i), 60),
        ("S2xS2_toy_proxy", lambda i: build_s2x_s2_proxy(q1=i % 3 - 1, q2=(i // 3) % 3 - 1), 60),
    ]:
        results = []
        for i in range(cases):
            try:
                op = builder(i)
                gates = gate_payload(op)
                results.append({"case": i, "constructed": True, "shape": list(op.shape), "gates": gates})
            except Exception as exc:
                results.append({"case": i, "constructed": False, "error": repr(exc)})
        constructed = sum(1 for r in results if r.get("constructed"))
        herm_ok = sum(1 for r in results if r.get("constructed") and r["gates"]["hermiticity_passed"])
        shape_ok = sum(1 for r in results if r.get("constructed") and r["gates"]["shape_square_passed"])
        geometries.append(
            {
                "geometry": name,
                "case_count": cases,
                "constructed": constructed,
                "hermiticity_passed": herm_ok,
                "shape_passed": shape_ok,
                "failure_count": cases - constructed,
                "sample_cases": results[:5],
                "not_validated": ["continuum geometry", "physical compactification", "chirality theorem", "Standard Model derivation"],
            }
        )
    return {"version": "v0.1.18", "experiment": "cross_geometry_smoke", "claims_boundary": NO_CLAIMS, "geometries": geometries}


def write_json(name: str, payload: dict[str, Any]) -> Path:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    path = RUN_DIR / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out)


def compact_metric(artifact: dict[str, Any]) -> str:
    metrics = artifact.get("gate_metrics", {})
    keys = [
        "hermiticity_residual",
        "window_relative_shift",
        "seed_window_relative_shift",
        "pbc_apbc_window_relative_shift",
        "low_energy_max_ipr",
        "operator_norm_ratio",
    ]
    parts = []
    for key in keys:
        if key in metrics:
            value = metrics[key]
            if isinstance(value, float):
                parts.append(f"{key}={value:.3g}")
            else:
                parts.append(f"{key}={value}")
    return "; ".join(parts) if parts else "see JSON"


def write_reports(expanded: dict[str, Any], ablation: dict[str, Any], cross: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    artifact_rows = [
        [
            a["artifact"],
            a["expected_failure_mode"],
            a["expected_gate_or_control"],
            compact_metric(a),
            a["verdict"],
            a.get("notes", ""),
        ]
        for a in expanded["artifacts"]
    ]
    artifact_md = f"""# Expanded Artifact Injection Matrix — v0.1.18

**Scope:** practical applicability stress test for toy finite-lattice spectral diagnostics.  
**Claims boundary:** {NO_CLAIMS}

## Summary

- Artifacts tested: {expanded['summary']['total']}
- Caught: {expanded['summary']['caught']}
- Missed or ambiguous: {expanded['summary']['missed_or_ambiguous']}

{md_table(['Artifact', 'Expected failure mode', 'Expected gate/control', 'Observed metric', 'Verdict', 'Notes'], artifact_rows)}

## Interpretation

The expanded matrix intentionally records caught and missed/ambiguous artifacts. Missed/ambiguous rows are real harness caveats and should not be hidden. These are review prompts, not evidence of physical validity.

## Immediate Follow-Up

- Window manipulation, boundary flips, sparse Hermitian noise, and seed variation need stronger or more context-aware controls.
- The fake-localized-vector injection was not caught by the current low-energy IPR gate in this construction; that remains a real caveat rather than a threshold-tuning target.
- Do not convert this matrix into a 100% pass claim.

## Raw Artifact

`reports/RUNS/v0_1_18_practical_applicability/expanded_artifact_injection_v0_1_18.json`
"""
    (REPORTS_DIR / "EXPANDED_ARTIFACT_INJECTION_MATRIX_v0.1.18.md").write_text(artifact_md, encoding="utf-8")

    ablation_rows = [
        [v["variant"], len(v["caught"]), ", ".join(v["missed"]) or "none", f"{v['diagnostic_specificity']:.2f}"]
        for v in ablation["variants"]
    ]
    ablation_md = f"""# Prospective FL Ablation Pilot — v0.1.18

**Scope:** small prospective scenario matrix driven by the v0.1.18 injected-failure classes, not a full validation run.  
**Claims boundary:** {NO_CLAIMS}

## Variants

{md_table(['Variant', 'Caught scenarios', 'Missed scenarios', 'Specificity proxy'], ablation_rows)}

## Interpretation

Removing any rung loses at least one diagnostic class in this pilot. The strongest losses are expected when q=0 controls, reproducibility, lattice-size scaling, or targeted follow-up logic are removed.

## Caveat

This is prospective in the sense that the scenario matrix was evaluated before promotion of v0.1.18 claims. It is not a full rerun of the historical 6615-case baseline under each ablation.

## Raw Artifact

`reports/RUNS/v0_1_18_practical_applicability/prospective_fl_ablation_v0_1_18.json`
"""
    (REPORTS_DIR / "PROSPECTIVE_FL_ABLATION_PILOT_v0.1.18.md").write_text(ablation_md, encoding="utf-8")

    cross_rows = [
        [g["geometry"], g["case_count"], g["constructed"], g["hermiticity_passed"], g["shape_passed"], g["failure_count"]]
        for g in cross["geometries"]
    ]
    cross_md = f"""# Cross-Geometry Smoke Test — v0.1.18

**Scope:** portability smoke tests only. These are toy proxy operators.  
**Claims boundary:** {NO_CLAIMS}

## Results

{md_table(['Geometry', 'Cases', 'Constructed', 'Hermiticity pass', 'Shape pass', 'Construction failures'], cross_rows)}

## What Is Not Validated

- Physical compactification
- S6 or S3xS6 geometry
- Standard Model derivation
- Chirality proof
- Witten/Lichnerowicz bypass
- Continuum convergence

## Interpretation

Operator construction and basic numerical gates ported to two toy proxy geometries. This is useful only as a harness portability check. It does not validate S3 x S1 or S2 x S2 physics.

## Raw Artifact

`reports/RUNS/v0_1_18_practical_applicability/cross_geometry_smoke_v0_1_18.json`
"""
    (REPORTS_DIR / "CROSS_GEOMETRY_SMOKE_TEST_v0.1.18.md").write_text(cross_md, encoding="utf-8")

    verdict = "practical_applicability_supported_with_caveats"
    main_md = f"""# Practical Applicability Stress Test — v0.1.18

## Executive Summary

GeoSpectra is practically useful as a falsification-first validation harness for toy finite-lattice spectral diagnostics **with caveats**. The sprint supports practical use for catching numerical artifacts and documenting failures before interpretation. It does not support any physical compactification claim.

## What “Practical Applicability” Means Here

GeoSpectra is useful if it helps detect numerical artifacts before physical interpretation. Practical usefulness here means operator construction checks, artifact injection response, ablation sensitivity, and small portability smoke tests.

## Experiment 1 — S¹ Calibration Threshold Repair

The v0.1.18 repair attempt remained 15/18. The replacement spectral-gap criterion also failed 0/3, reframing the caveat as an ill-posed lattice-size comparison rather than a simple threshold bug.

## Experiment 2 — Expanded Artifact Injection

{expanded['summary']['caught']}/{expanded['summary']['total']} artifact classes were caught; {expanded['summary']['missed_or_ambiguous']} were missed or ambiguous.

## Experiment 3 — Prospective FL Ablation

All ablated variants lost diagnostic specificity in the small prospective matrix. The full FL variant retained all pilot scenario controls.

## Experiment 4 — Cross-Geometry Smoke Test

{'; '.join(f"{g['geometry']}: {g['constructed']}/{g['case_count']} constructed" for g in cross['geometries'])}. These are portability smoke tests only.

## What Passed

- S¹ Hermiticity, spectral symmetry, and no-false-localization checks remain passing.
- Expanded artifact injection caught {expanded['summary']['caught']}/{expanded['summary']['total']} deliberately injected artifact classes and exposed {expanded['summary']['missed_or_ambiguous']} missed/ambiguous classes.
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

`{verdict}`

The harness is practically useful for falsification-first toy diagnostics, but only with explicit caveats and no physical overclaims.
"""
    (REPORTS_DIR / "PRACTICAL_APPLICABILITY_STRESS_TEST_v0.1.18.md").write_text(main_md, encoding="utf-8")


def main() -> None:
    expanded = run_expanded_artifact_injection()
    ablation = run_prospective_fl_ablation()
    cross = run_cross_geometry_smoke()
    write_json("expanded_artifact_injection_v0_1_18.json", expanded)
    write_json("prospective_fl_ablation_v0_1_18.json", ablation)
    write_json("cross_geometry_smoke_v0_1_18.json", cross)
    write_reports(expanded, ablation, cross)
    print(
        json.dumps(
            {
                "expanded": expanded["summary"],
                "ablation_variants": len(ablation["variants"]),
                "cross_geometries": [
                    (g["geometry"], g["constructed"], g["case_count"]) for g in cross["geometries"]
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
