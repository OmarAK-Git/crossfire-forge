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

    def review(self, prompt: ReviewerPrompt) -> ReviewResult: ...


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


def parse_reviewer_output(raw_output: str) -> ReviewResult:
    """Parse reviewer JSON output; meter JSON and schema failures as discards."""
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError:
        return ReviewResult(findings=[], discard_count=1)

    if not isinstance(parsed, list):
        return ReviewResult(findings=[], discard_count=1)

    return validate_findings(parsed)


def collect_reviewer_results(
    reviewers: Sequence[Reviewer],
    prompt: ReviewerPrompt,
) -> ReviewResult:
    """Run N reviewers and aggregate schema-valid findings with discard totals."""
    findings: list[Finding] = []
    discard_count = 0
    for reviewer in reviewers:
        result = reviewer.review(prompt)
        findings.extend(result.findings)
        discard_count += result.discard_count
    return ReviewResult(findings=findings, discard_count=discard_count)
