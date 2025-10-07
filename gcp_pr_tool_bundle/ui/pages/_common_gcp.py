import streamlit as st, csv, os, json
from guided_care_plan.state import get_answers, set_answer, get_aud, normalize_multi

QUESTIONS_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "guided_care_plan", "questions", "questions.csv")

def load_questions():
    rows = list(csv.DictReader(open(QUESTIONS_CSV, "r", encoding="utf-8")))
    order, grouped = [], {}
    for r in rows:
        qid = r["id"]
        if qid not in grouped:
            grouped[qid] = {"id": qid, "label": r["label"], "type": r["type"], "choices": [], "conditional_show": r.get("conditional_show","")}
            order.append(qid)
        grouped[qid]["choices"].append({"id": r["choice_id"], "label": r["choice_label"]})
    return [grouped[i] for i in order]

def show_single(q, answers):
    labels = [c["label"] for c in q["choices"]]
    ids = [c["id"] for c in q["choices"]]
    cur = answers.get(q["id"], ids[0] if ids else None)
    idx = ids.index(cur) if cur in ids else 0
    sel = st.selectbox(q["label"], labels, index=idx, key=q["id"]+"_ctrl")
    set_answer(q["id"], ids[labels.index(sel)])

def show_multi(q, answers):
    labels = [c["label"] for c in q["choices"]]
    ids = [c["id"] for c in q["choices"]]
    cur = answers.get(q["id"], [])
    defaults = [labels[ids.index(v)] for v in cur if v in ids]
    sel = st.multiselect(q["label"], labels, default=defaults, key=q["id"]+"_ctrl")
    chosen_ids = [ids[labels.index(s)] for s in sel]
    set_answer(q["id"], normalize_multi(chosen_ids))

def should_show(q, answers):
    cond = (q.get("conditional_show") or "").strip()
    if not cond: return True
    # Implement the two used conditions deterministically
    if "medicaid_status" in cond and "!=" in cond:
        return answers.get("medicaid_status") != "yes"
    if "SHOW when cognition in" in cond:
        return (answers.get("cognition") in {"mild","moderate","severe"})
    if "SHOW when any of {" in cond:
        return any([answers.get("cognition") in {"mild","moderate","severe"},
                    answers.get("mobility") in {"cane_or_walker","wheelchair"},
                    answers.get("falls") in {"one","recurrent"},
                    answers.get("home_safety") in {"some_risks","unsafe"}])
    return True
