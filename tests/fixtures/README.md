# Crossfire Forge — default review corpus (pinned)

This file is the v0.1 default authoritative corpus per spec FR-1.

## Security posture

Spec-review is advisory-only (NG3). The tool never modifies Epic bodies, applies labels, or touches factory code.

## Corpus identity

Path: `README.md`
Purpose: Pin the default single-file corpus for deterministic run identity (NFR-4).

## Fixture epics

Test epics live alongside this README under `tests/fixtures/`:

- `epic_441.md` — minimal Epic #441 stand-in (zero structured fields)
- `epic_complete.md` — all FR-3 fields populated with valid values
- `epic_injection.md` — embedded instruction attempt (AC-3)
- `epic_placeholder.md` — placeholder-valued structured fields (FR-4 seeds)
- `epic_secret.md` — planted secret for AC-5 scanner tests
