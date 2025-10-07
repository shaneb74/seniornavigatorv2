# ui/cost_planner_template.py
from __future__ import annotations

import contextlib
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Tuple, Union

import streamlit as st

# ------------------------------------------------------------
# Base theme: ensure global app styles load before CP overrides
# ------------------------------------------------------------
try:
    from ui.theme import inject_theme as _inject_base
except Exception:  # pragma: no cover - fallback for legacy contexts
    def _inject_base() -> None:
        pass


# -------------------------------------------------------------------
# Theme + global styles (additive; do NOT call set_page_config here)
# -------------------------------------------------------------------
def apply_cost_planner_theme(
    primary: str = "#0B5CD8",
    surface: str = "var(--surface, #f6f8fa)",
    ink: str = "var(--ink, #111418)",
    ink_muted: str = "var(--ink-muted, #6b7280)",
) -> None:
    # Always load the global app theme first (blue bg/sidebar, etc.)
    _inject_base()

    # Cost Planner–specific tweaks (kept additive)
    st.markdown(
        f"""
        <style>
          :root {{
            --brand: {primary};
            --ink: {ink};
            --ink-muted: {ink_muted};
          }}
          .sn-card {{
            background: {surface};
            border: 1px solid rgba(0,0,0,.08);
            border-radius: 16px;
            padding: clamp(1rem, 2vw, 1.5rem);
          }}
          .sn-hero h1 {{
            font-size: clamp(1.6rem, 3.2vw, 2.2rem);
            margin: 0 0 .25rem 0;
          }}
          .sn-hero p {{
            color: var(--ink-muted);
            margin: 0;
          }}
          .sn-kicker {{
            color: var(--ink-muted);
            font-weight: 600;
            letter-spacing: .02em;
            text-transform: uppercase;
            font-size: .8rem;
            margin: 0 0 .25rem 0;
          }}
          .sn-mod-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 1rem;
          }}
          .sn-btn {{
            display:inline-flex;align-items:center;gap:.5rem;
            border-radius: 10px;border:1px solid rgba(0,0,0,.08);
            padding:.6rem .9rem;background:#fff;
          }}
          .sn-btn.primary {{ background: var(--brand); color: #fff; border: none; }}
          .sn-btn.ghost   {{ background: transparent; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# Small containers usable as context managers
# -------------------------------------------------------------------
@contextlib.contextmanager
def section(title: str = "", subtitle: str = "", gap: str = "1rem", **style):
    if title or subtitle:
        st.markdown(
            f"""
            <div class="sn-section" style="display:flex;flex-direction:column;gap:{gap};">
              {f"<h3 style='margin:0'>{title}</h3>" if title else ""}
              {f"<p style='margin:0;color:var(--ink-muted)'>{subtitle}</p>" if subtitle else ""}
            """,
            unsafe_allow_html=True,
        )
        try:
            yield
        finally:
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        yield


@contextlib.contextmanager
def toolbar(**style):
    st.markdown('<div class="sn-toolbar">', unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


@contextlib.contextmanager
def drawer(title: str = "", **style):
    st.markdown('<div class="sn-drawer sn-card">', unsafe_allow_html=True)
    if title:
        st.subheader(title, divider=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


@contextlib.contextmanager
def metric_panel(gap: str = "0.5rem", **style):
    st.markdown(
        f'<div class="sn-metrics sn-card" style="display:grid;gap:{gap}">',
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------------------
# Header / Hero
# -------------------------------------------------------------------
def render_app_header(
    title: Optional[str] = None,
    subtitle: str = "",
    kicker: Optional[str] = None,
    icon: Optional[str] = None,
    right: Optional[str] = None,
) -> None:
    if not title:
        return
    left_col, right_col = st.columns([1, 1], gap="large")
    with left_col:
        st.markdown('<div class="sn-hero">', unsafe_allow_html=True)
        if kicker:
            st.markdown(f"<div class='sn-kicker'>{kicker}</div>", unsafe_allow_html=True)
        line = (icon + " ") if icon else ""
        st.markdown(f"<h1>{line}{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<p>{subtitle}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right_col:
        if right:
            st.markdown(right, unsafe_allow_html=True)


def render_wizard_hero(title: str, subtitle: str = "", emoji: Optional[str] = None) -> None:
    render_app_header(title=title, subtitle=subtitle, icon=emoji)


# -------------------------------------------------------------------
# Module cards grid
# modules: Iterable[dict] with keys: title, blurb, key, on_click (callable) OR href
# -------------------------------------------------------------------
def render_module_cards(
    modules: Iterable[Dict[str, Any]],
    *,
    button_label: str = "Open",
    cols: Optional[Tuple[int, ...]] = None,
) -> Dict[str, bool]:
    """Returns a dict {module_key: clicked_bool}."""
    clicks: Dict[str, bool] = {}
    st.markdown('<div class="sn-mod-grid">', unsafe_allow_html=True)
    for m in modules:
        title = m.get("title", "Untitled")
        blurb = m.get("blurb", "")
        key = m.get("key", title.lower().replace(" ", "_"))
        href = m.get("href")
        on_click = m.get("on_click")

        with st.container(border=True):
            st.markdown(f"### {title}")
            if blurb:
                st.caption(blurb)
            if href:
                # link-style button (works on Streamlit 1.40+)
                if st.link_button(button_label, href=href, key=f"mod_link_{key}"):  # type: ignore[attr-defined]
                    clicks[key] = True
            else:
                if st.button(button_label, key=f"mod_btn_{key}"):
                    clicks[key] = True
                    if callable(on_click):
                        on_click()
    st.markdown("</div>", unsafe_allow_html=True)
    return clicks


# -------------------------------------------------------------------
# Wizard help
# -------------------------------------------------------------------
def render_wizard_help(text: str = "", tips: Optional[Iterable[str]] = None, *, open: bool = False) -> None:  # noqa: A002
    with st.expander("Need a hand?", expanded=open):
        if text:
            st.write(text)
        if tips:
            for t in tips:
                st.write("• " + str(t))


# -------------------------------------------------------------------
# Navigation controls
# -------------------------------------------------------------------
@dataclass
class NavButton:
    label: str
    key: str
    kind: str = "primary"  # 'primary' | 'secondary' | 'ghost'
    icon: Optional[str] = None
    # legacy alias for compatibility: maps to `kind`
    type: Optional[str] = None  # noqa: A003

    def __post_init__(self) -> None:
        if self.type:
            self.kind = self.type
            self.type = None

    def render(self) -> bool:
        label = f"{self.icon} {self.label}" if self.icon else self.label
        if self.kind == "primary":
            return st.button(label, type="primary", key=self.key)
        if self.kind == "secondary":
            return st.button(label, key=self.key)
        # ghost / fallback
        return st.button(label, key=self.key)


def _to_navbtn(x: Union[NavButton, Dict[str, Any], None]) -> Optional[NavButton]:
    if x is None:
        return None
    if isinstance(x, NavButton):
        return x
    if isinstance(x, dict):
        return NavButton(**x)
    return NavButton(str(x), key=f"nav_{str(x)}")


def render_nav_buttons(
    prev: Union[NavButton, Dict[str, Any], None] = None,
    next: Union[NavButton, Dict[str, Any], None] = None,
    *,
    align: str = "right",
    gap: str = "0.6rem",
) -> Dict[str, bool]:
    """
    Renders prev/next in a row. Returns {'prev': bool, 'next': bool}.
    Accepts NavButton instances OR dicts with keys: label, key, type/kind, icon.
    """
    prev = _to_navbtn(prev)
    next = _to_navbtn(next)

    left, right = st.columns([1, 1])
    result = {"prev": False, "next": False}
    with left:
        if prev:
            result["prev"] = prev.render()
    with right:
        if next:
            st.markdown(
                f"<div style='display:flex;justify-content:flex-end;gap:{gap}'>",
                unsafe_allow_html=True,
            )
            result["next"] = next.render()
            st.markdown("</div>", unsafe_allow_html=True)
    return result


# -------------------------------------------------------------------
# Minimal extras used by some pages
# -------------------------------------------------------------------
def two_col_cols(ratio: Tuple[float, float] = (1, 1), gap: str = "1.25rem"):
    try:
        return st.columns(ratio, gap=gap)
    except Exception:
        return st.columns(ratio)


# Dynamic fallback: unknown helper names
def __getattr__(name: str):
    lname = name.lower()
    if any(k in lname for k in ("panel", "section", "container", "group", "block", "layout", "drawer", "toolbar")):
        @contextlib.contextmanager
        def _cm(*args, **kwargs):
            yield
        return _cm

    def _fn(*args, **kwargs):
        pass

    return _fn


def render_nav(buttons):
    """
    Convenience wrapper: accept [prev, next] (NavButton or dict) and render.
    Usage:
        render_nav([
            {"label": "Back", "key": "nav_back", "type": "secondary"},
            {"label": "Next", "key": "nav_next", "type": "primary", "icon": "➡️"},
        ])
    """
    if buttons is None:
        return {"prev": False, "next": False}
    try:
        seq = list(buttons)
    except Exception:
        seq = [buttons]
    prev = seq[0] if len(seq) > 0 else None
    nxt = seq[1] if len(seq) > 1 else None
    return render_nav_buttons(prev=prev, next=nxt)


def ensure_cp_state():
    if "cp" not in st.session_state or not isinstance(st.session_state.cp, dict):
        st.session_state.cp = {"sections": {}}
    else:
        st.session_state.cp.setdefault("sections", {})
    return st.session_state.cp


def segmented_control(label, options, *, key, default=None):
    ss_key = f"cp_segment_{key}"
    if ss_key not in st.session_state and default is not None:
        st.session_state[ss_key] = default
    try:
        st.segmented_control(label, list(options), key=ss_key, default=st.session_state.get(ss_key, default))
    except Exception:
        opts = list(options)
        idx = opts.index(default) if default in opts else 0
        st.selectbox(label, opts, index=idx, key=ss_key)


def update_section(step_key: str, payload: dict) -> None:
    cp = ensure_cp_state()
    cp["sections"][step_key] = {"data": dict(payload or {}), "ts": __import__("time").time()}


def go_to_step(step_key: str) -> None:
    st.session_state["cp_next_step"] = step_key
    try:
        st.rerun()
    except Exception:
        pass


def render_drawer(*, step_key: str, title: str, badge=None, description="", body=None, footer_note=None):
    from types import SimpleNamespace

    cp = ensure_cp_state()
    with st.container(border=True):
        left, right = st.columns([1, 1])
        with left:
            st.subheader(title)
            if description:
                st.caption(description)
            if badge:
                st.markdown(f"<div class='pfma-note'>{badge}</div>", unsafe_allow_html=True)
        with right:
            pass
        st.markdown("---")
        payload = body(cp) if callable(body) else {}
        st.markdown("---")
        l, r = st.columns([1, 1])
        with l:
            if footer_note:
                st.markdown(f"<div class='pfma-note'>{footer_note}</div>", unsafe_allow_html=True)
        with r:
            c1, c2 = st.columns([1, 1])
            with c1:
                save = st.button("Save", key=f"{step_key}_save")
            with c2:
                next_clicked = st.button("Save & Continue", key=f"{step_key}_save_next")
    saved = bool(save or next_clicked)
    next_step = st.session_state.get("cp_next_step") if next_clicked else None
    return SimpleNamespace(saved=saved, payload=payload, next_step=next_step, ok=saved, message=None)


@contextlib.contextmanager
def card(title: str | None = None, subtitle: str = ""):
    """Shared rounded card wrapper (matches PFMA drawers)."""
    with st.container(border=True):
        if title:
            st.subheader(title)
        if subtitle:
            st.caption(subtitle)
        yield
