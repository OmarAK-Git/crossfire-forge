# Phase 3 — Advisory GitHub Action

Run slug: `phase-3-github-action`  
Source: `docs/implementation-plan-v0.4.md` § Phase 3 (Tasks 17–20)  
**Status: BLOCKED on D-2** (maintainer secrets + installation approval)

## Goal

Action updates one comment per Epic, persists sanitized artifacts only, cancels stale runs, banners stale reviews, self-tests without issue noise.

## Success Criteria

- AC-7: two mocked runs → one updated comment
- AC-8: broken config fails visibly; no issue comments from self-test
- Gatekeeper PASS
- NFR-5: no `labels: write` in permissions block

## Current Context

Blocked until maintainer provides D-2 buy-in and secrets configuration.

## Constraints

- INV-7: Action entrypoint has no `--debug-raw-envelopes`
- NFR-1 fail-open: failures annotate, never block factory
- FR-12 self-test posts nothing to issues

## Risks

| Risk | Approval required | Mitigation |
| --- | --- | --- |
| Secrets misconfiguration | yes | Self-test AC-8; fork PRs get no secrets by platform |
| TOCTOU stale window (R-6) | no | Document residual; stale banner best-effort |

## Work Packets

| ID | Objective | Owner | Status |
| --- | --- | --- | --- |
| 17-upsert | TASK-017 comment upsert | implementer | blocked |
| 18-auth | TASK-018 authorization | implementer | blocked |
| 19-workflow | TASK-019 workflow YAML | implementer | blocked |
| 20-selftest | TASK-020 weekly self-test | implementer | blocked |

## Verification

See `verification-ledger.md`.

## Reusable Artifacts

- `.github/workflows/spec-review.yml`, `spec-review-selftest.yml`
- `crossfire_forge/github/`
