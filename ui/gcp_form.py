from __future__ import annotations

import re
from typing import Dict, List

import streamlit as st

from gcp_core.questions import BEHAVIOR_RISKS_LABEL, load_questions
from gcp_core.state import (
    ensure_session,
    get_answers,
    get_answer,
    set_answer,
    set_medicaid_ack,
    clear_answer,
)

try:
    from streamlit import segmented_control as _has_segmented_control  # type: ignore[attr-defined]
    _SEGMENTED_AVAILABLE = True
except Exception:  # pragma: no cover
    _SEGMENTED_AVAILABLE = False


def _question_index() -> Dict[str, Dict]:
    index: Dict[str, Dict] = {}
    for row in load_questions():
        qid = row["id"]
        entry = index.setdefault(
            qid,
            {
                "label": (row.get("label") or "").strip(),
                "type": (row.get("type") or "single").strip(),
                "choices": [],
                "conditional_show": (row.get("conditional_show") or "").strip(),
            },
        )
        cid = row.get("choice_id")
        if cid:
            entry["choices"].append(
                {
                    "id": cid,
                    "label": (row.get("choice_label") or "").strip(),
                }
            )
    return index


_QUESTION_INDEX = _question_index()

COGNITION_QID = "cognition"
BEHAVIOR_QID = "behavior_risks"
BEHAVIOR_MULTI_LABEL = BEHAVIOR_RISKS_LABEL
_RAW_SEVERE_COG_CHOICES = {
    "severe",
    "severe memory issues",
    "advanced",
    "advanced dementia",
    "advanced_dementia",
    "advanced alzheimers",
    "advanced alzheimer's",
    "needs constant supervision",
    "needs_constant_supervision",
    "significant memory loss",
    "significant_memory_loss",
    "late-stage dementia",
    "late_stage_dementia",
    "late stage dementia",
    "late stage alzheimers",
    "late stage alzheimer's",
    "alzheimers advanced",
    "alzheimers_advanced",
    "serious_confusion",
    "serious confusion",
    "frequent_memory_issues",
    "frequent memory issues",
}


def _normalize_literal(value: object) -> str:
    text = "" if value is None else str(value)
    lowered = text.lower()
    stripped = lowered.replace("_", " ").replace("-", " ")
    cleaned = re.sub(r"[^0-9a-z\s]", " ", stripped)
    return " ".join(cleaned.split())


_SEVERE_COG_MATCHES = {_normalize_literal(choice) for choice in _RAW_SEVERE_COG_CHOICES}


def _bundle_visible(question: Dict, answers: Dict) -> bool:
    expr = (question.get("conditional_show") or "").strip()
    if not expr:
        return True
    lowered = expr.lower()
    if not lowered.startswith("show when"):
        return True
    clause = expr[len("SHOW when") :].strip()
    for op in ("!=", "=="):
        if op in clause:
            left, right = clause.split(op, 1)
            key = left.strip()
            value = right.strip().strip("'\"")
            current = answers.get(key)
            if isinstance(current, list):
                current = ",".join(current)
            return (current != value) if op == "!=" else (current == value)
    return True


def _normalize_choices(question: Dict) -> List[Dict]:
    choices = question.get("choices") or _QUESTION_INDEX.get(question["id"], {}).get("choices") or []
    return choices


def render_pill_choice(
    qid: str,
    label: str,
    options: List[str],
    *,
    current_token: str | None,
    token_by_label: Dict[str, str],
    label_by_token: Dict[str, str],
    key: str,
    disabled: bool = False,
) -> str | None:
    placeholder = "Select an option"
    display_options = [placeholder] + [opt for opt in options if opt != placeholder]
    current_label = label_by_token.get((current_token or ""), placeholder)

    if _SEGMENTED_AVAILABLE:
        picked_label = st.segmented_control(  # type: ignore[attr-defined]
            label,
            options=display_options,
            default=current_label if current_label in display_options else placeholder,
            key=key,
            disabled=disabled,
        )
    else:
        picked_label = st.radio(
            label,
            options=display_options,
            index=display_options.index(current_label) if current_label in display_options else 0,
            key=key,
            horizontal=True,
            disabled=disabled,
        )

    if picked_label == placeholder:
        return None
    return token_by_label.get(picked_label)


def _is_severe_cognition(value: object | None) -> bool:
    normalized = _normalize_literal(value)
    if not normalized:
        return False
    if normalized in _SEVERE_COG_MATCHES:
        return True
    if "severe" in normalized and ("memory" in normalized or "dementia" in normalized):
        return True
    if "advanced" in normalized and ("dementia" in normalized or "alzheim" in normalized):
        return True
    if "needs" in normalized and "supervision" in normalized:
        return True
    return False


def _should_render(question: Dict, answers: Dict) -> bool:
    qid = question.get("id", "")
    if qid == BEHAVIOR_QID:
        cognition_value = answers.get(COGNITION_QID)
        if not _is_severe_cognition(cognition_value):
            return False
    return _bundle_visible(question, answers)


def render_question(question: Dict) -> None:
    ensure_session()
    answers = get_answers()
    qid = question["id"]
    question = {
        **(_QUESTION_INDEX.get(qid, {})),
        **question,
    }

    if not _should_render(question, answers):
        if qid in answers:
            clear_answer(qid)
        return

    label = question.get("label") or "Question"
    helper = (question.get("helper") or question.get("help") or "").strip()
    qtype = question.get("type", "single")
    choices = _normalize_choices(question)

    st.markdown('<div class="gcp-question card section">', unsafe_allow_html=True)
    st.markdown(f"**{label}**")
    if helper:
        st.caption(helper)

    if qtype in {"single", "multi"} and not choices:
        st.warning(f"No choices configured for: {qid}")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    if qtype == "single":
        option_labels = [choice["label"] for choice in choices]
        token_by_label = {choice["label"]: choice["id"] for choice in choices}
        label_by_token = {choice["id"]: choice["label"] for choice in choices}
        normalizer = {}
        for token, lbl in label_by_token.items():
            normalizer[_normalize_literal(token)] = token
            normalizer[_normalize_literal(lbl)] = token

        stored_value = get_answer(qid)
        current_token = None
        if isinstance(stored_value, str):
            current_token = normalizer.get(_normalize_literal(stored_value))
            if current_token is None and stored_value in label_by_token:
                current_token = stored_value

        picked_token = render_pill_choice(
            qid=qid,
            label=label,
            options=option_labels,
            current_token=current_token,
            token_by_label=token_by_label,
            label_by_token=label_by_token,
            key=f"gcp_{qid}_pill",
        )

        if picked_token is None:
            clear_answer(qid)
            if qid == "medicaid_status":
                set_medicaid_ack(False)
        else:
            set_answer(qid, picked_token)
            if qid == "medicaid_status" and picked_token == "no":
                set_medicaid_ack(False)

    elif qtype == "multi":
        if qid == BEHAVIOR_QID:
            label = BEHAVIOR_MULTI_LABEL
        token_label = {choice["id"]: choice["label"] for choice in choices}
        option_tokens = [choice["id"] for choice in choices]
        current_ids = get_answer(qid, [])
        default_tokens = [token for token in option_tokens if token in (current_ids or [])]

        if qid == BEHAVIOR_QID:
            st.markdown('<div class="gcp-pill-multi">', unsafe_allow_html=True)

        picked_tokens = st.multiselect(
            label,
            option_tokens,
            default=default_tokens,
            key=f"gcp_{qid}_multi",
            format_func=lambda token: token_label.get(token, token.replace("_", " ").title()),
            placeholder="Select all that apply",
            label_visibility="visible",
        )

        if qid == BEHAVIOR_QID:
            st.markdown("</div>", unsafe_allow_html=True)

        if picked_tokens:
            set_answer(qid, picked_tokens)
        else:
            clear_answer(qid)

    elif qtype == "text":
        current_value = get_answer(qid, "")
        value = st.text_input(
            label,
            value=current_value,
            key=qid,
            label_visibility="visible",
        )
        set_answer(qid, value)

    st.markdown("</div>", unsafe_allow_html=True)


def render_section(section_name: str, questions: List[Dict]) -> None:
    ensure_session()
    st.markdown('<div class="gcp-section">', unsafe_allow_html=True)
    for question in questions:
        render_question(question)
    st.markdown("</div>", unsafe_allow_html=True)
