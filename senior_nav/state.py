"""Session state helpers for the simplified Senior Navigator flow."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, MutableMapping

import streamlit as st


@dataclass
class CompletionFlags:
    """Simple view over module completion state."""

    data: MutableMapping[str, bool] = field(default_factory=dict)

    def get(self, key: str) -> bool:
        return bool(self.data.get(key, False))

    def mark(self, key: str, value: bool = True) -> None:
        self.data[key] = bool(value)


DEFAULT_STATE: Dict[str, Any] = {
    "entry_ready": False,
    "entry_type": None,
    "visitor_name": "",
    "gcp": None,
    "cost_planner": {},
    "pfma": None,
    "documents_registry": {},
    "completion": {},
    "ai_messages": [],
}


def ensure_base_state() -> None:
    """Populate baseline keys so downstream pages can rely on them."""

    for key, value in DEFAULT_STATE.items():
        if key in st.session_state:
            continue
        if isinstance(value, dict):
            st.session_state[key] = dict(value)
        elif isinstance(value, list):
            st.session_state[key] = list(value)
        else:
            st.session_state[key] = value


def completions() -> CompletionFlags:
    """Return a lightweight adapter around completion flags."""

    ensure_base_state()
    data = st.session_state.setdefault("completion", {})
    return CompletionFlags(data)


def require_entry_ready() -> None:
    """Redirect to the welcome page when a session has not started."""

    ensure_base_state()
    if not st.session_state.get("entry_ready"):
        from .navigation import switch_page, WELCOME_PAGE

        switch_page(WELCOME_PAGE)
        st.stop()


def require_entry_type() -> None:
    """Ensure the audience selection has been made before continuing."""

    require_entry_ready()
    if not st.session_state.get("entry_type"):
        from .navigation import AUDIENCING_PAGE, switch_page

        switch_page(AUDIENCING_PAGE)
        st.stop()
