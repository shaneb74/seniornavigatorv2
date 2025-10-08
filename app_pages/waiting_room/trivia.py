# Waiting Room Trivia stub
from __future__ import annotations

import streamlit as st


QUESTIONS = [
    {
        "question": "Which care professional specializes in assessing home safety?",
        "options": ["Physical therapist", "Occupational therapist", "Speech therapist", "Nutritionist"],
        "answer": "Occupational therapist",
    },
    {
        "question": "How often should medication lists be reviewed?",
        "options": ["Every 5 years", "Only after hospital stays", "At least annually", "Never"],
        "answer": "At least annually",
    },
    {
        "question": "What paperwork authorizes someone to make health decisions?",
        "options": ["Living trust", "Durable power of attorney", "Home lease", "Home deed"],
        "answer": "Durable power of attorney",
    },
    {
        "question": "Which housing option offers the most skilled care?",
        "options": ["Independent living", "Assisted living", "Skilled nursing", "Senior co-housing"],
        "answer": "Skilled nursing",
    },
    {
        "question": "What’s an early sign a caregiver may need more support?",
        "options": ["Frequent burnout or anxiety", "Scheduling weekly family calls", "Installing ramp access", "Buying grab bars"],
        "answer": "Frequent burnout or anxiety",
    },
]


def _score_state() -> dict:
    trivia = st.session_state.get("trivia")
    if not isinstance(trivia, dict):
        trivia = {}
    trivia.setdefault("score", 0)
    trivia.setdefault("answered", {})
    st.session_state["trivia"] = trivia
    return trivia


def render() -> None:
    st.title("Waiting Room · Trivia")
    st.write("Preview questions while we finish the full experience.")

    state = _score_state()
    answered = state["answered"]

    for idx, item in enumerate(QUESTIONS):
        question_key = f"question_{idx}"
        st.subheader(item["question"])
        current = answered.get(question_key)
        choice = st.radio(
            "Pick one",
            item["options"],
            index=item["options"].index(current) if current in item["options"] else -1,
            key=f"{question_key}_choice",
        )
        if st.button("Check answer", key=f"{question_key}_check"):
            if not choice:
                st.warning("Select an answer first.")
            else:
                answered[question_key] = choice
                if choice == item["answer"]:
                    state["score"] += 1
                    st.success("Correct!")
                else:
                    st.error(f"The best answer is {item['answer']}.")
                st.session_state["trivia"] = state

    st.info(f"Score so far: {state['score']} / {len(QUESTIONS)}")
    if st.button("Back to Waiting Room", type="secondary"):
        try:
            st.switch_page("app_pages/SeniorNav_waiting_room.py")  # type: ignore[attr-defined]
        except Exception:
            st.session_state["nav_target"] = "app_pages/SeniorNav_waiting_room.py"
            st.rerun()


render()
