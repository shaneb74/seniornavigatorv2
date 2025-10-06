from __future__ import annotations

import streamlit as st

from senior_nav import navigation
from senior_nav.documents import list_documents
from senior_nav.state import completions, ensure_base_state, require_entry_ready
from senior_nav.ui import header, render_ai_launcher, set_page_config


set_page_config(title="Care Planning Hub")
ensure_base_state()
require_entry_ready()
flags = completions()

visitor_name = st.session_state.get("visitor_name")
hero = "Welcome back" if visitor_name else "Your concierge care hub"
header(hero if not visitor_name else f"{hero}, {visitor_name}", "Pick up where you left off.")

with st.container():
    st.subheader("Planning modules")
    col1, col2, col3 = st.columns(3)

    with col1:
        status = "Complete" if flags.get("gcp") else "Start here"
        cta = "View plan" if flags.get("gcp") else "Begin plan"
        if st.button(f"🧭 Guided Care Plan\n{status}", key="hub_gcp", use_container_width=True):
            if st.session_state.get("entry_type"):
                navigation.switch_page(navigation.GCP_PAGE)
            else:
                navigation.switch_page(navigation.AUDIENCING_PAGE)
        st.caption("Answer step-by-step questions to capture needs and recommendations.")
        st.caption(status)

    with col2:
        cp_ready = bool(st.session_state.get("gcp"))
        cost_status = "Complete" if flags.get("cost_planner") else ("Ready" if cp_ready else "Locked")
        disabled = not cp_ready
        if st.button(
            f"💰 Cost Planner\n{cost_status}",
            key="hub_cost",
            disabled=disabled,
            use_container_width=True,
        ):
            navigation.switch_page(navigation.COST_PLANNER_PAGE)
        st.caption("Estimate ongoing costs based on your care plan recommendations.")

    with col3:
        pfma_status = "Booked" if flags.get("pfma") else "Next step"
        if st.button(
            f"🤝 Plan for My Advisor\n{pfma_status}",
            key="hub_pfma",
            use_container_width=True,
        ):
            navigation.switch_page(navigation.PFMA_PAGE)
        st.caption("Share updates and book time with your concierge advisor.")

st.markdown("---")

with st.container():
    st.subheader("Documents")
    docs = list_documents()
    if not docs:
        st.info("Your exported documents will appear here once you complete a module.")
    else:
        st.write(f"You have {len(docs)} document(s) ready to view.")
        if st.button("Open My Documents", key="hub_docs"):
            navigation.switch_page(navigation.DOCUMENTS_PAGE)

render_ai_launcher()
