"""Sample audiencing demo focused on the proxy journey."""
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


ENTRY_OPTIONS = (
    {
        "value": "proxy",
        "icon": "👥",
        "title": "I'm here for John",
        "description": "Walk me through supporting John with empathy and clarity.",
    },
    {
        "value": "self",
        "icon": "👤",
        "title": "I'm planning for myself",
        "description": "Help me understand what matters most for my own plan.",
    },
    {
        "value": "pro",
        "icon": "🧑‍💼",
        "title": "I'm a professional",
        "description": "I’m preparing guidance to share with families like John's.",
    },
)


def safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.experimental_rerun()


def _ensure_care_context() -> dict[str, object]:
    return st.session_state.setdefault("care_context", {"person_name": "John"})


def _handle_entry_selection(entry_value: str) -> None:
    state = ensure_audiencing_state()
    state["entry"] = entry_value
    state.setdefault("people", {}).update({"recipient_name": "John", "proxy_name": ""})
    apply_audiencing_sanitizer(state)
    compute_audiencing_route(state)
    snapshot = snapshot_audiencing(state)
    st.session_state["audiencing_snapshot"] = snapshot
    log_audiencing_set(snapshot)

    care_context = _ensure_care_context()
    care_context["person_name"] = "John" if entry_value != "self" else "You"

    gate_state = st.session_state.setdefault("gate", {})
    gate_state["medicaid_offramp_shown"] = False

    safe_switch_page("pages/contextual_welcome.py")


def _render_option(option: dict[str, str], *, highlight: bool) -> None:
    button_type = "primary" if highlight else "secondary"
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:.6rem;">
                <div style="font-size:2rem;">{option['icon']}</div>
                <div style="font-size:1.1rem;font-weight:600;">{option['title']}</div>
                <p style="margin:0;color:var(--ink-muted);">{option['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        pressed = st.button(
            "Choose",
            key=f"aud_john_choice_{option['value']}",
            type=button_type,
            use_container_width=True,
        )
        if pressed:
            _handle_entry_selection(option["value"])


def render_audiencing_entry(*, emphasize: str = "proxy") -> None:
    inject_theme()
    st.set_page_config(page_title="Tell Us About John", layout="centered")
    st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

    debug_flag = bool(st.session_state.get("dev_debug"))

    ensure_audiencing_state()

    with card_panel():
        st.markdown(
            """
            <div class="sn-hero-h1" style="margin-bottom:.4rem;">
              Let's get to know your role with John
            </div>
            <p style="margin:0;color:var(--ink-muted);font-size:1.05rem;">
              A few quick questions help us guide you to the right care. Some are essential,
              others help personalize your journey.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "Pick the role that best fits how you're helping John today."
        )

        cols = st.columns(3, gap="large")
        for col, option in zip(cols, ENTRY_OPTIONS):
            with col:
                _render_option(option, highlight=option["value"] == emphasize)

    if debug_flag:
        with st.expander("Debug: Audiencing state", expanded=False):
            st.json(st.session_state.get("audiencing", {}))
            st.markdown("---")
            st.json(st.session_state.get("audiencing_snapshot", {}))

    st.markdown("</div>", unsafe_allow_html=True)


render_audiencing_entry()

