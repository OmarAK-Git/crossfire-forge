# Gatekeeper Review — Phase 1 Tasks 1–8 (Contract Harness)

**Reviewed:** 2026-07-05T05:30:00Z  
**Reviewer:** Independent gatekeeper (phase-1-09-gatekeeper)  
**Verdict:** **PASS**

## Scope

Independent review of Phase 1 Tasks 1–8 implementation surface against `docs/spec-v0.4.md` §§5–8. Out of scope: Phase 1 exit gate (VERIFY-P1-001), Layer 0 full parser (TASK-015), aggregator/renderer/Action mode (Phase 2+).

| Task | Module / artifact | Spec touchpoints |
| --- | --- | --- |
| TASK-001 | `pyproject.toml`, `crossfire_forge/__init__.py`, `cli.py` | Skeleton; CLI entry |
| TASK-002 | `schemas.py`, `taxonomy.py` | §5 finding taxonomy, NG7 |
| TASK-003 | `hashing.py` | NFR-4 run identity |
| TASK-004 | `tests/fixtures/*` | FR-1 corpus pin, AC fixtures |
| TASK-005 | `safety.py` | FR-2, AC-5, R-4 |
| TASK-006 | `input_loader.py`, CLI `hashes` | FR-1 |
| TASK-007 | `prompts.py` | FR-5 (contract), R-1, AC-3 groundwork |
| TASK-008 | `reviewers/base.py`, `reviewers/fake.py` | FR-6 (schema-or-discard, metering) |

## Verification Method

1. Read all `crossfire_forge/` modules and Phase 1 `tests/test_*.py` files.
2. Map each module to spec §§5–8 requirements within Tasks 1–8 boundaries per `docs/implementation-plan-v0.4.md`.
3. Run `python -m pytest tests/ -q` — **59 passed** (2026-07-05).
4. Confirm `python -m crossfire_forge.cli --help` exits 0 (VERIFY-P1-002).

## Spec §5 — Finding Taxonomy

| Requirement | Status | Evidence |
| --- | --- | --- |
| Exactly three types: `assumption`, `violation`, `safety_warning` | ✓ | `taxonomy.FindingType`; `test_finding_types_are_exactly_three` |
| No `risk` type | ✓ | `test_discriminated_union_rejects_unknown_type`; fake invalid payload includes `"risk"` |
| No `severity` field | ✓ | Schemas omit severity; ranking deferred to renderer (Phase 2) |
| Assumption requires `alternative` | ✓ | `AssumptionFinding`; `test_assumption_without_alternative_fails` |
| Violation requires `standards_ref` (NG7) | ✓ | `ViolationFinding`; NG7 failure tests |
| Common fields: `statement`, `evidence`, `blast_radius`, `reviewer_votes`, `agreement_count` | ✓ | `FindingBase` with validation |
| Blast radius BR-1/BR-2/BR-3 | ✓ | `BlastRadius` enum matches §10 labels |
| Ledger + run identity models | ✓ | `Ledger`, `RunIdentity`, `CorpusHash` |

## Spec §6 — Functional Requirements (Phase 1 subset)

| Requirement | Task | Status | Notes |
| --- | --- | --- | --- |
| FR-1 Inputs (Epic + ordered corpus) | 006 | ✓ | `load_inputs`, default `README.md` corpus, pinned hashes |
| FR-2 Pre-prompt secret scanner | 005 | ✓ | `detect-secrets`-class scan; generic abort; no leakage (AC-5) |
| FR-3 Layer 0 parse | — | Deferred | TASK-015 (Phase 2); fixtures prepared |
| FR-4 Seeds | — | Deferred | TASK-015; prompt accepts seed strings |
| FR-5 Reviewer fan-out (contract) | 007–008 | Partial ✓ | Delimited data, review-not-obey, no tools; live fan-out in Phase 2 |
| FR-6 Schema-or-discard, metered | 008 | Partial ✓ | `validate_findings`, `parse_reviewer_output`, `discard_count`; workflow annotation deferred |
| FR-7–FR-12 | — | Out of scope | Phase 2–3 |

**FR-2 detail:** `scan_pre_prompt` scans epic and corpus entries; raises `SafetyAbort` with generic message; logger and exception surfaces do not reproduce planted secret (`test_epic_secret_no_leakage_in_message_logs_or_stderr`).

**FR-5 / R-1 detail:** System instructions fixed across clean and injection epics; injection phrases confined to delimited user blocks; schema instructions enumerate three finding types only.

**FR-6 detail:** Invalid JSON → 1 discard; invalid schema items discarded per-item without repair; `collect_reviewer_results` sums discards across N fakes.

## Spec §7 — Non-Functional Requirements (Phase 1 subset)

| Requirement | Status | Notes |
| --- | --- | --- |
| NFR-4 Run identity | ✓ | `(epic_hash, corpus_hashes, model_roster, tool_version)` deterministic via SHA-256 |
| NFR-1, NFR-2 (full), NFR-3, NFR-5 | Deferred | Action/ledger pipeline not built |

## Spec §8 — Invariants (groundwork only)

| Invariant | Phase 1 status |
| --- | --- |
| INV-1 Never edits Epic | ✓ No edit paths in harness |
| INV-2 Never human-blocking | ✓ Advisory-only modules |
| INV-3 Unsanitized model text | Deferred — sanitizer TASK-013 |
| INV-4 No label application | ✓ No label code |
| INV-5 One comment per Epic | Deferred — Phase 3 |
| INV-6 Conservation | Deferred — aggregator TASK-011 |
| INV-7 No raw persistence | Deferred — `--debug-raw-envelopes` TASK-014 |

## Task Acceptance Checklist

| Task | Done criterion | Gatekeeper |
| --- | --- | --- |
| 001 Skeleton | pytest + `--help` | ✓ |
| 002 Schemas | NG7 structural enforcement | ✓ |
| 003 Hashing | Deterministic identity | ✓ |
| 004 Fixtures | Five epics + README, stable hashes | ✓ |
| 005 Safety | AC-5 abort, no leakage | ✓ |
| 006 Loader | Local load + CLI hashes | ✓ |
| 007 Prompts | Injection cannot alter system | ✓ |
| 008 Fake reviewer | N fakes, schema-valid only, discards metered | ✓ |

## Minor Notes (non-blocking)

1. **Layer 0 (FR-3/FR-4)** — Not implemented in Tasks 1–8; correctly scheduled as TASK-015. Fixtures (`epic_placeholder.md`, `epic_complete.md`) are ready.
2. **Corpus secret scan** — `scan_pre_prompt` scans corpus content (FR-2), but tests cover epic secret only; add corpus-path test in a later task.
3. **FR-6 workflow annotation** — Discard metering is in-process only; GitHub workflow warning (AC-6 full) awaits Phase 2 orchestration.
4. **VERIFY-P1-001** — Phase 1 exit pytest row remains orchestrator-owned; this review independently confirms 59/59 green on 2026-07-05.
5. **Default fixtures directory** — CLI defaults `--fixtures-dir` to `tests/fixtures/`; appropriate for local harness; production corpus path is a Phase 2 concern.

## Verdict Rationale

**PASS** — Tasks 1–8 deliver the contract-first local harness promised in Phase 1: discriminated-union schemas with NG7 enforcement, deterministic run identity, pinned fixtures, FR-2 secret abort without leakage, FR-1 input loading, FR-5/R-1 prompt isolation, and FR-6 schema-or-discard with discard metering via fake reviewers. Deferred items (Layer 0, aggregation, rendering, Action mode, full AC-1–AC-4/AC-6–AC-8) are explicitly out of Tasks 1–8 scope per the implementation plan. No blocking defects found on the reviewed surface.

---

_Independent gatekeeper review — phase-1-09-gatekeeper_
