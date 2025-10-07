"""Care Planning Hub — PFMA-styled, no spacer bars"""
from __future__ import annotations
import streamlit as st

from gcp_core.state import ensure_session, resume_target
from ui.components import ModuleCard, ModuleGrid
from ui.state import get_completion

def _goto(path: str, fail_msg: str | None = None) -> None:
    try:
        st.switch_page(path)  # type: ignore[attr-defined]
    except Exception:
        st.warning(fail_msg or f"Navigation failed. Verify {path} is registered in app.py.")
        st.rerun()

def render_hub() -> None:
    ensure_session()
    gcp_path = resume_target()

    st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="display:flex;flex-direction:column;gap:.5rem;margin-bottom:1rem;">
          <div class="sn-hero-h1" style="font-size:2.0rem;">Care Planning Hub</div>
          <p style="margin:0;color:var(--ink-muted);font-size:1.02rem;">
            Start with the Guided Care Plan, then explore the Cost Planner, and connect with your advisor when ready.
          </p>
        </div>
        """, unsafe_allow_html=True
    )

    aud_state = st.session_state.get("aud")
    care_context = st.session_state.get("care_context", {})
    person_name = (care_context.get("person_name") or "").strip()
    entry = aud_state.get("entry") if isinstance(aud_state, dict) else None
    if entry == "self":
        planning_for = "You"
    elif entry == "proxy":
        planning_for = person_name or "Your Loved One"
    else:
        planning_for = None

    if planning_for:
        st.caption(f"Planning for: {planning_for}")

    gcp_status = get_completion("gcp")
    cost_planner_status = get_completion("cost_planner")
    pfma_status = get_completion("pfma")

    begin_path = "app_pages/gcp_v2/gcp_landing_v2.py"
    resume_path = gcp_path or begin_path

    with ModuleGrid(cols=3, gap="large") as cols:
        with cols[0]:
            ModuleCard(
                icon="🧭",
                title="Guided Care Plan",
                body="Answer a few questions to get a tailored care recommendation.",
                primary_label="Begin",
                on_primary=lambda: _goto(
                    begin_path,
                    fail_msg="Navigation failed. Verify app_pages/gcp_v2/gcp_landing_v2.py is registered in app.py.",
                ),
                secondary_label="Resume" if gcp_status == "in_progress" else None,
                on_secondary=(lambda: _goto(resume_path)) if gcp_status == "in_progress" else None,
                status=gcp_status,
                testid="hub-card-gcp",
            )

        with cols[1]:
            ModuleCard(
                icon="💰",
                title="Cost Planner",
                body="Estimate monthly costs, compare options, and export a plan.",
                primary_label="Open Cost Planner",
                on_primary=lambda: _goto(
                    "app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py",
                    fail_msg="Navigation failed. Verify the Cost Planner modules hub is registered in app.py.",
                ),
                status=cost_planner_status,
                testid="hub-card-cost-planner",
            )

        with cols[2]:
            ModuleCard(
                icon="🤝",
                title="Plan for My Advisor",
                body="Package your situation into a concise brief for our team.",
                primary_label="Open PFMA",
                on_primary=lambda: _goto(
                    "app_pages/pfma.py",
                    fail_msg="Navigation failed. Verify app_pages/pfma.py is registered in app.py.",
                ),
                status=pfma_status,
                testid="hub-card-pfma",
            )

    st.markdown('</div>', unsafe_allow_html=True)

render_hub()
