from ui.ux_enhancements import apply_global_ux, render_stepper
import streamlit as st

apply_global_ux()
render_stepper()

st.markdown("""
<div class="scn-hero">
  <h1>AI Advisor</h1>
  <h2>I’m Navi — your expert advisor.</h2>
  <p>I help you see the whole map: care paths, hidden costs, and what to ask providers.
  For your loved one.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; gap:12px; flex-wrap:wrap;">
  <a href="#" style="display:inline-block; padding:10px 14px; border:1px solid #e5e7eb; border-radius:999px; text-decoration:none;">What does home care include?</a>
  <a href="#" style="display:inline-block; padding:10px 14px; border:1px solid #e5e7eb; border-radius:999px; text-decoration:none;">How do we compare assisted living vs memory care?</a>
  <a href="#" style="display:inline-block; padding:10px 14px; border:1px solid #e5e7eb; border-radius:999px; text-decoration:none;">What paperwork do we need?</a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="border: 1px solid #e0e0e0; border-radius: 12px; padding: 16px; background: #fff;">
  <h3>Ask Me Anything</h3>
  <p>Type your question about your loved one’s care below, or click a question above.</p>
</div>
""", unsafe_allow_html=True)

st.text_input("Your question...", key="ai_input", placeholder="e.g., How can I afford home care?")
st.button("Send", key="ai_send", type="primary")

st.markdown("""
<div style="margin-top: 1rem; border: 1px solid #e0e0e0; border-radius: 12px; padding: 16px; background: #fff;">
  <strong>Response:</strong> I’m here to help! Tell me more about your loved one’s situation...
  <div style="text-align: right; margin-top: 0.5rem;">
    <a href="#" style="text-decoration:none;">📧 Send via SMS</a>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""<div class="scn-nav-row"></div>""", unsafe_allow_html=True)
col1, col2 = st.columns([1,1])
with col1:
    if st.button("Back: Hub"):
        st.switch_page('pages/hub.py')
with col2:
    if st.button("Next: Cost Planner"):
        st.switch_page('pages/cost_planner.py')
