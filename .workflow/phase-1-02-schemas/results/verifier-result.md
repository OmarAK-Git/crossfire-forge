---
task_id: phase-1-02-schemas
verified: 2026-07-05T05:16:00Z
status: passed
score: 5/5 acceptance criteria verified
behavior_unverified: 0
overrides_applied: 0
---

# Phase 1 Task 2 — Schemas Verification Report

**Goal:** Core schemas and taxonomy with discriminated-union findings (three types), ledger, run identity; invalid payloads fail validation including uncited violations (NG7).

**Verified:** 2026-07-05T05:16:00Z  
**Status:** passed  
**Re-verification:** No — initial verification

## Goal Achievement

### Acceptance Criteria (Task Scope Only)

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Three finding types in discriminated union per spec §5 | ✓ VERIFIED | `FindingType` enum has exactly `assumption`, `violation`, `safety_warning` (`taxonomy.py`). `Finding` is `Annotated[Union[AssumptionFinding, ViolationFinding, SafetyWarningFinding], Field(discriminator="type")]` (`schemas.py:31-35`). Tests: `test_finding_types_are_exactly_three`, `test_discriminated_union_rejects_unknown_type`. |
| 2 | Violation requires `standards_ref`; uncited fails validation (NG7) | ✓ VERIFIED | `ViolationFinding.standards_ref: str = Field(min_length=1)` (`schemas.py:25`). Missing field fails via discriminated union (`test_violation_without_standards_ref_fails_ng7`); empty string fails via `min_length=1` (`test_violation_with_empty_standards_ref_fails_ng7`). |
| 3 | Ledger and run-identity models validate valid/invalid payloads | ✓ VERIFIED | `RunIdentity`, `CorpusHash`, `Ledger` in `schemas.py:38-52` with NFR-4 fields (epic_hash, corpus_hashes, model_roster, tool_version). Valid: `test_run_identity_validates`, `test_ledger_validates`. Invalid: `test_run_identity_rejects_empty_epic_hash`, `test_run_identity_rejects_empty_corpus`, `test_ledger_rejects_invalid_finding`. |
| 4 | Tests demonstrate invalid payloads fail | ✓ VERIFIED | 14 tests; 7 assert `ValidationError` on invalid payloads (NG7, missing alternative, unknown type, empty identity fields, negative agreement_count, invalid finding in ledger). |
| 5 | Verifier checks Task 2 only, not full Phase 1 | ✓ VERIFIED | Scope limited to `schemas.py`, `taxonomy.py`, `test_schemas.py`. No hashing, safety scanner, reviewers, or CLI review command implemented (plan constraint honored). |

**Score:** 5/5 acceptance criteria verified (0 present, behavior-unverified)

### Spec §5 Field Alignment

| Field | Spec §5 | Implementation | Status |
| --- | --- | --- | --- |
| `type` | discriminator | `Literal[FindingType.*]` per subclass + union discriminator | ✓ |
| `statement` | required | `FindingBase.statement` min_length=1 | ✓ |
| `evidence` | required | `FindingBase.evidence` min_length=1 | ✓ |
| `alternative` | assumptions only | `AssumptionFinding.alternative` min_length=1 | ✓ |
| `blast_radius` | required | `FindingBase.blast_radius: BlastRadius` (BR-1/2/3) | ✓ |
| `standards_ref` | violations only | `ViolationFinding.standards_ref` min_length=1 | ✓ |
| `reviewer_votes` | required | `FindingBase.reviewer_votes: list[str]` | ✓ |
| `agreement_count` | required | `FindingBase.agreement_count` ge=0 | ✓ |

No `risk` or `severity` fields (spec design decisions honored).

### Required Artifacts

| Artifact | Expected | Exists | Substantive | Wired | Status |
| --- | --- | --- | --- | --- | --- |
| `crossfire_forge/taxonomy.py` | FindingType + BlastRadius enums | ✓ | ✓ | imported by schemas + tests | ✓ VERIFIED |
| `crossfire_forge/schemas.py` | Finding union, RunIdentity, Ledger | ✓ | ✓ | imported by tests | ✓ VERIFIED |
| `tests/test_schemas.py` | Valid/invalid payload coverage | ✓ | ✓ | exercises all models | ✓ VERIFIED |

### Key Link Verification

| From | To | Via | Status |
| --- | --- | --- | --- |
| `schemas.py` | `taxonomy.py` | `from crossfire_forge.taxonomy import BlastRadius, FindingType` | ✓ WIRED |
| `test_schemas.py` | `schemas.py` | direct imports + `TypeAdapter(Finding)` | ✓ WIRED |
| `Ledger.findings` | `Finding` union | `list[Finding]` field type | ✓ WIRED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| All schema tests pass | `python -m pytest tests/test_schemas.py -v` | 14 passed in 0.13s (exit 0) | ✓ PASS |
| NG7 uncited violation rejected | `test_violation_without_standards_ref_fails_ng7` (via pytest) | ValidationError with `standards_ref` in message | ✓ PASS |
| Discriminated union rejects unknown type | `test_discriminated_union_rejects_unknown_type` (via pytest) | ValidationError on `type: "risk"` | ✓ PASS |

### Anti-Patterns Found

None in changed files. No TBD/FIXME/XXX/TODO/PLACEHOLDER markers in `schemas.py`, `taxonomy.py`, or `test_schemas.py`.

### Out-of-Scope Check (Plan Constraints)

| Constraint | Status |
| --- | --- |
| No hashing implementation | ✓ — only hash *fields* on models, no hash computation |
| No safety scanner | ✓ — not present |
| No reviewers | ✓ — not present |
| No CLI review command | ✓ — not present |

### Informational Notes (Not Gaps)

- `reviewer_votes` accepts an empty list; spec does not require min_length on the list. Aggregation invariants may tighten in later phases (noted by implementer).
- `standards_ref` is a non-empty string citation; structured corpus-path validation deferred to later tasks (appropriate for Task 2 scope).

## Verdict

All Task 2 acceptance criteria are met in the codebase with behavioral test evidence. Phase 1 Task 2 goal achieved. Ready to proceed.

---

_Verified: 2026-07-05T05:16:00Z_  
_Verifier: gsd-verifier (fresh context)_
