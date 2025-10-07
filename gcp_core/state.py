from __future__ import annotations

from typing import List

import streamlit as st
from gcp_pr_tool_bundle.guided_care_plan.state import *  # noqa: F401,F403
from gcp_pr_tool_bundle.guided_care_plan.state import (
    get_answers as _bundle_get_answers,
    set_answer as _bundle_set_answer,
    normalize_multi as _normalize_multi,
)  # noqa: F401

from .questions import BEHAVIOR_RISKS_OPTIONS

BEHAVIOR_RISKS_QID = "behavior_risks"
_BEHAVIOR_RISK_ORDER = [token for token, _ in BEHAVIOR_RISKS_OPTIONS]
_BEHAVIOR_RISK_TOKENS = set(_BEHAVIOR_RISK_ORDER)
_BEHAVIOR_RISK_INDEX = {token: index for index, token in enumerate(_BEHAVIOR_RISK_ORDER)}


SECTION_PATHS = {
    "landing": "app_pages/gcp_v2/gcp_landing_v2.py",
    "daily": "app_pages/gcp_v2/gcp_daily_life_v2.py",
    "safety": "app_pages/gcp_v2/gcp_health_safety_v2.py",
    "context": "app_pages/gcp_v2/gcp_context_prefs_v2.py",
    "recommendation": "app_pages/gcp_v2/gcp_recommendation_v2.py",
}

PROGRESS_KEYS = ("landing", "daily", "safety", "context", "done")


def ensure_session() -> None:
    answers = _bundle_get_answers()
    gcp = st.session_state.get("gcp")
    if not isinstance(gcp, dict):
        st.session_state.gcp = {
            "answers": answers,
            "progress": {key: False for key in PROGRESS_KEYS},
            "snapshots": [],
        }
    else:
        gcp.setdefault("answers", answers)
        gcp.setdefault("progress", {key: False for key in PROGRESS_KEYS})
        gcp.setdefault("snapshots", [])
        gcp["answers"] = answers


def get_state() -> dict:
    ensure_session()
    return st.session_state.gcp


def get_answer(key: str, default=None):
    ensure_session()
    answers = st.session_state.gcp["answers"]
    if key == BEHAVIOR_RISKS_QID:
        normalized = _normalize_behavior_risks(answers.get(key))
        if normalized:
            answers[key] = normalized
            return list(normalized)
        answers.pop(key, None)
        return []
    return answers.get(key, default)


def set_answer(key: str, value) -> None:
    ensure_session()
    answers = st.session_state.gcp["answers"]
    if key == BEHAVIOR_RISKS_QID:
        normalized = _normalize_behavior_risks(value)
        if not normalized:
            answers.pop(key, None)
            _bundle_set_answer(key, None)
            return
        _bundle_set_answer(key, normalized)
        answers[key] = list(normalized)
        return

    if value is None or (isinstance(value, str) and not value.strip()):
        answers.pop(key, None)
        _bundle_set_answer(key, None)
        return
    if isinstance(value, list):
        value = _normalize_multi(value)
    _bundle_set_answer(key, value)
    answers[key] = value
    if key == "medicaid_status" and value == "no":
        # Clearing any lingering acknowledgement flag keeps the landing notice honest.
        answers.pop("medicaid_ack", None)
        st.session_state.pop("gcp_ack_medicaid_notice", None)


def set_section_complete(name: str) -> None:
    ensure_session()
    if name in st.session_state.gcp["progress"]:
        st.session_state.gcp["progress"][name] = True


def latest_snapshot() -> dict | None:
    ensure_session()
    snapshots = st.session_state.gcp["snapshots"]
    return snapshots[-1] if snapshots else None


def save_snapshot(snapshot: dict) -> None:
    ensure_session()
    snapshots = st.session_state.gcp["snapshots"]
    if snapshots:
        last = snapshots[-1]
        if (
            last.get("version") == snapshot.get("version")
            and last.get("answers") == snapshot.get("answers")
        ):
            snapshots[-1] = snapshot
            return
    snapshots.append(snapshot)


def resume_target() -> str:
    ensure_session()
    progress = st.session_state.gcp["progress"]
    order = [
        ("landing", SECTION_PATHS["landing"]),
        ("daily", SECTION_PATHS["daily"]),
        ("safety", SECTION_PATHS["safety"]),
        ("context", SECTION_PATHS["context"]),
    ]
    for key, path in order:
        if not progress.get(key):
            return path
    return SECTION_PATHS["recommendation"]


# ---- Medicaid helpers (session-scoped ack) ----
def norm(val: str | None) -> str:
    return (val or "").strip().lower()


def medicaid_status(answers: dict) -> str:
    return norm(answers.get("medicaid_status"))


def set_ack_medicaid(flag: bool) -> None:
    import streamlit as st
    st.session_state["gcp_ack_medicaid_notice"] = bool(flag)


def get_ack_medicaid() -> bool:
    import streamlit as st
    return bool(st.session_state.get("gcp_ack_medicaid_notice"))


def _normalize_behavior_risks(value: object) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    elif isinstance(value, set):
        value = list(value)
    elif isinstance(value, tuple):
        value = list(value)

    if not isinstance(value, list):
        return []

    seen = set()
    cleaned = []
    for token in value:
        if not isinstance(token, str):
            continue
        token = token.strip()
        if not token or token not in _BEHAVIOR_RISK_TOKENS or token in seen:
            continue
        seen.add(token)
        cleaned.append(token)

    cleaned.sort(key=lambda token: _BEHAVIOR_RISK_INDEX.get(token, len(_BEHAVIOR_RISK_ORDER)))
    return cleaned


def behavior_risks() -> List[str]:
    """Return the normalized behavior risk selections."""
    return get_answer(BEHAVIOR_RISKS_QID, [])
