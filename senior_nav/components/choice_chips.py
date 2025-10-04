"""Reusable Streamlit choice chip components for the Senior Navigator."""
from __future__ import annotations

from typing import Iterable, Mapping, Sequence

import streamlit as st


ChoiceOption = str | Mapping[str, str] | tuple[str, str]


def _normalize_options(options: Sequence[ChoiceOption]) -> list[tuple[str, str]]:
    """Return a list of (value, label) pairs for the provided options."""

    normalized: list[tuple[str, str]] = []
    for option in options:
        if isinstance(option, str):
            normalized.append((option, option))
        elif isinstance(option, Mapping):
            value = option.get("value")
            if value is None:
                continue
            label = option.get("label", str(value))
            normalized.append((str(value), str(label)))
        else:
            value, label = option
            normalized.append((str(value), str(label)))
    return normalized


def choice_single(
    label: str,
    options: Sequence[ChoiceOption],
    value: str | None = None,
    *,
    key: str | None = None,
    help_text: str | None = None,
) -> str:
    """Render an accessible single-select control styled as a chip group.

    Prefers Streamlit's segmented control (>= 1.30) for built-in keyboard support.
    Falls back to ``st.radio`` while preserving horizontal presentation.
    Returns the selected option.
    """

    normalized = _normalize_options(options)
    if not normalized:
        raise ValueError("choice_single requires at least one option")

    values = [option for option, _ in normalized]
    labels = {option: label for option, label in normalized}

    selection = value if value in values else values[0]
    widget_key = key or f"cs_{label}"

    try:
        selected = st.segmented_control(
            label,
            values,
            default=selection,
            key=widget_key,
            format_func=lambda option: labels.get(option, option),
            help=help_text,
        )
    except Exception:
        selected = st.radio(
            label,
            values,
            index=values.index(selection),
            horizontal=True,
            key=widget_key,
            format_func=lambda option: labels.get(option, option),
            help=help_text,
        )
    return selected


def choice_multi(
    label: str,
    options: Sequence[ChoiceOption],
    values: Iterable[str] | None = None,
    *,
    key: str | None = None,
) -> list[str]:
    """Render an accessible multi-select control styled as a chip grid.

    Uses native checkboxes for screen-reader compatibility and applies chip
    styling via CSS. Returns the list of selected options ordered as provided.
    """

    normalized = _normalize_options(options)
    if not normalized:
        return []

    current_values = set(str(item) for item in (values or []))
    widget_prefix = key or f"cm_{label}"

    column_count = min(len(normalized), 4)
    columns = st.columns(column_count)

    selected: list[str] = []
    for index, (option_value, option_label) in enumerate(normalized):
        column = columns[index % column_count]
        with column:
            checked = st.checkbox(
                option_label,
                value=option_value in current_values,
                key=f"{widget_prefix}_{option_value}",
            )
        if checked:
            selected.append(option_value)

    return selected


def normalize_none(values: Iterable[str] | None) -> list[str]:
    """Apply the shared "none" selection rule used across GCP multi-selects."""

    if not values:
        return []

    collected = list(values)
    if "none" in collected and len(collected) > 1:
        return []
    return collected
