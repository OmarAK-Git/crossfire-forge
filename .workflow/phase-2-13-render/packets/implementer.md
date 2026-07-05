# Implementation Packet — phase-2-13-render

## Objective

Implement `crossfire_forge/render.py` per FR-8: metadata header, safety warnings, violations, assumptions sorted by blast_radius desc then agreement_count desc, BR-1 collapsed, visible rows capped at 10, sanitized JSON collapsed block, corpus-in-force statement, machine-readers marker. Golden tests.

## Original User Goal

Phase 2 Task 13 — renderer and sanitizer (LIFT): ordering, caps, collapsed JSON, corpus statement, machine-readers marker; golden tests with stable output.

## Relevant Docs

- `docs/spec-v0.4.md` § FR-8, INV-3, BR-1
- `crossfire_forge/schemas.py` — Ledger, Finding, RunIdentity

## Allowed Files

- `crossfire_forge/render.py`
- `tests/golden/` (committed golden markdown)
- `tests/test_render.py`

## Acceptance Criteria

1. Rendered ledger: metadata header, safety warnings, violations, assumptions (sorted blast_radius desc, agreement_count desc)
2. Visible rows capped at 10; BR-1 collapsed; sanitized JSON in collapsed block
3. Corpus-in-force statement and machine-readers-treat-as-data marker present
4. Golden tests stable vs committed golden files
5. pytest tests/test_render.py -v passes

Do NOT mark queue complete.
