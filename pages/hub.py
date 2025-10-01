import streamlit as st

# Hub page mimicking the dashboard design
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Dashboard")
st.markdown("<h2>For your loved ones</h2>", unsafe_allow_html=True)
st.markdown("<p>Select a person: <select><option>John</option><option>Add +</option></select></p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Assessment section
st.subheader("Assessment")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("For your loved ones")
with col2:
    st.button("Add +", key="add_person", type="secondary")

# Card sections
st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 1rem;">', unsafe_allow_html=True)

# Understand the situation
st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
st.markdown("### Understand the situation")
st.markdown("- 📋 **Guided Care Plan**")
st.write("Recommendation")
st.write("🏠 **In-Home Care**")
st.button("See responses", key="see_responses", type="primary")
st.button("Start over", key="start_over", type="secondary")
st.success("Completed ✓")
st.markdown('</div>', unsafe_allow_html=True)

# Understand the costs
st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
st.markdown("### Understand the costs")
st.markdown("- 💰 **Cost Estimator**")
st.write("Assess the cost structure for various care options for John. The cost estimate will automatically update based on selected choices.")
st.button("Start", key="cost_estimator_start", type="primary")
st.write("Next step ★")
st.markdown('</div>', unsafe_allow_html=True)

# Connect with an advisor
st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
st.markdown("### Connect with an advisor to plan the care")
st.markdown("- 📞 **Get Connected**")
st.write("Whenever you're ready to meet with an advisor.")
st.button("Get connected", key="get_connected", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# FAQs & Answers
st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem; background: #fff5f5;">', unsafe_allow_html=True)
st.markdown("### FAQs & Answers")
st.markdown("- 🤖 **AI Agent**")
st.write("Receive instant, tailored assistance from our advanced AI chat.")
st.button("Open", key="ai_agent_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Start from scratch
st.button("↻ Start from scratch", key="start_from_scratch", type="secondary")
st.write("Chose this option if you would like remove saved progress for John and start fresh.")

# Additional services
st.subheader("Additional services")
col1, col2 = st.columns(2)
with col1:
    st.markdown("- 🤖 **AI Health Check**")
    st.write("Get insights about John overall body health")
    st.button("Open", key="ai_health_open", type="secondary")
with col2:
    st.markdown("- 📚 **Learning Center**")
    st.write("Media Center")
    st.button("Open", key="learning_center_open", type="secondary")
