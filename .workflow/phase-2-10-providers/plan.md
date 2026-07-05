# Phase 2 Task 10 — Provider adapters

Run slug: `phase-2-10-providers`  
Queue item: `phase-2-10-providers`

## Goal

Phase 2 Task 10 — provider adapters (LIFT): Vertex and second greenfield adapters; mocked contract tests pass for both.

## Scope

Provider adapter modules and mocked HTTP contract tests only. No live model calls; no aggregator or CLI review command.

## Acceptance Criteria

1. Vertex adapter implements the Reviewer interface with httpx-based mocked contract tests.
2. Second greenfield provider adapter implements the same interface with mocked contract tests.
3. Tests pass without live API credentials or network calls to real providers.
4. The verifier checks only Task 10 acceptance, not full Phase 2 completion.

## Verification

```powershell
pytest tests/test_providers.py -v
```
