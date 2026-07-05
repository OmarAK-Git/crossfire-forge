"""Threshold tuning tests for Phase 2 Task 12 (FR-7)."""

import json
from pathlib import Path

import pytest
from rapidfuzz import fuzz

from crossfire_forge.aggregate import (
    DEFAULT_CLUSTER_THRESHOLD,
    THRESHOLD_JUSTIFICATION,
    cluster_findings,
)
from crossfire_forge.schemas import AssumptionFinding
from crossfire_forge.taxonomy import BlastRadius

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "threshold_pairs.json"


def _load_pairs() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _finding(statement: str, *, reviewer: str) -> AssumptionFinding:
    return AssumptionFinding(
        statement=statement,
        evidence="Fixture-derived threshold pair.",
        blast_radius=BlastRadius.BR2,
        reviewer_votes=[reviewer],
        agreement_count=1,
        alternative="Resolve before deployment.",
    )


def _same_cluster(clusters: list[tuple[int, ...]], left: int, right: int) -> bool:
    return any(left in cluster and right in cluster for cluster in clusters)


@pytest.fixture(name="pair_data")
def fixture_pair_data() -> dict:
    return _load_pairs()


def test_pinned_threshold_matches_fixture_record(pair_data: dict) -> None:
    assert pair_data["pinned_threshold"] == DEFAULT_CLUSTER_THRESHOLD
    assert DEFAULT_CLUSTER_THRESHOLD == 85
    assert "threshold_pairs.json" in THRESHOLD_JUSTIFICATION
    assert "token_set_ratio" in THRESHOLD_JUSTIFICATION


def test_fixture_pairs_separate_at_pinned_threshold(pair_data: dict) -> None:
    threshold = pair_data["pinned_threshold"]
    for entry in pair_data["pairs"]:
        similarity = fuzz.token_set_ratio(
            entry["statement_a"].casefold(),
            entry["statement_b"].casefold(),
        )
        if entry["label"] == "duplicate":
            assert similarity >= threshold, (
                f"duplicate pair below threshold: {entry['fixture_theme']} ({similarity})"
            )
        else:
            assert similarity < threshold, (
                f"distinct pair at/above threshold: {entry['fixture_theme']} ({similarity})"
            )


def test_duplicate_pairs_cluster_at_pinned_threshold(pair_data: dict) -> None:
    duplicates = [p for p in pair_data["pairs"] if p["label"] == "duplicate"]
    assert duplicates, "expected labeled duplicate pairs in fixture"

    for index, entry in enumerate(duplicates):
        findings = [
            _finding(entry["statement_a"], reviewer=f"r{index}a"),
            _finding(entry["statement_b"], reviewer=f"r{index}b"),
        ]
        clusters = cluster_findings(findings, threshold=DEFAULT_CLUSTER_THRESHOLD)
        assert len(clusters) == 1
        assert set(clusters[0]) == {0, 1}


def test_distinct_pairs_stay_separate_at_pinned_threshold(pair_data: dict) -> None:
    distinct = [p for p in pair_data["pairs"] if p["label"] == "distinct"]
    assert distinct, "expected labeled distinct pairs in fixture"

    for index, entry in enumerate(distinct):
        findings = [
            _finding(entry["statement_a"], reviewer=f"d{index}a"),
            _finding(entry["statement_b"], reviewer=f"d{index}b"),
        ]
        clusters = cluster_findings(findings, threshold=DEFAULT_CLUSTER_THRESHOLD)
        assert len(clusters) == 2
        assert not _same_cluster(clusters, 0, 1)
