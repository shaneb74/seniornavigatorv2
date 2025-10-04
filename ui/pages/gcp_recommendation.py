import streamlit as st
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.gcp_shell import gcp_header, gcp_section
from senior_nav.components import buttons


def _init_state():
    st.session_state.setdefault("gcp_answers", {})
    st.session_state.setdefault("gcp", {})


def main():
    _init_state()
    gcp_header(4)

    answers = st.session_state["gcp_answers"]
    gcp = st.session_state.get("gcp", {})

    # Scope page-level button CSS
    buttons.page_start()

    def rec_body():
        st.subheader("Your care recommendation")

        # Link-style refresh
        st.markdown('<div data-variant="link">', unsafe_allow_html=True)
        if buttons.secondary("Refresh recommendation", key="gcp_refresh"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("We’ll show your personalized recommendation here with a short explanation.")

        pay = gcp.get("payment_context") or (
            "medicaid" if answers.get("medicaid_status") == "yes" else "private"
        )

        if pay == "medicaid":
            st.info(
                "Medicaid covers long-term care differently. Next we’ll guide you to Plan for My Advisor. "
                "Cost Planner is optional."
            )
        else:
            st.info("You can continue to the Cost Planner to explore costs, offsets, and timeline.")

        # Bottom CTAs
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
            if buttons.secondary("Back", key="gcp_rec_back"):
                safe_switch_page("ui/pages/gcp_context_prefs.py")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            if pay == "medicaid":
                if buttons.primary("Continue to Plan for My Advisor", key="gcp_to_pfma"):
                    safe_switch_page("ui/pages/05_plan_for_my_advisor.py")
            else:
                if buttons.primary("Continue to Cost Planner", key="gcp_to_cp"):
                    safe_switch_page("ui/pages/03_cost_planner.py")

    gcp_section("Guided Care Plan", "Recommendation", rec_body)

    buttons.page_end()


if __name__ == "__main__":
    main()