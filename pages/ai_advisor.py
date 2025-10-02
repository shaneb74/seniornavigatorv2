import streamlit as st

# AI Advisor Page
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("AI Advisor")
st.markdown("<h2>Hey—I'm here for you and John.</h2>", unsafe_allow_html=True)
st.markdown("<p>Ask anything about care, costs, or next steps. I’ll keep it simple and on track.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Frequently Asked Questions Section
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
st.markdown("### Top Questions", unsafe_allow_html=True)
st.markdown("<p>Quick answers to common queries.</p>", unsafe_allow_html=True)
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; text-align: left;">', unsafe_allow_html=True)
st.write("**How much does home care cost?**")
st.write("Depends on hours—typically $20-$25/hour. Let’s check John’s needs!")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; text-align: left;">', unsafe_allow_html=True)
st.write("**Can VA help with costs?**")
st.write("If John served, yes—up to $2,247/month. We can explore that.")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; text-align: left;">', unsafe_allow_html=True)
st.write("**What’s next after planning?**")
st.write("Book an advisor call—takes 2 min to set up!")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# GPT Chat Interface
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Ask Me Anything", unsafe_allow_html=True)
st.markdown("<p>Type your question about John’s care below.</p>", unsafe_allow_html=True)
st.text_input("Your question...", key="ai_input", placeholder="e.g., How can I afford home care?")
st.button("Send", key="ai_send", type="primary")
st.markdown('<div style="margin-top: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; background: #f9f9f9;">', unsafe_allow_html=True)
st.write("**Response:** I’m here to help! Tell me more about John’s situation...")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_ai", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
