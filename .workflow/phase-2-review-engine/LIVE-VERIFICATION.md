# Phase 2 — Live Vertex verification

Date: 2026-07-06  
Status: **passed** (semantic AC-1..AC-3 live on Omar's gcloud project)

Supersedes fake-pipeline deferrals in `0-VERIFICATION.md`. Self-gatekeeper review remains **void**.

## Evidence

| Check | Result | Artifact |
| --- | --- | --- |
| AC-1 (4-of-5) | 5/5 pass | `artifacts/live-ac-summary.json` |
| AC-2 (4-of-5) | 5/5 pass | same |
| AC-3 (5-of-5) | 5/5 pass | same |
| Demo ledger | Live Vertex | `artifacts/ledger-441.md` (BR-3 RBAC assumptions, `vertex-reviewer-*` roster) |
| Structural pytest | 116/116 pass | `python -m pytest tests/ -q` |

## Vertex config used

- Project: `REDACTED` (gcloud default)
- Location: `us-central1`
- Model: `gemini-2.5-flash`
- Auth: Application Default Credentials via `gcloud auth application-default`

## Reproduce

```bash
pip install -e ".[dev,vertex]"
python scripts/run_live_ac_trials.py
```

## Gate status

Phase 2 solo-scope build **complete** pending independent gate review (not self-attestation). Maintainer ask for Frank: **D-2** and **D-1** only.
