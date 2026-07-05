"""Local Epic and corpus loading (FR-1)."""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from crossfire_forge.hashing import content_hash, corpus_entry
from crossfire_forge.schemas import CorpusHash

DEFAULT_FIXTURES_DIR = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
DEFAULT_CORPUS_PATHS: tuple[str, ...] = ("README.md",)


@dataclass(frozen=True)
class LoadedInput:
    """Epic body plus ordered corpus entries with content hashes."""

    epic_path: str
    epic_content: str
    epic_hash: str
    corpus: list[tuple[str, str]]
    corpus_hashes: list[CorpusHash]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_epic(epic_path: Path) -> tuple[str, str]:
    """Load Epic markdown and return (content, content_hash)."""
    content = _read_text(epic_path)
    return content, content_hash(content)


def load_corpus(
    corpus_paths: Sequence[str],
    *,
    fixtures_dir: Path | None = None,
) -> tuple[list[tuple[str, str]], list[CorpusHash]]:
    """Load ordered corpus files relative to fixtures_dir."""
    base = fixtures_dir if fixtures_dir is not None else DEFAULT_FIXTURES_DIR
    corpus: list[tuple[str, str]] = []
    corpus_hashes: list[CorpusHash] = []
    for rel_path in corpus_paths:
        content = _read_text(base / rel_path)
        corpus.append((rel_path, content))
        corpus_hashes.append(corpus_entry(rel_path, content))
    return corpus, corpus_hashes


def load_inputs(
    epic_path: Path,
    corpus_paths: Sequence[str] | None = None,
    *,
    fixtures_dir: Path | None = None,
) -> LoadedInput:
    """Load a local Epic and ordered corpus with stable content hashes."""
    paths = list(DEFAULT_CORPUS_PATHS if corpus_paths is None else corpus_paths)
    epic_content, epic_hash = load_epic(epic_path)
    corpus, corpus_hashes = load_corpus(paths, fixtures_dir=fixtures_dir)
    return LoadedInput(
        epic_path=str(epic_path),
        epic_content=epic_content,
        epic_hash=epic_hash,
        corpus=corpus,
        corpus_hashes=corpus_hashes,
    )
