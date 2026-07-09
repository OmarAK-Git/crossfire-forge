#!/usr/bin/env python3
"""R0 history-hygiene verification (post filter-repo).

Exits 0 when forbidden literals and paths are absent from all commits.
Run after any history rewrite or before gate sign-off.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Owner-local replacements file (parent of repo); literals must never be committed.
REPLACEMENTS_FILE = REPO_ROOT.parent / "GCP_forge_docket-filter-repo-replacements.txt"

FORBIDDEN_PATHS = (
    ".cursor",
    ".claude/worktrees",
)

FORBIDDEN_ARTIFACT_PATTERNS = (
    "343932223796",
    "C:\\Users",
    "C:/Users/oalan",
    '"vertex_project"',
)


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _pick_literals() -> list[str]:
    if not REPLACEMENTS_FILE.is_file():
        print(f"WARN: replacements file missing: {REPLACEMENTS_FILE}", file=sys.stderr)
        return []
    literals: list[str] = []
    for line in REPLACEMENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("literal:") and "==>" in line:
            literals.append(line.split("literal:", 1)[1].split("==>", 1)[0])
    return literals


def main() -> int:
    failures: list[str] = []

    for path in FORBIDDEN_PATHS:
        proc = _run("git", "log", "--all", "--oneline", "--", path)
        if proc.stdout.strip():
            failures.append(f"git log --all -- {path} is not empty")

    for literal in _pick_literals():
        proc = _run("git", "log", "-S", literal, "--oneline", "--all")
        if proc.stdout.strip():
            failures.append(f"git log -S found literal in history: {literal!r}")

    for pattern in FORBIDDEN_ARTIFACT_PATTERNS:
        proc = _run("git", "grep", "-n", pattern, "HEAD", "--", "artifacts/")
        if proc.stdout.strip():
            failures.append(
                f"git grep HEAD artifacts/ matched forbidden pattern: {pattern!r}"
            )

    if failures:
        for item in failures:
            print(f"FAIL: {item}", file=sys.stderr)
        return 1

    print("history_hygiene_ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
