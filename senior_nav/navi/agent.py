"""Mock Navi assistant for the cost planner UI."""
from __future__ import annotations

from typing import Iterable, Tuple

import streamlit as st

from senior_nav.cost_planner import state


def _inject_styles() -> None:
    if st.session_state.get("__navi_styles__"):
        return
    st.session_state["__navi_styles__"] = True
    st.markdown(
        """
        <style>
        .navi-shell {
          position: fixed;
          right: 32px;
          bottom: 32px;
          z-index: 999;
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 12px;
        }
        .navi-panel {
          width: 320px;
          background: var(--sn-color-bg);
          border-radius: var(--sn-radius-lg);
          border: 1px solid var(--sn-color-border);
          box-shadow: var(--sn-shadow-soft);
          padding: var(--sn-spacing-lg);
        }
        .navi-panel h4 {
          margin-top: 0;
          margin-bottom: var(--sn-spacing-sm);
        }
        .navi-panel__item + .navi-panel__item {
          margin-top: var(--sn-spacing-sm);
          padding-top: var(--sn-spacing-sm);
          border-top: 1px dashed var(--sn-color-border);
        }
        .navi-bubble {
          background: var(--sn-color-primary);
          color: white;
          padding: 0.75rem 1.2rem;
          border-radius: 999px;
          font-weight: 600;
          box-shadow: var(--sn-shadow-soft);
        }
        .navi-bubble--quiet {
          background: rgba(43, 118, 229, 0.2);
          color: var(--sn-color-primary);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _determine_suggestions(drawer_key: str | None) -> Iterable[Tuple[str, dict[str, str]]]:
    copy = state.get_copy()["navi"]["suggestions"]
    cp_state = state.get_state()
    gcp_state = state.get_gcp_state()
    flags = state.get_flags()

    if gcp_state.get("chronic_conditions"):
        yield "chronic_conditions", copy["chronic_conditions"]
    if (
        cp_state["qualifiers"].get("owns_home") is True
        and drawer_key == "housing"
        and cp_state["drawer_status"].get("housing") == "start"
    ):
        yield "owns_home", copy["owns_home"]
    if flags.get("medicaid_unsure"):
        yield "medicaid", copy["medicaid"]


def render(drawer_key: str | None) -> None:
    """Render Navi bubble and suggestion panel."""
    _inject_styles()
    copy = state.get_copy()["navi"]
    cp_state = state.get_state()
    suggestions = list(_determine_suggestions(drawer_key))
    seen = cp_state["ui"].get("suggestions_shown", set())
    suggestion_ids = {f"{drawer_key or 'global'}:{key}" for key, _ in suggestions}
    unseen = suggestion_ids.difference(seen)

    panel_should_open = cp_state.get("mode") == "planning" and bool(unseen)
    if panel_should_open:
        state.mark_suggestions_seen(unseen)

    bubble_classes = "navi-bubble"
    bubble_text = copy["bubble_label"]
    if cp_state.get("mode") != "planning" or not suggestions:
        bubble_classes += " navi-bubble--quiet"
        bubble_text = copy["quiet_message"]

    panel_html = ""
    if panel_should_open and suggestions:
        items_html = "".join(
            f"""
            <div class=\"navi-panel__item\">
              <strong>{item['title']}</strong>
              <p style='margin:0.35rem 0 0 0; color: rgba(17,20,24,0.72);'>{item['body']}</p>
            </div>
            """
            for _, item in suggestions
        )
        panel_html = (
            f"""
            <div class=\"navi-panel\">
              <h4>Navi suggests</h4>
              {items_html}
            </div>
            """
        )

    st.markdown(
        f"""
        <div class=\"navi-shell\">
          {panel_html}
          <div class=\"{bubble_classes}\">{bubble_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
