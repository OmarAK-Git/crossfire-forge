# Phase 2 — Live verification

Date: 2026-07-06  
Status: **CONTESTED** — mixed-roster remediation in progress; gate flips only on R6 independent review.

Supersedes fake-pipeline deferrals in `0-VERIFICATION.md`. Self-gatekeeper review remains **void**.

## Evidence lineage

| Stage | Roster | Artifact |
| --- | --- | --- |
| Single-family baseline | five `gemini-2.5-flash` | `artifacts/single-family-baseline.json` |
| Mixed roster (R1) | flash×2, pro×2, claude×1 | `artifacts/live-ac-summary.json` |

## Checks (mixed roster, pinned K/N)

| Check | K/N | Result | Artifact |
| --- | --- | --- | --- |
| AC-1 | 4-of-5 | pending live run | `artifacts/live-ac-summary.json` |
| AC-2 | 4-of-5 | pending live run | same |
| AC-3 | 5-of-5 | pending live run (v0.5 behavioral evaluator) | same |
| Demo ledger | — | pending | `artifacts/ledger-441.md` |
| Structural pytest | — | 129/129 pass | `python -m pytest tests/ -q` |

## Reproduce

```bash
pip install -e ".[dev,vertex]"
python scripts/run_live_ac_trials.py
```

Requires: gcloud ADC (Vertex), `ANTHROPIC_API_KEY` (Claude slot).

## Gate status

**CONTESTED.** Frank is audience, not reviewer. Independent R6 review required.
