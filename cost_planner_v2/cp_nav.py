"""Navigation helpers for legacy cost planner modules."""

from __future__ import annotations

from senior_nav.navigation import switch_page


def goto(path: str) -> None:
    """Navigate to another Streamlit page, mirroring the global helper."""

    switch_page(path)
