import streamlit as st

# Hub page with cards
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Your Care Planning Hub")
st.markdown("<h2>Choose a tool to start or continue.</h2>", unsafe_allow_html=True)
st.markdown("<p>Recommended path: Guided Care Plan → Cost Planner → Smart Review → Plan for My Advisor.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Cards for tools (simulated with expanders or columns)
st.subheader("Available Tools")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Guided Care Plan**")
    st.write("Answer 12 questions to get a personalized care recommendation.")
    st.button("Start GCP", type="primary")

with col2:
    st.markdown("**Cost Planner**")
    st.write("Estimate costs and explore payment options.")
    st.button("Start Cost Planner", type="primary")

col3, col4 = st.columns(2)
with col3:
    st.markdown("**Smart Review**")
    st.write("Get an expert review of your plan.")
    st.button("Start Smart Review", type="primary")

with col4:
    st.markdown("**Plan for My Advisor**")
    st.write("Book an appointment and prepare data.")
    st.button("Start PFMA", type="primary")

st.markdown("**Exports**")
st.write("Download your plan summary.")
st.button("Go to Exports", type="primary")
