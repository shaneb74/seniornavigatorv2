import streamlit as st

# Plan for My Advisor - Refined Design with Progress Bar
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Plan for My Advisor")
st.markdown("<h2>Get your ducks in a row for John.</h2>", unsafe_allow_html=True)
st.markdown("<p>Prepare for your concierge call—simple steps to make it smooth.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Progress Bar - Horizontal with Sections
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.5rem; text-align: center; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
st.markdown("### Your Progress")
st.markdown('<div style="height: 20px; background: repeating-linear-gradient(to right, #e0e0e0 0%, #e0e0e0 25%, #e0e0e0 25%, #e0e0e0 50%, #e0e0e0 50%, #e0e0e0 75%, #e0e0e0 75%, #e0e0e0 100%); display: flex; justify-content: space-between;">', unsafe_allow_html=True)
st.markdown('<span style="position: absolute; left: 12.5%; transform: translateX(-50%);">Care Plan</span>', unsafe_allow_html=True)
st.markdown('<span style="position: absolute; left: 37.5%; transform: translateX(-50%);">Cost Plan</span>', unsafe_allow_html=True)
st.markdown('<span style="position: absolute; left: 62.5%; transform: translateX(-50%);">Care Needs</span>', unsafe_allow_html=True)
st.markdown('<span style="position: absolute; left: 87.5%; transform: translateX(-50%);">Benefits</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Care Needs Section
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Care Needs")
st.markdown("<p>Share John’s daily needs to help your advisor.</p>", unsafe_allow_html=True)
marital_status = st.radio("Marital Status", ["Single", "Married", "Widowed"])
living_situation = st.radio("Living Situation", ["Alone", "With Spouse", "With Family"])
smoking = st.radio("Smoking", ["No", "Occasional", "Regular"])
alcohol = st.radio("Alcohol", ["No", "Occasional", "Regular"])
sleep_concerns = st.radio("Sleep Concerns", ["No", "Occasional", "Regular"])
hearing = st.radio("Hearing", ["No", "Mild", "Severe"])
vision = st.radio("Vision", ["No", "Mild", "Severe"])
weight_trend = st.radio("Weight Trend", ["Stable", "Loss", "Gain"])
incontinence = st.radio("Incontinence", ["No", "Occasional", "Regular"])
st.checkbox("This looks right?", key="care_needs_confirm")
st.button("Save Care Needs", key="save_care", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Benefits Section
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px; margin-top: 1.5rem;">', unsafe_allow_html=True)
st.markdown("### Benefits")
st.markdown("<p>Details on insurance and eligibility to unlock savings.</p>", unsafe_allow_html=True)
insurance_company = st.text_input("Insurance Company", value="Blue Cross")
ltc_insurance = st.radio("LTC Insurance", ["Yes", "No", "Unsure"])
medicaid_status = st.radio("Medicaid Status", ["Yes", "In process", "No", "Unsure"])
va_eligibility = st.radio("VA Eligibility", ["Yes", "No", "Unsure"])
st.checkbox("This looks right?", key="benefits_confirm")
st.button("Save Benefits", key="save_benefits", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_pfma", type="secondary")
with col2:
    st.button("Finish Prep", key="finish_pfma", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
