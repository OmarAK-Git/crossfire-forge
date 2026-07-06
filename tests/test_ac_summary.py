"""Structural live AC summary writer tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from crossfire_forge.ac_summary import (
    TrialSummary,
    assert_summary_sanitized,
    build_ac_summary_payload,
    write_ac_summary,
)


def test_build_ac_summary_rejects_forbidden_keys() -> None:
    payload = build_ac_summary_payload(
        roster_label="mixed",
        roster_resolution={
            "roster_label": "mixed",
            "degraded": False,
            "resolved_slots": ["gemini-2.5-flash", "gemini-2.5-pro"],
            "distinct_model_families": ["gemini"],
        },
        trials=[
            TrialSummary(
                criterion="AC-1",
                k=4,
                n=5,
                trial_results=(True,) * 5,
                passed=True,
            )
        ],
        all_passed=True,
    )
    with pytest.raises(ValueError, match="forbidden summary key"):
        assert_summary_sanitized({**payload, "vertex_project": "123456789012"})


def test_build_ac_summary_rejects_absolute_ledger_path() -> None:
    payload = build_ac_summary_payload(
        roster_label="mixed",
        roster_resolution={
            "roster_label": "mixed",
            "degraded": False,
            "resolved_slots": ["gemini-2.5-flash"],
            "distinct_model_families": ["gemini"],
        },
        trials=[],
        all_passed=False,
    )
    payload["ledger_441_path"] = r"C:\Users\secret\artifacts\ledger-441.md"
    with pytest.raises(ValueError, match="absolute"):
        assert_summary_sanitized(payload)


def test_write_ac_summary_uses_relative_ledger_path_only(tmp_path: Path) -> None:
    out = tmp_path / "live-ac-summary.json"
    payload = build_ac_summary_payload(
        roster_label="mixed",
        roster_resolution={
            "roster_label": "mixed",
            "degraded": False,
            "resolved_slots": ["gemini-2.5-flash"],
            "distinct_model_families": ["gemini"],
        },
        trials=[],
        all_passed=False,
    )
    write_ac_summary(out, payload)
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded["ledger_441_path"] == "artifacts/ledger-441.md"
    assert "C:\\Users" not in out.read_text(encoding="utf-8")
