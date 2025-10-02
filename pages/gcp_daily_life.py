import streamlit as st

# Guard
if "care_context" not in st.session_state:
    st.session_state.care_context = {"gcp_answers": {}}
answers = st.session_state.care_context.setdefault("gcp_answers", {})

st.title("Guided Care Plan — Daily Life & Support")
st.caption("Step 1 of 3")
st.markdown("---")

def idx_or_default(val, options, default=0):
    try:
        return val if isinstance(val, int) and 0 <= val < len(options) else default
    except Exception:
        return default

def set_idx_from_choice(key, choice, options):
    answers[key] = options.index(choice)

opt_adl = ["Independent", "Occasional reminders", "Help with some tasks", "Rely on help for most tasks"]
adl_idx = idx_or_default(answers.get("adl_dependency_idx", 0), opt_adl, 0)
adl_choice = st.segmented_control(
    "How well can you manage everyday activities like bathing, dressing, or preparing meals on your own?",
    options=opt_adl,
    default=opt_adl[adl_idx],
    label_visibility="visible",
    key="gcp_seg_adl",
)
set_idx_from_choice("adl_dependency_idx", adl_choice, opt_adl)
st.caption("ADLs include bathing, dressing, meals, and chores. This tells us the level of daily support.")

opt_support = [
    "I have support most of the time",
    "I have support a few days a week",
    "I have support occasionally",
    "I don’t have regular support",
]
sup_idx = idx_or_default(answers.get("caregiver_support_level_idx", 0), opt_support, 0)
sup_choice = st.segmented_control(
    "How much regular support do you have from a caregiver or family member?",
    options=opt_support,
    default=opt_support[sup_idx],
    label_visibility="visible",
    key="gcp_seg_support",
)
set_idx_from_choice("caregiver_support_level_idx", sup_choice, opt_support)
st.caption("Strong support can offset higher daily needs.")

opt_meds = ["None", "A few, easy to manage", "Several, harder to manage", "Not sure"]
med_idx = idx_or_default(answers.get("meds_complexity_idx", 0), opt_meds, 0)
med_choice = st.segmented_control(
    "Do you take medications, and how manageable is the routine?",
    options=opt_meds,
    default=opt_meds[med_idx],
    label_visibility="visible",
    key="gcp_seg_meds",
)
set_idx_from_choice("meds_complexity_idx", med_choice, opt_meds)
st.caption("This helps us understand missed‑med risk when combined with cognition.")

opt_social = ["Frequent contact", "Occasional contact", "Rarely see others", "Often alone"]
soc_idx = idx_or_default(answers.get("social_isolation_idx", 0), opt_social, 0)
soc_choice = st.segmented_control(
    "How often do you connect with friends, family, or activities?",
    options=opt_social,
    default=opt_social[soc_idx],
    label_visibility="visible",
    key="gcp_seg_social",
)
set_idx_from_choice("social_isolation_idx", soc_choice, opt_social)

st.markdown("<div class='row-actions'><div class='left'>", unsafe_allow_html=True)
if st.button("Back", key="gcp_dl_back"):
    st.switch_page("pages/gcp.py")
st.markdown("</div><div class='right'>", unsafe_allow_html=True)
if st.button("Next", key="gcp_dl_next"):
    st.switch_page("pages/gcp_health_safety.py")
st.markdown("</div></div>", unsafe_allow_html=True)
