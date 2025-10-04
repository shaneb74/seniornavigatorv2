import streamlit as st
from senior_nav.components.choice_chips import (
    choice_multi,
    choice_single,
    normalize_none,
)
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section, primary_secondary


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
def main():
    _init_state()
    gcp_header(2)
    answers = st.session_state["gcp_answers"]

    def form():
        answers["cognition"] = choice_single(
            "How is memory and thinking?",
            ["normal", "mild", "moderate", "severe"],
            value=answers.get("cognition", "normal"),
            key="gcp_cognition",
        )

        answers["behavior_risks"] = normalize_none(
            choice_multi(
                "Any wandering or unsafe behaviors?",
                ["wandering", "agitation", "exit_seeking", "none"],
                values=answers.get("behavior_risks", []),
                key="gcp_behavior_risks",
            )
        )

        answers["falls"] = choice_single(
            "Falls in the last 12 months?",
            ["none", "one", "recurrent"],
            value=answers.get("falls", "none"),
            key="gcp_falls",
        )

        answers["med_mgmt"] = choice_single(
            "How complex are medications to manage?",
            ["simple", "several", "complex"],
            value=answers.get("med_mgmt", "simple"),
            key="gcp_med_mgmt",
        )

        answers["home_safety"] = choice_single(
            "Is the home setup safe (stairs/bath/etc.)?",
            ["safe", "some_risks", "unsafe"],
            value=answers.get("home_safety", "safe"),
            key="gcp_home_safety",
        )

        answers["supervision"] = choice_single(
            "Do they have needed supervision at home?",
            ["always", "sometimes", "rarely", "never"],
            value=answers.get("supervision", "always"),
            key="gcp_supervision",
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
