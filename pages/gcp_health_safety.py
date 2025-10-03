import streamlit as st

from guided_care_plan import ensure_gcp_session, get_question_meta, render_stepper

SECTION_QUESTIONS = [
    "falls_history",
    "cognition",
    "behavior_signals",
    "supervision_need",
]


def _ensure_widget_defaults(answers):
    for question_id in SECTION_QUESTIONS:
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
_ensure_widget_defaults(answers)

st.title("Guided Care Plan — Health & Safety")
st.caption("Step 2 of 5")

render_stepper(2)

error_placeholder = st.empty()

with st.form("gcp_health_safety_form"):
    selections = {qid: _render_radio(qid) for qid in SECTION_QUESTIONS}
    submitted = st.form_submit_button("Continue to Context & Preferences", type="primary")

if submitted:
    missing = [qid for qid, value in selections.items() if value is None]
    if missing:
        error_placeholder.error("Answer each question before moving on.")
    else:
        answers.update(selections)
        st.switch_page("pages/gcp_context_prefs.py")

if st.button("Back to Daily Life"):
    st.switch_page("pages/gcp_daily_life.py")
