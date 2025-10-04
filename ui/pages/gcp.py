import streamlit as st
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import (
    gcp_header,
    gcp_section,
    primary_secondary,
)


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
    st.session_state.setdefault("gcp_status", "in_progress")


def main():
    _init_state()
    gcp_header(0)

    answers = st.session_state["gcp_answers"]

    def form():
        st.subheader("Financial Eligibility")
        answers["medicaid_status"] = st.radio(
            "Are you currently on Medicaid or receiving state long-term care assistance?",
            options=["yes", "no", "unsure"],
            index=(
                ["yes", "no", "unsure"].index(answers.get("medicaid_status", "no"))
                if answers.get("medicaid_status") in ["yes", "no", "unsure"]
                else 1
            ),
            horizontal=True,
        )

        if answers["medicaid_status"] != "yes":
            st.subheader("Financial Confidence")
            answers["funding_confidence"] = st.radio(
                "How confident do you feel about paying for care?",
                options=["no_worries", "confident", "unsure", "not_confident"],
                index=(
                    ["no_worries", "confident", "unsure", "not_confident"].index(
                        answers.get("funding_confidence", "unsure")
                    )
                ),
                horizontal=True,
            )
        else:
            st.info(
                "Medicaid changes how care is paid. We’ll still show a care recommendation, then guide the next step."
            )

        st.session_state["gcp_answers"] = answers

        def _next():
            safe_switch_page("ui/pages/gcp_daily_life.py")

        primary_secondary("Continue", _next)

    gcp_section("Guided Care Plan", "Financial", form)


if __name__ == "__main__":
    main()
