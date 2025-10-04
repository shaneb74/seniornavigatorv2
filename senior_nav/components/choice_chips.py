"""Reusable Streamlit choice chip components for the Senior Navigator."""
from __future__ import annotations

from typing import Iterable, Sequence

import streamlit as st


def _ensure_sequence(options: Iterable[str]) -> list[str]:
    """Return a concrete list copy of the provided options."""
    return list(options)


def choice_single(
    label: str,
    options: Sequence[str],
    value: str | None = None,
    *,
    key: str | None = None,
) -> str:
    """Render an accessible single-select control styled as a chip group.

    Prefers Streamlit's segmented control (>= 1.30) for built-in keyboard support.
    Falls back to ``st.radio`` while preserving horizontal presentation.
    Returns the selected option.
    """

    opts = _ensure_sequence(options)
    if not opts:
        raise ValueError("choice_single requires at least one option")

    selection = value if value in opts else opts[0]
    widget_key = key or f"cs_{label}"

    try:
        selected = st.segmented_control(
            label,
            opts,
            default=selection,
            key=widget_key,
        )
    except Exception:
        selected = st.radio(
            label,
            opts,
            index=opts.index(selection),
            horizontal=True,
            key=widget_key,
        )
    return selected


def choice_multi(
    label: str,
    options: Sequence[str],
    values: Iterable[str] | None = None,
    *,
    key: str | None = None,
) -> list[str]:
    """Render an accessible multi-select control styled as a chip grid.

    Uses native checkboxes for screen-reader compatibility and applies chip
    styling via CSS. Returns the list of selected options ordered as provided.
    """

    opts = _ensure_sequence(options)
    current_values = set(values or [])
    widget_prefix = key or f"cm_{label}"

    if not opts:
        return []

    column_count = min(len(opts), 4)
    columns = st.columns(column_count)

    selected: list[str] = []
    for index, option in enumerate(opts):
        column = columns[index % column_count]
        with column:
            checked = st.checkbox(
                option,
                value=option in current_values,
                key=f"{widget_prefix}_{option}",
            )
        if checked:
            selected.append(option)

    return selected


def normalize_none(values: Iterable[str] | None) -> list[str]:
    """Apply the shared "none" selection rule used across GCP multi-selects."""

    if not values:
        return []

    collected = list(values)
    if "none" in collected and len(collected) > 1:
        return []
    return collected
