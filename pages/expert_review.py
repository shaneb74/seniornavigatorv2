
import streamlit as st

# ---------- Session guard ----------
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
auth = ctx.get('is_authenticated', False)
name = ctx.get('person_name', 'Your Loved One')

gcp_done = bool(ctx.get('gcp_recommendation')) or bool(ctx.get('gcp_answers'))
est = ctx.get('cost_estimate', {})
est_done = bool(est.get('completed'))
est_zip_ok = bool(est.get('zip')) and len(str(est.get('zip'))) == 5

mods = ctx.get('module_progress', {})
mods_total = 5 if isinstance(mods, dict) else 0
mods_done = sum(1 for k,v in mods.items() if v) if isinstance(mods, dict) else 0

st.title("Expert Review")
st.caption("A quick double-check to make sure you didn’t miss anything important.")

# Completion strip
st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.write("**Guided Care Plan**")
    st.success("Completed" if gcp_done else "Incomplete", icon="✅" if gcp_done else "⚠️")
with c2:
    st.write("**Quick Estimate**")
    if est_done and est_zip_ok:
        st.success("Completed", icon="✅")
    elif est_done:
        st.warning("ZIP missing", icon="⚠️")
    else:
        st.info("Not started", icon="ℹ️")
with c3:
    st.write("**Modules**")
    st.caption(f"{mods_done} of {mods_total} completed")
with c4:
    st.write("**Account**")
    st.success("Logged in" if auth else "Not logged in", icon="🔒" if auth else "🔓")

st.markdown("---")

# === Focus areas / suggestions ===
st.subheader("Suggestions to review")

suggestions = []

care_flags = ctx.get('care_flags', {})
gcp = ctx.get('gcp_answers', {})

# Safety & Home Setup
home_safety = gcp.get('home_setup_safety') or care_flags.get('home_not_suitable')
recent_fall = gcp.get('recent_fall') == "Yes" or care_flags.get('recent_fall') == True
if home_safety in ("Needs modifications", "Not suitable") or recent_fall:
    suggestions.append({
        "title": "Safety & Home Setup",
        "reason": "Because: home may need modifications or a recent fall was reported.",
        "button": ("Open module", "pages/cost_planner_mods.py")
    })

# Cognition & Meds
cognition = gcp.get('cognition_level')
meds_complexity = gcp.get('meds_complexity')
if cognition in ("Frequent memory issues", "Serious confusion") or meds_complexity in ("Several, harder to manage",):
    suggestions.append({
        "title": "Cognition & Medications",
        "reason": "Because: memory issues and/or medication complexity were noted.",
        "button": ("Open Meds", "pages/medication_management.py")
    })

# Benefits & Offsets
if care_flags.get('is_veteran') or care_flags.get('has_ltc') or care_flags.get('on_medicaid'):
    suggestions.append({
        "title": "Benefits & Coverage",
        "reason": "Because: veteran/LTC/Medicaid indicators may unlock offsets.",
        "button": ("Open Benefits", "pages/cost_planner_benefits.py")
    })

# Housing Decision
reco = ctx.get('gcp_recommendation')
if reco in ("Assisted living", "Memory care") and not mods.get('housing', False):
    suggestions.append({
        "title": "Housing Path",
        "reason": f"Because: recommendation was {reco} but the Housing module isn’t completed.",
        "button": ("Open Housing", "pages/cost_planner_housing.py")
    })

# In-Home Care Load
if (est.get('setting_label') == "In-home care") and not mods.get('home_care', False):
    ih = est.get('in_home', {})
    if not ih.get('hours_per_day') or not ih.get('days_per_month'):
        suggestions.append({
            "title": "Home Care Support",
            "reason": "Because: hours/day or days/month are missing.",
            "button": ("Open Home Care", "pages/cost_planner_home_care.py")
        })

if not suggestions:
    st.success("No issues found. Nice work — your plan looks consistent with your answers.", icon="✅")
else:
    for s in suggestions:
        with st.container(border=True):
            left, mid = st.columns([6,2])
            with left:
                st.write(f"**{s['title']}**")
                st.caption(s["reason"])
            with mid:
                if st.button(s["button"][0], key=f"open_{s['title'].lower().replace(' ','_')}"):
                    st.switch_page(s["button"][1])

st.markdown("---")
st.subheader("What you’ve covered")
covered = []
if gcp_done:
    covered.append("Guided Care Plan")
if est_done:
    setting = est.get('setting_label', 'In-home care')
    monthly = est.get('estimate_monthly', 0)
    zip_code = est.get('zip', '')
    line = f"Quick Estimate • {setting}"
    if monthly:
        line += f" • ${monthly:,}/mo"
    if zip_code:
        line += f" • ZIP {zip_code}"
    covered.append(line)
for key, label in [
    ('home_care','Home Care Support'),
    ('daily_aids','Daily Living Aids'),
    ('housing','Housing Path'),
    ('benefits','Benefits Check'),
    ('mods','Age-in-Place Upgrades'),
]:
    if mods.get(key):
        covered.append(label)

if covered:
    for item in covered:
        st.write(f"✅ {item}")
else:
    st.caption("We’ll list completed items here as you work through them.")

st.markdown("---")
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("Back to Modules", key="rev_back_modules"):
        st.switch_page("pages/cost_planner_modules.py")
with b2:
    if st.button("Proceed to PFMA", key="rev_to_pfma"):
        st.switch_page("pages/pfma.py")
with b3:
    if not auth:
        if st.button("Log in to save", key="rev_login"):
            ctx['is_authenticated'] = True
            st.rerun()
