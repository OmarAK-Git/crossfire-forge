"""AC trial persistence and criterion-filtered diagnostic runs."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from crossfire_forge.ac_summary import build_ac_summary_payload, write_ac_summary
from crossfire_forge.ac_trials import (
    AC_TRIALS_REL_DIR,
    CRITERION_SPECS,
    diagnostic_summary_filename,
    persist_trial_ledger,
    run_criterion_trials,
    select_criteria,
    trial_dir_relative,
)
from crossfire_forge.cli import build_review_ledger
from crossfire_forge.harness import AC2_K, AC2_N
from crossfire_forge.taxonomy import BlastRadius
from crossfire_forge.render import render_ledger

FIXTURES_DIR = Path(__file__).parent / "fixtures"
EPIC_COMPLETE = FIXTURES_DIR / "epic_complete.md"
REPO_ARTIFACTS = Path(__file__).resolve().parents[1] / "artifacts"
LIVE_LEDGER_441 = REPO_ARTIFACTS / "ledger-441.md"


def test_select_criteria_defaults_to_all() -> None:
    assert select_criteria(None) == ("AC-1", "AC-2", "AC-3")


def test_select_criteria_filters_and_dedupes() -> None:
    assert select_criteria(["AC-2"]) == ("AC-2",)
    assert select_criteria(["AC-2", "AC-1", "AC-2"]) == ("AC-2", "AC-1")


def test_select_criteria_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="unknown criteria"):
        select_criteria(["AC-9"])


def test_diagnostic_summary_filename_single_criterion() -> None:
    assert diagnostic_summary_filename(["AC-2"]) == "ac2-diagnostic-summary.json"
    assert diagnostic_summary_filename(["AC-1", "AC-3"]) == "ac-diagnostic-summary.json"


def test_persist_trial_ledger_writes_markdown_and_findings(tmp_path: Path) -> None:
    ledger = build_review_ledger(
        EPIC_COMPLETE,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        provider="fake",
        reviewer_count=3,
    )
    rendered = render_ledger(ledger)
    roster_resolution = {
        "roster_label": "fake",
        "degraded": False,
        "resolved_slots": ["fake-reviewer-1", "fake-reviewer-2", "fake-reviewer-3"],
        "distinct_model_families": ["fake"],
    }

    rel_dir = persist_trial_ledger(
        artifacts_root=tmp_path,
        criterion="AC-2",
        trial_num=1,
        epic_fixture="epic_complete.md",
        ledger=ledger,
        rendered_markdown=rendered,
        passed=False,
        roster_resolution=roster_resolution,
    )

    assert rel_dir == trial_dir_relative("AC-2", 1)
    trial_dir = tmp_path / "ac-trials" / "AC-2" / "trial-1"
    assert (trial_dir / "ledger.md").read_text(encoding="utf-8") == rendered
    findings = json.loads((trial_dir / "findings.json").read_text(encoding="utf-8"))
    assert findings["criterion"] == "AC-2"
    assert findings["trial"] == 1
    assert findings["epic_fixture"] == "epic_complete.md"
    assert findings["passed"] is False
    assert findings["roster_resolution"] == roster_resolution
    assert len(findings["findings"]) == len(ledger.findings)
    for raw, finding in zip(findings["findings"], ledger.findings, strict=True):
        assert raw["type"] == finding.type.value
        assert raw["statement"] == finding.statement
        assert raw["evidence"] == finding.evidence
        assert raw["blast_radius"] == finding.blast_radius.value
        assert raw["reviewer_votes"] == finding.reviewer_votes
        assert raw["agreement_count"] == finding.agreement_count


def test_run_criterion_trials_persists_all_trials_with_fake_reviewer(tmp_path: Path) -> None:
    spec = CRITERION_SPECS["AC-2"]

    def fake_trial_runner(epic: Path):
        ledger = build_review_ledger(
            epic,
            corpus=["README.md"],
            fixtures_dir=FIXTURES_DIR,
            provider="fake",
            reviewer_count=3,
        )
        return ledger, render_ledger(ledger)

    summary = run_criterion_trials(
        spec=spec,
        epic=EPIC_COMPLETE,
        artifacts_root=tmp_path,
        roster_resolution={
            "roster_label": "fake",
            "degraded": False,
            "resolved_slots": ["fake-reviewer-1", "fake-reviewer-2", "fake-reviewer-3"],
            "distinct_model_families": ["fake"],
        },
        trial_runner=fake_trial_runner,
    )

    assert summary.criterion == "AC-2"
    assert summary.k == AC2_K
    assert summary.n == AC2_N
    assert len(summary.trial_results) == AC2_N
    assert summary.trial_artifact_dirs is not None
    assert len(summary.trial_artifact_dirs) == AC2_N
    assert summary.passed is (sum(summary.trial_results) >= AC2_K)

    for trial_num, rel_dir in enumerate(summary.trial_artifact_dirs, start=1):
        assert rel_dir == trial_dir_relative("AC-2", trial_num)
        trial_dir = tmp_path / "ac-trials" / "AC-2" / f"trial-{trial_num}"
        assert (trial_dir / "ledger.md").is_file()
        assert (trial_dir / "findings.json").is_file()


def test_diagnostic_summary_payload_omits_ledger_441_path(tmp_path: Path) -> None:
    from crossfire_forge.ac_summary import TrialSummary

    payload = build_ac_summary_payload(
        roster_label="fake",
        roster_resolution={
            "roster_label": "fake",
            "degraded": False,
            "resolved_slots": ["fake-reviewer-1"],
            "distinct_model_families": ["fake"],
        },
        trials=[
            TrialSummary(
                criterion="AC-2",
                k=4,
                n=5,
                trial_results=(False,) * 5,
                passed=False,
                trial_artifact_dirs=tuple(
                    trial_dir_relative("AC-2", trial) for trial in range(1, 6)
                ),
            )
        ],
        all_passed=False,
        include_ledger_441=False,
        trials_base_dir=AC_TRIALS_REL_DIR,
    )
    out = tmp_path / "ac2-diagnostic-summary.json"
    write_ac_summary(out, payload)
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert "ledger_441_path" not in loaded
    assert loaded["trials_base_dir"] == AC_TRIALS_REL_DIR
    assert loaded["trials"][0]["trial_artifact_dirs"][0] == trial_dir_relative("AC-2", 1)


def test_ac2_fake_reviewer_produces_br2_slot_stamped_findings() -> None:
    """Fake-reviewer trial machinery emits BR-2 findings with pipeline slot stamps.

    The evaluator verdict itself is covered by hand-built ledgers in
    test_harness.py; the fake reviewer's finding *type* varies with the prompt
    digest, so asserting a verdict here would couple the test to fixture bytes.
    """
    ledger = build_review_ledger(
        EPIC_COMPLETE,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        provider="fake",
        reviewer_count=3,
    )
    assert ledger.findings
    assert all(f.blast_radius == BlastRadius.BR2 for f in ledger.findings)
    for finding in ledger.findings:
        assert finding.reviewer_votes
        assert all(vote.startswith("slot-") for vote in finding.reviewer_votes)
        assert finding.agreement_count == len(set(finding.reviewer_votes))


def test_persistence_does_not_touch_live_ledger_441(tmp_path: Path) -> None:
    if not LIVE_LEDGER_441.is_file():
        pytest.skip("no committed ledger-441.md baseline to protect")

    before = LIVE_LEDGER_441.read_bytes()
    ledger = build_review_ledger(
        EPIC_COMPLETE,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        provider="fake",
        reviewer_count=1,
    )
    persist_trial_ledger(
        artifacts_root=tmp_path,
        criterion="AC-2",
        trial_num=99,
        epic_fixture="epic_complete.md",
        ledger=ledger,
        rendered_markdown=render_ledger(ledger),
        passed=False,
        roster_resolution={
            "roster_label": "fake",
            "degraded": False,
            "resolved_slots": ["fake-reviewer-1"],
            "distinct_model_families": ["fake"],
        },
    )
    assert LIVE_LEDGER_441.read_bytes() == before
    assert (tmp_path / "ac-trials" / "AC-2" / "trial-99" / "findings.json").is_file()
