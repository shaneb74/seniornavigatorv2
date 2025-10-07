from __future__ import annotations

import streamlit as st

from ui.theme import inject_theme

inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# pages/welcome.py
"""Welcome page with hero and two entry cards (safe, self-contained)."""

import io
import base64
import mimetypes
from urllib.parse import urlparse
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

# --- Safe image utilities (local-only, silent fallback) ---
def _resolve_local(path_str: str) -> Path:
    p = Path(path_str)
    if p.is_absolute():
        return p
    here = Path(__file__).resolve().parent
    cand = (here / path_str).resolve()
    if cand.exists():
        return cand
    root = here.parents[1] if len(here.parents) > 1 else here.parent
    return (root / path_str).resolve()


def safe_image(path_str: str) -> Image.Image | None:
    try:
        p = _resolve_local(path_str)
        if not p.exists():
            return None
        return Image.open(p)
    except Exception:
        return None

# ------------------ Page / session ------------------
# (moved to app.py) st.set_page_config(...)
# Minimal, safe session scaffolding so this page never dies
if "care_context" not in st.session_state:
    st.session_state.care_context = {"person_name": "Your Loved One"}
if "aud" not in st.session_state:
    st.session_state.aud = {
        "entry": "proxy",                # "proxy" | "self" | "pro"
        "recipient_name": None,
        "proxy_name": None,
        "qualifiers": {},
    }

# convenience aliases used later
care_context = st.session_state.care_context
aud = st.session_state.aud

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

      /* HERO photo "polaroid" look */
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

      /* Helper note (more prominent and aligned to CTA cards) */
      .sn-helper-note{
        margin-top: 1.2rem;
        text-align: center;
        font-size: 1.05rem;
        font-weight: 500;
        color: #0B5CD8; /* brand blue to link visually with buttons */
        background: rgba(11,92,216,0.06);
        padding: 0.75rem 1rem;
        border-radius: 10px;
        display: inline-block;
        max-width: 560px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
      }

      /* ===== Review Card (pairs visually with .sn-bbb) ===== */
      .sn-row-badges {
        display:flex; gap:14px; align-items:center; flex-wrap:wrap; margin: 4px 0 22px 0;
      }
      .sn-bbb{
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        background:#fff;
        border:1px solid rgba(2,6,23,.06);
        border-radius:14px; padding:12px 14px;
        box-shadow:0 8px 24px rgba(0,0,0,.04);
        min-width:140px;
      }
      .sn-bbb img{max-width:120px; height:auto;}
      .sn-bbb .meta{margin-top:6px; font-size:.85rem; color:#334155; font-weight:600;}
      .sn-review {
        display:flex; gap:12px; align-items:flex-start;
        background:#fff;
        border:1px solid rgba(2,6,23,.06);
        border-radius:14px; padding:12px 14px;
        box-shadow:0 8px 24px rgba(0,0,0,.06);
        max-width:780px;
      }
      .sn-review .avatar {
        flex:0 0 auto; width:40px; height:40px; border-radius:999px; overflow:hidden;
        background:#EEF2FF; display:flex; align-items:center; justify-content:center;
        font-weight:700; color:#0B5CD8; border:1px solid rgba(2,6,23,.06);
      }
      .sn-review .body { flex:1 1 auto; }
      .sn-review .meta {
        display:flex; align-items:center; gap:8px; margin-bottom:4px;
        font-size:.92rem; color:#334155; font-weight:600;
      }
      .sn-review .stars { display:inline-flex; gap:2px; line-height:0; color:#F59E0B; }
      .sn-review .source { font-size:.82rem; color:#64748B; font-weight:500; }
      .sn-review .quote { font-size:.95rem; color:#1F2937; }
      .sn-review .quote em { color:#0B5CD8; font-style:normal; font-weight:700; }

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
        st.warning("Image exists but isn't valid. Use PNG/JPG/WEBP.")
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

# ------------------ Navigation helper ------------------
def safe_switch_page(target: str, query_key: str | None = None, query_value: str | None = None) -> None:
    """
    Try to navigate to a page path. If st.switch_page isn't available,
    optionally set a query param and rerun as a no-op.
    """
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        if query_key and query_value:
            st.query_params[query_key] = query_value
        st.rerun()

# =====================================================================
# HERO - text on the left, image on the right; CTAs inside the left col
# =====================================================================
left, right = st.columns([7, 5], gap="large")

with left:
    st.markdown(
        """
        <div class="hero-h1">Concierge Care · Senior Navigator</div>
        <div class="hero-h2">
          Expert Advisors. No cost ever. Highest customer service in the industry.
          Concierge service with face-to-face planning from a real person.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="
          display:flex; gap:10px; flex-wrap:wrap; margin: 4px 0 18px 0;
          font-weight:600; font-size:14px;
        ">
          <span style="background:#eef4ff;border:1px solid #cfe0ff;border-radius:999px;padding:6px 10px;">
            Expert advice, personalized to you
          </span>
          <span style="background:#eef4ff;border:1px solid #cfe0ff;border-radius:999px;padding:6px 10px;">
            No cost, ever
          </span>
          <span style="background:#eef4ff;border:1px solid #cfe0ff;border-radius:999px;padding:6px 10px;">
            Concierge, white-glove support
          </span>
          <span style="background:#eef4ff;border:1px solid #cfe0ff;border-radius:999px;padding:6px 10px;">
            Real human guidance
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Start Now", key="hero_start"):
            safe_switch_page("pages/SeniorNav_welcome_someone_else.py")
    with c2:
        if st.button("Log in", key="hero_login"):
            safe_switch_page("pages/SeniorNav_login.py", "view", "login")

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
st.markdown(
    """
    <div role="note" aria-label="Track record"
         style="margin: 6px 0 18px 0; padding: 12px 14px;
                background:#f7fafc; border:1px solid #e6edf7; border-radius:12px;">
      <strong>Best in the industry:</strong> Over <strong>20,000</strong> families served ·
      <strong>15 years</strong> of excellence
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="section-kicker">How we can help you</div>', unsafe_allow_html=True)

# =====================================================================
# CARDS - each card is a bordered Streamlit container (CTA inside)
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
                safe_switch_page(page_to, "view", "open")

# ---------- Two-card row ----------
col1, col2 = st.columns(2, gap="large")

with col1:
    card(
        "static/images/Someone-Else.png",
        "I would like to support my loved ones",
        "For someone",
        "For someone",
        "pages/SeniorNav_welcome_someone_else.py",
    )

with col2:
    # Restored bottom-right image card
    # If your asset uses a different filename (e.g., "Yourself.png"), change the path.
    card(
        "static/images/Self.png",
        "I would like to plan for myself",
        "For myself",
        "For me",
        "pages/SeniorNav_welcome_self.py",
    )

helper_note = (
    "Supporting more than one person? No problem — "
    "you can easily add another loved one later in your Cost Planner or Care Hub."
)
st.markdown(f'<div class="sn-helper-note">{helper_note}</div>', unsafe_allow_html=True)

bbb = img_html(
    "static/images/better-business-bureau-logo.png",
    cls="",
    style="max-width:120px;height:auto;",
    alt="Better Business Bureau A+ Rating badge",
)
fallback_bbb = (
    '<div role="img" aria-label="Better Business Bureau: A+ Rating" '
    'style="display:flex;flex-direction:column;align-items:center;gap:4px;">'
    '<div style="font-weight:800;font-size:18px;letter-spacing:.2px;">BBB</div>'
    '<div style="font-size:14px;color:#334155;">A+ Rating</div>'
    "</div>"
)

avatar_img = img_html(
    "static/images/reviewer-teresa.png",
    cls="",
    style="width:100%;height:100%;object-fit:cover;",
    alt="Reviewer Teresa smiling",
)
avatar_html = (
    f'<div class="avatar">{avatar_img}</div>'
    if avatar_img
    else '<div class="avatar" aria-hidden="true">T</div>'
)

STAR = (
    '<svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor" '
    'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.802 2.036a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.802-2.036a1 1 0 00-1.175 0l-2.802 2.036c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.88 8.72c-.783-.57-.38-1.81.588-1.81H6.93a1 1 0 00.95-.69l1.169-3.292z"/>'
    "</svg>"
)
stars_html = f'<span class="stars" aria-label="5 out of 5 stars">{STAR * 5}</span>'

st.markdown(
    f"""
    <div class="sn-row-badges">
      <div class="sn-bbb">
        {bbb or fallback_bbb}
        <div class="meta">A+ Rating</div>
      </div>

      <div class="sn-review" role="figure" aria-label="Customer review">
        {avatar_html}
        <div class="body">
          <div class="meta">
            {stars_html}
            <span>5.0</span>
            <span class="source">Google review (example)</span>
          </div>
          <div class="quote">
            “Working with <em>Mary</em>, our Expert Advisor at Concierge Care Advisors,
            was wonderful. She helped me (<em>Teresa</em>) find the best personalized care
            options for my mom, guiding us every step with patience and expertise.”
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div style='margin:1.5rem 0 0; display:flex; justify-content:center;'>",
    unsafe_allow_html=True,
)
pro_clicked = st.button("For Professionals", key="welcome_professional", type="primary")
st.markdown("</div>", unsafe_allow_html=True)


# =====================================================================
# Actions - safe wiring that never NameErrors if other modules are absent
# =====================================================================
if 'continue_clicked' in locals() and continue_clicked:
    # Default: assume proxy flow; update state and move on
    if aud.get("entry") == "proxy":
        aud["recipient_name"] = (aud.get("recipient_name") or "").strip() or None
        aud["proxy_name"] = None
        care_context["person_name"] = aud.get("recipient_name") or "Your Loved One"
        safe_switch_page("pages/SeniorNav_welcome_someone_else.py")
    elif aud.get("entry") == "self":
        care_context["person_name"] = "You"
        safe_switch_page("pages/SeniorNav_welcome_self.py")
    else:
        # fallback if entry type is odd
        safe_switch_page("pages/SeniorNav_welcome_someone_else.py")

if pro_clicked:
    aud["entry"] = "pro"
    aud["qualifiers"] = {k: False for k in aud.get("qualifiers", {}).keys()}
    care_context["person_name"] = "Your Loved One"
<<<<<<< Updated upstream
    # Route to professional intake if available; otherwise keep UX alive
    target = "pages/professional_mode.py"
=======
    target = "app_pages/SeniorNav_professional_hub.py"
>>>>>>> Stashed changes
    safe_switch_page(target, "flow", "pro")
