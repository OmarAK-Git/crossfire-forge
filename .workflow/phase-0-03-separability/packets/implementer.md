# Implementation Packet — phase-0-03-separability

## Objective

Audit Docket, Crucible, and Tumbler import surfaces against docs/spec-v0.4.md §13 reuse rows. Record evidence-backed separability findings and a provisional PORT/LIFT/BUILD/Process reuse recommendation per row.

## Original User Goal

Complete Phase 0 packet 03-separability: audit Docket, Crucible, and Tumbler import surfaces for the spec section 13 reuse rows.

## Relevant Docs and State

- `docs/spec-v0.4.md` §13 (10-row reuse table — authoritative)
- `docs/implementation-plan-v0.4.md` § Phase 0, § Repository layout, § Reuse map
- `.workflow/phase-0-evidence-audit/plan.md` (packet 03-separability)
- `.workflow/phase-0-evidence-audit/state.json` (update packet 03 status only)
- `.workflow/phase-0-evidence-audit/verification-ledger.md` (do NOT update VERIFY-P0-004 — that is packet 04 scope)

## Spec §13 Rows to Audit

| Spec item | Source | Provisional mode |
| --- | --- | --- |
| FR-2 pre-prompt secret scanner | Docket | PORT |
| INV-6 conservation accounting | Docket | PORT |
| FR-5 multi-reviewer fan-out | Docket / Crossfire practice | LIFT (PORT pending audit) |
| FR-7 merge + agreement counting | Crucible | PORT |
| AC-2 no manufactured findings | Crucible | PORT |
| R-1 injection separation | Tumbler | PORT |
| FR-8 final secret pre-filter | Tumbler | PORT |
| Phase gating discipline | Crucible → Tumbler | Process reuse |
| Vertex provider adapter | Docket / Tumbler | PORT |
| §10 rubric, FR-3, NFR-4, FR-12 | — | BUILD |

## Allowed Files (write)

- `.workflow/phase-0-evidence-audit/packets/03-separability.md` (create)
- `.workflow/phase-0-evidence-audit/state.json` (update packet 03 status only)
- `.workflow/phase-0-evidence-audit/verification-ledger.md` (optional: add packet-level note only if needed; do NOT update VERIFY-P0-004)

## Do Not Touch

- `memory-bank/traceability.md` (packet 04)
- `docs/spec-v0.4.md`
- `baseline.json`
- Any `.codex` / `.claude` files
- Full Phase 0 exit gate artifacts

## Acceptance Criteria

1. Every source system named in spec §13 is considered with evidence or documented access blocker.
2. Record separability findings for: Docket pre-flight secret gate, Docket conservation ledger, Docket reviewer fan-out vs ADK runtime, Crucible merge/anti-sycophancy, Tumbler isolation/pre-filter, phase-gating discipline, Vertex adapter, and BUILD row.
3. Each provisional PORT row gets a packet-level recommendation: PORT, LIFT, BUILD, or Process reuse — with file:line or command-output evidence where upstream code is accessible.
4. Update phase-0-evidence-audit state.json packet 03 status to `done`.

## Verification Commands

```powershell
Test-Path .workflow\phase-0-evidence-audit\packets\03-separability.md
Select-String -Path .workflow\phase-0-evidence-audit\packets\03-separability.md -Pattern 'Docket','Crucible','Tumbler','PORT','LIFT','BUILD'
```

## Upstream Discovery (read-only)

```powershell
gh repo list fkc1e100 --limit 30
gh search code "secret" user:fkc1e100 --limit 20
gh search code "conservation" user:fkc1e100 --limit 20
# If source repos are private/unavailable, document the blocker and use
# docs/implementation-plan-v0.4.md module mappings + architectural analysis
# with explicit UNVERIFIED flags where code cannot be inspected.
```

Known public maintainer repo: `fkc1e100/gcp-template-forge` (Forge Factory — not Docket/Crucible/Tumbler directly).

## Expected Result Schema

Return:
- `changed_files`: list of paths written
- `checks_run`: commands executed
- `findings_summary`: one paragraph on separability posture
- `recommendations_table`: 10 rows with final recommendation per §13 row
- `unresolved_risks`: access blockers, ADK coupling concerns
- `approval_gates`: any gates hit

Do NOT mark the queue item complete. Controller + verifier handle completion.
