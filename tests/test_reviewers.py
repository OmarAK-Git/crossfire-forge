"""Reviewer interface and fake reviewer tests for Phase 1 Task 8 (FR-6, AC-6)."""

from pathlib import Path

from crossfire_forge.prompts import build_reviewer_prompt
from crossfire_forge.reviewers.base import (
    FINDING_ADAPTER,
    collect_reviewer_results,
    parse_reviewer_output,
)
from crossfire_forge.reviewers.fake import FakeReviewer

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def _fixed_prompt():
    return build_reviewer_prompt(
        _load("epic_441.md"),
        [("README.md", _load("README.md"))],
        ["region unspecified"],
    )


def test_n_fakes_collect_only_schema_valid_findings() -> None:
    prompt = _fixed_prompt()
    reviewers = [
        FakeReviewer("fake-reviewer-1"),
        FakeReviewer("fake-reviewer-2"),
        FakeReviewer("fake-reviewer-3"),
    ]

    result = collect_reviewer_results(reviewers, prompt)

    assert len(result.findings) == 3
    assert result.discard_count == 0
    for finding in result.findings:
        FINDING_ADAPTER.validate_python(finding.model_dump())


def test_discards_metered_when_fake_returns_invalid_json_or_schema() -> None:
    prompt = _fixed_prompt()

    schema_result = FakeReviewer(
        "noncompliant-schema",
        non_compliant=True,
        non_compliant_mode="schema",
    ).review(prompt)
    assert schema_result.findings
    assert schema_result.discard_count == 2

    json_result = FakeReviewer(
        "noncompliant-json",
        non_compliant=True,
        non_compliant_mode="json",
    ).review(prompt)
    assert json_result.findings == []
    assert json_result.discard_count == 1

    parsed = parse_reviewer_output("{not valid json")
    assert parsed.findings == []
    assert parsed.discard_count == 1

    for finding in schema_result.findings:
        FINDING_ADAPTER.validate_python(finding.model_dump())


def test_deterministic_output_on_fixed_input() -> None:
    prompt = _fixed_prompt()
    reviewer = FakeReviewer("fake-reviewer-1")

    first = reviewer.review(prompt)
    second = reviewer.review(prompt)

    assert first == second
    assert first.discard_count == 0
    assert len(first.findings) == 1
