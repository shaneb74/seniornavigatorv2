"""Medical and daily aids drawer."""
from __future__ import annotations
from ui.theme import inject_theme

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, get_numeric, recompute_costs, set_numeric

inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

ensure_core_state()
cp = st.session_state["cost_planner"]
gcp = st.session_state.get("gcp", {})

st.title("Medical and daily living aids")
st.caption("Capture medication costs, supplies, and transport to appointments.")

chronic = gcp.get("chronic_conditions", [])
if chronic:
    st.info(
        "Chronic conditions noted in the Guided Care Plan: " + ", ".join(chronic),
        icon="🧬",
    )

rx = st.number_input(
    "Prescription medications",
    min_value=0.0,
    step=25.0,
    value=float(get_numeric("medical_prescriptions")),
    help="Monthly prescription spending across retail and mail order.",
)
set_numeric("medical_prescriptions", rx)

supplies = st.number_input(
    "Medical supplies & equipment",
    min_value=0.0,
    step=25.0,
    value=float(get_numeric("medical_supplies")),
    help="Incontinence products, DME rentals, batteries, and similar.",
)
set_numeric("medical_supplies", supplies)

transport = st.number_input(
    "Medical transportation",
    min_value=0.0,
    step=25.0,
    value=float(get_numeric("medical_transport")),
    help="Ambulance subscriptions, paratransit, or rides to medical appointments.",
)
set_numeric("medical_transport", transport)

recompute_costs()

st.metric("Medical subtotal", format_currency(cp["subtotals"]["medical"]))

st.markdown("---")

col_hub, col_back, col_next = st.columns([1, 1, 1])
with col_hub:
    if st.button("Return to Hub", type="secondary"):
        st.switch_page("pages/hub.py")
with col_back:
    if st.button("Back: Care"):
        st.switch_page("pages/cost_planner_home_care.py")
with col_next:
    if st.button("Next: Insurance", type="primary"):
        st.switch_page("pages/cost_planner_benefits.py")

st.markdown('</div>', unsafe_allow_html=True)
