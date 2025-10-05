"""Standalone entry to render the loved one contextual welcome variant."""
from __future__ import annotations

from ui.pages.contextual_welcome_base import render


def main() -> None:
    render("loved")


if __name__ == "__main__":
    main()
