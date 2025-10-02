import streamlit as st

if "care_context" not in st.session_state:
    st.session_state.care_context = {"gcp_answers": {}}
answers = st.session_state.care_context["gcp_answers"]

st.title("Guided Care Plan — Health & Safety")
st.caption("Step 2 of 3")
st.markdown("---")

opt_cog = ["Sharp", "Sometimes forgetful", "Frequent memory issues", "Serious confusion"]
cog_idx = answers.get("cognition_level_idx", 0)
cog = st.radio(
    "How would you rate your memory and thinking in daily life?",
    opt_cog,
    index=cog_idx if 0 <= cog_idx < len(opt_cog) else 0,
    key="gcp_q_cognition",
)
answers["cognition_level_idx"] = opt_cog.index(cog)
st.caption("We'll pair this with medications and safety to gauge supervision needs.")

opt_mob = ["I walk easily", "I use a cane", "I use a walker", "I use a wheelchair"]
mob_idx = answers.get("mobility_idx", 0)
mob = st.radio(
    "How do you usually get around?",
    opt_mob,
    index=mob_idx if 0 <= mob_idx < len(opt_mob) else 0,
    key="gcp_q_mobility",
)
answers["mobility_idx"] = opt_mob.index(mob)
st.caption("We mean typical movement at home and outside.")

opt_home = ["Well-prepared", "Mostly safe", "Needs modifications", "Not suitable"]
home_idx = answers.get("home_setup_safety_idx", 0)
home = st.radio(
    "How safe and manageable is your home for daily living as you age?",
    opt_home,
    index=home_idx if 0 <= home_idx < len(opt_home) else 0,
    key="gcp_q_home",
)
answers["home_setup_safety_idx"] = opt_home.index(home)
st.caption("Think stairs, bathrooms, lighting, grab bars, and trip hazards.")

opt_fall = ["Yes", "No", "Not sure"]
fall_idx = answers.get("recent_fall_idx", 1)
fall = st.radio(
    "Has there been a fall in the last 6 months?",
    opt_fall,
    index=fall_idx if 0 <= fall_idx < len(opt_fall) else 1,
    key="gcp_q_fall",
)
answers["recent_fall_idx"] = opt_fall.index(fall)
st.caption("Recent falls increase the need for supervision or home changes.")

st.markdown("<div class='row-actions'><div class='left'>", unsafe_allow_html=True)
if st.button("Back", key="gcp_hs_back"):
    st.switch_page("pages/gcp_daily_life.py")
st.markdown("</div><div class='right'>", unsafe_allow_html=True)
if st.button("Next", key="gcp_hs_next"):
    st.switch_page("pages/gcp_context_prefs.py")
st.markdown("</div></div>", unsafe_allow_html=True)
