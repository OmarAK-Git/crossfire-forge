# Implementation Packet — phase-2-12-threshold

## Objective

Pin lexical clustering threshold with labeled duplicate/distinct pairs from fixtures; commit pair set + justification; tests prove duplicates cluster and distinct pairs stay separate.

## Original User Goal

Phase 2 Task 12 — threshold tuning: labeled duplicate/distinct pairs from fixtures; pin clustering threshold with recorded justification.

## Relevant Docs

- `docs/implementation-plan-v0.4.md` § Phase 2 Task 12
- `crossfire_forge/aggregate.py` — DEFAULT_CLUSTER_THRESHOLD placeholder from Task 11
- `tests/fixtures/` epic fixtures

## Allowed Files

- `crossfire_forge/aggregate.py` (pin threshold + justification constant/comment)
- `tests/fixtures/threshold_pairs.json` (labeled pairs)
- `tests/test_threshold.py`
- `.workflow/phase-2-review-engine/verification-ledger.md`

## Do Not Touch

- render.py, cli.py, layer0.py
- Full Phase 2 exit gate

## Acceptance Criteria

1. Labeled duplicate and distinct finding pairs derived from fixtures and committed in threshold_pairs.json
2. Clustering threshold pinned in code/config with recorded justification
3. Tests demonstrate duplicates cluster and distinct pairs stay separate at pinned threshold
4. pytest tests/test_threshold.py -v passes

## Verification

```powershell
pytest tests/test_threshold.py -v
```

Do NOT mark queue complete.
