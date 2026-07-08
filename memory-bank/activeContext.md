# Active Context

Last updated: 2026-07-08

## Current focus

**Phase 2 gate is PASS** (R6 recorded 2026-07-08). Mixed-roster semantic trials completed live: AC-1 5/5, AC-2 4/5, AC-3 5/5 at pinned K/N (`artifacts/live-ac-summary.json`, 2026-07-08T17:59:54Z). Demo ledger `artifacts/ledger-441.md` is live mixed-roster output from Epic #441's verbatim body. Current work: outreach-doc sync and in-person pitch prep.

## What shipped

- `--provider vertex` and `--provider mixed` CLI paths (gcloud ADC + optional Anthropic)
- `scripts/run_live_ac_trials.py` — pinned K/N harness for AC-1..AC-3; full mixed-roster run recorded 2026-07-08
- AC-2 Phase C corroboration rule (PR #1): fail on any violation/safety_warning and on corroborated BR-2+ (agreement ≥ 2); tolerate uncorroborated BR-2+ assumption singletons — `docs/design-note-ac2-corroboration-rule.md`
- R2 evaluator ruling signed (bug fix); R0 history rewrite verified clean; repo renamed `crossfire-forge`
- `artifacts/single-family-baseline.json` — prior single-family interim evidence (superseded)

## Known residuals

- `live-ac-summary.json` stamps AC-3 `provisional: true` via a hard-coded flag in `ac_trials.py` — stale now that the R2 ruling is signed; superseded by the gate record, fix stamping before any future run.
- Corroboration rule couples to the lexical clusterer's `agreement_count` (tracked in `docs/design-note-ac2-corroboration-rule.md`).

## Maintainer ask (Frank only)

1. **D-2** — Action buy-in + secrets
2. **D-1** — ingestion unit answer

## Next

In-person pitch (demo ledger + live AC summary) → D-2 approval → Phase 3 GitHub Action; D-1/D-3 gate Phase 4 paired study.
