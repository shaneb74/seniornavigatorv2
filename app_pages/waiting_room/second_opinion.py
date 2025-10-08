# Waiting Room Second Opinion stub
from __future__ import annotations

from datetime import datetime

import streamlit as st


def _state() -> dict:
    data = st.session_state.get("second_opinion")
    if not isinstance(data, dict):
        data = {}
    st.session_state["second_opinion"] = data
    return data


def render() -> None:
    st.title("Waiting Room · Second Opinion")
    st.write("Request a consult and we’ll follow up with available times.")

    submitted_state = _state()
    last = submitted_state.get("last_request")
    if isinstance(last, dict):
        st.success("Request submitted. We’ll reach out shortly.")
        st.markdown(
            f"**Topic:** {last.get('topic', '—')}  \n**Submitted:** {last.get('ts', '—')}"
        )

    with st.form("second_opinion_request"):
        name = st.text_input("Name")
        contact = st.text_input("Preferred contact (email or phone)")
        topic = st.selectbox(
            "Topic",
            [
                "Medication review",
                "Behavior changes",
                "Safety & falls",
                "Care planning",
                "Other",
            ],
        )
        submitted = st.form_submit_button("Submit Request", type="primary")

    if submitted:
        if not name.strip() or not contact.strip():
            st.warning("Add your name and contact so we can follow up.")
        else:
            payload = {
                "name": name.strip(),
                "contact": contact.strip(),
                "topic": topic,
                "ts": datetime.utcnow().isoformat(),
            }
            submitted_state["last_request"] = payload
            st.session_state["second_opinion"] = submitted_state
            st.success("Request submitted. We’ll reach out shortly.")

    if st.button("Back to Waiting Room", type="secondary"):
        try:
            st.switch_page("app_pages/SeniorNav_waiting_room.py")  # type: ignore[attr-defined]
        except Exception:
            st.session_state["nav_target"] = "app_pages/SeniorNav_waiting_room.py"
            st.rerun()


render()
