import streamlit as st
from senior_nav.components.choice_chips import choice_multi, normalize_none
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section
from senior_nav.components import buttons


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
def main():
    _init_state()
    gcp_header(3)
    buttons.page_start()
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

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
            if buttons.secondary("Back", key="gcp_context_back"):
                safe_switch_page("ui/pages/gcp_health_safety.py")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            if buttons.primary("See Care Recommendation", key="gcp_to_rec"):
                safe_switch_page("ui/pages/gcp_recommendation.py")

    gcp_section("Guided Care Plan", "Context & Preferences", form)
    buttons.page_end()


if __name__ == "__main__":
    main()
