"""Final confirmation and PFMA handoff for Cost Planner with unified styling."""

from __future__ import annotations

import json

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, recompute_costs

ensure_core_state()
cp = st.session_state["cost_planner"]
aud_snapshot = st.session_state.get("audiencing_snapshot") or st.session_state.get("audiencing")

recompute_costs()

st.set_page_config(page_title="Cost Planner • Confirm", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.9rem;">Cost Planner</h2>
<h1 style="margin-bottom:0.4rem;">Confirm & share</h1>
<p style="max-width:640px; color:#475569;">Lock in the current snapshot, export it, or share with an advisor.</p>
""", unsafe_allow_html=True)

monthly = format_currency(cp["monthly_total"])
offsets = format_currency(cp["subtotals"]["offsets"])
net = format_currency(cp["net_out_of_pocket"])

st.markdown('<div class="sn-card" style="margin-top:1.2rem; display:flex; flex-direction:column; gap:1.4rem;">', unsafe_allow_html=True)
metrics = st.columns(4)
metrics[0].metric("Monthly costs", monthly)
metrics[1].metric("Offsets", offsets)
metrics[2].metric("Net out-of-pocket", net)
if cp.get("runway_months") is not None:
    metrics[3].metric("Runway", f"{cp['runway_months']:.1f} months")
else:
    metrics[3].metric("Runway", "—")

st.markdown("<h3>Ready to share?</h3>", unsafe_allow_html=True)
confirm = st.checkbox("I reviewed these numbers and they reflect our plan.")

snapshot_json = json.dumps(cp["snapshot_for_crm"], indent=2).encode("utf-8")
st.download_button(
    "Download CRM snapshot",
    data=snapshot_json,
    file_name="cost_planner_snapshot.json",
    mime="application/json",
    disabled=not confirm,
)

col_share, col_tweak = st.columns(2, gap="large")
with col_share:
    if st.button("Share with Advisor / PFMA", type="primary", disabled=not confirm, use_container_width=True):
        st.session_state["last_event"] = {
            "type": "cost_planner_shared",
            "audiencing": aud_snapshot,
        }
        st.switch_page("pages/pfma_confirm_cost_plan.py")
with col_tweak:
    if st.button("Tweak estimate", use_container_width=True):
        st.switch_page("pages/cost_planner_estimate.py")

st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
    footer_cols = st.columns([1, 1, 1])
    hub_clicked = False
    back_clicked = False
    with footer_cols[0]:
        back_clicked = st.button("Back", type="secondary", use_container_width=True)
    with footer_cols[2]:
        hub_clicked = st.button("Return to Hub", type="primary", use_container_width=True)
    st.markdown('</div><div class="sn-footer-note">Next step ✺</div></div>', unsafe_allow_html=True)

if back_clicked:
    st.switch_page("pages/cost_planner_estimate_summary.py")
if hub_clicked:
    st.switch_page("pages/hub.py")
