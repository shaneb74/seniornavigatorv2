import streamlit as st

# Benefits Check Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Benefits Check for John")
st.markdown("<h2>Unlock potential savings.</h2>", unsafe_allow_html=True)
st.markdown("<p>See what John might qualify for.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mockup benefits options
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left;">', unsafe_allow_html=True)
st.write("Veteran status (WWII vet John):")
st.button("Yes - VA Aid & Attendance", key="va_yes", type="primary")
st.write("Est. aid: $1,500/month")
st.button("Spouse qualifies?", key="spouse_check", type="primary")
st.write("Medicaid eligibility:")
st.button("Income < $2,829/mo", key="income_check", type="primary")
st.button("Assets < $2M", key="assets_check", type="primary")
st.write("You might qualify: ~ $8,760/year")
st.button("Next: Medicare Gap", key="medicare_next", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_bc", type="secondary")
with col2:
    st.button("Save & Next", key="next_bc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
