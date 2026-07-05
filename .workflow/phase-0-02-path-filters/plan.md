# Task — phase-0-02-path-filters

## Goal

Complete Phase 0 packet 02-path-filters: inspect sandbox-validation workflows for paths filters and record the answer with evidence.

## Success Criteria

- The relevant sandbox-validation workflow files are inspected, or the task stops with an approval request for exact read-only upstream commands if those files are unavailable locally.
- The path-filter answer is recorded in `.workflow/phase-0-evidence-audit/packets/02-path-filters.md` with file:line or command-output evidence.
- VERIFY-P0-003 is updated with the packet-level result.
- The verifier checks only packet 02 acceptance, not full Phase 0 completion.

## Constraints

- Packet-level Phase 0 research only. Do not run or satisfy the full Phase 0 exit gate.
- Allowed files only (see implementer packet).
- Read-only upstream inspection via `gh` or raw GitHub URLs is permitted (same repo as packet 01: `fkc1e100/gcp-template-forge`).

## Risks

| Risk | Approval required | Mitigation |
| --- | --- | --- |
| Upstream workflows unavailable locally | yes | Use read-only `gh api` or raw.githubusercontent.com fetch |
| Over-scoping to full Phase 0 exit | no | Task verifier scope is `task` only |

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| implementer | Inspect workflows; write packet + ledger update | gsd-executor | pending |

## Verification

| ID | Requirement | Check | Expected |
| --- | --- | --- | --- |
| VERIFY-TASK-001 | Packet exists | `Test-Path .workflow\phase-0-evidence-audit\packets\02-path-filters.md` | true |
| VERIFY-TASK-002 | Ledger updated | `Select-String VERIFY-P0-003 verification-ledger.md` | match with pass/partial |
