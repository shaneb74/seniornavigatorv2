# pages/welcome.py
"""Welcome page with hero and entry cards."""

import io
import base64
import mimetypes
from urllib.parse import urlparse
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

# ------------------ Page / session ------------------
st.set_page_config(layout="wide")

if "care_context" not in st.session_state:
    st.session_state.care_context = {}
ctx = st.session_state.care_context

# ------------------ CSS ------------------
st.markdown(
    """
    <style>
      /* Keep layout crisp on large screens */
      .block-container{
        max-width: 1120px;
        margin: 0 auto;
        padding-top: 1.25rem;
        padding-bottom: 3rem;
      }

      /* HERO text */
      .hero-h1{
        font-size: clamp(28px, 4.2vw, 44px);
        line-height: 1.06;
        font-weight: 800;
        letter-spacing: .2px;
        margin: 0 0 .3rem 0;
      }
      .hero-h2{
        font-size: clamp(16px, 1.8vw, 18px);
        color: rgba(0,0,0,0.72);
        font-weight: 500;
        margin: .5rem 0 1.0rem 0;
      }

      /* HERO photo “polaroid” look */
      .hero-photo{
        border-radius: 8px;
        background: #fff;
        box-shadow: 0 10px 20px rgba(0,0,0,.16);
        border: 10px solid #fff;
        transform: rotate(-2deg);
        display: block;
      }

      .divider{ margin: 1.25rem 0 1rem; border: none; border-top: 1px solid rgba(0,0,0,.08); }
      .section-kicker{
        font-size: clamp(18px, 2.2vw, 22px);
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #2a2a2a;
        margin: .25rem 0 1rem 0;
      }

      /* Style Streamlit bordered containers as cards */
      div[data-testid="stVerticalBlockBorderWrapper"]{
        border: 1px solid rgba(0,0,0,.06);
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0,0,0,.08);
      }

      /* Card image: a bit smaller & centered */
      .card-photo{
        width: clamp(280px, 82%, 420px);
        border-radius: 14px;
        box-shadow: 0 6px 16px rgba(0,0,0,.12);
        display: block;
        margin: .35rem auto .8rem;
      }

      /* Safety: hide truly empty markdown containers */
      div[data-testid="stMarkdownContainer"]:empty{ display:none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ Image helpers (robust + cached) ------------------
def _resolve_path(path_str: str) -> Path:
    """
    Resolve a relative asset path robustly:
    - absolute path -> return as-is
    - relative -> try alongside this file, then repo root
    """
    p = Path(path_str)
    if p.is_absolute() or p.exists():
        return p
    here = Path(__file__).resolve().parent
    cand = here / path_str
    if cand.exists():
        return cand
    # try project root (/mount/src/<repo>/)
    root = here.parents[1] if len(here.parents) > 1 else here.parent
    return root / path_str

@st.cache_data(show_spinner=False)
def load_bytes(path_str: str) -> bytes | None:
    """Read local file bytes or fetch remote, validate with PIL, and cache."""
    try:
        parsed = urlparse(path_str)
        if parsed.scheme in ("http", "https"):
            import urllib.request
            with urllib.request.urlopen(path_str, timeout=10) as r:
                data = r.read()
        else:
            p = _resolve_path(path_str)
            if not p.exists():
                st.info(f"Add image at {path_str} (resolved → {p})")
                return None
            data = p.read_bytes()
        # validate image
        Image.open(io.BytesIO(data)).verify()
        return data
    except UnidentifiedImageError:
        st.warning("Image exists but isn’t valid. Use PNG/JPG/WEBP.")
    except Exception as e:
        st.warning(f"Couldn't load image: {e}")
    return None

def data_uri(path_str: str) -> str | None:
    """Return a data: URI for the image (base64) or None if missing/invalid."""
    b = load_bytes(path_str)
    if not b:
        return None
    ext = Path(urlparse(path_str).path).suffix.lower()
    mime = mimetypes.types_map.get(ext, "image/png")
    return f"data:{mime};base64,{base64.b64encode(b).decode('ascii')}"

def img_html(path_str: str, cls: str = "", style: str = "", alt: str = "") -> str | None:
    """Single <img> tag with base64 data (prevents URL/path issues)."""
    uri = data_uri(path_str)
    if not uri:
        return None
    cls_attr = f' class="{cls}"' if cls else ""
    style_attr = f' style="{style}"' if style else ""
    alt_attr = f' alt="{alt}"' if alt else ' alt=""'
    return f'<img src="{uri}"{cls_attr}{style_attr}{alt_attr}>'

# =====================================================================
# HERO — text on the left, image on the right; CTAs inside the left col
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
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Start Now", key="hero_start"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    with c2:
        if st.button("Log in", key="hero_login"):
            st.switch_page("pages/login.py")

with right:
    hero_tag = img_html(
        "static/images/Hero.png",
        cls="hero-photo",
        style="width:min(420px, 100%);",  # responsive and a touch smaller
        alt="Caregiver smiling with older adult",
    )
    if hero_tag:
        st.markdown(
            """
            <div style="background: radial-gradient(120% 120% at 80% 10%, #eef2ff 0%, #ffffff 60%);
                        padding: 18px; border-radius: 18px;">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(hero_tag, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">How we can help you</div>', unsafe_allow_html=True)

# =====================================================================
# CARDS — each card is a bordered Streamlit container (CTA inside)
# =====================================================================
def card(image_path: str, title: str, sub: str, button_label: str, page_to: str) -> None:
    with st.container(border=True):
        tag = img_html(image_path, cls="card-photo", alt=title)
        if tag:
            st.markdown(
                f"""
                <div style="display:flex; flex-direction:column; align-items:center;">
                  <div style="position:relative; display:inline-block;">
                    <div style="position:absolute; inset:0; border-radius:14px;
                                background: linear-gradient(180deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0) 60%);"></div>
                    {tag}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
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
