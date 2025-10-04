"""Reusable Streamlit choice chip components for the Senior Navigator."""
from __future__ import annotations

from typing import Iterable, Mapping, Sequence
import streamlit as st

# A choice can be:
# - "foo"                              -> value="foo", label="foo"
# - {"value": "foo", "label": "Foo"}   -> explicit mapping
# - ("foo", "Foo")                     -> explicit tuple
ChoiceOption = str | Mapping[str, str] | tuple[str, str]


def _normalize_options(options: Sequence[ChoiceOption]) -> list[tuple[str, str]]:
    """Return a list of (value, label) pairs for the provided options.

    - str -> (str, str)
    - Mapping -> uses keys 'value' and optional 'label' (falls back to str(value))
    - tuple -> (value, label)
    """
    normalized: list[tuple[str, str]] = []
    for option in options:
        if isinstance(option, str):
            normalized.append((option, option))
        elif isinstance(option, Mapping):
            value = option.get("value")
            if value is None:
                # Skip invalid mapping without a value key
                continue
            label = option.get("label", str(value))
            normalized.append((str(value), str(label)))
        else:
            val, lab = option
            normalized.append((str(val), str(lab)))
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
    Returns the selected option VALUE (not label).
    """
    normalized = _normalize_options(options)
    if not normalized:
        raise ValueError("choice_single requires at least one option")

    values = [v for v, _ in normalized]
    labels = {v: l for v, l in normalized}

    selection = value if value in values else values[0]
    widget_key = key or f"cs_{label}"

    try:
        # segmented_control supports format_func and help
        selected = st.segmented_control(
            label,
            values,
            default=selection,
            key=widget_key,
            format_func=lambda v: labels.get(v, v),
            help=help_text,
        )
    except Exception:
        # Fallback for older Streamlit; keep the same formatting
        selected = st.radio(
            label,
            values,
            index=values.index(selection),
            horizontal=True,
            key=widget_key,
            format_func=lambda v: labels.get(v, v),
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
    styling via CSS. Returns the list of selected OPTION VALUES, ordered as provided.
    """
    normalized = _normalize_options(options)
    if not normalized:
        return []

    # Compare as strings because normalization stringifies values
    current_values = set(str(v) for v in (values or []))
    widget_prefix = key or f"cm_{label}"

    column_count = min(len(normalized), 4)
    columns = st.columns(column_count)

    selected: list[str] = []
    for idx, (opt_value, opt_label) in enumerate(normalized):
        col = columns[idx % column_count]
        with col:
            checked = st.checkbox(
                opt_label,
                value=(opt_value in current_values),
                key=f"{widget_prefix}_{opt_value}",
            )
        if checked:
            selected.append(opt_value)

    return selected


def normalize_none(values: Iterable[str] | None) -> list[str]:
    """Apply the shared 'none' selection rule used across GCP multi-selects.

    If 'none' is present alongside any other value, return [].
    """
    if not values:
        return []
    collected = list(values)
    if "none" in collected and len(collected) > 1:
        return []
    return collected