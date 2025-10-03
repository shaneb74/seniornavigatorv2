import streamlit as st
from pathlib import Path

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "care_context" not in st.session_state:
    st.session_state.care_context = {"person_name": "Your Loved One"}

st.markdown("""
<style>
.block-container { max-width: 1100px; }
.hero h1 { font-size: 42px; line-height: 1.15; margin: 0 0 .4rem 0; }
.hero .eyebrow { text-transform: uppercase; letter-spacing: .12em; font-weight: 700; font-size: 13px; color: #6b7280; }
.hero .sub { color: #4b5563; max-width: 42ch; }
.card { border: 1px solid #e5e7eb; border-radius: 14px; padding: 18px; }
.card h3 { margin: 6px 0 2px 0; }
.card p  { color: #4b5563; margin: 0 0 12px 0; }
.card .cta { display: flex; justify-content: flex-end; }
.stButton>button { border-radius: 10px; padding: .55rem 1rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

def _img(path: str) -> str | None:
    for p in (Path("static/img")/path, Path(path)):
        if p.exists():
            return str(p)
    return None

HERO = _img("Hero.png")
IMG_SOMEONE = _img("Someone Else.png")
IMG_MYSELF = _img("Myself.png")

left, right = st.columns([5,7], vertical_alignment="center")
with left:
    st.markdown('<div class="hero eyebrow">Concierge Care • Senior Navigator</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero"><h1>Your compassionate guide to senior care decisions</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="hero sub">Every care decision matters. We’re here to guide you — at no cost — whether planning for yourself or a loved one.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("Start Now", key="welcome_start", type="primary"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    with c2:
        if st.button("Log in", key="welcome_login"):
            login_path = Path("pages/login.py")
            if login_path.exists():
                st.switch_page("pages/login.py")
            else:
                st.session_state.is_authenticated = True
                st.rerun()

with right:
    if HERO:
        st.image(HERO, use_column_width=True)
    else:
        st.info("Add **Hero.png** to `static/img/` (or project root) to show the hero image.")

st.markdown("---")

st.subheader("How we can help you")

colA, colB = st.columns(2)

with colA:
    with st.container(border=False):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if IMG_SOMEONE:
            st.image(IMG_SOMEONE, use_column_width=True)
        st.markdown("### I would like to support my loved ones")
        st.markdown("We’ll guide you step-by-step so you can feel confident you’re doing the right things.")
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("For someone", key="cta_for_someone"):
            st.switch_page("pages/tell_us_about_loved_one.py")
        st.markdown('</div></div>', unsafe_allow_html=True)

with colB:
    with st.container(border=False):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if IMG_MYSELF:
            st.image(IMG_MYSELF, use_column_width=True)
        st.markdown("### I’m looking for support just for myself")
        st.markdown("Quickly explore options and costs, then build a plan that fits your goals.")
        st.markdown('<div class="cta">', unsafe_allow_html=True)
        if st.button("For myself", key="cta_for_myself"):
            st.switch_page("pages/tell_us_about_you.py")
        st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("---")
c3, c4 = st.columns([3,1])
with c3:
    st.caption("Already started a plan?")
with c4:
    if st.button("Open Care Hub", key="open_hub_quick"):
        st.switch_page("pages/hub.py")
