from __future__ import annotations

import streamlit as st

from senior_nav import navigation
from senior_nav.documents import register_json
from senior_nav.state import completions, ensure_base_state, require_entry_type
from senior_nav.ui import header, render_ai_launcher, set_page_config


set_page_config(title="Guided Care Plan")
ensure_base_state()
require_entry_type()
flags = completions()

entry_type = st.session_state.get("entry_type")
header("Guided Care Plan", "Capture needs, safety, and funding in one place.")

existing = st.session_state.get("gcp") or {}
answers = existing.get("answers", {})

with st.form("gcp_form"):
    medicaid_choice = st.selectbox(
        "Do you currently receive Medicaid benefits?",
        ("Yes", "No", "Unsure"),
        index=("Yes", "No", "Unsure").index(answers.get("medicaid_q0", "Unsure")) if answers.get("medicaid_q0") else 2,
        help="We start with Medicaid to understand any coverage you may already have.",
    )
    living_setting = st.selectbox(
        "Where is the person living today?",
        (
            "At home",
            "With family",
            "Independent living",
            "Assisted living",
            "Memory care",
        ),
        index=(
            ("At home",
             "With family",
             "Independent living",
             "Assisted living",
             "Memory care")
        ).index(answers.get("living_setting", "At home")) if answers.get("living_setting") else 0,
    )
    safety_level = st.select_slider(
        "How much day-to-day support is needed?",
        options=["Low", "Moderate", "High"],
        value=answers.get("care_intensity", "Moderate"),
    )
    payment_context = st.selectbox(
        "How do you expect to pay for care?",
        (
            "Private pay",
            "Long-term care insurance",
            "Medicaid",
            "Medicare",
            "Veterans benefits",
        ),
        index=(
            ("Private pay",
             "Long-term care insurance",
             "Medicaid",
             "Medicare",
             "Veterans benefits")
        ).index(existing.get("payment_context", "Private pay")) if existing.get("payment_context") else 0,
    )
    funding_confidence = st.slider(
        "How confident do you feel about paying for this plan?",
        min_value=0,
        max_value=100,
        value=int(float(existing.get("funding_confidence", 0.5)) * 100),
        help="We'll use this to highlight the right cost planning mode.",
    )
    notes = st.text_area(
        "Anything else we should know?",
        value=answers.get("notes", ""),
        placeholder="Share context such as diagnoses, risks, or preferences.",
    )
    submitted = st.form_submit_button("Save care plan", type="primary")

if submitted:
    funding_score = round(funding_confidence / 100, 2)
    recommended_setting = "Memory care" if safety_level == "High" else (
        "Assisted living" if safety_level == "Moderate" else "In-home support"
    )

    contract = {
        "answers": {
            "medicaid_q0": medicaid_choice,
            "living_setting": living_setting,
            "care_intensity": safety_level,
            "notes": notes,
            "entry_type": entry_type,
        },
        "recommended_setting": recommended_setting,
        "care_intensity": safety_level,
        "payment_context": payment_context,
        "funding_confidence": funding_score,
        "medicaid_unsure_flag": medicaid_choice == "Unsure",
    }
    st.session_state.gcp = contract
    flags.mark("gcp", True)
    register_json("care_plan", kind="care_plan", title="Care Plan", payload=contract)
    st.success("Care plan saved. We'll take you back to the hub.")
    navigation.switch_page(navigation.HUB_PAGE)

render_ai_launcher()
