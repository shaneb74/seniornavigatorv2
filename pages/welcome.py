import streamlit as st
from pathlib import Path

# --- tiny helpers ------------------------------------------------------------
def _find_image(base_name_no_ext: str):
    """Return first matching image Path among common folders & extensions or None."""
    exts = [".png", ".jpg", ".jpeg", ".webp"]
    roots = ["static", "static/image", "static/images", "assets"]
    for root in roots:
        for ext in exts:
            p = Path(root) / f"{base_name_no_ext}{ext}"
            if p.exists():
                return p
    return None

def _image_or_note(label: str, base_name_no_ext: str, *, width: int):
    p = _find_image(base_name_no_ext)
    if p and p.exists():
        st.image(str(p), width=width)
    else:
        st.info(f"Add image at **static/** or **assets/** with name `{base_name_no_ext}.png/jpg`.", icon="🖼️")

# --- page-scoped CSS (safe, minimal) ----------------------------------------
st.markdown(
    """
    <style>
    /* keep this lightweight & page-scoped */
    .home-hero { margin-top: .25rem; }
    .home-hero .stImage img { border-radius: 8px; box-shadow: 0 14px 26px rgba(0,0,0,.10); transform: rotate(-2deg); }
    .tile { border: 1px solid rgba(0,0,0,.08); border-radius: 14px; padding: 18px; background: #fff; }
    .tile h4 { margin: 0 0 8px 0; }
    .cta-row { display:flex; gap:12px; align-items:center; }
    .kicker { font-size:.95rem; color:#6b7280; margin-bottom: 6px;}
    .big-title { font-size: 2.2rem; font-weight: 800; line-height: 1.15; letter-spacing: -0.01em; }
    .muted { color:#6b7280; }
    .pro-row { margin-top: 18px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Welcome")
st.caption("A simple starting point for families and professionals.")
st.divider()

# --- HERO --------------------------------------------------------------------
c1, c2 = st.columns([7,5], vertical_alignment="center")
with c1:
    st.markdown('<div class="kicker">Concierge Care • Senior Navigator</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-title">Your compassionate<br/>guide to senior care decisions</div>', unsafe_allow_html=True)
    st.write("Every care decision matters. We’re here to guide you — at no cost — whether planning for yourself or a loved one.")
    cta_l, cta_r = st.columns([1,1])
    with cta_l:
        if st.button("Start Now", type="primary", key="home_start"):
            st.switch_page("pages/welcome.py")  # keep user in prototype; wire wherever you like
    with cta_r:
        if st.button("Log in", key="home_login"):
            st.switch_page("pages/login.py")
with c2:
    st.container(border=False).write("")  # keep layout stable
    _image_or_note("Hero", "Hero", width=520)

st.divider()

# --- HOW WE CAN HELP ---------------------------------------------------------
st.subheader("How we can help you")
lc, rc = st.columns(2)
with lc:
    st.markdown('<div class="tile">', unsafe_allow_html=True)
    _image_or_note("Someone Else", "Someone Else", width=320)
    st.markdown("**I would like to support my loved ones**\n\n<span class='muted'>For someone</span>", unsafe_allow_html=True)
    if st.button("Continue", key="help_someone"):
        st.switch_page("pages/tell_us_about_loved_one.py")
    st.markdown("</div>", unsafe_allow_html=True)

with rc:
    st.markdown('<div class="tile">', unsafe_allow_html=True)
    _image_or_note("Myself", "Myself", width=320)
    st.markdown("**I’m looking for support just for myself**\n\n<span class='muted'>For myself</span>", unsafe_allow_html=True)
    if st.button("Continue", key="help_myself"):
        st.switch_page("pages/tell_us_about_you.py")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="pro-row">', unsafe_allow_html=True)
if st.button("For professionals", key="help_pro"):
    st.switch_page("pages/professional_mode.py")
st.markdown('</div>', unsafe_allow_html=True)