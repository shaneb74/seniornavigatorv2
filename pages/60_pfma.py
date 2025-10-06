from __future__ import annotations

from datetime import date, time

import streamlit as st

from senior_nav import navigation
from senior_nav.state import completions, ensure_base_state, require_entry_ready
from senior_nav.ui import header, render_ai_launcher, set_page_config


set_page_config(title="Plan for My Advisor")
ensure_base_state()
require_entry_ready()
flags = completions()

header("Plan for My Advisor", "Share details and confirm your advisor appointment.")

snapshot = st.session_state.get("gcp")
if snapshot:
    with st.expander("Care plan snapshot"):
        st.json({k: v for k, v in snapshot.items() if k != "answers"})
        st.markdown("**Medicaid question:** " + snapshot.get("answers", {}).get("medicaid_q0", "Unsure"))

existing = st.session_state.get("pfma") or {}

with st.form("pfma_form"):
    appointment_date = st.date_input(
        "Preferred appointment date",
        value=existing.get("appointment_date", date.today()),
    )
    appointment_time = st.time_input(
        "Preferred time",
        value=existing.get("appointment_time", time(hour=11, minute=0)),
    )
    contact = st.text_input(
        "Best phone or email",
        value=existing.get("contact_info", ""),
    )
    notes = st.text_area(
        "Notes for your advisor",
        value=existing.get("notes", ""),
        placeholder="Share goals, questions, or constraints.",
    )
    submitted = st.form_submit_button("Book appointment", type="primary")

if submitted:
    st.session_state.pfma = {
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "contact_info": contact,
        "notes": notes,
    }
    flags.mark("pfma", True)
    st.success("Advisor appointment captured. Returning to the hub.")
    navigation.switch_page(navigation.HUB_PAGE)

render_ai_launcher()
