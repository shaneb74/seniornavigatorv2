import streamlit as st
from senior_nav.components.choice_chips import choice_single
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section
from senior_nav.components import buttons


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
    st.session_state.setdefault("gcp_status", "in_progress")


def main():
    _init_state()
    gcp_header(0)
    buttons.page_start()

    answers = st.session_state["gcp_answers"]

    def form():
        st.subheader("Financial Eligibility")
        answers["medicaid_status"] = choice_single(
            "Are you currently on Medicaid or receiving state long-term care assistance?",
            ["yes", "no", "unsure"],
            value=answers.get("medicaid_status", "no"),
            key="gcp_medicaid_status",
        )

        if answers["medicaid_status"] != "yes":
            st.subheader("Financial Confidence")
            answers["funding_confidence"] = choice_single(
                "How confident do you feel about paying for care?",
                ["no_worries", "confident", "unsure", "not_confident"],
                value=answers.get("funding_confidence", "unsure"),
                key="gcp_funding_confidence",
            )
        else:
            st.info(
                "Medicaid changes how care is paid. We’ll still show a care recommendation, then guide the next step."
            )

        st.session_state["gcp_answers"] = answers

        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
            if buttons.secondary("Return to Hub", key="gcp_return_hub"):
                safe_switch_page("ui/pages/app.py")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            if buttons.primary("Continue to Daily Life & Support", key="gcp_to_daily"):
                safe_switch_page("ui/pages/gcp_daily_life.py")

    gcp_section("Guided Care Plan", "Financial", form)
    buttons.page_end()


if __name__ == "__main__":
    main()
