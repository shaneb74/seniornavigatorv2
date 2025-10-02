import streamlit as st
import re

if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'estimating',
        'care_flags': {},
        'person_name': 'Your Loved One',
        'cost_estimate': {}
    }

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')
planning_mode = ctx.get('planning_mode', 'estimating')
cost_state = ctx.setdefault('cost_estimate', {})

st.title(f"Estimate Costs for {person_name}")
st.caption("A quick estimate based on a few selections. You can refine in the full planner later.")

scenario_options = ["In-home care", "Assisted living", "Memory care"]
scenario = cost_state.get('setting_label', scenario_options[0])
scenario = st.selectbox("Care setting", scenario_options, index=scenario_options.index(scenario) if scenario in scenario_options else 0, key="est_scenario")

zip_default = cost_state.get('zip', '')
zip_val = st.text_input("ZIP code", value=zip_default, max_chars=5, key="est_zip")
zip_valid = bool(re.fullmatch(r"\d{5}", zip_val))

st.markdown('---')

mobility_opts = ["None", "Cane", "Walker", "Wheelchair"]
chronic_opts = ["Diabetes","Hypertension","Dementia","Parkinson's","Stroke","CHF","COPD","Arthritis"]

if scenario == "In-home care":
    st.subheader(f"{person_name} — Scenario: In-home care")
    c = cost_state.setdefault('in_home', {})
    hours = st.slider(f"{person_name} • Hours per day", 1, 24, c.get('hours_per_day', 4), key="in_hours")
    days = st.slider(f"{person_name} • Days per month", 1, 31, c.get('days_per_month', 20), key="in_days")
    mobility = st.selectbox(f"{person_name} • Mobility", mobility_opts, index=mobility_opts.index(c.get('mobility', 'None')), key="in_mob")
    chronic = st.multiselect(f"{person_name} • Chronic conditions", chronic_opts, default=c.get('chronic_conditions', []), key="in_chronic")
    c.update({'hours_per_day': hours, 'days_per_month': days, 'mobility': mobility, 'chronic_conditions': chronic})

elif scenario == "Assisted living":
    st.subheader(f"{person_name} — Scenario: Assisted Living")
    c = cost_state.setdefault('assisted', {})
    care_level = st.selectbox(f"{person_name} • Care level", ["Low","Medium","High"], index=["Low","Medium","High"].index(c.get('care_level','Medium')), key="al_level")
    room_type = st.selectbox(f"{person_name} • Room type", ["Studio","1-Bedroom","2-Bedroom","Shared"], index=["Studio","1-Bedroom","2-Bedroom","Shared"].index(c.get('room_type','Studio')), key="al_room")
    mobility = st.selectbox(f"{person_name} • Mobility", mobility_opts, index=mobility_opts.index(c.get('mobility', 'None')), key="al_mob")
    chronic = st.multiselect(f"{person_name} • Chronic conditions", chronic_opts, default=c.get('chronic_conditions', []), key="al_chronic")
    c.update({'care_level': care_level, 'room_type': room_type, 'mobility': mobility, 'chronic_conditions': chronic})

else:
    st.subheader(f"{person_name} — Scenario: Memory Care")
    c = cost_state.setdefault('memory', {})
    acuity = st.selectbox(f"{person_name} • Acuity level", ["Low Acuity","Moderate Acuity","High Acuity"], index=["Low Acuity","Moderate Acuity","High Acuity"].index(c.get('acuity','Moderate Acuity')), key="mc_acuity")
    room_type = st.selectbox(f"{person_name} • Room type", ["Studio","1-Bedroom","2-Bedroom","Shared"], index=["Studio","1-Bedroom","2-Bedroom","Shared"].index(c.get('room_type','Studio')), key="mc_room")
    mobility = st.selectbox(f"{person_name} • Mobility", mobility_opts, index=mobility_opts.index(c.get('mobility', 'None')), key="mc_mob")
    chronic = st.multiselect(f"{person_name} • Chronic conditions", chronic_opts, default=c.get('chronic_conditions', []), key="mc_chronic")
    c.update({'acuity': acuity, 'room_type': room_type, 'mobility': mobility, 'chronic_conditions': chronic})

st.markdown('---')

placeholder_monthly = cost_state.get('estimate_monthly', 5200)
placeholder_low = int(placeholder_monthly * 0.9)
placeholder_high = int(placeholder_monthly * 1.15)

st.caption("Estimated Monthly Cost")
st.markdown(f"# ${placeholder_monthly:,}")
st.caption(f"Typical range: ${placeholder_low:,} – ${placeholder_high:,}")
st.caption("Local average, before benefits or insurance.")

cost_state['setting_label'] = scenario
cost_state['zip'] = zip_val
cost_state['estimate_monthly'] = placeholder_monthly
cost_state['estimate_range'] = [placeholder_low, placeholder_high]
cost_state['completed'] = True

st.markdown('---')
col1, col2 = st.columns(2)

with col1:
    if st.button('Back to Hub', key='est_back_hub'):
        st.switch_page('pages/hub.py')

with col2:
    if planning_mode == 'estimating':
        if st.button('See Summary', key='est_to_summary', disabled=not zip_valid):
            st.switch_page('pages/cost_planner_evaluation.py')
    else:
        if st.button('Continue to Planner', key='est_to_modules', disabled=not zip_valid):
            st.switch_page('pages/cost_planner_modules.py')
