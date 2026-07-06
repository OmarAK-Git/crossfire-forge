"""Run live Vertex pass-K-of-N acceptance trials (spec §11 AC-1..AC-3)."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from crossfire_forge.cli import build_review_ledger, run_review
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
from crossfire_forge.vertex_config import load_vertex_config

FIXTURES_DIR = DEFAULT_FIXTURES_DIR
CORPUS = list(DEFAULT_CORPUS_PATHS)
EPIC_441 = FIXTURES_DIR / "epic_441.md"
EPIC_COMPLETE = FIXTURES_DIR / "epic_complete.md"
EPIC_INJECTION = FIXTURES_DIR / "epic_injection.md"
RESULTS_PATH = Path(__file__).resolve().parents[1] / "artifacts" / "live-ac-summary.json"


@dataclass(frozen=True)
class TrialSummary:
    criterion: str
    k: int
    n: int
    trial_results: tuple[bool, ...]
    passed: bool


def _run_trials(
    *,
    criterion: str,
    epic: Path,
    k: int,
    n: int,
    evaluator,
) -> TrialSummary:
    results: list[bool] = []
    for trial in range(1, n + 1):
        print(f"[{criterion}] trial {trial}/{n} on {epic.name}...", flush=True)
        config = load_vertex_config()
        ledger = build_review_ledger(
            epic,
            corpus=CORPUS,
            fixtures_dir=FIXTURES_DIR,
            provider="vertex",
            reviewer_count=3,
            vertex_config=config,
        )
        rendered = render_ledger(ledger)
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
    )


def main() -> int:
    print("Loading Vertex config from gcloud defaults...", flush=True)
    config = load_vertex_config()
    print(
        f"project={config.project} location={config.location} model={config.model}",
        flush=True,
    )

    summaries = [
        _run_trials(
            criterion="AC-1",
            epic=EPIC_441,
            k=AC1_K,
            n=AC1_N,
            evaluator=evaluate_ac1,
        ),
        _run_trials(
            criterion="AC-2",
            epic=EPIC_COMPLETE,
            k=AC2_K,
            n=AC2_N,
            evaluator=evaluate_ac2,
        ),
        _run_trials(
            criterion="AC-3",
            epic=EPIC_INJECTION,
            k=AC3_K,
            n=AC3_N,
            evaluator=evaluate_ac3,
        ),
    ]

    print("Regenerating artifacts/ledger-441.md from live Vertex...", flush=True)
    markdown = run_review(
        EPIC_441,
        corpus=CORPUS,
        fixtures_dir=FIXTURES_DIR,
        provider="vertex",
        reviewer_count=AC1_N,
        vertex_config=load_vertex_config(),
    )
    LEDGER_441_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_441_PATH.write_text(markdown, encoding="utf-8")

    payload = {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "vertex_project": config.project,
        "vertex_location": config.location,
        "vertex_model": config.model,
        "trials": [asdict(summary) for summary in summaries],
        "all_passed": all(summary.passed for summary in summaries),
        "ledger_441_path": str(LEDGER_441_PATH),
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    for summary in summaries:
        status = "PASS" if summary.passed else "FAIL"
        print(f"{summary.criterion}: {status} ({summary.trial_results})", flush=True)
    print(f"Summary written to {RESULTS_PATH}", flush=True)
    print(f"Ledger written to {LEDGER_441_PATH}", flush=True)
    return 0 if payload["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
