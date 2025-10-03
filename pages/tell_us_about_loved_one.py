"""Proxy-entry audiencing flow with unified design system."""

from __future__ import annotations

import streamlit as st

from audiencing import (
    URGENT_FEATURE_FLAG,
    apply_audiencing_sanitizer,
    compute_audiencing_route,
)

st.set_page_config(page_title="Tell us about your loved one", layout="wide")

# ---------------------------------------------------------------------------
# Session defaults
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
route = audiencing.setdefault("route", {"next": None})
route.setdefault("next", None)
audiencing.setdefault("recipient_name", None)
audiencing.setdefault("proxy_name", None)

care_context = st.session_state.setdefault(
    "care_context",
    {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,
        "gcp_cost": None,
    },
)

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
st.markdown("""
<div style="display:flex; flex-direction:column; gap:0.8rem;">
  <div>
    <h1>Tell us about your loved one</h1>
    <p style="max-width:640px; color:#475569;">These details help us tailor the guidance to their household and benefits.</p>
  </div>
</div>
""", unsafe_allow_html=True)

name_cols = st.columns(2, gap="large")
with name_cols[0]:
    recipient_name = st.text_input(
        "What’s their name?",
        value=audiencing.get("recipient_name") or "",
        placeholder="Add the person you’re caring for",
    )
with name_cols[1]:
    proxy_name = st.text_input(
        "What’s your name?",
        value=audiencing.get("proxy_name") or "",
        placeholder="Optional",
    )

qualifier_cards = [
    {
        "key": "is_veteran",
        "label": "Are they a veteran?",
        "hint": "Impacts benefits and offsets.",
    },
    {
        "key": "has_partner",
        "label": "Do they have a partner?",
        "hint": "Determines household setup.",
    },
    {
        "key": "owns_home",
        "label": "Do they own their home?",
        "hint": "Affects housing and home modifications.",
    },
    {
        "key": "on_medicaid",
        "label": "Are they on Medicaid?",
        "hint": "We will show you the right path.",
    },
]

if URGENT_FEATURE_FLAG:
    qualifier_cards.append(
        {
            "key": "urgent",
            "label": "Is this urgent?",
            "hint": "We’ll prioritize faster options if needed.",
        }
    )

columns = st.columns(2, gap="large")
for idx, card in enumerate(qualifier_cards):
    col = columns[idx % 2]
    with col:
        st.markdown('<div class="sn-field-card">', unsafe_allow_html=True)
        toggle_value = st.toggle(
            card["label"],
            value=bool(qualifiers.get(card["key"], False)),
            key=f"aud_proxy_{card['key']}",
        )
        st.markdown(
            f"<div class='sn-field-hint'>{card['hint']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        qualifiers[card["key"]] = bool(toggle_value)

# Normalize, compute route, and snapshot
audiencing["recipient_name"] = (recipient_name or "").strip() or None
audiencing["proxy_name"] = (proxy_name or "").strip() or None
qualifiers.setdefault("urgent", False)
if not URGENT_FEATURE_FLAG:
    qualifiers["urgent"] = False

apply_audiencing_sanitizer(audiencing)
audiencing["route"] = compute_audiencing_route(audiencing)

care_context["person_name"] = audiencing.get("recipient_name") or "Your Loved One"

st.session_state["audiencing_snapshot"] = {
    "entry": audiencing["entry"],
    "qualifiers": audiencing["qualifiers"].copy(),
    "route": audiencing["route"].copy(),
}

ready = audiencing.get("recipient_name") is not None

with st.container():
    st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
    footer_cols = st.columns([1, 1, 1])
    continue_clicked = False
    disabled_reason = None if ready else "Enter your loved one’s name to continue."
    with footer_cols[1]:
        continue_clicked = st.button(
            "Go to your Concierge Care Hub",
            type="primary",
            use_container_width=True,
            key="aud_proxy_continue",
            disabled=not ready,
            help=disabled_reason,
        )
    st.markdown('</div><div class="sn-footer-note">Personalized guidance will reference them by name.</div></div>', unsafe_allow_html=True)

if continue_clicked:
    st.session_state["last_event"] = {"type": "audiencing_set"}
    st.switch_page("pages/hub.py")

with st.expander("Debug: Audiencing state", expanded=False):
    st.json(audiencing)
    st.markdown("---")
    st.json(st.session_state.get("audiencing_snapshot", {}))

if st.button("Back to Welcome", type="secondary"):
    st.switch_page("pages/welcome.py")
