# Progress

Source: `docs/implementation-plan-v0.4.md` exit gates. Last verified: 2026-07-05.

| Phase | Workflow slug | Status | Exit gate |
| --- | --- | --- | --- |
| 0 | `phase-0-evidence-audit` | **passed** | `baseline.json`; §13 resolved; path-filter recorded |
| 1 | `phase-1-contract-harness` | **passed** | 59 pytest green; AC-5; gatekeeper PASS |
| 2 | `phase-2-review-engine` | **passed** | 117 pytest green; AC-1–6 (semantic deferrals); gatekeeper PASS; `ledger-441.md` |
| 3 | `phase-3-github-action` | **blocked (D-2)** | AC-7, AC-8; gatekeeper PASS |
| 4 | `phase-4-gate-mode-validation` | **blocked (D-1, D-3)** | design note; paired study |

## v0.1 exit criteria

- [x] `pytest` passes (117/117 as of 2026-07-05)
- [x] AC-1–AC-6 covered by tests/harness (semantic AC-1..AC-3 live trials deferred)
- [x] `crossfire-forge review` produces golden-format ledger; `artifacts/ledger-441.md` via sanitized pipeline
- [ ] Action mode (AC-7, AC-8) — Phase 3, blocked on D-2
- [x] No code path applies `status:ai-agent-active` or any label
- [x] Gatekeeper PASS on Phases 0, 1, 2 exit gates

## Deferred (non-blocking, documented)

- Live semantic pass-K-of-N for AC-1 (4-of-5 BR-3 RBAC), AC-2 (4-of-5 complete epic), AC-3 (5-of-5 injection E2E) — needs maintainer Vertex credentials
- `ledger-441.md` is a fake-pipeline demo (BR-2), not a live-model BR-3 artifact
- NFR-3 provider timeouts — mock-tested only
- FR-6 GitHub workflow warning annotation — in-process discard metering only until Action mode

## Repository layout (implemented)

```text
crossfire_forge/          # package (schemas through harness; no github/ yet)
tests/fixtures/           # five Epics + README corpus
tests/golden/             # ledger format golden
artifacts/ledger-441.md   # demo output
baseline.json             # Phase 0 historical baseline
```

Not yet built: `crossfire_forge/github/`, `.github/workflows/spec-review*.yml`
