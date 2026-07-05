"""Pre-prompt safety scanner tests for Phase 1 Task 5 (FR-2, AC-5)."""

import logging
from pathlib import Path

import pytest

from crossfire_forge.safety import SafetyAbort, scan_pre_prompt

FIXTURES_DIR = Path(__file__).parent / "fixtures"
PLANTED_SECRET = "ghp_FIXTURE00000000000000000000000000000000"


def _load(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def test_epic_secret_triggers_abort() -> None:
    with pytest.raises(SafetyAbort, match="suspected secret"):
        scan_pre_prompt(epic_content=_load("epic_secret.md"))


def test_epic_secret_no_leakage_in_message_logs_or_stderr(
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.DEBUG, logger="crossfire_forge")

    with pytest.raises(SafetyAbort) as exc_info:
        scan_pre_prompt(epic_content=_load("epic_secret.md"))

    captured = capsys.readouterr()
    surfaces = (
        str(exc_info.value),
        caplog.text,
        captured.out,
        captured.err,
    )
    for surface in surfaces:
        assert PLANTED_SECRET not in surface


def test_clean_epic_passes() -> None:
    scan_pre_prompt(epic_content=_load("epic_complete.md"))
