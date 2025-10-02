
import streamlit as st

# Guard session
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'planning_mode': 'estimating',
        'person_name': 'Your Loved One',
        'is_authenticated': False,
        'cost_estimate': {}
    }

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')
auth = ctx.get('is_authenticated', False)
est = ctx.get('cost_estimate', {})

st.title(f"Estimated Costs for {person_name}")
st.caption("A quick monthly estimate based on your selections. For a full plan tailored to your details, continue in the planner.")

# Pull display fields
setting = est.get('setting_label') or est.get('setting') or 'In-home care'
zip_code = est.get('zip', '')
monthly = est.get('estimate_monthly', 5200)
rng = est.get('estimate_range', [int(monthly*0.9), int(monthly*1.15)])

# Context string by scenario
context_bits = []
if setting.lower().startswith('in-home'):
    c = est.get('in_home', {})
    hrs = c.get('hours_per_day')
    dpm = c.get('days_per_month')
    if hrs and dpm:
        context_bits.append(f"{hrs} hrs/day × {dpm} days")
elif setting.lower().startswith('assisted'):
    c = est.get('assisted', {})
    if c.get('room_type'):
        context_bits.append(c['room_type'])
    if c.get('care_level'):
        context_bits.append(f"Care level {c['care_level']}")
elif setting.lower().startswith('memory'):
    c = est.get('memory', {})
    if c.get('room_type'):
        context_bits.append(c['room_type'])
    if c.get('acuity'):
        context_bits.append(f"Acuity {c['acuity']}")

topline = " • ".join(bit for bit in [setting, f"ZIP {zip_code}" if zip_code else None, " • ".join(context_bits) if context_bits else None] if bit)

st.markdown('---')
st.markdown(f"## ${monthly:,}/mo")
low, high = rng[0], rng[1]
st.caption(f"Typical range: ${low:,} – ${high:,}")
if topline:
    st.caption(topline)
st.caption("Local averages, before benefits or insurance.")

# Assumptions block
st.markdown('---')
st.subheader("Assumptions & Notes")
bullets = []

# mobility
for key in ('in_home','assisted','memory'):
    c = est.get(key, {})
    mob = c.get('mobility')
    if mob:
        bullets.append(f"Mobility: {mob}")
        break

# chronic conditions
for key in ('in_home','assisted','memory'):
    c = est.get(key, {})
    ch = c.get('chronic_conditions', [])
    if ch:
        bullets.append("Chronic conditions: " + ", ".join(ch))
        break
if not bullets:
    bullets.append("No specific mobility or chronic conditions provided.")

for b in bullets:
    st.write(f"- {b}")

st.caption("This estimate is a starting point. Benefits, insurance, and detailed planning may reduce costs.")

st.markdown('---')
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Back to Hub', key='sum_back_hub'):
        st.switch_page('pages/hub.py')

with col2:
    if st.button('Open Full Planner', key='sum_open_planner'):
        st.switch_page('pages/cost_planner_modules.py')

with col3:
    # Demo-only login placeholder: set auth True and continue
    if not auth:
        if st.button('Log in to continue', key='sum_login'):
            ctx['is_authenticated'] = True
            st.switch_page('pages/cost_planner_modules.py')
