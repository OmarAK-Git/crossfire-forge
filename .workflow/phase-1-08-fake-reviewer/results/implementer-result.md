# Implementer Result — phase-1-08-fake-reviewer

## changed_files

- `crossfire_forge/reviewers/__init__.py` (created — package exports for reviewer interface and fake reviewer)
- `crossfire_forge/reviewers/base.py` (created — `Reviewer` protocol, `ReviewResult`, schema-or-discard helpers `validate_findings` / `parse_reviewer_output`, and `collect_reviewer_results` for N-reviewer fan-out)
- `crossfire_forge/reviewers/fake.py` (created — `FakeReviewer` with SHA-256–seeded deterministic findings and `non_compliant` modes for schema vs JSON discard metering)
- `tests/test_reviewers.py` (created — N-fake collection, discard metering, and deterministic output tests)

## checks_run

- `pytest tests/test_reviewers.py -v` — exit 0; 3 passed in 0.13s (Python 3.13.12, pytest 9.0.3)

## findings_summary

Implemented the reviewer provider boundary per FR-6: `Reviewer.review(prompt) -> ReviewResult` carries schema-validated findings plus a discard counter. `FakeReviewer` derives finding type and text from a fixed prompt digest so harness runs are reproducible. Non-compliant modes simulate invalid schema payloads (two discards) or invalid JSON (one discard) without repair. `collect_reviewer_results` aggregates N fake outputs while preserving only validated findings.

## unresolved_risks

- Live provider adapters and aggregator conservation (INV-6) are deferred to Phase 2.
- JSON discard path in `FakeReviewer` short-circuits before emitting raw output; real adapters will route model strings through `parse_reviewer_output`.
- AC-6 workflow warning annotation requires harness wiring not in Task 8 scope.

## approval_gates

- None required for this task.
