# Task — phase-1-02-schemas

## Goal

Phase 1 Task 2 — core schemas and taxonomy: discriminated-union findings (three types), ledger, run identity; invalid payloads fail validation including uncited violations (NG7).

## Success Criteria

- Finding models use a discriminated union with exactly three finding types per docs/spec-v0.4.md section 5.
- Violation findings require standards_ref; uncited violations fail pydantic validation (NG7).
- Ledger and run-identity models validate representative valid and invalid payloads.
- Tests demonstrate invalid payloads fail validation.
- The verifier checks only Task 2 acceptance, not full Phase 1 completion.

## Constraints

- Contract-first schemas and taxonomy only. Do not implement hashing, safety, reviewers, or CLI review command.

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| implementer | schemas.py, taxonomy.py, test_schemas.py | gsd-executor | pending |
