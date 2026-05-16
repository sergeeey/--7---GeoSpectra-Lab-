from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FiniteSizePoint:
    size: int
    metric: float


def summarize_scaling(sizes: list[int], metrics: list[float]) -> list[FiniteSizePoint]:
    return [FiniteSizePoint(int(size), float(metric)) for size, metric in zip(sizes, metrics)]
