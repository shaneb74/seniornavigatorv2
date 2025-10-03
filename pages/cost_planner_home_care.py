"""Care drawer for Cost Planner with unified styling."""

from __future__ import annotations

import streamlit as st

from cost_planner_shared import (
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

st.set_page_config(page_title="Cost Planner • Care", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.9rem;">Cost Planner</h2>
<h1 style="margin-bottom:0.4rem;">Care staffing</h1>
<p style="max-width:640px; color:#475569;">Estimate care staffing, second-person support, and supplemental services.</p>
""", unsafe_allow_html=True)

recommended = gcp.get("recommended_setting")
if recommended:
    st.markdown(
        "<div class='sn-banner sn-banner--success'>🧭 <div>Guided Care Plan suggested <strong>{}</strong> with {} care intensity.</div></div>".format(
            recommended.title(), gcp.get("care_intensity", "unknown")
        ),
        unsafe_allow_html=True,
    )

st.markdown('<div class="sn-card" style="margin-top:1.2rem;">', unsafe_allow_html=True)
st.markdown("<span class='sn-chip'>Drawer</span>", unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0.6rem;'>Care staffing and services</h3>", unsafe_allow_html=True)

base_rate = st.number_input(
    "Primary care or staffing cost",
    min_value=0.0,
    step=50.0,
    value=float(get_numeric("care_base_rate")),
    help="Monthly base rate for in-home staffing or community care.",
)
set_numeric("care_base_rate", base_rate)

col_left, col_right = st.columns(2, gap="large")
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
st.markdown(
    f"<p style='margin-top:1.4rem; font-weight:600;'>Care subtotal: {format_currency(cp['subtotals']['care'])}</p>",
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
    st.switch_page("pages/cost_planner_housing.py")
if next_clicked:
    st.switch_page("pages/cost_planner_daily_aids.py")
