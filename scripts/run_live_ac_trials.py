"""Run live mixed-roster pass-K-of-N acceptance trials (spec §11 AC-1..AC-3)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from pathlib import Path

from crossfire_forge.ac_summary import build_ac_summary_payload, write_ac_summary
from crossfire_forge.ac_trials import (
    AC_TRIALS_REL_DIR,
    CRITERION_SPECS,
    diagnostic_summary_filename,
    run_criterion_trials,
    select_criteria,
)
from crossfire_forge.cli import build_review_ledger, run_review
from crossfire_forge.env_loader import load_local_dotenv
from crossfire_forge.harness import LEDGER_441_PATH
from crossfire_forge.input_loader import DEFAULT_CORPUS_PATHS, DEFAULT_FIXTURES_DIR
from crossfire_forge.render import render_ledger
from crossfire_forge.roster import resolve_live_roster
from crossfire_forge.schemas import Ledger
from crossfire_forge.vertex_config import load_vertex_config

FIXTURES_DIR = DEFAULT_FIXTURES_DIR
CORPUS = list(DEFAULT_CORPUS_PATHS)
EPIC_441 = FIXTURES_DIR / "epic_441.md"
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


def _make_trial_runner(
    *,
    corpus: list[str],
    fixtures_dir: Path,
    provider: str,
    reviewer_count: int,
    vertex_config,
    allow_vertex_only: bool,
    resolved,
) -> Callable[[Path], tuple[Ledger, str]]:
    def trial_runner(epic: Path) -> tuple[Ledger, str]:
        ledger = build_review_ledger(
            epic,
            corpus=corpus,
            fixtures_dir=fixtures_dir,
            provider=provider,  # type: ignore[arg-type]
            reviewer_count=reviewer_count,
            vertex_config=vertex_config,
            allow_vertex_only=allow_vertex_only,
            resolved_roster=resolved,
        )
        return ledger, render_ledger(ledger)

    return trial_runner


def main(argv: list[str] | None = None) -> int:
    load_local_dotenv()
    parser = argparse.ArgumentParser(description="Run live mixed-roster AC-1..AC-3 trials")
    parser.add_argument(
        "--allow-vertex-only",
        action="store_true",
        help="Allow degraded Vertex-only roster when ANTHROPIC_API_KEY is unset.",
    )
    parser.add_argument(
        "--criterion",
        action="append",
        choices=tuple(CRITERION_SPECS),
        metavar="CRITERION",
        help=(
            "Run only selected criteria (repeatable). "
            "Skips ledger-441 regeneration and writes a diagnostic summary artifact."
        ),
    )
    args = parser.parse_args(argv)

    criteria = select_criteria(args.criterion)
    diagnostic_mode = args.criterion is not None

    if not diagnostic_mode:
        _archive_single_family_baseline()

    resolved = resolve_live_roster(allow_vertex_only=args.allow_vertex_only)
    print(
        f"Resolved roster [{resolved.roster_label}]: "
        f"{', '.join(resolved.distinct_model_families)} "
        f"({len(resolved.slots)} reviewers, degraded={resolved.degraded})",
        flush=True,
    )

    roster_resolution = resolved.to_metadata()
    trial_runner = _make_trial_runner(
        corpus=CORPUS,
        fixtures_dir=FIXTURES_DIR,
        provider="mixed",
        reviewer_count=len(resolved.slots),
        vertex_config=load_vertex_config(),
        allow_vertex_only=args.allow_vertex_only,
        resolved=resolved,
    )

    summaries = []
    for criterion in criteria:
        spec = CRITERION_SPECS[criterion]
        epic = FIXTURES_DIR / spec.epic_fixture
        print(f"Running {criterion} ({spec.k}-of-{spec.n}) on {spec.epic_fixture}...", flush=True)
        summary = run_criterion_trials(
            spec=spec,
            epic=epic,
            artifacts_root=ARTIFACTS_DIR,
            roster_resolution=roster_resolution,
            trial_runner=trial_runner,
        )
        for trial_num, passed in enumerate(summary.trial_results, start=1):
            status = "PASS" if passed else "FAIL"
            count = summary.finding_counts[trial_num - 1] if summary.finding_counts else 0
            print(
                f"  trial {trial_num}/{spec.n}: {status} ({count} findings)",
                flush=True,
            )
        summaries.append(summary)

    if not diagnostic_mode:
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

    results_path = (
        ARTIFACTS_DIR / diagnostic_summary_filename(criteria)
        if diagnostic_mode
        else RESULTS_PATH
    )
    payload = build_ac_summary_payload(
        roster_label=resolved.roster_label,
        roster_resolution=roster_resolution,
        trials=summaries,
        all_passed=all(summary.passed for summary in summaries),
        epic_fixtures={
            criterion: CRITERION_SPECS[criterion].epic_fixture for criterion in criteria
        },
        include_ledger_441=not diagnostic_mode,
        trials_base_dir=AC_TRIALS_REL_DIR,
    )
    write_ac_summary(results_path, payload)

    for summary in summaries:
        status = "PASS" if summary.passed else "FAIL"
        print(f"{summary.criterion}: {status} ({summary.trial_results})", flush=True)
    print(f"Summary written to {results_path.relative_to(ARTIFACTS_DIR.parent)}", flush=True)
    if not diagnostic_mode:
        print(f"Ledger written to {LEDGER_441_PATH.relative_to(ARTIFACTS_DIR.parent)}", flush=True)
    return 0 if payload["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
