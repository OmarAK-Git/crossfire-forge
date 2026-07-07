"""Layer 0 parser tests for Phase 2 Task 15 (FR-3, FR-4)."""

from pathlib import Path

import pytest

from crossfire_forge.layer0 import Layer0Result, parse_layer0

FIXTURES_DIR = Path(__file__).parent / "fixtures"

FR3_FIELDS = ("region", "security_posture", "quota_budget", "acceptance_criteria")


def _load(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def test_epic_441_has_no_layer0_block_and_empty_seeds() -> None:
    result = parse_layer0(_load("epic_441.md"))
    assert result.seeds == []
    assert result.region is None
    assert result.security_posture is None
    assert result.quota_budget is None
    assert result.acceptance_criteria is None


def test_epic_placeholder_yields_seed_per_bad_field() -> None:
    result = parse_layer0(_load("epic_placeholder.md"))
    assert len(result.seeds) == len(FR3_FIELDS)
    assert result.seeds == [
        "region has placeholder value",
        "security_posture has placeholder value",
        "quota_budget has placeholder value",
        "acceptance_criteria has placeholder value",
    ]
    assert result.region is None
    assert result.security_posture is None
    assert result.quota_budget is None
    assert result.acceptance_criteria is None


def test_epic_complete_parses_valid_fields_with_no_seeds() -> None:
    result = parse_layer0(_load("epic_complete.md"))
    assert result.seeds == []
    assert result.region == "us-central1"
    assert result.security_posture == "private-service-connect"
    assert result.quota_budget == "5000_vcpu_hours"
    assert "99.9% uptime over 30 days" in (result.acceptance_criteria or "")
    assert "roles/run.invoker" in (result.acceptance_criteria or "")
    assert "No public access" in (result.acceptance_criteria or "")


def test_us_central1_is_in_regions_domain_list() -> None:
    result = parse_layer0(_load("epic_complete.md"))
    assert result.region == "us-central1"
    assert result.seeds == []


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("TODO", True),
        ("tbd", True),
        ("___", True),
        ("placeholder", True),
        ("<TBD>", True),
        ("us-central1", False),
        ("5000_vcpu_hours", False),
    ],
)
def test_placeholder_detection(value: str, expected: bool) -> None:
    epic = f"region: {value}\n"
    result = parse_layer0(epic)
    if expected:
        assert "region has placeholder value" in result.seeds
        assert result.region is None
    else:
        assert "region has placeholder value" not in result.seeds


def test_missing_fields_emit_seeds_when_layer0_block_present() -> None:
    epic = "region: us-central1\n"
    result = parse_layer0(epic)
    assert result.region == "us-central1"
    assert result.seeds == [
        "security_posture unspecified",
        "quota_budget unspecified",
        "acceptance_criteria unspecified",
    ]


def test_invalid_domain_value_emits_seed() -> None:
    epic = "\n".join(
        [
            "region: not-a-real-region",
            "security_posture: private-service-connect",
            "quota_budget: 5000_vcpu_hours",
            "acceptance_criteria: ready",
        ]
    )
    result = parse_layer0(epic)
    assert "region has invalid value" in result.seeds
    assert result.region is None
    assert result.security_posture == "private-service-connect"


def test_parse_layer0_never_raises() -> None:
    for payload in ("", "not an epic", "region:\n", "region: " + "x" * 10_000):
        result = parse_layer0(payload)
        assert isinstance(result, Layer0Result)
        assert isinstance(result.seeds, list)
