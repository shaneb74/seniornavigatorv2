"""Cost Planner entry: establish mode, household, and audience context."""
from __future__ import annotations
from ui.theme import inject_theme

import streamlit as st

from cost_planner_shared import (
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    audiencing_badges,
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
qualifiers = aud.get("qualifiers", {})

st.title("Cost Planner")
st.caption("TurboTax-style walkthrough to understand monthly costs, offsets, and runway.")

entry, badges = audiencing_badges()
alert_lines = [
    f"Planning for **{entry}** audience.",
]
if badges:
    alert_lines.append(" * ".join(badges))
st.info(" \n".join(alert_lines))

if qualifiers.get("on_medicaid"):
    st.warning(
        "Medicaid coverage detected. We'll default costs to the Medicaid payment context and log a short-circuit entry.",
        icon="💡",
    )

recommended = gcp.get("recommended_setting")
if recommended:
    st.success(
        f"Guided Care Plan recommends **{recommended.title()}** with {gcp.get('care_intensity', 'unknown')} care intensity.",
        icon="🧭",
    )

col_mode, col_household = st.columns([2, 2])
with col_mode:
    mode_label = {
        "tinkering": "I'm exploring rough numbers",
        "planning": "I need a real plan with runway",
    }
    mode_choice = st.radio(
        "Planner mode",
        options=["tinkering", "planning"],
        format_func=lambda val: mode_label[val],
        index=["tinkering", "planning"].index(cp.get("mode", "tinkering")),
        horizontal=False,
    )
    if mode_choice != cp.get("mode"):
        cp["mode"] = mode_choice

with col_household:
    household_label = {
        "single": "Single household",
        "split": "Split household",
    }
    disable_partner = not qualifiers.get("has_partner")
    household_choice = st.radio(
        "Household",
        options=["single", "split"],
        format_func=lambda val: household_label[val],
        index=["single", "split"].index(cp.get("household", "single")),
        horizontal=False,
        disabled=disable_partner,
        help="Partners must be enabled in Audiencing to plan for a split household." if disable_partner else None,
    )
    cp["household"] = household_choice if not disable_partner else "single"

st.markdown("---")

if cp["mode"] == "planning":
    assets_default = get_numeric("assets_total")
    assets_value = st.number_input(
        "Liquid assets available for care",
        min_value=0.0,
        step=500.0,
        value=float(assets_default),
        help="Enter savings that could be used to cover care. We'll calculate runway based on net out-of-pocket.",
    )
    set_numeric("assets_total", assets_value)
else:
    set_numeric("assets_total", 0.0)

recompute_costs()

subtotals = cp["subtotals"]
summary_cols = st.columns(3)
summary_cols[0].metric("Monthly costs", format_currency(cp["monthly_total"]))
summary_cols[1].metric("Offsets", format_currency(subtotals["offsets"]))
summary_cols[2].metric("Net out-of-pocket", format_currency(cp["net_out_of_pocket"]))

st.markdown("---")

with st.expander("Debug: Cost Planner session state", expanded=False):
    st.json(
        {
            "mode": cp["mode"],
            "household": cp["household"],
            "audiencing": aud,
            "gcp": gcp,
            "inputs": cp["inputs"],
        }
    )

st.markdown("---")

col_left, col_right = st.columns(2)
with col_left:
    if st.button("Return to Hub", type="secondary"):
        st.switch_page("pages/hub.py")
with col_right:
    if st.button("Start Housing", type="primary"):
        st.switch_page("pages/cost_planner_housing.py")

st.markdown('</div>', unsafe_allow_html=True)
