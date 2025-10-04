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

    # Scope the page so our primary/secondary/link button CSS doesn't affect other modules
    buttons.page_start()

    def rec_body():
        payment_context = gcp.get("payment_context") or (
            "medicaid" if answers.get("medicaid_status") == "yes" else "private"
        )

        # Top: title + refresh (link-like)
        st.subheader("Your care recommendation")

        st.markdown('<div data-variant="link">', unsafe_allow_html=True)
        if buttons.secondary("Refresh recommendation", key="gcp_refresh"):
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Body copy
        st.write("We’ll show your personalized recommendation here with a short explanation.")
        if payment_context == "medicaid":
            st.info(
                "Medicaid covers long-term care differently. Next we’ll guide you to Plan for My Advisor. "
                "Cost Planner is optional."
            )
        else:
            st.info("You can continue to the Cost Planner to explore costs, offsets, and timeline.")

        # Bottom CTAs (primary/secondary)
        def _to_cp():
            safe_switch_page("ui/pages/03_cost_planner.py")  # adjust if your file name differs

        def _to_pfma():
            safe_switch_page("ui/pages/05_plan_for_my_advisor.py")

        c1, c2 = st.columns([1, 1])
        if payment_context == "medicaid":
            with c1:
                # Primary: PFMA
                if buttons.primary("Continue to Plan for My Advisor", key="gcp_to_pfma"):
                    _to_pfma()
            with c2:
                # Secondary: CP optional
                st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
                if buttons.secondary("Open Cost Planner (optional)", key="gcp_to_cp_opt"):
                    _to_cp()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            with c1:
                # Primary: CP
                if buttons.primary("Open Cost Planner", key="gcp_to_cp"):
                    _to_cp()
            with c2:
                # Secondary: PFMA
                st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
                if buttons.secondary("Plan for My Advisor", key="gcp_to_pfma_alt"):
                    _to_pfma()
                st.markdown("</div>", unsafe_allow_html=True)

    gcp_section("Guided Care Plan", "Recommendation", rec_body)

    buttons.page_end()


if __name__ == "__main__":
    main()