from __future__ import annotations

import base64
import html
import mimetypes
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterable, Literal
from uuid import uuid4

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

StatusValue = Literal["not_started", "in_progress", "complete"]

_STATUS_MAP: dict[StatusValue, dict[str, str]] = {
    "not_started": {"label": "Not started", "classes": "sn-chip"},
    "in_progress": {"label": "In progress", "classes": "sn-chip info"},
    "complete": {"label": "Complete", "classes": "sn-chip ok", "icon": "✓"},
}


def _slugify(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "card"


def _icon_markup(icon: str | None) -> str:
    if not icon:
        return ""

    icon = icon.strip()
    if not icon:
        return ""

    path = Path(icon)
    if path.exists() and path.is_file():
        try:
            mime = mimetypes.guess_type(path.name)[0] or "image/png"
            data = base64.b64encode(path.read_bytes()).decode("ascii")
            return (
                "<span class='sn-card-icon image'>"
                f"<img src='data:{mime};base64,{data}' alt='' role='presentation' />"
                "</span>"
            )
        except Exception:
            pass

    return f"<span class='sn-card-icon emoji'>{html.escape(icon)}</span>"


@contextmanager
def ModuleGrid(cols: int = 3, *, gap: str = "large") -> Iterable[DeltaGenerator]:
    """Layout helper yielding a responsive set of Streamlit columns for cards."""
    column_count = max(1, int(cols or 1))
    container = st.container()
    with container:
        st.markdown(
            f"<div class='sn-module-grid sn-module-grid-{column_count}' data-cols='{column_count}'>",
            unsafe_allow_html=True,
        )
        columns = st.columns(column_count, gap=gap)
        try:
            yield columns
        finally:
            st.markdown("</div>", unsafe_allow_html=True)


def ModuleCard(
    *,
    title: str,
    body: str,
    icon: str | None = None,
    primary_label: str = "Open",
    on_primary: Callable[[], None] | None = None,
    secondary_label: str | None = None,
    on_secondary: Callable[[], None] | None = None,
    status: StatusValue = "not_started",
    caption: str | None = None,
    disabled: bool = False,
    testid: str | None = None,
) -> None:
    """Render a reusable module card with consistent layout and actions."""
    status_key: StatusValue = status if status in _STATUS_MAP else "not_started"
    status_meta = _STATUS_MAP[status_key]

    status_label = status_meta["label"]
    status_classes = status_meta["classes"]
    status_icon = status_meta.get("icon")
    status_icon_markup = f"<span class='sn-chip-icon'>{status_icon}</span>" if status_icon else ""
    status_aria = f"Status: {status_label}"

    card_classes = ["sn-card"]
    if disabled:
        card_classes.append("is-disabled")

    title_id = f"sn-module-card-title-{uuid4().hex}"
    base_key = testid or _slugify(title)

    opening_attrs = [
        f"class=\"{' '.join(card_classes)}\"",
        f'role="group"',
        f'aria-labelledby="{title_id}"',
    ]
    if testid:
        opening_attrs.append(f'data-testid="{testid}"')

    card_header = (
        f"<div class='sn-card-header'>"
        f"  <div class='sn-card-heading'>"
        f"    {_icon_markup(icon)}"
        f"    <h3 id='{title_id}' class='sn-card-title'>{html.escape(title)}</h3>"
        f"  </div>"
        f"  <span class='{status_classes}' aria-label='{status_aria}'>"
        f"    {status_icon_markup}{html.escape(status_label)}"
        f"  </span>"
        f"</div>"
    )

    caption_html = ""
    if caption:
        caption_html = f"<p class='sn-card-caption'>{html.escape(caption)}</p>"

    body_html = (
        "<div class='sn-card-body'>"
        f"  <p>{html.escape(body)}</p>"
        f"  {caption_html}"
        "</div>"
    )

    st.markdown(f"<div {' '.join(opening_attrs)}>", unsafe_allow_html=True)
    st.markdown(card_header, unsafe_allow_html=True)
    st.markdown(body_html, unsafe_allow_html=True)

    st.markdown("<div class='sn-card-actions'>", unsafe_allow_html=True)

    primary_disabled = disabled or on_primary is None
    secondary_disabled = disabled or on_secondary is None

    if primary_label:
        primary_help = f"{primary_label} {title}"
        with st.container():
            clicked = st.button(
                primary_label,
                key=f"{base_key}_primary",
                type="primary",
                use_container_width=True,
                disabled=primary_disabled,
                help=primary_help,
            )
            if clicked and on_primary:
                on_primary()

    if secondary_label:
        secondary_help = f"{secondary_label} {title}"
        with st.container():
            clicked_secondary = st.button(
                secondary_label,
                key=f"{base_key}_secondary",
                type="secondary",
                use_container_width=True,
                disabled=secondary_disabled,
                help=secondary_help,
            )
            if clicked_secondary and on_secondary:
                on_secondary()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

@contextmanager
def card_panel(padding="1rem", gap="1rem", **kwargs):
    """
    Context-managed card wrapper used as:
        with card_panel(padding="..."):
            ...children...
    """
    st.markdown(
        f"""
        <div class="sn-card-panel" style="
            padding:{padding};
            display:flex; flex-direction:column; gap:{gap};
            background:var(--surface, #f6f8fa);
            border:1px solid rgba(0,0,0,.08);
            border-radius:16px;
        ">
        """,
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)

# Generic fallbacks for any other component names referenced in legacy code.
def __getattr__(name: str):
    # Non-context-manager placeholder: prints a small notice, returns None.
    def _fallback(*args, **kwargs):
        st.caption(f"ui.components.{name}() placeholder")
    return _fallback
