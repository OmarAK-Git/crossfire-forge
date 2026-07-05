# Implementation Packet — phase-1-01-skeleton

## Objective

Bootstrap the Crossfire-Forge Python project: pyproject.toml, package stub, CLI entrypoint, minimal tests. Wire Python 3.12, pytest, pydantic v2, typer, httpx.

## Original User Goal

Phase 1 Task 1 — project skeleton: Python 3.12, pytest, pydantic, typer, httpx wired; pytest and crossfire-forge --help run.

## Relevant Docs and State

- `docs/implementation-plan-v0.4.md` § Repository layout, Phase 1 Task 1
- `docs/spec-v0.4.md` (context only; no schemas yet)
- `.workflow/phase-1-contract-harness/verification-ledger.md` (update VERIFY-P1-002)
- `.workflow/phase-1-contract-harness/plan.md`

## Allowed Files (write)

- `pyproject.toml`
- `crossfire_forge/` (create `__init__.py`, `cli.py` only — no schemas, safety, reviewers)
- `tests/` (minimal conftest or placeholder test acceptable)
- `.workflow/phase-1-contract-harness/verification-ledger.md` (VERIFY-P1-002 row only)
- `.workflow/phase-1-contract-harness/state.json` (optional status note)

## Do Not Touch

- `crossfire_forge/schemas.py`, `safety.py`, `reviewers/`, etc. (later tasks)
- `.codex` / `.claude`
- `memory-bank/` (except if unavoidable — prefer not)
- Full Phase 1 exit gate

## Acceptance Criteria

1. `pyproject.toml` declares Python 3.12 with pytest, pydantic v2, typer, httpx; CLI script `crossfire-forge` points at `crossfire_forge.cli:app`.
2. `crossfire-forge --help` exits 0 (may require editable install — if so, run `pip install -e ".[dev]"` or equivalent and note in result).
3. `pytest --collect-only` succeeds.
4. Update VERIFY-P1-002 in `.workflow/phase-1-contract-harness/verification-ledger.md` with task-level result when checks pass.

## Verification Commands

```powershell
pytest --collect-only
crossfire-forge --help
```

## Expected Result Schema

Return:
- `changed_files`: list of paths written
- `checks_run`: commands executed (including any pip install)
- `findings_summary`: one paragraph on skeleton state
- `unresolved_risks`: blockers or approval gates hit
- `approval_gates`: list any gates (e.g. pip install)

Do NOT mark the queue item complete. Controller + verifier handle completion.
