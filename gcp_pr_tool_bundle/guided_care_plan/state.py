import streamlit as st

def get_answers() -> dict:
    return st.session_state.setdefault("gcp_answers", {})

def set_answer(key: str, value):
    get_answers()[key] = value

def get_aud() -> dict:
    return (st.session_state.get("audiencing") or {}).get("qualifiers", {}) or {}

def normalize_multi(vals):
    vals = set(vals or [])
    if "none" in vals:
        return []
    return sorted(vals)
