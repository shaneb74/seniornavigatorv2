"""Guided Care Plan – Context & Preferences section."""

from __future__ import annotations

import streamlit as st

from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper
from guided_care_plan.state import current_audiencing_snapshot

BASE_QUESTIONS = ["living_situation"]
CONDITIONAL_QUESTIONS = {
    "partner_support": {"qualifier": "has_partner", "default": "no_partner"},
    "home_safety": {"qualifier": "owns_home", "default": "not_homeowner"},
    "veteran_benefits": {"qualifier": "is_veteran", "default": "not_applicable"},
}

answers, _ = ensure_gcp_session()
snapshot = current_audiencing_snapshot()
qualifiers = snapshot.get("qualifiers", {})

st.set_page_config(page_title="GCP – Context & Preferences", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.95rem;">Guided Care Plan</h2>
<h1 style="margin-bottom:0.4rem;">Context & preferences</h1>
<p style="max-width:660px; color:#475569;">We tailor recommendations based on living setup, partner involvement, and benefits.</p>
""", unsafe_allow_html=True)

render_stepper(3)

visible_questions = list(BASE_QUESTIONS)
for question_id, cfg in CONDITIONAL_QUESTIONS.items():
    if qualifiers.get(cfg["qualifier"]):
        visible_questions.append(question_id)
    else:
        answers[question_id] = cfg["default"]
        st.session_state[f"gcp_{question_id}"] = cfg["default"]

for question_id in visible_questions:
    meta = get_question_meta(question_id)
    option_map = {opt["value"]: opt["label"] for opt in meta["options"]}
    values = list(option_map.keys())
    default_value = answers.get(question_id, values[0])
    if default_value not in values:
        default_value = values[0]
    st.markdown(f"<h3 style='margin-top:1.6rem;'>{meta['label']}</h3>", unsafe_allow_html=True)
    st.markdown('<div class="sn-choice-group">', unsafe_allow_html=True)
    selected = st.radio(
        meta["label"],
        options=values,
        index=values.index(default_value),
        key=f"gcp_{question_id}",
        label_visibility="collapsed",
        format_func=lambda value, m=option_map: m[value],
    )
    st.markdown("</div>", unsafe_allow_html=True)
    if meta.get("description"):
        st.caption(meta["description"])
    answers[question_id] = selected

with st.container():
    st.markdown('<div class="sn-sticky-footer"><div class="sn-footer-inner">', unsafe_allow_html=True)
    footer_cols = st.columns([1, 1, 1])
    skip_clicked = False
    continue_clicked = False
    with footer_cols[0]:
        skip_clicked = st.button(
            "Skip",
            type="secondary",
            use_container_width=True,
            key="gcp_context_skip",
        )
    with footer_cols[2]:
        continue_clicked = st.button(
            "Continue",
            type="primary",
            use_container_width=True,
            key="gcp_context_continue",
        )
    st.markdown(
        "</div><div class=\"sn-footer-note\">Respond as a person receiving care even if you’re filling it for someone else.</div></div>",
        unsafe_allow_html=True,
    )

if continue_clicked or skip_clicked:
    st.switch_page("pages/gcp_recommendation.py")
