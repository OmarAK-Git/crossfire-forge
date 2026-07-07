"""Reviewer provider interface and schema-or-discard validation (FR-6)."""

import json
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from pydantic import TypeAdapter, ValidationError

from crossfire_forge.prompts import ReviewerPrompt
from crossfire_forge.schemas import Finding

FINDING_ADAPTER = TypeAdapter(Finding)


@dataclass(frozen=True)
class ReviewResult:
    """Validated reviewer output with discard metering."""

    findings: list[Finding]
    discard_count: int


class Reviewer(Protocol):
    """Provider that reviews a prompt and returns schema-validated findings."""

    reviewer_id: str

    def review(self, prompt: ReviewerPrompt) -> ReviewResult: ...


def slot_vote_id(slot_index: int, reviewer_id: str) -> str:
    """Stable per-slot vote id, distinct even when one model fills two slots.

    Format ``slot-<n>:<model-id>`` (1-based). The slot index guarantees
    distinctness across roster slots; the model id keeps the vote human-readable.
    """
    return f"slot-{slot_index}:{reviewer_id}"


def stamp_finding_slot(finding: Finding, slot_id: str) -> Finding:
    """Overwrite pipeline-owned attribution on one finding (spec v0.5 §5, R-1).

    Any model-authored ``reviewer_votes``/``agreement_count`` are discarded as
    untrusted input; the collecting slot becomes the single source of truth
    (a singleton is one distinct reviewer slot, agreement 1).
    """
    data = finding.model_dump()
    data["reviewer_votes"] = [slot_id]
    data["agreement_count"] = 1
    return FINDING_ADAPTER.validate_python(data)


def validate_findings(raw: Sequence[object]) -> ReviewResult:
    """Validate each raw finding; discard schema-invalid items without repair."""
    findings: list[Finding] = []
    discard_count = 0
    for item in raw:
        try:
            findings.append(FINDING_ADAPTER.validate_python(item))
        except ValidationError:
            discard_count += 1
    return ReviewResult(findings=findings, discard_count=discard_count)


def _strip_markdown_fences(raw_output: str) -> str:
    """Remove optional ```json fences from model output."""
    stripped = raw_output.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def parse_reviewer_output(raw_output: str) -> ReviewResult:
    """Parse reviewer JSON output; meter JSON and schema failures as discards."""
    normalized = _strip_markdown_fences(raw_output)
    try:
        parsed = json.loads(normalized)
    except json.JSONDecodeError:
        return ReviewResult(findings=[], discard_count=1)

    if not isinstance(parsed, list):
        return ReviewResult(findings=[], discard_count=1)

    return validate_findings(parsed)


def collect_reviewer_results(
    reviewers: Sequence[Reviewer],
    prompt: ReviewerPrompt,
) -> ReviewResult:
    """Run N reviewers and aggregate schema-valid findings with discard totals.

    This is the single collection point where per-reviewer results are gathered
    for aggregation: every finding is stamped with its originating roster slot
    (spec v0.5 §5), so ``reviewer_votes``/``agreement_count`` become facts the
    pipeline computes, never text a model authors.
    """
    findings: list[Finding] = []
    discard_count = 0
    for index, reviewer in enumerate(reviewers, start=1):
        result = reviewer.review(prompt)
        slot_id = slot_vote_id(index, reviewer.reviewer_id)
        findings.extend(stamp_finding_slot(finding, slot_id) for finding in result.findings)
        discard_count += result.discard_count
    return ReviewResult(findings=findings, discard_count=discard_count)
