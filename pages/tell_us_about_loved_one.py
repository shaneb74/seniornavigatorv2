"""Proxy-entry audiencing flow capturing names and qualifiers."""

from __future__ import annotations

import streamlit as st

from audiencing import (
    URGENT_FEATURE_FLAG,
    apply_audiencing_sanitizer,
    compute_audiencing_route,
)

st.set_page_config(page_title="Tell Us About Your Loved One", layout="wide")

st.title("Tell Us About Your Loved One")
st.caption("These toggles make sure the right guidance shows up first.")

audiencing = st.session_state.setdefault(
    "audiencing",
    {
        "entry": None,
        "qualifiers": {
            "is_veteran": False,
            "has_partner": False,
            "owns_home": False,
            "on_medicaid": False,
            "urgent": False,
        },
        "route": {"next": None},
        "recipient_name": None,
        "proxy_name": None,
    },
)

audiencing["entry"] = "proxy"

qualifiers = audiencing.setdefault(
    "qualifiers",
    {
        "is_veteran": False,
        "has_partner": False,
        "owns_home": False,
        "on_medicaid": False,
        "urgent": False,
    },
)

for key in ("is_veteran", "has_partner", "owns_home", "on_medicaid", "urgent"):
    qualifiers.setdefault(key, False)

route = audiencing.setdefault("route", {"next": None})
route.setdefault("next", None)

audiencing.setdefault("recipient_name", None)
audiencing.setdefault("proxy_name", None)

recipient_name = st.text_input(
    "What is their name?",
    value=audiencing.get("recipient_name") or "",
    help="We use this to personalize the Hub for them.",
)
proxy_name = st.text_input(
    "What is your name?",
    value=audiencing.get("proxy_name") or "",
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

qualifiers.update(
    {
        "is_veteran": bool(is_veteran),
        "has_partner": bool(has_partner),
        "owns_home": bool(owns_home),
        "on_medicaid": bool(on_medicaid),
        "urgent": bool(urgent_case) if URGENT_FEATURE_FLAG else False,
    }
)

audiencing["recipient_name"] = (recipient_name or "").strip() or None
audiencing["proxy_name"] = (proxy_name or "").strip() or None

apply_audiencing_sanitizer(audiencing)
audiencing["route"] = compute_audiencing_route(audiencing)

care_context = st.session_state.setdefault(
    "care_context",
    {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,
        "gcp_cost": None,
    },
)
care_context["person_name"] = audiencing.get("recipient_name") or "Your Loved One"

st.session_state["audiencing_snapshot"] = {
    "entry": audiencing["entry"],
    "qualifiers": audiencing["qualifiers"].copy(),
    "route": audiencing["route"].copy(),
}

ready = audiencing.get("recipient_name") is not None

st.write("")
st.divider()

disabled_reason = None
if not ready:
    disabled_reason = "Enter your loved one's name to continue."

if st.button(
    "Go to your Concierge Care Hub",
    type="primary",
    use_container_width=True,
    disabled=not ready,
    help=disabled_reason,
):
    st.session_state["last_event"] = {"type": "audiencing_set"}
    st.switch_page("pages/hub.py")

with st.expander("Debug: Audiencing state", expanded=False):
    st.json(audiencing)
    st.markdown("---")
    st.json(st.session_state.get("audiencing_snapshot", {}))

st.button("Back to Welcome", on_click=lambda: st.switch_page("pages/welcome.py"))
