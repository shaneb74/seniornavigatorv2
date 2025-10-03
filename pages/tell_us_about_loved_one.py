"""Proxy-entry audiencing flow capturing names and qualifiers."""

from __future__ import annotations
from ui.theme import inject_theme

import streamlit as st

from audiencing import (
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    URGENT_FEATURE_FLAG,
    apply_audiencing_sanitizer,
    compute_audiencing_route,
    ensure_audiencing_state,
    log_audiencing_set,
    snapshot_audiencing,
)

st.set_page_config(page_title="Tell Us About Your Loved One", layout="wide")

state = ensure_audiencing_state()
state["entry"] = "proxy"
apply_audiencing_sanitizer(state)
qualifiers = state["qualifiers"]
people = state.setdefault("people", {"recipient_name": "", "proxy_name": ""})

st.title("Tell Us About Your Loved One")
st.caption("These toggles make sure the right guidance shows up first.")

with st.form("audiencing_proxy_form"):
    recipient_name = st.text_input(
        "What is their name?",
        value=people.get("recipient_name", ""),
        help="We use this to personalize the Hub for them.",
    )
    proxy_name = st.text_input(
        "What is your name?",
        value=people.get("proxy_name", ""),
        help="Optional, for caregiver-facing notes.",
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        is_veteran = st.toggle(
            "Are they a veteran?",
            value=qualifiers.get("is_veteran", False),
            key="aud_proxy_is_veteran",
        )
        owns_home = st.toggle(
            "Do they own their home?",
            value=qualifiers.get("owns_home", False),
            key="aud_proxy_owns_home",
        )
    with col2:
        has_partner = st.toggle(
            "Do they have a partner?",
            value=qualifiers.get("has_partner", False),
            key="aud_proxy_has_partner",
        )
        on_medicaid = st.toggle(
            "Are they on Medicaid?",
            value=qualifiers.get("on_medicaid", False),
            key="aud_proxy_on_medicaid",
        )

    urgent_case = False
    if URGENT_FEATURE_FLAG:
        urgent_case = st.toggle(
            "Is this urgent?",
            value=qualifiers.get("urgent", False),
            key="aud_proxy_urgent",
        )

    submitted = st.form_submit_button("Continue", use_container_width=True)

if submitted:
    people["recipient_name"] = recipient_name.strip()
    people["proxy_name"] = proxy_name.strip()
    qualifiers.update(
        {
            "is_veteran": bool(is_veteran),
            "has_partner": bool(has_partner),
            "owns_home": bool(owns_home),
            "on_medicaid": bool(on_medicaid),
            "urgent": bool(urgent_case) if URGENT_FEATURE_FLAG else False,
        }
    )
    apply_audiencing_sanitizer(state)
    compute_audiencing_route(state)
    snapshot = snapshot_audiencing(state)
    st.session_state["audiencing_snapshot"] = snapshot
    log_audiencing_set(snapshot)
    st.switch_page("pages/hub.py")

st.divider()

with st.expander("Debug: Audiencing state", expanded=False):
    st.json(state)
    st.markdown("---")
    st.json(st.session_state.get("audiencing_snapshot", {}))

st.button("Back to Welcome", on_click=lambda: st.switch_page("pages/welcome.py"))

st.markdown('</div>', unsafe_allow_html=True)
