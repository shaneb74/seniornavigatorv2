"""Guided Care Plan – Health & Safety section."""

from __future__ import annotations

import streamlit as st

from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper

SECTION_QUESTIONS = [
    "cognition",
    "behavior_risks",
    "falls",
    "med_mgmt",
    "home_safety",
    "supervision",
]

answers, _ = ensure_gcp_session()

st.set_page_config(page_title="GCP – Health & Safety", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.95rem;">Guided Care Plan</h2>
<h1 style="margin-bottom:0.4rem;">Health & Safety</h1>
<p style="max-width:660px; color:#475569;">Tell us about memory, behaviors, falls, medications, and supervision so we can understand any safety risks.</p>
""", unsafe_allow_html=True)

render_stepper(2)

for question_id in SECTION_QUESTIONS:
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
            key="gcp_health_skip",
        )
    with footer_cols[2]:
        continue_clicked = st.button(
            "Continue",
            type="primary",
            use_container_width=True,
            key="gcp_health_continue",
        )
    st.markdown(
        "</div><div class=\"sn-footer-note\">Respond as a person receiving care even if you’re filling it for someone else.</div></div>",
        unsafe_allow_html=True,
    )

if continue_clicked or skip_clicked:
    st.switch_page("pages/gcp_context_prefs.py")
