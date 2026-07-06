# Phase 0 evidence verification (human + reproducible)

Date: 2026-07-05  
Status: **verified against saved artifacts** (not agent prose alone)

## Artifacts checked

| Artifact | Path | Result |
| --- | --- | --- |
| Baseline JSON | `baseline.json` | Valid JSON; `fix_commits_per_pr.count` = 255 matches `pr-details.json` row count |
| Raw PR list | `.workflow/phase-0-evidence-audit/results/pr-raw.jsonl` | 255 lines |
| Per-PR commit counts | `.workflow/phase-0-evidence-audit/results/pr-details.json` | 255 entries |
| Recompute script | `.workflow/phase-0-evidence-audit/results/compute_baseline.py` | Exists; reads `pr-raw.jsonl`, writes distributions |

## Distribution spot-check (`baseline.json`)

- `fix_commits_per_pr`: n=255, median=0, p75=3, mean=4.05, max=29
- `time_to_merge_hours`: n=170 (merged PRs only)
- `all_prs`: total=255, merged=170, open=2

## Stall story evidence (query-backed fields in JSON)

- `pr_482_open`: true
- `pr_482_kcc_provision_failed`: true
- `pr_482_circuit_breaker_failed`: true
- PR #482 commit/fix counts present in `queries.pr_482`

## Path-filter claim

Recorded in packet `02-path-filters.md` with upstream file references. Re-fetch from public repo recommended before maintainer pitch if files may have changed since 2026-07-05.

## Note

`compute_baseline.py` re-fetches live `gh` data for PR commit counts when run fresh; committed `pr-details.json` is the frozen evidence for the recorded distributions. Do not re-run full compute in CI without pinning — use saved `pr-details.json` for reproducibility checks.
