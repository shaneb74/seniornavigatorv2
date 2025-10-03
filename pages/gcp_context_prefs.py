"""Guided Care Plan - Context & Preferences section."""
from __future__ import annotations



import streamlit as st

from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper
from guided_care_plan.state import current_audiencing_snapshot

from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope gcp">', unsafe_allow_html=True)


BASE_QUESTIONS = ["living_situation"]
CONDITIONAL_QUESTIONS = {
    "partner_support": {
        "qualifier": "has_partner",
        "default": "no_partner",
    },
    "home_safety": {
        "qualifier": "owns_home",
        "default": "not_homeowner",
    },
    "veteran_benefits": {
        "qualifier": "is_veteran",
        "default": "not_applicable",
    },
}


def _ensure_widget_defaults(answers, qualifiers):
    for question_id in BASE_QUESTIONS:
        _seed_default(question_id, answers)
    for question_id, cfg in CONDITIONAL_QUESTIONS.items():
        if qualifiers.get(cfg["qualifier"]):
            _seed_default(question_id, answers)
        else:
            answers[question_id] = cfg["default"]
            st.session_state[f"gcp_{question_id}"] = cfg["default"]


def _seed_default(question_id: str, answers):
    meta = get_question_meta(question_id)
    options = [option["value"] for option in meta["options"]]
    default_value = answers.get(question_id) or options[0]
    if default_value not in options:
        default_value = options[0]
    st.session_state.setdefault(f"gcp_{question_id}", default_value)


def _render_radio(question_id: str) -> str:
    meta = get_question_meta(question_id)
    option_map = {opt["value"]: opt["label"] for opt in meta["options"]}
    values = list(option_map.keys())
    selected_value = st.session_state.get(f"gcp_{question_id}", values[0])
    try:
        index = values.index(selected_value)
    except ValueError:
        index = 0
    with st.container(border=True):
        choice = st.radio(
            meta["label"],
            options=values,
            index=index,
            key=f"gcp_{question_id}",
            format_func=lambda value: option_map[value],
        )
        if meta.get("description"):
            st.caption(meta["description"])
    return choice


answers, _ = ensure_gcp_session()
snapshot = current_audiencing_snapshot()
qualifiers = snapshot.get("qualifiers", {})

_ensure_widget_defaults(answers, qualifiers)

st.title("Guided Care Plan - Context & Preferences")
st.caption("Step 3 of 5")

render_stepper(3)

error_placeholder = st.empty()

visible_questions = list(BASE_QUESTIONS)
for question_id, cfg in CONDITIONAL_QUESTIONS.items():
    if qualifiers.get(cfg["qualifier"]):
        visible_questions.append(question_id)

with st.form("gcp_context_form"):
    selections = {qid: _render_radio(qid) for qid in visible_questions}
    submitted = st.form_submit_button("Continue to Medical Check", type="primary")

if submitted:
    missing = [qid for qid, value in selections.items() if value is None]
    if missing:
        error_placeholder.error("Answer each question before moving on.")
    else:
        answers.update(selections)
        for question_id, cfg in CONDITIONAL_QUESTIONS.items():
            if not qualifiers.get(cfg["qualifier"]):
                answers[question_id] = cfg["default"]
        st.switch_page("pages/gcp_recommendation.py")

if st.button("Back to Health & Safety"):
    st.switch_page("pages/gcp_health_safety.py")

st.markdown('</div>', unsafe_allow_html=True)