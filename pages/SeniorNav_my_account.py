from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import ensure_aud, top_nav

st.set_page_config(layout="wide", page_title="My Account")
inject_theme()
ensure_aud()
top_nav()
st.markdown("## My Account")
with st.form("acct"):
    name = st.text_input("Name", value=st.session_state.aud.get("recipient_name",""))
    email = st.text_input("Email")
    prefs = st.text_area("Preferences")
    ok = st.form_submit_button("Save", type="primary", use_container_width=True)
    if ok:
        st.session_state.aud["recipient_name"] = name
        st.success("Saved")
