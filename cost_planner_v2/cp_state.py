from __future__ import annotations
from typing import Any, Dict
import streamlit as st

_CP_KEY = "cp"

def ensure_cp() -> Dict[str, Any]:
    """Return the Cost Planner state dict in session_state, creating it if missing."""
    store = st.session_state.get(_CP_KEY)
    if not isinstance(store, dict):
        store = {}
        st.session_state[_CP_KEY] = store
    return store

# --- Back-compat wrappers used by older pages (no recursion) ---
def ensure_cp_state() -> Dict[str, Any]:
    return ensure_cp()

def ensure_cp_session() -> Dict[str, Any]:
    return ensure_cp()

def get_cp(key: str, default=None):
    return ensure_cp().get(key, default)

def set_cp(key: str, value):
    ensure_cp()[key] = value
    return value
