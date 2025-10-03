
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Welcome", layout="centered")

# --- Small, local CSS just for this page (doesn't touch your global style.css) ---
WELCOME_CSS = """
<style>
.welcome-super{font-size:.9rem;color:#6b7280;margin-bottom:.25rem;}
.welcome-title{font-size:2.4rem;line-height:1.15;font-weight:800;letter-spacing:-.01em;color:#111827;}
.welcome-sub{max-width:40ch;color:#374151;}
.pro-cta-wrap{display:flex;justify-content:center;margin-top:.75rem;}
/* Image card shadow to match comp */
.welcome-card img{border-radius:8px;box-shadow:0 16px 30px rgba(0,0,0,.08),0 3px 8px rgba(0,0,0,.06);}
/* Tighten container */
.block-container{max-width:1100px !important;}
</style>
"""
st.markdown(WELCOME_CSS, unsafe_allow_html=True)

# ---- Resolve image paths robustly ----
ROOT = Path(__file__).resolve().parents[1]  # project root (same level as app.py)

def find_img(basenames):
    """Return first existing image path from common locations and extensions."""
    if isinstance(basenames, str):
        basenames = [basenames]
    candidates = []
    exts = ["png","jpg","jpeg","webp"]
    folders = [
        ROOT/"static",
        ROOT/"static"/"image",
        ROOT/"static"/"images",
        ROOT/"assets",
        ROOT,  # last resort if user dropped in root
    ]
    for base in basenames:
        stem = Path(base).stem  # e.g., "Hero"
        for f in folders:
            for ext in exts:
                p = f / f"{stem}.{ext}"
                candidates.append(p)
                if p.exists():
                    return p
    return None

HERO_PATH = find_img(["Hero.png", "Hero"])
SOMEONE_PATH = find_img(["Someone Else.png", "SomeoneElse", "Someone"])
MYSELF_PATH = find_img(["Myself.png", "Myself"])

# ---- Header / Hero copy ----
st.markdown(
    """
    <div class="welcome-super">Concierge Care • Senior Navigator</div>
    <h1 class="welcome-title">Your compassionate<br/>guide to senior care decisions</h1>
    <p class="welcome-sub">
      Every care decision matters. We’re here to guide you — at no cost —
      whether planning for yourself or a loved one.
    </p>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1,1], vertical_alignment="center")
with left:
    cc1, cc2 = st.columns([0.55, 0.45])
    with cc1:
        if st.button("Start Now", key="hero_start", type="primary"):
            st.switch_page("pages/welcome.py")  # stays here; user picks below
    with cc2:
        if st.button("Log in", key="hero_login"):
            st.switch_page("pages/login.py")
with right:
    with st.container():  # use_container_width honors page width
        if HERO_PATH and HERO_PATH.exists():
            st.image(str(HERO_PATH), use_container_width=True, output_format="auto")
        else:
            st.info("Hero image not found. Place **Hero.png/jpg** in `static/`, `static/image/`, `static/images/`, or `assets/`.", icon="ℹ️")

st.divider()
st.subheader("How we can help you")

L, R = st.columns(2)
with L:
    with st.container(border=True):
        if SOMEONE_PATH and SOMEONE_PATH.exists():
            st.image(str(SOMEONE_PATH), use_container_width=True, output_format="auto")
        else:
            st.info("Add **Someone Else.png** (or jpg) to `static/`, `static/image/`, `static/images/`, or `assets/`.", icon="ℹ️")
        st.write("**I would like to support my loved ones**")
        st.caption("For someone")
        if st.button("Continue", key="tile_someone"):
            st.switch_page("pages/tell_us_about_loved_one.py")

with R:
    with st.container(border=True):
        if MYSELF_PATH and MYSELF_PATH.exists():
            st.image(str(MYSELF_PATH), use_container_width=True, output_format="auto")
        else:
            st.info("Add **Myself.png** (or jpg) to `static/`, `static/image/`, `static/images/`, or `assets/`.", icon="ℹ️")
        st.write("**I’m looking for support just for myself**")
        st.caption("For myself")
        if st.button("Continue", key="tile_myself"):
            st.switch_page("pages/tell_us_about_you.py")

st.markdown('<div class="pro-cta-wrap">', unsafe_allow_html=True)
if st.button("For professionals", key="pro_cta"):
    st.switch_page("pages/professional_mode.py")
st.markdown('</div>', unsafe_allow_html=True)
