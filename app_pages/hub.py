"""Care Planning Hub — PFMA-styled, no spacer bars"""
from __future__ import annotations
import streamlit as st

from gcp_core.state import ensure_session, resume_target

def _goto(path: str, fail_msg: str | None = None) -> None:
    try:
        st.switch_page(path)  # type: ignore[attr-defined]
    except Exception:
        st.warning(fail_msg or f"Navigation failed. Verify {path} is registered in app.py.")
        st.rerun()

def _tile(*, icon: str, status: str, title: str, desc: str, cta: str, dest: str, key: str, btn_type: str = "secondary", fail_msg: str | None = None) -> None:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:.5rem;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:1.4rem">{icon}</div>
                <div style="font-size:.9rem;color:var(--ink-muted)">{status}</div>
              </div>
              <h3 style="margin:0">{title}</h3>
              <p style="margin:.2rem 0 0;color:var(--ink-muted)">{desc}</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button(cta, type=btn_type, width="stretch", key=key):
            _goto(dest, fail_msg=fail_msg)

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

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        _tile(
            icon="🧭",
            status="Start here",
            title="Guided Care Plan",
            desc="Answer step-by-step to understand needs, safety, and the right care setting.",
            cta="Begin Guided Care Plan",
            dest=gcp_path,
            key="hub_gcp_begin",
            btn_type="primary",
            fail_msg="Navigation failed. Verify app.py registers app_pages/gcp_v2/gcp_landing_v2.py.",
        )
    with c2:
        _tile(
            icon="💰",
            status="Optional",
            title="Cost Planner",
            desc="Estimate monthly care costs and see how income, benefits, and savings fit.",
            cta="Explore costs",
            dest="app_pages/cost_planner_v2/cost_planner_landing_v2.py",
            key="hub_cp"
        )
    with c3:
        _tile(
            icon="🤝",
            status="Next step",
            title="Plan for My Advisor",
            desc="Share your context so a concierge advisor can help map next moves.",
            cta="Connect now",
            dest="app_pages/pfma.py",
            key="hub_pfma"
        )

    st.markdown('</div>', unsafe_allow_html=True)

render_hub()
