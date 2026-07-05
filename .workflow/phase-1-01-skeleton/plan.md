# Task — phase-1-01-skeleton

## Goal

Phase 1 Task 1 — project skeleton: Python 3.12, pytest, pydantic, typer, httpx wired; pytest and crossfire-forge --help run.

## Success Criteria

- pyproject.toml declares Python 3.12 with pytest, pydantic v2, typer, and httpx.
- crossfire-forge --help exits 0 from repo root.
- pytest collects and runs (even if zero or minimal tests).
- VERIFY-P1-002 is updated with the task-level result.
- The verifier checks only Task 1 acceptance, not full Phase 1 completion.

## Constraints

- Project bootstrap only. Wire dependencies and CLI entrypoint; no schemas, safety, or reviewer modules yet.
- Allowed files only (see implementer packet).
- Stop and request approval before `pip install` or other dependency installs.

## Risks

| Risk | Approval required | Mitigation |
| --- | --- | --- |
| Dependency install needed for verification | yes | Create pyproject.toml; request approval for pip install at verification |
| Over-scoping to full Phase 1 | no | Task verifier scope is `task` only |

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| implementer | Bootstrap pyproject.toml, package stub, CLI entrypoint | gsd-executor | pending |

## Verification

| ID | Requirement | Check | Expected |
| --- | --- | --- | --- |
| VERIFY-P1-002 | CLI | `crossfire-forge --help` | exit 0 |
| VERIFY-TASK-001 | pytest collect | `pytest --collect-only` | collects tests |
