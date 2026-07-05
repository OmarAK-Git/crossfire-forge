# Orchestration — phase-2-11-aggregator

Controller: `.cursor/commands/gsd-autopilot-loop.md`

## Dispatch

1. Implementer (`gsd-executor`) runs against `packets/implementer.md`.
2. Controller sanity-checks diff and scope.
3. Fresh-context verifier (`gsd-verifier`) checks task acceptance only.
4. Queue updated only after verifier evidence.
