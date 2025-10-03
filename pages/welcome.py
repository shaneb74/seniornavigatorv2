# pages/welcome.py
import io
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

# ------------------ Page / session ------------------
st.set_page_config(layout="wide")

if "care_context" not in st.session_state:
    st.session_state.care_context = {}
ctx = st.session_state.care_context

st.title("Welcome")
st.caption("A simple starting point for families and professionals.")

# ------------------ CSS ------------------
st.markdown(
    """
    <style>
      .block-container { padding-top: 1.25rem; padding-bottom: 3rem; }

      /* HERO text */
      .hero-h1 {
        font-size: clamp(28px, 4.2vw, 44px);
        line-height: 1.06;
        font-weight: 800;
        letter-spacing: .2px;
        margin: 0 0 .3rem 0;
      }
      .hero-h2 {
        font-size: clamp(16px, 1.8vw, 18px);
        color: rgba(0,0,0,0.72);
        font-weight: 500;
        margin: .5rem 0 1.0rem 0;
      }

      /* HERO photo “polaroid” look */
      .hero-photo {
        border-radius: 8px;
        background: #fff;
        box-shadow: 0 12px 22px rgba(0,0,0,.18);
        border: 10px solid #fff;
        transform: rotate(-3deg);
        display: block;
      }

      .divider { margin: 1.5rem 0 1.25rem 0; border: none; border-top: 1px solid rgba(0,0,0,.08); }
      .section-kicker {
        font-size: clamp(18px, 2.2vw, 22px);
        font-weight: 800;
        letter-spacing: .10em;
        text-transform: uppercase;
        color: #2a2a2a;
        margin: .25rem 0 1rem 0;
      }

      /* Style Streamlit bordered containers as cards */
      div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(0,0,0,.06);
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,.08);
      }
      /* Ensure inner content has breathing room */
      div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlockBorderWrapper"]) {
        padding: 0 !important;
      }

      /* Card photo polish */
      .card-photo img {
        width: 100%;
        border-radius: 14px;
        box-shadow: 0 6px 16px rgba(0,0,0,.12);
        display: block;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ Image loader (reliable on Cloud) ------------------
def load_bytes(path_str: str) -> bytes | None:
    """
    Read image as bytes and validate with PIL.
    """
    p = Path(path_str)
    if not p.exists():
        st.info(f"Add image at {path_str}")
        return None
    try:
        data = p.read_bytes()
        Image.open(io.BytesIO(data)).verify()
        return data
    except UnidentifiedImageError:
        st.warning(f"{p.name} exists but isn't a valid image file. Use PNG/JPG/WEBP.")
    except Exception as e:
        st.warning(f"Couldn't load {p.name}: {e}")
    return None

# =====================================================================
# HERO — text on the left, image on the right (all inside one row)
# =====================================================================
left, right = st.columns([7, 5], gap="large")

with left:
    st.markdown(
        """
        <div class="hero-h1">YOUR COMPASSIONATE<br>GUIDE TO SENIOR<br>CARE DECISIONS</div>
        <div class="hero-h2">
          Every care decision matters. We’re here to guide you — at no cost —
          whether planning for yourself or a loved one.
        </div>
        """,
        unsafe_allow_html=True,
    )
    # CTAs INSIDE the hero (left) column
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Start Now", key="hero_start"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    with c2:
        if st.button("Log in", key="hero_login"):
            st.switch_page("pages/login.py")

with right:
    hero_b = load_bytes("static/images/Hero.png")
    if hero_b:
        # Use markdown to apply the polaroid class; explicit width prevents tiny image
        st.markdown(
            f'<img class="hero-photo" src="data:image/png;base64,{Image.open(io.BytesIO(hero_b))._repr_png_().decode() if hasattr(Image.open(io.BytesIO(hero_b)), "_repr_png_") else ""}" style="width:420px;">',
            unsafe_allow_html=True,
        )
        # Fallback if PIL object doesn't expose _repr_png_, just use st.image
        if not hero_b:
            st.image(hero_b, width=420)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">How we can help you</div>', unsafe_allow_html=True)

# =====================================================================
# CARDS — each card is a real Streamlit bordered container
# =====================================================================
def card(image_path: str, title: str, sub: str, button_label: str, page_to: str) -> None:
    with st.container(border=True):
        # Image first
        b = load_bytes(image_path)
        if b:
            # Render image and give it a class so it gets rounded/shadowed
            st.markdown('<div class="card-photo">', unsafe_allow_html=True)
            st.image(b, width="stretch")  # fills the card width
            st.markdown('</div>', unsafe_allow_html=True)

        # Text + CTA inside the same container (so the button is inside the card)
        st.markdown(f"**{title}**")
        st.caption(sub)
        _, right_btn = st.columns([1, 1])
        with right_btn:
            if st.button(button_label, key=f"btn_{page_to}"):
                st.switch_page(page_to)

col1, col2 = st.columns(2, gap="large")
with col1:
    card(
        "static/images/Someone-Else.png",
        "I would like to support my loved ones",
        "For someone",
        "For someone",
        "pages/tell_us_about_loved_one.py",
    )
with col2:
    card(
        "static/images/Myself.png",
        "I’m looking for support just for myself",
        "For myself",
        "For myself",
        "pages/tell_us_about_you.py",
    )
