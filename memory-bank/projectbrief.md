# Crossfire-Forge — Project Brief

Source: `docs/spec-v0.4.md` (CONSOLIDATED, ready for Phase 0).

## One-liner

A non-blocking spec-review stage for the Forge Factory: a deterministic completeness check (Layer 0) plus a multi-model adversarial review (Layer 1) over an Epic, emitting one ranked **assumption ledger** as a single idempotent issue comment — before the factory commits real infrastructure.

## Goals

- **G1** — Surface and rank silent architectural assumptions an Epic forces the Factory to make.
- **G2** — Flag conflicts with repository standards, grounded in cited authoritative documents.
- **G3** — Zero changes to factory daemons, zero human turns, zero blocking, zero labels in v0.1.
- **G4** — Maintainer buy-in evidence: real ledger from Epic #441 via fully sanitized pipeline.

## Non-goals (v0.1)

- NG1 — Interactive clarification questions.
- NG2 — Reviewing sub-issues (unless maintainer confirms otherwise).
- NG3 — Modifying Epics, applying labels, or touching factory code.
- NG4 — Cost accounting or budget caps.
- NG5 — Byte-level deterministic model output (format determinism only).
- NG6 — Persisting raw reviewer transcripts to GitHub-managed storage.
- NG7 — Violation findings without corpus citation.

## Delivery strategy

CLI-first, fakes-first. Build engine as standalone CLI against pinned fixtures; fake reviewer before live models; advisory GitHub Action only after demo + maintainer secrets (D-2).

## Stack

Python 3.12, pydantic v2, httpx, typer, pytest, detect-secrets-class scanner, rapidfuzz. Vertex AI adapter first.

## Open dependencies

- **D-1** — Maintainer: ingestion unit and decomposition mechanics.
- **D-2** — Maintainer: buy-in + secrets for in-repo Action (blocks Phase 3).
- **D-3** — Paired deploy-run validation requires maintainer sandbox.
