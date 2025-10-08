# Guided Care Plan state helpers
from __future__ import annotations

from typing import Any, Dict, Iterable, MutableMapping

import streamlit as st

_DEFAULT_PROGRESS: Dict[str, int] = {
    "landing": 0,
    "daily_life": 0,
    "health_safety": 0,
    "context_prefs": 0,
    "done": 0,
}

_DEFAULT_RESUME_PATH = "app_pages/gcp_v2/gcp_landing_v2.py"
_MEDICAID_FIELD = "medicaid_status"

_YES_TOKENS = {"yes", "y", "enrolled", "on_medicaid", "medicaid_yes"}
_NO_TOKENS = {"no", "n", "not_enrolled", "private_pay", "medicaid_no"}
_UNSURE_TOKENS = {"unsure", "not_sure", "maybe", "unknown", "question"}


def ensure_session() -> MutableMapping[str, Any]:
    """Ensure the GCP session object exists with default structure."""
    gcp = st.session_state.get("gcp")
    if not isinstance(gcp, dict):
        gcp = {}
        st.session_state["gcp"] = gcp

    gcp.setdefault("answers", {})
    if not isinstance(gcp["answers"], dict):
        gcp["answers"] = {}

    progress = gcp.setdefault("progress", {})
    if not isinstance(progress, dict):
        progress = {}
        gcp["progress"] = progress
    for key, value in _DEFAULT_PROGRESS.items():
        progress.setdefault(key, int(value))

    gcp.setdefault("medicaid_ack", False)
    gcp.setdefault("resume_target", _DEFAULT_RESUME_PATH)
    gcp.setdefault("_last_medicaid_status", "unknown")
    return gcp


def get_answers() -> Dict[str, Any]:
    """Return the current answers dict (mutable)."""
    return ensure_session()["answers"]


def set_answer(qid: str, value: Any) -> None:
    """Persist a normalized answer; clear when value is falsy."""
    gcp = ensure_session()
    answers = gcp["answers"]
    previous_status = get_medicaid_status(answers)

    if value is None:
        answers.pop(qid, None)
    elif isinstance(value, str):
        stripped = value.strip()
        if stripped:
            answers[qid] = stripped
        else:
            answers.pop(qid, None)
    elif isinstance(value, (list, tuple, set)):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        if cleaned:
            answers[qid] = cleaned
        else:
            answers.pop(qid, None)
    else:
        answers[qid] = value

    if qid == _MEDICAID_FIELD:
        current_status = get_medicaid_status(answers)
        if current_status != previous_status:
            gcp["medicaid_ack"] = False
            gcp["_last_medicaid_status"] = current_status


def clear_answer(qid: str) -> None:
    """Remove a question answer entirely."""
    set_answer(qid, None)


def get_medicaid_status(answers: Dict[str, Any] | None = None) -> str:
    """Return the normalized Medicaid status token."""
    if answers is None:
        answers = get_answers()

    raw = answers.get(_MEDICAID_FIELD)
    token: str = ""
    if isinstance(raw, (list, tuple)):
        token = str(raw[0]) if raw else ""
    else:
        token = str(raw or "")

    normalized = token.strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in _YES_TOKENS:
        return "yes"
    if normalized in _NO_TOKENS:
        return "no"
    if normalized in _UNSURE_TOKENS:
        return "unsure"
    return "unknown"


def set_medicaid_ack(flag: bool) -> None:
    ensure_session()["medicaid_ack"] = bool(flag)


def get_medicaid_ack() -> bool:
    return bool(ensure_session().get("medicaid_ack"))


def set_progress(section: str, pct: int) -> None:
    """Clamp and store section progress (0-100)."""
    gcp = ensure_session()
    if section not in gcp["progress"]:
        gcp["progress"][section] = 0
    gcp["progress"][section] = max(0, min(int(pct), 100))


def resume_target() -> str:
    return str(ensure_session().get("resume_target", _DEFAULT_RESUME_PATH))


def set_resume_target(path: str) -> None:
    if not isinstance(path, str) or not path:
        return
    ensure_session()["resume_target"] = path


def get_progress(section: str) -> int:
    """Return progress for a section (0-100)."""
    return int(ensure_session().get("progress", {}).get(section, 0))
