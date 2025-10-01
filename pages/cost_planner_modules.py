import streamlit as st

# Cost Planner: Recommended Modules
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Recommended Cost Modules")
st.markdown("<h2>Adjust your care options.</h2>", unsafe_allow_html=True)
st.markdown("<p>Slide to see costs update instantly.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Module cards with improved mobile spacing
st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; justify-content: center;">', unsafe_allow_html=True)

# Home Care Hours
st.markdown('<div style="flex: 1; min-width: 280px; max-width: 320px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center;">', unsafe_allow_html=True)
st.markdown("### Home Care Hours", unsafe_allow_html=True)
st.write("Weekly hours: 0 to 40")
st.write("~ $1,260/month @ $21/hr")
st.button("Open Slider", key="home_care_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Daily Living Aids
st.markdown('<div style="flex: 1; min-width: 280px; max-width: 320px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center;">', unsafe_allow_html=True)
st.markdown("### Daily Living Aids", unsafe_allow_html=True)
st.write("Support level: Minimal to Full")
st.write("Add-ons: $210")
st.button("Open Toggles", key="daily_aids_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Housing Path
st.markdown('<div style="flex: 1; min-width: 280px; max-width: 320px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center;">', unsafe_allow_html=True)
st.markdown("### Housing Path", unsafe_allow_html=True)
st.write("Keep or sell your home?")
st.button("Open Options", key="housing_path_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Benefits Check
st.markdown('<div style="flex: 1; min-width: 280px; max-width: 320px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center;">', unsafe_allow_html=True)
st.markdown("### Benefits Check", unsafe_allow_html=True)
st.write("Explore veteran or Medicaid options")
st.button("Open Benefits", key="benefits_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Home Modifications
st.markdown('<div style="flex: 1; min-width: 280px; max-width: 320px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center;">', unsafe_allow_html=True)
st.markdown("### Age-in-Place Upgrades", unsafe_allow_html=True)
st.write("Modify home for safety")
st.write("$3,800 total - one-time cost")
st.button("Open Modifications", key="mods_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Mode", key="back_to_mode", type="secondary")
with col2:
    st.button("Next: Expert Review", key="next_review", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
