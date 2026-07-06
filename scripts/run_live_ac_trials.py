"""Run live mixed-roster pass-K-of-N acceptance trials (spec §11 AC-1..AC-3)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from crossfire_forge.ac_summary import TrialSummary, build_ac_summary_payload, write_ac_summary
from crossfire_forge.cli import build_review_ledger, run_review
from crossfire_forge.env_loader import load_local_dotenv
from crossfire_forge.harness import (
    AC1_K,
    AC1_N,
    AC2_K,
    AC2_N,
    AC3_K,
    AC3_N,
    LEDGER_441_PATH,
    evaluate_ac1,
    evaluate_ac2,
    evaluate_ac3,
    run_pass_k_of_n,
)
from crossfire_forge.input_loader import DEFAULT_CORPUS_PATHS, DEFAULT_FIXTURES_DIR
from crossfire_forge.render import render_ledger
from crossfire_forge.roster import ResolvedRoster, resolve_live_roster
from crossfire_forge.vertex_config import load_vertex_config

FIXTURES_DIR = DEFAULT_FIXTURES_DIR
CORPUS = list(DEFAULT_CORPUS_PATHS)
EPIC_441 = FIXTURES_DIR / "epic_441.md"
EPIC_COMPLETE = FIXTURES_DIR / "epic_complete.md"
EPIC_INJECTION = FIXTURES_DIR / "epic_injection.md"
ARTIFACTS_DIR = Path(__file__).resolve().parents[1] / "artifacts"
RESULTS_PATH = ARTIFACTS_DIR / "live-ac-summary.json"
BASELINE_PATH = ARTIFACTS_DIR / "single-family-baseline.json"


def _archive_single_family_baseline() -> None:
    """Retain prior single-family results when regenerating mixed-roster summary."""
    if not RESULTS_PATH.is_file() or BASELINE_PATH.is_file():
        return
    import json

    existing = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    if existing.get("roster_label") != "mixed":
        baseline = {**existing, "roster_label": "single-family-baseline"}
        BASELINE_PATH.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")


def _run_trials(
    *,
    criterion: str,
    epic: Path,
    k: int,
    n: int,
    evaluator,
    resolved: ResolvedRoster,
    allow_vertex_only: bool,
) -> TrialSummary:
    results: list[bool] = []
    finding_counts: list[int] = []
    for trial in range(1, n + 1):
        print(f"[{criterion}] trial {trial}/{n} on {epic.name}...", flush=True)
        ledger = build_review_ledger(
            epic,
            corpus=CORPUS,
            fixtures_dir=FIXTURES_DIR,
            provider="mixed",
            reviewer_count=len(resolved.slots),
            vertex_config=load_vertex_config(),
            allow_vertex_only=allow_vertex_only,
            resolved_roster=resolved,
        )
        rendered = render_ledger(ledger)
        finding_counts.append(len(ledger.findings))
        if criterion == "AC-3":
            results.append(evaluator(ledger, rendered_markdown=rendered))
        else:
            results.append(evaluator(ledger))
        print(f"  -> {'PASS' if results[-1] else 'FAIL'}", flush=True)
    passed = run_pass_k_of_n(results, k, n)
    return TrialSummary(
        criterion=criterion,
        k=k,
        n=n,
        trial_results=tuple(results),
        passed=passed,
        finding_counts=tuple(finding_counts),
        provisional=criterion == "AC-3",
        provisional_reason=(
            "AC-3 evaluator ruling provisional until human sign-off per R2"
            if criterion == "AC-3"
            else None
        ),
    )


def main(argv: list[str] | None = None) -> int:
    load_local_dotenv()
    parser = argparse.ArgumentParser(description="Run live mixed-roster AC-1..AC-3 trials")
    parser.add_argument(
        "--allow-vertex-only",
        action="store_true",
        help="Allow degraded Vertex-only roster when ANTHROPIC_API_KEY is unset.",
    )
    args = parser.parse_args(argv)

    _archive_single_family_baseline()

    resolved = resolve_live_roster(allow_vertex_only=args.allow_vertex_only)
    print(
        f"Resolved roster [{resolved.roster_label}]: "
        f"{', '.join(resolved.distinct_model_families)} "
        f"({len(resolved.slots)} reviewers, degraded={resolved.degraded})",
        flush=True,
    )

    summaries = [
        _run_trials(
            criterion="AC-1",
            epic=EPIC_441,
            k=AC1_K,
            n=AC1_N,
            evaluator=evaluate_ac1,
            resolved=resolved,
            allow_vertex_only=args.allow_vertex_only,
        ),
        _run_trials(
            criterion="AC-2",
            epic=EPIC_COMPLETE,
            k=AC2_K,
            n=AC2_N,
            evaluator=evaluate_ac2,
            resolved=resolved,
            allow_vertex_only=args.allow_vertex_only,
        ),
        _run_trials(
            criterion="AC-3",
            epic=EPIC_INJECTION,
            k=AC3_K,
            n=AC3_N,
            evaluator=evaluate_ac3,
            resolved=resolved,
            allow_vertex_only=args.allow_vertex_only,
        ),
    ]

    print("Regenerating artifacts/ledger-441.md from resolved roster...", flush=True)
    markdown = run_review(
        EPIC_441,
        corpus=CORPUS,
        fixtures_dir=FIXTURES_DIR,
        provider="mixed",
        reviewer_count=len(resolved.slots),
        vertex_config=load_vertex_config(),
        allow_vertex_only=args.allow_vertex_only,
        resolved_roster=resolved,
    )
    LEDGER_441_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_441_PATH.write_text(markdown, encoding="utf-8")

    payload = build_ac_summary_payload(
        roster_label=resolved.roster_label,
        roster_resolution=resolved.to_metadata(),
        trials=summaries,
        all_passed=all(summary.passed for summary in summaries),
        epic_fixtures={
            "AC-1": "epic_441.md",
            "AC-2": "epic_complete.md",
            "AC-3": "epic_injection.md",
        },
    )
    write_ac_summary(RESULTS_PATH, payload)

    for summary in summaries:
        status = "PASS" if summary.passed else "FAIL"
        print(f"{summary.criterion}: {status} ({summary.trial_results})", flush=True)
    print(f"Summary written to {RESULTS_PATH.relative_to(ARTIFACTS_DIR.parent)}", flush=True)
    print(f"Ledger written to {LEDGER_441_PATH.relative_to(ARTIFACTS_DIR.parent)}", flush=True)
    return 0 if payload["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
