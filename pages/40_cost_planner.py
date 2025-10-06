from __future__ import annotations

import streamlit as st

from senior_nav import navigation
from senior_nav.documents import register_json
from senior_nav.state import completions, ensure_base_state, require_entry_ready
from senior_nav.ui import header, render_ai_launcher, set_page_config


set_page_config(title="Cost Planner")
ensure_base_state()
require_entry_ready()
flags = completions()

header("Cost Planner", "Build a cost picture from your guided care plan.")

contract = st.session_state.get("gcp")
if not contract:
    st.warning("Complete the Guided Care Plan first so we know which costs to model.")
    if st.button("Go to Guided Care Plan", type="primary"):
        navigation.switch_page(navigation.GCP_PAGE)
    render_ai_launcher()
    st.stop()

recommended = contract.get("recommended_setting", "In-home support")
intensity = contract.get("care_intensity", "Moderate")
payment_context = contract.get("payment_context", "Private pay")
confidence = float(contract.get("funding_confidence", 0.5))

baseline_map = {
    "In-home support": 2800,
    "Assisted living": 4200,
    "Memory care": 5600,
}
default_baseline = baseline_map.get(recommended, 3200)
mode_index = 0 if confidence >= 0.6 else 1

with st.expander("Care plan snapshot", expanded=True):
    st.markdown(
        f"**Recommended setting:** {recommended}  \\n**Care intensity:** {intensity}  \\n**Payment context:** {payment_context}"
    )

with st.form("cost_planner_form"):
    planning_mode = st.radio(
        "How would you like to plan costs?",
        ("Guided plan", "Explore options"),
        index=mode_index,
    )
    monthly_cost = st.number_input(
        "Estimated monthly cost",
        min_value=0,
        value=int(st.session_state.get("cost_planner", {}).get("monthly_cost", default_baseline)),
        step=100,
        help="Start with a baseline that matches your recommended setting.",
    )
    monthly_income = st.number_input(
        "Income & benefits covering costs",
        min_value=0,
        value=int(st.session_state.get("cost_planner", {}).get("monthly_income", 1800)),
        step=100,
    )
    savings_to_use = st.number_input(
        "Monthly savings you're willing to apply",
        min_value=0,
        value=int(st.session_state.get("cost_planner", {}).get("savings_to_use", 600)),
        step=50,
    )
    submitted = st.form_submit_button("Save cost summary", type="primary")

if submitted:
    gap = max(monthly_cost - (monthly_income + savings_to_use), 0)
    summary = {
        "mode": planning_mode,
        "monthly_cost": monthly_cost,
        "monthly_income": monthly_income,
        "savings_to_use": savings_to_use,
        "uncovered_gap": gap,
        "based_on": contract,
    }
    st.session_state.cost_planner = summary
    flags.mark("cost_planner", True)
    register_json("cost_summary", kind="cost_summary", title="Cost Summary", payload=summary)
    st.success("Cost summary saved and added to My Documents.")
    navigation.switch_page(navigation.HUB_PAGE)

render_ai_launcher()
