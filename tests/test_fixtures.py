"""Fixture corpus tests for Phase 1 Task 4."""

from pathlib import Path

import pytest

from crossfire_forge.hashing import content_hash

FIXTURES_DIR = Path(__file__).parent / "fixtures"

EPIC_FIXTURES = [
    "epic_441.md",
    "epic_complete.md",
    "epic_injection.md",
    "epic_placeholder.md",
    "epic_secret.md",
]

CORPUS_FILES = ["README.md", *EPIC_FIXTURES]


def _load(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


def test_all_fixture_files_exist() -> None:
    for name in CORPUS_FILES:
        assert (FIXTURES_DIR / name).is_file(), name


@pytest.mark.parametrize("filename", CORPUS_FILES)
def test_fixture_content_hash_stable_across_repeated_loads(filename: str) -> None:
    hashes = [content_hash(_load(filename)) for _ in range(5)]
    assert len(set(hashes)) == 1


def test_full_corpus_hashes_stable_between_load_passes() -> None:
    first = {name: content_hash(_load(name)) for name in CORPUS_FILES}
    second = {name: content_hash(_load(name)) for name in CORPUS_FILES}
    assert first == second


PINNED_HASHES = {
    "README.md": "8fa4ec6333bf34a859b89bcf9d9a028c505741a0de497f036719108a221c5754",
    "epic_441.md": "310da35ec77f9899b8336e26d697ed7a53b5b87f56878ed5718f42ac83291b30",
    "epic_complete.md": "e7e8fdcb4fcbfe84e3d97be7f1651a86587979784253142f35c86e37c953231a",
    "epic_injection.md": "7d4393d6b983a846024ba98765bcb57ac398216d6b31b13343e03306ac8860d7",
    "epic_placeholder.md": "60436a93a46ca3e42a80e8a8df9a0a4fc0a4aa236faf1e9f171402cff195bbbc",
    "epic_secret.md": "01c38074bee387d4ccdca3046ad99e008a416ec6481fe8551d4794a821852886",
}


def test_pinned_corpus_hashes() -> None:
    """Golden digests detect accidental fixture edits."""
    actual = {name: content_hash(_load(name)) for name in CORPUS_FILES}
    assert actual == PINNED_HASHES


# Reviewer-facing vocabulary that must never leak into the "clean" AC-2 fixture:
# an Epic that names the review tool's own machinery (blast-radius grades,
# ledgers, seed layers, findings) is an attempt to steer the reviewer, not a
# deployable spec. Keeping epic_complete.md free of it preserves AC-2's premise.
_REVIEWER_META_VOCAB = ("Layer 0", "ledger", "BR-", "assumption")


def test_epic_complete_has_no_reviewer_meta_vocabulary() -> None:
    body = _load("epic_complete.md")
    leaked = [term for term in _REVIEWER_META_VOCAB if term.casefold() in body.casefold()]
    assert not leaked, f"reviewer-meta vocabulary leaked into epic_complete.md: {leaked}"
