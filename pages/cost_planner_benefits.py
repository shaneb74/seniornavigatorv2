import streamlit as st

# Benefits Check Detail - Enhanced for amazing look
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Benefits Check for John")
st.markdown("<h2>Unlock potential savings.</h2>", unsafe_allow_html=True)
st.markdown("<p>See what John might qualify for with these simple checks. It could save thousands each year!</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Veteran status section with expander and icons
with st.expander("Veteran Status (WWII Vet John) 💂‍♂️", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.button("Yes - VA Aid & Attendance", key="va_yes", type="primary")
        st.write("Est. aid: $1,500/month")
    with col2:
        st.button("Spouse Qualifies?", key="spouse_check", type="primary")

# Medicaid eligibility section with expander and icons
with st.expander("Medicaid Eligibility 🏥", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.button("Income < $2,829/mo", key="income_check", type="primary")
    with col2:
        st.button("Assets < $2M", key="assets_check", type="primary")
    st.success("You might qualify: ~ $8,760/year")

# Next section with button
st.button("Next: Medicare Gap", key="medicare_gap", type="primary")

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_bc", type="secondary")
with col2:
    st.button("Save & Next", key="next_bc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
