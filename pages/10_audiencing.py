from __future__ import annotations

import streamlit as st

from senior_nav import navigation
from senior_nav.state import ensure_base_state, require_entry_ready
from senior_nav.ui import header, render_ai_launcher, set_page_config


set_page_config(title="Who are you planning for?")
ensure_base_state()
require_entry_ready()

header("Who are you planning for?", "This helps tailor the questions and resources.")

options = {
    "For myself": "self",
    "For someone else": "proxy",
    "I'm a professional": "pro",
}

existing = st.session_state.get("entry_type")
labels = list(options.keys())
index = labels.index(next((label for label, key in options.items() if key == existing), labels[1])) if existing else 1

with st.form("audiencing_form"):
    choice_label = st.radio("Select the option that fits best", labels, index=index)
    submitted = st.form_submit_button("Continue to guided plan", type="primary")

if submitted:
    st.session_state.entry_type = options[choice_label]
    navigation.switch_page(navigation.GCP_PAGE)

render_ai_launcher()
