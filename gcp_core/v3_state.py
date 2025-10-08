"""Session helpers for Guided Care Plan V3."""
from __future__ import annotations

from typing import Any, Dict, Iterable, MutableMapping

import streamlit as st

from ui.state import get_completion, set_completion

_SESSION_KEY = "gcp_v3"
_DEFAULT_SCORECARD: Dict[str, Any] = {
    "domains": {},
    "tier": None,
    "tier_label": "",
    "flags": set(),
    "narrative": [],
    "highlights": [],
}


def _normalize_status(raw: Any) -> str:
    if raw is None:
        return "unknown"
    text = str(raw).strip().lower()
    mapping = {
        "yes": {"yes", "y", "true", "on_medicaid", "currently on medicaid"},
        "no": {"no", "n", "false", "not on medicaid"},
    }
    for token, options in mapping.items():
        if text in options:
            return token
    if "yes" in text and "medicaid" in text:
        return "yes"
    if "no" in text and "medicaid" in text:
        return "no"
    return "unknown"


def ensure_session() -> MutableMapping[str, Any]:
    """Ensure the V3 session bucket exists with default structure."""
    bucket = st.session_state.setdefault(_SESSION_KEY, {})
    if not isinstance(bucket, dict):
        bucket = {}
        st.session_state[_SESSION_KEY] = bucket

    answers = bucket.setdefault("answers", {})
    if not isinstance(answers, dict):
        answers = {}
        bucket["answers"] = answers

    flags = bucket.setdefault("flags", set())
    if not isinstance(flags, set):
        flags = set(flags or [])
        bucket["flags"] = flags

    scorecard = bucket.setdefault("scorecard", dict(_DEFAULT_SCORECARD))
    if not isinstance(scorecard, dict):
        scorecard = dict(_DEFAULT_SCORECARD)
        bucket["scorecard"] = scorecard

    bucket.setdefault("completed", False)
    bucket.setdefault("medicaid_status", "unknown")
    return bucket


def reset_partial(keys: Iterable[str]) -> None:
    """Remove specific answer keys."""
    answers = ensure_session()["answers"]
    for key in keys:
        answers.pop(key, None)


def get_answers() -> Dict[str, Any]:
    """Return the live answers dictionary."""
    return ensure_session()["answers"]


def _mark_in_progress() -> None:
    if get_completion("gcp") == "not_started":
        set_completion("gcp", "in_progress")


def set_answer(key: str, value: Any) -> None:
    """Persist an answer value, normalizing empties."""
    bucket = ensure_session()
    answers = bucket["answers"]

    if value is None:
        answers.pop(key, None)
    elif isinstance(value, str):
        trimmed = value.strip()
        if trimmed:
            answers[key] = trimmed
        else:
            answers.pop(key, None)
    elif isinstance(value, (list, tuple, set)):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        if cleaned:
            answers[key] = cleaned
        else:
            answers.pop(key, None)
    else:
        answers[key] = value

    if key == "medicaid_status":
        status = _normalize_status(answers.get(key))
        bucket["medicaid_status"] = status
        st.session_state["medicaid_status"] = status
    _mark_in_progress()


def clear_answer(key: str) -> None:
    """Remove a single answer."""
    set_answer(key, None)


def get_medicaid_status() -> str:
    """Return normalized Medicaid status token."""
    bucket = ensure_session()
    status = bucket.get("medicaid_status", "unknown")
    if not isinstance(status, str):
        status = "unknown"
    return status


def update_flags(new_flags: Iterable[str]) -> set[str]:
    """Replace the derived flag set."""
    bucket = ensure_session()
    flag_set = set(str(flag).strip() for flag in new_flags if str(flag).strip())
    bucket["flags"] = flag_set
    return flag_set


def get_flags() -> set[str]:
    return ensure_session().get("flags", set())


def update_scorecard(data: Dict[str, Any]) -> Dict[str, Any]:
    """Store the latest scorecard snapshot."""
    bucket = ensure_session()
    bucket["scorecard"] = dict(data)
    return bucket["scorecard"]


def get_scorecard() -> Dict[str, Any]:
    return ensure_session().get("scorecard", dict(_DEFAULT_SCORECARD))


def mark_complete() -> None:
    bucket = ensure_session()
    bucket["completed"] = True
    set_completion("gcp", "complete")


def mark_not_started() -> None:
    bucket = ensure_session()
    bucket["completed"] = False
    bucket["scorecard"] = dict(_DEFAULT_SCORECARD)
    bucket["flags"] = set()
    set_completion("gcp", "not_started")

