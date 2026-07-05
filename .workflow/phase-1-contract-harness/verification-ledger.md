# Verification Ledger — phase-1-contract-harness

| ID | Requirement | Check | Command or Evidence | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VERIFY-P1-001 | Phase 1 exit | pytest | `pytest` | all pass | — | pending |
| VERIFY-AC-5 | FR-2 | secret abort | `pytest -k secret` | abort, no leakage | — | pending |
| VERIFY-P1-002 | TASK-001 | CLI | `crossfire-forge --help` | exit 0 | — | pending |
| VERIFY-P1-003 | Two-surface | Gatekeeper TASK-009 | review record | PASS | — | pending |
