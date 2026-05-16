from __future__ import annotations


def gudhi_available() -> bool:
    try:
        import gudhi  # noqa: F401
    except Exception:
        return False
    return True
