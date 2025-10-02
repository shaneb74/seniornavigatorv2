import streamlit as st

if "care_context" not in st.session_state:
    st.session_state.care_context = {"gcp_answers": {}}
answers = st.session_state.care_context.setdefault("gcp_answers", {})

st.title("Guided Care Plan — Health & Safety")
st.caption("Step 2 of 3")
st.markdown("---")

def idx_or_default(val, options, default=0):
    try:
        return val if isinstance(val, int) and 0 <= val < len(options) else default
    except Exception:
        return default

def set_idx_from_choice(key, choice, options):
    answers[key] = options.index(choice)

opt_cog = ["Sharp", "Sometimes forgetful", "Frequent memory issues", "Serious confusion"]
cog_idx = idx_or_default(answers.get("cognition_level_idx", 0), opt_cog, 0)
cog_choice = st.segmented_control(
    "How would you rate your memory and thinking in daily life?",
    options=opt_cog,
    default=opt_cog[cog_idx],
    label_visibility="visible",
    key="gcp_seg_cognition",
)
set_idx_from_choice("cognition_level_idx", cog_choice, opt_cog)
st.caption("We'll pair this with medications and safety to gauge supervision needs.")

opt_mob = ["I walk easily", "I use a cane", "I use a walker", "I use a wheelchair"]
mob_idx = idx_or_default(answers.get("mobility_idx", 0), opt_mob, 0)
mob_choice = st.segmented_control(
    "How do you usually get around?",
    options=opt_mob,
    default=opt_mob[mob_idx],
    label_visibility="visible",
    key="gcp_seg_mobility",
)
set_idx_from_choice("mobility_idx", mob_choice, opt_mob)
st.caption("We mean typical movement at home and outside.")

opt_home = ["Well-prepared", "Mostly safe", "Needs modifications", "Not suitable"]
home_idx = idx_or_default(answers.get("home_setup_safety_idx", 0), opt_home, 0)
home_choice = st.segmented_control(
    "How safe and manageable is your home for daily living as you age?",
    options=opt_home,
    default=opt_home[home_idx],
    label_visibility="visible",
    key="gcp_seg_home",
)
set_idx_from_choice("home_setup_safety_idx", home_choice, opt_home)
st.caption("Think stairs, bathrooms, lighting, grab bars, and trip hazards.")

opt_fall = ["Yes", "No", "Not sure"]
fall_idx = idx_or_default(answers.get("recent_fall_idx", 1), opt_fall, 1)
fall_choice = st.segmented_control(
    "Has there been a fall in the last 6 months?",
    options=opt_fall,
    default=opt_fall[fall_idx],
    label_visibility="visible",
    key="gcp_seg_fall",
)
set_idx_from_choice("recent_fall_idx", fall_choice, opt_fall)
st.caption("Recent falls increase the need for supervision or home changes.")

st.markdown("<div class='row-actions'><div class='left'>", unsafe_allow_html=True)
if st.button("Back", key="gcp_hs_back"):
    st.switch_page("pages/gcp_daily_life.py")
st.markdown("</div><div class='right'>", unsafe_allow_html=True)
if st.button("Next", key="gcp_hs_next"):
    st.switch_page("pages/gcp_context_prefs.py")
st.markdown("</div></div>", unsafe_allow_html=True)
