"""Care drawer for Cost Planner."""
from __future__ import annotations
from ui.theme import inject_theme

import streamlit as st

from cost_planner_shared import (
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    ensure_core_state,
    format_currency,
    get_numeric,
    recompute_costs,
    set_numeric,
)

ensure_core_state()
cp = st.session_state["cost_planner"]
aud = st.session_state["audiencing"]
gcp = st.session_state.get("gcp", {})
quals = aud.get("qualifiers", {})

st.title("Care staffing and services")
st.caption("Estimate care staffing, second person support, and supplemental services.")

recommended = gcp.get("recommended_setting")
if recommended:
    st.info(
        f"Guided Care Plan suggested {recommended.title()} with {gcp.get('care_intensity', 'unknown')} care intensity.",
        icon="🩺",
    )

base_rate = st.number_input(
    "Primary care or staffing cost",
    min_value=0.0,
    step=50.0,
    value=float(get_numeric("care_base_rate")),
    help="Monthly base rate for in-home staffing or community care.",
)
set_numeric("care_base_rate", base_rate)

col_left, col_right = st.columns(2)
with col_left:
    addon = st.number_input(
        "Level-of-care add-ons",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("care_level_addon")),
        help="Medication management, behavior support, or acuity fees.",
    )
    set_numeric("care_level_addon", addon)

with col_right:
    supplemental = st.number_input(
        "Supplemental support services",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("care_support_services")),
        help="Adult day, respite, transportation, or wellness memberships.",
    )
    set_numeric("care_support_services", supplemental)

if cp.get("household") == "split" and quals.get("has_partner"):
    second_person = st.number_input(
        "Second person care add-on",
        min_value=0.0,
        step=25.0,
        value=float(get_numeric("care_second_person")),
        help="Care costs for a partner or second person in the household.",
    )
    set_numeric("care_second_person", second_person)
else:
    set_numeric("care_second_person", 0.0)

recompute_costs()

st.metric("Care subtotal", format_currency(cp["subtotals"]["care"]))

st.markdown("---")

col_hub, col_back, col_next = st.columns([1, 1, 1])
with col_hub:
    if st.button("Return to Hub", type="secondary"):
        st.switch_page("pages/hub.py")
with col_back:
    if st.button("Back: Housing"):
        st.switch_page("pages/cost_planner_housing.py")
with col_next:
    if st.button("Next: Medical", type="primary"):
        st.switch_page("pages/cost_planner_daily_aids.py")

st.markdown('</div>', unsafe_allow_html=True)
