"""Medical and daily aids drawer with unified styling."""

from __future__ import annotations

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, get_numeric, recompute_costs, set_numeric

ensure_core_state()
cp = st.session_state["cost_planner"]
gcp = st.session_state.get("gcp", {})

st.set_page_config(page_title="Cost Planner • Medical", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.9rem;">Cost Planner</h2>
<h1 style="margin-bottom:0.4rem;">Medical & daily aids</h1>
<p style="max-width:640px; color:#475569;">Capture medication costs, supplies, and transportation to appointments.</p>
""", unsafe_allow_html=True)

chronic = gcp.get("chronic_conditions", [])
if chronic:
    st.markdown(
        "<div class='sn-banner'>🧬 <div>Chronic conditions noted in the Guided Care Plan: {}.</div></div>".format(
            ", ".join(chronic)
        ),
        unsafe_allow_html=True,
    )

st.markdown('<div class="sn-card" style="margin-top:1.2rem;">', unsafe_allow_html=True)
st.markdown("<span class='sn-chip'>Drawer</span>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0.6rem;'>Medical and daily living aids</h3>", unsafe_allow_html=True)

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
st.markdown(
    f"<p style='margin-top:1.4rem; font-weight:600;'>Medical subtotal: {format_currency(cp['subtotals']['medical'])}</p>",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
    footer_cols = st.columns([1, 1, 1])
    back_clicked = False
    next_clicked = False
    with footer_cols[0]:
        back_clicked = st.button("Back", type="secondary", use_container_width=True)
    with footer_cols[2]:
        next_clicked = st.button("Next step", type="primary", use_container_width=True)
    st.markdown('</div><div class="sn-footer-note">Next step ✺</div></div>', unsafe_allow_html=True)

if back_clicked:
    st.switch_page("pages/cost_planner_home_care.py")
if next_clicked:
    st.switch_page("pages/cost_planner_benefits.py")
