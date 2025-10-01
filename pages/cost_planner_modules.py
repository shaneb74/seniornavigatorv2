import streamlit as st

# Cost Planner: Recommended Modules
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Recommended Cost Modules")
st.markdown("<h2>Adjust your care options for John.</h2>", unsafe_allow_html=True)
st.markdown("<p>Slide or toggle to see costs update—takes just a minute!</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Module cards with realistic content and improved layout
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; justify-items: center; padding: 1rem;">', unsafe_allow_html=True)

# Home Care Hours
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Home Care Hours", unsafe_allow_html=True)
st.write("Support for John: Morning help, evening check-ins")
st.write("Weekly: 0 to 40 hours")
st.write("Est. cost: $1,050 - $1,500/month")
st.button("Open Slider", key="home_care_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Daily Living Aids
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Daily Living Aids", unsafe_allow_html=True)
st.write("For John: Bath chair, pill dispenser")
st.write("Options: Bathing ($150), Meds ($60)")
st.write("Add-ons: $210 total")
st.button("Open Toggles", key="daily_aids_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Housing Path
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Housing Path", unsafe_allow_html=True)
st.write("John’s 2-bed home: Keep or sell?")
st.write("Costs vary: $2,000 - $6,000/mo if kept")
st.button("Open Options", key="housing_path_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Benefits Check
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Benefits Check", unsafe_allow_html=True)
st.write("For WWII vet John: VA or Medicaid?")
st.write("Potential savings: Up to $8,760/year")
st.button("Open Benefits", key="benefits_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Home Modifications
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: center; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Age-in-Place Upgrades", unsafe_allow_html=True)
st.write("For John: Ramps, stair lift")
st.write("Est. cost: $3,000 - $4,500 one-time")
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
