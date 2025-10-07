"""
gcp_core package init — minimal, safe exports.
Do NOT import from .scoring here; let callers import `gcp_core.scoring` directly.
"""

from .state import (  # noqa: F401
    ensure_session,
    resume_target,
    get_state as _get_state,
    get_answers as _get_answers,
    get_answer,
    set_answer,
    clear_answer,
    medicaid_status,
    get_medicaid_status,
    set_medicaid_ack as _set_medicaid_ack,
    get_medicaid_ack as _get_medicaid_ack,
)


def answers():
    """Return the current answers dict from the session state."""
    ensure_session()
    return _get_answers()


def set_medicaid_ack(flag: bool) -> None:
    """Set the Medicaid acknowledgement flag in session state."""
    _set_medicaid_ack(bool(flag))


def clear_medicaid_ack() -> None:
    """Clear the Medicaid acknowledgement flag."""
    _set_medicaid_ack(False)


def has_medicaid_ack() -> bool:
    """Return True if the Medicaid acknowledgement flag is set."""
    return bool(_get_medicaid_ack())


__all__ = [
    "ensure_session",
    "resume_target",
    "answers",
    "clear_answer",
    "get_medicaid_status",
    "get_answer",
    "set_answer",
    "medicaid_status",
    "set_medicaid_ack",
    "clear_medicaid_ack",
    "has_medicaid_ack",
]
