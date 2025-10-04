from __future__ import annotations

# Shared renderer for the Contextual Welcome (modal + pills + collage)

from pathlib import Path
import streamlit as st

# --- theme import with safe fallback (so the page always renders) ---
try:
    from ui.theme import inject_theme  # type: ignore
except Exception:
    def inject_theme() -> None:
        st.markdown(
            """
            <style>
              .block-container{max-width:1160px;padding-top:8px;}
              header[data-testid="stHeader"]{background:transparent;}
              footer{visibility:hidden;}
            </style>
            """,
            unsafe_allow_html=True,
        )

# Try to use your audiencing helpers if they exist; otherwise no-ops
try:
    from audiencing import ensure_audiencing_state, snapshot_audiencing  # type: ignore
except Exception:  # pragma: no cover
    ensure_audiencing_state = None
    snapshot_audiencing = None


IMAGE_MAP = {
    "self": "static/images/contextual_welcome_self.png",
    "proxy": "static/images/contextual_welcome_someone_else.png",
}

COPY = {
    "self": {
        "headline": "We're here to help you find the support you're looking for.",
        "input_label": "What's your name?",
        "pill_self": "For me",
        "pill_proxy": "For someone",
    },
    "proxy": {
        "headline": "We're here to help you find the support your loved ones need.",
        "input_label": "What's their name?",
        "pill_self": "For me",
        "pill_proxy": "For someone",
    },
}


def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = target
        st.rerun()


def _ensure_care_context() -> dict:
    return st.session_state.setdefault(
        "care_context",
        {"person_name": "Your Loved One", "gcp_answers": {}, "gcp_recommendation": None},
    )


def _get_image(entry: str) -> str:
    candidate = IMAGE_MAP.get(entry, IMAGE_MAP["proxy"])
    return candidate if Path(candidate).exists() else IMAGE_MAP["proxy"]


def render(which: str = "you") -> None:
    """
    Render the Contextual Welcome:
      which = "you" -> self variant
      which = "loved" -> proxy/loved-one variant
    """
    entry = "self" if which in ("you", "self") else "proxy"

    st.set_page_config(page_title="Welcome", layout="wide")
    inject_theme()

    # --- CSS for background + modal + pills (ASCII only) ---
    st.markdown(
        """
        <style>
          .cw-wrap { position: relative; min-height: 86vh; background: #eaf0ff40; border-radius: 20px; }
          .cw-canvas { position: absolute; right: 0; top: 0; bottom: 0; width: 64%; pointer-events: none; }
          .cw-canvas img { position: absolute; right: 3%; top: 6%; width: 88%; max-width: 980px; filter: drop-shadow(0 16px 32px rgba(15,23,42,0.18)); border-radius: 6px; }
          .cw-modal { position: relative; z-index: 2; width: 520px; margin: 72px 0 0 64px; background: #fff; border-radius: 14px;
                      box-shadow: 0 12px 40px rgba(15,23,42,0.12); padding: 24px 24px 22px; }
          .cw-pills { display: flex; gap: 10px; margin-bottom: 10px; }
          .cw-pill { font-size: 14px; border-radius: 10px; padding: 8px 14px; border: 1px solid #e5e7eb; background: #f8fafc; cursor: pointer; }
          .cw-pill.is-active { background: #0b5cd8; color: #fff; border-color: #0b5cd8; }
          .cw-close { position: absolute; right: 14px; top: 14px; width: 28px; height: 28px; border-radius: 999px; border: 1px solid #e5e7eb; display:flex; align-items:center; justify-content:center; color:#64748b; }
          .cw-h1 { font-size: 28px; line-height: 1.25; font-weight: 800; margin: 12px 0 16px; color: #0f172a; }
          .cw-form { display:flex; gap: 12px; }
          .cw-form .txt { flex: 1; }
          .cw-helper { margin-top: 10px; font-size: 12px; color:#475569; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Persist small bit of UI state so toggling rerenders cleanly
    ui = st.session_state.setdefault("cw_ui", {"entry": entry})
    entry = ui.get("entry", entry)

    copy = COPY[entry]
    img_src = _get_image(entry)

    # ----- BG canvas + modal -----
    st.markdown('<div class="cw-wrap">', unsafe_allow_html=True)

    # collage on the right
    st.markdown(f'<div class="cw-canvas"><img alt="collage" src="{img_src}"/></div>', unsafe_allow_html=True)

    # modal block
    with st.container():
        st.markdown('<div class="cw-modal">', unsafe_allow_html=True)

        # pills row
        col_pills, col_close = st.columns([10, 1])
        with col_pills:
            pill_proxy_cls = "cw-pill is-active" if entry == "proxy" else "cw-pill"
            pill_self_cls = "cw-pill is-active" if entry == "self" else "cw-pill"
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button(copy["pill_proxy"], key="cw_pill_proxy", use_container_width=False):
                    st.session_state["cw_ui"]["entry"] = "proxy"
                    st.rerun()
            with col_b:
                if st.button(copy["pill_self"], key="cw_pill_self", use_container_width=False):
                    st.session_state["cw_ui"]["entry"] = "self"
                    st.rerun()
            # swap the buttons to look like pills via CSS classes
            st.markdown(
                f"""
                <script>
                  const btns = window.parent.document.querySelectorAll('[data-testid="baseButton-secondary"]');
                  if (btns && btns.length >= 2) {{
                    btns[btns.length-2].classList.add("{pill_proxy_cls}");
                    btns[btns.length-1].classList.add("{pill_self_cls}");
                  }}
                </script>
                """,
                unsafe_allow_html=True,
            )
        with col_close:
            st.markdown('<div class="cw-close">x</div>', unsafe_allow_html=True)

        # headline
        st.markdown(f'<div class="cw-h1">{copy["headline"]}</div>', unsafe_allow_html=True)

        # name input + continue
        default_name = st.session_state.get("cw_name", "")
        name = st.text_input(copy["input_label"], value=default_name, key="cw_name")

        col_txt, col_btn = st.columns([3, 1])
        with col_btn:
            if st.button("Continue", type="primary", use_container_width=True):
                # stash into care_context
                ctx = _ensure_care_context()
                if entry == "self":
                    ctx["person_name"] = name or "You"
                else:
                    ctx["person_name"] = name or "Your Loved One"

                # update audiencing if available
                if ensure_audiencing_state:
                    state = ensure_audiencing_state()
                    state["entry"] = entry
                    people = state.setdefault("people", {"recipient_name": "", "proxy_name": ""})
                    if entry == "self":
                        people["proxy_name"] = ""
                        people["recipient_name"] = ""
                    else:
                        people["recipient_name"] = name or people.get("recipient_name", "")
                    # keep a snapshot for downstream pages, when helper exists
                    if snapshot_audiencing:
                        st.session_state["audiencing_snapshot"] = snapshot_audiencing(state)

                _safe_switch_page("pages/hub.py")

        st.caption("If you want to assess several people, do not worry-you can easily move on to the next step!")
        st.markdown("</div>", unsafe_allow_html=True)  # end modal

    st.markdown("</div>", unsafe_allow_html=True)  # end wrap
