# Verification Ledger — phase-0-evidence-audit

| ID | Requirement | Check | Command or Evidence | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VERIFY-P0-001 | Phase 0 exit | baseline.json | file present + valid JSON | committed | present, valid JSON (fix_commits n=255, time_to_merge n=170); `git status` → `??` uncommitted | fail |
| VERIFY-P0-002 | Phase 0 exit | Stall line | spec §2 update or memo | CONFIRMED or DROPPED | CONFIRMED in spec §2; cited `baseline.json` stall_story_evidence + packet 01-gh-baseline | pass |
| VERIFY-P0-003 | Phase 0 exit | Path filters | workflow YAML inspection | recorded | YES — both sandbox-validation-kcc.yml (lines 8–11) and sandbox-validation-tf.yml (lines 8–10) use `on.push.paths` on main only; no PR trigger; evidence in packets/02-path-filters.md | pass |
| VERIFY-P0-004 | Phase 0 exit | §13 reuse map | memory-bank/traceability.md | all rows resolved | 10 rows in `## Section 13 reuse map (Phase 0 resolved)` — 8 LIFT, 1 Process reuse, 1 BUILD; evidence in packets/03-separability.md + packets/04-reuse-map.md | pass |
| VERIFY-P0-005 | Two-surface | Gatekeeper | independent review record | PASS | `.workflow/phase-0-evidence-audit/gatekeeper-review.md` — independent gatekeeper review **PASS** (2026-07-05); PR counts/distributions/fix_commits formula/PR482 stall story verified against pr-raw.jsonl + pr-details.json | pass |
