# Requirement Traceability Matrix

Canonical RTM for T2+ accountability. Last updated: 2026-07-05 (post Phase 2 exit). Status values: `proposed`, `approved`, `planned`, `in_progress`, `implemented`, `verified`, `reviewed`, `done`, `blocked`, `deferred`, `rejected`.

## Functional requirements

| Req | AC | Decision | Task | Code/Diff | Verification | Review | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-1 | — | — | TASK-006, TASK-014 | `input_loader.py`, `cli.py` | VERIFY-FR-1 | gatekeeper P2 | verified |
| FR-2 | AC-5 | — | TASK-005 | `safety.py` | VERIFY-AC-5 | gatekeeper P1 | verified |
| FR-3 | — | — | TASK-015 | `layer0.py` | VERIFY-FR-3 | gatekeeper P2 | verified |
| FR-4 | — | — | TASK-015 | `layer0.py` | VERIFY-FR-4 | gatekeeper P2 | verified |
| FR-5 | AC-1, AC-2 | — | TASK-008, TASK-010 | `reviewers/` | VERIFY-AC-1 | gatekeeper P2 | verified (semantic deferral) |
| FR-6 | AC-6 | DEC-003 | TASK-008 | `reviewers/base.py`, `fake.py` | VERIFY-AC-6 | gatekeeper P2 | verified |
| FR-7 | AC-2 | DEC-004 | TASK-011 | `aggregate.py` | VERIFY-INV-6 | gatekeeper P2 | verified |
| FR-8 | AC-3 | — | TASK-013 | `render.py` | VERIFY-AC-3 | gatekeeper P2 | verified (semantic deferral) |
| FR-9 | AC-7 | — | TASK-017 | — | VERIFY-AC-7 | — | blocked |
| FR-10 | — | — | TASK-019 | — | VERIFY-FR-10 | — | blocked |
| FR-11 | — | — | TASK-018 | — | VERIFY-FR-11 | — | blocked |
| FR-12 | AC-8 | DEC-006 | TASK-020 | — | VERIFY-AC-8 | — | blocked |

## Acceptance criteria

| Req | AC | Decision | Task | Code/Diff | Verification | Review | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-5, G1 | AC-1 | — | TASK-016 | `harness.py` | VERIFY-AC-1 | gatekeeper P2 | verified (live deferral) |
| FR-5 | AC-2 | DEC-001 | TASK-016 | `harness.py` | VERIFY-AC-2 | gatekeeper P2 | verified (live deferral) |
| FR-8, R-1 | AC-3 | — | TASK-007, TASK-013 | `prompts.py`, `render.py` | VERIFY-AC-3 | gatekeeper P2 | verified (live deferral) |
| NFR-4 | AC-4 | — | TASK-003 | `hashing.py` | VERIFY-AC-4 | gatekeeper P2 | verified |
| FR-2 | AC-5 | — | TASK-005 | `safety.py` | VERIFY-AC-5 | gatekeeper P1 | verified |
| FR-6 | AC-6 | DEC-003 | TASK-008 | `reviewers/` | VERIFY-AC-6 | gatekeeper P2 | verified |
| FR-9 | AC-7 | — | TASK-017 | — | VERIFY-AC-7 | — | blocked |
| FR-12 | AC-8 | DEC-006 | TASK-020 | — | VERIFY-AC-8 | — | blocked |

## Invariants

| Req | AC | Task | Status |
| --- | --- | --- | --- |
| INV-1 | — | TASK-019 | blocked |
| INV-4 | — | TASK-021 | blocked |
| INV-6 | — | TASK-011 | verified |
| INV-7 | — | TASK-014 | verified |

## Goals

| Req | Task | Status |
| --- | --- | --- |
| G4 | TASK-016 | verified (`artifacts/ledger-441.md`; fake pipeline demo) |

## Section 13 reuse map (Phase 0 resolved)

Resolved per `docs/spec-v0.4.md` §13 and packet 03 separability audit. All provisional PORT rows downgraded to **LIFT** because upstream Docket/Crucible/Tumbler repos are inaccessible for import-surface audit.

| # | Spec item | Source | Spec mode | Phase 0 mode | Implementation |
| --- | --- | --- | --- | --- | --- |
| 1 | FR-2 pre-prompt secret scanner | Docket | PORT | **LIFT** | `safety.py` |
| 2 | INV-6 conservation accounting | Docket | PORT | **LIFT** | `aggregate.py` |
| 3 | FR-5 independent multi-reviewer fan-out | Docket | LIFT | **LIFT** | `reviewers/` |
| 4 | FR-7 merge + agreement counting | Crucible | PORT | **LIFT** | `aggregate.py` |
| 5 | AC-2 no manufactured findings | Crucible | PORT | **LIFT** | taxonomy + harness evaluators |
| 6 | R-1 injection separation | Tumbler | PORT | **LIFT** | `prompts.py` |
| 7 | FR-8 final secret pre-filter | Tumbler | PORT | **LIFT** | `render.py` |
| 8 | Phase gating discipline | Process | Process reuse | **Process reuse** | `.workflow/` gates |
| 9 | Vertex provider adapter | Docket/Tumbler | PORT | **LIFT** | `reviewers/vertex.py` |
| 10 | §10 rubric, Layer 0, identity, self-test | — | BUILD | **BUILD** | `layer0.py`, `harness.py`, etc. |
