# Memory Bank

Live projections for agent context. **Authoritative sources** remain `docs/spec-v0.4.md` and `docs/implementation-plan-v0.4.md`; update these files when those docs change, then refresh the matching memory-bank entries.

## Layout

| File / dir | Role |
| --- | --- |
| `projectbrief.md` | One-liner, goals, non-goals (from spec §1–4) |
| `activeContext.md` | Current phase, active `.workflow/<slug>/`, constraints |
| `tasks.md` | Task checklist — mirrors implementation plan |
| `progress.md` | Phase exit-gate status |
| `traceability.md` | Requirement traceability matrix (RTM) |
| `creative/` | Design decisions distilled from spec |
| `reflection/` | Session reflections (populated at phase end) |
| `archive/` | Completed run summaries moved from `.workflow/` |

## Workflow convention

Every phase and multi-step task runs under `.workflow/<slug>/` with `plan.md` as human source of truth and `state.json` as machine state. See `OPS.md`.
