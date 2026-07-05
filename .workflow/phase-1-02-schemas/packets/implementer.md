# Implementation Packet — phase-1-02-schemas

## Objective

Implement core pydantic v2 schemas and taxonomy: three-type discriminated-union findings, ledger, run identity. Enforce NG7 (uncited violations fail validation).

## Original User Goal

Phase 1 Task 2 — core schemas and taxonomy: discriminated-union findings (three types), ledger, run identity; invalid payloads fail validation including uncited violations (NG7).

## Relevant Docs

- `docs/spec-v0.4.md` §5 Finding taxonomy, §8 schemas (if present)
- `docs/implementation-plan-v0.4.md` Phase 1 Task 2

## Allowed Files

- `crossfire_forge/schemas.py`
- `crossfire_forge/taxonomy.py`
- `tests/test_schemas.py`
- `.workflow/phase-1-contract-harness/verification-ledger.md` (optional note)

## Do Not Touch

- hashing.py, safety.py, cli review, reviewers/
- Full Phase 1 exit gate

## Acceptance Criteria

1. Exactly three finding types: `assumption`, `violation`, `safety_warning` (discriminated union on `type`).
2. Violation requires `standards_ref`; missing/empty fails validation (NG7).
3. Ledger and run-identity models exist and validate valid/invalid payloads.
4. tests/test_schemas.py demonstrates invalid payloads fail.

## Verification Commands

```powershell
pytest tests/test_schemas.py -v
```

Write `.workflow/phase-1-02-schemas/results/implementer-result.md` when done. Do NOT mark queue done.
