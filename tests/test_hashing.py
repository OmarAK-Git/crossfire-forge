"""Hashing and run-identity tests for Phase 1 Task 3 (NFR-4)."""

from crossfire_forge import __version__
from crossfire_forge.hashing import build_run_identity, content_hash, corpus_entry
from crossfire_forge.schemas import RunIdentity

_SAMPLE_EPIC = "# Epic\nDeploy the widget to prod.\n"
_SAMPLE_CORPUS = [("README.md", "# Corpus\nSecurity posture.\n")]
_SAMPLE_ROSTER = ["fake-reviewer-1", "fake-reviewer-2"]


def test_content_hash_is_deterministic() -> None:
    first = content_hash("same bytes every time")
    second = content_hash("same bytes every time")
    assert first == second


def test_content_hash_differs_for_different_content() -> None:
    assert content_hash("alpha") != content_hash("beta")


def test_content_hash_string_and_utf8_bytes_match() -> None:
    text = "Epic body with unicode: café"
    assert content_hash(text) == content_hash(text.encode("utf-8"))


def test_corpus_entry_hashes_content_and_preserves_path() -> None:
    entry = corpus_entry("README.md", "pinned corpus")
    assert entry.path == "README.md"
    assert entry.content_hash == content_hash("pinned corpus")


def test_build_run_identity_is_repeatable() -> None:
    kwargs = {
        "epic_content": _SAMPLE_EPIC,
        "corpus": _SAMPLE_CORPUS,
        "model_roster": _SAMPLE_ROSTER,
        "tool_version": "0.1.0",
    }
    first = build_run_identity(**kwargs)
    second = build_run_identity(**kwargs)
    assert first == second
    assert first.model_dump() == second.model_dump()


def test_build_run_identity_stable_across_many_calls() -> None:
    identities = [
        build_run_identity(
            epic_content=_SAMPLE_EPIC,
            corpus=_SAMPLE_CORPUS,
            model_roster=_SAMPLE_ROSTER,
        )
        for _ in range(10)
    ]
    assert len({identity.model_dump_json() for identity in identities}) == 1


def test_build_run_identity_fields_match_inputs() -> None:
    identity = build_run_identity(
        epic_content=_SAMPLE_EPIC,
        corpus=_SAMPLE_CORPUS,
        model_roster=_SAMPLE_ROSTER,
        tool_version="0.1.0",
    )
    assert isinstance(identity, RunIdentity)
    assert identity.epic_hash == content_hash(_SAMPLE_EPIC)
    assert len(identity.corpus_hashes) == 1
    assert identity.corpus_hashes[0].path == "README.md"
    assert identity.corpus_hashes[0].content_hash == content_hash(_SAMPLE_CORPUS[0][1])
    assert identity.model_roster == _SAMPLE_ROSTER
    assert identity.tool_version == "0.1.0"


def test_build_run_identity_defaults_tool_version() -> None:
    identity = build_run_identity(
        epic_content=_SAMPLE_EPIC,
        corpus=_SAMPLE_CORPUS,
        model_roster=_SAMPLE_ROSTER,
    )
    assert identity.tool_version == __version__


def test_build_run_identity_changes_when_epic_changes() -> None:
    base = build_run_identity(
        epic_content=_SAMPLE_EPIC,
        corpus=_SAMPLE_CORPUS,
        model_roster=_SAMPLE_ROSTER,
        tool_version="0.1.0",
    )
    changed = build_run_identity(
        epic_content=_SAMPLE_EPIC + "\nextra line",
        corpus=_SAMPLE_CORPUS,
        model_roster=_SAMPLE_ROSTER,
        tool_version="0.1.0",
    )
    assert base.epic_hash != changed.epic_hash


def test_build_run_identity_preserves_corpus_order() -> None:
    identity = build_run_identity(
        epic_content=_SAMPLE_EPIC,
        corpus=[
            ("a.md", "first"),
            ("b.md", "second"),
        ],
        model_roster=_SAMPLE_ROSTER,
        tool_version="0.1.0",
    )
    assert [entry.path for entry in identity.corpus_hashes] == ["a.md", "b.md"]
