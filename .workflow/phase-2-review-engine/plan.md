# Phase 2 — Review engine and ledger

Run slug: `phase-2-review-engine`  
Source: `docs/implementation-plan-v0.4.md` § Phase 2 (Tasks 10–16)

## Goal

CLI produces maintainer-facing sanitized ledger from pinned fixtures, then live models; demo `ledger-441.md` via fully sanitized pipeline.

## Success Criteria

- AC-1 through AC-6 covered by tests or harness scripts
- INV-6 conservation demonstrated on aggregator
- Gatekeeper PASS
- `artifacts/ledger-441.md` attached to DM draft

## Current Context

- Requires Phase 1 exit gate PASS
- Ends solo-scope build; Phase 3 blocked on maintainer D-2

## Constraints

- Fake-reviewer E2E before live Vertex/second provider calls
- Lexical clustering threshold pinned with labeled pairs (TASK-012)
- `--debug-raw-envelopes` absent from Action entrypoint by construction (INV-7)

## Risks

| Risk | Approval required | Mitigation |
| --- | --- | --- |
| Live model cost/variance | yes | pass-K-of-N harness; pinned roster in ledger header |
| Threshold tuning unstable | no | Commit pair set + justification with threshold |

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| 10-providers | TASK-010 provider adapters | implementer | pending |
| 11-aggregator | TASK-011 aggregator + INV-6 | implementer | pending |
| 12-threshold | TASK-012 clustering threshold | implementer | pending |
| 13-render | TASK-013 renderer + sanitizer | implementer | pending |
| 14-cli | TASK-014 CLI review command | implementer | pending |
| 15-layer0 | TASK-015 Layer 0 parser | implementer | pending |
| 16-harness | TASK-016 pass-K-of-N + ledger-441 | implementer | pending |

## Verification

See `verification-ledger.md`.

## Reusable Artifacts

- `artifacts/ledger-441.md`, `tests/golden/`, provider adapters
