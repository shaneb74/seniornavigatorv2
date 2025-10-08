# Shared AI agent card component for Waiting Room and related pages
from __future__ import annotations

from datetime import datetime
from typing import Callable, List, Optional

from html import escape

import streamlit as st

AskHandler = Callable[[str], str]

_INPUT_KEY = "_ai_agent_prompt"


def _ensure_ai_state() -> dict:
    state = st.session_state.get("ai")
    if not isinstance(state, dict):
        state = {"history": [], "suggested_prompts": []}
        st.session_state["ai"] = state
    state.setdefault("history", [])
    state.setdefault("suggested_prompts", [])
    return state


def _default_agent_response(prompt: str) -> str:
    trimmed = prompt.strip()
    if not trimmed:
        return "Let me know what you’d like to explore and I’ll share planning tips you can review with your care team."
    return (
        "Here are starting points to explore next:\n"
        f"• Summarize what you know about “{trimmed}”.\n"
        "• List questions to raise with licensed professionals.\n"
        "• Outline actions you can revisit in your Care Hub.\n\n"
        "Remember: This assistant offers general guidance only. Confirm decisions with qualified experts."
    )


def render_agent_card(
    *,
    suggested: Optional[List[str]] = None,
    on_ask: Optional[AskHandler] = None,
) -> None:
    """
    Render the AI advisor dock. Keeps history in st.session_state.ai.history.
    """
    ai_state = _ensure_ai_state()
    if suggested:
        ai_state["suggested_prompts"] = suggested
    suggestions = suggested or ai_state.get("suggested_prompts", [])

    st.markdown("<div class='sn-card sn-agent-card'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sn-card-header">
          <div class="sn-card-header-left">
            <span class="sn-icon sn-icon--emoji" aria-hidden="true">🤖</span>
            <div class="sn-card-heading">
              <h3 class="sn-card-title">Ask an Advisor (AI)</h3>
              <p class="sn-card-caption">For general guidance only; not medical, legal, or financial advice.</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sn-card-body'>", unsafe_allow_html=True)

    if suggestions:
        chip_cols = st.columns(min(len(suggestions), 3), gap="small")
        for idx, prompt_text in enumerate(suggestions):
            col = chip_cols[idx % len(chip_cols)]
            with col:
                if st.button(
                    prompt_text,
                    key=f"agent_suggest_{idx}",
                    help="Use this question",
                    type="secondary",
                ):
                    st.session_state[_INPUT_KEY] = prompt_text
                    st.experimental_rerun()

    prompt_value = st.session_state.get(_INPUT_KEY, "")
    input_cols = st.columns([4, 1], gap="small")
    with input_cols[0]:
        user_prompt = st.text_input(
            "Ask the advisor",
            value=prompt_value,
            key=_INPUT_KEY,
            placeholder="Type a question to get planning guidance…",
            label_visibility="collapsed",
        )
    submitted = False
    with input_cols[1]:
        submitted = st.button(
            "Ask",
            key="agent_submit",
            type="primary",
            use_container_width=True,
            disabled=not user_prompt.strip(),
            help="Send your question to the AI advisor",
        )

    if submitted:
        ask_handler = on_ask or _default_agent_response
        response_text = ask_handler(user_prompt)
        history: List[dict] = ai_state.setdefault("history", [])
        timestamp = datetime.utcnow().isoformat()
        history.append({"role": "user", "content": user_prompt.strip(), "ts": timestamp})
        history.append({"role": "assistant", "content": response_text, "ts": timestamp})
        st.session_state[_INPUT_KEY] = ""
        st.experimental_rerun()

    history: List[dict] = ai_state.get("history", [])
    if history:
        st.markdown("**Recent questions**")
        for turn in history[-6:]:
            role = turn.get("role", "user").capitalize()
            content = escape(turn.get("content", ""))
            st.markdown(f"<p><strong>{escape(role)}:</strong> {content}</p>", unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)
