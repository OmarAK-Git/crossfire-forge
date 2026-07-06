"""Roster resolution tests (remediation pre-approval)."""

from __future__ import annotations

import pytest

from crossfire_forge.roster import DEGRADED_ROSTER_BANNER, resolve_live_roster


def test_resolve_live_roster_fails_without_anthropic_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY not set"):
        resolve_live_roster(allow_vertex_only=False)


def test_resolve_live_roster_degraded_requires_explicit_flag(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    resolved = resolve_live_roster(allow_vertex_only=True)
    assert resolved.degraded is True
    assert resolved.roster_label == "degraded-vertex-only"
    assert resolved.distinct_model_families == ("gemini",)
    assert DEGRADED_ROSTER_BANNER in capsys.readouterr().err


def test_resolve_live_roster_full_mixed_reports_provider_families(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(
        "crossfire_forge.roster.resolve_anthropic_sonnet_model",
        lambda: "claude-sonnet-test",
    )
    resolved = resolve_live_roster(allow_vertex_only=False)
    assert resolved.distinct_model_families == ("gemini", "claude")
