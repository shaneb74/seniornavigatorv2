import streamlit as st
from senior_nav.components.choice_chips import (
    choice_multi,
    choice_single,
    normalize_none,
)
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section
from senior_nav.components import buttons


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
def main():
    _init_state()
    gcp_header(2)
    buttons.page_start()
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

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
            if buttons.secondary("Back", key="gcp_health_back"):
                safe_switch_page("ui/pages/gcp_daily_life.py")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            if buttons.primary("Continue to Context & Preferences", key="gcp_to_context"):
                safe_switch_page("ui/pages/gcp_context_prefs.py")

    gcp_section("Guided Care Plan", "Health & Safety", form)
    buttons.page_end()


if __name__ == "__main__":
    main()
