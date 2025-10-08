from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import streamlit as st

from gcp_core import clear_answer, ensure_session, get_answers, set_answer

COGNITION_QID = "cognition_level"
BEHAVIOR_QID = "behavior_risks"
SEVERE_TOKENS = {
    "major_decline",
    "advanced_dementia",
    "advanced",
    "severe",
    "needs_supervision",
    "needs_constant_supervision",
    "late_stage",
}

BEHAVIOR_CHOICES: List[Dict[str, str]] = [
    {"value": "wandering", "label": "Wandering"},
    {"value": "aggression", "label": "Aggression"},
    {"value": "elopement", "label": "Elopement (trying to leave)"},
    {"value": "exit_seeking", "label": "Exit-seeking"},
    {"value": "confusion", "label": "Confusion or disorientation"},
    {"value": "sundowning", "label": "Sundowning (night agitation)"},
    {"value": "repetitive_questioning", "label": "Repetitive questioning"},
    {"value": "poor_judgment", "label": "Poor judgment (unsafe decisions)"},
    {"value": "hoarding", "label": "Hoarding"},
    {"value": "sleep_disturbances", "label": "Sleep disturbances"},
]


def normalize_single(value: Optional[str], choices: Sequence[Dict[str, str]]) -> Optional[str]:
    """Normalize a label or token to the canonical token."""
    if value is None:
        return None
    text = str(value).strip().lower()
    if not text:
        return None
    for choice in choices:
        token = choice.get("value", "")
        label = choice.get("label", "")
        if text == str(token).strip().lower():
            return token
        if text == str(label).strip().lower():
            return token
    return None


def _is_severe_cognition(answers: Dict[str, object]) -> bool:
    token = normalize_single(answers.get(COGNITION_QID), [{"label": "", "value": t} for t in SEVERE_TOKENS])
    if token and token in SEVERE_TOKENS:
        return True
    raw = str(answers.get(COGNITION_QID) or "").lower()
    if any(word in raw for word in ("advanced", "severe", "needs supervision", "late-stage", "late stage")):
        return True
    return False


def _render_radio(
    qid: str,
    label: str,
    choices: Sequence[Dict[str, str]],
    help_text: Optional[str],
) -> Tuple[bool, bool]:
    answers = get_answers()
    current = normalize_single(answers.get(qid), choices)
    placeholder = "-- Select one --"
    labels = [placeholder] + [choice["label"] for choice in choices]
    default_index = 0
    if current:
        for idx, choice in enumerate(choices):
            if choice["value"] == current:
                default_index = idx + 1
                break
    picked_label = st.radio(
        label,
        labels,
        index=default_index,
        horizontal=True,
        help=help_text,
        key=f"{qid}_radio",
    )
    if picked_label == placeholder:
        picked_token = None
    else:
        picked_token = normalize_single(picked_label, choices)
    changed = picked_token != current
    if picked_token is None:
        clear_answer(qid)
    elif changed:
        set_answer(qid, picked_token)
    return True, changed


def _render_multiselect(
    qid: str,
    label: str,
    choices: Sequence[Dict[str, str]],
    help_text: Optional[str],
) -> Tuple[bool, bool]:
    answers = get_answers()
    existing = answers.get(qid)
    if not isinstance(existing, list):
        existing = []
    label_by_token = {choice["value"]: choice["label"] for choice in choices}
    default_labels = [label_by_token[token] for token in existing if token in label_by_token]
    picked_labels = st.multiselect(
        label,
        list(label_by_token.values()),
        default=default_labels,
        help=help_text,
        key=f"{qid}_multiselect",
    )
    picked_tokens = [
        choice["value"]
        for choice in choices
        if choice["label"] in picked_labels
    ]
    changed = picked_tokens != existing
    if picked_tokens:
        if changed:
            set_answer(qid, picked_tokens)
    else:
        if existing:
            clear_answer(qid)
            changed = True
    return True, changed


def _render_slider(
    qid: str,
    label: str,
    help_text: Optional[str],
    **opts,
) -> Tuple[bool, bool]:
    answers = get_answers()
    default = answers.get(qid)
    opts = dict(opts)
    min_value = int(opts.pop("min_value", 0))
    max_value = int(opts.pop("max_value", 100))
    step = int(opts.pop("step", 1))
    default_value = opts.pop("value", default if isinstance(default, (int, float)) else 0)
    slider_value = st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        step=step,
        value=int(default if isinstance(default, (int, float)) else default_value),
        help=help_text,
        key=f"{qid}_slider",
        **opts,
    )
    changed = slider_value != default
    if changed:
        set_answer(qid, slider_value)
    return True, changed


def _render_text(
    qid: str,
    label: str,
    help_text: Optional[str],
    textarea: bool = False,
) -> Tuple[bool, bool]:
    answers = get_answers()
    current = str(answers.get(qid) or "")
    if textarea:
        new_value = st.text_area(label, value=current, help=help_text, key=f"{qid}_textarea")
    else:
        new_value = st.text_input(label, value=current, help=help_text, key=f"{qid}_text")
    new_trimmed = new_value.strip()
    if new_trimmed:
        changed = new_trimmed != current
        if changed:
            set_answer(qid, new_trimmed)
    else:
        changed = bool(current)
        if changed:
            clear_answer(qid)
    return True, changed


def render_question(
    qid: str,
    label: str,
    qtype: str,
    *,
    choices: Optional[Sequence[Dict[str, str]]] = None,
    help: Optional[str] = None,
    **kwargs,
) -> Tuple[bool, bool]:
    """
    Render a question widget and persist the answer.
    Returns (was_shown, value_changed).
    """
    ensure_session()
    answers = get_answers()

    if qid == BEHAVIOR_QID and not _is_severe_cognition(answers):
        if answers.get(qid):
            clear_answer(qid)
            return False, True
        return False, False

    qtype = qtype.lower()
    if qtype == "radio":
        assert choices, "Radio question requires choices."
        return _render_radio(qid, label, choices, help)
    if qtype == "multiselect":
        assert choices, "Multiselect question requires choices."
        return _render_multiselect(qid, label, choices, help)
    if qtype == "slider":
        return _render_slider(qid, label, help, **kwargs)
    if qtype == "textarea":
        return _render_text(qid, label, help, textarea=True)
    if qtype == "text":
        return _render_text(qid, label, help)

    raise ValueError(f"Unsupported question type: {qtype}")
