"""Credential hygiene: planted env values must not leak into artifacts (R3)."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from crossfire_forge.ac_summary import assert_summary_sanitized, build_ac_summary_payload
from crossfire_forge.cli import run_review
from crossfire_forge.roster import ResolvedRoster

FIXTURES_DIR = Path(__file__).parent / "fixtures"
EPIC_441 = FIXTURES_DIR / "epic_441.md"

FAKE_SA_PATH = "/tmp/fake-service-account.json"
FAKE_BEARER = "ya29.fake-bearer-token-for-hygiene-test-only-000000000000"
FAKE_ANTHROPIC = "sk-ant-fake-key-for-hygiene-test-only-000000000000"
FAKE_GCP_PROJECT = "123456789012"


def _run_pipeline_with_planted_credentials() -> str:
    planted = {
        "GOOGLE_APPLICATION_CREDENTIALS": FAKE_SA_PATH,
        "VERTEX_ACCESS_TOKEN": FAKE_BEARER,
        "ANTHROPIC_API_KEY": FAKE_ANTHROPIC,
    }
    original = {key: os.environ.get(key) for key in planted}
    os.environ.update(planted)
    try:
        return run_review(
            EPIC_441,
            corpus=["README.md"],
            fixtures_dir=FIXTURES_DIR,
            provider="fake",
            reviewer_count=3,
        )
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def test_planted_credentials_absent_from_ledger_and_metadata() -> None:
    markdown = _run_pipeline_with_planted_credentials()
    needles = (FAKE_SA_PATH, FAKE_BEARER, FAKE_ANTHROPIC, FAKE_GCP_PROJECT)
    for needle in needles:
        assert needle not in markdown

    details_start = markdown.find("<details>")
    if details_start != -1:
        json_block = markdown[details_start:]
        for needle in needles:
            assert needle not in json_block

    parsed = json.loads(
        markdown.split("```json", maxsplit=1)[1].split("```", maxsplit=1)[0]
    )
    serialized = json.dumps(parsed)
    for needle in needles:
        assert needle not in serialized


def test_ac_summary_writer_never_emits_project_ids_or_absolute_paths() -> None:
    resolved = ResolvedRoster(
        slots=(),
        roster_label="mixed",
        degraded=False,
        resolved_slots=("gemini-2.5-flash", "gemini-2.5-pro"),
        distinct_model_families=("gemini",),
    )
    payload = build_ac_summary_payload(
        roster_label=resolved.roster_label,
        roster_resolution=resolved.to_metadata(),
        trials=[],
        all_passed=False,
    )
    blob = json.dumps(payload)
    assert FAKE_GCP_PROJECT not in blob
    assert "C:\\Users" not in blob
    assert "vertex_project" not in blob
    with pytest.raises(ValueError, match="forbidden summary key"):
        assert_summary_sanitized({**payload, "vertex_project": FAKE_GCP_PROJECT})
