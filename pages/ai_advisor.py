import streamlit as st

# AI Advisor Page
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("AI Advisor")
st.markdown("<h2>I'm your care coach—here for you and John.</h2>", unsafe_allow_html=True)
st.markdown("<p>No judgment, just clear answers about care, costs, or next steps.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Frequently Asked Questions Section
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; margin-bottom: 1.5rem; background: #f9f9f9;">', unsafe_allow_html=True)
st.markdown("### Top Questions", unsafe_allow_html=True)
st.markdown("<p>Click a question to see the answer below.</p>", unsafe_allow_html=True)
st.markdown('<div style="display: block;">', unsafe_allow_html=True)
st.markdown('<a href="#" style="display: block; text-decoration: none; color: #2E6EFF; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 1rem; background: #ffffff;" onmouseover="this.style.textDecoration=\'underline\'; this.style.cursor=\'pointer\';" onmouseout="this.style.textDecoration=\'none\';">How much does home care cost?</a>', unsafe_allow_html=True)
st.markdown('<a href="#" style="display: block; text-decoration: none; color: #2E6EFF; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 1rem; background: #ffffff;" onmouseover="this.style.textDecoration=\'underline\'; this.style.cursor=\'pointer\';" onmouseout="this.style.textDecoration=\'none\';">Can VA help with costs?</a>', unsafe_allow_html=True)
st.markdown('<a href="#" style="display: block; text-decoration: none; color: #2E6EFF; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; background: #ffffff;" onmouseover="this.style.textDecoration=\'underline\'; this.style.cursor=\'pointer\';" onmouseout="this.style.textDecoration=\'none\';">What’s next after planning?</a>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# GPT Chat Interface
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px; background: #f0f0f0;">', unsafe_allow_html=True)
st.markdown("### Ask Me Anything", unsafe_allow_html=True)
st.markdown("<p>Type your question about John’s care below, or click a question above.</p>", unsafe_allow_html=True)
st.text_input("Your question...", key="ai_input", placeholder="e.g., How can I afford home care?")
st.button("Send", key="ai_send", type="primary")
st.markdown('<div style="margin-top: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; background: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.write("**Response:** I’m here to help! Tell me more about John’s situation...")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_ai", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
