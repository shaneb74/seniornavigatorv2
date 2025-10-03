
import streamlit as st
from pathlib import Path

def inject_css():
    css = Path("static/style.css")
    if css.exists():
        st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)
inject_css()

if "care_context" not in st.session_state:
    st.session_state.care_context = {"person_name":"Your Loved One"}

st.markdown('<div class="h-eyebrow">Concierge Care • Senior Navigator</div>', unsafe_allow_html=True)
st.markdown('<div class="h-display">Your compassionate<br/>guide to senior care decisions</div>', unsafe_allow_html=True)
st.markdown('<div class="h-sub">Every care decision matters. We’re here to guide you — at no cost — whether planning for yourself or a loved one.</div>', unsafe_allow_html=True)

c1, c2 = st.columns([0.23,0.18])
with c1:
    if st.button("Start Now", key="start_now"):
        st.switch_page("pages/tell_us_about_loved_one.py")
with c2:
    if st.button("Log in", key="login_btn"):
        st.switch_page("pages/login.py")

st.markdown("---")

hero_path = Path("static/images/Hero.png")
if hero_path.exists():
    html = '''
    <div class="hero">
      <div></div>
      <div class="hero-figure"><img src="static/images/Hero.png" alt="Hero"></div>
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)

st.markdown("### How we can help you")
st.markdown('<div class="cards">', unsafe_allow_html=True)

# Card 1
st.markdown('<div class="card">', unsafe_allow_html=True)
if Path("static/images/Someone Else.png").exists():
    st.image("static/images/Someone Else.png", use_container_width=True)
st.markdown('<div class="card-inner">', unsafe_allow_html=True)
st.markdown("#### I would like to support my loved ones")
st.caption("Simple guidance that saves time and reduces stress.")
colA, colB = st.columns([0.5,0.5])
with colA:
    st.markdown('<span class="pill">For someone</span>', unsafe_allow_html=True)
with colB:
    if st.button("Choose", key="card_someone"):
        st.switch_page("pages/tell_us_about_loved_one.py")
st.markdown('</div></div>', unsafe_allow_html=True)

# Card 2
st.markdown('<div class="card">', unsafe_allow_html=True)
if Path("static/images/Myself.png").exists():
    st.image("static/images/Myself.png", use_container_width=True)
st.markdown('<div class="card-inner">', unsafe_allow_html=True)
st.markdown("#### I’m looking for support just for myself")
st.caption("Start private, personalized planning right away.")
colC, colD = st.columns([0.5,0.5])
with colC:
    st.markdown('<span class="pill">For myself</span>', unsafe_allow_html=True)
with colD:
    if st.button("Choose", key="card_myself"):
        st.switch_page("pages/tell_us_about_you.py")
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
