"""Expert review drawer with unified styling."""

from __future__ import annotations

import streamlit as st

from cost_planner_shared import (
    ensure_core_state,
    expert_flag,
    format_currency,
    get_numeric,
    recompute_costs,
)

ensure_core_state()
cp = st.session_state["cost_planner"]
gcp = st.session_state.get("gcp", {})

title = "Expert review"

st.set_page_config(page_title="Cost Planner • Expert Review", layout="wide")

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

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.9rem;">Cost Planner</h2>
<h1 style="margin-bottom:0.4rem;">Expert review & decision trace</h1>
<p style="max-width:640px; color:#475569;">Resolve any flagged inconsistencies before generating exports.</p>
""", unsafe_allow_html=True)

st.markdown('<div class="sn-card" style="margin-top:1.2rem;">', unsafe_allow_html=True)
st.markdown("<span class='sn-chip'>Drawer</span>", unsafe_allow_html=True)

if cp["expert_flags"]:
    for flag in cp["expert_flags"]:
        st.markdown(f"<div class='sn-banner'>⚠️ <div>{flag}</div></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='sn-banner sn-banner--success'>✅ <div>No expert review flags at this time.</div></div>", unsafe_allow_html=True)

st.markdown("<h3 style='margin-top:1.4rem;'>Decision log</h3>", unsafe_allow_html=True)
if cp["decision_log"]:
    for entry in cp["decision_log"]:
        st.write(f"• {entry}")
else:
    st.caption("No decisions logged yet.")

st.markdown("<h3 style='margin-top:1.4rem;'>Snapshot checks</h3>", unsafe_allow_html=True)
metric_cols = st.columns(3)
metric_cols[0].metric("Monthly costs", format_currency(cp["monthly_total"]))
metric_cols[1].metric("Net out-of-pocket", format_currency(cp["net_out_of_pocket"]))
if cp.get("runway_months") is not None:
    metric_cols[2].metric("Runway (months)", f"{cp['runway_months']:.1f}")

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
    st.switch_page("pages/cost_planner_freeform.py")
if next_clicked:
    st.switch_page("pages/cost_planner_estimate_summary.py")
