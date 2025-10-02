import streamlit as st

# Plan for My Advisor - Refined Design
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Plan for My Advisor")
st.markdown("<h2>Get your ducks in a row for John.</h2>", unsafe_allow_html=True)
st.markdown("<p>Prepare for your concierge call—simple steps to make it smooth.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Badge Progress Display - Horizontal
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; text-align: center; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
st.markdown("### Your Progress")
st.markdown('<div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #ccc; border-radius: 8px; padding: 0.5rem 1rem; background: #e0e0e0; display: flex; align-items: center;"><span>Guided Plan</span><span style="margin-left: 0.5rem;">🟢</span></div>', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #ccc; border-radius: 8px; padding: 0.5rem 1rem; background: #e0e0e0; display: flex; align-items: center;"><span>Cost Plan</span><span style="margin-left: 0.5rem;">🟢</span></div>', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #ccc; border-radius: 8px; padding: 0.5rem 1rem; background: #e0e0e0; display: flex; align-items: center;"><span>Care Needs</span><span style="margin-left: 0.5rem;">🟢</span></div>', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #ccc; border-radius: 8px; padding: 0.5rem 1rem; background: #e0e0e0; display: flex; align-items: center;"><span>Benefits</span><span style="margin-left: 0.5rem;">🟢</span></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Care Needs Section
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Care Needs", unsafe_allow_html=True)
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
st.markdown("### Benefits", unsafe_allow_html=True)
st.markdown("<p>Details on insurance and eligibility to unlock savings.</p>", unsafe_allow_html=True)
insurance_company = st.text_input("Insurance Company", value="Blue Cross")
ltc_insurance = st.radio("LTC Insurance", ["Yes", "No", "Unsure"])
medicaid_status = st.radio("Medicaid Status", ["Yes", "In process", "No", "Unsure"])
va_eligibility = st.radio("VA Eligibility", ["Yes", "No", "Unsure"])
st.checkbox("This looks right?", key="benefits_confirm")
st.button("Save Benefits", key="save_benefits", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Personal Info Section
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px; margin-top: 1.5rem;">', unsafe_allow_html=True)
st.markdown("### Personal Info", unsafe_allow_html=True)
st.markdown("<p>Confirm contact details for your advisor.</p>", unsafe_allow_html=True)
confirmed_name = st.text_input("Name", value="John Doe")
confirmed_phone = st.text_input("Phone", value="1234567890")
confirmed_email = st.text_input("Email", value="john@example.com")
confirmed_referral = st.text_input("Referral", value="Friend")
st.checkbox("This looks right?", key="personal_info_confirm")
st.button("Save Personal Info", key="save_personal", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Smart Review Notes Section
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px; margin-top: 1.5rem;">', unsafe_allow_html=True)
st.markdown("### Smart Review Notes", unsafe_allow_html=True)
st.markdown("<p>Notes from AI review—share with advisor.</p>", unsafe_allow_html=True)
st.text_area("Notes", value="John may qualify for VA aid. Check spend down for Medicaid.")
st.checkbox("This looks right?", key="notes_confirm")
st.button("Save Notes", key="save_notes", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_pfma", type="secondary")
with col2:
    st.button("Finish Prep", key="finish_pfma", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
