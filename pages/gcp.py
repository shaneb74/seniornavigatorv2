"""Guided Care Plan intro with unified styling."""

from __future__ import annotations

import streamlit as st

from guided_care_plan import ensure_gcp_session, render_stepper
from guided_care_plan.state import current_audiencing_snapshot

st.set_page_config(page_title="Guided Care Plan", layout="centered")

answers, gcp_result = ensure_gcp_session()
snapshot = current_audiencing_snapshot()

person_name = "Your Loved One"
if snapshot.get("entry") == "self":
    person_name = "You"
else:
    people = snapshot.get("people", {})
    person_name = people.get("recipient_name") or "Your Loved One"

st.title(f"Guided Care Plan for {person_name}")
st.caption("Five quick sections to create a starting point and DecisionTrace.")

render_stepper(0)

st.write(
    """
Answer twelve short questions across daily life, safety, and context. We’ll use them with your audience
snapshot to surface a personalized care recommendation, highlight safety considerations, and point you back
to the Concierge Care Hub with the right next steps.
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

st.markdown("---")

start_col, hub_col = st.columns([2, 1])
with start_col:
    if st.button("Start Section 1", type="primary"):
        st.switch_page("pages/gcp_daily_life.py")
with hub_col:
    if st.button("Return to Hub"):
        st.switch_page("pages/hub.py")

with st.expander("Debug: Current answers", expanded=False):
    st.json({"answers": answers, "gcp": gcp_result, "audiencing": snapshot})
