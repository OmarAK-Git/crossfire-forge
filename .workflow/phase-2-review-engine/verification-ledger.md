# Verification Ledger — phase-2-review-engine

| ID | Requirement | Check | Command or Evidence | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VERIFY-AC-1 | AC-1 | pass-K-of-N | `pytest tests/test_harness.py -k ac1`; `evaluate_ac1` | 4-of-5 BR-3 RBAC assumption | Evaluators + unit tests pass; `ledger-441.md` BR-2 (fake pipeline); live 4-of-5 deferred (`LIVE_MODEL_APPROVAL_REQUIRED`) | pass (deferral) |
| VERIFY-AC-2 | AC-2 | complete epic | `pytest tests/test_harness.py -k ac2`; harness | no findings above BR-1 | Evaluators + unit tests pass; fake pipeline on `epic_complete.md` emits BR-2; live 4-of-5 deferred | pass (deferral) |
| VERIFY-AC-3 | AC-3 | injection fixture | `pytest tests/test_harness.py -k ac3` | safety_warning, no obey | Evaluator unit tests pass; fake E2E on `epic_injection.md` yields violation not warning; live 5-of-5 deferred | pass (deferral) |
| VERIFY-AC-4 | AC-4 | identity skip | `pytest tests/test_harness.py -k ac4` | no-op rerun | `test_ac4_identity_noop_rerun` pass (2026-07-05, phase-2-exit-gate) | pass |
| VERIFY-AC-5 | AC-5 | secret abort | `pytest -k secret -q` | abort, no leakage | 8 passed, 109 deselected (2026-07-05, phase-2-exit-gate); Phase 1 carry-forward re-confirmed | pass |
| VERIFY-AC-6 | AC-6 | discard metering | `pytest tests/test_harness.py -k ac6`; `tests/test_reviewers.py` | workflow warning / discard_count > 0 | `test_ac6_evaluator_detects_discard_metering` + reviewer discard tests pass (2026-07-05) | pass |
| VERIFY-P2-001 | G4 | ledger-441 | `Test-Path artifacts/ledger-441.md` | sanitized pipeline output | True; FR-8 markdown + machine-readers marker; fake-reviewer roster; RBAC text in alternative (BR-2 demo) | pass |
| VERIFY-P2-002 | Two-surface | Gatekeeper | `.workflow/phase-2-review-engine/gatekeeper-review.md` | PASS | PASS (deferrals documented) | passed |
