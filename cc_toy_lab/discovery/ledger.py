from __future__ import annotations

from datetime import datetime
from pathlib import Path


LEDGER_PATH = Path("reports") / "DISCOVERY_LEDGER.md"


def append_finding(
    short_name: str,
    status: str,
    block: str,
    observation: str,
    importance: str,
    next_check: str,
    confidence: float,
    config_path: str = "",
    data_path: str = "",
    figure_path: str = "",
) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LEDGER_PATH.exists():
        LEDGER_PATH.write_text("# Discovery Ledger\n\n", encoding="utf-8")
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    entry = f"""## Finding {stamp} - {short_name}

**Status:** {status}  
**Block:** {block}  
**Config:** {config_path}  
**Data:** {data_path}  
**Figures:** {figure_path}

### What is observed
{observation}

### Why it may matter
{importance}

### Alternative explanations
Artifact, seed sensitivity, discretization, or an under-specified toy model remain possible until checked.

### How to check next
{next_check}

### Confidence
{confidence:.2f}

"""
    with LEDGER_PATH.open("a", encoding="utf-8") as handle:
        handle.write(entry)
