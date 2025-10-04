import streamlit as st
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section, primary_secondary


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
    st.session_state.setdefault("gcp", {})


def main():
    _init_state()
    gcp_header(4)
    answers = st.session_state["gcp_answers"]
    gcp = st.session_state.get("gcp", {})

    def rec_body():
        payment_context = gcp.get("payment_context") or (
            "medicaid" if answers.get("medicaid_status") == "yes" else "private"
        )
        st.subheader("Your care recommendation")
        st.write(
            "We’ll show your personalized recommendation here with a short explanation."
        )
        if payment_context == "medicaid":
            st.info(
                """Medicaid covers long-term care differently. Next we’ll guide you to Plan for My Advisor. Cost Planner is optional."""
            )
        else:
            st.info(
                """You can continue to the Cost Planner to explore costs, offsets, and timeline."""
            )

        def _to_cp():
            safe_switch_page("ui/pages/03_cost_planner.py")

        def _to_pfma():
            safe_switch_page("ui/pages/05_plan_for_my_advisor.py")

        if payment_context == "medicaid":
            primary_secondary(
                "Continue to Plan for My Advisor",
                _to_pfma,
                "Open Cost Planner (optional)",
                _to_cp,
            )
        else:
            primary_secondary(
                "Open Cost Planner",
                _to_cp,
                "Plan for My Advisor",
                _to_pfma,
            )

    gcp_section("Guided Care Plan", "Recommendation", rec_body)


if __name__ == "__main__":
    main()
