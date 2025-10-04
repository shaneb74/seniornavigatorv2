"""Session state helpers for the cost planner wizard."""
from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import streamlit as st

_DEFAULT_STATE: Dict[str, Any] = {
    "mode": "exploring",
    "qualifiers": {
        "contribution_style": "unified",
        "contributors": [],
        "owns_home": None,
        "is_veteran": None,
    },
    "drawer_status": {
        "housing": "start",
        "care": "start",
        "medical": "start",
        "insurance_benefits": "start",
        "debts_other": "start",
    },
    "ui": {
        "progress": 0,
        "suggestions_shown": set(),
    },
}


def ensure_state() -> None:
    """Ensure the cost planner state exists in ``st.session_state``."""
    if "cp" not in st.session_state:
        st.session_state["cp"] = copy.deepcopy(_DEFAULT_STATE)
    ui = st.session_state["cp"].setdefault("ui", {})
    if not isinstance(ui.get("suggestions_shown"), set):
        ui["suggestions_shown"] = set(ui.get("suggestions_shown", []))


def get_state() -> Dict[str, Any]:
    ensure_state()
    return st.session_state["cp"]


def get_flags() -> Dict[str, Any]:
    return st.session_state.get("flags", {})


def get_gcp_state() -> Dict[str, Any]:
    return st.session_state.get("gcp", {})


def get_progress() -> int:
    return get_state()["ui"].get("progress", 0)


def set_progress(index: int) -> None:
    state = get_state()
    state["ui"]["progress"] = max(0, index)


def set_mode(mode: str) -> None:
    get_state()["mode"] = mode


def update_qualifier(key: str, value: Any) -> None:
    get_state()["qualifiers"][key] = value


def set_drawer_status(key: str, status: str) -> None:
    get_state()["drawer_status"][key] = status


def mark_suggestions_seen(suggestion_ids: set[str]) -> None:
    if not suggestion_ids:
        return
    seen = get_state()["ui"].setdefault("suggestions_shown", set())
    seen.update(suggestion_ids)


@lru_cache(maxsize=1)
def get_copy() -> Dict[str, Any]:
    """Load and cache the cost planner copy."""
    path = Path("copy/cost_planner_strings.json")
    return json.loads(path.read_text())
