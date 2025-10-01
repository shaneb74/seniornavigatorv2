import streamlit as st

# Age-in-Place Upgrades Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Age-in-Place Upgrades for John")
st.markdown("<h2>Make home safer to stay.</h2>", unsafe_allow_html=True)
st.markdown("<p>Pick upgrades to fit John’s needs.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mockup modification toggles
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left;">', unsafe_allow_html=True)
st.write("Upgrade options for John’s home:")
st.button("Grab bars in bath ($500)", key="grab_bars", type="primary")
st.button("Stair lift ($1,200)", key="stair_lift", type="primary")
st.button("Widened doorways ($1,000)", key="widened_doors", type="primary")
st.button("Smart sensors ($900)", key="smart_sensors", type="primary")
st.write("Total est.: $3,800 - one-time cost")
st.write("Tax credit? Up to $2,000 if eligible")
st.button("Learn More", key="tax_credit", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_mods", type="secondary")
with col2:
    st.button("Save & Next", key="next_mods", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
