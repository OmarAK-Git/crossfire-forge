"""Finding aggregation: lexical clustering, judge merge, conservation (FR-7, INV-6)."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Protocol

from rapidfuzz import fuzz

from crossfire_forge.reviewers.base import FINDING_ADAPTER, validate_findings
from crossfire_forge.schemas import Finding
from crossfire_forge.taxonomy import BlastRadius

THRESHOLD_JUSTIFICATION = (
    "Fixture-tuned against tests/fixtures/threshold_pairs.json (epic_* themes). "
    "All labeled duplicate paraphrase pairs score >=85 on rapidfuzz "
    "token_set_ratio; all labeled distinct cross-theme pairs score <=62. "
    "85 separates duplicate findings from distinct ones with margin below "
    "rapidfuzz's 100 ceiling."
)

DEFAULT_CLUSTER_THRESHOLD = 85


@dataclass(frozen=True)
class DiscardRecord:
    """Input finding discarded during aggregation with an explicit reason."""

    input_index: int
    reason: str


@dataclass(frozen=True)
class MergeRecord:
    """Input findings merged into one aggregated output finding."""

    input_indices: tuple[int, ...]
    output_index: int


@dataclass(frozen=True)
class ConservationLedger:
    """INV-6 accounting: every input index appears in exactly one bucket."""

    input_count: int
    merged: tuple[MergeRecord, ...]
    rendered: tuple[int, ...]
    collapsed: tuple[int, ...]
    discarded: tuple[DiscardRecord, ...]

    def accounted_indices(self) -> set[int]:
        indices: set[int] = set(self.rendered) | set(self.collapsed)
        for record in self.merged:
            indices.update(record.input_indices)
        for record in self.discarded:
            indices.add(record.input_index)
        return indices

    def is_conserved(self) -> bool:
        accounted = self.accounted_indices()
        return len(accounted) == self.input_count and accounted == set(
            range(self.input_count)
        )


@dataclass(frozen=True)
class AggregateResult:
    """Aggregated findings plus conservation ledger and judge discard metering."""

    findings: list[Finding]
    ledger: ConservationLedger
    judge_discard_count: int


class Judge(Protocol):
    """Merge a cluster of similar findings; return raw objects for schema-or-discard."""

    def merge(self, cluster: Sequence[Finding]) -> list[object]: ...


JudgeCallable = Callable[[Sequence[Finding]], list[object]]


def _statement_similarity(left: str, right: str) -> float:
    return float(fuzz.token_set_ratio(left.casefold(), right.casefold()))


def _finding_sort_key(finding: Finding) -> tuple[str, str, str]:
    return (finding.statement, finding.evidence, finding.type.value)


def cluster_findings(
    findings: Sequence[Finding],
    *,
    threshold: float = DEFAULT_CLUSTER_THRESHOLD,
) -> list[tuple[int, ...]]:
    """Group findings by lexical similarity using a deterministic greedy pass."""
    if not findings:
        return []

    order = sorted(range(len(findings)), key=lambda idx: _finding_sort_key(findings[idx]))
    clusters: list[tuple[int, ...]] = []
    assigned: set[int] = set()

    for anchor in order:
        if anchor in assigned:
            continue
        members = [anchor]
        assigned.add(anchor)
        anchor_statement = findings[anchor].statement
        for candidate in order:
            if candidate in assigned:
                continue
            if _statement_similarity(
                anchor_statement, findings[candidate].statement
            ) >= threshold:
                members.append(candidate)
                assigned.add(candidate)
        clusters.append(tuple(members))

    return clusters


def _combine_votes(cluster: Sequence[Finding]) -> tuple[list[str], int]:
    votes: list[str] = []
    seen: set[str] = set()
    for finding in cluster:
        for vote in finding.reviewer_votes:
            if vote not in seen:
                seen.add(vote)
                votes.append(vote)
    votes.sort()
    return votes, len(votes)


def _max_blast_radius(cluster: Sequence[Finding]) -> BlastRadius:
    order = {BlastRadius.BR1: 1, BlastRadius.BR2: 2, BlastRadius.BR3: 3}
    return max(cluster, key=lambda finding: order[finding.blast_radius]).blast_radius


def _apply_vote_metadata(finding: Finding, votes: list[str], agreement_count: int) -> Finding:
    data = finding.model_dump()
    data["reviewer_votes"] = votes
    data["agreement_count"] = agreement_count
    return FINDING_ADAPTER.validate_python(data)


def _call_judge(judge: Judge | JudgeCallable, cluster: Sequence[Finding]) -> list[object]:
    if hasattr(judge, "merge"):
        return judge.merge(cluster)  # type: ignore[union-attr]
    return judge(cluster)


def _collapse_exact_duplicates(
    findings: Sequence[Finding],
    indices: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...], Finding | None]:
    """Exact-statement duplicates collapse to one rendered finding without judge."""
    groups: dict[str, list[int]] = {}
    for idx in indices:
        groups.setdefault(findings[idx].statement, []).append(idx)

    if len(groups) == 1 and len(indices) > 1:
        canonical_idx = min(indices)
        collapsed = tuple(sorted(idx for idx in indices if idx != canonical_idx))
        cluster_findings_local = [findings[idx] for idx in indices]
        votes, agreement_count = _combine_votes(cluster_findings_local)
        rendered = _apply_vote_metadata(findings[canonical_idx], votes, agreement_count)
        return (canonical_idx,), collapsed, rendered

    return (), (), None


def aggregate_findings(
    findings: Sequence[Finding],
    judge: Judge | JudgeCallable,
    *,
    threshold: float = DEFAULT_CLUSTER_THRESHOLD,
) -> AggregateResult:
    """Cluster lexically, merge within clusters via judge, and account every input."""
    input_findings = list(findings)
    clusters = cluster_findings(input_findings, threshold=threshold)

    output: list[Finding] = []
    merged_records: list[MergeRecord] = []
    rendered_indices: list[int] = []
    collapsed_indices: list[int] = []
    discarded_records: list[DiscardRecord] = []
    judge_discard_count = 0

    for cluster_indices in clusters:
        cluster = [input_findings[idx] for idx in cluster_indices]

        if len(cluster_indices) == 1:
            rendered_indices.append(cluster_indices[0])
            output.append(cluster[0])
            continue

        rendered_idx, collapsed, collapsed_finding = _collapse_exact_duplicates(
            input_findings, cluster_indices
        )
        if collapsed_finding is not None:
            rendered_indices.extend(rendered_idx)
            collapsed_indices.extend(collapsed)
            output.append(collapsed_finding)
            continue

        raw = _call_judge(judge, cluster)
        validated = validate_findings(raw)
        judge_discard_count += validated.discard_count

        if not validated.findings:
            for idx in cluster_indices:
                discarded_records.append(
                    DiscardRecord(
                        input_index=idx,
                        reason="judge_output_schema_discarded",
                    )
                )
            continue

        merged_finding = validated.findings[0]
        votes, agreement_count = _combine_votes(cluster)
        data = merged_finding.model_dump()
        data["reviewer_votes"] = votes
        data["agreement_count"] = agreement_count
        data["blast_radius"] = _max_blast_radius(cluster)
        merged_finding = FINDING_ADAPTER.validate_python(data)

        output_index = len(output)
        output.append(merged_finding)
        merged_records.append(
            MergeRecord(input_indices=cluster_indices, output_index=output_index)
        )

    ledger = ConservationLedger(
        input_count=len(input_findings),
        merged=tuple(merged_records),
        rendered=tuple(rendered_indices),
        collapsed=tuple(collapsed_indices),
        discarded=tuple(discarded_records),
    )

    return AggregateResult(
        findings=output,
        ledger=ledger,
        judge_discard_count=judge_discard_count,
    )
