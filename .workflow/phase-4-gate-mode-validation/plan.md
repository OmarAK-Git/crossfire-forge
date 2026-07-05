# Phase 4 — Gate-mode design + paired validation

Run slug: `phase-4-gate-mode-validation`  
Source: `docs/implementation-plan-v0.4.md` § Phase 4 (Tasks 21–22)  
**Status: BLOCKED on D-1 and D-3**

## Goal

Gate mode stays unimplemented in v0.1; document fail-open vs fail-closed decision; run paired validation study only in maintainer collaboration.

## Success Criteria

- Gate-mode design note exists; INV-4 test proves no label application path
- Paired validation study pre-registered (null result acceptable)

## Current Context

Blocked on D-1 (ingestion unit) and D-3 (maintainer sandbox for paired study).

## Constraints

- No v0.1 code path applies any label (INV-4)
- Gate-mode authorization hash-bound, never label-carried (future)

## Risks

| Risk | Approval required | Mitigation |
| --- | --- | --- |
| Scope creep into gate implementation | no | Design note only; no gate-mode code |

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| 21-design-note | TASK-021 gate-mode design note | implementer | blocked |
| 22-paired-study | TASK-022 paired validation | orchestrator | blocked |

## Verification

See `verification-ledger.md`.

## Reusable Artifacts

- `docs/decisions/gate-mode-design.md` (planned)
