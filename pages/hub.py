import streamlit as st

# Hub page mimicking the dashboard design
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Your Care Hub")
st.markdown("<h2>Start or pick up where you left off.</h2>", unsafe_allow_html=True)
st.markdown("<p>Explore tools tailored for John’s needs.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Assessment section with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 150px;">', unsafe_allow_html=True)
st.markdown("### Assessment")
st.markdown("<p>For John—let’s build his plan step by step.</p>", unsafe_allow_html=True)
st.button("Start Assessment", key="start_assess", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Card sections with uniform tile design
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; justify-items: center; padding: 1rem;">', unsafe_allow_html=True)

# Guided Care Plan
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Guided Care Plan", unsafe_allow_html=True)
st.markdown("<p>Answer 12 questions to find John’s best care fit—simple and clear.</p>", unsafe_allow_html=True)
st.button("Start Plan", key="start_gcp", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Cost Planner
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Cost Planner", unsafe_allow_html=True)
st.markdown("<p>Explore costs and plan John’s budget with ease—step-by-step or freeform.</p>", unsafe_allow_html=True)
st.button("Start Planner", key="start_cost", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Plan for My Advisor
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Plan for My Advisor", unsafe_allow_html=True)
st.markdown("<p>Book an expert to guide John’s next steps—ready when you are.</p>", unsafe_allow_html=True)
st.button("Get Connected", key="start_pfma", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Additional options
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 150px; margin-top: 1.5rem;">', unsafe_allow_html=True)
st.markdown("### Exports")
st.markdown("<p>Download John’s plan summary—PDF or CSV.</p>", unsafe_allow_html=True)
st.button("View Exports", key="view_exports", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
