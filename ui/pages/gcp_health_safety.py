import streamlit as st
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section, primary_secondary


def _init_state():
    st.session_state.setdefault("gcp_answers", {})


def _normalize_none(selected_list):
    if "none" in selected_list and len(selected_list) > 1:
        return []
    return selected_list


def main():
    _init_state()
    gcp_header(2)
    answers = st.session_state["gcp_answers"]

    def form():
        answers["cognition"] = st.radio(
            "How is memory and thinking?",
            ["normal", "mild", "moderate", "severe"],
            index=(
                ["normal", "mild", "moderate", "severe"].index(
                    answers.get("cognition", "normal")
                )
            ),
            horizontal=True,
        )

        behavior = st.multiselect(
            "Any wandering or unsafe behaviors?",
            ["wandering", "agitation", "exit_seeking", "none"],
            default=answers.get("behavior_risks", []),
        )
        answers["behavior_risks"] = _normalize_none(behavior)

        answers["falls"] = st.radio(
            "Falls in the last 12 months?",
            ["none", "one", "recurrent"],
            index=(
                ["none", "one", "recurrent"].index(answers.get("falls", "none"))
            ),
            horizontal=True,
        )

        answers["med_mgmt"] = st.radio(
            "How complex are medications to manage?",
            ["simple", "several", "complex"],
            index=(
                ["simple", "several", "complex"].index(
                    answers.get("med_mgmt", "simple")
                )
            ),
            horizontal=True,
        )

        answers["home_safety"] = st.radio(
            "Is the home setup safe (stairs/bath/etc.)?",
            ["safe", "some_risks", "unsafe"],
            index=(
                ["safe", "some_risks", "unsafe"].index(
                    answers.get("home_safety", "safe")
                )
            ),
            horizontal=True,
        )

        answers["supervision"] = st.radio(
            "Do they have needed supervision at home?",
            ["always", "sometimes", "rarely", "never"],
            index=(
                ["always", "sometimes", "rarely", "never"].index(
                    answers.get("supervision", "always")
                )
            ),
            horizontal=True,
        )

        st.session_state["gcp_answers"] = answers

        def _back():
            safe_switch_page("ui/pages/gcp_daily_life.py")

        def _next():
            safe_switch_page("ui/pages/gcp_context_prefs.py")

        primary_secondary("Continue", _next, "Back", _back)

    gcp_section("Guided Care Plan", "Health & Safety", form)


if __name__ == "__main__":
    main()
