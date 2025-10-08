# Second Opinion request confirmation form
from __future__ import annotations

from datetime import datetime
from typing import Dict

import streamlit as st

from ui.theme import inject_theme


def _goto(path: str) -> None:
    try:
        st.switch_page(path)  # type: ignore[attr-defined]
    except Exception:
        st.session_state["nav_target"] = path
        st.rerun()


def _ensure_referrals() -> Dict[str, object]:
    referrals = st.session_state.get("referrals")
    if not isinstance(referrals, dict):
        referrals = {}
        st.session_state["referrals"] = referrals
    return referrals


def render() -> None:
    inject_theme()

    st.caption("Care Hub → Waiting Room → Second Opinion")
    st.title("Second Opinion Request")

    referrals = _ensure_referrals()
    request = referrals.get("second_opinion")
    if not isinstance(request, dict):
        st.warning("Start from the Waiting Room to choose a consult topic before completing this form.")
        if st.button("Back to Waiting Room", type="secondary"):
            _goto("app_pages/SeniorNav_waiting_room.py")
        return

    reason = request.get("reason", "—")
    timestamp = request.get("ts", "")

    st.markdown("### Your request")
    st.markdown(f"- **Reason:** {reason}")
    st.markdown(f"- **Requested at:** {timestamp or 'Pending'}")

    confirmation = referrals.get("second_opinion_form")
    if isinstance(confirmation, dict) and confirmation.get("submitted"):
        st.success("Thanks! We’ll follow up shortly to schedule your consult.")
        if st.button("Back to Waiting Room", type="secondary"):
            _goto("app_pages/SeniorNav_waiting_room.py")
        return

    with st.form("second_opinion_details"):
        name = st.text_input("Your name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        best_times = st.text_input("Best times to connect (optional)")
        submitted = st.form_submit_button("Submit request", type="primary")

    if submitted:
        if not name.strip() or not email.strip():
            st.warning("Name and email help our team reach you quickly—please add them before submitting.")
        else:
            referrals["second_opinion_form"] = {
                "name": name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "best_times": best_times.strip(),
                "reason": reason,
                "initial_ts": timestamp,
                "ts": datetime.utcnow().isoformat(),
                "submitted": True,
            }
            st.session_state["referrals"] = referrals
            st.success("Thanks! We’ll follow up shortly to schedule your consult.")

    if st.button("Back to Waiting Room", type="secondary"):
        _goto("app_pages/SeniorNav_waiting_room.py")


render()
