from __future__ import annotations
import streamlit as st

def _state():
    if "gcp" not in st.session_state:
        st.session_state.gcp = {"answers": {}, "flags": {}, "route": None, "payment_context": "private"}
    return st.session_state.gcp

def _meets_visibility(q, data):
    cond = q.get("visible_if")
    if not cond:
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

def render_question(q):
    data = _state()
    answers = data["answers"]
    qid = q["id"]
    if not _meets_visibility(q, data):
        return

    st.markdown('<div class="gcp-question card section">', unsafe_allow_html=True)
    st.markdown(f"<p class='gcp-question__label'>{q['label']}</p>", unsafe_allow_html=True)
    if q.get("helper"):
        st.markdown(f"<p class='gcp-question__helper'>{q['helper']}</p>", unsafe_allow_html=True)

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
