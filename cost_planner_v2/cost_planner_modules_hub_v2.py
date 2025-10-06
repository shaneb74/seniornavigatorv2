from __future__ import annotations
import streamlit as st
from ui.pfma import apply_pfma_theme
from cost_planner_v2.cp_state import ensure_cp
from cost_planner_v2.cp_nav import goto

apply_pfma_theme()
ensure_cp()

st.markdown("<div class='pfma-card'>", unsafe_allow_html=True)
st.markdown("### Your Plan Modules (v2)")
st.caption("Work through modules in any order. Then view Your Money Timeline.")

modules = [
    ("Income", "pages/cost_planner_v2/cost_planner_income_v2.py"),
    ("Other Monthly Costs", "pages/cost_planner_v2/cost_planner_expenses_v2.py"),
    ("Caregiver Support", "pages/cost_planner_v2/cost_planner_caregiver_v2.py"),
    ("Benefits", "pages/cost_planner_v2/cost_planner_benefits_v2.py"),
    ("Home Decisions", "pages/cost_planner_v2/cost_planner_home_v2.py"),
    ("Liquidity Nudge", "pages/cost_planner_v2/cost_planner_liquidity_v2.py"),
    ("Home Modifications", "pages/cost_planner_v2/cost_planner_home_mods_v2.py"),
    ("Assets", "pages/cost_planner_v2/cost_planner_assets_v2.py"),
]

for label, page in modules:
    cols = st.columns([3,1])
    with cols[0]: st.write(f"**{label}**")
    with cols[1]:
        if st.button("Open", key=f"open_{label}"):
            goto(page)
    st.divider()

if st.button("View Money Timeline", type="primary"):
    goto("pages/cost_planner_v2/cost_planner_timeline_v2.py")

st.markdown("</div>", unsafe_allow_html=True)
