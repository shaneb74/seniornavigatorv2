import streamlit as st

# ---------- Session guard ----------
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}
ctx = st.session_state.care_context

st.title("Welcome")
st.caption("A simple starting point for families and professionals.")

# Hero image rendered via raw <img> so CSS can size it reliably
st.markdown(
    '''
    <div class="photo-frame tilt-left">
      <img src="static/images/Hero.png" class="hero-img"/>
    </div>
    ''',
    unsafe_allow_html=True,
)

st.markdown("---")

# Choice pills (radio) — use hidden label to avoid accessibility warnings
choice = st.radio(
    "Who are we planning for?",
    ["Myself", "Someone Else", "I'm a professional"],
    index=0,
    horizontal=True,
    label_visibility="collapsed",
    key="welcome_choice",
)

st.markdown("")

if st.button("Continue", key="welcome_continue"):
    # Persist rough audience for later copy
    ctx['audience'] = choice

    if choice == "Myself":
        st.switch_page('pages/tell_us_about_you.py')
    elif choice == "Someone Else":
        st.switch_page('pages/tell_us_about_loved_one.py')
    else:
        # Professional mode requires auth later in flow
        st.switch_page('pages/professional_mode.py')
