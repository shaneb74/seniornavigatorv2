from __future__ import annotations
import streamlit as st

def ensure_gcp() -> dict:
    g = st.session_state.get("gcp")
    if not isinstance(g, dict):
        st.session_state.gcp = {}
    return st.session_state.gcp

def get_gcp(key, default=None):
    return ensure_gcp().get(key, default)

def set_gcp(key, value):
    ensure_gcp()[key] = value
    return value
