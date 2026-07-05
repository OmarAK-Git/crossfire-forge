# Task — phase-0-03-separability

## Goal

Complete Phase 0 packet 03-separability: audit Docket, Crucible, and Tumbler import surfaces for the spec section 13 reuse rows.

## Success Criteria

- Every source system named in docs/spec-v0.4.md section 13 is considered: Docket, Crucible, Tumbler, Crossfire practice, process reuse, Vertex adapter, and BUILD rows.
- The packet records evidence-backed separability findings for Docket pre-flight secret gate, Docket conservation ledger, Docket reviewer fan-out versus ADK runtime, Crucible merge/anti-sycophancy surfaces, Tumbler isolation/pre-filter surfaces, phase-gating discipline, and Vertex provider adapter.
- Each provisional PORT row receives a packet-level recommendation: PORT, LIFT, BUILD, or Process reuse.
- The verifier checks only packet 03 acceptance, not full Phase 0 completion.

## Constraints

- Packet-level Phase 0 research only. Produce separability evidence and recommendations; do not run the full Phase 0 exit gate.
- Allowed files only (see implementer packet).
- Read-only upstream inspection via `gh` or raw GitHub URLs is permitted.

## Risks

| Risk | Approval required | Mitigation |
| --- | --- | --- |
| Source repos unavailable locally | yes | Use read-only `gh api` / raw.githubusercontent.com |
| Over-scoping to full Phase 0 exit | no | Task verifier scope is `task` only |

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| implementer | Audit import surfaces; write packet + state update | gsd-executor | pending |

## Verification

| ID | Requirement | Check | Expected |
| --- | --- | --- | --- |
| VERIFY-TASK-001 | Packet exists | `Test-Path .workflow\phase-0-evidence-audit\packets\03-separability.md` | true |
| VERIFY-TASK-002 | Packet covers systems | `Select-String Docket,Crucible,Tumbler,PORT,LIFT,BUILD 03-separability.md` | matches |
