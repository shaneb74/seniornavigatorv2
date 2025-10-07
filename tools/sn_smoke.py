"""
Senior Navigator — invariant smoke checks (no pytest required)

Run:
  python tools/sn_smoke.py

Exit codes:
  0 -> all checks passed
  1 -> one or more checks failed

These checks intentionally avoid UI rendering; they exercise core helpers,
theme injection guards, snapshot structure, resume order, and Medicaid-ack
reset behavior. Keep this file pure-Python (no external deps).
"""

from __future__ import annotations
import sys
import json
import time
from typing import Callable, List, Tuple

RESULTS: List[Tuple[str, bool, str]] = []


def check(name: str, fn: Callable[[], None]) -> None:
    try:
        fn()
        RESULTS.append((name, True, ""))
    except AssertionError as e:
        RESULTS.append((name, False, str(e)))
    except Exception as e:
        RESULTS.append((name, False, f"{type(e).__name__}: {e}"))


def summary_exit() -> None:
    ok = all(passed for _, passed, _ in RESULTS)
    width = max(len(name) for name, _, _ in RESULTS) if RESULTS else 0
    print("\nSN SMOKE REPORT")
    print("=" * 72)
    for name, passed, msg in RESULTS:
        pad = " " * (width - len(name))
        status = "PASS" if passed else "FAIL"
        print(f"{status:>4}  {name}{pad}  {('- ' + msg) if (msg and not passed) else ''}")
    print("=" * 72)
    print("OK" if ok else "FAILED")
    sys.exit(0 if ok else 1)

try:
    import streamlit as st  # type: ignore
except Exception as e:
    print("ERROR: streamlit import failed — create/activate the venv first.")
    print(e)
    sys.exit(1)

try:
    from ui.theme import inject_theme
except Exception:
    inject_theme = None

try:
    from gcp_core.state import (
        ensure_session,
        get_answer,
        set_answer,
        latest_snapshot,
        save_snapshot,
        set_section_complete,
        resume_target,
    )
    from gcp_core.engine import snapshot as build_snapshot
except Exception as e:
    print("ERROR: gcp_core.* modules not importable. Did CODEX vendor the bundle?")
    print(e)
    sys.exit(1)


def _reset_session() -> None:
    st.session_state.clear()
    if inject_theme:
        inject_theme()


def test_theme_injected_once() -> None:
    if not inject_theme:
        raise AssertionError("inject_theme() missing; expected ui/theme.py")
    _reset_session()
    inject_theme()
    inject_theme()
    flag_names = [k for k in st.session_state.keys() if "theme_injected" in k]
    assert flag_names, "No theme guard flag found in session_state"
    assert all(st.session_state.get(k) for k in flag_names), "Theme guard not set to truthy"


def test_gcp_session_bootstrap() -> None:
    _reset_session()
    ensure_session()
    assert "gcp" in st.session_state, "Missing session_state['gcp']"
    g = st.session_state.gcp
    assert isinstance(g, dict), "session_state['gcp'] must be a dict"
    assert "answers" in g and isinstance(g["answers"], dict), "gcp.answers missing"
    assert "progress" in g and isinstance(g["progress"], dict), "gcp.progress missing"


def test_resume_order_contract() -> None:
    _reset_session()
    ensure_session()
    target = resume_target()
    assert "gcp_landing_v2" in target, f"Unexpected first resume target: {target}"
    set_section_complete("landing")
    target = resume_target()
    assert "gcp_daily_life_v2" in target, f"Unexpected second resume target: {target}"
    set_section_complete("daily")
    set_section_complete("safety")
    target = resume_target()
    assert "gcp_context_prefs_v2" in target, f"Unexpected third resume target: {target}"
    set_section_complete("context")
    target = resume_target()
    assert "gcp_recommendation_v2" in target, f"Unexpected final resume target: {target}"


def test_medicaid_ack_reset_when_no() -> None:
    _reset_session()
    ensure_session()
    set_answer("medicaid_status", "yes")
    set_answer("medicaid_ack", True)
    set_answer("medicaid_status", "no")
    ack = get_answer("medicaid_ack")
    assert not ack, f"Expected medicaid_ack cleared/false when status=='no', found {ack!r}"


def test_snapshot_contract() -> None:
    _reset_session()
    ensure_session()
    set_answer("medicaid_status", "no")
    snap = build_snapshot(dict(st.session_state.gcp["answers"]), scoring={"dummy": True})
    assert isinstance(snap, dict), "snapshot() must return dict"
    assert snap.get("version") == "gcp.v1.0", f"Unexpected snapshot version: {snap.get('version')}"
    assert "answers" in snap and isinstance(snap["answers"], dict), "Snapshot missing answers"
    save_snapshot(snap)
    latest = latest_snapshot()
    assert latest and latest.get("version") == "gcp.v1.0", "latest_snapshot() missing or wrong version"
    json.dumps(latest)


if __name__ == "__main__":
    start = time.time()
    check("Theme injected once (idempotent)", test_theme_injected_once)
    check("GCP session bootstrap",             test_gcp_session_bootstrap)
    check("Resume order contract",             test_resume_order_contract)
    check("Medicaid ack clears on 'no'",       test_medicaid_ack_reset_when_no)
    check("Snapshot structure & version",      test_snapshot_contract)
    dur_ms = int((time.time() - start) * 1000)
    RESULTS.append((f"Runtime {dur_ms}ms", True, ""))
    summary_exit()
