"""Expert review drawer for Cost Planner."""
from __future__ import annotations
from ui.theme import inject_theme

import streamlit as st

from cost_planner_shared import (
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    ensure_core_state,
    expert_flag,
    format_currency,
    get_numeric,
    recompute_costs,
)

ensure_core_state()
cp = st.session_state["cost_planner"]
gcp = st.session_state.get("gcp", {})
aud = st.session_state.get("audiencing", {})

recompute_costs()
cp["expert_flags"] = []

chronic = gcp.get("chronic_conditions", [])
if chronic and get_numeric("medical_prescriptions") == 0:
    expert_flag("Medications listed but Rx cost is 0")

recommended = gcp.get("recommended_setting")
if recommended in {"assisted", "memory"} and get_numeric("housing_base_rent") == 0:
    expert_flag("Community setting selected without housing base rent")

if gcp.get("care_intensity") == "high" and get_numeric("care_base_rate") == 0:
    expert_flag("High care needs but care staffing cost missing")

if cp["mode"] == "planning" and cp.get("runway_months") is None:
    expert_flag("Planning mode without positive runway")

st.title("Expert review & decision trace")
st.caption("Resolve any flagged inconsistencies before generating exports.")

if cp["expert_flags"]:
    for flag in cp["expert_flags"]:
        st.warning(flag, icon="⚠️")
else:
    st.success("No expert review flags at this time.", icon="✅")

st.subheader("Decision log")
if cp["decision_log"]:
    for entry in cp["decision_log"]:
        st.write(f"* {entry}")
else:
    st.caption("No decisions logged yet.")

st.subheader("Snapshot checks")
st.metric("Monthly costs", format_currency(cp["monthly_total"]))
st.metric("Net out-of-pocket", format_currency(cp["net_out_of_pocket"]))
if cp.get("runway_months") is not None:
    st.metric("Runway (months)", f"{cp['runway_months']:.1f}")

st.markdown("---")

col_hub, col_back, col_next = st.columns([1, 1, 1])
with col_hub:
    if st.button("Return to Hub", type="secondary"):
        st.switch_page("pages/hub.py")
with col_back:
    if st.button("Back: Debts & Other"):
        st.switch_page("pages/cost_planner_freeform.py")
with col_next:
    if st.button("Next: Summary", type="primary"):
        st.switch_page("pages/cost_planner_estimate_summary.py")

st.markdown('</div>', unsafe_allow_html=True)
