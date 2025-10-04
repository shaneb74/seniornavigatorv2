"""Render a lightweight progress stepper."""
from __future__ import annotations

from typing import Iterable

import streamlit as st


def render(labels: Iterable[str], current_index: int) -> None:
    """Render the cost planner stepper as a static visual."""
    items = list(labels)
    html_parts = ["<ul class=\"sn-stepper\">"]
    for idx, label in enumerate(items, start=1):
        css_class = "sn-stepper__item"
        if idx - 1 == current_index:
            css_class += " is-active"
        html_parts.append(
            f"<li class=\"{css_class}\" data-step=\"{idx}\">{label}</li>"
        )
    html_parts.append("</ul>")
    st.markdown("\n".join(html_parts), unsafe_allow_html=True)
