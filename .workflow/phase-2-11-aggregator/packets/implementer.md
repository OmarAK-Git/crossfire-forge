# Implementation Packet — phase-2-11-aggregator

## Objective

Implement `crossfire_forge/aggregate.py` with lexical clustering (rapidfuzz), judge merge within clusters, schema-or-discard, conservation accounting (INV-6), and reproducible agreement counts. Mock judge; no live models.

## Original User Goal

Phase 2 Task 11 — aggregator (LIFT): lexical clustering before judge merge; schema-or-discard; conservation accounting (INV-6); agreement counts reproducible on fixed input.

## Relevant Docs and State

- `docs/spec-v0.4.md` § FR-7, INV-6
- `docs/implementation-plan-v0.4.md` § Phase 2 Task 11
- `crossfire_forge/schemas.py` — Finding models, Ledger
- `crossfire_forge/reviewers/base.py` — validate_findings, parse_reviewer_output
- `memory-bank/traceability.md` § section 13 (Crucible merge + Docket conservation LIFT)

## Allowed Files (write)

- `crossfire_forge/aggregate.py`
- `tests/test_aggregate.py`
- `pyproject.toml` (add rapidfuzz dependency if needed — note approval if pip install required)
- `.workflow/phase-2-review-engine/verification-ledger.md` (optional VERIFY row)

## Do Not Touch

- `crossfire_forge/render.py`, `cli.py`, provider adapters beyond imports
- Live judge model calls
- Threshold tuning / labeled pairs (Task 12)
- Full Phase 2 exit gate

## Acceptance Criteria

1. Lexical clustering groups duplicate findings before judge-model merge within clusters (rapidfuzz; use a placeholder threshold constant, e.g. DEFAULT_CLUSTER_THRESHOLD — Task 12 will pin it).
2. Judge output is schema-or-discarded; merge and drop decisions are recorded in conservation ledger structure.
3. Unique findings are conserved (INV-6) on fixed test input: inputs == merged ∪ rendered ∪ collapsed ∪ discarded-with-reason.
4. Agreement counts are reproducible on fixed input.
5. `pytest tests/test_aggregate.py -v` passes with mocked/deterministic judge.

## Verification Commands

```powershell
pytest tests/test_aggregate.py -v
```

## Expected Result Schema

Return changed_files, checks_run, findings_summary, unresolved_risks, approval_gates.

Do NOT mark queue item complete.
