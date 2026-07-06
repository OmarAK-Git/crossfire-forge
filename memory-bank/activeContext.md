# Active Context

Last updated: 2026-07-06

## Current focus

**Phase 2 gate is CONTESTED.** Structural harness is green; mixed-roster semantic trials and independent R6 review are pending. Demo ledger and `live-ac-summary.json` are placeholders until `scripts/run_live_ac_trials.py` completes a mixed run.

## What shipped

- `--provider vertex` and `--provider mixed` CLI paths (gcloud ADC + optional Anthropic)
- `scripts/run_live_ac_trials.py` — pinned K/N harness for AC-1..AC-3 (awaiting live mixed-roster run)
- `artifacts/single-family-baseline.json` — honest interim single-family evidence
- Upstream diff: `.workflow/port-validation/safety-prompts-diff.md`
- Self-gatekeeper invalidated; `LIVE_MODEL_APPROVAL_REQUIRED` removed

## Maintainer ask (Frank only)

1. **D-2** — Action buy-in + secrets
2. **D-1** — ingestion unit answer

## Next

Complete mixed-roster live trials → R6 independent review → Phase 3 GitHub Action after D-2 approval.
