# Implementation Packet — phase-2-10-providers

## Objective

Implement Vertex and second greenfield provider adapters that satisfy the `Reviewer` protocol, with httpx-based mocked contract tests. No live API calls.

## Original User Goal

Phase 2 Task 10 — provider adapters (LIFT): Vertex and second greenfield adapters; mocked contract tests pass for both.

## Relevant Docs and State

- `docs/implementation-plan-v0.4.md` § Phase 2 Task 10, repository layout (`reviewers/vertex.py`, second provider)
- `docs/spec-v0.4.md` § FR-5, FR-6, section 13 row 9 (Vertex LIFT)
- `memory-bank/traceability.md` § section 13 row 9
- `crossfire_forge/reviewers/base.py` — `Reviewer` protocol, `parse_reviewer_output`, `ReviewResult`
- `crossfire_forge/reviewers/fake.py` — reference implementation pattern
- `crossfire_forge/prompts.py` — `ReviewerPrompt` (system + user)
- `.workflow/phase-2-review-engine/verification-ledger.md` (optional task note only)

## Allowed Files (write)

- `crossfire_forge/reviewers/vertex.py`
- `crossfire_forge/reviewers/second_provider.py`
- `crossfire_forge/reviewers/base.py` (only if shared helper needed)
- `crossfire_forge/reviewers/__init__.py`
- `tests/test_providers.py`
- `pyproject.toml` (only if test deps needed — prefer stdlib/httpx already present)
- `.workflow/phase-2-review-engine/verification-ledger.md` (VERIFY row for Task 10 if you add one)

## Do Not Touch

- `crossfire_forge/aggregate.py`, `render.py`, `layer0.py`, `cli.py` review wiring
- Live Vertex or external API credentials
- `.codex` / `.claude`
- Full Phase 2 exit gate or gatekeeper review

## Acceptance Criteria

1. `VertexReviewer` (or equivalent) implements `Reviewer.review(prompt) -> ReviewResult` using httpx to call Vertex-style generateContent endpoint shape; tests mock transport — no real network.
2. Second greenfield adapter (e.g. `SecondProviderReviewer`) implements same interface with distinct endpoint/payload shape; mocked contract tests pass.
3. Both adapters use `parse_reviewer_output` or equivalent schema-or-discard path; invalid model JSON increments discard_count.
4. `pytest tests/test_providers.py -v` passes from repo root without credentials.

## Verification Commands

```powershell
pytest tests/test_providers.py -v
```

## Expected Result Schema

Return:
- `changed_files`: list of paths written
- `checks_run`: commands executed
- `findings_summary`: one paragraph on adapter design
- `unresolved_risks`: blockers or approval gates hit
- `approval_gates`: list any gates (pip install, etc.)

Do NOT mark the queue item complete. Controller + verifier handle completion.
