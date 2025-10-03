"""Concierge Care Hub with unified senior-friendly design."""

from __future__ import annotations

import streamlit as st

from audiencing import (
    URGENT_FEATURE_FLAG,
    apply_audiencing_sanitizer,
    ensure_audiencing_state,
    reset_audiencing_state,
    snapshot_audiencing,
)

st.set_page_config(page_title="Concierge Care Hub", layout="wide")

state = ensure_audiencing_state()
apply_audiencing_sanitizer(state)
snapshot = snapshot_audiencing(state)
st.session_state["audiencing_snapshot"] = snapshot

care_context = st.session_state.setdefault(
    "care_context",
    {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,
        "gcp_cost": None,
    },
)

person_name = care_context.get("person_name") or "Your Loved One"
if snapshot.get("entry") == "self":
    person_name = "You"

gcp_state = st.session_state.get("gcp", {})
gcp_recommendation = gcp_state.get("recommended_setting")
gcp_intensity = gcp_state.get("care_intensity")

SETTING_COPY = {
    "home": "In-home care",
    "assisted": "Assisted living",
    "memory": "Memory care",
    "skilled-reserved": "Skilled nursing (reserved)",
}
INTENSITY_COPY = {
    "low": "Low support",
    "med": "Moderate support",
    "high": "High support",
}

recommendation_subtitle = None
if gcp_recommendation:
    setting_label = SETTING_COPY.get(gcp_recommendation, gcp_recommendation.title())
    intensity_label = INTENSITY_COPY.get(gcp_intensity, gcp_intensity)
    recommendation_subtitle = (
        f"Recommendation: {setting_label}" + (f" • {intensity_label}" if intensity_label else "")
    )

flags = snapshot.get("flags", {})
visibility = snapshot.get("visibility", {})

if flags.get("medicaid"):
    st.markdown(
        "<div class='sn-banner'>🩺 <div>Medicaid is on file. We’ll highlight off-ramp options and Cost Planner shortcuts with this in mind.</div></div>",
        unsafe_allow_html=True,
    )

if URGENT_FEATURE_FLAG and flags.get("urgent"):
    st.markdown(
        "<div class='sn-banner sn-banner--success'>⚡ <div>Urgent case noted. Advisors will prioritize quicker responses.</div></div>",
        unsafe_allow_html=True,
    )

chip_text = "For yourself"
if snapshot.get("entry") == "proxy":
    chip_text = f"For someone {person_name}"
elif snapshot.get("entry") == "pro":
    chip_text = "Professional mode"

st.markdown(
    f"""
<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; margin-top:1.6rem;">
  <div>
    <h1 style="margin-bottom:0.2rem;">Concierge Care Hub</h1>
    <p style="color:#475569; max-width:620px;">Keep everything for {person} organized — recommendations, costs, and ways to get help.</p>
  </div>
  <div class="sn-chip">{chip}</div>
</div>
""".format(person=person_name, chip=chip_text),
    unsafe_allow_html=True,
)

tiles = [
    {
        "key": "tile_gcp",
        "badge": "Guided Care Plan",
        "title": "Understand the situation",
        "subtitle": recommendation_subtitle or "Capture needs, risks, and preferences in five steps.",
        "description": "See or update the Guided Care Plan for actionable recommendations.",
        "cta": "See responses" if recommendation_subtitle else "Start now",
        "page": "pages/gcp.py",
    },
    {
        "key": "tile_cost",
        "badge": "Cost Estimator",
        "title": "Understand the costs",
        "subtitle": None,
        "description": f"Estimate monthly costs and offsets tailored for {'you' if person_name == 'You' else person_name}.",
        "cta": "Open cost estimator",
        "page": "pages/cost_planner.py",
    },
    {
        "key": "tile_advisor",
        "badge": "Get Connected",
        "title": "Connect with an advisor",
        "subtitle": "Whenever you’re ready to meet with an advisor.",
        "description": "Share this snapshot so our team can coordinate services and paperwork.",
        "cta": "Get connected",
        "page": "pages/pfma.py",
    },
    {
        "key": "tile_ai",
        "badge": "AI Agent",
        "title": "AI assistance",
        "subtitle": "Receive instant, tailored assistance from our advanced AI chat.",
        "description": "Ask questions any time for quick answers and next steps.",
        "cta": "Open AI agent",
        "page": "pages/ai_advisor.py",
    },
]

for idx, tile in enumerate(tiles):
    if idx % 2 == 0:
        cols = st.columns(2, gap="large")
    col = cols[idx % 2]
    with col:
        st.markdown('<div class="sn-dashboard-card">', unsafe_allow_html=True)
        st.markdown(f"<span class='sn-chip'>{tile['badge']}</span>", unsafe_allow_html=True)
        st.markdown(f"<h3>{tile['title']}</h3>", unsafe_allow_html=True)
        if tile.get("subtitle"):
            st.markdown(
                f"<p class='sn-subtitle'>{tile['subtitle']}</p>",
                unsafe_allow_html=True,
            )
        st.markdown(
            f"<p class='sn-subtitle' style='margin-top:0.4rem;'>{tile['description']}</p>",
            unsafe_allow_html=True,
        )
        clicked = st.button(
            tile["cta"],
            key=tile["key"],
            type="primary",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        if clicked:
            st.switch_page(tile["page"])

hidden_messages = []
if not visibility.get("partner", True):
    hidden_messages.append("Partner planning tools are hidden for single-household scenarios.")
if not visibility.get("home", True):
    hidden_messages.append("Homeownership tasks are hidden because you told us the home isn’t owned.")
if not visibility.get("veteran", True):
    hidden_messages.append("VA benefits are hidden when the person isn’t a veteran.")

if hidden_messages:
    items = "".join(f"<li>{msg}</li>" for msg in hidden_messages)
    st.markdown(
        f"<div class='sn-choice-note'><strong>Why some items are hidden:</strong><ul style='margin:0.6rem 0 0 1.2rem;'>{items}</ul></div>",
        unsafe_allow_html=True,
    )

with st.container():
    st.markdown('<div class="sn-dashboard-note">Prefer a fresh start? Resetting clears responses and estimates so you can begin again.</div>', unsafe_allow_html=True)
    if st.button("Start from scratch", key="hub_reset"):
        reset_audiencing_state()
        st.session_state.pop("gcp_answers", None)
        st.session_state.pop("gcp", None)
        st.session_state.pop("cost_planner", None)
        st.session_state.pop("audiencing_snapshot", None)
        st.session_state.pop("care_context", None)
        st.rerun()
