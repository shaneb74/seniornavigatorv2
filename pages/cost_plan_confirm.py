"""Final confirmation and PFMA handoff for Cost Planner."""
from __future__ import annotations
from ui.theme import inject_theme

import json

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, recompute_costs

inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

ensure_core_state()
cp = st.session_state["cost_planner"]
aud_snapshot = st.session_state.get("audiencing_snapshot") or st.session_state.get("audiencing")

recompute_costs()

st.title("Confirm cost plan & handoff")
st.caption("Lock in the current snapshot, export it, or share with an advisor.")

monthly = format_currency(cp["monthly_total"])
offsets = format_currency(cp["subtotals"]["offsets"])
net = format_currency(cp["net_out_of_pocket"])

st.metric("Monthly costs", monthly)
st.metric("Offsets", offsets)
st.metric("Net out-of-pocket", net)

if cp.get("runway_months") is not None:
    st.metric("Runway", f"{cp['runway_months']:.1f} months")

st.subheader("Ready to share?")
confirm = st.checkbox("I reviewed these numbers and they reflect our plan.")

snapshot_json = json.dumps(cp["snapshot_for_crm"], indent=2).encode("utf-8")
st.download_button(
    "Download CRM snapshot",
    data=snapshot_json,
    file_name="cost_planner_snapshot.json",
    mime="application/json",
    disabled=not confirm,
)

col_share, col_tweak = st.columns(2)
with col_share:
    if st.button("Share with Advisor / PFMA", type="primary", disabled=not confirm):
        st.session_state["last_event"] = {
            "type": "cost_planner_shared",
            "audiencing": aud_snapshot,
        }
        st.switch_page("pages/pfma_confirm_cost_plan.py")
with col_tweak:
    if st.button("Tweak estimate"):
        st.switch_page("pages/cost_planner_estimate.py")

st.markdown("---")

col_hub, col_back = st.columns(2)
with col_hub:
    if st.button("Return to Hub", type="secondary"):
        st.switch_page("pages/hub.py")
with col_back:
    if st.button("Back to Summary"):
        st.switch_page("pages/cost_planner_estimate_summary.py")

st.markdown('</div>', unsafe_allow_html=True)
