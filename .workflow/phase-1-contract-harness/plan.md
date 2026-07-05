# Phase 1 — Contract and local harness

Run slug: `phase-1-contract-harness`  
Source: `docs/implementation-plan-v0.4.md` § Phase 1 (Tasks 1–9)

## Goal

Deliver schemas, safety, hashing, fixtures, Layer 0 stub, and prompt contract — testable without any live model.

## Success Criteria

- `pytest` green on Tasks 1–8
- AC-5 demonstrated (secret abort, no leakage)
- Gatekeeper PASS on independent surface
- `crossfire-forge --help` runs

## Current Context

- Blocked on Phase 0 exit gate for final PORT/LIFT resolutions affecting Tasks 5 and 7
- Repository layout per implementation plan § Repository layout

## Constraints

- Contract-first: TASK-002 schemas before downstream modules
- Fake reviewer before any provider API
- `--debug-raw-envelopes` local only (INV-7 groundwork)

## Risks

| Risk | Approval required | Mitigation |
| --- | --- | --- |
| PORT downgrade for Docket/Tumbler | no | LIFT against same spec items |
| Schema churn breaks downstream tasks | no | Gatekeeper checkpoint TASK-009 |

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| 01-skeleton | TASK-001 project skeleton | implementer | pending |
| 02-schemas | TASK-002 core schemas + taxonomy | implementer | pending |
| 03-hashing | TASK-003 hashing / run identity | implementer | pending |
| 04-fixtures | TASK-004 fixture set | implementer | pending |
| 05-safety | TASK-005 pre-prompt scanner (AC-5) | implementer | pending |
| 06-loader | TASK-006 input loader | implementer | pending |
| 07-prompts | TASK-007 prompt contract | implementer | pending |
| 08-fake-reviewer | TASK-008 reviewer + fake | implementer | pending |
| 09-gatekeeper | Independent review Tasks 1–8 | code-reviewer | pending |

## Verification

See `verification-ledger.md`. Commands: `pytest`, AC-5 harness.

## Reusable Artifacts

- `crossfire_forge/schemas.py`, `tests/fixtures/`, `tests/test_*.py`
