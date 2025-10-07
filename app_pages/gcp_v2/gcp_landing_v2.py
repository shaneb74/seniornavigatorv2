from __future__ import annotations

import streamlit as st

from gcp_core import scoring as gcp_scoring
from gcp_core.engine import questions_for_section, snapshot as build_snapshot
from gcp_core.state import (
    ensure_session,
    get_answers,
    get_medicaid_status,
    get_medicaid_ack,
    set_medicaid_ack,
    save_snapshot,
    set_section_complete,
)
from ui.gcp_form import render_section


def _render_medicaid_notice_for_landing(status: str, acknowledged: bool) -> None:
    if status not in {"yes", "unsure"} or acknowledged:
        return

    is_yes = status == "yes"
    with st.container(border=True):
        st.subheader("A quick note about Medicaid" if is_yes else "Not sure about Medicaid?")
        if is_yes:
            st.write(
                "We offer limited advisor services when someone is on **Medicaid** or state long-term care assistance. "
                "You can keep going—we’ll still prepare recommendations and planning tools for you."
            )
        else:
            st.write(
                "If you’re unsure about Medicaid eligibility, keep going. We’ll still guide you and highlight next steps, "
                "even if Medicaid ultimately applies."
            )

        col_link, col_ack = st.columns([1, 1])
        with col_link:
            st.link_button(
                "Learn about Medicaid",
                "https://www.medicaid.gov/",
            )
            st.caption("Opens in a new tab.")
        with col_ack:
            if st.button("I understand", type="primary"):
                set_medicaid_ack(True)
                st.rerun()


def _can_continue_on_landing(ans: dict, status: str, acknowledged: bool) -> bool:
    if status == "no":
        value = ans.get("funding_confidence")
        if isinstance(value, str):
            return bool(value.strip())
        return value is not None
    if status in {"yes", "unsure"}:
        return acknowledged
    return False
ensure_session()

answers = get_answers()
status = get_medicaid_status()
acknowledged = get_medicaid_ack()
if status not in {"yes", "unsure"} and acknowledged:
    set_medicaid_ack(False)
    acknowledged = False

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Guided Care Plan · Start")
st.caption("We’ll begin with financial eligibility, then daily life, health & safety, and preferences.")

render_section("financial", questions_for_section("financial"))

_render_medicaid_notice_for_landing(status, acknowledged)

can_continue = _can_continue_on_landing(answers, status, acknowledged)
if not can_continue:
    if status == "no":
        st.caption("Select your Medicaid status and share how confident you are about private funding to continue.")
    elif status in {"yes", "unsure"}:
        st.caption("Acknowledge the Medicaid note above to keep going.")
    else:
        st.caption("Tell us about Medicaid to continue.")

if st.button("Continue", type="primary", width="stretch", disabled=not can_continue):
    scoring = gcp_scoring.score_answers(answers)
    snapshot_record = build_snapshot(answers, scoring)
    save_snapshot(snapshot_record)
    set_section_complete("landing")
    st.switch_page("app_pages/gcp_v2/gcp_daily_life_v2.py")

if st.button("Save & exit to Hub", type="secondary", width="stretch"):
    st.switch_page("app_pages/hub.py")
