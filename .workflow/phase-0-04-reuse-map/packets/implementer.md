# Implementation Packet — phase-0-04-reuse-map

## Objective

Use packet 03 separability evidence to finalize the §13 reuse map in memory-bank/traceability.md and record packet 04 result.

## Original User Goal

Complete Phase 0 packet 04-reuse-map: update memory-bank traceability with final section 13 reuse modes.

## Evidence source (read)

- `.workflow/phase-0-evidence-audit/packets/03-separability.md` — final recommendations (7 PORT→LIFT, 1 LIFT, 1 Process reuse, 1 BUILD)
- `docs/spec-v0.4.md` §13 — 10 rows

## Allowed Files (write)

- `memory-bank/traceability.md` (add §13 reuse-map section)
- `.workflow/phase-0-evidence-audit/packets/04-reuse-map.md` (create summary packet)
- `.workflow/phase-0-evidence-audit/state.json` (packet 04 status only)
- `.workflow/phase-0-evidence-audit/verification-ledger.md` (VERIFY-P0-004 row only)

## Acceptance Criteria

1. Add `## Section 13 reuse map (Phase 0 resolved)` to traceability.md with all 10 rows and final modes from packet 03.
2. Each row cites packet 03 evidence or explains BUILD.
3. Create packets/04-reuse-map.md summarizing the integration.
4. Update packet 04 status in state.json to `done`.
5. Update VERIFY-P0-004 to pass with packet-level note.

## Verification Commands

```powershell
Select-String -Path memory-bank\traceability.md -Pattern 'section 13','FR-2 pre-prompt secret scanner','Vertex provider adapter','BUILD'
Select-String -Path .workflow\phase-0-evidence-audit\verification-ledger.md -Pattern 'VERIFY-P0-004'
```

Write implementer result to `.workflow/phase-0-04-reuse-map/results/implementer-result.md`
Do NOT mark queue complete.
