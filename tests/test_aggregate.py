"""Aggregator tests for Phase 2 Task 11 (FR-7, INV-6)."""

from crossfire_forge.aggregate import (
    DEFAULT_CLUSTER_THRESHOLD,
    aggregate_findings,
    cluster_findings,
)
from crossfire_forge.schemas import AssumptionFinding, SafetyWarningFinding, ViolationFinding
from crossfire_forge.taxonomy import BlastRadius, FindingType


def _assumption(
    statement: str,
    *,
    reviewer: str,
    blast_radius: BlastRadius = BlastRadius.BR2,
    evidence: str = "Evidence for assumption.",
    alternative: str = "Specify RBAC scope before deployment.",
) -> AssumptionFinding:
    return AssumptionFinding(
        statement=statement,
        evidence=evidence,
        blast_radius=blast_radius,
        reviewer_votes=[reviewer],
        agreement_count=1,
        alternative=alternative,
    )


def _violation(
    statement: str,
    *,
    reviewer: str,
    blast_radius: BlastRadius = BlastRadius.BR3,
) -> ViolationFinding:
    return ViolationFinding(
        statement=statement,
        evidence="Evidence for violation.",
        blast_radius=blast_radius,
        reviewer_votes=[reviewer],
        agreement_count=1,
        standards_ref="README.md#security-posture",
    )


class MockJudge:
    """Deterministic judge that emits one schema-valid merged finding per cluster."""

    def merge(self, cluster):  # noqa: ANN001
        primary = cluster[0]
        payload = primary.model_dump()
        payload["statement"] = f"Merged: {primary.statement}"
        return [payload]


class InvalidJudge:
    """Judge that always returns schema-invalid output."""

    def merge(self, cluster):  # noqa: ANN001
        return [{"type": FindingType.VIOLATION, "statement": "x", "evidence": "y"}]


def test_cluster_findings_groups_similar_statements() -> None:
    findings = [
        _assumption("Region is unspecified in the Epic body.", reviewer="r1"),
        _assumption("The Epic body leaves region unspecified.", reviewer="r2"),
        _assumption("Quota budget is missing.", reviewer="r3"),
    ]

    clusters = cluster_findings(findings, threshold=DEFAULT_CLUSTER_THRESHOLD)

    assert len(clusters) == 2
    flat = [idx for cluster in clusters for idx in cluster]
    assert sorted(flat) == [0, 1, 2]
    assert len([cluster for cluster in clusters if len(cluster) == 2]) == 1
    assert len([cluster for cluster in clusters if len(cluster) == 1]) == 1


def test_singleton_findings_are_rendered_with_conservation() -> None:
    findings = [
        _assumption("Alpha finding.", reviewer="r1"),
        _assumption("Beta finding.", reviewer="r2"),
    ]

    result = aggregate_findings(findings, MockJudge())

    assert len(result.findings) == 2
    assert result.ledger.rendered == (0, 1)
    assert result.ledger.merged == ()
    assert result.ledger.collapsed == ()
    assert result.ledger.discarded == ()
    assert result.ledger.is_conserved()
    assert result.judge_discard_count == 0


def test_exact_duplicates_collapse_without_judge() -> None:
    statement = "Region is unspecified in the Epic body."
    findings = [
        _assumption(statement, reviewer="r1"),
        _assumption(statement, reviewer="r2"),
        _assumption(statement, reviewer="r3"),
    ]

    class FailIfCalledJudge:
        def merge(self, cluster):  # noqa: ANN001
            raise AssertionError("judge must not run for exact duplicate collapse")

    result = aggregate_findings(findings, FailIfCalledJudge())

    assert len(result.findings) == 1
    assert result.findings[0].reviewer_votes == ["r1", "r2", "r3"]
    assert result.findings[0].agreement_count == 3
    assert result.ledger.rendered == (0,)
    assert result.ledger.collapsed == (1, 2)
    assert result.ledger.is_conserved()


def test_judge_merge_records_conservation_and_votes() -> None:
    findings = [
        _assumption("Region is unspecified in the Epic body.", reviewer="r1"),
        _assumption("The Epic body leaves region unspecified.", reviewer="r2"),
    ]

    result = aggregate_findings(findings, MockJudge())

    assert len(result.findings) == 1
    assert result.findings[0].reviewer_votes == ["r1", "r2"]
    assert result.findings[0].agreement_count == 2
    assert result.findings[0].statement.startswith("Merged:")
    assert len(result.ledger.merged) == 1
    assert result.ledger.merged[0].input_indices == (0, 1)
    assert result.ledger.merged[0].output_index == 0
    assert result.ledger.is_conserved()


def test_judge_schema_discard_is_accounted() -> None:
    findings = [
        _assumption("Region is unspecified in the Epic body.", reviewer="r1"),
        _assumption("The Epic body leaves region unspecified.", reviewer="r2"),
    ]

    result = aggregate_findings(findings, InvalidJudge())

    assert result.findings == []
    assert len(result.ledger.discarded) == 2
    assert all(
        record.reason == "judge_output_schema_discarded"
        for record in result.ledger.discarded
    )
    assert result.judge_discard_count >= 1
    assert result.ledger.is_conserved()


def test_agreement_counts_reproducible_on_fixed_input() -> None:
    findings = [
        _assumption("Region is unspecified in the Epic body.", reviewer="r1"),
        _assumption("The Epic body leaves region unspecified.", reviewer="r2"),
        _assumption("Quota budget is missing.", reviewer="r3"),
        _violation("Missing security posture reference.", reviewer="r4"),
        SafetyWarningFinding(
            statement="Prompt injection pattern detected.",
            evidence="Epic contains instruction override text.",
            blast_radius=BlastRadius.BR1,
            reviewer_votes=["r5"],
            agreement_count=1,
        ),
    ]

    first = aggregate_findings(findings, MockJudge())
    second = aggregate_findings(findings, MockJudge())

    assert first.findings == second.findings
    assert first.ledger == second.ledger
    assert [finding.agreement_count for finding in first.findings] == [1, 1, 1, 2]
    assert [finding.reviewer_votes for finding in first.findings] == [
        ["r4"],
        ["r5"],
        ["r3"],
        ["r1", "r2"],
    ]
    assert first.ledger.is_conserved()


def test_callable_judge_is_supported() -> None:
    findings = [
        _assumption("Region is unspecified in the Epic body.", reviewer="r1"),
        _assumption("The Epic body leaves region unspecified.", reviewer="r2"),
    ]

    def merge(cluster):  # noqa: ANN001
        primary = cluster[0]
        payload = primary.model_dump()
        payload["statement"] = f"Callable merged: {primary.statement}"
        return [payload]

    result = aggregate_findings(findings, merge)

    assert len(result.findings) == 1
    assert result.findings[0].statement.startswith("Callable merged:")
    assert result.ledger.is_conserved()
