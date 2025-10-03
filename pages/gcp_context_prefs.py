"""Guided Care Plan – Context & Preferences section."""

from __future__ import annotations

import streamlit as st

from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper

answers, _ = ensure_gcp_session()

st.set_page_config(page_title="GCP – Context & Preferences", layout="wide")

st.markdown("""
<h2 style="text-transform:uppercase; letter-spacing:0.08em; color:#6b7280; font-size:0.95rem;">Guided Care Plan</h2>
<h1 style="margin-bottom:0.4rem;">Context & Preferences</h1>
<p style="max-width:660px; color:#475569;">Share any ongoing health conditions and the preferences that should shape the plan.</p>
""", unsafe_allow_html=True)

render_stepper(3)

# Chronic conditions (multi-select)
chronic_meta = get_question_meta("chronic")
chronic_options = chronic_meta["options"]
stored_chronic = answers.get("chronic") or []
if not stored_chronic and "None" in chronic_options:
    stored_chronic = ["None"]

st.markdown('<div class="sn-card" style="margin-top:1.4rem;">', unsafe_allow_html=True)
st.markdown(f"<h3>{chronic_meta['label']}</h3>", unsafe_allow_html=True)
selected_chronic = st.multiselect(
    chronic_meta["label"],
    options=chronic_options,
    default=stored_chronic,
    help=chronic_meta.get("description"),
    key="gcp_chronic",
    label_visibility="collapsed",
)
if not selected_chronic and "None" in chronic_options:
    selected_chronic = ["None"]
answers["chronic"] = selected_chronic
st.markdown("</div>", unsafe_allow_html=True)

# Preferences (multi-select)
preferences_meta = get_question_meta("preferences")
preferences_options = preferences_meta["options"]
stored_preferences = answers.get("preferences") or []
if not stored_preferences and "No strong preference" in preferences_options:
    stored_preferences = ["No strong preference"]

st.markdown('<div class="sn-card" style="margin-top:1.4rem;">', unsafe_allow_html=True)
st.markdown(f"<h3>{preferences_meta['label']}</h3>", unsafe_allow_html=True)
selected_preferences = st.multiselect(
    preferences_meta["label"],
    options=preferences_options,
    default=stored_preferences,
    help=preferences_meta.get("description"),
    key="gcp_preferences",
    label_visibility="collapsed",
)
if not selected_preferences and "No strong preference" in preferences_options:
    selected_preferences = ["No strong preference"]
answers["preferences"] = selected_preferences
st.markdown("</div>", unsafe_allow_html=True)

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
