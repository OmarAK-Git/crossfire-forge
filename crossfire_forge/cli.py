"""Crossfire-Forge CLI entrypoint."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from pathlib import Path

import typer

from crossfire_forge.aggregate import aggregate_findings
from crossfire_forge.hashing import build_run_identity
from crossfire_forge.input_loader import DEFAULT_CORPUS_PATHS, DEFAULT_FIXTURES_DIR, load_inputs
from crossfire_forge.layer0 import parse_layer0
from crossfire_forge.prompts import ReviewerPrompt, build_reviewer_prompt
from crossfire_forge.render import render_ledger
from crossfire_forge.reviewers.base import ReviewResult, collect_reviewer_results
from crossfire_forge.reviewers.fake import FakeReviewer
from crossfire_forge.safety import SafetyAbort, scan_pre_prompt
from crossfire_forge.schemas import Finding, Ledger

app = typer.Typer(
    name="crossfire-forge",
    help="Crossfire-Forge: contract-first Epic review harness.",
    no_args_is_help=True,
)


class _FirstFindingJudge:
    """Deterministic mock judge: emit the first finding in a cluster unchanged."""

    def merge(self, cluster: Sequence[Finding]) -> list[object]:
        return [cluster[0].model_dump(mode="json")]


def _collect_findings(
    reviewers: Sequence[FakeReviewer],
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
    fake_count: int,
    debug_raw_envelopes: bool = False,
) -> Ledger:
    """Execute the fake-reviewer review pipeline and return a structured ledger."""
    loaded = load_inputs(epic, corpus, fixtures_dir=fixtures_dir)
    scan_pre_prompt(epic_content=loaded.epic_content, corpus=loaded.corpus)

    layer0 = parse_layer0(loaded.epic_content)
    prompt = build_reviewer_prompt(loaded.epic_content, loaded.corpus, layer0.seeds)
    reviewers = [FakeReviewer(f"fake-reviewer-{index}") for index in range(1, fake_count + 1)]

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
    return Ledger(identity=identity, findings=aggregated.findings)


def run_review(
    epic: Path,
    *,
    corpus: list[str],
    fixtures_dir: Path,
    fake_count: int,
    debug_raw_envelopes: bool = False,
) -> str:
    """Execute the fake-reviewer review pipeline and return rendered ledger markdown."""
    ledger = build_review_ledger(
        epic,
        corpus=corpus,
        fixtures_dir=fixtures_dir,
        fake_count=fake_count,
        debug_raw_envelopes=debug_raw_envelopes,
    )
    return render_ledger(ledger)


@app.callback()
def main() -> None:
    """Crossfire-Forge CLI root."""


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
    fake_count: int = typer.Option(
        3,
        "--fake-count",
        min=1,
        help="Number of deterministic fake reviewers to run.",
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
) -> None:
    """Run end-to-end Epic review with deterministic fake reviewers."""
    try:
        markdown = run_review(
            epic,
            corpus=corpus,
            fixtures_dir=fixtures_dir,
            fake_count=fake_count,
            debug_raw_envelopes=debug_raw_envelopes,
        )
    except SafetyAbort as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    if output is not None:
        output.write_text(markdown, encoding="utf-8")
    typer.echo(markdown, nl=False)

