import streamlit as st
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section, primary_secondary


def _init_state():
    st.session_state.setdefault("gcp_answers", {})


def main():
    _init_state()
    gcp_header(1)
    answers = st.session_state["gcp_answers"]

    def form():
        answers["who_for"] = st.radio(
            "Who are you planning for?",
            ["self", "parent", "spouse", "other"],
            index=(
                ["self", "parent", "spouse", "other"].index(
                    answers.get("who_for", "self")
                )
            ),
            horizontal=True,
        )
        answers["living_now"] = st.radio(
            "Where do they live today?",
            ["own_home", "with_family", "independent", "assisted", "memory", "skilled"],
            index=(
                ["own_home", "with_family", "independent", "assisted", "memory", "skilled"].index(
                    answers.get("living_now", "own_home")
                )
            ),
            horizontal=True,
        )
        answers["caregiver_support"] = st.radio(
            "How much caregiver support is available?",
            ["none", "few_days_week", "most_days", "24_7"],
            index=(
                ["none", "few_days_week", "most_days", "24_7"].index(
                    answers.get("caregiver_support", "none")
                )
            ),
            horizontal=True,
        )
        answers["adl_help"] = st.radio(
            "How many daily activities need help?",
            ["0-1", "2-3", "4-5", "6+"],
            index=(
                ["0-1", "2-3", "4-5", "6+"].index(answers.get("adl_help", "0-1"))
            ),
            horizontal=True,
        )

        st.session_state["gcp_answers"] = answers

        def _back():
            safe_switch_page("ui/pages/gcp.py")

        def _next():
            safe_switch_page("ui/pages/gcp_health_safety.py")

        primary_secondary("Continue", _next, "Back", _back)

    gcp_section("Guided Care Plan", "Daily Life & Support", form)


if __name__ == "__main__":
    main()
