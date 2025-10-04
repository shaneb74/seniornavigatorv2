import streamlit as st
from senior_nav.components.choice_chips import choice_single
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section
from senior_nav.components import buttons


def _init_state():
    st.session_state.setdefault("gcp_answers", {})


def main():
    _init_state()
    gcp_header(1)
    buttons.page_start()
    answers = st.session_state["gcp_answers"]

    def form():
        answers["who_for"] = choice_single(
            "Who are you planning for?",
            ["self", "parent", "spouse", "other"],
            value=answers.get("who_for", "self"),
            key="gcp_who_for",
        )
        answers["living_now"] = choice_single(
            "Where do they live today?",
            ["own_home", "with_family", "independent", "assisted", "memory", "skilled"],
            value=answers.get("living_now", "own_home"),
            key="gcp_living_now",
        )
        answers["caregiver_support"] = choice_single(
            "How much caregiver support is available?",
            ["none", "few_days_week", "most_days", "24_7"],
            value=answers.get("caregiver_support", "none"),
            key="gcp_caregiver_support",
        )
        answers["adl_help"] = choice_single(
            "How many daily activities need help?",
            ["0-1", "2-3", "4-5", "6+"],
            value=answers.get("adl_help", "0-1"),
            key="gcp_adl_help",
        )

        st.session_state["gcp_answers"] = answers

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
            if buttons.secondary("Back to financial questions", key="gcp_daily_back"):
                safe_switch_page("ui/pages/gcp.py")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            if buttons.primary("Continue to Health & Safety", key="gcp_to_health"):
                safe_switch_page("ui/pages/gcp_health_safety.py")

    gcp_section("Guided Care Plan", "Daily Life & Support", form)
    buttons.page_end()


if __name__ == "__main__":
    main()
