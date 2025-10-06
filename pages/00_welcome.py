from __future__ import annotations

import streamlit as st

from senior_nav import navigation
from senior_nav.state import ensure_base_state
from senior_nav.ui import set_page_config


set_page_config(title="Welcome")
ensure_base_state()

if st.session_state.get("entry_ready"):
    st.info("Welcome back! You're all set to continue planning.")
    if st.button("Go to hub", type="primary"):
        navigation.switch_page(navigation.HUB_PAGE)

st.markdown(
    """
    <div style="max-width:720px;">
      <h1>Senior Care Navigator</h1>
      <p style="font-size:1.05rem;line-height:1.6;">
        Answer a few questions, explore cost options, and share details with your concierge advisor.
        Tell us who you're planning for and we'll tailor the experience.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("welcome_form"):
    name = st.text_input(
        "What's your name? (optional)",
        value=st.session_state.get("visitor_name", ""),
        placeholder="Alex",
    )
    submitted = st.form_submit_button("Continue", type="primary")

if submitted:
    st.session_state.visitor_name = name.strip()
    st.session_state.entry_ready = True
    navigation.switch_page(navigation.HUB_PAGE)
