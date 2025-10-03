inject_theme()
st.markdown('<div class="sn-scope gcp">', unsafe_allow_html=True)

# pages/gcp.py
"""Guided Care Plan intro with unified styling."""

from __future__ import annotations
import streamlit as st

from guided_care_plan import ensure_gcp_session, render_stepper
from guided_care_plan.state import current_audiencing_snapshot

from ui.theme import inject_theme

st.set_page_config(page_title="Guided Care Plan", layout="centered")

# -------- helpers --------
def safe_switch_page(target: str) -> None:
    """Try to navigate; if not available, fail softly."""
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        # As a fallback, set a query param and rerun to keep UX responsive.
        st.query_params["next"] = target
        st.experimental_rerun()

# -------- state --------
answers, gcp_result = ensure_gcp_session()
snapshot = current_audiencing_snapshot()

person_name = "Your Loved One"
if snapshot.get("entry") == "self":
    person_name = "You"
else:
    people = snapshot.get("people", {}) or {}
    person_name = people.get("recipient_name") or "Your Loved One"

# -------- header --------
st.title(f"Guided Care Plan for {person_name}")
st.caption("Five quick sections to create a starting point and DecisionTrace.")
render_stepper(0)

# -------- intro copy (HTML allowed) --------
st.markdown(
    f"""
Answer twelve short questions across daily life, safety, and context. We'll use them with your audience
snapshot to surface a personalized care recommendation, highlight safety considerations, and point you back
to the Concierge Care Hub with the right next steps.
<div class="sn-card" style="margin-top:1.4rem;">
  <p style="font-size:1rem; color:#475569; margin-bottom:0.6rem;">
    You're planning for <strong>{person_name}</strong>. We'll reuse your audiencing details and apply the Guided Care Plan logic to highlight safety considerations, recommend a setting, and connect cost planning.
  </p>
  <ul style="color:#475569; line-height:1.7; margin-left:1.2rem;">
    <li>Five sections with plain-language questions.</li>
    <li>Automatically applies your household, benefits, and Medicaid context.</li>
    <li>Produces a DecisionTrace for advisors and cost planning.</li>
  </ul>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# -------- actions --------
start_col, hub_col = st.columns([2, 1])
with start_col:
    if st.button("Start Section 1", type="primary"):
        safe_switch_page("pages/gcp_daily_life.py")
with hub_col:
    if st.button("Return to Hub"):
        safe_switch_page("pages/hub.py")

# -------- debug --------
with st.expander("Debug: Current answers", expanded=False):
    st.json(
        {
            "answers": answers,
            "gcp": gcp_result,
            "audiencing": snapshot,
        }
    )