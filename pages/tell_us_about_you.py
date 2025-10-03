"""Self-entry audiencing flow with qualifier toggles."""

from __future__ import annotations

import streamlit as st

from audiencing import (
    URGENT_FEATURE_FLAG,
    apply_audiencing_sanitizer,
    compute_audiencing_route,
)

st.set_page_config(page_title="Tell Us About You", layout="wide")

st.title("Tell Us About You")
st.caption("These quick yes/no toggles tailor what you see next.")

# ---------------------------------------------------------------------------
# Ensure audiencing + care context defaults follow the shared contract
# ---------------------------------------------------------------------------
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

audiencing["entry"] = "self"

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

qualifiers.update(
    {
        "is_veteran": bool(is_veteran),
        "has_partner": bool(has_partner),
        "owns_home": bool(owns_home),
        "on_medicaid": bool(on_medicaid),
        "urgent": bool(urgent_case) if URGENT_FEATURE_FLAG else False,
    }
)

audiencing["recipient_name"] = None
audiencing["proxy_name"] = None

# Normalize, compute the route, and prep the snapshot before rendering the CTA
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
care_context["person_name"] = "You"

st.session_state["audiencing_snapshot"] = {
    "entry": audiencing["entry"],
    "qualifiers": audiencing["qualifiers"].copy(),
    "route": audiencing["route"].copy(),
}

st.write("")
st.divider()

if st.button(
    "Go to your Concierge Care Hub",
    type="primary",
    use_container_width=True,
):
    st.session_state["last_event"] = {"type": "audiencing_set"}
    st.switch_page("pages/hub.py")

with st.expander("Debug: Audiencing state", expanded=False):
    st.json(audiencing)
    st.markdown("---")
    st.json(st.session_state.get("audiencing_snapshot", {}))

st.button("Back to Welcome", on_click=lambda: st.switch_page("pages/welcome.py"))
