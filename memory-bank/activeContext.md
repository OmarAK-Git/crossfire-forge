# Active Context

Last updated: 2026-07-05

## Current focus

**Phase 0 — Evidence, baseline & separability audit** (2–3 h, parallel with Phase 1)

Active workflow run: `.workflow/phase-0-evidence-audit/`

## Tier

T3 — full accountable loop per phase under `.workflow/<slug>/`.

## Constraints

- PASS-only gates: no phase begins until predecessor exit gate passes.
- Two-surface protocol: implementation on agentic IDE; gatekeeper review on independent surface at every gate.
- Do not build against UNVERIFIED items in spec §2.
- Phase 3 blocked on D-2; Phase 4 blocked on D-1 and D-3.

## Next actions

1. ~~Run three `gh` queries → `baseline.json`~~ **done** (packet 01-gh-baseline; repo `fkc1e100/gcp-template-forge`)
2. Inspect `sandbox-validation-*.yml` for path filters (packet 02-path-filters).
3. Separability audit: Docket, Crucible, Tumbler PORT rows (spec §13).
4. Resolve every §13 row to final PORT/LIFT/BUILD mode.
5. Gatekeeper review of baseline methodology; git-commit `baseline.json` for VERIFY-P0-001 exit.

## Canonical docs

- Spec: `docs/spec-v0.4.md`
- Plan: `docs/implementation-plan-v0.4.md`
