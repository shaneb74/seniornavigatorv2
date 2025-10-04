"""Contextual welcome experience for caregivers supporting a loved one."""
from __future__ import annotations

import streamlit as st

from audiencing import (
    apply_audiencing_sanitizer,
    compute_audiencing_route,
    ensure_audiencing_state,
    log_audiencing_set,
    snapshot_audiencing,
)
from ui.components import card_panel
from ui.theme import inject_theme


HERO_COPY = {
    "headline": "We’re here to support you and your loved one",
    "body": (
        "We'll start with a few questions to understand care needs and your comfort",
        " planning. From there, we'll recommend options and resources to help you feel",
        " ready for the conversations ahead.",
    ),
    "accent": "We’ll guide you step by step so you always feel confident about what comes next.",
}

FEATURE_CARDS = (
    {
        "title": "Get grounded fast",
        "copy": "Answer a few essentials so we can highlight the right moves for your family.",
    },
    {
        "title": "Stay oriented",
        "copy": "Your Care Planning Hub keeps the Guided Care Plan, Cost Planner, and advisor handoff within reach.",
    },
    {
        "title": "Share with ease",
        "copy": "Export notes and roadmaps so siblings and loved ones stay in the loop.",
    },
)


def safe_switch_page(target: str) -> None:
    """Navigate to another page while handling Streamlit fallbacks."""

    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()


def _prime_audiencing_state() -> dict[str, object]:
    state = ensure_audiencing_state()
    state["entry"] = "proxy"
    people = state.setdefault("people", {"recipient_name": "", "proxy_name": ""})
    people.setdefault("recipient_name", "")
    people.setdefault("proxy_name", "")

    apply_audiencing_sanitizer(state)
    compute_audiencing_route(state)

    snapshot = snapshot_audiencing(state)
    st.session_state["audiencing_snapshot"] = snapshot
    log_audiencing_set(snapshot)

    care_context = st.session_state.setdefault("care_context", {"person_name": "Your Loved One"})
    care_context["person_name"] = people.get("recipient_name") or "Your Loved One"

    gate_state = st.session_state.setdefault("gate", {})
    gate_state.setdefault("medicaid_offramp_shown", False)

    return state


def _render_feature_cards() -> None:
    cols = st.columns(3, gap="large")
    for column, spec in zip(cols, FEATURE_CARDS):
        with column:
            with st.container(border=True):
                st.markdown(f"**{spec['title']}**")
                st.caption(spec["copy"])


def render_contextual_welcome_loved_one() -> None:
    inject_theme()
    st.set_page_config(page_title="Welcome – Supporting Your Loved One", layout="centered")
    st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    debug_flag = bool(st.session_state.get("dev_debug"))

    _prime_audiencing_state()

    with card_panel():
        st.markdown(
            f"""
            <div class="sn-hero-h1" style="margin-bottom:.4rem;">{HERO_COPY['headline']}</div>
            <p style="margin:0;color:var(--ink-muted);font-size:1.05rem;">{''.join(HERO_COPY['body'])}</p>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "We’ll guide you through a quick plan so you always know the next right step to take together."
        )

        st.markdown("<div class='sn-hr'></div>", unsafe_allow_html=True)

        _render_feature_cards()

        st.markdown("<div class='sn-hr'></div>", unsafe_allow_html=True)

        cta_col, helper_col = st.columns([2, 1])
        with cta_col:
            if st.button(
                "Continue to Care Planning Hub →",
                type="primary",
                use_container_width=True,
            ):
                safe_switch_page("pages/hub.py")
        with helper_col:
            st.caption(
                "The Care Planning Hub keeps your Guided Care Plan, Cost Planner, and advisor tools organized."
            )

    if debug_flag:
        with st.expander("Debug: Loved one contextual welcome", expanded=False):
            st.json(st.session_state.get("audiencing", {}))
            st.markdown("---")
            st.json(st.session_state.get("audiencing_snapshot", {}))

    st.markdown("</div>", unsafe_allow_html=True)


render_contextual_welcome_loved_one()
