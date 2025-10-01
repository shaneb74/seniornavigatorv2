import streamlit as st

# Cost Planner: Benefits Check Drawer
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Benefits Check")
st.markdown("<h2>Explore your options.</h2>", unsafe_allow_html=True)
st.markdown("<p>See what you might qualify for.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Veteran status
veteran = st.radio("Veteran?", ["Yes", "No"], key="veteran_status")

if veteran == "Yes":
    st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
    st.write("VA Aid & Attendance: $0 - $2,247/mo")
    st.write("~ $1,500/mo")
    st.button("Adjust", key="va_adjust", type="primary")
    st.write("Spouse qualifies?")
    st.button("Check Eligibility", key="spouse_check", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; margin-top: 1rem;">', unsafe_allow_html=True)
st.write("Medicaid Eligibility")
st.write("Under $2,829 income?")
st.button("Yes", key="income_yes", type="primary")
st.write("Under $2M assets?")
st.button("Yes", key="assets_yes", type="primary")
st.write("You might qualify: $8,760/year covered")
st.markdown('</div>', unsafe_allow_html=True)

st.write("Next: Medicare Gap?")
st.button("Explore", key="medicare_gap", type="primary")

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_benefits", type="secondary")
with col2:
    st.button("Save & Next", key="next_benefits", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
