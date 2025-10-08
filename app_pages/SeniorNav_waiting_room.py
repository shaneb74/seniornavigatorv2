# Waiting Room — distinct post-plan experience
from __future__ import annotations

from html import escape
from typing import Dict, Iterable

import streamlit as st


FEATURES = [
    {
        "key": "trivia",
        "icon": "🧠",
        "title": "Trivia Time",
        "desc": "Test your care knowledge with quick daily questions.",
        "cta": "Play Trivia",
        "target": "app_pages/waiting_room/trivia.py",
    },
    {
        "key": "partners",
        "icon": "🤝",
        "title": "Partner Spotlight",
        "desc": "Meet trusted organizations ready to lend a hand.",
        "cta": "View Partners",
        "target": "app_pages/waiting_room/partners.py",
    },
    {
        "key": "second_opinion",
        "icon": "🩺",
        "title": "Second Opinion",
        "desc": "Request a consult with a physician or gerontologist.",
        "cta": "Request Consult",
        "target": "app_pages/waiting_room/second_opinion.py",
    },
]


def _progress_flags() -> Dict[str, bool]:
    progress = st.session_state.get("progress")
    if not isinstance(progress, dict):
        progress = {}
        st.session_state["progress"] = progress
    for key in ("gcp_done", "cp_done", "pfma_done"):
        progress.setdefault(key, False)
    return progress  # type: ignore[return-value]


def _goto(path: str) -> None:
    try:
        st.switch_page(path)  # type: ignore[attr-defined]
    except Exception:
        st.session_state["nav_target"] = path
        st.rerun()


def _feature_card(*, icon: str, title: str, desc: str, cta: str, target: str, disabled: bool, key: str) -> None:
    with st.container():
        st.markdown(
            f"""
            <div class="sn-card sn-waiting-card">
              <div class="sn-card-header">
                <div class="sn-card-header-left">
                  <span class="sn-icon sn-icon--emoji" role="img" aria-label="{escape(title)} icon">{escape(icon)}</span>
                  <div class="sn-card-heading">
                    <h3 class="sn-card-title">{escape(title)}</h3>
                    <p class="sn-card-caption">{escape(desc)}</p>
                  </div>
                </div>
              </div>
              <div class="sn-card-body">
            """,
            unsafe_allow_html=True,
        )
        button = st.button(
            cta,
            key=f"{key}_cta",
            type="primary",
            use_container_width=True,
            disabled=disabled,
            help=cta if not disabled else "Unlock this feature by completing a plan.",
        )
        st.markdown("</div></div>", unsafe_allow_html=True)
        if button and not disabled:
            _goto(target)


def _agent_state() -> Dict[str, object]:
    agent = st.session_state.get("agent")
    if not isinstance(agent, dict):
        agent = {}
        st.session_state["agent"] = agent
    agent.setdefault("open", False)
    agent.setdefault("last_prompt", "")
    return agent  # type: ignore[return-value]


def _render_agent_toggle() -> None:
    agent = _agent_state()
    cols = st.columns([1, 5, 1])
    with cols[-1]:
        label = "Ask our Care Agent" if not agent["open"] else "Hide Care Agent"
        if st.button(label, key="_agent_toggle", type="secondary"):
            agent["open"] = not agent["open"]
            st.session_state["agent"] = agent
            st.experimental_rerun()

    if agent["open"]:
        dock_cols = st.columns([3, 1])
        with dock_cols[-1]:
            with st.container():
                st.markdown(
                    """
                    <div class="sn-card sn-agent-dock">
                      <div class="sn-card-header">
                        <div class="sn-card-header-left">
                          <span class="sn-icon sn-icon--emoji" aria-hidden="true">🤖</span>
                          <div class="sn-card-heading">
                            <h3 class="sn-card-title">Ask our Care Agent</h3>
                            <p class="sn-card-caption">Share a question and we’ll note it for your next session.</p>
                          </div>
                        </div>
                      </div>
                      <div class="sn-card-body">
                    """,
                    unsafe_allow_html=True,
                )
                prompt = st.text_input(
                    "Ask a question",
                    value=str(agent.get("last_prompt") or ""),
                    key="_agent_prompt",
                    label_visibility="collapsed",
                    placeholder="Type your question…",
                )
                send = st.button(
                    "Send",
                    key="_agent_send",
                    type="primary",
                    use_container_width=True,
                    disabled=not prompt.strip(),
                )
                st.markdown("</div></div>", unsafe_allow_html=True)
                if send and prompt.strip():
                    agent["last_prompt"] = prompt.strip()
                    st.session_state["agent"] = agent
                    st.success("Saved! We’ll remember this for next time.")


def render() -> None:
    progress = _progress_flags()
    unlocked = any(progress.get(flag, False) for flag in ("gcp_done", "cp_done", "pfma_done"))

    st.title("Waiting Room")
    st.write("Explore helpful extras while you consider next steps.")

    if not unlocked:
        st.info("Complete a plan to unlock extras.")

    columns = st.columns(3, gap="large")
    for idx, feature in enumerate(FEATURES):
        column = columns[idx % len(columns)]
        with column:
            _feature_card(
                icon=feature["icon"],
                title=feature["title"],
                desc=feature["desc"],
                cta=feature["cta"],
                target=feature["target"],
                disabled=not unlocked,
                key=feature["key"],
            )

    _render_agent_toggle()


render()
