# Phase 0 — Evidence, baseline & separability audit

Run slug: `phase-0-evidence-audit`  
Source: `docs/implementation-plan-v0.4.md` § Phase 0

## Goal

Confirm or drop the #479/#482 stall story; extract historical baseline; establish docs-PR safety; resolve the spec §13 reuse map before implementation commits to PORT paths.

## Success Criteria

- `baseline.json` committed with fix-commits-per-PR and time-to-merge distributions
- Spec §2 stall line marked CONFIRMED or DROPPED with evidence
- `sandbox-validation-*.yml` path-filter answer recorded
- Every spec §13 row resolved to final PORT / LIFT / BUILD mode

## Current Context

- Spec v0.4 CONSOLIDATED; no application code yet
- Phase 0 runs parallel with Phase 1 start (skeleton can begin after audit items that block PORT decisions)
- Active memory-bank: `memory-bank/activeContext.md`

## Constraints

- Do not build against UNVERIFIED spec §2 dependencies
- PASS-only: Phase 1 full PORT work waits on separability audit outcomes where contingent
- Two-surface protocol: gatekeeper reviews audit artifacts independently

## Risks

| Risk | Approval required | Mitigation |
| --- | --- | --- |
| PORT rows fail separability audit | no | Downgrade to LIFT per plan; no spec change |
| `gh` access unavailable for baseline queries | yes | Record blocker; use manual maintainer-provided exports |
| Wrong ingestion unit assumed (D-1) | no | Flag UNVERIFIED; do not implement gate-mode paths |

## Approval Required

- External `gh` queries against maintainer's repo (read-only)

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| 01-gh-baseline | Run three gh queries → `baseline.json` | implementer | done |
| 02-path-filters | Inspect sandbox-validation workflows for `paths:` | researcher | pending |
| 03-separability | Audit Docket/Crucible/Tumbler import surfaces | researcher | pending |
| 04-reuse-map | Resolve §13 table to final modes | orchestrator | pending |

## Integration Policy

- Research packets return `file:line` evidence only; no code edits
- `baseline.json` merged only after gatekeeper confirms query methodology
- Failed PORT → update memory-bank/traceability.md and phase-1 packets

## Verification

See `verification-ledger.md`. Exit gate: all VERIFY rows pass.

## Reusable Artifacts

- `baseline.json`
- Separability audit memo → `memory-bank/creative/` or `docs/decisions/`
- Updated `memory-bank/traceability.md` §13 resolutions
