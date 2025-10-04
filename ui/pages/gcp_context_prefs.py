import streamlit as st
from senior_nav.components.choice_chips import choice_multi, normalize_none
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section, primary_secondary


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
def main():
    _init_state()
    gcp_header(3)
    answers = st.session_state["gcp_answers"]

    def form():
        answers["chronic"] = normalize_none(
            choice_multi(
                "Any chronic conditions?",
                ["diabetes", "parkinson", "stroke", "copd", "chf", "other", "none"],
                values=answers.get("chronic", []),
                key="gcp_chronic",
            )
        )

        answers["preferences"] = normalize_none(
            choice_multi(
                "Any strong preferences?",
                ["stay_home", "be_near_family", "structured_care", "private_room", "none"],
                values=answers.get("preferences", []),
                key="gcp_preferences",
            )
        )

        st.session_state["gcp_answers"] = answers

        def _back():
            safe_switch_page("ui/pages/gcp_health_safety.py")

        def _next():
            safe_switch_page("ui/pages/gcp_recommendation.py")

        primary_secondary("Continue", _next, "Back", _back)

    gcp_section("Guided Care Plan", "Context & Preferences", form)


if __name__ == "__main__":
    main()
