
import streamlit as st

# Cost Planner: Recommended Modules
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Recommended Cost Modules")
st.markdown("<h2>Adjust your care options for your loved one.</h2>", unsafe_allow_html=True)
st.markdown("<p>Each module helps you understand costs and options—no pressure, just clarity.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Tile grid - each self-explanatory with importance content
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; justify-items: center; padding: 1rem;">', unsafe_allow_html=True)

# Home Care Support
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Home Care Support", unsafe_allow_html=True)
st.markdown("<p>Many seniors prefer staying home—home care keeps them safe and independent with help for meds, meals, or companionship. It's essential when daily tasks get harder, allowing your loved one to age in place without major changes.</p>", unsafe_allow_html=True)
if st.button("Explore Home Care", key="explore_home_care", type="primary"):
    st.switch_page("pages/cost_planner_home_care.py")
st.markdown('</div>', unsafe_allow_html=True)

# Daily Living Aids
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Daily Living Aids", unsafe_allow_html=True)
st.markdown("<p>Small tools make big differences—like bath chairs for safety or pill dispensers for routine. For your loved one, these aids prevent falls and ensure meds are taken right, adding comfort without full-time help.</p>", unsafe_allow_html=True)
if st.button("Explore Daily Aids", key="explore_daily_aids", type="primary"):
    st.switch_page("pages/cost_planner_daily_aids.py")
st.markdown('</div>', unsafe_allow_html=True)

# Housing Path
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Housing Path", unsafe_allow_html=True)
st.markdown("<p>Deciding to keep or sell the family home is emotional—factor in mortgage, upkeep, and taxes if staying, or equity from selling for new options like assisted living. Explore how each path affects your loved one's budget and lifestyle.</p>", unsafe_allow_html=True)
if st.button("Explore Housing", key="explore_housing", type="primary"):
    st.switch_page("pages/cost_planner_housing.py")
st.markdown('</div>', unsafe_allow_html=True)

# Benefits Check
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Benefits Check", unsafe_allow_html=True)
st.markdown("<p>Veterans like your loved one may qualify for VA aid, while Medicaid covers long-term care gaps. Unlocking these can save thousands yearly—check eligibility to ease the financial load without cutting corners on care.</p>", unsafe_allow_html=True)
if st.button("Explore Benefits", key="explore_benefits", type="primary"):
    st.switch_page("pages/cost_planner_benefits.py")
st.markdown('</div>', unsafe_allow_html=True)

# Age-in-Place Upgrades
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Age-in-Place Upgrades", unsafe_allow_html=True)
st.markdown("<p>Simple home changes like grab bars or stair lifts help your loved one stay safe longer, avoiding moves to facilities. These one-time investments promote independence and reduce risks like falls in familiar surroundings.</p>", unsafe_allow_html=True)
if st.button("Explore Upgrades", key="explore_upgrades", type="primary"):
    st.switch_page("pages/cost_planner_mods.py")
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
