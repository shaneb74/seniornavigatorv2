"""Housing drawer for the Cost Planner with unified styling."""

from __future__ import annotations

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, get_numeric, recompute_costs, set_numeric

ensure_core_state()
cp = st.session_state["cost_planner"]
aud = st.session_state["audiencing"]
quals = aud.get("qualifiers", {})

st.set_page_config(page_title="Cost Planner • Housing", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.9rem;">Cost Planner</h2>
<h1 style="margin-bottom:0.4rem;">Housing</h1>
<p style="max-width:640px; color:#475569;">Capture recurring housing payments before care or benefits.</p>
""", unsafe_allow_html=True)

if not quals.get("owns_home"):
    st.markdown(
        "<div class='sn-banner'>🏢 <div>This household doesn’t own a home. Maintenance fields are hidden and treated as $0.</div></div>",
        unsafe_allow_html=True,
    )

st.markdown('<div class="sn-card" style="margin-top:1.2rem;">', unsafe_allow_html=True)
st.markdown("<span class='sn-chip'>Drawer</span>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0.6rem;'>Housing and living costs</h3>", unsafe_allow_html=True)

base_rent = st.number_input(
    "Monthly housing cost (rent, mortgage, or community fee)",
    min_value=0.0,
    step=50.0,
    value=float(get_numeric("housing_base_rent")),
    help="Include rent, mortgage, or assisted living base fees.",
)
set_numeric("housing_base_rent", base_rent)

col_a, col_b = st.columns(2, gap="large")
with col_a:
    utilities = st.number_input(
        "Utilities & services",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("housing_utilities")),
        help="Electric, water, trash, cable, HOA dues.",
    )
    set_numeric("housing_utilities", utilities)

with col_b:
    if quals.get("owns_home"):
        maintenance = st.number_input(
            "Maintenance or HOA",
            min_value=0.0,
            step=25.0,
            value=float(get_numeric("housing_maintenance")),
            help="Repairs, lawn care, or HOA assessments.",
        )
        set_numeric("housing_maintenance", maintenance)
    else:
        set_numeric("housing_maintenance", 0.0)

recompute_costs()
st.markdown(
    f"<p style='margin-top:1.4rem; font-weight:600;'>Housing subtotal: {format_currency(cp['subtotals']['housing'])}</p>",
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
    st.switch_page("pages/cost_planner_estimate.py")
if next_clicked:
    st.switch_page("pages/cost_planner_home_care.py")
