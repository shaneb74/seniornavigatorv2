"""Contextual welcome entry point that routes to the correct variant."""
from __future__ import annotations

import streamlit as st

from ui.pages.contextual_welcome_base import render


def main() -> None:
    entry = st.session_state.get("audiencing", {}).get("entry", "self")
    render("you" if entry == "self" else "loved")


if __name__ == "__main__":
    main()
