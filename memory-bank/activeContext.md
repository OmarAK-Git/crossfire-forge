# Active Context

Last updated: 2026-07-05

## Current focus

**Phase 2 complete — solo-scope build done.** Awaiting maintainer buy-in (D-2) before Phase 3 (advisory GitHub Action).

Latest verification: `.workflow/phase-2-review-engine/0-VERIFICATION.md` (passed, 117/117 pytest).

## Tier

T3 — full accountable loop per phase under `.workflow/<slug>/`.

## What exists now

- `crossfire_forge/` — CLI review engine (schemas, safety, hashing, Layer 0, prompts, fake + Vertex/second providers, aggregator, renderer, harness)
- `tests/` — 117 pytest cases; five Epic fixtures + pinned corpus
- `artifacts/ledger-441.md` — demo ledger from sanitized fake-reviewer pipeline (G4 evidence)
- `baseline.json` — historical fix-commits-per-PR and time-to-merge distributions (Phase 0)

## Constraints

- PASS-only gates: no phase begins until predecessor exit gate passes.
- Two-surface protocol: implementation on agentic IDE; gatekeeper review on independent surface at every gate.
- Phase 3 blocked on **D-2** (maintainer buy-in + secrets for in-repo Action).
- Phase 4 blocked on **D-1** (ingestion unit) and **D-3** (paired sandbox validation).
- Semantic AC-1..AC-3 live pass-K-of-N trials deferred — requires maintainer Vertex credentials (`LIVE_MODEL_APPROVAL_REQUIRED` in `harness.py`).

## Next actions (maintainer-facing)

1. **Demo** — run pytest + `crossfire-forge review` on `epic_441.md`; attach `artifacts/ledger-441.md` to DM draft.
2. **Approve D-2** — secrets + installation approval to enable Phase 3 Action mode.
3. **Optional live trial** — run Vertex reviewers against fixtures with maintainer GCP credentials to close semantic AC deferrals.

## Canonical docs

- Spec: `docs/spec-v0.4.md`
- Plan: `docs/implementation-plan-v0.4.md`
- Demo artifact: `artifacts/ledger-441.md`
