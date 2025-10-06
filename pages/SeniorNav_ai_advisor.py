from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav, safe_switch

st.set_page_config(layout="wide", page_title="AI Advisor")
inject_theme()
top_nav()

st.markdown("## AI Advisor")
st.subheader("I'm Navi — your expert advisor.")
st.write("Pages I help you see the whole map: care paths, hidden costs, decisions no one talks about. For your loved one.")

st.markdown("#### Top Questions")
q1 = "How much does home care cost?"
q2 = "Can VA help with costs?"
q3 = "What's next after planning?"

col = st.columns(3)
if col[0].button(q1, use_container_width=True):
    st.session_state["ai_input"] = q1
    st.session_state.setdefault("ai_thread", []).append(("user", q1))
if col[1].button(q2, use_container_width=True):
    st.session_state["ai_input"] = q2
    st.session_state.setdefault("ai_thread", []).append(("user", q2))
if col[2].button(q3, use_container_width=True):
    st.session_state["ai_input"] = q3
    st.session_state.setdefault("ai_thread", []).append(("user", q3))

st.markdown("#### Ask Me Anything")
prompt = st.text_input("Your question…", key="ai_input", placeholder="e.g., How can I afford home care?")
send = st.button("Send", type="primary", key="ai_send")
clear = st.button("Clear chat")

if clear:
    st.session_state["ai_thread"] = []
    st.session_state["ai_input"] = ""

thread = st.session_state.setdefault("ai_thread", [])

def _fake_llm_answer(q: str) -> str:
    if not q.strip():
        return "Ask me anything about care planning, costs, or supports."
    if "home care cost" in q.lower():
        return "Non-medical home care often ranges from $28–$40/hr in most areas. 20 hrs/week ≈ $2,400–$3,200/mo."
    if "va" in q.lower():
        return "Possibly. VA Aid & Attendance or Community Care programs can offset costs if eligibility criteria are met."
    if "next" in q.lower():
        return "Next steps: confirm safety, sketch a weekly schedule, estimate cost, then compare benefits (Medicaid/VA)."
    return "Here’s a general path: assess safety, match setting/supports, plan the budget, and revisit monthly."

if send and prompt.strip():
    thread.append(("user", prompt.strip()))
    thread.append(("assistant", _fake_llm_answer(prompt.strip())))
    st.session_state["ai_input"] = ""

st.divider()
st.markdown("#### Conversation")
for role, msg in thread:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Navi:** {msg}")

if thread:
    last = thread[-1][1]
    st.markdown(f"[📧 Send via SMS](sms:&body={last})")

st.divider()
if st.button("Back to Hub", key="back_ai", use_container_width=True):
    safe_switch("pages/guided_care_hub.py")
