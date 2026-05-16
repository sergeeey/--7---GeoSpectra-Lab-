from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Any

import numpy as np


REPORTS_DIR = Path("reports")


def ensure_report_tree() -> None:
    for path in [
        REPORTS_DIR / "FIGURES",
        REPORTS_DIR / "DATA",
        REPORTS_DIR / "RUNS",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def make_run_dir(experiment_name: str) -> Path:
    ensure_report_tree()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = REPORTS_DIR / "RUNS" / f"{stamp}_{experiment_name}"
    (run_dir / "figures").mkdir(parents=True, exist_ok=True)
    return run_dir


def to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return to_jsonable(asdict(value))
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    return value


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_jsonable(payload), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_summary(path: Path, title: str, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join([f"# {title}", "", *lines, ""])
    path.write_text(body, encoding="utf-8")
