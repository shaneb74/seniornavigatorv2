"""Self-entry audiencing flow with qualifier toggles."""
from __future__ import annotations


from ui.theme import inject_theme

import streamlit as st

from audiencing import (

    URGENT_FEATURE_FLAG,
    apply_audiencing_sanitizer,
    compute_audiencing_route,
    ensure_audiencing_state,
    log_audiencing_set,
    snapshot_audiencing,


)
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


st.set_page_config(page_title="Tell Us About You", layout="wide")

state = ensure_audiencing_state()
state["entry"] = "self"
apply_audiencing_sanitizer(state)
qualifiers = state["qualifiers"]
people = state.setdefault("people", {"recipient_name": "", "proxy_name": ""})

st.title("Tell Us About You")
st.caption("These quick yes/no toggles tailor what you see next.")

with st.form("audiencing_self_form"):
    name = st.text_input(
        "What should we call you?",
        value=people.get("recipient_name", ""),
        help="Optional. We use this name in the Hub to personalize your plan.",
    )

    col1, col2 = st.columns(2, gap="large")
    with col1:
        is_veteran = st.toggle(
            "Are you a veteran?",
            value=qualifiers.get("is_veteran", False),
            key="aud_self_is_veteran",
        )
        owns_home = st.toggle(
            "Do you own your home?",
            value=qualifiers.get("owns_home", False),
            key="aud_self_owns_home",
        )
    with col2:
        has_partner = st.toggle(
            "Do you have a partner?",
            value=qualifiers.get("has_partner", False),
            key="aud_self_has_partner",
        )
        on_medicaid = st.toggle(
            "Are you on Medicaid?",
            value=qualifiers.get("on_medicaid", False),
            key="aud_self_on_medicaid",
        )

    urgent_case = False
    if URGENT_FEATURE_FLAG:
        urgent_case = st.toggle(
            "Is this urgent?",
            value=qualifiers.get("urgent", False),
            key="aud_self_urgent",
        )

    submitted = st.form_submit_button("Continue", use_container_width=True)

if submitted:
    people["recipient_name"] = name.strip()
    people["proxy_name"] = ""
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