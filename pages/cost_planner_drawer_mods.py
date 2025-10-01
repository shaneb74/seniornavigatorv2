import streamlit as st

# Cost Planner: Home Modifications Drawer
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Age-in-Place Upgrades")
st.markdown("<h2>Modify your home for safety.</h2>", unsafe_allow_html=True)
st.markdown("<p>Select options below.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Modification toggles
st.markdown('<div style="display: grid; gap: 1rem;">', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; text-align: center;">', unsafe_allow_html=True)
st.write("Grab bars in bath")
st.button("Add", key="grab_bars", type="primary")
st.write("+$500")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; text-align: center;">', unsafe_allow_html=True)
st.write("Stair lift")
st.button("Add", key="stair_lift", type="primary")
st.write("+$1,200")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; text-align: center;">', unsafe_allow_html=True)
st.write("Widened doorways")
st.button("Add", key="widened_doors", type="primary")
st.write("+$1,000")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; text-align: center;">', unsafe_allow_html=True)
st.write("Smart sensors")
st.button("Add", key="smart_sensors", type="primary")
st.write("+$900")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("$3,800 total - one-time cost")
st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
st.write("Tax credit? Up to $2k if...")
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
