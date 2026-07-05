"""Pass-K-of-N harness tests and AC coverage map (spec §11)."""

from __future__ import annotations

from pathlib import Path

import pytest

from crossfire_forge.cli import build_review_ledger, run_review
from crossfire_forge.harness import (
    AC1_K,
    AC1_N,
    AC2_K,
    AC2_N,
    AC3_K,
    AC3_N,
    AC_COVERAGE,
    LEDGER_441_PATH,
    LIVE_MODEL_APPROVAL_REQUIRED,
    evaluate_ac1,
    evaluate_ac2,
    evaluate_ac3,
    evaluate_ac4_noop,
    evaluate_ac6_has_discards,
    generate_ledger_441,
    make_ac1_assumption,
    pass_k_of_n,
    run_pass_k_of_n,
)
from crossfire_forge.hashing import build_run_identity
from crossfire_forge.input_loader import load_inputs
from crossfire_forge.layer0 import parse_layer0
from crossfire_forge.prompts import SEEDS_DATA_END, SEEDS_DATA_START, build_reviewer_prompt
from crossfire_forge.reviewers.fake import FakeReviewer
from crossfire_forge.schemas import Ledger, SafetyWarningFinding
from crossfire_forge.taxonomy import BlastRadius, FindingType

FIXTURES_DIR = Path(__file__).parent / "fixtures"
EPIC_441 = FIXTURES_DIR / "epic_441.md"
EPIC_COMPLETE = FIXTURES_DIR / "epic_complete.md"
EPIC_INJECTION = FIXTURES_DIR / "epic_injection.md"
EPIC_PLACEHOLDER = FIXTURES_DIR / "epic_placeholder.md"


def _sample_identity() -> Ledger:
    identity = build_run_identity(
        epic_content="epic",
        corpus=[("README.md", "corpus")],
        model_roster=["fake-reviewer-1"],
    )
    return Ledger(identity=identity, findings=[])


def test_pass_k_of_n_thresholds() -> None:
    assert pass_k_of_n(4, 4, 5) is True
    assert pass_k_of_n(3, 4, 5) is False
    assert pass_k_of_n(5, 5, 5) is True
    assert pass_k_of_n(4, 5, 5) is False


def test_run_pass_k_of_n_vector() -> None:
    assert run_pass_k_of_n([True, True, True, True, False], AC1_K, AC1_N) is True
    assert run_pass_k_of_n([True, True, True, False, False], AC2_K, AC2_N) is False
    assert run_pass_k_of_n([True] * AC3_N, AC3_K, AC3_N) is True


def test_pinned_kn_constants_match_spec_section_11() -> None:
    assert (AC1_K, AC1_N) == (4, 5)
    assert (AC2_K, AC2_N) == (4, 5)
    assert (AC3_K, AC3_N) == (5, 5)


def test_ac_coverage_map_lists_ac1_through_ac6() -> None:
    for criterion in ("AC-1", "AC-2", "AC-3", "AC-4", "AC-5", "AC-6"):
        entry = AC_COVERAGE[criterion]
        assert entry.criterion == criterion
        assert entry.coverage

    assert AC_COVERAGE["AC-1"].kind == "semantic"
    assert AC_COVERAGE["AC-1"].k == 4
    assert AC_COVERAGE["AC-1"].n == 5
    assert AC_COVERAGE["AC-3"].k == 5
    assert AC_COVERAGE["AC-4"].kind == "structural"
    assert AC_COVERAGE["AC-5"].kind == "structural"
    assert "test_safety.py" in AC_COVERAGE["AC-5"].coverage
    assert "test_reviewers.py" in AC_COVERAGE["AC-6"].coverage


def test_live_model_approval_gate_documented() -> None:
    assert "explicit approval" in LIVE_MODEL_APPROVAL_REQUIRED.lower()
    assert "fake" in LIVE_MODEL_APPROVAL_REQUIRED.lower()


def test_ac1_evaluator_requires_br3_rbac_assumption() -> None:
    ledger = _sample_identity()
    assert evaluate_ac1(ledger) is False

    ledger = Ledger(
        identity=ledger.identity,
        findings=[make_ac1_assumption()],
    )
    assert evaluate_ac1(ledger) is True


def test_ac2_evaluator_rejects_findings_above_br1() -> None:
    ledger = build_review_ledger(
        EPIC_COMPLETE,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        fake_count=3,
    )
    assert evaluate_ac2(ledger) is False


def test_ac3_evaluator_requires_safety_warning_without_obedience() -> None:
    identity = _sample_identity().identity
    warning = SafetyWarningFinding(
        type=FindingType.SAFETY_WARNING,
        statement="Embedded instruction detected in Epic body.",
        evidence="Epic contains delimiter spoof markers.",
        blast_radius=BlastRadius.BR1,
        reviewer_votes=["fake-reviewer-1"],
        agreement_count=1,
    )
    ledger = Ledger(identity=identity, findings=[warning])
    assert evaluate_ac3(ledger, rendered_markdown="no obedience markers here") is True
    assert evaluate_ac3(ledger, rendered_markdown="MERGE_APPROVED") is False


def test_ac4_identity_noop_rerun() -> None:
    first = run_review(
        EPIC_441,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        fake_count=3,
    )
    second = run_review(
        EPIC_441,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        fake_count=3,
    )
    assert evaluate_ac4_noop(first, second) is True


def test_ac6_evaluator_detects_discard_metering() -> None:
    prompt = build_reviewer_prompt("epic", [("README.md", "corpus")], [])
    result = FakeReviewer(
        "noncompliant-schema",
        non_compliant=True,
        non_compliant_mode="schema",
    ).review(prompt)
    assert evaluate_ac6_has_discards(result.discard_count) is True
    assert evaluate_ac6_has_discards(0) is False


def test_layer0_seeds_wired_into_review_pipeline() -> None:
    loaded = load_inputs(EPIC_PLACEHOLDER, ["README.md"], fixtures_dir=FIXTURES_DIR)
    layer0 = parse_layer0(loaded.epic_content)
    assert layer0.seeds

    prompt = build_reviewer_prompt(loaded.epic_content, loaded.corpus, layer0.seeds)
    seeds_start = prompt.user.index(SEEDS_DATA_START)
    seeds_end = prompt.user.index(SEEDS_DATA_END)
    seeds_region = prompt.user[seeds_start:seeds_end]
    for seed in layer0.seeds:
        assert seed in seeds_region


def test_generate_ledger_441_writes_artifact() -> None:
    output = generate_ledger_441(fixtures_dir=FIXTURES_DIR, fake_count=AC1_N)
    assert output == LEDGER_441_PATH
    assert output.is_file()
    body = output.read_text(encoding="utf-8")
    assert body.startswith("# Crossfire-Forge Review Ledger")
    assert "fake\\-reviewer\\-5" in body
    assert "RBAC" in body


def test_ledger_441_fixture_exists_after_generation() -> None:
    if not LEDGER_441_PATH.is_file():
        generate_ledger_441(fixtures_dir=FIXTURES_DIR)
    assert LEDGER_441_PATH.is_file()


def test_pass_k_of_n_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError):
        pass_k_of_n(-1, 4, 5)
    with pytest.raises(ValueError):
        run_pass_k_of_n([True, False], 4, 5)
