"""Shared form helpers for the cost planner UI."""
from __future__ import annotations

from typing import Mapping

import streamlit as st


def choice_group(
    label: str,
    options: Mapping[str, str],
    *,
    key: str,
    default: str | None = None,
    horizontal: bool = False,
) -> str:
    """Render a radio choice using friendly labels."""
    keys = list(options.keys())
    if default is None:
        default = keys[0]
    return st.radio(
        label,
        options=keys,
        format_func=lambda value: options[value],
        key=key,
        index=keys.index(default) if default in keys else 0,
        horizontal=horizontal,
    )


def text_input(label: str, *, key: str, placeholder: str | None = None) -> str:
    """Render a text input."""
    return st.text_input(label, key=key, placeholder=placeholder or "")


def currency_input(label: str, *, key: str) -> str:
    """Render a simple currency text input (UI only)."""
    return st.text_input(label, key=key, placeholder="$0")


def checklist(options: list[str], *, key_prefix: str) -> dict[str, bool]:
    """Render a list of checkboxes and return their state."""
    state: dict[str, bool] = {}
    for idx, item in enumerate(options):
        state[item] = st.checkbox(item, key=f"{key_prefix}_{idx}")
    return state


def confirmation_checkbox(label: str, *, key: str) -> bool:
    """Render a confirmation checkbox."""
    return st.checkbox(label, key=key)
