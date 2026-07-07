"""Reviewer interface and fake reviewer tests for Phase 1 Task 8 (FR-6, AC-6)."""

from pathlib import Path

from crossfire_forge.prompts import ReviewerPrompt, build_reviewer_prompt
from crossfire_forge.reviewers.base import (
    FINDING_ADAPTER,
    ReviewResult,
    collect_reviewer_results,
    parse_reviewer_output,
    slot_vote_id,
    stamp_finding_slot,
)
from crossfire_forge.reviewers.fake import FakeReviewer
from crossfire_forge.taxonomy import BlastRadius, FindingType

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


class _ScriptedReviewer:
    """Reviewer that returns a fixed, pre-validated ReviewResult."""

    def __init__(self, reviewer_id: str, raw: list[object]) -> None:
        self.reviewer_id = reviewer_id
        self._raw = raw

    def review(self, prompt: ReviewerPrompt) -> ReviewResult:  # noqa: ARG002
        findings = [FINDING_ADAPTER.validate_python(item) for item in self._raw]
        return ReviewResult(findings=findings, discard_count=0)


def _raw_assumption(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "type": FindingType.ASSUMPTION,
        "statement": "RBAC scope is unspecified.",
        "evidence": "Epic omits Role vs ClusterRole.",
        "blast_radius": BlastRadius.BR3,
        "alternative": "Specify a namespaced Role.",
    }
    payload.update(overrides)
    return payload


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


def test_slot_vote_id_is_distinct_per_slot_for_same_model() -> None:
    assert slot_vote_id(1, "gemini-2.5-flash") == "slot-1:gemini-2.5-flash"
    assert slot_vote_id(2, "gemini-2.5-flash") == "slot-2:gemini-2.5-flash"
    assert slot_vote_id(1, "gemini-2.5-flash") != slot_vote_id(2, "gemini-2.5-flash")


def test_stamp_overwrites_model_authored_attribution() -> None:
    """Fabricated reviewer_votes/agreement_count are discarded; stamp wins (R-1)."""
    finding = FINDING_ADAPTER.validate_python(
        _raw_assumption(reviewer_votes=["totally", "made", "up"], agreement_count=99)
    )
    stamped = stamp_finding_slot(finding, "slot-1:gemini-2.5-flash")
    assert stamped.reviewer_votes == ["slot-1:gemini-2.5-flash"]
    assert stamped.agreement_count == 1


def test_collect_stamps_fabricated_votes_at_collection() -> None:
    prompt = _fixed_prompt()
    reviewer = _ScriptedReviewer(
        "gemini-2.5-flash",
        [_raw_assumption(reviewer_votes=["fabricated"], agreement_count=42)],
    )

    result = collect_reviewer_results([reviewer], prompt)

    assert len(result.findings) == 1
    assert result.findings[0].reviewer_votes == ["slot-1:gemini-2.5-flash"]
    assert result.findings[0].agreement_count == 1


def test_collect_stamps_findings_missing_attribution_fields() -> None:
    prompt = _fixed_prompt()
    reviewer = _ScriptedReviewer("gemini-2.5-pro", [_raw_assumption()])

    result = collect_reviewer_results([reviewer], prompt)

    assert len(result.findings) == 1
    assert result.findings[0].reviewer_votes == ["slot-1:gemini-2.5-pro"]
    assert result.findings[0].agreement_count == 1


def test_collect_same_model_two_slots_gets_distinct_slot_ids() -> None:
    prompt = _fixed_prompt()
    reviewers = [
        _ScriptedReviewer("gemini-2.5-flash", [_raw_assumption()]),
        _ScriptedReviewer("gemini-2.5-flash", [_raw_assumption()]),
    ]

    result = collect_reviewer_results(reviewers, prompt)

    assert [f.reviewer_votes for f in result.findings] == [
        ["slot-1:gemini-2.5-flash"],
        ["slot-2:gemini-2.5-flash"],
    ]
