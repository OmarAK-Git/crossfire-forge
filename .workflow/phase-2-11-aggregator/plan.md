# Phase 2 Task 11 — Aggregator

Run slug: `phase-2-11-aggregator`  
Queue item: `phase-2-11-aggregator`

## Goal

Phase 2 Task 11 — aggregator (LIFT): lexical clustering before judge merge; schema-or-discard; conservation accounting (INV-6); agreement counts reproducible on fixed input.

## Scope

aggregate.py and aggregator tests only. Use rapidfuzz with threshold placeholder (pinned in Task 12). Mock judge provider; no live models.

## Verification

```powershell
pytest tests/test_aggregate.py -v
```
