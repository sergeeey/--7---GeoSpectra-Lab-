from __future__ import annotations

import sys
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import radion_stabilization, spectral_localization


def main() -> None:
    print("Running radion MVP...")
    radion_stabilization.run(Namespace(n_agents=120, t_final=40.0, dt=0.01, seed=42))
    print("Running spectral MVP smoke...")
    spectral_localization.run(Namespace(quick=True, size=512, disorder_count=30, realizations=30, seed=42))
    print("MVP smoke complete")


if __name__ == "__main__":
    main()
