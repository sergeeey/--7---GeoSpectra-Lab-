"""Gate 3 Full Diagnostic Runner"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

import time
import s3_s1_product_discretized_ipr_smoke as smoke
import s3_s1_gate3_profiles as profiles

print("=== Gate 3 Full Diagnostic ===\n")
print("Profile: FULL (1440 cases)")
print("Estimated time: ~20 minutes")
print("Disorder: W ∈ {0, 2, 4, 8, 12}")
print("j_max: {1, 2, 3}")
print("s1_sizes: {8, 16, 24, 32}")
print()

output_dir = Path("reports/RUNS/gate3_full_diagnostic_v0.1.20")
output_dir.mkdir(parents=True, exist_ok=True)

start = time.time()
agg, results = smoke.run_ipr_smoke(output_dir, profiles.PROFILE_FULL)
elapsed = time.time() - start

print("\n" + "=" * 60)
print("GATE 3 FULL DIAGNOSTIC COMPLETE")
print("=" * 60)
print(f"Total time: {elapsed/60:.1f} minutes")
print(f'Cases: {agg["total_cases"]}')
print(f'Metric: {agg["metric_version"]}')
print()
print(f'**Absolute IPR Contrast: {agg["ipr_contrast_absolute"]:.2f}x**')
print(f'Clean: {agg["clean_mean_ipr_absolute"]:.4f}')
print(f'Disordered: {agg["disordered_mean_ipr_absolute"]:.4f}')
print()
print(f'Verdict: {agg["ipr_smoke_verdict"].upper()}')
print("=" * 60)
