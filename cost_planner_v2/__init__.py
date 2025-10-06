"""Cost Planner v2 package bootstrap helpers."""

from __future__ import annotations

import importlib
import sys


def _ensure_shared_module() -> None:
    """Expose the Streamlit page helpers as ``cost_planner_v2._shared``."""

    module_name = "pages.cost_planner_v2._shared"
    try:
        shared_module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        # Leave a lightweight breadcrumb for diagnostics without crashing startup.
        print(f"⚠️  cost_planner_v2: unable to import {module_name}")
        return

    alias = f"{__name__}._shared"
    sys.modules.setdefault(alias, shared_module)
    globals().setdefault("_shared", shared_module)


_ensure_shared_module()

__all__ = ["_shared"]
