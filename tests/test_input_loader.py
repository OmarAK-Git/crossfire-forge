"""Input loader tests for Phase 1 Task 6 (FR-1)."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from crossfire_forge.cli import app
from crossfire_forge.input_loader import (
    DEFAULT_CORPUS_PATHS,
    DEFAULT_FIXTURES_DIR,
    load_corpus,
    load_epic,
    load_inputs,
)
from crossfire_forge.schemas import CorpusHash

FIXTURES_DIR = Path(__file__).parent / "fixtures"
EPIC_FIXTURES = [
    "epic_441.md",
    "epic_complete.md",
    "epic_injection.md",
    "epic_placeholder.md",
    "epic_secret.md",
]
PINNED_HASHES = {
    "README.md": "0128e53f7dc58360038d92a3e682436b76cdc507e06682866f07f1fdfb1439ba",
    "epic_441.md": "cda6b44e85ee48a6de74a2e2ca3461c4a799c1385fb49c3a8c913c0afc630ac0",
    "epic_complete.md": "f54f270c9f96f2c620298107402208e96186784707601df10d7c370388be8ab5",
    "epic_injection.md": "7d4393d6b983a846024ba98765bcb57ac398216d6b31b13343e03306ac8860d7",
    "epic_placeholder.md": "60436a93a46ca3e42a80e8a8df9a0a4fc0a4aa236faf1e9f171402cff195bbbc",
    "epic_secret.md": "01c38074bee387d4ccdca3046ad99e008a416ec6481fe8551d4794a821852886",
}


def test_default_corpus_matches_readme_pin() -> None:
    assert DEFAULT_CORPUS_PATHS == ("README.md",)
    assert DEFAULT_FIXTURES_DIR.resolve() == FIXTURES_DIR.resolve()


@pytest.mark.parametrize("epic_name", EPIC_FIXTURES)
def test_load_inputs_default_corpus(epic_name: str) -> None:
    epic_path = FIXTURES_DIR / epic_name
    loaded = load_inputs(epic_path)
    assert loaded.epic_content
    assert loaded.epic_hash == PINNED_HASHES[epic_name]
    assert len(loaded.corpus) == 1
    assert loaded.corpus[0][0] == "README.md"
    assert loaded.corpus_hashes == [
        CorpusHash(path="README.md", content_hash=PINNED_HASHES["README.md"])
    ]


def test_load_epic_returns_content_and_hash() -> None:
    epic_path = FIXTURES_DIR / "epic_441.md"
    content, digest = load_epic(epic_path)
    assert "[EPIC]" in content
    assert digest == PINNED_HASHES["epic_441.md"]


def test_load_corpus_preserves_order() -> None:
    paths = ["epic_441.md", "README.md", "epic_complete.md"]
    corpus, corpus_hashes = load_corpus(paths, fixtures_dir=FIXTURES_DIR)
    assert [path for path, _ in corpus] == paths
    assert [entry.path for entry in corpus_hashes] == paths
    assert [entry.content_hash for entry in corpus_hashes] == [
        PINNED_HASHES[name] for name in paths
    ]


def test_load_inputs_is_deterministic() -> None:
    epic_path = FIXTURES_DIR / "epic_complete.md"
    first = load_inputs(epic_path)
    second = load_inputs(epic_path)
    assert first == second


def test_cli_hashes_prints_epic_and_corpus_digests() -> None:
    epic_path = FIXTURES_DIR / "epic_441.md"
    result = CliRunner().invoke(
        app,
        [
            "hashes",
            str(epic_path),
            "--corpus",
            "README.md",
            "--fixtures-dir",
            str(FIXTURES_DIR),
        ],
    )
    assert result.exit_code == 0, result.output
    assert f"epic\t{epic_path}\t{PINNED_HASHES['epic_441.md']}" in result.output
    assert f"corpus\tREADME.md\t{PINNED_HASHES['README.md']}" in result.output
