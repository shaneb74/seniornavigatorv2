from __future__ import annotations
import streamlit as st
from gcp_core.engine import questions_for_section
from gcp_core.state import (
    ensure_session,
    get_state,
    medicaid_status,
    get_ack_medicaid,
    set_ack_medicaid,
    set_section_complete,
)
from ui.gcp_form import render_section


def _render_medicaid_notice_for_landing(answers: dict) -> None:
    status = medicaid_status(answers)
    if status not in ("yes", "unsure") or get_ack_medicaid():
        return

    is_yes = status == "yes"
    title = "A quick note about Medicaid" if is_yes else "Not sure about Medicaid?"
    with st.container(border=True):
        st.subheader(title)
        if is_yes:
            st.write(
                "We offer limited services for people on **Medicaid** or state long-term care assistance. "
                "You can still use our tools and get a recommendation here. "
                "_Note: Medicaid is not Medicare — we **do** support Medicare._"
            )
        else:
            st.write(
                "If you’re **unsure** about Medicaid, you can keep going and we’ll still provide guidance. "
                "If Medicaid ends up applying, our advisors may have limited options, "
                "but the tools here remain fully usable."
            )

        col_link, col_ack = st.columns([1, 1])
        with col_link:
            st.link_button(
                "Learn about Medicaid",
                "https://www.medicaid.gov/",
                type="secondary",
            )
            st.caption("Opens in a new tab.")
        with col_ack:
            if st.button("I understand — continue", key="gcp_landing_medicaid_ack", type="secondary"):
                set_ack_medicaid(True)
                st.rerun()


def _can_continue_on_landing(ans: dict) -> bool:
    status = medicaid_status(ans)
    if status == "no":
        return bool((ans.get("funding_confidence") or "").strip())
    if status in ("yes", "unsure"):
        return get_ack_medicaid()
    return False
ensure_session()

state = get_state()
answers = state["answers"]

status = medicaid_status(answers)
if status not in ("yes", "unsure"):
    set_ack_medicaid(False)

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Guided Care Plan · Start")
st.caption("We’ll begin with financial eligibility, then daily life, health & safety, and preferences.")

render_section("financial", questions_for_section("financial"))

_render_medicaid_notice_for_landing(answers)

disabled = not _can_continue_on_landing(answers)
if disabled:
    st.caption("Select your Medicaid status and, if not enrolled, a funding confidence level to continue.")

if st.button("Continue", type="primary", width="stretch", disabled=disabled):
    set_section_complete("landing")
    st.switch_page("app_pages/gcp_v2/gcp_daily_life_v2.py")

if st.button("Save & exit to Hub", type="secondary", width="stretch"):
    st.switch_page("app_pages/hub.py")
