"""Housing drawer for the Cost Planner."""
from __future__ import annotations
from ui.theme import inject_theme

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, get_numeric, recompute_costs, set_numeric

inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

ensure_core_state()
cp = st.session_state["cost_planner"]
aud = st.session_state["audiencing"]
quals = aud.get("qualifiers", {})

st.title("Housing and living costs")
st.caption("Capture recurring housing payments before care or benefits.")

if not quals.get("owns_home"):
    st.info(
        "Audiencing shows this household does not own a home. Home maintenance fields are hidden and treated as $0.",
        icon="🏢",
    )

base_rent = st.number_input(
    "Monthly housing cost (rent, mortgage, or community fee)",
    min_value=0.0,
    step=50.0,
    value=float(get_numeric("housing_base_rent")),
    help="Include rent, mortgage, or assisted living base fees.",
)
set_numeric("housing_base_rent", base_rent)

col_a, col_b = st.columns(2)
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

st.metric("Housing subtotal", format_currency(cp["subtotals"]["housing"]))

st.markdown("---")

col_hub, col_back, col_next = st.columns([1, 1, 1])
with col_hub:
    if st.button("Return to Hub", type="secondary"):
        st.switch_page("pages/hub.py")
with col_back:
    if st.button("Back to Intro"):
        st.switch_page("pages/cost_planner_estimate.py")
with col_next:
    if st.button("Next: Care", type="primary"):
        st.switch_page("pages/cost_planner_home_care.py")

st.markdown('</div>', unsafe_allow_html=True)
