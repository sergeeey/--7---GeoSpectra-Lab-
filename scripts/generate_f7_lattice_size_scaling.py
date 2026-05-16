#!/usr/bin/env python3
"""
Generate F7: Lattice-Size Scaling Plot (Ring/alpha=0 Convergence)

Source: reports/FIGURE_DATA_LATTICE_SIZE_SCALING_v0.1.16.md
Output: reports/figures/F7_lattice_size_scaling.png
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Data from lattice-size scaling table
s1_sizes = [8, 16, 24, 32, 48, 64, 96]
failure_rates = [19.8, 0.8, 15.1, 2.4, 2.4, 0.0, 0.0]

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Main data series
ax.plot(
    s1_sizes,
    failure_rates,
    "o-",
    color="#2E86AB",
    linewidth=2,
    markersize=8,
    label="Ring/alpha=0 (disordered)",
    zorder=3,
)

# Decision Rule 1 threshold (horizontal)
ax.axhline(
    y=2.0,
    color="#D32F2F",
    linestyle="--",
    linewidth=1.5,
    label="Decision Rule 1 threshold (2%)",
    zorder=2,
)

# Convergence threshold (vertical)
ax.axvline(
    x=64,
    color="#388E3C",
    linestyle="--",
    linewidth=1.5,
    label="Convergence threshold (s1_size=64)",
    zorder=2,
)

# Shaded region for small-lattice artifact zone
ax.axvspan(8, 48, alpha=0.1, color="red", zorder=1)

# Annotations
ax.annotate(
    "Converged:\n0/252 = 0.0%",
    xy=(64, 0.0),
    xytext=(75, 5),
    arrowprops=dict(arrowstyle="->", color="#388E3C", lw=1.5),
    fontsize=10,
    color="#388E3C",
    weight="bold",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#388E3C"),
)

ax.annotate(
    "Small-lattice\nartifact zone",
    xy=(24, 15.1),
    xytext=(24, 22),
    arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.5),
    fontsize=10,
    color="#D32F2F",
    weight="bold",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#D32F2F"),
)

# Axis labels and title
ax.set_xlabel("s1_size (S¹ Lattice Discretization Points)", fontsize=12, weight="bold")
ax.set_ylabel("Failure Rate (%)", fontsize=12, weight="bold")
ax.set_title(
    "Ring/alpha=0 Lattice-Size Scaling: Convergence at s1_size≥64",
    fontsize=13,
    weight="bold",
    pad=15,
)

# Grid and styling
ax.grid(True, alpha=0.3, linestyle=":", zorder=0)
ax.set_xlim(0, 100)
ax.set_ylim(-1, 25)
ax.set_xticks(s1_sizes)
ax.legend(loc="upper right", fontsize=9, framealpha=0.95)

# Tight layout
plt.tight_layout()

# Save
output_dir = Path(__file__).parent.parent / "reports" / "figures"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "F7_lattice_size_scaling.png"

plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✅ F7 saved: {output_path}")
print(f"   Data points: {len(s1_sizes)}")
print(f"   Key result: s1_size≥64 → 0.0% failure rate (converged)")
print(f"   Small-lattice artifact zone: s1_size<64 → 8.1% failure rate")
