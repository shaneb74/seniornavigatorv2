"""Wizard registry and loader for the cost planner."""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, List

from . import state


@dataclass(frozen=True)
class Step:
    key: str
    label: str
    path: str
    drawer_key: str | None = None


STEPS: List[Step] = [
    Step("landing", "Landing", "pages/cost_planner_v2/cost_planner_landing_v2.py"),
    Step("modules", "Modules", "pages/cost_planner_v2/cost_planner_modules_hub_v2.py"),
    Step("income", "Income", "pages/cost_planner_v2/cost_planner_income_v2.py", drawer_key="income"),
    Step("expenses", "Expenses", "pages/cost_planner_v2/cost_planner_expenses_v2.py", drawer_key="expenses"),
    Step("caregiver", "Caregiver Support", "pages/cost_planner_v2/cost_planner_caregiver_v2.py", drawer_key="caregiver"),
    Step("benefits", "Benefits", "pages/cost_planner_v2/cost_planner_benefits_v2.py", drawer_key="benefits"),
    Step("home", "Home Decisions", "pages/cost_planner_v2/cost_planner_home_v2.py", drawer_key="home"),
    Step("liquidity", "Liquidity", "pages/cost_planner_v2/cost_planner_liquidity_v2.py", drawer_key="liquidity"),
    Step("home_mods", "Home Modifications", "pages/cost_planner_v2/cost_planner_home_mods_v2.py", drawer_key="home_mods"),
    Step("assets", "Assets", "pages/cost_planner_v2/cost_planner_assets_v2.py", drawer_key="assets"),
    Step("timeline", "Timeline", "pages/cost_planner_v2/cost_planner_timeline_v2.py"),
]


def get_steps() -> List[Step]:
    return STEPS


def get_current_step() -> Step:
    index = max(0, min(state.get_progress(), len(STEPS) - 1))
    return STEPS[index]


def get_step_index(step: Step) -> int:
    return STEPS.index(step)


def set_current_step(index: int) -> None:
    capped = max(0, min(index, len(STEPS) - 1))
    state.set_progress(capped)


@lru_cache(maxsize=None)
def load_step_module(step: Step):
    """Dynamically load the module for a step."""
    path = Path(step.path)
    module_name = "cp_" + "_".join(path.with_suffix("").parts)
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load step module at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "render"):
        main = getattr(module, "main", None)
        if callable(main):  # back-compat shim
            setattr(module, "render", main)
    return module


def run_step(step: Step) -> None:
    module = load_step_module(step)
    render: Callable[[], None] | None = getattr(module, "render", None)
    if render is None:
        raise AttributeError(f"Step module {step.path} must define a render() function")
    render()
