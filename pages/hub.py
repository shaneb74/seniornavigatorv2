"""Concierge Care Hub with shared design system components."""
from __future__ import annotations

import streamlit as st

from ui import components as ui
from ui.theme import inject as inject_theme

st.set_page_config(page_title="Your Concierge Care Hub", layout="wide")
inject_theme()

# ---------------------------------------------------------------------------
# Session scaffolding
# ---------------------------------------------------------------------------
care_context = st.session_state.setdefault(
    "care_context",
    {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,
        "gcp_cost": None,
    },
)

aud_snapshot = st.session_state.get("audiencing_snapshot", {})
aud_entry = aud_snapshot.get("entry", "proxy")

if aud_entry == "self":
    person_chip = "For yourself"
    person_name = "You"
else:
    person_name = care_context.get("person_name") or "Your Loved One"
    if aud_entry == "proxy":
        person_chip = f"For someone {person_name}"
    elif aud_entry == "pro":
        person_chip = "Professional view"
    else:
        person_chip = "Assessment"

# Guided Care Plan state
st.session_state.setdefault("gcp_answers", {})
gcp_state = st.session_state.setdefault(
    "gcp",
    {
        "recommended_setting": None,
        "care_intensity": None,
        "safety_flags": [],
        "chronic_conditions": [],
        "payment_context": None,
        "funding_confidence": None,
        "audiencing_snapshot": None,
        "DecisionTrace": None,
    },
)

SETTING_LABELS = {
    "home": "In-home support",
    "assisted": "Assisted living",
    "memory": "Memory care",
    "skilled-reserved": "Skilled nursing",
}

recommendation_code = gcp_state.get("recommended_setting") or care_context.get("gcp_recommendation")
recommendation_label = SETTING_LABELS.get(recommendation_code, recommendation_code or "Recommendation pending")
intensity = gcp_state.get("care_intensity")
gcp_completed = bool(gcp_state.get("DecisionTrace") or recommendation_code)

# ---------------------------------------------------------------------------
# Page chrome
# ---------------------------------------------------------------------------
ui.notice(
    "Log in for a better experience — continue where you left off, with your information kept secure and confidential following HIPAA guidelines."
)

chips = " ".join(
    [
        '<span class="sn-badge">Assessment</span>',
        f'<span class="sn-badge">{person_chip}</span>',
        f'<span class="sn-badge">{person_name}</span>',
    ]
)

st.markdown(
    f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
      <div style="font-weight:800;letter-spacing:.08em;font-size:2rem;color:var(--ink);">DASHBOARD</div>
      <div style="display:flex;gap:.4rem;flex-wrap:wrap;justify-content:flex-end;">{chips}<span class=\"sn-badge\">Add +</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Card grid helpers
# ---------------------------------------------------------------------------

def reset_gcp() -> None:
    st.session_state["gcp_answers"] = {}
    gcp_state.update(
        {
            "recommended_setting": None,
            "care_intensity": None,
            "safety_flags": [],
            "chronic_conditions": [],
            "payment_context": None,
            "funding_confidence": None,
            "audiencing_snapshot": None,
            "DecisionTrace": None,
        }
    )
    care_context["gcp_recommendation"] = None
    care_context["gcp_cost"] = None
    st.rerun()


def render_status(label: str, completed: bool) -> None:
    chip_class = "sn-chip active" if completed else "sn-chip"
    st.markdown(f'<span class="{chip_class}">{label}</span>', unsafe_allow_html=True)


# Guided Care Plan card body
if gcp_completed:
    rec_pieces = ["<span style=\"opacity:.85;\">Recommendation</span>"]
    if recommendation_label:
        rec_pieces.append(f"<strong>{recommendation_label}</strong>")
    if intensity:
        rec_pieces.append(f"<span style=\"opacity:.75;\">· {intensity.title()} intensity</span>")
    gcp_body = f"<p>{' '.join(rec_pieces)}</p>"
else:
    gcp_body = (
        "<p>Answer 12 quick questions to understand the right level of care, risks, and priorities for next steps.</p>"
    )


def gcp_footer() -> None:
    col_open, col_reset, col_status = st.columns([1.3, 1.1, 1])
    with col_open:
        if ui.button("Open Guided Plan" if gcp_completed else "Start Guided Plan", primary=True, key="hub_gcp_open"):
            st.switch_page("pages/gcp.py")
    with col_reset:
        if ui.button("Start over", key="hub_gcp_reset"):
            reset_gcp()
    with col_status:
        render_status("Completed" if gcp_completed else "Not started", gcp_completed)


# Cost planner card body & footer
cost_subtitle = (
    f"Assess the cost structure for various care options for {person_name}. "
    "The estimate will automatically update based on your selected choices."
)


def cost_footer() -> None:
    col_start, col_helper = st.columns([1.1, 1])
    with col_start:
        if ui.button("Start", primary=True, key="hub_cost_start"):
            st.switch_page("pages/cost_planner_estimate.py")
    with col_helper:
        st.markdown('<span class="sn-field-note">Next step ✺</span>', unsafe_allow_html=True)


def advisor_footer() -> None:
    if ui.button("Get connected", primary=True, key="hub_advisor"):
        st.switch_page("pages/pfma.py")


def ai_footer() -> None:
    if ui.button("Open", key="hub_ai"):
        st.switch_page("pages/ai_advisor.py")

def render_gcp_card() -> None:
    ui.card(
        "Understand the situation",
        body=gcp_body,
        badge_text="🧭 Guided Care Plan",
        footer=gcp_footer,
    )


def render_cost_card() -> None:
    ui.card(
        "Understand the costs",
        body=f"<p>{cost_subtitle}</p>",
        badge_text="🧮 Cost Estimator",
        footer=cost_footer,
    )


def render_advisor_card() -> None:
    ui.card(
        "Connect with an advisor to plan the care",
        body="<p>Whenever you’re ready to meet with an advisor.</p>",
        badge_text="🎧 Get Connected",
        footer=advisor_footer,
    )


def render_ai_card() -> None:
    ui.card(
        "FAQs &amp; Answers",
        body="<p>Receive instant, tailored assistance from our advanced AI chat.</p>",
        badge_text="✨ AI Agent",
        footer=ai_footer,
        gradient=True,
    )


card_renderers = [render_gcp_card, render_cost_card, render_advisor_card, render_ai_card]
for idx in range(0, len(card_renderers), 2):
    row = card_renderers[idx : idx + 2]
    cols = st.columns(len(row), gap="large")
    for col, render in zip(cols, row):
        with col:
            render()

st.markdown(
    """
    <div class="sn-dashboard-note">
      <span class="sn-badge">↻ Start from scratch</span>
      <span style="color:var(--ink-muted);font-size:.92rem;">Choose this option if you would like to remove saved progress for your current plan and start fresh.</span>
    </div>
    <div class="sn-hr"></div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div style="font-weight:800;color:var(--ink);margin:2px 0 8px;">Additional services</div>', unsafe_allow_html=True)

st.markdown('<div class="sn-compact-row">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="sn-compact-tile">
      <div>
        <div class="title">AI Health Check</div>
        <div class="subtitle">Get insights about overall health status</div>
      </div>
      <a class="sn-btn" href="?view=health_open">Open</a>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="sn-compact-tile">
      <div>
        <div class="title">Learning Center</div>
        <div class="subtitle">Media Center</div>
      </div>
      <a class="sn-btn" href="?view=media_open">Open</a>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Query param fallbacks for deep links
# ---------------------------------------------------------------------------
view = st.query_params.get("view")
if view:
    try:
        if view == "start_costs":
            st.switch_page("pages/cost_planner_estimate.py")
        elif view == "get_connected":
            st.switch_page("pages/pfma.py")
        elif view == "ai_open":
            st.switch_page("pages/ai_advisor.py")
        elif view == "see_responses":
            st.switch_page("pages/gcp.py")
        elif view == "start_over":
            reset_gcp()
        elif view == "health_open":
            st.switch_page("pages/ai_advisor.py")
        elif view == "media_open":
            st.switch_page("pages/trusted_partners.py")
    except Exception:
        pass
