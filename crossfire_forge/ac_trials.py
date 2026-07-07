"""Per-trial AC diagnostic artifact persistence (AC-2 instrumentation)."""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from crossfire_forge.ac_summary import TrialSummary
from crossfire_forge.harness import (
    AC1_K,
    AC1_N,
    AC2_K,
    AC2_N,
    AC3_K,
    AC3_N,
    evaluate_ac1,
    evaluate_ac2,
    evaluate_ac3,
    run_pass_k_of_n,
)
from crossfire_forge.schemas import Finding, Ledger

AC_TRIALS_REL_DIR = "artifacts/ac-trials"
ALL_AC_CRITERIA = ("AC-1", "AC-2", "AC-3")


@dataclass(frozen=True)
class CriterionSpec:
    criterion: str
    epic_fixture: str
    k: int
    n: int
    evaluator: Callable[..., bool]
    needs_rendered: bool = False


CRITERION_SPECS: dict[str, CriterionSpec] = {
    "AC-1": CriterionSpec(
        criterion="AC-1",
        epic_fixture="epic_441.md",
        k=AC1_K,
        n=AC1_N,
        evaluator=evaluate_ac1,
    ),
    "AC-2": CriterionSpec(
        criterion="AC-2",
        epic_fixture="epic_complete.md",
        k=AC2_K,
        n=AC2_N,
        evaluator=evaluate_ac2,
    ),
    "AC-3": CriterionSpec(
        criterion="AC-3",
        epic_fixture="epic_injection.md",
        k=AC3_K,
        n=AC3_N,
        evaluator=evaluate_ac3,
        needs_rendered=True,
    ),
}


def trial_dir_relative(criterion: str, trial_num: int) -> str:
    """Relative path for one trial's persisted ledger artifacts."""
    return f"{AC_TRIALS_REL_DIR}/{criterion}/trial-{trial_num}"


def diagnostic_summary_filename(criteria: Sequence[str]) -> str:
    """Summary JSON filename for criterion-filtered diagnostic runs."""
    if len(criteria) == 1:
        number = criteria[0].removeprefix("AC-")
        return f"ac{number}-diagnostic-summary.json"
    return "ac-diagnostic-summary.json"


def select_criteria(criteria_filter: Sequence[str] | None) -> tuple[str, ...]:
    """Return ordered criteria to run; default is AC-1..AC-3."""
    if not criteria_filter:
        return ALL_AC_CRITERIA
    unknown = [c for c in criteria_filter if c not in CRITERION_SPECS]
    if unknown:
        msg = f"unknown criteria: {', '.join(unknown)}"
        raise ValueError(msg)
    seen: set[str] = set()
    ordered: list[str] = []
    for criterion in criteria_filter:
        if criterion not in seen:
            seen.add(criterion)
            ordered.append(criterion)
    return tuple(ordered)


def serialize_finding(finding: Finding) -> dict[str, Any]:
    """Serialize one finding with the fields needed for AC-2 diagnostics."""
    data = finding.model_dump(mode="json")
    return {
        "type": data["type"],
        "statement": data["statement"],
        "evidence": data["evidence"],
        "blast_radius": data["blast_radius"],
        "reviewer_votes": data["reviewer_votes"],
        "agreement_count": data["agreement_count"],
        **{
            key: data[key]
            for key in ("alternative", "standards_ref")
            if key in data
        },
    }


def persist_trial_ledger(
    *,
    artifacts_root: Path,
    criterion: str,
    trial_num: int,
    epic_fixture: str,
    ledger: Ledger,
    rendered_markdown: str,
    passed: bool,
    roster_resolution: dict[str, Any],
) -> str:
    """Write rendered ledger markdown and findings JSON; return relative trial dir."""
    rel_dir = trial_dir_relative(criterion, trial_num)
    trial_dir = artifacts_root / rel_dir.removeprefix("artifacts/")
    trial_dir.mkdir(parents=True, exist_ok=True)

    (trial_dir / "ledger.md").write_text(rendered_markdown, encoding="utf-8")

    findings_payload = {
        "criterion": criterion,
        "trial": trial_num,
        "epic_fixture": epic_fixture,
        "passed": passed,
        "roster_resolution": roster_resolution,
        "findings": [serialize_finding(f) for f in ledger.findings],
    }
    (trial_dir / "findings.json").write_text(
        json.dumps(findings_payload, indent=2) + "\n",
        encoding="utf-8",
    )
    return rel_dir


def run_criterion_trials(
    *,
    spec: CriterionSpec,
    epic: Path,
    artifacts_root: Path,
    roster_resolution: dict[str, Any],
    trial_runner: Callable[[Path], tuple[Ledger, str]],
) -> TrialSummary:
    """Run N trials for one criterion, persisting each ledger to artifacts_root."""
    results: list[bool] = []
    finding_counts: list[int] = []
    artifact_dirs: list[str] = []

    for trial in range(1, spec.n + 1):
        print(
            f"[{spec.criterion}] trial {trial}/{spec.n} on {epic.name}...",
            flush=True,
        )
        ledger, rendered = trial_runner(epic)
        finding_counts.append(len(ledger.findings))
        if spec.needs_rendered:
            passed = spec.evaluator(ledger, rendered_markdown=rendered)
        else:
            passed = spec.evaluator(ledger)
        results.append(passed)
        print(f"  -> {'PASS' if passed else 'FAIL'}", flush=True)
        artifact_dirs.append(
            persist_trial_ledger(
                artifacts_root=artifacts_root,
                criterion=spec.criterion,
                trial_num=trial,
                epic_fixture=spec.epic_fixture,
                ledger=ledger,
                rendered_markdown=rendered,
                passed=passed,
                roster_resolution=roster_resolution,
            )
        )

    passed = run_pass_k_of_n(results, spec.k, spec.n)
    return TrialSummary(
        criterion=spec.criterion,
        k=spec.k,
        n=spec.n,
        trial_results=tuple(results),
        passed=passed,
        finding_counts=tuple(finding_counts),
        trial_artifact_dirs=tuple(artifact_dirs),
        provisional=spec.criterion == "AC-3",
        provisional_reason=(
            "AC-3 evaluator ruling provisional until human sign-off per R2"
            if spec.criterion == "AC-3"
            else None
        ),
    )
