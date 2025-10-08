from __future__ import annotations

from typing import Literal, cast

import streamlit as st

ProgressValue = Literal["not_started", "in_progress", "complete"]

_PROGRESS_BUCKET = "_sn_progress"
_VALID_STATUSES: set[ProgressValue] = {"not_started", "in_progress", "complete"}


def _ensure_bucket() -> dict[str, str]:
    bucket = st.session_state.setdefault(_PROGRESS_BUCKET, {})
    if not isinstance(bucket, dict):
        bucket = {}
        st.session_state[_PROGRESS_BUCKET] = bucket
    return bucket


def get_completion(key: str) -> ProgressValue:
    """
    Look up a completion status from session state, falling back to 'not_started'.
    """
    bucket = _ensure_bucket()
    value = bucket.get(key, "not_started")
    if value not in _VALID_STATUSES:
        return "not_started"
    return cast(ProgressValue, value)


def set_completion(key: str, value: ProgressValue) -> None:
    """
    Persist a validated completion status into session state.
    """
    if value not in _VALID_STATUSES:
        raise ValueError(f"Invalid completion status '{value}'.")
    bucket = _ensure_bucket()
    bucket[key] = value


def mark_complete(key: str) -> None:
    """Shortcut to mark a module as complete."""
    set_completion(key, "complete")
