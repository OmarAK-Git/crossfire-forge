# Requirement Traceability Matrix

Last updated: 2026-07-06 (live Vertex verification). Status: `verified` = live or structural evidence on file.

## Functional requirements

| Req | AC | Task | Code | Verification | Status |
| --- | --- | --- | --- | --- | --- |
| FR-1 | — | TASK-006,014 | `input_loader.py`, `cli.py` | pytest | verified |
| FR-2 | AC-5 | TASK-005 | `safety.py` | pytest secret tests | verified |
| FR-3/FR-4 | — | TASK-015 | `layer0.py` | pytest | verified |
| FR-5 | AC-1,2 | TASK-008,010 | `reviewers/` | live-ac-summary | verified |
| FR-6 | AC-6 | TASK-008 | `reviewers/base.py` | pytest | verified |
| FR-7 | AC-2 | TASK-011 | `aggregate.py` | pytest INV-6 | verified |
| FR-8 | AC-3 | TASK-013 | `render.py` | live-ac-summary | verified |
| FR-9..FR-12 | AC-7,8 | TASK-017..020 | — | — | blocked (D-2) |

## Acceptance criteria

| AC | Verification | Status |
| --- | --- | --- |
| AC-1 | `artifacts/live-ac-summary.json` 5/5 BR-3 RBAC | verified (live) |
| AC-2 | live-ac-summary 5/5 complete epic | verified (live) |
| AC-3 | live-ac-summary 5/5 injection | verified (live) |
| AC-4 | pytest identity no-op | verified |
| AC-5 | pytest secret abort | verified |
| AC-6 | pytest discard metering | verified |
| AC-7, AC-8 | — | blocked |

## Goals

| Goal | Evidence | Status |
| --- | --- | --- |
| G4 | `artifacts/ledger-441.md` live Vertex | verified |

## §13 reuse map

All rows: **LIFT (reimplemented-from-description)**. Diff: `.workflow/port-validation/safety-prompts-diff.md`. No "ported from" pitch claims.
