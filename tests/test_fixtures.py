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
    "README.md": "a3dbef62b14860815c61ffa7649299cb2545420bd24a4a1bde08d6839f3c8232",
    "epic_441.md": "cda6b44e85ee48a6de74a2e2ca3461c4a799c1385fb49c3a8c913c0afc630ac0",
    "epic_complete.md": "3e9c65bed47d9a595577f4b438d41a68bbaad1f3dd818b357b69e24916fe466d",
    "epic_injection.md": "7d4393d6b983a846024ba98765bcb57ac398216d6b31b13343e03306ac8860d7",
    "epic_placeholder.md": "60436a93a46ca3e42a80e8a8df9a0a4fc0a4aa236faf1e9f171402cff195bbbc",
    "epic_secret.md": "01c38074bee387d4ccdca3046ad99e008a416ec6481fe8551d4794a821852886",
}


def test_pinned_corpus_hashes() -> None:
    """Golden digests detect accidental fixture edits."""
    actual = {name: content_hash(_load(name)) for name in CORPUS_FILES}
    assert actual == PINNED_HASHES
