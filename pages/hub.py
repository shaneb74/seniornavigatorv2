"""Concierge Care Hub that adapts to the audiencing snapshot."""

from __future__ import annotations

import streamlit as st

from audiencing import (
    URGENT_FEATURE_FLAG,
    apply_audiencing_sanitizer,
    ensure_audiencing_state,
    reset_audiencing_state,
    snapshot_audiencing,
)

# Page config must be set before any UI output
st.set_page_config(page_title="Concierge Care Hub", layout="wide")

# ---------- Audiencing snapshot ----------
state = ensure_audiencing_state()
apply_audiencing_sanitizer(state)
snapshot = snapshot_audiencing(state)
st.session_state["audiencing_snapshot"] = snapshot

# ---------- Session guard (fixed: closed parenthesis) ----------
care_context = st.session_state.setdefault(
    "care_context",
    {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,  # 'In-home care' | 'Assisted living' | 'Memory care' | None
        "gcp_cost": None,            # e.g., '$5,200/mo'
    },
)
ctx = st.session_state.care_context
person_name = ctx.get("person_name", "Your Loved One")

st.title("Dashboard")  # keep your H1; match your design copy if needed

# ---------- Hub-only CSS fixes ----------
# 1) Nuke any global "card decorators" that create empty rounded boxes above content.
#    These often target Streamlit block wrappers or inject ::before/::after backgrounds.
st.markdown(
    """
    <style>
      /* Scope to this page only by wrapping all below in .hub-scope */
      .hub-scope [data-testid="stVerticalBlock"],
      .hub-scope [data-testid="stHorizontalBlock"] {
        /* Remove any background/box/shadow/min-height global decorations */
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        outline: none !important;
        min-height: auto !important;
      }
      /* Kill pseudo-element decorations that some themes inject */
      .hub-scope *::before,
      .hub-scope *::after {
        box-shadow: none !important;
        background: none !important;
      }

      /* Our actual cards */
      .sn-card {
        background: #fff;
        border: 1px solid rgba(2,6,23,0.08);
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(2,6,23,0.06);
        padding: 22px;
        margin: 24px 0;
      }
      .sn-title { font-weight: 800; font-size: 18px; margin: 0 0 6px 0; }
      .sn-subtle { color: #475569; margin: 0 0 12px 0; }
      .sn-status {
        font-size: 12px;
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(2, 6, 23, 0.08);
        background: #F8FAFC;
        display: inline-block;
      }
      .sn-card .stButton>button {
        padding: 10px 14px;
        border-radius: 10px;
        font-weight: 600;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Page scope wrapper to confine the resets above ----------
st.markdown('<div class="hub-scope">', unsafe_allow_html=True)

def card(
    title: str,
    subtitle: str,
    cta_label: str,
    cta_key: str,
    on_click_page: str,
    status: str | None = None,
) -> None:
    st.markdown('<div class="sn-card">', unsafe_allow_html=True)
    # Use Streamlit columns for layout; they stay INSIDE our card because the card
    # is a real DOM node, not a pseudo-element.
    c1, c2, c3 = st.columns([6, 2, 2], vertical_alignment="center")
    with c1:
        st.markdown(f'<p class="sn-title">{title}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="sn-subtle">{subtitle}</p>', unsafe_allow_html=True)
    with c2:
        if st.button(cta_label, key=cta_key):
            st.switch_page(on_click_page)
    with c3:
        if status:
            st.markdown(f'<span class="sn-status">{status}</span>', unsafe_allow_html=True)
        else:
            st.markdown("&nbsp;", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Guided Care Plan ----------
gcp_completed = bool(ctx.get("gcp_recommendation")) or bool(ctx.get("gcp_answers"))
rec_text = ctx.get("gcp_recommendation") or "Understand the situation"
cost_text = ctx.get("gcp_cost") or "In progress"

card(
    title="Guided Care Plan",
    subtitle=(
        f"{rec_text} • {cost_text}"
        if gcp_completed
        else f"See what we learned from your answers and refine the recommendation for {person_name}."
    ),
    cta_label=("Open" if gcp_completed else "Start guided plan"),
    cta_key="hub_gcp_start",
    on_click_page="pages/gcp.py",
    status=("Completed ✅" if gcp_completed else "In progress"),
)

# ---------- Cost Planner ----------
card(
    title="Cost Estimator",
    subtitle=(
        f"Assess the total cost scenarios across options for {person_name}. "
        f"The estimate will update based on your guided plan."
    ),
    cta_label="Open estimator",
    cta_key="hub_open_cp",
    on_click_page="pages/cost_planner.py",
)

# ---------- Plan for My Advisor ----------
card(
    title="Plan for My Advisor",
    subtitle="Book time with a concierge advisor and share your plan.",
    cta_label="Get connected",
    cta_key="hub_pfma",
    on_click_page="pages/pfma.py",
)

# ---------- Medication Management ----------
card(
    title="Medication Management",
    subtitle="Keep meds on track with simple reminders and checks.",
    cta_label="Open",
    cta_key="hub_meds",
    on_click_page="pages/medication_management.py",
)

# ---------- Risk Navigator ----------
card(
    title="Risk Navigator",
    subtitle="Quick safety check to reduce avoidable risks at home.",
    cta_label="Run check",
    cta_key="hub_risk",
    on_click_page="pages/risk_navigator.py",
)

# ---------- Assessment (last) ----------
card(
    title="Assessment",
    subtitle="Additional screening tools and forms.",
    cta_label="Open assessment",
    cta_key="hub_assess",
    on_click_page="pages/care_plan_confirm.py",
)

st.markdown("</div>", unsafe_allow_html=True)  # end .hub-scope
