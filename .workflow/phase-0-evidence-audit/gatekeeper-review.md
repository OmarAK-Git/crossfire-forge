# Gatekeeper Review — Phase 0 Packet 01 (GH Baseline)

**Reviewed:** 2026-07-05T05:01:00Z  
**Reviewer:** Independent gatekeeper (phase-0-gatekeeper-baseline)  
**Verdict:** **PASS**

## Scope

Cross-checked internal consistency across:

| Artifact | Role |
| --- | --- |
| `baseline.json` | Published baseline (distributions, PR #482, stall story) |
| `.workflow/phase-0-evidence-audit/packets/01-gh-baseline.md` | Methodology and query summary |
| `.workflow/phase-0-evidence-audit/results/pr-raw.jsonl` | Raw PR enumeration (255 rows) |
| `.workflow/phase-0-evidence-audit/results/pr-details.json` | Per-PR commit counts and merge metadata |
| `.workflow/phase-0-evidence-audit/results/compute_baseline.py` | Reproducible computation script |

## Verification Method

1. **Python recomputation** (offline, from cached `pr-details.json` + `pr-raw.jsonl`, using the same `dist()` and formula logic as `compute_baseline.py`).
2. **Manual spot-check** of PR #482 row in all three PR artifacts vs `baseline.json` queries and `stall_story_evidence`.

Live re-run of `compute_baseline.py` against the GitHub API was **not** performed (requires network + 255 API calls); offline recomputation from cached artifacts is sufficient to validate published numbers.

## Checks Performed

### 1. PR population counts

| Metric | baseline.json | pr-raw.jsonl | pr-details.json | Match |
| --- | ---: | ---: | ---: | --- |
| Total PRs | 255 | 255 | 255 | ✓ |
| Merged | 170 | — | 170 (`merged_at` set) | ✓ |
| Open | 2 | 2 (`state: open`) | 2 | ✓ |
| Closed unmerged | 83 | — | 83 | ✓ |

`170 + 2 + 83 = 255` — partition is complete and consistent.

### 2. Fix commits formula: `max(0, commit_count - 1)`

- Recomputed across all 255 rows in `pr-details.json`.
- **Violations: 0**
- PR #482: `commit_count=2`, `fix_commits=1` in both `pr-details.json` and `baseline.json` → ✓

### 3. Distribution statistics

Recomputed `fix_commits_per_pr`, `total_commits_per_pr`, and `time_to_merge_hours` from `pr-details.json` using the script's `dist()` helper (sorted-array p25/p75, `statistics.median`, rounded mean):

| Distribution | count | median | mean | p75 | max |
| --- | ---: | ---: | ---: | ---: | ---: |
| fix_commits_per_pr | 255 | 0 | 4.05 | 3 | 29 |
| total_commits_per_pr | 255 | 1 | 5.01 | 4 | 30 |
| time_to_merge_hours | 170 | 0.0192 | 5.07 | 2.82 | 91.25 |

All values **exact match** `baseline.json` `distributions` block. Packet 01 summary table matches (rounded display only).

### 4. PR #482 stall story evidence

| Field | baseline.json | pr-details / pr-raw | Consistent |
| --- | --- | --- | --- |
| `state` | `open` | `open` | ✓ |
| `commit_count` / `fix_commits` | 2 / 1 | 2 / 1 | ✓ |
| `merged_at` | `null` | `null` | ✓ |
| `created_at` | `2026-05-29T21:11:34Z` | same in pr-raw | ✓ |
| `failed_checks` | Circuit Breaker; KCC Provision (templates/gke-k8s-rbac-manager) | — | ✓ (snapshot in baseline) |
| `stall_story_evidence.pr_482_open` | `true` | PR state open | ✓ |
| `stall_story_evidence.pr_482_kcc_provision_failed` | `true` | KCC in `failed_checks` | ✓ |
| `stall_story_evidence.pr_482_circuit_breaker_failed` | `true` | Circuit Breaker in `failed_checks` | ✓ |
| `check_conclusions.failure` | 2 | len(`failed_checks`) = 2 | ✓ |

`issue_479_open` and `epic_441_open` are **not** present in `pr-raw.jsonl` or `pr-details.json` (separate issue API queries per packet 01). Values in `baseline.json` align with packet 01 narrative; not independently re-verified from issue artifacts in this review.

### 5. Packet 01 vs baseline.json

- Documented PR total (255), closed issues (198), distribution medians/means, and PR #482 stall narrative all match `baseline.json`.
- Methodology notes (`fix_commits` formula, time-to-merge for merged PRs only) match script implementation.

## Limitations (non-blocking)

These do **not** fail the methodology review but should be noted for downstream consumers:

1. **`compute_baseline.py` partial hardcoding** — `closed_issues_non_pr.count` (198), `issue_479_open`, `epic_441_open`, and PR #482 metadata fields (`closes_issue`, `parent_epic`, `generated_by`) are literals in the script, not derived from cached JSONL/JSON artifacts. Full end-to-end offline replay requires additional issue-query artifacts.
2. **Check-run snapshot** — PR #482 check conclusions are pinned to commit `ea3701d…` at generation time; live re-run may differ if checks changed since 2026-05-31.
3. **`baseline.json` uncommitted** — tracked separately in VERIFY-P0-001; does not affect methodology consistency.

## Verdict Rationale

**PASS** — All PR-level counts, the fix-commits formula, distribution statistics, and PR #482 stall-story fields that can be derived from `pr-raw.jsonl` and `pr-details.json` are internally consistent with `baseline.json` and with the methodology documented in packet 01. No blocking gaps found.

---

_Independent gatekeeper review — phase-0-gatekeeper-baseline_
