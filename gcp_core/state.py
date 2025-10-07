from __future__ import annotations

import re
from collections.abc import MutableMapping
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

_MISSING = object()


def norm_token(value: str | None) -> str:
    """Normalize a freeform value into a safe, lowercase token."""
    if not value:
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\w]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


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


def _answers_dict() -> dict:
    ensure_session()
    return st.session_state.gcp["answers"]


def get_state() -> dict:
    ensure_session()
    return st.session_state.gcp


def _normalize_for_store(key: str, value):
    if key == BEHAVIOR_RISKS_QID:
        normalized = _normalize_behavior_risks(value)
        if not normalized:
            return False, None
        return True, list(normalized)

    if value is None:
        return False, None

    if isinstance(value, str):
        trimmed = value.strip()
        if not trimmed:
            return False, None
        return True, trimmed

    if isinstance(value, (set, tuple)):
        value = list(value)

    if isinstance(value, list):
        normalized_list = _normalize_multi(value)
        if not normalized_list:
            return False, None
        return True, normalized_list

    return True, value


def _resolve_get_args(target, maybe_qid, default):
    if isinstance(target, MutableMapping):
        if maybe_qid is _MISSING:
            raise TypeError("qid is required when providing an answers mapping")
        return target, maybe_qid, default

    key = target
    default_value = default
    if maybe_qid is not _MISSING:
        default_value = maybe_qid
    answers = _answers_dict()
    return answers, key, default_value


def get_answer(target, maybe_qid=_MISSING, default=None):
    answers, key, default_value = _resolve_get_args(target, maybe_qid, default)

    if key == BEHAVIOR_RISKS_QID:
        normalized = _normalize_behavior_risks(answers.get(key))
        if normalized:
            answers[key] = list(normalized)
            return list(normalized)
        answers.pop(key, None)
        return default_value if default_value is not None else []

    value = answers.get(key, _MISSING)
    if value is _MISSING:
        return default_value

    if isinstance(value, str):
        trimmed = value.strip()
        if not trimmed:
            answers.pop(key, None)
            return default_value
        return trimmed

    return value


def _resolve_set_args(target, maybe_qid, maybe_value):
    if isinstance(target, MutableMapping):
        if maybe_qid is _MISSING or maybe_value is _MISSING:
            raise TypeError("qid and value are required when providing an answers mapping")
        return target, maybe_qid, maybe_value, False

    if maybe_qid is _MISSING:
        raise TypeError("value is required")

    answers = _answers_dict()
    return answers, target, maybe_qid, True


def set_answer(target, maybe_qid=_MISSING, value=_MISSING) -> None:
    answers, key, raw_value, write_bundle = _resolve_set_args(target, maybe_qid, value)

    should_store, normalized_value = _normalize_for_store(key, raw_value)

    if should_store:
        answers[key] = normalized_value
    else:
        answers.pop(key, None)

    if write_bundle:
        _bundle_set_answer(key, normalized_value if should_store else None)
        if key == "medicaid_status" and normalized_value == "no":
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
