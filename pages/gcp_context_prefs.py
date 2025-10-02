import streamlit as st

if "care_context" not in st.session_state:
    st.session_state.care_context = {"gcp_answers": {}}
answers = st.session_state.care_context.setdefault("gcp_answers", {})

st.title("Guided Care Plan — Context & Preferences")
st.caption("Step 3 of 3")
st.markdown("---")

def idx_or_default(val, options, default=0):
    try:
        return val if isinstance(val, int) and 0 <= val < len(options) else default
    except Exception:
        return default

def set_idx_from_choice(key, choice, options):
    answers[key] = options.index(choice)

opt_fund = ["Very confident", "Somewhat confident", "Somewhat concerned", "Very concerned"]
fund_idx = idx_or_default(answers.get("funding_confidence_idx", 1), opt_fund, 1)
fund_choice = st.segmented_control(
    "How would you describe your financial situation when it comes to paying for care?",
    options=opt_fund,
    default=opt_fund[fund_idx],
    label_visibility="visible",
    key="gcp_seg_funding",
)
set_idx_from_choice("funding_confidence_idx", fund_choice, opt_fund)
st.caption("This helps right-size options for budget.")

opt_geo = ["Very easy", "Fairly easy", "Somewhat difficult", "Very difficult"]
geo_idx = idx_or_default(answers.get("geographic_access_idx", 1), opt_geo, 1)
geo_choice = st.segmented_control(
    "How accessible are services like pharmacies, grocery stores, and doctors from your home?",
    options=opt_geo,
    default=opt_geo[geo_idx],
    label_visibility="visible",
    key="gcp_seg_geo",
)
set_idx_from_choice("geographic_access_idx", geo_choice, opt_geo)
st.caption("Think drive time, transit availability, and speed of getting appointments.")

opts_chronic = ["Diabetes","Hypertension","Dementia","Parkinson's","Stroke","CHF","COPD","Arthritis"]
chronic = st.multiselect(
    "Do you have any ongoing health conditions? Select all that apply.",
    opts_chronic,
    default=answers.get("chronic_conditions_list", []),
    key="gcp_seg_chronic",
)
answers["chronic_conditions_list"] = chronic

opt_move = [
    "I prefer to stay home",
    "I'd rather stay home but open if needed",
    "I'm comfortable either way",
    "I'm comfortable moving",
]
move_idx = idx_or_default(answers.get("move_willingness_idx", 1), opt_move, 1)
move_choice = st.segmented_control(
    "If care is recommended, how open are you to changing where care happens?",
    options=opt_move,
    default=opt_move[move_idx],
    label_visibility="visible",
    key="gcp_seg_move",
)
set_idx_from_choice("move_willingness_idx", move_choice, opt_move)
st.caption("This frames recommendations. It doesn't override safety.")

st.markdown("<div class='row-actions'><div class='left'>", unsafe_allow_html=True)
if st.button("Back", key="gcp_cp_back"):
    st.switch_page("pages/gcp_health_safety.py")
st.markdown("</div><div class='right'>", unsafe_allow_html=True)
if st.button("Get my recommendation", key="gcp_cp_next"):
    st.switch_page("pages/gcp_recommendation.py")
st.markdown("</div></div>", unsafe_allow_html=True)
