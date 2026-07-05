# Requirement Traceability Matrix

Canonical RTM for T2+ accountability. Update rows as tasks progress. Status values: `proposed`, `approved`, `planned`, `in_progress`, `implemented`, `verified`, `reviewed`, `done`, `blocked`, `deferred`, `rejected`.

## Functional requirements

| Req | AC | Decision | Task | Code/Diff | Verification | Review | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-1 | — | — | TASK-006 | — | VERIFY-FR-1 | — | planned |
| FR-2 | AC-5 | — | TASK-005 | — | VERIFY-AC-5 | — | planned |
| FR-3 | — | — | TASK-015 | — | VERIFY-FR-3 | — | planned |
| FR-4 | — | — | TASK-015 | — | VERIFY-FR-4 | — | planned |
| FR-5 | AC-1, AC-2 | — | TASK-008, TASK-010 | — | VERIFY-AC-1 | — | planned |
| FR-6 | AC-6 | — | TASK-008 | — | VERIFY-AC-6 | — | planned |
| FR-7 | AC-2 | — | TASK-011 | — | VERIFY-INV-6 | — | planned |
| FR-8 | AC-3 | — | TASK-013 | — | VERIFY-AC-3 | — | planned |
| FR-9 | AC-7 | — | TASK-017 | — | VERIFY-AC-7 | — | blocked |
| FR-10 | — | — | TASK-019 | — | VERIFY-FR-10 | — | blocked |
| FR-11 | — | — | TASK-018 | — | VERIFY-FR-11 | — | blocked |
| FR-12 | AC-8 | — | TASK-020 | — | VERIFY-AC-8 | — | blocked |

## Acceptance criteria

| Req | AC | Decision | Task | Code/Diff | Verification | Review | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FR-5, G1 | AC-1 | — | TASK-016 | — | VERIFY-AC-1 | — | planned |
| FR-5 | AC-2 | DEC-001 | TASK-016 | — | VERIFY-AC-2 | — | planned |
| FR-8, R-1 | AC-3 | — | TASK-007, TASK-013 | — | VERIFY-AC-3 | — | planned |
| NFR-4 | AC-4 | — | TASK-003 | — | VERIFY-AC-4 | — | planned |
| FR-2 | AC-5 | — | TASK-005 | — | VERIFY-AC-5 | — | planned |
| FR-6 | AC-6 | — | TASK-008 | — | VERIFY-AC-6 | — | planned |
| FR-9 | AC-7 | — | TASK-017 | — | VERIFY-AC-7 | — | blocked |
| FR-12 | AC-8 | — | TASK-020 | — | VERIFY-AC-8 | — | blocked |

## Invariants

| Req | AC | Task | Status |
| --- | --- | --- | --- |
| INV-1 | — | TASK-019 | blocked |
| INV-4 | — | TASK-021 | blocked |
| INV-6 | — | TASK-011 | planned |
| INV-7 | — | TASK-014 | planned |

## Goals

| Req | Task | Status |
| --- | --- | --- |
| G4 | TASK-016 | planned |

## Section 13 reuse map (Phase 0 resolved)

Resolved per `docs/spec-v0.4.md` §13 and packet 03 separability audit (`.workflow/phase-0-evidence-audit/packets/03-separability.md`). All provisional PORT rows downgraded to **LIFT** because upstream Docket/Crucible/Tumbler repos are inaccessible for import-surface audit; Process reuse and BUILD unchanged.

| # | Spec item | Source | What carries over | Spec mode | Phase 0 mode | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FR-2 pre-prompt secret scanner | Docket | Pre-flight secret detection gate | PORT | **LIFT** | Packet 03 row 1: upstream `safety`/pre-flight module UNVERIFIED; target `safety.py` + `detect-secrets`-class lib architecturally standalone |
| 2 | INV-6 conservation accounting | Docket | Conservation ledger: inputs == accounted outputs | PORT | **LIFT** | Packet 03 row 2: conservation ledger in `aggregate.py` UNVERIFIED; local accounting pattern, not ADK-dependent in plan |
| 3 | FR-5 independent multi-reviewer fan-out | Docket / Crossfire practice | Orchestration pattern; agent code only if separable from ADK runtime | LIFT (PORT pending) | **LIFT** | Packet 03 row 3: ADK runtime excluded in implementation plan; no evidence Docket agents separate from ADK |
| 4 | FR-7 merge + agreement counting | Crucible | Multi-model debate merge; delta-as-metric scoring | PORT | **LIFT** | Packet 03 row 4: Crucible merge module UNVERIFIED; reimplement rapidfuzz cluster + judge merge per plan |
| 5 | AC-2 no manufactured findings | Crucible | Anti-sycophancy protocol prompts and tests | PORT | **LIFT** | Packet 03 row 5: anti-sycophancy prompts/tests UNVERIFIED; spec §5 structural controls (no `risk` type) ship as BUILD anyway |
| 6 | R-1 injection separation, schema-or-discard | Tumbler (Phase 3) | Prompt-injection isolation module | PORT | **LIFT** | Packet 03 row 6: Tumbler isolation module UNVERIFIED; `prompts.py` contract is greenfield-liftable |
| 7 | FR-8 final secret pre-filter | Tumbler | Secret pre-filter over rendered output | PORT | **LIFT** | Packet 03 row 7: Tumbler pre-filter UNVERIFIED; mirror FR-2 scanner over rendered output in `render.py` |
| 8 | Phase gating discipline | Crucible → Tumbler handoff | PASS-only gate protocol | Process reuse | **Process reuse** | Packet 03 row 8: PASS-only gates documented in `docs/implementation-plan-v0.4.md` § Delivery strategy / Phase exit gates; no code port required |
| 9 | Vertex provider adapter | Docket / Tumbler | Vertex AI client integration; matches maintainer GCP-native stack | PORT | **LIFT** | Packet 03 row 9: shared `vertex.py` UNVERIFIED; httpx Vertex client reimplemented per plan stack |
| 10 | §10 rubric, FR-3 fields, NFR-4 identity, FR-12 self-test | — | New to this system | BUILD | **BUILD** | Packet 03 row 10: new to Crossfire-Forge; no upstream source named in §13 — greenfield implementation |
