"""Crossfire-Forge CLI entrypoint."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Literal

import typer

from crossfire_forge.env_loader import load_local_dotenv
from crossfire_forge.aggregate import aggregate_findings
from crossfire_forge.hashing import build_run_identity
from crossfire_forge.input_loader import DEFAULT_CORPUS_PATHS, DEFAULT_FIXTURES_DIR, load_inputs
from crossfire_forge.layer0 import parse_layer0
from crossfire_forge.prompts import ReviewerPrompt, build_reviewer_prompt
from crossfire_forge.render import render_ledger
from crossfire_forge.reviewers.base import ReviewResult, Reviewer, collect_reviewer_results
from crossfire_forge.reviewers.anthropic import AnthropicReviewer
from crossfire_forge.reviewers.fake import FakeReviewer
from crossfire_forge.reviewers.vertex import VertexReviewer
from crossfire_forge.roster import ResolvedRoster, resolve_live_roster
from crossfire_forge.safety import SafetyAbort, scan_pre_prompt
from crossfire_forge.schemas import Finding, Ledger, RosterResolution
from crossfire_forge.vertex_config import VertexConfig, load_vertex_config

app = typer.Typer(
    name="crossfire-forge",
    help="Crossfire-Forge: contract-first Epic review harness.",
    no_args_is_help=True,
)

ProviderName = Literal["fake", "vertex", "mixed"]


class _FirstFindingJudge:
    """Deterministic mock judge: emit the first finding in a cluster unchanged."""

    def merge(self, cluster: Sequence[Finding]) -> list[object]:
        return [cluster[0].model_dump(mode="json")]


def build_fake_reviewers(count: int) -> list[FakeReviewer]:
    return [FakeReviewer(f"fake-reviewer-{index}") for index in range(1, count + 1)]


def build_vertex_reviewers(
    count: int,
    *,
    vertex_config: VertexConfig | None = None,
    model: str | None = None,
) -> list[VertexReviewer]:
    config = vertex_config or load_vertex_config()
    resolved_model = model or config.model
    return [
        VertexReviewer(
            project=config.project,
            location=config.location,
            model=resolved_model,
            reviewer_id=resolved_model,
        )
        for _ in range(count)
    ]


def build_mixed_reviewers(
    resolved: ResolvedRoster,
    *,
    vertex_config: VertexConfig | None = None,
) -> list[Reviewer]:
    config = vertex_config or load_vertex_config()
    reviewers: list[Reviewer] = []
    for slot in resolved.slots:
        if slot.provider == "vertex":
            reviewers.append(
                VertexReviewer(
                    project=config.project,
                    location=config.location,
                    model=slot.model_id,
                    reviewer_id=slot.model_id,
                )
            )
        elif slot.provider == "anthropic":
            reviewers.append(
                AnthropicReviewer(
                    model=slot.model_id,
                    reviewer_id=slot.model_id,
                )
            )
    return reviewers


def build_reviewers(
    provider: ProviderName,
    count: int,
    *,
    vertex_config: VertexConfig | None = None,
    allow_vertex_only: bool = False,
    resolved_roster: ResolvedRoster | None = None,
) -> list[Reviewer]:
    if provider == "fake":
        return build_fake_reviewers(count)
    if provider == "mixed":
        resolved = resolved_roster or resolve_live_roster(
            allow_vertex_only=allow_vertex_only
        )
        if count != len(resolved.slots):
            msg = f"mixed provider requires reviewer_count={len(resolved.slots)} (got {count})"
            raise ValueError(msg)
        return build_mixed_reviewers(resolved, vertex_config=vertex_config)
    return build_vertex_reviewers(count, vertex_config=vertex_config)


def _collect_findings(
    reviewers: Sequence[Reviewer],
    prompt: ReviewerPrompt,
    *,
    debug_raw_envelopes: bool,
) -> ReviewResult:
    if debug_raw_envelopes:
        findings: list[Finding] = []
        discard_count = 0
        for reviewer in reviewers:
            result = reviewer.review(prompt)
            envelope = {
                "reviewer_id": reviewer.reviewer_id,
                "findings": [
                    finding.model_dump(mode="json") for finding in result.findings
                ],
                "discard_count": result.discard_count,
            }
            print(json.dumps(envelope, sort_keys=True), file=sys.stderr)
            findings.extend(result.findings)
            discard_count += result.discard_count
        return ReviewResult(findings=findings, discard_count=discard_count)
    return collect_reviewer_results(reviewers, prompt)


def build_review_ledger(
    epic: Path,
    *,
    corpus: list[str],
    fixtures_dir: Path,
    provider: ProviderName = "fake",
    reviewer_count: int = 3,
    vertex_config: VertexConfig | None = None,
    debug_raw_envelopes: bool = False,
    allow_vertex_only: bool = False,
    resolved_roster: ResolvedRoster | None = None,
) -> Ledger:
    """Execute the review pipeline and return a structured ledger."""
    loaded = load_inputs(epic, corpus, fixtures_dir=fixtures_dir)
    scan_pre_prompt(epic_content=loaded.epic_content, corpus=loaded.corpus)

    layer0 = parse_layer0(loaded.epic_content)
    prompt = build_reviewer_prompt(loaded.epic_content, loaded.corpus, layer0.seeds)
    roster_meta: RosterResolution | None = None
    if provider == "mixed":
        resolved = resolved_roster or resolve_live_roster(
            allow_vertex_only=allow_vertex_only
        )
        roster_meta = RosterResolution(**resolved.to_metadata())
        reviewers = build_reviewers(
            provider,
            reviewer_count,
            vertex_config=vertex_config,
            allow_vertex_only=allow_vertex_only,
            resolved_roster=resolved,
        )
    else:
        reviewers = build_reviewers(
            provider,
            reviewer_count,
            vertex_config=vertex_config,
        )

    collected = _collect_findings(
        reviewers,
        prompt,
        debug_raw_envelopes=debug_raw_envelopes,
    )
    aggregated = aggregate_findings(collected.findings, _FirstFindingJudge())
    identity = build_run_identity(
        epic_content=loaded.epic_content,
        corpus=loaded.corpus,
        model_roster=[reviewer.reviewer_id for reviewer in reviewers],
    )
    return Ledger(
        identity=identity,
        findings=aggregated.findings,
        roster_resolution=roster_meta,
    )


def run_review(
    epic: Path,
    *,
    corpus: list[str],
    fixtures_dir: Path,
    provider: ProviderName = "fake",
    reviewer_count: int = 3,
    vertex_config: VertexConfig | None = None,
    debug_raw_envelopes: bool = False,
    allow_vertex_only: bool = False,
    resolved_roster: ResolvedRoster | None = None,
) -> str:
    """Execute the review pipeline and return rendered ledger markdown."""
    ledger = build_review_ledger(
        epic,
        corpus=corpus,
        fixtures_dir=fixtures_dir,
        provider=provider,
        reviewer_count=reviewer_count,
        vertex_config=vertex_config,
        debug_raw_envelopes=debug_raw_envelopes,
        allow_vertex_only=allow_vertex_only,
        resolved_roster=resolved_roster,
    )
    return render_ledger(ledger)


@app.callback()
def main() -> None:
    """Crossfire-Forge CLI root."""
    load_local_dotenv()


@app.command("hashes")
def print_hashes(
    epic: Path = typer.Argument(..., help="Path to Epic markdown file."),
    corpus: list[str] = typer.Option(
        list(DEFAULT_CORPUS_PATHS),
        "--corpus",
        help="Ordered corpus paths relative to --fixtures-dir.",
    ),
    fixtures_dir: Path = typer.Option(
        DEFAULT_FIXTURES_DIR,
        "--fixtures-dir",
        help="Base directory for corpus files.",
    ),
) -> None:
    """Print stable content hashes for a loaded Epic and corpus."""
    loaded = load_inputs(epic, corpus, fixtures_dir=fixtures_dir)
    typer.echo(f"epic\t{loaded.epic_path}\t{loaded.epic_hash}")
    for entry in loaded.corpus_hashes:
        typer.echo(f"corpus\t{entry.path}\t{entry.content_hash}")


@app.command("review")
def review(
    epic: Path = typer.Argument(..., help="Path to Epic markdown file."),
    corpus: list[str] = typer.Option(
        list(DEFAULT_CORPUS_PATHS),
        "--corpus",
        help="Ordered corpus paths relative to --fixtures-dir.",
    ),
    fixtures_dir: Path = typer.Option(
        DEFAULT_FIXTURES_DIR,
        "--fixtures-dir",
        help="Base directory for corpus files.",
    ),
    provider: ProviderName = typer.Option(
        "fake",
        "--provider",
        help="Reviewer backend: fake (CI), vertex (single-model live), or mixed (multi-family live).",
    ),
    reviewer_count: int = typer.Option(
        3,
        "--reviewer-count",
        min=1,
        help="Number of reviewers to run.",
    ),
    fake_count: int | None = typer.Option(
        None,
        "--fake-count",
        min=1,
        help="Deprecated alias for --reviewer-count when --provider fake.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional path to write rendered ledger markdown.",
    ),
    debug_raw_envelopes: bool = typer.Option(
        False,
        "--debug-raw-envelopes",
        help="Print raw reviewer envelopes to stderr (local development only).",
    ),
    allow_vertex_only: bool = typer.Option(
        False,
        "--allow-vertex-only",
        help="With --provider mixed: allow degraded Vertex-only roster when Anthropic key missing.",
    ),
) -> None:
    """Run end-to-end Epic review."""
    count = fake_count if fake_count is not None else reviewer_count
    try:
        markdown = run_review(
            epic,
            corpus=corpus,
            fixtures_dir=fixtures_dir,
            provider=provider,
            reviewer_count=count,
            debug_raw_envelopes=debug_raw_envelopes,
            allow_vertex_only=allow_vertex_only,
        )
    except SafetyAbort as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc

    if output is not None:
        output.write_text(markdown, encoding="utf-8")
    typer.echo(markdown, nl=False)
