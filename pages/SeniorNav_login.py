from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import ensure_aud, top_nav

st.set_page_config(layout="wide", page_title="Login")
inject_theme()
ensure_aud()
top_nav()
st.markdown("## Sign in")
with st.form("login"):
    u = st.text_input("Email")
    p = st.text_input("Password", type="password")
    ok = st.form_submit_button("Sign in", type="primary", use_container_width=True)
    if ok:
        st.session_state["auth_user"] = u
        st.success("Signed in")
        st.rerun()
