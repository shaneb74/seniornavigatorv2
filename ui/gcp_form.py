from __future__ import annotations
from typing import Dict, List

import streamlit as st

import gcp_core.state as gcp_state
from gcp_core.questions import load_questions
from gcp_core.state import ensure_session, get_state, get_answer, set_answer, set_ack_medicaid

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

SEVERE_COG_VALUES = {
    "serious_confusion",
    "advanced_dementia",
    "frequent_memory_issues",
    "serious confusion",
    "Serious confusion",
    "Advanced dementia",
    "advanced dementia",
    "Frequent memory issues",
    "frequent memory issues",
    "severe",
    "Severe",
    "Severe memory issues",
}


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


def _is_severe_cognition(answers: Dict) -> bool:
    raw = (answers.get(COGNITION_QID) or "").strip()
    if not raw:
        return False
    if raw in SEVERE_COG_VALUES:
        return True
    lowered = raw.lower().replace(" ", "_")
    if lowered in SEVERE_COG_VALUES:
        return True
    try:
        normed = (gcp_state.norm(raw) or "").strip()
    except Exception:
        normed = lowered
    return normed in SEVERE_COG_VALUES


def _should_render(question: Dict, answers: Dict) -> bool:
    qid = question.get("id", "")
    if qid == BEHAVIOR_QID and not _is_severe_cognition(answers):
        return False
    return _bundle_visible(question, answers)


def render_question(question: Dict) -> None:
    ensure_session()
    state = get_state()
    answers = state["answers"]
    qid = question["id"]
    question = {
        **(_QUESTION_INDEX.get(qid, {})),
        **question,
    }

    if not _should_render(question, answers):
        if answers.get(qid) is not None:
            set_answer(qid, None)
            answers.pop(qid, None)
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

        picked_token = render_pill_choice(
            qid=qid,
            label=label,
            options=option_labels,
            current_token=get_answer(qid),
            token_by_label=token_by_label,
            label_by_token=label_by_token,
            key=f"gcp_{qid}_pill",
        )

        if picked_token is None:
            answers.pop(qid, None)
            set_answer(qid, None)
            if qid == "medicaid_status":
                set_ack_medicaid(False)
        else:
            answers[qid] = picked_token
            set_answer(qid, picked_token)
            if qid == "medicaid_status" and picked_token == "no":
                set_ack_medicaid(False)

    elif qtype == "multi":
        option_labels = [choice["label"] for choice in choices]
        current_ids = get_answer(qid, [])
        default_labels = [choice["label"] for choice in choices if choice["id"] in (current_ids or [])]
        picked = st.multiselect(
            label,
            option_labels,
            default=default_labels,
            key=qid,
            label_visibility="visible",
        )
        selected_ids = [choice["id"] for choice in choices if choice["label"] in picked]
        set_answer(qid, selected_ids)

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
