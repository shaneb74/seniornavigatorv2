import streamlit as st

from ui.theme import inject_theme

inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: ai_advisor.py')

# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context

# AI Advisor Page
st.markdown(r'''<div class="scn-hero">''', unsafe_allow_html=True)
st.title("AI Advisor")
st.markdown(r'''<h2>I'm Navi-your expert advisor.</h2>''', unsafe_allow_html=True)
st.markdown(r'''<p>I help you see the whole map: care paths, hidden costs, decisions no one talks about. For your loved one.</p>''', unsafe_allow_html=True)
st.markdown(r'''</div>''', unsafe_allow_html=True)

# Frequently Asked Questions Section
st.markdown(r'''<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; margin-bottom: 1.5rem; background: #f9f9f9;">''', unsafe_allow_html=True)
st.markdown("### Top Questions", unsafe_allow_html=True)
st.markdown(r'''<p>Click a question to see the answer below.</p>''', unsafe_allow_html=True)
st.markdown(r'''<div style="display: block;">''', unsafe_allow_html=True)
st.markdown(r'''<a href="#" style="display: block; text-decoration: none; color: #2E6EFF; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 1rem; background: #ffffff;" onmouseover="this.style.textDecoration='underline'; this.style.cursor='pointer';" onmouseout="this.style.textDecoration='none';">How much does home care cost?</a>''', unsafe_allow_html=True)
st.markdown(r'''<a href="#" style="display: block; text-decoration: none; color: #2E6EFF; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 1rem; background: #ffffff;" onmouseover="this.style.textDecoration='underline'; this.style.cursor='pointer';" onmouseout="this.style.textDecoration='none';">Can VA help with costs?</a>''', unsafe_allow_html=True)
st.markdown(r'''<a href="#" style="display: block; text-decoration: none; color: #2E6EFF; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; background: #ffffff;" onmouseover="this.style.textDecoration='underline'; this.style.cursor='pointer';" onmouseout="this.style.textDecoration='none';">What's next after planning?</a>''', unsafe_allow_html=True)
st.markdown(r'''</div>''', unsafe_allow_html=True)
st.markdown(r'''</div>''', unsafe_allow_html=True)

# GPT Chat Interface
st.markdown(r'''<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px; background: #f0f0f0;">''', unsafe_allow_html=True)
st.markdown("### Ask Me Anything", unsafe_allow_html=True)
st.markdown(r'''<p>Type your question about your loved one's care below, or click a question above.</p>''', unsafe_allow_html=True)
st.text_input("Your question...", key="ai_input", placeholder="e.g., How can I afford home care?")
st.button("Send", key="ai_send", type="primary")
st.markdown(r'''<div style="margin-top: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">''', unsafe_allow_html=True)
st.write("**Response:** I'm here to help! Tell me more about your loved one's situation...")
st.markdown(r'''<div style="text-align: right; margin-top: 0.5rem;"><a href="sms:?body=I'm here to help! Tell me more about your loved one's situation..." style="color: #2E6EFF; text-decoration: none; font-size: 14px;" onmouseover="this.style.textDecoration='underline'; this.style.cursor='pointer';" onmouseout="this.style.textDecoration='none';">📧 Send via SMS</a></div>''', unsafe_allow_html=True)
st.markdown(r'''</div>''', unsafe_allow_html=True)
st.markdown(r'''</div>''', unsafe_allow_html=True)

# Navigation
st.markdown(r'''<div class="scn-nav-row">''', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_ai", type="secondary")
st.markdown(r'''</div>''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
