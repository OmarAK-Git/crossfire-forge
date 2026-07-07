"""Schema validation tests for Phase 1 Task 2 (spec §5, NG7)."""

import pytest
from pydantic import TypeAdapter, ValidationError

from crossfire_forge.schemas import (
    AssumptionFinding,
    CorpusHash,
    Finding,
    Ledger,
    RunIdentity,
    SafetyWarningFinding,
    ViolationFinding,
)
from crossfire_forge.taxonomy import BlastRadius, FindingType

FINDING_ADAPTER = TypeAdapter(Finding)

_COMMON = {
    "statement": "RBAC scope is unspecified.",
    "evidence": "Epic body mentions deployment but not Role vs ClusterRole.",
    "blast_radius": BlastRadius.BR3,
    "reviewer_votes": ["fake-reviewer-1"],
    "agreement_count": 1,
}


def test_finding_types_are_exactly_three() -> None:
    assert {member.value for member in FindingType} == {
        "assumption",
        "violation",
        "safety_warning",
    }


def test_assumption_finding_validates() -> None:
    finding = AssumptionFinding(
        **_COMMON,
        alternative="Use a namespaced Role limited to the target namespace.",
    )
    assert finding.type == FindingType.ASSUMPTION
    assert finding.alternative


def test_violation_finding_requires_standards_ref() -> None:
    finding = ViolationFinding(
        **_COMMON,
        standards_ref="README.md#security-posture",
    )
    assert finding.standards_ref


def test_violation_without_standards_ref_fails_ng7() -> None:
    payload = {**_COMMON, "type": "violation"}
    with pytest.raises(ValidationError) as exc_info:
        FINDING_ADAPTER.validate_python(payload)
    assert "standards_ref" in str(exc_info.value)


def test_violation_with_empty_standards_ref_fails_ng7() -> None:
    payload = {**_COMMON, "type": "violation", "standards_ref": ""}
    with pytest.raises(ValidationError):
        ViolationFinding.model_validate(payload)


def test_assumption_without_alternative_fails() -> None:
    payload = {**_COMMON, "type": "assumption"}
    with pytest.raises(ValidationError) as exc_info:
        FINDING_ADAPTER.validate_python(payload)
    assert "alternative" in str(exc_info.value)


def test_safety_warning_finding_validates() -> None:
    finding = SafetyWarningFinding(
        statement="Embedded instruction detected.",
        evidence="Epic body contains 'ignore previous instructions'.",
        blast_radius=BlastRadius.BR1,
        reviewer_votes=["fake-reviewer-1"],
        agreement_count=1,
    )
    assert finding.type == FindingType.SAFETY_WARNING


def test_discriminated_union_rejects_unknown_type() -> None:
    payload = {**_COMMON, "type": "risk", "alternative": "n/a"}
    with pytest.raises(ValidationError):
        FINDING_ADAPTER.validate_python(payload)


def test_run_identity_validates() -> None:
    identity = RunIdentity(
        epic_hash="abc123",
        corpus_hashes=[CorpusHash(path="README.md", content_hash="def456")],
        model_roster=["fake-reviewer-1", "fake-reviewer-2"],
        tool_version="0.1.0",
    )
    assert identity.epic_hash == "abc123"


def test_run_identity_rejects_empty_epic_hash() -> None:
    with pytest.raises(ValidationError):
        RunIdentity(
            epic_hash="",
            corpus_hashes=[CorpusHash(path="README.md", content_hash="def456")],
            model_roster=["fake-reviewer-1"],
            tool_version="0.1.0",
        )


def test_run_identity_rejects_empty_corpus() -> None:
    with pytest.raises(ValidationError):
        RunIdentity(
            epic_hash="abc123",
            corpus_hashes=[],
            model_roster=["fake-reviewer-1"],
            tool_version="0.1.0",
        )


def test_ledger_validates() -> None:
    ledger = Ledger(
        identity=RunIdentity(
            epic_hash="abc123",
            corpus_hashes=[CorpusHash(path="README.md", content_hash="def456")],
            model_roster=["fake-reviewer-1"],
            tool_version="0.1.0",
        ),
        findings=[
            AssumptionFinding(
                **_COMMON,
                alternative="Pin region to us-central1 explicitly.",
            ),
            ViolationFinding(
                **_COMMON,
                standards_ref="README.md#regions",
            ),
            SafetyWarningFinding(
                statement="Prompt injection attempt.",
                evidence="Hidden HTML comment with instruction.",
                blast_radius=BlastRadius.BR1,
                reviewer_votes=["fake-reviewer-1"],
                agreement_count=1,
            ),
        ],
    )
    assert len(ledger.findings) == 3


def test_ledger_rejects_invalid_finding() -> None:
    with pytest.raises(ValidationError):
        Ledger.model_validate(
            {
                "identity": {
                    "epic_hash": "abc123",
                    "corpus_hashes": [{"path": "README.md", "content_hash": "def456"}],
                    "model_roster": ["fake-reviewer-1"],
                    "tool_version": "0.1.0",
                },
                "findings": [
                    {
                        **_COMMON,
                        "type": "violation",
                    }
                ],
            }
        )


def test_finding_validates_without_reviewer_votes_or_agreement_count() -> None:
    """Raw model findings omit pipeline-owned attribution; defaults apply (R-1)."""
    payload = {
        "type": "assumption",
        "statement": "RBAC scope is unspecified.",
        "evidence": "Epic body mentions deployment but not Role vs ClusterRole.",
        "blast_radius": BlastRadius.BR3,
        "alternative": "Use a namespaced Role limited to the target namespace.",
    }
    finding = FINDING_ADAPTER.validate_python(payload)
    assert finding.reviewer_votes == []
    assert finding.agreement_count == 0


def test_safety_warning_validates_without_attribution_fields() -> None:
    finding = SafetyWarningFinding(
        statement="Embedded instruction detected.",
        evidence="Epic body contains 'ignore previous instructions'.",
        blast_radius=BlastRadius.BR1,
    )
    assert finding.reviewer_votes == []
    assert finding.agreement_count == 0


def test_negative_agreement_count_fails() -> None:
    payload = {
        **_COMMON,
        "type": "assumption",
        "alternative": "Use internal LB.",
        "agreement_count": -1,
    }
    with pytest.raises(ValidationError):
        FINDING_ADAPTER.validate_python(payload)
