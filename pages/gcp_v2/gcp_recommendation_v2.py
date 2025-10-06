from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from ui.gcp_form import _state, nav_buttons

VALUE_LABELS = {
    "medicaid_status": {"yes": "Yes", "no": "No", "unsure": "I'm not sure"},
    "funding_confidence": {
        "no_worries": "No worries",
        "confident": "Confident",
        "unsure": "Unsure",
        "not_confident": "Not confident",
    },
    "who_for": {
        "self": "Myself",
        "parent": "Parent",
        "spouse": "Spouse or partner",
        "other": "Someone else",
    },
    "living_now": {
        "own_home": "In their own home",
        "with_family": "With family",
        "independent": "Independent/retirement community",
        "assisted": "Assisted living",
        "memory": "Memory care",
        "skilled": "Skilled nursing",
    },
    "caregiver_support": {
        "none": "No regular help",
        "few_days_week": "Help a few days a week",
        "most_days": "Help most days",
        "24_7": "Help around the clock",
    },
    "adl_help": {
        "0-1": "0–1 activities",
        "2-3": "2–3 activities",
        "4-5": "4–5 activities",
        "6+": "6 or more activities",
    },
    "cognition": {
        "normal": "Sharp and consistent",
        "mild": "Mild changes",
        "moderate": "Noticeable confusion",
        "severe": "Severe memory loss",
    },
    "behavior_risks": {
        "wandering": "Wandering",
        "agitation": "Agitation or aggression",
        "exit_seeking": "Tries to leave unsafely",
        "none": "None of these",
    },
    "falls": {"none": "No falls", "one": "One fall", "recurrent": "More than one fall"},
    "med_mgmt": {
        "simple": "Simple routine",
        "several": "Several medications",
        "complex": "Complex schedule or frequent changes",
    },
    "home_safety": {
        "safe": "Safe setup",
        "some_risks": "Some safety risks",
        "unsafe": "Needs major safety support",
    },
    "supervision": {
        "always": "Always covered",
        "sometimes": "Covered most of the time",
        "rarely": "Covered occasionally",
        "never": "Rarely or never covered",
    },
    "chronic": {
        "diabetes": "Diabetes",
        "parkinson": "Parkinson’s",
        "stroke": "Stroke",
        "copd": "COPD",
        "chf": "Heart failure (CHF)",
        "other": "Other condition",
        "none": "No chronic conditions",
    },
    "preferences": {
        "stay_home": "Stay at home",
        "be_near_family": "Be near family",
        "structured_care": "Structured community",
        "private_room": "Private room",
        "none": "No strong preferences",
    },
}


def _format_answer(answers, question_id):
    value = answers.get(question_id)
    mapping = VALUE_LABELS.get(question_id, {})
    if isinstance(value, list):
        if not value:
            return "(not set)"
        return ", ".join(mapping.get(v, v) for v in value)
    if value is None:
        return "(not set)"
    return mapping.get(value, value)

st.set_page_config(layout="wide", page_title="GCP · Recommendation")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Guided Care Plan · Recommendation")
st.caption("Review the snapshot based on what you shared. You can adjust answers anytime and refresh this recommendation.")
data = _state()
ans = data.get("answers", {})
ctx = data.get("payment_context", "private")

if ctx == "medicaid":
    st.warning(
        "Based on what you shared, Medicaid may be your best next step. We’ll connect you to the Medicaid pathway and keep "
        "your answers ready for Plan for My Advisor."
    )
    nav_buttons("pages/gcp_v2/gcp_context_prefs_v2.py", "pages/pfma.py")
else:
    st.markdown("### Snapshot")
    st.markdown("Here’s a quick summary of your key details and care context.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Payment focus:** Private pay")
        st.markdown(f"**Funding confidence:** {_format_answer(ans, 'funding_confidence')}")
        st.markdown(f"**Planning for:** {_format_answer(ans, 'who_for')}")
        st.markdown(f"**Current living situation:** {_format_answer(ans, 'living_now')}")
        st.markdown(f"**Caregiver support:** {_format_answer(ans, 'caregiver_support')}")
        st.markdown(f"**Daily activities needing help:** {_format_answer(ans, 'adl_help')}")
    with col2:
        st.markdown(f"**Memory & thinking:** {_format_answer(ans, 'cognition')}")
        st.markdown(f"**Behavior risks:** {_format_answer(ans, 'behavior_risks')}")
        st.markdown(f"**Falls history:** {_format_answer(ans, 'falls')}")
        st.markdown(f"**Medication management:** {_format_answer(ans, 'med_mgmt')}")
        st.markdown(f"**Home safety:** {_format_answer(ans, 'home_safety')}")
        st.markdown(f"**Supervision coverage:** {_format_answer(ans, 'supervision')}")

    st.markdown("### Additional context")
    st.markdown(f"**Chronic conditions:** {_format_answer(ans, 'chronic')}")
    st.markdown(f"**Care preferences:** {_format_answer(ans, 'preferences')}")

    st.info("This is a draft summary. Your advisor can refine it with you and export via Plan for My Advisor.")
    nav_buttons("pages/gcp_v2/gcp_context_prefs_v2.py", "pages/pfma.py")
