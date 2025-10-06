from __future__ import annotations
import streamlit as st
import app_pages.SeniorNav_welcome_base as base
from app_pages.SeniorNav_welcome_base import render


def safe_switch_page(target: str, query_key: str | None = None, query_value: str | None = None) -> None:
    try:
        st.switch_page(target)
    except Exception:
        if query_key and query_value:
            st.query_params[query_key] = query_value
        st.rerun()


def _route(target: str, query_key: str | None = None, query_value: str | None = None) -> None:
    mapping = {
        "pages/guided_care_hub.py": "app_pages/hub.py",
        "app_pages/guided_care_hub.py": "app_pages/hub.py",
        "pages/welcome.py": "app_pages/welcome.py",
        "app_pages/welcome.py": "app_pages/welcome.py",
    }
    destination = mapping.get(target, target)
    safe_switch_page(destination, query_key, query_value)


_original_safe_switch = base.safe_switch
base.safe_switch = _route
try:
    render("self")
finally:
    base.safe_switch = _original_safe_switch

st.markdown("</div>", unsafe_allow_html=True)
