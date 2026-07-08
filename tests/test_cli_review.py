"""CLI review command tests for Phase 2 Task 14 (FR-1, FR-8, INV-7)."""

import json
from pathlib import Path

from typer.testing import CliRunner

from crossfire_forge.cli import app, run_review
from crossfire_forge.render import MACHINE_READERS_MARKER

FIXTURES_DIR = Path(__file__).parent / "fixtures"
EPIC_441 = FIXTURES_DIR / "epic_441.md"
PINNED_HASHES = {
    "README.md": "8fa4ec6333bf34a859b89bcf9d9a028c505741a0de497f036719108a221c5754",
    "epic_441.md": "310da35ec77f9899b8336e26d697ed7a53b5b87f56878ed5718f42ac83291b30",
}


def _invoke_review(*extra: str):
    return CliRunner().invoke(
        app,
        [
            "review",
            str(EPIC_441),
            "--corpus",
            "README.md",
            "--fixtures-dir",
            str(FIXTURES_DIR),
            *extra,
        ],
    )


def test_review_cli_runs_e2e_on_epic_441() -> None:
    expected = run_review(
        EPIC_441,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        reviewer_count=3,
    )
    result = _invoke_review()
    assert result.exit_code == 0, result.output
    assert result.output == expected
    assert "Run aborted: suspected secret" not in result.output


def test_review_cli_output_has_ledger_structure() -> None:
    result = _invoke_review()
    assert result.exit_code == 0, result.output
    body = result.output

    assert body.startswith("# Crossfire-Forge Review Ledger")
    assert MACHINE_READERS_MARKER in body
    assert PINNED_HASHES["epic_441.md"] in body
    assert PINNED_HASHES["README.md"] in body
    assert "fake\\-reviewer\\-1" in body
    assert "fake\\-reviewer\\-2" in body
    assert "fake\\-reviewer\\-3" in body
    assert "## Assumptions" in body
    # Safety-warning defanging in rendered output is guaranteed by
    # test_render.py (golden + defang unit test); the fake reviewer's finding
    # kind here is digest-derived and not a stable structural property.
    assert "## Corpus in Force" in body
    assert "Sanitized ledger JSON (machine-readable)" in body


def test_review_cli_writes_output_file(tmp_path: Path) -> None:
    out_path = tmp_path / "ledger.md"
    result = _invoke_review("--output", str(out_path))
    assert result.exit_code == 0, result.output
    assert out_path.read_text(encoding="utf-8") == result.output


def test_debug_raw_envelopes_default_off() -> None:
    result = _invoke_review()
    assert result.exit_code == 0, result.output
    assert result.stderr == ""


def test_debug_raw_envelopes_prints_to_stderr_only() -> None:
    result = _invoke_review("--debug-raw-envelopes")
    assert result.exit_code == 0, result.output
    assert result.output.startswith("# Crossfire-Forge Review Ledger")
    assert result.stderr

    envelopes = [json.loads(line) for line in result.stderr.splitlines() if line.strip()]
    assert len(envelopes) == 3
    assert {entry["reviewer_id"] for entry in envelopes} == {
        "fake-reviewer-1",
        "fake-reviewer-2",
        "fake-reviewer-3",
    }
    for entry in envelopes:
        assert entry["discard_count"] == 0
        assert len(entry["findings"]) == 1


def test_review_cli_aborts_on_secret_epic() -> None:
    result = CliRunner().invoke(
        app,
        [
            "review",
            str(FIXTURES_DIR / "epic_secret.md"),
            "--fixtures-dir",
            str(FIXTURES_DIR),
        ],
    )
    assert result.exit_code == 1
    assert "suspected secret" in result.stderr.lower()


def test_run_review_is_deterministic() -> None:
    first = run_review(
        EPIC_441,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        reviewer_count=3,
    )
    second = run_review(
        EPIC_441,
        corpus=["README.md"],
        fixtures_dir=FIXTURES_DIR,
        reviewer_count=3,
    )
    assert first == second


def test_review_cli_respects_fake_count() -> None:
    result = CliRunner().invoke(
        app,
        [
            "review",
            str(EPIC_441),
            "--fixtures-dir",
            str(FIXTURES_DIR),
            "--fake-count",
            "2",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "fake\\-reviewer\\-1" in result.output
    assert "fake\\-reviewer\\-2" in result.output
    assert "fake\\-reviewer\\-3" not in result.output


def test_inv4_v01_has_no_github_label_application_package() -> None:
    """INV-4: v0.1 never applies labels — no github/ package until Phase 3."""
    import crossfire_forge

    github_pkg = Path(crossfire_forge.__file__).resolve().parent / "github"
    assert not github_pkg.exists()
