import streamlit as st

# Guard
if "care_context" not in st.session_state:
    st.session_state.care_context = {"gcp_answers": {}}
answers = st.session_state.care_context.setdefault("gcp_answers", {})

st.title("Guided Care Plan — Daily Life & Support")
st.caption("Step 1 of 3")
st.markdown("---")

# ADL dependency
opt_adl = ["Independent", "Occasional reminders", "Help with some tasks", "Rely on help for most tasks"]
adl_idx = answers.get("adl_dependency_idx", 0)
adl = st.radio(
    "How well can you manage everyday activities like bathing, dressing, or preparing meals on your own?",
    opt_adl,
    index=adl_idx if 0 <= adl_idx < len(opt_adl) else 0,
    key="gcp_q_adl",
)
answers["adl_dependency_idx"] = opt_adl.index(adl)
st.caption("ADLs include bathing, dressing, meals, and chores. This tells us the level of daily support.")

# Caregiver support
opt_support = [
    "I have support most of the time",
    "I have support a few days a week",
    "I have support occasionally",
    "I don’t have regular support",
]
sup_idx = answers.get("caregiver_support_level_idx", 0)
sup = st.radio(
    "How much regular support do you have from a caregiver or family member?",
    opt_support,
    index=sup_idx if 0 <= sup_idx < len(opt_support) else 0,
    key="gcp_q_support",
)
answers["caregiver_support_level_idx"] = opt_support.index(sup)
st.caption("Strong support can offset higher daily needs.")

# Meds complexity
opt_meds = ["None", "A few, easy to manage", "Several, harder to manage", "Not sure"]
med_idx = answers.get("meds_complexity_idx", 0)
med = st.radio(
    "Do you take medications, and how manageable is the routine?",
    opt_meds,
    index=med_idx if 0 <= med_idx < len(opt_meds) else 0,
    key="gcp_q_meds",
)
answers["meds_complexity_idx"] = opt_meds.index(med)
st.caption("This helps us understand missed-med risk when combined with cognition.")

# Social isolation
opt_social = ["Frequent contact", "Occasional contact", "Rarely see others", "Often alone"]
soc_idx = answers.get("social_isolation_idx", 0)
soc = st.radio(
    "How often do you connect with friends, family, or activities?",
    opt_social,
    index=soc_idx if 0 <= soc_idx < len(opt_social) else 0,
    key="gcp_q_social",
)
answers["social_isolation_idx"] = opt_social.index(soc)

# Actions row (works with your CSS if present)
st.markdown("<div class='row-actions'><div class='left'>", unsafe_allow_html=True)
if st.button("Back", key="gcp_dl_back"):
    st.switch_page("pages/gcp.py")
st.markdown("</div><div class='right'>", unsafe_allow_html=True)
if st.button("Next", key="gcp_dl_next"):
    st.switch_page("pages/gcp_health_safety.py")
st.markdown("</div></div>", unsafe_allow_html=True)
