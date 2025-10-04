"""Contextual welcome experience for people planning for themselves."""
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
    "headline": "Welcome—let’s build a plan around you",
    "body": (
        "We’ll begin with a few quick questions about your situation and how you",
        " feel about covering care. From there, we’ll personalize the guidance",
        " so you can move forward with confidence.",
    ),
}

FEATURE_CARDS = (
    {
        "title": "Clarity first",
        "copy": "Understand what to focus on right away and what can wait until later.",
    },
    {
        "title": "Financial insight",
        "copy": "See how coverage, savings, and benefits shape your next moves.",
    },
    {
        "title": "Always accessible",
        "copy": "Your Care Planning Hub keeps everything organized so you can revisit anytime.",
    },
)


def safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()


def _prime_audiencing_state() -> dict[str, object]:
    state = ensure_audiencing_state()
    state["entry"] = "self"
    people = state.setdefault("people", {"recipient_name": "", "proxy_name": ""})
    people["recipient_name"] = ""
    people["proxy_name"] = ""

    apply_audiencing_sanitizer(state)
    compute_audiencing_route(state)

    snapshot = snapshot_audiencing(state)
    st.session_state["audiencing_snapshot"] = snapshot
    log_audiencing_set(snapshot)

    care_context = st.session_state.setdefault("care_context", {"person_name": "You"})
    care_context["person_name"] = "You"

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


def render_contextual_welcome_self() -> None:
    inject_theme()
    st.set_page_config(page_title="Welcome – Planning for Yourself", layout="centered")
    st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    debug_flag = bool(st.session_state.get("dev_debug"))

    _prime_audiencing_state()

    with card_panel():
        st.markdown(
            f"""
            <div class="sn-hero-h1" style="margin-bottom:.4rem;">{HERO_COPY['headline']}</div>
            <p style=\"margin:0;color:var(--ink-muted);font-size:1.05rem;\">{''.join(HERO_COPY['body'])}</p>
            """,
            unsafe_allow_html=True,
        )

        st.caption("We’ll tailor the journey so you feel clear, confident, and in control of every step.")

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
                "Your personalized Care Planning Hub keeps guided plans, cost tools, and advisor resources together."
            )

    if debug_flag:
        with st.expander("Debug: Self contextual welcome", expanded=False):
            st.json(st.session_state.get("audiencing", {}))
            st.markdown("---")
            st.json(st.session_state.get("audiencing_snapshot", {}))

    st.markdown("</div>", unsafe_allow_html=True)


render_contextual_welcome_self()
