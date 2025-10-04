"""Navigation helpers for the cost planner wizard."""
from __future__ import annotations

from . import state, wizard


def go_to(index: int) -> None:
    wizard.set_current_step(index)


def go_next() -> None:
    current = state.get_progress()
    wizard.set_current_step(current + 1)


def go_previous() -> None:
    current = state.get_progress()
    wizard.set_current_step(max(0, current - 1))


def mark_drawer_complete(drawer_key: str) -> None:
    state.set_drawer_status(drawer_key, "done")


def mark_drawer_open(drawer_key: str) -> None:
    state.set_drawer_status(drawer_key, "in_progress")
