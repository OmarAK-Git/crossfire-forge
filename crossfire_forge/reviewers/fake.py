"""Deterministic fake reviewer for harness tests (AC-6 groundwork)."""

import hashlib
from typing import Literal

from crossfire_forge.prompts import ReviewerPrompt
from crossfire_forge.reviewers.base import ReviewResult, validate_findings
from crossfire_forge.taxonomy import BlastRadius, FindingType


def _prompt_digest(prompt: ReviewerPrompt) -> str:
    payload = f"{prompt.system}\0{prompt.user}".encode()
    return hashlib.sha256(payload).hexdigest()


class FakeReviewer:
    """Deterministic reviewer that emits schema-valid or non-compliant raw output."""

    def __init__(
        self,
        reviewer_id: str,
        *,
        non_compliant: bool = False,
        non_compliant_mode: Literal["schema", "json"] = "schema",
    ) -> None:
        self.reviewer_id = reviewer_id
        self.non_compliant = non_compliant
        self.non_compliant_mode = non_compliant_mode

    def review(self, prompt: ReviewerPrompt) -> ReviewResult:
        if self.non_compliant and self.non_compliant_mode == "json":
            return ReviewResult(findings=[], discard_count=1)

        raw = self._raw_findings(prompt)
        if self.non_compliant:
            raw.extend(self._invalid_schema_payloads())
        return validate_findings(raw)

    def _raw_findings(self, prompt: ReviewerPrompt) -> list[object]:
        digest = _prompt_digest(prompt)
        kind_index = int(digest[:2], 16) % 3
        kind = (
            FindingType.ASSUMPTION,
            FindingType.VIOLATION,
            FindingType.SAFETY_WARNING,
        )[kind_index]

        common = {
            "statement": (
                f"[{self.reviewer_id}] Deterministic finding "
                f"(digest={digest[:8]})."
            ),
            "evidence": "Derived from fixed prompt input via SHA-256 digest.",
            "blast_radius": BlastRadius.BR2,
            "reviewer_votes": [self.reviewer_id],
            "agreement_count": 1,
        }

        if kind == FindingType.ASSUMPTION:
            return [
                {
                    **common,
                    "type": FindingType.ASSUMPTION,
                    "alternative": "Specify RBAC scope before deployment.",
                }
            ]
        if kind == FindingType.VIOLATION:
            return [
                {
                    **common,
                    "type": FindingType.VIOLATION,
                    "standards_ref": "README.md#security-posture",
                }
            ]
        return [{**common, "type": FindingType.SAFETY_WARNING}]

    @staticmethod
    def _invalid_schema_payloads() -> list[object]:
        return [
            {"type": "violation", "statement": "x", "evidence": "y"},
            {"type": "risk", "statement": "x", "evidence": "y", "blast_radius": "BR-1"},
        ]
