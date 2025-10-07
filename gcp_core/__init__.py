"""
gcp_core package init — minimal, safe exports.
Do NOT import from .scoring here; let callers import `gcp_core.scoring` directly.
"""

from .state import (  # noqa: F401
    ensure_session,
    resume_target,
    get_state as _get_state,
    get_answer,
    set_answer,
    medicaid_status,
    set_ack_medicaid as _set_ack_medicaid,
    get_ack_medicaid as _get_ack_medicaid,
)


def answers():
    """Return the current answers dict from the session state."""
    ensure_session()
    return _get_state().get("answers", {})


def set_medicaid_ack(flag: bool) -> None:
    """Set the Medicaid acknowledgement flag in session state."""
    _set_ack_medicaid(bool(flag))


def clear_medicaid_ack() -> None:
    """Clear the Medicaid acknowledgement flag."""
    _set_ack_medicaid(False)


def has_medicaid_ack() -> bool:
    """Return True if the Medicaid acknowledgement flag is set."""
    return bool(_get_ack_medicaid())


__all__ = [
    "ensure_session",
    "resume_target",
    "answers",
    "get_answer",
    "set_answer",
    "medicaid_status",
    "set_medicaid_ack",
    "clear_medicaid_ack",
    "has_medicaid_ack",
]
