"""Concierge Care Hub that adapts to the audiencing snapshot."""

from __future__ import annotations

import streamlit as st

from audiencing import (
    URGENT_FEATURE_FLAG,
    apply_audiencing_sanitizer,
    ensure_audiencing_state,
    snapshot_audiencing,
)

st.set_page_config(page_title="Concierge Care Hub", layout="wide")

state = ensure_audiencing_state()
apply_audiencing_sanitizer(state)
snapshot = snapshot_audiencing(state)
st.session_state["audiencing_snapshot"] = snapshot

visibility = snapshot["visibility"]
flags = snapshot["flags"]
route_next = snapshot.get("route", {}).get("next") or "gcp"

people = snapshot.get("people", {})
if snapshot.get("entry") == "self":
    person_display = people.get("recipient_name") or "you"
else:
    person_display = people.get("recipient_name") or "your loved one"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
HIDDEN_TOOLTIPS = {
    "partner": "Partner planning is hidden because you told us there isn't a partner involved.",
    "home": "Home ownership tools are hidden when the household does not own a home.",
    "veteran": "Veteran-specific resources are hidden if the person is not a veteran.",
}

hidden_items: list[tuple[str, str]] = []

def visible_item(tags: list[str], label: str) -> bool:
    """Determine if a card tagged with qualifiers should be shown."""

    for tag in tags:
        if not visibility.get(tag, True):
            hidden_items.append((label, tag))
            return False
    return True


def switch_page_if(path: str) -> None:
    """Helper to switch pages from within button callbacks."""

    if path:
        st.switch_page(path)


ROUTE_DESTINATIONS = {
    "gcp": {
        "label": "Start the Guided Care Plan",
        "description": "Answer a few questions so we can map the right mix of care options and benefits for {person}.",
        "page": "pages/gcp.py",
    },
    "pfma": {
        "label": "Connect with a Concierge Advisor",
        "description": "Share details with our advisors so we can coordinate next steps quickly for {person}.",
        "page": "pages/pfma.py",
    },
    "medicaid_off_ramp": {
        "label": "Review Medicaid Support",
        "description": "We'll confirm Medicaid coverage and guide you through the financial relief options available now.",
        "page": "pages/pfma.py",
    },
    "pro": {
        "label": "Open Professional Workspace",
        "description": "Jump into the tools built for discharge planners and referral partners.",
        "page": "pages/professional_mode.py",
    },
}

CARDS = [
    {
        "key": "guided_plan",
        "icon": "🧭",
        "title": "Guided Care Plan",
        "subtitle": "Understand the situation",
        "body": "Map needs, risks, and recommendations tailored to {person}.",
        "primary_label": "Open guided plan",
        "primary_page": "pages/gcp.py",
        "tags": [],
    },
    {
        "key": "cost_planner",
        "icon": "💰",
        "title": "Cost Planner",
        "subtitle": "Project care costs",
        "body": "Explore cost scenarios, offsets, and payment options.",
        "primary_label": "Open cost planner",
        "primary_page": "pages/cost_planner.py",
        "tags": [],
    },
    {
        "key": "advisor",
        "icon": "🤝",
        "title": "Concierge Advisor",
        "subtitle": "Plan with an expert",
        "body": "Schedule time with our team to coordinate services and next steps.",
        "primary_label": "Connect with an advisor",
        "primary_page": "pages/pfma.py",
        "tags": [],
    },
    {
        "key": "partner_support",
        "icon": "💞",
        "title": "Partner planning",
        "subtitle": "Support both of you",
        "body": "Coordinate preferences, legal documentation, and shared decisions when a partner is involved.",
        "primary_label": "Review partner checklist",
        "primary_page": "pages/care_prefs.py",
        "tags": ["partner"],
    },
    {
        "key": "home_support",
        "icon": "🏠",
        "title": "Home updates",
        "subtitle": "Safer living at home",
        "body": "Plan accessibility upgrades, maintenance, and utility support for the home.",
        "primary_label": "Explore home support",
        "primary_page": "pages/cost_planner_home_care.py",
        "tags": ["home"],
    },
    {
        "key": "va_benefits",
        "icon": "🎖️",
        "title": "VA & military benefits",
        "subtitle": "Check eligibility",
        "body": "Unlock veteran-specific programs, stipends, and respite coverage if they served.",
        "primary_label": "Review VA benefits",
        "primary_page": "pages/benefits_coverage.py",
        "tags": ["veteran"],
    },
    {
        "key": "risk_navigator",
        "icon": "🛡️",
        "title": "Risk Navigator",
        "subtitle": "Spot areas of concern",
        "body": "Track safety watchpoints so you can advocate for {person}.",
        "primary_label": "Open risk navigator",
        "primary_page": "pages/risk_navigator.py",
        "tags": [],
    },
    {
        "key": "medication_check",
        "icon": "💊",
        "title": "Medication check",
        "subtitle": "Review meds & interactions",
        "body": "Upload medications and get key questions for the care team.",
        "primary_label": "Review medications",
        "primary_page": "pages/medication_management.py",
        "tags": [],
    },
]

# ---------------------------------------------------------------------------
# Page body
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
      .block-container {
        max-width: 1160px;
        margin: 0 auto;
        padding-top: 2.25rem;
        padding-bottom: 3rem;
      }
      .hub-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.4rem;
      }
      .hub-card {
        border-radius: 20px;
        border: 1px solid rgba(15, 23, 42, 0.08);
        background: #ffffff;
        padding: 1.4rem;
        box-shadow: 0 24px 44px -32px rgba(15, 23, 42, 0.35);
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
        min-height: 240px;
      }
      .hub-card h4 {
        margin: 0;
        font-size: 1.12rem;
      }
      .hub-card small {
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        color: rgba(15, 23, 42, 0.56);
      }
      .hub-card button {
        border-radius: 12px !important;
        padding: 0.65rem 1rem;
        font-weight: 600;
      }
      .hub-card .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: #ffffff;
        border: none;
      }
      .hub-card .stButton>button:hover {
        background: linear-gradient(135deg, #4338ca, #4f46e5);
      }
      .hub-banner {
        border-radius: 18px;
        padding: 1.3rem 1.6rem;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.12), rgba(59, 130, 246, 0.1));
        border: 1px solid rgba(79, 70, 229, 0.28);
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
      }
      .hub-banner strong {
        font-size: 1.05rem;
      }
      .hub-banner .stButton>button {
        border-radius: 999px;
        padding: 0.55rem 1.1rem;
        background: #ffffff;
        color: #1e1b4b;
        border: 1px solid rgba(79, 70, 229, 0.4);
      }
      .hidden-note {
        font-size: 0.85rem;
        color: rgba(30, 41, 59, 0.7);
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Concierge Care Hub")
st.caption(f"Tailored for {person_display} based on what you shared.")

# Recommended next step banner
recommended = ROUTE_DESTINATIONS.get(route_next)
if recommended:
    with st.container():
        st.markdown("<div class='hub-banner'>", unsafe_allow_html=True)
        st.markdown(
            f"<strong>Next best step:</strong> {recommended['description'].format(person=person_display)}",
            unsafe_allow_html=True,
        )
        if st.button(recommended["label"], key="hub_recommended"):
            switch_page_if(recommended["page"])
        st.markdown("</div>", unsafe_allow_html=True)

if flags.get("medicaid"):
    st.info(
        "Medicaid is active for this household. Cost Planner will highlight Medicaid-covered services and skip non-applicable offsets.",
        icon="🛡️",
    )

if flags.get("urgent") and URGENT_FEATURE_FLAG:
    st.warning(
        "You've marked this as urgent. Advisors will prioritize rapid coordination across the tools below.",
        icon="⏱️",
    )

st.markdown("<div class='hub-grid'>", unsafe_allow_html=True)
for card in CARDS:
    if not visible_item(card.get("tags", []), card["title"]):
        continue
    with st.container():
        st.markdown("<div class='hub-card'>", unsafe_allow_html=True)
        st.markdown(
            f"<small>{card['subtitle']}</small><h4>{card['icon']} {card['title']}</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(card["body"].format(person=person_display))
        if st.button(card["primary_label"], key=f"hub_{card['key']}"):
            switch_page_if(card["primary_page"])
        st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if hidden_items:
    with st.expander("Why some tools are hidden", expanded=False):
        for label, tag in hidden_items:
            st.markdown(
                f"**{label}** — {HIDDEN_TOOLTIPS.get(tag, 'Hidden based on the audiencing qualifiers.')}"
            )

with st.expander("Debug: Audiencing snapshot", expanded=False):
    st.json(snapshot)
