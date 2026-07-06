# R6 — Independent gate review checklist

**Status:** CONTESTED — awaiting fresh-context reviewer (or owner)  
**Reviewer must NOT be:** Frank, the implementing agent, or anyone who authored the live iteration.

## Inputs to review

1. R0 public-exposure audit outcome (`.workflow/post-live-remediation-2026-07-05/R0-public-exposure-audit.md`)
2. Mixed-roster `artifacts/live-ac-summary.json` (pinned thresholds: AC-1 4-of-5, AC-2 4-of-5, AC-3 5-of-5)
3. Regenerated `artifacts/ledger-441.md` (model IDs in roster header, not `vertex-reviewer-*`)
4. R2 evaluator ruling (`R2-evaluator-ruling.md`) — human sign-off or provisional acceptance
5. Structural suite: `python -m pytest tests/ -q` → 129 pass

## Checklist

- [ ] R0 history scrub verified empty (`git log -S` for project ID and local paths)
- [ ] Mixed roster shows ≥2 distinct model families in ledger metadata
- [ ] AC-1..AC-3 pass at pinned K/N on mixed roster (not single-family)
- [ ] `live-ac-summary.json` contains aggregates only (no prompts, completions, project IDs, absolute paths)
- [ ] AC-3 evaluator change ruled (or explicitly accepted provisional)
- [ ] `safety_warning` fields defanged in rendered ledger
- [ ] No `gcloud auth print-access-token` in production code path
- [ ] Credential hygiene test passes

## Verdict

| Field | Value |
| --- | --- |
| Reviewer | ___ |
| Date | ___ |
| Verdict | PASS / CONTESTED / FAIL |
| Notes | ___ |

Gate flips to **PASS** only when verdict is PASS above.
