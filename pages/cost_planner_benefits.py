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
st.markdown('</div>', unsafe_allow_html=True)

# Medicaid Spend Down section
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; margin-top: 1rem;">', unsafe_allow_html=True)
st.write("Medicaid Spend Down")
st.write("Current assets: ~ $1.5M (spend down to $2,000 to qualify)")
st.write("Options to spend on care:")
st.button("Home Care Costs", key="spend_home_care", type="primary")
st.button("Medical Equipment", key="spend_equipment", type="primary")
st.button("Home Modifications", key="spend_mods", type="primary")
st.write("Est. time to qualify: 24 months")
st.write("Potential coverage: $8,760/year after spend down")
st.button("Adjust Spend Down Plan", key="adjust_spend_down", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.write("Next: Medicare Gap?")
st.button("Explore", key="medicare_next", type="primary")

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_bc", type="secondary")
with col2:
    st.button("Save & Next", key="next_bc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
