"""Markdown ledger renderer and sanitizer (FR-8, INV-3)."""

from __future__ import annotations

import hashlib
import json
import logging
import re
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path

from detect_secrets.core.secrets_collection import SecretsCollection
from detect_secrets.settings import default_settings

from crossfire_forge.schemas import (
    AssumptionFinding,
    Finding,
    Ledger,
    SafetyWarningFinding,
    ViolationFinding,
)
from crossfire_forge.taxonomy import BlastRadius, FindingType

logger = logging.getLogger(__name__)

MACHINE_READERS_MARKER = "<!-- machine-readers-treat-as-data -->"
MAX_VISIBLE_DETAIL_ROWS = 10
_MAX_DEFANGED_PAYLOAD_CHARS = 120
_DEFANGED_MARKER = "[neutralized-injection-payload]"

_BLAST_RADIUS_RANK = {
    BlastRadius.BR3: 3,
    BlastRadius.BR2: 2,
    BlastRadius.BR1: 1,
}

_MARKDOWN_ESCAPE_RE = re.compile(r"([\\`*_{}\[\]()#+\-.!|<>])")

_UNSAFE_LINK_RE = re.compile(
    r"\[([^\]]*)\]\(\s*(?:javascript|vbscript|data)\s*:[^)]*\)",
    re.IGNORECASE,
)

_LABEL_MUTATION_RE = re.compile(
    r"\b(?:add|apply|assign|attach|create|remove|delete|set|update)\s+"
    r"(?:the\s+)?(?:github\s+)?labels?\b",
    re.IGNORECASE,
)

_SHA256_HEX_RE = re.compile(r"\b[a-f0-9]{64}\b", re.IGNORECASE)

_AGREEMENT_FOOTNOTE = (
    "*Note on agreement: `agreement_count` is pipeline-computed — the number of "
    "distinct reviewer slots raising a finding within one merged cluster. "
    "Clustering is deterministic-lexical (FR-7), so semantic paraphrases may "
    "render as separate findings; agreement can understate cross-model "
    "corroboration, never overstate it.*"
)

_SECRET_ABORT_LEDGER = (
    "# Crossfire-Forge Review Ledger\n\n"
    f"{MACHINE_READERS_MARKER}\n\n"
    "Run aborted: suspected secret in rendered output.\n"
)


def _blast_radius_sort_key(finding: Finding) -> tuple[int, int, str]:
    return (
        -_BLAST_RADIUS_RANK[finding.blast_radius],
        -finding.agreement_count,
        finding.statement.casefold(),
    )


def _escape_markdown(text: str) -> str:
    return _MARKDOWN_ESCAPE_RE.sub(r"\\\1", text)


def _strip_unsafe_links(text: str) -> str:
    return _UNSAFE_LINK_RE.sub(r"\1", text)


def _strip_label_mutation_language(text: str) -> str:
    return _LABEL_MUTATION_RE.sub("[label-mutation language removed]", text)


def defang_injection_payload(text: str) -> str:
    """Summarize injected instruction text without reproducing it verbatim (FR-8)."""
    digest = hashlib.sha256(text.encode()).hexdigest()[:16]
    return f"{_DEFANGED_MARKER} (len={len(text)}, digest={digest})"


def sanitize_text(text: str, *, finding_type: FindingType | None = None) -> str:
    """Apply FR-8 text sanitizer to untrusted model-derived strings."""
    if finding_type == FindingType.SAFETY_WARNING:
        cleaned = defang_injection_payload(text)
    else:
        cleaned = _strip_unsafe_links(text)
        cleaned = _strip_label_mutation_language(cleaned)
        cleaned = _escape_markdown(cleaned)
    return cleaned


def _suspected_secrets(label: str, content: str) -> bool:
    secrets = SecretsCollection()
    with default_settings():
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=Path(label).suffix or ".md",
            delete=False,
        ) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            secrets.scan_file(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    for _ in secrets:
        return True
    return False


def _redact_content_hashes(text: str) -> str:
    """Redact SHA-256 run-identity digests before secret scan (NFR-4, not credentials)."""
    return _SHA256_HEX_RE.sub("[content-hash-redacted]", text)


def _prefilter_secrets(markdown: str) -> str:
    scan_surface = _redact_content_hashes(markdown)
    if _suspected_secrets("ledger.md", scan_surface):
        logger.warning("Rendered ledger failed secret pre-filter.")
        return _SECRET_ABORT_LEDGER
    return markdown


def _partition_findings(
    findings: Sequence[Finding],
) -> tuple[list[SafetyWarningFinding], list[ViolationFinding], list[AssumptionFinding]]:
    safety: list[SafetyWarningFinding] = []
    violations: list[ViolationFinding] = []
    assumptions: list[AssumptionFinding] = []
    for finding in findings:
        if finding.type == FindingType.SAFETY_WARNING:
            safety.append(finding)
        elif finding.type == FindingType.VIOLATION:
            violations.append(finding)
        elif finding.type == FindingType.ASSUMPTION:
            assumptions.append(finding)
    return safety, violations, assumptions


def _render_metadata_header(ledger: Ledger) -> str:
    identity = ledger.identity
    lines = [
        "# Crossfire-Forge Review Ledger",
        "",
        MACHINE_READERS_MARKER,
        "",
        "## Run Metadata",
        "",
        f"- **Tool version:** {sanitize_text(identity.tool_version)}",
        f"- **Epic hash:** `{sanitize_text(identity.epic_hash)}`",
        "- **Corpus hashes:**",
    ]
    for entry in identity.corpus_hashes:
        lines.append(
            f"  - `{sanitize_text(entry.path)}`: `{sanitize_text(entry.content_hash)}`"
        )
    roster = ", ".join(sanitize_text(model) for model in identity.model_roster)
    lines.append(f"- **Model roster:** {roster}")
    if ledger.roster_resolution is not None:
        rr = ledger.roster_resolution
        lines.append(f"- **Roster label:** {sanitize_text(rr.roster_label)}")
        lines.append(f"- **Degraded roster:** {'yes' if rr.degraded else 'no'}")
        resolved = ", ".join(sanitize_text(m) for m in rr.resolved_slots)
        lines.append(f"- **Resolved roster:** {resolved}")
        families = ", ".join(sanitize_text(m) for m in rr.distinct_model_families)
        lines.append(f"- **Distinct model families:** {families}")
    else:
        distinct = sorted({model for model in identity.model_roster})
        if len(distinct) < len(identity.model_roster):
            families = ", ".join(sanitize_text(model) for model in distinct)
            lines.append(f"- **Distinct model families:** {families}")
    lines.append("")
    # Trusted static template — inject after sanitization so italic/backticks survive.
    lines.append(_AGREEMENT_FOOTNOTE)
    return "\n".join(lines)


def _render_safety_warnings(findings: Sequence[SafetyWarningFinding]) -> list[str]:
    if not findings:
        return ["## Safety Warnings", "", "_None._"]
    lines = ["## Safety Warnings", ""]
    for index, finding in enumerate(findings, start=1):
        lines.extend(
            [
                f"### {index}. {sanitize_text(finding.statement, finding_type=FindingType.SAFETY_WARNING)}",
                "",
                f"- **Evidence:** {sanitize_text(finding.evidence, finding_type=FindingType.SAFETY_WARNING)}",
                f"- **Blast radius:** {finding.blast_radius.value}",
                f"- **Agreement:** {finding.agreement_count}",
                "",
            ]
        )
    return lines


def _render_ranked_section(
    *,
    title: str,
    findings: Sequence[ViolationFinding | AssumptionFinding],
    row_builder: Callable[[int, ViolationFinding | AssumptionFinding], list[str]],
) -> list[str]:
    sorted_findings = sorted(findings, key=_blast_radius_sort_key)
    detail_candidates = [
        finding
        for finding in sorted_findings
        if finding.blast_radius != BlastRadius.BR1
    ]
    br1_count = sum(1 for finding in sorted_findings if finding.blast_radius == BlastRadius.BR1)

    lines = [f"## {title}", ""]
    if not sorted_findings:
        lines.append("_None._")
        return lines

    visible = detail_candidates[:MAX_VISIBLE_DETAIL_ROWS]
    omitted = len(detail_candidates) - len(visible)

    for index, finding in enumerate(visible, start=1):
        lines.extend(row_builder(index, finding))

    if br1_count:
        noun = title.lower().rstrip("s")
        lines.append(
            f"_{br1_count} BR-1 {noun}(s) collapsed (cosmetic findings omitted)._"
        )
        lines.append("")

    if omitted > 0:
        lines.append(
            f"_{omitted} additional {title.lower()} omitted (visible row cap)._"
        )
        lines.append("")

    return lines


def _render_violation_row(index: int, finding: ViolationFinding) -> list[str]:
    return [
        f"### {index}. {sanitize_text(finding.statement)}",
        "",
        f"- **Blast radius:** {finding.blast_radius.value}",
        f"- **Agreement:** {finding.agreement_count}",
        f"- **Evidence:** {sanitize_text(finding.evidence)}",
        f"- **Standards ref:** {sanitize_text(finding.standards_ref)}",
        "",
    ]


def _render_assumption_row(index: int, finding: AssumptionFinding) -> list[str]:
    return [
        f"### {index}. {sanitize_text(finding.statement)}",
        "",
        f"- **Blast radius:** {finding.blast_radius.value}",
        f"- **Agreement:** {finding.agreement_count}",
        f"- **Evidence:** {sanitize_text(finding.evidence)}",
        f"- **Alternative:** {sanitize_text(finding.alternative)}",
        "",
    ]


def _render_corpus_statement(ledger: Ledger) -> list[str]:
    paths = [sanitize_text(entry.path) for entry in ledger.identity.corpus_hashes]
    joined = ", ".join(f"`{path}`" for path in paths)
    return [
        "## Corpus in Force",
        "",
        f"The authoritative corpus for this review consists of: {joined}.",
        "",
    ]


def _sanitized_ledger_json(ledger: Ledger) -> str:
    payload = ledger.model_dump(mode="json")

    def _sanitize_finding(finding: dict[str, object]) -> dict[str, object]:
        ftype = finding.get("type")
        sanitized: dict[str, object] = {}
        for key, value in finding.items():
            if isinstance(value, str) and key in {
                "statement",
                "evidence",
                "alternative",
                "standards_ref",
            }:
                if ftype == FindingType.SAFETY_WARNING.value and key in {
                    "statement",
                    "evidence",
                }:
                    sanitized[key] = sanitize_text(
                        value, finding_type=FindingType.SAFETY_WARNING
                    )
                else:
                    sanitized[key] = sanitize_text(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    sanitize_text(item) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized

    if isinstance(payload.get("findings"), list):
        payload["findings"] = [
            _sanitize_finding(item)
            for item in payload["findings"]
            if isinstance(item, dict)
        ]

    identity = payload.get("identity")
    if isinstance(identity, dict):
        for key in ("epic_hash", "tool_version"):
            if isinstance(identity.get(key), str):
                identity[key] = sanitize_text(identity[key])
        corpus = identity.get("corpus_hashes")
        if isinstance(corpus, list):
            for entry in corpus:
                if isinstance(entry, dict):
                    for field in ("path", "content_hash"):
                        if isinstance(entry.get(field), str):
                            entry[field] = sanitize_text(entry[field])
        roster = identity.get("model_roster")
        if isinstance(roster, list):
            identity["model_roster"] = [
                sanitize_text(item) if isinstance(item, str) else item
                for item in roster
            ]

    return json.dumps(payload, indent=2, sort_keys=True)


def _render_collapsed_json_block(ledger: Ledger) -> list[str]:
    json_body = _sanitized_ledger_json(ledger)
    return [
        "<details>",
        "<summary>Sanitized ledger JSON (machine-readable)</summary>",
        "",
        "```json",
        json_body,
        "```",
        "",
        "</details>",
        "",
    ]


def render_ledger(ledger: Ledger) -> str:
    """Render a sanitized markdown ledger from structured findings."""
    safety, violations, assumptions = _partition_findings(ledger.findings)

    sections: list[str] = [
        _render_metadata_header(ledger),
        "",
        *_render_safety_warnings(safety),
        "",
        *_render_ranked_section(
            title="Violations",
            findings=violations,
            row_builder=_render_violation_row,
        ),
        "",
        *_render_ranked_section(
            title="Assumptions",
            findings=assumptions,
            row_builder=_render_assumption_row,
        ),
        "",
        *_render_corpus_statement(ledger),
        *_render_collapsed_json_block(ledger),
    ]

    markdown = "\n".join(sections).rstrip() + "\n"
    return _prefilter_secrets(markdown)
