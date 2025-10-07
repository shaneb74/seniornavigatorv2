from __future__ import annotations

import streamlit as st

from gcp_core import scoring as gcp_scoring
from gcp_core.engine import build_conversational_summary, snapshot as build_snapshot
from gcp_core.questions import BEHAVIOR_RISKS_OPTIONS
from gcp_core.state import (
    ensure_session,
    get_answers,
    get_medicaid_status,
    get_medicaid_ack,
    set_medicaid_ack,
    save_snapshot,
    set_section_complete,
)
from ui.state import mark_complete

BEHAVIOR_RISK_LABELS = {token: label for token, label in BEHAVIOR_RISKS_OPTIONS}


def _render_medicaid_notice_for_reco(status: str, acknowledged: bool) -> None:
    if status not in {"yes", "unsure"} or acknowledged:
        return

    is_yes = status == "yes"
    with st.container(border=True):
        st.subheader("Before you proceed")
        if is_yes:
            st.write(
                "Because you’re using **Medicaid**, advisor options can be limited. "
                "These results and planning tools are still yours to explore."
            )
        else:
            st.write(
                "If you’re unsure about Medicaid eligibility, review these results and note any follow-ups we flag."
            )

        col_link, col_ack = st.columns([1, 1])
        with col_link:
            st.link_button("Learn about Medicaid", "https://www.medicaid.gov/")
        with col_ack:
            if st.button("I understand", type="primary"):
                set_medicaid_ack(True)
                st.rerun()


ensure_session()

answers = get_answers()
status = get_medicaid_status()
acknowledged = get_medicaid_ack()
if status not in {"yes", "unsure"} and acknowledged:
    set_medicaid_ack(False)
    acknowledged = False

scoring = gcp_scoring.score_answers(answers)
summary_bullets = build_conversational_summary(answers, scoring)
snapshot_record = build_snapshot(answers, scoring)
save_snapshot(snapshot_record)
set_section_complete("context")
set_section_complete("done")
mark_complete("gcp")

_render_medicaid_notice_for_reco(status, acknowledged)

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Your care recommendation")

SETTING_LABELS = {
    "remain_at_home": "Stay at home with current supports",
    "home_with_support": "Home with added support",
    "assisted_living": "Assisted living",
    "memory_care": "Memory care",
    "skilled_nursing": "Skilled nursing",
}

setting_key = scoring["recommended_setting"]
setting_label = SETTING_LABELS.get(setting_key, "Personalized follow-up")
primary_reason = scoring["rationale"][0]

st.write(f"We recommend **{setting_label}** because {primary_reason}")

st.markdown("### What we heard")
for bullet in summary_bullets:
    st.markdown(f"- {bullet}")

behavior_insights = scoring.get("behavior_risks", {})
behavior_tier = behavior_insights.get("tier")
if behavior_tier and behavior_tier != "none":
    st.markdown("### Safety signals we noticed")
    tokens = behavior_insights.get("flags", [])
    labels = [BEHAVIOR_RISK_LABELS.get(token, token.replace("_", " ").title()) for token in tokens]
    if labels:
        st.markdown(f"- {', '.join(labels)}")
    guidance_map = {
        "high": "Consider supervised routines, secure exits, and a safety check of the home.",
        "moderate": "Consider a daily check-in plan and environment safety adjustments.",
        "low": "Monitor for changes; note times of day (e.g., evenings) when issues increase.",
    }
    guidance = guidance_map.get(behavior_tier)
    if guidance:
        st.write(guidance)

active_flags = [flag for flag, value in scoring["risk_flags"].items() if value]
if active_flags:
    st.markdown("### Safety highlights")
    st.markdown(
        "<style>.gcp-chip{display:inline-block;padding:.35rem .65rem;border-radius:9999px;background:rgba(11,92,216,.12);color:#094099;font-weight:600;margin:0 .35rem .35rem 0;}</style>",
        unsafe_allow_html=True,
    )
    chip_line = "".join(f"<span class='gcp-chip'>{flag.replace('_',' ').title()}</span>" for flag in active_flags)
    st.markdown(chip_line, unsafe_allow_html=True)

if status != "yes":
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Continue to Cost Planner", type="primary", width="stretch", key="reco_to_cost_planner"):
            st.switch_page("app_pages/cost_planner_v2/cost_planner_landing_v2.py")
    with col2:
        if st.button("Return to Care Hub", type="secondary", width="stretch", key="reco_back_to_hub"):
            st.switch_page("app_pages/hub.py")
else:
    st.caption("Return to the Hub or adjust your answers to explore other planning options.")

if st.button("◀ Back", type="secondary", width="stretch"):
    st.switch_page("app_pages/gcp_v2/gcp_context_prefs_v2.py")

if st.button("Save & exit to Hub", type="secondary", width="stretch"):
    st.switch_page("app_pages/hub.py")

st.caption("Snapshot saved • v1.0")
