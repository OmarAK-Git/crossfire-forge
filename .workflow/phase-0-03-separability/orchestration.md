# Orchestration — phase-0-03-separability

## Dispatch Policy

1. Implementer (`gsd-executor`) audits Docket, Crucible, and Tumbler import surfaces via read-only upstream inspection.
2. Implementer writes `.workflow/phase-0-evidence-audit/packets/03-separability.md` with evidence-backed recommendations per spec §13 row.
3. Implementer updates packet 03 status in `.workflow/phase-0-evidence-audit/state.json`.
4. Fresh-context verifier (`gsd-verifier`) checks task acceptance only — not full Phase 0 exit.

## Upstream Sources

- Discover maintainer repos via `gh repo list fkc1e100` or `gh search repos`
- Inspect actual module/import surfaces for: secret gate, conservation ledger, reviewer fan-out vs ADK, merge/anti-sycophancy, isolation/pre-filter, Vertex adapter
- Read-only access: `gh api` or raw.githubusercontent.com

## Do Not Touch

- `memory-bank/traceability.md` (packet 04 scope)
- `docs/spec-v0.4.md`
- Any file outside `files_allowed`
