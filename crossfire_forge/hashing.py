"""Deterministic content hashing and run identity construction (NFR-4)."""

import hashlib
from collections.abc import Sequence

from crossfire_forge import __version__
from crossfire_forge.schemas import CorpusHash, RunIdentity


def content_hash(content: str | bytes) -> str:
    """Return the SHA-256 hex digest of content."""
    data = content.encode("utf-8") if isinstance(content, str) else content
    return hashlib.sha256(data).hexdigest()


def corpus_entry(path: str, content: str | bytes) -> CorpusHash:
    """Build a corpus hash entry for path and raw content."""
    return CorpusHash(path=path, content_hash=content_hash(content))


def build_run_identity(
    *,
    epic_content: str | bytes,
    corpus: Sequence[tuple[str, str | bytes]],
    model_roster: Sequence[str],
    tool_version: str | None = None,
) -> RunIdentity:
    """Construct a stable run identity from inputs and configuration."""
    return RunIdentity(
        epic_hash=content_hash(epic_content),
        corpus_hashes=[corpus_entry(path, content) for path, content in corpus],
        model_roster=list(model_roster),
        tool_version=tool_version if tool_version is not None else __version__,
    )
