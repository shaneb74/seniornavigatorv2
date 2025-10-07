from __future__ import annotations
import streamlit as st

<<<<<<< Updated upstream
def _state():
    if "gcp" not in st.session_state:
        st.session_state.gcp = {"answers": {}, "flags": {}, "route": None, "payment_context": "private"}
    return st.session_state.gcp

def _meets_visibility(q, data):
    cond = q.get("visible_if")
    if not cond:
=======
from gcp_core.questions import (
    BEHAVIOR_RISKS_LABEL,
    COGNITION_SEVERE_TOKENS,
    load_questions,
)
from gcp_core.state import ensure_session, get_state, get_answer, norm_token, set_ack_medicaid, set_answer

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

COGNITION_QID = "cognition"  # bundle id; update if the source uses a different key
BEHAVIOR_QID = "behavior_risks"
BEHAVIOR_MULTI_LABEL = BEHAVIOR_RISKS_LABEL

SEVERE_TOKENS = {
    "severe",
    "severe_decline",
    "significant_decline",
    "diagnosed_dementia",
    "alzheimers_dementia",
    "alzheimers",
    "dementia",
    "advanced_impairment",
}
SEVERE_TOKENS.update(COGNITION_SEVERE_TOKENS)

SEVERE_SUBSTRINGS = (
    "serious",
    "severe",
    "diagnosed",
    "dementia",
    "alzheimer",
    "alzheimers",
    "major",
    "advanced",
)


def _debug_enabled() -> bool:
    try:
        params = getattr(st, "query_params", {})
        if callable(params):
            params = params()
        getter = getattr(params, "get", None)
        value = getter("dbg", "") if callable(getter) else params.get("dbg", "")
        if isinstance(value, (list, tuple, set)):
            return any(str(v) == "1" for v in value)
        return str(value) == "1"
    except Exception:
        return False


def _current_cognition_token(answers: Dict) -> str:
    raw = get_answer(answers, COGNITION_QID)
    if isinstance(raw, dict):
        token_candidate = raw.get("token") or raw.get("value") or raw.get("id") or raw.get("label")
        label_candidate = raw.get("label") or token_candidate
    else:
        token_candidate = raw
        label_candidate = raw

    token_normalized = norm_token(token_candidate)
    label_normalized = norm_token(label_candidate)
    candidate = token_normalized or label_normalized

    label_text = label_candidate if isinstance(label_candidate, str) else ""
    if label_text and any(sub in label_text.lower() for sub in SEVERE_SUBSTRINGS):
        candidate = "severe"
    return candidate


def _is_severe_cognition(answers: Dict) -> bool:
    token = _current_cognition_token(answers)
    if not token:
        return False
    if token in SEVERE_TOKENS:
        return True
    return any(sub in token for sub in SEVERE_SUBSTRINGS)


def _bundle_visible(question: Dict, answers: Dict) -> bool:
    expr = (question.get("conditional_show") or "").strip()
    if not expr:
>>>>>>> Stashed changes
        return True
    # support medicaid_status__ne == "yes"
    key, val = next(iter(cond.items()))
    if key.endswith("__ne"):
        field = key[:-4]
        return data["answers"].get(field) != val
    return True

def _label_for(choices, value):
    d = dict(choices)
    return d.get(value, value)

<<<<<<< Updated upstream
def render_question(q):
    data = _state()
    answers = data["answers"]
    qid = q["id"]
    if not _meets_visibility(q, data):
=======
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


def _should_render(question: Dict, answers: Dict) -> bool:
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

    debug_caption = ""

    if qid == BEHAVIOR_QID:
        cognition_token = _current_cognition_token(answers)
        severe = _is_severe_cognition(answers)
        if not severe:
            set_answer(answers, BEHAVIOR_QID, None)
            if _debug_enabled():
                st.caption(f"[debug] Behavior gating: hidden (cognition={cognition_token or '∅'})")
            return
        if _debug_enabled():
            debug_caption = f"[debug] Behavior gating: VISIBLE (cognition={cognition_token or '∅'})"

    if not _should_render(question, answers):
        if answers.get(qid) is not None:
            set_answer(answers, qid, None)
>>>>>>> Stashed changes
        return

    st.markdown('<div class="gcp-question card section">', unsafe_allow_html=True)
<<<<<<< Updated upstream
    st.markdown(f"<p class='gcp-question__label'>{q['label']}</p>", unsafe_allow_html=True)
    if q.get("helper"):
        st.markdown(f"<p class='gcp-question__helper'>{q['helper']}</p>", unsafe_allow_html=True)
=======
    st.markdown(f"**{label}**")
    if helper:
        st.caption(helper)
    if debug_caption:
        st.caption(debug_caption)
>>>>>>> Stashed changes

    if q["type"] == "single":
        idx = None
        choice_ids = [cid for cid, _ in q["choices"]]
        labels = [lbl for _, lbl in q["choices"]]
        if qid in answers and answers[qid] in choice_ids:
            idx = choice_ids.index(answers[qid])
        picked = st.radio(
            "",
            labels,
            index=idx if idx is not None else 0,
            horizontal=False,
            key=f"gcp_{qid}_radio",
            label_visibility="collapsed",
        )
        answers[qid] = choice_ids[labels.index(picked)]

    elif q["type"] == "multi":
        choice_ids = [cid for cid, _ in q["choices"]]
        labels = [lbl for _, lbl in q["choices"]]
        preselect = []
        if qid in answers:
            preselect = [_label_for(q["choices"], v) for v in answers[qid]]
        picked = st.multiselect(
            "",
            labels,
            default=preselect,
            key=f"gcp_{qid}_multi",
            label_visibility="collapsed",
        )
        answers[qid] = [choice_ids[labels.index(lbl)] for lbl in picked]
        # mutually exclusive "none"
        if "none" in answers[qid] and len(answers[qid]) > 1:
            answers[qid] = ["none"]

    st.markdown('</div>', unsafe_allow_html=True)

    # side effects after specific answers
    if qid == "medicaid_status":
        if answers.get("medicaid_status") == "yes":
            data["payment_context"] = "medicaid"
            data["route"] = "medicaid_offramp"
        else:
            data["payment_context"] = "private"
            data["route"] = None

def render_section(section_name: str, questions):
    st.markdown('<div class="gcp-section">', unsafe_allow_html=True)
    for q in questions:
        render_question(q)
    st.markdown('</div>', unsafe_allow_html=True)

def nav_buttons(prev: str | None, nxt: str | None):
    cols = st.columns(2)
    with cols[0]:
        if prev and st.button("◀ Back", use_container_width=True):
            try:
                st.switch_page(prev)
            except Exception:
                st.query_params["next"] = prev
                st.rerun()
    with cols[1]:
        if nxt and st.button("Next ▶", use_container_width=True):
            try:
                st.switch_page(nxt)
            except Exception:
                st.query_params["next"] = nxt
                st.rerun()
