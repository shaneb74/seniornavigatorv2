from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme

def ensure_aud():
    if "aud" not in st.session_state or not isinstance(st.session_state.aud, dict):
        st.session_state.aud = {
            "entry": None,
            "recipient_name": "",
            "relationship_code": "",
            "relationship_label": "",
            "relationship_other": "",
            "professional_type": "",
            "proxy_name": "",
            "qualifiers": {},
        }
    return st.session_state.aud

def safe_switch(path: str):
    try:
        st.switch_page(path)
    except Exception:
        st.query_params["next"] = path
        st.rerun()

def top_nav():
    st.markdown(
        """
        <div style="display:flex;justify-content:flex-end;gap:.5rem;margin:-8px 0 8px 0">
          <a href="?page=pages/SeniorNav_ai_advisor.py" style="text-decoration:none;padding:.4rem .75rem;border:1px solid rgba(0,0,0,.08);border-radius:999px;background:var(--surface);color:var(--ink);font-weight:600;">AI Advisor</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

def pfma_card(title: str | None = None, subtitle: str = ""):
    inject_theme()
    return st.container(border=False)

