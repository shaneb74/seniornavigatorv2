"""Guided Care Plan intro with unified styling."""

from __future__ import annotations

import streamlit as st

from guided_care_plan import ensure_gcp_session, render_stepper
from guided_care_plan.state import current_audiencing_snapshot

st.set_page_config(page_title="Guided Care Plan", layout="wide")

answers, gcp_result = ensure_gcp_session()
snapshot = current_audiencing_snapshot()
aud_state = st.session_state.get("audiencing", {})

entry = snapshot.get("entry") or aud_state.get("entry")
person_name = aud_state.get("recipient_name") or "Your Loved One"
if entry == "self":
    person_name = "You"

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.95rem;">Guided Care Plan</h2>
<h1 style="margin-bottom:0.4rem;">Understand the situation</h1>
<p style="max-width:660px; color:#475569; font-size:1.05rem;">
  Answer a few questions about daily life, health, and preferences. We’ll create a recommendation and DecisionTrace that carries through the hub.
</p>
""", unsafe_allow_html=True)

render_stepper(0)

st.markdown(
    """
<div class="sn-card" style="margin-top:1.4rem;">
  <p style="font-size:1rem; color:#475569; margin-bottom:0.6rem;">
    You’re planning for <strong>{person}</strong>. We’ll reuse your audiencing details and apply the Guided Care Plan logic to highlight safety considerations, recommend a setting, and connect cost planning.
  </p>
  <ul style="color:#475569; line-height:1.7; margin-left:1.2rem;">
    <li>Five sections with plain-language questions.</li>
    <li>Automatically applies your household, benefits, and Medicaid context.</li>
    <li>Produces a DecisionTrace for advisors and cost planning.</li>
  </ul>
</div>
""".format(person=person_name),
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
    footer_cols = st.columns([1, 1, 1])
    start_clicked = False
    with footer_cols[1]:
        start_clicked = st.button(
            "Start Section 1",
            type="primary",
            use_container_width=True,
            key="gcp_intro_start",
        )
    st.markdown('</div><div class="sn-footer-note">You can return to the hub at any time to pick up where you left off.</div></div>', unsafe_allow_html=True)

if start_clicked:
    st.switch_page("pages/gcp_daily_life.py")

with st.expander("Debug: Current answers", expanded=False):
    st.json({"answers": answers, "gcp": gcp_result, "audiencing": snapshot})
