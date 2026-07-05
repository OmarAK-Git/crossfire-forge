# Design Decisions

Distilled from `docs/spec-v0.4.md`. Full records use `docs/decisions/DEC-NNN-<name>.md` when implementation choices branch; stubs live here for quick context.

## DEC-001 — No `risk` finding type

**Problem:** Unbounded "concerns" category lets reviewers pad clean Epics and pass AC-2 via side door.

**Decision:** Exactly three finding types: `assumption`, `violation`, `safety_warning`. Any concern must be an assumption with stated alternative and blast radius.

**Source:** spec §5

## DEC-002 — No `severity` field

**Problem:** Severity incoherent on assumptions; redundant on other types; second score invites arbitrary fill.

**Decision:** Single ranking dimension — blast radius — within fixed section order (safety warnings → violations → assumptions).

**Source:** spec §5

## DEC-003 — Schema-or-discard, metered

**Problem:** Repairing invalid model output hides model health signals.

**Decision:** Non-validating reviewer output discarded, never repaired; discards metered per model (FR-6, AC-6).

**Source:** spec §6 FR-6

## DEC-004 — Conservation-bound aggregation (INV-6)

**Problem:** Findings can vanish silently during merge.

**Decision:** Every input finding accounted as merged, rendered, collapsed, or discarded-with-reason.

**Source:** spec §8 INV-6, FR-7

## DEC-005 — CLI-first, fakes-first build order

**Problem:** GitHub plumbing before engine credibility wastes maintainer attention.

**Decision:** Schemas and safety first; fake-reviewer E2E before live models; Action only after demo + D-2.

**Source:** implementation plan § Delivery strategy, § Build order

## DEC-006 — Fail-open with compensated control

**Problem:** Reviewer failure must not block factory.

**Decision:** NFR-1 fail-open; FR-12 weekly self-test is compensating control for silent breakage.

**Source:** spec §7 NFR-1, FR-12
